import streamlit as st
from database import db_manager
from chatbot import chatbot
import config

# Page configuration
st.set_page_config(
    page_title="PDF ChatBot with MongoDB",
    page_icon="📄",
    layout="wide"
)

# Initialize session state
if 'processed_file' not in st.session_state:
    st.session_state.processed_file = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'qa_ready' not in st.session_state:
    st.session_state.qa_ready = False


def main():
    st.title("📄 PDF ChatBot with MongoDB")
    st.markdown("Upload a PDF document and ask questions about its content!")

    # Check configuration
    if not config.OPENAI_API_KEY:
        st.error("⚠️ OpenAI API key not configured. Please check your .env file.")
        return

    # Display connection status
    if not db_manager.is_connected():
        st.error("❌ Not connected to MongoDB. Please check your connection string.")
        return
    else:
        st.success("✅ Connected to MongoDB")

    # Sidebar
    with st.sidebar:
        st.header("📂 Operations")

        # File upload
        uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
        if uploaded_file is not None:
            if st.session_state.processed_file != uploaded_file.name:
                if st.button("Process PDF", key="process_btn"):
                    with st.spinner("Processing PDF..."):
                        success, message = chatbot.process_pdf(
                            uploaded_file.getvalue(),
                            uploaded_file.name
                        )
                        if success:
                            st.success("✅ " + message)
                            # Setup QA chain
                            qa_success, qa_message = chatbot.setup_qa_chain()
                            if qa_success:
                                st.session_state.qa_ready = True
                                st.session_state.processed_file = uploaded_file.name
                                st.rerun()
                            else:
                                st.error("❌ " + qa_message)
                        else:
                            st.error("❌ " + message)
                            st.info("💡 Try a different PDF file. Some PDFs are scanned images or encrypted.")

        # Clear documents
        if st.button("🧹 Clear All Documents", key="clear_btn"):
            success, message = db_manager.clear_all_documents()
            if success:
                chatbot.reset()
                st.session_state.processed_file = None
                st.session_state.chat_history = []
                st.session_state.qa_ready = False
                st.success("✅ " + message)
                st.rerun()
            else:
                st.error("❌ " + message)

        # Status
        st.divider()
        st.subheader("📊 Status")
        st.success("✅ MongoDB Connected")

        if st.session_state.processed_file:
            st.success(f"✅ PDF Loaded: {st.session_state.processed_file}")
        else:
            st.info("📝 No PDF processed")

        document_count = db_manager.get_document_count()
        st.write(f"📄 Documents in DB: {document_count}")
        st.write(f"🔍 Vector Index: {config.VECTOR_INDEX_NAME}")

    # Main chat area
    st.header("💬 Chat with your PDF")

    # Display chat history
    for i, chat in enumerate(st.session_state.chat_history):
        with st.chat_message("user"):
            st.markdown(chat["question"])
        with st.chat_message("assistant"):
            st.markdown(chat["answer"])
            if chat.get("sources"):
                with st.expander("View sources"):
                    for j, source in enumerate(chat["sources"]):
                        st.caption(f"Source {j + 1} (Page {source.metadata.get('page', 'N/A')}):")
                        st.caption(f"{source.page_content[:200]}...")

    # Question input
    question = st.chat_input("Ask a question about the PDF...")

    if question:
        # Add user question
        with st.chat_message("user"):
            st.markdown(question)

        # Get answer
        with st.chat_message("assistant"):
            if st.session_state.qa_ready:
                with st.spinner("Thinking..."):
                    answer, sources = chatbot.ask_question(question)
                    st.markdown(answer)

                    # Show sources if available
                    if sources:
                        with st.expander("View sources"):
                            for j, source in enumerate(sources):
                                st.caption(f"**Source {j + 1}** (Page {source.metadata.get('page', 'N/A')}):")
                                st.caption(f"{source.page_content[:250]}...")
            else:
                st.error("Please process a PDF first")
                answer = "Please process a PDF first"

        # Add to history
        st.session_state.chat_history.append({
            "question": question,
            "answer": answer,
            "sources": sources if 'sources' in locals() else []
        })

    # Quick actions
    st.divider()
    col1, col2 = st.columns(2)

    with col1:
        if st.button("📋 Summarize document", key="summarize_btn"):
            if st.session_state.qa_ready:
                question = "Can you summarize the key points of this document?"
                st.session_state.chat_history.append({
                    "question": question,
                    "answer": "Thinking..."
                })
                st.rerun()

    with col2:
        if st.button("❓ What is this about?", key="about_btn"):
            if st.session_state.qa_ready:
                question = "What is this document about?"
                st.session_state.chat_history.append({
                    "question": question,
                    "answer": "Thinking..."
                })
                st.rerun()


if __name__ == "__main__":
    main()