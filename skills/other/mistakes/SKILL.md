---
name: mistakes
description: Track and review mistake patterns with spaced repetition. Use when user wants to log a mistake, see their weak areas, or get targeted practice.
argument-hint: [log|list|stats|review|clear]
allowed-tools: Read, Write, Edit, Bash
---

Track and review the user's mistake patterns.

Action requested: $ARGUMENTS
(log | list | stats | review | clear)

If no action specified, show stats.

Categories tracked:
- edge-cases: Missing boundary conditions
- off-by-one: Index/loop errors
- complexity: Wrong time/space analysis
- pattern: Chose wrong algorithm
- syntax: Language-specific errors
- communication: Unclear explanation
- testing: Insufficient test cases

Actions:

**log**: Ask user to describe their mistake, then:
1. Categorize it
2. Store in data/mistakes.json with timestamp
3. Set next review date (spaced repetition)

**list**: Show all tracked mistakes with:
- Date logged
- Category
- Description
- Next review date

**stats**: Show frequency by category:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MISTAKE STATS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Edge Cases      ████████░░░░  8 (32%)
Off-by-One      ██████░░░░░░  6 (24%)
Complexity      ████░░░░░░░░  4 (16%)
...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total: 25 mistakes tracked

FOCUS AREAS:
Your top weakness is Edge Cases. Practice:
• Two Sum (empty array, single element)
• Valid Palindrome (empty string)
• Merge Intervals (no intervals)
```

**review**: Get 3 problems targeting the user's weakest category

**clear**: Reset mistake history (confirm first)
