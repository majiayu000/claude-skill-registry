---
name: coderabbit-review
description: Use this skill when working with CodeRabbit, such as running CodeRabbit reviews, generating and processing automated CodeRabbit comments, or evaluating CodeRabbit suggestions. 
---

# CodeRabbit Review Handler

Process CodeRabbit review comments with context-aware discretion.

## Instructions

### 1. Initial Context

Inform the user:
```
I'll review the CodeRabbit comments with discretion, as CodeRabbit doesn't have access to the entire codebase and may not understand the full context.

For each comment, I'll:
- Evaluate if it's valid given our codebase context
- Accept suggestions that improve code quality
- Ignore suggestions that don't apply to our architecture
- Explain my reasoning for accept/ignore decisions
```

### 2. Run Code Rabbit

If no comments are provided, run CodeRabbit in prompt-only mode to generate comments:

```bash
# Run CodeRabbit cli
coderabbit --prompt-only 
```

### 3. Evaluate Comments
- Parse the comments
- For each comment:
  - Read the relevant file to understand context
  - Determine if the suggestion is valid and beneficial
  - Decide to accept or ignore the suggestion
  - Document reasoning for each decision
- Ignore *.md files


### 4. Execute Fixes

Task a subagent to address the comments you've accepted

### 5. Validate Changes

Run relevant tests and linters to ensure code integrity:

Example:

```bash
# Run all unit tests
./scripts/test.sh unit 1 2>&1 | tail -100

# Run affected UI tests
./scripts/test.sh ui [TestName] 2>&1 | tail -100

# Run swiftlint on changed files and fix ANY issues
git diff --name-only origin/main...HEAD -- '*.swift' | xargs -r swiftlint lint --strict
```

### 6. Commit Changes

After applying changes commit your work using appropriate commit messages summarizing the changes made. Address any re-commit hook violations as needed.

### 7. Consolidate Results
After completion, provide a summary report:
```
📋 CodeRabbit Review Summary

Files Processed: {count}

Accepted Suggestions:
  {file}: {changes_made}
  
Ignored Suggestions:
  {file}: {reason_ignored}

Overall: {X}/{Y} suggestions applied
```

## Common Patterns to Ignore

- **Style preferences** that conflict with project conventions
- **Generic best practices** that don't apply to our specific use case
- **Performance optimizations** for code that isn't performance-critical
- **Accessibility suggestions** for internal tools
- **Security warnings** for already-validated patterns
- **Import reorganization** that would break our structure

## Common Patterns to Accept

- **Actual bugs** (null checks, error handling)
- **Security vulnerabilities** (unless false positive)
- **Resource leaks** (unclosed connections, memory leaks)
- **Type safety issues** (TypeScript/type hints)
- **Logic errors** (off-by-one, incorrect conditions)
- **Missing error handling** 

## Decision Framework

For each suggestion, consider:
1. **Is it correct?** - Does the issue actually exist?
2. **Is it relevant?** - Does it apply to our use case?
3. **Is it beneficial?** - Will fixing it improve the code?
4. **Is it safe?** - Could the change introduce problems?

Only apply if all answers are "yes" or the benefit clearly outweighs risks.

## Important Notes

- CodeRabbit is helpful but lacks context
- Trust your understanding of the codebase over generic suggestions
- Explain decisions briefly to maintain audit trail
- Batch related changes for efficiency
- Always run the relevant ui and unit tests, and/or create new tests to verify correctness after applying changes