---
name: versioning-constitutions
description: Use when architectural patterns evolve, tech stack changes, or foundational rules need updates - creates new constitution version directory, migrates/organizes content into modular files, updates symlink, and documents changes
---

# Versioning Constitutions

## Core Principle

**Constitution versions are immutable snapshots of architectural truth.**

When foundational rules change (patterns, tech stack, architecture), create a new version rather than editing in place. This preserves history, enables rollback, and makes changes explicit.

## When to Use This Skill

**ALWAYS create a new version when:**
- Adding a new mandatory pattern (e.g., adopting effect-ts for error handling)
- **Removing OR relaxing a mandatory pattern** (e.g., making next-safe-action optional)
- Changing tech stack (e.g., migrating from Prisma to Drizzle)
- Updating architectural boundaries (e.g., adding new layer)
- Deprecating rules that are no longer valid
- Major library version changes with breaking patterns (e.g., Next.js 15 → 16)

**CRITICAL:** Removing or relaxing a mandatory pattern ALWAYS requires a new version, even if existing code would still work. "Non-breaking" is not sufficient - any change to mandatory patterns needs versioning for audit trail.

**Do NOT use for:**
- Fixing typos or clarifying existing rules (edit current version directly)
- Adding examples to existing patterns (edit current version directly)
- Project-specific implementation details (those go in specs/)

**Test for Constitutionality:**

Before adding content to constitution, ask: "If we violate this rule, does the architecture break?"
- ✅ Constitutional: "Must use next-safe-action" → violating breaks type safety & validation
- ❌ Not constitutional: "Forms should have wrapper, fields, button" → violating just looks different

**Constitution = Architectural rules. Specs = Implementation patterns.**

## Process

### Step 1: Determine Version Number

Read `docs/constitutions/current/meta.md` to get current version.

**Version increment rules:**
- Increment by 1 (v1 → v2, v2 → v3)
- No semantic versioning (major.minor.patch)
- Sequential only

### Step 2: Create New Version Directory

```bash
# Create new version directory
mkdir -p docs/constitutions/v{N}

# Copy structure from current
cp docs/constitutions/current/*.md docs/constitutions/v{N}/
```

### Step 3: Update Content

Edit files in new version directory with changes:
- `meta.md` - Update version number, date, changelog
- `architecture.md` - Update if architectural boundaries changed
- `patterns.md` - Update if mandatory patterns changed
- `tech-stack.md` - Update if libraries added/removed
- `schema-rules.md` - Update if database philosophy changed
- `testing.md` - Update if testing requirements changed

**Critical - Minimal Changes Only:**
- Only change what NEEDS changing for this version
- NO reorganizing sections ("while I'm here")
- NO reformatting code examples
- NO alphabetizing lists
- NO renaming headings for style
- NO creating new categories unless absolutely required

The diff should show ONLY the substantive change, not stylistic improvements.

### Step 4: Update Symlink

```bash
# Remove old symlink
rm docs/constitutions/current

# Create new symlink pointing to new version
ln -s v{N} docs/constitutions/current
```

### Step 5: Verify References

Check that all references still work:

```bash
# Find all references to constitutions
grep -r "@docs/constitutions/current" .claude/
grep -r "docs/constitutions/current" .claude/
```

All references should use `current/` symlink, never hardcoded versions.

### Step 6: Document in meta.md

**MANDATORY:** Update `meta.md` with complete documentation:
- New version number (e.g., "Version: 2")
- Creation date (e.g., "Created: 2025-01-17")
- Previous version reference (e.g., "Previous: v1")
- **Summary of WHAT changed** (e.g., "Removed Redux prohibition")
- **Rationale for WHY** (e.g., "React Server Components handle all state needs, Redux adds complexity without benefit")

**The WHY is critical.** In 6 months, the context will be lost. Document:
- What problem does this change solve?
- What decision or discussion led to this?
- Why now vs earlier/later?

DO NOT rely on git commit messages or external docs. meta.md must be self-contained.

## Quality Checklist

Before updating symlink:
- [ ] New version directory exists at `docs/constitutions/v{N}/`
- [ ] All 6 files present (meta, architecture, patterns, tech-stack, schema-rules, testing)
- [ ] `meta.md` has correct version number and changelog
- [ ] Changes documented with rationale (why, not just what)
- [ ] Old version remains untouched (immutable)
- [ ] References in commands use `current/` not `v{N}/`

## Common Mistakes

### Mistake 1: Editing Current Version for Breaking Changes
**Wrong:** Edit `docs/constitutions/current/patterns.md` directly when removing next-safe-action requirement

**Right:** Create v2, update patterns.md in v2, update symlink

**Why:** Breaking changes need versioning. Commands/specs may reference old patterns.

### Mistake 2: Hardcoding Version in References
**Wrong:** `@docs/constitutions/v2/architecture.md`

**Right:** `@docs/constitutions/current/architecture.md`

**Why:** When v3 is created, all references break. Symlink abstracts version.

### Mistake 3: Reorganizing for Style
**Wrong:** "Let me alphabetize sections and rename files while versioning"

**Right:** Only change content that needs substantive updates

**Why:** Gratuitous changes obscure what actually changed. Diff should show real changes.

### Mistake 4: Forgetting to Update meta.md
**Wrong:** Copy files, update content, update symlink, done

**Right:** Update meta.md with version, date, and changelog

**Why:** Future you won't remember why version changed. Document the why.

### Mistake 5: Versioning Implementation Details
**Wrong:** Create v2 because we changed button component structure

**Right:** Constitution = foundational rules only. Implementation goes in specs/

**Why:** Constitution is for patterns/architecture/stack, not implementation choices.

### Mistake 6: Rationalizing In-Place Edits
**Wrong:** "This change is non-breaking, so I can edit v1 in-place per the meta.md guidance"

**Right:** Removing/relaxing ANY mandatory pattern requires versioning, even if "non-breaking"

**Why:** Audit trail matters more than technical breaking changes. Future readers need to know WHEN rules changed, not just that they did. Git history is not sufficient - constitution versions create explicit snapshots.

## Quick Reference

```bash
# Check current version
cat docs/constitutions/current/meta.md

# Create new version
mkdir -p docs/constitutions/v{N}
cp docs/constitutions/current/*.md docs/constitutions/v{N}/

# Edit content
# Update meta.md, then other files as needed

# Update symlink
rm docs/constitutions/current
ln -s v{N} docs/constitutions/current

# Verify
ls -la docs/constitutions/current
grep -r "constitutions/v[0-9]" .claude/  # Should return nothing
```

## Example: Adding New Pattern

Scenario: We're adopting `effect-ts` for error handling and deprecating throw/catch.

**Step 1:** Current version is v1 (read meta.md)

**Step 2:** Create v2
```bash
mkdir -p docs/constitutions/v2
cp docs/constitutions/current/*.md docs/constitutions/v2/
```

**Step 3:** Update content
- `meta.md`: Version 2, date, "Added effect-ts error handling pattern"
- `patterns.md`: Add new section on Effect error handling
- `tech-stack.md`: Add effect-ts to approved libraries
- Leave other files unchanged

**Step 4:** Update symlink
```bash
rm docs/constitutions/current
ln -s v2 docs/constitutions/current
```

**Step 5:** Verify references (should all use `current/`)

**Step 6:** meta.md documents why (type-safe error handling, eliminate throw)

## Testing This Skill

See `test-scenarios.md` for pressure scenarios and RED-GREEN-REFACTOR tests.
