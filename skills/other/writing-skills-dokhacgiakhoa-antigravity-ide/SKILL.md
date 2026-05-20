---
version: 4.1.0-fractal
name: writing-skills
description: Use when creating new skills, editing existing skills, or verifying skills work before deployment
---

# Writing Skills

## Overview

**Writing skills IS Test-Driven Development applied to process documentation.**

**Personal skills live in agent-specific directories (`~/.claude/skills` for Claude Code, `~/.codex/skills` for Codex)**

You write test cases (pressure scenarios with subagents), watch them fail (baseline behavior), write the skill (documentation), watch tests pass (agents comply), and refactor (close loopholes).

**Core principle:** If you didn't watch an agent fail without the skill, you don't know if the skill teaches the right thing.

**REQUIRED BACKGROUND:** You MUST understand superpowers:test-driven-development before using this skill. That skill defines the fundamental RED-GREEN-REFACTOR cycle. This skill adapts TDD to documentation.

**Official guidance:** For Anthropic's official skill authoring best practices, see anthropic-best-practices.md. This document provides additional patterns and guidelines that complement the TDD-focused approach in this skill.

## What is a Skill?

A **skill** is a reference guide for proven techniques, patterns, or tools. Skills help future Claude instances find and apply effective approaches.

**Skills are:** Reusable techniques, patterns, tools, reference guides

**Skills are NOT:** Narratives about how you solved a problem once

## TDD Mapping for Skills

| TDD Concept             | Skill Creation                                   |
| ----------------------- | ------------------------------------------------ |
| **Test case**           | Pressure scenario with subagent                  |
| **Production code**     | Skill document (SKILL.md)                        |
| **Test fails (RED)**    | Agent violates rule without skill (baseline)     |
| **Test passes (GREEN)** | Agent complies with skill present                |
| **Refactor**            | Close loopholes while maintaining compliance     |
| **Write test first**    | Run baseline scenario BEFORE writing skill       |
| **Watch it fail**       | Document exact rationalizations agent uses       |
| **Minimal code**        | Write skill addressing those specific violations |
| **Watch it pass**       | Verify agent now complies                        |
| **Refactor cycle**      | Find new rationalizations → plug → re-verify     |

The entire skill creation process follows RED-GREEN-REFACTOR.

## When to Create a Skill

**Create when:**

- Technique wasn't intuitively obvious to you
- You'd reference this again across projects
- Pattern applies broadly (not project-specific)
- Others would benefit

**Don't create for:**

- One-off solutions
- Standard practices well-documented elsewhere
- Project-specific conventions (put in CLAUDE.md)
- Mechanical constraints (if it's enforceable with regex/validation, automate it—save documentation for judgment calls)

## Skill Types

## 🧠 Knowledge Modules (Fractal Skills)

### 1. [Technique](./sub-skills/technique.md)
### 2. [Pattern](./sub-skills/pattern.md)
### 3. [Reference](./sub-skills/reference.md)
### 4. [1. Rich Description Field](./sub-skills/1-rich-description-field.md)
### 5. [2. Keyword Coverage](./sub-skills/2-keyword-coverage.md)
### 6. [3. Descriptive Naming](./sub-skills/3-descriptive-naming.md)
### 7. [4. Token Efficiency (Critical)](./sub-skills/4-token-efficiency-critical.md)
### 8. [4. Cross-Referencing Other Skills](./sub-skills/4-cross-referencing-other-skills.md)
### 9. [Self-Contained Skill](./sub-skills/self-contained-skill.md)
### 10. [Skill with Reusable Tool](./sub-skills/skill-with-reusable-tool.md)
### 11. [Skill with Heavy Reference](./sub-skills/skill-with-heavy-reference.md)
### 12. [Discipline-Enforcing Skills (rules/requirements)](./sub-skills/discipline-enforcing-skills-rulesrequirements.md)
### 13. [Technique Skills (how-to guides)](./sub-skills/technique-skills-how-to-guides.md)
### 14. [Pattern Skills (mental models)](./sub-skills/pattern-skills-mental-models.md)
### 15. [Reference Skills (documentation/APIs)](./sub-skills/reference-skills-documentationapis.md)
### 16. [Close Every Loophole Explicitly](./sub-skills/close-every-loophole-explicitly.md)
### 17. [Address "Spirit vs Letter" Arguments](./sub-skills/address-spirit-vs-letter-arguments.md)
### 18. [Build Rationalization Table](./sub-skills/build-rationalization-table.md)
### 19. [Create Red Flags List](./sub-skills/create-red-flags-list.md)
### 20. [Update CSO for Violation Symptoms](./sub-skills/update-cso-for-violation-symptoms.md)
### 21. [RED: Write Failing Test (Baseline)](./sub-skills/red-write-failing-test-baseline.md)
### 22. [GREEN: Write Minimal Skill](./sub-skills/green-write-minimal-skill.md)
### 23. [REFACTOR: Close Loopholes](./sub-skills/refactor-close-loopholes.md)
### 24. [❌ Narrative Example](./sub-skills/narrative-example.md)
### 25. [❌ Multi-Language Dilution](./sub-skills/multi-language-dilution.md)
### 26. [❌ Code in Flowcharts](./sub-skills/code-in-flowcharts.md)
### 27. [❌ Generic Labels](./sub-skills/generic-labels.md)
