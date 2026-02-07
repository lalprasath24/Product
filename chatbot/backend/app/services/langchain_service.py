import logging
from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import PGVector
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from app.core.config import settings

logger = logging.getLogger("remo_ai")

class LangChainRAGService:
    def __init__(self):
        # Initialize embeddings
        self.embeddings = HuggingFaceEmbeddings(
            model_name=settings.EMBEDDING_MODEL
        )
        
        # Initialize vector store
        self.vector_store = PGVector(
            connection_string=settings.DATABASE_URL,
            embedding_function=self.embeddings,
            collection_name="documents",
            use_jsonb=True
        )
        
        # Initialize LLM
        self.llm = ChatOpenAI(
            openai_api_key=settings.OPENROUTER_API_KEY,
            openai_api_base="https://openrouter.ai/api/v1",
            model_name="openai/gpt-3.5-turbo",
            temperature=0.7
        )
        
        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        

    

    async def add_document(self, filename: str, content: str):
        """Add document to vector store"""
        try:
            logger.info(f"Adding document to vector store: {filename}")
            logger.info(f"Content length: {len(content)} characters")
            
            # Split text into chunks
            chunks = self.text_splitter.split_text(content)
            logger.info(f"Split into {len(chunks)} chunks")
            
            # Add metadata
            metadatas = [{"filename": filename, "chunk_id": i} for i in range(len(chunks))]
            
            # Add to vector store
            self.vector_store.add_texts(chunks, metadatas=metadatas)
            
            logger.info(f"Document added successfully: {filename} with {len(chunks)} chunks")
            
        except Exception as e:
            logger.error(f"Failed to add document {filename}: {str(e)}")
            raise
    
    async def search_and_answer(self, query: str) -> str:
        """Search documents and generate answer"""
        try:
            logger.info(f"Processing query: {query[:50]}...")
            
            # Use simple RAG without conversation memory
            from langchain.chains import RetrievalQA
            
            qa_chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                chain_type="stuff",
                retriever=self.vector_store.as_retriever(search_kwargs={"k": 3})
            )
            
            response = qa_chain.run(query)
            
            logger.info("Response generated successfully")
            return response
            
        except Exception as e:
            logger.error(f"Failed to process query: {str(e)}")
            return "I'm having trouble processing your request right now. Please try again later."
    
    async def delete_document(self, filename: str):
        """Delete document from vector store"""
        try:
            logger.info(f"Deleting document from vector store: {filename}")
            
            # Note: PGVector doesn't have direct delete by metadata
            # This would require custom SQL or recreating the collection
            # For now, we'll log the operation
            logger.warning(f"Document deletion not fully implemented for: {filename}")
            
        except Exception as e:
            logger.error(f"Failed to delete document {filename}: {str(e)}")
            raise

# Global instance
rag_service = LangChainRAGService()