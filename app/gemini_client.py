"""Wrapper around the Gemini API."""
from __future__ import annotations

import os
from typing import Optional, List, Dict, Any

from dotenv import load_dotenv
import google.generativeai as genai


class GeminiClient:
    def __init__(self, model: str = "gemini-2.5-flash", api_key: Optional[str] = None) -> None:
        self.model_name = model
        load_dotenv()
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
        self._model: Optional[genai.GenerativeModel] = None

    def _ensure_model(self) -> None:
        if self._model is None:
            if not self.api_key:
                raise RuntimeError("GEMINI_API_KEY environment variable is not set")
            genai.configure(api_key=self.api_key)
            self._model = genai.GenerativeModel(self.model_name)

    def ask(self, text: str, question: str) -> str:
        """Ask a question about a piece of text."""
        self._ensure_model()
        prompt = f"Document:\n{text}\n\nQuestion: {question}"
        response = self._model.generate_content(prompt)
        return response.text.strip()
    
    def ask_with_image(self, question: str, image_data: Dict[str, Any]) -> str:
        """Ask a question about an image."""
        self._ensure_model()
        response = self._model.generate_content([question, image_data])
        return response.text.strip()
    
    def ask_multiple_documents(self, documents: Dict[str, str], question: str) -> str:
        """Ask a question about multiple documents for cross-checking."""
        self._ensure_model()
        
        # Prepare the prompt with multiple documents
        prompt = f"I have {len(documents)} documents to analyze:\n\n"
        
        for i, (doc_id, text) in enumerate(documents.items(), 1):
            prompt += f"Document {i} (ID: {doc_id}):\n{text}\n\n"
        
        prompt += f"Question: {question}\n\nPlease analyze all documents and provide a comprehensive answer, noting any similarities, differences, or contradictions between them."
        
        response = self._model.generate_content(prompt)
        return response.text.strip()
