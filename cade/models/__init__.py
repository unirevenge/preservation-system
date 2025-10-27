"""
CADE Models Package

This package contains data models and schemas used throughout the CADE system.
"""

from datetime import datetime
from typing import Any, ClassVar, Dict

from pydantic import BaseModel, Field


class BaseCadeModel(BaseModel):
    """Base model for all CADE data models."""

    id: str = Field(..., description="Unique identifier for the model instance")
    created_at: str = Field(default_factory=lambda: str(datetime.utcnow().isoformat()))
    updated_at: str = Field(default_factory=lambda: str(datetime.utcnow().isoformat()))

    class Config:
        json_encoders: ClassVar[Dict[str, Any]] = {
            "datetime": lambda v: v.isoformat() if hasattr(v, "isoformat") else str(v)
        }
        extra = "ignore"


# Import all models here to make them available when importing from cade.models
# These imports are commented out until the modules are created
# from .knowledge import KnowledgeItem, KnowledgeBase
# from .directive import Directive, DirectiveResult
# from .plugin import PluginConfig, PluginState

# Export all models
__all__ = [
    "BaseCadeModel",
    # 'KnowledgeItem',
    # 'KnowledgeBase',
    # 'Directive',
    # 'DirectiveResult',
    # 'PluginConfig',
    # 'PluginState'
]
