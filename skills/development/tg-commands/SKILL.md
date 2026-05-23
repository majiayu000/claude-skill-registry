---
name: tg-commands
description: Django management command patterns for the World of Darkness application. Use when creating custom management commands for data validation, monitoring, batch processing, or maintenance tasks. Triggers on command creation, validation tools, data integrity checks, or scheduled tasks.
---

# Management Command Patterns

## Command Structure

### Basic Command Template

```python
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = "Description of what this command does"

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('chronicle_id', type=int)

        # Optional arguments
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Show detailed output',
        )
        parser.add_argument(
            '--limit',
            type=int,
            default=100,
            help='Maximum records to process (default: 100)',
        )

    def handle(self, *args, **options):
        verbose = options['verbose']
        chronicle_id = options['chronicle_id']

        try:
            # Command logic here
            self.stdout.write(self.style.SUCCESS('Command completed'))
        except Exception as e:
            raise CommandError(f'Command failed: {e}')
```

### Output Styling

```python
# Success (green)
self.stdout.write(self.style.SUCCESS('Operation successful'))

# Error (red)
self.stdout.write(self.style.ERROR('Something failed'))

# Warning (yellow)
self.stdout.write(self.style.WARNING('Potential issue'))

# Notice (cyan)
self.stdout.write(self.style.NOTICE('Information'))

# Standard output
self.stdout.write('Regular message')

# Verbose output (respect verbosity setting)
if options['verbosity'] >= 2:
    self.stdout.write('Debug details...')
```

## Data Validation Command

### Pattern: validate_data_integrity

```python
from django.core.management.base import BaseCommand
from django.db import transaction

class Command(BaseCommand):
    help = "Validate data integrity across models"

    def add_arguments(self, parser):
        parser.add_argument(
            '--fix',
            action='store_true',
            help='Attempt to fix issues automatically',
        )
        parser.add_argument(
            '--model',
            type=str,
            help='Validate specific model only',
        )

    def handle(self, *args, **options):
        fix_mode = options['fix']
        issues = []

        # Run validators
        issues.extend(self.validate_characters(fix_mode))
        issues.extend(self.validate_chronicles(fix_mode))
        issues.extend(self.validate_orphans(fix_mode))

        # Report results
        if issues:
            self.stdout.write(self.style.WARNING(f'Found {len(issues)} issues'))
            for issue in issues:
                self.stdout.write(f"  - {issue}")
        else:
            self.stdout.write(self.style.SUCCESS('No issues found'))

    def validate_characters(self, fix_mode):
        """Check character data consistency."""
        issues = []
        from characters.models import Character

        # Check for characters without owners
        orphans = Character.objects.filter(owner__isnull=True)
        for char in orphans:
            issues.append(f"Character {char.id} has no owner")
            if fix_mode:
                char.delete()
                self.stdout.write(f"  Fixed: Deleted orphan character {char.id}")

        return issues

    def validate_chronicles(self, fix_mode):
        """Check chronicle consistency."""
        issues = []
        # Add validation logic
        return issues

    def validate_orphans(self, fix_mode):
        """Check for orphaned related objects."""
        issues = []
        # Add orphan detection logic
        return issues
```

## Monitoring Command

### Pattern: monitor_validation

```python
import json
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone

class Command(BaseCommand):
    help = "Monitor validation status for alerting"

    def add_arguments(self, parser):
        parser.add_argument(
            '--json',
            action='store_true',
            help='Output in JSON format for monitoring tools',
        )
        parser.add_argument(
            '--period',
            type=int,
            default=24,
            help='Analysis period in hours (default: 24)',
        )

    def handle(self, *args, **options):
        period = timedelta(hours=options['period'])
        since = timezone.now() - period

        stats = self.collect_stats(since)

        if options['json']:
            self.stdout.write(json.dumps(stats, indent=2, default=str))
        else:
            self.print_report(stats)

    def collect_stats(self, since):
        """Collect validation statistics."""
        from characters.models import Character
        from chronicles.models import Chronicle

        return {
            'timestamp': timezone.now().isoformat(),
            'period_hours': 24,
            'characters': {
                'total': Character.objects.count(),
                'created_recently': Character.objects.filter(created__gte=since).count(),
                'modified_recently': Character.objects.filter(modified__gte=since).count(),
            },
            'chronicles': {
                'total': Chronicle.objects.count(),
                'active': Chronicle.objects.filter(end_date__isnull=True).count(),
            },
            'health': 'OK',
        }

    def print_report(self, stats):
        """Print human-readable report."""
        self.stdout.write(self.style.NOTICE('=== Validation Monitor ==='))
        self.stdout.write(f"Timestamp: {stats['timestamp']}")
        self.stdout.write(f"Characters: {stats['characters']['total']}")
        self.stdout.write(f"  Created (24h): {stats['characters']['created_recently']}")
        self.stdout.write(f"Chronicles: {stats['chronicles']['total']}")
        self.stdout.write(self.style.SUCCESS(f"Health: {stats['health']}"))
```

## Batch Processing Command

### Pattern: Process in Batches

```python
from django.core.management.base import BaseCommand
from django.db import transaction

class Command(BaseCommand):
    help = "Process records in batches"

    def add_arguments(self, parser):
        parser.add_argument(
            '--batch-size',
            type=int,
            default=1000,
            help='Records per batch (default: 1000)',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be done without making changes',
        )

    def handle(self, *args, **options):
        batch_size = options['batch_size']
        dry_run = options['dry_run']

        from characters.models import Character
        queryset = Character.objects.filter(needs_processing=True)
        total = queryset.count()

        if dry_run:
            self.stdout.write(f"Would process {total} records")
            return

        processed = 0
        for batch in self.batch_iterator(queryset, batch_size):
            with transaction.atomic():
                for obj in batch:
                    self.process_record(obj)
                    processed += 1

            self.stdout.write(f"Processed {processed}/{total}")

        self.stdout.write(self.style.SUCCESS(f'Completed: {processed} records'))

    def batch_iterator(self, queryset, batch_size):
        """Yield batches from queryset."""
        start = 0
        while True:
            batch = list(queryset[start:start + batch_size])
            if not batch:
                break
            yield batch
            start += batch_size

    def process_record(self, obj):
        """Process a single record."""
        obj.needs_processing = False
        obj.save(update_fields=['needs_processing'])
```

## Interactive Command

### Pattern: Confirmation and Progress

```python
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Dangerous operation requiring confirmation"

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Skip confirmation prompt',
        )

    def handle(self, *args, **options):
        if not options['force']:
            confirm = input('This will delete data. Continue? [y/N]: ')
            if confirm.lower() != 'y':
                self.stdout.write('Cancelled.')
                return

        # Show progress
        from characters.models import Character
        total = Character.objects.count()

        for i, char in enumerate(Character.objects.iterator(), 1):
            self.process(char)
            if i % 100 == 0:
                self.stdout.write(f'\rProcessed {i}/{total}', ending='')
                self.stdout.flush()

        self.stdout.write('')  # Newline
        self.stdout.write(self.style.SUCCESS('Complete'))
```

## Command Testing

### Test Pattern

```python
from io import StringIO
from django.core.management import call_command
from django.test import TestCase

class CommandTestCase(TestCase):
    def test_validate_command(self):
        out = StringIO()
        call_command('validate_data_integrity', stdout=out)
        output = out.getvalue()
        self.assertIn('No issues found', output)

    def test_command_with_options(self):
        out = StringIO()
        call_command(
            'validate_data_integrity',
            '--fix',
            '--verbose',
            stdout=out
        )
        output = out.getvalue()
        self.assertIn('SUCCESS', output)

    def test_command_error_handling(self):
        err = StringIO()
        with self.assertRaises(SystemExit):
            call_command('mycommand', '--invalid', stderr=err)
```

## File Location

Commands go in:
```
app_name/
└── management/
    ├── __init__.py
    └── commands/
        ├── __init__.py
        └── command_name.py
```

## Common Command Types

| Command Type | Purpose | Example |
|-------------|---------|---------|
| Validation | Check data integrity | `validate_data_integrity` |
| Monitoring | Health checks for alerts | `monitor_validation` |
| Batch processing | Update many records | `recalculate_xp` |
| Maintenance | Cleanup, archive | `archive_old_scenes` |
| Import/Export | Data migration | `import_characters` |
| Development | Testing helpers | `create_test_data` |
