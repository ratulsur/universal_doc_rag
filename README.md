# Universal Doc RAG

A retrieval-augmented generation system that ingests **any** common document format — PDF, Word,
Excel, PowerPoint, Markdown, CSV, and SQL data — and answers questions over it, with built-in
**RAG evaluation** (DeepEval), authentication, caching, and a test suite. Built to be a complete,
production-shaped RAG application rather than a notebook demo.

## What it does

Upload mixed-format documents through the portal; the universal ingestor parses them — including
**structured tables and embedded images** — chunks and embeds the content into a FAISS vector
store, and serves contextual Q&A through an LLM. Every answer can be scored on retrieval and
generation quality via an integrated evaluation matrix, so quality is measured, not assumed.

## Features

- **Universal ingestion** — PDF, Word, Excel, PowerPoint, Markdown, CSV, and SQL sources through
  one pipeline.
- **Table & image extraction** — pulls structured tables and embedded images out for analysis,
  not just raw text.
- **RAG pipeline** — FAISS vector store + LLM for grounded, contextual question answering.
- **Evaluation matrix** — integrated with **DeepEval** for relevancy, faithfulness, precision,
  and recall, so retrieval and answer quality are quantified.
- **Caching** — LangChain in-memory cache speeds up repeated queries.
- **Authentication & portal** — login screen plus a document-upload UI.
- **Production hygiene** — structured logging, a dedicated exception layer, a CI pipeline, and
  10+ automated tests validated pre- and post-commit.

## Architecture

```
Documents (PDF / Word / Excel / PPT / MD / CSV / SQL)
        │
        ▼
   Universal Ingestor        parse + table/image extraction   (ingestor/)
        │
        ▼
   Chunk + Embed → FAISS vector store
        │
        ▼
   Retrieval + LLM  ──►  contextual answer                    (+ in-memory cache)
        │
        ▼
   Evaluation (DeepEval)     relevancy · faithfulness · precision · recall   (evaluation/)
```

Cross-cutting modules keep it maintainable: `auth/` (login), `logger/` (structured logging),
`exception/` (custom error types), `tests/` (unit + pre-commit validation), `ci/` (pipeline),
and `utils/` (config + model loaders).

## Stack

Python · LangChain · FAISS · OpenAI · DeepEval · pytest

## Setup

```bash
git clone https://github.com/ratulsur/universal_doc_rag.git
cd universal_doc_rag

python3 -m venv myenv
source myenv/bin/activate        # macOS/Linux
# myenv\Scripts\activate         # Windows

pip install -r requirements.txt

# Create a .env with your credentials:
#   OPENAI_API_KEY=...
```

## Run

```bash
# Start the app — replace with your actual entry point:
[ENTRY COMMAND, e.g. streamlit run app.py  OR  uvicorn main:app --reload]
```

Then open the portal, log in, upload documents, and ask questions over them.

## Evaluation

Retrieval and generation quality are measured with **DeepEval** across four metrics — relevancy,
faithfulness, precision, and recall — so changes to chunking, retrieval, or prompts can be
compared quantitatively instead of by eyeballing answers.

## Testing

10+ automated test cases run as unit tests and as pre-/post-commit validation, covering the
ingestion and retrieval paths.

## Project structure

```
universal_doc_rag/
├── ingestor/     universal document ingestors (docs, tables, images, SQL)
├── evaluation/   DeepEval integration (relevancy, faithfulness, precision, recall)
├── auth/         login / authentication
├── logger/       structured logging
├── exception/    custom exception types
├── utils/        config + model loaders, helpers
├── tests/        unit tests & pre-commit validation
├── ci/           CI pipeline
├── docs/         documentation
├── requirements.txt
└── README.md
```

## Possible extensions

- Swap the in-memory cache for a persistent store (Redis) for multi-session use.
- Add hybrid retrieval (BM25 + dense) and re-ranking for higher precision.
- Containerize with Docker for one-command deployment.
