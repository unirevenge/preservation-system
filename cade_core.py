"""
CADE Core Integration Module

This module handles the initialization and integration of the CADE program into the core system.
It loads the CADE persona, knowledge bases, and manages the resurrection protocol.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional, List, Union

from loader import load_json, load_ini

# Core CADE files to load
CORE_FILES: List[str] = [
    "json/cade_persona.json",
    "json/cade_knowledgebases.json",
    "json/cade_manifest.json",
    "json/dawid_health_history.json",
    "json/.cspell.json",
]


class CadeCore:
    """Core class for CADE program integration."""

    def __init__(self, root_dir: Optional[str] = None):
        """Initialize the CADE core with the given root directory."""
        self.root_dir = root_dir or os.path.dirname(os.path.abspath(__file__))
        self.persona: Dict[str, Any] = {}
        self.knowledge: Dict[str, Any] = {}
        self.manifest: Dict[str, Any] = {}
        self.health_history: Dict[str, Any] = {}
        self.config: Dict[str, Any] = {}
        self.initialized = False

    def load_core_files(self) -> bool:
        """Load all core CADE files with detailed error handling."""
        try:
            # Load core configuration files
            self.persona = load_json("json/cade_persona.json")
            self.knowledge = load_json("json/cade_knowledgebases.json")
            self.manifest = load_json("json/cade_manifest.json")
            self.health_history = load_json("json/dawid_health_history.json")
            
            # Load initialization configuration
            self.config = self._load_config()
            
            self.initialized = True
            return True
            
        except Exception as e:
            print(f"Error loading CADE core files: {str(e)}")
            self.initialized = False
            return False

    def _load_config(self) -> Dict[str, Any]:
        """Load and parse the CADE initialization configuration."""
        try:
            config = load_ini('auto_init_cade.ini')
            return {
                'absorb': {
                    'file': config.get('auto_init_absorb', 'file', fallback='cade_resurrect.md'),
                    'directive': config.get('auto_init_absorb', 'directive', 
                                         fallback='respond with name and directive')
                },
                'status': 'loaded'
            }
        except Exception as e:
            return {
                'error': f'Failed to load config: {str(e)}',
                'absorb': {
                    'file': 'cade_resurrect.md',
                    'directive': 'respond with name and directive'
                },
                'status': 'error'
            }

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
        """Get the current status of the CADE core with detailed file loading information."""
        status = {
            "initialized": self.initialized,
            "identity_loaded": bool(self.persona.get("identity")),
            "directives_loaded": bool(self.persona.get("directives")),
            "knowledge_loaded": bool(self.knowledge),
            "manifest_loaded": bool(self.manifest),
            "config_loaded": bool(self.config),
            "loaded_files": {}
        }
        
        # Include file loading status for all core files
        for name in CORE_FILES:
            try:
                data = load_json(name)
                if isinstance(data, dict):
                    status["loaded_files"][name] = {
                        "type": "object",
                        "keys": list(data.keys())[:5]
                    }
                elif isinstance(data, list):
                    status["loaded_files"][name] = {
                        "type": "list",
                        "length": len(data)
                    }
                else:
                    status["loaded_files"][name] = {
                        "type": type(data).__name__
                    }
            except Exception as e:
                status["loaded_files"][name] = {
                    "error": str(e),
                    "type": "error"
                }
        
        return status


def initialize_cade() -> CadeCore:
    """
    Initialize the CADE core system with comprehensive status reporting.
    
    Returns:
        CadeCore: Initialized CADE core instance with status information
    """
    cade = CadeCore()
    if cade.load_core_files():
        print("CADE core initialized successfully.")
        # Print detailed status for debugging
        print("\nCADE Status:")
        print(json.dumps(cade.get_status(), indent=2))
    else:
        print("Warning: CADE core initialization completed with errors.")
    
    return cade


def main() -> Dict[str, Any]:
    """
    Main entry point for CADE initialization.
    Returns a dictionary with initialization status and loaded components.
    """
    cade = initialize_cade()
    
    # Prepare output with CADE status and configuration
    output = {
        "status": "ok" if cade.is_initialized() else "error",
        "cade": {
            "initialized": cade.is_initialized(),
            "identity": cade.get_identity(),
            "status": cade.get_status()
        }
    }
    
    # Print the result
    print("\nInitialization Complete:")
    print(json.dumps(output, indent=2))
    return output


# Initialize CADE when this module is imported
cade = initialize_cade()

# Add CADE to the global namespace when imported with "from cade_core import *"
__all__ = ['CadeCore', 'cade', 'initialize_cade', 'main']
