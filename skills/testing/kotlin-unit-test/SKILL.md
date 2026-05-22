---
name: kotlin-unit-test
description: Smart Kotlin unit testing with auto-detection, coverage analysis, and AI edge cases. Use when generating tests for biz/ layer classes, analyzing test coverage gaps, or discovering edge cases.
---

# Kotlin Unit Test

Project-specific skill for intelligent Kotlin unit testing.

## When to Use

- Generating tests for business logic classes (biz/ layer)
- Analyzing test coverage gaps
- Discovering edge cases for existing code
- Before writing new tests to understand what's missing

## Workflow

1. **Analyze class**: `python scripts/analyze_kotlin.py units <file.kt>`
2. **Check coverage**: `python scripts/analyze_kotlin.py coverage <source_dir> <test_dir>`
3. **Discover edge cases**: Load `references/edge-case-discovery.md`
4. **Write tests**: Follow patterns in `references/test-patterns.md`

## Script Commands

```bash
# Analyze single file - extract testable units
python scripts/analyze_kotlin.py units app/src/main/.../SomeClass.kt

# Analyze coverage gaps between source and test directories
python scripts/analyze_kotlin.py coverage app/src/main/java/.../biz app/src/test/java/.../biz
```

## Output Format

JSON structured output for parsing:
```json
{
  "class_name": "SomeClass",
  "methods": [...],
  "dependencies": [...],
  "coverage": {"tested": [], "missing": []}
}
```

## References

| File | Purpose |
|------|---------|
| `references/test-patterns.md` | JUnit4 + MockK + Turbine patterns |
| `references/edge-case-discovery.md` | AI prompts for finding edge cases |

## Integration

Works with `.claude/agents/unit-test-agent.md` for test generation workflow.
