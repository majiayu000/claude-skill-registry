---
name: faion-dev-django
user-invocable: false
description: Universal Django coding guidelines and architecture patterns. Use when writing Django code, creating models, services, API endpoints, tests, or reviewing code quality. Supports Django 4.0+ and 5.x with Python 3.9+.
---

# Django Coding Standards

**Universal guidelines for Django 4.0+ and 5.x with Python 3.9+**

---

## Quick Reference

**Supported versions:**
- Python: 3.9+ (prefer 3.11+)
- Django: 4.2 LTS or 5.2 LTS for new projects
- PostgreSQL: 12+ (14+ for Django 5.0+)

---

## Core Principles

### 1. Import Style

```python
# Cross-app imports - ALWAYS with alias
from apps.orders import models as order_models
from apps.users import services as user_services
from apps.catalog import constants as catalog_constants

# Own modules (relative)
from .models import User
from . import constants
```

### 2. Services = Functions

```python
# services/activation.py
def activate_user_item(
    user: User,
    item_code: str,
    *,
    activated_by: Admin,
) -> Item:
    """Activate item for user."""
    item = Item.objects.get(code=item_code)
    item.user = user
    item.is_active = True
    item.save(update_fields=['user', 'is_active', 'updated_at'])
    return item
```

### 3. Multi-line Parameters

```python
def create_order(
    user: User,
    amount: Decimal,
    order_type: str,
    *,  # Keyword-only after
    item: Item | None = None,
    notify: bool = True,
) -> Order:
    ...
```

### 4. Thin Views

```python
class ItemActivationView(APIView):
    def post(self, request):
        serializer = ItemActivationRequest(data=request.data)
        serializer.is_valid(raise_exception=True)

        item = services.activate_user_item(
            user=request.user,
            item_code=serializer.validated_data['item_code'],
        )

        return Response(ItemResponse(item).data)
```

### 5. Testing with pytest

```python
@pytest.mark.django_db
def test_activate_item_success(user, item):
    result = services.activate_user_item(
        user=user,
        item_code=item.code,
    )
    assert result.is_active is True
    assert result.user == user
```

---

## Decision Tree: Where to Put Code

```
What does the function do?
│
├─► Changes DB (CREATE/UPDATE/DELETE)?
│   └─► services/
├─► Makes external API calls?
│   └─► services/ or integrations/
├─► Pure function (validation, calculation)?
│   └─► utils/
└─► Data transformation?
    └─► utils/
```

---

## Key Patterns

**Base model:**
```python
class BaseModel(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
```

**Constants with TextChoices:**
```python
class UserType(models.TextChoices):
    REGULAR = 'regular', 'Regular'
    PREMIUM = 'premium', 'Premium'
```

**Specific exception handling:**
```python
try:
    obj = MyModel.objects.get(pk=pk)
except MyModel.DoesNotExist:
    raise NotFoundError(f"Object {pk} not found")
```

---

## References

For detailed information, read the reference files:

- [references/imports.md](references/imports.md) - Import style and organization
- [references/services.md](references/services.md) - Services architecture
- [references/models.md](references/models.md) - Model patterns and ForeignKey
- [references/testing.md](references/testing.md) - pytest, fixtures, parametrize
- [references/api.md](references/api.md) - DRF views and serializers
- [references/celery.md](references/celery.md) - Celery tasks
- [references/quality.md](references/quality.md) - Code quality tools

---

## Sources

- [Django Docs](https://docs.djangoproject.com/)
- [DRF Docs](https://www.django-rest-framework.org/)
- [pytest-django](https://pytest-django.readthedocs.io/)
