---
name: docs-verify
description: Documentation verification for 3-Tier system - validates line limits, cross-references, file counts
---

# SKILL: Documentation Verification

> **Purpose**: Validate 3-Tier documentation system compliance - line limits, cross-references, file counts

---

## Quick Start

### When to Use

- After closing plan (`/03_close`)
- After running `/document`
- Before committing documentation changes

### Quick Reference

```bash
# Pure bash link check (no external deps)
for file in CLAUDE.md docs/ai-context/*.md; do
  [ -f "$file" ] || continue
  grep -oE '@[^][:space:]]+' "$file" | while read ref; do
    ref_path="${ref#@}"
    [ ! -e "$ref_path" ] && echo "Broken: $ref in $file"
  done
done
```

---

## Change Detection (MANDATORY FIRST STEP)

**Before running verification, check if docs changed**:

```bash
# Get changed markdown files (with fallback)
CHANGED_MD=$(git diff --name-only HEAD~1 -- "*.md" 2>/dev/null || git diff --name-only -- "*.md" 2>/dev/null || echo "FALLBACK_FULL_VERIFY")

# Fallback: If git diff fails, run full verification
if [ "$CHANGED_MD" = "FALLBACK_FULL_VERIFY" ]; then
    echo "Cannot detect changes, running full verification"
    CHANGED_MD=$(find . -name "*.md" -type f ! -path "*/.git/*" ! -path "*/.trash/*")
fi

if [ -z "$CHANGED_MD" ]; then
    echo "No markdown files changed"
    echo "Skipping documentation verification"
    exit 0
fi

echo "Changed markdown files:"
echo "$CHANGED_MD"
```

---

## Core Concepts

### 3-Tier System

**Tier 1** (3 files, ≤200 lines each):
- `CLAUDE.md` - Project architecture, features, Quick Start
- `docs/ai-context/project-structure.md` - Tech stack, file tree
- `docs/ai-context/docs-overview.md` - Documentation navigation

**Tier 2**: Component CONTEXT.md files (unlimited)

**Tier 3**: Feature-specific CONTEXT.md files

---

## Verification Checks

### 1. Tier 1 Line Limits (Changed Files Only)

**Limit**: ≤200 lines per file

```bash
TIER1_FILES=(
  "CLAUDE.md"
  "docs/ai-context/project-structure.md"
  "docs/ai-context/docs-overview.md"
)

for file in "${TIER1_FILES[@]}"; do
  # Only check if file was changed
  if echo "$CHANGED_MD" | grep -q "$file"; then
    LINES=$(wc -l < "$file" | tr -d ' ')
    if [ "$LINES" -gt 200 ]; then
      echo "FAIL: $file has $LINES lines (limit: 200)"
      exit 1
    fi
    echo "$file: $LINES lines"
  fi
done
```

**On violation**: Extract content to Tier 2 CONTEXT.md files

### 2. Tier 1 File Count (CRITICAL)

**Limit**: Exactly 2 files in `docs/ai-context/`

```bash
COUNT=$(find docs/ai-context -maxdepth 1 -name "*.md" -type f | wc -l | tr -d ' ')
if [ "$COUNT" -ne 2 ]; then
  echo "FAIL: docs/ai-context/ has $COUNT files (expected: 2)"
  exit 1
fi
```

### 3. Cross-Reference Validation (Changed Files Only)

```bash
# Only validate changed files
for file in $CHANGED_MD; do
  [ -f "$file" ] || continue
  grep -oE '@\.(claude|docs)/[^][:space:]]+' "$file" 2>/dev/null | while read ref; do
    ref_path="${ref#@}"
    ref_path="${ref_path%[\`\*\]\"]}"
    if [ ! -e "$ref_path" ]; then
      echo "Broken reference: $ref in $file"
    fi
  done
done
```

### 4. Circular Reference Detection

```bash
# Check for self-references (A → A)
find . -name "*.md" ! -path "*/REFERENCE.md" ! -path "*/.git/*" | while read file; do
  refs=$(grep -oE '@\.(claude|docs)/[^)[:space:]+' "$file" || true)
  for ref in $refs; do
    if [ "${ref#@}" = "$file" ]; then
      echo "Self-reference: $file"
    fi
  done
done
```

### 5. Skill Count Validation

```bash
ACTUAL=$(find .claude/skills -name "SKILL.md" | wc -l | tr -d ' ')
STATED=$(grep -oE '\*\*[0-9]+ Skills\*\*' README.md | grep -oE '[0-9]+' || echo "0")

if [ "$ACTUAL" -ne "$STATED" ]; then
  echo "WARNING: Skill count mismatch - README: $STATED, actual: $ACTUAL"
fi
```

---

## Integration Pattern

### In Commands

```markdown
## Step 3: Documentation Verification

Invoke the `docs-verify` skill to validate documentation compliance.

The skill checks:
- Tier 1 line limits (≤200 lines)
- Tier 1 file count (exactly 2 in ai-context/)
- Cross-reference validity
- Circular references
```

Claude reads this skill file and executes the bash commands inline.

---

## Related Skills

**three-tier-docs**: Full 3-Tier documentation system | **vibe-coding**: File size standards

---

**Version**: claude-pilot 4.4.14
