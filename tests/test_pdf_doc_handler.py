# tests/test_doc_handler_pdf.py
from pathlib import Path
from ingestor.common_ingestor import DocHandler

def test_doc_handler_save_and_read(tmp_path, make_pdf):
    dh = DocHandler(data_dir=str(tmp_path))
    pdf_path = make_pdf(Path(dh.session_path) / "sample.pdf", "Hello World")
    text = dh.read_pdf(str(pdf_path))
    assert "Hello World" in text
