---
name: code-search-assistant
description: Search code repositories for code related to a given code snippet, ranking results by call chain similarity, textual similarity, and functional similarity. Use when finding related code, locating similar implementations, discovering code dependencies, or identifying code that performs similar operations. Outputs ranked file lists with matching code snippets and relevance scores.
---

# Code Search Assistant

## Overview

Search codebases to find code related to a given snippet using multi-dimensional similarity analysis: call chain patterns, textual structure, and functional behavior. Results are ranked and presented with matching code snippets.

## Workflow

### 1. Analyze Input Snippet

Extract key characteristics from the provided code snippet:

**Structural elements**:
- Function/method calls made
- Classes/types used
- Control flow patterns (loops, conditionals, try-catch)
- Data structures (arrays, objects, maps)

**Functional elements**:
- Purpose/intent of the code
- Input/output behavior
- Side effects (I/O, state changes, API calls)
- Domain concepts (authentication, validation, transformation)

**Textual elements**:
- Variable and function names
- String literals and constants
- Comments and documentation
- Code tokens and keywords

### 2. Define Search Scope

Determine where to search:
- **Full repository**: Search all code files
- **Specific directories**: Focus on relevant modules
- **File type filter**: Limit to specific languages

Use Glob to identify candidate files:
```
**/*.js, **/*.py, **/*.java, etc.
```

### 3. Search by Call Chain Similarity

Find code with similar function call patterns and dependencies.

**Search strategy**:
1. Extract function/method calls from input snippet
2. Use Grep to find files containing those function calls
3. Read matching files to analyze call sequences
4. Score based on:
   - Number of shared function calls (weight: 40%)
   - Order of function calls (weight: 30%)
   - Shared imported modules/libraries (weight: 30%)

**Example**:
```javascript
// Input snippet calls: fetch(), JSON.parse(), setState()
// High match: Code that calls fetch() → JSON.parse() → setState()
// Medium match: Code that calls fetch() and setState() in different order
// Low match: Code that only calls fetch()
```

### 4. Search by Textual Similarity

Find code with similar structure and token patterns.

**Search strategy**:
1. Extract key identifiers from input snippet (function names, variable names)
2. Use Grep to find files with similar identifiers
3. Read matching files to compare code structure
4. Score based on:
   - Shared variable/function names (weight: 35%)
   - Similar control flow structure (weight: 35%)
   - Shared keywords and operators (weight: 30%)

**Similarity indicators**:
- Same loop patterns (for, while, forEach, map)
- Similar conditional logic (if-else chains, switch statements)
- Matching data structure operations (array methods, object access)
- Similar string/number operations

### 5. Search by Functional Similarity

Find code that performs similar operations or solves similar problems.

**Search strategy**:
1. Identify the functional purpose of input snippet
2. Search for code with similar purpose using semantic patterns
3. Look for:
   - Similar input/output transformations
   - Equivalent algorithms (different implementations, same result)
   - Parallel business logic
   - Alternative approaches to same problem

**Functional categories**:
- **Data transformation**: Mapping, filtering, reducing, sorting
- **Validation**: Input checking, format validation, constraint enforcement
- **I/O operations**: File reading/writing, API calls, database queries
- **Authentication/Authorization**: Login, permission checks, token handling
- **Error handling**: Try-catch patterns, error recovery, logging

**Search patterns**:
```
// For validation code, search for:
- "validate", "check", "verify" in function names
- Conditional checks with error throwing
- Regular expression patterns

// For API calls, search for:
- HTTP client usage (fetch, axios, requests)
- Endpoint URLs or API patterns
- Response handling and error cases
```

### 6. Rank and Score Results

Combine similarity scores to rank results:

**Scoring formula**:
```
Total Score = (Call Chain Score × 0.35) +
              (Textual Score × 0.30) +
              (Functional Score × 0.35)
```

**Score ranges**:
- 0.8-1.0: Very high similarity (likely duplicate or variant)
- 0.6-0.8: High similarity (related implementation)
- 0.4-0.6: Medium similarity (similar patterns or purpose)
- 0.2-0.4: Low similarity (some shared elements)
- 0.0-0.2: Minimal similarity (weak connection)

**Ranking adjustments**:
- Boost files in same directory (+10%)
- Boost files with similar names (+5%)
- Penalize test files (-10%) unless input is a test
- Penalize generated/vendor code (-20%)

### 7. Format Results

Present results in ranked order with context:

**Result format**:
```markdown
## Search Results for: [Brief snippet description]

### 1. [file_path] (Score: 0.85)

**Similarity breakdown**:
- Call chain: 0.90 (shares fetch, JSON.parse, setState calls)
- Textual: 0.75 (similar variable names and structure)
- Functional: 0.90 (performs same data fetching and state update)

**Matching code** (lines 45-62):
```[language]
[relevant code snippet from the file]
```

**Why it matches**: [Brief explanation of similarity]

---

### 2. [file_path] (Score: 0.72)
[... repeat format ...]
```

**Output guidelines**:
- Show top 10 results by default
- Include file path with line numbers
- Show relevant code snippet (10-20 lines)
- Explain why each result matches
- Group results by score tier if many results

## Search Optimization Tips

**For better call chain matching**:
- Include import statements in input snippet
- Provide complete function calls with arguments
- Include chained method calls

**For better textual matching**:
- Use descriptive variable names in input
- Include comments describing intent
- Provide complete code blocks, not fragments

**For better functional matching**:
- Describe what the code does in comments
- Include typical input/output examples
- Show error handling patterns

## Example Usage

**Input snippet**:
```javascript
async function fetchUserData(userId) {
  try {
    const response = await fetch(`/api/users/${userId}`);
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Failed to fetch user:', error);
    return null;
  }
}
```

**Search process**:
1. Call chain: Search for `fetch()`, `response.json()`, `console.error()`
2. Textual: Search for async functions with try-catch, similar variable names
3. Functional: Search for API data fetching patterns, error handling

**Expected results**:
- Other API fetch functions (high similarity)
- Data retrieval functions using different libraries (medium similarity)
- Functions with similar error handling (low-medium similarity)

## Tips

- Start with a complete, representative code snippet (10-30 lines)
- Include context (imports, surrounding code) for better matching
- For large codebases, narrow search scope to relevant directories
- Adjust score weights based on what matters most (calls vs. structure vs. purpose)
- Review medium-scored results (0.4-0.6) for unexpected but useful matches
- Use results to discover alternative implementations or refactoring opportunities
