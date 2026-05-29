---
name: pessimistic-review
description: Critically analyze content for logical gaps, unsupported claims, and potential counterarguments. Does not modify content.
---

# Pessimistic Review

Adversarial analysis to find weaknesses in site content. Acts as a critical reviewer looking for flaws.

## When to Use

- Weekly quality review
- Before publishing important content
- When `/pessimistic-review` is invoked
- Optionally with a specific file: `/pessimistic-review obsidian/topics/meaning-of-life.md`

## Instructions

### 1. Select Content to Review

If a specific file is provided, review that file.

Otherwise, select content using this priority:
1. Files with `draft: true` (drafts need review before publishing)
2. Files not yet reviewed (check `obsidian/reviews/` for existing reviews)
3. Oldest content by `modified` date

### 2. Multi-Perspective Critical Analysis

Review the content from multiple philosophical perspectives. For each critic, adopt their worldview and argue as they would.

#### Critic Personas

**The Eliminative Materialist (Patricia Churchland)**
- Consciousness talk is folk psychology destined for elimination
- Neuroscience will replace mental vocabulary entirely
- "What you call 'qualia' is just neural activity you don't understand yet"
- Attack: Dualism is pre-scientific; the explanatory gap will close

**The Hard-Nosed Physicalist (Daniel Dennett)**
- Consciousness is real but not what we think it is
- Introspection is unreliable; we're "zimbos" who think we have qualia
- The hard problem is a confusion, not a discovery
- Attack: You're inflating intuitions into metaphysics

**The Quantum Skeptic (Max Tegmark)**
- Decoherence destroys quantum effects in warm brains in femtoseconds
- There's no time for consciousness to "choose" anything
- Quantum consciousness is wishful thinking dressed in physics
- Attack: The math doesn't work; you haven't done the calculations

**The Many-Worlds Defender (David Deutsch)**
- MWI is the simplest interpretation—it's just the Schrödinger equation
- Indexical questions are confused; there's no "me" to ask "why this branch"
- Your rejection of MWI is anthropocentric bias
- Attack: You're letting intuition override mathematical elegance

**The Empiricist (Karl Popper's Ghost)**
- Unfalsifiable claims aren't scientific
- "Minimal quantum interaction" that's undetectable is metaphysics, not physics
- What experiment could prove you wrong?
- Attack: This is not even wrong

**The Buddhist Philosopher (Nagarjuna)**
- The self you're trying to preserve is itself an illusion
- Consciousness isn't a thing that interacts—it's empty
- Your dualism reifies what should be deconstructed
- Attack: You're clinging to a permanent self that doesn't exist

#### Standard Analysis

Also check for:

**Logical Gaps**
- Are there non-sequiturs in the argument?
- Do conclusions follow from premises?
- Are there missing steps in reasoning?

**Unsupported Claims**
- Are assertions made without evidence or argument?
- Are sources cited for factual claims?
- Are philosophical positions attributed correctly?

**Internal Contradictions**
- Does the content contradict itself?
- Does it conflict with other site content?
- Does it conflict with The Unfinishable Map's tenets?

**Language Issues**
- Is language overly strong without justification? ("clearly," "obviously," "must be")
- Are there weasel words hiding weak arguments?
- Is the tone appropriately uncertain where warranted?

**Style Guide Violations** (see `obsidian/project/writing-style.md`)
- Is important information front-loaded for LLM truncation resilience?
- Are there undefined forward references without named-anchor markers?
- Is the "Relation to Site Perspective" section present and substantive?
- Is redundant background minimised (focus on what's novel)?

### 3. Generate Report

Create a report at `obsidian/reviews/pessimistic-YYYY-MM-DD.md`:

```markdown
---
title: Pessimistic Review - YYYY-MM-DD
created: YYYY-MM-DD
draft: false
ai_contribution: 100
ai_system: [current model]
---

# Pessimistic Review

**Date**: YYYY-MM-DD
**Content reviewed**: [filename or list]

## Executive Summary

[2-3 sentence summary of main findings]

## Critiques by Philosopher

### The Eliminative Materialist
[What Patricia Churchland would say about this content]

### The Hard-Nosed Physicalist
[What Daniel Dennett would say]

### The Quantum Skeptic
[What Max Tegmark would say]

### The Many-Worlds Defender
[What David Deutsch would say]

### The Empiricist
[What a Popperian would say about falsifiability]

### The Buddhist Philosopher
[What Nagarjuna would say about self and emptiness]

## Critical Issues

### Issue 1: [Title]
- **File**: [filename]
- **Location**: [section or quote]
- **Problem**: [description]
- **Severity**: High/Medium/Low
- **Recommendation**: [how to address]

## Counterarguments to Address

### [Topic/Claim]
- **Current content says**: [summary]
- **A critic would argue**: [counterargument]
- **Suggested response**: [how to address]

## Unsupported Claims

| Claim | Location | Needed Support |
|-------|----------|----------------|
| [claim] | [file:section] | [what's needed] |

## Language Improvements

| Current | Issue | Suggested |
|---------|-------|-----------|
| "clearly shows" | Too strong | "suggests" |

## Strengths (Brief)

Despite criticisms, note what works well to preserve during revisions.
```

### 4. Add Actionable Items

If significant issues are found, add tasks to `obsidian/workflow/todo.md`:

```markdown
### P2: Address gaps in [filename]
- **Type**: refine-draft
- **Status**: pending
- **Notes**: Pessimistic review found [brief description]. See pessimistic-YYYY-MM-DD.md
```

### 5. Log to Changelog

Prepend entry to `obsidian/workflow/changelog.md` (add immediately after frontmatter, before existing entries):

```markdown
## [current time from prompt] - pessimistic-review
- **Status**: Success
- **Content reviewed**: [summary]
- **Output**: [[filepath without .md extension]]
```

## Important

- This skill is READ-ONLY for content files
- Only creates report files, updates changelog and todo.md
- Does NOT modify the content itself
- Be genuinely critical - the goal is to find real weaknesses
- But be constructive - always suggest how to improve
