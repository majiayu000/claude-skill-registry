---
name: validate-skill-coverage
description: Audit which product development lifecycle phases have skills and which have gaps when the user asks to check skill coverage, audit skills, or find lifecycle gaps
author: chalk
version: "1.0.0"
metadata-version: "3"
allowed-tools: Read, Glob, Grep
argument-hint: "[optional: specific phase or lifecycle to check]"
read-only: true
destructive: false
idempotent: true
open-world: false
user-invocable: true
tags: validation, skills, coverage
---

# Validate Skill Coverage

## Overview

Meta-skill that audits the skills index against product development lifecycle phases. Identifies which phases are well-covered, which have gaps, and how skills are distributed across the lifecycle. Outputs a coverage report directly in the conversation.

## Workflow

1. **Read the skills index** — Read `skills/skills-index.yaml` to get the full list of registered skills with their categories, tiers, and descriptions.

2. **Read individual skill files** — For each skill in the index, read its `SKILL.md` to understand what lifecycle phase(s) it covers. Note the skill's tier (Tier 1 = daily driver, Tier 2 = important, Tier 3 = reference/stack-specific).

3. **Define lifecycle phases** — Map skills against these standard product development phases:
   - **Discovery**: User research, JTBD analysis, feedback synthesis
   - **Definition**: PRD writing, user stories, requirements
   - **Design**: API design, data modeling, experiment design
   - **Planning**: Estimation, backlog scoring, sprint planning
   - **Implementation**: Coding patterns, code review, commit messages
   - **Testing**: Test plans, test coverage validation, testing patterns
   - **Release**: Release checklists, release notes, rollback plans
   - **Operations**: Incident reports, debugging, security audits
   - **Evaluation**: Metrics analysis, decision logging, research synthesis
   - **Governance**: ADRs, RFCs, tech debt management

4. **Generate the coverage matrix** — For each phase, list: (a) skills that cover it, (b) the tier of each skill, (c) whether the coverage is complete or partial.

5. **Identify gaps** — Flag phases with no skills or only Tier 3 (reference) coverage. Prioritize gaps by impact: phases that every team needs (implementation, testing) are higher priority than niche phases.

6. **Assess distribution** — Check for imbalances: too many skills in one phase (redundancy), missing Tier 1 skills for critical phases, or Tier 3 skills without corresponding Tier 1/2 foundations.

7. **Report in conversation** — Present the coverage matrix, gap analysis, and recommendations directly in the conversation. Do not write a file.

## Output

- **Format**: Coverage report delivered in the conversation (no file written)
- **Key sections**: Coverage Matrix (phase x skill table), Gap Analysis (uncovered phases ranked by priority), Distribution Assessment (tier balance), Recommendations (suggested new skills to fill gaps)

## Anti-patterns

- **Treating all gaps equally** — A missing "sprint planning" skill is lower priority than a missing "security audit" skill. Prioritize gaps by risk and frequency of need.
- **Ignoring tier balance** — A phase covered only by Tier 3 reference skills lacks the opinionated guidance that Tier 1/2 skills provide. Flag this as partial coverage, not full coverage.
- **Static analysis only** — Coverage on paper does not mean coverage in practice. Note if skills exist but are likely underused (e.g., too complex, too niche).
- **Recommending skills for every gap** — Not every gap needs a skill. Some phases are better served by external tools, team processes, or existing documentation. Recommend skills only where agent assistance adds clear value.
