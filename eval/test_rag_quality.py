# tests/eval/test_rag_quality.py
import os
from deepeval import evaluate
from deepeval.test_case import LLMTestCase
from deepeval.metrics import (
    AnswerRelevancyMetric,
    FaithfulnessMetric,
    ContextualPrecisionMetric,
    ContextualRecallMetric,
)

from utils.config_loader import load_config
from utils.model_loader import ModelLoader
from langchain_community.vectorstores import FAISS
from eval.rag_adapter import SimpleRAG  

FAISS_INDEX_DIR = "faiss_index"

def _build_rag() -> SimpleRAG:
    config = load_config()
    ml = ModelLoader(config)

    embeddings = ml.load_embeddings()
    vs = FAISS.load_local(
        folder_path=FAISS_INDEX_DIR,
        embeddings=embeddings,
        allow_dangerous_deserialization=True,
    )
    retriever = vs.as_retriever(search_type="similarity", search_kwargs={"k": 5})
    return SimpleRAG(retriever=retriever)

# --- local helper to get (answer, contexts) ---
def _answer_with_context(rag: SimpleRAG, question: str):
    docs = rag.retriever.get_relevant_documents(question)
    contexts = [d.page_content for d in docs]
    answer = rag.ask(question)
    return answer, contexts

def test_rag_quality_basic():
    rag = _build_rag()

    cases = [
        {
            "question": "What is the main topic of the document?",
            "expected": "The document discusses computing topics (Unix systems and AI).",
        },
        {
            "question": "What are applications of quantum computing in NLP?",
            "expected": "Information retrieval, question answering, and text classification.",
        },
    ]

    metrics = [
        AnswerRelevancyMetric(threshold=0.6),
        FaithfulnessMetric(threshold=0.6),
        ContextualPrecisionMetric(threshold=0.6),
        ContextualRecallMetric(threshold=0.6),
    ]

    test_cases = []
    for c in cases:
        answer, contexts = _answer_with_context(rag, c["question"])
        test_cases.append(
            LLMTestCase(
                input=c["question"],
                actual_output=answer,
                expected_output=c["expected"],
                context=contexts,
            )
        )

    evaluate(test_cases, metrics=metrics)
