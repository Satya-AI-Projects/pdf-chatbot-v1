# 📄 PDF ChatBot Application

A powerful AI-powered PDF document analysis tool that allows you to upload PDF documents and have intelligent conversations about their content. Built with Streamlit, MongoDB, and OpenAI's GPT models.

## 🌟 Features

- **PDF Document Upload**: Drag-and-drop interface for easy PDF uploads
- **Intelligent Q&A**: Ask questions about your PDF content using AI
- **Source Citations**: Get answers with references to specific document sections
- **Vector Search**: Advanced semantic search through document content
- **Real-time Chat**: Interactive chat interface with conversation history
- **Document Management**: Clear and manage uploaded documents
- **MongoDB Storage**: Scalable vector storage for document embeddings

## 🏗️ Architecture

- **Frontend**: Streamlit web interface
- **Backend**: Python with LangChain framework
- **Database**: MongoDB with vector search capabilities
- **AI Engine**: OpenAI GPT models for text processing and Q&A
- **Vector Storage**: OpenAI embeddings for semantic search

## 📋 Prerequisites

Before running this application, ensure you have:

- **Python 3.8+** installed on your system
- **MongoDB** (local installation or MongoDB Atlas account)
- **OpenAI API Key** (get one from [OpenAI Platform](https://platform.openai.com/api-keys))
- **Git** (for cloning the repository)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd pdf-chatbot
```

### 2. Set Up Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up MongoDB

#### Option A: Local MongoDB (Recommended for development)

```bash
# Install MongoDB using Homebrew (macOS)
brew tap mongodb/brew
brew install mongodb-community

# Start MongoDB service
brew services start mongodb-community

# Verify MongoDB is running
mongosh --eval "db.adminCommand('ping')"
```

#### Option B: MongoDB Atlas (Cloud)

1. Create a free account at [MongoDB Atlas](https://www.mongodb.com/atlas)
2. Create a new cluster
3. Get your connection string
4. Use the Atlas connection string in your environment variables

### 5. Configure Environment Variables

Create a `.env` file in the project root:

```bash
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# MongoDB Configuration
MONGODB_URI=mongodb://localhost:27017/pdfchatbot
DATABASE_NAME=pdfchatbot
COLLECTION_NAME=documents
VECTOR_INDEX_NAME=pdf_vector_index_v2

# OpenAI Model Configuration
OPENAI_MODEL=gpt-3.5-turbo
```

**Important**: Replace `your_openai_api_key_here` with your actual OpenAI API key.

### 6. Run the Application

```bash
# Activate virtual environment (if not already active)
source venv/bin/activate

# Start the application
streamlit run app.py
```

The application will be available at:
- **Local URL**: http://localhost:8501
- **Network URL**: http://[your-ip]:8501

## 📖 User Manual

### Getting Started

1. **Open the Application**: Navigate to http://localhost:8501 in your web browser
2. **Check Status**: Ensure you see "✅ Connected to MongoDB" and "✅ OpenAI API key configured"
3. **Upload a PDF**: Use the file uploader in the sidebar to select a PDF document
4. **Process Document**: Click "Process PDF" to extract and analyze the content
5. **Start Chatting**: Once processed, you can ask questions about the document

### Using the Chat Interface

#### Basic Questions
- "What is this document about?"
- "Summarize the key points"
- "What are the main conclusions?"
- "Explain the methodology used"

#### Specific Queries
- "What does section 3.2 say about pricing?"
- "Find information about the budget allocation"
- "What are the risks mentioned in the document?"
- "Who are the key stakeholders mentioned?"

#### Advanced Features
- **Source Citations**: Click "View sources" to see which parts of the document were used for answers
- **Chat History**: Your conversation history is maintained during the session
- **Quick Actions**: Use the "Summarize document" and "What is this about?" buttons for common queries

### Managing Documents

#### Uploading New Documents
1. Click "Choose a PDF file" in the sidebar
2. Select your PDF file
3. Click "Process PDF" to analyze the content
4. Wait for the "✅ Successfully processed" message

#### Clearing Documents
1. Click "🧹 Clear All Documents" in the sidebar
2. Confirm the action
3. All documents and chat history will be cleared

### Understanding the Interface

#### Sidebar
- **File Upload**: Upload and process PDF documents
- **Clear Documents**: Remove all uploaded documents
- **Status Panel**: Shows connection status and document count

#### Main Area
- **Chat History**: Displays your conversation with the AI
- **Question Input**: Type your questions here
- **Quick Actions**: Common question buttons
- **Source Citations**: Expandable sections showing document sources

## 🔧 Configuration Options

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `OPENAI_API_KEY` | Your OpenAI API key | - | Yes |
| `MONGODB_URI` | MongoDB connection string | `mongodb://localhost:27017/pdfchatbot` | Yes |
| `DATABASE_NAME` | MongoDB database name | `pdfchatbot` | No |
| `COLLECTION_NAME` | MongoDB collection name | `documents` | No |
| `VECTOR_INDEX_NAME` | Vector search index name | `pdf_vector_index_v2` | No |
| `OPENAI_MODEL` | OpenAI model to use | `gpt-3.5-turbo` | No |

### Customization

You can modify the application behavior by editing `config.py`:

```python
# Text processing settings
CHUNK_SIZE = 1000          # Size of text chunks
CHUNK_OVERLAP = 200        # Overlap between chunks
MAX_DOCUMENTS_RETRIEVED = 3  # Number of relevant chunks to retrieve
```

## 🛠️ Troubleshooting

### Common Issues

#### 1. MongoDB Connection Failed
**Error**: "❌ Not connected to MongoDB"

**Solutions**:
- Ensure MongoDB is running: `brew services start mongodb-community`
- Check connection string in `.env` file
- Verify MongoDB is accessible: `mongosh --eval "db.adminCommand('ping')"`

#### 2. OpenAI API Key Error
**Error**: "⚠️ OpenAI API key not configured"

**Solutions**:
- Add your API key to the `.env` file
- Ensure the key is valid and has sufficient credits
- Check for typos in the API key

#### 3. PDF Processing Failed
**Error**: "❌ PDF processing failed"

**Solutions**:
- Ensure the PDF is not password-protected
- Check if the PDF contains extractable text (not just images)
- Try with a different PDF file
- Verify the file is not corrupted

#### 4. SSL/TLS Connection Issues
**Error**: SSL handshake failed

**Solutions**:
- For local MongoDB, the app automatically tries different connection options
- For MongoDB Atlas, ensure your IP is whitelisted
- Check your network connection

### Performance Issues

#### Slow Response Times
- Reduce `MAX_DOCUMENTS_RETRIEVED` in config.py
- Use a faster OpenAI model (gpt-3.5-turbo instead of gpt-4)
- Ensure MongoDB is running locally for better performance

#### Memory Issues
- Process smaller PDFs
- Clear documents regularly
- Restart the application if needed

## 📁 Project Structure

```
pdf-chatbot/
├── app.py                 # Main Streamlit application
├── chatbot.py            # PDF processing and Q&A logic
├── config.py             # Configuration settings
├── database.py           # MongoDB connection management
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (create this)
├── test_connection.py    # MongoDB connection test
├── test_pdf.py          # PDF processing test
├── test_streamlit.py    # Streamlit app test
└── README.md            # This file
```

## 🔒 Security Notes

- Never commit your `.env` file to version control
- Keep your OpenAI API key secure
- Use environment variables for production deployments
- Regularly rotate your API keys

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🆘 Support

If you encounter any issues:

1. Check the troubleshooting section above
2. Review the application logs in the terminal
3. Ensure all dependencies are properly installed
4. Verify your environment variables are correct

## 🎯 Future Enhancements

- Support for multiple document types (Word, PowerPoint, etc.)
- User authentication and document sharing
- Advanced search filters and sorting
- Export chat conversations
- Batch document processing
- Custom AI model integration

---

**Happy Document Analysis!** 🚀