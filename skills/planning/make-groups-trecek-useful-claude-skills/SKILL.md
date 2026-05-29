---
name: make-groups
description: Break a large plan, architecture proposal, or feature document into sequenced implementation groups for the make-plan pipeline. Use when user says "make groups", "group requirements", "sequence groups", or wants to decompose a large document into ordered implementation units.
hooks:
  PreToolUse:
    - matcher: "*"
      hooks:
        - type: command
          command: "echo 'Decomposing into sequenced implementation groups...'"
          once: true
---

# Implementation Group Decomposition Skill

Break a large document — architecture proposal, feature spec, migration plan, or requirements set — into self-contained implementation groups ordered for sequential execution through the make-plan pipeline.

## When to Use

- User says "make groups", "group requirements", "sequence groups", "decompose into groups"
- User has a large document with many requirements/features that must be implemented incrementally
- User wants to feed groups one at a time through `/make-plan`

## Core Principles

- **Groups are implementation units, not categories.** Each group must be independently plannable and implementable. A group produces a working, testable increment.
- **Requirements travel with their group.** Every requirement from the source document must appear in exactly one group, referenced by its original ID. No requirement is dropped or split.
- **Dependency order is the sequencing rule.** Group A's output is available when Group B starts. Order by what produces foundations first, consumers last.
- **Source material is unverified input.** Verify claims about the codebase against subagent findings before incorporating them into grouping decisions.

## Critical Constraints

**NEVER:**
- Modify any source code files
- Create files outside `temp/make-groups/` directory
- Drop, split, or rewrite requirements — reference them by original ID
- Create groups that cannot be independently planned
- Include implementation steps or technical approach in the group descriptions

**ALWAYS:**
- Use subagents to verify codebase structure before finalizing groups
- Include every requirement from the source document in exactly one group
- Assign each group a sequential suffix: groupA, groupB, ... groupZ
- State dependencies between groups explicitly
- Write to `temp/make-groups/` directory

## Workflow

### Step 1: Read the Source Document

Read the full document. Inventory every requirement (REQ-*), feature, and deliverable. Build a raw list with original IDs preserved.

### Step 2: Verify Against Codebase

Launch **parallel Explore subagents** to understand:

- What exists today that the requirements relate to
- Module boundaries and dependency directions
- Which components are foundational vs. consumers

### Step 3: Form Groups

Cluster requirements into groups. Each group must:

1. Be independently plannable — someone could take this group to `/make-plan` without needing other groups implemented first (except declared dependencies)
2. Produce a working increment — after implementation, the system is in a valid state
3. Contain all related requirements — no requirement is orphaned or deferred

Name each group with a short descriptive label and assign suffix groupA through groupZ in implementation order.

### Step 4: Order by Dependency

Sort groups so that each group's dependencies are satisfied by earlier groups. Document the dependency chain explicitly.

### Step 5: Write the Groups Documents

Produce three outputs in `temp/make-groups/`:

**5a. Index file (consolidated):** `groups_{topic}_{YYYY-MM-DD_HHMMSS}.md`

```markdown
# Implementation Groups: {Topic}

**Date:** {YYYY-MM-DD}
**Source:** {Document path or description}
**Groups:** {count}

## Per-Group Files

- `groupA_{topic}_{ts}.md`
- `groupB_{topic}_{ts}.md`
- ...

## Manifest

`manifest_{topic}_{ts}.json`

## Dependency Chain

{group_id} → {group_id} → ... (linear or DAG as needed)

---

## {Group Label} (groupA)

### Purpose
{What this group delivers and why it comes at this position in the sequence}

### Dependencies
{None, or list of group IDs that must be complete first}

### Requirements
- **REQ-XXX-001:** {Original requirement text}
- **REQ-XXX-002:** {Original requirement text}
- ...

### Planning Context
{What make-plan needs to know: affected modules, key interfaces, constraints. Factual only — no prescribed approach.}

---

## {Group Label} (groupB)

{Same structure}

---

{Repeat for each group}

## Traceability

| Requirement | Group |
|-------------|-------|
| REQ-XXX-001 | groupA |
| REQ-XXX-002 | groupA |
| REQ-YYY-001 | groupB |
| ... | ... |
```

**5b. Per-group files:** `groupA_{topic}_{ts}.md`, `groupB_{topic}_{ts}.md`, etc.

Each per-group file contains the group's section extracted from the index — one self-contained file per group for pipeline consumption:

```markdown
# {Group Label} (groupA)

## Purpose
{What this group delivers}

## Dependencies
{None, or list of group IDs}

## Requirements
- **REQ-XXX-001:** {text}
- **REQ-XXX-002:** {text}

## Planning Context
{What make-plan needs to know}
```

**5c. Manifest file:** `manifest_{topic}_{ts}.json`

Machine-readable manifest for pipeline orchestration:

```json
{
    "topic": "{topic}",
    "date": "{YYYY-MM-DD}",
    "source": "{document path}",
    "group_count": 7,
    "dependency_chain": ["groupA", "groupB", "groupC"],
    "groups": [
        {
            "id": "groupA",
            "label": "{Group Label}",
            "file": "groupA_{topic}_{ts}.md",
            "dependencies": [],
            "requirements": ["REQ-XXX-001", "REQ-XXX-002"]
        }
    ],
    "index_file": "groups_{topic}_{ts}.md"
}
```

### Step 6: Verify Completeness

Before finalizing, check:

- Every requirement from the source document appears in the traceability table
- No requirement appears in more than one group
- No group depends on a group that comes after it in the sequence
- Each group is self-contained enough to be a `/make-plan` input
- Per-group file count matches group count in manifest
- All per-group files are written to disk

Report to terminal: index file path, manifest file path, per-group file count, and the dependency chain.

## Output Location

```
temp/make-groups/
├── groups_{topic}_{ts}.md           # Consolidated index (all groups)
├── manifest_{topic}_{ts}.json       # Machine-readable manifest
├── groupA_{topic}_{ts}.md           # Individual per-group file
├── groupB_{topic}_{ts}.md
└── ...
```

## Feature Branch Recommendation

When implementing multiple groups from this skill's output, **always work on a feature branch**, not directly on `main`. Group implementations take multiple plan-implement-merge cycles and should not land on the base branch until the full set is complete.

After `make-groups` completes, create a feature branch before starting the pipeline:

```bash
git checkout -b feature/{topic}
```

Then run each group through `/make-plan` → `/dry-walkthrough` → `/implement-worktree` using the feature branch as the base branch for all merge operations.

## Related Skills

- **`/make-req`** — Produces requirements from raw input (this skill groups existing requirements)
- **`/make-plan`** — Consumes individual groups as planning input
- **`/audit-impl`** — Audits the full implementation against all group plans before final merge
- **`/elaborate-phase`** — Elaborates phases within a plan (this skill creates the groups that become plans)
- **`/dry-walkthrough`** — Validates plans produced from groups
