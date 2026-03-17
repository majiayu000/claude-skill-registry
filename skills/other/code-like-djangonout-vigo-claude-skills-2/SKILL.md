---
name: code-like-djangonout
description: Provides Django web framework expertise including project structure, models, views, admin, Celery tasks, testing, and Python best practices. Use when generating, analyzing, refactoring, or reviewing Django/Python code.
---

# Django Development Skill

## When to Use

Use this skill when:

- Writing, reviewing, or refactoring Django applications
- Creating or modifying Django models, views, admin, forms
- Setting up Django project structure and tooling
- Implementing Celery tasks and signals
- Writing Django tests
- Configuring linters (ruff, pylint) for Python/Django

## Prerequisites Check

Before starting any Django work:

```bash
# Check Python version
python --version

# Check for .python-version file
cat .python-version 2>/dev/null

# Verify virtual environment is active
echo $VIRTUAL_ENV

# Check Django version
python -c "import django; print(django.VERSION)"

# Check if ruff is available
command -v ruff
```

---

## Instructions

### General Coding Approach

- All naming and comments must be in **English**
- Follow Python (PEP 8) and Django conventions
- Virtual environment must be activated
- Detect project's Python version and use appropriate features
- **Do not use type annotations** (Django doesn't fully rely on them)
- If annotations are needed, import: `from __future__ import annotations`

---

### Formatting and Linting

#### Ruff Setup

```bash
python -m pip install ruff
```

Minimal `.ruff.toml`:

```toml
line-length = 119
indent-width = 4
target-version = "py312"
exclude = [
    "**/migrations",
    "**/manage.py",
]

[format]
quote-style = "single"
exclude = ["**/manage.py"]

[lint]
select = ["ALL"]
allowed-confusables = ["ı", "'"]
mccabe.max-complexity = 15
ignore = [
    "ANN",    # annotations
    "D",      # docstrings (pydocstyle)
    "D203",   # one-blank-line-before-class
    "D213",   # multi-line-summary-second-line
    "ISC001", # implicit string concat
    "COM812", # missing trailing comma
    "ERA",    # commented out code
    "RUF012", # mutable class default
    "FBT002", # boolean default positional arg
    "TD003",  # missing todo link
    "FIX002", # line contains todo
    "PT009",  # pytest unittest assertion
    "PT019",  # pytest fixture param
    "PT027",  # pytest unittest raises
    "PGH004", # file-wide noqa
    "INP001", # implicit namespace package
]

[lint.flake8-quotes]
inline-quotes = "single"
docstring-quotes = "double"

[lint.pylint]
max-statements = 100
max-returns = 20
max-args = 10
max-positional-args = 8
max-branches = 20

[lint.isort]
known-first-party = ["core"]
section-order = [
    "future",
    "standard-library",
    "django",
    "third-party",
    "first-party",
    "local-folder",
]

[lint.isort.sections]
django = ["django"]
```

#### Pylint Setup

```bash
python -m pip install pylint

# Generate config if missing
pylint --generate-rcfile > .pylintrc
```

#### Acceptable noqa Comments

- `# noqa: S324` - hashlib security
- `# noqa: SLF001` - Model._meta access
- `# noqa: ARG002` - unused args in Django overrides

Always ask before adding other noqa comments.

---

### Coding Style

#### Quote Convention

Always use **single quotes**. Double quotes only for docstrings or unavoidable 
cases:

```python
# ✅ Good
user_name = 'vigo'
page = request.GET.get('page')

# ✅ Acceptable
message = "vigo's number"
```

#### No Magic Values

```python
# ❌ Bad
def check_age(user):
    if user.age > 10:
        pass

# ✅ Good
USER_MAX_AGE = 10

def check_age(user):
    if user.age > USER_MAX_AGE:
        pass
```

#### Dict Access

Always use `.get()` for dict access:

```python
# ❌ Bad
value = FOO['bar']

# ✅ Good
value = FOO.get('bar')
value = FOO.get('bar', 'default')
```

#### Error Handling

Never use blind exceptions. Always handle specific exceptions:

```python
# ❌ Bad
try:
    do_something()
except Exception:
    pass

# ✅ Good
try:
    do_something()
except SpecificError as exc:
    logger.exception('Operation failed: %s', exc)
    raise
```

#### Service-Specific Exceptions

Every service must have its own exception:

```python
# exceptions.py
class ProjectError(Exception):
    def __init__(self, message, humans=False, **extras):
        if humans:
            message = message.title()
        super().__init__(message)
        self.humans = humans
        self.message = message
        self.extras = extras


class NotificationServiceError(ProjectError):
    ...


# services/notification.py
import logging

logger = logging.getLogger('project.NotificationService')


class NotificationService:
    def send(self, recipient, message):
        try:
            response = ExternalAPI.send(recipient, message)
        except ExternalAPIError as exc:
            logger.exception('Failed to send notification')
            raise NotificationServiceError('Notification failed') from exc
        return response
```

---

### Django Project Structure

```
core/
    admin/
        __init__.py
        user.py
    fixtures/
        core.user.json
    forms/
        __init__.py
        user.py
    management/
        __init__.py
        commands/
            create_foo.py
    migrations/
    models/
        __init__.py
        user.py
    services/
        __init__.py
        notification.py
    signals/
        __init__.py
        user.py
    tasks/
        __init__.py
        notification.py
    templates/
        auth/
            signin.html
    views/
        __init__.py
        auth/
            __init__.py
            login.py
    checks.py
    storage.py
```

---

### AppConfig Example

```python
# pylint: disable=W0611,C0415
# ruff: noqa: F401,PLC0415
from django.apps import AppConfig
from django.conf import settings


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        from .signals import user_signals
        from .tasks import notification_tasks

        if settings.DEBUG:
            from .checks import check_environment_variables, check_models
```

---

### Model Rules

#### Basic Structure

```python
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _


class PostManager(models.Manager):
    def get_by_natural_key(self, author_email, title):
        author = get_user_model().objects.get_by_natural_key(author_email)
        return self.get(author=author, title=title)


class Post(models.Model):
    # 1. Field declarations
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('created at'),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('updated at'),
    )
    title = models.CharField(
        max_length=255,
        verbose_name=_('title'),
    )
    body = models.TextField(
        blank=True,
        verbose_name=_('body'),
    )
    author = models.ForeignKey(
        to=get_user_model(),
        related_name='posts',
        related_query_name='post',
        on_delete=models.CASCADE,
        verbose_name=_('author'),
    )

    # 2. Custom managers
    objects = PostManager()

    # 3. Class Meta
    class Meta:
        app_label = 'core'
        db_table = 'post'
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')

    # 4. __str__
    def __str__(self):
        return f'{self.title}'

    # 5. save (if needed)

    # 6. natural_key
    def natural_key(self):
        return (self.author.email, self.title)

    natural_key.dependencies = ['auth.user']

    # 7. get_absolute_url (if needed)
```

#### Model Method Order

1. Field declarations
2. Custom managers
3. `class Meta`
4. `__str__`
5. `save`
6. `natural_key`
7. `get_absolute_url`

#### Model Checklist

| Requirement | Example |
|-------------|---------|
| Manager with `get_by_natural_key` | `objects = PostManager()` |
| `class Meta` with required attrs | `app_label`, `db_table`, `verbose_name`, `verbose_name_plural` |
| `natural_key` method | Must match manager's `get_by_natural_key` |
| `verbose_name` on all fields | Use `gettext_lazy`: `verbose_name=_('title')` |
| Choices as callable | `choices=get_language_choices` |
| Relational fields with all kwargs | `to`, `related_name`, `related_query_name`, `on_delete` |

#### Choices

Use callable for choices (allows changes without migration):

```python
def get_language_choices():
    return settings.LANGUAGES


class Page(models.Model):
    language = models.CharField(
        max_length=2,
        choices=get_language_choices,
        verbose_name=_('language'),
    )
```

Or use Django's TextChoices:

```python
class LanguageChoices(models.TextChoices):
    ENGLISH = 'en', _('English')
    TURKISH = 'tr', _('Turkish')
```

Or stdlib Enum:

```python
from enum import StrEnum


class CandidateStatus(StrEnum):
    STARTED = 'started'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'
```

#### Constraints and Indexes

```python
class Meta:
    constraints = [
        models.UniqueConstraint(
            fields=['name', 'owner'],
            condition=models.Q(owner__isnull=False),
            name='uc_org_name_owner',  # uc_<identifier>_<field>
        ),
    ]
    indexes = [
        models.Index(
            fields=['candidate_name'],
            condition=~models.Q(candidate_name=''),
            name='idx_cand_name',  # idx_<identifier>_<field>
        ),
    ]
```

#### File Upload Fields

```python
from django.core.files.storage import FileSystemStorage


def dynamic_file_storage():
    return FileSystemStorage()


def upload_video_path(instance, filename):
    return f'videos/{instance.pk}/{filename}'


class Media(models.Model):
    video = models.FileField(
        upload_to=upload_video_path,
        storage=dynamic_file_storage,
        verbose_name=_('video'),
    )
```

---

### Admin Rules

Admin files live in `<app>/admin/<model>.py`:

```python
from django.contrib import admin

from core.admin.base import BaseModelAdmin
from core.models import Post


@admin.register(Post)
class PostAdmin(BaseModelAdmin):
    list_display = ('title', 'author', 'created_at')
    list_display_links = ('title',)
    search_fields = ('title', 'body')
    ordering = ('-created_at',)

    # Performance for ForeignKey fields
    autocomplete_fields = ('author',)
    list_select_related = ('author',)
```

#### Minimum Admin Properties

- `list_display`
- `list_display_links`
- `search_fields`
- `ordering`

For ForeignKey fields, always add:

- `autocomplete_fields`
- `list_select_related`

---

### View Rules

- Views live in `<app>/views/`
- **Only Class-Based Views** (no function-based views)
- Separate business logic into **service layer**

```python
# ❌ Bad - logic in view
class OrderView(View):
    def post(self, request):
        # 50 lines of business logic here
        ...


# ✅ Good - logic in service
class OrderView(View):
    def post(self, request):
        form = self.get_form()
        if not form.is_valid():
            return self.form_invalid(form)

        service = OrderService(
            request=request,
            form=form,
            logger=self.logger,
        )
        redirect_url = service.process_order()
        return HttpResponseRedirect(redirect_url)
```

---

### Internationalization

Never use hardcoded strings:

```python
# ❌ Bad
return HttpResponse('Error')

# ✅ Good
from django.utils.translation import gettext_lazy as _

return HttpResponse(_('Error'))
```

In templates:

```html
{% load i18n %}

{% translate "Welcome" %}

{% blocktranslate with name=user.name %}
Hello, {{ name }}!
{% endblocktranslate %}
```

---

### Celery Tasks

Tasks live in `<app>/tasks/`:

```python
# tasks/notification.py
from celery import shared_task

from core.services.notification import NotificationService, NotificationServiceError


@shared_task(
    bind=True,
    max_retries=3,
    default_retry_delay=60,
)
def send_notification_task(self, user_id, message):
    try:
        service = NotificationService()
        service.send(user_id, message)
    except NotificationServiceError as exc:
        self.retry(exc=exc)
```

Register in AppConfig.ready():

```python
def ready(self):
    from .tasks import notification  # noqa: F401
```

---

### Testing

Tests live in `tests/` directory:

```
tests/
    test_models_post.py
    test_views_auth.py
    test_services_notification.py
    test_forms_user.py
    test_tasks_notification.py
```

Naming convention: `test_<type>_<name>.py`

Use stdlib and Django's test suites:

```python
from django.test import TestCase


class PostModelTest(TestCase):
    def test_str_returns_title(self):
        post = Post(title='Hello')
        self.assertEqual(str(post), 'Hello')
```

---

### Django System Checks

Create `checks.py` for custom checks:

```python
# pylint: disable=W0613
# ruff: noqa: ARG001,SLF001
import ast
import inspect
import os

import django.apps
from django.core import checks
from django.core.exceptions import FieldDoesNotExist

DEVELOPMENT_ENVIRONMENT_VARIABLES = [
    'DJANGO_SECRET_KEY',
    'DATABASE_URL',
    # other required environment variable name
]

FIELD_VERBOSE_NAME_WHITE_LIST = ['slug']
# MODEL_NAME_WHITE_LIST = [foomodel']


@checks.register()
def check_environment_variables(app_configs, **kwargs):
    errors = []
    for var_name in DEVELOPMENT_ENVIRONMENT_VARIABLES:
        if not os.environ.get(var_name):
            errors = [
                *errors,
                checks.Error(
                    f'Missing environment variable for development: {var_name}',
                    hint=f'Set the "{var_name}" environment variable in your environment.',
                    id='core.ENV001',
                ),
            ]
    return errors


def check_model_get_argument(node, arg):
    for kw in node.value.keywords:
        if kw.arg == arg:
            return kw
    return None


def check_model_is_gettext_node(node):
    if not isinstance(node, ast.Call):
        return False

    return node.func.id == '_'


def check_model_get_field(model, node):
    if not isinstance(node, ast.Assign):
        return None
    if len(node.targets) != 1:
        return None
    if not isinstance(node.targets[0], ast.Name):
        return None
    try:
        return model._meta.get_field(node.targets[0].id)
    except FieldDoesNotExist:
        return None


def check_model_fields_verbose_name(field, node):
    verbose_name = check_model_get_argument(node, 'verbose_name')
    if field.name not in FIELD_VERBOSE_NAME_WHITE_LIST:
        if verbose_name is None:
            yield checks.Warning(
                'Field has no verbose name',
                hint='Set verbose name on the field.',
                obj=field,
                id='BLT001',
            )
        elif not check_model_is_gettext_node(verbose_name.value):
            yield checks.Warning(
                'Verbose name should use gettext _() style',
                hint='Use gettext on the verbose name.',
                obj=field,
                id='BLT002',
            )


def check_model_class_meta(class_meta, model):
    if class_meta is None:
        yield checks.Warning(
            f'Model "{model._meta.model_name}" must define class Meta',
            hint=f'Add class Meta to model "{model._meta.model_name}".',
            obj=model,
            id='BLT003',
        )
    else:
        verbose_name = None
        verbose_name_plural = None

        for node in ast.iter_child_nodes(class_meta):
            if not isinstance(node, ast.Assign):
                continue

            if not isinstance(node.targets[0], ast.Name):
                continue

            attr = node.targets[0].id

            if attr == 'verbose_name':
                verbose_name = node

            if attr == 'verbose_name_plural':
                verbose_name_plural = node

        if verbose_name is None:
            yield checks.Warning(
                'Model has no verbose name',
                hint='Add verbose_name to class Meta.',
                obj=model,
                id='BLT004',
            )

        elif not check_model_is_gettext_node(verbose_name.value):
            yield checks.Warning(
                'Verbose name in class Meta should use gettext',
                hint=f'Use gettext on the verbose_name of class Meta "{model._meta.model_name}".',
                obj=model,
                id='BLT002',
            )

        if verbose_name_plural is None:
            yield checks.Warning(
                'Model has no verbose name plural',
                hint='Add verbose_name_plural to class Meta.',
                obj=model,
                id='BLT005',
            )

        elif not check_model_is_gettext_node(verbose_name_plural.value):
            yield checks.Warning(
                'Verbose name plural in class Meta should use gettext',
                hint=f'Use gettext on the verbose_name_plural of class Meta "{model._meta.model_name}".',
                obj=model,
                id='BLT002',
            )


def check_model(model):
    """

    BLT001: Field has no verbose name.
    BLT002: Verbose name should use gettext.
    BLT003: Model must define class Meta.
    BLT004: Model has no verbose name.
    BLT005: Model has no verbose name plural.

    """
    if model._meta.model_name not in MODEL_NAME_WHITE_LIST:
        model_source = inspect.getsource(model)
        model_node = ast.parse(model_source)
        class_meta = None
        for node in model_node.body[0].body:
            if isinstance(node, ast.ClassDef) and node.name == 'Meta':
                class_meta = node

            field = check_model_get_field(model, node)
            if field is None:
                continue

            yield from check_model_fields_verbose_name(field, node)

        yield from check_model_class_meta(class_meta, model)


@checks.register(checks.Tags.models)
def check_models(app_configs, **kwargs):
    errors = []
    for app in django.apps.apps.get_app_configs():
        if app.path.find('site-packages') > -1:
            continue

        for model in app.get_models():
            for check_message in check_model(model):
                errors = [*errors, check_message]
    return errors
```

---

### Pre-Commit Hooks

```bash
brew install pre-commit
pre-commit install
```

Minimal `.pre-commit-config.yaml`:

```yaml
exclude: core/migrations/
fail_fast: true
repos:
  - repo: local
    hooks:
      - id: django-check
        name: Django checks
        entry: scripts/pre-commit/django-check.bash
        language: script
        always_run: true
        pass_filenames: false

      - id: ruff
        name: Ruff linter
        entry: ruff check .
        language: system
        types: [python]

      - id: pylint
        name: Pylint check
        entry: pylint -rn -sn -d R0401 config core
        language: system
        types: [python]

      - id: django-test
        name: Django tests
        entry: scripts/pre-commit/run-tests.bash
        language: system
        types: [python]
        pass_filenames: false
```

`scripts/pre-commit/django-check.bash`:

```bash
#!/usr/bin/env bash
set -euo pipefail

DJANGO_ENV=production python manage.py check --deploy || exit 0
```

`scripts/pre-commit/run-tests.bash`:

```bash
#!/usr/bin/env bash
set -euo pipefail

coverage run manage.py test --failfast
```

---

### Commit Messages

Format:

```
[claude]: <verb> <description in lowercase>

- Detail 1
- Detail 2

Fixes #123

🤖 Generated with [Claude Code](https://claude.ai/code)
Co-Authored-By: Claude <noreply@anthropic.com>
```

Example:

```
[claude]: add user notification service

- Implement NotificationService with retry logic
- Add NotificationServiceError for error handling
- Create Celery task for async notifications

Fixes #42

🤖 Generated with [Claude Code](https://claude.ai/code)
Co-Authored-By: Claude <noreply@anthropic.com>
```

---

## Quick Reference

| Task | Command |
|------|---------|
| Check Python version | `python --version` |
| Run linter | `ruff check .` |
| Format code | `ruff format .` |
| Run pylint | `pylint config core` |
| Run tests | `python manage.py test` |
| Run with coverage | `coverage run manage.py test` |
| Django check | `python manage.py check` |
| Django check deploy | `python manage.py check --deploy` |
| Make migrations | `python manage.py makemigrations` |
| Apply migrations | `python manage.py migrate` |

---

## Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [Pylint Documentation](https://pylint.readthedocs.io/)
- [Celery Documentation](https://docs.celeryq.dev/)
