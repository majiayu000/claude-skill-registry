---
name: django-expert
version: 1.0.0
description: Expert-level Django development for robust Python web applications with ORM, admin, and authentication
category: frameworks
tags: [django, python, web, orm, mvc, rest-framework]
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash(python:*, django-admin:*, manage.py:*)
---

# Django Expert

Expert guidance for Django - high-level Python web framework for building secure, scalable web applications with batteries included.

## Core Concepts

### Django Architecture
- MVT (Model-View-Template) pattern
- ORM (Object-Relational Mapping)
- Admin interface
- Authentication system
- URL routing
- Template engine
- Forms and validation

### Key Components
- Models (database tables)
- Views (business logic)
- Templates (presentation)
- URLs (routing)
- Forms (user input)
- Middleware (request/response processing)

## Project Setup

```bash
# Install Django
pip install django

# Create project
django-admin startproject myproject
cd myproject

# Create app
python manage.py startapp myapp

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run server
python manage.py runserver
```

## Models

```python
# myapp/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Post(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['slug']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.status == 'published' and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'Comment by {self.author} on {self.post}'
```

## Views

```python
# myapp/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView
from django.contrib import messages
from .models import Post, Comment
from .forms import PostForm, CommentForm

# Function-based view
def post_list(request):
    posts = Post.objects.filter(status='published').select_related('author')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status='published')
    comments = post.comments.select_related('author')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Comment added successfully')
            return redirect('post_detail', slug=slug)
    else:
        form = CommentForm()

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form
    })

# Class-based views
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(status='published').select_related('author')

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_queryset(self):
        return Post.objects.filter(status='published')

class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
```

## URLs

```python
# myproject/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),
]

# myapp/urls.py
from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('post/create/', views.PostCreateView.as_view(), name='post_create'),
]
```

## Forms

```python
# myapp/forms.py
from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'slug', 'content', 'status']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10}),
        }

    def clean_slug(self):
        slug = self.cleaned_data['slug']
        if Post.objects.filter(slug=slug).exists():
            raise forms.ValidationError('Slug already exists')
        return slug

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3}),
        }
```

## Django REST Framework

```python
# Install: pip install djangorestframework

# settings.py
INSTALLED_APPS = [
    ...
    'rest_framework',
]

# serializers.py
from rest_framework import serializers
from .models import Post, Comment

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = ['id', 'author', 'content', 'created_at']

class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'slug', 'author', 'content',
                  'status', 'created_at', 'comments']

# views.py (API)
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.filter(status='published')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        post = self.get_object()
        post.status = 'published'
        post.save()
        return Response({'status': 'published'})

# urls.py (API)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'posts', PostViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
```

## Admin Interface

```python
# myapp/admin.py
from django.contrib import admin
from .models import Post, Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'

    actions = ['make_published']

    def make_published(self, request, queryset):
        queryset.update(status='published')
    make_published.short_description = "Mark selected as published"

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'author', 'created_at']
    list_filter = ['created_at']
    search_fields = ['content']
```

## Authentication

```python
# views.py
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

# URLs
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', signup, name='signup'),
]
```

## Testing

```python
# myapp/tests.py
from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Post

class PostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='test')
        self.post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            author=self.user,
            content='Test content',
            status='published'
        )

    def test_post_creation(self):
        self.assertEqual(self.post.title, 'Test Post')
        self.assertEqual(str(self.post), 'Test Post')

    def test_post_slug_unique(self):
        with self.assertRaises(Exception):
            Post.objects.create(
                title='Another Post',
                slug='test-post',  # Duplicate slug
                author=self.user,
                content='Content'
            )

class PostViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test', password='test')

    def test_post_list_view(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_post_create_requires_auth(self):
        response = self.client.get('/post/create/')
        self.assertEqual(response.status_code, 302)  # Redirect to login

        self.client.login(username='test', password='test')
        response = self.client.get('/post/create/')
        self.assertEqual(response.status_code, 200)
```

## Best Practices

- Use select_related/prefetch_related to avoid N+1 queries
- Implement proper validation in forms
- Use class-based views for common patterns
- Protect against CSRF attacks (enabled by default)
- Use Django's built-in authentication
- Implement proper permission checks
- Add database indexes for frequently queried fields
- Use Django migrations for schema changes

## Resources

- Django Docs: https://docs.djangoproject.com/
- Django REST Framework: https://www.django-rest-framework.org/
- Django Packages: https://djangopackages.org/
