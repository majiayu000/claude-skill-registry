---
name: plan-marshall-config
description: Project-level infrastructure configuration for marshal.json
allowed-tools: Read, Write, Edit, Bash
---

# Plan-Marshall Config Skill

Manages project-level infrastructure configuration in `.plan/marshal.json`.

## What This Skill Provides

- **Skill Domains**: Implementation skill defaults and optionals per domain
- **System Settings**: Retention and cleanup configuration
- **Plan Defaults**: Default values for new plans

## When to Activate This Skill

Activate this skill when:
- Initializing project configuration (`/marshall-steward` wizard)
- Querying implementation skills for a domain
- Managing retention settings
- Configuring plan defaults

---

## Workflow: Initialize Configuration

**Pattern**: Script Automation

Initialize marshal.json with defaults.

```bash
python3 .plan/execute-script.py plan-marshall:plan-marshall-config:plan-marshall-config init
```

---

## Workflow: Query Skill Domains

**Pattern**: Read-Process-Write

Get implementation skills for a specific domain.

### Get Domain Defaults

```bash
python3 .plan/execute-script.py plan-marshall:plan-marshall-config:plan-marshall-config \
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
python3 .plan/execute-script.py plan-marshall:plan-marshall-config:plan-marshall-config \
  skill-domains get-optionals --domain java-implementation
```

### Validate Skill in Domain

```bash
python3 .plan/execute-script.py plan-marshall:plan-marshall-config:plan-marshall-config \
  skill-domains validate --domain java-core --skill pm-dev-java:java-lombok
```

---

## Workflow: System Settings

**Pattern**: Read-Process-Write

Manage system-level infrastructure settings.

### Get Retention Settings

```bash
python3 .plan/execute-script.py plan-marshall:plan-marshall-config:plan-marshall-config \
  system retention get
```

### Set Retention Field

```bash
python3 .plan/execute-script.py plan-marshall:plan-marshall-config:plan-marshall-config \
  system retention set --field logs_days --value 7
```

---

## Workflow: Plan Defaults

**Pattern**: Read-Process-Write

Manage default values for new plans.

### List Plan Defaults

```bash
python3 .plan/execute-script.py plan-marshall:plan-marshall-config:plan-marshall-config \
  plan defaults list
```

### Get Specific Default

```bash
python3 .plan/execute-script.py plan-marshall:plan-marshall-config:plan-marshall-config \
  plan defaults get --field commit_strategy
```

### Set Default Value

```bash
python3 .plan/execute-script.py plan-marshall:plan-marshall-config:plan-marshall-config \
  plan defaults set --field create_pr --value true
```

---

## API Reference

### Noun: skill-domains

| Verb | Parameters | Purpose |
|------|------------|---------|
| `list` | (none) | List all domains |
| `get` | `--domain` | Get full domain config (returns nested structure for technical domains) |
| `get-defaults` | `--domain` | Get default skills (returns `core.defaults` for nested domains) |
| `get-optionals` | `--domain` | Get optional skills (returns `core.optionals` for nested domains) |
| `set` | `--domain [--profile] [--defaults] [--optionals]` | Set domain config (use `--profile` for nested domains) |
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

Standard profiles: `implementation`, `testing`, `quality`.

### resolve-workflow-skill

| Parameters | Purpose |
|------------|---------|
| `--phase` | Resolve system workflow skill for phase (init, outline, plan, execute, finalize) |

Always returns from the `system` domain's `workflow_skills`.

### resolve-workflow-skill-extension

| Parameters | Purpose |
|------------|---------|
| `--domain --type` | Resolve domain-specific workflow extension (types: outline, triage) |

Returns null (not error) if extension doesn't exist for the domain.

### get-workflow-skills

| Parameters | Purpose |
|------------|---------|
| (none) | Get all workflow skills from system domain (5-phase model: init, outline, plan, execute, finalize) |

### Noun: system

| Verb | Parameters | Purpose |
|------|------------|---------|
| `retention get` | (none) | Get all retention settings |
| `retention set` | `--field --value` | Set retention field |

### Noun: plan

| Verb | Parameters | Purpose |
|------|------------|---------|
| `defaults list` | (none) | List all plan defaults |
| `defaults get` | `--field` | Get default value |
| `defaults set` | `--field --value` | Set default value |

### Noun: ci

| Verb | Parameters | Purpose |
|------|------------|---------|
| `get` | (none) | Get full CI config |
| `get-provider` | (none) | Get CI provider and repo URL |
| `get-tools` | (none) | Get authenticated tools list |
| `set-provider` | `--provider --repo-url` | Set CI provider |
| `set-tools` | `--tools` | Set authenticated tools (comma-separated) |

### init

```bash
python3 .plan/execute-script.py plan-marshall:plan-marshall-config:plan-marshall-config \
  init [--force]
```

---

## Data Model

### marshal.json Location

`.plan/marshal.json`

### Structure

The defaults template contains only `system` domain. Technical domains (java, javascript, etc.) are added during project initialization based on detection or manual configuration.

**Example** (Java project after init):

```json
{
  "skill_domains": {
    "system": {
      "defaults": ["plan-marshall:general-development-rules"],
      "optionals": ["plan-marshall:diagnostic-patterns"],
      "workflow_skills": {
        "1-init": "pm-workflow:phase-1-init",
        "2-outline": "pm-workflow:phase-2-outline",
        "3-plan": "pm-workflow:phase-3-plan",
        "4-execute": "pm-workflow:phase-4-execute",
        "5-finalize": "pm-workflow:phase-5-finalize"
      }
    },
    "java": {
      "workflow_skill_extensions": {
        "outline": "pm-dev-java:java-outline-ext",
        "triage": "pm-dev-java:ext-triage-java"
      },
      "core": {
        "defaults": ["pm-dev-java:java-core"],
        "optionals": ["pm-dev-java:java-null-safety", "pm-dev-java:java-lombok"]
      },
      "implementation": {
        "defaults": [],
        "optionals": ["pm-dev-java:java-cdi", "pm-dev-java:java-maintenance"]
      },
      "testing": {
        "defaults": ["pm-dev-java:junit-core"],
        "optionals": ["pm-dev-java:junit-integration"]
      },
      "quality": {
        "defaults": ["pm-dev-java:javadoc"],
        "optionals": []
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
    "defaults": {
      "compatibility": "deprecations",
      "commit_strategy": "phase-specific",
      "create_pr": false,
      "verification_required": true,
      "branch_strategy": "direct"
    }
  }
}
```

---

## Standard Domains

### System Domain

The `system` domain contains workflow skills (5-phase model) and base skills applied to all tasks.

| Field | Purpose |
|-------|---------|
| `defaults` | Base skills loaded for all tasks (`plan-marshall:general-development-rules`) |
| `optionals` | Optional base skills available for selection |
| `workflow_skills` | Maps 5 phases to workflow skill references |

**Workflow Phases**: `init`, `outline`, `plan`, `execute`, `finalize`

### Technical Domains (Profile Structure)

Technical domains use nested structure with `workflow_skill_extensions` and profiles.

| Profile | Phase | Purpose |
|---------|-------|---------|
| `core` | all | Skills loaded for all profiles |
| `implementation` | execute | Production code tasks |
| `testing` | execute | Test code tasks |
| `quality` | finalize | Documentation, verification |

**Available Domains**:

| Domain | Core Defaults | Extensions |
|--------|---------------|------------|
| `java` | `pm-dev-java:java-core` | outline, triage |
| `javascript` | `pm-dev-frontend:cui-javascript` | outline, triage |
| `plan-marshall-plugin-dev` | `pm-plugin-development:plugin-architecture` | triage |

Use `resolve-domain-skills --domain {domain} --profile {profile}` to get aggregated skills.

---

## Scripts

| Script | Notation |
|--------|----------|
| plan-marshall-config | `plan-marshall:plan-marshall-config` |

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
