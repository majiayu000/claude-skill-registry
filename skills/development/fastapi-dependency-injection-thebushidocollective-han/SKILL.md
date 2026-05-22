---
name: fastapi-dependency-injection
description: Master FastAPI dependency injection for building modular, testable APIs.
  Use when creating reusable dependencies and services.
allowed-tools:
  - Bash
  - Read
---

# FastAPI Dependency Injection

Master FastAPI's dependency injection system for building modular,
testable APIs with reusable dependencies.

## Basic Dependencies

Simple dependency injection patterns in FastAPI.

```python
from fastapi import Depends, FastAPI

app = FastAPI()

def get_db():
    db = Database()
    try:
        yield db
    finally:
        db.close()

@app.get('/users')
async def get_users(db = Depends(get_db)):
    return await db.query('SELECT * FROM users')

# Simple function dependency
def common_parameters(q: str = None, skip: int = 0, limit: int = 100):
    return {'q': q, 'skip': skip, 'limit': limit}

@app.get('/items')
async def read_items(commons: dict = Depends(common_parameters)):
    return commons

# Async dependencies
async def get_async_db():
    db = await AsyncDatabase.connect()
    try:
        yield db
    finally:
        await db.disconnect()

@app.get('/async-users')
async def get_async_users(db = Depends(get_async_db)):
    return await db.fetch_all('SELECT * FROM users')
```

## Dependency Scopes

Understand dependency lifecycle and caching.

```python
from fastapi import Depends

# Request-scoped dependency (default, cached per request)
def get_current_user(token: str = Depends(oauth2_scheme)):
    user = decode_token(token)
    return user

# Multiple uses in same request reuse the same instance
@app.get('/profile')
async def get_profile(
    user1 = Depends(get_current_user),
    user2 = Depends(get_current_user)  # Same instance as user1
):
    assert user1 is user2  # True
    return user1

# No caching (use_cache=False)
def get_fresh_data(use_cache: bool = False):
    return fetch_from_api()

@app.get('/data')
async def get_data(data = Depends(get_fresh_data, use_cache=False)):
    return data  # Fetches fresh data each time

# Singleton pattern (application scope)
class Settings:
    def __init__(self):
        self.app_name = "MyApp"
        self.admin_email = "admin@example.com"

settings = Settings()  # Created once at startup

def get_settings():
    return settings

@app.get('/settings')
async def read_settings(settings: Settings = Depends(get_settings)):
    return settings
```

## Sub-Dependencies

Build complex dependency chains.

```python
from fastapi import Depends, HTTPException, status

# Sub-dependency chain
def get_db():
    db = Database()
    try:
        yield db
    finally:
        db.close()

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db = Depends(get_db)
):
    user = db.query_one('SELECT * FROM users WHERE token = ?', token)
    if not user:
        raise HTTPException(status_code=401, detail='Invalid token')
    return user

def get_current_active_user(
    current_user = Depends(get_current_user)
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail='Inactive user')
    return current_user

def get_admin_user(
    current_user = Depends(get_current_active_user)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail='Not authorized')
    return current_user

# Use in endpoint
@app.delete('/users/{user_id}')
async def delete_user(
    user_id: int,
    admin = Depends(get_admin_user),
    db = Depends(get_db)
):
    await db.execute('DELETE FROM users WHERE id = ?', user_id)
    return {'status': 'deleted'}
```

## Class-Based Dependencies

Use classes for stateful dependencies.

```python
from fastapi import Depends

class Database:
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.connection = None

    async def connect(self):
        self.connection = await create_connection(self.connection_string)
        return self

    async def disconnect(self):
        if self.connection:
            await self.connection.close()

    async def fetch_all(self, query: str):
        return await self.connection.fetch_all(query)

# Callable class (using __call__)
class DatabaseDependency:
    def __init__(self):
        self.db = None

    async def __call__(self):
        if not self.db:
            self.db = Database('postgresql://localhost/db')
            await self.db.connect()
        return self.db

db_dependency = DatabaseDependency()

@app.get('/users')
async def get_users(db = Depends(db_dependency)):
    return await db.fetch_all('SELECT * FROM users')

# Class with initialization parameters
class Pagination:
    def __init__(self, skip: int = 0, limit: int = 100):
        self.skip = skip
        self.limit = limit

@app.get('/items')
async def get_items(pagination: Pagination = Depends()):
    return {'skip': pagination.skip, 'limit': pagination.limit}

# Advanced class-based dependency with configuration
class ServiceClient:
    def __init__(
        self,
        api_key: str,
        timeout: int = 30,
        max_retries: int = 3
    ):
        self.api_key = api_key
        self.timeout = timeout
        self.max_retries = max_retries
        self.client = None

    async def __call__(self):
        if not self.client:
            self.client = await create_http_client(
                api_key=self.api_key,
                timeout=self.timeout
            )
        return self.client

# Factory function for configurable class-based dependency
def create_service_dependency(api_key: str):
    return ServiceClient(api_key=api_key, timeout=60)

service = create_service_dependency('my-api-key')

@app.get('/external-data')
async def get_external_data(client = Depends(service)):
    return await client.fetch('/data')
```

## Generator Dependencies for Cleanup

Use generator functions to ensure proper resource cleanup.

```python
from contextlib import asynccontextmanager
from fastapi import Depends
import httpx

# Database connection with cleanup
async def get_db_connection():
    connection = await Database.connect('postgresql://localhost/db')
    try:
        yield connection
    finally:
        await connection.close()
        print('Database connection closed')

# HTTP client with cleanup
async def get_http_client():
    async with httpx.AsyncClient(timeout=30.0) as client:
        yield client
    # Client automatically closed after yield

@app.get('/external-api')
async def call_external_api(client = Depends(get_http_client)):
    response = await client.get('https://api.example.com/data')
    return response.json()

# File handle with cleanup
async def get_file_writer(filename: str):
    file = await aiofiles.open(filename, mode='a')
    try:
        yield file
    finally:
        await file.close()

# Multiple resources with cleanup
async def get_resources():
    db = await Database.connect('postgresql://localhost/db')
    cache = await Redis.connect('redis://localhost')
    logger = Logger('app')

    try:
        yield {'db': db, 'cache': cache, 'logger': logger}
    finally:
        await cache.close()
        await db.close()
        logger.shutdown()

@app.post('/process')
async def process_data(
    data: dict,
    resources = Depends(get_resources)
):
    db = resources['db']
    cache = resources['cache']
    logger = resources['logger']

    logger.info('Processing data')
    result = await db.save(data)
    await cache.invalidate('data_cache')
    return result

# Context manager as dependency
@asynccontextmanager
async def transaction_context(db = Depends(get_db)):
    async with db.begin() as transaction:
        try:
            yield transaction
            await transaction.commit()
        except Exception:
            await transaction.rollback()
            raise

async def get_transaction(db = Depends(get_db)):
    async with transaction_context(db) as txn:
        yield txn

@app.post('/transfer')
async def transfer_funds(
    from_account: int,
    to_account: int,
    amount: float,
    txn = Depends(get_transaction)
):
    await txn.execute(
        'UPDATE accounts SET balance = balance - ? WHERE id = ?',
        amount, from_account
    )
    await txn.execute(
        'UPDATE accounts SET balance = balance + ? WHERE id = ?',
        amount, to_account
    )
    return {'status': 'success'}
```

## Dependency Chains and Sub-Dependencies

Build complex dependency hierarchies.

```python
from fastapi import Depends, HTTPException
from typing import Optional

# Level 1: Configuration
def get_config():
    return {
        'database_url': 'postgresql://localhost/db',
        'redis_url': 'redis://localhost',
        'secret_key': 'super-secret'
    }

# Level 2: Infrastructure (depends on config)
def get_db(config: dict = Depends(get_config)):
    db = Database(config['database_url'])
    try:
        yield db
    finally:
        db.close()

def get_cache(config: dict = Depends(get_config)):
    cache = Redis(config['redis_url'])
    try:
        yield cache
    finally:
        cache.close()

# Level 3: Authentication (depends on infrastructure)
def get_token_from_header(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail='Missing token')
    scheme, token = authorization.split()
    if scheme.lower() != 'bearer':
        raise HTTPException(status_code=401, detail='Invalid scheme')
    return token

def verify_token(
    token: str = Depends(get_token_from_header),
    config: dict = Depends(get_config)
):
    try:
        payload = jwt.decode(
            token,
            config['secret_key'],
            algorithms=['HS256']
        )
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail='Invalid token')

def get_current_user(
    payload: dict = Depends(verify_token),
    db = Depends(get_db)
):
    user_id = payload.get('user_id')
    user = db.query_one('SELECT * FROM users WHERE id = ?', user_id)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    return user

# Level 4: Authorization (depends on authentication)
def get_active_user(user = Depends(get_current_user)):
    if not user.is_active:
        raise HTTPException(status_code=403, detail='Inactive user')
    return user

def require_permission(permission: str):
    def permission_checker(user = Depends(get_active_user)):
        if permission not in user.permissions:
            raise HTTPException(
                status_code=403,
                detail=f'Permission {permission} required'
            )
        return user
    return permission_checker

# Level 5: Business logic (depends on authorization)
def get_user_service(
    db = Depends(get_db),
    cache = Depends(get_cache),
    current_user = Depends(get_active_user)
):
    return UserService(db=db, cache=cache, user=current_user)

# Use in endpoint
@app.post('/users/{user_id}/deactivate')
async def deactivate_user(
    user_id: int,
    admin = Depends(require_permission('users.deactivate')),
    service = Depends(get_user_service)
):
    result = await service.deactivate_user(user_id)
    return result
```

## OAuth2 Dependencies

Implement OAuth2 authentication with dependencies.

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    HTTPBearer,
    HTTPAuthorizationCredentials
)
from datetime import datetime, timedelta
from jose import JWTError, jwt

# OAuth2 with password flow
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

SECRET_KEY = 'your-secret-key-here'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user_from_token(
    token: str = Depends(oauth2_scheme),
    db = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get('sub')
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await db.get_user_by_id(user_id)
    if user is None:
        raise credentials_exception
    return user

# OAuth2 with bearer token
bearer_scheme = HTTPBearer()

async def verify_bearer_token(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid authentication credentials'
        )

# OAuth2 with scopes
from fastapi.security import OAuth2PasswordBearer, SecurityScopes

oauth2_scheme_scopes = OAuth2PasswordBearer(
    tokenUrl='token',
    scopes={
        'users:read': 'Read user information',
        'users:write': 'Modify user information',
        'admin': 'Admin access'
    }
)

async def get_current_user_with_scopes(
    security_scopes: SecurityScopes,
    token: str = Depends(oauth2_scheme_scopes),
    db = Depends(get_db)
):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = 'Bearer'

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': authenticate_value},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get('sub')
        if user_id is None:
            raise credentials_exception
        token_scopes = payload.get('scopes', [])
    except JWTError:
        raise credentials_exception

    user = await db.get_user_by_id(user_id)
    if user is None:
        raise credentials_exception

    for scope in security_scopes.scopes:
        if scope not in token_scopes:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='Not enough permissions',
                headers={'WWW-Authenticate': authenticate_value},
            )
    return user

# Use with scopes
@app.get('/users/me', dependencies=[Security(
    get_current_user_with_scopes,
    scopes=['users:read']
)])
async def read_users_me(
    current_user = Depends(get_current_user_with_scopes)
):
    return current_user

@app.put('/users/me', dependencies=[Security(
    get_current_user_with_scopes,
    scopes=['users:write']
)])
async def update_user_me(
    user_update: UserUpdate,
    current_user = Depends(get_current_user_with_scopes),
    db = Depends(get_db)
):
    updated_user = await db.update_user(current_user.id, user_update)
    return updated_user
```

## Database Dependencies

Manage database connections with dependencies.

```python
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# SQLAlchemy setup
DATABASE_URL = 'postgresql+asyncpg://user:pass@localhost/db'
engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Dependency
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

# Usage
from sqlalchemy import select

@app.get('/users/{user_id}')
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    return user

# With transaction
@app.post('/users')
async def create_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    user = User(**user_data.dict())
    db.add(user)
    await db.flush()  # Get the ID before commit
    return user
```

## Authentication Dependencies

Implement authentication patterns.

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

SECRET_KEY = 'your-secret-key'
ALGORITHM = 'HS256'

# Token verification
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get('sub')
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await db.fetch_one('SELECT * FROM users WHERE email = ?', email)
    if user is None:
        raise credentials_exception
    return user

# Active user check
async def get_current_active_user(
    current_user = Depends(get_current_user)
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail='Inactive user')
    return current_user

# Role-based access
def require_role(required_role: str):
    async def role_checker(current_user = Depends(get_current_active_user)):
        if current_user.role != required_role:
            raise HTTPException(
                status_code=403,
                detail=f'Role {required_role} required'
            )
        return current_user
    return role_checker

@app.get('/admin')
async def admin_route(user = Depends(require_role('admin'))):
    return {'message': 'Admin access granted'}
```

## Caching Dependencies

Implement caching patterns with dependencies.

```python
from fastapi import Depends
from functools import lru_cache
import redis.asyncio as redis

# In-memory cache
@lru_cache()
def get_settings():
    return Settings()

@app.get('/config')
async def get_config(settings: Settings = Depends(get_settings)):
    return settings

# Redis cache dependency
class RedisCache:
    def __init__(self):
        self.redis = None

    async def get_connection(self):
        if not self.redis:
            self.redis = await redis.from_url('redis://localhost')
        return self.redis

    async def get(self, key: str):
        conn = await self.get_connection()
        value = await conn.get(key)
        return value.decode() if value else None

    async def set(self, key: str, value: str, expire: int = 3600):
        conn = await self.get_connection()
        await conn.set(key, value, ex=expire)

cache = RedisCache()

async def get_cache():
    return cache

@app.get('/cached-data/{key}')
async def get_cached_data(
    key: str,
    cache: RedisCache = Depends(get_cache)
):
    value = await cache.get(key)
    if value:
        return {'value': value, 'cached': True}

    # Fetch and cache
    value = fetch_expensive_data(key)
    await cache.set(key, value)
    return {'value': value, 'cached': False}
```

## Background Task Dependencies

Use dependencies with background tasks.

```python
from fastapi import BackgroundTasks, Depends
import asyncio

async def send_email(email: str, message: str):
    # Simulate sending email
    await asyncio.sleep(2)
    print(f'Email sent to {email}: {message}')

def get_email_service():
    # Could return configured email service
    return send_email

@app.post('/users')
async def create_user(
    user: UserCreate,
    background_tasks: BackgroundTasks,
    email_service = Depends(get_email_service),
    db = Depends(get_db)
):
    user_obj = await db.create_user(user)
    background_tasks.add_task(
        email_service,
        user.email,
        'Welcome to our service!'
    )
    return user_obj

# Complex background task with dependencies
class EmailService:
    def __init__(self, db = Depends(get_db)):
        self.db = db

    async def send_welcome_email(self, user_id: int):
        user = await self.db.get_user(user_id)
        await send_email(user.email, f'Welcome {user.name}!')

@app.post('/users/v2')
async def create_user_v2(
    user: UserCreate,
    background_tasks: BackgroundTasks,
    db = Depends(get_db)
):
    user_obj = await db.create_user(user)
    email_service = EmailService(db)
    background_tasks.add_task(
        email_service.send_welcome_email,
        user_obj.id
    )
    return user_obj

# Background task with cleanup
async def process_file_with_cleanup(file_path: str):
    try:
        # Process file
        await process_file(file_path)
    finally:
        # Cleanup
        os.remove(file_path)

@app.post('/upload')
async def upload_file(
    file: UploadFile,
    background_tasks: BackgroundTasks
):
    file_path = f'/tmp/{file.filename}'
    with open(file_path, 'wb') as f:
        f.write(await file.read())

    background_tasks.add_task(process_file_with_cleanup, file_path)
    return {'status': 'processing'}
```

## WebSocket Dependencies

Use dependencies with WebSocket connections.

```python
from fastapi import WebSocket, Depends, WebSocketDisconnect
from typing import List

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

def get_connection_manager():
    return manager

# WebSocket with authentication
async def get_ws_current_user(
    websocket: WebSocket,
    token: str = Query(...),
    db = Depends(get_db)
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get('sub')
        user = await db.get_user_by_id(user_id)
        if not user:
            await websocket.close(code=1008)
            raise HTTPException(status_code=401, detail='Invalid token')
        return user
    except JWTError:
        await websocket.close(code=1008)
        raise HTTPException(status_code=401, detail='Invalid token')

@app.websocket('/ws/{client_id}')
async def websocket_endpoint(
    websocket: WebSocket,
    client_id: int,
    manager: ConnectionManager = Depends(get_connection_manager),
    user = Depends(get_ws_current_user)
):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message = f'User {user.name}: {data}'
            await manager.broadcast(message)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f'User {user.name} left the chat')

# WebSocket with database
@app.websocket('/ws/messages/{room_id}')
async def message_websocket(
    websocket: WebSocket,
    room_id: int,
    db = Depends(get_db),
    user = Depends(get_ws_current_user)
):
    await websocket.accept()

    # Send message history
    messages = await db.get_room_messages(room_id)
    await websocket.send_json(messages)

    try:
        while True:
            data = await websocket.receive_text()
            # Save to database
            message = await db.create_message(
                room_id=room_id,
                user_id=user.id,
                content=data
            )
            await websocket.send_json(message)
    except WebSocketDisconnect:
        pass
```

## Custom Dependency Providers

Create custom dependency injection patterns.

```python
from typing import Callable, Type, TypeVar, Generic
from fastapi import Depends

T = TypeVar('T')

# Dependency factory
class DependencyFactory(Generic[T]):
    def __init__(self, dependency_class: Type[T], **kwargs):
        self.dependency_class = dependency_class
        self.kwargs = kwargs

    def __call__(self) -> T:
        return self.dependency_class(**self.kwargs)

# Service locator pattern
class ServiceLocator:
    def __init__(self):
        self._services = {}

    def register(self, name: str, service):
        self._services[name] = service

    def get(self, name: str):
        return self._services.get(name)

    def create_dependency(self, name: str):
        def get_service():
            service = self.get(name)
            if service is None:
                raise ValueError(f'Service {name} not registered')
            return service
        return get_service

# Initialize service locator
locator = ServiceLocator()
locator.register('db', Database('postgresql://localhost/db'))
locator.register('cache', Redis('redis://localhost'))

# Use in endpoint
get_db_from_locator = locator.create_dependency('db')

@app.get('/items')
async def get_items(db = Depends(get_db_from_locator)):
    return await db.fetch_all('SELECT * FROM items')

# Dependency provider with context
class ContextualDependency:
    def __init__(self, request: Request):
        self.request = request
        self.context = {}

    def set(self, key: str, value):
        self.context[key] = value

    def get(self, key: str):
        return self.context.get(key)

async def get_request_context(request: Request):
    context = ContextualDependency(request)
    context.set('request_id', str(uuid.uuid4()))
    context.set('timestamp', datetime.utcnow())
    return context

@app.get('/context-example')
async def context_example(context = Depends(get_request_context)):
    return {
        'request_id': context.get('request_id'),
        'timestamp': context.get('timestamp')
    }

# Lazy dependency loading
class LazyDependency:
    def __init__(self, factory: Callable):
        self.factory = factory
        self._instance = None

    def __call__(self):
        if self._instance is None:
            self._instance = self.factory()
        return self._instance

def create_expensive_service():
    print('Creating expensive service...')
    return ExpensiveService()

expensive_service = LazyDependency(create_expensive_service)

@app.get('/expensive')
async def use_expensive(service = Depends(expensive_service)):
    return service.do_work()
```

## Scoped Dependencies Per Request

Manage request-scoped state and lifecycle.

```python
from contextvars import ContextVar
from fastapi import Depends, Request

# Request-scoped storage using context variables
request_id_var: ContextVar[str] = ContextVar('request_id')

async def set_request_id(request: Request):
    request_id = request.headers.get('X-Request-ID', str(uuid.uuid4()))
    request_id_var.set(request_id)
    return request_id

async def get_request_id():
    return request_id_var.get()

# Request-scoped logger
class RequestLogger:
    def __init__(self, request_id: str = Depends(get_request_id)):
        self.request_id = request_id

    def info(self, message: str):
        print(f'[{self.request_id}] INFO: {message}')

    def error(self, message: str):
        print(f'[{self.request_id}] ERROR: {message}')

@app.get('/scoped-logging')
async def scoped_logging(
    request_id: str = Depends(set_request_id),
    logger: RequestLogger = Depends()
):
    logger.info('Processing request')
    # Do work
    logger.info('Request completed')
    return {'request_id': request_id}

# Request-scoped unit of work pattern
class UnitOfWork:
    def __init__(self, db = Depends(get_db)):
        self.db = db
        self.repositories = {}

    def get_repository(self, model_class):
        if model_class not in self.repositories:
            self.repositories[model_class] = Repository(self.db, model_class)
        return self.repositories[model_class]

    async def commit(self):
        await self.db.commit()

    async def rollback(self):
        await self.db.rollback()

@app.post('/complex-transaction')
async def complex_transaction(
    data: TransactionData,
    uow: UnitOfWork = Depends()
):
    try:
        user_repo = uow.get_repository(User)
        order_repo = uow.get_repository(Order)

        user = await user_repo.create(data.user)
        order = await order_repo.create(data.order, user_id=user.id)

        await uow.commit()
        return {'user': user, 'order': order}
    except Exception:
        await uow.rollback()
        raise
```

## Global Dependencies with app.dependency_overrides

Use global dependency management and overrides.

```python
from fastapi import FastAPI, Depends

app = FastAPI()

# Original dependencies
def get_production_db():
    return ProductionDatabase('postgresql://prod/db')

def get_production_cache():
    return RedisCache('redis://prod')

# Default app setup
@app.get('/data')
async def get_data(
    db = Depends(get_production_db),
    cache = Depends(get_production_cache)
):
    cached = await cache.get('data')
    if cached:
        return cached

    data = await db.fetch_all('SELECT * FROM data')
    await cache.set('data', data)
    return data

# Override for testing environment
if os.getenv('ENVIRONMENT') == 'test':
    def get_test_db():
        return TestDatabase(':memory:')

    def get_test_cache():
        return InMemoryCache()

    app.dependency_overrides[get_production_db] = get_test_db
    app.dependency_overrides[get_production_cache] = get_test_cache

# Override for development
if os.getenv('ENVIRONMENT') == 'development':
    def get_dev_db():
        return DevDatabase('postgresql://localhost/dev')

    app.dependency_overrides[get_production_db] = get_dev_db

# Dynamic override based on request
async def override_db_by_tenant(request: Request):
    tenant_id = request.headers.get('X-Tenant-ID')
    if tenant_id:
        return TenantDatabase(tenant_id)
    return get_production_db()

# Conditional override
def setup_dependencies(app: FastAPI, config: dict):
    if config.get('use_mock_db'):
        app.dependency_overrides[get_production_db] = lambda: MockDB()

    if config.get('use_local_cache'):
        app.dependency_overrides[get_production_cache] = lambda: LocalCache()

# Clear overrides
def clear_overrides():
    app.dependency_overrides = {}
```

## Testing with Dependencies

Override dependencies for testing.

```python
from fastapi.testclient import TestClient

# Original dependency
def get_db():
    db = ProductionDB()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides = {}

# Test with mock database
def test_get_users():
    def override_get_db():
        return MockDB()

    app.dependency_overrides[get_db] = override_get_db

    client = TestClient(app)
    response = client.get('/users')

    assert response.status_code == 200

    # Cleanup
    app.dependency_overrides = {}

# Pytest fixture for dependency override
import pytest

@pytest.fixture
def client():
    def override_get_db():
        return MockDB()

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client
    app.dependency_overrides = {}

def test_with_fixture(client):
    response = client.get('/users')
    assert response.status_code == 200
```

## Global Dependencies

Apply dependencies to all routes.

```python
from fastapi import FastAPI, Depends

# Logging dependency
async def log_request(request: Request):
    print(f'{request.method} {request.url}')

# Rate limiting
async def rate_limit(request: Request):
    client_ip = request.client.host
    # Check rate limit
    if is_rate_limited(client_ip):
        raise HTTPException(status_code=429, detail='Too many requests')

# Apply globally
app = FastAPI(dependencies=[Depends(log_request), Depends(rate_limit)])

# Apply to router
router = APIRouter(dependencies=[Depends(get_current_user)])

@router.get('/protected-resource')
async def protected_route():
    return {'message': 'This requires authentication'}

app.include_router(router)
```

## When to Use This Skill

Use fastapi-dependency-injection when building modern,
production-ready applications that require
advanced patterns, best practices, and optimal performance.

## FastAPI DI Best Practices

1. **Use yield for cleanup** - Always use yield for resources that
need cleanup like database connections, file handles, and network
connections to ensure proper resource management

2. **Leverage caching** - Use dependency caching (enabled by default)
to avoid redundant work within a request; multiple uses of the same
dependency in one request share the same instance

3. **Chain dependencies** - Build complex dependencies from simpler
sub-dependencies to create composable, testable, and maintainable code
structures

4. **Class-based for state** - Use classes for dependencies that
maintain state or configuration, leveraging `__call__` method for
callable instances

5. **Type hints everywhere** - Always add type hints for better editor
support, automatic validation, and improved documentation generation

6. **Override for testing** - Use dependency_overrides to inject mocks
during testing without modifying production code

7. **Global for cross-cutting** - Apply common dependencies (logging,
auth, rate limiting) globally or at router level to avoid repetition

8. **Async when possible** - Use async dependencies for I/O operations
to maximize performance and concurrency benefits

9. **Separate concerns** - Keep authentication, authorization, and
business logic in separate dependencies for better testability and
reusability

10. **Document dependencies** - Add docstrings to explain complex
dependency chains, especially when building multi-level hierarchies

11. **Use Security utilities** - Leverage FastAPI's security utilities
like OAuth2PasswordBearer and HTTPBearer for authentication patterns

12. **Validate early** - Place validation dependencies early in the
chain to fail fast and provide clear error messages

13. **Keep dependencies pure** - Dependencies should have minimal side
effects; use background tasks for non-critical operations

14. **Use context managers** - Wrap dependencies in context managers
when dealing with transactions or resource pools

15. **Dependency composition** - Compose larger dependencies from
smaller, focused ones rather than creating monolithic dependencies

## FastAPI DI Common Pitfalls

1. **Forgetting yield** - Not using yield means resources won't be
cleaned up properly, leading to connection leaks and resource exhaustion

2. **Circular dependencies** - Creating dependency cycles causes
infinite loops and stack overflow errors; design dependencies in a
directed acyclic graph

3. **Not using Depends()** - Forgetting Depends() wrapper means
function is called directly instead of being injected, breaking the
dependency resolution

4. **Overusing use_cache=False** - Disabling cache unnecessarily hurts
performance by creating multiple instances of the same dependency per
request

5. **Heavy dependencies** - Putting too much logic in dependencies
instead of services makes them hard to test and violates single
responsibility

6. **Not testing overrides** - Forgetting to test with
dependency_overrides means tests may use production resources instead
of mocks

7. **Mixing sync and async** - Incorrectly mixing synchronous and
asynchronous dependencies can block the event loop or cause runtime
errors

8. **Global state issues** - Not properly managing singleton
dependencies leads to shared state bugs in concurrent requests

9. **Exception handling** - Not handling exceptions in dependencies
properly can leave resources in inconsistent states or leak connections

10. **Type hint mistakes** - Missing or incorrect type hints break
dependency injection and automatic validation

11. **Ignoring dependency order** - Dependencies are executed in the
order they appear in function signature; incorrect order can cause
issues

12. **Not cleaning test overrides** - Forgetting to reset
app.dependency_overrides after tests causes subsequent tests to fail

13. **Overusing global dependencies** - Applying too many dependencies
globally can hurt performance and make debugging difficult

14. **Memory leaks with generators** - Not properly closing resources
in finally block of generator dependencies causes memory leaks

15. **Security misconfiguration** - Using weak or missing security
dependencies exposes endpoints to unauthorized access

## Advanced Caching Patterns

Implement sophisticated caching strategies with dependencies.

```python
from fastapi import Depends
import hashlib
import json

# Multi-layer cache with fallback
class CacheLayer:
    def __init__(
        self,
        memory_cache = Depends(get_memory_cache),
        redis_cache = Depends(get_redis_cache)
    ):
        self.memory = memory_cache
        self.redis = redis_cache

    async def get(self, key: str):
        # Try memory first
        value = self.memory.get(key)
        if value:
            return value

        # Try Redis
        value = await self.redis.get(key)
        if value:
            # Populate memory cache
            self.memory.set(key, value)
            return value

        return None

    async def set(self, key: str, value, ttl: int = 3600):
        self.memory.set(key, value, ttl=min(ttl, 300))
        await self.redis.set(key, value, ttl=ttl)

# Cache key generation
def create_cache_key(*args, **kwargs):
    key_data = json.dumps({'args': args, 'kwargs': kwargs}, sort_keys=True)
    return hashlib.md5(key_data.encode()).hexdigest()

# Dependency with automatic caching
def cached_dependency(ttl: int = 3600):
    async def dependency(
        params: dict,
        cache: CacheLayer = Depends()
    ):
        cache_key = create_cache_key(**params)
        cached_value = await cache.get(cache_key)

        if cached_value:
            return cached_value

        # Compute expensive value
        value = await compute_expensive_value(params)
        await cache.set(cache_key, value, ttl=ttl)
        return value

    return dependency

@app.get('/cached-endpoint')
async def cached_endpoint(
    result = Depends(cached_dependency(ttl=1800))
):
    return result

# Cache invalidation dependency
class CacheInvalidator:
    def __init__(self, cache: CacheLayer = Depends()):
        self.cache = cache
        self.invalidation_queue = []

    def invalidate(self, pattern: str):
        self.invalidation_queue.append(pattern)

    async def flush(self):
        for pattern in self.invalidation_queue:
            await self.cache.redis.delete_pattern(pattern)
        self.invalidation_queue.clear()

@app.post('/users')
async def create_user(
    user: UserCreate,
    db = Depends(get_db),
    invalidator: CacheInvalidator = Depends()
):
    new_user = await db.create_user(user)
    invalidator.invalidate('users:*')
    await invalidator.flush()
    return new_user
```

## Middleware-Style Dependencies

Use dependencies for cross-cutting concerns.

```python
from fastapi import Depends, Request
from time import time

# Request timing dependency
async def measure_request_time(request: Request):
    start_time = time()
    yield
    duration = time() - start_time
    print(f'{request.method} {request.url.path} took {duration:.3f}s')

# Request ID tracking
async def track_request_id(request: Request):
    request_id = request.headers.get('X-Request-ID', str(uuid.uuid4()))
    request.state.request_id = request_id
    yield request_id

def get_request_id(request: Request):
    return request.state.request_id

# Rate limiting per user
class RateLimiter:
    def __init__(self):
        self.requests = {}

    async def check_rate_limit(
        self,
        user = Depends(get_current_user),
        cache = Depends(get_cache)
    ):
        key = f'rate_limit:{user.id}'
        count = await cache.incr(key)

        if count == 1:
            await cache.expire(key, 60)

        if count > 100:
            raise HTTPException(
                status_code=429,
                detail='Rate limit exceeded'
            )
        return True

rate_limiter = RateLimiter()

@app.get('/protected')
async def protected_endpoint(
    rate_limit_ok = Depends(rate_limiter.check_rate_limit)
):
    return {'message': 'Success'}

# Request validation
async def validate_content_type(request: Request):
    content_type = request.headers.get('Content-Type')
    if not content_type or 'application/json' not in content_type:
        raise HTTPException(
            status_code=415,
            detail='Content-Type must be application/json'
        )
    return True

@app.post('/data', dependencies=[Depends(validate_content_type)])
async def post_data(data: dict):
    return data
```

## Resources

Official FastAPI documentation and guides:

- [FastAPI Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/)
  Core dependency injection concepts and basic usage
- [Advanced Dependencies](https://fastapi.tiangolo.com/advanced/advanced-dependencies/)
  Advanced patterns including dependency overrides and custom providers
- [Sub-Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/sub-dependencies/)
  Building complex dependency chains and hierarchies
- [Dependencies in Path Operations](https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-in-path-operation-decorators/)
  Using dependencies at the decorator level
- [Global Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/global-dependencies/)
  Applying dependencies to entire applications or routers
- [Testing Dependencies](https://fastapi.tiangolo.com/advanced/testing-dependencies/)
  Overriding dependencies for testing purposes
- [Security and OAuth2](https://fastapi.tiangolo.com/tutorial/security/)
  Security utilities and OAuth2 implementation with dependencies
- [SQL Databases](https://fastapi.tiangolo.com/tutorial/sql-databases/)
  Database session management with dependency injection
- [Async SQL](https://fastapi.tiangolo.com/advanced/async-sql-databases/)
  Async database patterns with SQLAlchemy

Additional resources:

- [FastAPI GitHub](https://github.com/tiangolo/fastapi)
  Source code and examples
- [FastAPI Discussions](https://github.com/tiangolo/fastapi/discussions)
  Community questions and patterns
- [Dependency Injection Design Pattern](https://en.wikipedia.org/wiki/Dependency_injection)
  General DI concepts and theory
