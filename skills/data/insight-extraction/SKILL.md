---
name: insight-extraction
description: 'Extract actionable insights from completed coding sessions. Use when a session completes to capture learnings for future sessions.'
version: 1.0.0
model: sonnet
invoked_by: both
user_invocable: true
tools: [Read, Write, Bash, Glob, Grep]
best_practices:
  - Extract ACTIONABLE knowledge, not logs
  - Every insight should help future sessions do something better
  - Be specific about files, patterns, and gotchas
error_handling: graceful
streaming: supported
source: auto-claude
---

# Insight Extraction Skill

## Overview

Analyze completed coding sessions and extract structured learnings for the memory system. Insights help future sessions avoid mistakes, follow established patterns, and understand the codebase faster.

**Core principle:** Extract ACTIONABLE knowledge, not logs. Every insight should help a future session do something better.

## When to Use

**Always:**

- After completing a coding task
- After fixing bugs
- After discovering new patterns
- After failed attempts (especially valuable)

**Exceptions:**

- Trivial changes with no learnings
- Documentation-only changes

## The Iron Law

```
NO SESSION END WITHOUT INSIGHT EXTRACTION FOR NON-TRIVIAL WORK
```

Non-trivial sessions should capture learnings before context is lost.

## Input Required

To extract insights, you need:

1. **Git diff** - What files changed and how
2. **Task description** - What was being implemented
3. **Attempt history** - Previous tries (if any), what approaches were used
4. **Session outcome** - Success or failure

## Workflow

### Phase 1: Gather Session Data

```bash
# Get the diff of changes
git diff HEAD~1 --stat
git diff HEAD~1

# Get commit message
git log -1 --pretty=format:"%s%n%n%b"

# Get list of modified files
git diff HEAD~1 --name-only
```

### Phase 2: Analyze File Insights

For each modified file, extract:

- **Purpose**: What role does this file play?
- **Changes made**: What was the modification? Focus on the "why" not just "what"
- **Patterns used**: What coding patterns were applied?
- **Gotchas**: Any file-specific traps?

**Good example:**

```json
{
  "path": "src/stores/terminal-store.ts",
  "purpose": "Zustand store managing terminal session state with immer middleware",
  "changes_made": "Added setAssociatedTask action to link terminals with tasks",
  "patterns_used": ["Zustand action pattern", "immer state mutation"],
  "gotchas": ["State changes must go through actions, not direct mutation"]
}
```

**Bad example (too vague):**

```json
{
  "path": "src/stores/terminal-store.ts",
  "purpose": "A store file",
  "changes_made": "Added some code",
  "patterns_used": [],
  "gotchas": []
}
```

### Phase 3: Extract Patterns

Only extract patterns that are **reusable**:

- Must apply to more than just this one case
- Include where/when to apply the pattern
- Reference a concrete example in the codebase

**Good example:**

```json
{
  "pattern": "Use e.stopPropagation() on interactive elements inside containers with onClick handlers",
  "applies_to": "Any clickable element nested inside a parent with click handling",
  "example": "Terminal.tsx header - dropdown needs stopPropagation to prevent focus stealing"
}
```

### Phase 4: Document Gotchas

Must be **specific** and **actionable**:

- Include what triggers the problem
- Include how to solve or prevent it
- Avoid generic advice ("be careful with X")

**Good example:**

```json
{
  "gotcha": "Terminal header onClick steals focus from child interactive elements",
  "trigger": "Adding buttons/dropdowns to Terminal header without stopPropagation",
  "solution": "Call e.stopPropagation() in onClick handlers of child elements"
}
```

### Phase 5: Document Approach Outcome

Capture the learning from success or failure:

- If **succeeded**: What made this approach work? What was key?
- If **failed**: Why did it fail? What would have worked instead?
- **Alternatives tried**: What other approaches were attempted?

This helps future sessions learn from past attempts.

### Phase 6: Generate Recommendations

Specific, actionable advice for future work:

- Must be implementable by a future session
- Should be specific to this codebase, not generic
- Focus on what's next or what to watch out for

**Good:** "When adding more controls to Terminal header, follow the dropdown pattern in this session - use stopPropagation and position relative to header"

**Bad:** "Write good code" or "Test thoroughly"

### Phase 7: Output Structured Insights

Create the structured insight output:

```markdown
# Session Insights: [Task Name]

## Date

[timestamp]

## Task

[Description of what was being implemented]

## Outcome

[SUCCESS/FAILURE]

## File Insights

### [file-path]

- **Purpose**: [what this file does]
- **Changes**: [what was changed and why]
- **Patterns**: [patterns used]
- **Gotchas**: [things to watch out for]

## Patterns Discovered

### [Pattern Name]

- **Pattern**: [description]
- **Applies to**: [when to use]
- **Example**: [file or code reference]

## Gotchas Discovered

### [Gotcha Name]

- **Issue**: [what to avoid]
- **Trigger**: [what causes it]
- **Solution**: [how to handle]

## Approach Analysis

### What Worked

[Description of successful approach]

### What Failed (if applicable)

[Description of failed approaches and why]

### Alternatives Tried

[List of other approaches attempted]

## Recommendations for Future Sessions

1. [Specific recommendation 1]
2. [Specific recommendation 2]
```

Save to `.claude/context/memory/learnings.md` (append).

## Handling Edge Cases

### Empty or Minimal Diff

If the diff is very small or empty:

- Still extract file purposes if you can infer them
- Note that the session made minimal changes
- Focus on recommendations for next steps

### Failed Session

If the session failed:

- Focus on **why it failed** - this is the most valuable insight
- Extract what was learned from the failure
- Recommendations should address how to succeed next time

### Multiple Files Changed

- Prioritize the most important 3-5 files
- Skip boilerplate changes (package-lock.json, etc.)
- Focus on files central to the feature

## Verification Checklist

Before completing insight extraction:

- [ ] Git diff analyzed
- [ ] File insights extracted for key files
- [ ] Reusable patterns documented
- [ ] Gotchas documented with triggers and solutions
- [ ] Approach outcome documented
- [ ] Recommendations are specific and actionable
- [ ] Insights saved to memory file

## Common Mistakes

### Too Vague

**Why it's wrong:** "Fixed the bug" helps no one.

**Do this instead:** "Fixed race condition in useEffect by adding cleanup function. Pattern: always return cleanup from async effects."

### Generic Advice

**Why it's wrong:** "Test your code" is not actionable.

**Do this instead:** "Run `npm test src/stores` after changing store logic - the tests catch state management bugs."

### Missing Context

**Why it's wrong:** Future sessions won't understand why.

**Do this instead:** Include file paths, function names, and specific scenarios.

## Integration with Other Skills

This skill works well with:

- **session-handoff**: Use insights in handoff documents
- **summarize-changes**: Complement change summaries with insights
- **debugging**: Extract insights from debugging sessions

## Memory Protocol

**Before starting:**
Read `.claude/context/memory/learnings.md`

**After completing:**

- New pattern -> `.claude/context/memory/learnings.md`
- Issue found -> `.claude/context/memory/issues.md`
- Decision made -> `.claude/context/memory/decisions.md`

> ASSUME INTERRUPTION: If it's not in memory, it didn't happen.
