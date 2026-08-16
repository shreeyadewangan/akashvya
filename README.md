# Air-Gapped Predictive NOC Copilot for Secure MPLS Operations

An offline Network Operations Center (NOC) Copilot that predicts network degradation before user impact, provides grounded explanations via local Large Language Models (LLMs), and retrieves corrective steps from offline runbooks.

---

## Project Structure

```text
mpls_copilot/
├── app.py                      # Main Streamlit Dashboard
├── requirements.txt            # Master dependencies
├── README.md                   # System documentation
├── phase1/
│   ├── data/
│   │   └── synthetic_telemetry.csv
│   ├── generate_telemetry.py
│   └── visualize_telemetry.py
├── phase2/
│   └── ml/
│       ├── models/             # Trained ML models (.joblib)
│       ├── predict.py          # Real-time inference
│       ├── preprocessing.py    # Metric preprocessors
│       ├── risk_engine.py      # Deterministic risk & TTI score
│       └── train.py            # Model training script
├── phase3/
│   ├── llm_copilot.py         # Ollama LLM integration
│   └── test_copilot.py
└── phase4/
    ├── knowledge/              # Markdown runbooks & topology
    │   ├── incidents/
    │   ├── runbooks/
    │   └── topology/
    ├── vector_db/              # Local ChromaDB embeddings
    ├── rag_engine.py           # Offline vector retrieval
    └── test_rag.py