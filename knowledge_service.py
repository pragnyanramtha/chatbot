import json
from typing import List, Optional
from models import KnowledgeBase, KnowledgeEntry

class KnowledgeService:
    def __init__(self, config_path: str = "config.json"):
        self.config_path = config_path
        self.knowledge_base = self._load_knowledge_base()
    
    def _load_knowledge_base(self) -> KnowledgeBase:
        """Load knowledge base from config.json"""
        try:
            with open(self.config_path, 'r') as f:
                data = json.load(f)
                return KnowledgeBase(**data)
        except FileNotFoundError:
            return KnowledgeBase(entries=[], lastUpdated="")
    
    def search_knowledge(self, query: str, tags: Optional[List[str]] = None) -> List[KnowledgeEntry]:
        """Search knowledge base by query and optional tags"""
        results = []
        query_lower = query.lower()
        
        for entry in self.knowledge_base.entries:
            # Check if query matches key or value
            if (query_lower in entry.key.lower() or 
                query_lower in entry.value.lower()):
                
                # If tags specified, check if entry has matching tags
                if tags:
                    if any(tag in entry.tags for tag in tags):
                        results.append(entry)
                else:
                    results.append(entry)
        
        return results
    
    def get_all_entries(self) -> List[KnowledgeEntry]:
        """Get all knowledge base entries"""
        return self.knowledge_base.entries
    
    def get_relevant_context(self, query: str, max_entries: int = 3) -> str:
        """Get relevant context for the query"""
        relevant_entries = self.search_knowledge(query)[:max_entries]
        
        if not relevant_entries:
            return ""
        
        context = "Relevant information from knowledge base:\n\n"
        for entry in relevant_entries:
            context += f"**{entry.key}:**\n{entry.value}\n\n"
        
        return context