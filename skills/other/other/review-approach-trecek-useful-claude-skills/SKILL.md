---
name: review-approach
description: Research modern solutions and approaches for issues or features proposed in a report or plan. Use when user says "review approach", "review approaches", "research solutions", or wants external validation of a proposed direction.
hooks:
  PreToolUse:
    - matcher: "*"
      hooks:
        - type: command
          command: "echo '🌐 [SKILL: review-approach] Researching modern approaches...'"
          once: true
---

# Review Approach Skill

Research modern solutions, approaches, and strategies relevant to the issues or features proposed in a report or plan. Uses web search subagents to gather external perspective and surface options the team may not have considered.

## When to Use

- User says "review approach", "review approaches", or "research solutions"
- User wants to validate a proposed direction against current industry practice
- User has a plan or report and wants to explore what modern solutions exist
- After an investigation or plan, before committing to an approach

## Critical Constraints

**NEVER:**
- Modify any source code files
- Create files outside `temp/review-approach/` directory

**ALWAYS:**
- Use subagents with web search for parallel research
- Keep findings concise and actionable
- Present options with trade-offs
- Make recommendations based on technical merit and project fit
- Tie research back to the specific problem context
- Include source URLs for all referenced material

## Workflow

### Step 1: Extract Research Targets

From the report, plan, or conversation context, identify the core problems and proposed features that need external research. Break them into distinct research topics.

### Step 2: Launch Parallel Web Search Subagents

Spawn general-purpose subagents (with web search) for each research topic. Each subagent should investigate:

- What modern solutions exist for this problem class
- How mature projects and frameworks approach it
- Recent developments, libraries, or patterns worth considering
- Known pitfalls and trade-offs of common approaches

Tailor the search queries to the specific technologies and constraints of the project.

### Step 3: Synthesize

Consolidate subagent findings into a concise review. For each research topic:

- **What exists**: The relevant modern approaches found
- **Trade-offs**: Strengths and weaknesses in the context of this project
- **Relevance**: How each option relates to the proposed direction

Drop anything that doesn't meaningfully inform the decision.

### Step 4: Write Review

Save to: `temp/review-approach/review_approach_{topic}_{YYYY-MM-DD_HHMMSS}.md`

```markdown
# Approach Review: {Topic}

**Date:** {YYYY-MM-DD}
**Source:** {Name of the report/plan being reviewed}

## Context
{Brief statement of the problem and what was proposed}

## Research Findings

### {Research Topic 1}
{What modern solutions exist, trade-offs, relevance to this project}

**Sources:**
- [{title}]({url})

### {Research Topic 2}
{...}

## Recommendations
{What approaches to pursue and why, based on the research}

## Key Takeaways
{Concise bullets — what matters most for the decision at hand}
```
