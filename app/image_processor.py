"""Image processing utilities."""
from __future__ import annotations

import base64
from typing import Dict, Any


class ImageProcessor:
    """Simple image handler for Gemini integration."""
    
    def __init__(self) -> None:
        pass
    
    def prepare_image_for_gemini(self, image_bytes: bytes, content_type: str) -> Dict[str, Any]:
        """Prepare image data for Gemini API."""
        # Extract mime type
        mime_type = content_type
        
        # Convert to base64 for Gemini
        image_b64 = base64.b64encode(image_bytes).decode('utf-8')
        
        return {
            "inline_data": {
                "mime_type": mime_type,
                "data": image_b64
            }
        }
    
    def is_supported_image(self, content_type: str) -> bool:
        """Check if the image format is supported by Gemini."""
        supported_formats = {
            'image/jpeg',
            'image/jpg', 
            'image/png',
            'image/gif',
            'image/webp'
        }
        return content_type.lower() in supported_formats