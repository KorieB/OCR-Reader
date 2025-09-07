"""Wrapper around the Gemini API."""
from __future__ import annotations

import os
from typing import Optional

<<<<<<< HEAD
=======
from dotenv import load_dotenv
>>>>>>> 45567c0d393cf18bd88b8eb3a2009dedf2c918f7
import google.generativeai as genai


class GeminiClient:
    def __init__(self, model: str = "gemini-2.5-flash", api_key: Optional[str] = None) -> None:
        self.model_name = model
<<<<<<< HEAD
=======
        load_dotenv()
>>>>>>> 45567c0d393cf18bd88b8eb3a2009dedf2c918f7
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
