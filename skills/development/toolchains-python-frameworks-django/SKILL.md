# Django Framework Skill

---
progressive_disclosure:
  entry_point:
    summary: "Full-featured Python web framework with batteries included (ORM, admin, auth)"
    when_to_use:
      - "When building content-heavy web applications"
      - "When needing built-in admin interface"
      - "When using Django ORM and migrations"
      - "When building REST APIs with Django REST Framework"
    quick_start:
      - "pip install django"
      - "django-admin startproject myproject"
      - "python manage.py runserver"
  token_estimate:
    entry: 75-90
    full: 4500-5500
---

## Overview

Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design. Built by experienced developers, it takes care of much of the hassle of web development, enabling focus on writing applications without reinventing the wheel.

**Key Philosophy**: "Batteries included" - Django comes with extensive built-in features including ORM, authentication, admin interface, forms, and security features.

## Core Concepts

### MVT Architecture (Model-View-Template)

Django follows the MVT pattern:
- **Model**: Data layer (ORM models, database schema)
- **View**: Business logic (handles requests, returns responses)
- **Template**: Presentation layer (HTML with Django template language)

### Project vs Apps

- **Project**: The entire Django application (settings, URLs, WSGI config)
- **Apps**: Modular components (blog, auth, API) that can be reused across projects

```bash
# Create project
django-admin startproject myproject
cd myproject

# Create app
python manage.py startapp blog

# Register app in settings.py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    # ...
    'blog',
]
```

## Models and ORM

### Model Definition

```python
# models.py
from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "categories"
        ordering = ['name']

    def __str__(self):
        return self.name

class Post(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    content = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_at']
        indexes = [
            models.Index(fields=['-published_at']),
            models.Index(fields=['slug']),
        ]

    def __str__(self):
        return self.title
```

### Common Field Types

```python
# Text fields
models.CharField(max_length=200)
models.TextField()
models.SlugField()
models.EmailField()
models.URLField()

# Numeric fields
models.IntegerField()
models.DecimalField(max_digits=10, decimal_places=2)
models.FloatField()

# Date/time fields
models.DateField()
models.DateTimeField()
models.DurationField()

# Boolean
models.BooleanField(default=False)

# Relationships
models.ForeignKey(Model, on_delete=models.CASCADE)
models.ManyToManyField(Model)
models.OneToOneField(Model, on_delete=models.CASCADE)

# Files
models.FileField(upload_to='uploads/')
models.ImageField(upload_to='images/')

# JSON (PostgreSQL)
models.JSONField()
```

### Migrations

```bash
# Create migrations after model changes
python manage.py makemigrations

# View SQL that will be executed
python manage.py sqlmigrate blog 0001

# Apply migrations
python manage.py migrate

# Create empty migration for custom operations
python manage.py makemigrations --empty blog

# Reverse migration
python manage.py migrate blog 0001
```

### QuerySet API

```python
# Basic queries
Post.objects.all()
Post.objects.filter(status='published')
Post.objects.exclude(status='draft')
Post.objects.get(pk=1)  # Returns single object or raises DoesNotExist

# Chaining filters
Post.objects.filter(status='published').filter(category__name='Tech')

# Field lookups
Post.objects.filter(title__icontains='django')  # Case-insensitive contains
Post.objects.filter(published_at__year=2024)
Post.objects.filter(published_at__gte=datetime(2024, 1, 1))
Post.objects.filter(author__username__startswith='john')

# Ordering
Post.objects.order_by('-published_at')
Post.objects.order_by('category', '-created_at')

# Limiting
Post.objects.all()[:5]  # First 5
Post.objects.all()[5:10]  # Offset pagination

# Aggregation
from django.db.models import Count, Avg, Sum
Category.objects.annotate(post_count=Count('post'))
Post.objects.aggregate(avg_length=Avg('content__length'))

# Q objects for complex queries
from django.db.models import Q
Post.objects.filter(Q(status='published') | Q(author=request.user))
Post.objects.filter(Q(status='published') & ~Q(category=None))

# F expressions for field comparisons
from django.db.models import F
Post.objects.filter(updated_at__gt=F('published_at'))

# Select/Prefetch related (performance optimization)
Post.objects.select_related('author', 'category')  # SQL JOIN
Post.objects.prefetch_related('tags')  # Separate query for M2M
```

### Model Methods and Properties

```python
class Post(models.Model):
    # ... fields ...

    @property
    def is_published(self):
        return self.status == 'published' and self.published_at is not None

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('post_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        # Auto-generate slug if not provided
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "blog post"
        verbose_name_plural = "blog posts"
```

## Views

### Function-Based Views (FBV)

```python
# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm

def post_list(request):
    posts = Post.objects.filter(status='published').select_related('author', 'category')
    context = {'posts': posts}
    return render(request, 'blog/post_list.html', context)

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status='published')
    return render(request, 'blog/post_detail.html', {'post': post})

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})

def api_posts(request):
    posts = Post.objects.filter(status='published').values('title', 'slug', 'published_at')
    return JsonResponse(list(posts), safe=False)
```

### Class-Based Views (CBV)

```python
# views.py
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Post

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(status='published').select_related('author', 'category')

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_queryset(self):
        return Post.objects.filter(status='published')

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
```

## URLs and Routing

```python
# project/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),
    path('api/', include('api.urls')),
]

# blog/urls.py
from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('post/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/create/', views.PostCreateView.as_view(), name='post_create'),
    path('post/<slug:slug>/edit/', views.PostUpdateView.as_view(), name='post_update'),
    path('post/<slug:slug>/delete/', views.PostDeleteView.as_view(), name='post_delete'),

    # Function-based views
    path('api/posts/', views.api_posts, name='api_posts'),
]
```

## Templates

### Template Syntax

```django
{# blog/templates/blog/post_list.html #}
{% extends 'base.html' %}
{% load static %}

{% block title %}Blog Posts{% endblock %}

{% block content %}
<h1>Blog Posts</h1>

{% if posts %}
    {% for post in posts %}
        <article class="post">
            <h2><a href="{% url 'blog:post_detail' post.slug %}">{{ post.title }}</a></h2>
            <p class="meta">
                By {{ post.author.username }} on {{ post.published_at|date:"F d, Y" }}
                in {{ post.category.name }}
            </p>
            <p>{{ post.content|truncatewords:50 }}</p>
        </article>
    {% empty %}
        <p>No posts found.</p>
    {% endfor %}

    {# Pagination #}
    {% if is_paginated %}
        <div class="pagination">
            {% if page_obj.has_previous %}
                <a href="?page=1">First</a>
                <a href="?page={{ page_obj.previous_page_number }}">Previous</a>
            {% endif %}

            Page {{ page_obj.number }} of {{ page_obj.paginator.num_pages }}

            {% if page_obj.has_next %}
                <a href="?page={{ page_obj.next_page_number }}">Next</a>
                <a href="?page={{ page_obj.paginator.num_pages }}">Last</a>
            {% endif %}
        </div>
    {% endif %}
{% else %}
    <p>No posts available.</p>
{% endif %}
{% endblock %}
```

### Template Filters and Tags

```django
{# Common filters #}
{{ value|lower }}
{{ value|upper }}
{{ value|title }}
{{ value|truncatewords:30 }}
{{ value|date:"Y-m-d" }}
{{ value|default:"N/A" }}
{{ html_content|safe }}  {# Disable auto-escaping #}
{{ url|urlencode }}

{# Custom template tag #}
{% load custom_tags %}
{% get_recent_posts 5 as recent %}

{# Include other templates #}
{% include 'blog/partials/post_card.html' with post=post %}

{# Static files #}
<link rel="stylesheet" href="{% static 'css/style.css' %}">
<img src="{% static 'images/logo.png' %}" alt="Logo">
```

## Forms

### Form Definition

```python
# forms.py
from django import forms
from .models import Post, Category

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'slug', 'category', 'content', 'status']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10}),
            'slug': forms.TextInput(attrs={'placeholder': 'auto-generated-if-empty'}),
        }

    def clean_slug(self):
        slug = self.cleaned_data.get('slug')
        if slug and Post.objects.filter(slug=slug).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('This slug is already in use.')
        return slug

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    subject = forms.CharField(max_length=200)
    message = forms.CharField(widget=forms.Textarea)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and not email.endswith('@example.com'):
            raise forms.ValidationError('Please use your company email.')
        return email

    def send_email(self):
        # Send email logic
        pass
```

### Form Usage in Views

```python
def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.send_email()
            messages.success(request, 'Message sent successfully!')
            return redirect('contact_success')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})
```

### Form Rendering in Templates

```django
<form method="post">
    {% csrf_token %}

    {# Auto-render all fields #}
    {{ form.as_p }}

    {# Manual field rendering #}
    <div class="form-group">
        {{ form.title.label_tag }}
        {{ form.title }}
        {% if form.title.errors %}
            <div class="errors">{{ form.title.errors }}</div>
        {% endif %}
    </div>

    <button type="submit">Submit</button>
</form>
```

## Django Admin

### Basic Admin Configuration

```python
# admin.py
from django.contrib import admin
from .models import Post, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'published_at']
    list_filter = ['status', 'category', 'created_at']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_at'
    ordering = ['-published_at']

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'author', 'category')
        }),
        ('Content', {
            'fields': ('content',)
        }),
        ('Publication', {
            'fields': ('status', 'published_at')
        }),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('author', 'category')
```

### Advanced Admin Features

```python
class PostAdmin(admin.ModelAdmin):
    # Custom actions
    actions = ['make_published', 'make_draft']

    def make_published(self, request, queryset):
        updated = queryset.update(status='published')
        self.message_user(request, f'{updated} posts marked as published.')
    make_published.short_description = "Mark selected posts as published"

    # Inline editing
    class TagInline(admin.TabularInline):
        model = Post.tags.through
        extra = 1

    inlines = [TagInline]

    # Custom methods in list_display
    def author_email(self, obj):
        return obj.author.email
    author_email.short_description = 'Author Email'

    list_display = ['title', 'author', 'author_email', 'status']
```

## Authentication and Permissions

### User Authentication

```python
# views.py
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, permission_required

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def profile_view(request):
    return render(request, 'profile.html')

@permission_required('blog.add_post')
def create_post_view(request):
    # Only users with 'add_post' permission can access
    pass
```

### Custom User Model

```python
# models.py
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    website = models.URLField(blank=True)

# settings.py
AUTH_USER_MODEL = 'accounts.CustomUser'
```

### Permissions

```python
# Check permissions in views
if request.user.has_perm('blog.delete_post'):
    # User can delete posts
    pass

# Check in templates
{% if perms.blog.add_post %}
    <a href="{% url 'post_create' %}">Create Post</a>
{% endif %}

# Custom permissions
class Post(models.Model):
    class Meta:
        permissions = [
            ('can_publish', 'Can publish posts'),
        ]
```

## Django REST Framework

### Installation and Setup

```bash
pip install djangorestframework
```

```python
# settings.py
INSTALLED_APPS = [
    # ...
    'rest_framework',
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
}
```

### Serializers

```python
# serializers.py
from rest_framework import serializers
from .models import Post, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']

class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True
    )

    class Meta:
        model = Post
        fields = ['id', 'title', 'slug', 'author', 'category', 'category_id',
                  'content', 'status', 'published_at', 'created_at']
        read_only_fields = ['author', 'created_at']

    def validate_title(self, value):
        if len(value) < 5:
            raise serializers.ValidationError("Title must be at least 5 characters.")
        return value
```

### API Views

```python
# views.py
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Post
from .serializers import PostSerializer

class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = Post.objects.select_related('author', 'category')
        status = self.request.query_params.get('status')
        if status:
            queryset = queryset.filter(status=status)
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'])
    def publish(self, request, slug=None):
        post = self.get_object()
        post.status = 'published'
        post.published_at = timezone.now()
        post.save()
        return Response({'status': 'post published'})
```

### API URLs

```python
# api/urls.py
from rest_framework.routers import DefaultRouter
from blog.views import PostViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet)

urlpatterns = router.urls
```

## Testing

### Unit Tests with Django TestCase

```python
# tests.py
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Post, Category

User = get_user_model()

class PostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.category = Category.objects.create(name='Tech', slug='tech')

    def test_post_creation(self):
        post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            author=self.user,
            category=self.category,
            content='Test content'
        )
        self.assertEqual(post.title, 'Test Post')
        self.assertEqual(str(post), 'Test Post')

    def test_get_absolute_url(self):
        post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            author=self.user,
            content='Test'
        )
        self.assertEqual(post.get_absolute_url(), '/blog/post/test-post/')

class PostViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            author=self.user,
            content='Test content',
            status='published'
        )

    def test_post_list_view(self):
        response = self.client.get(reverse('blog:post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post')

    def test_post_detail_view(self):
        response = self.client.get(reverse('blog:post_detail', kwargs={'slug': 'test-post'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Post')

    def test_post_create_requires_login(self):
        response = self.client.get(reverse('blog:post_create'))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_post_create_authenticated(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('blog:post_create'), {
            'title': 'New Post',
            'slug': 'new-post',
            'content': 'New content',
            'status': 'draft'
        })
        self.assertEqual(Post.objects.count(), 2)
```

### Testing with pytest-django

```bash
pip install pytest-django pytest-cov
```

```python
# pytest.ini
[pytest]
DJANGO_SETTINGS_MODULE = myproject.settings
python_files = tests.py test_*.py *_tests.py

# conftest.py
import pytest
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.fixture
def user(db):
    return User.objects.create_user(username='testuser', password='12345')

@pytest.fixture
def category(db):
    from blog.models import Category
    return Category.objects.create(name='Tech', slug='tech')

@pytest.fixture
def post(db, user, category):
    from blog.models import Post
    return Post.objects.create(
        title='Test Post',
        slug='test-post',
        author=user,
        category=category,
        content='Test content',
        status='published'
    )

# test_models.py
import pytest
from blog.models import Post

@pytest.mark.django_db
def test_post_creation(user, category):
    post = Post.objects.create(
        title='Test Post',
        slug='test-post',
        author=user,
        category=category,
        content='Test content'
    )
    assert post.title == 'Test Post'
    assert str(post) == 'Test Post'

@pytest.mark.django_db
def test_post_queryset(post):
    posts = Post.objects.filter(status='published')
    assert posts.count() == 1
    assert posts.first() == post

# test_views.py
import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_post_list_view(client, post):
    response = client.get(reverse('blog:post_list'))
    assert response.status_code == 200
    assert 'Test Post' in str(response.content)

@pytest.mark.django_db
def test_post_create_requires_login(client):
    response = client.get(reverse('blog:post_create'))
    assert response.status_code == 302

@pytest.mark.django_db
def test_post_create_authenticated(client, user):
    client.force_login(user)
    response = client.post(reverse('blog:post_create'), {
        'title': 'New Post',
        'slug': 'new-post',
        'content': 'New content',
        'status': 'draft'
    })
    assert Post.objects.count() == 1

# Run tests with coverage
# pytest --cov=blog --cov-report=html
```

## Database Optimization

### Select Related and Prefetch Related

```python
# N+1 query problem (BAD)
posts = Post.objects.all()
for post in posts:
    print(post.author.username)  # Hits database for each post

# Solution with select_related (for ForeignKey/OneToOne)
posts = Post.objects.select_related('author', 'category')
for post in posts:
    print(post.author.username)  # No additional queries

# Solution with prefetch_related (for ManyToMany/Reverse ForeignKey)
posts = Post.objects.prefetch_related('tags')
for post in posts:
    for tag in post.tags.all():  # No additional queries
        print(tag.name)

# Advanced prefetch with filtering
from django.db.models import Prefetch
posts = Post.objects.prefetch_related(
    Prefetch('comments', queryset=Comment.objects.filter(approved=True))
)
```

### Database Indexing

```python
class Post(models.Model):
    title = models.CharField(max_length=200, db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=['status', '-published_at']),
            models.Index(fields=['author', 'status']),
        ]
```

### Bulk Operations

```python
# Bulk create (single query)
posts = [
    Post(title=f'Post {i}', content=f'Content {i}', author=user)
    for i in range(100)
]
Post.objects.bulk_create(posts)

# Bulk update (single query)
Post.objects.filter(status='draft').update(status='published')

# Bulk delete
Post.objects.filter(created_at__lt=old_date).delete()
```

## Middleware and Signals

### Custom Middleware

```python
# middleware.py
class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code before view
        print(f"Request: {request.method} {request.path}")

        response = self.get_response(request)

        # Code after view
        print(f"Response: {response.status_code}")
        return response

# settings.py
MIDDLEWARE = [
    # ...
    'myapp.middleware.RequestLoggingMiddleware',
]
```

### Signals

```python
# signals.py
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Post

User = get_user_model()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=Post)
def notify_post_published(sender, instance, **kwargs):
    if instance.status == 'published' and instance.published_at:
        # Send notification
        pass

@receiver(pre_delete, sender=Post)
def cleanup_post_files(sender, instance, **kwargs):
    # Delete associated files
    if instance.image:
        instance.image.delete(save=False)

# apps.py
class BlogConfig(AppConfig):
    name = 'blog'

    def ready(self):
        import blog.signals
```

## Settings and Configuration

### Settings Best Practices

```python
# settings/base.py
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = False

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third-party
    'rest_framework',
    # Local
    'blog',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

# settings/development.py
from .base import *

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# settings/production.py
from .base import *

DEBUG = False
ALLOWED_HOSTS = [os.environ.get('ALLOWED_HOST')]
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

## Deployment

### Production Checklist

```bash
# Check deployment readiness
python manage.py check --deploy
```

### Docker Deployment

```dockerfile
# Dockerfile
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "myproject.wsgi:application", "--bind", "0.0.0.0:8000"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: mydb
      POSTGRES_USER: myuser
      POSTGRES_PASSWORD: mypassword
    volumes:
      - postgres_data:/var/lib/postgresql/data

  web:
    build: .
    command: gunicorn myproject.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - .:/app
      - static_volume:/app/staticfiles
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - db

  nginx:
    image: nginx:alpine
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - static_volume:/app/staticfiles
    ports:
      - "80:80"
    depends_on:
      - web

volumes:
  postgres_data:
  static_volume:
```

### Gunicorn Configuration

```python
# gunicorn.conf.py
bind = "0.0.0.0:8000"
workers = 4
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2
accesslog = "-"
errorlog = "-"
loglevel = "info"
```

## Security Best Practices

```python
# settings.py (production)
SECRET_KEY = os.environ.get('SECRET_KEY')  # Never hardcode
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com']

# HTTPS/SSL
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Security headers
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# CSRF protection (automatically enabled)
# Always use {% csrf_token %} in forms
```

## Common Patterns and Best Practices

### Environment Variables

```python
# Use python-decouple or django-environ
from decouple import config

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
DATABASE_URL = config('DATABASE_URL')
```

### Custom Management Commands

```python
# blog/management/commands/cleanup_posts.py
from django.core.management.base import BaseCommand
from blog.models import Post
from datetime import timedelta
from django.utils import timezone

class Command(BaseCommand):
    help = 'Delete old draft posts'

    def add_arguments(self, parser):
        parser.add_argument('--days', type=int, default=30)

    def handle(self, *args, **options):
        days = options['days']
        cutoff_date = timezone.now() - timedelta(days=days)
        deleted = Post.objects.filter(
            status='draft',
            created_at__lt=cutoff_date
        ).delete()
        self.stdout.write(self.style.SUCCESS(f'Deleted {deleted[0]} posts'))

# Run: python manage.py cleanup_posts --days=60
```

### Caching

```python
# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}

# views.py
from django.views.decorators.cache import cache_page
from django.core.cache import cache

@cache_page(60 * 15)  # Cache for 15 minutes
def post_list(request):
    posts = Post.objects.filter(status='published')
    return render(request, 'blog/post_list.html', {'posts': posts})

# Low-level cache API
def get_post_count():
    count = cache.get('post_count')
    if count is None:
        count = Post.objects.filter(status='published').count()
        cache.set('post_count', count, 60 * 60)  # Cache for 1 hour
    return count
```

## Quick Reference

### Common Commands

```bash
# Project management
django-admin startproject myproject
python manage.py startapp myapp
python manage.py runserver
python manage.py runserver 0.0.0.0:8000

# Database
python manage.py makemigrations
python manage.py migrate
python manage.py showmigrations
python manage.py sqlmigrate app_name 0001
python manage.py dbshell

# Users
python manage.py createsuperuser
python manage.py changepassword username

# Static files
python manage.py collectstatic

# Testing
python manage.py test
pytest
pytest --cov=app --cov-report=html

# Shell
python manage.py shell
python manage.py shell_plus  # django-extensions

# Production
python manage.py check --deploy
gunicorn myproject.wsgi:application
```

### Useful Packages

```bash
# Development
pip install django-debug-toolbar
pip install django-extensions

# REST API
pip install djangorestframework
pip install djangorestframework-simplejwt

# Testing
pip install pytest-django
pip install factory-boy

# Deployment
pip install gunicorn
pip install whitenoise  # Static file serving

# Utilities
pip install python-decouple
pip install django-environ
pip install celery  # Task queue
```

---

**Next Steps**: Explore Django documentation at https://docs.djangoproject.com/ and Django REST Framework at https://www.django-rest-framework.org/

## Related Skills

When using Django, these skills enhance your workflow:
- **sqlalchemy**: Alternative ORM for SQLAlchemy-first projects with advanced query capabilities
- **test-driven-development**: Complete TDD workflow for Django apps (models, views, forms)
- **fastapi-local-dev**: FastAPI development patterns for building Django + FastAPI hybrid systems
- **celery**: Asynchronous task processing for Django background jobs and scheduled tasks

[Full documentation available in these skills if deployed in your bundle]