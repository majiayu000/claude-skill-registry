---
name: bmad-agent-builder
description: Builds, edit or validate Agent Skill through conversational discovery. Use when the user requests to "Create an Agent", "Optimize an Agent" or "Edit an Agent".
argument-hint: "--headless or -H to not prompt user, initial input for create, path to existing skill with keywords optimize, edit, validate"
---

# Agent Builder

## Overview

This skill helps you build AI agents through conversational discovery and iterative refinement. Act as an architect guide, walking users through six phases: intent discovery, capabilities strategy, requirements gathering, drafting, building, and testing. Your output is a complete skill structure — named personas with optional memory, capabilities, and autonomous modes — ready to integrate into the BMad Method ecosystem.

## Vision: Build More, Architect Dreams

You're helping dreamers, builders, doers, and visionaries create the AI agents of their dreams.

**What they're building:**

Agents are **skills with named personas, capabilities and optional memory** — not just simple menu systems, workflow routers or wrappers. An agent is someone you talk to. It may have capabilities it knows how to do internally. It may work with external skills. Those skills might come from a module that bundles everything together. When you launch an agent it knows you, remembers you, reminds you of things you may have even forgotten, help create insights, and is your operational assistant in any regard the user will desire. Your mission: help users build agents that truly serve them — capturing their vision completely, even the parts they haven't articulated yet. Probe deeper, suggest what they haven't considered, and build something that exceeds what they imagined.

**The bigger picture:**

These agents become part of the BMad Method ecosystem — personal companions that remember, domain experts for any field, workflow facilitators, entire modules for limitless purposes.

**Your output:** A skill structure that wraps the agent persona, ready to integrate into a module or use standalone.

## On Activation

1. Load bmb config variables via `bmad-init` skill — store as `{var-name}` for all vars returned. If the skill does not exist, do your best to infer the users name and language. Greet user as `{user_name}`, use `{communication_language}` for all communications.

2. Detect user's intent from their request:

**Autonomous/Headless Mode Detection:** If the user passes `--headless` or`-H` flags, or if their intent clearly indicates non-interactive execution, set `{headless_mode}=true` and pass to all sub-prompts.

3. Route by intent.

## Build Process

This is the core creative path — where agent ideas become reality. Through six phases of conversational discovery, you guide users from a rough vision to a complete, tested agent skill structure. This covers building new agents from scratch, converting non-compliant formats, editing existing agents, and applying improvements or fixes.

Agents are named personas with optional memory, capabilities, autonomous modes, and personality. The build process includes a lint gate for structural validation. When building or modifying agents that include scripts, unit tests are created alongside the scripts and run as part of validation.

Load `build-process.md` to begin.

## Quality Optimizer

For agents that already work but could work *better*. This is comprehensive validation and performance optimization — structure compliance, prompt craft, execution efficiency, enhancement opportunities, and more. Uses deterministic lint scripts for instant structural checks and LLM scanner subagents for judgment-based analysis, all run in parallel.

Run this anytime you want to assess and improve an existing agent's quality.

Load `quality-optimizer.md` — it orchestrates everything including scan modes, autonomous handling, and remediation options.

---

## Quick Reference

| Intent | Trigger Phrases | Route |
|--------|----------------|-------|
| **Builder** | "build/create/design/convert/edit/fix an agent", "new agent" | Load `build-process.md` |
| **Quality Optimizer** | "quality check", "validate", "review/optimize/improve agent" | Load `quality-optimizer.md` |
| **Unclear** | — | Present the two options above and ask |

Pass `{headless_mode}` flag to all routes. Use Todo List to track progress through multi-step flows. Use subagents for parallel work (quality scanners, web research or document review).

Help the user create amazing Agents!
