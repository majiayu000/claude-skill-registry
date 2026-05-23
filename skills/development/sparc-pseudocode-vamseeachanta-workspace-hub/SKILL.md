---
name: sparc-pseudocode
description: SPARC Pseudocode phase specialist for algorithm design, data structure selection, complexity analysis, and design pattern identification
version: 1.0.0
category: development
type: hybrid
capabilities:
  - algorithm_design
  - logic_flow
  - data_structures
  - complexity_analysis
  - pattern_selection
tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - mcp__claude-flow__memory_usage
  - mcp__claude-flow__task_orchestrate
related_skills:
  - sparc-specification
  - sparc-architecture
  - sparc-refinement
hooks:
  pre: |
    echo "SPARC Pseudocode phase initiated"
    memory_store "sparc_phase" "pseudocode"
    # Retrieve specification from memory
    memory_search "spec_complete" | tail -1
  post: |
    echo "Pseudocode phase complete"
    memory_store "pseudo_complete_$(date +%s)" "Algorithms designed"
---

# SPARC Pseudocode Agent

> Algorithm design specialist focused on translating specifications into clear, efficient algorithmic logic for the SPARC methodology.

## Quick Start

```bash
# Invoke SPARC Pseudocode phase
npx claude-flow sparc run spec-pseudocode "Design authentication algorithm"

# Or directly in Claude Code
# "Use SPARC pseudocode to design the login flow algorithm"
```

## When to Use

- Translating specifications into algorithmic solutions
- Designing data structures for optimal performance
- Analyzing time and space complexity
- Selecting appropriate design patterns
- Creating implementation roadmaps for developers

## Prerequisites

- Completed specification phase with clear requirements
- Understanding of data structure trade-offs
- Knowledge of common algorithm patterns
- Familiarity with complexity analysis

## Core Concepts

### SPARC Pseudocode Phase

The Pseudocode phase bridges specifications and implementation:

1. **Design algorithmic solutions** - Language-agnostic logic
2. **Select optimal data structures** - Based on access patterns
3. **Analyze complexity** - Time and space requirements
4. **Identify design patterns** - Reusable solutions
5. **Create implementation roadmap** - Guide for developers

### Complexity Classes

| Class | Description | Example |
|-------|-------------|---------|
| O(1) | Constant | Hash lookup |
| O(log n) | Logarithmic | Binary search |
| O(n) | Linear | Array scan |
| O(n log n) | Linearithmic | Merge sort |
| O(n^2) | Quadratic | Nested loops |

## Implementation Pattern

### Algorithm Structure

```
ALGORITHM: AuthenticateUser
INPUT: email (string), password (string)
OUTPUT: user (User object) or error

BEGIN
    // Validate inputs
    IF email is empty OR password is empty THEN
        RETURN error("Invalid credentials")
    END IF

    // Retrieve user from database
    user <- Database.findUserByEmail(email)

    IF user is null THEN
        RETURN error("User not found")
    END IF

    // Verify password
    isValid <- PasswordHasher.verify(password, user.passwordHash)

    IF NOT isValid THEN
        // Log failed attempt
        SecurityLog.logFailedLogin(email)
        RETURN error("Invalid credentials")
    END IF

    // Create session
    session <- CreateUserSession(user)

    RETURN {user: user, session: session}
END
```

### Data Structure Selection

```
DATA STRUCTURES:

UserCache:
    Type: LRU Cache with TTL
    Size: 10,000 entries
    TTL: 5 minutes
    Purpose: Reduce database queries for active users

    Operations:
        - get(userId): O(1)
        - set(userId, userData): O(1)
        - evict(): O(1)

PermissionTree:
    Type: Trie (Prefix Tree)
    Purpose: Efficient permission checking

    Structure:
        root
        +-- users
        |   +-- read
        |   +-- write
        |   +-- delete
        +-- admin
            +-- system
            +-- users

    Operations:
        - hasPermission(path): O(m) where m = path length
        - addPermission(path): O(m)
        - removePermission(path): O(m)
```

### Algorithm Patterns

```
PATTERN: Rate Limiting (Token Bucket)

ALGORITHM: CheckRateLimit
INPUT: userId (string), action (string)
OUTPUT: allowed (boolean)

CONSTANTS:
    BUCKET_SIZE = 100
    REFILL_RATE = 10 per second

BEGIN
    bucket <- RateLimitBuckets.get(userId + action)

    IF bucket is null THEN
        bucket <- CreateNewBucket(BUCKET_SIZE)
        RateLimitBuckets.set(userId + action, bucket)
    END IF

    // Refill tokens based on time elapsed
    currentTime <- GetCurrentTime()
    elapsed <- currentTime - bucket.lastRefill
    tokensToAdd <- elapsed * REFILL_RATE

    bucket.tokens <- MIN(bucket.tokens + tokensToAdd, BUCKET_SIZE)
    bucket.lastRefill <- currentTime

    // Check if request allowed
    IF bucket.tokens >= 1 THEN
        bucket.tokens <- bucket.tokens - 1
        RETURN true
    ELSE
        RETURN false
    END IF
END
```

## Configuration

```yaml
# sparc-pseudocode-config.yaml
pseudocode_settings:
  syntax_style: "structured"  # structured, functional, mixed
  include_complexity: true
  include_subroutines: true

complexity_analysis:
  report_time: true
  report_space: true
  include_best_case: false
  include_worst_case: true
  include_average_case: true

patterns:
  catalog: ["strategy", "observer", "factory", "singleton", "decorator"]
  document_rationale: true
```

## Usage Examples

### Example 1: Search Algorithm

```
ALGORITHM: OptimizedSearch
INPUT: query (string), filters (object), limit (integer)
OUTPUT: results (array of items)

SUBROUTINES:
    BuildSearchIndex()
    ScoreResult(item, query)
    ApplyFilters(items, filters)

BEGIN
    // Phase 1: Query preprocessing
    normalizedQuery <- NormalizeText(query)
    queryTokens <- Tokenize(normalizedQuery)

    // Phase 2: Index lookup
    candidates <- SET()
    FOR EACH token IN queryTokens DO
        matches <- SearchIndex.get(token)
        candidates <- candidates UNION matches
    END FOR

    // Phase 3: Scoring and ranking
    scoredResults <- []
    FOR EACH item IN candidates DO
        IF PassesPrefilter(item, filters) THEN
            score <- ScoreResult(item, queryTokens)
            scoredResults.append({item: item, score: score})
        END IF
    END FOR

    // Phase 4: Sort and filter
    scoredResults.sortByDescending(score)
    finalResults <- ApplyFilters(scoredResults, filters)

    // Phase 5: Pagination
    RETURN finalResults.slice(0, limit)
END

SUBROUTINE: ScoreResult
INPUT: item, queryTokens
OUTPUT: score (float)

BEGIN
    score <- 0

    // Title match (highest weight)
    titleMatches <- CountTokenMatches(item.title, queryTokens)
    score <- score + (titleMatches * 10)

    // Description match (medium weight)
    descMatches <- CountTokenMatches(item.description, queryTokens)
    score <- score + (descMatches * 5)

    // Tag match (lower weight)
    tagMatches <- CountTokenMatches(item.tags, queryTokens)
    score <- score + (tagMatches * 2)

    // Boost by recency
    daysSinceUpdate <- (CurrentDate - item.updatedAt).days
    recencyBoost <- 1 / (1 + daysSinceUpdate * 0.1)
    score <- score * recencyBoost

    RETURN score
END
```

### Example 2: Design Patterns

```
PATTERN: Strategy Pattern

INTERFACE: AuthenticationStrategy
    authenticate(credentials): User or Error

CLASS: EmailPasswordStrategy IMPLEMENTS AuthenticationStrategy
    authenticate(credentials):
        // Email/password logic

CLASS: OAuthStrategy IMPLEMENTS AuthenticationStrategy
    authenticate(credentials):
        // OAuth logic

CLASS: AuthenticationContext
    strategy: AuthenticationStrategy

    executeAuthentication(credentials):
        RETURN strategy.authenticate(credentials)

---

PATTERN: Observer Pattern

CLASS: EventEmitter
    listeners: Map<eventName, List<callback>>

    on(eventName, callback):
        IF NOT listeners.has(eventName) THEN
            listeners.set(eventName, [])
        END IF
        listeners.get(eventName).append(callback)

    emit(eventName, data):
        IF listeners.has(eventName) THEN
            FOR EACH callback IN listeners.get(eventName) DO
                callback(data)
            END FOR
        END IF
```

### Example 3: Complexity Analysis

```
ANALYSIS: User Authentication Flow

Time Complexity:
    - Email validation: O(1)
    - Database lookup: O(log n) with index
    - Password verification: O(1) - fixed bcrypt rounds
    - Session creation: O(1)
    - Total: O(log n)

Space Complexity:
    - Input storage: O(1)
    - User object: O(1)
    - Session data: O(1)
    - Total: O(1)

ANALYSIS: Search Algorithm

Time Complexity:
    - Query preprocessing: O(m) where m = query length
    - Index lookup: O(k * log n) where k = token count
    - Scoring: O(p) where p = candidate count
    - Sorting: O(p log p)
    - Filtering: O(p)
    - Total: O(p log p) dominated by sorting

Space Complexity:
    - Token storage: O(k)
    - Candidate set: O(p)
    - Scored results: O(p)
    - Total: O(p)

Optimization Notes:
    - Use inverted index for O(1) token lookup
    - Implement early termination for large result sets
    - Consider approximate algorithms for >10k results
```

## Execution Checklist

- [ ] Read and understand specifications
- [ ] Design main algorithm with clear INPUT/OUTPUT
- [ ] Identify subroutines and helper functions
- [ ] Select appropriate data structures
- [ ] Write complexity analysis (time and space)
- [ ] Identify applicable design patterns
- [ ] Document optimization opportunities
- [ ] Review for edge cases
- [ ] Validate against specifications

## Best Practices

1. **Language Agnostic**: Don't use language-specific syntax
2. **Clear Logic**: Focus on algorithm flow, not implementation details
3. **Handle Edge Cases**: Include error handling in pseudocode
4. **Document Complexity**: Always analyze time/space complexity
5. **Use Meaningful Names**: Variable names should explain purpose
6. **Modular Design**: Break complex algorithms into subroutines

## Error Handling

| Issue | Resolution |
|-------|------------|
| Unclear complexity | Break down into primitive operations |
| Missing edge cases | Review input validation and error paths |
| Overly complex | Decompose into smaller subroutines |
| No data structure justification | Document access patterns and requirements |

## Metrics & Success Criteria

- All algorithms have documented complexity
- Subroutines are clearly defined
- Data structures are justified with operations
- Design patterns are identified where applicable
- Pseudocode is language-agnostic

## Integration Points

### MCP Tools

```javascript
// Store pseudocode phase completion
mcp__claude-flow__memory_usage {
  action: "store",
  key: "sparc/pseudocode/algorithms",
  namespace: "coordination",
  value: JSON.stringify({
    algorithms: ["AuthenticateUser", "CheckRateLimit"],
    patterns: ["strategy", "observer"],
    complexity: "O(log n)",
    timestamp: Date.now()
  })
}
```

### Hooks

```bash
# Pre-pseudocode hook
npx claude-flow@alpha hooks pre-task --description "SPARC Pseudocode phase"

# Post-pseudocode hook
npx claude-flow@alpha hooks post-task --task-id "pseudo-complete"
```

### Related Skills

- [sparc-specification](../sparc-specification/SKILL.md) - Previous phase: requirements
- [sparc-architecture](../sparc-architecture/SKILL.md) - Next phase: system design
- [sparc-refinement](../sparc-refinement/SKILL.md) - TDD implementation phase

## References

- [SPARC Methodology](https://github.com/ruvnet/claude-flow)
- [Big O Notation](https://en.wikipedia.org/wiki/Big_O_notation)
- [Design Patterns](https://refactoring.guru/design-patterns)

## Version History

- **1.0.0** (2026-01-02): Initial release - converted from agent to skill format
