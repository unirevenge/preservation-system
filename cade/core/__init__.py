"""
CADE Core Package

This package contains the core functionality of the CADE system.
"""

from .cade import CadeCore, initialize_cade, main
from .directive import Directive, DirectiveResult
from .extension import CadeExtension, ExtensionInfo
from .plugin import CadePlugin, PluginInfo

__all__ = [
    "CadeCore",
    "CadePlugin",
    "PluginInfo",
    "CadeExtension",
    "ExtensionInfo",
    "Directive",
    "DirectiveResult",
    "initialize_cade",
    "main",
]
