---
name: ln-625-dependencies-auditor
description: Dependencies and reuse audit worker (L3). Checks outdated packages, unused dependencies, reinvented wheels, custom implementations of standard library features. Returns findings with severity, location, effort, recommendations.
allowed-tools: Read, Grep, Glob, Bash
---

# Dependencies & Reuse Auditor (L3 Worker)

Specialized worker auditing dependency management and code reuse.

## Purpose & Scope

- **Worker in ln-620 coordinator pipeline**
- Audit **dependencies and reuse** (Categories 7+8: Medium Priority)
- Check outdated packages, unused deps, wheel reinvention
- Calculate compliance score (X/10)

## Inputs (from Coordinator)

Receives `contextStore` with tech stack, package manifest paths, codebase root.

## Workflow

1) Parse context
2) Run dependency checks (outdated, unused, reinvented)
3) Collect findings
4) Calculate score
5) Return JSON

## Audit Rules

### 1. Outdated Packages
**Detection:**
- Run `npm outdated --json` (Node.js)
- Run `pip list --outdated --format=json` (Python)
- Run `cargo outdated --format=json` (Rust)

**Severity:**
- **HIGH:** Major version behind (security risk)
- **MEDIUM:** Minor version behind
- **LOW:** Patch version behind

**Recommendation:** Update to latest version, test for breaking changes

**Effort:** S-M (update version, run tests)

### 2. Unused Dependencies
**Detection:**
- Parse package.json/requirements.txt
- Grep codebase for `import`/`require` statements
- Find dependencies never imported

**Severity:**
- **MEDIUM:** Unused production dependency (bloats bundle)
- **LOW:** Unused dev dependency

**Recommendation:** Remove from package manifest

**Effort:** S (delete line, test)

### 3. Available Features Not Used
**Detection:**
- Check for axios when native fetch available (Node 18+)
- Check for lodash when Array methods sufficient
- Check for moment when Date.toLocaleString sufficient

**Severity:**
- **MEDIUM:** Unnecessary dependency (increases bundle size)

**Recommendation:** Use native alternative

**Effort:** M (refactor code to use native API)

### 4. Custom Implementations
**Detection:**
- Grep for custom sorting algorithms
- Check for hand-rolled validation (vs validator.js)
- Find custom date parsing (vs date-fns/dayjs)

**Severity:**
- **HIGH:** Custom crypto (security risk)
- **MEDIUM:** Custom utilities with well-tested alternatives

**Recommendation:** Replace with established library

**Effort:** M (integrate library, replace calls)

## Scoring Algorithm

```
penalty = (high * 1.0) + (medium * 0.5) + (low * 0.2)
score = max(0, 10 - penalty)
```

## Output Format

```json
{
  "category": "Dependencies & Reuse",
  "score": 7,
  "total_issues": 8,
  "high": 2,
  "medium": 4,
  "low": 2,
  "findings": [
    {
      "severity": "HIGH",
      "location": "package.json:15",
      "issue": "express v4.17.0 (current: v4.19.2, 2 major versions behind)",
      "principle": "Dependency Management / Security Updates",
      "recommendation": "Update to v4.19.2 for security fixes",
      "effort": "M"
    }
  ]
}
```

---
**Version:** 3.0.0
**Last Updated:** 2025-12-23
