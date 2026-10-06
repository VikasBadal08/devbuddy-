from app.core.db import SessionLocal
from app.ingestion.chunker import process_repository
from app.ingestion.embedder import generate_embeddings
from app.models.code_chunk import CodeChunk


def ingest_repository(repo_path: str):
    print("Starting ingestion...")

    # 1. Extract code chunks
    chunks = process_repository(repo_path)

    print(f"Total chunks found: {len(chunks)}")

    if not chunks:
        print("No code chunks found.")
        return

    # 2. Generate embeddings
    texts = [chunk["content"] for chunk in chunks]

    embeddings = generate_embeddings(texts)

    print(f"Total embeddings generated: {len(embeddings)}")

    # 3. Attach embeddings
    for chunk, embedding in zip(chunks, embeddings):
        chunk["embedding"] = embedding

    # 4. Store in PostgreSQL
    db = SessionLocal()

    try:
        # Remove previous ingestion
        db.query(CodeChunk).delete()

        for chunk in chunks:
            db_chunk = CodeChunk(
                file_path=chunk["file_path"],
                content=chunk["content"],
                embedding=chunk["embedding"],
            )

            db.add(db_chunk)

        db.commit()

        print("Ingestion completed successfully!")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    ingest_repository("app")