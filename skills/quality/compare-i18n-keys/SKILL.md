---
name: compare-i18n-keys
description: Compare translation keys between legacy Angular translate pipe and new Transloco t() function. Use when migrating i18n keys from old codebase to new codebase, or when the user asks to compare/fix translation keys.
---

Compare translation keys between legacy Angular `translate` pipe and new Transloco `t()` function, then fix the new project.

## Arguments

- `$ARGUMENTS` - Format: `--from <source_path> --to <target_path>`
  - `--from`: Source HTML file in old project
  - `--to`: Target HTML file in new project

## Process

### Step 1: Extract Keys from Source (Legacy Angular)

Read the source file and extract translation keys using these patterns:

**Pattern 1: Basic translate pipe**
```
{{ 'key' | translate }}
```

**Pattern 2: Translate pipe with parameters**
```
{{ 'key' | translate: { param: value } }}
```

**Pattern 3: Translate in attribute**
```
placeholder="{{ 'key' | translate }}"
label="{{ 'key' | translate }}"
matTooltip="{{ 'key' | translate }}"
```

### Step 2: Extract Keys from Target (Transloco)

Read the target file and extract translation keys using these patterns:

**Pattern 1: Basic t() function**
```
{{ t('key') }}
t('key')
```

**Pattern 2: t() in attribute binding**
```
[label]="t('key')"
[placeholder]="t('key')"
[matTooltip]="t('key')"
```

### Step 3: Compare and Generate Report

Create a comparison report with:

| Category | Description |
|----------|-------------|
| **OK** | Key matches exactly |
| **DIFFERENT** | Key exists but different (may be intentional) |
| **MISSING** | Source key not found in target |
| **EXTRA** | Target key not in source (informational) |

### Step 4: Output Report

```markdown
# i18n Key Comparison Report

**Source:** {from_path}
**Target:** {to_path}

## Summary

| Category | Count |
|----------|-------|
| Matching Keys | X |
| Different Keys | Y |
| Missing Keys | Z |

**Match Rate: XX%**

## Missing Keys (Need Fix)

| Source Key | Context |
|------------|---------|
| `key.name` | Where it's used |

## Different Keys (Review)

| Source Key | Target Key |
|------------|------------|
| `old.key` | `new.key` |
```

### Step 5: Apply Fixes

If user confirms, fix the target file by replacing incorrect keys with correct ones from source.

## Usage

```bash
/compare-i18n-keys --from=/path/to/legacy/component.html --to=/path/to/new/component.html
```
