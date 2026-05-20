---
name: trim
description: "ONLY when user explicitly types /trim. Never auto-trigger on optimize, shorten, or reduce."
argument-hint: "[file-path]"
---

# /trim - Token-Efficient File Optimization

Optimize a file for token efficiency while preserving 100% of information/functionality.

## Flow

1. **Get path** - from argument or ask user
2. **Read original** - read file, note exact line count
3. **Inventory** - list EVERY discrete fact, rule, instruction, example, value in the file
4. **Optimize** - condense formatting/prose only, never delete inventory items
5. **Verify** - check new version against inventory, confirm every item present
6. **Write** - only if verification passes
7. **Report** - before/after line counts, what was condensed (not removed)

## Constraints

- **ZERO INFORMATION LOSS** - every fact, rule, value, example must survive
- **Inventory is sacred** - if it was in the original, it must be in the result
- **Only condense prose** - remove filler words, redundant phrasing, extra whitespace
- **Never merge meaning** - two distinct rules stay as two rules, even if similar
- **When in doubt, keep it** - verbosity is acceptable, information loss is not
- **Keep valid** - no syntax errors, proper formatting
- **No code changes** - don't alter functionality in code files

## Verification Checklist (mandatory)

Before writing the optimized file, explicitly confirm:

1. Count items in original inventory
2. Count items in new version
3. If counts differ, STOP - restore missing items
4. List any items that changed meaning - if any, STOP - restore original wording

## Failure Mode

If uncertain whether something is redundant or meaningful: **KEEP IT**.
Tokens are cheap. Lost information cannot be recovered.
