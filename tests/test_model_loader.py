# tests/test_model_loader.py
import pytest
from utils.model_loader import ModelLoader

def test_model_loader_embeds_hf(monkeypatch):
    cfg = {
        "embedding_model": {"provider": "huggingface", "model_name": "any-model"},
        "llm": {"provider": "Groq", "model_name": "deepseek", "temperature": 0, "max_output_tokens": 64},
    }
    ml = ModelLoader(cfg)
    emb = ml.load_embeddings()
    assert hasattr(emb, "embed_query")

def test_model_loader_llm_groq_env_missing(monkeypatch):
    
    cfg = {"embedding_model": {"provider": "huggingface", "model_name": "m"},
           "llm": {"provider": "Groq", "model_name": "deepseek"}}
    ml = ModelLoader(cfg)
    llm = ml.load_llm()
    
    assert llm is not None

def test_model_loader_raises_on_unknown_provider():
    cfg = {"embedding_model": {"provider": "??", "model_name": "m"},
           "llm": {"provider": "Groq", "model_name": "deepseek"}}
    with pytest.raises(ValueError):
        ModelLoader(cfg).load_embeddings()
