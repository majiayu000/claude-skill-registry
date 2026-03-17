---
name: django
description: python library
version: 6.0.2
ecosystem: python
license: BSD-3-Clause
generated_with: claude-sonnet-4-5-20250929
---

## Imports

```python
import django
from django.conf import settings
from django.core.management import execute_from_command_line
from django.http import HttpRequest, HttpResponse, JsonResponse, Http404
from django.urls import include, path, reverse
from django.shortcuts import get_object_or_404, redirect, render
from django.db import models, transaction
from django.contrib import admin
from django.apps import AppConfig, apps
from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist
from django.test import TestCase, override_settings
from django.views.generic.base import View
```

## Core Patterns

### Project entrypoint and settings bootstrap ✅ Current
```python
from __future__ import annotations

import os
import sys

import django
from django.conf import settings
from django.core.management import execute_from_command_line


def main() -> None:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

    # Minimal safety check: ensure settings can be imported/configured.
    django.setup()

    # Run Django's management command runner (e.g., runserver, migrate, test).
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
```
* Use `DJANGO_SETTINGS_MODULE` to point Django at your settings module, then call `django.setup()` before interacting with models in standalone scripts.
* `execute_from_command_line()` is the standard entrypoint for `manage.py`.

### URL routing + function-based view ✅ Current
```python
from __future__ import annotations

from django.http import HttpRequest, HttpResponse, JsonResponse, Http404
from django.urls import path


def healthz(request: HttpRequest) -> JsonResponse:
    return JsonResponse({"status": "ok"})


def hello(request: HttpRequest, name: str) -> HttpResponse:
    if not name:
        raise Http404("Name is required")
    return HttpResponse(f"Hello, {name}!")


urlpatterns = [
    path("healthz/", healthz, name="healthz"),
    path("hello/<str:name>/", hello, name="hello"),
]
```
* Use `path()` for common URL patterns and typed converters like `<str:name>`.
* Raise `Http404` for "not found" responses; Django will render a 404 page (or JSON if you handle it).

### Render templates + redirects ✅ Current
```python
from __future__ import annotations

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse


def index(request: HttpRequest) -> HttpResponse:
    # Renders templates/index.html with context.
    return render(request, "index.html", {"user_agent": request.META.get("HTTP_USER_AGENT", "")})


def go_home(request: HttpRequest) -> HttpResponse:
    # Prefer named URLs for redirects.
    return redirect(reverse("home"))
```
* Use `render()` to return an `HttpResponse` with a template.
* Use `redirect()` with `reverse()` (named routes) to avoid hardcoding URLs.

### Models + ORM queries + transactions ✅ Current
```python
from __future__ import annotations

from django.db import models, transaction


class Article(models.Model):
    title = models.CharField(max_length=200)
    published = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title


def publish_article(article_id: int) -> None:
    # Example of an atomic update.
    with transaction.atomic():
        article = Article.objects.select_for_update().get(pk=article_id)
        article.published = True
        article.save(update_fields=["published"])
```
* Define models by subclassing `models.Model`; use `objects` manager for queries.
* Wrap multi-step updates in `transaction.atomic()`; use `select_for_update()` for row locking where supported.

### Admin registration ✅ Current
```python
from __future__ import annotations

from django.contrib import admin
from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=200)
    published = models.BooleanField(default=False)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "published")
    list_filter = ("published",)
    search_fields = ("title",)
```
* Register models with the admin via `@admin.register(Model)` and customize with `ModelAdmin`.

### App configuration ✅ Current
```python
from __future__ import annotations

from django.apps import AppConfig


class MyAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "myapp"
    verbose_name = "My Application"

    def ready(self) -> None:
        # Import signal handlers, register checks, etc.
        # Only runs once when Django starts.
        pass  # import myapp.signals  # noqa: F401
```
* Subclass `AppConfig` to customize app metadata and perform initialization in `ready()`.
* Register your `AppConfig` in `INSTALLED_APPS` as `"myapp.apps.MyAppConfig"`.
* The `name` attribute must match an importable Python package path in your project.
* Use `ready()` for one-time initialization like registering signal handlers (be careful not to import models at module level to avoid import cycles).

### Class-based views (ListView) ✅ Current
```python
from __future__ import annotations

from django.views.generic.list import ListView
from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)


class AuthorListView(ListView):
    model = Author
    template_name = "authors/list.html"
    context_object_name = "authors"
    paginate_by = 30
    ordering = ["name"]
```
* Use `ListView` for listing querysets with built-in pagination support.
* Set `paginate_by` to enable pagination; Django adds `page_obj`, `paginator`, and `is_paginated` to context.

### Class-based views (DetailView) ✅ Current
```python
from __future__ import annotations

from django.views.generic.detail import DetailView
from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)


class AuthorDetailView(DetailView):
    model = Author
    template_name = "authors/detail.html"
    context_object_name = "author"
    slug_field = "slug"
    slug_url_kwarg = "slug"
```
* Use `DetailView` for displaying single object details.
* Django automatically fetches object by `pk` or custom slug field.

## Configuration

- **Settings module**: Set `DJANGO_SETTINGS_MODULE="package.settings"` (commonly via environment variable) before calling `django.setup()` in standalone code.
- **Common settings to customize** (in your settings file):
  - `DEBUG` (bool)
  - `SECRET_KEY` (string)
  - `ALLOWED_HOSTS` (list[str])
  - `INSTALLED_APPS` (list[str])
  - `MIDDLEWARE` (list[str])
  - `ROOT_URLCONF` (string)
  - `TEMPLATES` (list[dict])
  - `DATABASES` (dict)
  - `STATIC_URL` / `STATIC_ROOT`
  - `DEFAULT_STORAGE_ALIAS` (string, for custom storage backends)
  - `STATICFILES_STORAGE_ALIAS` (string, for static files storage)
- **Docs workflow (source + build)**:
  - Django docs are written in reStructuredText and built with Sphinx.
  - Build locally from the `docs/` directory:
    - `python -m pip install Sphinx`
    - `make html` (or `make.bat html` on Windows)
    - open `docs/_build/html/index.html`
- **Tests**: Run Django's test suite following the official unit test instructions in Django's contributing docs.

## Pitfalls

### Wrong: Building documentation from the wrong directory
```python
# This is a shell command, not Python; shown here to illustrate the mistake.
# Wrong (run from repo root):
# make html
raise SystemExit("Run `make html` from the `docs/` directory so Sphinx finds its config.")
```

### Right: Build docs from `docs/` so Sphinx finds configuration
```python
# This is a shell command, not Python; shown here to illustrate the fix.
# cd docs
# python -m pip install Sphinx
# make html
# # Windows: make.bat html
raise SystemExit("Build docs from `docs/` (not repo root) to ensure Sphinx config is discovered.")
```

### Wrong: Using ORM models before `django.setup()` in a standalone script
```python
from __future__ import annotations

import os

from django.db import models


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")


class Article(models.Model):
    title = models.CharField(max_length=200)


# Importing/using models without django.setup() can fail depending on context.
# For example, app registry may not be ready.
raise SystemExit("Call django.setup() before using models in standalone scripts.")
```

### Right: Call `django.setup()` before importing/using app models
```python
from __future__ import annotations

import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

# Now it's safe to import and use models from installed apps.
raise SystemExit("Django is initialized; you can now import and use models safely.")
```

### Wrong: Hardcoding URLs instead of using `reverse()`
```python
from __future__ import annotations

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect


def go_home(request: HttpRequest) -> HttpResponse:
    # Breaks if the URL changes.
    return redirect("/home/")
```

### Right: Use named URLs with `reverse()` (or pass the view name to `redirect()`)
```python
from __future__ import annotations

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse


def go_home(request: HttpRequest) -> HttpResponse:
    return redirect(reverse("home"))
```

### Wrong: Catch-all `Exception` instead of raising `Http404` for missing objects
```python
from __future__ import annotations

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

# NOTE: In real code, you'd import your model, e.g. from app.models import Article


def detail(request: HttpRequest, pk: int) -> HttpResponse:
    try:
        raise Exception("pretend ORM lookup failed")  # placeholder for a failing lookup
    except Exception:
        # Returns 200 with an error page, not a 404.
        return render(request, "not_found.html", status=200)
```

### Right: Use `get_object_or_404()` (or raise `Http404`) for missing records
```python
from __future__ import annotations

from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=200)


def detail(request: HttpRequest, pk: int) -> HttpResponse:
    article = get_object_or_404(Article, pk=pk)
    return render(request, "detail.html", {"article": article})
```

### Wrong: ListView without model or queryset
```python
from __future__ import annotations

from django.views.generic.list import ListView


class AuthorListView(ListView):
    template_name = "authors/list.html"
    # Missing: model, queryset, or get_queryset() override
```
* Django will raise `ImproperlyConfigured` exception.

### Right: ListView with model or queryset defined
```python
from __future__ import annotations

from django.views.generic.list import ListView
from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=200)


class AuthorListView(ListView):
    model = Author  # or: queryset = Author.objects.all()
    template_name = "authors/list.html"
```

### Wrong: Accessing settings before configuration
```python
from __future__ import annotations

from django.conf import settings

# Accessing settings before django.setup() or settings.configure()
print(settings.DEBUG)  # May raise ImproperlyConfigured
```

### Right: Configure or setup before accessing settings
```python
from __future__ import annotations

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

from django.conf import settings
print(settings.DEBUG)  # Safe after setup
```

## References

- [Homepage](https://www.djangoproject.com/)
- [Documentation](https://docs.djangoproject.com/)
- [Release notes](https://docs.djangoproject.com/en/stable/releases/)
- [Funding](https://www.djangoproject.com/fundraising/)
- [Source](https://github.com/django/django)
- [Tracker](https://code.djangoproject.com/)
- [New ticket](https://code.djangoproject.com/newticket)
- [Contributing guide](https://docs.djangoproject.com/en/dev/internals/contributing/)
- [Django Discord](https://chat.djangoproject.com)
- [Django Forum](https://forum.djangoproject.com/)

## Migration from previous versions

For upgrade guidance specific to version 6.0.2, consult Django's release notes:
https://docs.djangoproject.com/en/stable/releases/

Key migration considerations:
- Review `INSTALLED_APPS` to ensure all apps have proper `AppConfig` classes.
- Check for deprecated settings or middleware in your settings module.
- Run `python manage.py check` to identify configuration issues.
- Test pagination and class-based views if upgrading from older versions.
- Review custom storage backends if using `DEFAULT_STORAGE_ALIAS` or `STATICFILES_STORAGE_ALIAS`.

## API Reference

### Core Initialization
- **django.setup(set_prefix: bool = True) -> None** - Initialize Django (apps registry, settings); call in standalone scripts before ORM usage.
- **django.VERSION** - Tuple representing Django version: `(major, minor, micro, releaselevel, serial)`.
- **django.__version__** - String representation of Django version (e.g., "6.0.2").

### Configuration
- **django.conf.settings** - Access configured settings (lazy proxy, read-only in most runtime code).
- **django.conf.Settings(settings_module: str)** - Settings object initialized from a module path.
- **django.conf.LazySettings** - Lazy proxy for global Django settings or custom settings object.
- **django.conf.LazySettings.configure(default_settings=global_settings, **options) -> None** - Manually configure settings without a settings module.
- **django.conf.LazySettings.configured** - Property that returns `True` if settings have been configured.
- **django.conf.Settings.is_overridden(setting: str) -> bool** - Check if a setting has been overridden from defaults.
- **django.conf.ENVIRONMENT_VARIABLE** - Constant for `DJANGO_SETTINGS_MODULE` environment variable name.
- **django.conf.DEFAULT_STORAGE_ALIAS** - Constant for default storage alias name.
- **django.conf.STATICFILES_STORAGE_ALIAS** - Constant for staticfiles storage alias name.

### Apps
- **django.apps.AppConfig** - Base class for Django application configuration.
- **django.apps.apps** - Global application registry instance (Apps type).

### Management
- **django.core.management.execute_from_command_line(argv)** - Run management commands (used by `manage.py`).

### URLs
- **django.urls.path(route, view, kwargs=None, name=None)** - Define URL patterns with converters.
- **django.urls.include(module)** - Include other URLconfs (apps).
- **django.urls.reverse(viewname, args=None, kwargs=None)** - Build URLs from named routes.

### HTTP
- **django.http.HttpRequest** - Incoming request object (headers in `META`, method, user, etc.).
- **django.http.HttpResponse(content=b"", status=200, ...)** - Basic HTTP response type.
- **django.http.JsonResponse(data, status=200, ...)** - JSON response with proper content type/encoding.
- **django.http.Http404** - Exception to signal a 404 response.

### Shortcuts
- **django.shortcuts.render(request, template_name, context=None, status=None)** - Render template to `HttpResponse`.
- **django.shortcuts.redirect(to, *args, **kwargs)** - Return an HTTP redirect response.
- **django.shortcuts.get_object_or_404(klass, *args, **kwargs)** - Fetch object or raise `Http404`.

### Models & Database
- **django.db.models.Model** - Base class for ORM models.
- **django.db.transaction.atomic()** - Transaction context manager/decorator for atomic DB operations.

### Admin
- **django.contrib.admin.site / admin.register()** - Admin registration and configuration entrypoints.
- **django.contrib.admin.ModelAdmin** - Base class for customizing model admin interface.

### Views
- **django.views.generic.base.View** - Base class for all Django class-based views.
- **django.views.generic.list.ListView** - Generic view for displaying a list of objects with pagination support.
- **django.views.generic.detail.DetailView** - Generic view for displaying a single object.
- **django.views.generic.detail.SingleObjectTemplateResponseMixin** - Mixin for template response handling in detail views.
- **django.views.generic.edit.ModelFormMixin** - Mixin for model form handling in edit views.

### Exceptions
- **django.core.exceptions.ImproperlyConfigured** - Exception for Django configuration errors.
- **django.core.exceptions.ObjectDoesNotExist** - Exception raised when object lookup fails.

### Testing
- **django.test.TestCase** - Base test case class for Django tests with database isolation and fixtures.
- **django.test.override_settings(**kwargs)** - Decorator/context manager for temporarily overriding settings in tests.

## Current Library State (from source analysis)

### Version Information
- **Version**: 6.0.2
- **Ecosystem**: Python
- **License**: BSD-3-Clause

### Key Capabilities
- Full-featured web framework with ORM, templating, URL routing, and admin interface
- Class-based and function-based views for flexible request handling
- Built-in pagination support with customizable paginators
- Application registry system for modular app configuration
- Comprehensive testing infrastructure with test client and database isolation
- Settings management with lazy loading and environment-based configuration
- Transaction management with atomic operations and row-level locking
- Generic views for common patterns (list, detail, create, update, delete)

### Testing Patterns
The source analysis shows extensive use of:
- `TestCase` with `setUpTestData` for efficient test data creation
- `@override_settings` decorator for temporary settings changes in tests
- `self.client.get/post()` for simulating HTTP requests
- `assertTemplateUsed`, `assertNumQueries`, and context assertions
- Test-driven patterns for pagination, ordering, and error handling
