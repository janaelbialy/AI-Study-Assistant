# confifg.py
import os 
# NOTE: We only need to import 'os' to securely load the API key from environment variables.

class GeminiConfig:
    """Class to hold Gemini API configuration and helper logic."""
    
    # 🔴 Security: The key is loaded from an environment variable instead of being hardcoded.
    # Ensure the GEMINI_API_KEY environment variable is set on your system.
    API_KEY = os.getenv("GEMINI_API_KEY") 
    
    # URL for the specific Gemini model endpoint
    MODEL_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent"
    
    @staticmethod
    def get_headers():
        """Returns the standard headers required for the API request."""
        return {
            "Content-Type": "application/json"
        }
        