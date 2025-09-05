from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from pydantic import BaseModel
import io
from pypdf import PdfReader

from .document_store import DocumentStore
from .gemini_client import GeminiClient

app = FastAPI()
_store = DocumentStore()


def get_store() -> DocumentStore:
    return _store


def get_gemini_client() -> GeminiClient:
    return GeminiClient()


class QuestionRequest(BaseModel):
    question: str


@app.post("/documents")
async def upload_document(
    file: UploadFile = File(...),
    store: DocumentStore = Depends(get_store),
):
    if file.content_type not in {"application/pdf", "text/plain"}:
        raise HTTPException(status_code=400, detail="Unsupported file type")
    content = await file.read()
    if file.content_type == "application/pdf":
        try:
            reader = PdfReader(io.BytesIO(content))
            text = "\n".join(page.extract_text() or "" for page in reader.pages)
        except Exception as exc:
            raise HTTPException(status_code=400, detail="Failed to process PDF") from exc
    else:
        text = content.decode("utf-8", errors="ignore")
    doc_id = store.add_document(text, file.filename)
    return {"id": doc_id}


@app.get("/documents")
def list_documents(store: DocumentStore = Depends(get_store)):
    return {"documents": store.list_documents()}


@app.post("/documents/{doc_id}/question")
def ask_question(
    doc_id: str,
    request: QuestionRequest,
    store: DocumentStore = Depends(get_store),
    client: GeminiClient = Depends(get_gemini_client),
):
    try:
        text = store.get_text(doc_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Document not found")
    answer = client.ask(text, request.question)
    return {"answer": answer}
