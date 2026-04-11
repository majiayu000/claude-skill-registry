---
name: latent-space-engineering
description: 'Shape agent behavior through instruction framing, emotional priming, and style transfer rather than information density alone.'
version: 1.7.1
alwaysApply: false
category: methodology
tags:
  - prompt-engineering
  - agent-behavior
  - instruction-framing
  - style-transfer
  - review-optimization
progressive_loading: true
dependencies:
  hub: []
  modules:
    - modules/emotional-framing.md
    - modules/style-gene-transfer.md
    - modules/competitive-review.md
complexity: basic
model_hint: fast
estimated_tokens: 300
---
# Latent Space Engineering

Shape agent behavior by framing instructions for
optimal performance. Distinct from context engineering
(packing the right information), this skill addresses
HOW instructions are framed to put agents in productive
mental states.

## When To Use

- Composing agent dispatch prompts
- Writing skill instructions that guide behavior
- Dispatching 3+ parallel review agents
- Generating code or documentation that must match
  an existing style

## When NOT To Use

- Packing factual context (use context-optimization)
- Simple single-shot tasks with no behavioral nuance
- Tasks where instruction tone is irrelevant

## Core Techniques

### 1. Emotional Framing

Replace threat-based prompting with calm, confident
instructions. Fear-based prompts cause rushing and
corner-cutting.

**Load module**: `modules/emotional-framing.md`

### 2. Style Gene Transfer

Inject exemplar code or prose into context before
requesting output. Agents reproduce stylistic
attributes from pre-loaded samples.

**Load module**: `modules/style-gene-transfer.md`

### 3. Competitive Review

Frame multi-agent review dispatch with competitive
incentives to increase rigor and thoroughness.

**Load module**: `modules/competitive-review.md`

## Quick Reference

| Technique | When | Module |
|-----------|------|--------|
| Emotional framing | Any agent prompt | emotional-framing |
| Style gene transfer | Code/doc generation | style-gene-transfer |
| Competitive review | 3+ parallel reviewers | competitive-review |
