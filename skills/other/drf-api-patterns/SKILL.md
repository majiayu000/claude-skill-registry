---
name: drf-api-patterns
description: >
  Build REST APIs with Django REST Framework: serializers, ViewSets, permissions,
  pagination, filtering with django-filter, throttling, and versioning. Use when the
  user builds Django APIs, asks about DRF patterns, implements CRUD endpoints, or
  needs API authentication and permissions. Trigger when you see Django views returning
  JSON manually instead of using DRF.
---

# DRF API Patterns

Build production-grade REST APIs with Django REST Framework. DRF provides serialization,
authentication, permissions, pagination, and more out of the box, so you write less
boilerplate and get consistent API behavior.

## When to Use
- User builds REST API endpoints in Django
- User needs serialization, validation, or pagination
- User implements authentication and permissions
- User asks about ViewSets, routers, or DRF best practices
- User needs filtering, search, or ordering on list endpoints

## Core Patterns

### Serializers

Serializers handle validation and conversion between Python objects and JSON.

```python
from rest_framework import serializers

class ArticleSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.get_full_name", read_only=True)
    comment_count = serializers.IntegerField(read_only=True)
    tags = serializers.SlugRelatedField(
        many=True, slug_field="name", queryset=Tag.objects.all()
    )

    class Meta:
        model = Article
        fields = [
            "id", "title", "slug", "body", "status",
            "author", "author_name", "tags", "comment_count",
            "created_at", "updated_at",
        ]
        read_only_fields = ["id", "slug", "created_at", "updated_at"]

    def validate_title(self, value: str) -> str:
        if len(value) < 5:
            raise serializers.ValidationError("Title must be at least 5 characters")
        return value

    def validate(self, attrs: dict) -> dict:
        """Cross-field validation."""
        if attrs.get("status") == "published" and not attrs.get("body"):
            raise serializers.ValidationError(
                {"body": "Published articles must have a body"}
            )
        return attrs

# Separate serializers for create vs read
class ArticleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ["title", "body", "tags", "status"]

    def create(self, validated_data):
        tags = validated_data.pop("tags", [])
        article = Article.objects.create(
            author=self.context["request"].user,
            **validated_data,
        )
        article.tags.set(tags)
        return article
```

### ViewSets and Routers

ViewSets combine list, create, retrieve, update, and destroy into one class.

```python
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count

class ArticleViewSet(viewsets.ModelViewSet):
    serializer_class = ArticleSerializer
    lookup_field = "slug"

    def get_queryset(self):
        return (
            Article.objects
            .select_related("author")
            .prefetch_related("tags")
            .annotate(comment_count=Count("comments"))
            .order_by("-created_at")
        )

    def get_serializer_class(self):
        if self.action == "create":
            return ArticleCreateSerializer
        return ArticleSerializer

    @action(detail=True, methods=["post"])
    def publish(self, request, slug=None):
        article = self.get_object()
        article.status = "published"
        article.save(update_fields=["status"])
        return Response({"status": "published"})

    @action(detail=False, methods=["get"])
    def trending(self, request):
        qs = self.get_queryset().filter(
            status="published"
        ).order_by("-view_count")[:10]
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

# urls.py
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("articles", ArticleViewSet, basename="article")

urlpatterns = [
    path("api/v1/", include(router.urls)),
]
```

### Permissions

```python
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS

class IsAuthorOrReadOnly(BasePermission):
    """Allow authors to edit, everyone else can only read."""

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_staff

class ArticleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def get_permissions(self):
        if self.action == "list":
            return []  # Public access for listing
        if self.action == "publish":
            return [IsAuthenticated(), IsAdminOrReadOnly()]
        return super().get_permissions()
```

### Pagination

```python
from rest_framework.pagination import CursorPagination, PageNumberPagination

class StandardPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = "page_size"
    max_page_size = 100

# Cursor pagination -- efficient for large datasets, no count query
class TimelinePagination(CursorPagination):
    page_size = 50
    ordering = "-created_at"
    cursor_query_param = "cursor"

class ArticleViewSet(viewsets.ModelViewSet):
    pagination_class = StandardPagination

# Global default in settings.py
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "myapp.pagination.StandardPagination",
    "PAGE_SIZE": 25,
}
```

### Filtering with django-filter

```python
import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

class ArticleFilter(django_filters.FilterSet):
    created_after = django_filters.DateFilter(
        field_name="created_at", lookup_expr="gte"
    )
    created_before = django_filters.DateFilter(
        field_name="created_at", lookup_expr="lte"
    )
    min_views = django_filters.NumberFilter(
        field_name="view_count", lookup_expr="gte"
    )
    tags = django_filters.CharFilter(method="filter_by_tags")

    class Meta:
        model = Article
        fields = ["status", "category", "author"]

    def filter_by_tags(self, queryset, name, value):
        tag_names = value.split(",")
        return queryset.filter(tags__name__in=tag_names).distinct()

class ArticleViewSet(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ArticleFilter
    search_fields = ["title", "body", "author__username"]
    ordering_fields = ["created_at", "view_count", "title"]
    ordering = ["-created_at"]
```

### Throttling

```python
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

class BurstRateThrottle(UserRateThrottle):
    scope = "burst"

class SustainedRateThrottle(UserRateThrottle):
    scope = "sustained"

# settings.py
REST_FRAMEWORK = {
    "DEFAULT_THROTTLE_CLASSES": [
        "myapp.throttles.BurstRateThrottle",
        "myapp.throttles.SustainedRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "burst": "60/min",
        "sustained": "1000/day",
        "anon": "20/min",
    },
}
```

### API Versioning

```python
# settings.py
REST_FRAMEWORK = {
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.URLPathVersioning",
    "ALLOWED_VERSIONS": ["v1", "v2"],
    "DEFAULT_VERSION": "v1",
}

# urls.py
urlpatterns = [
    path("api/<version>/", include(router.urls)),
]

# Conditional logic in views
class ArticleViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        if self.request.version == "v2":
            return ArticleV2Serializer
        return ArticleSerializer
```

## Anti-Patterns

- **Fat serializers with business logic**: Serializers should validate and transform.
  Keep business logic in services or model methods.
- **Using `ModelViewSet` for non-CRUD endpoints**: If you only need list and retrieve,
  use `mixins.ListModelMixin` and `mixins.RetrieveModelMixin` with `GenericViewSet`.
- **No pagination on list endpoints**: Unbounded QuerySets will crash on large tables.
  Always set a pagination class.
- **Skipping select_related in get_queryset**: DRF serializers accessing related fields
  trigger N+1 queries. Always optimize the QuerySet.
- **Testing with the Django test client instead of DRF's**: Use `APIClient` and
  `APIRequestFactory` for proper content negotiation and authentication.

## Quick Reference

| Feature | Configuration |
|---|---|
| Serializer | `ModelSerializer` with `Meta.fields` |
| ViewSet | `ModelViewSet` + Router |
| Custom action | `@action(detail=True/False)` |
| Permission | `BasePermission.has_object_permission` |
| Pagination | `PageNumberPagination` / `CursorPagination` |
| Filtering | `DjangoFilterBackend` + `FilterSet` |
| Search | `SearchFilter` + `search_fields` |
| Ordering | `OrderingFilter` + `ordering_fields` |
| Throttling | `UserRateThrottle` + `DEFAULT_THROTTLE_RATES` |
| Versioning | `URLPathVersioning` + `ALLOWED_VERSIONS` |
