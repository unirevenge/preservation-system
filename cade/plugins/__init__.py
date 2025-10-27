"""
CADE Plugins Package

This package contains all the plugin implementations for the CADE system.
"""

from typing import Dict, Type, Optional
from ..core.plugin import CadePlugin, PluginInfo

# This will be populated with available plugins
PLUGINS: Dict[str, Type[CadePlugin]] = {}

def register_plugin(plugin_class: Type[CadePlugin]) -> bool:
    """Register a plugin class."""
    if not issubclass(plugin_class, CadePlugin):
        return False
    
    plugin_info = getattr(plugin_class, 'info', None)
    if not isinstance(plugin_info, PluginInfo):
        return False
    
    PLUGINS[plugin_info.name] = plugin_class
    return True

def get_plugin(name: str) -> Optional[Type[CadePlugin]]:
    """Get a registered plugin by name."""
    return PLUGINS.get(name)

__all__ = ['CadePlugin', 'PluginInfo', 'register_plugin', 'get_plugin']
