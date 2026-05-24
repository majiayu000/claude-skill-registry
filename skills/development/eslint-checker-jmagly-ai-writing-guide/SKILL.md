---
name: eslint-checker
description: Run ESLint for JavaScript/TypeScript code quality and style enforcement. Use for static analysis and auto-fixing.
tools: Read, Write, Bash
---

# ESLint Checker Skill

## Purpose

Single responsibility: Execute ESLint for static analysis, style enforcement, and auto-fixing of JavaScript/TypeScript code. (BP-4)

## Grounding Checkpoint (Archetype 1 Mitigation)

Before executing, VERIFY:

- [ ] Node.js and npm available
- [ ] ESLint installed (local or global)
- [ ] Configuration file exists (eslint.config.js, .eslintrc.*)
- [ ] Target files/directories exist

**DO NOT run ESLint without confirming configuration.**

## Uncertainty Escalation (Archetype 2 Mitigation)

ASK USER instead of guessing when:

- Multiple ESLint configs found
- Auto-fix scope unclear (all vs specific rules)
- Conflicting rules with Prettier
- Custom rule configuration needed

**NEVER auto-fix without user confirmation on production code.**

## Context Scope (Archetype 3 Mitigation)

| Context Type | Included | Excluded |
|--------------|----------|----------|
| RELEVANT | Source files, ESLint config, ignore patterns | Test files (unless requested) |
| PERIPHERAL | Prettier config, tsconfig | Build outputs |
| DISTRACTOR | node_modules | Deployment configs |

## Workflow Steps

### Step 1: Environment Check (Grounding)

```bash
# Verify ESLint installed
npx eslint --version || npm install -D eslint

# Check config exists
ls eslint.config.* .eslintrc.* 2>/dev/null || echo "No ESLint config found"

# List ignored patterns
cat .eslintignore 2>/dev/null || echo "No .eslintignore"
```

### Step 2: Run Linting

**Basic lint:**
```bash
npx eslint src/
```

**With specific extensions:**
```bash
npx eslint . --ext .js,.ts,.tsx
```

**JSON output for parsing:**
```bash
npx eslint src/ --format json > eslint_results.json
```

**With auto-fix:**
```bash
npx eslint src/ --fix
```

**Dry-run fix (preview):**
```bash
npx eslint src/ --fix-dry-run
```

### Step 3: Analyze Results

```bash
# Summary format
npx eslint src/ --format stylish

# Count by rule
npx eslint src/ --format json | jq '[.[].messages[].ruleId] | group_by(.) | map({rule: .[0], count: length}) | sort_by(.count) | reverse'

# Errors only (ignore warnings)
npx eslint src/ --quiet
```

### Step 4: Generate Report

```bash
# HTML report
npx eslint src/ --format html -o eslint_report.html

# Markdown summary
echo "# ESLint Report"
echo "## Summary"
npx eslint src/ --format compact 2>&1 | tail -5
```

## Recovery Protocol (Archetype 4 Mitigation)

On error:

1. **PAUSE** - Don't auto-fix on error
2. **DIAGNOSE** - Check error type:
   - `Parsing error` → Check TypeScript config, syntax
   - `Rule not found` → Install missing plugin
   - `Config error` → Validate eslint.config.js
   - `No files found` → Check paths, ignore patterns
3. **ADAPT** - Adjust scope or configuration
4. **RETRY** - With corrected settings (max 3 attempts)
5. **ESCALATE** - Report config issues to user

## Checkpoint Support

State saved to: `.aiwg/working/checkpoints/eslint-checker/`

```
checkpoints/eslint-checker/
├── lint_results.json        # Full results
├── error_summary.md         # Error counts by rule
├── fix_preview.diff         # Proposed fixes
└── config_validation.json   # Config check results
```

## Common ESLint Options

| Option | Purpose |
|--------|---------|
| `--fix` | Auto-fix fixable issues |
| `--fix-dry-run` | Preview fixes |
| `--quiet` | Errors only |
| `--max-warnings N` | Fail if > N warnings |
| `--cache` | Use cache for speed |
| `--format json` | JSON output |
| `--ext .ts,.tsx` | File extensions |

## Configuration Templates

**eslint.config.js (flat config):**
```javascript
import js from '@eslint/js'
import typescript from '@typescript-eslint/eslint-plugin'
import tsParser from '@typescript-eslint/parser'

export default [
  js.configs.recommended,
  {
    files: ['**/*.ts', '**/*.tsx'],
    languageOptions: {
      parser: tsParser,
      parserOptions: {
        project: './tsconfig.json'
      }
    },
    plugins: {
      '@typescript-eslint': typescript
    },
    rules: {
      ...typescript.configs.recommended.rules,
      '@typescript-eslint/no-unused-vars': 'error'
    }
  },
  {
    ignores: ['node_modules/', 'dist/', '*.config.js']
  }
]
```

## References

- ESLint documentation: https://eslint.org/docs/
- TypeScript ESLint: https://typescript-eslint.io/
- REF-001: Production-Grade Agentic Workflows (BP-4)
- REF-002: LLM Failure Modes (Archetype 1 grounding)
