---
name: plant-seed
description: "Capture forward-looking idea as a seed for future feature design."
user-invocable: false
argument-hint: "<idea description>"
command: /plant-seed
allowed-tools:
  - Read
  - Write
  - Bash
  - Grep
  - Glob
  - Edit
routing:
  triggers:
    - plant seed
    - save idea for later
    - defer this idea
    - remember this for when
    - seed this
    - plant-seed
  pairs_with:
    - feature-lifecycle
  complexity: Simple
  category: process
---

# Plant Seed Skill

## Overview

Capture forward-looking ideas with trigger conditions so they resurface at the right time. Seeds carry WHY (rationale) and WHEN (trigger), making them far more valuable than bare TODO comments.

Seeds are stored locally in `.seeds/` (gitignored) and automatically surfaced during feature-lifecycle design phase when their trigger conditions match. This workflow is designed for deferred ideas only — if the user describes work that should happen now, suggest creating a task or issue instead.

---

## Instructions

### Phase 1: CAPTURE

**Goal**: Gather the idea, trigger condition, scope, and rationale from the user.

**Key Constraint**: This skill captures deferred ideas only. If the user describes something that should happen in the current session, suggest creating a task or issue instead. Planting a seed for immediate work means it never gets surfaced — it just gets forgotten in a different way.

**Step 1: Understand the idea**

Extract from the user's description:
- **What** (action): The specific thing to do when the time is right
- **Why** (rationale): The insight or observation that motivates this idea
- **When** (trigger): A human-readable string describing when this becomes relevant

If the user provides all three, proceed. If any are missing, ask:

For missing **trigger condition**:
> When should this idea resurface? Describe the condition, e.g.:
> - "when we add user accounts"
> - "when performance optimization is needed"
> - "when the API exceeds 10 endpoints"

For missing **scope**:
> How big is this work? Small (< 1 hour), Medium (1-4 hours), or Large (4+ hours)?

For missing **rationale**:
> Why does this matter? What's the insight behind this idea? (e.g., "Response times degrade linearly with DB calls per request -- at 10+ endpoints the shared query pattern becomes the bottleneck")

**Step 2: Generate seed ID**

Format: `seed-YYYY-MM-DD-slug`
- Date is today's date
- Slug is a short kebab-case summary of the action (3-5 words max)

Example: `seed-2026-03-22-cache-layer`

Seeds use this consistent ID format to ensure uniqueness and chronological sorting. If two seeds are planted the same day with the same slug, append `-2`, `-3` to the slug.

**Step 3: Discover breadcrumbs**

**Key Constraint**: Breadcrumbs preserve code references from capture time. Even if the codebase evolves, these paths help the user re-orient when the seed surfaces months later. Always grep for related files at capture time.

Search the codebase for files related to the seed's topic. Use the Grep tool with 2-3 key terms from the seed's action and rationale. Collect up to 10 file paths as breadcrumbs.

If no files match, breadcrumbs can be empty — the seed is still valuable without them.

**Gate**: Idea captured with all required fields (action, trigger, scope, rationale). Breadcrumbs discovered. Proceed to Confirm.

### Phase 2: CONFIRM

**Goal**: Show the complete seed to the user and get approval before writing.

Present the seed:

```
## Seed: seed-YYYY-MM-DD-slug [Scope]

Trigger: "human-readable trigger condition"
Rationale: Why this matters...
Action: What to do when triggered...
Breadcrumbs: file1.go, file2.py, ...

Plant this seed? [yes/no/edit]
```

Handle response:
- **yes**: Proceed to Write
- **no**: Discard and confirm the seed was not saved
- **edit**: Ask what to change, update fields, re-confirm

**Gate**: User approved the seed. Proceed to Write.

### Phase 3: WRITE

**Goal**: Persist the seed to `.seeds/index.json`.

**Key Constraint**: Seeds go in `.seeds/` which is gitignored — seeds are personal, not shared via version control. Different developers have different ideas and different trigger conditions; committing seeds pollutes the shared repo with personal notes.

**Step 1: Ensure directory exists**

```bash
mkdir -p .seeds/archived
```

**Step 2: Read or initialize index.json**

If `.seeds/index.json` exists, read it. Otherwise, initialize:

```json
{
  "seeds": []
}
```

**Step 3: Append seed**

Add the new seed to the `seeds` array:

```json
{
  "id": "seed-YYYY-MM-DD-slug",
  "status": "dormant",
  "planted": "YYYY-MM-DD",
  "trigger": "human-readable trigger condition",
  "scope": "Small|Medium|Large",
  "rationale": "Why this matters...",
  "action": "What to do when triggered...",
  "breadcrumbs": ["path/to/file1.go", "path/to/file2.py"]
}
```

**Step 4: Write updated index.json**

Write the complete updated index back to `.seeds/index.json`.

**Step 5: Confirm to user**

```
Seed planted: seed-YYYY-MM-DD-slug [Scope]
Trigger: "condition"
Status: dormant

This seed will surface automatically during /feature-lifecycle (design phase) when the
trigger condition matches. Review all seeds with: /plant-seed "list seeds"
```

**Gate**: Seed persisted to `.seeds/index.json`. Workflow complete.

---

### Seed Review Mode

When the user asks to "list seeds", "review seeds", or "show my seeds":

1. Read `.seeds/index.json`
2. Display all dormant seeds:

```
## Dormant Seeds (N total)

| ID | Scope | Trigger | Planted |
|----|-------|---------|---------|
| seed-2026-03-22-cache-layer | Medium | when the API exceeds 10 endpoints | 2026-03-22 |
| seed-2026-03-20-user-auth | Large | when we add user accounts | 2026-03-20 |
```

3. Offer actions: "Want to activate, dismiss, or edit any seed?"

### Seed Lifecycle Actions

**Harvest**: Move seed to `.seeds/archived/{seed-id}.json`, set status to `harvested`. Use when the seed's work has been incorporated into a feature.

**Dismiss**: Move seed to `.seeds/archived/{seed-id}.json`, set status to `dismissed`. Use when the seed is no longer relevant.

**Activate**: Change status from `dormant` to `active` in index.json. Use when the trigger condition has been met but work hasn't started yet.

To archive: remove the seed from `index.json` and write it as a standalone file to `.seeds/archived/{seed-id}.json`.

---

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `.seeds/` directory doesn't exist | First seed being planted | Create directory with `mkdir -p .seeds/archived` |
| `index.json` is malformed | Manual edit or corruption | Back up to `index.json.bak`, reinitialize with empty seeds array, warn user |
| Duplicate seed ID | Two seeds planted same day with same slug | Append `-2`, `-3` to slug |
| No breadcrumbs found | Idea is forward-looking, no related code yet | Plant with empty breadcrumbs -- still valuable |
| User describes immediate work | Seed system is for deferred work | Suggest creating a task or doing the work now |
| Vague trigger like "someday" or "eventually" | Cannot be matched during feature-lifecycle design phase | Ask for a specific, observable condition |
| Missing rationale ("it would be nice") | Without WHY, the seed loses value when surfaced months later | Capture the specific insight or observation |

---

## References

- [Feature Lifecycle](../feature-lifecycle/SKILL.md) - Seeds are surfaced during feature-lifecycle design phase (Phase 0)
