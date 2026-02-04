---
name: refactor-suggestions
description: Suggest refactors for modified code focusing on security, maintainability, readability, and functional programming purity
category: refactoring
disable-model-invocation: false
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash
---

# Refactor Suggestions

Inspect the repository for code changes and recommend refactors.

## Procedure

### Phase 1 - Get the Changes
1. Get all changes in this branch compared to the default branch since it diverged
2. Scoped from those changes, analyze code from modified and added functions
3. Suggest (do not re-write functions) refactors focused on:
   - Security
   - Maintainability
   - Readability
   - Logic flow
   - Functional programming purity

### Refactor Categories to Consider
- Increases purity and immutability
- Reduces side effects and shared state
- Improves readability and testability
- Eliminates security anti-patterns
- Simplifies complex conditionals
- Extracts reusable utilities
- Improves error handling

### Phase 2 - Return Suggestions

Return Markdown structured as follows:

```markdown
# Suggestions

**functionName**
location: src/path/to/file.ts `functionName`
description: Detailed explanation of why this function should be refactored
refactor strategy: Explain rationale explicitly
refactored code:
```
function() {
  // suggested implementation
}
```

**anotherFunction**
...
```

## Constraints
- Analyze only within the given code. Do not invent missing context or external APIs
- Be deterministic and concise
- Focus on actionable, specific suggestions
