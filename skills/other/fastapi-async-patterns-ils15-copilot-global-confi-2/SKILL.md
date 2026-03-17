---
name: fastapi-async-patterns
description: Create async FastAPI endpoints with proper error handling, dependency injection, service/repository patterns, and type safety. Includes async database queries, pagination, filtering, and Gemini integration.
---

# FastAPI Async Patterns Skill

## When to Use

Use this skill when:
- Creating new FastAPI endpoints with async support
- Building service layers with dependency injection
- Implementing repository patterns for data access
- Adding pagination, filtering, or search
- Integrating with async databases (SQLAlchemy async)
- Handling Gemini AI integration with fallbacks
- Creating proper error handling and validation

## Key Patterns

### 1. Service Layer Architecture

```python
# services/product_service.py
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Product
from app.repositories import ProductRepository
from app.schemas import ProductCreate, ProductResponse

class ProductService:
    def __init__(self, db: AsyncSession):
        self.repository = ProductRepository(db)
    
    async def create_product(self, product_data: ProductCreate) -> ProductResponse:
        """Create product with validation and error handling"""
        existing = await self.repository.get_by_slug(product_data.slug)
        if existing:
            raise ValueError(f"Product slug '{product_data.slug}' already exists")
        
        product = await self.repository.create(product_data.dict())
        return ProductResponse.from_orm(product)
    
    async def list_products(
        self,
        skip: int = 0,
        limit: int = 10,
        category: Optional[str] = None
    ) -> List[ProductResponse]:
        """List products with pagination and filtering"""
        filters = {}
        if category:
            filters['category'] = category
        
        products = await self.repository.list(skip=skip, limit=limit, filters=filters)
        return [ProductResponse.from_orm(p) for p in products]
    
    async def search_products(self, query: str) -> List[ProductResponse]:
        """Full-text search with Gemini enrichment"""
        products = await self.repository.search(query)
        # Optional: Enhance with Gemini insights
        return [ProductResponse.from_orm(p) for p in products]
```

### 2. Repository Pattern (Data Access)

```python
# repositories/product_repository.py
from typing import Optional, List, Dict, Any
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Product

class ProductRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create(self, data: Dict[str, Any]) -> Product:
        """Create new product"""
        product = Product(**data)
        self.db.add(product)
        await self.db.commit()
        await self.db.refresh(product)
        return product
    
    async def get_by_id(self, product_id: int) -> Optional[Product]:
        """Get product by ID"""
        result = await self.db.execute(
            select(Product).where(Product.id == product_id)
        )
        return result.scalar_one_or_none()
    
    async def get_by_slug(self, slug: str) -> Optional[Product]:
        """Get product by slug"""
        result = await self.db.execute(
            select(Product).where(Product.slug == slug)
        )
        return result.scalar_one_or_none()
    
    async def list(
        self,
        skip: int = 0,
        limit: int = 10,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Product]:
        """List products with filtering and pagination"""
        query = select(Product)
        
        if filters:
            for key, value in filters.items():
                if hasattr(Product, key):
                    query = query.where(getattr(Product, key) == value)
        
        query = query.offset(skip).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def search(self, query: str) -> List[Product]:
        """Full-text search"""
        result = await self.db.execute(
            select(Product).where(
                Product.title.ilike(f"%{query}%") |
                Product.description.ilike(f"%{query}%")
            )
        )
        return result.scalars().all()
    
    async def update(self, product_id: int, data: Dict[str, Any]) -> Optional[Product]:
        """Update product"""
        product = await self.get_by_id(product_id)
        if not product:
            return None
        
        for key, value in data.items():
            if hasattr(product, key):
                setattr(product, key, value)
        
        await self.db.commit()
        await self.db.refresh(product)
        return product
    
    async def delete(self, product_id: int) -> bool:
        """Delete product"""
        product = await self.get_by_id(product_id)
        if not product:
            return False
        
        await self.db.delete(product)
        await self.db.commit()
        return True
```

### 3. Router with Dependency Injection

```python
# routers/products.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.services.product_service import ProductService
from app.schemas import ProductCreate, ProductResponse

router = APIRouter(prefix="/api/products", tags=["products"])

async def get_product_service(db: AsyncSession = Depends(get_db)) -> ProductService:
    return ProductService(db)

@router.get("", response_model=list[ProductResponse])
async def list_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    category: str = Query(None),
    service: ProductService = Depends(get_product_service)
):
    """List all products with pagination"""
    return await service.list_products(skip=skip, limit=limit, category=category)

@router.get("/search", response_model=list[ProductResponse])
async def search_products(
    q: str = Query(..., min_length=1),
    service: ProductService = Depends(get_product_service)
):
    """Search products by query"""
    try:
        return await service.search_products(q)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: int,
    service: ProductService = Depends(get_product_service)
):
    """Get product by ID"""
    product = await service.repository.get_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return ProductResponse.from_orm(product)

@router.post("", response_model=ProductResponse, status_code=201)
async def create_product(
    product: ProductCreate,
    service: ProductService = Depends(get_product_service)
):
    """Create new product"""
    try:
        return await service.create_product(product)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    product: ProductCreate,
    service: ProductService = Depends(get_product_service)
):
    """Update product"""
    updated = await service.repository.update(product_id, product.dict(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="Product not found")
    return ProductResponse.from_orm(updated)

@router.delete("/{product_id}", status_code=204)
async def delete_product(
    product_id: int,
    service: ProductService = Depends(get_product_service)
):
    """Delete product"""
    success = await service.repository.delete(product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
```

### 4. Error Handling with Custom Exceptions

```python
# exceptions.py
from fastapi import HTTPException, status

class ProductNotFoundError(HTTPException):
    def __init__(self, product_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found"
        )

class DuplicateSlugError(HTTPException):
    def __init__(self, slug: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Product with slug '{slug}' already exists"
        )

class ValidationError(HTTPException):
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=message
        )
```

### 5. Gemini Integration with Fallback

```python
# services/gemini_service.py
import os
from typing import Optional
import google.generativeai as genai

class GeminiService:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel("gemini-pro") if self.api_key else None
    
    async def generate_product_description(
        self,
        title: str,
        category: str,
        max_length: int = 500
    ) -> Optional[str]:
        """Generate product description using Gemini with fallback"""
        if not self.model:
            return None  # Fallback to default description
        
        try:
            prompt = f"""
            Create a compelling product description for an e-commerce site.
            Title: {title}
            Category: {category}
            Max length: {max_length} characters
            
            Return only the description, no additional text.
            """
            
            response = await self.model.generate_content_async(prompt)
            return response.text[:max_length]
        except Exception as e:
            print(f"Gemini error: {e}")
            return None  # Fallback gracefully
    
    async def generate_seo_keywords(
        self,
        title: str,
        description: str
    ) -> Optional[list[str]]:
        """Generate SEO keywords"""
        if not self.model:
            return None
        
        try:
            prompt = f"""
            Generate 5-10 SEO keywords for this product:
            Title: {title}
            Description: {description}
            
            Return only keywords separated by commas, no additional text.
            """
            
            response = await self.model.generate_content_async(prompt)
            return [kw.strip() for kw in response.text.split(",")]
        except Exception:
            return None
```

## Best Practices

✅ **Always use async/await** for database and external API calls  
✅ **Dependency Injection** - Use FastAPI `Depends()` for services  
✅ **Type hints** - Use Pydantic schemas for request/response  
✅ **Error handling** - Use HTTPException with proper status codes  
✅ **Pagination** - Implement skip/limit for large datasets  
✅ **Filtering** - Build dynamic filters for list endpoints  
✅ **Repository pattern** - Keep data access logic separate  
✅ **Service layer** - Business logic goes in services, not routers  

## Related Files in Skill

- [service-template.py](./service-template.py) - Service class template
- [repository-template.py](./repository-template.py) - Repository class template
- [router-template.py](./router-template.py) - Router with dependency injection

## References

- FastAPI Async: https://fastapi.tiangolo.com/async-sql-databases/
- SQLAlchemy 2.0 Async: https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html
- Dependency Injection: https://fastapi.tiangolo.com/tutorial/dependencies/
