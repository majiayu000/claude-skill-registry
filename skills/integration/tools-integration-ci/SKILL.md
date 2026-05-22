---
name: tools-integration-ci
description: CI provider abstraction with unified API for GitHub and GitLab operations (PR, issues, CI status)
user-invocable: false
allowed-tools: Read, Bash
---

# Tools Integration CI Skill

Unified CI provider abstraction using **static routing** - one script per provider, config stores full commands.

## What This Skill Provides

- Provider detection and health verification
- PR operations (create, reviews)
- CI status and wait operations
- Issue operations (create)
- Unified TOON output format across providers

## When to Activate This Skill

Activate when:
- Detecting CI provider from repository configuration
- Verifying CI tool installation and authentication
- Creating or managing pull requests
- Checking CI status or waiting for CI completion
- Creating issues

---

## Architecture

**Static Routing Pattern**: Config stores full commands, wizard generates provider-specific paths.

```
marshal.json                          Scripts
ci.commands.pr-create ─────────────► github.py pr create
ci.commands.ci-status ─────────────► github.py ci status
```

**Load Reference**: For full architecture details:
```
Read standards/architecture.md
```

---

## Skill Structure

```
tools-integration-ci/
├── SKILL.md                     # This file
├── standards/
│   ├── architecture.md          # Static routing, skill boundaries
│   ├── api-contract.md          # Shared TOON output formats
│   ├── github-impl.md           # GitHub-specific: gh CLI
│   └── gitlab-impl.md           # GitLab-specific: glab CLI
└── scripts/
    ├── ci_health.py             # Detection & verification
    ├── github.py                # GitHub operations via gh
    └── gitlab.py                # GitLab operations via glab
```

---

## Scripts

| Script | Notation | Purpose |
|--------|----------|---------|
| ci_health | `plan-marshall:tools-integration-ci:ci_health` | Provider detection & verification |
| github | `plan-marshall:tools-integration-ci:github` | GitHub operations via gh CLI |
| gitlab | `plan-marshall:tools-integration-ci:gitlab` | GitLab operations via glab CLI |

---

## Workflow: Health Check

**Pattern**: Command Chain Execution

Detect CI provider and verify tools are available and authenticated.

### Step 1: Run Health Check

```bash
python3 .plan/execute-script.py plan-marshall:tools-integration-ci:ci_health status
```

### Step 2: Process Result

```toon
status: success
provider: github
repo_url: https://github.com/org/repo
confidence: high
required_tool: gh
required_tool_ready: true
overall: healthy

tools[2]{name,installed,authenticated}:
git	true	true
gh	true	true
```

---

## Workflow: Detect Provider

**Pattern**: Command Chain Execution

Detect CI provider from git remote URL.

### Step 1: Run Detection

```bash
python3 .plan/execute-script.py plan-marshall:tools-integration-ci:ci_health detect
```

### Step 2: Process Result

```toon
status: success
provider: github
repo_url: https://github.com/org/repo
confidence: high
```

---

## Workflow: Persist Configuration

**Pattern**: Command Chain Execution

Detect provider and persist to marshal.json with static commands.

### Step 1: Run Persist

```bash
python3 .plan/execute-script.py plan-marshall:tools-integration-ci:ci_health persist
```

### Step 2: Process Result

```toon
status: success
persisted_to: marshal.json

ci_config{key,value}:
provider	github
repo_url	https://github.com/org/repo

ci_commands[5]{name,command}:
pr-create	python3 .plan/execute-script.py plan-marshall:tools-integration-ci:github pr create
pr-reviews	python3 .plan/execute-script.py plan-marshall:tools-integration-ci:github pr reviews
ci-status	python3 .plan/execute-script.py plan-marshall:tools-integration-ci:github ci status
ci-wait	python3 .plan/execute-script.py plan-marshall:tools-integration-ci:github ci wait
issue-create	python3 .plan/execute-script.py plan-marshall:tools-integration-ci:github issue create
```

---

## Workflow: Create PR

**Pattern**: Config-Driven Execution

Create a pull request using config-stored command.

### Step 1: Resolve Command from Config

```bash
COMMAND=$(jq -r '.ci.commands["pr-create"]' .plan/marshal.json)
```

### Step 2: Execute with Arguments

```bash
eval "$COMMAND --title 'Add feature X' --body 'Description' --base main"
```

### Alternative: Direct Script Invocation

```bash
python3 .plan/execute-script.py plan-marshall:tools-integration-ci:github pr create \
    --title "Add feature X" \
    --body "Description" \
    --base main
```

### Step 3: Process Result

```toon
status: success
operation: pr_create
pr_number: 456
pr_url: https://github.com/org/repo/pull/456
```

---

## Workflow: Check CI Status

**Pattern**: Config-Driven Execution

Check CI status for a pull request.

### Step 1: Resolve and Execute

```bash
COMMAND=$(jq -r '.ci.commands["ci-status"]' .plan/marshal.json)
eval "$COMMAND --pr-number 123"
```

### Step 2: Process Result

```toon
status: success
operation: ci_status
pr_number: 123
overall_status: pending

checks[3]{name,status,conclusion}:
build	completed	success
test	in_progress	-
lint	completed	failure
```

---

## Workflow: Wait for CI

**Pattern**: Polling with Timeout

Wait for CI checks to complete with two-layer timeout pattern.

### Step 1: Execute with Timeout

Use outer shell timeout as safety net:

```bash
timeout 600s python3 .plan/execute-script.py plan-marshall:tools-integration-ci:github ci wait \
    --pr-number 123
```

**Claude Bash Tool**: Set `timeout` parameter to `600000` (ms).

### Step 2: Process Result

```toon
status: success
operation: ci_wait
pr_number: 123
final_status: success
duration_sec: 95
```

---

## Workflow: Get PR Reviews

**Pattern**: Config-Driven Execution

Get reviews for a pull request.

### Step 1: Resolve and Execute

```bash
COMMAND=$(jq -r '.ci.commands["pr-reviews"]' .plan/marshal.json)
eval "$COMMAND --pr-number 123"
```

### Step 2: Process Result

```toon
status: success
operation: pr_reviews
pr_number: 123

reviews[2]{user,state,submitted_at}:
alice	APPROVED	2025-01-15T10:30:00Z
bob	CHANGES_REQUESTED	2025-01-15T11:00:00Z
```

---

## Workflow: Create Issue

**Pattern**: Config-Driven Execution

Create an issue.

### Step 1: Resolve and Execute

```bash
COMMAND=$(jq -r '.ci.commands["issue-create"]' .plan/marshal.json)
eval "$COMMAND --title 'Bug: feature X' --body 'Description'"
```

### Step 2: Process Result

```toon
status: success
operation: issue_create
issue_number: 789
issue_url: https://github.com/org/repo/issues/789
```

---

## Workflow: View Issue

**Pattern**: Config-Driven Execution

View issue details.

### Step 1: Resolve and Execute

```bash
python3 .plan/execute-script.py plan-marshall:tools-integration-ci:github issue view \
    --issue 123
```

### Step 2: Process Result

```toon
status: success
operation: issue_view
issue_number: 123
issue_url: https://github.com/org/repo/issues/123
title: Bug in authentication flow
body: When users try to login...
author: username
state: open
created_at: 2025-01-15T10:30:00Z
updated_at: 2025-01-18T14:20:00Z

labels[2]:
- bug
- priority:high

assignees[1]:
- alice
```

---

## Storage Pattern

**Split storage** (shared vs local):

| File | Content | Shared |
|------|---------|--------|
| `.plan/marshal.json` | `ci.provider`, `ci.repo_url`, `ci.commands` | Yes (git) |
| `.plan/run-configuration.json` | `ci.authenticated_tools`, command timeouts | No (local) |

---

## Error Handling

All operations return TOON error format on failure:

```toon
status: error
operation: pr_create
error: Authentication failed
context: gh auth status returned non-zero
```

Exit codes:
- `0`: Success (stdout)
- `1`: Error (stderr)

---

## Tool Requirements

| Provider | CLI Tool | Auth Check |
|----------|----------|------------|
| github | `gh` | `gh auth status` |
| gitlab | `glab` | `glab auth status` |

---

## References

- `standards/architecture.md` - Static routing and skill boundaries
- `standards/api-contract.md` - Shared TOON output formats
- `standards/github-impl.md` - GitHub-specific implementation
- `standards/gitlab-impl.md` - GitLab-specific implementation
