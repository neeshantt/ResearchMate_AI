
import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="ResearchMate AI",
    page_icon="📚",
    layout="wide"
)

st.title("📚 ResearchMate AI")
st.caption("Your intelligent PDF summarization and research assistant")


# Initialize session state
if "documents" not in st.session_state:
    st.session_state.documents = {}

if "messages" not in st.session_state:
    st.session_state.messages = {}


# ---------------- SIDEBAR ----------------

with st.sidebar:

    st.header("📄 Document Library")

    uploaded_files = st.file_uploader(
        "Upload PDF documents",
        type=["pdf"],
        accept_multiple_files=True
    )

    if st.button("Process Documents", use_container_width=True):

        if not uploaded_files:
            st.warning("Please select at least one PDF.")

        else:

            progress = st.progress(0)

            for i, uploaded_file in enumerate(uploaded_files):

                with st.spinner(f"Processing {uploaded_file.name}..."):

                    try:
                        response = requests.post(
                            f"{API_URL}/upload-pdf",
                            files={
                                "file": (
                                    uploaded_file.name,
                                    uploaded_file.getvalue(),
                                    "application/pdf"
                                )
                            },
                            timeout=600
                        )

                        response.raise_for_status()

                        data = response.json()

                        doc_id = data["document_id"]

                        st.session_state.documents[doc_id] = {
                            "filename": data["filename"],
                            "summary": data["summary"]
                        }

                        st.session_state.messages[doc_id] = []

                    except requests.RequestException as e:
                        st.error(
                            f"Failed to process {uploaded_file.name}: {e}"
                        )

                progress.progress((i + 1) / len(uploaded_files))

            st.success("Document processing completed!")


    st.divider()

    
st.subheader("📚 Uploaded Documents")

if st.session_state.documents:

    for doc_id, doc in list(st.session_state.documents.items()):

        col1, col2 = st.columns([4, 1])

        with col1:
            st.write("📄 " + doc["filename"])

        with col2:

            if st.button("🗑️", key=f"delete_{doc_id}"):

                try:
                    response = requests.delete(
                        f"{API_URL}/documents/{doc_id}",
                        timeout=30
                    )

                    response.raise_for_status()

                    # Remove document from frontend state
                    del st.session_state.documents[doc_id]

                    # Remove associated chat history
                    st.session_state.messages.pop(doc_id, None)

                    st.success("Document deleted successfully!")

                    st.rerun()

                except requests.RequestException as e:
                    st.error(f"Deletion failed: {e}")

    else:
                     st.info("No documents uploaded yet.")


# ---------------- MAIN AREA ----------------

if st.session_state.documents:

    st.subheader("Select a Document")

    document_ids = list(st.session_state.documents.keys())

    selected_id = st.selectbox(
        "Choose a PDF to work with",
        options=document_ids,
        format_func=lambda doc_id: st.session_state.documents[doc_id]["filename"]
    )

    selected_document = st.session_state.documents[selected_id]

    # ---------------- SUMMARY ----------------

    st.divider()

    st.subheader("📑 Document Summary")

    st.markdown(selected_document["summary"])

    # ---------------- CHAT ----------------

    st.divider()

    st.subheader("💬 Ask Your Document")

    if selected_id not in st.session_state.messages:
        st.session_state.messages[selected_id] = []

    messages = st.session_state.messages[selected_id]

    for message in messages:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    question = st.chat_input(
        f"Ask something about {selected_document['filename']}..."
    )

    if question:

        messages.append({
            "role": "user",
            "content": question
        })

        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):

            with st.spinner("ResearchMate is thinking..."):

                try:
                    response = requests.post(
                        f"{API_URL}/ask",
                        json={
                            "document_id": selected_id,
                            "question": question
                        },
                        timeout=120
                    )

                    response.raise_for_status()

                    answer = response.json()["answer"]

                    st.markdown(answer)

                    messages.append({
                        "role": "assistant",
                        "content": answer
                    })

                except requests.RequestException as e:
                    st.error(f"Question failed: {e}")

else:

    st.info("Upload your PDFs using the sidebar to get started.")

    st.markdown("""
    ### What ResearchMate AI offers

    - Multiple PDF uploads
    -  Automatic document summaries
    -  Document-specific AI conversations
    -  Context-based question answering
    -  Multiple document management
    """)
