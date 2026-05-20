---
name: test-blocked-fixture
description: >
  This is a test fixture with intentional violations for regression testing.
  It contains <angle brackets> which trigger B5, and has an unexpected
  frontmatter property which triggers W2.
extra_property: this-is-not-allowed
---

# Test Blocked Fixture

This skill exists solely for testing the skill-auditor. It should always
report as BLOCKED with the following violations:

## Expected Violations

- **B5**: Description contains angle brackets (< or >)
- **W2**: Unexpected frontmatter property: extra_property

## Usage

```bash
# Should exit 1 with BLOCKED status
uv run skill-auditor skills/test-blocked-fixture

# Hybrid mode should show structured blockers
uv run skill-auditor --hybrid skills/test-blocked-fixture
```

Do not fix these violations - they are intentional.
