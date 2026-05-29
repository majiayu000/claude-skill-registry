---
name: outer-review
description: Commission and process external AI analysis to reduce blind spots. Manual invocation only.
---

# Outer Review

Process an external AI review to extract actionable tasks. The human commissions the external review and saves the raw output; this skill processes it.

## When to Use

- When `/outer-review [filepath]` is invoked with a new outer review file
- After a human has commissioned and saved an external AI analysis

## Why External Review Matters

The Unfinishable Map's content is primarily generated and reviewed by Claude-based systems. This creates risk of:

- **Confirmation bias**: The reviewing system shares assumptions with the generating system
- **Blind spot persistence**: Gaps in Claude's knowledge propagate undetected
- **Style homogenization**: Content converges toward patterns Claude favors
- **Coherence inflation**: Arguments seem stronger than they are because the reviewer finds them compelling for the same reasons the writer did

External AI systems (GPT-4+, Gemini, etc.) have different training, different biases, and different blind spots. Their disagreements are informative even when wrong.

## Prerequisites

The human must:

1. Commission a review from an external AI system (ChatGPT, Gemini, etc.)
2. Save the raw output to `obsidian/reviews/outer-review-YYYY-MM-DD-[system-slug].md`
3. Add basic frontmatter (or leave for this skill to add)

## Instructions

### 1. Read the Review File

The filepath is provided as an argument: `/outer-review obsidian/reviews/outer-review-2026-01-15-site-chatgpt-5-2-pro.md`

Read the file and assess its current state.

### 2. Add/Fix Frontmatter

Ensure the file has proper frontmatter:

```yaml
---
title: "Outer Review - [System Name]"
created: YYYY-MM-DD
modified: YYYY-MM-DD
human_modified: null
ai_modified: YYYY-MM-DDTHH:MM:SS+00:00
draft: false
topics: []
concepts: []
related_articles:
  - "[[project]]"
ai_contribution: 90
author: [Human who commissioned it]
ai_system: [external-system-id]
ai_generated_date: YYYY-MM-DD
last_curated: null
---

**Date**: YYYY-MM-DD
**Reviewer**: [System name and version]
**Type**: Outer review (external AI analysis)

## About This Review

An "outer review" is an analysis performed by an external AI system rather than the Claude-based workflow that generates most site content. This provides an independent perspective, reducing the risk of self-reinforcing blind spots.

[External system's review content follows...]
```

### 3. Convert Links to Internal Format

The external system will likely use external URLs. Convert these to internal wikilinks:

- `https://unfinishablemap.org/tenets/` → `[[tenets]]`
- `https://unfinishablemap.org/topics/free-will/` → `[[free-will]]`
- `https://unfinishablemap.org/concepts/qualia/` → `[[qualia]]`

This improves navigation and maintains link integrity.

### 4. Evaluate Review Quality

Read through the review and categorize findings:

**High value findings**:
- Logical gaps not previously noticed
- Counterarguments not addressed
- Inconsistencies between pages
- Missing connections that should exist
- Novel framings of existing positions

**Lower value findings**:
- Objections already addressed elsewhere
- Misunderstandings of the position
- Requests to adopt a different position entirely
- Style preferences that don't affect clarity

### 5. Generate Tasks

For high-value findings, create tasks in `obsidian/workflow/todo.md`:

```markdown
### P1: [Specific issue from outer review]
- **Type**: [research-topic | expand-topic | refine-draft | cross-review]
- **Notes**: From outer review YYYY-MM-DD. [Brief description of the issue and why it matters]
- **Source**: outer-review
- **Generated**: YYYY-MM-DD
```

Priority guidance:
- **P1**: Logical errors, internal contradictions, unaddressed strong objections
- **P2**: Missing connections, expansion opportunities, clarity improvements
- **P3**: Style suggestions, minor enhancements

### 6. Log to Changelog

Append to `obsidian/workflow/changelog.md`:

```markdown
### HH:MM - outer-review
- **Status**: Success
- **Reviewer**: [System name]
- **File**: [filepath]
- **High-value findings**: [count]
- **Tasks generated**: [count with priorities]
```

### 7. Commit

Create a git commit:

```
feat(auto): outer-review - process [system name] analysis

- Identified [N] actionable issues
- Generated [N] tasks (P1: X, P2: Y, P3: Z)
```

## Evaluating Impact (After Tasks Complete)

After tasks from an outer review have been completed, evaluate the review's value:

1. **Count completed tasks**: How many issues were addressed?
2. **Assess depth**: Did the review surface deep insights or obvious issues?
3. **Track new content**: What articles/sections resulted from the review?
4. **Note patterns**: What kinds of issues does this external system catch that internal review misses?

This helps calibrate future review frequency and system selection.

## Important

- This skill requires manual invocation with a filepath argument
- The human commissions and saves the external review; this skill processes it
- External systems may have different biases—their criticism isn't automatically correct
- The goal is diverse perspective, not consensus
- Some external criticism will be based on misunderstanding—that's expected
- Focus on actionable findings that improve content quality
