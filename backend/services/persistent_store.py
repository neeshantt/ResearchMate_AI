
import faiss
from pathlib import Path

# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# FAISS index storage directory
INDEX_DIR = BASE_DIR / "data" / "indexes"

INDEX_DIR.mkdir(parents=True, exist_ok=True)

def save_faiss_index(index, document_id):
    """
    Save a FAISS index permanently on disk.
    """

    index_path = INDEX_DIR / f"{document_id}.faiss"

    faiss.write_index(index, str(index_path))

    return str(index_path)

def load_faiss_index(index_path):
    """
    Load a previously saved FAISS index.
    """

    index_path = Path(index_path)

    if not index_path.exists():
        raise FileNotFoundError(
            f"FAISS index not found: {index_path}"
        )

    index = faiss.read_index(str(index_path))

    return index

def delete_faiss_index(index_path):
    """
    Delete a saved FAISS index.
    """

    index_path = Path(index_path)

    if index_path.exists():
        index_path.unlink()
        return True

    return False