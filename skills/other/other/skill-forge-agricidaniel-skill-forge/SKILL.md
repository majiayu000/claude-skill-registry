---
name: skill-forge
description: >
  Ultimate Claude Code skill creator and architect. Designs, scaffolds, builds,
  reviews, evolves, and publishes production-grade Claude Code skills following
  the Agent Skills open standard and 3-layer architecture (directive, orchestration,
  execution). Handles single-file skills, multi-skill orchestrators with sub-skills
  and subagents, MCP-enhanced workflows, and full skill ecosystems. Industry
  detection for skill domain. Triggers on: "create skill", "build skill", "new skill",
  "skill creator", "skill builder", "skill-forge", "design skill", "scaffold skill",
  "review skill", "improve skill", "publish skill", "skill architecture",
  "convert skill", "port skill", "multi-platform", "cross-platform",
  "eval skill", "test skill", "benchmark skill", "skill evals",
  "measure skill", "skill performance", "skill A/B test".
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - Write
  - Edit
  - WebFetch
---

# Skill Forge — Ultimate Claude Code Skill Creator

Build production-grade Claude Code skills following the Agent Skills open standard,
progressive disclosure architecture, and battle-tested patterns from high-performing
skills like claude-seo and claude-ads.

## Quick Reference

| Command | What it does |
|---------|-------------|
| `/skill-forge` | Interactive skill creation wizard |
| `/skill-forge plan <domain>` | Architecture and design planning |
| `/skill-forge build <name>` | Scaffold and build a skill from plan |
| `/skill-forge review <path>` | Audit an existing skill for quality |
| `/skill-forge evolve <path>` | Improve skill based on feedback/issues |
| `/skill-forge eval <path>` | Run eval pipeline to test skill quality |
| `/skill-forge benchmark <path>` | Benchmark skill with variance analysis |
| `/skill-forge publish <path>` | Package and prepare for distribution |
| `/skill-forge convert <path>` | Convert skill to Codex/Gemini/Antigravity/Cursor |

## Orchestration Logic

### Interactive Mode (`/skill-forge`)

Walk the user through the full skill creation lifecycle:

1. **Discovery**: Ask about the domain, use cases, and target users
2. **Architecture**: Determine skill complexity tier and design structure
3. **Build**: Generate all files following chosen template
4. **Review**: Validate structure, frontmatter, triggers, and quality
5. **Eval**: Run eval pipeline with assertions and grading
6. **Benchmark**: Measure pass rate, time, tokens with variance analysis
7. **Iterate**: Refine based on eval results and feedback

### Command Routing

For specific commands, load the relevant sub-skill:
- `/skill-forge plan` -> `skills/skill-forge-plan/SKILL.md`
- `/skill-forge build` -> `skills/skill-forge-build/SKILL.md`
- `/skill-forge review` -> `skills/skill-forge-review/SKILL.md`
- `/skill-forge evolve` -> `skills/skill-forge-evolve/SKILL.md`
- `/skill-forge eval` -> `skills/skill-forge-eval/SKILL.md`
- `/skill-forge benchmark` -> `skills/skill-forge-benchmark/SKILL.md`
- `/skill-forge publish` -> `skills/skill-forge-publish/SKILL.md`
- `/skill-forge convert` -> `skills/skill-forge-convert/SKILL.md`

## Skill Complexity Tiers

Detect the appropriate tier based on user's description:

### Tier 1: Single Skill (1 SKILL.md)
- Simple workflow or document generation
- No sub-skills or subagents needed
- Under 200 lines of instructions
- **Template**: `assets/templates/minimal.md`

### Tier 2: Skill + Scripts (SKILL.md + scripts/)
- Needs deterministic execution (validation, data processing)
- Python/Bash scripts for fragile operations
- **Template**: `assets/templates/workflow.md`

### Tier 3: Multi-Skill Orchestrator (main + sub-skills)
- Complex domain with multiple distinct workflows
- Main skill routes to specialized sub-skills
- Shared references across sub-skills
- **Template**: `assets/templates/multi-skill.md`

### Tier 4: Full Ecosystem (orchestrator + sub-skills + agents + scripts)
- Enterprise-grade skill with parallel subagent delegation
- Multiple execution scripts for deterministic tasks
- Industry templates and reference knowledge
- **Template**: `assets/templates/ecosystem.md`

## Core Principles (Enforce in ALL generated skills)

### 1. Progressive Disclosure (3 Levels)
- **Level 1 (frontmatter)**: Always in system prompt. Name + description only (~50-100 tokens)
- **Level 2 (SKILL.md body)**: Loaded on activation. Core instructions (<500 lines, <5000 tokens)
- **Level 3 (references/scripts/assets)**: Loaded on-demand. Detailed knowledge and execution

### 2. Description is King
The `description` field determines when the skill activates. It MUST contain:
- WHAT the skill does (capabilities)
- WHEN to use it (trigger phrases users would say)
- Key domain keywords for matching

Read `references/description-guide.md` for the complete framework.

### 3. The 3-Layer Architecture
- **Layer 1 (Directive)**: SKILL.md instructions, reference files = the "what"
- **Layer 2 (Orchestration)**: Claude's routing and decision-making = the "how"
- **Layer 3 (Execution)**: Scripts in scripts/ = the "do"

Push deterministic work into scripts. Keep probabilistic decisions in instructions.

### 4. Naming Conventions
- Skill folder: `kebab-case` (lowercase + hyphens only)
- Name field must match folder name exactly
- Sub-skills: `{parent}-{child}` (e.g., `seo-audit`, `ads-google`)
- Agents: `agents/{skill}-{role}.md` (e.g., `agents/seo-technical.md`)
- No "claude" or "anthropic" in skill names (reserved)

### 5. File Rules
- Required: `SKILL.md` (exact case)
- No `README.md` inside skill folders
- No XML angle brackets in frontmatter
- Reference files: focused, small, loaded on-demand
- Scripts: atomic, testable, well-documented

## Quality Gates

Before marking any generated skill as complete:
- [ ] SKILL.md exists with valid YAML frontmatter
- [ ] Name is valid kebab-case (1-64 chars)
- [ ] Description includes WHAT + WHEN + keywords (<1024 chars)
- [ ] No XML tags in frontmatter
- [ ] Instructions are specific and actionable (not vague)
- [ ] Error handling included for common failures
- [ ] Examples provided for key workflows
- [ ] SKILL.md body under 500 lines
- [ ] Reference files linked (not inlined) for detailed knowledge
- [ ] Scripts have docstrings, type hints, error handling

Run `python scripts/validate_skill.py <path>` to verify programmatically.

## Reference Files

Load on-demand as needed -- do NOT load all at startup:
- `references/anatomy.md` -- Skill file structure, naming rules, agent format
- `references/patterns.md` -- Proven workflow patterns with examples
- `references/frontmatter-spec.md` -- YAML frontmatter specification (skills)
- `references/description-guide.md` -- Writing trigger-optimized descriptions
- `references/testing-guide.md` -- Testing methodology and checklist
- `references/pro-agent.md` -- 3-layer architecture deep dive
- `references/tools-reference.md` -- All tool names, permission patterns, MCP
- `references/hooks-reference.md` -- Hook events, types, quality gate patterns
- `references/skills-activation.md` -- Skill discovery, activation, advanced features
- `references/platforms.md` -- Platform specs and conversion rules

## Sub-Skills

This skill orchestrates 8 specialized sub-skills:

1. **skill-forge-plan** -- Architecture design and use case planning
2. **skill-forge-build** -- Scaffold and generate skill files
3. **skill-forge-review** -- Audit and validate existing skills
4. **skill-forge-evolve** -- Improve skills based on feedback
5. **skill-forge-eval** -- Run eval pipeline with assertions and grading
6. **skill-forge-benchmark** -- Benchmark performance with variance analysis
7. **skill-forge-publish** -- Package and prepare for distribution
8. **skill-forge-convert** -- Convert skills for Codex, Gemini CLI, Antigravity, Cursor
