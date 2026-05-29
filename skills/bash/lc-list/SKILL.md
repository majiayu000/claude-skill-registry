---
name: lc-list
description: List LeetCode problems by difficulty level (easy/medium/hard)
---

# LeetCode List

List LeetCode problems.

## Usage

`/lc-list` - List all problems
`/lc-list easy` - List Easy problems only
`/lc-list medium` - List Medium problems only
`/lc-list hard` - List Hard problems only

## Instructions

Run the appropriate leetcode-cli command based on the argument:

- No argument or "all": `leetcode list 2>/dev/null | head -30`
- "easy": `leetcode list -q eL 2>/dev/null | head -30`
- "medium": `leetcode list -q mL 2>/dev/null | head -30`
- "hard": `leetcode list -q hL 2>/dev/null | head -30`

Show the results to the user.
