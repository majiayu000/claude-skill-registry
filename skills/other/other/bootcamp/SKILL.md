---
name: bootcamp
description: Guided onboarding walkthrough for new Embry OS users via Embry Lawson persona
triggers:
  - "bootcamp"
  - "onboarding"
  - "getting started"
allowed-tools:
  - Bash
provides:
  - bootcamp
composes:
  - service-status
  - data-audit
  - task-monitor
---

# Bootcamp

Guided onboarding for new Embry OS users, delivered through the Embry Lawson
persona.  The walkthrough adapts to the user's role and composes existing skills
(`/service-status`, `/data-audit`) so every step touches real system state.

## Usage

```bash
# Full onboarding for a manufacturing-floor operator
./run.sh start --role operator

# Compliance officer track
./run.sh start --role compliance-officer

# Developer track
./run.sh start --role developer

# Preview the onboarding script without executing anything
./run.sh start --role developer --dry-run

# Resume from where you left off
./run.sh resume
```

## Roles

| Role                 | Focus                                                                 |
|----------------------|-----------------------------------------------------------------------|
| `operator`           | Manufacturing floor workflows, sensor monitoring, voice commands      |
| `compliance-officer` | OSCAL export, audit timeline, compliance drift detection              |
| `developer`          | Skill creation, daemon architecture, testing                          |

## Steps

Every track follows the same five-step structure:

1. **Welcome** -- introduce Embry OS and the user's role context
2. **Health Check** -- verify daemon health via `/service-status`
3. **Data Overview** -- assess data completeness via `/data-audit`
4. **First Query** -- walk through a role-appropriate first query
5. **Compliance Baseline** -- show current compliance posture

Progress is saved to `~/.embry/bootcamp_state.json` so you can `resume` at any
time.
