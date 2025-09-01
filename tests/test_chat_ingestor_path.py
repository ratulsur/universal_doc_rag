# tests/test_chat_ingestor_paths.py
from ingestor.common_ingestor import ChatIngestor

def test_chat_ingestor_session_dirs(tmp_session):
    ci = ChatIngestor(
        temp_base=str(tmp_session["data_dir"].parent),
        faiss_base=str(tmp_session["faiss_dir"].parent),
        use_session_dirs=True,
        session_id=tmp_session["session_id"],
    )
    assert ci.temp_dir.name == tmp_session["session_id"]
    assert ci.faiss_dir.name == tmp_session["session_id"]
