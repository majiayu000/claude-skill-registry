---
name: enterprise-compound
description: "Captures institutional knowledge after solving problems. Documents what was solved, how, and how to prevent it. Searchable by tags and categories. Builds organizational memory that compounds over time. Use after fixes are verified or features are complete."
---

# Enterprise Compound — Institutional Knowledge Capture

## Philosophy

Every solved problem is an investment. If the solution lives only in git history, it is lost. If it lives in a searchable, tagged, cross-referenced knowledge base, it compounds. The next person (or agent) who hits the same class of problem finds the answer in seconds instead of hours.

Three principles:
1. **Capture at the moment of understanding.** The best time to document is right after solving — before context fades.
2. **Structure for retrieval, not for reading.** Tags, categories, and YAML frontmatter make solutions findable.
3. **Prevent, not just solve.** Every solution document includes a prevention section — how to stop this class of problem from recurring.

```
/enterprise-compound                          # capture the last fix/feature from the current session
/enterprise-compound fix: order duplication bug # capture a specific solution
/enterprise-compound feature: kanban board     # capture a feature's key decisions
```

---

## Triggers

Run this skill when:

| Event | Trigger |
|-------|---------|
| Bug fix verified and committed | Capture the root cause, investigation path, and fix |
| Feature verified and committed | Capture key design decisions, tradeoffs, and patterns |
| Debugging session found a root cause | Capture even if the fix is not yet applied |
| Architecture decision made | Capture the decision, alternatives considered, and rationale |
| Gotcha discovered | Capture the trap and how to avoid it |
| Performance issue resolved | Capture the bottleneck, measurement, and optimization |
| Integration quirk found | Capture the external system behavior and workaround |

---

## Step 1: Check for Duplicates

Before creating a new solution document, search for existing ones.

### Search existing solutions:
```bash
ls docs/solutions/ 2>/dev/null | grep -i "<keywords>"
```

### Search memory for prior knowledge:
Query memory (Memora/Muninn if available) with the problem domain keywords to check if this was already captured.

### Search git history:
```bash
git log --oneline --all --grep="<keywords>" | head -10
```

**If a duplicate exists**: update the existing document instead of creating a new one. Add the new findings, update the date, and note what changed.

**If a near-duplicate exists**: link to it. Cross-reference in both documents.

---

## Step 2: Classify the Solution

Determine the solution type and severity to guide the document structure.

| Type | When | Sections Required |
|------|------|-------------------|
| `bug-fix` | Fixed a defect | Problem, Investigation, Root Cause, Solution, Prevention |
| `feature` | Built new functionality | Problem, Design Decision, Implementation, Key Patterns, Gotchas |
| `architecture` | Made a structural decision | Context, Decision, Alternatives, Consequences |
| `gotcha` | Found a non-obvious trap | Trap, Symptom, Cause, Avoidance |
| `performance` | Resolved a performance issue | Symptom, Measurement, Bottleneck, Optimization, Verification |
| `integration` | External system quirk | System, Behavior, Workaround, Documentation Gap |

| Severity | When |
|----------|------|
| `critical` | Data corruption, security, production outage |
| `high` | Functional bug affecting users, performance degradation |
| `medium` | Incorrect behavior in edge cases, developer experience |
| `low` | Cosmetic, documentation, minor inconvenience |

---

## Step 3: Write the Solution Document

### File location: `docs/solutions/YYYY-MM-DD-<slug>.md`

Create the directory if it does not exist:
```bash
mkdir -p docs/solutions
```

### Document Template

````markdown
---
title: "<descriptive title>"
date: YYYY-MM-DD
type: bug-fix | feature | architecture | gotcha | performance | integration
severity: critical | high | medium | low
module: <affected module — e.g., "orders", "sync", "kanban", "auth">
files:
  - <file path 1>
  - <file path 2>
tags:
  - <tag1 — e.g., "sql", "race-condition", "null-guard", "rex-api">
  - <tag2>
  - <tag3>
related:
  - <path to related solution doc, if any>
  - <related commit hash, if useful>
---

# <Title>

## Problem

[2-4 sentences describing what went wrong or what was needed. Include the user-visible symptom if applicable.]

**Reported as**: [exact error message, user complaint, or test failure]
**Affected area**: [module, endpoint, component]
**Impact**: [who was affected and how]

## Investigation

[What was checked, in what order, and what was ruled out. This section is valuable because it saves the next person from repeating dead-end investigations.]

1. **First checked**: [what and why] — Result: [what was found]
2. **Then checked**: [what and why] — Result: [what was found]
3. **Ruled out**: [what was NOT the cause and why]
4. **Key insight**: [the moment of understanding — what led to the root cause]

### Execution Trace
```
[entry point] → [layer] → [layer] → ROOT CAUSE at [file:line]
```

## Root Cause

[For bug-fix type. 2-3 sentences explaining the actual defect — not the symptom.]

**What**: [the specific defect]
**Where**: [file:line]
**Why**: [how it got there — design oversight, copy-paste without adaptation, missing requirement, etc.]

## Design Decision

[For feature and architecture types. What was decided and why.]

**Decision**: [what was chosen]
**Alternatives considered**:
1. [Alternative A] — rejected because [reason]
2. [Alternative B] — rejected because [reason]

**Rationale**: [why this approach was chosen over alternatives]

## Solution

[What was done to fix/implement. Exact files, exact changes, exact reasoning.]

### Changes
| File | Change | Why |
|------|--------|-----|
| `path/to/file.js` | [what changed] | [why this specific change] |
| `path/to/other.js` | [what changed] | [why this specific change] |

### Key Code
```javascript
// Only include code if it illustrates a non-obvious pattern or technique
// that someone would need to see to understand the solution
```

### Blast Radius
[For bug-fix type. What else was checked and fixed as part of the blast radius scan.]

- [Sibling 1]: [same bug / OK]
- [Sibling 2]: [same bug / OK]

## Prevention

[How to prevent this CLASS of problem from recurring. Not "don't make this mistake" — concrete, actionable prevention.]

### Checklist (add to relevant skill/process)
- [ ] [specific check to add to a review checklist]
- [ ] [specific pattern to follow in future code]

### Pattern to Follow
```javascript
// If this solution established a pattern, show the pattern here
// so future code can copy it
```

### Anti-Pattern to Avoid
```javascript
// If this bug came from a common anti-pattern, show what NOT to do
// with a comment explaining why
```

### Automation Opportunity
[Can this class of bug be caught automatically? Lint rule, test pattern, pre-commit hook?]

## Tags Reference

[Brief explanation of each tag for searchability]
- `<tag1>`: [why this tag — what category it represents]
- `<tag2>`: [why this tag]
````

---

## Step 4: Save to Memory

After writing the solution document, save the key knowledge for cross-session retrieval. Use whichever memory backend is available (Memora MCP, Muninn MCP, or filesystem fallback).

### What to save:

**Always save**:
- The root cause (for bugs) or the key design decision (for features)
- The prevention guidance
- Any gotchas discovered during investigation

**Save format**:
```
Topic: [module] — [problem/feature summary]
Type: [solution | gotcha | decision | pattern]
Key finding: [1-2 sentences — the essential knowledge]
Prevention: [1 sentence — how to avoid this in future]
Reference: docs/solutions/YYYY-MM-DD-<slug>.md
Tags: [comma-separated tags]
```

### Memory save commands:

For bug fixes and gotchas — save as issue type:
```
MEMORY: save — type "issue", tags matching the document tags.
Content: the root cause, the fix, and the prevention pattern.
```

For features and architecture — save as decision type:
```
MEMORY: save — type "decision", tags matching the document tags.
Content: the decision, the rationale, and the key patterns.
```

For patterns and anti-patterns — save as pattern type:
```
MEMORY: save — appropriate tags.
Content: the pattern to follow or avoid, with code example.
```

---

## Step 5: Cross-Reference

### Link from MEMORY.md

If the solution is significant (critical/high severity, or establishes a new pattern), add a reference to the relevant section of `MEMORY.md`.

### Link from related solutions

If the document references or is referenced by other solutions, update both documents with cross-references in the `related` frontmatter field.

### Link from affected code

For critical bugs, consider adding a brief comment in the code pointing to the solution document:

```javascript
// GOTCHA: REX API returns success status even on failure.
// See docs/solutions/2026-03-09-rex-error-as-success.md
```

Use this sparingly — only for traps that are genuinely surprising and would catch future developers.

---

## Examples

### Example 1: Bug Fix Solution

```yaml
---
title: "getStaffUsers returns inactive and system accounts"
date: 2026-03-08
type: bug-fix
severity: high
module: sticky-notes
files:
  - src/services/feature/helpers.js
  - src/services/feature/queries.js
  - src/services/feature/kanban.js
tags:
  - sql
  - filter-gap
  - blast-radius
  - staff-visibility
related:
  - docs/contracts/2026-03-08-sticky-note-staff-visibility-contract.md
---
```

### Example 2: Architecture Decision

```yaml
---
title: "Placeholder product system design — dual-placeholder approach"
date: 2026-03-05
type: architecture
severity: medium
module: orders
files:
  - src/services/exampleService.js
  - src/jobs/exampleJob.js
tags:
  - placeholder
  - order-sync
  - rex-api
  - design-decision
related:
  - docs/plans/2026-03-05-placeholder-products-plan.md
---
```

### Example 3: Gotcha

```yaml
---
title: "REX API OrderCreate rejects orders with OrderTotal <= 0"
date: 2026-03-06
type: gotcha
severity: medium
module: rex-api
files:
  - src/services/orderService.js
tags:
  - rex-api
  - platform-limitation
  - order-sync
  - zero-dollar
---
```

---

## Quick Capture Mode

For low-severity gotchas or quick patterns, use a shortened format:

```markdown
---
title: "<title>"
date: YYYY-MM-DD
type: gotcha
severity: low
module: <module>
tags: [<tag1>, <tag2>]
---

# <Title>

**Trap**: [what goes wrong]
**Cause**: [why]
**Fix**: [what to do instead]
```

Save to Memora and move on. Full investigation section is not needed for simple gotchas.

---

## Metrics — How Knowledge Compounds

Track these to see the value of captured knowledge:

| Metric | How to Measure |
|--------|---------------|
| Solutions referenced | How often a solution doc is read by agents (memory recall hits) |
| Time saved | When a solution doc prevents re-investigation of a known issue |
| Duplicate bugs prevented | When a prevention checklist catches a bug before it ships |
| Pattern adoption | When a documented pattern is reused in new code |

The ROI of a solution document is: **(time to investigate originally) x (number of times referenced)**.

A 2-hour investigation documented in 10 minutes saves 2 hours every time someone hits the same class of problem. After 3 references, the document has paid for itself 6x over.

---

## Output — Compound Report

Print this after saving the solution:

```
═══════════════════════════════════════════════════════════
                   ENTERPRISE COMPOUND REPORT
═══════════════════════════════════════════════════════════

## Knowledge Captured
Type:     [bug-fix / feature / architecture / gotcha / performance / integration]
Severity: [critical / high / medium / low]
Module:   [module name]

## Document
Path: docs/solutions/YYYY-MM-DD-<slug>.md
Tags: [tag1, tag2, tag3]

## Key Knowledge
[1-2 sentences — the essential finding]

## Prevention Added
[1 sentence — what checklist item or pattern was established]

## Memora
Saved: [YES — type, tags, backend used]
Cross-references: [list of related docs updated]

## Knowledge Base Status
Total solutions: [N] documents in docs/solutions/
This module: [N] solutions for [module name]
This tag: [N] solutions tagged [primary tag]

═══════════════════════════════════════════════════════════
```
