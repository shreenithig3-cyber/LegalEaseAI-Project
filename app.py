import os
from datetime import date

import requests
import streamlit as st

from dotenv import load_dotenv

from backend.services.export_service import (
    export_filename,
    format_docx,
    format_html_preview,
    format_pdf,
    format_txt
)


load_dotenv()


BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://127.0.0.1:8000"
).rstrip("/")


TIMEOUT = int(
    os.getenv(
        "REQUEST_TIMEOUT",
        "120"
    )
)


# -----------------------------------
# Page configuration
# -----------------------------------

st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="wide"
)


# -----------------------------------
# Custom CSS
# -----------------------------------

st.markdown(
    """
    <style>

    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 0;
    }

    .subtitle {
        text-align: center;
        color: #777;
        margin-bottom: 24px;
    }

    .preview {
        background: #171717;
        color: #f2f2f2;
        padding: 24px;
        border-radius: 12px;
        max-height: 620px;
        overflow-y: auto;
        line-height: 1.65;
    }

    .preview h3 {
        color: white;
        margin-top: 18px;
    }

    .preview p {
        margin: 8px 0;
    }

    .preview .bullet {
        margin: 6px 0 6px 18px;
    }

    .preview .blank {
        height: 8px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# -----------------------------------
# Header
# -----------------------------------

st.markdown(
    "<div class='main-title'>⚖️ LegalEase</div>",
    unsafe_allow_html=True
)


st.markdown(
    """
    <div class='subtitle'>
    AI-powered legal document drafting,
    editing and export
    </div>
    """,
    unsafe_allow_html=True
)


# -----------------------------------
# Sidebar
# -----------------------------------

with st.sidebar:

    st.header("Settings")

    st.write(
        f"Backend: `{BACKEND_URL}`"
    )

    st.info(
        "LegalEase generates drafts for review. "
        "It does not replace advice from a "
        "qualified lawyer."
    )


# -----------------------------------
# Session state
# -----------------------------------

if "document" not in st.session_state:

    st.session_state.document = ""


if "doc_type" not in st.session_state:

    st.session_state.doc_type = (
        "Employment Contract"
    )


# -----------------------------------
# Input columns
# -----------------------------------

column1, column2 = st.columns(2)


with column1:

    document_type = st.text_input(
        "Document Type",
        value=st.session_state.doc_type,
        placeholder=(
            "e.g. NDA, Lease Agreement, "
            "Employment Contract"
        )
    )


    parties = st.text_area(
        "Parties Involved",
        height=120,
        placeholder=(
            "e.g. Jane Doe (Employee), "
            "ABC Technologies (Employer)"
        )
    )


with column2:

    effective_date = st.text_input(
        "Effective Date",
        value=date.today().isoformat(),
        placeholder="YYYY-MM-DD"
    )


    terms = st.text_area(
        "Terms & Conditions",
        height=120,
        placeholder=(
            "Separate clauses with semicolons ;"
        ),
        help=(
            "Example: Payment within 30 days; "
            "Confidentiality applies; "
            "Either party may terminate "
            "with 15 days notice"
        )
    )


# -----------------------------------
# Generate button
# -----------------------------------

generate_button = st.button(
    "✨ Generate Document",
    type="primary",
    use_container_width=True
)


if generate_button:

    if not all(
        [
            document_type.strip(),
            parties.strip(),
            terms.strip(),
            effective_date.strip()
        ]
    ):

        st.error(
            "Please fill in all four fields."
        )


    else:

        payload = {

            "document_type":
                document_type.strip(),

            "parties":
                parties.strip(),

            "terms":
                terms.strip(),

            "effective_date":
                effective_date.strip()
        }


        with st.spinner(
            "Generating your draft..."
        ):

            try:

                response = requests.post(

                    f"{BACKEND_URL}/generate",

                    json=payload,

                    timeout=TIMEOUT
                )


                response.raise_for_status()


                data = response.json()


                st.session_state.document = (
                    data["content"]
                )


                st.session_state.doc_type = (
                    data["document_type"]
                )


                if data.get("demo_mode"):

                    st.warning(
                        "Demo mode is active. "
                        "This draft was generated "
                        "locally, not by Gemini."
                    )

                else:

                    st.success(
                        "Document generated successfully."
                    )


            except requests.RequestException as exc:

                st.error(
                    "Could not connect to the "
                    "FastAPI backend."
                )

                st.info(
                    "Make sure FastAPI is running "
                    "on port 8000."
                )

                st.code(
                    "uvicorn backend.main:app "
                    "--reload --port 8000"
                )

                st.caption(
                    str(exc)
                )


# -----------------------------------
# Document area
# -----------------------------------

if st.session_state.document:

    st.divider()


    st.subheader(
        "📄 Document Preview"
    )


    html_preview = (
        format_html_preview(
            st.session_state.document
        )
    )


    st.markdown(
        f"""
        <div class="preview">
        {html_preview}
        </div>
        """,
        unsafe_allow_html=True
    )


    # --------------------------------
    # Editing
    # --------------------------------

    st.subheader(
        "✏️ Edit Document"
    )


    edited_document = st.text_area(

        "Editable document",

        value=st.session_state.document,

        height=500,

        label_visibility="collapsed"
    )


    st.session_state.document = (
        edited_document
    )


    # --------------------------------
    # Downloads
    # --------------------------------

    st.subheader(
        "⬇️ Download"
    )


    button1, button2, button3 = (
        st.columns(3)
    )


    # TXT

    with button1:

        st.download_button(

            "⬇️ Download TXT",

            data=format_txt(
                st.session_state.document
            ),

            file_name=export_filename(
                st.session_state.doc_type,
                "txt"
            ),

            mime="text/plain",

            use_container_width=True
        )


    # DOCX

    with button2:

        st.download_button(

            "⬇️ Download DOCX",

            data=format_docx(

                st.session_state.document,

                st.session_state.doc_type
            ),

            file_name=export_filename(
                st.session_state.doc_type,
                "docx"
            ),

            mime=(
                "application/vnd.openxmlformats-"
                "officedocument.wordprocessingml.document"
            ),

            use_container_width=True
        )


    # PDF

    with button3:

        st.download_button(

            "⬇️ Download PDF",

            data=format_pdf(

                st.session_state.document,

                st.session_state.doc_type
            ),

            file_name=export_filename(
                st.session_state.doc_type,
                "pdf"
            ),

            mime="application/pdf",

            use_container_width=True
        )


else:

    st.info(
        "Enter the document details above "
        "and click Generate Document."
    )