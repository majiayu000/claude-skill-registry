---
name: code-cleanup
description: Dead code detection and removal using knip (recommended) or standard tooling. Use when removing unused imports, variables, or dead files.
---

# SKILL: Code Cleanup

> **Purpose**: Dead code detection and removal using knip (recommended) or ESLint/TypeScript fallback
> **Target**: Coder Agent, cleanup commands

---

## ⚠️ EXECUTION DIRECTIVE

**IMPORTANT**: Execute ALL steps IMMEDIATELY and AUTOMATICALLY.

**Core Philosophy**: Auto-apply Low/Medium risk | High-risk: User confirmation | Safe flags: `--dry-run`, `--apply` | Verification after each batch

---

## Quick Start

### When to Use This Skill
- Remove unused import statements
- Detect and delete dead files (zero references)
- Clean up codebase after refactoring

### Usage
```bash
MODE="${1:-files}"  # imports|files|all
SCOPE="${2:-repo}"  # repo|path=...
```

---

## .cleanup-ignore Support

Create `.cleanup-ignore` file in project root:

```gitignore
# Core infrastructure
**/auth/**
**/database/**
**/*.config.*

# Entry points
**/index.ts
**/main.ts

# Generated files
**/generated/**
**/*.gen.ts
```

**Loading order**: Read `.cleanup-ignore` → Apply patterns → Exclude protected files

---

## Step 1: Detect Dead Code

### Detection Tools

**Recommended: knip**
```bash
npx knip                    # Full analysis
npx knip --reporter compact # Concise output
npx knip --fix              # Auto-fix safe issues
```

**Fallback: Standard tooling**
```bash
grep -r "import.*from" src/ --include="*.ts"  # Unused imports
find src/ -name "*.ts" -exec grep -l "{}" \;   # Dead files
```

### Dead File Detection Procedure

```bash
EXCLUDE="--glob '!*.test.ts' --glob '!*.spec.ts' --glob '!index.ts'"
rg --files $EXCLUDE src/ | while read file; do
  refs=$(rg -c "from.*['\"]$file" src/ || echo 0)
  [ "$refs" -eq 0 ] && echo "$file: 0 references"
done
```

---

## Step 2: Risk Classification (4-Level)

| Risk | File Types | Action |
|------|------------|--------|
| **SAFE** | Tests (`*.test.*`), mocks, fixtures | auto-remove |
| **CAUTION** | Utils, helpers, internal modules | auto-remove + prompt |
| **WARNING** | Components, services, hooks | tests pass first |
| **DANGER** | Auth, database, config, API routes | require `--force` |

```bash
classify_risk() {
  case "$1" in
    *.test.* | *.spec.* | */__mocks__/*) echo "SAFE" ;;
    */utils/* | */helpers/* | */lib/*) echo "CAUTION" ;;
    */components/* | */services/* | */hooks/*) echo "WARNING" ;;
    */auth/* | */database/* | *.config.* | */api/*) echo "DANGER" ;;
    *) echo "CAUTION" ;;
  esac
}
```

---

## Step 3: Cleanup with Confirmation

```bash
detect_dead_files() {
  rg --files --glob '!*.test.ts' src/ | while read file; do
    refs=$(rg -c "from.*['\"]$file" src/ || echo 0)
    [ "$refs" -eq 0 ] && echo "$file|$(classify_risk "$file")"
  done
}
# Auto-apply SAFE/CAUTION/WARNING, confirm DANGER
detect_dead_files | while IFS='|' read -r file risk; do
  if [ "$risk" = "DANGER" ]; then
    echo "DANGER: $file [A) Delete / B) Skip]"
    read -p "Choose: " choice
    [ "$choice" = "A" ] && rm "$file"
  else
    echo "Auto-deleting: $file" && rm "$file"
  fi
done
```

---

## Step 4: Verification

```bash
npm test || { echo "❌ Tests failed"; git checkout -- .; exit 1; }
npm run type-check || { echo "❌ Type check failed"; git checkout -- .; exit 1; }
npm run lint || { echo "❌ Lint failed"; git checkout -- .; exit 1; }
echo "✅ All checks passed"
```

**Rollback on failure**: `git checkout -- .`

---

## Step 5: Execution Logging

```bash
mkdir -p .cleanup
LOG_FILE=".cleanup/$(date +%Y-%m-%d_%H%M%S).log"
if [ "$DELETED_COUNT" -gt 0 ]; then
  echo "# Cleanup Log - $(date +%Y-%m-%d)" > "$LOG_FILE"
  echo "## Deleted: $DELETED_COUNT files" >> "$LOG_FILE"
  echo "✓ Log saved: $LOG_FILE"
fi
```

**stdout**: `✅ Cleanup Complete - Deleted: 5 files, Tests: PASS`

---

## Parallel Detection (Optional)

```markdown
Task A: npx knip --reporter json
Task B: eslint . --report-unused-disable-directives --format json
Task C: tsc --noUnusedLocals --noEmit 2>&1
# Merge: Deduplicate → Apply .cleanup-ignore → Classify by risk
```

**Safe**: All detection commands are read-only.

---

## Pre-flight Safety

```bash
[ -n "$(git status --porcelain)" ] && { echo "⚠️  Working directory not clean"; exit 2; }
```

---

## Troubleshooting

**False Positives**: Dynamic imports, runtime requires | **Test Failures**: `git checkout -- .`

---

## Best Practices

- **Run tests after each batch**: Max 10 deletions per batch | **Conservative exclusion**: Exclude index.*, main.*, *.config.* | **Risk-based approach**: Auto-apply Low/Medium, confirm High | **Clean working directory**: Block if modified/staged files exist

---

## Further Reading

**Internal**: @.claude/skills/code-cleanup/REFERENCE.md | @.claude/skills/vibe-coding/SKILL.md

**External**: [ESLint Unused Vars Rule](https://typescript-eslint.io/rules/no-unused-vars/) | [knip](https://knip.dev/) | **⚠️ SAFETY**: Auto-rollback on verification failure
