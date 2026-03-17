---
name: methodology-spec-evolution
description: Guides evolution of book-llms/ methodology specification files with cross-file consistency. Handles version bumps, terminology propagation, and backward compatibility checks. Use when modifying any file in book-llms/ — the highest error-risk activity in this project.
protocol_id: PROTO-ORG-3
protocol_file: organon/protocols/PROTOCOLS.md
tools: [organon-verify, organon-find, organon-health]
loads:
  - book-llms/ETHOS.md
  - book-llms/PHILOSOPHY.md
  - book-llms/overview.md
  - CLAUDE.md
---

# Methodology Spec Evolution Workflow

> Implements PROTO-ORG-3 from `organon/protocols/PROTOCOLS.md`. Ensures cross-file consistency when evolving the methodology specification.

---

## When to Use This Skill

Use this skill when:
- **Modifying any file in `book-llms/`** — specification changes
- **Adding a new concept** to the methodology
- **Changing terminology** across the specification
- **Updating the frontmatter schema** or template structure
- **Adding or modifying patterns** in patterns.md

**Purpose:** Methodology changes are the highest error-risk activity. A change to one file typically requires propagation to 3-6 other files. This workflow prevents drift.

---

## Context Loading

1. Load meta-organon constraints:
   - Read `book-llms/ETHOS.md` (invariants governing all organon creation)
   - Read `book-llms/PHILOSOPHY.md` (reasoning behind methodology design)
2. Load overview for cross-reference baseline:
   - Read `book-llms/overview.md` (high-level methodology overview)
3. Load project constraints:
   - Read `CLAUDE.md` (project-level guidance that must stay in sync)

---

## Steps

### Step 1: Assess Impact

Before making any changes, understand the blast radius:

Use the Grep tool to search for the concept across all project files:

```
Grep pattern="<concept-being-changed>" path="."
```

Also check which organon files relate by name:

```bash
cd packages/tools && npx organon find --name "<concept>"
```

Every file returned is a potential propagation target.

**Known high-propagation files:**
- `book-llms/ETHOS.md` changes → affects templates.md, frontmatter-system.md, patterns.md, scopes.md, overview.md, CLAUDE.md
- `book-llms/frontmatter-system.md` changes → affects templates.md, ETHOS.md (structure templates), packages/tools parsers
- `book-llms/three-layer-architecture.md` changes → affects workflow-authoring.md, templates.md, patterns.md
- Terminology changes → grep ALL files including CLAUDE.md, README.md, skill files

### Step 2: Check Backward Compatibility

Ask: Will this change break existing organon implementations in other projects?

| Change Type | Backward Compatible? | Action |
|-------------|---------------------|--------|
| Adding new optional frontmatter field | Yes | Proceed |
| Adding new required frontmatter field | No | Requires RFC + major version bump |
| Changing field semantics | No | Requires RFC + major version bump |
| Adding new pattern or anti-pattern | Yes | Proceed |
| Removing or renaming a pattern | No | Requires deprecation period |
| Adding new section to template | Yes (if optional) | Proceed |
| Changing required section structure | No | Requires RFC + major version bump |

If not backward compatible: STOP. Create an RFC (use `domain-feature-design` skill) before proceeding.

### Step 3: Make Primary Change

Edit the target file in `book-llms/`. Follow section structure from `book-llms/ETHOS.md`.

### Step 4: Propagate to Related Files

Check and update each of these files in order:

1. **`book-llms/scopes.md`** — Known to lag behind core concept changes. If scope definitions changed, update here first.

2. **`book-llms/templates.md`** — If structure templates changed, update the corresponding template scaffold. Must match ETHOS.md structure templates exactly.

3. **`book-llms/frontmatter-system.md`** — If frontmatter schema changed, update the detailed schema. Must match ETHOS.md and templates.md.

4. **`book-llms/patterns.md`** — If patterns or anti-patterns changed, update the catalog. Note: ETHOS.md and patterns.md anti-pattern tables are intentionally divergent (~11 shared, ~6 unique each).

5. **`book-llms/overview.md`** — If high-level concepts changed, update the overview.

6. **`CLAUDE.md`** — If project-level guidance changed, update CLAUDE.md. This is the agent-facing entry point and must stay authoritative.

### Step 5: Bump Versions

Update the `version` field in YAML frontmatter of **ALL** modified files:
- Minor bump (e.g., "1.0" → "1.1") for additive changes
- Major bump (e.g., "1.1" → "2.0") for breaking changes

**Common mistake:** Only bumping the primary file's version. ALL modified files must be bumped.

### Step 6: Grep for Stale Terminology

Search ALL files for old terminology that should have been updated:

Use the Grep tool to search all files for old terminology:

```
Grep pattern="<old-term>" path="."
```

Also check organon files by name:

```bash
cd packages/tools && npx organon find --name "<old-term>"
```

Additionally, manually check common stale term locations:
- Check CLAUDE.md
- Check README.md (project root)
- Check all skill files in `.claude/skills/`
- Check organon/ self-governance files

### Step 7: Run Full Verification

```bash
cd packages/tools && npx organon verify
cd packages/tools && npx organon health
```

All gates must pass. Health score should not decrease.

---

## Cross-File Consistency Checklist

After any methodology change, verify:

- [ ] `scopes.md` uses same terminology as ETHOS.md
- [ ] `templates.md` structure matches ETHOS.md structure templates
- [ ] `frontmatter-system.md` schema matches templates.md scaffolds
- [ ] `patterns.md` references current concepts (not stale ones)
- [ ] `overview.md` reflects the current state of the methodology
- [ ] `CLAUDE.md` invariants match `organon/ETHOS.md` invariants
- [ ] All modified files have bumped version numbers
- [ ] No old terminology found in grep sweep

---

## Verification

- [ ] All modified files have bumped version numbers
- [ ] `organon verify` passes all gates
- [ ] `organon health` score has not decreased
- [ ] No stale terminology found in grep sweep
- [ ] scopes.md is in sync with core concept changes
- [ ] Cross-file consistency checklist passes

---

## Error Recovery

| Failure | Recovery Action |
|---------|-----------------|
| Stale terminology found after commit | Run full grep sweep again (Grep tool across project root). Update all remaining instances. |
| scopes.md out of sync | Re-read scopes.md alongside ETHOS.md. Update scopes.md to match current concepts. |
| Version not bumped in a modified file | Check git diff for all files touched. Bump version in any file that was modified but not version-bumped. |
| Backward compatibility broken unintentionally | Assess impact. If minor, document in CHANGELOG. If major, create RFC and bump major version. |
| `organon verify` fails after changes | Fix reported issues. Most common: frontmatter counts not updated after adding/removing invariants. |
| templates.md diverges from ETHOS.md | ETHOS.md is source of truth for structure templates. Update templates.md to match. |
| patterns.md anti-pattern table confusion | Remember: ETHOS.md covers organon authoring mistakes; patterns.md covers broader project anti-patterns. ~11 shared, ~6 unique each. Don't force full sync. |
