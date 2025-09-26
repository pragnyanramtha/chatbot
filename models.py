from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ChatHistoryItem(BaseModel):
    role: str  # 'user' or 'model'
    content: str
    timestamp: datetime

class KnowledgeEntry(BaseModel):
    id: str
    key: str
    value: str
    tags: List[str]
    createdAt: str
    updatedAt: str

class KnowledgeBase(BaseModel):
    title: Optional[str] = "Chatbot"
    description: Optional[str] = "AI Assistant"
    entries: List[KnowledgeEntry]
    lastUpdated: str
    
    class Config:
        # Ignore extra fields like $schema
        extra = "ignore"

class ChatMessage(BaseModel):
    message: str
    session_id: Optional[str] = "default"

class ChatResponse(BaseModel):
    response: str
    sources: Optional[List[str]] = None
    session_id: str