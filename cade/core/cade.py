"""
CADE Core Module

This module contains the main CADE core class that ties together all the components.
"""

import asyncio
import logging
from typing import Dict, Any, Optional, List, Type, Callable, TypeVar, Union
from pathlib import Path
import json
import importlib
import sys

from ..models import BaseCadeModel
from .plugin import CadePlugin, PluginInfo
from .extension import CadeExtension, ExtensionInfo
from .directive import Directive, DirectiveResult
from ..utils import logger, load_json, save_json

# Type variables
T = TypeVar('T')

class CadeCore:
    """Main CADE core class that manages plugins, extensions, and directives."""
    
    def __init__(self):
        self.initialized = False
        self.plugins: Dict[str, CadePlugin] = {}
        self.extensions: Dict[str, CadeExtension] = {}
        self.directives: Dict[str, Directive] = {}
        self.config: Dict[str, Any] = {}
        
        # Set up logging
        self.logger = logger
        
    async def initialize(self, config_path: Optional[str] = None) -> bool:
        """Initialize the CADE core.
        
        Args:
            config_path: Optional path to a configuration file.
            
        Returns:
            bool: True if initialization was successful, False otherwise.
        """
        if self.initialized:
            self.logger.warning("CADE core is already initialized")
            return True
            
        try:
            self.logger.info("Initializing CADE core...")
            
            # Load configuration
            if config_path:
                self.config = self._load_config(config_path)
            
            # Initialize built-in components
            await self._initialize_builtins()
            
            # Load and initialize plugins
            await self._load_plugins()
            
            # Load and initialize extensions
            await self._load_extensions()
            
            # Register built-in directives
            self._register_builtin_directives()
            
            self.initialized = True
            self.logger.info("CADE core initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize CADE core: {e}", exc_info=True)
            return False
    
    async def shutdown(self) -> None:
        """Shut down the CADE core and clean up resources."""
        if not self.initialized:
            return
            
        self.logger.info("Shutting down CADE core...")
        
        # Clean up extensions
        for ext in list(self.extensions.values()):
            try:
                ext.cleanup()
            except Exception as e:
                self.logger.error(f"Error cleaning up extension {ext.info.name}: {e}")
        
        # Clean up plugins
        for plugin in list(self.plugins.values()):
            try:
                plugin.cleanup()
            except Exception as e:
                self.logger.error(f"Error cleaning up plugin {plugin.info.name}: {e}")
        
        self.initialized = False
        self.logger.info("CADE core shutdown complete")
    
    async def execute_directive(self, name: str, **kwargs) -> DirectiveResult:
        """Execute a directive by name.
        
        Args:
            name: Name of the directive to execute.
            **kwargs: Arguments to pass to the directive.
            
        Returns:
            DirectiveResult: The result of executing the directive.
        """
        if not self.initialized:
            return DirectiveResult.error_result("CADE core is not initialized")
            
        directive = self.directives.get(name)
        if not directive:
            return DirectiveResult.error_result(f"Unknown directive: {name}")
            
        try:
            self.logger.debug(f"Executing directive: {name} with args: {kwargs}")
            result = await directive.execute(**kwargs)
            return result
        except Exception as e:
            self.logger.error(f"Error executing directive {name}: {e}", exc_info=True)
            return DirectiveResult.error_result(f"Error executing directive: {str(e)}")
    
    def register_plugin(self, plugin: CadePlugin) -> bool:
        """Register a plugin with the CADE core.
        
        Args:
            plugin: The plugin to register.
            
        Returns:
            bool: True if registration was successful, False otherwise.
        """
        if not isinstance(plugin, CadePlugin):
            self.logger.error(f"Invalid plugin type: {type(plugin).__name__}")
            return False
            
        if plugin.info.name in self.plugins:
            self.logger.warning(f"Plugin '{plugin.info.name}' is already registered")
            return False
            
        try:
            if plugin.initialize():
                self.plugins[plugin.info.name] = plugin
                self.logger.info(f"Registered plugin: {plugin.info.name} v{plugin.info.version}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error initializing plugin {plugin.info.name}: {e}")
            return False
    
    def register_extension(self, extension: CadeExtension) -> bool:
        """Register an extension with the CADE core.
        
        Args:
            extension: The extension to register.
            
        Returns:
            bool: True if registration was successful, False otherwise.
        """
        if not isinstance(extension, CadeExtension):
            self.logger.error(f"Invalid extension type: {type(extension).__name__}")
            return False
            
        if extension.info.name in self.extensions:
            self.logger.warning(f"Extension '{extension.info.name}' is already registered")
            return False
            
        try:
            if extension.initialize():
                self.extensions[extension.info.name] = extension
                self.logger.info(f"Registered extension: {extension.info.name} v{extension.info.version}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error initializing extension {extension.info.name}: {e}")
            return False
    
    def register_directive(self, directive: Directive) -> bool:
        """Register a directive with the CADE core.
        
        Args:
            directive: The directive to register.
            
        Returns:
            bool: True if registration was successful, False otherwise.
        """
        if not isinstance(directive, Directive):
            self.logger.error(f"Invalid directive type: {type(directive).__name__}")
            return False
            
        if directive.name in self.directives:
            self.logger.warning(f"Directive '{directive.name}' is already registered")
            return False
            
        self.directives[directive.name] = directive
        self.logger.debug(f"Registered directive: {directive.name}")
        return True
    
    def get_status(self) -> Dict[str, Any]:
        """Get the current status of the CADE core."""
        return {
            "initialized": self.initialized,
            "plugins": {name: plugin.get_status() for name, plugin in self.plugins.items()},
            "extensions": {name: ext.get_status() for name, ext in self.extensions.items()},
            "directives": list(self.directives.keys()),
            "config": {"loaded": bool(self.config)}
        }
    
    # Internal methods
    
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from a file."""
        try:
            config = load_json(config_path)
            if not isinstance(config, dict):
                self.logger.warning(f"Invalid configuration format in {config_path}")
                return {}
            return config
        except Exception as e:
            self.logger.error(f"Error loading configuration from {config_path}: {e}")
            return {}
    
    async def _initialize_builtins(self) -> None:
        """Initialize built-in components."""
        # This method can be used to initialize any built-in components
        pass
    
    async def _load_plugins(self) -> None:
        """Load and initialize plugins."""
        # This would typically scan a plugins directory and load plugins
        # For now, we'll just log that we're loading plugins
        self.logger.debug("Loading plugins...")
    
    async def _load_extensions(self) -> None:
        """Load and initialize extensions."""
        # This would typically scan an extensions directory and load extensions
        # For now, we'll just log that we're loading extensions
        self.logger.debug("Loading extensions...")
    
    def _register_builtin_directives(self) -> None:
        """Register built-in directives."""
        # This would register any built-in directives
        self.logger.debug("Registering built-in directives...")

def initialize_cade(config_path: Optional[str] = None) -> CadeCore:
    """Initialize and return a new CADE core instance.
    
    Args:
        config_path: Optional path to a configuration file.
        
    Returns:
        CadeCore: An initialized CADE core instance.
    """
    async def _init():
        cade = CadeCore()
        await cade.initialize(config_path)
        return cade
    
    # For simplicity, we're using asyncio.run here, but in a real application,
    # you'd want to manage the event loop more carefully
    return asyncio.run(_init())

async def main() -> None:
    """Main entry point for the CADE core."""
    cade = CadeCore()
    await cade.initialize()
    
    try:
        # Here you would typically start your application's main loop
        print("CADE core is running. Press Ctrl+C to exit.")
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        await cade.shutdown()

if __name__ == "__main__":
    asyncio.run(main())
