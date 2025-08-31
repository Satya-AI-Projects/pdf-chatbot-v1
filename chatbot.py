from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA
from langchain_mongodb import MongoDBAtlasVectorSearch
import tempfile
import os
import uuid
from datetime import datetime
import config
from database import db_manager
import traceback


class PDFChatBot:
    def __init__(self):
        self.qa_chain = None
        self.embeddings = None
        self.vector_store = None

    def initialize_embeddings(self):
        """Initialize OpenAI embeddings"""
        try:
            if not config.OPENAI_API_KEY:
                return False, "OpenAI API key not configured"

            self.embeddings = OpenAIEmbeddings(
                openai_api_key=config.OPENAI_API_KEY,
                model="text-embedding-ada-002"
            )
            return True, "Embeddings initialized"
        except Exception as e:
            return False, f"Failed to initialize embeddings: {e}"

    def process_pdf(self, file_content, filename):
        """Process PDF and store in MongoDB"""
        tmp_file_path = None
        try:
            # Check database connection
            if not db_manager.is_connected():
                return False, "Database not connected"

            # Initialize embeddings
            success, message = self.initialize_embeddings()
            if not success:
                return False, message

            # Save to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                tmp_file.write(file_content)
                tmp_file_path = tmp_file.name

            # Load PDF with better error handling
            try:
                loader = PyPDFLoader(tmp_file_path)
                documents = loader.load()

                if not documents or len(documents) == 0:
                    return False, "No text could be extracted from PDF. The PDF might be scanned or encrypted."

                # Check if documents contain actual text
                total_text_length = sum(len(doc.page_content) for doc in documents)
                if total_text_length == 0:
                    return False, "PDF appears to be empty or contains no extractable text."

            except Exception as e:
                return False, f"Failed to load PDF: {str(e)}. The PDF might be corrupted or encrypted."

            # Split text
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=config.CHUNK_SIZE,
                chunk_overlap=config.CHUNK_OVERLAP,
                length_function=len,
            )
            docs = text_splitter.split_documents(documents)

            # Add metadata
            for i, doc in enumerate(docs):
                doc.metadata["document_id"] = str(uuid.uuid4())
                doc.metadata["processed_at"] = datetime.now().isoformat()
                doc.metadata["original_filename"] = filename
                doc.metadata["chunk_index"] = i
                # Ensure each document has proper content
                if not doc.page_content or len(doc.page_content.strip()) == 0:
                    doc.page_content = "No content available"

            # Store in MongoDB
            self.vector_store = MongoDBAtlasVectorSearch.from_documents(
                documents=docs,
                embedding=self.embeddings,
                collection=db_manager.collection,
                index_name=config.VECTOR_INDEX_NAME
            )

            return True, f"Successfully processed {len(docs)} text chunks from {filename}"

        except Exception as e:
            error_trace = traceback.format_exc()
            print(f"PDF processing error: {error_trace}")
            return False, f"PDF processing failed: {str(e)}"
        finally:
            # Clean up temp file
            if tmp_file_path and os.path.exists(tmp_file_path):
                try:
                    os.unlink(tmp_file_path)
                except:
                    pass

    def setup_qa_chain(self):
        """Setup question-answering chain"""
        try:
            if not db_manager.is_connected():
                return False, "Database not connected"

            # Initialize embeddings if not already done
            if not self.embeddings:
                success, message = self.initialize_embeddings()
                if not success:
                    return False, message

            # Initialize LLM
            llm = ChatOpenAI(
                openai_api_key=config.OPENAI_API_KEY,
                model_name=config.OPENAI_MODEL,
                temperature=0
            )

            # Create vector store connection
            self.vector_store = MongoDBAtlasVectorSearch(
                collection=db_manager.collection,
                embedding=self.embeddings,
                index_name=config.VECTOR_INDEX_NAME
            )

            # Create retriever
            retriever = self.vector_store.as_retriever(
                search_type="similarity",
                search_kwargs={"k": config.MAX_DOCUMENTS_RETRIEVED}
            )

            # Create QA chain
            self.qa_chain = RetrievalQA.from_chain_type(
                llm=llm,
                chain_type="stuff",
                retriever=retriever,
                return_source_documents=True
            )

            return True, "QA chain ready"

        except Exception as e:
            error_trace = traceback.format_exc()
            print(f"QA chain setup error: {error_trace}")
            return False, f"QA chain setup failed: {str(e)}"

    def ask_question(self, question):
        """Ask a question and get response"""
        if not self.qa_chain:
            return "Please process a PDF first", []

        try:
            result = self.qa_chain.invoke({"query": question})
            return result["result"], result.get("source_documents", [])
        except Exception as e:
            error_trace = traceback.format_exc()
            print(f"Question answering error: {error_trace}")
            return f"Error getting answer: {str(e)}", []

    def reset(self):
        """Reset the chatbot state"""
        self.qa_chain = None
        self.vector_store = None


# Global chatbot instance
chatbot = PDFChatBot()