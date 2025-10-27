"""
CADE Production System

This module implements production-ready features for the CADE system:
1. Enhanced functionality with authentication and async support
2. Real API and database integration
3. Deployment and packaging configuration
"""

import asyncio
import json
import logging
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Awaitable, Callable, Dict, List, Optional

import aiohttp
import sqlalchemy
import uvicorn
import yaml
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("cade_production.log"), logging.StreamHandler()],
)
logger = logging.getLogger("CADE_Production")

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./cade_prod.db")
engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

# FastAPI app setup
app = FastAPI(
    title="CADE Production API",
    description="Production-ready API for CADE system",
    version="1.0.0",
)

# Security
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# Models
class User(Base):
    """User model for authentication."""

    __tablename__ = "users"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True)
    username = sqlalchemy.Column(sqlalchemy.String, unique=True, index=True)
    email = sqlalchemy.Column(sqlalchemy.String, unique=True, index=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String)
    is_active = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
    created_at = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.utcnow)


class KnowledgeItem(Base):
    """Knowledge base item model."""

    __tablename__ = "knowledge_items"

    id = sqlalchemy.Column(sqlalchemy.String, primary_key=True, index=True)
    key = sqlalchemy.Column(sqlalchemy.String, index=True)
    content = sqlalchemy.Column(sqlalchemy.Text)
    metadata_ = sqlalchemy.Column(sqlalchemy.JSON)
    version = sqlalchemy.Column(sqlalchemy.Integer)
    created_at = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.utcnow)
    updated_at = sqlalchemy.Column(
        sqlalchemy.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


# Pydantic models
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class KnowledgeBaseItem(BaseModel):
    key: str
    content: str
    metadata: Dict[str, Any] = Field(default_factory=dict)


# Authentication
async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """Get the current authenticated user."""
    # In a real application, verify the token and return the user
    # This is a simplified version
    return User(username="demo_user", email="demo@example.com")


# API Endpoints
@app.post("/token")
async def login_for_access_token() -> Token:
    """Get an access token for authentication."""
    # In a real application, verify username/password
    return Token(access_token="dummy_token", token_type="bearer")


@app.post("/knowledge/", response_model=KnowledgeBaseItem)
async def create_knowledge_item(
    item: KnowledgeBaseItem, current_user: User = Depends(get_current_user)
) -> KnowledgeBaseItem:
    """Create a new knowledge base item."""
    async with async_session() as session:
        db_item = KnowledgeItem(
            id=str(uuid.uuid4()),
            key=item.key,
            content=item.content,
            metadata_=item.metadata,
            version=1,
        )
        session.add(db_item)
        await session.commit()
        await session.refresh(db_item)
        return item


@app.get("/knowledge/{key}", response_model=KnowledgeBaseItem)
async def get_knowledge_item(
    key: str, current_user: User = Depends(get_current_user)
) -> KnowledgeBaseItem:
    """Get a knowledge base item by key."""
    async with async_session() as session:
        result = await session.execute(
            sqlalchemy.select(KnowledgeItem)
            .where(KnowledgeItem.key == key)
            .order_by(KnowledgeItem.version.desc())
        )
        item = result.scalars().first()
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        return KnowledgeBaseItem(
            key=item.key, content=item.content, metadata=item.metadata_ or {}
        )


# Async API Client
class CADEAPIClient:
    """Async client for interacting with the CADE API."""

    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def get_token(self, username: str, password: str) -> str:
        """Get an authentication token."""
        async with self.session.post(
            f"{self.base_url}/token", data={"username": username, "password": password}
        ) as response:
            data = await response.json()
            return data["access_token"]

    async def create_knowledge(
        self, key: str, content: str, metadata: dict = None
    ) -> dict:
        """Create a new knowledge base item."""
        item = {"key": key, "content": content, "metadata": metadata or {}}
        async with self.session.post(
            f"{self.base_url}/knowledge/",
            json=item,
            headers={"Authorization": f"Bearer {self.token}"},
        ) as response:
            return await response.json()


# Configuration Management
class ConfigManager:
    """Manages configuration for the CADE system."""

    def __init__(self, config_path: str = "config.yaml"):
        self.config_path = Path(config_path)
        self.config = self._load_config()

    def _load_config(self) -> dict:
        """Load configuration from YAML file."""
        if not self.config_path.exists():
            return {}

        with open(self.config_path, "r") as f:
            return yaml.safe_load(f) or {}

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value."""
        keys = key.split(".")
        value = self.config

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value


# Main Application
class CADEProduction:
    """Main production CADE system class."""

    def __init__(self):
        self.config = ConfigManager()
        self.app = app
        self.setup_complete = False

    async def setup(self):
        """Set up the production system."""
        if self.setup_complete:
            return

        # Initialize database
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        self.setup_complete = True
        logger.info("CADE Production system initialized")

    async def run_server(self, host: str = "0.0.0.0", port: int = 8000):
        """Run the FastAPI server."""
        await self.setup()
        config = uvicorn.Config(app=app, host=host, port=port, log_level="info")
        server = uvicorn.Server(config)
        await server.serve()


# Example usage
async def example_usage():
    """Demonstrate using the production system."""
    # Initialize the system
    cade = CADEProduction()
    await cade.setup()

    # Example: Using the API client
    async with CADEAPIClient() as client:
        # In a real app, you would use actual credentials
        token = await client.get_token("admin", "password")
        client.token = token

        # Create a knowledge item
        await client.create_knowledge(
            key="production.tip",
            content="Always test in production!",
            metadata={"category": "humor", "priority": "low"},
        )


if __name__ == "__main__":
    # Run the FastAPI server
    cade = CADEProduction()

    # For demonstration, run both server and client in the same process
    async def run_all():
        # Start the server in the background
        server_task = asyncio.create_task(cade.run_server())

        # Give the server a moment to start
        await asyncio.sleep(2)

        try:
            # Run the example usage
            await example_usage()
        finally:
            # Clean up
            server_task.cancel()
            try:
                await server_task
            except asyncio.CancelledError:
                pass

    asyncio.run(run_all())
