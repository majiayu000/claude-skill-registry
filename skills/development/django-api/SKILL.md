---
name: django-api
description: Django API development for 2025. Covers Django Ninja (modern, async-first, type-safe) and Django REST Framework (mature, ecosystem-rich). Use when building REST APIs, choosing between frameworks, implementing authentication, permissions, filtering, pagination, or async endpoints.
---

# Django API Development (2025)

## Framework Choice

| Factor | Django Ninja | Django REST Framework |
|--------|--------------|----------------------|
| **Best for** | New projects, performance-critical, type-safety | Complex apps, mature ecosystem needs |
| **Validation** | Pydantic (type hints) | Serializers |
| **Async** | Native, first-class | Via `adrf` package |
| **Docs** | Auto-generated OpenAPI | Via drf-spectacular |
| **Learning curve** | Lower (FastAPI-like) | Steeper but well-documented |
| **Ecosystem** | Growing | Extensive third-party packages |

**Recommendation:** Start with Django Ninja for new projects. Use DRF when you need its ecosystem (complex permissions, nested routers, etc).

---

## Django Ninja (Recommended for 2025)

### Setup

```bash
pip install django-ninja
```

```python
# config/urls.py
from ninja import NinjaAPI

api = NinjaAPI(
    title="My API",
    version="1.0.0",
    docs_url="/docs",  # Swagger UI at /api/docs
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
]
```

### Schemas (Pydantic)

```python
# apps/blog/api/schemas.py
from ninja import Schema, ModelSchema
from datetime import datetime
from apps.blog.models import Article


class ArticleIn(Schema):
    title: str
    body: str
    tag_ids: list[int] = []


class ArticleOut(ModelSchema):
    author_name: str

    class Meta:
        model = Article
        fields = ["id", "title", "slug", "status", "created_at"]

    @staticmethod
    def resolve_author_name(obj: Article) -> str:
        return obj.author.username


class ArticleDetailOut(ArticleOut):
    body: str
    tags: list[str]

    @staticmethod
    def resolve_tags(obj: Article) -> list[str]:
        return [t.name for t in obj.tags.all()]
```

**Key patterns:**
- Use `Schema` for input, `ModelSchema` for output
- Type hints drive validation and docs
- Use `resolve_*` for computed fields

### Endpoints

```python
# apps/blog/api/views.py
from ninja import Router
from django.shortcuts import get_object_or_404
from apps.blog.models import Article
from .schemas import ArticleIn, ArticleOut, ArticleDetailOut

router = Router(tags=["articles"])


@router.get("/", response=list[ArticleOut])
def list_articles(request, status: str | None = None):
    qs = Article.objects.select_related("author")
    if status:
        qs = qs.filter(status=status)
    return qs


@router.get("/{slug}", response=ArticleDetailOut)
def get_article(request, slug: str):
    return get_object_or_404(
        Article.objects.select_related("author").prefetch_related("tags"),
        slug=slug,
    )


@router.post("/", response=ArticleOut)
def create_article(request, payload: ArticleIn):
    article = Article.objects.create(
        author=request.user,
        title=payload.title,
        body=payload.body,
    )
    if payload.tag_ids:
        article.tags.set(payload.tag_ids)
    return article
```

### Async Endpoints

```python
# apps/blog/api/views.py
from ninja import Router
from asgiref.sync import sync_to_async

router = Router()


@router.get("/articles/", response=list[ArticleOut])
async def list_articles(request):
    # Wrap ORM calls with sync_to_async
    qs = await sync_to_async(list)(
        Article.objects.select_related("author")[:20]
    )
    return qs


@router.get("/external-data/")
async def fetch_external(request):
    import httpx
    async with httpx.AsyncClient() as client:
        resp = await client.get("https://api.example.com/data")
    return resp.json()
```

**When to use async:**
- External API calls (httpx, aiohttp)
- Multiple concurrent I/O operations
- Real-time / high-concurrency endpoints

**Note:** Django ORM is not fully async — wrap with `sync_to_async`.

### Authentication

```python
# apps/core/api/auth.py
from ninja.security import HttpBearer, APIKeyHeader
from django.contrib.auth.models import User


class AuthBearer(HttpBearer):
    def authenticate(self, request, token: str) -> User | None:
        # Validate JWT or token
        try:
            return User.objects.get(auth_token=token)
        except User.DoesNotExist:
            return None


class ApiKey(APIKeyHeader):
    param_name = "X-API-Key"

    def authenticate(self, request, key: str) -> User | None:
        try:
            return User.objects.get(api_key=key)
        except User.DoesNotExist:
            return None


# Usage
@router.get("/protected/", auth=AuthBearer())
def protected_endpoint(request):
    return {"user": request.auth.username}
```

### Wiring Routers

```python
# config/urls.py
from ninja import NinjaAPI
from apps.blog.api.views import router as blog_router
from apps.users.api.views import router as users_router

api = NinjaAPI()
api.add_router("/articles", blog_router)
api.add_router("/users", users_router)

urlpatterns = [
    path("api/v1/", api.urls),
]
```

---

## Django REST Framework

Use when you need the mature ecosystem or complex features.

### Setup

```python
# config/settings/base.py
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}
```

### Serializers

```python
# apps/blog/api/serializers.py
from rest_framework import serializers
from apps.blog.models import Article


class ArticleListSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        model = Article
        fields = ["id", "title", "slug", "author", "status", "created_at"]


class ArticleDetailSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True, write_only=True, source="tags"
    )

    class Meta:
        model = Article
        fields = ["id", "title", "slug", "body", "author", "tags", "tag_ids", "created_at"]
        read_only_fields = ["slug", "created_at"]
```

### ViewSets

```python
# apps/blog/api/views.py
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.select_related("author").prefetch_related("tags")
    lookup_field = "slug"

    def get_serializer_class(self):
        if self.action == "list":
            return ArticleListSerializer
        return ArticleDetailSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=["post"])
    def publish(self, request, slug=None):
        article = self.get_object()
        article.status = "published"
        article.save(update_fields=["status"])
        return Response({"status": "published"})
```

### Async DRF (via adrf)

```bash
pip install adrf
```

```python
from adrf.viewsets import ViewSet
from rest_framework.response import Response


class AsyncArticleViewSet(ViewSet):
    async def list(self, request):
        articles = await sync_to_async(list)(Article.objects.all()[:20])
        serializer = ArticleListSerializer(articles, many=True)
        return Response(serializer.data)
```

---

## Common Patterns (Both Frameworks)

### Filtering

```python
# Django Ninja
@router.get("/", response=list[ArticleOut])
def list_articles(
    request,
    status: str | None = None,
    author: str | None = None,
    created_after: date | None = None,
):
    qs = Article.objects.all()
    if status:
        qs = qs.filter(status=status)
    if author:
        qs = qs.filter(author__username=author)
    if created_after:
        qs = qs.filter(created_at__date__gte=created_after)
    return qs
```

```python
# DRF with django-filter
class ArticleFilter(django_filters.FilterSet):
    created_after = django_filters.DateFilter(field_name="created_at", lookup_expr="gte")

    class Meta:
        model = Article
        fields = ["status", "author__username"]
```

### Pagination

```python
# Django Ninja
from ninja.pagination import paginate, PageNumberPagination

@router.get("/", response=list[ArticleOut])
@paginate(PageNumberPagination, page_size=20)
def list_articles(request):
    return Article.objects.all()
```

### Error Handling

```python
# Django Ninja
from ninja.errors import HttpError

@router.get("/{id}")
def get_article(request, id: int):
    try:
        return Article.objects.get(id=id)
    except Article.DoesNotExist:
        raise HttpError(404, "Article not found")
```

---

## Testing

```python
# Django Ninja
from ninja.testing import TestClient
from config.urls import api

client = TestClient(api)


def test_list_articles():
    response = client.get("/articles/")
    assert response.status_code == 200


def test_create_article(authenticated_client):
    response = authenticated_client.post(
        "/articles/",
        json={"title": "Test", "body": "Content"},
    )
    assert response.status_code == 200
```

---

## Running with ASGI

For async support, use an ASGI server:

```bash
# Development
uvicorn config.asgi:application --reload

# Production
gunicorn config.asgi:application -k uvicorn.workers.UvicornWorker -w 4
```

---

## Common Pitfalls

1. **Mixing sync/async incorrectly**: Use `sync_to_async` for ORM in async views. Don't call sync code directly.

2. **N+1 queries**: Always `select_related`/`prefetch_related` — both frameworks need this.

3. **Blocking in async views**: Use `httpx` (async) not `requests` (sync) for external calls.

4. **Over-engineering auth**: Start simple. Django Ninja's built-in `HttpBearer` or DRF's `IsAuthenticated` cover most cases.

5. **No OpenAPI docs**: Django Ninja auto-generates. For DRF, always add drf-spectacular.