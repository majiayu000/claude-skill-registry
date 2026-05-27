---
name: blueprint-research
description: Research phase for blueprint workflow - toolbox resolution, lessons discovery, and parallel research agents
---

# Blueprint Research

Handles Steps 4-6 of the blueprint workflow: Toolbox resolution, lessons discovery, and parallel research execution.

## Input

```yaml
feature_description: string
tech_stack: string | string[]  # From config-reader
discovery_result: object       # From blueprint-discovery
```

## 1. Resolve Toolbox + Discover Lessons

**Read config (parallel):**
```
/majestic:config tech_stack generic
/majestic:config lessons_path .claude/lessons/
```

**Spawn agents (parallel):**
```
Task(majestic-engineer:workflow:toolbox-resolver):
  prompt: "Stage: blueprint | Tech Stack: {tech_stack}"

Task(majestic-engineer:workflow:lessons-discoverer):
  prompt: "workflow_phase: planning | tech_stack: {tech_stack} | task: {feature_description}"
```

**Store outputs:**
- `research_hooks` → for Step 2
- `coding_styles` → for Step 3
- `lessons_context` → for architect agent

**Non-blocking errors:**
- No toolbox found → Continue with core agents
- Lessons directory missing → Continue
- Discovery returns 0 lessons → Log, continue
- Discovery fails → Log warning, continue

## 2. Spawn Research Agents

**Core agents (always run):**
```
Task(majestic-engineer:research:git-researcher, prompt="{feature}")
Task(majestic-engineer:research:docs-researcher, prompt="{feature}")
Task(majestic-engineer:research:best-practices-researcher, prompt="{feature}")
```

**Stack-specific agents (from toolbox):**
```
For each hook in research_hooks:
  If hook.triggers.any_substring matches feature_description:
    Task(subagent_type=hook.agent, prompt="{feature} | Context: {hook.context}")
```

**Cap:** Maximum 5 total agents to avoid noise.

**Wait:** Collect all results before proceeding.

## 3. Spec Review + Skill Injection

**Run in parallel:**
```
Task(majestic-engineer:plan:spec-reviewer):
  prompt: "Feature: {feature} | Research: {combined_research}"

For each skill in coding_styles:
  Skill(skill: skill)
```

**Outputs:**
- `spec_findings` → gaps, edge cases, questions
- `skill_content` → loaded coding style content

## Output

```yaml
research_result:
  toolbox:
    research_hooks: array
    coding_styles: array
  lessons_context: string | null
  research_findings:
    git: string
    docs: string
    best_practices: string
    stack_specific: array
  spec_findings:
    gaps: array
    edge_cases: array
    questions: array
  skill_content: string
  ready_for_architecture: boolean
```
