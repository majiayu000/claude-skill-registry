---
name: form-extraction
description: Extract and analyze Angular Reactive Forms from source code for migration comparison and validation. Use when comparing forms between legacy and migrated code.
---

# Form Extraction Skill

Extract and analyze Angular Reactive Forms from source code for migration comparison and validation.

## Quick Commands

### Extract Form Controls

```bash
# From HTML - formControlName
grep -oE 'formControlName="[^"]+"' {path}/**/*.html | sort -u

# From HTML - formGroupName
grep -oE 'formGroupName="[^"]+"' {path}/**/*.html | sort -u

# From TypeScript - form definitions
grep -E '(this\.fb\.group|this\.#fb\.group|this\.fb\.nonNullable\.group|new FormGroup|new UntypedFormGroup)' {path}/**/*.ts
```

### Extract Validators

```bash
# Angular Validators (old)
grep -oE 'Validators\.(required|email|minLength|maxLength|min|max|pattern|nullValidator)(\([^)]*\))?' {path}/**/*.ts | sort -u

# OneValidators (new)
grep -oE 'OneValidators\.[a-zA-Z]+(\([^)]*\))?' {path}/**/*.ts | sort -u

# Custom validators
grep -oE '#?[a-zA-Z]+Validator\b' {path}/**/*.ts | sort -u
```

## Form Definition Patterns

| Pattern | Example |
| ------- | ------- |
| FormBuilder | `this.fb.group({ ... })` |
| Private FB | `this.#fb.group({ ... })` |
| NonNullable | `this.fb.nonNullable.group({ ... })` |
| Direct | `new FormGroup({ ... })` |
| Untyped | `new UntypedFormGroup({ ... })` |

## Validator Patterns

| Pattern | Example |
| ------- | ------- |
| Array syntax | `controlName: ['', [Validators.required]]` |
| Object syntax | `controlName: this.fb.control('', { validators: [...] })` |
| Group-level | `this.fb.group({...}, { validators: [...] })` |
| Async | `controlName: ['', [], [asyncValidator]]` |

## Validator Mapping (Old → New)

| Old (Validators) | New (OneValidators) |
| ---------------- | ------------------- |
| `Validators.required` | `OneValidators.required` |
| `Validators.email` | `OneValidators.email` |
| `Validators.minLength(n)` | `OneValidators.minLength(n)` |
| `Validators.maxLength(n)` | `OneValidators.maxLength(n)` |
| `Validators.min(n)` | `OneValidators.range(min, max)` |
| `Validators.max(n)` | `OneValidators.range(min, max)` |
| `Validators.pattern(x)` | `OneValidators.pattern(x)` |

## Error Display Patterns

### Validators with Built-in Messages (use `oneUiFormError` directly)

These validators have i18n messages built-in, use simple pattern:

```html
<mat-error oneUiFormError="fieldName"></mat-error>
```

| Validator | Built-in Message Key |
| --------- | -------------------- |
| `required` | `validators.required` |
| `minLength` | `validators.require_min_length` |
| `maxLength` | `validators.invalid_max_length` |
| `range` | `validators.invalid_range` |
| `rangeLength` | `validators.invalid_range` |
| `email` | `validators.invalid_email` |

### All Other Validators (MUST use `@if/@else`)

**All validators NOT in the list above** need explicit error handling with custom messages:

```html
@if (ctrl.hasError('pattern')) {
  <mat-error>{{ t('validators.your_custom_pattern_message') }}</mat-error>
} @else if (ctrl.hasError('duplicate')) {
  <mat-error>{{ t('validators.duplicate_xxx') }}</mat-error>
} @else {
  <mat-error oneUiFormError="fieldName"></mat-error>
}
```

| Validator | Reason |
| --------- | ------ |
| `pattern` | Generic message `validators.invalid`, need specific message |
| `duplicate` | Default `validators.duplicate`, often need context-specific message |
| Custom validators | No built-in message |
| Any other validator | Not in the 6 basic validators list |

## References

- Detailed patterns: `rules/tools/forms/patterns.md`
