# Fixture Validate Skill

> Version: 1.0.0
> Compiler: skill-compiler/1.0.0
> Last Updated: 2026-01-25

Validate fixture registry integrity as a validation pipeline step (hybrid gate).

## When to Activate

Use this skill when:
- Validation pipeline fixture step
- Validate fixtures
- Check fixture registry
- Fixture validation

## Core Principles

### 1. Fixtures Are Project Assets

Fixtures must be managed, not ad-hoc; every fixture should be intentional.

*Unmanaged test data leads to inconsistency, duplication, and maintenance burden.*

### 2. Reference Over Hardcode

Step definitions should reference fixtures, not contain inline test data.

*Inline data cannot be validated, updated centrally, or detected as duplicates.*

### 3. Dependency Integrity

Fixture dependency graphs must be acyclic and all references must resolve.

*Circular dependencies cause infinite loops; missing references cause runtime failures.*

### 4. Hybrid Trust Model

This is a HYBRID gate - failures can be overridden with documented justification.

*Some fixture issues have valid reasons (new feature, intentional deviation) that an agent can explain.*

---

## Workflow

### Phase 1: Discover Fixtures

Find all fixtures in the registry.

1. Scan tests/fixtures/ for *.fixture.* files
2. Parse each fixture file extracting _meta block if present
3. Build fixture inventory with paths, names, and metadata

**Outputs:** List of discovered fixtures, Metadata for each fixture

### Phase 2: Validate References

Check that all fixture references resolve.

1. Parse depends_on arrays from fixture metadata
2. Parse !ref tags from fixture content
3. Verify each referenced fixture exists in inventory
4. Record missing fixtures with source location

**Outputs:** List of valid references, List of missing fixtures with file/line

### Phase 3: Detect Orphans

Find fixtures not referenced by any test or other fixture.

1. Scan step definition files for fixture imports/references
2. Build reference graph from fixtures + step definitions
3. Identify fixtures with zero incoming references
4. Flag orphans (warning, not error)

**Outputs:** List of orphan fixtures, Reference count for each fixture

### Phase 4: Detect Cycles

Check for circular dependencies.

1. Build directed graph from depends_on relationships
2. Run cycle detection (DFS with back-edge detection)
3. If cycle found, report full cycle path

**Outputs:** Cycle detection result, Cycle path if found

### Phase 5: Check Hardcoded Data

Detect inline test data in step definitions.

1. Scan step definition files for suspicious patterns
2. Look for string literals in test setup (email, password, etc.)
3. Look for struct literals with test data
4. Report potential hardcoding with file/line

**Outputs:** List of suspected hardcoded data locations

### Phase 6: Generate Report

Produce structured JSON output per validation interface.

1. Aggregate all findings
2. Classify as error, warning, or info
3. Format as JSON per validation-interface.md
4. Return appropriate exit code

**Outputs:** JSON validation result to stdout, Exit code (0=passed, 1=failed, 2=warning)

---

## Validation Checks

| Check | Severity | Code | Description |
|-------|----------|------|-------------|
| Missing Reference | error | FIXTURE_MISSING | depends_on or !ref references nonexistent fixture |
| Circular Dependency | error | FIXTURE_CYCLE | Fixture dependency graph contains a cycle |
| Orphan Fixture | warning | FIXTURE_ORPHAN | Fixture has no references from tests or other fixtures |
| Hardcoded Data | warning | HARDCODED_DATA | Step definition contains inline test data |
| Schema Mismatch | error | FIXTURE_SCHEMA | Fixture data doesn't match declared schema |
| Deprecated Reference | warning | FIXTURE_DEPRECATED | Reference to deprecated fixture |

---

## Output Format

Following the validation interface specification:

```json
{
  "step": "fixture-validate",
  "status": "passed" | "failed" | "warning" | "skipped",
  "duration_ms": 87,
  "summary": "15 fixtures validated, 0 errors, 2 warnings",
  "details": {
    "fixtures_checked": 15,
    "fixtures_passed": 15,
    "references_validated": 42,
    "orphans_detected": 2,
    "cycles_detected": 0
  },
  "errors": [
    {
      "message": "Orphan fixture: no references found",
      "file": "tests/fixtures/legacy/old-user.fixture.yaml",
      "line": null,
      "column": null,
      "severity": "warning",
      "code": "FIXTURE_ORPHAN",
      "suggestion": "Remove if unused or add reference in test"
    }
  ]
}
```

---

## Exit Codes

| Code | Status | Meaning |
|------|--------|---------|
| 0 | passed | All checks passed, no issues |
| 1 | failed | Blocking error (missing fixture, cycle) |
| 2 | warning | Non-blocking issues (orphans, potential hardcoding) |
| 3 | skipped | No fixtures directory found |

---

## Patterns

| Pattern | When | Do | Why |
|---------|------|-----|-----|
| **Missing Fixture Detection** | depends_on references nonexistent fixture | Report error with source fixture path and line number | Missing fixtures cause runtime failures |
| **Orphan Detection** | Fixture has no references | Report warning with orphan fixture path | Orphans waste maintenance effort |
| **Cycle Detection** | Circular dependency found | Report error with full cycle path | Cycles prevent fixture loading |
| **Hardcode Detection** | Step definition contains inline test data | Report warning with file/line and suggest extraction | Hardcoded data should be fixtures |

---

## Anti-Patterns to Avoid

| Anti-Pattern | Why It Fails | Instead |
|--------------|--------------|---------|
| **Ignoring All Warnings** | Technical debt accumulates, orphans multiply | Review each warning, create follow-up tasks |
| **False Positive Suppression** | May hide real issues, erodes trust | Understand the detection before suppressing |
| **Override Without Justification** | No audit trail, issues recur | Always document override reason in bead notes |

---

## Hybrid Gate Override

This validation step is a HYBRID gate. Agents can override failures when there's a valid reason:

### Valid Override Reasons

- New fixture will be created in follow-up bead (reference track issue)
- Intentional deviation documented in feature spec
- Legacy fixture being deprecated with migration plan
- False positive from detection heuristics (document why)

### Override Protocol

1. Analyze the validation failure
2. Determine if override is justified
3. Document justification in bead notes:
   ```bash
   bd update <bead-id> --notes "OVERRIDE: fixture-validate failed on FIXTURE_MISSING for users/premium. Reason: New fixture, tracked in beadsmith-e12.X"
   ```
4. Proceed with bead closure

### Invalid Override Reasons

- "I'll fix it later" (without tracked issue)
- "It's just a warning" (warnings deserve investigation)
- "The detection is wrong" (without understanding why)

---

## Quality Checklist

Before completing fixture validation:

- [ ] All fixtures discovered and parsed
- [ ] All depends_on references validated
- [ ] Orphan fixtures identified
- [ ] Cycle detection completed
- [ ] Hardcoded data patterns checked
- [ ] Structured JSON report generated
- [ ] Exit code reflects overall status
- [ ] Any overrides documented in bead notes

---

## Examples

### All Fixtures Valid

```
1. Scan tests/fixtures/ -> 15 fixtures found
2. Validate references -> all resolve
3. Orphan check -> 0 orphans
4. Cycle check -> no cycles
5. Hardcode check -> 0 suspicious patterns
6. Output: {"step":"fixture-validate","status":"passed",...}
7. Exit code: 0
```

### Missing Fixture Reference

```
1. Scan -> 15 fixtures
2. Validate references -> tests/fixtures/scenarios/signup.fixture.yaml
   references "users/premium" which doesn't exist
3. Output includes error:
   {
     "message": "Referenced fixture not found: users/premium",
     "file": "tests/fixtures/scenarios/signup.fixture.yaml",
     "line": 8,
     "severity": "error",
     "code": "FIXTURE_MISSING"
   }
4. Exit code: 1 (failed)
```

### Orphan Fixture Detected

```
1. Scan -> 15 fixtures
2. Reference analysis -> tests/fixtures/legacy/old-user.fixture.yaml
   has 0 references from any step definition or other fixture
3. Output includes warning:
   {
     "message": "Orphan fixture: no references found",
     "file": "tests/fixtures/legacy/old-user.fixture.yaml",
     "severity": "warning",
     "code": "FIXTURE_ORPHAN"
   }
4. Exit code: 2 (warning) - can still close bead but should investigate
```

---

## References

- [docs/validation-interface.md](../docs/validation-interface.md) - Output format specification
- [docs/fixture-registry.md](../docs/fixture-registry.md) - Fixture structure and metadata
- [skills/validate-pipeline/](../skills/validate-pipeline/) - How this step is invoked
