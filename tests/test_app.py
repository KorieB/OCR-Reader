from fastapi.testclient import TestClient

from app.main import app, get_store, get_gemini_client
from app.document_store import DocumentStore


class FakeGeminiClient:
    def ask(self, text: str, question: str) -> str:
        assert text  # ensure document text passed
        assert question
        return "fake answer"


def setup_test_app():
    store = DocumentStore()
    app.dependency_overrides[get_store] = lambda: store
    app.dependency_overrides[get_gemini_client] = lambda: FakeGeminiClient()
    return TestClient(app)


def test_document_workflow():
    client = setup_test_app()
    # Upload a document
    response = client.post(
        "/documents",
        files={"file": ("test.txt", b"hello world", "text/plain")},
    )
    assert response.status_code == 200
    doc_id = response.json()["id"]

    # List documents
    response = client.get("/documents")
    assert response.status_code == 200
    docs = response.json()["documents"]
    assert len(docs) == 1
    assert docs[0]["id"] == doc_id

    # Ask question
    response = client.post(
        f"/documents/{doc_id}/question",
        json={"question": "What does the document say?"},
    )
    assert response.status_code == 200
    assert response.json()["answer"] == "fake answer"
