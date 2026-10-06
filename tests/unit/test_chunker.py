from app.ingestion.chunker import extract_chunks


def test_extract_function():
    code = b"""
def add(a, b):
    return a + b
"""

    chunks = extract_chunks(code)

    assert len(chunks) == 1
    assert chunks[0]["type"] == "function_definition"
    assert chunks[0]["name"] == "add"


def test_extract_class():
    code = b"""
class Calculator:

    def add(self, a, b):
        return a + b
"""

    chunks = extract_chunks(code)

    assert len(chunks) == 2

    assert chunks[0]["type"] == "class_definition"
    assert chunks[0]["name"] == "Calculator"

    assert chunks[1]["type"] == "function_definition"
    assert chunks[1]["name"] == "add"