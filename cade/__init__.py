"""
CADE (Context-Aware Development Environment) Core Package

This package provides the core functionality for the CADE system,
including initialization, plugin management, and core utilities.
"""

from .core import CadeCore, initialize_cade, main
from .version import __version__

# Initialize CADE when this package is imported
cade = initialize_cade()

__all__ = ["CadeCore", "__version__", "cade", "initialize_cade", "main"]
