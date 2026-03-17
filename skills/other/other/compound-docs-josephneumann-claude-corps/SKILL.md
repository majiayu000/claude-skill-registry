---
name: compound-docs
description: "This skill is auto-invoked when working with files in docs/solutions/ to ensure proper formatting and schema compliance. It validates solution documents and helps maintain consistency in the learnings database."
allowed-tools: Read, Bash, Glob, Grep, Edit
---

# Compound Docs: Solution Document Management

You are managing the project's solution documentation in `docs/solutions/`. This skill ensures documents follow the correct schema and are properly organized.

## Auto-Invocation Triggers

This skill activates automatically when:
- Creating a new file in `docs/solutions/`
- Editing an existing solution document
- Running `/compound` to capture a learning

## Schema Validation

All solution documents must have valid YAML frontmatter matching this schema:

### Required Fields

```yaml
---
module: string           # Affected module/area (e.g., "authentication", "database")
date: YYYY-MM-DD        # Date the solution was documented
problem_type: enum      # One of the defined problem types
symptoms:               # List of observable symptoms
  - string
root_cause: enum        # One of the defined root causes
severity: enum          # One of: critical, high, medium, low
---
```

### problem_type (required)

One of:
- `build-error` - Compilation, bundling, dependency issues
- `test-failure` - Test suite failures
- `runtime-error` - Exceptions, crashes at runtime
- `performance` - Slow operations, memory issues
- `database` - Query issues, migrations, data integrity
- `security` - Vulnerabilities, auth issues
- `integration` - Third-party API, service communication
- `logic-error` - Incorrect business logic
- `workflow` - Development process, tooling issues

### root_cause (required)

One of:
- `missing-dependency` - Package not installed or wrong version
- `config-error` - Configuration mistake
- `race-condition` - Timing/concurrency issue
- `incorrect-assumption` - Wrong understanding of behavior
- `api-change` - External API changed
- `missing-validation` - Input not validated
- `resource-exhaustion` - Memory, connections, etc.
- `logic-flaw` - Bug in business logic
- `documentation-gap` - Missing or wrong docs
- `other` - Doesn't fit other categories

### severity (required)

- `critical` - Production outage, data loss, security breach
- `high` - Major feature broken, significant user impact
- `medium` - Feature degraded, workaround exists
- `low` - Minor issue, cosmetic, edge case

### Optional Fields

```yaml
tags:                   # Additional searchable tags
  - string
related:                # Links to related solutions/issues
  - string
prevention:             # How to prevent recurrence
  - string
```

## Directory Structure

Solutions are organized by problem type:

```
docs/solutions/
├── build-errors/
├── test-failures/
├── runtime-errors/
├── performance/
├── database/
├── security/
├── integration/
├── logic-errors/
└── workflow/
```

## Filename Convention

```
[symptom-slug]-[module]-YYYYMMDD.md
```

Examples:
- `import-error-auth-20260124.md`
- `n-plus-one-query-orders-20260115.md`
- `jwt-expiry-api-20260110.md`

Rules:
- All lowercase
- Hyphens for spaces
- Symptom keyword first (searchable)
- Module second (context)
- Date last (versioning)

## Document Template

```markdown
---
module: [module-name]
date: [YYYY-MM-DD]
problem_type: [type]
symptoms:
  - [symptom 1]
  - [symptom 2]
root_cause: [cause]
severity: [level]
tags:
  - [tag1]
  - [tag2]
---

# [Descriptive Title]

## Symptom

[What was observed - error messages, unexpected behavior]

## Investigation

[How the problem was diagnosed - what was checked, what was ruled out]

## Root Cause

[The actual underlying issue]

## Solution

[What fixed it - specific code changes, config updates]

```[language]
// Code example if applicable
```

## Prevention

[How to avoid this in the future - tests, validations, patterns]

## Related

- [Link to related solution]
- [Link to issue/PR]
```

## Validation Workflow

When creating or editing a solution document:

1. **Check Frontmatter**
   - All required fields present
   - Enum values are valid
   - Date format is correct

2. **Check Structure**
   - File is in correct category directory
   - Filename follows convention
   - All template sections present

3. **Report Issues**
   ```
   Validation Issues:
   - [ ] Missing required field: severity
   - [ ] Invalid problem_type: "error" (should be one of: build-error, test-failure, ...)
   - [ ] File should be in docs/solutions/database/ based on problem_type
   ```

4. **Offer Fixes**
   - Auto-fix obvious issues (date format, directory)
   - Ask for input on semantic issues (problem_type, root_cause)

## Search Support

Help users find existing solutions:

```bash
# By module
grep -r "module: auth" docs/solutions/ --include="*.md" -l

# By problem type
grep -r "problem_type: test-failure" docs/solutions/ --include="*.md" -l

# By keyword in symptoms
grep -ri "timeout" docs/solutions/ --include="*.md" -l

# By date range
find docs/solutions/ -name "*2026*.md" -type f
```

## Maintenance Tasks

Periodic maintenance for the solutions database:

1. **Check for duplicates**: Similar symptoms in different docs
2. **Update stale solutions**: Old solutions may need updating
3. **Add cross-references**: Link related solutions
4. **Verify consistency**: Ensure all docs match current schema
