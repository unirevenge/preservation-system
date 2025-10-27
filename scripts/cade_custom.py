"""
CADE Custom Integration Example

This script demonstrates how to extend the CADE system with custom functionality,
including adding new knowledge, creating custom directives, and integrating
with external services.
"""

import logging
from datetime import datetime
from typing import Any, Dict

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("cade_custom.log"), logging.StreamHandler()],
)
logger = logging.getLogger("CADE_Custom")


class CadeCustom:
    """Custom CADE integration and extension class."""

    def __init__(self):
        self.knowledge_base = {}
        self.custom_directives = {}
        self.initialized = False

    def initialize(self) -> bool:
        """Initialize the custom CADE integration."""
        try:
            # Load any required configuration
            self._load_config()

            # Initialize knowledge base
            self._init_knowledge_base()

            # Register custom directives
            self._register_directives()

            self.initialized = True
            logger.info("CADE Custom integration initialized successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to initialize CADE Custom: {e}")
            return False

    def _load_config(self) -> None:
        """Load configuration for the custom integration."""
        self.config = {
            "version": "1.0.0",
            "last_updated": datetime.now().isoformat(),
            "features": ["knowledge_base", "custom_directives"],
        }

    def _init_knowledge_base(self) -> None:
        """Initialize the custom knowledge base."""
        # Example knowledge - in a real application, this would load from files/database
        self.knowledge_base = {
            "system": {
                "name": "CADE Custom Integration",
                "purpose": "Demonstrate extending CADE with custom functionality",
                "version": self.config["version"],
            },
            "directives": {
                "search": "Search the knowledge base",
                "add_knowledge": "Add new knowledge to the system",
                "list_directives": "List all available custom directives",
            },
            "examples": {
                "search": "search knowledge about Python",
                "add_knowledge": 'add_knowledge key="new_topic" content="Information about the topic"',
                "list_directives": "list_directives",
            },
        }

    def _register_directives(self) -> None:
        """Register custom directives."""
        self.custom_directives = {
            "search": self._handle_search,
            "add_knowledge": self._handle_add_knowledge,
            "list_directives": self._handle_list_directives,
        }

    def _handle_search(self, query: str) -> Dict[str, Any]:
        """Handle search directive."""
        results = []
        query = query.lower()

        def search_dict(d, path=""):
            for k, v in d.items():
                current_path = f"{path}.{k}" if path else k
                if isinstance(v, dict):
                    search_dict(v, current_path)
                elif isinstance(v, str) and query in v.lower():
                    results.append(
                        {
                            "path": current_path,
                            "content": v[:150] + "..." if len(v) > 150 else v,
                        }
                    )

        search_dict(self.knowledge_base)
        return {
            "query": query,
            "result_count": len(results),
            "results": results[:5],  # Return first 5 results
        }

    def _handle_add_knowledge(self, key: str, content: str) -> Dict[str, Any]:
        """Handle add_knowledge directive."""
        try:
            # In a real application, you would validate and sanitize the input
            keys = key.split(".")
            current = self.knowledge_base

            for k in keys[:-1]:
                if k not in current:
                    current[k] = {}
                current = current[k]

            current[keys[-1]] = content

            return {
                "status": "success",
                "message": f"Added knowledge at {key}",
                "key": key,
            }
        except Exception as e:
            return {"status": "error", "message": str(e), "key": key}

    def _handle_list_directives(self) -> Dict[str, Any]:
        """Handle list_directives directive."""
        return {
            "directives": list(self.custom_directives.keys()),
            "count": len(self.custom_directives),
        }

    def process_directive(self, directive: str, *args, **kwargs) -> Dict[str, Any]:
        """Process a custom directive."""
        if directive not in self.custom_directives:
            return {"status": "error", "message": f"Unknown directive: {directive}"}

        try:
            return self.custom_directives[directive](*args, **kwargs)
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error processing directive {directive}: {e!s}",
            }


def main():
    """Main function to demonstrate the custom CADE integration."""
    print("🚀 Starting CADE Custom Integration...\n")

    # Initialize the custom integration
    cade_custom = CadeCustom()
    if not cade_custom.initialize():
        print("❌ Failed to initialize CADE Custom integration")
        return

    print("✅ CADE Custom integration initialized successfully\n")

    # Example 1: List available directives
    print("📋 Available Directives:")
    result = cade_custom.process_directive("list_directives")
    for i, directive in enumerate(result.get("directives", []), 1):
        print(f"  {i}. {directive}")

    # Example 2: Search the knowledge base
    print("\n🔍 Searching knowledge base for 'directive':")
    search_result = cade_custom.process_directive("search", "directive")
    print(f"Found {search_result.get('result_count', 0)} results:")
    for i, item in enumerate(search_result.get("results", []), 1):
        print(f"  {i}. [{item['path']}] {item['content']}")

    # Example 3: Add new knowledge
    print("\n+ Adding new knowledge:")
    add_result = cade_custom.process_directive(
        "add_knowledge",
        key="custom.integration.example",
        content="This is an example of adding custom knowledge to CADE",
    )
    print(f"Status: {add_result.get('status', 'unknown')}")
    print(f"Message: {add_result.get('message', 'No message')}")

    # Verify the new knowledge was added
    print("\n🔍 Verifying new knowledge:")
    verify_result = cade_custom.process_directive("search", "example of adding")
    for item in verify_result.get("results", []):
        print(f"- {item['path']}: {item['content']}")

    print("\n✨ CADE Custom Integration Demo Complete!")


if __name__ == "__main__":
    main()
