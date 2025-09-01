# ingestor/rag_adapter.py
import sys
from typing import List, Tuple
from operator import itemgetter

from langchain_core.output_parsers import StrOutputParser
from langchain_community.vectorstores import FAISS
from utils.model_loader import ModelLoader
from exception.custom_exception import DocumentPortalException
from logger.custom_logger import CustomLogger


class SimpleRAG:
    """
    Minimal conversational RAG wrapper for our assignment.
    we are using FAISS retriever + LLM from ModelLoader.
    """

    def __init__(self, retriever):
        try:
            self.log = CustomLogger.get_logger(__name__)
            self.retriever = retriever
            self.llm = ModelLoader().load_llm()
            self._build_chain()
            self.log.info("SimpleRAG initialized")
        except Exception as e:
            self.log.error("Failed to init SimpleRAG", error=str(e))
            raise DocumentPortalException("Initialization error in SimpleRAG", sys) from e

    def _build_chain(self):
        """LCEL pipeline: retriever -> LLM -> text output"""
        try:
            def format_docs(docs):
                return "\n\n".join(d.page_content for d in docs)

            self.chain = (
                {
                    "context": self.retriever | format_docs,
                    "input": itemgetter("input"),
                }
                | self.llm
                | StrOutputParser()
            )
            self.log.info("LCEL chain built")
        except Exception as e:
            self.log.error("Error building LCEL chain", error=str(e))
            raise DocumentPortalException("Chain build error", sys) from e

    def invoke(self, question: str) -> str:
        """Answer a user query."""
        try:
            result = self.chain.invoke({"input": question})
            self.log.info("Chain invoked successfully")
            return result
        except Exception as e:
            self.log.error("Error invoking SimpleRAG", error=str(e))
            raise DocumentPortalException("Invoke error in SimpleRAG", sys) from e
