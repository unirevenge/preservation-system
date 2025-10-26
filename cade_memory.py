"""
CADE Memory Integration Module

This module provides memory management for the CADE system, integrating with the core CADE functionality
to provide persistent storage and retrieval of CADE's state, knowledge, and operational data.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List

from cade_core import CadeCore
from loader import load_json

class CadeMemory:
    """
    Memory management for the CADE system.
    Handles persistence and retrieval of CADE's state and knowledge.
    """
    
    def __init__(self, cade_core: Optional[CadeCore] = None, memory_dir: str = "memory"):
        """
        Initialize the CADE memory system.
        
        Args:
            cade_core: Optional CadeCore instance. If not provided, a new one will be created.
            memory_dir: Directory to store memory files.
        """
        self.core = cade_core if cade_core is not None else CadeCore()
        self.memory_dir = Path(memory_dir)
        self.memory_dir.mkdir(exist_ok=True)
        
        # Memory caches
        self._conversation_history: List[Dict[str, Any]] = []
        self._context_memory: Dict[str, Any] = {}
        self._knowledge_cache: Dict[str, Any] = {}
        
        # Initialize memory stores
        self._init_memory_stores()
    
    def _init_memory_stores(self) -> None:
        """Initialize memory stores from disk if they exist."""
        # Conversation history
        self.conversation_file = self.memory_dir / "conversation.json"
        if self.conversation_file.exists():
            try:
                self._conversation_history = load_json(str(self.conversation_file))
            except Exception as e:
                print(f"Error loading conversation history: {e}")
                self._conversation_history = []
        
        # Context memory
        self.context_file = self.memory_dir / "context.json"
        if self.context_file.exists():
            try:
                self._context_memory = load_json(str(self.context_file))
            except Exception as e:
                print(f"Error loading context memory: {e}")
                self._context_memory = {}
    
    def save_memory(self) -> bool:
        """Save all memory stores to disk."""
        try:
            # Save conversation history
            with open(self.conversation_file, 'w', encoding='utf-8') as f:
                json.dump(self._conversation_history, f, indent=2)
            
            # Save context memory
            with open(self.context_file, 'w', encoding='utf-8') as f:
                json.dump(self._context_memory, f, indent=2)
                
            return True
        except Exception as e:
            print(f"Error saving memory: {e}")
            return False
    
    def add_conversation_turn(self, role: str, content: str, metadata: Optional[Dict] = None) -> None:
        """
        Add a conversation turn to the memory.
        
        Args:
            role: 'user' or 'assistant'
            content: The message content
            metadata: Additional metadata to store with the message
        """
        turn = {
            'role': role,
            'content': content,
            'timestamp': datetime.now().isoformat(),
            'metadata': metadata or {}
        }
        self._conversation_history.append(turn)
        self.save_memory()
    
    def get_recent_conversation(self, num_turns: int = 5) -> List[Dict[str, Any]]:
        """Get the most recent conversation turns."""
        return self._conversation_history[-num_turns:]
    
    def update_context(self, key: str, value: Any) -> None:
        """Update a value in the context memory."""
        self._context_memory[key] = value
        self.save_memory()
    
    def get_context(self, key: str, default: Any = None) -> Any:
        """Get a value from the context memory."""
        return self._context_memory.get(key, default)
    
    def get_core_knowledge(self, key: str = None) -> Any:
        """
        Get knowledge from the CADE core.
        
        Args:
            key: Optional key to get specific knowledge. If None, returns all knowledge.
            
        Returns:
            The requested knowledge or None if not found.
        """
        if not self.core.is_initialized() and not self.core.load_core_files():
            return None
            
        if key:
            return self.core.knowledge.get(key)
        return self.core.knowledge
    
    def get_identity(self) -> Dict[str, Any]:
        """Get CADE's identity information."""
        if not self.core.is_initialized() and not self.core.load_core_files():
            return {}
        return self.core.get_identity()
    
    def get_directives(self) -> Dict[str, list]:
        """Get CADE's operational directives."""
        if not self.core.is_initialized() and not self.core.load_core_files():
            return {}
        return self.core.get_directives()
    
    def get_status(self) -> Dict[str, Any]:
        """Get the current status of the CADE memory system."""
        core_status = self.core.get_status() if self.core.is_initialized() else {"error": "CADE core not initialized"}
        
        return {
            "core_initialized": self.core.is_initialized(),
            "conversation_history_count": len(self._conversation_history),
            "context_memory_size": len(self._context_memory),
            "memory_dir": str(self.memory_dir.absolute()),
            "core_status": core_status
        }

# Global instance for easy import
cade_memory = CadeMemory()

# For easy import
__all__ = ['CadeMemory', 'cade_memory']
