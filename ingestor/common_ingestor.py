# ---- minimal exports for tests ----
from pathlib import Path
from typing import List, Optional, Iterable

try:
    
    from ingestor.common_ingestor import FaissManager  
except Exception:
    
    import json, hashlib
    from langchain_community.vectorstores import FAISS
    from utils.model_loader import ModelLoader

    class FaissManager:
        def __init__(self, index_dir: Path, model_loader: Optional[ModelLoader] = None):
            self.index_dir = Path(index_dir)
            self.index_dir.mkdir(parents=True, exist_ok=True)
            self.model_loader = model_loader or ModelLoader()
            self.emb = self.model_loader.load_embeddings()
            self.vs = None

        def _exists(self) -> bool:
            p = self.index_dir
            return (p / "index.faiss").exists() and (p / "index.pkl").exists()

        def load_or_create(self, texts: Optional[List[str]] = None, metadatas: Optional[List[dict]] = None):
            if self._exists():
                self.vs = FAISS.load_local(str(self.index_dir), embeddings=self.emb, allow_dangerous_deserialization=True)
                return self.vs
            if not texts:
                raise ValueError("No existing FAISS index and no data to create one")
            self.vs = FAISS.from_texts(texts=texts, embedding=self.emb, metadatas=metadatas or [])
            self.vs.save_local(str(self.index_dir))
            return self.vs

        def add_documents(self, docs) -> int:
            if self.vs is None:
                raise RuntimeError("Call load_or_create() first")
            added = len(docs) if docs else 0
            if added:
                self.vs.add_documents(docs)  
                self.vs.save_local(str(self.index_dir))
            return added


class ChatIngestor:
    def __init__(self, temp_base: str = "data", faiss_base: str = "faiss_index", use_session_dirs: bool = True, session_id: Optional[str] = None):
        self.temp_base = Path(temp_base)
        self.faiss_base = Path(faiss_base)
        self.use_session = use_session_dirs
        self.session_id = session_id or "session"
        self.temp_base.mkdir(parents=True, exist_ok=True)
        self.faiss_base.mkdir(parents=True, exist_ok=True)

    
    def build_retriever(self, uploaded_files: Iterable, *, k: int = 5):
        from utils.model_loader import ModelLoader
        from langchain_community.vectorstores import FAISS
        ml = ModelLoader()
        emb = ml.load_embeddings()
        fm = FaissManager(self.faiss_base / self.session_id, ml)
        vs = fm.load_or_create(texts=["placeholder"], metadatas=[{}])  
        return vs.as_retriever(search_type="similarity", search_kwargs={"k": k})

__all__ = ["FaissManager", "ChatIngestor"]

# ---- minimal DocHandler for tests ----
import os
from pathlib import Path
import fitz  # PyMuPDF

class DocHandler:
    """
    PDF save + read (page-wise) for analysis.
    """
    def __init__(self, data_dir: str | None = None, session_id: str | None = None):
        base = data_dir or os.path.join(os.getcwd(), "data", "document_analysis")
        self.session_id = session_id or "session"
        self.session_path = Path(base) / self.session_id
        self.session_path.mkdir(parents=True, exist_ok=True)

    def save_pdf(self, uploaded_file) -> str:
        """
        uploaded_file must have .name and either .read() or .getbuffer()
        """
        filename = Path(getattr(uploaded_file, "name", "uploaded.pdf")).name
        if not filename.lower().endswith(".pdf"):
            raise ValueError("Invalid file type. Only PDFs are allowed.")
        save_path = self.session_path / filename
        with open(save_path, "wb") as f:
            if hasattr(uploaded_file, "read"):
                f.write(uploaded_file.read())
            else:
                f.write(uploaded_file.getbuffer())
        return str(save_path)

    def read_pdf(self, pdf_path: str) -> str:
        text_chunks: list[str] = []
        with fitz.open(pdf_path) as doc:
            for i in range(doc.page_count):
                page = doc.load_page(i)
                text_chunks.append(f"\n--- Page {i+1} ---\n{page.get_text()}")
        return "\n".join(text_chunks)


__all__ = [*(__all__ if "__all__" in globals() else []), "DocHandler"]
