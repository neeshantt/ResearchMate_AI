
import sqlite3
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "researchmate.db"

DATA_DIR.mkdir(parents=True, exist_ok=True)


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                document_id TEXT PRIMARY KEY,
                filename TEXT NOT NULL,
                file_path TEXT NOT NULL,
                index_path TEXT NOT NULL,
                summary TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                chunks TEXT DEFAULT '[]'
            )
        """)

        columns = [
            row["name"]
            for row in conn.execute("PRAGMA table_info(documents)")
        ]

        if "chunks" not in columns:
            conn.execute(
                "ALTER TABLE documents ADD COLUMN chunks TEXT DEFAULT '[]'"
            )


def save_document(document_id, filename, file_path,
                  index_path, summary=None, chunks=None):

    with get_connection() as conn:
        conn.execute("""
            INSERT OR REPLACE INTO documents
            (document_id, filename, file_path, index_path, summary, chunks)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            document_id,
            filename,
            file_path,
            index_path,
            summary,
            json.dumps(chunks or [])
        ))


def get_document(document_id):
    with get_connection() as conn:
        document = conn.execute(
            "SELECT * FROM documents WHERE document_id = ?",
            (document_id,)
        ).fetchone()

    if not document:
        return None

    result = dict(document)
    result["chunks"] = json.loads(result["chunks"] or "[]")
    return result


def get_all_documents():
    with get_connection() as conn:
        documents = conn.execute(
            "SELECT * FROM documents ORDER BY created_at DESC"
        ).fetchall()

    return [dict(doc) for doc in documents]


def delete_document(document_id):
    with get_connection() as conn:
        cursor = conn.execute(
            "DELETE FROM documents WHERE document_id = ?",
            (document_id,)
        )
        return cursor.rowcount > 0


if __name__ == "__main__":
    initialize_database()
    print("ResearchMate database initialized successfully!")
