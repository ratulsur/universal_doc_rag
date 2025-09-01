# tests/test_image_extractor_loads.py #
import importlib

def test_image_extractor_module_loads():
    m = importlib.import_module("ingestor.image_extractor")
    assert hasattr(m, "__file__")
