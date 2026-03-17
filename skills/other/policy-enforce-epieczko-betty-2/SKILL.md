---
name: policy.enforce
description: Enforces policy rules for skill and agent manifests
---

# policy.enforce

Enforces policy rules for skill and agent manifests including naming conventions, semantic versioning, permissions validation, and status lifecycle checks.

## Overview

The `policy.enforce` skill validates skill and agent manifests against Betty Framework policy rules to ensure consistency and compliance across the framework. It supports both single-file validation and batch mode for scanning all manifests.

## Policy Rules

### 1. Naming Convention
- Names must be **lowercase only**
- Can use **dots** for namespacing (e.g., `api.define`, `workflow.compose`)
- Must start with a lowercase letter
- Must end with a letter or number
- **No spaces, underscores, or hyphens** in the name field

**Valid Examples:**
- `api.define`
- `policy.enforce`
- `skill.create`

**Invalid Examples:**
- `API.define` (uppercase)
- `api_define` (underscore)
- `api define` (space)
- `api-define` (hyphen)

### 2. Semantic Versioning
- Must follow semantic versioning format: `MAJOR.MINOR.PATCH`
- Optional pre-release suffix allowed (e.g., `1.0.0-alpha`)

**Valid Examples:**
- `0.1.0`
- `1.0.0`
- `2.3.1-beta`

**Invalid Examples:**
- `1.0` (missing patch)
- `v1.0.0` (prefix not allowed)
- `1.0.0.0` (too many segments)

### 3. Permissions
Only the following permissions are allowed:
- `filesystem` (or scoped: `filesystem:read`, `filesystem:write`)
- `network` (or scoped: `network:http`, `network:https`)
- `read`
- `write`

Any other permissions will trigger a violation.

### 4. Status
Must be one of:
- `draft` - Under development
- `active` - Production ready
- `deprecated` - Still works but not recommended
- `archived` - No longer maintained

## Usage

### Single File Validation

Validate a single skill or agent manifest:

```bash
python3 skills/policy.enforce/policy_enforce.py path/to/skill.yaml
```

Example:
```bash
python3 skills/policy.enforce/policy_enforce.py skills/api.define/skill.yaml
```

### Batch Mode

Validate all manifests in `skills/` and `agents/` directories:

```bash
python3 skills/policy.enforce/policy_enforce.py --batch
```

Or simply run without arguments:
```bash
python3 skills/policy.enforce/policy_enforce.py
```

### Strict Mode

Treat warnings as errors (if warnings are implemented in future):

```bash
python3 skills/policy.enforce/policy_enforce.py --batch --strict
```

## Output Format

The skill outputs JSON with the following structure:

### Single File Success

```json
{
  "success": true,
  "path": "skills/api.define/skill.yaml",
  "manifest_type": "skill",
  "violations": [],
  "violation_count": 0,
  "message": "All policy checks passed"
}
```

### Single File Failure

```json
{
  "success": false,
  "path": "skills/example/skill.yaml",
  "manifest_type": "skill",
  "violations": [
    {
      "field": "name",
      "rule": "naming_convention",
      "message": "Name contains uppercase letters: 'API.define'. Names must be lowercase.",
      "severity": "error"
    },
    {
      "field": "version",
      "rule": "semantic_versioning",
      "message": "Invalid version: '1.0'. Must follow semantic versioning (e.g., 1.0.0, 0.1.0-alpha)",
      "severity": "error"
    }
  ],
  "violation_count": 2,
  "message": "Found 2 policy violation(s)"
}
```

### Batch Mode

```json
{
  "success": true,
  "mode": "batch",
  "message": "Validated 15 manifest(s): 15 passed, 0 failed",
  "total_manifests": 15,
  "passed": 15,
  "failed": 0,
  "results": [
    {
      "success": true,
      "path": "skills/api.define/skill.yaml",
      "manifest_type": "skill",
      "violations": [],
      "violation_count": 0,
      "message": "All policy checks passed"
    }
  ]
}
```

## Interpreting Results

### Exit Codes
- `0` - All policy checks passed
- `1` - One or more policy violations found

### Violation Severity
- `error` - Blocking violation that must be fixed
- `warning` - Non-blocking issue (recommended to fix)

### Common Violations

**Naming Convention Violations:**
- Use lowercase: `API.define` → `api.define`
- Use dots instead of underscores: `api_define` → `api.define`
- Remove spaces: `api define` → `api.define`

**Version Violations:**
- Add patch version: `1.0` → `1.0.0`
- Remove prefix: `v1.0.0` → `1.0.0`

**Permission Violations:**
- Use only allowed permissions
- Replace `http` with `network:http`
- Replace `file` with `filesystem`

**Status Violations:**
- Use lowercase: `Active` → `active`
- Use valid values: `production` → `active`

## Integration with CI/CD

Add to your CI pipeline to enforce policies on all manifests:

```yaml
# .github/workflows/policy-check.yml
name: Policy Enforcement

on: [push, pull_request]

jobs:
  policy-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run Policy Enforcement
        run: |
          python3 skills/policy.enforce/policy_enforce.py --batch
```

## Inputs

| Input | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `manifest_path` | string | No | - | Path to a single manifest file to validate |
| `--batch` | boolean | No | false | Enable batch mode to validate all manifests |
| `--strict` | boolean | No | false | Treat warnings as errors |

## Outputs

| Output | Type | Description |
|--------|------|-------------|
| `success` | boolean | Whether all policy checks passed |
| `violations` | array | List of policy violations found |
| `violation_count` | integer | Total number of violations |
| `message` | string | Summary message |
| `path` | string | Path to the validated manifest (single mode) |
| `manifest_type` | string | Type of manifest: "skill" or "agent" (single mode) |
| `total_manifests` | integer | Total number of manifests checked (batch mode) |
| `passed` | integer | Number of manifests that passed (batch mode) |
| `failed` | integer | Number of manifests that failed (batch mode) |
| `results` | array | Individual results for each manifest (batch mode) |

## Dependencies

- `betty.config` - Configuration and paths
- `betty.validation` - Validation utilities
- `betty.logging_utils` - Logging infrastructure
- PyYAML - YAML parsing

## Status

**Active** - Production ready

## Examples

### Example 1: Validate a Single Skill

```bash
$ python3 skills/policy.enforce/policy_enforce.py skills/api.define/skill.yaml
{
  "success": true,
  "path": "skills/api.define/skill.yaml",
  "manifest_type": "skill",
  "violations": [],
  "violation_count": 0,
  "message": "All policy checks passed"
}
```

### Example 2: Batch Validation

```bash
$ python3 skills/policy.enforce/policy_enforce.py --batch
{
  "success": true,
  "mode": "batch",
  "message": "Validated 15 manifest(s): 15 passed, 0 failed",
  "total_manifests": 15,
  "passed": 15,
  "failed": 0,
  "results": [...]
}
```

### Example 3: Failed Validation

```bash
$ python3 skills/policy.enforce/policy_enforce.py skills/bad-example/skill.yaml
{
  "success": false,
  "path": "skills/bad-example/skill.yaml",
  "manifest_type": "skill",
  "violations": [
    {
      "field": "name",
      "rule": "naming_convention",
      "message": "Name contains uppercase letters: 'Bad-Example'. Names must be lowercase.",
      "severity": "error"
    }
  ],
  "violation_count": 1,
  "message": "Found 1 policy violation(s)"
}
$ echo $?
1
```

## Future Enhancements

- Custom policy rule definitions via YAML files
- Support for warning-level violations
- Auto-fix capability for common violations
- Policy exemptions and overrides
- Historical violation tracking
