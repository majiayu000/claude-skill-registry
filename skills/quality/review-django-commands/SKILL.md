---
name: review-django-commands
description: Review Django management commands for proper structure and refactor if needed
argument-hint: [<app-path>] [--fix] [--verbose]
---

# review-django-commands

**Category**: Django Development

## Usage

```bash
/review-django-commands [<app-path>] [--fix] [--verbose]
```

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `<app-path>` | No | Path to Django app or project (default: current directory) |
| `--fix` | No | Automatically refactor non-compliant commands |
| `--verbose` | No | Show detailed analysis for each command |

## Purpose

Review Django management commands to ensure they follow the thin-command/service-layer pattern:

1. **Scans** all management commands in the project
2. **Analyzes** command structure for anti-patterns
3. **Reports** compliance with best practices
4. **Refactors** non-compliant commands (with `--fix`)

## Best Practice Pattern

Commands should be thin wrappers that delegate to services:

```
apps/{app}/
├── management/
│   └── commands/
│       └── {command_name}.py    # Thin: parse args, call service, format output
└── services/
    └── {domain}.py              # Fat: business logic, DB operations
```

### Good Pattern

```python
# management/commands/publish_scheduled.py
class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--dry-run", action="store_true")

    def handle(self, *args, **options):
        result = publish_scheduled_articles(dry_run=options["dry_run"])
        self.stdout.write(self.style.SUCCESS(f"Published {result.count} articles"))
```

```python
# services/publishing.py
def publish_scheduled_articles(dry_run: bool = False) -> PublishResult:
    """Business logic lives here - testable without command scaffolding."""
    ...
```

### Anti-Patterns to Detect

| Anti-Pattern | Description | Severity |
|--------------|-------------|----------|
| Fat commands | Business logic in `handle()` | HIGH |
| Direct ORM queries | Complex querysets in command | HIGH |
| Missing service layer | No corresponding service file | MEDIUM |
| No type hints | Missing return types, parameters | LOW |
| No docstrings | Missing command help text | LOW |
| Hardcoded values | Magic numbers/strings in logic | MEDIUM |

---

## Execution Instructions for Claude Code

When this command is run, Claude Code should:

### 1. Parse Arguments

```
APP_PATH = first positional argument or "."
FIX_MODE = true if --fix specified
VERBOSE = true if --verbose specified
```

### 2. Find Management Commands

Scan for management command files:

```bash
find "$APP_PATH" -path "*/management/commands/*.py" -not -name "__init__.py"
```

### 3. Analyze Each Command

For each command file, analyze:

#### 3.1 Command Structure Check

```python
CHECKS = {
    "thin_handle": {
        "description": "handle() delegates to service",
        "severity": "HIGH",
        "check": "handle method < 30 lines, calls external function"
    },
    "no_orm_in_handle": {
        "description": "No direct ORM queries in handle()",
        "severity": "HIGH",
        "check": "No Model.objects.* calls in handle()"
    },
    "service_exists": {
        "description": "Corresponding service file exists",
        "severity": "MEDIUM",
        "check": "services/{domain}.py exists in same app"
    },
    "type_hints": {
        "description": "Methods have type hints",
        "severity": "LOW",
        "check": "handle() has return type annotation"
    },
    "has_help": {
        "description": "Command has help text",
        "severity": "LOW",
        "check": "help attribute or docstring defined"
    },
    "no_hardcoded": {
        "description": "No hardcoded values in logic",
        "severity": "MEDIUM",
        "check": "No magic numbers/strings in handle()"
    }
}
```

#### 3.2 Complexity Metrics

Calculate:
- Lines of code in `handle()` method
- Number of ORM calls
- Cyclomatic complexity (if/for/while count)
- Number of external function calls

### 4. Report Results

#### Default Output

```
Django Command Review
=====================

Project: ./apps
Commands found: 5

Results:
  apps/blog/management/commands/publish_scheduled.py: PASS
  apps/blog/management/commands/cleanup_drafts.py: FAIL
    - [HIGH] Fat command: handle() has 85 lines, should be < 30
    - [HIGH] Direct ORM: 3 Model.objects.* calls in handle()
    - [MEDIUM] No service: services/drafts.py not found
  apps/users/management/commands/sync_users.py: WARN
    - [LOW] No type hints on handle()
    - [LOW] Missing help text
  apps/orders/management/commands/process_orders.py: FAIL
    - [HIGH] Fat command: handle() has 120 lines
    - [HIGH] Direct ORM: 8 Model.objects.* calls
    - [MEDIUM] Hardcoded values: found 3 magic numbers

Summary:
  Passed: 2/5
  Warnings: 1/5
  Failed: 2/5

Run with --fix to refactor non-compliant commands.
```

#### Verbose Output (--verbose)

```
Django Command Review
=====================

=== apps/blog/management/commands/cleanup_drafts.py ===

Current Structure:
  handle() lines: 85
  ORM calls: 3
  Complexity: 12
  External calls: 0

Issues:
  [HIGH] Fat command
    Line 25-110: Business logic should move to service

  [HIGH] Direct ORM queries
    Line 32: Draft.objects.filter(status='draft', created_at__lt=cutoff)
    Line 45: Draft.objects.exclude(author__is_active=True)
    Line 78: draft.delete()

  [MEDIUM] No service layer
    Expected: apps/blog/services/drafts.py

Recommended Refactoring:
  1. Create apps/blog/services/drafts.py
  2. Move lines 25-110 to cleanup_old_drafts() function
  3. Command should only: parse args, call service, format output

...
```

### 5. Fix Mode (--fix)

If `--fix` is specified for failing commands:

#### 5.1 Create Service File

```python
# apps/blog/services/drafts.py
from dataclasses import dataclass
from django.utils import timezone
from apps.blog.models import Draft


@dataclass
class CleanupResult:
    deleted_count: int
    skipped_ids: list[int]


def cleanup_old_drafts(days: int = 30, dry_run: bool = False) -> CleanupResult:
    """
    Delete drafts older than specified days.

    Business logic extracted from management command.
    """
    cutoff = timezone.now() - timezone.timedelta(days=days)
    drafts = Draft.objects.filter(
        status='draft',
        created_at__lt=cutoff,
    ).exclude(author__is_active=True)

    if dry_run:
        return CleanupResult(deleted_count=drafts.count(), skipped_ids=[])

    deleted = 0
    skipped = []
    for draft in drafts:
        try:
            draft.delete()
            deleted += 1
        except Exception:
            skipped.append(draft.id)

    return CleanupResult(deleted_count=deleted, skipped_ids=skipped)
```

#### 5.2 Refactor Command

```python
# apps/blog/management/commands/cleanup_drafts.py
from django.core.management.base import BaseCommand
from apps.blog.services.drafts import cleanup_old_drafts


class Command(BaseCommand):
    help = "Delete old draft articles that haven't been published"

    def add_arguments(self, parser):
        parser.add_argument(
            "--days",
            type=int,
            default=30,
            help="Delete drafts older than this many days (default: 30)",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be deleted without making changes",
        )

    def handle(self, *args, **options) -> None:
        days = options["days"]
        dry_run = options["dry_run"]

        if dry_run:
            self.stdout.write(self.style.WARNING("DRY RUN - no changes will be made"))

        result = cleanup_old_drafts(days=days, dry_run=dry_run)

        if result.skipped_ids:
            self.stderr.write(
                self.style.ERROR(f"Failed to delete: {result.skipped_ids}")
            )

        self.stdout.write(
            self.style.SUCCESS(f"Deleted {result.deleted_count} drafts")
        )
```

#### 5.3 Report Fixes

```
Refactoring non-compliant commands...

apps/blog/management/commands/cleanup_drafts.py:
  Created: apps/blog/services/drafts.py
  Backup: cleanup_drafts.py.backup
  Refactored: cleanup_drafts.py
  Status: FIXED

apps/orders/management/commands/process_orders.py:
  Created: apps/orders/services/orders.py
  Backup: process_orders.py.backup
  Refactored: process_orders.py
  Status: FIXED

Fixed: 2 commands
Re-run to verify: /review-django-commands
```

### 6. Exit Codes

- `0`: All commands compliant
- `1`: Some commands need refactoring (and --fix not specified)
- `2`: No management commands found

---

## Examples

```bash
# Review all commands in current project
/review-django-commands

# Review specific app
/review-django-commands apps/blog

# Detailed analysis
/review-django-commands --verbose

# Auto-refactor non-compliant commands
/review-django-commands --fix

# Review and fix specific app
/review-django-commands apps/orders --fix --verbose
```

## Service Layer Guidelines

When refactoring commands, services should:

| Aspect | Guideline |
|--------|-----------|
| **Location** | `apps/{app}/services/{domain}.py` |
| **Return type** | Use `@dataclass` for complex results |
| **Parameters** | Accept primitive types, not Django request/options |
| **Side effects** | Clearly document any side effects |
| **Testability** | No command scaffolding required to test |
| **Reusability** | Callable from views, tasks, other commands |

## Related Skills

| Skill | Purpose |
|-------|---------|
| `python-experts:django-dev` | Django management command patterns |
| `python-experts:python-style` | Python coding standards |
| `python-experts:python-testing-expert` | Testing service functions |

## Related Commands

| Command | Purpose |
|---------|---------|
| `/parallel-ready-django` | Check Django project for parallel development |
| `/parallel-fix-django` | Fix Django blockers for parallelization |
