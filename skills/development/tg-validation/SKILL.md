---
name: tg-validation
description: Data validation patterns for the World of Darkness Django application including database constraints, model validators, and atomic transactions. Use when implementing XP/freebie spending transactions, adding database constraints to models, writing clean() validation methods, or ensuring data integrity for character stats.
---

# Data Validation Patterns

This skill provides validation patterns for ensuring data integrity across the WoD application.

## When to Use This Skill

- Adding `@transaction.atomic` to multi-step operations (XP spending, freebie allocation)
- Adding `CheckConstraint` to model Meta classes
- Writing `clean()` methods for cross-field validation
- Adding field validators (`MinValueValidator`, `MaxValueValidator`)
- Writing tests for validation logic

## Quick Reference

### Transaction Pattern (XP/Freebie Operations)

```python
from django.db import transaction
from django.core.exceptions import ValidationError

class Character(Model):
    @transaction.atomic
    def spend_xp(self, trait_name, cost, category):
        # Lock row for concurrent access
        char = Character.objects.select_for_update().get(pk=self.pk)
        
        if char.xp < cost:
            raise ValidationError(f"Insufficient XP: need {cost}, have {char.xp}")
        
        char.xp -= cost
        char.spent_xp.append({...})
        char.save(update_fields=['xp', 'spent_xp'])
```

### Database Constraint Pattern

```python
from django.db.models import CheckConstraint, Q

class Character(Model):
    class Meta:
        constraints = [
            CheckConstraint(
                check=Q(xp__gte=0),
                name='%(app_label)s_%(class)s_xp_non_negative',
                violation_error_message="XP cannot be negative"
            ),
        ]
```

### Model Validation Pattern

```python
class Human(Character):
    def clean(self):
        super().clean()
        if self.temporary_willpower > self.willpower:
            raise ValidationError({
                'temporary_willpower': f"Cannot exceed permanent willpower ({self.willpower})"
            })
```

### Field Validator Pattern

```python
from django.core.validators import MinValueValidator, MaxValueValidator

class AttributeBlock(models.Model):
    strength = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
```

## Detailed Patterns

For detailed implementation patterns including:
- Full XP spending transaction implementation
- Scene XP award transactions
- All attribute/ability constraints
- Status state machine validation
- JSON schema validation for spent_xp
- Migration strategies for adding constraints

See [references/validation-patterns.md](references/validation-patterns.md)

## Priority Guidelines

| Priority | What to Validate | Pattern |
|----------|-----------------|---------|
| CRITICAL | XP/freebie operations | `@transaction.atomic` + `select_for_update()` |
| HIGH | Numeric ranges (1-10, 0-5) | `CheckConstraint` + Field validators |
| MEDIUM | Cross-field rules | `clean()` method |
| LOW | JSON structure | JSON schema validation |

## Testing Validation

```python
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError

class TestCharacterValidation(TestCase):
    def test_xp_cannot_be_negative_db_constraint(self):
        character.xp = -100
        with self.assertRaises(IntegrityError):
            character.save()

    def test_xp_cannot_be_negative_model_validation(self):
        character.xp = -100
        with self.assertRaises(ValidationError):
            character.full_clean()
```
