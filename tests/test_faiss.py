# tests/test_faiss_manager_unit.py
from types import SimpleNamespace
from pathlib import Path
from langchain.schema import Document
from ingestor.common_ingestor import FaissManager

def test_faiss_manager_idempotent(tmp_path, fake_embeddings, monkeypatch):
    fm = FaissManager(tmp_path, model_loader=None)
    # inject fake embeddings directly
    fm.emb = fake_embeddings

    # fake vectorstore with counters
    added = []
    class _VS:
        def add_documents(self, docs): added.extend(docs)
        def save_local(self, *_args, **_kwargs): pass

    fm.vs = _VS()
    fm._meta = {"rows": {}}

    docs = [Document(page_content="A", metadata={"source": "f1"})]
    n1 = fm.add_documents(docs)
    n2 = fm.add_documents(docs)

    assert n1 == 1
    assert n2 == 0
    assert Path(tmp_path / "ingested_meta.json").exists()
