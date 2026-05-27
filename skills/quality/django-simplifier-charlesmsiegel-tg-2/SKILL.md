---
name: django-simplifier
description: Simplify overly complex Django code and detect Django-specific anti-patterns. Use when user asks to simplify, refactor, or improve Django code, find N+1 queries, detect Django anti-patterns, optimize QuerySets, or analyze Django project architecture. Triggers on requests involving Django models, views, QuerySets, ORM optimization, serializers, forms, signals, middleware, or Django best practices. For general Python analysis, use the python-simplifier skill instead.
---

# Django Code Simplifier

Transform complex Django code into clean, performant, idiomatic solutions.

## Analysis Scripts

```bash
# Comprehensive Django analysis (runs all Django checks)
python scripts/analyze_django.py /path/to/project

# Individual analyzers:
python scripts/find_django_issues.py .           # N+1 queries, fat views, basic issues
python scripts/find_django_antipatterns.py .     # ORM misuse, security issues, model problems
python scripts/find_django_overengineering.py .  # Unnecessary abstractions, premature patterns

# Filter by category or severity:
python scripts/find_django_antipatterns.py . --category performance
python scripts/find_django_antipatterns.py . --category security
python scripts/find_django_antipatterns.py . --min-severity medium

# JSON output for CI/tooling
python scripts/analyze_django.py . --format json > report.json
```

## What Each Script Detects

### `find_django_issues.py` - Basic Issues
- N+1 query risks (`.all()` in loops)
- `.save()` / `.delete()` / `.create()` in loops
- Fat views (100+ lines)
- Hardcoded URLs instead of `reverse()`
- Missing `select_related` / `prefetch_related`

### `find_django_antipatterns.py` - Comprehensive Anti-Patterns

| Category | Issues Detected |
|----------|-----------------|
| **query** | `save_in_loop`, `create_in_loop`, `unbounded_queryset`, `update_without_f`, `raw_sql`, `deprecated_extra` |
| **performance** | `excessive_queries`, nested template loops, template queries |
| **model** | `missing_str_method`, `fat_model`, `too_many_fields` |
| **view** | `hardcoded_url`, `fat_view_method`, `url_without_name` |
| **form** | `query_in_form_clean` |
| **security** | `hardcoded_secret`, `debug_true`, `mark_safe_usage`, `eval_exec_usage` |

### `find_django_overengineering.py` - Over-Engineering

| Issue | Description |
|-------|-------------|
| `single_impl_abstract_model` | Abstract model with only one concrete child |
| `unused_abstract_model` | Abstract model never extended |
| `unnecessary_manager` | Custom manager with ≤1 method |
| `unnecessary_signal` | Signal for simple save logic |
| `single_use_mixin` | Mixin used only once |
| `deep_form_inheritance` | Form/Serializer with 3+ inheritance levels |
| `unnecessary_middleware` | Middleware with minimal logic |
| `unnecessary_service_layer` | Service wrapping simple CRUD |

## Common Django Patterns

### N+1 Query Prevention

```python
# Before: N+1 problem
for order in Order.objects.all():
    print(order.customer.name)  # Query per iteration!

# After: select_related (ForeignKey/OneToOne)
for order in Order.objects.select_related('customer'):
    print(order.customer.name)  # Single query

# After: prefetch_related (ManyToMany/reverse FK)
for customer in Customer.objects.prefetch_related('orders'):
    print(customer.orders.count())
```

### Bulk Operations

```python
# Before: Loop creates (N queries)
for data in items:
    Model.objects.create(**data)

# After: bulk_create (1 query)
Model.objects.bulk_create([Model(**d) for d in items])

# Before: Loop updates
for obj in queryset:
    obj.status = 'done'
    obj.save()

# After: Single update
queryset.update(status='done')

# With F() for safe increment
from django.db.models import F
Product.objects.filter(id=1).update(stock=F('stock') - 1)
```

### Fat View → Thin View

```python
# Before: Business logic in view
def order_view(request, order_id):
    order = Order.objects.get(id=order_id)
    # 50 lines of business logic...
    return render(...)

# After: Logic in model/service
def order_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    result = order.process()  # Logic moved to model
    return render(request, 'order.html', {'result': result})
```

### Signals → Explicit Methods

```python
# Before: Hidden signal
@receiver(post_save, sender=Order)
def update_inventory(sender, instance, **kwargs):
    # Hard to trace, implicit behavior
    ...

# After: Explicit method
class Order(models.Model):
    def complete(self):
        self.status = 'completed'
        self.save()
        self._update_inventory()  # Explicit, traceable
```

### URL Best Practices

```python
# Before: Hardcoded
return redirect('/orders/123/')

# After: Named URL
from django.urls import reverse
return redirect(reverse('order-detail', args=[123]))

# Or with shortcut
from django.shortcuts import redirect
return redirect('order-detail', pk=123)
```

## Model Best Practices

```python
class Order(models.Model):
    # Always add __str__
    def __str__(self):
        return f"Order #{self.number}"
    
    # Use TextChoices
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        COMPLETED = 'completed', 'Completed'
    
    status = models.CharField(max_length=20, choices=Status.choices)
    
    # Don't use null=True on CharField
    # BAD: name = models.CharField(null=True, blank=True)
    # GOOD:
    name = models.CharField(blank=True, default='')
    
    # Always set related_name
    customer = models.ForeignKey(Customer, related_name='orders', on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [models.Index(fields=['status', 'created_at'])]
```

## Django Over-Engineering Signs

| Pattern | Problem | Solution |
|---------|---------|----------|
| Abstract model with 1 child | Premature abstraction | Merge into concrete model |
| CBV with 6+ overrides | Too complex | Use function-based view |
| Single-use mixin | No reuse benefit | Inline the code |
| Many signal handlers | Hard to trace | Use explicit method calls |
| Custom manager for simple filter | Unnecessary | Use QuerySet methods |
| Service layer for CRUD | Extra indirection | Use model methods |

## Security Checklist

```python
# Use get_object_or_404 with ownership check
order = get_object_or_404(Order, id=id, owner=request.user)

# Never use mark_safe with user data
# BAD: mark_safe(user_input)
# GOOD:
from django.utils.html import format_html
format_html('<p>{}</p>', user_input)

# Keep secrets out of code
# BAD: SECRET_KEY = 'hardcoded-secret'
# GOOD: SECRET_KEY = os.environ.get('SECRET_KEY')
```

## When to Use What

| Need | Use |
|------|-----|
| Simple CRUD | Generic views, ModelForm |
| Complex business logic | Model methods |
| Cross-cutting concerns | Middleware (sparingly) |
| Decoupled apps | Signals (sparingly) |
| Query optimization | select_related, prefetch_related |
| Bulk operations | bulk_create, bulk_update, update() |
