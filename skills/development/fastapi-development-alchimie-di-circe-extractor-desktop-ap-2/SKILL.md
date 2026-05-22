---
name: fastapi-development
description: Modern Python API development with FastAPI covering async patterns, Pydantic validation, dependency injection, and production deployment
---

# FastAPI Development

A comprehensive skill for building modern, high-performance Python APIs with FastAPI. Master async/await patterns, Pydantic data validation, dependency injection, authentication, database integration, and production-ready deployment strategies.

## When to Use This Skill

Use this skill when:

- Building RESTful APIs with Python for web, mobile, or microservices
- Developing high-performance, asynchronous backend services
- Creating APIs with automatic interactive documentation (OpenAPI/Swagger)
- Implementing OAuth2, JWT authentication, or other security patterns
- Integrating with SQL or NoSQL databases in Python applications
- Building APIs that require strong data validation and type safety
- Developing microservices with automatic request/response validation
- Creating APIs with WebSocket support for real-time features
- Migrating from Flask, Django REST Framework, or other Python frameworks
- Building production-ready APIs with proper error handling and testing
- **create FastAPI endpoint with SSE streaming** for agent communication
- **implement Unix socket IPC for osxphotos** sandbox integration
- **add circuit breaker for sidecar management** and crash recovery

## Core Concepts

### FastAPI Philosophy

FastAPI is built on three foundational principles:

- **Fast to Code**: Reduce development time with automatic validation and documentation
- **Fast to Run**: High performance comparable to NodeJS and Go (via Starlette and Pydantic)
- **Fewer Bugs**: Automatic validation reduces human errors by about 40%
- **Standards-Based**: Built on OpenAPI and JSON Schema standards
- **Editor Support**: Full autocomplete, type checking, and inline documentation

### Key FastAPI Features

1. **Type Hints**: Python 3.6+ type hints for validation and documentation
2. **Async Support**: Native async/await for high-performance I/O operations
3. **Pydantic Models**: Automatic request/response validation and serialization
4. **Dependency Injection**: Elegant system for sharing logic across endpoints
5. **OpenAPI Docs**: Automatic interactive API documentation
6. **Security**: Built-in support for OAuth2, JWT, API keys, and more
7. **Testing**: Easy to test with TestClient and async test support

### Core Architecture Components

1. **FastAPI App**: The main application instance
2. **Path Operations**: Endpoint definitions with HTTP methods
3. **Pydantic Models**: Data validation and serialization schemas
4. **Dependencies**: Reusable logic for authentication, database, etc.
5. **Routers**: Organize endpoints into modules
6. **Middleware**: Process requests/responses globally
7. **Background Tasks**: Execute code after returning responses

## Getting Started

### Installation

```bash
# Basic installation
pip install fastapi

# With ASGI server for production
pip install "fastapi[all]"

# Or install separately
pip install fastapi uvicorn[standard]

# Additional dependencies
pip install python-multipart  # For form data
pip install python-jose[cryptography]  # For JWT
pip install passlib[bcrypt]  # For password hashing
pip install sqlalchemy  # For SQL databases
pip install databases  # For async database support
```

### Minimal FastAPI Application

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

# Run with: uvicorn main:app --reload
```

## Pydantic Models for Data Validation

### Basic Model Definition

```python
from pydantic import BaseModel, Field, EmailStr, HttpUrl
from typing import Optional, List
from datetime import datetime

class User(BaseModel):
    id: int
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    full_name: Optional[str]
    is_active: bool

    class Config:
        orm_mode = True  # For SQLAlchemy models
```

### TRAE_Extractor-app: Agent Configuration Models

```python
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Literal, Dict, Any

class AgentToolConfig(BaseModel):
    """Configuration for a single agent tool"""
    name: str = Field(..., description="Tool name")
    type: Literal["mcp", "native", "api", "think", "memory", "filesystem"] = Field(
        ...,
        description="Tool type"
    )
    config: Dict[str, Any] = Field(
        default_factory=dict,
        description="Tool-specific configuration"
    )
    command: Optional[str] = Field(None, description="Command for MCP tools")
    args: Optional[List[str]] = Field(None, description="Command arguments")
    env: Optional[Dict[str, str]] = Field(None, description="Environment variables")

class AgentConfig(BaseModel):
    """Configuration for a single agent in Cagent team"""
    name: str = Field(..., min_length=1, max_length=50)
    model: str = Field(..., description="Model reference from models section")
    description: str = Field(..., min_length=10, description="Agent purpose")
    instruction: str = Field(..., min_length=50, description="Agent system prompt")
    toolsets: List[AgentToolConfig] = Field(
        default_factory=list,
        description="List of tool configurations"
    )
    rag: Optional[List[str]] = Field(
        None,
        description="List of RAG knowledge bases to use"
    )
    sub_agents: Optional[List[str]] = Field(
        None,
        description="List of sub-agent names this agent can delegate to"
    )
    add_prompt_files: Optional[List[str]] = Field(
        None,
        description="Additional prompt files to include"
    )

class CagentTeamConfig(BaseModel):
    """Complete Cagent team configuration"""
    version: str = Field(..., pattern=r'^\d+\.\d+$')
    models: Dict[str, Any] = Field(
        ...,
        description="Model definitions (provider, model name, max_tokens)"
    )
    agents: Dict[str, AgentConfig] = Field(
        ...,
        description="Agent configurations keyed by agent name"
    )
    rag: Optional[Dict[str, Any]] = Field(
        None,
        description="RAG knowledge base configurations"
    )
    metadata: Optional[Dict[str, str]] = Field(
        None,
        description="Team metadata (author, license, version)"
    )

# Example usage:
config = CagentTeamConfig(
    version="1.0",
    models={
        "sonnet": {
            "provider": "anthropic",
            "model": "claude-sonnet-4-5",
            "max_tokens": 64000
        }
    },
    agents={
        "captioning": AgentConfig(
            name="captioning",
            model="sonnet",
            description="Generates captions and social media copy",
            instruction="You are a captioning specialist...",
            toolsets=[
                AgentToolConfig(
                    type="mcp",
                    command="npx",
                    args=["-y", "@perplexity-ai/mcp-server"],
                    env={"PERPLEXITY_API_KEY": "${PERPLEXITY_API_KEY}"}
                )
            ],
            rag=["brand_guidelines", "platform_specs"]
        )
    }
)
```

### TRAE_Extractor-app: Brand Knowledge Schemas

```python
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict
from enum import Enum

class ToneStyle(str, Enum):
    """Brand tone styles"""
    INFORMAL_CONSCIOUS = "informal_conscious"
    PASSIONATE = "passionate"
    EDUCATIONAL = "educational"
    DIRECT = "direct"

class BrandGuideline(BaseModel):
    """Single brand guideline entry"""
    category: str = Field(..., description="Guideline category")
    content: str = Field(..., min_length=10, description="Guideline content")
    priority: Literal["high", "medium", "low"] = Field("medium")
    examples: Optional[List[str]] = Field(None, description="Example messages")

class BrandTone(BaseModel):
    """Brand tone of voice configuration"""
    style: ToneStyle = Field(..., description="Primary tone style")
    characteristics: List[str] = Field(
        ...,
        min_items=1,
        description="Tone characteristics"
    )
    do_examples: List[str] = Field(
        ...,
        min_items=1,
        description="Correct tone examples"
    )
    dont_examples: List[str] = Field(
        ...,
        min_items=1,
        description="Incorrect tone examples to avoid"
    )

class BrandKnowledge(BaseModel):
    """Complete brand knowledge base"""
    brand_name: str = Field(..., min_length=1)
    mission: str = Field(..., min_length=50)
    core_values: List[str] = Field(..., min_items=1)
    tone_guidelines: BrandTone
    visual_identity: Optional[Dict[str, str]] = Field(None)
    communication_principles: List[str] = Field(..., min_items=1)
    key_messages: List[str] = Field(..., min_items=1)
    audience_segments: Optional[Dict[str, Dict[str, str]]] = Field(None)
    hashtags: Dict[str, List[str]] = Field(
        default_factory=dict,
        description="Hashtag categories and lists"
    )

# Example usage:
slow_food_knowledge = BrandKnowledge(
    brand_name="Slow Food",
    mission="Slow Food promuove il diritto al piacere e difende il diritto al cibo buono, pulito e giusto per tutti.",
    core_values=[
        "Qualità e Autenticità",
        "Sostenibilità Ambientale",
        "Equità Economica",
        "Comunità e Cultura"
    ],
    tone_guidelines=BrandTone(
        style=ToneStyle.INFORMAL_CONSCIOUS,
        characteristics=["informale ma consapevole", "appassionato ma non predicatorio"],
        do_examples=[
            "Un caffè buono non nasce al bar freddo, ma dalle mani di chi coltiva e torrefà con cura ogni chicco"
        ],
        dont_examples=[
            "Compra locale o sei nemico dell'ambiente",
            "I nostri prodotti hanno un coefficiente di sostenibilità biocertificato standardizzato secondo ISO 14001"
        ]
    ),
    communication_principles=[
        "Trasparenza",
        "Autenticità",
        "Educazione",
        "Inclusività",
        "Comunità"
    ],
    key_messages=[
        "Il cibo buono non è un lusso, è un diritto",
        "Dietro ogni prodotto c'è una storia di territorio"
    ],
    hashtags={
        "primary": ["#SlowFood", "#BuonoLimpoGiusto"],
        "sustainability": ["#SoilHealth", "#BiodiversityMatters"],
        "community": ["#FoodCommunity", "#AgriculturalPride"]
    }
)
```

### TRAE_Extractor-app: Media Metadata Validation

```python
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Tuple
from datetime import datetime
from enum import Enum

class MediaType(str, Enum):
    """Media file types"""
    IMAGE = "image"
    VIDEO = "video"

class EXIFData(BaseModel):
    """EXIF metadata from photos"""
    camera_make: Optional[str] = Field(None, max_length=50)
    camera_model: Optional[str] = Field(None, max_length=50)
    date_taken: Optional[datetime] = Field(None)
    gps_coordinates: Optional[Tuple[float, float]] = Field(None)
    iso: Optional[int] = Field(None, ge=100, le=6400)
    aperture: Optional[float] = Field(None, ge=1.0, le=32.0)
    shutter_speed: Optional[str] = Field(None, max_length=20)
    focal_length: Optional[int] = Field(None, ge=1, le=1000)

class MediaMetadata(BaseModel):
    """Metadata for extracted media files"""
    filename: str = Field(..., pattern=r'^[\w\-\.]+\.(jpg|png|mp4|mov|jpeg)$')
    file_size_bytes: int = Field(..., gt=0)
    media_type: MediaType = Field(..., description="Type of media")
    exif_data: Optional[EXIFData] = Field(None)
    tags: List[str] = Field(
        default_factory=list,
        max_length=20,
        description="User-defined tags"
    )
    album: Optional[str] = Field(None, max_length=100)
    date_imported: datetime = Field(default_factory=datetime.utcnow)
    cloudinary_public_id: Optional[str] = Field(None)
    cloudinary_url: Optional[str] = Field(None, regex=r'^https://res\.cloudinary\.com/.*')

    @validator('filename')
    def validate_filename(cls, v):
        """Ensure filename has valid extension"""
        valid_extensions = ['.jpg', '.jpeg', '.png', '.mp4', '.mov']
        if not any(v.lower().endswith(ext) for ext in valid_extensions):
            raise ValueError(f'Invalid file extension. Must be one of: {valid_extensions}')
        return v

class MediaExtractionResult(BaseModel):
    """Result of media extraction operation"""
    album: str = Field(..., description="Source album name")
    export_path: str = Field(..., description="Export directory")
    media_count: int = Field(..., ge=0, description="Number of files extracted")
    media_files: List[MediaMetadata] = Field(..., description="Extracted media metadata")
    extraction_time: float = Field(..., gt=0, description="Extraction duration in seconds")
    success: bool = Field(..., description="Whether extraction succeeded")

# Example usage:
extraction_result = MediaExtractionResult(
    album="Summer 2024",
    export_path="~/Exports/summer-2024",
    media_count=42,
    media_files=[
        MediaMetadata(
            filename="sunset-beach.jpg",
            file_size_bytes=2048576,
            media_type=MediaType.IMAGE,
            exif_data=EXIFData(
                camera_make="Apple",
                camera_model="iPhone 15 Pro",
                date_taken=datetime(2024, 7, 15, 18, 30, 0),
                iso=100,
                aperture=2.8
            ),
            tags=["sunset", "beach", "summer"],
            album="Summer 2024"
        )
    ],
    extraction_time=12.5,
    success=True
)
```

### TRAE_Extractor-app: Post Scheduling Data Structures

```python
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum

class SocialPlatform(str, Enum):
    """Supported social media platforms"""
    INSTAGRAM = "instagram"
    FACEBOOK = "facebook"
    LINKEDIN = "linkedin"
    TWITTER = "twitter"
    TIKTOK = "tiktok"

class PostStatus(str, Enum):
    """Post scheduling status"""
    PENDING = "pending"
    SCHEDULED = "scheduled"
    PUBLISHED = "published"
    FAILED = "failed"
    CANCELLED = "cancelled"

class ScheduledPost(BaseModel):
    """Scheduled social media post"""
    post_id: Optional[str] = Field(None, description="Post ID from platform")
    media_id: str = Field(..., description="Cloudinary public ID or media file ID")
    caption: str = Field(..., min_length=10, max_length=2200, description="Post caption")
    platforms: List[SocialPlatform] = Field(..., min_items=1, description="Target platforms")
    scheduled_at: datetime = Field(..., description="Scheduled publish time")
    hashtags: List[str] = Field(
        default_factory=list,
        max_length=30,
        description="Hashtags to include"
    )
    status: PostStatus = Field(default=PostStatus.PENDING)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    published_at: Optional[datetime] = Field(None)
    error_message: Optional[str] = Field(None, description="Error if publishing failed")

    @validator('scheduled_at')
    def validate_scheduled_time(cls, v):
        """Ensure scheduled time is in the future"""
        if v <= datetime.utcnow():
            raise ValueError('Scheduled time must be in the future')
        return v

class CaptionVariation(BaseModel):
    """Caption variation for different platforms"""
    platform: SocialPlatform = Field(..., description="Target platform")
    caption: str = Field(..., min_length=10, max_length=2200)
    hashtags: List[str] = Field(default_factory=list, max_length=30)
    character_limit: Optional[int] = Field(None, description="Platform-specific character limit")

class CaptionGenerationResult(BaseModel):
    """Result of caption generation by agent"""
    media_id: str = Field(..., description="Media file ID")
    variations: List[CaptionVariation] = Field(..., min_items=1)
    suggested_hashtags: List[str] = Field(default_factory=list, max_length=30)
    tone_analysis: Optional[Dict[str, str]] = Field(None, description="Tone analysis results")
    generation_time: float = Field(..., gt=0)

# Example usage:
scheduled_post = ScheduledPost(
    media_id="cloudinary/summer-beach-abc123",
    caption="Beautiful sunset at the beach. The colors of nature never disappoint! 🌅 #sunset #beach #nature",
    platforms=[SocialPlatform.INSTAGRAM, SocialPlatform.FACEBOOK],
    scheduled_at=datetime(2024, 8, 1, 18, 0, 0),
    hashtags=["#sunset", "#beach", "#nature", "#summer"]
)
```

### Nested Models

```python
class Image(BaseModel):
    url: HttpUrl
    name: str

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    tax: Optional[float] = None
    tags: List[str] = []
    images: Optional[List[Image]] = None

# Request example:
# {
#   "name": "Laptop",
#   "price": 999.99,
#   "tags": ["electronics", "computers"],
#   "images": [
#     {"url": "http://example.com/img1.jpg", "name": "Front view"}
#   ]
# }
```

### Model Validation and Examples

```python
from pydantic import BaseModel, Field, validator

class Product(BaseModel):
    name: str = Field(..., example="MacBook Pro")
    price: float = Field(..., gt=0, example=1999.99)
    discount: Optional[float] = Field(None, ge=0, le=100, example=10.0)

    @validator('discount')
    def discount_check(cls, v, values):
        if v and 'price' in values:
            discounted = values['price'] * (1 - v/100)
            if discounted < 0:
                raise ValueError('Discounted price cannot be negative')
        return v

    class Config:
        schema_extra = {
            "example": {
                "name": "MacBook Pro 16",
                "price": 2499.99,
                "discount": 15.0
            }
        }
```

## Path Operations and Routing

### HTTP Methods and Path Parameters

```python
from fastapi import FastAPI, Path, Query, Body
from typing import Optional

app = FastAPI()

# GET with path parameter
@app.get("/items/{item_id}")
async def read_item(
    item_id: int = Path(..., title="The ID of the item", ge=1),
    q: Optional[str] = Query(None, max_length=50)
):
    return {"item_id": item_id, "q": q}

# POST with request body
@app.post("/items/")
async def create_item(item: Item):
    return {"item": item, "message": "Item created"}

# PUT for updates
@app.put("/items/{item_id}")
async def update_item(
    item_id: int,
    item: Item = Body(...),
):
    return {"item_id": item_id, "item": item}

# DELETE
@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    return {"message": f"Item {item_id} deleted"}

# PATCH for partial updates
@app.patch("/items/{item_id}")
async def partial_update_item(
    item_id: int,
    item: dict = Body(...)
):
    return {"item_id": item_id, "updated_fields": item}
```

### Query Parameters with Validation

```python
from fastapi import Query
from typing import List, Optional

@app.get("/search/")
async def search_items(
    q: str = Query(..., min_length=3, max_length=50),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    sort_by: Optional[str] = Query(None, regex="^(name|price|date)$"),
    tags: List[str] = Query([], description="Filter by tags")
):
    return {
        "q": q,
        "skip": skip,
        "limit": limit,
        "sort_by": sort_by,
        "tags": tags
    }
```

### Response Models

```python
from typing import List

@app.post("/users/", response_model=UserResponse)
async def create_user(user: UserCreate):
    # Hash password, save to DB
    db_user = {
        "id": 1,
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name,
        "is_active": True
    }
    return db_user

@app.get("/users/", response_model=List[UserResponse])
async def list_users(skip: int = 0, limit: int = 100):
    users = [...]  # Fetch from database
    return users

# Exclude fields from response
class UserInDB(User):
    hashed_password: str

@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    user = get_user_from_db(user_id)  # Returns UserInDB
    return user  # Password excluded automatically
```

## Async/Await Patterns

### When to Use async vs def

```python
# Use async def when:
# - Making database queries with async driver
# - Calling external APIs with httpx/aiohttp
# - Using async I/O operations
# - Working with async libraries

@app.get("/async-example")
async def async_endpoint():
    # Can use await inside
    result = await async_database_query()
    external_data = await async_http_call()
    return {"result": result, "external": external_data}

# Use def when:
# - Working with synchronous libraries
# - Performing CPU-bound operations
# - No async operations needed

@app.get("/sync-example")
def sync_endpoint():
    # Regular synchronous code
    result = synchronous_database_query()
    return {"result": result}
```

### Async Database Operations

```python
import asyncio
from databases import Database

DATABASE_URL = "postgresql://user:password@localhost/dbname"
database = Database(DATABASE_URL)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    query = "SELECT * FROM users WHERE id = :user_id"
    user = await database.fetch_one(query, {"user_id": user_id})
    return user

@app.post("/users/")
async def create_user(user: UserCreate):
    query = """
        INSERT INTO users (username, email, hashed_password)
        VALUES (:username, :email, :password)
        RETURNING *
    """
    hashed_password = hash_password(user.password)
    new_user = await database.fetch_one(
        query,
        {
            "username": user.username,
            "email": user.email,
            "password": hashed_password
        }
    )
    return new_user
```

### Concurrent Operations

```python
import asyncio
import httpx

async def fetch_user(user_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://api.example.com/users/{user_id}")
        return response.json()

@app.get("/users/batch")
async def get_multiple_users(user_ids: List[int] = Query(...)):
    # Fetch all users concurrently
    users = await asyncio.gather(*[fetch_user(uid) for uid in user_ids])
    return {"users": users}
```

## Dependency Injection

### Basic Dependencies

```python
from fastapi import Depends
from typing import Optional

# Simple dependency function
async def common_parameters(
    q: Optional[str] = None,
    skip: int = 0,
    limit: int = 100
):
    return {"q": q, "skip": skip, "limit": limit}

@app.get("/items/")
async def read_items(commons: dict = Depends(common_parameters)):
    return commons

@app.get("/users/")
async def read_users(commons: dict = Depends(common_parameters)):
    return commons
```

### Class-Based Dependencies

```python
class Pagination:
    def __init__(
        self,
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=100)
    ):
        self.skip = skip
        self.limit = limit

@app.get("/items/")
async def list_items(pagination: Pagination = Depends()):
    return {
        "skip": pagination.skip,
        "limit": pagination.limit,
        "items": []  # Fetch with pagination
    }
```

### Database Session Dependency

```python
from sqlalchemy.orm import Session
from typing import Generator

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users/{user_id}")
async def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

### Sub-Dependencies

```python
from fastapi import Header, HTTPException

async def verify_token(x_token: str = Header(...)):
    if x_token != "secret-token":
        raise HTTPException(status_code=400, detail="Invalid token")
    return x_token

async def verify_key(x_key: str = Header(...)):
    if x_key != "secret-key":
        raise HTTPException(status_code=400, detail="Invalid key")
    return x_key

async def verify_credentials(
    token: str = Depends(verify_token),
    key: str = Depends(verify_key)
):
    return {"token": token, "key": key}

@app.get("/protected/")
async def protected_route(credentials: dict = Depends(verify_credentials)):
    return {"message": "Access granted", "credentials": credentials}
```

### Global Dependencies

```python
async def log_requests():
    print("Request received")

app = FastAPI(dependencies=[Depends(log_requests)])

# This dependency runs for ALL endpoints
```

## Authentication and Security

### OAuth2 Password Bearer with JWT

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional

SECRET_KEY = "your-secret-key-here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = get_user_from_db(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user
```

### API Key Authentication

```python
from fastapi import Security
from fastapi.security import APIKeyHeader

API_KEY = "your-api-key"
api_key_header = APIKeyHeader(name="X-API-Key")

async def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API Key"
        )
    return api_key

@app.get("/secure-data")
async def get_secure_data(api_key: str = Depends(verify_api_key)):
    return {"data": "This is secure data"}
```

### OAuth2 with Scopes

```python
from fastapi.security import OAuth2PasswordBearer, SecurityScopes

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={
        "items:read": "Read items",
        "items:write": "Create and update items",
        "users:read": "Read user information"
    }
)

async def get_current_user_with_scopes(
    security_scopes: SecurityScopes,
    token: str = Depends(oauth2_scheme)
):
    # Verify token and check scopes
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )

    # Decode JWT and verify scopes...
    return user

@app.get("/items/", dependencies=[Security(get_current_user_with_scopes, scopes=["items:read"])])
async def read_items():
    return [{"item": "Item 1"}, {"item": "Item 2"}]

@app.post("/items/", dependencies=[Security(get_current_user_with_scopes, scopes=["items:write"])])
async def create_item(item: Item):
    return {"item": item}
```

## Database Integration

### SQLAlchemy Setup

```python
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost/dbname"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Models
class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

Base.metadata.create_all(bind=engine)
```

### CRUD Operations

```python
from sqlalchemy.orm import Session

# Create
@app.post("/users/", response_model=UserResponse)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = UserModel(
        username=user.username,
        email=user.email,
        hashed_password=get_password_hash(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Read
@app.get("/users/{user_id}", response_model=UserResponse)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Update
@app.put("/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_update: UserCreate,
    db: Session = Depends(get_db)
):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.username = user_update.username
    user.email = user_update.email
    if user_update.password:
        user.hashed_password = get_password_hash(user_update.password)

    db.commit()
    db.refresh(user)
    return user

# Delete
@app.delete("/users/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}
```

## Background Tasks

```python
from fastapi import BackgroundTasks

def send_email(email: str, message: str):
    # Simulate sending email
    print(f"Sending email to {email}: {message}")

def process_file(filename: str):
    # Simulate file processing
    print(f"Processing file: {filename}")

@app.post("/send-notification/")
async def send_notification(
    email: str,
    background_tasks: BackgroundTasks
):
    background_tasks.add_task(send_email, email, "Welcome!")
    return {"message": "Notification scheduled"}

@app.post("/upload/")
async def upload_file(
    file: str,
    background_tasks: BackgroundTasks
):
    # Save file first
    background_tasks.add_task(process_file, file)
    return {"message": "File uploaded, processing in background"}
```

## SSE Streaming for Agent Communication

Server-Sent Events (SSE) enable real-time streaming of agent updates from the Python sidecar to the Electron renderer. This pattern is essential for providing live feedback during long-running agent operations.

### Basic SSE Endpoint

```python
from fastapi import APIRouter
from sse_starlette.sse import EventSourceResponse
import asyncio
from typing import AsyncGenerator

agent_router = APIRouter(prefix="/agent", tags=["agent"])

# Global event queues for SSE streams
event_queues: dict[str, asyncio.Queue] = {}

class StreamEvent(BaseModel):
    """Event streamed via SSE"""
    event_type: str  # 'thinking', 'tool_call', 'result', 'error', 'keepalive'
    data: dict
    timestamp: float

async def agent_event_generator(request_id: str) -> AsyncGenerator:
    """Generate events from agent event queue for SSE streaming"""
    # Create queue if not exists
    if request_id not in event_queues:
        event_queues[request_id] = asyncio.Queue()
    
    queue = event_queues[request_id]
    
    try:
        while True:
            try:
                # Wait for event with timeout (30s)
                event = await asyncio.wait_for(queue.get(), timeout=30.0)
                yield {
                    "event": event.event_type,
                    "data": event.json(),
                }
                
                # Stop streaming on terminal events
                if event.event_type in ("result", "error"):
                    break
                    
            except asyncio.TimeoutError:
                # Send keepalive event to prevent connection timeout
                yield {
                    "event": "keepalive",
                    "data": "{}",
                }
    except asyncio.CancelledError:
        pass
    finally:
        # Cleanup queue
        if request_id in event_queues:
            del event_queues[request_id]

@agent_router.get("/stream/{request_id}")
async def stream_events(request_id: str):
    """
    Stream real-time events from agent execution via Server-Sent Events.
    
    Usage:
    - Client connects to /agent/stream/{request_id}
    - Server sends events as they occur
    - Stream ends when terminal event (result/error) is sent
    """
    return EventSourceResponse(
        agent_event_generator(request_id),
        media_type="text/event-stream",
    )
```

### Sending Events to Stream

```python
async def send_agent_event(request_id: str, event_type: str, data: dict):
    """Send event to agent stream"""
    if request_id in event_queues:
        event = StreamEvent(
            event_type=event_type,
            data=data,
            timestamp=time.time()
        )
        await event_queues[request_id].put(event)

# Example: Stream agent thinking process
async def execute_agent_with_streaming(agent_id: str, request_id: str, input_data: dict):
    await send_agent_event(request_id, "thinking", {"agent": agent_id, "status": "starting"})
    
    # Execute agent logic
    result = await run_agent(agent_id, input_data)
    
    await send_agent_event(request_id, "result", {"agent": agent_id, "result": result})
```

### Client-Side SSE Consumption

```typescript
// In Electron renderer
const eventSource = new EventSource('http://localhost:8000/agent/stream/req-123');

eventSource.addEventListener('thinking', (e) => {
  const data = JSON.parse(e.data);
  console.log('Agent thinking:', data);
});

eventSource.addEventListener('result', (e) => {
  const data = JSON.parse(e.data);
  console.log('Agent result:', data);
  eventSource.close();
});

eventSource.onerror = () => {
  console.error('SSE connection error');
  eventSource.close();
};
```

## Unix Socket IPC with osxphotos Sandbox

Unix socket IPC enables secure communication between the Python sidecar and the osxphotos sandbox process. This pattern ensures osxphotos runs in isolation with no network access and strict path whitelisting.

### Security Considerations

- **NO network access**: osxphotos process cannot make HTTP requests
- **Read-only on Photos Library**: osxphotos can only read from Apple Photos
- **Write whitelist**: Export paths must be pre-approved directories
- **Sandbox isolation**: Process runs in restricted environment

### Unix Socket Client

```python
import socket
import json
import os
from typing import Optional, Dict, Any

class OsxphotosSandboxClient:
    """Client for communicating with osxphotos sandbox via Unix socket"""
    
    def __init__(self, socket_path: str):
        self.socket_path = socket_path
        self.timeout = 30  # seconds
    
    async def extract_photos(
        self,
        album: str,
        export_path: str,
        options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Extract photos from album via osxphotos sandbox.
        
        Args:
            album: Photos album name
            export_path: Destination directory (must be in whitelist)
            options: Additional extraction options
            
        Returns:
            Dict with extraction results
            
        Raises:
            ValueError: If export path is not in whitelist
            ConnectionError: If socket connection fails
        """
        # Validate export path is in whitelist
        if not self._is_path_allowed(export_path):
            raise ValueError(
                f"Export path not in whitelist: {export_path}. "
                f"Allowed paths: {self._get_allowed_paths()}"
            )
        
        request = {
            "method": "extract",
            "params": {
                "album": album,
                "export_path": export_path,
                "options": options or {}
            }
        }
        
        try:
            with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
                s.settimeout(self.timeout)
                s.connect(self.socket_path)
                
                # Send request
                s.sendall(json.dumps(request).encode('utf-8'))
                
                # Receive response
                response_data = b""
                while True:
                    chunk = s.recv(4096)
                    if not chunk:
                        break
                    response_data += chunk
                
                response = json.loads(response_data.decode('utf-8'))
                
                if response.get("status") == "error":
                    raise RuntimeError(response.get("message", "Unknown error"))
                
                return response
                
        except socket.timeout:
            raise ConnectionError(f"Socket timeout after {self.timeout}s")
        except FileNotFoundError:
            raise ConnectionError(f"Socket not found: {self.socket_path}")
        except Exception as e:
            raise ConnectionError(f"Socket communication failed: {e}")
    
    def _is_path_allowed(self, path: str) -> bool:
        """Check if path is in allowed whitelist"""
        expanded_path = os.path.expanduser(path)
        allowed_paths = self._get_allowed_paths()
        return any(expanded_path.startswith(p) for p in allowed_paths)
    
    def _get_allowed_paths(self) -> list[str]:
        """Get list of allowed export paths"""
        return [
            os.path.expanduser("~/Exports/"),
            os.path.expanduser("~/Documents/TraeExports/"),
            os.path.expanduser("~/Desktop/TraeExports/"),
        ]
```

### Unix Socket Server (osxphotos Side)

```python
import socket
import json
import os
from pathlib import Path

class OsxphotosSandboxServer:
    """Unix socket server for osxphotos sandbox"""
    
    def __init__(self, socket_path: str):
        self.socket_path = socket_path
        self.running = False
    
    def start(self):
        """Start the Unix socket server"""
        # Remove existing socket if present
        if os.path.exists(self.socket_path):
            os.unlink(self.socket_path)
        
        server_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        server_socket.bind(self.socket_path)
        server_socket.listen(5)
        self.running = True
        
        print(f"osxphotos sandbox server listening on {self.socket_path}")
        
        while self.running:
            try:
                conn, _ = server_socket.accept()
                self._handle_request(conn)
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Error handling connection: {e}")
        
        server_socket.close()
    
    def _handle_request(self, conn: socket.socket):
        """Handle incoming request"""
        try:
            # Receive request
            request_data = b""
            while True:
                chunk = conn.recv(4096)
                if not chunk:
                    break
                request_data += chunk
            
            request = json.loads(request_data.decode('utf-8'))
            
            # Process request
            if request["method"] == "extract":
                response = self._extract_photos(request["params"])
            else:
                response = {
                    "status": "error",
                    "message": f"Unknown method: {request['method']}"
                }
            
            # Send response
            conn.sendall(json.dumps(response).encode('utf-8'))
            
        except Exception as e:
            error_response = {
                "status": "error",
                "message": str(e)
            }
            conn.sendall(json.dumps(error_response).encode('utf-8'))
        finally:
            conn.close()
    
    def _extract_photos(self, params: dict) -> dict:
        """Extract photos using osxphotos (sandboxed)"""
        # Import osxphotos here to ensure it's loaded in sandbox
        import osxphotos
        
        album = params["album"]
        export_path = params["export_path"]
        options = params.get("options", {})
        
        # Validate export path
        if not self._is_path_allowed(export_path):
            return {
                "status": "error",
                "message": f"Export path not allowed: {export_path}"
            }
        
        # Extract photos
        photos = osxphotos.export(
            album,
            export_path,
            **options
        )
        
        return {
            "status": "success",
            "photos": photos,
            "count": len(photos)
        }
    
    def _is_path_allowed(self, path: str) -> bool:
        """Check if path is in allowed whitelist"""
        expanded_path = os.path.expanduser(path)
        allowed_paths = [
            os.path.expanduser("~/Exports/"),
            os.path.expanduser("~/Documents/TraeExports/"),
            os.path.expanduser("~/Desktop/TraeExports/"),
        ]
        return any(expanded_path.startswith(p) for p in allowed_paths)
    
    def stop(self):
        """Stop the server"""
        self.running = False
        if os.path.exists(self.socket_path):
            os.unlink(self.socket_path)
```

### Integration with FastAPI

```python
from fastapi import FastAPI, HTTPException

app = FastAPI()

# Initialize osxphotos client
osxphotos_client = OsxphotosSandboxClient("/tmp/osxphotos.sock")

@app.post("/photos/extract")
async def extract_photos(album: str, export_path: str):
    """Extract photos from album via osxphotos sandbox"""
    try:
        result = await osxphotos_client.extract_photos(album, export_path)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ConnectionError as e:
        raise HTTPException(status_code=503, detail="osxphotos sandbox not available")
```

## Circuit Breaker for Sidecar Lifecycle

Circuit breaker pattern prevents cascading failures when the Python sidecar crashes repeatedly. It tracks failures and temporarily stops restart attempts after a threshold.

### Circuit Breaker Implementation

```python
from datetime import datetime, timedelta
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

class CircuitBreaker:
    """Circuit breaker for sidecar lifecycle management"""
    
    def __init__(
        self,
        max_failures: int = 3,
        window_minutes: int = 5,
        cooldown_minutes: int = 10
    ):
        """
        Initialize circuit breaker.
        
        Args:
            max_failures: Maximum failures before opening circuit
            window_minutes: Time window to count failures
            cooldown_minutes: Time to wait before retrying after opening
        """
        self.max_failures = max_failures
        self.window_minutes = window_minutes
        self.cooldown_minutes = cooldown_minutes
        self.failures: List[datetime] = []
        self.state = "closed"  # closed, open, half-open
        self.last_failure_time: Optional[datetime] = None
    
    def record_failure(self):
        """Record a failure and update circuit state"""
        now = datetime.now()
        self.failures.append(now)
        self.last_failure_time = now
        
        # Remove failures outside window
        self.failures = [
            f for f in self.failures
            if now - f < timedelta(minutes=self.window_minutes)
        ]
        
        # Check if threshold exceeded
        if len(self.failures) >= self.max_failures:
            self.state = "open"
            logger.warning(
                f"Circuit breaker OPEN: {len(self.failures)} failures in "
                f"{self.window_minutes} minutes. Cooldown for {self.cooldown_minutes} minutes."
            )
    
    def record_success(self):
        """Record a success and reset circuit state"""
        self.failures.clear()
        self.state = "closed"
        self.last_failure_time = None
        logger.info("Circuit breaker CLOSED: Sidecar is healthy")
    
    def can_execute(self) -> bool:
        """
        Check if operation can be executed.
        
        Returns:
            True if circuit is closed or half-open, False if open
        """
        if self.state == "closed":
            return True
        
        if self.state == "open":
            # Check if cooldown period has passed
            if self.last_failure_time:
                time_since_failure = datetime.now() - self.last_failure_time
                if time_since_failure >= timedelta(minutes=self.cooldown_minutes):
                    self.state = "half-open"
                    logger.info("Circuit breaker HALF-OPEN: Attempting recovery")
                    return True
            return False
        
        if self.state == "half-open":
            return True
        
        return False
    
    def get_status(self) -> dict:
        """Get current circuit breaker status"""
        return {
            "state": self.state,
            "failures_in_window": len(self.failures),
            "max_failures": self.max_failures,
            "last_failure": self.last_failure_time.isoformat() if self.last_failure_time else None,
            "can_execute": self.can_execute()
        }
```

### Integration with Sidecar Manager

```python
from typing import Optional

class SidecarManager:
    """Manages Python sidecar lifecycle with circuit breaker"""
    
    def __init__(self):
        self.circuit_breaker = CircuitBreaker(
            max_failures=3,
            window_minutes=5,
            cooldown_minutes=10
        )
        self.process: Optional[subprocess.Popen] = None
    
    async def start(self) -> bool:
        """Start sidecar if circuit breaker allows"""
        if not self.circuit_breaker.can_execute():
            logger.warning(
                f"Cannot start sidecar: Circuit breaker is {self.circuit_breaker.state}"
            )
            return False
        
        try:
            # Start sidecar process
            self.process = subprocess.Popen(
                ["python", "main.py"],
                cwd="python/",
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Wait for health check
            await self._wait_for_health()
            
            # Record success
            self.circuit_breaker.record_success()
            return True
            
        except Exception as e:
            logger.error(f"Failed to start sidecar: {e}")
            self.circuit_breaker.record_failure()
            return False
    
    async def _wait_for_health(self, timeout: int = 30):
        """Wait for sidecar to become healthy"""
        import httpx
        
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                response = await httpx.get("http://localhost:8000/health")
                if response.status_code == 200:
                    return
            except Exception:
                pass
            await asyncio.sleep(1)
        
        raise TimeoutError("Sidecar health check timeout")
    
    def stop(self):
        """Stop sidecar process"""
        if self.process:
            self.process.terminate()
            self.process.wait()
            self.process = None
    
    def get_status(self) -> dict:
        """Get sidecar status including circuit breaker"""
        return {
            "running": self.process is not None,
            "circuit_breaker": self.circuit_breaker.get_status()
        }
```

### Usage Example

```python
# Initialize sidecar manager
sidecar_manager = SidecarManager()

# Try to start sidecar
if await sidecar_manager.start():
    print("Sidecar started successfully")
else:
    print("Sidecar cannot start (circuit breaker open)")
    print(f"Status: {sidecar_manager.get_status()}")

# Check status
status = sidecar_manager.get_status()
print(f"Circuit breaker state: {status['circuit_breaker']['state']}")
print(f"Can execute: {status['circuit_breaker']['can_execute']}")
```

## Error Handling

### Custom Exception Handlers

```python
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

class CustomException(Exception):
    def __init__(self, name: str):
        self.name = name

@app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name} did something wrong."},
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()},
    )

@app.get("/items/{item_id}")
async def read_item(item_id: str):
    if item_id == "error":
        raise CustomException(name="Item")
    return {"item_id": item_id}
```

## Testing

### Basic Tests with TestClient

```python
from fastapi.testclient import TestClient

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_create_item():
    response = client.post(
        "/items/",
        json={"name": "Test Item", "price": 10.5}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Test Item"

def test_authentication():
    response = client.post(
        "/token",
        data={"username": "testuser", "password": "testpass"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
```

### Async Tests

```python
import pytest
from httpx import AsyncClient

@pytest.mark.anyio
async def test_read_items():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/items/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.anyio
async def test_create_user():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/users/",
            json={
                "username": "newuser",
                "email": "new@example.com",
                "password": "securepass123"
            }
        )
    assert response.status_code == 200
    assert response.json()["username"] == "newuser"
```

## Routers and Organization

### APIRouter for Modular Code

```python
# routers/users.py
from fastapi import APIRouter, Depends

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(verify_token)],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def list_users():
    return [{"username": "user1"}, {"username": "user2"}]

@router.get("/{user_id}")
async def get_user(user_id: int):
    return {"user_id": user_id}

# main.py
from routers import users

app = FastAPI()
app.include_router(users.router)
```

## Best Practices

### 1. Project Structure

```
my_fastapi_project/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── item.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── item.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── users.py
│   │   └── items.py
│   ├── dependencies/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── database.py
│   └── utils/
│       ├── __init__.py
│       └── security.py
├── tests/
│   ├── __init__.py
│   ├── test_users.py
│   └── test_items.py
├── requirements.txt
├── .env
└── README.md
```

### 2. Configuration Management

```python
from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "My FastAPI App"
    database_url: str
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"

settings = Settings()
```

### 3. Documentation

```python
app = FastAPI(
    title="My API",
    description="This is a very custom API",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "users",
            "description": "Operations with users.",
        },
        {
            "name": "items",
            "description": "Manage items.",
        },
    ]
)

@app.post(
    "/items/",
    response_model=Item,
    tags=["items"],
    summary="Create an item",
    description="Create an item with all the information",
    response_description="The created item",
)
async def create_item(item: Item):
    return item
```

## Production Deployment

### Docker Setup

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Run with Gunicorn and Uvicorn Workers

```bash
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

---

**Skill Version**: 1.0.0
**Last Updated**: October 2025
**Skill Category**: Backend Development, API Development, Python
**Compatible With**: FastAPI 0.100+, Python 3.7+, Pydantic 2.0+
