---
name: pragmatic-audit
description: Scan codebase for Pragmatic Programmer anti-patterns. Reports findings. Triggers on "pragmatic audit" or "/pragmatic-audit".
---

# Pragmatic Audit: Code Quality Scanner

Scan the codebase for bad programming practices and report findings.

## What It Checks

| Category | What to Look For |
|----------|------------------|
| DRY | Repeated code patterns, duplicate styles |
| SOLID | God objects (500+ lines), single-use abstractions |
| KISS | Nested ternaries, deep nesting, complex regex |
| Hardcoded | Magic numbers, inline colors, hardcoded URLs |
| Broken Windows | TODO/FIXME comments, console.log in production |
| Coupling | Deep imports (../../../), circular deps |

## How to Run

```bash
# DRY violations
grep -r "bg-white dark:bg-gray-800 rounded" app/ --include="*.tsx"

# God objects
find app -name "*.tsx" -o -name "*.ts" | xargs wc -l | awk '$1 > 500'

# Nested ternaries
grep -rE "\?.*\?.*:" app/ --include="*.tsx"

# Console.log in production
grep -r "console.log(" app/ --include="*.ts" --include="*.tsx" | grep -v ".test." | grep -v ".spec."

# Deep imports
grep -rE "from\s+['\"]\.\.\/\.\.\/\.\.\/" app/ --include="*.ts"
```

## Output Format

Report findings like this:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PRAGMATIC AUDIT COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Files scanned: 142
Issues found: 23

By Category:
  DRY violations:     8
  God objects:        3
  Console.log:        6
  Deep imports:       4
  Other:              2

Top Priority:
  1. checkout/page.tsx (892 lines) - refactor needed
  2. AdminSidebar.tsx - repeated card patterns
  3. api/stripe/webhook/route.ts - 6 console.log statements
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Exclusions

Skip these in scans:
- node_modules/
- .next/
- dist/
- *.test.* and *.spec.* files

## Triggers

- "pragmatic audit"
- "code quality audit"
- "/pragmatic-audit"
