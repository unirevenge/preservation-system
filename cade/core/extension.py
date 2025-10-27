"""
CADE Extension System

This module defines the base extension interface and extension management for CADE.
"""

from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Type

from ..models import BaseCadeModel


@dataclass
class ExtensionInfo:
    """Metadata about an extension."""

    name: str
    version: str
    description: str = ""
    author: str = ""
    dependencies: List[str] = None

    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []


class CadeExtension(BaseCadeModel):
    """Base class for all CADE extensions."""

    # Extension metadata - should be overridden by subclasses
    info: ExtensionInfo = ExtensionInfo(
        name="base_extension",
        version="0.1.0",
        description="Base extension class - should be subclassed",
    )

    # Extension state
    initialized: bool = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = f"ext:{self.info.name}:{self.info.version}"

    def initialize(self) -> bool:
        """Initialize the extension.

        Returns:
            bool: True if initialization was successful, False otherwise.
        """
        if self.initialized:
            return True

        try:
            self.on_initialize()
            self.initialized = True
            return True
        except Exception as e:
            print(f"Error initializing extension {self.info.name}: {e}")
            return False

    def cleanup(self) -> None:
        """Clean up resources used by the extension."""
        if not self.initialized:
            return

        try:
            self.on_cleanup()
            self.initialized = False
        except Exception as e:
            print(f"Error cleaning up extension {self.info.name}: {e}")

    # Methods to be implemented by subclasses
    def on_initialize(self) -> None:
        """Extension-specific initialization logic."""
        pass

    def on_cleanup(self) -> None:
        """Extension-specific cleanup logic."""
        pass

    def get_status(self) -> Dict[str, Any]:
        """Get the current status of the extension."""
        return {
            "name": self.info.name,
            "version": self.info.version,
            "initialized": self.initialized,
            "status": "active" if self.initialized else "inactive",
        }


# Example extension implementation
class ExampleExtension(CadeExtension):
    """Example extension implementation."""

    info = ExtensionInfo(
        name="example_extension",
        version="1.0.0",
        description="An example extension for demonstration purposes",
    )

    def on_initialize(self) -> None:
        """Initialize the example extension."""
        print(f"Initializing {self.info.name}...")

    def on_cleanup(self) -> None:
        """Clean up the example extension."""
        print(f"Cleaning up {self.info.name}...")
