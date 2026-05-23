---
name: tg-caching
description: Django caching patterns for the World of Darkness application. Use when implementing view caching, queryset caching, cache invalidation, or optimizing database queries. Triggers on performance optimization, cache configuration, slow query fixes, or Redis cache usage.
---

# Caching Patterns

## Configuration

### Development (LocMemCache)
```python
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
        "OPTIONS": {"MAX_ENTRIES": 1000},
    }
}
```

### Production (Redis)
```python
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.environ.get("REDIS_URL"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"max_connections": 50},
            "COMPRESSOR": "django_redis.compressors.zlib.ZlibCompressor",
        },
    }
}
```

## Cache Timeout Constants

Use in `core/cache.py`:

```python
CACHE_TIMEOUT_SHORT = 60        # 1 minute
CACHE_TIMEOUT_MEDIUM = 300      # 5 minutes
CACHE_TIMEOUT_LONG = 900        # 15 minutes
CACHE_TIMEOUT_VERY_LONG = 3600  # 1 hour
CACHE_TIMEOUT_DAY = 86400       # 24 hours
```

## Caching Strategies

### 1. View-Level Caching

For static pages identical for all users:

```python
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

@method_decorator(cache_page(60 * 15), name='dispatch')
class MeritFlawListView(ListView):
    model = MeritFlaw
    template_name = "characters/core/meritflaw/list.html"
```

**Use for:** Reference data lists, public pages, rarely-changing content.
**Don't use for:** User-specific pages, permission-gated content.

### 2. Queryset Caching

For expensive database queries:

```python
from core.cache import cache_function, CACHE_TIMEOUT_MEDIUM

class CharacterDetailView(DetailView):
    @staticmethod
    @cache_function(timeout=CACHE_TIMEOUT_MEDIUM, key_prefix="char_scenes")
    def get_character_scenes(character_id):
        return list(
            Scene.objects.filter(characters__id=character_id)
            .select_related("chronicle", "location")
            .prefetch_related("characters")
            .order_by("-date_of_scene")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["scenes"] = self.get_character_scenes(self.object.id)
        return context
```

### 3. Manual Cache Access

```python
from django.core.cache import cache

# Set with timeout
cache.set('my_key', data, timeout=300)

# Get with default
data = cache.get('my_key', default=None)

# Delete
cache.delete('my_key')

# Get or set pattern
def get_expensive_data():
    key = 'expensive_calculation'
    result = cache.get(key)
    if result is None:
        result = perform_expensive_calculation()
        cache.set(key, result, timeout=300)
    return result
```

### 4. Template Fragment Caching

```django
{% load cache %}

{% cache 900 character_details character.id %}
    <div class="character-details">
        {{ character.name }}
        {{ character.description }}
    </div>
{% endcache %}
```

## Cache Key Generator

```python
class CacheKeyGenerator:
    PREFIX = "tg"

    @classmethod
    def make_model_key(cls, model_class, **filters):
        filter_str = ":".join(f"{k}={v}" for k, v in sorted(filters.items()))
        return f"{cls.PREFIX}:queryset:{model_class.__name__}:{filter_str}"

    @classmethod
    def make_view_key(cls, view_name, **params):
        param_str = ":".join(f"{k}={v}" for k, v in sorted(params.items()))
        return f"{cls.PREFIX}:view:{view_name}:{param_str}"
```

## Cache Invalidation

### On Model Save

```python
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

@receiver([post_save, post_delete], sender=Character)
def invalidate_character_cache(sender, instance, **kwargs):
    cache.delete(f"tg:queryset:Character:id={instance.id}")
    cache.delete(f"tg:queryset:Character:chronicle={instance.chronicle_id}")
```

### Manual Invalidation

```python
# Single key
cache.delete('specific_key')

# Pattern-based (Redis only)
from django_redis import get_redis_connection
con = get_redis_connection("default")
keys = con.keys("tg:queryset:Character:*")
if keys:
    con.delete(*keys)

# Clear all (use sparingly!)
cache.clear()
```

## Best Practices

### Do Cache
- Reference data (merits/flaws, archetypes, clans)
- Expensive aggregations
- API responses
- Static content lists

### Don't Cache
- User-specific permissions
- Frequently changing data
- Data displayed immediately after modification
- Session-dependent content

### Cache Duration Guidelines

| Content Type | Timeout | Example |
|-------------|---------|---------|
| Static reference | 15-60 min | Merit/flaw lists |
| Semi-static | 5-15 min | Character lists |
| News/updates | 1-5 min | Home page |
| Real-time | Don't cache | Chat, notifications |

### Combine with Query Optimization

```python
# GOOD: Cache an optimized query
@cache_function(timeout=300)
def get_characters():
    return Character.objects.select_related('owner').prefetch_related('merits_and_flaws')

# BAD: Caching doesn't fix N+1
@cache_function(timeout=300)
def get_characters():
    return Character.objects.all()  # N+1 on access
```

## Debugging

### Check Cache Status

```python
from django.core.cache import cache

# Test connection
cache.set('test', 'value')
assert cache.get('test') == 'value'
print("Cache working!")

# Check Redis keys (Redis only)
from django_redis import get_redis_connection
con = get_redis_connection("default")
print(f"Total keys: {len(con.keys('*'))}")
```

### Clear Cache

```bash
# Django shell
python manage.py shell
>>> from django.core.cache import cache
>>> cache.clear()

# Redis CLI
redis-cli FLUSHDB
```
