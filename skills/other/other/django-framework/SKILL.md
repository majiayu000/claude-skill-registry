---
name: django-framework
description: "Master Django framework for building robust Python web applications with ORM, authentication, and REST APIs. Use for: developing full-stack web applications, creating REST APIs with Django REST Framework, implementing authentication and authorization, database modeling with Django ORM, building admin interfaces, handling forms and validation, deploying Django applications, and integrating third-party packages."
---

# Django Framework

Build robust, scalable web applications and REST APIs with Django's batteries-included Python framework.

## Overview

Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design. It follows the "batteries-included" philosophy, providing built-in features for authentication, ORM, admin interface, forms, and more. Django REST Framework (DRF) extends Django to build powerful Web APIs with minimal code.

## When to Use Django

| Scenario | Reason | Key Feature |
|----------|--------|-------------|
| Full-stack web applications | Complete framework with everything built-in | MTV architecture, ORM, admin |
| REST API development | Powerful API toolkit | Django REST Framework |
| Database-driven applications | Robust ORM with migrations | Models, QuerySets |
| Rapid prototyping | Quick development with conventions | Admin interface, scaffolding |
| Enterprise applications | Security, scalability, maintainability | Built-in security features |
| Content management systems | Admin interface and permissions | Django Admin |
| Authentication-heavy apps | Comprehensive auth system | User model, permissions |

## Core Architecture

### MTV Pattern (Model-Template-View)

**Model**: Data layer (database schema)
**Template**: Presentation layer (HTML)
**View**: Business logic layer (request handling)

**URL Configuration**: Maps URLs to views

```python
# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
]
```

## Django ORM

### Models

```python
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Posts'
    
    def __str__(self):
        return self.title
```

### QuerySets

```python
# Retrieve all posts
Post.objects.all()

# Filter
Post.objects.filter(published=True)

# Get single object
Post.objects.get(pk=1)

# Chaining
Post.objects.filter(published=True).order_by('-created_at')[:10]

# Complex queries
from django.db.models import Q
Post.objects.filter(Q(title__icontains='django') | Q(content__icontains='django'))

# Aggregation
from django.db.models import Count, Avg
Post.objects.aggregate(total=Count('id'), avg_length=Avg('content__length'))
```

### Relationships

```python
class Author(models.Model):
    name = models.CharField(max_length=100)

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    
class Tag(models.Model):
    name = models.CharField(max_length=50)
    
class Article(models.Model):
    title = models.CharField(max_length=200)
    tags = models.ManyToManyField(Tag, related_name='articles')
```

## Views

### Function-Based Views

```python
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

def post_list(request):
    posts = Post.objects.filter(published=True)
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})
```

### Class-Based Views

```python
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10
    
    def get_queryset(self):
        return Post.objects.filter(published=True)

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

class PostCreateView(CreateView):
    model = Post
    fields = ['title', 'content']
    success_url = reverse_lazy('post_list')
```

## Django REST Framework

### Serializers

```python
from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'author_name', 'created_at']
        read_only_fields = ['author', 'created_at']
    
    def validate_title(self, value):
        if len(value) < 5:
            raise serializers.ValidationError("Title must be at least 5 characters")
        return value
```

### ViewSets

```python
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        post = self.get_object()
        post.published = True
        post.save()
        return Response({'status': 'published'})
```

### Routers

```python
from rest_framework.routers import DefaultRouter
from .views import PostViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet)

urlpatterns = router.urls
```

## Authentication

### Built-in Authentication

```python
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

@login_required
def protected_view(request):
    return render(request, 'protected.html')

class ProtectedView(LoginRequiredMixin, View):
    login_url = '/login/'
```

### DRF Authentication

**Token Authentication:**
```python
# settings.py
INSTALLED_APPS = [
    'rest_framework',
    'rest_framework.authtoken',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
}

# views.py
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('api/token/', obtain_auth_token),
]
```

**JWT Authentication:**
```python
# Install: pip install djangorestframework-simplejwt

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
]
```

## Permissions

```python
from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user

class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
```

## Forms and Validation

```python
from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10}),
        }
    
    def clean_title(self):
        title = self.cleaned_data['title']
        if Post.objects.filter(title=title).exists():
            raise forms.ValidationError("Title already exists")
        return title
```

## Middleware

```python
class CustomMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Before view
        request.custom_attribute = 'value'
        
        response = self.get_response(request)
        
        # After view
        response['X-Custom-Header'] = 'value'
        
        return response

# settings.py
MIDDLEWARE = [
    'myapp.middleware.CustomMiddleware',
]
```

## Admin Interface

```python
from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'published', 'created_at']
    list_filter = ['published', 'created_at']
    search_fields = ['title', 'content']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(author=request.user)
```

## Database Migrations

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Show migrations
python manage.py showmigrations

# Rollback
python manage.py migrate myapp 0003
```

## Testing

```python
from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Post

class PostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('testuser', 'test@example.com', 'password')
        self.post = Post.objects.create(title='Test', content='Content', author=self.user)
    
    def test_post_creation(self):
        self.assertEqual(self.post.title, 'Test')
        self.assertEqual(str(self.post), 'Test')

class PostAPITest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('testuser', 'test@example.com', 'password')
    
    def test_post_list(self):
        response = self.client.get('/api/posts/')
        self.assertEqual(response.status_code, 200)
```

## Performance Optimization

### Query Optimization

```python
# Use select_related for ForeignKey
posts = Post.objects.select_related('author').all()

# Use prefetch_related for ManyToMany
articles = Article.objects.prefetch_related('tags').all()

# Only fetch needed fields
posts = Post.objects.only('title', 'created_at')

# Defer heavy fields
posts = Post.objects.defer('content')
```

### Caching

```python
from django.core.cache import cache

def get_posts():
    posts = cache.get('posts')
    if posts is None:
        posts = list(Post.objects.all())
        cache.set('posts', posts, 300)  # 5 minutes
    return posts
```

## Deployment

### Production Settings

```python
# settings.py
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': '5432',
    }
}

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
```

### WSGI/ASGI

**Gunicorn:**
```bash
gunicorn myproject.wsgi:application --bind 0.0.0.0:8000
```

**Uvicorn (ASGI):**

---

**Note:** This file was automatically condensed to meet the 500-line requirement. Additional content has been moved to the references/ folder.
