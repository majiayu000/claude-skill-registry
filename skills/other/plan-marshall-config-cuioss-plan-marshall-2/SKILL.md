---
name: manage-plan-marshall-config
description: Project-level infrastructure configuration for marshal.json
user-invocable: false
allowed-tools: Read, Write, Edit, Bash
---

# Plan-Marshall Config Skill

Manages project-level infrastructure configuration in `.plan/marshal.json`.

## What This Skill Provides

- **Skill Domains**: Implementation skill defaults and optionals per domain
- **System Settings**: Retention and cleanup configuration
- **Plan Phase Configuration**: Phase-specific settings (branching, compatibility, commit strategy, pipelines)

## When to Activate This Skill

Activate this skill when:
- Initializing project configuration (`/marshall-steward` wizard)
- Querying implementation skills for a domain
- Managing retention settings
- Configuring plan phase settings

---

## Workflow: Initialize Configuration

**Pattern**: Script Automation

Initialize marshal.json with defaults.

```bash
python3 .plan/execute-script.py plan-marshall:manage-plan-marshall-config:plan-marshall-config init
```

---

## Workflow: Query Skill Domains

**Pattern**: Read-Process-Write

Get implementation skills for a specific domain.

### Get Domain Defaults

```bash
python3 .plan/execute-script.py plan-marshall:manage-plan-marshall-config:plan-marshall-config \
  skill-domains get-defaults --domain java-core
```

**Output**:
```toon
status: success
domain: java-core
defaults[1]:
- pm-dev-java:java-core
```

### Get Domain Optionals

```bash
python3 .plan/execute-script.py plan-marshall:manage-plan-marshall-config:plan-marshall-config \
  skill-domains get-optionals --domain java-implementation
```

### Validate Skill in Domain

```bash
python3 .plan/execute-script.py plan-marshall:manage-plan-marshall-config:plan-marshall-config \
  skill-domains validate --domain java-core --skill pm-dev-java:java-lombok
```

---

## Workflow: System Settings

**Pattern**: Read-Process-Write

Manage system-level infrastructure settings.

### Get Retention Settings

```bash
python3 .plan/execute-script.py plan-marshall:manage-plan-marshall-config:plan-marshall-config \
  system retention get
```

### Set Retention Field

```bash
python3 .plan/execute-script.py plan-marshall:manage-plan-marshall-config:plan-marshall-config \
  system retention set --field logs_days --value 7
```

---

## Workflow: Plan Phase Configuration

**Pattern**: Read-Process-Write

Manage phase-specific plan configuration. Each phase has its own sub-noun.

### Get Phase Configuration

```bash
python3 .plan/execute-script.py plan-marshall:manage-plan-marshall-config:plan-marshall-config \
  plan phase-2-refine get
```

### Get Specific Phase Field

```bash
python3 .plan/execute-script.py plan-marshall:manage-plan-marshall-config:plan-marshall-config \
  plan phase-2-refine get --field compatibility
```

### Set Phase Field

```bash
python3 .plan/execute-script.py plan-marshall:manage-plan-marshall-config:plan-marshall-config \
  plan phase-5-execute set --field commit_strategy --value per_plan
```

---

## Workflow: CI Command Lookup

**Pattern**: Lookup and Execute

Get a CI command by name, then execute with arguments.

### Get CI Command

```bash
python3 .plan/execute-script.py plan-marshall:manage-plan-marshall-config:plan-marshall-config \
  ci get-command --name issue-view
```

**Output**:
```toon
status: success
name: issue-view
command: python3 .plan/execute-script.py plan-marshall:tools-integration-ci:github issue view
```

### Execute the Command

Parse the `command` field from output, then execute with arguments:

```bash
python3 .plan/execute-script.py plan-marshall:tools-integration-ci:github issue view --issue 123
```

**Available CI commands** (registered via `ci_health persist`):
- `pr-create` - Create pull request
- `pr-reviews` - Get PR reviews
- `pr-comments` - Get PR comments
- `ci-status` - Check CI status
- `ci-wait` - Wait for CI completion
- `issue-create` - Create issue
- `issue-view` - View issue details

---

## API Reference

### Noun: skill-domains

| Verb | Parameters | Purpose |
|------|------------|---------|
| `list` | (none) | List all domains |
| `get` | `--domain` | Get full domain config (returns nested structure for technical domains) |
| `get-defaults` | `--domain` | Get default skills (returns `core.defaults` for nested domains) |
| `get-optionals` | `--domain` | Get optional skills (returns `core.optionals` for nested domains) |
| `set` | `--domain [--profile] [--defaults] [--optionals]` | Set domain config (profiles read from extension.py, system domain only) |
| `add` | `--domain --defaults [--optionals]` | Add new domain |
| `validate` | `--domain --skill` | Check if skill valid (searches all profiles for nested domains) |
| `detect` | (none) | Auto-detect domains from project files |
| `get-extensions` | `--domain` | Get workflow skill extensions for domain |
| `set-extensions` | `--domain --type --skill` | Set workflow skill extension (types: outline, triage) |
| `get-available` | (none) | Get available domains based on detected build systems |
| `configure` | `--domains` | Configure selected domains with templates |

### resolve-domain-skills

| Parameters | Purpose |
|------------|---------|
| `--domain --profile` | Resolve skills for domain and profile (aggregates `{domain}.core` + `{domain}.{profile}`) |

Standard profiles: `implementation`, `module_testing`, `integration_testing`, `quality`.

### resolve-workflow-skill

| Parameters | Purpose |
|------------|---------|
| `--phase` | Resolve system workflow skill for phase (init, refine, outline, plan, execute, verify, finalize) |

Always returns from the `system` domain's `workflow_skills`.

### resolve-workflow-skill-extension

| Parameters | Purpose |
|------------|---------|
| `--domain --type` | Resolve domain-specific workflow extension (types: outline, triage) |

Returns null (not error) if extension doesn't exist for the domain.

### get-workflow-skills

| Parameters | Purpose |
|------------|---------|
| (none) | Get all workflow skills from system domain (7-phase model) |

### get-skills-by-profile

| Parameters | Purpose |
|------------|---------|
| `--domain` | Get skills organized by profile for architecture enrichment |

### configure-task-executors

| Parameters | Purpose |
|------------|---------|
| (none) | Auto-discover profiles and register task executors (convention: profile X -> `pm-workflow:task-X`) |

### resolve-task-executor

| Parameters | Purpose |
|------------|---------|
| `--profile` | Resolve task executor skill for a profile (e.g., implementation, module_testing) |

### Noun: ext-defaults

| Verb | Parameters | Purpose |
|------|------------|---------|
| `get` | `--key` | Get extension default value |
| `set` | `--key --value` | Set extension default value (always overwrites) |
| `set-default` | `--key --value` | Set value only if key does not exist (write-once) |
| `list` | (none) | List all extension defaults |
| `remove` | `--key` | Remove extension default |

### Noun: system

| Verb | Parameters | Purpose |
|------|------------|---------|
| `retention get` | (none) | Get all retention settings |
| `retention set` | `--field --value` | Set retention field |

### Noun: plan

Phase-specific configuration using `plan {phase} {verb}` pattern.

| Verb | Parameters | Purpose |
|------|------------|---------|
| `phase-1-init get` | `[--field]` | Get init phase configuration |
| `phase-1-init set` | `--field --value` | Set init phase field (branch_strategy) |
| `phase-2-refine get` | `[--field]` | Get refine phase configuration |
| `phase-2-refine set` | `--field --value` | Set refine phase field (confidence_threshold, compatibility) |
| `phase-5-execute get` | `[--field]` | Get execute phase configuration |
| `phase-5-execute set` | `--field --value` | Set execute phase field (commit_strategy) |
| `phase-6-verify get` | `[--field]` | Get verify phase configuration |
| `phase-6-verify set-step` | `--step --enabled` | Toggle generic verify step |
| `phase-6-verify set-domain-step` | `--domain --step --enabled` | Toggle domain verify step |
| `phase-6-verify set-max-iterations` | `--value` | Set verify max iterations |
| `phase-7-finalize get` | (none) | Get finalize phase configuration |
| `phase-7-finalize set-step` | `--step --enabled` | Toggle finalize step |
| `phase-7-finalize set-max-iterations` | `--value` | Set finalize max iterations |

### Noun: ci

| Verb | Parameters | Purpose |
|------|------------|---------|
| `get` | (none) | Get full CI config |
| `get-provider` | (none) | Get CI provider and repo URL |
| `get-tools` | (none) | Get authenticated tools list |
| `get-command` | `--name` | Get single CI command by name (ready to execute) |
| `set-provider` | `--provider --repo-url` | Set CI provider |
| `set-tools` | `--tools` | Set authenticated tools (comma-separated) |
| `persist` | `--provider --repo-url [--commands] [--tools] [--git-present]` | Persist full CI config (provider, commands, tools) |

### init

```bash
python3 .plan/execute-script.py plan-marshall:manage-plan-marshall-config:plan-marshall-config \
  init [--force]
```

---

## Data Model

### marshal.json Location

`.plan/marshal.json`

### Structure

The defaults template contains only `system` domain. Technical domains (java, javascript, etc.) are added during project initialization based on detection or manual configuration. Technical domains store only `bundle` reference and `workflow_skill_extensions` -- profiles are loaded at runtime from `extension.py`.

**Example** (Java project after init):

```json
{
  "skill_domains": {
    "system": {
      "defaults": ["plan-marshall:ref-development-standards"],
      "optionals": ["plan-marshall:ref-development-standards"],
      "task_executors": {
        "implementation": "pm-workflow:task-implementation",
        "module_testing": "pm-workflow:task-module_testing",
        "integration_testing": "pm-workflow:task-integration_testing"
      }
    },
    "java": {
      "bundle": "pm-dev-java",
      "workflow_skill_extensions": {
        "triage": "pm-dev-java:ext-triage-java"
      }
    }
  },
  "system": {
    "retention": {
      "logs_days": 1,
      "archived_plans_days": 5,
      "memory_days": 5,
      "temp_on_maintenance": true
    }
  },
  "plan": {
    "phase-1-init": {
      "branch_strategy": "direct"
    },
    "phase-2-refine": {
      "confidence_threshold": 95,
      "compatibility": "breaking"
    },
    "phase-5-execute": {
      "commit_strategy": "per_deliverable"
    },
    "phase-6-verify": {
      "max_iterations": 5,
      "1_quality_check": true,
      "2_build_verify": true,
      "domain_steps": {}
    },
    "phase-7-finalize": {
      "max_iterations": 3,
      "1_commit_push": true,
      "2_create_pr": true,
      "3_automated_review": true,
      "4_sonar_roundtrip": true,
      "5_knowledge_capture": true,
      "6_lessons_capture": true
    }
  }
}
```

---

## Standard Domains

### System Domain

The `system` domain contains task executors and base skills applied to all tasks.

| Field | Purpose |
|-------|---------|
| `defaults` | Base skills loaded for all tasks (`plan-marshall:ref-development-standards`) |
| `optionals` | Optional base skills available for selection |
| `task_executors` | Maps profiles to task executor skills (convention: profile X -> `pm-workflow:task-X`) |

### Technical Domains (Profile Structure)

Technical domains store `bundle` reference and `workflow_skill_extensions` in marshal.json. Profiles are loaded at runtime from `extension.py`.

| Profile | Phase | Purpose |
|---------|-------|---------|
| `core` | all | Skills loaded for all profiles |
| `implementation` | execute | Production code tasks |
| `module_testing` | execute | Unit/module test tasks |
| `integration_testing` | execute | Integration test tasks |
| `quality` | verify | Documentation, verification |

**Available Domains**:

| Domain | Bundle | Extensions |
|--------|--------|------------|
| `java` | `pm-dev-java` | triage |
| `javascript` | `pm-dev-frontend` | triage |
| `plan-marshall-plugin-dev` | `pm-plugin-development` | outline, triage |
| `documentation` | `pm-documents` | outline, triage |

Use `resolve-domain-skills --domain {domain} --profile {profile}` to get aggregated skills.

---

## Scripts

| Script | Notation |
|--------|----------|
| plan-marshall-config | `plan-marshall:manage-plan-marshall-config` |

Script characteristics:
- Uses Python stdlib only (json, argparse, pathlib, xml.etree)
- Outputs TOON to stdout
- Exit code 0 for success, 1 for errors
- Supports `--help` flag

---

## Integration Points

### With plan-marshall Skill
- Called during wizard initialization
- Called from configuration menus

### With Implementation Agents
- `skill-domains get-defaults` provides skills to load
- `skill-domains get-optionals` provides available optionals

### With Cleanup
- `system retention get` provides retention settings

---

## Error Handling

All operations validate prerequisites before proceeding:

```toon
status: error
error: marshal.json not found. Run command /marshall-steward first
```

Standard error conditions:
- `marshal.json not found` - Run `/marshall-steward` first
- `skill_domains not configured` - Run `/marshall-steward` first
- `Unknown domain: {name}` - Domain doesn't exist
