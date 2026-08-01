---
name: yaml-validator
description: 'Comprehensive YAML syntax validation, error fixing, and schema validation
  for various formats (GitHub Actions, Docker Compose, Kubernetes, GitLab CI). Use
  when Claude needs to: (1) Validate YAML synta'
---

---
name: yaml-validator
description: Comprehensive YAML syntax validation, error fixing, and schema validation for various formats (GitHub Actions, Docker Compose, Kubernetes, GitLab CI). Use when Claude needs to: (1) Validate YAML syntax, (2) Check YAML files for errors, (3) Fix common YAML formatting issues, (4) Validate against schemas like GitHub Actions workflows, Docker Compose files, Kubernetes manifests, or GitLab CI pipelines, (5) Debug YAML parsing errors. Triggers on phrases like "check yaml", "validate yaml", "fix yaml errors", "yaml syntax".
---

# YAML Validator

Validate, fix, and check YAML files against schemas.

## Quick Start

### Basic Syntax Validation

Validate YAML files for syntax errors:

```bash
python scripts/validate_yaml.py file.yml
python scripts/validate_yaml.py file1.yml file2.yml  # Multiple files
python scripts/validate_yaml.py *.yml --quiet         # Only show errors
```

### Auto-Fix Common Errors

Automatically fix common YAML issues:

```bash
python scripts/fix_yaml.py file.yml -i              # Fix in-place
python scripts/fix_yaml.py file.yml > fixed.yml     # Output to new file
python scripts/fix_yaml.py *.yml -i --no-backup     # Fix without backups
```

Common fixes applied:
- Convert tabs to spaces
- Remove trailing whitespace
- Normalize indentation
- Add newline at end of file
- Remove excessive blank lines

### Schema Validation

Validate against specific schemas:

```bash
# Auto-detect schema type
python scripts/validate_schema.py workflow.yml

# Explicit schema type
python scripts/validate_schema.py -t home-assistant configuration.yaml
python scripts/validate_schema.py -t github-actions .github/workflows/ci.yml
python scripts/validate_schema.py -t docker-compose docker-compose.yml
python scripts/validate_schema.py -t kubernetes deployment.yml
python scripts/validate_schema.py -t gitlab-ci .gitlab-ci.yml

# List available schemas
python scripts/validate_schema.py --list-schemas
```

## Workflow

### When YAML validation is requested:

1. **Check syntax first**: Use `validate_yaml.py` to identify syntax errors
2. **Fix if needed**: Use `fix_yaml.py` to auto-fix common issues
3. **Validate schema**: Use `validate_schema.py` for format-specific validation

### For YAML errors:

1. Run validation to identify the issue
2. Check `references/common-errors.md` for guidance on specific error types
3. Apply fixes manually or use `fix_yaml.py`
4. Re-validate to confirm

### For schema validation:

1. Identify the YAML type (GitHub Actions, Docker Compose, etc.)
2. Run `validate_schema.py` with appropriate type
3. See `references/schemas.md` for schema-specific requirements

## Supported Schemas

- **home-assistant**: Home Assistant configuration files
- **github-actions**: GitHub Actions workflow files
- **docker-compose**: Docker Compose configuration files
- **kubernetes**: Kubernetes resource manifests
- **gitlab-ci**: GitLab CI/CD pipeline files

See `references/schemas.md` for detailed schema documentation.

## Common Error Patterns

For detailed error explanations and fixes, see `references/common-errors.md`:

- Indentation errors (tabs vs spaces)
- Quote mismatches
- Colon spacing issues
- Boolean value confusion
- Multiline string formatting
- Duplicate keys
- Special character handling

## Dependencies

Scripts require:
- Python 3.7+
- PyYAML: `pip install pyyaml`
- jsonschema: `pip install jsonschema` (for schema validation only)

## Exit Codes

All scripts use standard exit codes:
- `0`: Success (all files valid)
- `1`: Validation failed (syntax or schema errors)
- `2`: Missing dependencies or invalid arguments
