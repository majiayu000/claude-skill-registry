---
name: refactoring
description: Apply refactoring patterns when consolidating code, extracting functions, or discussing DRY principles. Use when identifying duplicate code, planning consolidation, or discussing code organization. Auto-apply when editing files in src/ or when user mentions "duplicate", "refactor", "DRY", "extract", "consolidate", or "similar code".
---

# Refactoring Skill

Guide for identifying and consolidating duplicate code while maintaining codebase quality.

## Core Principle: Discuss Before Deciding

**IMPORTANT**: Always discuss refactoring decisions with the user before implementing. Use `AskUserQuestion` to:
- Confirm whether code is truly duplicate vs. intentionally similar
- Validate proposed extraction patterns
- Get approval on naming and module placement
- Check if there are historical reasons for current structure

## Critical Anti-Pattern: Dead Helpers

**The most dangerous duplication**: A tested helper that production doesn't use.

```
❌ What we found:
   marchingSquares.js: renderMultiContour() - tested, used by Storybook
   main.jsx: inline loop doing same thing - untested, used in production

   Result: Tests pass, but production runs different code.
```

### How to Detect

Before any refactoring work, check for unused helpers:
```bash
grep -l "export function" src/render/*.js | while read f; do
  funcs=$(grep -o "export function [a-zA-Z]*" "$f" | cut -d' ' -f3)
  for func in $funcs; do
    if ! grep -rq "$func" src/main.jsx src/stories/; then
      echo "⚠️  $f: $func exported but not used in production"
    fi
  done
done
```

### How to Fix

1. **If helper is correct**: Update main.jsx to use it, delete inline code
2. **If inline is correct**: Delete the unused helper and its tests
3. **Never leave both**: One implementation, used everywhere

## Duplicate Code Patterns to Look For

### 1. Copy-Paste Functions
Similar functions with minor variations:
```javascript
// Suspicious pattern - similar structure, different constants
function calculateFoamA(x, y) {
  return x * 0.5 + y * FOAM_FACTOR_A;
}
function calculateFoamB(x, y) {
  return x * 0.5 + y * FOAM_FACTOR_B;
}
```

**Before refactoring, ASK**:
- Are these intentionally separate for performance/clarity?
- Should they share logic or remain independent?

### 2. Repeated Logic Blocks
Same operations appearing in multiple places:
```javascript
// Pattern: repeated clamping/normalization
const value = Math.max(0, Math.min(1, rawValue));  // appears in 5 files
```

### 3. Similar Data Transformations
Multiple functions doing equivalent transformations on different data shapes.

### 4. Parallel Structures
Similar class/module structures that could share a base:
```javascript
// src/render/foamRenderer.js
// src/render/waveRenderer.js
// Both have: init(), update(), render(), cleanup()
```

## Refactoring Decision Framework

### When TO Consolidate (Rule of 3+)
- Same logic appears 3+ times
- Changes to one copy usually require changes to others
- The abstraction has a clear, meaningful name
- User agrees the duplication is problematic

### When NOT to Consolidate
- Code is similar but serves different purposes
- Premature abstraction would obscure intent
- Performance-critical paths benefit from inlining
- User prefers explicit over DRY in this case

## Discovery Process

1. **Identify candidates**: Use grep/glob to find similar patterns
2. **Assess scope**: How many instances? How similar?
3. **Discuss with user**: Present findings, propose options
4. **Get explicit approval**: Before any extraction
5. **Plan the refactor**: Create plan document if significant
6. **Implement incrementally**: One extraction at a time
7. **Verify**: Run tests after each change

## Codebase-Specific Patterns

This project uses:
- Vanilla JavaScript (no TypeScript)
- Canvas 2D rendering
- Physics simulation with tight loops
- Vitest for testing

**Performance considerations**:
- Rendering code may intentionally inline for speed
- Physics calculations may duplicate for cache locality
- Always check if duplication is intentional optimization

## Discussion Templates

When presenting refactoring opportunities:

```
I found [N] similar code blocks:
- [file1:line] - [brief description]
- [file2:line] - [brief description]

Options:
A) Extract to shared function in [module]
B) Keep separate (they serve different purposes)
C) Other approach

Which direction would you prefer?
```

## Integration with Plans

For significant refactoring:
1. Create plan in `plans/refactoring/` using `/feat refactoring/[name]`
2. Document current state, proposed changes, affected files
3. Track progress via plan status

## Commands Reference

```bash
# Search for similar functions
grep -r "function.*calculate" src/

# Find files with similar structure
find src/ -name "*.js" -exec grep -l "pattern" {} \;

# Check test coverage before refactoring
npm test

# Verify after changes
npm run lint && npm test
```

## Checklist Before Refactoring

- [ ] Discussed approach with user
- [ ] Confirmed duplication is problematic (not intentional)
- [ ] Tests exist for affected code
- [ ] User approved proposed pattern/naming
- [ ] Plan document created (if significant change)

## CRITICAL: Testing After Refactoring

After EVERY refactoring change, run tests in this order:

```bash
# 1. Lint first (fast feedback)
npm run lint

# 2. Smoke test - verify app actually loads
npx playwright test tests/smoke.spec.js:3

# 3. Specific tests for changed files
npx vitest run src/path/changed-file.test.js

# 4. Full suite only if needed
npm test
```

**DO NOT skip the smoke test** - unit tests can pass while the app is broken (e.g., broken imports not exercised in unit tests).

**DO NOT run the full test suite first** - start with specific tests for faster iteration.
