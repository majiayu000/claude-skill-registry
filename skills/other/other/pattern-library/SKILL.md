---
name: vibe-pattern-library
description: Detects recurring implementation patterns and records them for reuse. When the same code pattern appears 3+ times, it belongs in the pattern library.
user-invocable: true
---

# vibe-pattern-library

Three similar lines of code is fine. But when you implement the same pattern for the third time across different files, codify it.

## When to Use This Skill

- You notice implementing the same pattern again (3rd+ time)
- You find yourself copying code structure from another file
- After a code review suggests "we always do X this way"
- When onboarding to a project and want to learn established patterns

## When NOT to Use This Skill

- First or second use of a pattern (too early to codify)
- Patterns that are specific to one module (not reusable)
- Language-standard patterns already in the style guide

## Steps

1. **Detect** — Notice when you're implementing something you've seen before:
   - Table-driven tests
   - Error wrapping with context
   - Retry with backoff
   - Repository pattern
   - Builder pattern
   - Event handler registration
   - Middleware chains

2. **Record** the pattern:
   ```
   ### [Pattern Name]
   **Category**: [Testing | Error Handling | Concurrency | Data | API | etc.]
   **When to use**: [Specific situation]
   **Template**:
   ```[language]
   [The canonical implementation]
   ```
   **Variations**:
   - [Variation 1]: [when to use]
   **Anti-patterns**:
   - Don't [common mistake]
   **Examples in codebase**: [file:line references]
   ```

3. **Store** — Save to:
   - `docs/patterns.md` or `docs/patterns/[category].md`
   - Claude memory for cross-session access

4. **Reference** — When implementing the pattern again, suggest the recorded version instead of re-inventing

## Output Format

### Pattern: [Name]
**Category**: [category]
**Occurrences found**: X files

```[language]
// Canonical implementation
[code]
```

**Saved to**: [location]
