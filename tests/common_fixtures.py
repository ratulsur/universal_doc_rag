# tests/conftest.py
import os
import uuid
import json
import fitz  # PyMuPDF
import pytest
from pathlib import Path

@pytest.fixture
def tmp_session(tmp_path: Path):
    """Returns a fresh temp session dir structure (data + faiss)."""
    session_id = f"session_{uuid.uuid4().hex[:8]}"
    data = tmp_path / "data" / session_id
    faiss = tmp_path / "faiss_index" / session_id
    data.mkdir(parents=True, exist_ok=True)
    faiss.mkdir(parents=True, exist_ok=True)
    return {"session_id": session_id, "data_dir": data, "faiss_dir": faiss}

@pytest.fixture
def make_pdf():
    """Create a minimal PDF with given text and return path."""
    def _make_pdf(path: Path, text: str = "Hello PDF"):
        doc = fitz.open()
        page = doc.new_page()
        page.insert_text((72, 72), text)
        doc.save(str(path))
        doc.close()
        return path
    return _make_pdf

@pytest.fixture
def fake_llm(monkeypatch):
    """Monkeypatch ModelLoader.load_llm to a simple echo-like object."""
    class _Echo:
        def invoke(self, x):  # LCEL sometimes calls .invoke
            
            if isinstance(x, dict):
                return x.get("input") or x.get("context") or ""
            return x
        
        def __or__(self, other):  # for LCEL 
            return self
    from utils import model_loader as ml
    monkeypatch.setattr(ml.ModelLoader, "load_llm", lambda self: _Echo())
    return _Echo()

@pytest.fixture
def fake_embeddings(monkeypatch):
    """Monkeypatch ModelLoader.load_embeddings to a deterministic fake."""
    class _FakeEmb:
        def embed_query(self, text: str):
            return [float((sum(map(ord, text)) % 7) + i) for i in range(3)]
        def embed_documents(self, texts):
            return [self.embed_query(t) for t in texts]
    from utils import model_loader as ml
    monkeypatch.setattr(ml.ModelLoader, "load_embeddings", lambda self: _FakeEmb())
    return _FakeEmb()

@pytest.fixture(autouse=True)
def clean_env(monkeypatch):
    """Ensure env vars that can trip tests are present but harmless."""
    monkeypatch.setenv("GROQ_API_KEY", "dummy")
    monkeypatch.setenv("OPENAI_API_KEY", "dummy")
    monkeypatch.setenv("LANGCHAIN_API_KEY", "dummy")
    monkeypatch.setenv("HF_API", "dummy")
