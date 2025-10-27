"""
CADE Usage Example

This module demonstrates practical usage of the CADE system's capabilities,
including knowledge base access and directive handling.
"""

import json
from typing import Any, Dict, List

from cade_core import cade


def explore_knowledge_bases() -> Dict[str, Any]:
    """Explore and return information about CADE's knowledge bases."""
    if not cade.is_initialized():
        return {"error": "CADE core is not initialized"}

    knowledge = cade.knowledge
    if not knowledge:
        return {"message": "No knowledge bases found", "status": "empty"}

    # Get basic information about knowledge bases
    kb_info: Dict[str, Any] = {
        "knowledge_bases": list(knowledge.keys()),
        "integrated_memory_size": len(knowledge.get("integrated_memory", [])),
        "sample_entries": {},
    }

    # Get sample entries from each knowledge base
    sample_entries: Dict[str, Any] = {}
    for kb_name, kb_data in knowledge.items():
        if isinstance(kb_data, list) and kb_data:
            sample_entries[kb_name] = kb_data[:3]  # First 3 entries
        elif isinstance(kb_data, dict) and kb_data:
            sample_entries[kb_name] = {
                k: v for i, (k, v) in enumerate(kb_data.items()) if i < 3
            }

    kb_info["sample_entries"] = sample_entries

    return kb_info


def get_system_health() -> Dict[str, Any]:
    """Get a comprehensive health check of the CADE system."""
    if not cade.is_initialized():
        return {"status": "error", "message": "CADE core is not initialized"}

    status = cade.get_status()
    health = {
        "status": "operational" if status.get("initialized") else "degraded",
        "components": {
            "core": status.get("initialized", False),
            "identity": status.get("identity_loaded", False),
            "directives": status.get("directives_loaded", False),
            "knowledge": status.get("knowledge_loaded", False),
            "manifest": status.get("manifest_loaded", False),
        },
        "config_loaded": status.get("config_loaded", False),
    }

    # Add any additional health checks here
    return health


def find_relevant_directives(query: str) -> List[Dict[str, Any]]:
    """
    Find directives relevant to a specific query.

    Args:
        query: The search query to find relevant directives

    Returns:
        List of matching directives with their categories
    """
    if not cade.is_initialized():
        return [{"error": "CADE core is not initialized"}]

    query = query.lower()
    directives = cade.get_directives()
    results = []

    for category, directive_list in directives.items():
        for directive in directive_list:
            # Handle both string and dictionary directives
            directive_text = (
                directive.lower()
                if isinstance(directive, str)
                else str(
                    directive.get("name", "") + " " + directive.get("description", "")
                ).lower()
            )

            if query in directive_text:
                results.append(
                    {
                        "category": category,
                        "directive": (
                            directive if isinstance(directive, str) else dict(directive)
                        ),
                    }
                )

    return results


def main():
    """Main function to demonstrate CADE system usage."""
    print("🔍 Exploring CADE System Capabilities\n")

    # 1. Check system health
    print("🩺 System Health Check:")
    health = get_system_health()
    print(json.dumps(health, indent=2))

    # 2. Explore knowledge bases
    print("\n📚 Knowledge Base Overview:")
    kb_info = explore_knowledge_bases()
    print(f"Found {len(kb_info.get('knowledge_bases', []))} knowledge bases")
    print(
        f"Total entries in integrated memory: {kb_info.get('integrated_memory_size', 0)}"
    )

    # 3. Search directives
    print("\n🔍 Searching directives related to 'emotion':")
    emotion_directives = find_relevant_directives("emotion")
    print(f"Found {len(emotion_directives)} relevant directives")

    for i, directive in enumerate(emotion_directives[:3], 1):  # Show first 3
        print(f"\n  {i}. {directive['category']}:")
        print(f"     {directive['directive']}")

    print("\n✨ CADE Usage Example Complete!")


if __name__ == "__main__":
    main()
