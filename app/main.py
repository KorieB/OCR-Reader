from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import io
from pypdf import PdfReader

# Support running both as a package (e.g. ``uvicorn app.main:app``) and as a
# standalone script (``python app/main.py``).  Relative imports work only when
# the module is part of a package, so fall back to absolute imports if needed.
try:  # pragma: no cover - trivial import glue
    from .document_store import DocumentStore
    from .gemini_client import GeminiClient
    from .image_processor import ImageProcessor
except ImportError:  # executed when running as ``python app/main.py``
    from document_store import DocumentStore
    from gemini_client import GeminiClient
    from image_processor import ImageProcessor

app = FastAPI(
    title="Enhanced OCR Reader API",
    description="Upload documents and images, ask questions, and cross-check multiple files",
    version="2.0.0"
)

# Add CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

_store = DocumentStore()
_image_processor = ImageProcessor()


@app.get("/", include_in_schema=False)
async def root() -> RedirectResponse:
    """Redirect the bare URL to the interactive API docs."""
    return RedirectResponse("/docs")


def get_store() -> DocumentStore:
    return _store


def get_gemini_client() -> GeminiClient:
    return GeminiClient()


def get_image_processor() -> ImageProcessor:
    return _image_processor


class QuestionRequest(BaseModel):
    question: str


class MultiDocumentQuestionRequest(BaseModel):
    question: str
    document_ids: List[str]


class ImageQuestionRequest(BaseModel):
    question: str


@app.post("/documents", summary="Upload Document or Image")
async def upload_document(
    file: UploadFile = File(...),
    store: DocumentStore = Depends(get_store),
    image_processor: ImageProcessor = Depends(get_image_processor),
):
    """Upload a PDF, text file, or image for analysis."""
    content = await file.read()
    
    if file.content_type == "application/pdf":
        try:
            reader = PdfReader(io.BytesIO(content))
            text = "\n".join(page.extract_text() or "" for page in reader.pages)
            doc_id = store.add_document(text, file.filename, "pdf")
        except Exception as exc:
            raise HTTPException(status_code=400, detail="Failed to process PDF") from exc
            
    elif file.content_type == "text/plain":
        text = content.decode("utf-8", errors="ignore")
        doc_id = store.add_document(text, file.filename, "text")
        
    elif image_processor.is_supported_image(file.content_type):
        # For images, store the raw image data and a placeholder text
        text = f"[Image: {file.filename}]"
        doc_id = store.add_document(text, file.filename, "image", content, file.content_type)
        
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type. Supported: PDF, TXT, JPEG, PNG, GIF, WebP")
    
    return {"id": doc_id, "filename": file.filename, "type": store.get_document(doc_id)["file_type"]}


@app.get("/documents", summary="List All Documents")
def list_documents(store: DocumentStore = Depends(get_store)):
    """Get a list of all uploaded documents."""
    return {"documents": store.list_documents()}


@app.delete("/documents/{doc_id}", summary="Delete Document")
def delete_document(
    doc_id: str,
    store: DocumentStore = Depends(get_store),
):
    """Delete a document by ID."""
    if store.delete_document(doc_id):
        return {"message": "Document deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Document not found")


@app.post("/documents/{doc_id}/question", summary="Ask Question About Single Document")
def ask_question(
    doc_id: str,
    request: QuestionRequest,
    store: DocumentStore = Depends(get_store),
    client: GeminiClient = Depends(get_gemini_client),
    image_processor: ImageProcessor = Depends(get_image_processor),
):
    """Ask a question about a specific document (text, PDF, or image)."""
    try:
        document = store.get_document(doc_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Document not found")
    
    if document["file_type"] == "image":
        # Handle image question
        image_data = image_processor.prepare_image_for_gemini(
            document["image_data"], 
            document["content_type"]
        )
        answer = client.ask_with_image(request.question, image_data)
    else:
        # Handle text/PDF question
        answer = client.ask(document["text"], request.question)
    
    return {"answer": answer, "document_id": doc_id, "filename": document["filename"]}


@app.post("/documents/cross-check", summary="Cross-Check Multiple Documents")
def cross_check_documents(
    request: MultiDocumentQuestionRequest,
    store: DocumentStore = Depends(get_store),
    client: GeminiClient = Depends(get_gemini_client),
):
    """Ask a question that compares and analyzes multiple documents."""
    if len(request.document_ids) < 2:
        raise HTTPException(status_code=400, detail="At least 2 documents required for cross-checking")
    
    if len(request.document_ids) > 5:
        raise HTTPException(status_code=400, detail="Maximum 5 documents allowed for cross-checking")
    
    # Get document texts
    documents = store.get_multiple_texts(request.document_ids)
    
    if len(documents) != len(request.document_ids):
        missing_docs = set(request.document_ids) - set(documents.keys())
        raise HTTPException(status_code=404, detail=f"Documents not found: {list(missing_docs)}")
    
    answer = client.ask_multiple_documents(documents, request.question)
    
    return {
        "answer": answer, 
        "document_ids": request.document_ids,
        "documents_analyzed": len(documents)
    }


@app.get("/health", summary="Health Check")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "version": "2.0.0"}
