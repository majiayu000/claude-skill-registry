---
name: review
description: Quick code review for files or recent changes, checking for bugs, best practices, and potential improvements
---

# Review Skill

Perform a quick, focused code review on specified files or recent git changes.

## Instructions

### 1. Determine Review Scope

Parse the user's request to determine what to review:
- **Specific file(s)**: `/review src/main/java/.../MyService.java`
- **Recent changes**: `/review changes` or `/review diff`
- **Staged changes**: `/review staged`
- **Last commit**: `/review last-commit`
- **Feature/component**: `/review ForecastService` (find and review related files)

### 2. Gather Code to Review

Based on scope:

**For specific files:**
- Use `Read` to load the file content

**For git changes:**
- Use `Bash` with `git diff` for unstaged changes
- Use `Bash` with `git diff --cached` for staged changes
- Use `Bash` with `git show HEAD` for last commit
- Use `Bash` with `git diff HEAD~N` for recent N commits

**For component/feature:**
- Use `Glob` and `Grep` to find relevant files
- Read the main files involved

### 3. Review Checklist

Analyze the code for:

#### Correctness
- Logic errors or bugs
- Off-by-one errors
- Null/undefined handling
- Edge cases not covered
- Incorrect assumptions

#### Security
- Input validation issues
- Injection vulnerabilities (SQL, command, XSS)
- Hardcoded secrets or credentials
- Unsafe data handling

#### Performance
- Inefficient algorithms (O(n²) when O(n) possible)
- Unnecessary iterations or allocations
- Missing caching opportunities
- Blocking calls in reactive code

#### Best Practices
- Code style consistency
- Naming conventions
- Error handling patterns
- Resource cleanup (try-with-resources, close())
- Thread safety in concurrent code

#### Maintainability
- Code duplication
- Overly complex methods (consider splitting)
- Missing or misleading comments
- Dead code

#### Project-Specific (varun.surf)
- Reactive patterns (WebFlux compliance)
- Proper use of virtual threads/StructuredTaskScope
- Cache invalidation concerns
- External API error handling

### 4. Severity Levels

Categorize findings:

- **Critical**: Bugs, security issues, data loss risks
- **Warning**: Performance issues, bad practices, potential bugs
- **Suggestion**: Style improvements, minor optimizations, readability

## Output Format

```markdown
## Code Review: [File/Scope]

### Summary
- Files reviewed: X
- Lines analyzed: Y
- Issues found: Z (X critical, Y warnings, Z suggestions)

### Critical Issues

#### [Issue Title]
**File**: `path/to/file.java:line`
**Problem**: [Description]
**Fix**: [Suggested solution]
```java
// Before
problematic code

// After
fixed code
```

### Warnings

#### [Issue Title]
**File**: `path/to/file.java:line`
**Problem**: [Description]
**Suggestion**: [How to improve]

### Suggestions

- `file.java:42` - Consider extracting this to a method
- `file.java:78` - Variable name could be more descriptive

### What Looks Good

- Proper error handling in [location]
- Good use of [pattern/practice]
- Clean separation of concerns

### Files Reviewed
- `path/to/file1.java` - [brief note]
- `path/to/file2.java` - [brief note]
```

## Examples

```bash
# Review a specific file
/review src/main/java/com/github/pwittchen/varun/service/ForecastService.java

# Review recent uncommitted changes
/review changes

# Review staged changes before commit
/review staged

# Review the last commit
/review last-commit

# Review a component by name
/review AggregatorService

# Review multiple files
/review src/main/java/.../controller/*.java
```

## Notes

- Keep reviews focused and actionable
- Prioritize critical issues over style nitpicks
- Provide concrete fix suggestions, not just problem descriptions
- Reference project patterns from CLAUDE.md when relevant
- For large diffs, focus on the most impactful changes
- Don't repeat issues that appear multiple times; note "X similar occurrences"
