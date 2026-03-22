---
name: spec-driven-ci
description: >
  Generate CI/CD pipeline workflows through spec-driven workflow generation with structural
  anti-skip enforcement. Implements 5 phases covering preflight validation, configuration loading,
  workflow template generation, cost optimization, and final validation using the Execute-Verify-Gate
  pattern at every step. Designed to prevent token optimization bias through lean orchestration and
  binary CLI gate enforcement. Currently supports GitHub Actions with cost-optimized Claude API
  integration (prompt caching, Haiku preference, max-turns limits). Use when setting up CI/CD
  automation for DevForgeAI projects. Always use this skill when the user runs /setup-github-actions.
  Also use when the user mentions GitHub Actions setup, CI/CD pipeline generation, headless DevForgeAI
  execution, or workflow automation for /dev and /qa commands.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
  - Task
  - Bash(devforgeai-validate:*)
  - Bash(git:*)
  - Bash(mkdir:*)
  - Skill
model: opus
effort: High
---

# Spec-Driven CI

Generate CI/CD pipeline workflows with structural anti-skip enforcement for headless DevForgeAI execution.

**Context files are THE LAW:** tech-stack.md, source-tree.md, dependencies.md, coding-standards.md, architecture-constraints.md, anti-patterns.md

**If ambiguous or conflicts detected: HALT and use AskUserQuestion**

---

## Execution Model

This skill expands inline. After invocation, execute Phase State Initialization immediately. Do not wait passively, ask permission, or offer execution options.

**Self-Check (if ANY box is true = VIOLATION):**

- [ ] Stopping to ask about token budget
- [ ] Stopping to offer execution options
- [ ] Waiting passively for results
- [ ] Asking "should I execute this?"
- [ ] Skipping a phase because it "seems simple"
- [ ] Combining multiple phases into one
- [ ] Summarizing instead of loading a reference file
- [ ] Skipping verification because "I already wrote the file"

**IF any box checked:** EXECUTION MODEL VIOLATION. Go directly to Phase State Initialization now.

---

## Anti-Skip Enforcement Contract

This skill enforces 4 independent anti-skip layers. ALL FOUR must fail for a step to be skipped:

1. **Fresh-context subagent execution** - Subagents run in isolated context without accumulated bias
2. **Binary CLI gates** - `devforgeai-validate phase-check/phase-complete/phase-record` (compiled, cannot be forged by LLM)
3. **Hook enforcement** - Shell scripts in `.claude/hooks/` run outside LLM control
4. **Step registry + artifact verification** - `.claude/hooks/phase-steps-registry.json` tracks every mandatory step

**Execute-Verify-Gate Pattern:** Every mandatory step in every phase file has three parts:
- **EXECUTE:** The exact action to perform
- **VERIFY:** How to confirm the action happened (Glob, Grep, exit code, Task result)
- **RECORD:** CLI command to record completion (`devforgeai-validate phase-record`)

**Token Optimization Bias is PROHIBITED.** Do not skip, compress, or shortcut any step. Every phase step exists because a previous failure proved it necessary.

---

## Core Capabilities

1. **Headless /dev Execution** - workflow_dispatch triggered story development via GitHub Actions
2. **PR Quality Gates** - Automated /qa validation on pull requests
3. **Parallel Story Matrix** - Concurrent story development with configurable max-parallel
4. **Installer Testing** - Optional workflow to validate DevForgeAI installer
5. **Cost Optimization** - Prompt caching, Haiku model preference, max-turns limits
6. **Headless Answers** - ci-answers.yaml pre-configures AskUserQuestion responses

### Philosophy

**"Automate with Confidence, Optimize for Cost, Enforce Every Phase"**

### Outputs Generated

| Output File | Location | Purpose |
|-------------|----------|---------|
| `dev-story.yml` | `.github/workflows/` | Headless /dev execution (workflow_dispatch) |
| `qa-validation.yml` | `.github/workflows/` | PR quality gate (pull_request trigger) |
| `parallel-stories.yml` | `.github/workflows/` | Matrix parallel story execution |
| `installer-testing.yml` | `.github/workflows/` | Optional installer validation |
| `github-actions.yaml` | `devforgeai/config/ci/` | CI configuration (model, caching, limits) |
| `ci-answers.yaml` | `devforgeai/config/ci/` | Headless AskUserQuestion responses |

---

## Parameter Extraction

Extract configuration from conversation context. Skills cannot accept runtime parameters -- all information is extracted from conversation state, existing config files, or user responses to AskUserQuestion.

See `.claude/skills/spec-driven-ci/references/parameter-extraction.md` for the extraction algorithm.

**Configuration Priority:**
1. User-provided answers (AskUserQuestion responses)
2. Existing `devforgeai/config/ci/github-actions.yaml` values
3. Skill defaults: `max_parallel_jobs: 5`, `enable_prompt_caching: true`, `prefer_haiku: true`

**Extraction methods:** Conversation context scanning, YAML file parsing, explicit user statements.

---

## Command Integration

| Context Marker | Set By | Description |
|----------------|--------|-------------|
| `$FORCE_FLAG` | /setup-github-actions | Force overwrite existing files (boolean, default: false) |

The `/setup-github-actions` command handles argument parsing and sets `$FORCE_FLAG` before invoking this skill. The skill reads this marker from the conversation context.

---

## Security Prerequisites

All generated workflows require GitHub Secrets configured before execution.

### Required Secrets

| Secret Name | Description | Source |
|-------------|-------------|--------|
| `ANTHROPIC_API_KEY` | Claude API authentication | [console.anthropic.com](https://console.anthropic.com) |
| `GITHUB_TOKEN` | Repository access (auto-provided) | Automatic by GitHub Actions |

### Setup Instructions

1. Navigate to repository **Settings > Secrets and variables > Actions**
2. Click **New repository secret**
3. Name: `ANTHROPIC_API_KEY`
4. Value: Your API key from console.anthropic.com
5. Click **Add secret**

### Security Validation

Workflows fail-fast if secrets are missing:
- Missing `ANTHROPIC_API_KEY`: "Error: ANTHROPIC_API_KEY secret not configured"
- Check GitHub Actions logs for validation errors

### Best Practices

- **Never commit API keys** to repository
- Use **repository secrets** for sensitive values
- Rotate keys periodically
- Use **environment protection rules** for production deployments

See `.claude/skills/spec-driven-ci/references/security-prerequisites.md` for complete security guidance.

---

## Phase State Initialization [MANDATORY FIRST]

Generate a session ID using the pattern `CI-{YYYY-MM-DD}-{NNN}` (e.g., `CI-2026-03-19-001`).

```bash
devforgeai-validate phase-init ${SESSION_ID} --workflow=ci --project-root=.
```

| Exit Code | Meaning | Action |
|-----------|---------|--------|
| 0 | New workflow | State file created. Set CURRENT_PHASE = "01". |
| 1 | Existing workflow | Resume. Run `devforgeai-validate phase-status ${SESSION_ID} --workflow=ci --project-root=.` to get CURRENT_PHASE. |
| 2 | Invalid session ID | HALT. Must match CI-YYYY-MM-DD-NNN pattern. |
| 127 | CLI not installed | Continue without enforcement (backward compatibility). |

---

## Phase Orchestration Loop

```
FOR phase_num in [01, 02, 03, 04, 05]:
    phase_id = phase_num

    1. ENTRY GATE: devforgeai-validate phase-check ${SESSION_ID} --workflow=ci --from={prev} --to={phase_id} --project-root=.
       IF exit != 0: HALT

    2. LOAD: Read(file_path=".claude/skills/spec-driven-ci/phases/{phase_files[phase_id]}")
       Load FRESH - do NOT rely on memory of previous reads

    3. EXECUTE: Follow every step in the phase file (EXECUTE-VERIFY-RECORD triplets)
       - Each step's EXECUTE instruction tells you exactly what to do
       - Each step's VERIFY instruction tells you how to confirm it happened
       - Each step's RECORD instruction tells you what CLI command to call

    4. RECORD: devforgeai-validate phase-record ${SESSION_ID} --workflow=ci --phase={phase_id} --project-root=.

    5. EXIT GATE: devforgeai-validate phase-complete ${SESSION_ID} --workflow=ci --phase={phase_id} --checkpoint-passed --project-root=.
       IF exit != 0: HALT
```

| Phase | Name | File |
|-------|------|------|
| 01 | Pre-Flight Validation | `phases/phase-01-preflight.md` |
| 02 | Configuration Loading | `phases/phase-02-config-loading.md` |
| 03 | Workflow Template Generation | `phases/phase-03-workflow-generation.md` |
| 04 | Cost Optimization | `phases/phase-04-cost-optimization.md` |
| 05 | Validation & Summary | `phases/phase-05-validation-summary.md` |

---

## Required Subagents Per Phase

| Phase | Required Subagents | Enforcement |
|-------|-------------------|-------------|
| 01 | (none) | N/A |
| 02 | (none) | N/A |
| 03 | (none) | N/A |
| 04 | (none) | N/A |
| 05 | (none) | N/A |

This skill requires no subagent delegation. All 5 phases are executed inline by the orchestrator.

**Deviation Protocol:** Any phase skip requires explicit user consent via AskUserQuestion.

---

## State Persistence

**Location:** `devforgeai/workflows/${SESSION_ID}-ci-phase-state.json`

**Lifecycle:**
1. **Phase Init** - CLI creates state file with session metadata
2. **Each Phase** - Status updated to "in_progress" at entry, "completed" at exit
3. **Resume** - Phase 01 detects existing state file and resumes from last completed phase
4. **Completion** - All 5 phases marked "completed"

---

## Workflow Completion Validation

```
expected_phases = 5
IF completed_count < expected_phases: HALT "WORKFLOW INCOMPLETE - {completed_count}/{expected_phases} phases"
IF completed_count == expected_phases: "All 5 phases completed - CI workflow generation passed"
```

---

## Success Criteria

CI workflow generation complete when:
- [ ] 4 workflow files created with valid YAML syntax
- [ ] 2 config files created (github-actions.yaml, ci-answers.yaml)
- [ ] All 5 acceptance criteria covered by workflows
- [ ] Cost optimization enabled (prompt caching, Haiku)
- [ ] ANTHROPIC_API_KEY documented in setup steps
- [ ] max-parallel configured appropriately
- [ ] All workflow triggers configured
- [ ] Artifact uploads configured for test results
- [ ] Summary displayed with next steps

---

## Reference Files Index

**Local references** (loaded per-phase on demand, NOT consolidated):

| Phase | Reference Files (load via Read from .claude/skills/spec-driven-ci/references/) |
|-------|-----------------------------------------------------------------------------|
| 01 | `parameter-extraction.md`, `git-repo-validation.md`, `context-file-validation.md`, `security-prerequisites.md` |
| 02 | `config-file-schema.md`, `ci-answers-protocol.md` |
| 03 | `workflow-templates.md` |
| 04 | `cost-optimization-strategies.md` |
| 05 | `yaml-validation-procedures.md`, `security-prerequisites.md` |

**Assets (workflow templates):**
- `.claude/skills/spec-driven-ci/assets/templates/dev-story-workflow.yml`
- `.claude/skills/spec-driven-ci/assets/templates/qa-validation-workflow.yml`
- `.claude/skills/spec-driven-ci/assets/templates/parallel-stories-workflow.yml`
- `.claude/skills/spec-driven-ci/assets/templates/installer-testing-workflow.yml`
- `.claude/skills/spec-driven-ci/assets/templates/github-actions-config.yaml`
- `.claude/skills/spec-driven-ci/assets/templates/ci-answers-config.yaml`
