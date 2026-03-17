---
name: pm-update
description: Backward pass through older decisions to update status, meta_state, and cross-links after a sprint or documentation session. Finds decisions made outdated by newer evidence. Triggers on "/pm-update", "/pm-update [decision]", "update registers", "propagate changes", "mark superseded".
user-invocable: true
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
context: fork
---

## Runtime Configuration (Step 0)

Read `ops/derivation-manifest.md` for vocabulary mapping. Key terms:
- decisions folder, decision registers, meta_state field, superseded/outdated/invalidated states

Read `ops/config.yaml` for stale threshold (stale_issue_days).

---

## EXECUTE NOW

**Target: $ARGUMENTS**

Parse immediately:
- If target contains decision name: propagate from that decision outward
- If target is empty: find all decisions whose meta_state should change based on recent activity
- If target is "stale": find all decisions where last_reviewed > stale threshold

**START NOW.**

---

## Philosophy

**Decisions age. The PM system must age them deliberately, not accidentally.**

A decision created in Sprint 2 about "use Dulwich for bare Git repos" might be superseded by Sprint 5 evidence. But if no one updates that decision note, the PM system will continue treating outdated information as current. meta_state drift is silent failure — the system appears to work while actually pointing to stale conclusions.

/pm-update is the backward pass. After /pm-document creates new decisions and /pm-link connects them, /pm-update propagates the implications: older decisions that now have a `supersedes` relationship should move to `meta_state: outdated`. Issues marked `open` that were resolved this sprint should move to `status: resolved`. Architectural decisions invalidated by new evidence should be flagged.

The update pass is NOT editorial — it is status propagation. It follows the graph of connections and applies the logical consequence of new information to older nodes.

---

## What Triggers Updates

| Trigger | Old Decision Changes |
|---------|---------------------|
| New decision `supersedes` older one | Older → `meta_state: outdated` |
| Sprint record closes an issue | Issue decision → `status: resolved`, `sprint_resolved: N` |
| Evidence invalidates an architectural decision | → `status: invalidated`, add note in body |
| New sprint happened | All decisions with `last_reviewed` older than threshold → flag |
| Tech fact corrected | Old tech-fact → `status: invalidated`, new one → `status: active` |

---

## Workflow

### 1. Identify What Changed

Read the source of the update — either the named decision or recent activity:

```bash
# Find decisions created/modified recently
ls -lt decisions/ | head -20

# Find what supersedes what
rg "supersedes" decisions/ --include="*.md" -l
rg "invalidates" decisions/ --include="*.md" -l
```

### 2. Trace the Impact Graph

For each new decision that supersedes or invalidates something:

1. Read the new decision's `Relevant Notes` section
2. Identify the older decisions referenced
3. Read each older decision
4. Determine the correct status change

### 3. Find Stale Issues

```bash
# Find all open issues
rg "^type: issue" decisions/ --include="*.md" -l | xargs -I{} sh -c 'rg "^status: open" "{}" && echo "{}"'

# Find all in-progress issues
rg "^status: in-progress" decisions/ --include="*.md" -l
```

For each open issue: is there a sprint record that resolved it? Update accordingly.

### 4. Apply Updates

For each decision requiring update:

**Status change:**
```yaml
# Before
status: open
meta_state: current

# After — issue resolved in Sprint 5
status: resolved
sprint_resolved: 5
meta_state: current
last_reviewed: YYYY-MM-DD
```

**Outdated by newer decision:**
```yaml
# Before
status: active
meta_state: current

# After — superseded by newer architectural decision
status: superseded
meta_state: outdated
last_reviewed: YYYY-MM-DD
```

Add a note in the body: "Superseded by [[newer decision]] in Sprint N."

### 5. Update Decision Registers

After updating individual decisions, update the relevant decision registers:
- Move superseded decisions from "Core Decisions" to "History"
- Update "Open Questions" section — remove resolved items
- Update "Tensions" section — resolve or dissolve if applicable

### 6. Output Report

```
## Update Complete

### Decisions Updated
- [[decision A]] — status: open → resolved (Sprint N resolved this)
- [[decision B]] — meta_state: current → outdated (superseded by [[C]])
- [[decision C]] — last_reviewed updated to YYYY-MM-DD

### Registers Updated
- [[issue-register]] — moved 2 issues to resolved section
- [[architecture-register]] — moved 1 decision to History

### Decisions Flagged (Need Attention)
- [[decision D]] — last_reviewed > 14 days, no recent sprint touched it
- [[decision E]] — status: in-progress, no sprint record references it

### Next Steps
- /pm-review [decision D] — stale decision needs review
- /pm-link [decision C] — new superseding decision may have more connections
```

---

## Quality Gates

- Never change a decision status without a documented reason (sprint reference, or newer decision reference)
- Never remove content from decision bodies — only append
- Always update `last_reviewed` when modifying a decision
- Decision registers must accurately reflect the current state of their constituent decisions
