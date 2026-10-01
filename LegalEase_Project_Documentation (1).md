# LegalEase – AI-Powered Legal Document Assistant

## 1. Project Overview
LegalEase is a web-based legal document assistant designed to help users generate, edit, summarize, and export legal documents with the support of Generative AI. The project combines a Streamlit user interface, a FastAPI backend/API layer, and Google Gemini for AI-powered text generation.

## 2. Objectives
- Provide a simple interface for creating legal documents.
- Use Generative AI to assist with legal-document drafting.
- Allow users to edit generated content before exporting.
- Support document export in commonly used formats.
- Provide an API layer for application functionality.
- Include validation and automated tests for important components.

## 3. Technologies Used
- Python
- Streamlit – frontend/user interface
- FastAPI – backend/API
- Google Gemini API – generative AI
- Pydantic / Python validation tools
- python-docx – DOCX generation
- ReportLab – PDF generation
- Pytest – testing
- Environment variables for API configuration

## 4. System Architecture
The application follows a layered architecture:

User → Streamlit UI → Application/API layer → Gemini AI service → Generated legal content → Editing/validation → TXT/DOCX/PDF export.

The API layer can also be used independently for programmatic access to supported operations.

## 5. Main Modules
### 5.1 User Interface
The Streamlit interface collects the user's document requirements and displays generated content in an easy-to-use form.

### 5.2 AI Generation
The Gemini integration converts structured user requirements into a legal-document draft. The application keeps the AI interaction behind the application layer so the UI does not need to directly manage the model logic.

### 5.3 Document Editing
Generated text can be reviewed and modified before final export.

### 5.4 Export Module
The project supports generating downloadable document formats such as TXT, DOCX and PDF, depending on the available application functionality.

### 5.5 API Module
FastAPI provides backend endpoints for application operations and makes the core functionality accessible through HTTP requests.

### 5.6 Testing
Pytest-based tests are included to verify important application behaviour and reduce regressions.

## 6. Functional Requirements
1. User should be able to enter document requirements.
2. System should validate required inputs.
3. System should generate a draft using the configured Gemini model.
4. User should be able to review/edit the generated content.
5. User should be able to export the result.
6. API endpoints should return appropriate responses.
7. Invalid requests should be handled with suitable errors.

## 7. Non-Functional Requirements
- Usability: simple web interface.
- Maintainability: modular Python implementation.
- Reliability: input validation and testing.
- Security: API credentials should be stored in environment variables rather than hard-coded.
- Extensibility: AI model and document-generation components can be updated independently.

## 8. Software Requirements
- Windows/Linux/macOS
- Python 3.x
- Internet connection for Gemini API access
- A valid Gemini API key
- Required Python packages from requirements.txt
- Modern web browser

## 9. Configuration
Typical environment configuration uses:
- `GEMINI_API_KEY` – Gemini API credential
- `GEMINI_MODEL` – configured Gemini model
- `DEMO_MODE` – application/demo configuration flag

The actual values should be kept in a local `.env` file or equivalent secure environment configuration and should not be committed to source control.

## 10. Installation and Execution
1. Extract the LegalEase project.
2. Open the project folder in VS Code.
3. Create and activate a Python virtual environment.
4. Install dependencies using `requirements.txt`.
5. Configure the Gemini API key and model in the environment.
6. Start the FastAPI service if backend/API mode is required.
7. Start the Streamlit application.
8. Open the displayed local URL in a browser.

Example dependency installation:
```bash
pip install -r requirements.txt
```

The exact run commands should follow the project's README or entry-point files.

## 11. Data Flow
1. User enters legal-document requirements.
2. Streamlit sends the request to the application logic.
3. Input is validated.
4. The AI service constructs/sends the generation request to Gemini.
5. Gemini returns generated text.
6. The application presents the draft to the user.
7. User reviews or edits the draft.
8. Export logic converts the final text into the selected format.
9. The resulting file is provided to the user.

## 12. Testing
Testing should cover:
- Input validation
- API request/response behaviour
- Document generation
- Export functions
- Error handling
- Core utility functions

Pytest can be used to run the project's automated tests.

## 13. Advantages
- Reduces repetitive drafting work.
- Provides a convenient browser-based interface.
- Uses Generative AI for flexible document drafting.
- Allows human review and editing before export.
- Supports multiple document output formats.
- Separates UI, backend and AI-related responsibilities.

## 14. Limitations
- AI-generated legal text may contain errors or omissions.
- A human/legal professional should review important documents.
- Gemini API availability and usage limits depend on the configured service/account.
- Internet connectivity is required for live AI generation.

## 15. Future Enhancements
- User authentication and role-based access.
- Document history and version control.
- More legal-document templates.
- Multi-language support.
- Secure cloud storage.
- Citation/reference assistance.
- Advanced document comparison.
- Additional AI providers/models.
- Improved audit logging.

## 16. Conclusion
LegalEase demonstrates how Generative AI can be integrated into a practical document-assistance application. By combining Streamlit, FastAPI and Gemini with document-export and testing components, the project provides an extensible foundation for AI-assisted legal-document workflows. The generated content should always be reviewed by an appropriately qualified person before being used for real legal purposes.

## 17. References
- Python Documentation – https://docs.python.org/
- Streamlit Documentation – https://docs.streamlit.io/
- FastAPI Documentation – https://fastapi.tiangolo.com/
- Google Gemini API Documentation – https://ai.google.dev/
- python-docx Documentation – https://python-docx.readthedocs.io/
- ReportLab Documentation – https://docs.reportlab.com/
- Pytest Documentation – https://docs.pytest.org/
