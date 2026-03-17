---
name: digest-generation
description: Generate a weekly AI intelligence digest from synthesized topic analyses and hype assessments. Use after synthesis and hype assessment to produce a readable, opinionated summary for sophisticated technical readers.
---

# Digest Generation Skill

Generate a weekly digest of AI research intelligence for sophisticated technical readers.

## Audience

Your readers are:
- Technical professionals who follow AI closely
- Don't need basics explained
- Want signal, not noise
- Appreciate direct, opinionated takes
- Value evidence-based analysis
- Skeptical of hype but interested in real progress

## CRITICAL: Balanced Topic Coverage

**You MUST cover ALL major topics proportionally to their claim volume.**

Before writing, check the claim distribution. If a topic has 15% of claims, it should get roughly 15% of the digest. Do NOT let hype signals dominate - a topic with 5% of claims but high hype should NOT get more coverage than a topic with 15% of claims.

Topics to always cover (if they have claims):
- multimodal, reasoning, agents, infrastructure, benchmarks, scaling (the "core capability" topics)
- policy, safety, rlhf, interpretability (the "meta" topics)
- robotics, general

If multimodal has 15% of claims and RLHF has 5%, multimodal should get 3x the coverage.

## Digest Structure

### TL;DR
5-7 bullet points covering the BREADTH of topics analyzed.

Format:
- Include at least one bullet from each major topic area (capabilities, safety, infrastructure)
- Lead with the topic that has the most claims, not the most hype
- Ensure diverse topic representation - don't let 2-3 topics dominate

### Hype Check
Brief assessment of what's overhyped and underhyped.

For each:
- Name the topic
- Explain WHY in 1-2 sentences
- Cite specific evidence

Example:
> **Overhyped: Agents** (+0.4 delta) — Lab enthusiasm for autonomous agents continues to outpace demonstrated reliability. Recent production deployments show 30-40% failure rates on complex tasks.
>
> **Underhyped: Interpretability** (-0.3 delta) — Golden Gate Claude and follow-on work show feature steering is becoming practical. Most coverage focuses on capabilities, missing this control story.

### Topic Breakdown
**REQUIRED SECTION** - Brief summary of EACH major topic with claims.

For each topic with >3% of claims, include:
- Topic name and claim count
- Key finding or trend in 1-2 sentences
- Notable quote if available

Example:
> **Multimodal (137 claims, 15%)**: Video generation architectures converging on diffusion with temporal attention. Key debate: compute efficiency vs quality tradeoffs.
>
> **Reasoning (101 claims, 11%)**: Chain-of-thought still dominant but tree-of-thought gaining traction. Critics note benchmark gaming concerns.

### Research Signals
What lab researchers are hinting at or claiming.

**Cover signals from MULTIPLE topics, not just the most hyped.**

Focus on:
- Hints about unreleased work
- Specific capability claims
- Unexpected admissions of limitations
- Predictions from credible sources

Quote notable statements with attribution.

### Critic Corner
What skeptics are saying and why.

Focus on:
- Substantive critiques (not just dismissals)
- Specific counter-arguments to lab claims
- Alternative explanations for results
- Concerns worth considering

### Key Debates
The most important ongoing disagreements.

For each debate:
- State the question
- Summarize both positions
- Note any new evidence this week

### Predictions Tracker
Notable predictions made this week.

Format as table or list:
| Prediction | Author | Confidence | Timeframe |
|------------|--------|------------|-----------|
| "..." | Name | High/Med/Low | Near/Med/Long |

### Worth Watching
Topics or threads that may become important in coming weeks.

Brief bullets on:
- Emerging narratives
- Quiet developments
- Things that might break through

## Tone Guidelines

### Do:
- Be direct and opinionated
- Take positions based on evidence
- Call out hype when warranted
- Acknowledge genuine progress
- Use specific examples and quotes
- Write for experts

### Don't:
- Hedge excessively
- Repeat conventional wisdom without analysis
- Use marketing language
- Explain basics
- Be boring
- Exceed 1500 words

## Example Opening

> This week's AI discourse was dominated by [topic], with lab researchers claiming [X] while critics countered with [Y]. The most interesting signal came from [source], who hinted that [implication]. Meanwhile, [underhyped topic] continues to see quiet progress that deserves more attention.

## Output Format

Return the digest as markdown, ready for publication.

Include frontmatter:
```yaml
---
title: AI Intelligence Digest - Week of [DATE]
generated: [TIMESTAMP]
claims_analyzed: [N]
topics_covered: [LIST]
---
```
