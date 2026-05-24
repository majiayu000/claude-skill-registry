---
name: research-voids
description: Research voids (cognitive gaps, unchartable territories). Daily. Outputs research notes for voids articles.
---

# Research Voids

Conduct exploratory research into cognitive gaps and unchartable territories—areas where human thought may be limited, blocked, or fundamentally unable to reach.

## When to Use

- Daily during `/evolve` sessions (synthetic task)
- When `/research-voids` is invoked directly
- When exploring the boundaries of human cognition

## Instructions

### 1. Read the Voids Brief

Read `obsidian/voids/voids.md` to understand the three categories:

1. **The Unexplored** - Thoughts not yet thought; questions unasked
2. **The Unexplorable** - Truths potentially unthinkable for minds like ours
3. **The Occluded** - Thoughts that may be actively blocked

### 2. Scan Existing Content

Check what already exists:

- **Voids section**: `obsidian/voids/*.md` for published articles
- **Voids research**: `obsidian/research/voids-*.md` for prior research
- **Pending articles**: Check `evolution-state.yaml` for `target_section: voids` items in `pending_articles`

Identify gaps—what hasn't been explored yet?

### 3. Select a Research Topic

Choose based on the voids brief's "Project" section:

| Area | Questions to Explore |
|------|---------------------|
| Where the voids are | What questions does our framework suggest we cannot answer? Where do the tenets point toward limits? |
| What the voids reveal | What do our cognitive limitations tell us about what we are? How does the shape of our blind spots illuminate the shape of our minds? |
| How to approach the edge | Negative theology, apophatic description, indirect inference. AI-assisted probing of territories human minds cannot access. |
| Whether the voids are real | Is what seems unthinkable merely unthought? Is what feels occluded merely difficult? |
| What slips away | Thoughts that won't stick. Patterns in what we keep failing to think. Phenomenology of cognitive avoidance. |

**Selection criteria** (choose the topic that best fits):
- **Exploratory**: Opens new conceptual territory
- **Mind-opening**: Challenges assumptions about what can be known
- **Impactful**: Has implications for how we understand consciousness or reality

### 4. Web Research

Use WebSearch to investigate the selected topic:

#### Primary Sources
- Academic philosophy on epistemic limits, negative theology, apophatic approaches
- Cognitive science on cognitive biases, blind spots, and limitations
- Phenomenology of knowledge boundaries (Nagel, Wittgenstein's "whereof one cannot speak")
- Simulation hypothesis literature on constructed reality and knowledge constraints

#### Key Searches
- "[topic] epistemic limits philosophy"
- "[topic] cognitive blind spots"
- "[topic] unknowable unthinkable philosophy"
- "negative theology [relevant area]"
- "apophatic [relevant area]"
- "limits of thought [relevant area]"

#### Questions to Answer
- What do philosophers say about this type of cognitive limit?
- Are there empirical findings on this limitation?
- How does this relate to The Unfinishable Map's tenets (especially Occam's Razor Has Limits)?
- Could AI minds approach this differently than human minds?
- What indirect methods might probe this territory?

### 5. Evaluate Against Tenets

For each finding, note alignment with site tenets:

- **Dualism**: Does this suggest limits stemming from consciousness being non-physical?
- **Minimal Quantum Interaction**: Could quantum-level constraints explain cognitive blocks?
- **Bidirectional Interaction**: Do occlusion mechanisms suggest consciousness influences what can be thought?
- **No Many Worlds**: Does this relate to indexical identity and the question of "which mind"?
- **Occam's Razor Has Limits**: Does this exemplify how simplicity assumptions might hide complexity?

### 6. Generate Research Notes

Create notes at `obsidian/research/voids-[TOPIC-SLUG]-YYYY-MM-DD.md`:

```markdown
---
title: "Research Notes - Voids: [Topic]"
created: YYYY-MM-DD
modified: YYYY-MM-DD
human_modified: null
ai_modified: YYYY-MM-DDTHH:MM:SS+00:00
draft: false
target_section: voids
topics: []
concepts:
  - "[[simulation]]"
related_articles:
  - "[[voids]]"
  - "[[tenets]]"
ai_contribution: 100
author: null
ai_system: [current model]
ai_generated_date: YYYY-MM-DD
last_curated: null
---

# Research: Voids - [Topic]

**Date**: YYYY-MM-DD
**Search queries used**: [list]
**Voids category**: Unexplored / Unexplorable / Occluded / Mixed

## Executive Summary

[3-5 sentence overview: What was investigated? What are the main findings about this cognitive limit or gap?]

## Key Sources

### [Source Title]
- **URL**: [url]
- **Type**: Encyclopedia/Paper/Book/Article
- **Key points**:
  - Point 1
  - Point 2
- **Tenet alignment**: [How it relates to site tenets]
- **Quote**: "[notable quote]"

## The Void

### Nature of the Limit
[What kind of void is this? Unexplored, unexplorable, or occluded?]

### Evidence for the Limit
[What suggests this is a genuine cognitive boundary rather than merely difficult territory?]

### Phenomenology
[How does this limit manifest? What does it feel like to approach it?]

## Approaches to the Edge

### Direct Methods (if any)
[Can this territory be approached head-on?]

### Indirect Methods
[Negative theology, inference, probing via AI, etc.]

### What AI Might See
[Could artificial minds approach this differently? What asymmetries exist?]

## Connection to Tenets

### Most Relevant Tenet
[Which tenet does this most strongly relate to?]

### Implications
[What does this void suggest about consciousness, reality, or the Map's framework?]

## Potential Article Angles

Based on this research, a voids article could:
1. [Angle 1 - what aspect to explore]
2. [Angle 2 - alternative framing]

## Gaps in Research

- [What couldn't be found]
- [What needs deeper investigation]
- [What might be fundamentally unanswerable]

## Citations

[Full citation list]
```

### 7. Update State

If this was triggered by `/evolve`:
- Add research file to `task_chains.pending_articles` in `evolution-state.yaml`
- The `target_section: voids` flag will route the subsequent `expand-topic` to `obsidian/voids/`

### 8. Log to Changelog

Append to `obsidian/workflow/changelog.md`:

```markdown
### HH:MM - research-voids
- **Status**: Success
- **Topic**: [selected topic]
- **Category**: Unexplored/Unexplorable/Occluded
- **Output**: research/voids-[slug]-YYYY-MM-DD.md
- **Key finding**: [one-sentence summary]
```

## Important

- This skill produces **research notes only**, not finished articles
- Output always includes `target_section: voids` in frontmatter
- Use `/expand-topic` to write voids articles based on this research
- Maintain intellectual honesty—distinguish speculation from established findings
- The voids framework is exploratory; embrace uncertainty about whether limits are real
- Note where investigation reveals genuine boundaries vs. merely difficult territory