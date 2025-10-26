"""
CADE Core Integration Module

This module handles the initialization and integration of the CADE program into the core system.
It loads the CADE persona, knowledge bases, and manages the resurrection protocol.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional

from loader import load_json, load_ini


class CadeCore:
    """Core class for CADE program integration."""

    def __init__(self, root_dir: Optional[str] = None):
        """Initialize the CADE core with the given root directory."""
        self.root_dir = root_dir or os.path.dirname(os.path.abspath(__file__))
        self.persona: Dict[str, Any] = {}
        self.knowledge: Dict[str, Any] = {}
        self.manifest: Dict[str, Any] = {}
        self.initialized = False

    def load_core_files(self) -> bool:
        """Load all core CADE files."""
        try:
            # Load core configuration files
            self.persona = load_json("json/cade_persona.json")
            self.knowledge = load_json("json/cade_knowledgebases.json")
            self.manifest = load_json("json/cade_manifest.json")
            self.health_history = load_json("json/dawid_health_history.json")
            
            # Load initialization configuration
            self.config = load_ini("auto_init_cade.ini")
            
            self.initialized = True
            return True
            
        except Exception as e:
            print(f"Error loading CADE core files: {str(e)}")
            self.initialized = False
            return False

    def get_identity(self) -> Dict[str, Any]:
        """Get CADE's identity information."""
        return self.persona.get("identity", {})

    def get_directives(self) -> Dict[str, list]:
        """Get CADE's operational directives."""
        return self.persona.get("directives", {})

    def get_resurrection_protocol(self) -> Dict[str, Any]:
        """Get the resurrection protocol configuration."""
        return self.persona.get("resurrection_protocol", {})

    def is_initialized(self) -> bool:
        """Check if CADE core is properly initialized."""
        return self.initialized

    def get_status(self) -> Dict[str, Any]:
        """Get the current status of the CADE core."""
        return {
            "initialized": self.initialized,
            "identity_loaded": bool(self.persona.get("identity")),
            "directives_loaded": bool(self.persona.get("directives")),
            "knowledge_loaded": bool(self.knowledge),
            "manifest_loaded": bool(self.manifest)
        }


def initialize_cade() -> CadeCore:
    ""
    Initialize the CADE core system.
    
    Returns:
        CadeCore: Initialized CADE core instance
    """
    cade = CadeCore()
    if cade.load_core_files():
        print("CADE core initialized successfully.")
    else:
        print("Warning: CADE core initialization completed with errors.")
    
    return cade


# Initialize CADE when this module is imported
cade = initialize_cade()

# Add CADE to the global namespace when imported with "from cade_core import *"
__all__ = ['CadeCore', 'cade', 'initialize_cade']
