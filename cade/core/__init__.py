"""
CADE Core Package

This package contains the core functionality of the CADE system.
"""

from .plugin import CadePlugin, PluginInfo
from .extension import CadeExtension, ExtensionInfo
from .directive import Directive, DirectiveResult
from .cade import CadeCore, initialize_cade, main

__all__ = [
    'CadeCore',
    'CadePlugin',
    'PluginInfo',
    'CadeExtension',
    'ExtensionInfo',
    'Directive',
    'DirectiveResult',
    'initialize_cade',
    'main'
]
