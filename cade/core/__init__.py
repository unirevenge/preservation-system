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
    "CadeExtension",
    "CadePlugin",
    "Directive",
    "DirectiveResult",
    "ExtensionInfo",
    "PluginInfo",
    "initialize_cade",
    "main",
]
