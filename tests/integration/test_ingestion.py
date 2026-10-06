from app.core.db import SessionLocal
from app.models.code_chunk import CodeChunk
from app.ingestion.chunker import process_repository
from app.ingestion.embedder import generate_embeddings


def test_ingestion_pipeline():
    # Extract chunks
    chunks = process_repository("app")

    assert len(chunks) > 0

    # Generate embeddings
    texts = [chunk["content"] for chunk in chunks]
    embeddings = generate_embeddings(texts)

    assert len(embeddings) == len(chunks)

    for embedding in embeddings:
        assert len(embedding) == 384

    # Store in database
    db = SessionLocal()

    try:
        db.query(CodeChunk).delete()

        for chunk, embedding in zip(chunks, embeddings):
            db_chunk = CodeChunk(
                file_path=chunk["file_path"],
                content=chunk["content"],
                embedding=embedding,
            )

            db.add(db_chunk)

        db.commit()

        # Verify database
        count = db.query(CodeChunk).count()

        assert count == len(chunks)

        stored_chunks = db.query(CodeChunk).all()

        for chunk in stored_chunks:
            assert chunk.file_path
            assert chunk.content
            assert len(chunk.embedding) == 384

    finally:
        db.close()