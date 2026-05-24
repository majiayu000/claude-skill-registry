---
name: issue-classification
description: Configure issue classification for ADWs to route work to the correct templates. Use when setting up automatic classification of GitHub issues into chores, bugs, and features.
allowed-tools: Read, Grep, Glob
---

# Issue Classification

Guide for configuring automatic classification of issues into problem classes.

## When to Use

- Setting up ADW issue routing
- Improving classification accuracy
- Handling edge cases in classification
- Designing custom problem classes

## Why Classification Matters

Classification routes issues to the correct template:

```text
Issue: "Login button not working"
  ↓
Classification: /bug
  ↓
Template: Bug fix plan with root cause analysis
```

Without classification, agents don't know which workflow to use.

## Standard Problem Classes

### Chore

Maintenance tasks, updates, cleanup:

```text
Examples:
- "Update dependencies to latest"
- "Clean up unused imports"
- "Rename function to follow convention"
- "Add missing documentation"

Signals:
- "update", "upgrade", "clean", "remove", "rename"
- "documentation", "comment", "format"
- No user-facing change
- Maintenance in nature
```

### Bug

Defects, errors, unexpected behavior:

```text
Examples:
- "Login form submits twice"
- "404 error on profile page"
- "Data not saving correctly"
- "Crash when clicking button"

Signals:
- "error", "bug", "fix", "broken", "crash"
- "not working", "fails", "incorrect"
- Something that worked before now doesn't
- Unexpected behavior
```

### Feature

New functionality, enhancements:

```text
Examples:
- "Add dark mode toggle"
- "Implement user authentication"
- "Create new dashboard page"
- "Add export to CSV"

Signals:
- "add", "create", "implement", "new"
- "enhance", "improve", "extend"
- User-facing new capability
- Didn't exist before
```

## Classification Command

### Basic Structure

```markdown
# Issue Classification

Analyze the issue and respond with exactly one of:
- `/chore` - maintenance, updates, cleanup
- `/bug` - defects, errors, unexpected behavior
- `/feature` - new functionality, enhancements

If the issue doesn't fit any category, respond with `0`.

## Issue
$ARGUMENTS
```

### Enhanced with Examples

```markdown
# Issue Classification

Classify the GitHub issue into one of these categories.

## Categories

### /chore
- Maintenance and cleanup tasks
- Dependency updates
- Refactoring without behavior change
- Documentation improvements

Examples: "update deps", "clean up code", "rename variables"

### /bug
- Something broken that should work
- Errors, crashes, incorrect behavior
- Regressions from previous functionality

Examples: "button doesn't work", "error on page", "crash when..."

### /feature
- New functionality
- Enhancements to existing features
- User-facing improvements

Examples: "add dark mode", "create API endpoint", "implement..."

## Rules
1. Respond with exactly one: /chore, /bug, /feature, or 0
2. If unclear, prefer /chore (safest default)
3. If multiple types, choose the primary purpose

## Issue
$ARGUMENTS
```

## Classification Accuracy

### Testing Classification

```bash
# Test chores
claude -p "/classify-issue 'Update all dependencies'"
# Expected: /chore

claude -p "/classify-issue 'Clean up unused imports'"
# Expected: /chore

# Test bugs
claude -p "/classify-issue 'Login form submits twice on enter'"
# Expected: /bug

claude -p "/classify-issue '404 error on profile page'"
# Expected: /bug

# Test features
claude -p "/classify-issue 'Add dark mode toggle'"
# Expected: /feature

claude -p "/classify-issue 'Implement OAuth with Google'"
# Expected: /feature
```

### Handling Edge Cases

**Multi-type issues:**

```text
"Fix the broken login AND add remember me feature"

Approach: Classify by primary purpose
If equal: Request issue be split
```

**Unclear issues:**

```text
"Improve the performance"

Approach: Default to /chore
Rationale: Safest, lowest risk
```

**Not classifiable:**

```text
"Question about the API"

Approach: Return 0
Action: Human triage required
```

## Custom Problem Classes

For specialized workflows, extend the base classes:

### Example: Refactor Class

```markdown
### /refactor
- Code restructuring
- Architecture changes
- Performance optimization
- No functional change

Examples: "refactor auth module", "optimize queries", "restructure..."
```

### Example: Security Class

```markdown
### /security
- Vulnerability fixes
- Security improvements
- Access control changes
- Compliance requirements

Examples: "fix XSS vulnerability", "add rate limiting", "update auth..."
```

## Integration with ADW

In your ADW orchestrator:

```python
def classify_and_route(issue):
    # Classify
    result = execute_agent("classifier", issue)
    issue_type = parse_classification(result)

    # Route to template
    if issue_type == "/chore":
        return execute_agent("planner", "/chore", issue)
    elif issue_type == "/bug":
        return execute_agent("planner", "/bug", issue)
    elif issue_type == "/feature":
        return execute_agent("planner", "/feature", issue)
    else:
        return mark_for_triage(issue)
```

## Model Selection

For classification, use Haiku:

| Model | Speed | Cost | Accuracy |
| --- | --- | --- | --- |
| Haiku | Fast | Low | Good for simple decisions |
| Sonnet | Medium | Medium | Better for nuanced cases |

Haiku is usually sufficient since classification is a simple decision.

## Quality Metrics

Track classification quality:

- **Accuracy**: % correctly classified
- **Confusion matrix**: Which misclassifications happen
- **Override rate**: How often humans change classification

## Related Memory Files

- @piter-framework.md - Classification is the "I" in PITER
- @adw-anatomy.md - How classification fits in ADW
- @template-engineering.md - Templates for each class

## Version History

- **v1.0.0** (2025-12-26): Initial release

---

## Last Updated

**Date:** 2025-12-26
**Model:** claude-opus-4-5-20251101
