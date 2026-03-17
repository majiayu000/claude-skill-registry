---
name: updating-documentation
description: Update existing project documentation to reflect changes made during a session. Analyzes what changed in code and surgically updates only affected documentation. Use when (1) a coding session has modified component behavior or interfaces, (2) implementation work is complete and docs need to stay in sync, (3) refactoring changed patterns or conventions, or (4) code was deleted and docs may reference removed things. Run at the end of a session — "when it's all said and done."
---

# Updating Documentation

Surgically update existing documentation to reflect changes made during a coding session. Run this **after implementation work is complete** — when it's all said and done.

## Core Principles

1. **Surgical Updates**: Only touch documentation affected by the session's changes. Never rewrite unrelated docs.
2. **Change-Driven**: Start from what changed (git diff, modified files), then trace to affected docs. Never explore the codebase looking for things to update.
3. **Preserve Style**: Match the existing documentation's tone, format, and level of detail.
4. **No Fabrication**: Only document changes you can verify. Don't speculate about intent or future plans.
5. **Minimal Disruption**: Small, precise edits over wholesale rewrites.
6. **Respect the Hierarchy**: Changes may affect docs at multiple levels. A renamed domain entity needs updates in domain docs, which may cascade to architecture, process, and component docs that reference it. Always update from the top down.

## Documentation Hierarchy

This skill updates documentation across all levels. When tracing affected docs, check every level:

```
Domain              ← Entity definitions, terminology, domain rules
  ↓
Architecture        ← System structure, design decisions, layer boundaries
  ↓
Business Processes  ← End-to-end workflows, failure scenarios
  ↓
Components          ← Module internals, interfaces, behavior
```

A single code change can affect multiple levels. For example, renaming a domain entity touches domain docs (definition), architecture docs (references), process docs (flow descriptions), and component docs (interface signatures).

## Workflow

### Step 1: Identify What Changed

1. Review the session's changes (`git diff`, modified/created/deleted files)
2. Categorize changes by documentation impact:
   - **New components**: May need new documentation (flag for docs-writer)
   - **Modified interfaces**: Existing docs may describe old signatures
   - **Behavioral changes**: Existing docs may describe old behavior
   - **Deleted code**: Docs may reference things that no longer exist
   - **New patterns or conventions**: May need documenting if they deviate from existing norms

### Step 2: Find Affected Documentation

1. Read AGENTS.md for documentation pointers
2. Search existing docs for references to changed components, functions, types, or files
3. Check if changed files have associated documentation (e.g., `docs/auth.md` for `src/auth/`)
4. Identify docs that describe interfaces, behaviors, or patterns that were modified

**If no documentation exists for the changed areas**, skip to Step 4 — there's nothing to update.

### Step 3: Make Targeted Updates

For each affected doc:

1. **Read the current doc** to understand what it says
2. **Compare against the changes** to identify what's now wrong or incomplete
3. **Make surgical edits** — update specific sections, don't rewrite the whole file
4. **Add new sections** only if the changes introduced genuinely new concepts within the existing component's scope

Types of updates:

| Change Type | Doc Update |
|---|---|
| Interface change (signatures, params, returns) | Update the Key Interfaces section |
| Behavioral change (logic, flow, error handling) | Update descriptions of how things work |
| New dependency added | Update the Dependencies section |
| Dependency removed | Remove stale references |
| Pattern change (new convention adopted) | Update the Patterns & Conventions section |
| Code deleted | Remove references to removed components |

### Step 4: Handle Documentation Gaps

If the session's changes introduced undocumented areas:

1. **Do not write full docs** — that's the job of the appropriate documenting skill
2. **Flag the gap with a specific recommendation**:
   - New domain concepts introduced → recommend `documenting-domain`
   - Architectural changes (new layers, patterns) → recommend `documenting-architecture`
   - New business workflows → recommend `documenting-business-processes`
   - New modules or components → recommend `documenting-components`
3. **Update AGENTS.md pointers** only if new doc files were actually created in this session

### Step 4.5: Check for Duplication

While updating, watch for concepts that are duplicated across documentation levels:

1. If a domain term is redefined in component docs, consolidate to domain docs and replace with a reference
2. If an architectural pattern is re-explained in process docs, consolidate to architecture docs and replace with a reference
3. Flag any duplication found to the user — don't silently reorganize large sections

### Step 5: Verify Consistency

After updates:

1. Check that AGENTS.md pointers still point to valid files
2. Ensure no docs reference removed code or renamed interfaces
3. Confirm updated docs accurately reflect the new state

## Integration with Other Skills

This skill is designed to run **after other work completes**:

- **After plan execution**: When an agent finishes implementing a sub-plan, run this to keep documentation in sync
- **After refactoring**: When code structure changes, docs referencing old structure need updates
- **After bug fixes**: If the fix changed documented behavior or revealed incorrect documentation

This skill does **not** create documentation from scratch — it only updates what exists. For undocumented areas, recommend the appropriate documenting skill:
- `documenting-domain` — for business concepts and terminology
- `documenting-architecture` — for system design and structure
- `documenting-business-processes` — for end-to-end business workflows
- `documenting-components` — for specific modules and interfaces

## Rules

- **Never rewrite docs that weren't affected by the session's changes**
- **Never create comprehensive documentation from scratch** — that's the docs-writer's job; only make targeted updates here
- **Always start from the diff** — changes drive updates, not exploration
- **Preserve the original author's voice** — edit surgically, don't rewrite
- **Flag gaps, don't fill them** — if something needs full documentation, recommend docs-writer instead
- **No meta-commentary** — don't add "updated by AI" or session timestamps to docs
