# Smart Document Q&A API

This service lets you upload documents (PDF or text) and ask questions about their contents using the Gemini 2.5 Flash model.

## Usage
1. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```
2. Provide your Gemini API key
   ```bash
   export GEMINI_API_KEY="your_key_here"
   ```
   You can also place this in a `.env` file.
3. Start the server
   ```bash
   uvicorn app.main:app --reload
   ```

## Endpoints
- `POST /documents` – upload a PDF or text file
- `GET /documents` – list uploaded documents
- `POST /documents/{doc_id}/question` – ask a question about a document

## Docker
1. Build the image
   ```bash
   docker build -t smart-doc-qa .
   ```
2. Run the container
   ```bash
   docker run -p 8000:8000 -e GEMINI_API_KEY="your_key_here" smart-doc-qa
   ```
   The API will be available at `http://localhost:8000`.
