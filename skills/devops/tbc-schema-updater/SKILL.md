---
name: TBC Schema Updater
description: This skill should be used when the user asks to "update TBC schemas", "regenerate schemas from kicker", "sync schemas with new TBC version", "extract schemas from kicker-aggregated.json", "update template schemas", or mentions "schema update", "schema regeneration", "kicker update", or "new TBC release".
version: 1.1.0
---

# TBC Schema Updater

This skill manages the extraction and regeneration of JSON schemas from the TBC Kicker source, keeping the validation schemas synchronized with new To-Be-Continuous releases.

## Overview

The TBC Kicker skill uses JSON schemas to validate `.gitlab-ci.yml` inputs against real template variables. When TBC releases new versions with updated variables, features, or templates, regenerate the schemas to keep validation accurate.

## Prerequisites

Before regenerating schemas, ensure the kicker source is available:

```bash
# Clone kicker repository if not present
git clone https://gitlab.com/to-be-continuous/kicker.git /tmp/kicker

# Or update existing clone
cd /tmp/kicker && git pull
```

The source file is located at:
```
/tmp/kicker/src/assets/kicker-aggregated.json
```

## Schema Regeneration Workflow

### Step 1: Verify Source

Check that the kicker source is up to date:

```bash
cd /tmp/kicker
git log -1 --oneline
```

### Step 2: Run Extraction

Execute the extraction script:

```bash
cd /path/to/gitlab-tbc/skills/tbc-kicker
python3 scripts/extract-schemas.py \
  --input /tmp/kicker/src/assets/kicker-aggregated.json \
  --output-dir schemas/
```

### Step 3: Verify Results

Check the generated schemas:

```bash
# Count schemas (should be ~50)
ls schemas/*.json | wc -l

# Verify a specific schema
python3 scripts/validate-inputs.py --list-valid aws
```

### Step 4: Validate Examples

Run validation on existing examples:

```bash
for f in examples/*.yml; do
  python3 scripts/validate-inputs.py "$f"
done
```

## Extraction Script

The `scripts/extract-schemas.py` script handles:

1. **Variable name transformation**: `AWS_CLI_IMAGE` → `cli-image`
2. **Type inference**: string, boolean, enum, number
3. **Feature variables**: Grouped under `x-feature` metadata
4. **Variant variables**: Grouped under `x-variant` metadata
5. **Schema metadata**: prefix, kind, features, variants lists
6. **Component names**: Extracts valid component names from `template_path` (base + variants)

### Script Options

```bash
python3 scripts/extract-schemas.py --help

Options:
  --input, -i     Path to kicker-aggregated.json
  --output-dir, -o   Output directory for schemas
  --template, -t     Extract only a specific template
```

### Single Template Extraction

To extract or update a single template:

```bash
python3 scripts/extract-schemas.py \
  --input /tmp/kicker/src/assets/kicker-aggregated.json \
  --output-dir schemas/ \
  --template python
```

## Schema Format

Each generated schema follows this structure:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Template Name",
  "description": "to-be-continuous/project-path",
  "type": "object",
  "properties": {
    "inputs": {
      "type": "object",
      "properties": {
        "input-name": {
          "type": "string",
          "description": "...",
          "default": "...",
          "x-feature": "Feature Name",
          "x-variant": "Variant Name",
          "x-advanced": true
        }
      },
      "additionalProperties": false
    }
  },
  "_meta": {
    "prefix": "PREFIX_",
    "kind": "build|hosting|analysis",
    "features": ["Feature1", "Feature2"],
    "variants": ["Variant1", "Variant2"],
    "variable_count": 25
  }
}
```

## Handling New Templates

When TBC adds new templates:

1. Run full extraction (new templates auto-discovered)
2. Verify new schema is correct
3. Update tbc-kicker SKILL.md if needed (new template categories)
4. Add example configuration if significant

## Validation Levels

The `validate-inputs.py` script performs 3-level validation:

| Level | What it validates | Error example |
|-------|-------------------|---------------|
| **Component** | Name exists (`gitlab-ci-{name}` or `gitlab-ci-{name}-{variant}`) | `Component 'aws' not found` |
| **Version** | Exists in `project.tags` | `Version '99' not found` |
| **Inputs** | Exist in schema properties | `'region' is not valid` |

### Validation Order

1. Parse component string: `to-be-continuous/{project}/{component}@{version}`
2. Find template by `project.path` in `_meta.json`
3. Check component exists in `components[]`
4. Check version exists in `project.tags[]`
5. Validate inputs against schema

## Troubleshooting

### Schema Not Found

If validation reports "No schema found for template":

1. Check if template uses different project path
2. Verify schema exists in `schemas/` directory
3. Re-run extraction if missing

### Variable Name Mismatch

The script transforms variable names:
- Strips prefix: `PYTHON_IMAGE` → `image`
- Lowercase: `IMAGE` → `image`
- Hyphens: `BUILD_SYSTEM` → `build-system`

If mismatch occurs, check the `_meta.prefix` in schema.

### Missing Features/Variants

Features and variants are extracted from the kicker JSON. If missing:

1. Verify kicker source is updated
2. Check feature/variant structure in kicker-aggregated.json

## Additional Resources

### Reference Files

- **`references/kicker-structure.md`** - Structure of kicker-aggregated.json

### Scripts

- **`scripts/extract-schemas.py`** - Main extraction script (shared with tbc-kicker)

## _meta.json Structure

The extraction script generates `schemas/_meta.json` with template metadata:

```json
{
  "generated_from": "/tmp/kicker/src/assets/kicker-aggregated.json",
  "template_count": 50,
  "templates": {
    "python": {
      "name": "Python",
      "project": {
        "path": "to-be-continuous/python",
        "tag": "7.5.2",
        "tags": ["7.5.2", "7.5", "7", ...]
      },
      "variable_count": 48,
      "components": ["gitlab-ci-python", "gitlab-ci-python-vault", "gitlab-ci-python-gcp"]
    }
  }
}
```

### Key Fields

| Field | Description |
|-------|-------------|
| `project.path` | GitLab project path |
| `project.tag` | Latest version |
| `project.tags` | All available versions |
| `components` | Valid component names (base + variants) |

### Component Name Format

Component names are extracted from `template_path`:
- `templates/gitlab-ci-python.yml` → `gitlab-ci-python`
- `templates/gitlab-ci-python-vault.yml` → `gitlab-ci-python-vault`

The validation script uses this to verify component names in `.gitlab-ci.yml`:
```yaml
# Correct format
- component: $CI_SERVER_FQDN/to-be-continuous/python/gitlab-ci-python@7

# NOT: python/python@7 (missing gitlab-ci- prefix)
```

## Recommended Workflow

1. **Watch TBC releases**: Monitor https://gitlab.com/to-be-continuous for updates
2. **Update kicker clone**: `git pull` in /tmp/kicker
3. **Regenerate schemas**: Run extraction script
4. **Validate examples**: Ensure existing examples still pass
5. **Fix breaking changes**: Update examples if variables renamed/removed
6. **Document changes**: Note significant schema changes
