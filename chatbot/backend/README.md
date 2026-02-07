# Remo AI Backend - LangChain RAG System

FastAPI backend with LangChain and PostgreSQL vector storage for milk delivery company AI assistant.

## Features

- **LangChain Integration**: Advanced RAG pipeline with document chunking and retrieval
- **Vector Search**: PostgreSQL with pgvector for semantic similarity search
- **OpenRouter API**: GPT-3.5-turbo for intelligent responses
- **Document Management**: Upload, store, and manage company documents

## Setup

1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

2. **Database Setup**
```bash
# Install PostgreSQL and pgvector extension
# Run setup_db.sql in PostgreSQL
psql -U postgres -f setup_db.sql
```

3. **Environment Configuration**
```bash
# Copy env_example.txt to .env and update values
cp env_example.txt .env
```

Required environment variables:
- `OPENROUTER_API_KEY`: Your OpenRouter API key
- `DATABASE_URL`: PostgreSQL connection string
- `EMBEDDING_MODEL`: Sentence transformer model (default: sentence-transformers/all-MiniLM-L6-v2)

4. **Run Server**
```bash
python main.py
```

## API Endpoints

- `POST /api/upload` - Upload .txt files (milk delivery instructions)
- `GET /api/files` - List uploaded documents
- `DELETE /api/files/{filename}` - Delete document
- `POST /api/chat` - Chat with AI using LangChain RAG pipeline

## LangChain RAG Pipeline

1. **Document Processing**: Text splitting with RecursiveCharacterTextSplitter
2. **Embedding**: HuggingFace sentence transformers for vector embeddings
3. **Vector Storage**: PostgreSQL with pgvector for similarity search
4. **Retrieval**: Top-k similar document chunks
5. **Generation**: OpenRouter GPT-3.5-turbo with custom prompt template

## Example Usage

Upload milk delivery instructions as .txt files, then ask:
- "What are the delivery timings?"
- "What products do you deliver?"
- "How to handle fresh milk?"

The AI uses LangChain's RetrievalQA chain to search the vector database and provide accurate responses based on your company documents.