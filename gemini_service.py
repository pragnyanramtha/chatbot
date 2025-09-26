import google.generativeai as genai
import os
from typing import Optional, Dict, List
from datetime import datetime

class GeminiService:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        
        genai.configure(api_key=self.api_key)
        
        # Try different model names in order of preference
        model_names = ['gemini-2.5-flash', 'gemini-2.5-flash-lite', 'gemini-2.5-pro']
        self.model = None
        
        for model_name in model_names:
            try:
                self.model = genai.GenerativeModel(model_name)
                print(f"Successfully initialized with model: {model_name}")
                break
            except Exception as e:
                print(f"Failed to initialize model {model_name}: {e}")
                continue
        
        if not self.model:
            # List available models for debugging
            try:
                models = genai.list_models()
                available_models = [m.name for m in models]
                print(f"Available models: {available_models}")
            except Exception as e:
                print(f"Could not list models: {e}")
            raise ValueError("Could not initialize any Gemini model")
        
        # Store chat sessions - in production, use a database
        self.chat_sessions: Dict[str, List[Dict]] = {}
    
    def _get_chat_history(self, session_id: str) -> List[Dict]:
        """Get chat history for a session"""
        if session_id not in self.chat_sessions:
            self.chat_sessions[session_id] = []
        return self.chat_sessions[session_id]
    
    def _add_to_history(self, session_id: str, role: str, content: str):
        """Add message to chat history"""
        history = self._get_chat_history(session_id)
        history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
        
        # Keep only last 20 messages to avoid token limits
        if len(history) > 20:
            self.chat_sessions[session_id] = history[-20:]
    
    async def generate_response(self, prompt: str, context: Optional[str] = None, session_id: str = "default") -> str:
        """Generate response using Gemini API with chat memory"""
        try:
            # Get chat history for this session
            history = self._get_chat_history(session_id)
            
            # Build conversation context
            conversation_context = ""
            if history:
                conversation_context = "Previous conversation:\n"
                for msg in history[-10:]:  # Use last 10 messages for context
                    role = "User" if msg["role"] == "user" else "Assistant"
                    conversation_context += f"{role}: {msg['content']}\n"
                conversation_context += "\n"
            
            # Combine all context
            full_prompt = ""
            if context:
                full_prompt += f"Knowledge Base Context:\n{context}\n\n"
            
            if conversation_context:
                full_prompt += conversation_context
            
            full_prompt += f"Current User Question: {prompt}\n\n"
            full_prompt += "Please provide a helpful response based on the context and conversation history above. If the context doesn't contain relevant information, provide a general helpful response. Maintain conversation continuity."
            
            # Generate response
            response = self.model.generate_content(full_prompt)
            response_text = response.text
            
            # Add to chat history
            self._add_to_history(session_id, "user", prompt)
            self._add_to_history(session_id, "model", response_text)
            
            return response_text
        
        except Exception as e:
            error_msg = f"Sorry, I encountered an error while processing your request: {str(e)}"
            # Still add to history for continuity
            self._add_to_history(session_id, "user", prompt)
            self._add_to_history(session_id, "model", error_msg)
            return error_msg
    
    def get_session_history(self, session_id: str) -> List[Dict]:
        """Get full chat history for a session"""
        return self._get_chat_history(session_id)
    
    def clear_session(self, session_id: str):
        """Clear chat history for a session"""
        if session_id in self.chat_sessions:
            del self.chat_sessions[session_id]
    
    def list_sessions(self) -> List[str]:
        """List all active session IDs"""
        return list(self.chat_sessions.keys())