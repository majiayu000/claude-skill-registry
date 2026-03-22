---
name: django-orm-mastery
description: >
  Master Django ORM patterns: QuerySets, select_related, prefetch_related, F/Q objects,
  annotations, aggregations, and raw SQL safety. Use when the user writes Django database
  queries, asks about ORM optimization, encounters N+1 queries, or works with complex
  filtering and aggregation. Trigger when you see inefficient Django queries.
---

# Django ORM Mastery

Write efficient, expressive Django ORM queries. The ORM is lazy by default -- QuerySets
are not evaluated until iterated. Understanding this is key to avoiding N+1 queries
and building performant applications.

## When to Use
- User writes Django model queries
- User encounters slow queries or N+1 problems
- User needs complex filtering, aggregation, or annotation
- User asks about select_related vs prefetch_related
- User needs database-level operations without pulling data into Python

## Core Patterns

### QuerySet Basics and Chaining

QuerySets are lazy -- they build SQL without executing until evaluated. Chain freely.

```python
# Lazy -- no SQL executed yet
qs = (
    Article.objects
    .filter(status="published")
    .exclude(category__name="draft")
    .order_by("-published_at")
)

# SQL executes when you iterate, slice, call list(), len(), bool(), etc.
articles = list(qs[:10])

# Efficient existence check -- use .exists() not len() or bool()
if Article.objects.filter(slug=slug).exists():
    raise ValidationError("Slug already taken")

# Efficient count -- use .count() not len(qs)
total = Article.objects.filter(status="published").count()

# Get or 404
from django.shortcuts import get_object_or_404
article = get_object_or_404(Article, slug=slug, status="published")
```

### select_related (ForeignKey / OneToOne)

Performs a SQL JOIN. Use for ForeignKey and OneToOneField relationships. Fetches
related objects in a single query.

```python
# WITHOUT select_related -- N+1 problem
articles = Article.objects.all()
for article in articles:
    print(article.author.name)  # Each access hits the database

# WITH select_related -- single JOIN query
articles = Article.objects.select_related("author", "category").all()
for article in articles:
    print(article.author.name)  # No extra query -- already loaded

# Chain through relationships
comments = (
    Comment.objects
    .select_related("article__author", "article__category")
    .filter(is_approved=True)
)
```

### prefetch_related (ManyToMany / Reverse FK)

Performs a separate query and joins in Python. Use for ManyToManyField and reverse
ForeignKey relationships.

```python
from django.db.models import Prefetch

# Basic prefetch -- separate query for tags
articles = Article.objects.prefetch_related("tags").all()

# Custom Prefetch with filtering
articles = Article.objects.prefetch_related(
    Prefetch(
        "comments",
        queryset=Comment.objects.filter(is_approved=True).select_related("author"),
        to_attr="approved_comments",  # Access as article.approved_comments
    )
)

for article in articles:
    for comment in article.approved_comments:  # No extra queries
        print(f"{comment.author.name}: {comment.text}")
```

### F Objects (Database-Level Operations)

Use F() to reference field values in queries without pulling data into Python.

```python
from django.db.models import F

# Increment without race condition
Article.objects.filter(id=article_id).update(view_count=F("view_count") + 1)

# Compare fields
products = Product.objects.filter(stock__lt=F("reorder_level"))

# Arithmetic between fields
orders = Order.objects.annotate(
    profit=F("revenue") - F("cost")
).filter(profit__gt=0)

# Reference related fields
articles = Article.objects.filter(
    comments_count__gt=F("category__avg_comments") * 2
)
```

### Q Objects (Complex Lookups)

Use Q() for OR conditions, negation, and complex boolean logic.

```python
from django.db.models import Q

# OR condition
results = Article.objects.filter(
    Q(status="published") | Q(author=current_user)
)

# AND with OR
results = Article.objects.filter(
    Q(status="published") & (Q(category="tech") | Q(category="science"))
)

# Negation
results = Article.objects.filter(~Q(status="archived"))

# Dynamic query building
filters = Q()
if search_term:
    filters &= Q(title__icontains=search_term) | Q(body__icontains=search_term)
if category:
    filters &= Q(category__slug=category)
if date_from:
    filters &= Q(published_at__gte=date_from)

articles = Article.objects.filter(filters)
```

### Annotations and Aggregations

Push computation to the database instead of doing it in Python.

```python
from django.db.models import Count, Avg, Sum, Max, Min, Value, CharField
from django.db.models.functions import Coalesce, Upper, TruncMonth

# Aggregate -- returns a dict
stats = Order.objects.aggregate(
    total_revenue=Sum("amount"),
    avg_order=Avg("amount"),
    order_count=Count("id"),
    max_order=Max("amount"),
)

# Annotate -- adds computed fields to each object in QuerySet
authors = (
    User.objects
    .annotate(
        article_count=Count("articles"),
        avg_rating=Avg("articles__rating"),
        total_views=Sum("articles__view_count"),
    )
    .filter(article_count__gt=5)
    .order_by("-total_views")
)

# Conditional aggregation
from django.db.models import Case, When, IntegerField

articles = Article.objects.annotate(
    engagement_score=Case(
        When(view_count__gt=1000, then=Value(3)),
        When(view_count__gt=100, then=Value(2)),
        default=Value(1),
        output_field=IntegerField(),
    )
)

# Group by month
monthly_revenue = (
    Order.objects
    .annotate(month=TruncMonth("created_at"))
    .values("month")
    .annotate(
        revenue=Sum("amount"),
        count=Count("id"),
    )
    .order_by("month")
)
```

### Raw SQL (When ORM Is Not Enough)

Use parameterized queries to prevent SQL injection. Never interpolate user input.

```python
# Safe raw query with parameters
users = User.objects.raw(
    "SELECT * FROM auth_user WHERE email LIKE %s AND is_active = %s",
    [f"%@{domain}", True],
)

# Raw SQL for complex queries that don't map to a model
from django.db import connection

def get_revenue_report(year: int) -> list[dict]:
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT category, SUM(amount) as total, COUNT(*) as count
            FROM orders_order
            WHERE EXTRACT(YEAR FROM created_at) = %s
            GROUP BY category
            ORDER BY total DESC
            """,
            [year],
        )
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
```

## Anti-Patterns

- **N+1 queries**: Accessing related objects in a loop without `select_related` or
  `prefetch_related`. Use `django-debug-toolbar` to spot these.
- **Python-level filtering**: Using `[a for a in articles if a.status == "published"]`
  instead of `.filter(status="published")`. Let the database do the filtering.
- **Counting with `len(qs)`**: Use `.count()` which executes `SELECT COUNT(*)` instead
  of fetching all rows.
- **String interpolation in raw SQL**: `f"WHERE id = {user_id}"` is a SQL injection
  vulnerability. Always use parameterized queries with `%s` placeholders.
- **Calling `.all()` before `.filter()`**: `.filter()` already returns a new QuerySet.
  `Article.objects.filter(...)` is cleaner than `Article.objects.all().filter(...)`.

## Quick Reference

| Operation | Method |
|---|---|
| FK/OneToOne join | `.select_related("field")` |
| M2M/Reverse FK | `.prefetch_related("field")` |
| OR conditions | `Q(a=1) \| Q(b=2)` |
| Database-level field ref | `F("field_name")` |
| Aggregate (single result) | `.aggregate(total=Sum("field"))` |
| Annotate (per-row) | `.annotate(count=Count("rel"))` |
| Conditional | `Case(When(cond, then=val))` |
| Existence check | `.exists()` |
| Efficient count | `.count()` |
| Bulk create | `.bulk_create([obj1, obj2])` |
| Bulk update | `.bulk_update(objs, ["field"])` |
