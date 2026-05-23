---
name: phase-5-finalize
description: Complete plan execution with git workflow and PR management
allowed-tools: Read, Bash, Glob, SlashCommand
---

# Phase Finalize Skill

**Role**: Finalize phase skill. Handles git workflow (commit, push, PR) and plan completion. Reads configuration from config.toon written during init phase.

**Key Pattern**: Configuration-agnostic execution. All finalize behavior determined by config.toon values.

## When to Activate This Skill

Activate when:
- Execute phase has completed (all tasks done)
- Ready to commit and potentially create PR
- Plan is in `finalize` phase

---

## Scripts

| Script | Purpose |
|--------|---------|
| `pm-workflow:manage-config:manage-config` | Config field access |
| `pm-workflow:manage-references:manage-references` | Reference file CRUD |
| `pm-workflow:manage-lifecycle:manage-lifecycle` | Phase transitions |
| `plan-marshall:logging:manage-log` | Work log entries |
| `pm-workflow:workflow-integration-git:git-workflow` | Commit, push, PR creation |

---

## Configuration Source

All finalize configuration is read from config.toon (written during init phase):

```bash
python3 .plan/execute-script.py pm-workflow:manage-config:manage-config get-multi \
  --plan-id {plan_id} \
  --fields create_pr,verification_required,verification_command,branch_strategy
```

Returns only the required finalize fields in a single call.

**Config Fields Used**:

| Field | Values | Description |
|-------|--------|-------------|
| `create_pr` | true/false | Whether to create a pull request |
| `verification_required` | true/false | Whether verification must pass |
| `verification_command` | command/null | Verification command to run |
| `branch_strategy` | feature/direct | Branch strategy |

---

## Operation: finalize

**Input**: `plan_id`

### Step 0: Log Phase Start

```bash
python3 .plan/execute-script.py plan-marshall:logging:manage-log \
  work {plan_id} INFO "[STATUS] (pm-workflow:phase-5-finalize) Starting finalize phase"
```

### Step 1: Read Configuration

```bash
python3 .plan/execute-script.py pm-workflow:manage-config:manage-config get-multi \
  --plan-id {plan_id} \
  --fields create_pr,verification_required,verification_command,branch_strategy
```

Returns: `create_pr`, `verification_required`, `verification_command`, `branch_strategy` in a single call.

Also read references context for branch and issue information:

```bash
python3 .plan/execute-script.py pm-workflow:manage-references:manage-references get-context \
  --plan-id {plan_id}
```

Returns: `branch`, `base_branch`, `issue_url`, `build_system`, and file counts in a single call.

**After reading configuration**, log the finalize strategy decision:

```bash
python3 .plan/execute-script.py plan-marshall:logging:manage-log \
  work {plan_id} INFO "[DECISION] (pm-workflow:phase-5-finalize) Finalize strategy: verification={verification_required}, PR={create_pr}, branch={branch_strategy}"
```

### Step 2: Run Verification (if required)

If `verification_required == true` and `verification_command` is set:

```bash
SlashCommand("{verification_command}")
```

Common verification commands:
- `/pm-dev-builder:builder-build-and-fix` - Java/Gradle/Maven
- `/pm-dev-builder:builder-build-and-fix system=npm` - JavaScript
- `/pm-plugin-development:plugin-doctor` - Plugin development

If verification fails, report error and allow retry.

### Step 3: Commit Workflow

Load the git-workflow skill for commit operations:

```
Skill: pm-workflow:workflow-integration-git
```

The git-workflow skill handles:
- Artifact detection and cleanup (*.class, *.temp files)
- Commit message generation following conventional commits
- Stage, commit, and push operations

**Parameters** (from config and request):
- `message`: Generated from request.md summary
- `push`: true (always push in finalize)
- `create-pr`: from `create_pr` config field

### Step 4: Create PR (if enabled)

If `create_pr == true`, the git-workflow skill creates the PR with:
- Title from request.md
- Body using `templates/pr-template.md`
- Issue link from references.toon (`Closes #{issue}` if present)

### Step 5: PR Workflow (if PR created)

If PR was created and `pr_workflow` expected:

```
SlashCommand("/pm-workflow:pr-doctor")
```

This handles CI monitoring and review addressing.

### Step 6: Mark Plan Complete

Transition to complete:

```bash
python3 .plan/execute-script.py pm-workflow:manage-lifecycle:manage-lifecycle transition \
  --plan-id {plan_id} \
  --completed finalize
```

### Step 7: Log Completion

```bash
python3 .plan/execute-script.py plan-marshall:logging:manage-log \
  work {plan_id} INFO "[STATUS] (pm-workflow:phase-5-finalize) Plan completed: commit={commit_hash}, PR={pr_url|skipped}"
```

---

## Output

**Success**:

```toon
status: success
plan_id: {plan_id}

actions:
  verification: {passed|skipped}
  commit: {commit_hash}
  push: success
  pr: {created #{number}|skipped}
  pr_workflow: {completed|skipped}

next_state: complete
```

**Error**:

```toon
status: error
plan_id: {plan_id}
step: {verification|commit|push|pr}
message: {error_description}
recovery: {recovery_suggestion}
```

---

## Error Handling

On any error, **first log the error** to work-log:

```bash
python3 .plan/execute-script.py plan-marshall:logging:manage-log \
  work {plan_id} ERROR "[ERROR] (pm-workflow:phase-5-finalize) {step} failed - {error_type}: {error_context}"
```

### Verification Failure

```toon
status: error
step: verification
message: Build failed with errors
recovery: Fix errors and re-run finalize
```

### Git Commit Failure

```toon
status: error
step: commit
message: Nothing to commit or merge conflict
recovery: Resolve conflicts, then re-run finalize
```

### Push Failure

```toon
status: error
step: push
message: Remote rejected push
recovery: Pull changes, resolve conflicts, then re-run finalize
```

### PR Creation Failure

```toon
status: error
step: pr
message: PR already exists or branch not pushed
recovery: Check existing PRs or push branch first
```

---

## Resumability

The skill checks current state before each step:

1. **Has verification passed?** Skip if already verified
2. **Are there uncommitted changes?** Skip commit if clean
3. **Is branch pushed?** Skip push if remote is current
4. **Does PR exist?** Skip creation if PR exists
5. **Is plan already complete?** Skip if finalize done

---

## Finalize by Domain

### Java / JavaScript

Full workflow:
1. Verification (build/test)
2. Commit
3. Push
4. Create PR
5. PR workflow (/pr-doctor)

### Plugin Development

Partial workflow:
1. Verification (/plugin-doctor)
2. Commit
3. Push
4. (No PR)

### Generic

Minimal workflow:
1. (No verification)
2. Commit
3. Push
4. (No PR)

---

## Standards (Load On-Demand)

### Validation
```
Read standards/validation.md
```
Contains: Configuration requirements, step-by-step validation checklist, output format examples

### Triage Integration
```
Read standards/triage-integration.md
```
Contains: How to load domain-specific triage extensions, findings routing, decision flow, iteration loop

### Lessons Integration
```
Read standards/lessons-integration.md
```
Contains: How lessons inform triage decisions, lesson query before decisions, recording new triage lessons

---

## Templates

| Template | Purpose |
|----------|---------|
| `templates/pr-template.md` | PR body format |

---

## Scripts Used

| Script | Command | Purpose |
|--------|---------|---------|
| `pm-workflow:manage-config:manage-config` | `get-multi` | Read finalize config fields |
| `pm-workflow:manage-references:manage-references` | `get-context` | Read branch, issue info |
| `pm-workflow:manage-lifecycle:manage-lifecycle` | `transition` | Phase transition |
| `plan-marshall:logging:manage-log` | `work` | Log completion |
| `pm-workflow:workflow-integration-git:git-workflow` | `format-commit`, `analyze-diff` | Commit message generation |

---

## Integration

### Phase Routing

This skill is invoked when plan is in `5-finalize` phase:

```
pm-workflow:manage-lifecycle route --phase 5-finalize → pm-workflow:phase-5-finalize
```

### Command Integration

- **/plan-execute action=finalize** - May invoke this skill
- **/pr-doctor** - Used during PR workflow

### Related Skills

- **git-workflow** - Handles commit, push, and PR creation
- **plan-execute** - Previous phase (executes tasks)
- **manage-lifecycle** - Handles phase transitions
- **java-triage** - Java triage extension (pm-dev-java)
- **javascript-triage** - JavaScript triage extension (pm-dev-frontend)
- **plugin-triage** - Plugin development triage extension (pm-plugin-development)
