import os
from dotenv import load_dotenv

load_dotenv()

# MongoDB Configuration
MONGODB_URI = os.getenv("MONGODB_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME", "pdfchatbot")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "documents")
VECTOR_INDEX_NAME = os.getenv("VECTOR_INDEX_NAME", "pdf_vector_index_v2")

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

# Application Configuration
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
MAX_DOCUMENTS_RETRIEVED = 3