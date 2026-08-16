import os
import glob
import requests
import chromadb
from chromadb.utils import embedding_functions

# Dynamic Base Directory Resolution (Anchored to phase4/)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KNOWLEDGE_BASE_DIR = os.path.join(BASE_DIR, "knowledge")
VECTOR_DB_DIR = os.path.join(BASE_DIR, "vector_db")

OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2"

# Local Embedding Function (Offline SentenceTransformers)
embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

def initialize_vector_db():
    """Reads local Markdown documents from phase4/knowledge and indexes into phase4/vector_db."""
    client = chromadb.PersistentClient(path=VECTOR_DB_DIR)
    
    collection = client.get_or_create_collection(
        name="noc_knowledge_base",
        embedding_function=embedding_func
    )

    if collection.count() > 0:
        return collection

    documents = []
    metadatas = []
    ids = []
    doc_id = 0

    filepaths = glob.glob(f"{KNOWLEDGE_BASE_DIR}/**/*.md", recursive=True)
    
    for filepath in filepaths:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        chunks = [c.strip() for c in content.split("\n\n") if len(c.strip()) > 30]
        doc_name = os.path.basename(filepath)

        for chunk in chunks:
            documents.append(chunk)
            metadatas.append({"source": doc_name, "filepath": filepath})
            ids.append(f"doc_chunk_{doc_id}")
            doc_id += 1

    if documents:
        collection.add(documents=documents, metadatas=metadatas, ids=ids)
        print(f"Indexed {len(documents)} document chunks into local Vector DB at {VECTOR_DB_DIR}.")

    return collection

def retrieve_relevant_context(query_text, top_k=2):
    """Queries phase4 ChromaDB collection using local vector similarity search."""
    collection = initialize_vector_db()
    results = collection.query(query_texts=[query_text], n_results=top_k)

    retrieved_chunks = []
    sources = set()

    if results and "documents" in results and len(results["documents"]) > 0:
        for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
            retrieved_chunks.append(doc)
            sources.add(meta["source"])

    return "\n---\n".join(retrieved_chunks), list(sources)

def generate_grounded_noc_report(ml_output, telemetry, topology_info):
    """Combines ML metrics + Phase 4 local vector search + local Ollama inference."""
    predicted_issue = ml_output.get("predicted_issue", "Network Anomaly")
    
    search_query = f"{predicted_issue} utilization {telemetry.get('utilization_pct')}% latency {telemetry.get('latency_ms')}ms drops bgp"
    retrieved_context, retrieved_sources = retrieve_relevant_context(search_query, top_k=2)

    system_prompt = """You are an air-gapped NOC Copilot for secure MPLS network operations.
Your job is to explain network failure predictions using ONLY the supplied telemetry and local internal runbooks.

STRICT ACCURACY RULES:
1. Ground your response STRICTLY on the provided telemetry facts and RETRIEVED INTERNAL DOCUMENTS.
2. If the retrieved internal documents do NOT contain sufficient steps for the issue, state: "Insufficient internal runbook data available for detailed step."
3. MUST explicitly cite document names (e.g., [RB-MPLS-001], [RB-BGP-002]) in the "Retrieved Sources" section.
4. STRICTLY DISTINGUISH between facts, predictions, and hypotheses:
   - [Observed Fact]: Metrics directly provided in input.
   - [ML Prediction]: Machine Learning model outputs.
   - [Hypothesis]: Root cause explanations.

Required Output Headers:
Predicted Issue: <Issue name>
Confidence: <Confidence percentage>
Risk: <Risk Score and Level>
Time-to-Impact: <Estimated timeframe>
Why: <Short explanation of elevated risk>
Evidence:
 - [Observed Fact] <Metric observation>
Probable Root Cause: [Hypothesis] <Logical cause>
Affected Scope: <Site | Device | Interface>
Recommended Actions: (Derived from retrieved runbooks)
 1. <Step from runbook>
Urgency: <CRITICAL | HIGH | MEDIUM | LOW>
Retrieved Sources: <List cited document source filenames>
"""

    user_prompt = f"""
NETWORK CONTEXT:
Site: {topology_info.get('site')} | Device: {topology_info.get('device')} | Interface: {topology_info.get('interface')}

OBSERVED TELEMETRY:
- Utilization: {telemetry.get('utilization_pct')}% | Latency: {telemetry.get('latency_ms')}ms | Jitter: {telemetry.get('jitter_ms')}ms
- Packet Loss: {telemetry.get('packet_loss_pct')}% | Errors: {telemetry.get('interface_errors')} | BGP Flaps: {telemetry.get('bgp_flaps')}

ML PREDICTION:
- Predicted Issue: {predicted_issue}
- Confidence: {ml_output.get('confidence')}
- Risk Score: {ml_output.get('risk_score')} ({ml_output.get('risk_level')})
- Time-to-Impact: {ml_output.get('time_to_impact')}

RETRIEVED INTERNAL RUNBOOKS & KNOWLEDGE CONTEXT:
{retrieved_context if retrieved_context else "No relevant runbooks found."}

Generate the grounded NOC Copilot report following system rules.
"""

    payload = {
        "model": MODEL_NAME,
        "system": system_prompt,
        "prompt": user_prompt,
        "stream": False,
        "options": {"temperature": 0.1}
    }

    try:
        response = requests.post(OLLAMA_API_URL, json=payload, timeout=60)
        response.raise_for_status()
        return response.json().get("response", "Error: Empty response."), retrieved_sources
    except Exception as e:
        return f"ERROR communicating with local LLM: {str(e)}", retrieved_sources