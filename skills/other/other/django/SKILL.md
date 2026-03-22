---
name: django
description: |
  Django 5+ framework guardrails, patterns, and best practices for AI-assisted development.
  Use when working with Django projects, or when the user mentions Django.
  Provides ORM patterns, views, templates, DRF, admin, and security guidelines.
license: MIT
metadata:
  author: samuel
  version: "1.0"
  category: framework
  language: python
  extensions: ".py"
---

# Django Framework Guide

> Applies to: Django 5+, Django REST Framework, Django Channels
> Language: Python 3.10+

## Core Principles

1. **Batteries Included**: Leverage Django's built-in features before adding third-party packages
2. **DRY**: Don't Repeat Yourself -- use abstract models, mixins, and shared utilities
3. **Fat Models, Thin Views**: Keep business logic in models and services, not views
4. **Explicit Over Implicit**: Use clear URL patterns, explicit imports, named relationships
5. **Security by Default**: CSRF, XSS protection, SQL injection prevention are built in

## When to Use Django

**Good fit:**
- Full-stack web applications with templates
- Admin interface needed out of the box
- Content management systems
- Session-based authentication
- ORM with built-in migrations

**Consider alternatives:**
- Pure APIs with async-first needs (FastAPI)
- Minimal framework overhead (Flask)
- Real-time heavy workloads without Channels

## Project Structure

```
myproject/
├── manage.py
├── pyproject.toml
├── requirements/
│   ├── base.txt
│   ├── dev.txt
│   └── prod.txt
├── config/                    # Project configuration
│   ├── __init__.py
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── dev.py
│   │   └── prod.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── apps/                      # Django applications
│   ├── users/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── forms.py
│   │   ├── serializers.py     # If using DRF
│   │   ├── services.py        # Business logic
│   │   └── tests/
│   │       ├── __init__.py
│   │       ├── test_models.py
│   │       ├── test_views.py
│   │       └── test_services.py
│   └── core/                  # Shared utilities
│       ├── __init__.py
│       ├── models.py          # Abstract base models
│       └── mixins.py
├── templates/
│   ├── base.html
│   └── components/
├── static/
│   ├── css/
│   └── js/
└── tests/
    └── conftest.py
```

- Split settings into `base.py`, `dev.py`, `prod.py`
- Group apps under `apps/` directory
- Keep `core/` app for shared abstract models and utilities
- Place business logic in `services.py`, not in views
- Co-locate tests inside each app under `tests/` directory

## Guardrails

### Settings

- Never hardcode `SECRET_KEY` -- use `python-decouple` or environment variables
- Split settings: `base.py` (shared), `dev.py` (debug), `prod.py` (secure)
- Always define `AUTH_USER_MODEL` before first migration
- Set `DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"`
- Use `ALLOWED_HOSTS` in production (never `["*"]`)

### Models

- Always define `__str__` on every model
- Always set `class Meta` with `db_table`, `ordering`, and `indexes`
- Use abstract base models for shared fields (`TimeStampedModel`, `UUIDModel`)
- Use `TextChoices`/`IntegerChoices` for status fields (not raw strings)
- Add `related_name` to all ForeignKey and OneToOneField relationships
- Use `on_delete` explicitly: `CASCADE`, `PROTECT`, `SET_NULL`, `SET_DEFAULT`
- Add database indexes for frequently queried fields
- Use `validators` at model level for domain constraints

### Abstract Base Models

```python
# apps/core/models.py
from django.db import models
import uuid


class TimeStampedModel(models.Model):
    """Abstract base with created/updated timestamps."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDModel(models.Model):
    """Abstract base with UUID primary key."""
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )

    class Meta:
        abstract = True
```

### Custom User Model

- Always create a custom user model before the first migration
- Extend `AbstractUser` (not `AbstractBaseUser` unless you need full control)
- Set `AUTH_USER_MODEL = "users.User"` in settings

```python
# apps/users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from apps.core.models import TimeStampedModel, UUIDModel


class User(AbstractUser, UUIDModel, TimeStampedModel):
    email = models.EmailField(unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        db_table = "users"
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["email"])]

    def __str__(self) -> str:
        return self.email
```

## Views and URLs

### Class-Based Views (CBVs)

- Use `ListView`, `DetailView`, `CreateView`, `UpdateView` for CRUD
- Use `LoginRequiredMixin` for authenticated views
- Override `get_queryset()` to add filtering and `select_related`/`prefetch_related`
- Override `form_valid()` to inject the current user

```python
from django.views.generic import ListView
from django.db.models import Q
from .models import Product


class ProductListView(ListView):
    model = Product
    template_name = "products/list.html"
    context_object_name = "products"
    paginate_by = 20

    def get_queryset(self):
        qs = Product.objects.filter(
            status=Product.Status.PUBLISHED
        )
        search = self.request.GET.get("q")
        if search:
            qs = qs.filter(
                Q(name__icontains=search)
                | Q(description__icontains=search)
            )
        return qs.select_related("category")
```

### URL Configuration

```python
# config/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("apps.api.urls")),
    path("", include("apps.products.urls")),
]
```

- Use `include()` for app-level URL namespaces
- Use `app_name` in each app's `urls.py` for reverse resolution
- Serve media files in DEBUG mode only

## ORM Essentials

### Query Optimization

- Always use `select_related()` for ForeignKey/OneToOne (SQL JOIN)
- Always use `prefetch_related()` for ManyToMany/reverse FK (separate query)
- Use `only()` or `defer()` to limit fields when not all columns needed
- Never call `Model.objects.all()` without pagination or limits
- Use `F()` expressions for database-level operations
- Use `Q()` objects for complex lookups

### Avoiding N+1 Queries

```python
# BAD: N+1 queries
for product in Product.objects.all():
    print(product.category.name)  # Extra query per product

# GOOD: Single JOIN query
for product in Product.objects.select_related("category"):
    print(product.category.name)  # No extra queries
```

### Transactions

- Use `@transaction.atomic` for multi-step writes
- Use `select_for_update()` for optimistic locking

```python
from django.db import transaction

@transaction.atomic
def transfer_stock(source_id, dest_id, qty):
    source = Product.objects.select_for_update().get(id=source_id)
    dest = Product.objects.select_for_update().get(id=dest_id)
    source.stock -= qty
    dest.stock += qty
    source.save(update_fields=["stock"])
    dest.save(update_fields=["stock"])
```

## Admin Configuration

```python
from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "price", "status"]
    list_filter = ["status", "category", "created_at"]
    search_fields = ["name", "description"]
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ["created_at", "updated_at"]
    ordering = ["-created_at"]

    fieldsets = (
        (None, {"fields": ("name", "slug", "description")}),
        ("Pricing", {"fields": ("price", "stock")}),
        ("Classification", {"fields": ("category", "status")}),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )
```

- Always register models with `@admin.register(Model)`
- Use `list_display` for useful columns, `list_filter` for filtering
- Use `prepopulated_fields` for slug generation
- Group fields with `fieldsets` for organized admin forms

## Django REST Framework (DRF)

### Settings

```python
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_PAGINATION_CLASS": (
        "rest_framework.pagination.PageNumberPagination"
    ),
    "PAGE_SIZE": 20,
    "DEFAULT_THROTTLE_RATES": {
        "anon": "100/hour",
        "user": "1000/hour",
    },
}
```

### ViewSets and Routers

- Use `ModelViewSet` for full CRUD
- Use `@action(detail=True/False)` for custom endpoints
- Override `get_serializer_class()` for different read/write serializers
- Override `get_queryset()` to add `select_related`/`prefetch_related`

```python
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related("category")
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return ProductCreateSerializer
        return ProductSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=["post"])
    def publish(self, request, pk=None):
        product = self.get_object()
        product.status = Product.Status.PUBLISHED
        product.save(update_fields=["status"])
        return Response({"status": "published"})
```

### Serializers

- Use `ModelSerializer` for standard CRUD
- Add `read_only_fields` for computed/auto fields
- Validate in `validate_<field>()` or `validate()` methods
- Use nested serializers for read, flat IDs for write

## Security Essentials

- CSRF: Enabled by default for forms; use `@csrf_exempt` sparingly
- XSS: Django templates auto-escape by default; never use `|safe` with user data
- SQL Injection: ORM uses parameterized queries; never use raw SQL with string formatting
- Clickjacking: `X-Frame-Options` middleware enabled by default
- HTTPS: Set `SECURE_SSL_REDIRECT = True` in production
- HSTS: Set `SECURE_HSTS_SECONDS` in production
- Cookies: Set `SESSION_COOKIE_SECURE = True` and `CSRF_COOKIE_SECURE = True`
- Passwords: Use `AUTH_PASSWORD_VALIDATORS` (enabled by default)
- CORS: Use `django-cors-headers` with explicit allowed origins (never `CORS_ALLOW_ALL_ORIGINS` in production)

## Testing

### Standards

- Use `pytest` with `pytest-django` (not Django's built-in test runner)
- Mark database tests with `@pytest.mark.django_db`
- Use `factory-boy` or fixtures for test data
- Use `APIClient` for DRF endpoint testing
- Coverage target: >80% for business logic
- Test file naming: `test_models.py`, `test_views.py`, `test_services.py`

### Fixtures

```python
# conftest.py
import pytest
from rest_framework.test import APIClient
from apps.users.models import User


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="testpass123",
    )


@pytest.fixture
def authenticated_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client
```

## Commands Reference

```bash
# Development
python manage.py runserver
python manage.py shell_plus          # django-extensions

# Migrations
python manage.py makemigrations
python manage.py migrate
python manage.py showmigrations

# Testing
pytest
pytest -v --cov=apps --cov-report=html
pytest apps/products/ -k "test_create"

# Database
python manage.py dbshell
python manage.py dumpdata products > fixtures/products.json
python manage.py loaddata fixtures/products.json

# Static files
python manage.py collectstatic

# Celery
celery -A config worker -l info
celery -A config beat -l info
```

## Dependencies

**Base**: `Django>=5.0`, `djangorestframework`, `django-cors-headers`, `django-filter`, `djangorestframework-simplejwt`, `python-decouple`, `psycopg2-binary`, `whitenoise`

**Dev**: `pytest`, `pytest-django`, `pytest-cov`, `factory-boy`, `django-debug-toolbar`, `django-extensions`, `black`, `ruff`, `mypy`, `django-stubs`

## Best Practices

### Do

- Use `select_related` and `prefetch_related` for every queryset
- Create indexes for frequently queried fields
- Use `@transaction.atomic` for multi-step operations
- Validate at both model level and serializer level
- Write services for business logic (not in views)
- Use signals sparingly (prefer explicit service calls)
- Cache expensive queries with Django cache framework
- Use environment variables for all configuration

### Don't

- Put business logic in views
- Use raw SQL without parameterization
- Ignore N+1 query problems
- Store sensitive data in settings files
- Use `Model.objects.all()` without limits
- Skip migrations in production
- Use `CORS_ALLOW_ALL_ORIGINS = True` in production
- Use `|safe` template filter with user-provided data

## Advanced Topics

For detailed code examples and advanced patterns, see:

- [references/patterns.md](references/patterns.md) -- DRF serializers, middleware, services, signals, Celery tasks, management commands, deployment, and testing patterns

## External References

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Two Scoops of Django](https://www.feldroy.com/books/two-scoops-of-django-3-x)
- [Django Best Practices](https://django-best-practices.readthedocs.io/)
