---
name: test-augmentation
description: >
  Validates and improves test coverage for code changes. Checks coverage thresholds,
  identifies untested code paths, and provides guidance on writing effective tests.
  Use after making code changes or when improving test quality.
compatibility: Works with Java (JaCoCo), JavaScript/TypeScript (Jest/NYC), Python (coverage.py), Go (go test)
metadata:
  version: "1.0.0"
  technology: global
---

# Test Augmentation

> **Note**: Shell scripts are intentionally omitted. Coverage checks are implemented in `.scripts/lib/skills/test-augmentation.ts` and invoked via `npm run skills:test-augmentation`.

## When to use this skill

- After implementing new features
- When refactoring existing code
- To identify gaps in test coverage
- During test quality improvements

## Skill Contents

### Available Resources

**📚 references/** - Detailed documentation
- [go](references/go)
- [java](references/java)
- [python](references/python)
- [test patterns](references/test-patterns.md)
- [typescript](references/typescript)

---

## Coverage Tools

| Technology | Tool |
|------------|------|
| Java | JaCoCo |
| JavaScript/TypeScript | Jest, NYC |
| Python | coverage.py, pytest-cov |
| Go | go test -cover |

## References

| Technology | Reference |
|------------|-----------|
| Java | `references/java/test-patterns.md` |
| TypeScript | `references/typescript/test-patterns.md` |
| Python | `references/python/test-patterns.md` |
| Go | `references/go/test-patterns.md` |

## TODO

- [ ] Define coverage thresholds by project type
- [ ] Implement coverage change detection
- [ ] Add test quality metrics
- [ ] Create test pattern guidance by technology
<!-- AUTO-GENERATED FILE - DO NOT EDIT DIRECTLY -->
<!-- Source: bitsoex/ai-code-instructions → global/skills/test-augmentation/SKILL.md -->
<!-- To modify, edit the source file and run the distribution workflow -->

