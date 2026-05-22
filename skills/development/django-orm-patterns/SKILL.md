---
name: django-orm-patterns
description: Use when Django ORM patterns with models, queries, and relationships. Use when building database-driven Django applications.
allowed-tools:
  - Bash
  - Read
---

# Django ORM Patterns

Master Django ORM for building efficient, scalable database-driven
applications with complex queries and relationships.

## Model Definition

Define models with proper field types, constraints, and metadata.

```python
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class User(models.Model):
    email = models.EmailField(unique=True, db_index=True)
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['created_at', 'is_active']),
        ]
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    published = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['author', 'published']),
        ]
```

## QuerySet API Basics

Use Django's QuerySet API for efficient database queries.

```python
# All records
users = User.objects.all()

# Filtering
active_users = User.objects.filter(is_active=True)
inactive_users = User.objects.exclude(is_active=True)

# Get single record (raises exception if not found or multiple found)
user = User.objects.get(email='user@example.com')

# Get or create
user, created = User.objects.get_or_create(
    email='user@example.com',
    defaults={'name': 'John Doe'}
)

# Update or create
user, created = User.objects.update_or_create(
    email='user@example.com',
    defaults={'name': 'Jane Doe', 'is_active': True}
)

# Chaining filters
posts = Post.objects.filter(published=True).filter(author__is_active=True)

# Order by
users = User.objects.order_by('-created_at', 'name')

# Limit results
recent_users = User.objects.all()[:10]

# Count
user_count = User.objects.filter(is_active=True).count()

# Exists
has_active_users = User.objects.filter(is_active=True).exists()
```

## Q Objects for Complex Queries

Build complex queries with Q objects for OR and NOT operations.

```python
from django.db.models import Q

# OR queries
users = User.objects.filter(
    Q(name__icontains='john') | Q(email__icontains='john')
)

# AND with OR
users = User.objects.filter(
    Q(is_active=True) & (Q(name__icontains='john') | Q(email__icontains='john'))
)

# NOT queries
users = User.objects.filter(~Q(is_active=True))

# Complex combinations
posts = Post.objects.filter(
    Q(published=True) &
    (Q(author__name__icontains='john') | Q(title__icontains='important')) &
    ~Q(views__lt=100)
)

# Dynamic query building
def search_users(name=None, email=None, is_active=None):
    query = Q()
    if name:
        query &= Q(name__icontains=name)
    if email:
        query &= Q(email__icontains=email)
    if is_active is not None:
        query &= Q(is_active=is_active)
    return User.objects.filter(query)
```

## F Objects for Field References

Use F objects to reference model fields in queries and updates.

```python
from django.db.models import F

# Compare fields
posts = Post.objects.filter(views__gt=F('author__posts__count'))

# Update based on current value
Post.objects.filter(published=True).update(views=F('views') + 1)

# Avoid race conditions
post = Post.objects.get(id=1)
post.views = F('views') + 1
post.save()
post.refresh_from_db()  # Get updated value

# Complex expressions
from django.db.models import ExpressionWrapper, IntegerField

Post.objects.annotate(
    adjusted_views=ExpressionWrapper(
        F('views') * 2 + 10,
        output_field=IntegerField()
    )
)
```

## Aggregation and Annotation

Perform database-level calculations and add computed fields.

```python
from django.db.models import Count, Sum, Avg, Max, Min

# Simple aggregation
from django.db.models import Avg
avg_views = Post.objects.aggregate(Avg('views'))
# Returns: {'views__avg': 42.5}

# Multiple aggregations
stats = Post.objects.aggregate(
    total_posts=Count('id'),
    avg_views=Avg('views'),
    max_views=Max('views'),
    min_views=Min('views')
)

# Annotation (adds field to each object)
users = User.objects.annotate(
    post_count=Count('posts'),
    total_views=Sum('posts__views')
)

for user in users:
    print(f"{user.name}: {user.post_count} posts, {user.total_views} views")

# Filter by annotation
popular_users = User.objects.annotate(
    post_count=Count('posts')
).filter(post_count__gt=10)

# Complex annotations
from django.db.models import Case, When, Value, CharField

User.objects.annotate(
    user_type=Case(
        When(post_count__gt=10, then=Value('prolific')),
        When(post_count__gt=5, then=Value('active')),
        default=Value('casual'),
        output_field=CharField()
    )
)
```

## Prefetch and Select Related (N+1 Prevention)

Optimize queries by reducing database hits with eager loading.

```python
# Select related (for ForeignKey and OneToOne)
posts = Post.objects.select_related('author').all()
for post in posts:
    print(post.author.name)  # No additional query

# Prefetch related (for ManyToMany and reverse ForeignKey)
from django.db.models import Prefetch

users = User.objects.prefetch_related('posts').all()
for user in users:
    for post in user.posts.all():  # No additional query
        print(post.title)

# Custom prefetch
users = User.objects.prefetch_related(
    Prefetch(
        'posts',
        queryset=Post.objects.filter(published=True).order_by('-created_at')
    )
)

# Multiple levels
posts = Post.objects.select_related(
    'author'
).prefetch_related(
    'author__posts'  # Prefetch all posts by the same author
)

# Combining both
Post.objects.select_related('author').prefetch_related('tags')
```

## Custom Managers and QuerySets

Create reusable query logic with custom managers and querysets.

```python
from django.db import models

class PublishedQuerySet(models.QuerySet):
    def published(self):
        return self.filter(published=True)

    def recent(self):
        return self.order_by('-created_at')[:10]

    def by_author(self, author):
        return self.filter(author=author)

class PublishedManager(models.Manager):
    def get_queryset(self):
        return PublishedQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()

    def recent(self):
        return self.get_queryset().recent()

class Post(models.Model):
    # fields...
    objects = models.Manager()  # Default manager
    published_posts = PublishedManager()  # Custom manager

    class Meta:
        base_manager_name = 'objects'

# Usage
Post.published_posts.published().recent()
Post.published_posts.published().by_author(user)

# Chaining custom methods
class UserQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)

    def with_posts(self):
        return self.annotate(post_count=Count('posts')).filter(post_count__gt=0)

User.objects.active().with_posts()
```

## Transactions and Atomic Blocks

Ensure data consistency with database transactions.

```python
from django.db import transaction

# Atomic decorator
@transaction.atomic
def create_user_with_post(email, name, post_title):
    user = User.objects.create(email=email, name=name)
    Post.objects.create(title=post_title, author=user)
    return user

# Context manager
def update_user_posts(user_id):
    try:
        with transaction.atomic():
            user = User.objects.select_for_update().get(id=user_id)
            user.posts.update(published=True)
            user.is_active = True
            user.save()
    except Exception as e:
        # Transaction is rolled back
        raise

# Savepoints
from django.db import transaction

with transaction.atomic():
    user = User.objects.create(email='user@example.com')

    sid = transaction.savepoint()
    try:
        Post.objects.create(title='Test', author=user)
    except:
        transaction.savepoint_rollback(sid)
    else:
        transaction.savepoint_commit(sid)

# Select for update (locking)
with transaction.atomic():
    user = User.objects.select_for_update().get(id=1)
    user.is_active = False
    user.save()
```

## Advanced Select and Prefetch Patterns

Master complex query optimization with advanced eager loading techniques.

```python
from django.db.models import Prefetch, Count, Q

# Basic select_related (ForeignKey, OneToOne)
posts = Post.objects.select_related('author', 'category')

# Multi-level select_related
comments = Comment.objects.select_related('post__author__profile')

# Prefetch with custom queryset
users = User.objects.prefetch_related(
    Prefetch(
        'posts',
        queryset=Post.objects.filter(published=True).select_related('category'),
        to_attr='published_posts'
    )
)

# Multiple prefetch with different filters
authors = User.objects.prefetch_related(
    Prefetch(
        'posts',
        queryset=Post.objects.filter(published=True),
        to_attr='published_posts'
    ),
    Prefetch(
        'posts',
        queryset=Post.objects.filter(published=False),
        to_attr='draft_posts'
    )
)

# Nested prefetch
posts = Post.objects.prefetch_related(
    Prefetch(
        'comments',
        queryset=Comment.objects.select_related('author').prefetch_related(
            Prefetch(
                'replies',
                queryset=Comment.objects.select_related('author')
            )
        )
    )
)

# Prefetch with annotations
users = User.objects.prefetch_related(
    Prefetch(
        'posts',
        queryset=Post.objects.annotate(
            comment_count=Count('comments')
        ).filter(comment_count__gt=0)
    )
)
```

## Database Functions and Expressions

Leverage database functions for complex operations.

```python
from django.db.models import F, Value, CharField, Case, When, Q
from django.db.models.functions import Concat, Lower, Upper, Length, Substr, Coalesce

# String operations
users = User.objects.annotate(
    full_name=Concat('first_name', Value(' '), 'last_name')
)

users = User.objects.annotate(
    email_lower=Lower('email'),
    name_upper=Upper('name')
)

# String functions
posts = Post.objects.annotate(
    title_length=Length('title')
).filter(title_length__gt=50)

# Substring
posts = Post.objects.annotate(
    title_preview=Substr('title', 1, 50)
)

# Coalesce (return first non-null value)
posts = Post.objects.annotate(
    display_name=Coalesce('custom_title', 'title', Value('Untitled'))
)

# Date functions
from django.db.models.functions import TruncDate, TruncMonth, ExtractYear, Now

posts = Post.objects.annotate(
    created_date=TruncDate('created_at'),
    created_month=TruncMonth('created_at'),
    created_year=ExtractYear('created_at')
)

# Date arithmetic
from datetime import timedelta
from django.utils import timezone

recent_posts = Post.objects.filter(
    created_at__gte=timezone.now() - timedelta(days=7)
)

# Mathematical functions
from django.db.models.functions import Abs, Ceil, Floor, Round

products = Product.objects.annotate(
    price_rounded=Round('price'),
    discount_abs=Abs('discount')
)

# Conditional expressions
User.objects.annotate(
    user_type=Case(
        When(posts__count__gt=100, then=Value('power_user')),
        When(posts__count__gt=10, then=Value('active')),
        When(posts__count__gt=0, then=Value('casual')),
        default=Value('lurker'),
        output_field=CharField()
    )
)

# Complex conditional updates
Post.objects.update(
    status=Case(
        When(Q(published=True) & Q(views__gt=1000), then=Value('viral')),
        When(Q(published=True) & Q(views__gt=100), then=Value('popular')),
        When(published=True, then=Value('published')),
        default=Value('draft'),
        output_field=CharField()
    )
)
```

## Advanced Aggregation Patterns

Perform complex database-level calculations.

```python
from django.db.models import (
    Count, Sum, Avg, Max, Min, StdDev, Variance,
    Q, F, Value, CharField, When, Case
)
from django.db.models.functions import Coalesce

# Multiple aggregations with filters
stats = Post.objects.aggregate(
    total_posts=Count('id'),
    published_posts=Count('id', filter=Q(published=True)),
    draft_posts=Count('id', filter=Q(published=False)),
    avg_views=Avg('views'),
    max_views=Max('views'),
    total_views=Sum('views'),
    std_dev_views=StdDev('views')
)

# Conditional aggregation
User.objects.aggregate(
    active_users=Count('id', filter=Q(is_active=True)),
    inactive_users=Count('id', filter=Q(is_active=False)),
    avg_posts_active=Avg('posts__count', filter=Q(is_active=True))
)

# Annotation with conditional aggregation
users = User.objects.annotate(
    published_post_count=Count('posts', filter=Q(posts__published=True)),
    draft_post_count=Count('posts', filter=Q(posts__published=False)),
    total_views=Sum('posts__views'),
    avg_post_views=Avg('posts__views')
).filter(published_post_count__gt=0)

# Group by with annotation
from django.db.models.functions import TruncDate

daily_stats = Post.objects.annotate(
    date=TruncDate('created_at')
).values('date').annotate(
    post_count=Count('id'),
    total_views=Sum('views'),
    avg_views=Avg('views')
).order_by('-date')

# Subquery aggregation
from django.db.models import OuterRef, Subquery

# Get latest comment for each post
latest_comment = Comment.objects.filter(
    post=OuterRef('pk')
).order_by('-created_at')

posts = Post.objects.annotate(
    latest_comment_date=Subquery(latest_comment.values('created_at')[:1]),
    latest_comment_author=Subquery(latest_comment.values('author__name')[:1])
)

# Complex nested aggregation
User.objects.annotate(
    total_post_views=Sum('posts__views'),
    total_comment_count=Count('posts__comments'),
    avg_comments_per_post=Case(
        When(posts__count=0, then=Value(0)),
        default=Count('posts__comments') / Count('posts', distinct=True)
    )
)
```

## Database Indexes and Optimization

Optimize query performance with proper indexing.

```python
class Post(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            # Single field
            models.Index(fields=['created_at']),

            # Composite index
            models.Index(fields=['author', 'published']),

            # Descending index
            models.Index(fields=['-created_at']),

            # Named index
            models.Index(fields=['title'], name='post_title_idx'),

            # Partial index (PostgreSQL)
            models.Index(
                fields=['author'],
                name='published_posts_idx',
                condition=models.Q(published=True)
            ),

            # Expression index (PostgreSQL)
            models.Index(
                Lower('title'),
                name='post_title_lower_idx'
            ),

            # Multi-column with includes (PostgreSQL)
            models.Index(
                fields=['author'],
                name='author_includes_idx',
                include=['title', 'created_at']
            ),
        ]

        # Unique together
        unique_together = [['author', 'title']]

        # Constraints (Django 2.2+)
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'slug'],
                name='unique_author_slug'
            ),
            models.CheckConstraint(
                check=Q(views__gte=0),
                name='views_non_negative'
            ),
        ]

# Query optimization techniques
# Only load needed fields
posts = Post.objects.only('id', 'title', 'author_id')

# Defer heavy fields
posts = Post.objects.defer('content', 'metadata')

# Values and values_list for dictionaries/tuples
post_data = Post.objects.values('id', 'title', 'author__name')
post_ids = Post.objects.values_list('id', flat=True)

# Combine optimizations
posts = Post.objects.select_related('author').only(
    'title', 'author__name'
).filter(
    published=True
)

# Use iterator() for large querysets
for post in Post.objects.iterator(chunk_size=1000):
    process_post(post)

# Use explain() to analyze queries
print(Post.objects.filter(published=True).explain(analyze=True))
```

## Model Inheritance Patterns

Implement proper model inheritance strategies.

```python
from django.db import models

# Abstract base classes (no database table)
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Post(TimeStampedModel):
    title = models.CharField(max_length=200)
    content = models.TextField()
    # Inherits created_at and updated_at

# Multi-table inheritance (separate tables, joins required)
class BaseContent(models.Model):
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

class Article(BaseContent):
    # Has implicit OneToOne to BaseContent
    body = models.TextField()
    published = models.BooleanField(default=False)

class Video(BaseContent):
    duration = models.IntegerField()
    video_url = models.URLField()

# Proxy models (same table, different behavior)
class PublishedPostManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(published=True)

class Post(models.Model):
    title = models.CharField(max_length=200)
    published = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

class PublishedPost(Post):
    objects = PublishedPostManager()

    class Meta:
        proxy = True
        ordering = ['-created_at']

    def publish(self):
        self.published = True
        self.save()

# When to use each:
# - Abstract: Share fields/methods, no polymorphic queries
# - Multi-table: Need polymorphic queries, different fields
# - Proxy: Same fields, different managers/methods
```

## Advanced QuerySet Methods

Master advanced QuerySet operations.

```python
# Bulk operations for performance
posts = [
    Post(title=f'Post {i}', author=user)
    for i in range(1000)
]
Post.objects.bulk_create(posts, batch_size=100)

# Bulk update (Django 2.2+)
posts = Post.objects.filter(author=user)
for post in posts:
    post.views += 1
Post.objects.bulk_update(posts, ['views'], batch_size=100)

# Bulk create with returning IDs (PostgreSQL)
posts = Post.objects.bulk_create(posts, batch_size=100, ignore_conflicts=True)

# Update with F expressions (atomic, no race conditions)
Post.objects.filter(id=1).update(views=F('views') + 1)

# Get or create with complex lookups
user, created = User.objects.get_or_create(
    email='user@example.com',
    defaults={
        'name': 'John Doe',
        'is_active': True
    }
)

# Update or create
post, created = Post.objects.update_or_create(
    author=user,
    slug='my-post',
    defaults={
        'title': 'My Post',
        'content': 'Updated content'
    }
)

# In bulk (Django 4.1+)
Post.objects.bulk_create(
    posts,
    update_conflicts=True,
    update_fields=['title', 'content'],
    unique_fields=['author', 'slug']
)

# Union, intersection, difference
published = Post.objects.filter(published=True)
featured = Post.objects.filter(featured=True)

all_posts = published.union(featured)  # Posts that are published OR featured
both = published.intersection(featured)  # Posts that are both
only_published = published.difference(featured)  # Published but not featured

# Distinct
authors = Post.objects.values('author').distinct()

# With PostgreSQL distinct on
posts = Post.objects.order_by('author', '-created_at').distinct('author')

# Reverse queryset
recent_first = Post.objects.order_by('-created_at')
oldest_first = recent_first.reverse()

# None queryset
empty = Post.objects.none()  # Returns empty queryset
```

## Raw SQL When Needed

Use raw SQL for complex queries that ORM cannot handle efficiently.

```python
# Raw queries
users = User.objects.raw('SELECT * FROM app_user WHERE is_active = %s', [True])
for user in users:
    print(user.name)

# Execute custom SQL
from django.db import connection

def get_user_stats():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT u.id, u.name, COUNT(p.id) as post_count
            FROM app_user u
            LEFT JOIN app_post p ON p.author_id = u.id
            GROUP BY u.id, u.name
            HAVING COUNT(p.id) > 5
        """)
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

# Combining ORM with raw SQL
User.objects.raw("""
    SELECT * FROM app_user
    WHERE id IN (
        SELECT DISTINCT author_id FROM app_post WHERE published = TRUE
    )
""")
```

## Migrations Best Practices

Manage database schema changes safely and efficiently.

```python
# Create migration
# python manage.py makemigrations

# Custom migration
from django.db import migrations

def forwards_func(apps, schema_editor):
    User = apps.get_model('app', 'User')
    for user in User.objects.all():
        user.is_active = True
        user.save()

def reverse_func(apps, schema_editor):
    pass

class Migration(migrations.Migration):
    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]

# Add field with default
class Migration(migrations.Migration):
    operations = [
        migrations.AddField(
            model_name='user',
            name='status',
            field=models.CharField(max_length=20, default='active'),
        ),
    ]

# Rename field
operations = [
    migrations.RenameField(
        model_name='user',
        old_name='name',
        new_name='full_name',
    ),
]

# Add index
operations = [
    migrations.AddIndex(
        model_name='post',
        index=models.Index(fields=['author', 'created_at']),
    ),
]
```

## When to Use This Skill

Use django-orm-patterns when building modern, production-ready
applications that require
advanced patterns, best practices, and optimal performance.

## Signal Patterns and Best Practices

Use Django signals carefully for decoupled event handling.

```python
from django.db.models.signals import post_save, pre_save, post_delete, m2m_changed
from django.dispatch import receiver
from django.db import transaction

# Basic signal receiver
@receiver(post_save, sender=Post)
def post_created_handler(sender, instance, created, **kwargs):
    if created:
        # Send notification
        notify_followers(instance.author, instance)

# Pre-save validation
@receiver(pre_save, sender=User)
def normalize_email(sender, instance, **kwargs):
    if instance.email:
        instance.email = instance.email.lower()

# Conditional signal execution
@receiver(post_save, sender=Post)
def update_stats(sender, instance, created, update_fields, **kwargs):
    # Skip if only certain fields updated
    if update_fields and 'views' in update_fields:
        return

    # Update statistics
    instance.author.update_post_count()

# M2M changed signal
@receiver(m2m_changed, sender=Post.tags.through)
def tags_changed(sender, instance, action, **kwargs):
    if action == 'post_add':
        # Tags were added
        pass
    elif action == 'post_remove':
        # Tags were removed
        pass

# Avoid signals in transactions
@receiver(post_save, sender=Order)
def send_confirmation_email(sender, instance, created, **kwargs):
    if created:
        # Wait for transaction to commit
        transaction.on_commit(lambda: send_email(instance))

# Disconnect signals when needed
from django.test import TestCase

class PostTestCase(TestCase):
    def setUp(self):
        # Disconnect signal for testing
        post_save.disconnect(post_created_handler, sender=Post)

    def tearDown(self):
        # Reconnect signal
        post_save.connect(post_created_handler, sender=Post)
```

## Custom Field Types

Create reusable custom field types for complex data.

```python
from django.db import models
import json

# JSON field (before Django 3.1)
class JSONField(models.TextField):
    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return json.loads(value)

    def to_python(self, value):
        if isinstance(value, dict):
            return value
        if value is None:
            return value
        return json.loads(value)

    def get_prep_value(self, value):
        return json.dumps(value)

# Encrypted field
from cryptography.fernet import Fernet

class EncryptedField(models.TextField):
    def __init__(self, *args, **kwargs):
        self.cipher_suite = Fernet(settings.FIELD_ENCRYPTION_KEY)
        super().__init__(*args, **kwargs)

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return self.cipher_suite.decrypt(value.encode()).decode()

    def get_prep_value(self, value):
        if value is None:
            return value
        return self.cipher_suite.encrypt(value.encode()).decode()

# Usage
class User(models.Model):
    metadata = JSONField(default=dict)
    ssn = EncryptedField()

# Array field (PostgreSQL)
from django.contrib.postgres.fields import ArrayField

class Post(models.Model):
    tags = ArrayField(models.CharField(max_length=50), default=list)
    ratings = ArrayField(models.IntegerField(), default=list)

    class Meta:
        indexes = [
            models.Index(fields=['tags']),
        ]

# Query array fields
posts = Post.objects.filter(tags__contains=['django'])
posts = Post.objects.filter(tags__overlap=['python', 'django'])
```

## Query Debugging and Profiling

Debug and optimize database queries effectively.

```python
from django.db import connection, reset_queries
from django.test.utils import override_settings
import time

# Log all queries
@override_settings(DEBUG=True)
def analyze_queries(func):
    def wrapper(*args, **kwargs):
        reset_queries()
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()

        print(f"Function: {func.__name__}")
        print(f"Number of queries: {len(connection.queries)}")
        print(f"Time taken: {end - start:.2f}s")

        for query in connection.queries:
            print(f"SQL: {query['sql']}")
            print(f"Time: {query['time']}s\n")

        return result
    return wrapper

# Usage
@analyze_queries
def get_user_posts(user_id):
    user = User.objects.get(id=user_id)
    posts = user.posts.all()
    return list(posts)

# Django Debug Toolbar integration
# Add to INSTALLED_APPS
INSTALLED_APPS = [
    'debug_toolbar',
]

# Middleware
MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

# Explain queries
queryset = Post.objects.filter(published=True)
print(queryset.explain())  # Basic explain
print(queryset.explain(verbose=True))  # Verbose
print(queryset.explain(analyze=True))  # Actually run query

# Query count assertion in tests
from django.test import TestCase
from django.test.utils import override_settings

class PostTestCase(TestCase):
    def test_query_count(self):
        with self.assertNumQueries(3):
            # Should execute exactly 3 queries
            user = User.objects.get(id=1)
            posts = list(user.posts.all())
            comments = list(Comment.objects.filter(post__in=posts))

# Find duplicate queries
def find_duplicate_queries():
    from collections import Counter

    queries = [q['sql'] for q in connection.queries]
    duplicates = [q for q, count in Counter(queries).items() if count > 1]

    for sql in duplicates:
        print(f"Duplicate query: {sql}")
```

## Advanced Manager Patterns

Build sophisticated custom managers for complex business logic.

```python
from django.db import models
from django.db.models import Q, Count, Avg

class PostQuerySet(models.QuerySet):
    def published(self):
        return self.filter(published=True)

    def draft(self):
        return self.filter(published=False)

    def by_author(self, author):
        return self.filter(author=author)

    def popular(self, min_views=100):
        return self.filter(views__gte=min_views)

    def recent(self, days=7):
        from django.utils import timezone
        from datetime import timedelta
        cutoff = timezone.now() - timedelta(days=days)
        return self.filter(created_at__gte=cutoff)

    def with_stats(self):
        return self.annotate(
            comment_count=Count('comments'),
            avg_rating=Avg('ratings__score')
        )

    def optimized(self):
        return self.select_related('author').prefetch_related('comments')

class PostManager(models.Manager.from_queryset(PostQuerySet)):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)

    def with_deleted(self):
        return super().get_queryset()

class Post(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    published = models.BooleanField(default=False)
    views = models.IntegerField(default=0)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = PostManager()

    def soft_delete(self):
        from django.utils import timezone
        self.deleted_at = timezone.now()
        self.save()

# Usage - methods chain naturally
recent_popular = Post.objects.published().recent().popular().with_stats()
author_drafts = Post.objects.by_author(user).draft().optimized()

# Multiple manager pattern
class AllPostsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

class Post(models.Model):
    # ... fields ...
    objects = PostManager()  # Default, excludes deleted
    all_objects = AllPostsManager()  # Includes deleted
```

## Database-Specific Features

Leverage PostgreSQL-specific features when available.

```python
from django.contrib.postgres.fields import ArrayField, JSONField, HStoreField
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.contrib.postgres.aggregates import ArrayAgg, StringAgg

# Full-text search
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    search_vector = SearchVectorField(null=True)

    class Meta:
        indexes = [
            GinIndex(fields=['search_vector']),
        ]

# Update search vector
from django.contrib.postgres.search import SearchVector

Post.objects.update(
    search_vector=SearchVector('title', weight='A') + SearchVector('content', weight='B')
)

# Search
query = SearchQuery('django')
posts = Post.objects.annotate(
    rank=SearchRank('search_vector', query)
).filter(search_vector=query).order_by('-rank')

# Array aggregation
authors = User.objects.annotate(
    post_titles=ArrayAgg('posts__title', distinct=True),
    tags_list=StringAgg('posts__tags', delimiter=', ', distinct=True)
)

# JSON operations
from django.contrib.postgres.fields.jsonb import KeyTextTransform

users = User.objects.annotate(
    city=KeyTextTransform('city', 'metadata')
).filter(city='New York')

# Range fields
from django.contrib.postgres.fields import IntegerRangeField, DateRangeField

class Event(models.Model):
    name = models.CharField(max_length=200)
    date_range = DateRangeField()
    capacity = IntegerRangeField()

from django.db.models import Q
from datetime import date

# Find events happening on a specific date
events = Event.objects.filter(date_range__contains=date(2024, 1, 15))

# Find overlapping events
events = Event.objects.filter(
    date_range__overlap=(date(2024, 1, 1), date(2024, 1, 31))
)
```

## Django ORM Best Practices

1. **Use select_related and prefetch_related** - Always optimize queries to
   prevent N+1 problems
2. **Index frequently queried fields** - Add database indexes for fields used
   in filters and joins
3. **Use get_or_create carefully** - Wrap in transactions when dealing with
   race conditions
4. **Avoid queries in loops** - Batch operations and use bulk methods when
   possible
5. **Use only() and defer() wisely** - Load only necessary fields for large
   models
6. **Leverage F() expressions** - Use database-level operations to avoid race
   conditions
7. **Use transactions for data integrity** - Wrap related operations in atomic
   blocks
8. **Create custom managers** - Encapsulate common query patterns in reusable
   managers
9. **Use exists() for checks** - More efficient than count() when only
   checking existence
10. **Monitor query performance** - Use django-debug-toolbar to identify slow
    queries
11. **Implement soft deletes with managers** - Use custom managers to hide
    deleted records
12. **Use database functions** - Leverage Django's database functions for
    complex operations
13. **Batch database operations** - Use bulk_create and bulk_update for large
    datasets
14. **Use iterator() for large datasets** - Avoid loading entire querysets
    into memory
15. **Apply database constraints** - Use CheckConstraint and UniqueConstraint
    for data integrity

## Django ORM Common Pitfalls

1. **N+1 query problem** - Forgetting to use select_related or
   prefetch_related causes excessive queries
2. **Loading too much data** - Using .all() without pagination can cause
   memory issues
3. **Inefficient updates** - Using save() in loops instead of bulk_update or
   update()
4. **Missing database indexes** - Slow queries on unindexed fields in large
   tables
5. **Incorrect use of get()** - Not handling DoesNotExist or
   MultipleObjectsReturned exceptions
6. **Lazy evaluation confusion** - Querysets are lazy; understand when they
   actually execute
7. **Transaction isolation issues** - Not using select_for_update when needed
   for locking
8. **Mixing F() with save()** - Must call refresh_from_db() after saving F()
   expressions
9. **Inefficient aggregations** - Running Python calculations instead of
   database aggregations
10. **Migration conflicts** - Not coordinating migrations in team environments
11. **Signal performance issues** - Signals in tight loops can cause
    performance problems
12. **Overusing signals** - Prefer explicit calls over implicit signal-based
    logic
13. **Not using transactions with signals** - Signals fire before transaction
    commit by default
14. **Incorrect distinct() usage** - Using distinct() without understanding
    its implications
15. **Ignoring database-specific features** - Missing out on PostgreSQL
    full-text search, arrays, etc.

## Resources

- [Django ORM Documentation](https://docs.djangoproject.com/en/stable/topics/db/)
- [Django QuerySet API Reference](https://docs.djangoproject.com/en/stable/ref/models/querysets/)
- [Django Database Optimization](https://docs.djangoproject.com/en/stable/topics/db/optimization/)
- [Django Migration Guide](https://docs.djangoproject.com/en/stable/topics/migrations/)
- [Django Database Transactions](https://docs.djangoproject.com/en/stable/topics/db/transactions/)
