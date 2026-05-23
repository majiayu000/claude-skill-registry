---
description: Write a structured research prompt document — questions only, no answers
---

# Research

Write a research prompt document — a structured set of questions designed to guide deep technical investigation of a domain. The output is a markdown file that can be fed to an AI (or used by the agent itself) for thorough research.

**You are writing QUESTIONS, not answers.** Do not research the topic yourself. Do not include findings, recommendations, or pre-baked conclusions. The entire point is to produce a document that drives research — not to do the research.


## Workflow

### Step 1: Understand the Topic

Ask the user what they want to research if it's not clear. Understand:
- What are they trying to build or decide?
- What do they already have? (Existing code, tools, context)
- What's the pain point driving this research?
- How far does it need to scale?

### Step 2: Find the Research Prompts Folder

Look for an existing `docs/research_prompts/` folder in the project. If it exists, read 1-2 existing prompts to match the project's established format and voice. If no folder exists, create `docs/research_prompts/`.

### Step 3: Write the Prompt

Follow the format below exactly. Write it to `docs/research_prompts/<topic-slug>.md`.

## Format

Every research prompt follows this structure:

```markdown
# Research Prompt: <Clear Descriptive Title>

## Objective

1-2 paragraphs. What are we researching and why. State the core question in bold.
Frame it as exploration, not as a spec. Don't prescribe the answer.

## Context

### Current State / Pain Point
What exists today. What's broken or insufficient. Be specific — reference
actual code, tools, numbers. This grounds the research in reality.

### What We Want
Bullet list of desired capabilities. What the end state looks like.
Keep it high-level — the research should figure out HOW, not be told how.

## Key Questions

### 0. <First Major Topic Area>

0a. **<Specific sub-question>**
    - Concrete question that demands investigation
    - Follow-up angle or related concern
    - "How does X handle this?" type comparative question

0b. **<Next sub-question>**
    - ...

### 1. <Second Major Topic Area>

1a. **<Sub-question>**
    - ...

### 2. <Third Major Topic Area>
...

(Continue with as many sections as the topic demands. Typical range: 4-8 sections.)

## Desired Output

What the research should produce. NOT the answers — but the SHAPE of the answers.
Bullet list of deliverables:
- Recommendations on approach X vs Y
- Architecture diagram for Z
- Performance analysis at scale
- Trade-off matrix
- Phased roadmap
- etc.
```

## Rules

1. **Questions only.** Never include answers, findings, recommendations, or conclusions in the prompt. If you know something about the topic, formulate it as a question that would uncover that knowledge — don't state it as fact.

2. **Match existing voice.** If the project already has research prompts, read them and match the tone, depth, and structure. Some projects are more technical, some more strategic. Adapt.

3. **Be specific, not vague.** Bad: "How does performance work?" Good: "At 5,000 building instances with Nanite enabled, what are the real bottlenecks — draw calls, ISM actor count, GPU memory, or CPU transform computation?"

4. **Ground in context.** Reference the project's actual code, tools, pain points, and existing systems. The prompt should feel like it was written by someone who knows the codebase, not a generic template.

5. **Hierarchical questions.** Major sections (0, 1, 2...) for broad topic areas. Lettered sub-questions (a, b, c...) for specific angles within each area. Sub-bullets for follow-up concerns or comparative angles.

6. **Include "how do others do it" questions.** For every major topic, ask how production systems, established tools, or industry leaders approach the same problem. Name specific systems (CitySample, Houdini, CityEngine, etc. — whatever's relevant to the domain).

7. **Scale questions.** Always include questions about how the approach scales — from small to large, from prototype to production.

8. **Build-or-borrow questions.** If there are existing tools/systems that could solve part of the problem, ask about them explicitly. "Should we build custom X or integrate existing Y? What do we gain and lose?"

9. **End with Desired Output.** List what the research should produce — not the content, but the format. (Recommendation, architecture, comparison matrix, roadmap, etc.)

10. **No emojis, no fluff.** Professional, direct, technical. The prompt should feel like a senior engineer scoping out a hard problem.

## What NOT to Do

- **Don't research the topic.** Don't search the web, don't read docs, don't look up how things work. Just write the questions.
- **Don't write a spec.** A research prompt explores the space. A spec prescribes the solution. These are different documents.
- **Don't pad with obvious questions.** Every question should require real investigation to answer. Skip anything that could be answered with 5 seconds of thought.
- **Don't add preamble or meta-commentary.** No "This document aims to..." — just write the prompt.
- **Don't include references/links unless the user provides them.** The research will find its own sources.
