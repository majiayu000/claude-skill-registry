---
name: ai-prompt
description: "Use when optimizing prompts, skill descriptions, or agent instructions for clarity, specificity, and behavioral effectiveness."
effort: high
argument-hint: "<text>|--skill <name>"
---


# Prompt

## Purpose

Prompt optimization and creation. Improves prompts, skill descriptions, and agent instructions using proven techniques: explicit over implicit, examples over rules, structured formatting, and positive framing. Can auto-enhance prompts for other skills or manually optimize user-provided text.

## Trigger

- Command: `/ai-prompt "<text>"` (optimize text) or `/ai-prompt --skill <name>` (optimize a skill's description)
- Context: writing a new prompt, improving an existing skill's description, crafting agent instructions.

## When to Use

- Writing or refining skill `description` fields (CSO optimization)
- Crafting system prompts for AI integrations
- Improving agent instruction clarity
- Before publishing any prompt-based artifact

## Optimization Techniques

Apply these in order of impact:

### 1. Be Explicit Over Implicit

| Before | After |
|--------|-------|
| "Handle errors properly" | "Wrap database calls in try/except, log the exception with stack trace, return a structured error response with HTTP 500" |
| "Follow best practices" | "Apply guard clauses for early return, extract methods over 20 lines, name variables by intent not type" |

### 2. Show, Do Not Tell

Replace rules with examples. One concrete example is worth five abstract instructions.

```
Bad:  "Use descriptive names"
Good: "Name variables by what they represent:
       - `user_count` not `n`
       - `is_valid` not `flag`
       - `retry_delay_seconds` not `delay`"
```

### 3. Structure with XML Tags or Markdown

Use clear structural markers for different sections. Group related instructions. Use tables for multi-dimensional comparisons.

### 4. Explain WHY for Each Rule

Rules without rationale get ignored or misapplied. Every constraint should include its motivation.

```
Bad:  "Max 3 retries"
Good: "Max 3 retries (beyond 3, the underlying issue is systemic, not transient -- escalate instead of retrying)"
```

### 5. Positive Framing

State what TO do, not what NOT to do. The brain processes positive instructions faster.

```
Bad:  "Don't use generic error messages"
Good: "Include the specific operation, input value, and expected format in every error message"
```

### 6. CSO Optimization (for skill descriptions)

The `description` field is a search query match surface. Optimize for triggering conditions, not capability summaries.

Pattern: `"Use when [specific situation + observable trigger]"`

```
Bad:  "Database migration planning tool"
Good: "Use when planning database schema changes, assessing migration locking impact, or designing rollback procedures"
```

### 7. Cialdini Principles (for discipline-enforcing skills)

For skills that enforce process (guard, verify, commit):
- **Authority**: cite specific standards and their rationale
- **Consistency**: reference past decisions and established patterns
- **Social proof**: "teams that skip this step spend 3x longer debugging"

## Procedure

### Optimizing text

1. **Analyze** -- identify which techniques are missing from the input.
2. **Apply** -- rewrite applying all relevant techniques.
3. **Compare** -- present before/after with annotations explaining each change.
4. **Validate** -- check the optimized version is not longer than necessary (concise beats comprehensive).

### Optimizing a skill description

1. **Read skill** -- load `.claude/skills/ai-{name}/SKILL.md`.
2. **Extract current description** -- from frontmatter.
3. **CSO-optimize** -- rewrite using triggering-condition pattern.
4. **Present** -- show before/after for approval.
5. **Apply** -- update the frontmatter if approved.

## Quick Reference

```
/ai-prompt "check if the code follows our standards"   # optimize this text
/ai-prompt --skill guard                                 # optimize guard's description
/ai-prompt --skill commit                                # optimize commit's description
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Optimizing for length (making it longer = better) | Concise and specific beats long and vague |
| Adding hedging language ("try to", "if possible") | Be direct: state the expected behavior |
| Removing context while shortening | Keep the WHY, remove the fluff |

$ARGUMENTS
