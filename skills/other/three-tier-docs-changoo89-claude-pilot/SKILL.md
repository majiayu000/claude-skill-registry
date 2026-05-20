---
name: three-tier-docs
description: Use after code changes. Syncs CLAUDE.md, CONTEXT.md, and docs/ai-context/ automatically.
---

# SKILL: Three-Tier Documentation

> **Purpose**: Auto-sync documentation across 3 tiers (CLAUDE.md → CONTEXT.md → docs/)
> **Target**: Documenter agent after implementation

---

## Quick Start

### When to Use This Skill
- After implementing features
- After refactoring code
- After creating new components
- Run via `/document` command

### Quick Reference
```bash
# Tier 1: Sync 3 Entry Point documents
# - CLAUDE.md (≤200 lines)
# - docs/ai-context/project-structure.md
# - docs/ai-context/docs-overview.md

# Tier 2: Component CONTEXT.md (≤200 lines)
# - Purpose, key files, patterns

# Tier 3: Feature CONTEXT.md (≤200 lines)
# - Implementation details
```

---

## What This Skill Covers

### In Scope
- 3-tier documentation hierarchy (CLAUDE.md, CONTEXT.md, docs/)
- Size limits and content organization
- Auto-sync patterns after code changes

### Out of Scope
- Detailed templates → @.claude/skills/three-tier-docs/REFERENCE.md
- Verification skills → docs-verify
- Git documentation workflow → @.claude/skills/git-master/SKILL.md

---

## Core Concepts

### 3-Tier Hierarchy

**Tier 1: Entry Points** (3 files only)
- `CLAUDE.md` - Architecture, features, Quick Start (≤200 lines)
- `docs/ai-context/project-structure.md` - Tech stack, file tree (≤200 lines)
- `docs/ai-context/docs-overview.md` - Documentation navigation, Tier mapping (≤200 lines)
- **Required**: CLAUDE.md top section must reference the other 2 files
- **Constraint**: docs/ai-context/ folder must contain exactly 2 files

**Tier 2: CONTEXT.md** (Component Directory)
- **Purpose**: Component context
- **Content**: Purpose, key files, patterns
- **Size**: ≤200 lines per file
- **Scope**: Component-level context

**Tier 3: CONTEXT.md** (Feature Directory)
- **Purpose**: Feature implementation details
- **Content**: Implementation details, deep-dive
- **Size**: ≤200 lines per file
- **Scope**: Feature-level context

### Content Organization

| Tier | Location | Files | Update Frequency |
|------|----------|-------|------------------|
| 1 | Root + docs/ai-context/ | CLAUDE.md, project-structure.md, docs-overview.md | Project changes |
| 2 | Component dirs | CONTEXT.md | Component changes |
| 3 | Feature dirs | CONTEXT.md | Feature changes |

---

## Execution Steps

### Step 1: Sync Tier 1 Documents

**Tier 1 Structure** (3 files total):
- `CLAUDE.md` - Project architecture, features, Quick Start (≤200 lines)
- `docs/ai-context/project-structure.md` - Tech stack, file tree
- `docs/ai-context/docs-overview.md` - Documentation navigation, Tier mapping

**Required**: CLAUDE.md must reference project-structure.md and docs-overview.md at the top

**Verification**:
```bash
# Check Tier 1 files exist
for file in "CLAUDE.md" "docs/ai-context/project-structure.md" "docs/ai-context/docs-overview.md"; do
  if [ ! -f "$file" ]; then
    echo "FAIL: Missing Tier 1 file: $file"
    exit 1
  fi
done

# Check CLAUDE.md references the other 2 files
if ! grep -q "project-structure.md" CLAUDE.md || ! grep -q "docs-overview.md" CLAUDE.md; then
  echo "FAIL: CLAUDE.md must reference project-structure.md and docs-overview.md"
  exit 1
fi

echo "✓ Tier 1 documents verified"
```

---

### Step 2: Generate Component CONTEXT.md Files

**Target directories**: Any directory with code files (e.g., src/, components/, lib/)

**Script**: See REFERENCE.md for full bash implementation

```bash
# Generate CONTEXT.md for key directories
for dir in src/ components/ lib/ .claude/commands/ .claude/skills/ .claude/agents/; do
  [ -d "$dir" ] || continue
  [ -f "$dir/CONTEXT.md" ] && [ -s "$dir/CONTEXT.md" ] && continue
  # Generate template (see REFERENCE.md for full script)
  echo "✓ Generated $dir/CONTEXT.md"
done
```

**Size Limit**: ≤200 lines per file

---

### Step 3: Verify Documentation Compliance

Invoke the `docs-verify` skill for comprehensive validation.

**Validation includes**:
- Tier 1 line limits (≤200 lines): CLAUDE.md, project-structure.md, docs-overview.md
- ai-context file count (exactly 2 files)
- Cross-reference validation
- Circular reference detection

**Script**: See @.claude/skills/docs-verify/SKILL.md for full verification commands

### Step 4: Inline Verification

Verify documentation compliance immediately after update:

```bash
# 1. Tier 1 Line Limits (≤200)
for file in CLAUDE.md docs/ai-context/*.md; do
  [ -f "$file" ] || continue
  lines=$(wc -l < "$file" | tr -d ' ')
  [ "$lines" -gt 200 ] && echo "FAIL: $file has $lines lines (limit: 200)"
done

# 2. ai-context file count (exactly 2)
count=$(find docs/ai-context -maxdepth 1 -name "*.md" -type f | wc -l | tr -d ' ')
[ "$count" -ne 2 ] && echo "FAIL: docs/ai-context/ has $count files (expected: 2)"

# 3. Cross-reference check
grep -oE '@[^][:space:]]+' CLAUDE.md | while read ref; do
  [ ! -e "${ref#@}" ] && echo "Broken: $ref"
done
```

---

## Verification Failure Recovery

**Line count violations**: CLAUDE.md >200 lines → Extract to docs/ai-context/ | CONTEXT.md >200 lines → Move examples or simplify

**Broken cross-references**: Check file exists with `test -f {path}` | Use absolute paths (e.g., `@.claude/skills/...`)

**Missing frontmatter**: Add required fields (name, description) | Validate with `yamllint {file}`

**Recovery Steps**: Invoke docs-verify skill → Find violating file → Apply fix from REFERENCE.md → Re-verify

---

## Further Reading

**Internal**: @.claude/skills/three-tier-docs/REFERENCE.md - Complete templates, examples, verification patterns | @.claude/skills/documentation-best-practices/SKILL.md - Size limits, quality standards

**External**: [Documentation System Design](https://documentation.divio.com/) | [Writing for AI](https://docs.anthropic.com/claude/docs/guide-to-writing-good-docs)

---

**Version**: claude-pilot 4.4.15
