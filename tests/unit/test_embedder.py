from app.ingestion.embedder import (
    generate_embedding,
    generate_embeddings,
)


def test_generate_embedding():
    text = "def add(a, b): return a + b"

    embedding = generate_embedding(text)

    assert isinstance(embedding, list)
    assert len(embedding) == 384


def test_generate_embeddings():
    texts = [
        "How do I connect PostgreSQL?",
        "How do I reverse a string?",
        "What is FastAPI?",
    ]

    embeddings = generate_embeddings(texts)

    assert len(embeddings) == 3

    for embedding in embeddings:
        assert isinstance(embedding, list)
        assert len(embedding) == 384