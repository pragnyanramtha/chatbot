from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import logging
import traceback

from models import ChatMessage, ChatResponse
from knowledge_service import KnowledgeService
from gemini_service import GeminiService

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Chatbot API", description="FastAPI chatbot with Gemini AI and knowledge base")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
try:
    knowledge_service = KnowledgeService()
    logger.info("Knowledge service initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize knowledge service: {e}")
    raise

try:
    gemini_service = GeminiService()
    logger.info("Gemini service initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Gemini service: {e}")
    raise

@app.get("/")
async def root():
    return {"message": "Chatbot API is running"}

@app.post("/chat", response_model=ChatResponse)
async def chat(message: ChatMessage):
    """Chat endpoint that uses knowledge base and Gemini AI"""
    try:
        logger.info(f"Received message: {message.message}")
        
        # Get relevant context from knowledge base
        context = knowledge_service.get_relevant_context(message.message)
        logger.info(f"Context found: {len(context)} characters")
        
        # Generate response using Gemini with session support
        response = await gemini_service.generate_response(
            message.message, 
            context, 
            message.session_id or "default"
        )
        logger.info(f"Generated response: {len(response)} characters")
        
        # Get sources (relevant entries)
        relevant_entries = knowledge_service.search_knowledge(message.message)[:3]
        sources = [entry.key for entry in relevant_entries] if relevant_entries else None
        logger.info(f"Sources found: {sources}")
        
        return ChatResponse(
            response=response, 
            sources=sources, 
            session_id=message.session_id or "default"
        )
    
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/knowledge")
async def get_knowledge():
    """Get all knowledge base entries"""
    return knowledge_service.get_all_entries()

@app.get("/config")
async def get_config():
    """Get configuration including title and description"""
    return {
        "title": knowledge_service.knowledge_base.title,
        "description": knowledge_service.knowledge_base.description
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/sessions")
async def list_sessions():
    """List all active chat sessions"""
    return {"sessions": gemini_service.list_sessions()}

@app.get("/sessions/{session_id}/history")
async def get_session_history(session_id: str):
    """Get chat history for a specific session"""
    history = gemini_service.get_session_history(session_id)
    return {"session_id": session_id, "history": history}

@app.delete("/sessions/{session_id}")
async def clear_session(session_id: str):
    """Clear chat history for a specific session"""
    gemini_service.clear_session(session_id)
    return {"message": f"Session {session_id} cleared"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)