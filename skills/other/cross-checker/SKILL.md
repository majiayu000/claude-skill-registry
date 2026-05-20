---
name: cross-checker
description: Verify every claim from multiple independent angles -- code, docs, tests, git history. Use when you need high confidence that something is correct before acting on it.
---

# Cross-Checker: Multi-Angle Verification

Never trust a single source. Verify from at least two independent angles before accepting a claim as fact.

## The cross-checking method

For any claim, check it against multiple sources:

### Source 1: The code itself
Read the actual file. What does the code do?
This is the strongest evidence.

### Source 2: Tests
What do the tests expect? Tests reveal intended behavior.
If a test expects validateToken to return false for expired tokens, that's the designed behavior.

### Source 3: Git history
What was the original intent? Git blame and commit messages reveal why code was written.
"commit abc123: fix token expiration check to reject tokens older than 24h"

### Source 4: Documentation
README, comments, JSDoc, API docs. Do they match the code?
If docs say one thing and code does another, the code is truth but the discrepancy matters.

### Source 5: Configuration
Config files, environment variables, feature flags.
Runtime behavior may differ from what the code looks like.

### Source 6: Dependencies
Package versions, API compatibility, deprecated features.
A function might exist in the code but be broken due to a dependency update.

## Minimum verification standard

| Situation | Minimum angles needed |
|-----------|----------------------|
| Stating a fact to the user | 1 (read the code) |
| Recommending a code change | 2 (code + tests or git history) |
| Security-related claims | 3 (code + tests + docs/config) |
| Production deployment advice | 3 (code + config + git history) |
| "This is safe to delete" | 3 (code + grep for references + tests) |

## Cross-check workflow

1. Make the initial claim based on what you know
2. Identify which type of claim it is (fact, recommendation, security)
3. Check the required number of angles
4. If sources agree: proceed with confidence
5. If sources disagree: flag the discrepancy, investigate further
6. If sources are insufficient: say so, suggest how to get more evidence

## Red flags that demand cross-checking

- "This function is never called" (grep the entire codebase first)
- "This file isn't used anymore" (check imports, configs, build scripts)
- "This dependency can be removed" (check all import statements)
- "This environment variable isn't needed" (check all config files and deploy scripts)
- "This test is redundant" (check what specific edge case it covers)
