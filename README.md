# Enhanced OCR Reader 

A powerful full-stack application that combines document processing, image analysis, and AI-powered question answering. Upload PDFs, text files, and images, then ask questions or perform cross-document analysis using Google's Gemini AI.

## Features

###  **Multi-Format Document Support**
- **PDF Documents** - Extract and analyze text content
- **Text Files** - Process plain text documents  
- **Images** - Analyze JPEG, PNG, GIF, WebP files using Gemini's vision capabilities

### **AI-Powered Analysis**
- **Single Document Q&A** - Ask questions about individual documents or images
- **Cross-Document Checking** - Compare and analyze up to 5 documents simultaneously
- **Smart Context Understanding** - Gemini AI provides contextual, detailed responses

###  **Modern Web Interface**
- **React Frontend** - Clean, responsive user interface
- **Drag & Drop Upload** - Easy file uploading with visual feedback
- **Real-time Processing** - Live updates and progress indicators
- **Document Management** - View, select, and delete uploaded documents

### **Production Ready**
- **Docker Support** - Full containerization for easy deployment
- **RESTful API** - Well-documented endpoints with OpenAPI/Swagger
- **Health Monitoring** - Built-in health checks and error handling

##  Quick Start

### Prerequisites
- Docker & Docker Compose
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

### 1. Clone & Setup
```bash
git clone https://github.com/KorieB/OCR-Reader.git
cd OCR-Reader
git checkout feature/enhanced-ui-multifile

# Setup environment
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

### 2. Run with Docker
```bash
# Full-stack (Backend + Frontend)
docker-compose up --build

# Backend only
docker-compose up backend --build

```

### 3. Access the Application
- **Web Interface:** http://localhost:3000
- **API Documentation:** http://localhost:8000/docs
- **API Endpoints:** http://localhost:8000

## 📚 Usage Examples

### Web Interface
1. **Upload Documents:** Drag & drop or click to upload files
2. **Select Mode:** Choose single document or cross-checking
3. **Select Documents:** Check the documents you want to analyze
4. **Ask Questions:** Type your question and get AI-powered answers

### API Usage
```bash
# Upload a document
curl -X POST "http://localhost:8000/documents" \
  -F "file=@contract.pdf"

# Ask a question
curl -X POST "http://localhost:8000/documents/{doc_id}/question" \
  -H "Content-Type: application/json" \
  -d '{"question": "What are the main terms?"}'

# Cross-check documents
curl -X POST "http://localhost:8000/documents/cross-check" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Compare these contracts",
    "document_ids": ["id1", "id2"]
  }'
```

##  Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   React Frontend │    │   FastAPI Backend │    │   Gemini AI     │
│   (Port 3000)    │◄──►│   (Port 8000)     │◄──►│   Google Cloud  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
        │                        │
        └────── Docker Compose ──┘
```

### Backend Components
- **FastAPI** - High-performance Python web framework
- **Document Store** - In-memory document management
- **Image Processor** - Handles image preparation for Gemini
- **Gemini Client** - AI integration for text and image analysis

### Frontend Components  
- **React** - Modern UI framework
- **Vite** - Fast development build tool
- **Axios** - HTTP client for API communication
- **Lucide React** - Beautiful icons

## Development

### Backend Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run backend only
cd app
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development
```bash
# Install dependencies
cd frontend
npm install

# Run development server
npm run dev
```

### Run Tests
```bash
# Backend tests
python -m pytest

# API tests (with running server)
curl http://localhost:8000/health
```

## 📖 API Reference

### Core Endpoints
- `POST /documents` - Upload document or image
- `GET /documents` - List all documents  
- `POST /documents/{id}/question` - Ask about single document
- `POST /documents/cross-check` - Compare multiple documents
- `DELETE /documents/{id}` - Remove document

### Supported File Types
- **Documents:** PDF, TXT
- **Images:** JPEG, PNG, GIF, WebP

See [API_DOCUMENTATION.md](./API_DOCUMENTATION.md) for complete API reference.

##  Configuration

### Environment Variables
```bash
# Required
GEMINI_API_KEY=your_gemini_api_key_here

# Optional (alternatives)
GOOGLE_API_KEY=your_google_api_key_here
```

### Docker Compose Options
```bash
# Production (optimized builds)
docker-compose up

# Development (with hot reload)  
docker-compose --profile dev up

# Backend only
docker-compose up backend

# Custom ports
docker-compose up -p 8080:8000 -p 3001:3000
```

## 🤝 Contributing

1. **Fork the repository**
2. **Create feature branch:** `git checkout -b feature/amazing-feature`
3. **Make changes** and test thoroughly
4. **Commit changes:** `git commit -m 'Add amazing feature'`
5. **Push to branch:** `git push origin feature/amazing-feature`
6. **Open Pull Request**

### Development Guidelines
- Follow Python PEP 8 for backend code
- Use ESLint/Prettier for frontend code  
- Write tests for new features
- Update documentation for API changes

##  License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support & Contact

- **Issues:** [GitHub Issues](https://github.com/KorieB/OCR-Reader/issues)
- **Discussions:** [GitHub Discussions](https://github.com/KorieB/OCR-Reader/discussions)
- **Documentation:** [API Docs](./API_DOCUMENTATION.md)


