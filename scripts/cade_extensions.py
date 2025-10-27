"""
CADE System Extensions

This module demonstrates how to extend the CADE system with custom functionality,
including new modules, directives, and integrations.
"""

import json
import logging
import os
import sys
from pathlib import Path
from typing import Any, Callable, Dict, List

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import CADE core
from cade_core import cade

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("cade_system.log"), logging.StreamHandler()],
)
logger = logging.getLogger("CADE_Extensions")


class CadeExtensionManager:
    """Manages CADE system extensions and plugins."""

    def __init__(self):
        self.extensions: Dict[str, Dict[str, Any]] = {}
        self.custom_directives: Dict[str, Dict[str, Any]] = {}
        self.initialized = False

    def register_extension(
        self, name: str, version: str, description: str = ""
    ) -> bool:
        """Register a new extension with the CADE system."""
        if name in self.extensions:
            logger.warning(f"Extension '{name}' is already registered")
            return False

        self.extensions[name] = {
            "version": version,
            "description": description,
            "status": "registered",
        }
        logger.info(f"Registered extension: {name} v{version}")
        return True

    def register_directive(
        self, name: str, handler: Callable, category: str = "custom"
    ) -> bool:
        """Register a custom directive handler."""
        if not callable(handler):
            logger.error(f"Handler for directive '{name}' is not callable")
            return False

        self.custom_directives[name] = {"handler": handler, "category": category}
        logger.info(f"Registered directive: {name} (category: {category})")
        return True

    def initialize(self) -> bool:
        """Initialize all registered extensions."""
        if not cade.is_initialized():
            logger.error("CADE core is not initialized")
            return False

        for ext_name, ext_data in self.extensions.items():
            try:
                # Here you would initialize each extension
                ext_data["status"] = "initialized"
                logger.debug(f"Initialized extension: {ext_name}")
            except Exception as e:
                ext_data["status"] = f"error: {e!s}"
                logger.error(f"Failed to initialize {ext_name}: {e}")

        self.initialized = True
        logger.info("CADE Extensions initialized successfully")
        return True

    def process_directive(self, directive: str, *args, **kwargs) -> Any:
        """Process a custom directive."""
        if directive not in self.custom_directives:
            logger.warning(f"No handler registered for directive: {directive}")
            return None

        handler_info = self.custom_directives[directive]
        try:
            result = handler_info["handler"](*args, **kwargs)
            logger.debug(f"Processed directive '{directive}' successfully")
            return result
        except Exception as e:
            logger.error(f"Error processing directive '{directive}': {e}")
            return None


# Example extension: Knowledge Base Manager
class KnowledgeBaseManager:
    """Manages knowledge base operations for the CADE system."""

    def __init__(self):
        self.knowledge_base = {}
        self.logger = logging.getLogger("CADE_KB_Manager")

    def load_knowledge(self, file_path: str) -> bool:
        """Load knowledge from a JSON file."""
        try:
            path = Path(file_path)
            with path.open(encoding="utf-8") as f:
                data = json.load(f)
                self.knowledge_base.update(data)
            self.logger.info(f"Loaded knowledge from {file_path}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to load knowledge: {e}")
            return False

    def query(self, query: str) -> List[Dict[str, Any]]:
        """Query the knowledge base."""
        # Simple text-based search (can be replaced with more sophisticated search)
        results = []
        query = query.lower()

        for key, value in self.knowledge_base.items():
            if isinstance(value, str) and query in value.lower():
                results.append({"key": key, "snippet": value[:100] + "..."})
            elif isinstance(value, dict):
                # Handle nested dictionaries
                for k, v in value.items():
                    if query in str(k).lower() or query in str(v).lower():
                        results.append(
                            {"key": f"{key}.{k}", "snippet": str(v)[:100] + "..."}
                        )

        self.logger.debug(f"Found {len(results)} results for query: {query}")
        return results


# Example usage
def setup_extensions():
    """Set up and register all extensions."""
    # Initialize the extension manager
    ext_manager = CadeExtensionManager()

    # Register the Knowledge Base Manager extension
    kb_manager = KnowledgeBaseManager()
    ext_manager.register_extension(
        name="KnowledgeBaseManager",
        version="1.0.0",
        description="Advanced knowledge base management for CADE",
    )

    # Register custom directives
    def search_kb(query: str) -> List[Dict[str, Any]]:
        """Search the knowledge base."""
        return kb_manager.query(query)

    ext_manager.register_directive(
        name="search_knowledge", handler=search_kb, category="knowledge"
    )

    # Initialize all extensions
    if ext_manager.initialize():
        logger.info("All extensions initialized successfully")
    else:
        logger.error("Failed to initialize some extensions")

    return ext_manager


def main():
    """Demonstrate the CADE extensions."""
    print("🚀 Setting up CADE Extensions...\n")

    # Example: Load some knowledge
    kb_manager = KnowledgeBaseManager()
    kb_manager.load_knowledge("json/cade_knowledgebases.json")

    # Example search
    print("🔍 Searching knowledge base...")
    results = kb_manager.query("memory")
    print(f"Found {len(results)} results:")
    for i, result in enumerate(results[:3], 1):  # Show first 3 results
        print(f"{i}. {result['key']}: {result['snippet']}")

    print("\n✨ CADE Extensions Demo Complete!")


if __name__ == "__main__":
    main()
