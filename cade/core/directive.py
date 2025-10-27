"""
CADE Directive System

This module defines the directive interface and directive management for CADE.
"""

from typing import Dict, Any, Optional, List, Type, Callable, TypeVar, Generic
from dataclasses import dataclass
from pydantic import BaseModel, Field
from ..models import BaseCadeModel

# Type variable for directive result
try:
    from typing import TypeVar
    T = TypeVar('T')
except ImportError:
    T = Any

class DirectiveResult(BaseModel):
    """Result of executing a directive."""
    success: bool = Field(..., description="Whether the directive executed successfully")
    message: str = Field("", description="Result message or error description")
    data: Dict[str, Any] = Field(default_factory=dict, description="Additional result data")
    
    @classmethod
    def success_result(cls, message: str = "", **data) -> 'DirectiveResult':
        """Create a successful result."""
        return cls(success=True, message=message, data=data)
    
    @classmethod
    def error_result(cls, message: str = "", **data) -> 'DirectiveResult':
        """Create an error result."""
        return cls(success=False, message=message, data=data)

class Directive(BaseCadeModel, Generic[T]):
    """Base class for CADE directives.
    
    Directives are named commands or actions that can be executed by the system.
    """
    
    name: str = Field(..., description="Unique name of the directive")
    description: str = Field("", description="Description of what the directive does")
    requires: List[str] = Field(default_factory=list, description="List of required permissions")
    
    async def execute(self, **kwargs) -> DirectiveResult:
        """Execute the directive with the given arguments.
        
        Args:
            **kwargs: Arguments specific to the directive.
            
        Returns:
            DirectiveResult: The result of executing the directive.
        """
        try:
            result = await self._execute(**kwargs)
            if isinstance(result, DirectiveResult):
                return result
            return DirectiveResult.success_result("Directive executed successfully", result=result)
        except Exception as e:
            return DirectiveResult.error_result(f"Error executing directive: {str(e)}")
    
    async def _execute(self, **kwargs) -> Any:
        """Subclasses should implement this method to provide directive-specific logic."""
        raise NotImplementedError("Subclasses must implement _execute method")

# Example directive implementation
class ExampleDirective(Directive):
    """Example directive that demonstrates the directive system."""
    
    name = "example"
    description = "An example directive that echoes back the input"
    
    async def _execute(self, text: str = "", **kwargs) -> str:
        """Echo back the input text."""
        return f"Echo: {text}"
