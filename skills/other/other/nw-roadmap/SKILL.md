---
name: nw-roadmap
description: "Creates a phased roadmap.json for a feature goal with acceptance criteria and TDD steps. Use when planning implementation steps before execution."
user-invocable: false
argument-hint: '[agent] [goal-description] - Example: @solution-architect "Migrate to microservices"'
---

# NW-ROADMAP: Goal Planning

**Wave**: CROSS_WAVE
**Agent**: Architect (nw-solution-architect) or domain-appropriate agent

## Overview

Dispatches expert agent to fill a pre-scaffolded YAML roadmap skeleton. CLI tools handle structure; agent handles content.

Output: `docs/feature/{feature-id}/deliver/roadmap.json`

## Usage

```bash
/nw-roadmap @nw-solution-architect "Migrate monolith to microservices"
/nw-roadmap @nw-software-crafter "Replace legacy authentication system"
/nw-roadmap @nw-product-owner "Implement multi-tenant support"
```

## Execution Steps

You MUST execute these steps in order. Do NOT skip any.

1. **Parse Parameters** — Extract agent name (after @, validated against agent registry), goal description (quoted string), and derive feature-id from goal in kebab-case (e.g., "Migrate to OAuth2" -> "migrate-to-oauth2"). Gate: agent name, goal, and feature-id all resolved.

2. **Scaffold Skeleton** — Run `des.cli.roadmap init` via Bash BEFORE invoking agent. Gate: CLI exits 0; stop and report error on non-zero exit.

```bash
des-roadmap init \
  --project-id {feature-id} \
  --goal "{goal-description}" \
  --output docs/feature/{feature-id}/deliver/roadmap.json
```
For complex projects add: `--phases 3 --steps "01:3,02:2,03:1"`

Do NOT write the file manually.

3. **Invoke Agent** — Invoke the named agent via Task tool to fill skeleton TODO placeholders. Gate: agent completes without error.

```
@{agent-name}

Fill in the roadmap skeleton at docs/feature/{feature-id}/deliver/roadmap.json.
Replace every TODO with real content. Do NOT change the YAML structure
(phases, steps, keys). Fill in: names, descriptions, acceptance criteria,
time estimates, dependencies, and implementation_scope paths.

Goal: {goal-description}
```

Context to pass (if available): measurement baseline|mikado-graph.md|existing docs.

4. **Validate** — Run `des-roadmap validate` via Bash. Gate: exit 0 = success; exit 1 = print errors and stop; exit 2 = usage error, stop.

```bash
des-roadmap validate docs/feature/{feature-id}/deliver/roadmap.json
```

## Invocation Principles

Keep agent prompt minimal. Agent knows roadmap structure and planning methodology.

Pass: skeleton file path + goal description + measurement context (if available).
Do not pass: YAML templates|phase guidance|step decomposition rules.

For performance roadmaps, include measurement context inline so agent can validate targets against baselines.

## Success Criteria

### Dispatcher (you) — all 4 must be checked

- [ ] 1. Parameters parsed (agent name, goal, feature-id)
- [ ] 2. `des.cli.roadmap init` executed via Bash (exit 0)
- [ ] 3. Agent invoked via Task tool to fill TODO placeholders
- [ ] 4. `des.cli.roadmap validate` executed via Bash (exit 0)

### Agent output (reference)

- [ ] 5. All TODO placeholders replaced with real content
- [ ] 6. Steps are self-contained and atomic
- [ ] 7. Acceptance criteria are behavioral and measurable
- [ ] 8. Step decomposition ratio <= 2.5 (steps / production files)
- [ ] 9. Dependencies mapped, time estimates provided

## Error Handling

- Invalid agent: report valid agents and stop
- Missing goal: show usage syntax and stop
- Scaffold failure (exit 2): report CLI error and stop
- Validation failure (exit 1): print errors, do not proceed

## Examples

### Example 1: Standard architecture roadmap
```
/nw-roadmap @nw-solution-architect "Migrate authentication to OAuth2"
```
Derives feature-id="migrate-auth-to-oauth2", scaffolds skeleton, invokes agent to fill TODOs, validates. Produces docs/feature/migrate-auth-to-oauth2/deliver/roadmap.json.

### Example 2: Performance roadmap with measurement context
```
/nw-roadmap @nw-solution-architect "Optimize test suite execution"
```
Passes measurement data inline. Agent fills skeleton, validates targets against baseline, prioritizes largest bottleneck first.

### Example 3: Mikado refactoring
```
/nw-roadmap @nw-software-crafter "Extract payment module from monolith"
```
Agent fills skeleton with methodology: mikado, references mikado-graph.md, maps leaf nodes to steps.

## Workflow Context

```bash
/nw-roadmap @agent "goal"           # 1. Plan (init -> agent fills -> validate)
/nw-execute @agent "feature-id" "01-01" # 2. Execute steps
/nw-finalize @agent "feature-id"        # 3. Finalize
```
