---
name: spec
description: Create a specification for non-trivial changes. Creates GitHub issue + spec file in a dedicated directory.
allowed-tools: Read, Write, Bash(gh:*), Glob
---

# Spec Skill

Create lightweight specifications for changes that benefit from upfront design.

## Usage

```
/spec "description"
/spec composition "Add Valkey caching"
/spec infrastructure "Add GPU node pool"
```

**Types** (optional): `composition` | `infrastructure` | `security` | `platform`

If type is omitted, infer from description or ask.

## When to Use

- New Crossplane compositions
- Major infrastructure changes (VPC, EKS, IAM)
- Security changes (network policies, RBAC, PKI)
- Multi-component platform features

## When NOT to Use

- Version bumps, documentation-only, single-file bug fixes, minor config tweaks

## Workflow

### 1. Generate Identifiers

```bash
# Next spec number (3 digits)
MAX_NUM=$(find docs/specs -name "spec.md" -path "*/[0-9]*" 2>/dev/null | \
  sed 's|.*/\([0-9]*\)-.*|\1|' | sort -rn | head -1)
SPEC_NUM=$(printf "%03d" $((10#${MAX_NUM:-0} + 1)))

# Slug from description (3-4 meaningful words, kebab-case)
# Filter stop words, take meaningful words, join with hyphens
```

### 2. Create GitHub Issue

```bash
ISSUE_URL=$(gh issue create \
  --title "[SPEC] ${TITLE}" \
  --label "spec,spec:draft" \
  --body "## Summary
${DESCRIPTION}

## Spec Directory
\`docs/specs/${SPEC_NUM}-${SLUG}/\`

---
_Lightweight spec. See spec file for details._")

ISSUE_NUM=$(echo "$ISSUE_URL" | grep -oP 'issues/\K\d+$')
```

**Labels used**:
- `spec` - All specification issues
- `spec:draft` - Initial state (add manually: `spec:implementing` when work starts, `spec:done` when archived)

### 3. Create Spec Directory and File

```bash
SPEC_DIR="docs/specs/${SPEC_NUM}-${SLUG}"
mkdir -p "$SPEC_DIR"
```

Copy template from `docs/specs/templates/spec.md` and fill:
- `SPEC-XXX` → `SPEC-${SPEC_NUM}`
- `#XXX` → `#${ISSUE_NUM}`
- `YYYY-MM-DD` → current date
- `[Title]` → from description

### 4. Link in Issue

```bash
gh issue comment ${ISSUE_NUM} --body "Spec created: [\`${SPEC_DIR}/spec.md\`](${SPEC_DIR}/spec.md)"
```

### 5. Output

```
Spec created:

  Issue: https://github.com/Smana/cloud-native-ref/issues/XXX (label: spec:draft)
  Spec:  docs/specs/XXX-slug/spec.md

Next:
  1. Fill in the spec (use /clarify for [NEEDS CLARIFICATION] sections)
  2. Run /spec-status to see pipeline overview
  3. When starting work: gh issue edit XXX --remove-label "spec:draft" --add-label "spec:implementing"
  4. Implement the changes
  5. Reference in PR: "Implements #XXX"
  6. After merge: spec is auto-archived by GitHub Action
```

## Template Location

`docs/specs/templates/spec.md` (~80 lines)

## Clarifications

Use `/clarify` to resolve `[NEEDS CLARIFICATION: ...]` markers with structured options, or discuss conversationally with Claude.

## Integration

- `/spec` creates spec + issue with `spec:draft` label (this skill)
- `/spec-status` shows pipeline overview (Draft/Implementing/Done counts)
- `/clarify` resolves [NEEDS CLARIFICATION] markers with structured options
- `/create-pr` auto-detects specs and references issue
- `/commit` for commits
- GitHub Action auto-archives specs on PR merge
