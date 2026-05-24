---
id: py-django-loop-without-eager
title: Django ORM iteration — verify select_related/prefetch_related to avoid N+1
severity: warning
impact: HIGH
impactDescription: Hot-path or correctness risk at realistic n
language: python
tags: python, warning, complexity-cuts
---

# Django ORM iteration — verify select_related/prefetch_related to avoid N+1

Iterating a Django QuerySet that touches a related model triggers one extra query per row — classic N+1. `select_related` (foreign key, one query with JOIN) or `prefetch_related` (reverse / many-to-many, two queries) fixes it.

## Fix

Add .select_related('fk') for FK/OneToOne, .prefetch_related('rel') for reverse FK / M2M.

## Incorrect

```python
# N+1 queries
for order in Order.objects.all():
    print(order.user.email)  # extra query per order
```

## Correct

```python
# 1 query with JOIN
for order in Order.objects.select_related("user"):
    print(order.user.email)

# For reverse FK / M2M:
for user in User.objects.prefetch_related("orders"):
    for order in user.orders.all():
        ...
```

## Escalate to

If this pattern is widespread in the codebase, load **complexity-cuts** for the corrective workflow.
