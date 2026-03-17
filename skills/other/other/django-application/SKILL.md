---
name: django-application
description: Develop production-grade Django applications with models, views, ORM queries, authentication, and admin interfaces. Use when building web applications, managing databases with Django ORM, and implementing authentication systems.
---

# Django Application

## Overview

Build comprehensive Django web applications with proper model design, view hierarchies, database operations, user authentication, and admin functionality following Django conventions and best practices.

## When to Use

- Creating Django web applications
- Designing models and database schemas
- Implementing views and URL routing
- Building authentication systems
- Using Django ORM for database operations
- Creating admin interfaces and dashboards

## Instructions

### 1. **Django Project Setup**

```bash
django-admin startproject myproject
cd myproject
python manage.py startapp users
python manage.py startapp products
```

### 2. **Model Design with ORM**

```python
# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('user', 'Regular User'),
    ]
    profile_picture = models.ImageField(upload_to='profiles/', null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['role']),
        ]

    def __str__(self):
        return self.email

# products/models.py
User = get_user_model()

class Product(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]

    title = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['slug', 'owner']

    def __str__(self):
        return self.title

class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['product', 'author']
```

### 3. **Views with Class-Based and Function-Based Approaches**

```python
# products/views.py
from django.views import View
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q, Count, Avg
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from .models import Product, ProductReview
from .serializers import ProductSerializer

# Class-based view with authentication
class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'products/list.html'
    context_object_name = 'products'
    paginate_by = 20

    def get_queryset(self):
        queryset = Product.objects.filter(status='published')

        # Search and filter
        search = self.request.GET.get('q')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )

        # Price range filter
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        return queryset.annotate(
            review_count=Count('reviews'),
            avg_rating=Avg('reviews__rating')
        ).order_by('-created_at')

# REST API ViewSet
class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def get_queryset(self):
        return Product.objects.filter(owner=self.request.user)

    @action(detail=True, methods=['post'])
    def add_review(self, request, pk=None):
        product = self.get_object()
        serializer = ProductReviewSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(product=product, author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def reviews(self, request, pk=None):
        product = self.get_object()
        reviews = product.reviews.all()
        serializer = ProductReviewSerializer(reviews, many=True)
        return Response(serializer.data)
```

### 4. **Authentication and Permissions**

```python
# users/views.py
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
from rest_framework.authtoken.models import Token
from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

@require_http_methods(['POST'])
@csrf_protect
def login_view(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    user = authenticate(request, username=email, password=password)

    if user is not None:
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return JsonResponse({
            'success': True,
            'token': token.key,
            'user_id': user.id
        })

    return JsonResponse({'error': 'Invalid credentials'}, status=401)

@require_http_methods(['POST'])
def logout_view(request):
    logout(request)
    return JsonResponse({'success': True})
```

### 5. **Database Queries and Optimization**

```python
# products/queries.py
from django.db.models import Q, Count, Avg, F, Case, When, Value
from django.db.models.functions import Coalesce
from .models import Product, ProductReview

# Optimized queries with select_related and prefetch_related
def get_product_details(product_id):
    return Product.objects.select_related('owner').prefetch_related(
        'reviews__author'
    ).get(id=product_id)

# Aggregation queries
def get_top_products():
    return Product.objects.annotate(
        review_count=Count('reviews'),
        avg_rating=Avg('reviews__rating'),
        total_reviews=Count('reviews', distinct=True)
    ).filter(review_count__gt=0).order_by('-avg_rating')[:10]

# Complex filtering
def search_products(query, category=None, min_price=None, max_price=None):
    queryset = Product.objects.filter(
        Q(title__icontains=query) | Q(description__icontains=query)
    )

    if category:
        queryset = queryset.filter(category=category)
    if min_price:
        queryset = queryset.filter(price__gte=min_price)
    if max_price:
        queryset = queryset.filter(price__lte=max_price)

    return queryset.select_related('owner')

# Bulk operations
def bulk_update_stock(updates):
    products_to_update = []
    for product_id, new_stock in updates.items():
        product = Product.objects.get(id=product_id)
        product.stock = new_stock
        products_to_update.append(product)

    Product.objects.bulk_update(products_to_update, ['stock'])
```

### 6. **URL Routing**

```python
# myproject/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from products.views import ProductViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-token-auth/', obtain_auth_token),
]
```

### 7. **Admin Interface Customization**

```python
# products/admin.py
from django.contrib import admin
from .models import Product, ProductReview

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'stock', 'status', 'owner', 'created_at']
    list_filter = ['status', 'created_at', 'owner']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Basic Info', {
            'fields': ('title', 'slug', 'owner')
        }),
        ('Details', {
            'fields': ('description', 'price', 'stock', 'status')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.owner = request.user
        super().save_model(request, obj, form, change)

@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'author', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    readonly_fields = ['created_at']
```

## Best Practices

### ✅ DO
- Use models for database operations
- Implement proper indexes on frequently queried fields
- Use select_related and prefetch_related for query optimization
- Implement authentication and permissions
- Use Django Forms for form validation
- Cache expensive queries
- Use management commands for batch operations
- Implement logging for debugging
- Use middleware for cross-cutting concerns
- Validate user input

### ❌ DON'T
- Use raw SQL without ORM
- N+1 query problems without optimization
- Store secrets in code
- Trust user input directly
- Override __init__ in models unnecessarily
- Make synchronous heavy operations in views
- Use inheritance models unless necessary
- Expose stack traces in production

## Complete Example

```python
# settings.py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'rest_framework',
    'users',
    'products'
]

AUTH_USER_MODEL = 'users.CustomUser'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}

# models.py + views.py (see sections above)
# urls.py + admin.py (see sections above)
```
