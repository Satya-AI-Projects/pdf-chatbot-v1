# PDF ChatBot Application

A Streamlit-based application that allows you to upload PDF documents and ask questions about their content using OpenAI's language models and MongoDB for vector storage.

## Features

- PDF document upload and processing
- Text extraction and chunking
- Vector embeddings stored in MongoDB
- Interactive chat interface
- Source citation for answers

## Setup Instructions

### Prerequisites

- Python 3.8+
- MongoDB (local or Atlas)
- OpenAI API key

### Installation

1. Clone or download this project
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   

I'll explain the complete solution and the purpose of each file in this PDF ChatBot application.

## 🏗️ Architecture Overview

This is a full-stack application with:
- **Frontend**: Streamlit web UI
- **Backend**: Python with LangChain
- **Database**: MongoDB for vector storage
- **AI**: OpenAI for embeddings and chat

## 📁 File Structure & Purpose

### 1. **app.py** - Main Application File
**Purpose**: The heart of the application that combines everything.

**Key Components**:
- **Streamlit UI**: Creates the web interface with file upload and chat
- **PDF Processing**: Handles PDF uploads, text extraction, and chunking
- **Vector Storage**: Manages embeddings in MongoDB
- **QA System**: Handles question-answering using LangChain

**Key Functions**:
- `process_pdf()`: Extracts text from PDF and creates embeddings
- `setup_qa_chain()`: Configures the question-answering system
- `ask_question()`: Processes user queries and returns answers

### 2. **config.py** - Configuration Management
**Purpose**: Centralizes all configuration settings and environment variables.

```python
class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/pdfchatbot")
    # ... other settings
```

**Why it's important**:
- Single source for all configurations
- Environment variable management
- Validation of required settings
- Default values for optional settings

### 3. **utils/database.py** - Database Connection Handler
**Purpose**: Manages MongoDB connections using Singleton pattern.

```python
class MongoDBClient:
    _instance = None  # Singleton pattern
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.client = MongoClient(Config.MONGODB_URI)
        return cls._instance
```

**Benefits**:
- **Singleton pattern**: Ensures only one database connection
- **Connection pooling**: Efficient resource usage
- **Clean abstraction**: Separation of database logic

### 4. **requirements.txt** - Dependencies Management
**Purpose**: Lists all Python packages needed for the application.

**Key packages**:
- `streamlit`: Web UI framework
- `langchain`: AI workflow orchestration
- `openai`: Access to GPT models
- `pymongo`: MongoDB driver
- `pypdf`: PDF text extraction
- `python-dotenv`: Environment variable management

### 5. **.env** - Environment Configuration
**Purpose**: Stores sensitive credentials and environment-specific settings.

**Example content**:
```
OPENAI_API_KEY=your_actual_key_here
MONGODB_URI=mongodb://localhost:27017/pdfchatbot
```

**Security benefits**:
- Keeps secrets out of code
- Different configurations for dev/prod
- Easy to update without code changes

## 🔄 How the Application Works

### 1. **PDF Processing Flow**
```
PDF Upload → Text Extraction → Chunking → Embedding → MongoDB Storage
```

### 2. **Question-Answering Flow**
```
User Question → Vector Search → Context Retrieval → GPT Processing → Answer
```

### 3. **MongoDB Vector Search Setup**
The application uses MongoDB's vector search capabilities:
- Stores text chunks as vectors
- Enables semantic search
- Returns most relevant content for questions

## 🛠️ Solution to Dependency Conflict

The error you encountered was due to incompatible versions:
- `langchain 0.0.346` requires `langchain-core<0.1`
- `langchain-community 0.0.10` requires `langchain-core>=0.1.8`

**My solution**: Use compatible versions that work together:
```txt
langchain==0.0.350
langchain-community==0.0.14
langchain-openai==0.0.5
```

## 🗄️ MongoDB Setup Requirements

### For Local MongoDB:
```bash
# Install MongoDB
brew install mongodb-community

# Start MongoDB
brew services start mongodb-community

# Create database (automatically created when used)
```

### For MongoDB Atlas (Cloud):
1. Create account at [MongoDB Atlas](https://www.mongodb.com/atlas)
2. Create a cluster
3. Get connection string
4. Update `.env` file

## 🚀 How to Run the Application

### 1. **Setup Environment**
```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. **Configure Environment**
```bash
# Edit .env file with your actual values
OPENAI_API_KEY=sk-your-actual-key-here
MONGODB_URI=mongodb://localhost:27017/pdfchatbot
```

### 3. **Run Application**
```bash
streamlit run app.py
```

## 🎯 Key Features Implemented

1. **PDF Upload & Processing**: Drag-and-drop PDF upload with text extraction
2. **Vector Embeddings**: Converts text to numerical vectors for semantic search
3. **Semantic Search**: Finds most relevant content using cosine similarity
4. **Chat Interface**: Clean UI for asking questions and viewing answers
5. **Source Citation**: Shows which parts of the document were used for answers
6. **Session Management**: Maintains chat history during the session

## 🔧 Customization Options

You can easily modify:
- **Chunk size**: Change `chunk_size` in `RecursiveCharacterTextSplitter`
- **Search results**: Modify `k` value in `search_kwargs`
- **AI model**: Switch between GPT-3.5 and GPT-4
- **Temperature**: Adjust creativity of responses
- **Database**: Switch between local MongoDB and MongoDB Atlas

This architecture provides a robust, scalable foundation for a document QA system that can be extended with additional features like user authentication, multiple document support, or advanced analytics.