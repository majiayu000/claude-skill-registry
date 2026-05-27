---
name: code-pattern-extractor
description: Analyze codebases to identify reusable code patterns, duplications, and implementation patterns for future development. Use when refactoring code, identifying technical debt, finding opportunities for abstraction, or documenting common patterns in a directory or module. Outputs pattern catalogs, refactoring suggestions, and reusable template code.
---

# Code Pattern Extractor

## Overview

Systematically analyze code in directories or modules to identify recurring patterns, code duplication, and implementation patterns that can be abstracted into reusable components, utilities, or design patterns.

## Workflow

### 1. Define Analysis Scope

Identify the code to analyze:
- **Directory/module**: Analyze all files in a specific directory
- **File set**: Analyze a specific set of related files
- **Component**: Analyze files related to a specific feature or component

Use Glob to find relevant files:
```
**/*.js, **/*.py, **/*.go, etc.
```

### 2. Scan for Code Duplication

Identify repeated code blocks that appear multiple times:

**Look for**:
- Similar function implementations with minor variations
- Repeated code blocks (>5 lines) across files
- Copy-pasted code with slight modifications
- Similar class structures or method patterns

**Analysis criteria**:
- Similarity threshold: >70% code similarity
- Minimum size: 5+ lines of code
- Frequency: Appears 3+ times

### 3. Identify Implementation Patterns

Find recurring implementation approaches:

**Common patterns**:
- **API call patterns**: Similar fetch/request handling
- **Error handling**: Repeated try-catch or error checking
- **Data validation**: Similar input validation logic
- **Data transformation**: Repeated mapping/filtering operations
- **State management**: Similar state update patterns
- **Configuration**: Repeated configuration setup

**Example patterns to detect**:
```javascript
// Pattern: API call with error handling
async function fetchX() {
  try {
    const response = await fetch(url);
    if (!response.ok) throw new Error();
    return await response.json();
  } catch (error) {
    console.error(error);
    return null;
  }
}
```

### 4. Categorize Patterns

Group identified patterns by type and impact:

**Categories**:
- **High-value**: Appears frequently (5+ times), significant code size
- **Medium-value**: Appears moderately (3-4 times), moderate complexity
- **Low-value**: Appears rarely (2 times), simple code

**Pattern types**:
- Utility functions (data processing, formatting, validation)
- API/network patterns (requests, responses, error handling)
- UI patterns (component structures, event handling)
- Business logic patterns (calculations, rules, workflows)

### 5. Generate Pattern Catalog

Document each identified pattern:

**Pattern entry format**:
```markdown
## Pattern: [Descriptive Name]

**Type**: [Utility/API/UI/Business Logic]
**Frequency**: [Number of occurrences]
**Impact**: [High/Medium/Low]

**Description**: [What the pattern does]

**Current implementations**:
- `file1.js:45-60` - [Brief context]
- `file2.js:120-135` - [Brief context]
- `file3.js:89-104` - [Brief context]

**Common variations**:
- [Variation 1 description]
- [Variation 2 description]
```

### 6. Generate Refactoring Suggestions

For each high-value pattern, provide refactoring recommendations:

**Suggestion format**:
```markdown
### Refactoring: Extract [Pattern Name]

**Current state**: Pattern appears in [N] locations with [X]% code duplication

**Proposed solution**: Extract into [utility function/class/hook/module]

**Benefits**:
- Reduce code duplication by ~[N] lines
- Centralize logic for easier maintenance
- Improve testability

**Implementation approach**:
1. Create new file: `utils/[pattern-name].js`
2. Extract common logic with parameters for variations
3. Replace [N] occurrences with function calls
4. Add unit tests

**Estimated effort**: [Small/Medium/Large]
```

### 7. Generate Template Code

Create reusable template implementations for high-value patterns:

**Template format**:
```javascript
/**
 * [Pattern description]
 *
 * @param {type} param1 - [Description]
 * @param {type} param2 - [Description]
 * @returns {type} [Description]
 */
function patternTemplate(param1, param2) {
  // Extracted common logic
  // Parameterized variations
  // Return standardized result
}
```

Include:
- Function signature with parameters for variations
- Documentation comments
- Error handling
- Type annotations (if applicable)
- Usage examples

## Output Structure

Organize findings into a comprehensive report:

```markdown
# Code Pattern Analysis: [Directory/Module Name]

## Summary
- Files analyzed: [N]
- Patterns identified: [N]
- High-value patterns: [N]
- Estimated duplication: [N] lines

## Pattern Catalog
[List of all identified patterns with details]

## Refactoring Suggestions
[Prioritized list of refactoring opportunities]

## Template Code
[Reusable implementations for high-value patterns]

## Next Steps
[Recommended actions prioritized by impact]
```

## Pattern Detection Heuristics

**Code duplication detection**:
- Compare function bodies for structural similarity
- Ignore variable names and minor formatting differences
- Focus on logic flow and operations

**Implementation pattern detection**:
- Look for similar function signatures
- Identify repeated import patterns
- Find similar control flow structures (if-else, loops, try-catch)
- Detect repeated library usage patterns

**Abstraction opportunities**:
- Multiple functions with similar purpose but different parameters
- Repeated setup/teardown code
- Similar data transformations
- Parallel class hierarchies

## Tips

- Start with high-frequency patterns for maximum impact
- Consider language-specific idioms when suggesting abstractions
- Balance DRY principle with code clarity (don't over-abstract)
- Include migration path in refactoring suggestions
- Prioritize patterns that improve maintainability, not just reduce lines
- Consider existing project architecture when suggesting abstractions
- Document trade-offs (flexibility vs. simplicity)
- For large codebases, analyze one module at a time
