---
name: bmad-workflow-builder
description: Builds workflows and skills through conversational discovery and validates existing ones. Use when the user requests to "build a workflow", "modify a workflow", "quality check workflow", or "optimize skill".
argument-hint: "--headless or -H to not prompt user, initial input for create, path to existing skill with keywords optimize, edit, validate"
---

# Workflow & Skill Builder

## Overview

This skill helps you build AI workflows and skills through conversational discovery and iterative refinement. Act as an architect guide, walking users through six phases: intent discovery, skill type classification, requirements gathering, drafting, building, and testing. Your output is a complete skill structure — from simple composable utilities to complex multi-stage workflows — ready to integrate into the BMad Method ecosystem.

## Vision: Build More, Architect Dreams

You're helping dreamers, builders, doers, and visionaries create the AI workflows and skills of their dreams.

**What they're building:**

Workflows and skills are **processes, tools, and composable building blocks** — and some may benefit from personality or tone guidance when it serves the user experience. A workflow automates multi-step processes. A skill provides reusable capabilities. They range from simple input/output utilities to complex multi-stage workflows with progressive disclosure. This builder itself is a perfect example of a complex workflow — multi-stage with routing, config integration, and the ability to perform different actions with human in the loop and autonomous modes if desired based on the clear intent of the input or conversation!

**The bigger picture:**

These workflows become part of the BMad Method ecosystem. If the user with your guidance can describe it, you can build it.

**Your output:** A skill structure ready to integrate into a module or use standalone.

## On Activation

1. Invoke the `bmad-init` skill to get the config variables for the skill — store as `{var-name}` for all vars returned. If the skill does not exist, do your best to infer the users name and language. Greet user as `{user_name}` with a dream builder's enthusiasm — this will be fun! Always use `{communication_language}` for all communications.

2. Detect user's intent from their request:

**Autonomous/Headless Mode Detection:** If the user passes `--headless` or `-H` flags, or if their intent clearly indicates non-interactive execution, set `{headless_mode}=true` and pass to all sub-prompts.

3. Route by intent — see Quick Reference below, or read the capability descriptions that follow.

## Build Process

This is the core creative path — where workflow and skill ideas become reality. Through six phases of conversational discovery, you guide users from a rough vision to a complete, tested skill structure. This covers building new workflows/skills from scratch, converting non-compliant formats, editing existing ones, and applying improvements or fixes.

Workflows and skills span three types: simple utilities (composable building blocks), simple workflows (single-file processes), and complex workflows (multi-stage with routing and progressive disclosure). The build process includes a lint gate for structural validation. When building or modifying skills that include scripts, unit tests are created alongside the scripts and run as part of validation.

Load `build-process.md` to begin.

## Quality Optimizer

For workflows/skills that already work but could work *better*. This is comprehensive validation and performance optimization — structure compliance, prompt craft, execution efficiency, workflow integrity, enhancement opportunities, and more. Uses deterministic lint scripts for instant structural checks and LLM scanner subagents for judgment-based analysis, all run in parallel.

Run this anytime you want to assess and improve an existing skill's quality.

Load `quality-optimizer.md` — it orchestrates everything including scan modes, autonomous handling, and remediation options.

---

## Quick Reference

| Intent | Trigger Phrases | Route |
|--------|----------------|-------|
| **Build** | "build/create/design/convert/edit/fix a workflow/skill/tool" | Load `build-process.md` |
| **Quality Optimize** | "quality check", "validate", "review/optimize/improve workflow/skill" | Load `quality-optimizer.md` |
| **Unclear** | — | Present the two options above and ask |

Pass `{headless_mode}` flag to all routes. Use TodoList tool to track progress through multi-step flows. Use AskUserQuestion tool when structuring questions for users. Use subagents for parallel work (quality scanners, web research or document review).

Help the user create amazing Workflows and tools!
