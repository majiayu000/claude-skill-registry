---
name: Scouting Code Patterns
description: Find and document external code patterns from public sources. Use when user mentions 'find examples', 'scout patterns', 'research implementations', or starting new feature without precedent.
---

# Pattern Scout

## When to Use
- User asks to "find examples"
- Starting new feature without precedent
- Need to research best practices
- References docs/prompts/SCOUT-*

## Process
1. Read PRP from docs/prps/ for context
2. Search for 3-5 public examples (MIT/Apache licenses)
3. For each, document:
   - PATTERN name
   - USE WHEN scenarios
   - KEY CONCEPTS
   - Minimal compilable stub
   - VALIDATION approach
4. Save to examples/[category]/
5. Include Source URL
6. Run npm run sync to update CLAUDE.md

## Output Format
Create files in examples/[category]/:
```
// PATTERN: [name]
// USE WHEN: [scenarios]
// SOURCE: [URL]
// VALIDATION: [how to test]

[minimal compilable code]
```

## Anti-patterns
- Don't paste proprietary code
- Don't include non-working examples
- Always provide source attribution