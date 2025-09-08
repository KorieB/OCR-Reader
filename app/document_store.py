from typing import Dict, List
from uuid import uuid4


class DocumentStore:
    """In-memory storage for uploaded documents."""

    def __init__(self) -> None:
        self._docs: Dict[str, Dict[str, str]] = {}

    def add_document(self, text: str, filename: str) -> str:
        doc_id = str(uuid4())
        self._docs[doc_id] = {"filename": filename, "text": text}
        return doc_id

    def list_documents(self) -> List[Dict[str, str]]:
        return [
            {"id": doc_id, "filename": info["filename"]}
            for doc_id, info in self._docs.items()
        ]

    def get_text(self, doc_id: str) -> str:
        if doc_id not in self._docs:
            raise KeyError(doc_id)
        return self._docs[doc_id]["text"]
