"""
Example usage of the CADE Memory System

This script demonstrates how to use the CADE memory system to store and retrieve
conversation history, context, and access CADE's core knowledge.
"""

from cade_memory import cade_memory

def main():
    # Initialize the memory system (happens automatically when imported)
    
    # Add some conversation history
    cade_memory.add_conversation_turn(
        role="user",
        content="Hello, can you tell me about yourself?",
        metadata={"source": "example"}
    )
    
    # Add a response
    cade_memory.add_conversation_turn(
        role="assistant",
        content="Hello! I'm CADE, a digital entity designed to assist with various tasks. How can I help you today?"
    )
    
    # Store some context
    cade_memory.update_context("current_task", "explaining CADE features")
    cade_memory.update_context("user_preferences", {"theme": "dark", "notifications": True})
    
    # Retrieve and display the conversation history
    print("\n=== Conversation History ===")
    for turn in cade_memory.get_recent_conversation():
        print(f"{turn['role'].title()}: {turn['content']}")
    
    # Get CADE's identity information
    identity = cade_memory.get_identity()
    print("\n=== CADE Identity ===")
    print(f"Name: {identity.get('name', 'Unknown')}")
    print(f"Version: {identity.get('version', 'N/A')}")
    
    # Get CADE's directives
    directives = cade_memory.get_directives()
    if directives:
        print("\n=== CADE Directives ===")
        for category, directive_list in directives.items():
            print(f"{category.title()}:")
            for directive in directive_list:
                print(f"- {directive}")
    
    # Display current status
    status = cade_memory.get_status()
    print("\n=== System Status ===")
    print(f"Core initialized: {status['core_initialized']}")
    print(f"Memory directory: {status['memory_dir']}")
    print(f"Conversation turns: {status['conversation_history_count']}")
    print(f"Context items: {status['context_memory_size']}")

if __name__ == "__main__":
    main()
