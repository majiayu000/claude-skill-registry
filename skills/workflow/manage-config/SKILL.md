---
name: manage-config
description: Manage per-plan configuration with schema validation
allowed-tools: Read, Glob, Bash
---

# Manage Config Skill

Per-plan configuration management for plan-specific settings stored in `config.toon`.

## What This Skill Provides

- Per-plan config.toon management with schema validation
- Domain array management for multi-domain plans
- Field-level get/set operations with nested access support
- Multi-field retrieval

Note: `workflow_skills` are NOT stored in config.toon. They are resolved at runtime from `marshal.json` via `plan-marshall-config resolve-workflow-skill`.

## When to Activate This Skill

Activate this skill when:
- Creating initial plan configuration
- Reading or updating plan settings
- Retrieving domains for a plan

---

## Storage Location

Configuration is stored in the plan directory:

```
.plan/plans/{plan_id}/config.toon
```

---

## File Format

See [standards/config-toon-format.md](standards/config-toon-format.md) for complete format specification including field definitions, phase values, and examples.

---

## Operations

Script: `pm-workflow:manage-config:manage-config`

### create

Create config.toon with domains configuration.

```bash
python3 .plan/execute-script.py pm-workflow:manage-config:manage-config create \
  --plan-id {plan_id} \
  --domains java
```

**Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `--domains` | string (comma-separated) | Yes | Domain list (e.g., `java` or `java,javascript`) |
| `--commit-strategy` | enum | No | `per_task` (default), `per_plan`, `none` |
| `--create-pr` | bool | No | Create PR on finalize (default from marshal.json) |
| `--verification-required` | bool | No | Require verification (default from marshal.json) |
| `--verification-command` | string | No | Verification command |
| `--branch-strategy` | enum | No | `feature` (default), `direct` |
| `--force` | flag | No | Overwrite existing config |

**Output** (TOON):
```toon
status: success
plan_id: my-feature
file: config.toon
created: true

config:
  domains[1]:
  - java
  commit_strategy: per_task
  create_pr: true
  verification_required: true
  branch_strategy: feature
```

### get-domains

Get the domains array from config.toon.

```bash
python3 .plan/execute-script.py pm-workflow:manage-config:manage-config \
  get-domains --plan-id {plan_id}
```

**Output** (TOON):
```toon
status: success
plan_id: my-feature
domains[2]:
- java
- javascript
count: 2
```

### read

Read entire config.toon content.

```bash
python3 .plan/execute-script.py pm-workflow:manage-config:manage-config read \
  --plan-id {plan_id}
```

**Output** (TOON):
```toon
status: success
plan_id: my-feature

config:
  domains[1]:
  - java
  commit_strategy: per_task
```

### get

Get a specific field value. Supports nested field access via dot notation.

```bash
# Simple field
python3 .plan/execute-script.py pm-workflow:manage-config:manage-config get \
  --plan-id {plan_id} \
  --field commit_strategy
```

**Output** (TOON):
```toon
status: success
plan_id: my-feature
field: commit_strategy
value: per_task
```

### set

Set a specific field value.

```bash
python3 .plan/execute-script.py pm-workflow:manage-config:manage-config set \
  --plan-id {plan_id} \
  --field commit_strategy \
  --value per_plan
```

**Output** (TOON):
```toon
status: success
plan_id: my-feature
field: commit_strategy
value: per_plan
previous: per_task
```

### get-multi

Get multiple fields in one call.

```bash
python3 .plan/execute-script.py pm-workflow:manage-config:manage-config get-multi \
  --plan-id {plan_id} \
  --fields "commit_strategy,branch_strategy"
```

**Output** (TOON):
```toon
status: success
plan_id: my-feature
commit_strategy: per_task
branch_strategy: feature
```

---

## Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `pm-workflow:manage-config:manage-config` | Per-plan config.toon operations | `python3 .plan/execute-script.py pm-workflow:manage-config:manage-config {subcommand} --help` |

---

## Validation Rules

| Field | Valid Values |
|-------|--------------|
| domains | lowercase identifiers (e.g., java, javascript, plan-marshall-plugin-dev, generic) |
| commit_strategy | per_task, per_plan, none |
| create_pr | true, false |
| verification_required | true, false |
| verification_command | any string |
| branch_strategy | feature, direct |

---

## Error Handling

```toon
status: error
plan_id: my-feature
error: invalid_domain
message: Invalid domain format: Java. Must be lowercase identifier
```

---

## Workflow Skill Resolution

Workflow skills are resolved from marshal.json (not config.toon):

```bash
python3 .plan/execute-script.py plan-marshall:plan-marshall-config:plan-marshall-config \
  resolve-workflow-skill --domain {domain} --phase {phase}
```

See `plan-marshall:plan-marshall-config` for workflow skill resolution.

---

## Integration Points

| Consumer | Operation | Purpose |
|----------|-----------|---------|
| plan-init-agent | `create` | Create config.toon with domains |
| solution-outline-agent | `get-domains` | Get domains for deliverable assignment |
| plan-execute | `read`, `get` | Read commit strategy, verification settings |
| plan-finalize | `get` | Check create_pr, branch_strategy |

---

## Related Skills

| Skill | Purpose |
|-------|---------|
| `plan-marshall:plan-marshall-config` | Project-level marshal.json configuration, workflow skill resolution |
