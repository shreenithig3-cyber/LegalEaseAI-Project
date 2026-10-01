import os
from dotenv import load_dotenv
from google import genai

load_dotenv()


class GeminiDocumentGenerator:

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY not found")

        self.client = genai.Client(api_key=api_key)

    def generate_document(
        self,
        document_type,
        parties,
        terms,
        effective_date
    ):
        prompt = f"""
Create a simple legal document.

Document Type: {document_type}

Parties:
{parties}

Terms:
{terms}

Effective Date:
{effective_date}

Generate a clear and professional draft.
"""

        response = self.client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )

        return response.text, False