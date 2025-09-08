import React, { useState, useEffect } from 'react'
import axios from 'axios'
import { Upload, FileText, Image, MessageSquare, Trash2, CheckCircle } from 'lucide-react'

const API_BASE_URL = 'http://localhost:8000'

function App() {
  const [documents, setDocuments] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [question, setQuestion] = useState('')
  const [answer, setAnswer] = useState('')
  const [selectedDocuments, setSelectedDocuments] = useState([])
  const [questionMode, setQuestionMode] = useState('single') // 'single' or 'cross-check'

  useEffect(() => {
    fetchDocuments()
  }, [])

  const fetchDocuments = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/documents`)
      setDocuments(response.data.documents)
    } catch (err) {
      setError('Failed to fetch documents')
    }
  }

  const handleFileUpload = async (files) => {
    if (!files || files.length === 0) return

    setLoading(true)
    setError('')
    setSuccess('')

    try {
      for (const file of files) {
        const formData = new FormData()
        formData.append('file', file)

        await axios.post(`${API_BASE_URL}/documents`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        })
      }

      setSuccess(`Successfully uploaded ${files.length} file(s)`)
      fetchDocuments()
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to upload file(s)')
    } finally {
      setLoading(false)
    }
  }

  const handleDeleteDocument = async (docId) => {
    if (!window.confirm('Are you sure you want to delete this document?')) return

    try {
      await axios.delete(`${API_BASE_URL}/documents/${docId}`)
      setSuccess('Document deleted successfully')
      fetchDocuments()
      setSelectedDocuments(selectedDocuments.filter(id => id !== docId))
    } catch (err) {
      setError('Failed to delete document')
    }
  }

  const handleAskQuestion = async () => {
    if (!question.trim()) {
      setError('Please enter a question')
      return
    }

    if (questionMode === 'single' && selectedDocuments.length !== 1) {
      setError('Please select exactly one document for single document questions')
      return
    }

    if (questionMode === 'cross-check' && selectedDocuments.length < 2) {
      setError('Please select at least 2 documents for cross-checking')
      return
    }

    setLoading(true)
    setError('')
    setAnswer('')

    try {
      let response
      if (questionMode === 'single') {
        response = await axios.post(`${API_BASE_URL}/documents/${selectedDocuments[0]}/question`, {
          question: question
        })
      } else {
        response = await axios.post(`${API_BASE_URL}/documents/cross-check`, {
          question: question,
          document_ids: selectedDocuments
        })
      }

      setAnswer(response.data.answer)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to get answer')
    } finally {
      setLoading(false)
    }
  }

  const handleDocumentSelection = (docId) => {
    if (questionMode === 'single') {
      setSelectedDocuments([docId])
    } else {
      setSelectedDocuments(prev => 
        prev.includes(docId) 
          ? prev.filter(id => id !== docId)
          : [...prev, docId]
      )
    }
  }

  const handleDragOver = (e) => {
    e.preventDefault()
    e.currentTarget.classList.add('dragover')
  }

  const handleDragLeave = (e) => {
    e.preventDefault()
    e.currentTarget.classList.remove('dragover')
  }

  const handleDrop = (e) => {
    e.preventDefault()
    e.currentTarget.classList.remove('dragover')
    const files = Array.from(e.dataTransfer.files)
    handleFileUpload(files)
  }

  const getFileIcon = (fileType) => {
    switch (fileType) {
      case 'image': return <Image size={16} />
      case 'pdf': return <FileText size={16} />
      default: return <FileText size={16} />
    }
  }

  const getFileTypeBadge = (fileType) => {
    return <span className={`file-type-badge file-type-${fileType}`}>{fileType}</span>
  }

  return (
    <div className="container">
      <div className="header">
        <h1>Enhanced OCR Reader</h1>
        <p>Upload documents and images, ask questions, and cross-check multiple files</p>
      </div>

      {error && <div className="error">{error}</div>}
      {success && <div className="success">{success}</div>}

      {/* Upload Section */}
      <div className="upload-section">
        <h2>Upload Documents</h2>
        <div 
          className="upload-area"
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          onClick={() => document.getElementById('fileInput').click()}
        >
          <Upload size={48} style={{ margin: '0 auto 10px', display: 'block', color: '#666' }} />
          <p>Drag & drop files here or click to browse</p>
          <p style={{ fontSize: '14px', color: '#999', marginTop: '10px' }}>
            Supports: PDF, TXT, JPEG, PNG, GIF, WebP
          </p>
          <input
            id="fileInput"
            type="file"
            className="file-input"
            multiple
            accept=".pdf,.txt,.jpg,.jpeg,.png,.gif,.webp"
            onChange={(e) => handleFileUpload(Array.from(e.target.files))}
          />
        </div>
      </div>

      {/* Documents Section */}
      <div className="documents-section">
        <h2>Documents ({documents.length})</h2>
        {documents.length === 0 ? (
          <p style={{ textAlign: 'center', color: '#666', padding: '20px' }}>
            No documents uploaded yet
          </p>
        ) : (
          documents.map((doc) => (
            <div key={doc.id} className="document-item">
              <div className="document-info">
                <h4>
                  {getFileIcon(doc.file_type)} {doc.filename} {getFileTypeBadge(doc.file_type)}
                </h4>
                <p>Uploaded: {new Date(doc.uploaded_at).toLocaleString()}</p>
              </div>
              <div className="document-actions">
                <label className="checkbox-item">
                  <input
                    type="checkbox"
                    checked={selectedDocuments.includes(doc.id)}
                    onChange={() => handleDocumentSelection(doc.id)}
                  />
                  Select
                </label>
                <button
                  className="btn btn-danger"
                  onClick={() => handleDeleteDocument(doc.id)}
                  title="Delete document"
                >
                  <Trash2 size={16} />
                </button>
              </div>
            </div>
          ))
        )}
      </div>

      {/* Question Section */}
      <div className="question-section">
        <h2>Ask Questions</h2>
        
        <div className="form-group">
          <label>Question Mode:</label>
          <div style={{ display: 'flex', gap: '15px', marginTop: '5px' }}>
            <label className="checkbox-item">
              <input
                type="radio"
                name="questionMode"
                value="single"
                checked={questionMode === 'single'}
                onChange={(e) => setQuestionMode(e.target.value)}
              />
              Single Document
            </label>
            <label className="checkbox-item">
              <input
                type="radio"
                name="questionMode"
                value="cross-check"
                checked={questionMode === 'cross-check'}
                onChange={(e) => setQuestionMode(e.target.value)}
              />
              Cross-Check Multiple Documents
            </label>
          </div>
        </div>

        <div className="form-group">
          <label>Selected Documents: {selectedDocuments.length}</label>
          <p style={{ fontSize: '14px', color: '#666' }}>
            {questionMode === 'single' 
              ? 'Select exactly 1 document' 
              : 'Select 2-5 documents for cross-checking'}
          </p>
        </div>

        <div className="form-group">
          <label htmlFor="question">Your Question:</label>
          <textarea
            id="question"
            className="form-control"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="What would you like to know about the document(s)?"
            rows={3}
          />
        </div>

        <button
          className="btn"
          onClick={handleAskQuestion}
          disabled={loading || !question.trim() || selectedDocuments.length === 0}
        >
          {loading ? 'Processing...' : (
            <>
              <MessageSquare size={16} style={{ marginRight: '5px' }} />
              Ask Question
            </>
          )}
        </button>
      </div>

      {/* Answer Section */}
      {answer && (
        <div className="answer-section">
          <h2>Answer</h2>
          <div className="answer-content">
            {answer}
          </div>
        </div>
      )}

      {loading && (
        <div className="loading">
          <p>Processing your request...</p>
        </div>
      )}
    </div>
  )
}

export default App