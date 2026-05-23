---
name: ralph-json-create-issues
description: Converts a PRD or plan markdown file into prd.json format for ralph-json-start-loop to execute autonomously. Use when user wants to convert a PRD or plan to JSON stories.
---

# Create PRD JSON

Convert a Product Requirements Document or plan file into JSON for Ralph.

## Input

Check these locations in order:

1. **`.claude/plans/`** — Where plan mode saves approved plans. Primary source.
2. **`plans/`** — Project-level plans directory.
3. **`prds/`** — Standalone PRDs not generated from plan mode.

If files exist in multiple locations, list all and ask which to convert. If only one file is found, use it directly. **If no files are found in any location, ask the user for the path to their PRD/plan file.**

## Conversion Rules

### Story Sizing (Critical)

Each story MUST complete in ONE Ralph iteration (one context window).

**Right-sized:**
- Add a database column
- Create a single UI component
- Add one API endpoint
- Add form validation
- Update a server action

**Too large (must split):**
```
❌ "Build entire auth system"
✅ "Add login form"
✅ "Add email validation"
✅ "Add auth server action"
```

### Dependency Ordering

Stories execute sequentially by priority:
1. Database/schema changes
2. Backend logic
3. API endpoints
4. UI components

### Cross-PRD Dependencies (Critical)

Ralph respects `dependsOn` to sequence PRDs. Before generating JSON:

1. **Scan existing PRDs** — Read all `prds/*.json` to know what features exist
2. **Detect dependencies** — Look for references in the markdown PRD:
   - Explicit: "See `elevenlabs-integration.md`", "Depends on morning brief"
   - Implicit: Story notes mentioning other features
   - Technical: Uses tables/APIs defined in another PRD
3. **Populate `dependsOn`** — Array of PRD names (without `.json` extension)

**Examples of dependency detection:**
```markdown
# In evening-ritual.md:
"See `elevenlabs-integration.md` for shared infrastructure"
→ dependsOn: ["elevenlabs-integration"]

"Depends on morning brief feature for regeneration"
→ dependsOn: ["elevenlabs-integration", "morning-brief"]
```

**If no dependencies detected:**
```json
"dependsOn": []
```

### Acceptance Criteria (Critical)

Must be explicit and verifiable:

**Good:**
```
- Email/password fields present
- Validates email format
- Shows error on invalid input
- Typecheck passes
- Verify at localhost:3000/login
```

**Bad:**
```
- Users can log in (vague)
- Works correctly (vague)
- Good UX (subjective)
```

**Required in every story:**
- "Typecheck passes"
- "Lint passes"

**Required for UI stories:**
- "Verify at localhost:3000/[path]"

## Output Format

Generate `prds/[feature-name].json`:

```json
{
  "projectName": "Feature Name",
  "branchName": "ralph/feature-name",
  "description": "Brief description",
  "dependsOn": ["other-feature", "another-feature"],
  "status": "pending",
  "completedAt": null,
  "userStories": [
    {
      "id": "US-001",
      "title": "Add login form",
      "description": "As a user, I want to see a login form so I can authenticate",
      "acceptanceCriteria": [
        "Email/password fields present",
        "Form submits on enter",
        "Typecheck passes",
        "Lint passes",
        "Verify at localhost:3000/login"
      ],
      "priority": 1,
      "passes": false,
      "notes": ""
    }
  ]
}
```

## Process

1. **Scan existing PRDs** — Read `prds/*.json` to understand the dependency landscape
2. Read the PRD/plan markdown file from `.claude/plans/`, `plans/`, or `prds/`
3. Derive feature name from filename (e.g., `auth-flow.md` → `auth-flow`)
4. **Detect dependencies** — Check for references to other PRDs in the markdown
5. Break into right-sized stories starting at US-001
6. Order by dependency (set priority)
7. Add explicit acceptance criteria
8. Save to `prds/[feature-name].json`

## Pre-Save Checklist

Before saving, verify:
- [ ] Each story completable in one iteration
- [ ] Stories ordered by dependency
- [ ] All criteria include "Typecheck passes"
- [ ] UI stories include "Verify at localhost:3000/..."
- [ ] No vague criteria ("works", "good", "correct")
- [ ] Story IDs are sequential (US-001, US-002, ...)
- [ ] `dependsOn` is populated (empty array if no dependencies)
- [ ] Dependencies reference existing PRD names (without extension)

## After Conversion

```
Created prds/[feature-name].json with [N] stories
Dependencies: [list or "none"]
Branch: ralph/[feature-name]

Run: /ralph-json-start-loop
```
