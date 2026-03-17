---
name: code-quality-gates
description: Use automatically before and after code changes. Ensures documentation, formatting, type safety, and audit standards.
---

# SKILL: Code Quality Gates

> **Purpose**: Automated quality checks before/after code changes (PreToolUse, PostToolUse, Stop hooks converted to skill logic)
> **Target**: All agents making code changes

---

## Quick Start

### When to Use This Skill
- Before creating any .md files (documentation gate)
- After writing code (formatting, type check)
- Before completing work (final audit)

### Quick Reference
```bash
# PreToolUse: Block .md creation
[[ "$file" == *.md ]] && echo "Use Write tool for .md" && return 1

# PostToolUse: Auto-format + type check
prettier --write "$file" && npx tsc --noEmit

# Stop: Console.log audit
grep -rn "console.log" src/ || true
```

---

## Quality Gates

### Gate 1: Documentation (PreToolUse)

**Purpose**: Block .md file creation via Bash

**Apply**: Before Bash commands
```bash
echo "$command" | grep -qiE '\.md' && echo "Use Write tool for .md" && return 1
```

### Gate 2: Formatting (PostToolUse)

**Purpose**: Auto-format after code changes

**Apply**: After Edit/Write
```bash
format_code() {
  case "${1##*.}" in
    js|ts|tsx|json|css|md) prettier --write "$1" ;;
    py) black "$1" ;;
  esac
}
```

### Gate 3: Type Safety (PostToolUse)

**Purpose**: Verify TypeScript type correctness

**Apply**: After .ts file changes
```bash
[ -f tsconfig.json ] && npx tsc --noEmit
```

### Gate 4: Console Audit (Stop)

**Purpose**: Flag console.log before completion

**Apply**: Before work completion
```bash
find src -name "*.ts" -o -name "*.js" | xargs grep -n "console.log"
```

---

## Integration Points

| Hook | Function | Agent | Trigger |
|------|----------|-------|---------|
| PreToolUse | Documentation gate | All | Before Bash |
| PostToolUse | Formatting | Coder | After Edit/Write |
| PostToolUse | Type check | Coder | After .ts changes |
| Stop | Console audit | Coder | Before completion |

---

## Verification

```bash
# Test all gates
echo "# Test" > test.md  # Should warn
echo "const x=1;" > test.js && prettier --write test.js  # Should format
echo "const x: string = 1;" > test.ts && npx tsc --noEmit  # Should error
grep -rn "console.log" src/  # Should find logs
```

---

## Related Skills

- **vibe-coding**: Code quality standards (≤50 lines/function, ≤200 lines/file)
- **coding-standards**: TypeScript, React, API, testing standards
- **tdd**: Test-driven development (Red-Green-Refactor)

---

**Version**: claude-pilot 4.3.0
