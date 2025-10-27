"""
CADE Extensions Package

This package contains extension modules that provide additional functionality
to the core CADE system.
"""

from typing import Dict, Optional, Type

from ..core.extension import CadeExtension, ExtensionInfo

# This will be populated with available extensions
EXTENSIONS: Dict[str, Type[CadeExtension]] = {}


def register_extension(extension_class: Type[CadeExtension]) -> bool:
    """Register an extension class."""
    if not issubclass(extension_class, CadeExtension):
        return False

    extension_info = getattr(extension_class, "info", None)
    if not isinstance(extension_info, ExtensionInfo):
        return False

    EXTENSIONS[extension_info.name] = extension_class
    return True


def get_extension(name: str) -> Optional[Type[CadeExtension]]:
    """Get a registered extension by name."""
    return EXTENSIONS.get(name)


__all__ = ["CadeExtension", "ExtensionInfo", "register_extension", "get_extension"]
