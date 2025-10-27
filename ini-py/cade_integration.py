"""
CADE System Integration

This script demonstrates how to integrate and interact with the CADE core system.
"""

from cade_core import CadeCore, cade


def display_identity():
    """Display CADE's identity information."""
    identity = cade.get_identity()
    print("\n=== CADE Identity ===")
    print(f"Name: {identity.get('name', 'Unknown')}")
    print(f"Version: {identity.get('version', 'N/A')}")
    print(f"Description: {identity.get('description', 'No description available')}")


def display_directives():
    """Display available directives."""
    directives = cade.get_directives()
    print("\n=== Available Directives ===")
    for category, directive_list in directives.items():
        print(f"\n{category.upper()}:")
        for directive in directive_list:
            if isinstance(directive, dict):
                print(f"- {directive.get('name', 'Unnamed directive')}")
            else:
                print(f"- {directive}")

    # Print a warning if no directives were found
    if not any(directives.values()):
        print("\n⚠️  No directives found or directives format is unexpected.")


def display_system_status():
    """Display system status and health."""
    status = cade.get_status()
    print("\n=== System Status ===")
    print(f"Initialized: {'✅' if status.get('initialized') else '❌'}")
    print(f"Identity Loaded: {'✅' if status.get('identity_loaded') else '❌'}")
    print(f"Directives Loaded: {'✅' if status.get('directives_loaded') else '❌'}")
    print(f"Knowledge Loaded: {'✅' if status.get('knowledge_loaded') else '❌'}")
    print(f"Manifest Loaded: {'✅' if status.get('manifest_loaded') else '❌'}")


def main():
    """Main function to demonstrate CADE integration."""
    print("🚀 Initializing CADE Integration...")

    # Check if CADE is properly initialized
    if not cade.is_initialized():
        print("❌ Error: CADE core failed to initialize!")
        return

    print("\n✅ CADE Core is ready!")

    # Display system information
    display_identity()
    display_directives()
    display_system_status()

    print("\n✨ CADE Integration Demo Complete!")


if __name__ == "__main__":
    main()
