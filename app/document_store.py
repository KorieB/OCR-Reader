from typing import Dict, List, Optional
from uuid import uuid4
from datetime import datetime


class DocumentStore:
    """In-memory storage for uploaded documents."""

    def __init__(self) -> None:
        self._docs: Dict[str, Dict[str, str]] = {}

    def add_document(self, text: str, filename: str, file_type: str = "text", image_data: Optional[bytes] = None, content_type: Optional[str] = None) -> str:
        doc_id = str(uuid4())
        self._docs[doc_id] = {
            "filename": filename, 
            "text": text,
            "file_type": file_type,
            "uploaded_at": datetime.now().isoformat(),
            "image_data": image_data,
            "content_type": content_type
        }
        return doc_id

    def list_documents(self) -> List[Dict[str, str]]:
        return [
            {
                "id": doc_id, 
                "filename": info["filename"],
                "file_type": info.get("file_type", "text"),
                "uploaded_at": info.get("uploaded_at", "")
            }
            for doc_id, info in self._docs.items()
        ]

    def get_text(self, doc_id: str) -> str:
        if doc_id not in self._docs:
            raise KeyError(doc_id)
        return self._docs[doc_id]["text"]
    
    def get_document(self, doc_id: str) -> Dict[str, str]:
        if doc_id not in self._docs:
            raise KeyError(doc_id)
        return self._docs[doc_id]

    def get_multiple_texts(self, doc_ids: List[str]) -> Dict[str, str]:
        """Get text from multiple documents for cross-checking."""
        result = {}
        for doc_id in doc_ids:
            if doc_id in self._docs:
                result[doc_id] = self._docs[doc_id]["text"]
        return result

    def delete_document(self, doc_id: str) -> bool:
        """Delete a document by ID."""
        if doc_id in self._docs:
            del self._docs[doc_id]
            return True
        return False
