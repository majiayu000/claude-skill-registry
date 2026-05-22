---
name: spec-driven-release
description: >
  Orchestrates production releases through spec-driven deployment workflow with structural
  anti-skip enforcement. Implements 8 phases covering setup, build, validation, staging,
  production deployment, post-deployment validation, documentation, and monitoring using the
  Execute-Verify-Gate pattern at every step. Designed to prevent token optimization bias
  through lean orchestration, fresh-context subagent delegation, and binary CLI gate
  enforcement. Supports multiple deployment strategies (blue-green, canary, rolling, recreate)
  and environments (staging, production). Use when deploying QA-approved stories.
  Always use this skill when the user runs /release.
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
  - Bash(kubectl:*)
  - Bash(docker:*)
  - Bash(terraform:*)
  - Bash(ansible:*)
  - Bash(az:*)
  - Bash(aws:*)
  - Bash(gcloud:*)
  - Bash(helm:*)
  - Bash(dotnet:*)
  - Bash(npm:*)
  - Bash(pytest:*)
  - Bash(python:*)
  - Bash(cargo:*)
  - Skill
model: opus
effort: High
---

# Spec-Driven Release

Orchestrate safe, automated deployments through strict 8-phase release workflow with staging validation, smoke testing, rollback capabilities, and release documentation.

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

**Token Optimization Bias is PROHIBITED.** Do not skip, compress, or shortcut any step. Every phase step exists because a previous failure proved it necessary. (Reference: RCA-001, RCA-002, RCA-041)

---

## Core Capabilities

1. **Automated Deployment** - Platform-agnostic (K8s, Docker, AWS, Azure, GCP, Vercel, Netlify, VPS)
2. **Progressive Rollout** - Blue-green, canary, rolling, recreate strategies
3. **Smoke Testing** - Health checks, critical path validation, performance verification
4. **Rollback Capability** - Automatic rollback on failure detection
5. **Release Documentation** - Release notes, changelog, audit trail
6. **Multi-Environment** - Staging-first with production promotion
7. **Build & Publish** - Tech stack detection, build execution, registry publishing

### Philosophy

**"Deploy with Confidence, Fail Gracefully, Safety Over Speed"**

---

## Parameter Extraction

Extract story ID, environment (staging/production), and deployment strategy from conversation context.

**Skills cannot accept runtime parameters.** All information extracted from conversation (YAML frontmatter, explicit statements, or file references).

See `.claude/skills/spec-driven-release/references/parameter-extraction.md` for the extraction algorithm.

Extraction methods: YAML frontmatter, file reference, explicit statement, status inference.
Default environment: staging (if unable to determine).

## Command Integration

| Context Marker | Set By | Description |
|----------------|--------|-------------|
| `$STORY_ID` | /release | Story identifier (STORY-NNN) |
| `$ENVIRONMENT` | /release | Target environment (staging/production) |

---

## Phase State Initialization [MANDATORY FIRST]

```bash
devforgeai-validate phase-init ${STORY_ID} --workflow=release --project-root=.
```

| Exit Code | Meaning | Action |
|-----------|---------|--------|
| 0 | New workflow | State file created. Set CURRENT_PHASE = "01". |
| 1 | Existing workflow | Resume. Run `devforgeai-validate phase-status ${STORY_ID} --workflow=release` to get CURRENT_PHASE. |
| 2 | Invalid story ID | HALT. Must match STORY-XXX pattern. |
| 127 | CLI not installed | Continue without enforcement (backward compatibility). |

---

## Phase Orchestration Loop

```
SKIP_PHASES = []  # Set by Phase 01 Step 1.9 based on project type

FOR phase_num in [01, 02, 03, 04, 05, 06, 07, 08]:
    phase_id = phase_num

    IF phase_id in SKIP_PHASES:
        Write skip marker with documented reason
        devforgeai-validate phase-record ${STORY_ID} --workflow=release --phase={phase_id} --status=skipped --project-root=.
        CONTINUE to next phase

    1. ENTRY GATE: devforgeai-validate phase-check ${STORY_ID} --workflow=release --from={prev} --to={phase_id} --project-root=.
       IF exit != 0: HALT

    2. LOAD: Read(file_path=".claude/skills/spec-driven-release/phases/{phase_files[phase_id]}")
       Load FRESH - do NOT rely on memory of previous reads

    3. EXECUTE: Follow every step in the phase file (EXECUTE-VERIFY-RECORD triplets)
       - Each step's EXECUTE instruction tells you exactly what to do
       - Each step's VERIFY instruction tells you how to confirm it happened
       - Each step's RECORD instruction tells you what CLI command to call

    4. RECORD: devforgeai-validate phase-record ${STORY_ID} --workflow=release --phase={phase_id} --project-root=.

    5. EXIT GATE: devforgeai-validate phase-complete ${STORY_ID} --workflow=release --phase={phase_id} --checkpoint-passed --project-root=.
       IF exit != 0: HALT
```

| Phase | Name | File |
|-------|------|------|
| 01 | Setup & Classification | `phases/phase-01-setup-classification.md` |
| 02 | Build & Package | `phases/phase-02-build-package.md` |
| 03 | Pre-Release Validation | `phases/phase-03-pre-release-validation.md` |
| 04 | Staging Deployment | `phases/phase-04-staging-deployment.md` |
| 05 | Production Deployment | `phases/phase-05-production-deployment.md` |
| 06 | Post-Deployment Validation | `phases/phase-06-post-deployment-validation.md` |
| 07 | Release Documentation | `phases/phase-07-release-documentation.md` |
| 08 | Monitoring, Cleanup & Closure | `phases/phase-08-monitoring-cleanup.md` |

---

## Required Subagents Per Phase

| Phase | Required Subagents | Enforcement |
|-------|-------------------|-------------|
| 01 | tech-stack-detector | BLOCKING |
| 02 | (none) | N/A |
| 03 | (none) | N/A |
| 04 | deployment-engineer | BLOCKING |
| 05 | deployment-engineer, security-auditor | BLOCKING |
| 06 | (none) | N/A |
| 07 | (none) | N/A |
| 08 | (none) | N/A |

**Deviation Protocol:** Any skip requires explicit user consent via AskUserQuestion.

---

## Adaptive Phase Skipping

Phase 01 classifies the project and sets SKIP_PHASES:

| Project Type | SKIP_PHASES | ACTIVE_PHASES | Rationale |
|-------------|-------------|---------------|-----------|
| **library** | [04, 05, 06, 08-monitoring] | [01, 02, 03, 07, 08-cleanup] | No deployment target |
| **cli** | [] | All phases | Deployable binary |
| **api** | [] | All phases | Deployable HTTP service |

**Detection:** Cargo.toml, package.json, pyproject.toml indicators (see Phase 01 steps).

**Skipped Phase Protocol:**
1. Load reference file for the phase (MANDATORY - even skipped phases load references)
2. Write skip marker with documented reason
3. Record skip via CLI gate
4. Advance to next phase

---

## State Persistence

**Location:** `devforgeai/workflows/${STORY_ID}-release-phase-state.json`

---

## Workflow Completion Validation

```
expected_phases = 8 - len(SKIP_PHASES)
IF completed_count < expected_phases: HALT "WORKFLOW INCOMPLETE - {completed_count}/{expected_phases} phases"
IF completed_count == expected_phases: "All {expected_phases} phases completed - Release workflow passed"
```

---

## Success Criteria

Release complete when:
- [ ] Setup and classification completed
- [ ] Build artifacts created (if applicable)
- [ ] Pre-release validation passed (QA approved, tests passing, config exists)
- [ ] Staging deployment + smoke tests passed (if applicable)
- [ ] Production deployment + smoke tests passed (if applicable)
- [ ] Post-deployment validation passed (if applicable)
- [ ] Release notes generated, story archived
- [ ] Monitoring configured (if applicable), checkpoint cleaned up
- [ ] Story status = "Released"

---

## Reference Files Index

**Local references** (loaded per-phase on demand, NOT consolidated):

| Phase | Reference Files (load via Read from .claude/skills/spec-driven-release/references/) |
|-------|-----------------------------------------------------------------------------|
| 01 | `parameter-extraction.md`, `tech-stack-detection.md`, `configuration-guide.md` |
| 02 | `build-commands.md`, `package-formats.md`, `registry-publishing.md` |
| 03 | `pre-release-validation.md`, `release-checklist.md` |
| 04 | `staging-deployment.md`, `deployment-strategies.md`, `platform-deployment-commands.md`, `smoke-testing-guide.md`, `post-staging-hooks.md` |
| 05 | `production-deployment.md`, `deployment-strategies.md`, `platform-deployment-commands.md`, `post-production-hooks.md` |
| 06 | `parallel-smoke-tests.md`, `post-deployment-validation.md`, `smoke-testing-guide.md`, `monitoring-metrics.md`, `rollback-procedures.md` |
| 07 | `release-documentation.md` |
| 08 | `monitoring-closure.md`, `monitoring-metrics.md` |

**Assets:**
- `.claude/skills/spec-driven-release/assets/templates/release-notes-template.md`
- `.claude/skills/spec-driven-release/assets/templates/deployment-config-template.yaml`
- `.claude/skills/spec-driven-release/assets/templates/rollback-plan-template.md`

**Automation Scripts:**
- `.claude/skills/spec-driven-release/scripts/health_check.py`
- `.claude/skills/spec-driven-release/scripts/smoke_test_runner.py`
- `.claude/skills/spec-driven-release/scripts/metrics_collector.py`
- `.claude/skills/spec-driven-release/scripts/rollback_automation.sh`
- `.claude/skills/spec-driven-release/scripts/release_notes_generator.py`
- `.claude/skills/spec-driven-release/scripts/emergency_rollback.sh`
- `.claude/skills/spec-driven-release/scripts/backup_database.sh`
