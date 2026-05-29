# Decision Audit Skill

> Version: 1.0.0
> Compiler: skill-compiler/1.0.0
> Last Updated: 2026-01-25

Record and query quality decisions and trade-offs during bead execution.

## When to Activate

Use this skill when:
- Skipped documentation
- Accepted tech debt
- Chose not to test
- Quality trade-off
- Decision audit
- Override with justification

## Core Principles

### 1. Explicit Over Silent

Quality trade-offs must be recorded, not silently skipped.

*Silent skips are invisible failures; explicit decisions are reviewable.*

### 2. Low Friction Recording

Recording a decision should be a single command.

*High friction leads to skipping the recording, defeating the purpose.*

### 3. Queryable By Category

Decisions should be retrievable by type for governance review.

*Enables patterns like "show all tech debt across project".*

### 4. Tied To Source

Every decision traces back to the bead that made it.

*Enables accountability and context understanding.*

---

## Decision Categories

| Code | Category | Examples |
|------|----------|----------|
| `DECISION:DOC` | Documentation skipped | "Internal function only", "Covered by README" |
| `DECISION:TEST` | Test coverage skipped | "Covered by integration", "Config-only change" |
| `DECISION:DEBT` | Tech debt accepted | "Hardcoded value", "TODO for phase 2" |
| `DECISION:LINT` | Lint/warning suppressed | "False positive", "Macro-generated code" |
| `DECISION:SCOPE` | Scope reduced | "Dropped feature", "Simplified approach" |
| `DECISION:DEFER` | Work deferred | "Filed follow-up bead", "Phase 2 work" |
| `DECISION:OTHER` | Uncategorized | Use sparingly, describe clearly |

---

## Recording Format

### Standard Format

```
DECISION:<CATEGORY>: <description>. Justification: <why>. Tracking: <reference>
```

### Examples

```bash
# In bead notes
bd update beadsmith-e12.5 --notes "DECISION:DOC: No API docs for internal function. Justification: No public consumers. Tracking: N/A"

# In close reason (for simple decisions)
bd close beadsmith-e12.5 -r "Completed: Parser implementation. DECISION:DOC: Internal only"

# Multiple decisions
bd update beadsmith-e12.7 --notes "DECISION:DEBT: Hardcoded timeout. Justification: Deadline. Tracking: beadsmith-e13.2
DECISION:LINT: Suppressed unused warning. Justification: Future use planned. Tracking: N/A"
```

---

## Workflow

### Phase 1: Identify Decision Point

Recognize when a quality trade-off is being made:

- Conscious choice to skip documentation
- Choice to not write tests for specific code
- Accepting a warning or lint issue
- Deferring work to future bead
- Any SKIPPED item in quality checklist

### Phase 2: Categorize Decision

Match to standard category code. Use `OTHER` only when no standard code fits.

### Phase 3: Record Decision

Use `bd update --notes` or include in `bd close -r` reason:

```bash
# Full format for notes
bd update <bead-id> --notes "DECISION:DEBT: <what>. Justification: <why>. Tracking: <ref>"

# Brief format for close reason
bd close <bead-id> -r "Completed: <summary>. DECISION:DOC: <brief reason>"
```

### Phase 4: Query Decisions (Post-Epic)

Review decisions during epic validation or governance review.

---

## Query Patterns

### All Decisions in Epic

```bash
bd list --parent <epic-id> --json | \
  jq -r '.[] | select(.notes != null) | select(.notes | contains("DECISION:")) | "\(.id): \(.notes)"'
```

### Decisions by Category

```bash
# Tech debt only
bd list --parent <epic-id> --json | \
  jq -r '.[] | select(.notes != null) | select(.notes | contains("DECISION:DEBT")) | "\(.id): \(.notes)"'

# Documentation only
bd list --parent <epic-id> --json | \
  jq -r '.[] | select(.notes != null) | select(.notes | contains("DECISION:DOC")) | "\(.id): \(.notes)"'
```

### Decision Count by Category

```bash
bd list --parent <epic-id> --json | \
  jq '[.[] | select(.notes != null) | .notes | capture("DECISION:(?<cat>[A-Z]+)") | .cat] | group_by(.) | map({category: .[0], count: length})'
```

### Decisions with Tracking References

```bash
bd list --parent <epic-id> --json | \
  jq -r '.[] | select(.notes != null) | select(.notes | contains("Tracking:")) | select(.notes | contains("DECISION:")) | "\(.id): \(.notes)"'
```

---

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Instead |
|--------------|---------|---------|
| **Silent Skipping** | No audit trail | Record with DECISION prefix |
| **Vague Justification** | "Not needed" | Specific reason |
| **Untracked Deferrals** | Work forgotten | Include bead/issue reference |
| **Novel Categories** | Can't aggregate | Use standard codes |

---

## Integration Points

### Quality Checklist (beads-loop step 7)

Each SKIPPED item becomes a decision:

```
Quality Checklist:
[ ] Documentation: SKIPPED - DECISION:DOC: Internal utility function

Record: bd update <id> --notes "DECISION:DOC: Skipped for internal utility. Justification: No public API."
```

### Validation Pipeline Override

Hybrid gate overrides are decisions:

```
Fixture validation: FAILED (1 missing fixture)
Override: Yes - new feature, fixture in follow-up

Record: bd update <id> --notes "DECISION:DEFER: Fixture for new feature. Justification: Will be created in beadsmith-e12.next. Tracking: beadsmith-e12.next"
```

### Epic Validation Review

Epic validation reviews accumulated decisions:

```
=== Decision Summary for beadsmith-e12 ===
DOC:   3 decisions
TEST:  1 decision
DEBT:  2 decisions
DEFER: 1 decision

Review each for appropriateness...
```

---

## Quality Checklist

Before completing decision recording:

- [ ] Decision point recognized
- [ ] Category assigned from standard list
- [ ] Justification is specific and reviewable
- [ ] Tracking reference included for deferrals
- [ ] Decision recorded in bead notes or close reason
- [ ] Format uses DECISION prefix

---

## Examples

### Example 1: Skip Documentation

```bash
# Context: Internal parsing function, no public API
bd update beadsmith-e12.5 --notes "DECISION:DOC: Skipped API docs for internal parse_fixture() function. Justification: No public consumers, function is implementation detail. Tracking: N/A"
```

### Example 2: Accept Tech Debt

```bash
# Context: Hardcoded value due to deadline
bd update beadsmith-e12.7 --notes "DECISION:DEBT: Hardcoded validation timeout (5000ms). Justification: Deadline pressure, works for current use case. Tracking: Filed beadsmith-e13.2 for configuration"
```

### Example 3: Defer Test Coverage

```bash
# Context: Covered by integration tests
bd update beadsmith-e12.10 --notes "DECISION:TEST: No unit tests for beads-loop changes. Justification: Behavior verified by integration flow. Tracking: N/A - covered by e2e"
```

### Example 4: Brief in Close Reason

```bash
# Context: Simple decision, record inline
bd close beadsmith-e12.12 -r "Completed: Quality checklist. DECISION:DOC: Command file only, self-documenting"
```

---

## References

- [skills/validate-pipeline](../skills/validate-pipeline/) - Where override decisions occur
- [skills/epic-validation](../skills/epic-validation/) - Where decisions are reviewed
- [commands/beads-loop.md](../commands/beads-loop.md) - Quality checklist generating decisions
