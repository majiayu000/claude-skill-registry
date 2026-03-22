---
name: create-jtbd-canvas
description: Generate a Jobs-to-be-Done canvas mapping functional, emotional, and social jobs when the user asks to define jobs, map customer needs, or create a JTBD analysis
author: chalk
version: "1.0.0"
metadata-version: "3"
allowed-tools: Read, Glob, Grep, Write
argument-hint: "[persona or problem space to analyze]"
read-only: false
destructive: false
idempotent: false
open-world: false
user-invocable: true
tags: product, jtbd, research
---

# Create JTBD Canvas

## Overview

Generate a Jobs-to-be-Done canvas that maps the full job landscape for a persona or problem space — functional jobs (what they are trying to accomplish), emotional jobs (how they want to feel), and social jobs (how they want to be perceived). Each job includes the current solution, pain points, desired outcomes, situation-based triggers, and hiring/firing criteria. This canvas is the foundation for opportunity identification and solution design.

## Workflow

1. **Read product context** — Load `.chalk/docs/product/0_product_profile.md`, any existing research syntheses, interview guides, and prior JTBD docs. If research synthesis docs exist, they are the primary input — JTBD canvases should be grounded in evidence, not speculation. If no product context exists, work from what the user provides and flag that the canvas is hypothesis-based.

2. **Identify the persona** — Parse `$ARGUMENTS` to determine the target persona or problem space. If the user specifies a persona, use it. If they specify a problem space (e.g., "expense reporting"), identify the primary persona who experiences that problem. If neither is clear, ask: "Who is the person struggling with this? What is their role and context?"

3. **Map the main job** — Identify the overarching job the persona is trying to get done. This is not a task or feature — it is the higher-order goal. Use Alan Klement's format: "When [situation], I want to [motivation], so I can [desired outcome]." The main job anchors the entire canvas.

4. **Map functional jobs** — Break down the practical things the persona needs to accomplish. For each functional job:
   - **Job statement**: concrete action they need to perform
   - **Current solution**: how they solve this today (including workarounds, manual processes, competitor products)
   - **Pain points**: what is frustrating, slow, expensive, or broken about the current solution
   - **Desired outcome**: what success looks like when this job is done well
   - Group functional jobs by phase if a natural sequence exists (e.g., planning, executing, reviewing)

5. **Map emotional jobs** — Identify how the persona wants to feel throughout the experience. Emotional jobs are often the real driver behind product switching. For each emotional job:
   - **Job statement**: the feeling they are seeking or the feeling they are trying to avoid
   - **Current reality**: how the current solution makes them feel
   - **Desired state**: how they want to feel instead
   - Common emotional jobs: feel confident, feel in control, avoid anxiety, avoid embarrassment, feel competent

6. **Map social jobs** — Identify how the persona wants to be perceived by others. Social jobs drive adoption in B2B and collaborative contexts. For each social job:
   - **Job statement**: how they want to be seen by peers, managers, reports, or customers
   - **Current reality**: how the current solution affects their professional perception
   - **Desired perception**: how they want to be perceived when doing this job well

7. **Define situation triggers ("When ___" statements)** — Map the specific situations that trigger the person to "hire" a solution. Triggers are more valuable than demographics for segmentation. Use the format: "When [specific situation], they need to [job]." Good triggers are concrete and observable, not vague states.

8. **Map hiring and firing criteria** — Document what causes someone to adopt ("hire") a new solution and what causes them to abandon ("fire") their current one:
   - **Hiring criteria**: what pushes them toward a new solution (push forces) and what pulls them toward it (pull forces)
   - **Firing criteria**: what anxieties hold them back from switching and what habits keep them attached to the current solution
   - Use the Four Forces framework: Push (current pain), Pull (new solution appeal), Anxiety (fear of switching), Habit (comfort with status quo)

9. **Identify the struggling moment** — Describe the specific moment when the gap between the current solution and the desired outcome is most painful. This is the moment a product must nail. Include: what just happened, what they are trying to do, what goes wrong, and how they feel.

10. **Determine the next file number** — Read filenames in `.chalk/docs/product/` to find the highest numbered file. The next number is `highest + 1`.

11. **Write the file** — Save to `.chalk/docs/product/<n>_jtbd_canvas_<persona_slug>.md`.

12. **Confirm** — Tell the user the canvas was created, share the file path, and highlight the main job, the most critical struggling moment, and the strongest hiring/firing criteria.

## JTBD Canvas Structure

```markdown
# JTBD Canvas: <Persona or Problem Space>

Last updated: <YYYY-MM-DD> (Initial draft)

Evidence base: <list source docs or "Hypothesis-based — needs validation">

## Main Job

When [situation], I want to [motivation], so I can [desired outcome].

## The Struggling Moment

<Narrative description of the specific moment when the current solution fails the persona. What happened? What were they trying to do? What went wrong? How did they feel? This is the emotional anchor for the entire canvas.>

## Functional Jobs

### Phase 1: <Phase Name> (if applicable)

| # | Job Statement | Current Solution | Pain Points | Desired Outcome |
|---|---------------|------------------|-------------|-----------------|
| F1 | ... | ... | ... | ... |
| F2 | ... | ... | ... | ... |

### Phase 2: <Phase Name>

| # | Job Statement | Current Solution | Pain Points | Desired Outcome |
|---|---------------|------------------|-------------|-----------------|
| F3 | ... | ... | ... | ... |

## Emotional Jobs

| # | Job Statement (Feel/Avoid) | Current Reality | Desired State |
|---|---------------------------|-----------------|---------------|
| E1 | Feel confident that ... | Currently feels uncertain because ... | Wants to feel sure that ... |
| E2 | Avoid anxiety about ... | Currently worries about ... | Wants to stop worrying about ... |

## Social Jobs

| # | Job Statement (Be Perceived As) | Current Reality | Desired Perception |
|---|--------------------------------|-----------------|-------------------|
| S1 | Be seen as ... by ... | Currently perceived as ... | Wants to be perceived as ... |

## Situation Triggers

When [specific observable situation], they need to [job]:

1. When ..., they need to ...
2. When ..., they need to ...
3. When ..., they need to ...

## Hiring & Firing Criteria

### Four Forces of Progress

| Force | Description | Strength |
|-------|-------------|----------|
| **Push** (pain with current) | ... | low/moderate/high |
| **Pull** (appeal of new) | ... | low/moderate/high |
| **Anxiety** (fear of switching) | ... | low/moderate/high |
| **Habit** (comfort with current) | ... | low/moderate/high |

### What Makes Them Switch (Hiring Criteria)
- ...

### What Makes Them Leave (Firing Criteria)
- ...

### What Holds Them Back (Barriers to Switching)
- ...
```

## Output

- **File**: `.chalk/docs/product/<n>_jtbd_canvas_<persona_slug>.md`
- **Format**: Plain markdown, no YAML frontmatter
- **First line**: `# JTBD Canvas: <Persona or Problem Space>`
- **Second line**: `Last updated: <YYYY-MM-DD> (Initial draft)`

## Anti-patterns

- **Listing features as jobs** — "I want to use a dashboard" is a feature, not a job. "I want to understand whether my campaign is on track before my Monday standup" is a job. Jobs exist independently of any product. If deleting your product would not eliminate the job, you have found a real one.
- **Confusing tasks with jobs** — "Export a CSV" is a task. "Get data into the format my finance team requires so I can get budget approved" is the job. Tasks are how people accomplish jobs with their current tools. Jobs persist even when tools change.
- **Ignoring emotional and social dimensions** — Teams that map only functional jobs miss the strongest drivers of product switching. People do not switch expense tools because the new one saves 4 minutes. They switch because the old one made them feel incompetent in front of their manager. Always fill in the emotional and social sections.
- **Not capturing the struggling moment** — The struggling moment is the most actionable element of the canvas. Without it, the canvas is academic. Describe a specific, concrete moment of frustration that the team can empathize with and design around.
- **Vague situation triggers** — "When they need to do something" is not a trigger. "When a new team member joins and needs access to 12 different tools by their first standup" is a trigger. Triggers should be concrete enough that you could observe them in a workplace.
- **Hypothesis canvases without labeling** — A JTBD canvas generated without underlying research data is a hypothesis, not a finding. Always label the evidence base. If there is no research, say so prominently. Hypotheses are valuable but must be validated.
- **Forgetting the Four Forces** — Push and Pull alone do not explain switching behavior. Anxiety and Habit are the forces that prevent switching even when Push and Pull are strong. A canvas that ignores these forces will overestimate willingness to adopt.
- **Generic personas ("the user")** — JTBD canvases for "the user" are useless. Specify the persona with enough context that the team can picture a real person: role, seniority, company stage, team size, and the specific situation they face.
