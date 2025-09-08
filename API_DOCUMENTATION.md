# Enhanced OCR Reader API Documentation

## Overview
The Enhanced OCR Reader API allows you to upload documents (PDF, text files) and images, ask questions about their content using AI, and perform cross-checking analysis across multiple documents.

**Base URL:** `http://localhost:8000`
**API Version:** 2.0.0

## Authentication
This API uses environment variables for authentication:
- `GEMINI_API_KEY`: Your Google Gemini API key

## Endpoints

### Health Check
```http
GET /health
```
**Description:** Check if the API is running properly.

**Response:**
```json
{
  "status": "healthy",
  "version": "2.0.0"
}
```

---

### Upload Document or Image
```http
POST /documents
```
**Description:** Upload a PDF, text file, or image for analysis.

**Request:**
- **Content-Type:** `multipart/form-data`
- **Body:** Form data with file field

**Supported File Types:**
- **Documents:** PDF, TXT
- **Images:** JPEG, PNG, GIF, WebP

**Response:**
```json
{
  "id": "uuid-string",
  "filename": "document.pdf",
  "type": "pdf"
}
```

**Error Response:**
```json
{
  "detail": "Unsupported file type. Supported: PDF, TXT, JPEG, PNG, GIF, WebP"
}
```

---

### List All Documents
```http
GET /documents
```
**Description:** Get a list of all uploaded documents.

**Response:**
```json
{
  "documents": [
    {
      "id": "uuid-string",
      "filename": "document.pdf",
      "file_type": "pdf",
      "uploaded_at": "2024-01-15T10:30:00"
    },
    {
      "id": "uuid-string-2",
      "filename": "image.jpg",
      "file_type": "image",
      "uploaded_at": "2024-01-15T10:35:00"
    }
  ]
}
```

---

### Delete Document
```http
DELETE /documents/{doc_id}
```
**Description:** Delete a document by ID.

**Parameters:**
- `doc_id` (path): UUID of the document to delete

**Response:**
```json
{
  "message": "Document deleted successfully"
}
```

**Error Response:**
```json
{
  "detail": "Document not found"
}
```

---

### Ask Question About Single Document
```http
POST /documents/{doc_id}/question
```
**Description:** Ask a question about a specific document (text, PDF, or image).

**Parameters:**
- `doc_id` (path): UUID of the document

**Request Body:**
```json
{
  "question": "What is this document about?"
}
```

**Response:**
```json
{
  "answer": "This document appears to be about...",
  "document_id": "uuid-string",
  "filename": "document.pdf"
}
```

**Error Responses:**
- `404`: Document not found
- `400`: Invalid request format

---

### Cross-Check Multiple Documents
```http
POST /documents/cross-check
```
**Description:** Ask a question that compares and analyzes multiple documents (2-5 documents).

**Request Body:**
```json
{
  "question": "Compare the main themes across these documents",
  "document_ids": ["uuid-1", "uuid-2", "uuid-3"]
}
```

**Response:**
```json
{
  "answer": "After analyzing the 3 documents, I found the following similarities and differences...",
  "document_ids": ["uuid-1", "uuid-2", "uuid-3"],
  "documents_analyzed": 3
}
```

**Error Responses:**
- `400`: Less than 2 or more than 5 documents specified
- `404`: One or more documents not found

---

## Request/Response Examples

### Upload a PDF Document
```bash
curl -X POST "http://localhost:8000/documents" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@contract.pdf"
```

### Ask a Question About an Image
```bash
curl -X POST "http://localhost:8000/documents/uuid-string/question" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What text can you see in this image?"
  }'
```

### Cross-Check Two Documents
```bash
curl -X POST "http://localhost:8000/documents/cross-check" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Are there any contradictions between these two contracts?",
    "document_ids": ["uuid-1", "uuid-2"]
  }'
```

---

## Error Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 400 | Bad Request - Invalid input or unsupported file type |
| 404 | Not Found - Document doesn't exist |
| 422 | Unprocessable Entity - Validation error |
| 500 | Internal Server Error - Server-side error |

---

## Rate Limits
No rate limits are currently implemented, but it's recommended to:
- Avoid uploading extremely large files (>50MB)
- Limit concurrent requests to prevent overwhelming the AI service

---

## Best Practices

### File Uploads
- **PDF files:** Ensure text is extractable (not scanned images)
- **Images:** Use high-quality, clear images for better AI analysis
- **File names:** Use descriptive names for easier identification

### Questions
- **Be specific:** Clear, specific questions get better answers
- **Context:** Provide context when asking complex questions
- **Cross-checking:** Use cross-checking for comparative analysis

### Example Good Questions
- ✅ "What are the key terms and conditions in this contract?"
- ✅ "Compare the pricing models mentioned in these two proposals"
- ✅ "What text is visible in this screenshot?"

### Example Poor Questions  
- ❌ "Tell me about this"
- ❌ "What is it?"
- ❌ "Analyze"

---

## Frontend Integration

The API includes CORS support for frontend applications running on:
- `http://localhost:3000` (React default)
- `http://localhost:5173` (Vite default)

### JavaScript Example
```javascript
// Upload a file
const formData = new FormData();
formData.append('file', file);

const response = await fetch('http://localhost:8000/documents', {
  method: 'POST',
  body: formData
});

const result = await response.json();
console.log('Uploaded:', result);

// Ask a question
const questionResponse = await fetch(`http://localhost:8000/documents/${result.id}/question`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    question: 'What is this document about?'
  })
});

const answer = await questionResponse.json();
console.log('Answer:', answer.answer);
```

---

## Interactive Documentation
Visit `http://localhost:8000/docs` for interactive API documentation with Swagger UI, where you can test all endpoints directly from your browser.