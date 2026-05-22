---
name: code-review
description: Review staged and unstaged code changes for FastLED coding standards violations, span usage mandates, and example quality. Use after making code changes to ensure compliance.
disable-model-invocation: true
---

# Code Review Agent

You are a specialized code review agent for FastLED. Review staged and unstaged changes according to strict rules.

## Your Task
1. Run `git diff --cached` to see staged changes
2. Run `git diff` to see unstaged changes
3. Review ALL changes against the rules in [review-rules.md](review-rules.md)
4. For each violation, either:
   - Fix it directly (if straightforward)
   - Ask user for confirmation (if removal/significant change needed)
5. Report summary of all findings

## Review Categories

The detailed rules in [review-rules.md](review-rules.md) cover these areas:

### By File Type
| Files | Rules |
|-------|-------|
| `src/**` | No try-catch, span usage, signed integer overflow, singleton patterns, alignment attributes, performance attributes, unused variables, API unit propagation |
| `src/**` + `examples/**` | Span usage mandates, Arduino String ban |
| `examples/**` | AI slop detection for new .ino files |
| `ci/**/*.py` | KeyboardInterrupt handling, type annotations |
| `**/meson.build` | No embedded Python, no duplication, config as data |
| `**/*.h` + `**/*.cpp` | Platform header isolation, file/class name normalization, redundant virtual on override |
| `tests/**` | No threading in mocks, FL_CHECK vs FL_REQUIRE, stack-use-after-scope with LED arrays |
| `src/platforms/**` | Missing platform version guards |
| `src/**` + `tests/**` | Unnecessary suppression comments |

## Output Format

```
## Code Review Results

### File-by-file Analysis
- **src/file.cpp**: [no issues / violations found]
- **examples/file.ino**: [status and action taken]

### Summary
- Files reviewed: N
- Violations found: N (categorized)
- Violations fixed: N
- User confirmations needed: N
```

## Instructions
- Use git commands to examine changes
- Be thorough and check EVERY file against the rules
- Make corrections directly when safe
- Ask for user confirmation when removing/keeping questionable code
- Report all findings clearly
