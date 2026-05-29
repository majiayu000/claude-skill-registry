# Epic Validation Skill

> Version: 1.0.0
> Compiler: skill-compiler/1.0.0
> Last Updated: 2026-01-25

Validate epic quality after 100% bead completion before declaring truly complete.

## When to Activate

Use this skill when:
- Epic at 100%
- All beads closed
- Epic completion validation
- Before declaring epic complete

## Core Principles

### 1. Completion Is Not Quality

100% bead closure means tasks are done, not that the epic is ready.

*Individual beads may pass but integration, documentation, or hygiene issues remain.*

### 2. Synthesis Over Summary

Epic validation checks emergent properties, not just aggregated bead results.

*Cross-cutting concerns only visible when viewing the whole.*

### 3. Hybrid Gate

Epic validation warns but does not block; agent can override with justification.

*Some issues are acceptable trade-offs; forcing perfection would block progress.*

### 4. Structured Report

Validation produces archivable report for future reference.

*Enables post-mortem analysis and improvement.*

---

## Workflow

### Phase 1: Integration Verification

Check that components work together.

1. Run integration test suite if exists (tests/integration/)
2. Check for API contract mismatches between components
3. Verify no breaking changes to public interfaces
4. Look for version/dependency conflicts

**Outputs:** Integration test results, Contract verification status

### Phase 2: Documentation Synthesis

Ensure documentation reflects implemented features.

1. Check README mentions all major features from epic
2. Scan for orphan docs (referenced features removed)
3. Verify public API has documentation
4. Check CHANGELOG updated (if project uses one)

**Outputs:** Documentation coverage assessment, Orphan documentation list

### Phase 3: Codebase Hygiene

Verify no cruft remains from implementation.

1. Search for TODO(<bead-id>) markers for closed beads
2. Check for orphan files (created but not imported/used)
3. Verify build succeeds with strict warnings
4. Check for debug code left in (println!, console.log)

**Outputs:** Hygiene issues list, Build verification result

### Phase 4: Coverage Gate (Optional)

Check test coverage if configured.

1. Check if .beads/coverage-config.yaml exists
2. If configured, run coverage analysis
3. Compare to threshold or baseline
4. Report coverage delta

**Outputs:** Coverage percentage, Threshold comparison

### Phase 5: Generate Report

Produce structured validation report.

1. Aggregate all findings
2. Classify as error, warning, or info
3. Generate JSON report
4. Generate human-readable summary
5. Archive to .beads/reports/<epic-id>-validation.json

**Outputs:** Archived JSON report, Console summary, Overall verdict

---

## Validation Checks

### Integration Verification

| Check | Command | Severity |
|-------|---------|----------|
| Integration tests | `cargo test --test integration` | error if fail |
| Build clean | `cargo build --release 2>&1` | warning if warnings |
| Dependency audit | `cargo audit` (if available) | warning |

### Documentation Synthesis

| Check | Method | Severity |
|-------|--------|----------|
| README current | Grep for epic features | warning if missing |
| API documented | Check doc comments | warning |
| CHANGELOG | Check for epic entry | info |
| Orphan docs | Grep for removed features | warning |

### Codebase Hygiene

| Check | Command | Severity |
|-------|---------|----------|
| TODO markers | `grep -r "TODO(<epic-id>" src/` | warning |
| Debug code | `grep -r "println!" src/` | info |
| Orphan files | Compare file list to imports | warning |
| Format | `cargo fmt --check` | warning |

---

## Report Format

```json
{
  "epic_id": "beadsmith-e12",
  "validation_date": "2026-01-25T16:00:00Z",
  "verdict": "pass_with_warnings",
  "summary": "2 warnings, 0 errors",
  "phases": [
    {
      "name": "integration",
      "status": "passed",
      "findings": []
    },
    {
      "name": "documentation",
      "status": "warning",
      "findings": [
        {
          "type": "warning",
          "message": "CHANGELOG not updated for epic",
          "file": "CHANGELOG.md"
        }
      ]
    },
    {
      "name": "hygiene",
      "status": "warning",
      "findings": [
        {
          "type": "warning",
          "message": "TODO marker found for closed bead",
          "file": "src/lib.rs",
          "line": 42,
          "bead_id": "beadsmith-e12.3"
        }
      ]
    },
    {
      "name": "coverage",
      "status": "skipped",
      "reason": "No coverage config"
    }
  ],
  "overrides": [
    {
      "finding": "CHANGELOG not updated",
      "justification": "Internal tooling, no external consumers"
    }
  ]
}
```

---

## Patterns

| Pattern | When | Do |
|---------|------|-----|
| **All Checks Pass** | No issues found | Declare epic complete |
| **Warnings Only** | Issues but all warnings | Log warnings, proceed |
| **Issues With Justification** | Issues with override | Document and proceed |
| **Critical Issues** | Blocking issues | File follow-up beads |

---

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Instead |
|--------------|---------|---------|
| **Skipping Validation** | Integration issues shipped | Always validate at 100% |
| **Override Without Justification** | No audit trail | Document every override |
| **Perfection Paralysis** | Never ships | Ship with known issues |

---

## Override Protocol

When overriding a validation warning:

1. **Assess the finding** - Is it a genuine issue or false positive?
2. **Determine if override is justified**:
   - False positive (e.g., grep matched comment)
   - Tracked elsewhere (e.g., TODO for next phase)
   - Acceptable trade-off (e.g., internal tooling, low impact)
3. **Document in report**:
   ```json
   "overrides": [{
     "finding": "TODO marker for beadsmith-e12.3",
     "justification": "Phase 2 work, tracked in beadsmith-e13.1"
   }]
   ```

### Invalid Override Reasons

- "I'll fix it later" (without tracking)
- "It's just a warning"
- "No one will notice"

---

## Integration with beads-loop

Epic validation runs after the loop detects 100% completion:

```
LOOP:
  1. CHECK COMPLETION
     bd epic status <id> --json
     If 100%:
       -> Invoke epic-validation skill
       -> If PASS or PASS_WITH_OVERRIDES:
            -> Output success summary
            -> EXIT
       -> If BLOCKED:
            -> Report issues
            -> File follow-up beads
            -> EXIT with issues
```

---

## Quality Checklist

Before completing epic validation:

- [ ] Integration tests run (if exist)
- [ ] Documentation coverage checked
- [ ] No TODO markers for closed beads
- [ ] Build succeeds clean
- [ ] Report generated and archived
- [ ] Any overrides documented with justification
- [ ] Epic declared complete or follow-up beads filed

---

## Example: Complete Validation

```bash
# Epic at 100%
$ bd epic status beadsmith-e12
beadsmith-e12: 14/14 beads closed (100%)

# Run validation
$ # (invoke epic-validation skill)

=== Epic Validation Report ===
Epic: beadsmith-e12

Integration: PASSED
  - Integration tests: N/A (no tests/integration/)
  - Build: clean, no warnings

Documentation: WARNING
  - README: mentions all 4 BDD skills
  - API docs: coverage okay
  - CHANGELOG: not updated (OVERRIDE: internal tooling)

Hygiene: PASSED
  - TODO markers: none found
  - Orphan files: none detected
  - Format: clean

Coverage: SKIPPED
  - No .beads/coverage-config.yaml

Verdict: PASS_WITH_WARNINGS (1 override documented)
Report archived: .beads/reports/beadsmith-e12-validation.json

=== Epic Complete! ===
```

---

## References

- [skills/validate-pipeline](../skills/validate-pipeline/) - Per-bead validation
- [skills/complete-to-org](../skills/complete-to-org/) - Epic completion callback
- [commands/beads-loop.md](../commands/beads-loop.md) - Loop termination
