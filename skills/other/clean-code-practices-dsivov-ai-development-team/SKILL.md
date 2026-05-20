---
name: clean-code-practices
description: Use when the Developer is writing or modifying code, implementing features, fixing bugs, or refactoring. Activates for any code writing task to ensure clean, readable, maintainable code following KISS, DRY, and YAGNI principles.
version: 1.0.0
---

# Clean Code Practices

## When This Applies

Apply this guidance whenever writing or modifying source code as the Developer role.

## Core Principles

### KISS — Keep It Simple
- Choose the simplest approach that works
- Avoid premature optimization
- If a solution needs a comment to explain what it does, simplify it

### DRY — Don't Repeat Yourself
- Extract common logic into shared functions only when used 3+ times
- Don't create abstractions for two similar lines — wait for the third
- Prefer duplication over the wrong abstraction

### YAGNI — You Aren't Gonna Need It
- Only implement what the task requires
- Don't add features "just in case"
- Don't design for hypothetical future requirements

## Naming

- **Variables**: Describe what they hold — `userEmail` not `e`, `totalPrice` not `tp`
- **Functions**: Describe what they do — `calculateTax()` not `process()`, `isValid()` not `check()`
- **Booleans**: Use is/has/can prefix — `isActive`, `hasPermission`, `canDelete`
- **Constants**: UPPER_SNAKE_CASE — `MAX_RETRIES`, `DEFAULT_TIMEOUT`
- **Be consistent**: If the codebase uses `get*` for retrievals, don't introduce `fetch*`

## Function Design

- **Single responsibility** — One function does one thing
- **Short** — If a function exceeds 30 lines, consider breaking it down
- **Few parameters** — 3 or fewer. If more, use an options object
- **No side effects** — Unless the function name clearly indicates mutation
- **Early returns** — Handle error cases first, then the happy path

```
// Prefer early returns
function process(input) {
  if (!input) return null;
  if (!input.isValid) throw new Error("Invalid input");

  // Happy path here
  return transform(input);
}
```

## Error Handling

- Handle errors at the appropriate level (not too early, not too late)
- Never swallow errors silently
- Include context in error messages — what failed, what was expected
- Use specific error types, not generic catch-all
- Validate at system boundaries (user input, API calls), trust internal code

## Code Organization

- Group related code together
- Keep imports organized (stdlib, external, internal)
- One concept per file — don't mix unrelated functionality
- Follow the project's existing patterns for file and folder structure

## What NOT To Do

- Don't add comments that restate the code (`// increment counter` above `counter++`)
- Don't leave TODO comments without task IDs
- Don't commit debug logging, console.log, or print statements
- Don't add empty catch blocks
- Don't use magic numbers — use named constants
