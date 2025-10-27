"""
CADE Interface Module

Provides a simplified interface for interacting with the CADE memory system.
This module wraps the core functionality into easy-to-use functions.
"""

from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from cade_memory import cade_memory

# Alias for easier access
mem = cade_memory


def say(text: str, role: str = "assistant", metadata: Optional[Dict] = None) -> None:
    """
    Add a message to the conversation history.

    Args:
        text: The message text
        role: Either 'user' or 'assistant'
        metadata: Optional additional metadata to store with the message
    """
    cade_memory.add_conversation_turn(role, text, metadata or {})


def remember(key: str, value: Any) -> None:
    """
    Store a value in the context memory.

    Args:
        key: The key to store the value under
        value: The value to store (must be JSON-serializable)
    """
    cade_memory.update_context(key, value)


def recall(key: str, default: Any = None) -> Any:
    """
    Retrieve a value from the context memory.

    Args:
        key: The key to retrieve
        default: Default value if key doesn't exist

    Returns:
        The stored value or default if not found
    """
    return cade_memory.get_context(key, default)


def get_identity() -> Dict[str, Any]:
    """Get CADE's identity information."""
    return cade_memory.get_identity()


def get_directives() -> Dict[str, list]:
    """Get CADE's operational directives."""
    return cade_memory.get_directives()


def get_status() -> Dict[str, Any]:
    """Get the current status of the CADE system."""
    return cade_memory.get_status()


def get_conversation(limit: int = 10) -> List[Dict[str, Any]]:
    """
    Get recent conversation history.

    Args:
        limit: Maximum number of turns to return

    Returns:
        List of conversation turns, most recent last
    """
    return cade_memory.get_recent_conversation(limit)


# Example usage
if __name__ == "__main__":
    # Example conversation
    say("Hello, I'm CADE. How can I help you today?", "assistant")
    say("What can you do?", "user", {"source": "example"})

    # Remember some context
    remember("current_task", "explaining capabilities")

    # Print conversation
    print("=== Conversation ===")
    for turn in get_conversation():
        print(f"{turn['role'].title()}: {turn['content']}")

    # Show current task
    print("\nCurrent task:", recall("current_task"))

    # Show system status
    status = get_status()
    print(f"\nSystem status: {status['core_initialized']}")
    print(f"Memory directory: {status['memory_dir']}")
