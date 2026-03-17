---
name: Beanie ODM
description: This skill should be used when the user asks to "create MongoDB model", "define Beanie document", "write MongoDB query", "create aggregation pipeline", "run database migration", "index MongoDB collection", or mentions Beanie, Motor, MongoDB documents, or async database operations. Provides MongoDB/Beanie ODM patterns for FastAPI.
version: 0.1.0
---

# Beanie ODM for MongoDB

This skill provides patterns for MongoDB integration using Beanie ODM with async Motor driver, optimized for FastAPI applications.

## Database Initialization

### Connection Setup

```python
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from app.domains.users.models import User
from app.domains.products.models import Product

async def init_database(settings: Settings):
    client = AsyncIOMotorClient(settings.mongodb_url)

    await init_beanie(
        database=client[settings.database_name],
        document_models=[
            User,
            Product,
            # Add all document models
        ]
    )
```

### Settings Configuration

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    mongodb_url: str = "mongodb://localhost:27017"
    database_name: str = "app_db"

    class Config:
        env_file = ".env"
```

## Document Models

### Basic Document

```python
from beanie import Document, Indexed
from pydantic import Field, EmailStr
from datetime import datetime
from typing import Optional

class User(Document):
    email: Indexed(EmailStr, unique=True)
    name: str
    hashed_password: str
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "users"  # Collection name
        use_state_management = True

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "name": "John Doe"
            }
        }
```

### Document with Relationships

```python
from beanie import Document, Link, BackLink
from typing import List, Optional

class Author(Document):
    name: str
    books: List[BackLink["Book"]] = Field(original_field="author")

    class Settings:
        name = "authors"

class Book(Document):
    title: str
    author: Link[Author]
    categories: List[Link["Category"]] = []

    class Settings:
        name = "books"

class Category(Document):
    name: str
    books: List[BackLink[Book]] = Field(original_field="categories")

    class Settings:
        name = "categories"
```

### Embedded Documents

```python
from beanie import Document
from pydantic import BaseModel
from typing import List

class Address(BaseModel):
    street: str
    city: str
    country: str
    postal_code: str

class Contact(BaseModel):
    type: str  # "email", "phone"
    value: str
    is_primary: bool = False

class Customer(Document):
    name: str
    addresses: List[Address] = []
    contacts: List[Contact] = []

    class Settings:
        name = "customers"
```

## Query Patterns

### Basic CRUD Operations

```python
# Create
user = User(email="user@example.com", name="John")
await user.insert()

# Create with validation
user = await User.insert_one(
    User(email="user@example.com", name="John")
)

# Read by ID
user = await User.get(user_id)

# Read with filter
users = await User.find(User.is_active == True).to_list()

# Update
user.name = "Jane"
await user.save()

# Partial update
await user.set({User.name: "Jane", User.updated_at: datetime.utcnow()})

# Delete
await user.delete()
```

### Advanced Queries

```python
from beanie.operators import In, RegEx, And, Or

# Find with operators
active_users = await User.find(
    And(
        User.is_active == True,
        User.created_at >= start_date
    )
).to_list()

# Regex search
users = await User.find(
    RegEx(User.name, "^John", options="i")
).to_list()

# In operator
users = await User.find(
    In(User.email, ["a@test.com", "b@test.com"])
).to_list()

# Pagination
users = await User.find_all().skip(20).limit(10).to_list()

# Sorting
users = await User.find_all().sort(-User.created_at).to_list()

# Projection (select specific fields)
users = await User.find_all().project(UserSummary).to_list()
```

## Aggregation Pipelines

```python
from beanie import PydanticObjectId

class UserStats(BaseModel):
    total_users: int
    active_users: int
    avg_age: float

# Aggregation pipeline
pipeline = [
    {"$match": {"is_active": True}},
    {"$group": {
        "_id": None,
        "total": {"$sum": 1},
        "avg_age": {"$avg": "$age"}
    }}
]

result = await User.aggregate(pipeline).to_list()

# Using Beanie aggregation
from beanie.odm.queries.aggregation import AggregationQuery

stats = await User.find(User.is_active == True).aggregate([
    {"$group": {
        "_id": "$department",
        "count": {"$sum": 1}
    }}
]).to_list()
```

## Indexes

```python
from beanie import Document, Indexed
from pymongo import IndexModel, ASCENDING, DESCENDING, TEXT

class Product(Document):
    # Single field index
    sku: Indexed(str, unique=True)

    # Compound index defined in Settings
    name: str
    category: str
    price: float
    description: str

    class Settings:
        name = "products"
        indexes = [
            # Compound index
            IndexModel(
                [("category", ASCENDING), ("price", DESCENDING)],
                name="category_price_idx"
            ),
            # Text index
            IndexModel(
                [("name", TEXT), ("description", TEXT)],
                name="search_idx"
            ),
            # TTL index
            IndexModel(
                [("expires_at", ASCENDING)],
                expireAfterSeconds=0,
                name="ttl_idx"
            )
        ]
```

## Transactions

```python
from beanie import Document
from motor.motor_asyncio import AsyncIOMotorClientSession

async def transfer_funds(
    from_account_id: str,
    to_account_id: str,
    amount: float,
    session: AsyncIOMotorClientSession
):
    async with await session.start_transaction():
        from_account = await Account.get(from_account_id, session=session)
        to_account = await Account.get(to_account_id, session=session)

        if from_account.balance < amount:
            raise ValueError("Insufficient funds")

        await from_account.set(
            {Account.balance: from_account.balance - amount},
            session=session
        )
        await to_account.set(
            {Account.balance: to_account.balance + amount},
            session=session
        )
```

## Service Layer Pattern

```python
from typing import List, Optional
from beanie import PydanticObjectId

class UserService:
    async def get_by_id(self, user_id: str) -> Optional[User]:
        return await User.get(PydanticObjectId(user_id))

    async def get_by_email(self, email: str) -> Optional[User]:
        return await User.find_one(User.email == email)

    async def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        is_active: Optional[bool] = None
    ) -> List[User]:
        query = User.find_all()
        if is_active is not None:
            query = User.find(User.is_active == is_active)
        return await query.skip(skip).limit(limit).to_list()

    async def create(self, data: UserCreate) -> User:
        user = User(**data.model_dump())
        await user.insert()
        return user

    async def update(self, user_id: str, data: UserUpdate) -> Optional[User]:
        user = await self.get_by_id(user_id)
        if not user:
            return None
        update_data = data.model_dump(exclude_unset=True)
        update_data["updated_at"] = datetime.utcnow()
        await user.set(update_data)
        return user
```

## Additional Resources

### Reference Files

For detailed patterns and migration guides:
- **`references/migrations.md`** - Database migration strategies
- **`references/performance.md`** - Query optimization tips
- **`references/relationships.md`** - Link and BackLink patterns

### Example Files

Working examples in `examples/`:
- **`examples/document_models.py`** - Complete document definitions
- **`examples/aggregations.py`** - Aggregation pipeline examples
- **`examples/service.py`** - Service layer implementation
