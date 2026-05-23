---
name: write-pr-desc
description: Generate a GitHub Pull Request description. Creates structured, reviewer-centric PR descriptions with title, summary, why (before/after), implementation details, and impact. Use when user says "write PR description", "PR desc", "describe this PR", or "generate PR description".
compatibility: Requires git for diff context, optionally gh CLI for PR metadata.
---

# Write PR Description

Generate a concise, factual, reviewer-centric Pull Request description.

## Core Principles

- Be concise, factual, and reviewer-centric
- Use short sentences, bullet points, and specific nouns
- Present tense, active voice
- Never make up information — only use what's in the code
- Focus on "why" over "what" — the diff shows what changed

## Process

1. Get the diff context (staged changes, branch diff, or PR diff)
2. Understand what changed and why
3. Generate description following the template below

## Required Sections

### Title (50 chars max)

Use imperative mood that completes: "If applied, this PR will..."
- Start with action verb: Add/Fix/Update/Remove/Refactor
- Capitalize first word, no period

### Summary

Brief overview explaining what this PR accomplishes:
- Primary change using imperative mood
- Scope: packages/modules affected
- Root cause (for bugs) or motivation (for features)
- Feature flags or configuration changes

### Why

Show the problem and solution through scenarios.

```markdown
### [Component/Feature Name]
[One-line problem statement]

**Before:**
- Scenario: [specific situation] → [problem/outcome]
- Impact: [user/system effect]

[ASCII diagram if it clarifies flow - 5-10 lines]

**After:**
- Scenario: [same situation] → [fixed outcome]
- Impact: [improvement achieved]

[ASCII diagram of new flow if needed]
```

### Implementation

3-5 bullets covering technical approach:
- Key design decisions and trade-offs
- New interfaces or patterns introduced
- Breaking changes or migrations
- Why this approach over alternatives
- Reference related commits if multiple logical changes

### Impact & Testing

```markdown
**Risk:** [One line - what could break]

**Changes:**
- Performance: [complexity/latency if significant]
- Behavior: [user-facing/API changes]
- Security: [auth/data access if relevant]

**Testing:**
- Coverage: [what's tested]
- Manual validation: [if needed]

**Rollout:**
- [Feature flags, compatibility notes]
```

### Related

- Links: [issues, RFCs]
- Follow-ups: [TODOs with owners]

## Constraints

- Max ~200 lines total
- Every section must add unique value
- Concrete examples > abstract descriptions
- Scenario-driven explanations
- Include ASCII diagrams only when they clarify architecture

## Examples

See [EXAMPLES.md](EXAMPLES.md) for bug fix and feature PR examples.
