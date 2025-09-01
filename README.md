Universal Ingestor → Ingests PDFs, Word, Excel, PPTs, Markdown, CSVs, and SQL data.

Table & Image Extraction → Extracts structured tables and embedded images for analysis.

RAG Pipeline → Uses FAISS vector store + LLM for contextual Q&A.

Evaluation Matrix → Integrated with DeepEval for relevancy, faithfulness, precision, and recall.

Caching → Uses LangChain in-memory cache to speed up repeated queries.

Testing → >10 automated test cases, validated pre- and post-commit.

UI → Login screen + document upload portal.

universal_doc_rag/
│── ingestor/              # Universal ingestors (docs, tables, images, SQL, etc.)
│── eval/                  # Evaluation adapters + DeepEval integration
│── tests/                 # Unit tests & pre-commit validation
│── utils/                 # Config loader, model loader, helpers
│── logger/                # Custom structured logging
│── ui/                    # Login screen & document portal UI
│── config/                # Config YAML files
│── .env.example           # Example environment variables (no secrets!)
│── requirements.txt       # Python dependencies
│── README.md              # Project documentation



#CLONING
git clone https://github.com/ratulsur/universal_doc_rag.git
cd universal_doc_rag

python3 -m venv myenv
source myenv/bin/activate  # macOS/Linux
myenv\Scripts\activate     # Windows



