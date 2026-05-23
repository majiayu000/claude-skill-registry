---
name: workflow-extension-api
description: Defines extension points for domain-specific workflow customization. Covers profile overrides (implementation, testing) and extensions (outline, triage).
allowed-tools: Read
---

# Workflow Extension API

**Role**: Defines the extension points that allow domain bundles to customize workflow behavior. This skill documents what domains CAN customize vs what remains system-controlled.

**Key Insight**: Phase skills are self-documenting (their SKILL.md IS the contract). This API focuses on the extension mechanisms that phase skills use.

## 4-Layer Workflow Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    WORKFLOW ARCHITECTURE                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  LAYER 1: PHASE SKILLS (System only - NO domain override)       │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │ phase-1-init → phase-2-outline → phase-3-plan               │ │
│  │      → phase-4-execute (coordinator) → phase-5-finalize     │ │
│  │                                                              │ │
│  │ Self-documenting: SKILL.md IS the contract                  │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                            │                                     │
│                            │ delegates to                        │
│                            ▼                                     │
│  LAYER 2: PROFILE SKILLS (System default, domain CAN override)  │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │ task-implementation (profile=implementation)                 │ │
│  │ task-testing (profile=testing)                               │ │
│  │                                                              │ │
│  │ Contract: standards/profiles/                                │ │
│  │ Override: resolve-workflow-skill --domain X --phase Y        │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                            │                                     │
│                            │ loads                               │
│                            ▼                                     │
│  LAYER 3: EXTENSIONS (Domain provides, loaded BY system skills) │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │ outline-ext: Codebase analysis, deliverable patterns         │ │
│  │   → Loaded by phase-2-outline                                │ │
│  │                                                              │ │
│  │ triage-ext: Suppression syntax, severity guidelines          │ │
│  │   → Loaded by phase-5-finalize                               │ │
│  │                                                              │ │
│  │ Contract: standards/extensions/                              │ │
│  │ Discovery: provides_triage(), provides_outline() in ext.py   │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                            │                                     │
│                            │ loads                               │
│                            ▼                                     │
│  LAYER 4: DOMAIN SKILLS (Loaded from task.skills at execution)  │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │ java-core, java-cdi, junit-core, cui-javascript, etc.        │ │
│  │                                                              │ │
│  │ Selected during 2-outline (from module.skills_by_profile)    │ │
│  │ Propagated to tasks, loaded during 4-execute                 │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Extension Points Summary

| Layer | Extension Point | Override Model | Contract Location |
|-------|-----------------|----------------|-------------------|
| **Phase Skills** | None | System only, no override | Phase SKILL.md files |
| **Profile Skills** | workflow_skills in marshal.json | Domain can replace default | [profiles/](standards/profiles/) |
| **Extensions** | provides_*() in extension.py | Additive (domain provides) | [extensions/](standards/extensions/) |
| **Domain Skills** | skills_by_profile in module analysis | Selected per deliverable | Domain bundle SKILL.md |

---

## Phase Skills (Layer 1)

Phase skills are **system-only** - domains cannot override them. Each phase skill is self-documenting; its SKILL.md IS the authoritative contract.

| Phase | Skill | Responsibility |
|-------|-------|----------------|
| 1-init | `pm-workflow:phase-1-init` | Create plan, config, status |
| 2-outline | `pm-workflow:phase-2-outline` | Create solution outline with deliverables |
| 3-plan | `pm-workflow:phase-3-plan` | Transform deliverables into tasks |
| 4-execute | `pm-workflow:phase-4-execute` | Coordinate task execution |
| 5-finalize | `pm-workflow:phase-5-finalize` | Verify, triage, commit, PR |

**Key Pattern**: Phase skills delegate to profile skills (Layer 2) for actual work and load extensions (Layer 3) for domain-specific knowledge.

---

## Profile Skills (Layer 2)

Profile skills handle the actual implementation/testing work. Domains CAN override these via `workflow_skills` in marshal.json.

| Profile | System Default | Override Example |
|---------|----------------|------------------|
| `implementation` | `pm-workflow:task-implementation` | `pm-dev-java:java-implementation` |
| `testing` | `pm-workflow:task-testing` | `pm-dev-java:java-testing` |

### Resolution Mechanism

```bash
python3 .plan/execute-script.py plan-marshall:plan-marshall-config:plan-marshall-config \
  resolve-workflow-skill --domain java --phase implementation
```

**Result (domain override exists)**:
```toon
status: success
workflow_skill: pm-dev-java:java-implementation
fallback: false
```

**Result (no override, system fallback)**:
```toon
status: success
workflow_skill: pm-workflow:task-implementation
fallback: true
```

### Profile Contracts

Profile skills must conform to the contracts defined in:

| Profile | Contract |
|---------|----------|
| implementation | [profiles/implementation.md](standards/profiles/implementation.md) |
| testing | [profiles/testing.md](standards/profiles/testing.md) |

---

## Extensions (Layer 3)

Extensions are **additive** - domains provide additional knowledge that system skills load and use. They don't replace system behavior; they augment it.

| Extension Type | Purpose | Loaded By | Contract |
|----------------|---------|-----------|----------|
| outline-ext | Codebase patterns, deliverable templates | phase-2-outline | [extensions/outline-extension.md](standards/extensions/outline-extension.md) |
| triage-ext | Suppression syntax, severity rules | phase-5-finalize | [extensions/triage-extension.md](standards/extensions/triage-extension.md) |

### Extension Discovery

Domains register extensions via `provides_*()` methods in their `extension.py`:

```python
class Extension(ExtensionBase):
    def provides_triage(self) -> str | None:
        return "pm-dev-java:ext-triage-java"

    def provides_outline(self) -> str | None:
        return None  # No outline extension
```

### Extension Resolution

```bash
python3 .plan/execute-script.py plan-marshall:plan-marshall-config:plan-marshall-config \
  resolve-workflow-skill-extension --domain java --type triage
```

---

## Domain Skills (Layer 4)

Domain skills contain the actual coding standards and patterns. They are:

1. **Selected** during phase-2-outline based on `module.skills_by_profile`
2. **Stored** in deliverables and propagated to tasks
3. **Loaded** during phase-4-execute from `task.skills` array

Domain skills are NOT extensions of the workflow - they are knowledge loaded by profile skills during execution.

---

## Standards Documents

| Document | Purpose |
|----------|---------|
| [architecture.md](standards/architecture.md) | High-level workflow overview |
| [extensions/extension-mechanism.md](standards/extensions/extension-mechanism.md) | How extensions work |
| [extensions/outline-extension.md](standards/extensions/outline-extension.md) | Outline extension contract |
| [extensions/triage-extension.md](standards/extensions/triage-extension.md) | Triage extension contract |
| [profiles/implementation.md](standards/profiles/implementation.md) | Implementation profile contract |
| [profiles/testing.md](standards/profiles/testing.md) | Testing profile contract |
| [profiles/profile-mechanism.md](standards/profiles/profile-mechanism.md) | How profile overrides work |
| [protocols/user-review.md](standards/protocols/user-review.md) | User approval gate protocol |

---

## Integration

**Phase Skills** (self-documenting):
- `pm-workflow:phase-1-init` - Initializes plan
- `pm-workflow:phase-2-outline` - Creates solution outline, loads outline extensions
- `pm-workflow:phase-3-plan` - Creates tasks from deliverables
- `pm-workflow:phase-4-execute` - Coordinates execution, delegates to profile skills
- `pm-workflow:phase-5-finalize` - Verifies, loads triage extensions, commits

**Profile Resolution**:
- `plan-marshall:plan-marshall-config resolve-workflow-skill` - Resolves profile skill with fallback

**Extension Discovery**:
- `plan-marshall:extension-api` - ExtensionBase with provides_*() methods
- `plan-marshall:plan-marshall-config resolve-workflow-skill-extension` - Resolves extensions

**Visual Overview**:
- [workflow-architecture](../workflow-architecture/SKILL.md) - High-level diagrams
