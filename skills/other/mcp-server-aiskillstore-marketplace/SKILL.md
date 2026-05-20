---
name: mcp-server
description: Generic MCP (Model Context Protocol) server development patterns. Provides reusable architecture and best practices for building MCP servers that expose any domain-specific operations as tools for AI agents. Framework-agnostic implementation supporting async operations, error handling, and enterprise-grade features.
license: MIT
---

# Generic MCP Server Development

This skill provides comprehensive patterns and reusable code for building MCP (Model Context Protocol) servers that can expose any domain operations as tools for AI agents. Follows 2025 best practices for performance, security, and maintainability.

## When to Use This Skill

Use this skill when you need to:
- Build an MCP server for any domain (not just todos)
- Expose database operations as MCP tools
- Create AI-agent accessible APIs
- Implement async MCP tool handlers
- Add proper error handling and validation
- Support rate limiting and caching
- Build enterprise-grade MCP servers
- Integrate with multiple storage backends

## 1. Generic MCP Server Architecture

```python
# mcp_server/core.py
#!/usr/bin/env python3
"""
Generic MCP Server Base Architecture
Provides reusable patterns for any MCP server implementation
"""

import asyncio
import json
import logging
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Sequence, Union, Callable
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from enum import Enum

import redis.asyncio as redis
from mcp.server import Server, NotificationOptions, stdio
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    Resource, Tool, TextContent, ImageContent, EmbeddedResource,
    LoggingLevel, CallToolRequest, EmptyResult,
    ListResourcesRequest, ListToolsRequest, ReadResourceRequest,
    GetPromptRequest, ListPromptsRequest
)
from pydantic import BaseModel, Field, validator
import aiofiles
import yaml
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("mcp_server")

class ServerConfig(BaseModel):
    """MCP Server configuration"""
    name: str
    version: str = "1.0.0"
    description: str
    debug: bool = False
    redis_url: Optional[str] = None
    rate_limit_requests: int = 100
    rate_limit_window: int = 60
    cache_ttl: int = 300
    max_retries: int = 3
    timeout: int = 30

    class Config:
        extra = "allow"

@dataclass
class RequestContext:
    """Request context for tool calls"""
    user_id: str
    session_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.utcnow)

class RateLimiter:
    """Redis-based rate limiter for MCP operations"""

    def __init__(self, redis_url: str, requests: int, window: int):
        self.redis_url = redis_url
        self.requests = requests
        self.window = window
        self._redis = None

    async def _get_redis(self):
        if not self._redis:
            self._redis = await redis.from_url(self.redis_url)
        return self._redis

    async def is_allowed(self, key: str) -> bool:
        """Check if request is allowed"""
        r = await self._get_redis()
        current = await r.incr(f"rate_limit:{key}")

        if current == 1:
            await r.expire(f"rate_limit:{key}", self.window)

        return current <= self.requests

    async def get_remaining(self, key: str) -> int:
        """Get remaining requests"""
        r = await self._get_redis()
        current = await r.get(f"rate_limit:{key}")
        return max(0, self.requests - int(current or 0))

class CacheManager:
    """Redis-based caching for MCP responses"""

    def __init__(self, redis_url: str, ttl: int = 300):
        self.redis_url = redis_url
        self.ttl = ttl
        self._redis = None

    async def _get_redis(self):
        if not self._redis:
            self._redis = await redis.from_url(self.redis_url)
        return self._redis

    def _make_key(self, tool_name: str, args: Dict[str, Any]) -> str:
        """Generate cache key from tool name and arguments"""
        import hashlib
        args_str = json.dumps(args, sort_keys=True)
        return f"cache:{tool_name}:{hashlib.md5(args_str.encode()).hexdigest()}"

    async def get(self, tool_name: str, args: Dict[str, Any]) -> Optional[Any]:
        """Get cached result"""
        r = await self._get_redis()
        key = self._make_key(tool_name, args)
        result = await r.get(key)
        return json.loads(result) if result else None

    async def set(self, tool_name: str, args: Dict[str, Any], value: Any):
        """Cache result"""
        r = await self._get_redis()
        key = self._make_key(tool_name, args)
        await r.setex(key, self.ttl, json.dumps(value))

class BaseMCPServer:
    """Base MCP Server with common functionality"""

    def __init__(self, config: ServerConfig):
        self.config = config
        self.server = Server(config.name)
        self.tools: Dict[str, Callable] = {}
        self.rate_limiter: Optional[RateLimiter] = None
        self.cache: Optional[CacheManager] = None

        # Setup optional components
        if config.redis_url:
            self.rate_limiter = RateLimiter(
                config.redis_url,
                config.rate_limit_requests,
                config.rate_limit_window
            )
            self.cache = CacheManager(
                config.redis_url,
                config.cache_ttl
            )

        # Register handlers
        self._register_handlers()

        logger.info(f"MCP Server '{config.name}' initialized")

    def _register_handlers(self):
        """Register MCP handlers"""
        @self.server.list_tools()
        async def handle_list_tools() -> List[Tool]:
            """Return list of available tools"""
            return await self.list_tools()

        @self.server.call_tool()
        async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
            """Handle tool call with rate limiting and caching"""
            return await self.call_tool(name, arguments)

    def register_tool(self, name: str, handler: Callable, schema: Dict[str, Any]):
        """Register a new tool"""
        self.tools[name] = {
            "handler": handler,
            "schema": schema
        }
        logger.info(f"Registered tool: {name}")

    async def list_tools(self) -> List[Tool]:
        """List all available tools"""
        tools = []
        for name, tool_info in self.tools.items():
            tools.append(Tool(
                name=name,
                description=tool_info["schema"].get("description", ""),
                inputSchema=tool_info["schema"].get("inputSchema", {})
            ))
        return tools

    async def call_tool(self, name: str, arguments: Dict[str, Any]) -> List[TextContent]:
        """Execute a tool call with full middleware pipeline"""
        start_time = datetime.utcnow()

        try:
            # Extract context from arguments
            context = self._extract_context(arguments)

            # Rate limiting check
            if self.rate_limiter:
                rate_key = f"{context.user_id}:{name}"
                if not await self.rate_limiter.is_allowed(rate_key):
                    return [TextContent(
                        type="text",
                        text=json.dumps({
                            "status": "error",
                            "error": "Rate limit exceeded",
                            "remaining": await self.rate_limiter.get_remaining(rate_key)
                        })
                    )]

            # Check cache
            if self.cache and self._is_cacheable(name):
                cached_result = await self.cache.get(name, arguments)
                if cached_result:
                    logger.info(f"Cache hit for tool: {name}")
                    return [TextContent(
                        type="text",
                        text=json.dumps(cached_result)
                    )]

            # Validate tool exists
            if name not in self.tools:
                raise ValueError(f"Unknown tool: {name}")

            # Validate arguments
            schema = self.tools[name]["schema"]
            self._validate_arguments(arguments, schema)

            # Execute tool
            handler = self.tools[name]["handler"]
            result = await self._execute_tool(handler, arguments, context)

            # Cache result if applicable
            if self.cache and self._is_cacheable(name) and result.get("status") != "error":
                await self.cache.set(name, arguments, result)

            # Log execution
            duration = (datetime.utcnow() - start_time).total_seconds()
            logger.info(f"Tool {name} executed in {duration:.2f}s for user {context.user_id}")

            return [TextContent(
                type="text",
                text=json.dumps(result, default=str)
            )]

        except Exception as e:
            logger.error(f"Error executing tool {name}: {str(e)}", exc_info=True)
            duration = (datetime.utcnow() - start_time).total_seconds()
            logger.error(f"Tool {name} failed after {duration:.2f}s")

            return [TextContent(
                type="text",
                text=json.dumps({
                    "status": "error",
                    "error": str(e),
                    "tool": name,
                    "timestamp": datetime.utcnow().isoformat()
                })
            )]

    def _extract_context(self, arguments: Dict[str, Any]) -> RequestContext:
        """Extract request context from arguments"""
        user_id = arguments.pop("_user_id", "anonymous")
        session_id = arguments.pop("_session_id", None)
        metadata = arguments.pop("_metadata", {})

        return RequestContext(
            user_id=user_id,
            session_id=session_id,
            metadata=metadata
        )

    def _validate_arguments(self, arguments: Dict[str, Any], schema: Dict[str, Any]):
        """Validate tool arguments against schema"""
        # Basic validation - can be extended with pydantic
        input_schema = schema.get("inputSchema", {})
        required = input_schema.get("required", [])
        properties = input_schema.get("properties", {})

        # Check required fields
        for field in required:
            if field not in arguments:
                raise ValueError(f"Missing required field: {field}")

        # Validate field types
        for field, value in arguments.items():
            if field in properties:
                field_schema = properties[field]
                expected_type = field_schema.get("type")

                if expected_type == "string" and not isinstance(value, str):
                    raise ValueError(f"Field {field} must be a string")
                elif expected_type == "integer" and not isinstance(value, int):
                    raise ValueError(f"Field {field} must be an integer")
                elif expected_type == "array" and not isinstance(value, list):
                    raise ValueError(f"Field {field} must be an array")

                # Check enum values
                if "enum" in field_schema and value not in field_schema["enum"]:
                    raise ValueError(f"Field {field} must be one of {field_schema['enum']}")

    def _is_cacheable(self, tool_name: str) -> bool:
        """Determine if tool result should be cached"""
        # Non-mutating operations are cacheable
        non_mutating = ["get", "list", "search", "find", "read"]
        return any(op in tool_name.lower() for op in non_mutating)

    async def _execute_tool(self, handler: Callable, arguments: Dict[str, Any], context: RequestContext) -> Dict[str, Any]:
        """Execute tool handler with error handling"""
        try:
            # Pass context to handler if it accepts it
            import inspect
            sig = inspect.signature(handler)

            if 'context' in sig.parameters:
                result = await handler(arguments, context=context)
            else:
                result = await handler(arguments)

            return result

        except Exception as e:
            logger.error(f"Tool handler failed: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }

    async def run(self):
        """Start the MCP server"""
        logger.info(f"Starting MCP server: {self.config.name}")
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name=self.config.name,
                    server_version=self.config.version,
                    capabilities=self.server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={},
                    )
                )
            )

def tool(
    name: Optional[str] = None,
    description: str = "",
    input_schema: Optional[Dict[str, Any]] = None
):
    """Decorator for registering MCP tools"""
    def decorator(func):
        tool_name = name or func.__name__
        schema = {
            "description": description or func.__doc__ or "",
            "inputSchema": input_schema or {}
        }

        # Store schema on function for later registration
        func._mcp_tool_schema = schema
        func._mcp_tool_name = tool_name

        return func
    return decorator
```

## 2. Database Integration Patterns

```python
# mcp_server/database.py
"""
Generic Database Integration for MCP Servers
Supports multiple ORMs and connection patterns
"""

import asyncio
from abc import ABC, abstractmethod
from contextlib import asynccontextmanager
from typing import Any, Dict, List, Optional, TypeVar, Generic, Union
from datetime import datetime
import json

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime, Text, Boolean, select, update, delete, insert
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import NullPool
import asyncpg
import motor.motor_asyncio
from redis.asyncio import Redis

# Type variables
T = TypeVar('T')

class DatabaseBackend(ABC):
    """Abstract base for database backends"""

    @abstractmethod
    async def connect(self):
        """Establish connection"""
        pass

    @abstractmethod
    async def disconnect(self):
        """Close connection"""
        pass

    @abstractmethod
    async def execute_query(self, query: str, params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Execute a query and return results"""
        pass

    @abstractmethod
    async def execute_command(self, command: str, params: Dict[str, Any] = None) -> Any:
        """Execute a command (INSERT, UPDATE, DELETE)"""
        pass

class PostgresBackend(DatabaseBackend):
    """PostgreSQL backend using asyncpg"""

    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.pool: Optional[asyncpg.Pool] = None

    async def connect(self):
        self.pool = await asyncpg.create_pool(
            self.connection_string,
            min_size=5,
            max_size=20,
            command_timeout=60
        )

    async def disconnect(self):
        if self.pool:
            await self.pool.close()

    async def execute_query(self, query: str, params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(query, *params.values() if params else [])
            return [dict(row) for row in rows]

    async def execute_command(self, command: str, params: Dict[str, Any] = None) -> Any:
        async with self.pool.acquire() as conn:
            return await conn.execute(command, *params.values() if params else [])

class SQLAlchemyBackend(DatabaseBackend):
    """SQLAlchemy backend for multiple databases"""

    def __init__(self, database_url: str, async_mode: bool = True):
        self.database_url = database_url
        self.async_mode = async_mode
        self.engine = None
        self.session_factory = None

    async def connect(self):
        if self.async_mode:
            self.engine = create_async_engine(
                self.database_url,
                pool_pre_ping=True,
                pool_recycle=300,
                echo=False
            )
            self.session_factory = async_sessionmaker(
                self.engine,
                class_=AsyncSession,
                expire_on_commit=False
            )
        else:
            self.engine = create_engine(
                self.database_url,
                pool_pre_ping=True,
                pool_recycle=300,
                echo=False
            )
            self.session_factory = sessionmaker(
                bind=self.engine,
                expire_on_commit=False
            )

    async def disconnect(self):
        if self.engine:
            await self.engine.dispose()

    @asynccontextmanager
    async def get_session(self):
        """Get database session"""
        async with self.session_factory() as session:
            try:
                yield session
                if self.async_mode:
                    await session.commit()
                else:
                    session.commit()
            except Exception:
                if self.async_mode:
                    await session.rollback()
                else:
                    session.rollback()
                raise
            finally:
                if self.async_mode:
                    await session.close()
                else:
                    session.close()

    async def execute_query(self, query: Any, params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Execute SQLAlchemy query"""
        async with self.get_session() as session:
            if isinstance(query, str):
                # Raw SQL query
                result = await session.execute(query, params or {})
                rows = result.fetchall()
                return [dict(row._mapping) for row in rows]
            else:
                # SQLAlchemy ORM query
                result = await session.execute(query)
                rows = result.fetchall()
                return [dict(row._mapping) for row in rows]

    async def execute_command(self, command: Any, params: Dict[str, Any] = None) -> Any:
        """Execute SQLAlchemy command"""
        async with self.get_session() as session:
            if isinstance(command, str):
                # Raw SQL command
                result = await session.execute(command, params or {})
                await session.commit()
                return result
            else:
                # SQLAlchemy ORM command
                await session.execute(command, params or {})
                await session.commit()
                return None

class MongoBackend(DatabaseBackend):
    """MongoDB backend using motor"""

    def __init__(self, connection_string: str, database_name: str):
        self.connection_string = connection_string
        self.database_name = database_name
        self.client = None
        self.db = None

    async def connect(self):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(self.connection_string)
        self.db = self.client[self.database_name]

    async def disconnect(self):
        if self.client:
            self.client.close()

    async def execute_query(self, collection: str, query: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Execute MongoDB find query"""
        cursor = self.db[collection].find(query or {})
        results = []
        async for document in cursor:
            # Convert ObjectId to string
            if '_id' in document:
                document['_id'] = str(document['_id'])
            results.append(document)
        return results

    async def execute_command(self, operation: str, collection: str, data: Dict[str, Any]) -> Any:
        """Execute MongoDB command"""
        if operation == "insert":
            result = await self.db[collection].insert_one(data)
            return str(result.inserted_id)
        elif operation == "update":
            filter_ = data.pop("_filter")
            update_data = {"$set": data}
            result = await self.db[collection].update_one(filter_, update_data)
            return result.modified_count
        elif operation == "delete":
            result = await self.db[collection].delete_one(data)
            return result.deleted_count

class DatabaseManager(Generic[T]):
    """Generic database manager for MCP servers"""

    def __init__(self, backend: DatabaseBackend):
        self.backend = backend
        self._connected = False

    async def connect(self):
        """Connect to database"""
        if not self._connected:
            await self.backend.connect()
            self._connected = True

    async def disconnect(self):
        """Disconnect from database"""
        if self._connected:
            await self.backend.disconnect()
            self._connected = False

    @asynccontextmanager
    async def transaction(self):
        """Database transaction context manager"""
        if hasattr(self.backend, 'get_session'):
            async with self.backend.get_session() as session:
                yield session
        else:
            # For backends that don't support transactions
            yield self.backend

    async def find_one(self, table_or_collection: str, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Find a single record"""
        if isinstance(self.backend, MongoBackend):
            results = await self.backend.execute_query(table_or_collection, query)
            return results[0] if results else None
        else:
            # SQL implementation
            where_clause = " AND ".join([f"{k} = :{k}" for k in query.keys()])
            sql = f"SELECT * FROM {table_or_collection} WHERE {where_clause} LIMIT 1"
            results = await self.backend.execute_query(sql, query)
            return results[0] if results else None

    async def find_many(
        self,
        table_or_collection: str,
        query: Dict[str, Any] = None,
        limit: int = None,
        offset: int = None,
        order_by: str = None
    ) -> List[Dict[str, Any]]:
        """Find multiple records"""
        query = query or {}

        if isinstance(self.backend, MongoBackend):
            cursor = self.backend.db[table_or_collection].find(query)
            if limit:
                cursor = cursor.limit(limit)
            if offset:
                cursor = cursor.skip(offset)
            if order_by:
                # MongoDB sort format
                sort_field, sort_dir = order_by.split()
                cursor = cursor.sort([(sort_field, 1 if sort_dir == 'ASC' else -1)])

            results = []
            async for document in cursor:
                if '_id' in document:
                    document['_id'] = str(document['_id'])
                results.append(document)
            return results
        else:
            # SQL implementation
            where_clause = ""
            if query:
                where_clause = "WHERE " + " AND ".join([f"{k} = :{k}" for k in query.keys()])

            sql = f"SELECT * FROM {table_or_collection} {where_clause}"

            if order_by:
                sql += f" ORDER BY {order_by}"

            if limit:
                sql += f" LIMIT {limit}"

            if offset:
                sql += f" OFFSET {offset}"

            return await self.backend.execute_query(sql, query)

    async def create(self, table_or_collection: str, data: Dict[str, Any]) -> Any:
        """Create a new record"""
        data = data.copy()

        # Add timestamps
        data['created_at'] = datetime.utcnow()
        data['updated_at'] = datetime.utcnow()

        if isinstance(self.backend, MongoBackend):
            return await self.backend.execute_command("insert", table_or_collection, data)
        else:
            # SQL implementation
            columns = list(data.keys())
            placeholders = [f":{col}" for col in columns]
            sql = f"INSERT INTO {table_or_collection} ({', '.join(columns)}) VALUES ({', '.join(placeholders)})"
            return await self.backend.execute_command(sql, data)

    async def update(self, table_or_collection: str, query: Dict[str, Any], data: Dict[str, Any]) -> int:
        """Update records"""
        data = data.copy()
        data['updated_at'] = datetime.utcnow()

        if isinstance(self.backend, MongoBackend):
            data['_filter'] = query
            return await self.backend.execute_command("update", table_or_collection, data)
        else:
            # SQL implementation
            where_clause = " AND ".join([f"{k} = :{k}" for k in query.keys()])
            set_clause = ", ".join([f"{k} = :update_{k}" for k in data.keys()])

            # Prefix update params to avoid conflicts
            update_params = {f"update_{k}": v for k, v in data.items()}
            params = {**query, **update_params}

            sql = f"UPDATE {table_or_collection} SET {set_clause} WHERE {where_clause}"
            result = await self.backend.execute_command(sql, params)
            return result.rowcount if hasattr(result, 'rowcount') else 0

    async def delete(self, table_or_collection: str, query: Dict[str, Any]) -> int:
        """Delete records"""
        if isinstance(self.backend, MongoBackend):
            return await self.backend.execute_command("delete", table_or_collection, query)
        else:
            # SQL implementation
            where_clause = " AND ".join([f"{k} = :{k}" for k in query.keys()])
            sql = f"DELETE FROM {table_or_collection} WHERE {where_clause}"
            result = await self.backend.execute_command(sql, query)
            return result.rowcount if hasattr(result, 'rowcount') else 0

    async def count(self, table_or_collection: str, query: Dict[str, Any] = None) -> int:
        """Count records"""
        query = query or {}

        if isinstance(self.backend, MongoBackend):
            return await self.backend.db[table_or_collection].count_documents(query)
        else:
            # SQL implementation
            where_clause = ""
            if query:
                where_clause = "WHERE " + " AND ".join([f"{k} = :{k}" for k in query.keys()])

            sql = f"SELECT COUNT(*) as count FROM {table_or_collection} {where_clause}"
            results = await self.backend.execute_query(sql, query)
            return results[0]['count'] if results else 0

# Factory function for creating database managers
def create_database_manager(database_url: str, backend_type: str = "auto") -> DatabaseManager:
    """Create database manager based on URL or backend type"""

    if backend_type == "auto":
        if database_url.startswith("postgresql+asyncpg://"):
            backend = SQLAlchemyBackend(database_url, async_mode=True)
        elif database_url.startswith("mongodb://"):
            import re
            match = re.match(r'mongodb://[^/]+/([^?]*)', database_url)
            db_name = match.group(1) if match else "default"
            backend = MongoBackend(database_url, db_name)
        elif database_url.startswith("postgresql://"):
            backend = PostgresBackend(database_url)
        else:
            backend = SQLAlchemyBackend(database_url, async_mode=True)
    else:
        if backend_type == "postgres":
            backend = PostgresBackend(database_url)
        elif backend_type == "mongodb":
            db_name = database_url.split("/")[-1].split("?")[0]
            backend = MongoBackend(database_url, db_name)
        elif backend_type == "sqlalchemy":
            backend = SQLAlchemyBackend(database_url)
        else:
            raise ValueError(f"Unknown backend type: {backend_type}")

    return DatabaseManager(backend)
```

## 3. Tool Implementation Patterns

```python
# mcp_server/tools.py
"""
Generic MCP Tool Implementation Patterns
"""

from typing import Any, Dict, List, Optional, Union, Callable
from datetime import datetime, timedelta
import json
import uuid
from dataclasses import dataclass, field

from .core import BaseMCPServer, tool, RequestContext
from .database import DatabaseManager

class BaseTool:
    """Base class for MCP tools"""

    def __init__(self, db_manager: DatabaseManager, cache=None):
        self.db_manager = db_manager
        self.cache = cache

    async def execute(self, args: Dict[str, Any], context: RequestContext = None) -> Dict[str, Any]:
        """Execute the tool logic"""
        raise NotImplementedError

    def _validate_permissions(self, context: RequestContext, required_permission: str = None) -> bool:
        """Validate user permissions"""
        # Implement permission checking logic
        return True

class CRUDBaseTool(BaseTool):
    """Base CRUD tool for any entity"""

    def __init__(self, table_name: str, db_manager: DatabaseManager, schema: Dict[str, Any]):
        super().__init__(db_manager)
        self.table_name = table_name
        self.schema = schema
        self.entity_name = table_name.rstrip('s')  # Remove plural 's'

    async def create(self, args: Dict[str, Any], context: RequestContext) -> Dict[str, Any]:
        """Create entity"""
        try:
            # Validate against schema
            validated_data = self._validate_data(args, for_create=True)

            # Add user context
            if context:
                validated_data['user_id'] = context.user_id
                if context.session_id:
                    validated_data['session_id'] = context.session_id

            # Insert into database
            result = await self.db_manager.create(self.table_name, validated_data)

            return {
                "status": "created",
                "id": result,
                "entity": self.entity_name,
                "timestamp": datetime.utcnow().isoformat()
            }

        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "entity": self.entity_name,
                "operation": "create"
            }

    async def get(self, args: Dict[str, Any], context: RequestContext) -> Dict[str, Any]:
        """Get entity by ID"""
        try:
            entity_id = args.get("id")
            if not entity_id:
                raise ValueError("Missing required field: id")

            # Add user filter for security
            query = {"id": entity_id}
            if context and not self._validate_permissions(context, "read_all"):
                query["user_id"] = context.user_id

            result = await self.db_manager.find_one(self.table_name, query)

            if not result:
                return {
                    "status": "not_found",
                    "entity": self.entity_name,
                    "id": entity_id
                }

            return {
                "status": "success",
                "entity": self.entity_name,
                "data": self._serialize_data(result)
            }

        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "entity": self.entity_name,
                "operation": "get"
            }

    async def list(self, args: Dict[str, Any], context: RequestContext) -> Dict[str, Any]:
        """List entities with filtering"""
        try:
            # Build query from args
            query = {}
            filters = args.get("filters", {})
            limit = args.get("limit", 20)
            offset = args.get("offset", 0)
            order_by = args.get("order_by", "created_at DESC")

            # Add user filter for security
            if context and not self._validate_permissions(context, "read_all"):
                query["user_id"] = context.user_id

            # Apply additional filters
            query.update(filters)

            # Fetch from database
            results = await self.db_manager.find_many(
                self.table_name,
                query=query,
                limit=limit,
                offset=offset,
                order_by=order_by
            )

            # Get total count
            total = await self.db_manager.count(self.table_name, query)

            return {
                "status": "success",
                "entity": self.entity_name,
                "data": [self._serialize_data(r) for r in results],
                "pagination": {
                    "total": total,
                    "limit": limit,
                    "offset": offset,
                    "has_more": offset + limit < total
                }
            }

        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "entity": self.entity_name,
                "operation": "list"
            }

    async def update(self, args: Dict[str, Any], context: RequestContext) -> Dict[str, Any]:
        """Update entity"""
        try:
            entity_id = args.pop("id", None)
            if not entity_id:
                raise ValueError("Missing required field: id")

            # Validate update data
            update_data = self._validate_data(args, for_create=False)

            # Build query filter
            query = {"id": entity_id}
            if context and not self._validate_permissions(context, "update_all"):
                query["user_id"] = context.user_id

            # Update in database
            affected = await self.db_manager.update(self.table_name, query, update_data)

            if affected == 0:
                return {
                    "status": "not_found",
                    "entity": self.entity_name,
                    "id": entity_id
                }

            return {
                "status": "updated",
                "entity": self.entity_name,
                "id": entity_id,
                "affected_rows": affected,
                "timestamp": datetime.utcnow().isoformat()
            }

        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "entity": self.entity_name,
                "operation": "update"
            }

    async def delete(self, args: Dict[str, Any], context: RequestContext) -> Dict[str, Any]:
        """Delete entity"""
        try:
            entity_id = args.get("id")
            if not entity_id:
                raise ValueError("Missing required field: id")

            # Build query filter
            query = {"id": entity_id}
            if context and not self._validate_permissions(context, "delete_all"):
                query["user_id"] = context.user_id

            # Delete from database
            affected = await self.db_manager.delete(self.table_name, query)

            if affected == 0:
                return {
                    "status": "not_found",
                    "entity": self.entity_name,
                    "id": entity_id
                }

            return {
                "status": "deleted",
                "entity": self.entity_name,
                "id": entity_id,
                "affected_rows": affected,
                "timestamp": datetime.utcnow().isoformat()
            }

        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "entity": self.entity_name,
                "operation": "delete"
            }

    def _validate_data(self, data: Dict[str, Any], for_create: bool = False) -> Dict[str, Any]:
        """Validate data against schema"""
        validated = {}
        schema_fields = self.schema.get("properties", {})
        required_fields = self.schema.get("required", [])

        # Check required fields for create
        if for_create:
            for field in required_fields:
                if field not in data:
                    raise ValueError(f"Missing required field: {field}")

        # Validate each field
        for field, value in data.items():
            if field not in schema_fields:
                continue  # Skip unknown fields or raise error based on strictness

            field_schema = schema_fields[field]
            field_type = field_schema.get("type")

            # Type validation
            if field_type == "string":
                if not isinstance(value, str):
                    raise ValueError(f"Field {field} must be a string")
                # Check min/max length
                if "minLength" in field_schema and len(value) < field_schema["minLength"]:
                    raise ValueError(f"Field {field} is too short")
                if "maxLength" in field_schema and len(value) > field_schema["maxLength"]:
                    raise ValueError(f"Field {field} is too long")
            elif field_type == "integer":
                if not isinstance(value, int):
                    raise ValueError(f"Field {field} must be an integer")
                # Check min/max value
                if "minimum" in field_schema and value < field_schema["minimum"]:
                    raise ValueError(f"Field {field} is too small")
                if "maximum" in field_schema and value > field_schema["maximum"]:
                    raise ValueError(f"Field {field} is too large")
            elif field_type == "array":
                if not isinstance(value, list):
                    raise ValueError(f"Field {field} must be an array")

            # Check enum values
            if "enum" in field_schema and value not in field_schema["enum"]:
                raise ValueError(f"Field {field} must be one of {field_schema['enum']}")

            validated[field] = value

        return validated

    def _serialize_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Serialize data for output"""
        serialized = data.copy()

        # Handle datetime serialization
        for key, value in serialized.items():
            if isinstance(value, datetime):
                serialized[key] = value.isoformat()
            elif isinstance(value, dict):
                # Convert complex types to JSON string
                try:
                    json.dumps(value)
                except TypeError:
                    serialized[key] = str(value)

        return serialized

class BulkOperationTool(BaseTool):
    """Tool for bulk operations on entities"""

    def __init__(self, table_name: str, db_manager: DatabaseManager, schema: Dict[str, Any]):
        super().__init__(db_manager)
        self.table_name = table_name
        self.schema = schema
        self.entity_name = table_name.rstrip('s')

    async def bulk_create(self, args: Dict[str, Any], context: RequestContext) -> Dict[str, Any]:
        """Bulk create entities"""
        try:
            items = args.get("items", [])
            if not items:
                raise ValueError("No items provided for bulk create")

            # Validate all items
            validated_items = []
            for item in items:
                validated = self._validate_item(item)
                if context:
                    validated["user_id"] = context.user_id
                validated_items.append(validated)

            # Insert all items
            results = []
            for item in validated_items:
                result = await self.db_manager.create(self.table_name, item)
                results.append(result)

            return {
                "status": "created",
                "entity": self.entity_name,
                "count": len(results),
                "ids": results,
                "timestamp": datetime.utcnow().isoformat()
            }

        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "entity": self.entity_name,
                "operation": "bulk_create"
            }

    async def bulk_update(self, args: Dict[str, Any], context: RequestContext) -> Dict[str, Any]:
        """Bulk update entities"""
        try:
            updates = args.get("updates", [])
            if not updates:
                raise ValueError("No updates provided")

            total_affected = 0
            for update in updates:
                entity_id = update.get("id")
                update_data = update.get("data", {})

                if not entity_id:
                    continue

                # Build query
                query = {"id": entity_id}
                if context:
                    query["user_id"] = context.user_id

                # Update
                affected = await self.db_manager.update(self.table_name, query, update_data)
                total_affected += affected

            return {
                "status": "updated",
                "entity": self.entity_name,
                "affected_rows": total_affected,
                "updates_processed": len(updates),
                "timestamp": datetime.utcnow().isoformat()
            }

        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "entity": self.entity_name,
                "operation": "bulk_update"
            }

    async def bulk_delete(self, args: Dict[str, Any], context: RequestContext) -> Dict[str, Any]:
        """Bulk delete entities"""
        try:
            ids = args.get("ids", [])
            if not ids:
                raise ValueError("No IDs provided for bulk delete")

            total_affected = 0
            for entity_id in ids:
                # Build query
                query = {"id": entity_id}
                if context:
                    query["user_id"] = context.user_id

                # Delete
                affected = await self.db_manager.delete(self.table_name, query)
                total_affected += affected

            return {
                "status": "deleted",
                "entity": self.entity_name,
                "affected_rows": total_affected,
                "ids_processed": len(ids),
                "timestamp": datetime.utcnow().isoformat()
            }

        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "entity": self.entity_name,
                "operation": "bulk_delete"
            }

    def _validate_item(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """Validate a single item"""
        # Use CRUD base tool validation
        crud_tool = CRUDBaseTool(self.table_name, self.db_manager, self.schema)
        return crud_tool._validate_data(item, for_create=True)
```

## 4. Example: Building a Generic Task Management MCP Server

```python
# examples/task_mcp_server.py
"""
Example: Task Management MCP Server using generic patterns
"""

import os
from typing import Dict, Any

from mcp_server.core import BaseMCPServer, ServerConfig, tool
from mcp_server.database import create_database_manager
from mcp_server.tools import CRUDBaseTool, BulkOperationTool

# Server configuration
config = ServerConfig(
    name="task-manager",
    version="1.0.0",
    description="Generic task management MCP server",
    redis_url=os.getenv("REDIS_URL", "redis://localhost:6379"),
    database_url=os.getenv("DATABASE_URL", "postgresql+asyncpg://user:pass@localhost/tasks")
)

# Task entity schema
TASK_SCHEMA = {
    "type": "object",
    "properties": {
        "title": {
            "type": "string",
            "minLength": 1,
            "maxLength": 200,
            "description": "Task title"
        },
        "description": {
            "type": "string",
            "maxLength": 1000,
            "description": "Task description"
        },
        "priority": {
            "type": "string",
            "enum": ["low", "medium", "high"],
            "default": "medium",
            "description": "Task priority"
        },
        "status": {
            "type": "string",
            "enum": ["todo", "in_progress", "completed"],
            "default": "todo",
            "description": "Task status"
        },
        "due_date": {
            "type": "string",
            "format": "date-time",
            "description": "Optional due date"
        },
        "tags": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Task tags"
        }
    },
    "required": ["title"]
}

class TaskMCPServer(BaseMCPServer):
    """Task Management MCP Server"""

    def __init__(self, config: ServerConfig):
        super().__init__(config)

        # Initialize database
        self.db_manager = create_database_manager(config.database_url)

        # Initialize tools
        self.task_tool = CRUDBaseTool("tasks", self.db_manager, TASK_SCHEMA)
        self.bulk_tool = BulkOperationTool("tasks", self.db_manager, TASK_SCHEMA)

        # Register tools
        self._register_task_tools()

    def _register_task_tools(self):
        """Register all task-related tools"""

        # Create task
        self.register_tool(
            "create_task",
            self.task_tool.create,
            {
                "description": "Create a new task",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string", "description": "Task title"},
                        "description": {"type": "string", "description": "Optional description"},
                        "priority": {"type": "string", "enum": ["low", "medium", "high"]},
                        "due_date": {"type": "string", "format": "date-time"},
                        "tags": {"type": "array", "items": {"type": "string"}}
                    },
                    "required": ["title"]
                }
            }
        )

        # Get task
        self.register_tool(
            "get_task",
            self.task_tool.get,
            {
                "description": "Get a task by ID",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer", "description": "Task ID"}
                    },
                    "required": ["id"]
                }
            }
        )

        # List tasks
        self.register_tool(
            "list_tasks",
            self.task_tool.list,
            {
                "description": "List tasks with optional filtering",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "filters": {"type": "object", "description": "Filter criteria"},
                        "limit": {"type": "integer", "minimum": 1, "maximum": 100, "default": 20},
                        "offset": {"type": "integer", "minimum": 0, "default": 0},
                        "order_by": {"type": "string", "description": "Order by field (e.g., 'created_at DESC')"}
                    }
                }
            }
        )

        # Update task
        self.register_tool(
            "update_task",
            self.task_tool.update,
            {
                "description": "Update a task",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer", "description": "Task ID"},
                        "title": {"type": "string", "description": "New title"},
                        "description": {"type": "string", "description": "New description"},
                        "priority": {"type": "string", "enum": ["low", "medium", "high"]},
                        "status": {"type": "string", "enum": ["todo", "in_progress", "completed"]},
                        "due_date": {"type": "string", "format": "date-time"},
                        "tags": {"type": "array", "items": {"type": "string"}}
                    },
                    "required": ["id"]
                }
            }
        )

        # Delete task
        self.register_tool(
            "delete_task",
            self.task_tool.delete,
            {
                "description": "Delete a task",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer", "description": "Task ID"}
                    },
                    "required": ["id"]
                }
            }
        )

        # Bulk create
        self.register_tool(
            "bulk_create_tasks",
            self.bulk_tool.bulk_create,
            {
                "description": "Create multiple tasks at once",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "items": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "title": {"type": "string"},
                                    "description": {"type": "string"},
                                    "priority": {"type": "string", "enum": ["low", "medium", "high"]},
                                    "tags": {"type": "array", "items": {"type": "string"}}
                                },
                                "required": ["title"]
                            }
                        }
                    },
                    "required": ["items"]
                }
            }
        )

        # Search tasks
        self.register_tool(
            "search_tasks",
            self._search_tasks,
            {
                "description": "Search tasks by text query",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search query"},
                        "limit": {"type": "integer", "minimum": 1, "maximum": 50, "default": 20}
                    },
                    "required": ["query"]
                }
            }
        )

    async def _search_tasks(self, args: Dict[str, Any], context) -> Dict[str, Any]:
        """Search tasks by text"""
        try:
            query = args.get("query", "")
            limit = args.get("limit", 20)

            # Build search query
            if isinstance(self.db_manager.backend, MongoBackend):
                # MongoDB text search
                search_query = {
                    "$text": {"$search": query}
                }
                if context and not self.task_tool._validate_permissions(context, "read_all"):
                    search_query["user_id"] = context.user_id

                results = await self.db_manager.find_many("tasks", search_query, limit=limit)
            else:
                # PostgreSQL full-text search
                sql = """
                SELECT * FROM tasks
                WHERE to_tsvector('english', title || ' ' || COALESCE(description, '')) @@ plainto_tsquery('english', :query)
                """
                params = {"query": query}

                if context and not self.task_tool._validate_permissions(context, "read_all"):
                    sql += " AND user_id = :user_id"
                    params["user_id"] = context.user_id

                sql += f" LIMIT {limit}"

                results = await self.db_manager.execute_query(sql, params)

            return {
                "status": "success",
                "entity": "task",
                "data": [self.task_tool._serialize_data(r) for r in results],
                "query": query,
                "count": len(results)
            }

        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "operation": "search_tasks"
            }

# Main execution
async def main():
    """Start the Task MCP Server"""
    server = TaskMCPServer(config)
    await server.run()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

## 5. Testing Patterns

```python
# tests/test_mcp_server.py
"""
Generic MCP Server Testing Patterns
"""

import pytest
import asyncio
from typing import Dict, Any, List
from unittest.mock import Mock, AsyncMock

from mcp_server.core import BaseMCPServer, ServerConfig, RequestContext
from mcp_server.database import DatabaseManager, create_database_manager
from mcp_server.tools import CRUDBaseTool

class MockDatabaseManager:
    """Mock database manager for testing"""

    def __init__(self):
        self.data = {}
        self.next_id = 1

    async def create(self, table: str, data: Dict[str, Any]) -> int:
        """Mock create"""
        entity_id = self.next_id
        data['id'] = entity_id
        self.data[f"{table}:{entity_id}"] = data
        self.next_id += 1
        return entity_id

    async def find_one(self, table: str, query: Dict[str, Any]) -> Dict[str, Any]:
        """Mock find one"""
        for key, value in self.data.items():
            table_name, entity_id = key.split(":")
            if table_name == table:
                match = True
                for k, v in query.items():
                    if value.get(k) != v:
                        match = False
                        break
                if match:
                    return value
        return None

    async def find_many(self, table: str, query: Dict[str, Any], limit: int = None) -> List[Dict[str, Any]]:
        """Mock find many"""
        results = []
        for key, value in self.data.items():
            table_name, entity_id = key.split(":")
            if table_name == table:
                match = True
                for k, v in query.items():
                    if value.get(k) != v:
                        match = False
                        break
                if match:
                    results.append(value)
                    if limit and len(results) >= limit:
                        break
        return results

    async def update(self, table: str, query: Dict[str, Any], data: Dict[str, Any]) -> int:
        """Mock update"""
        count = 0
        for key, value in self.data.items():
            table_name, entity_id = key.split(":")
            if table_name == table:
                match = True
                for k, v in query.items():
                    if value.get(k) != v:
                        match = False
                        break
                if match:
                    value.update(data)
                    count += 1
        return count

    async def delete(self, table: str, query: Dict[str, Any]) -> int:
        """Mock delete"""
        to_delete = []
        for key, value in self.data.items():
            table_name, entity_id = key.split(":")
            if table_name == table:
                match = True
                for k, v in query.items():
                    if value.get(k) != v:
                        match = False
                        break
                if match:
                    to_delete.append(key)

        for key in to_delete:
            del self.data[key]

        return len(to_delete)

@pytest.fixture
async def mock_db():
    """Mock database manager fixture"""
    return MockDatabaseManager()

@pytest.fixture
def test_schema():
    """Test entity schema"""
    return {
        "type": "object",
        "properties": {
            "name": {"type": "string", "minLength": 1},
            "value": {"type": "integer", "minimum": 0},
            "status": {"type": "string", "enum": ["active", "inactive"]},
            "tags": {"type": "array", "items": {"type": "string"}}
        },
        "required": ["name"]
    }

@pytest.fixture
def crud_tool(mock_db, test_schema):
    """CRUD tool fixture"""
    return CRUDBaseTool("test_entities", mock_db, test_schema)

@pytest.fixture
def user_context():
    """User context fixture"""
    return RequestContext(user_id="test_user", session_id="test_session")

class TestCRUDTool:
    """Test CRUD tool operations"""

    @pytest.mark.asyncio
    async def test_create_entity(self, crud_tool, user_context):
        """Test entity creation"""
        args = {
            "name": "Test Entity",
            "value": 100,
            "status": "active",
            "tags": ["test", "example"]
        }

        result = await crud_tool.create(args, user_context)

        assert result["status"] == "created"
        assert "id" in result
        assert result["entity"] == "test_entity"
        assert "timestamp" in result

    @pytest.mark.asyncio
    async def test_create_missing_required(self, crud_tool, user_context):
        """Test creation with missing required field"""
        args = {"value": 100}  # Missing 'name'

        result = await crud_tool.create(args, user_context)

        assert result["status"] == "error"
        assert "Missing required field" in result["error"]

    @pytest.mark.asyncio
    async def test_get_entity(self, crud_tool, user_context):
        """Test getting an entity"""
        # First create an entity
        create_args = {"name": "Test Get"}
        create_result = await crud_tool.create(create_args, user_context)
        entity_id = create_result["id"]

        # Get the entity
        get_args = {"id": entity_id}
        result = await crud_tool.get(get_args, user_context)

        assert result["status"] == "success"
        assert result["data"]["name"] == "Test Get"
        assert result["data"]["id"] == entity_id

    @pytest.mark.asyncio
    async def test_get_not_found(self, crud_tool, user_context):
        """Test getting non-existent entity"""
        args = {"id": 99999}
        result = await crud_tool.get(args, user_context)

        assert result["status"] == "not_found"

    @pytest.mark.asyncio
    async def test_list_entities(self, crud_tool, user_context):
        """Test listing entities"""
        # Create a few entities
        for i in range(3):
            args = {"name": f"Entity {i}"}
            await crud_tool.create(args, user_context)

        # List entities
        result = await crud_tool.list({}, user_context)

        assert result["status"] == "success"
        assert len(result["data"]) == 3
        assert "pagination" in result
        assert result["pagination"]["total"] == 3

    @pytest.mark.asyncio
    async def test_list_with_filters(self, crud_tool, user_context):
        """Test listing with filters"""
        # Create entities with different statuses
        await crud_tool.create({"name": "Active 1", "status": "active"}, user_context)
        await crud_tool.create({"name": "Inactive 1", "status": "inactive"}, user_context)
        await crud_tool.create({"name": "Active 2", "status": "active"}, user_context)

        # Filter by status
        result = await crud_tool.list(
            {"filters": {"status": "active"}},
            user_context
        )

        assert result["status"] == "success"
        assert all(entity["status"] == "active" for entity in result["data"])

    @pytest.mark.asyncio
    async def test_update_entity(self, crud_tool, user_context):
        """Test updating an entity"""
        # Create entity
        create_result = await crud_tool.create({"name": "Original"}, user_context)
        entity_id = create_result["id"]

        # Update entity
        update_args = {
            "id": entity_id,
            "name": "Updated",
            "value": 200
        }
        result = await crud_tool.update(update_args, user_context)

        assert result["status"] == "updated"
        assert result["affected_rows"] == 1

    @pytest.mark.asyncio
    async def test_delete_entity(self, crud_tool, user_context):
        """Test deleting an entity"""
        # Create entity
        create_result = await crud_tool.create({"name": "To Delete"}, user_context)
        entity_id = create_result["id"]

        # Delete entity
        delete_args = {"id": entity_id}
        result = await crud_tool.delete(delete_args, user_context)

        assert result["status"] == "deleted"
        assert result["affected_rows"] == 1

        # Verify deletion
        get_result = await crud_tool.get({"id": entity_id}, user_context)
        assert get_result["status"] == "not_found"

class TestMCPServer:
    """Test MCP Server functionality"""

    @pytest.mark.asyncio
    async def test_server_initialization(self):
        """Test server initialization"""
        config = ServerConfig(
            name="test-server",
            description="Test MCP Server"
        )

        server = BaseMCPServer(config)

        assert server.config.name == "test-server"
        assert server.server.name == "test-server"
        assert len(server.tools) == 0

    @pytest.mark.asyncio
    async def test_tool_registration(self):
        """Test tool registration"""
        config = ServerConfig(name="test-server", description="Test")
        server = BaseMCPServer(config)

        # Register a test tool
        async def test_tool(args: Dict[str, Any]) -> Dict[str, Any]:
            return {"status": "success", "data": args}

        schema = {
            "description": "Test tool",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "message": {"type": "string"}
                }
            }
        }

        server.register_tool("test_tool", test_tool, schema)

        assert "test_tool" in server.tools
        assert server.tools["test_tool"]["schema"] == schema

    @pytest.mark.asyncio
    async def test_rate_limiting(self):
        """Test rate limiting functionality"""
        # This would require mocking Redis or using a test instance
        # Implementation would depend on your rate limiting strategy
        pass

    @pytest.mark.asyncio
    async def test_caching(self):
        """Test caching functionality"""
        # This would require mocking Redis or using a test instance
        # Implementation would depend on your caching strategy
        pass

# Integration test example
class TestMCPServerIntegration:
    """Integration tests for MCP Server"""

    @pytest.mark.asyncio
    async def test_full_crud_workflow(self):
        """Test full CRUD workflow through MCP interface"""
        # Create mock server
        config = ServerConfig(
            name="test-integration",
            description="Integration test server"
        )

        # Use in-memory database
        mock_db = MockDatabaseManager()

        # Create CRUD tool
        test_schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "value": {"type": "integer"}
            },
            "required": ["name"]
        }

        crud_tool = CRUDBaseTool("items", mock_db, test_schema)

        # Register tools
        server = BaseMCPServer(config)
        server.register_tool(
            "create_item",
            crud_tool.create,
            {
                "description": "Create item",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "value": {"type": "integer"}
                    },
                    "required": ["name"]
                }
            }
        )

        # Test create
        result = await server.call_tool(
            "create_item",
            {"name": "Test Item", "value": 123}
        )

        response = json.loads(result[0].text)
        assert response["status"] == "created"

        # Test get (would need get_item tool)
        # Test list
        # Test update
        # Test delete
```

This generic MCP server skill provides a reusable foundation for building any MCP server, not just for todos. It includes:

1. **Core Server Architecture** - Base class with rate limiting, caching, and error handling
2. **Database Integration** - Support for PostgreSQL, MongoDB, and SQLAlchemy with async operations
3. **Tool Patterns** - Generic CRUD and bulk operation patterns that work with any entity
4. **Example Implementation** - Shows how to build a task management server using the generic patterns
5. **Testing Framework** - Comprehensive testing patterns and mocks

`★ Insight ─────────────────────────────────────`
The key architectural pattern here is the separation of concerns between:
- The MCP protocol handling (BaseMCPServer)
- The data access layer (DatabaseManager with multiple backends)
- The business logic layer (CRUDBaseTool and BulkOperationTool)
- The specific implementation (TaskMCPServer combining the components)

This makes the system highly reusable and maintainable. Any developer can quickly build a new MCP server by defining their entity schema and combining the generic tools.
`─────────────────────────────────────────────────`