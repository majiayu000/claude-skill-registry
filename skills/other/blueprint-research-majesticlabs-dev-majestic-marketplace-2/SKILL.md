---
name: blueprint-research
description: Research phase for blueprint workflow - toolbox resolution, lessons discovery, and parallel research agents
---

# Blueprint Research

Handles the research phase of the blueprint workflow: Toolbox resolution, lessons discovery, local/external research decision, and spec review.

## Input

```yaml
feature_description: string
tech_stack: string | string[]  # From config-reader
discovery_result:
  user_familiarity: high | medium | low  # Do they know the codebase?
  user_intent: speed | thoroughness      # What matters more?
  topic_risk: high | medium | low        # Security, payments, external APIs?
  uncertainty_level: high | medium | low # Is the approach clear?
```

## 1. Resolve Toolbox + Discover Lessons

**Read config (parallel):**
```
/majestic:config tech_stack generic
/majestic:config lessons_path .agents-os/lessons/
```

**Spawn agents (parallel):**
```
Task(majestic-engineer:workflow:toolbox-resolver):
  prompt: "Stage: blueprint | Tech Stack: {tech_stack}"

Task(majestic-engineer:workflow:lessons-discoverer):
  prompt: "workflow_phase: planning | tech_stack: {tech_stack} | task: {feature_description}"
```

**Store outputs:**
- `research_hooks` → for Step 4 (external research)
- `coding_styles` → for Step 5 (skill injection)
- `lessons_context` → for architect agent

**Non-blocking errors:**
- No toolbox found → Continue with core agents
- Lessons directory missing → Continue
- Discovery returns 0 lessons → Log, continue
- Discovery fails → Log warning, continue

## 2. Local Research (Always Runs)

Fast, local research to understand codebase patterns before deciding on external research.

```
Task(majestic-engineer:research:git-researcher, prompt="{feature}")
Task(majestic-engineer:research:repo-analyst, prompt="{feature}")
```

**Store:** `local_findings` - patterns, conventions, similar implementations

## 3. Research Decision

Based on discovery signals + local findings, decide if external research adds value.

**Decision matrix:**

| Condition | External Research |
|-----------|-------------------|
| `topic_risk: high` (security, payments, external APIs) | **Always** - cost of missing something too high |
| `local_findings` has strong patterns + `user_familiarity: high` | **Skip** - codebase is authoritative |
| `uncertainty_level: high` OR `user_familiarity: low` | **Research** - external perspective valuable |
| `user_intent: speed` + adequate local patterns | **Skip** - optimize for velocity |
| Default (no strong signal) | **Research** - err on side of thoroughness |

```
research_decision = evaluate(discovery_result, local_findings)
  → SKIP_EXTERNAL | RUN_EXTERNAL

If research_decision == SKIP_EXTERNAL:
  Announce: "Codebase has solid patterns for this. Proceeding without external research."
Else:
  Announce: "Running external research for {reason}."
```

## 4. External Research (Conditional)

**Only runs if `research_decision == RUN_EXTERNAL`**

```
Task(majestic-engineer:research:docs-researcher, prompt="{feature}")
Task(majestic-engineer:research:best-practices-researcher, prompt="{feature}")
```

**Stack-specific agents (from toolbox):**
```
For each hook in research_hooks:
  If hook.triggers.any_substring matches feature_description:
    Task(subagent_type=hook.agent, prompt="{feature} | Context: {hook.context}")
```

**Cap:** Maximum 4 external agents to avoid noise.

**Wait:** Collect all results before proceeding.

## 5. Spec Review + Skill Injection

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
  research_decision: SKIP_EXTERNAL | RUN_EXTERNAL
  research_decision_reason: string
  research_findings:
    local:
      git: string
      repo: string
    external:              # null if research_decision == SKIP_EXTERNAL
      docs: string | null
      best_practices: string | null
      stack_specific: array | null
  spec_findings:
    gaps: array
    edge_cases: array
    questions: array
  skill_content: string
  ready_for_architecture: boolean
```
