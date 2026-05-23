---
name: methodology
scope: partial
description: |
  Manage and guide developers through active development methodology workflows.
  Use when: TDD, BDD, SDD, ATDD, or custom methodology workflows are needed.
  Keywords: methodology, workflow, TDD, BDD, SDD, ATDD, phase, checkpoint, development process.
status: experimental
---

> [!WARNING]
> **Experimental Feature / 實驗性功能**
>
> This feature is under active development and may change significantly in v4.0.
> 此功能正在積極開發中，可能在 v4.0 中有重大變更。

# Methodology System Skill

> **Language**: English | [繁體中文](../../locales/zh-TW/skills/methodology-system/SKILL.md)

**Version**: 2.0.0
**Last Updated**: 2026-01-25

---

## Overview

The Methodology System provides a unified framework for managing development methodologies in projects that adopt Universal Development Standards.

### Two Independent Systems

```
┌────────────────────────────────────────────────────────────────────────────┐
│                  Two Independent Methodology Systems                         │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  System A: SDD (AI-Era Methodology)                                        │
│  ─────────────────────────────────────                                     │
│  /spec → Review → /derive-all → Implementation → Verification              │
│  Best for: New projects, AI-assisted development, greenfield features     │
│                                                                            │
│  System B: Double-Loop TDD (Traditional)                                   │
│  ─────────────────────────────────────                                     │
│  /bdd (Outer Loop) → /tdd (Inner Loop) → Demo                              │
│  Best for: Legacy systems, manual development, established codebases      │
│                                                                            │
│  Optional Input: ATDD Workshop                                             │
│  ─────────────────────────────────────                                     │
│  Stakeholder collaboration that feeds into EITHER system                   │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

### Supported Methodologies

**System A: SDD (Spec-Driven Development)**
- Proposal → Review → Forward Derivation → Implementation → Verification → Archive
- AI-native workflow with spec as authoritative source

**System B: Double-Loop TDD**
- **BDD** (Outer Loop) - Discovery → Formulation → Automation
- **TDD** (Inner Loop) - Red → Green → Refactor

**Optional Input**
- **ATDD** - Acceptance Test-Driven Development workshop (feeds into either system)

**Custom** - User-defined methodologies

---

## Features

### 1. Phase-Aware Guidance

AI automatically tracks the current phase and provides context-appropriate guidance:

```
┌─────────────────────────────────────────────┐
│ 📋 Current Methodology: TDD                  │
│ 📍 Current Phase: 🔴 RED (1-5 min)           │
│                                             │
│ Checklist:                                  │
│   ✅ Test describes behavior                │
│   ✅ Test name is clear                     │
│   ⬜ Test follows AAA pattern               │
│   ⬜ Test fails when run                    │
│                                             │
│ Next: Write the test following AAA pattern  │
└─────────────────────────────────────────────┘
```

### 2. Checkpoint Reminders

Automatic reminders based on methodology triggers:

- **Phase Transition**: Suggest commit when phase completes
- **Accumulation Warning**: Warn when changes exceed threshold
- **Skip Warning**: Alert after consecutive skipped check-ins

### 3. Methodology Switching

Switch between methodologies as project needs change:

```
/methodology switch bdd
```

### 4. Custom Methodology Support

Define team-specific workflows in `.standards/methodologies/`:

```yaml
id: my-team-workflow
name: My Team Workflow
phases:
  - id: plan
    name: Planning
    checklist:
      - id: requirements-clear
        text: Requirements understood
        required: true
```

---

## Commands

| Command | Description |
|---------|-------------|
| `/methodology` | Show current methodology status |
| `/methodology switch <id>` | Switch to different methodology |
| `/methodology phase [phase]` | Show or change current phase |
| `/methodology checklist` | Show current phase checklist |
| `/methodology skip` | Skip current phase (with warning) |
| `/methodology list` | List available methodologies |
| `/methodology create` | Create custom methodology |

---

## Configuration

Methodology configuration is stored in `.standards/manifest.json`:

```json
{
  "methodology": {
    "active": "tdd",
    "available": ["tdd", "bdd", "sdd", "atdd"],
    "config": {
      "tdd": {
        "checkpointsEnabled": true,
        "reminderIntensity": "suggest",
        "skipLimit": 3
      }
    }
  }
}
```

### Configuration Options

| Option | Values | Description |
|--------|--------|-------------|
| `active` | methodology id | Currently active methodology |
| `checkpointsEnabled` | `true`/`false` | Enable checkpoint reminders |
| `reminderIntensity` | `suggest`/`warning`/`strict` | How strongly to enforce checkpoints |
| `skipLimit` | number | Consecutive skips before warning |

---

## AI Behavior

### Detection

1. Check `.standards/manifest.json` for `methodology.active`
2. Load methodology definition from:
   - Built-in: `methodologies/{id}.methodology.yaml`
   - Custom: `.standards/methodologies/{id}.methodology.yaml`

### Phase Tracking

- Track current phase based on trigger conditions
- Update phase when exit conditions are met
- Provide phase-specific guidance and checklist

### Context Keywords

AI will automatically activate methodology context when these keywords are detected:

| System | Methodology | Keywords |
|--------|-------------|----------|
| A: SDD | SDD | specification, spec first, proposal, derive tests, forward derivation |
| B: Double-Loop | BDD (outer) | given when then, gherkin, cucumber, scenario, discovery |
| B: Double-Loop | TDD (inner) | test first, red green refactor, failing test |
| Input | ATDD | acceptance test, user story, product owner, workshop |

---

## Integration with Other Standards

### Check-in Standards

When a phase completes, the methodology system integrates with `checkin-standards.md`:

```
Phase GREEN completed.

Changes:
- Files: 3
- Lines: +45 / -2

Suggested commit:
  test(auth): add login validation test
  feat(auth): implement login validation

[1] Commit now  [2] Continue working  [3] View changes
```

### Code Review

Additional review checks are added based on active methodology:

- **TDD**: Tests follow naming conventions, single behavior per test
- **BDD**: Declarative style, reusable steps
- **SDD**: Change matches spec, no scope creep
- **ATDD**: All acceptance criteria have tests

---

## Related Skills

- [TDD Assistant](../tdd-assistant/SKILL.md) - Detailed TDD guidance
- [Spec-Driven Dev](../spec-driven-dev/SKILL.md) - SDD workflow
- [Code Review Assistant](../code-review-assistant/SKILL.md) - Review integration

---

## Files

- [integrated-flow.md](./integrated-flow.md) - Complete workflow guide for both systems
- [runtime.md](./runtime.md) - AI behavior and runtime guide
- [create-methodology.md](./create-methodology.md) - Custom methodology creation wizard

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.0.0 | 2026-01-25 | Refactor to two independent systems architecture |
| 1.0.0 | 2026-01-12 | Initial methodology system |
