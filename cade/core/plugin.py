"""
CADE Plugin System

This module defines the base plugin interface and plugin management for CADE.
"""

from dataclasses import dataclass
from typing import Any, Dict, List

from ..models import BaseCadeModel


@dataclass
class PluginInfo:
    """Metadata about a plugin."""

    name: str
    version: str
    description: str = ""
    author: str = ""
    dependencies: List[str] = None

    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []


class CadePlugin(BaseCadeModel):
    """Base class for all CADE plugins."""

    # Plugin metadata - should be overridden by subclasses
    info: PluginInfo = PluginInfo(
        name="base_plugin",
        version="0.1.0",
        description="Base plugin class - should be subclassed",
    )

    # Plugin state
    initialized: bool = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = f"plugin:{self.info.name}:{self.info.version}"

    def initialize(self) -> bool:
        """Initialize the plugin.

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
            print(f"Error initializing plugin {self.info.name}: {e}")
            return False

    def cleanup(self) -> None:
        """Clean up resources used by the plugin."""
        if not self.initialized:
            return

        try:
            self.on_cleanup()
            self.initialized = False
        except Exception as e:
            print(f"Error cleaning up plugin {self.info.name}: {e}")

    # Methods to be implemented by subclasses
    def on_initialize(self) -> None:
        """Plugin-specific initialization logic."""
        pass

    def on_cleanup(self) -> None:
        """Plugin-specific cleanup logic."""
        pass

    def get_status(self) -> Dict[str, Any]:
        """Get the current status of the plugin."""
        return {
            "name": self.info.name,
            "version": self.info.version,
            "initialized": self.initialized,
            "status": "active" if self.initialized else "inactive",
        }


# Example plugin implementation
class ExamplePlugin(CadePlugin):
    """Example plugin implementation."""

    info = PluginInfo(
        name="example_plugin",
        version="1.0.0",
        description="An example plugin for demonstration purposes",
    )

    def on_initialize(self) -> None:
        """Initialize the example plugin."""
        print(f"Initializing {self.info.name}...")

    def on_cleanup(self) -> None:
        """Clean up the example plugin."""
        print(f"Cleaning up {self.info.name}...")
