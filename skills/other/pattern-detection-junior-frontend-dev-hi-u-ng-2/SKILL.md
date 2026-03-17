---
name: pattern-detection
description: Detect and document existing code patterns in a codebase. Use to
  maintain consistency with established conventions when writing new code.
---

# Pattern Detection Skill

## Purpose
Identify and document patterns for consistency enforcement.

## Pattern Categories

### 1. Naming Conventions
Reference: [patterns/naming-conventions.md](patterns/naming-conventions.md)

Detection method:
- Sample 10+ files across different directories
- Extract function/class/variable names
- Identify dominant patterns

### 2. Error Handling
Reference: [patterns/error-handling.md](patterns/error-handling.md)

Detection method:
- Search for try/catch blocks
- Find custom error classes
- Check for error middleware

### 3. Testing Patterns
Reference: [patterns/testing-patterns.md](patterns/testing-patterns.md)

Detection method:
- Locate test files
- Analyze test structure
- Identify mocking approach

## Consistency Scoring

Rate codebase consistency:
- **High (90%+)**: Strong patterns, few deviations
- **Medium (70-89%)**: Clear patterns with some variation
- **Low (<70%)**: Inconsistent, needs standardization

## Output Format
Create patterns document with:
1. Detected patterns with examples
2. Consistency score per category
3. Deviation examples
4. Recommendations for standardization

## Storage Location
Save to: `docs/research/patterns-{date}.md`
