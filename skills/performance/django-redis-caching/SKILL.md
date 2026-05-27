---
name: django-redis-caching
description: Django Redis caching with django-cacheops. This skill should be used when implementing caching, adding cache invalidation, optimizing API performance, modifying models that affect cached data, or debugging cache-related issues in the Django backend.
---

# Django Redis Caching Skill

Implements Redis caching with django-cacheops for the DTX Django backend.

## Quick Reference

### Cacheops Configuration

All models use 1-hour cache timeout (configured in `settings.py`):
```python
CACHEOPS = {
    "app.tournament": {"ops": "all", "timeout": 60 * 60},
    "app.team": {"ops": "all", "timeout": 60 * 60},
    "app.customuser": {"ops": "all", "timeout": 60 * 60},
    "app.draft": {"ops": "all", "timeout": 60 * 60},
    "app.game": {"ops": "all", "timeout": 60 * 60},
    "app.draftround": {"ops": "all", "timeout": 60 * 60},
}
```

### View Caching Pattern

```python
from cacheops import cached_as

def list(self, request, *args, **kwargs):
    cache_key = f"model_list:{request.get_full_path()}"

    @cached_as(Model1, Model2, extra=cache_key, timeout=60 * 60)
    def get_data():
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return serializer.data

    return Response(get_data())
```

### Cache Invalidation Pattern

```python
from cacheops import invalidate_obj, invalidate_model

def save(self, *args, **kwargs):
    super().save(*args, **kwargs)
    # Invalidate specific instance
    invalidate_obj(self.related_obj)
    # Invalidate entire model cache
    invalidate_model(RelatedModel)
```

## DTX Model Cache Dependencies

When modifying data, invalidate these related caches:

| Changed Model | Also Invalidate |
|---------------|-----------------|
| DraftRound | Tournament, Draft, Team |
| Draft | Tournament |
| Team | Tournament (if tournament-scoped) |
| Game | Tournament, Team |
| CustomUser | Team (if member changes) |

## Key Principles

1. **Invalidate on Write**: Always invalidate related caches after mutations
2. **Monitor Dependencies**: Use `@cached_as(Model1, Model2, ...)` to auto-invalidate
3. **Use Specific Keys**: Include request path or pk in cache keys
4. **Keep Fresh for Detail**: Use `keep_fresh=True` for single-object retrieval

## Detailed References

- [Cacheops Patterns](references/cacheops-patterns.md) - Decorator usage, cache keys
- [Invalidation Strategies](references/invalidation-strategies.md) - When and how to invalidate
- [Model Dependencies](references/model-dependencies.md) - DTX model relationships

## Common Operations

### Disable Cache for Management Commands

```python
DISABLE_CACHE=true python manage.py <command>
```

### Manual Cache Invalidation

```python
from cacheops import invalidate_all, invalidate_model, invalidate_obj

# Nuclear option - invalidate everything
invalidate_all()

# Invalidate all instances of a model
invalidate_model(Tournament)

# Invalidate specific instance
invalidate_obj(tournament)
```

### Check if Cache is Working

```python
from django.core.cache import cache
cache.set('test_key', 'test_value', 30)
print(cache.get('test_key'))  # Should print 'test_value'
```

## Timeout Guidelines

| Data Type | Timeout | Reason |
|-----------|---------|--------|
| Static data | 60 * 60 (1h) | Rarely changes |
| Tournament state | 60 * 10 (10m) | Changes during events |
| Draft rounds | 60 * 10 (10m) | Active during drafts |
| External API (Discord) | 15s | Rate limiting, freshness |
