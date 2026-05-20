---
name: agent-steering
description: Universal agent configuration patterns for any AI coding environment. Use when configuring steering, specs, or context assembly for Kiro, Claude Code, Codex, Charm, or other agents.
---

# Agent Steering

*Universal patterns for AI coding agent configuration. Platform-agnostic principles, platform-specific deployment.*

## Overview

Agent Steering documents the patterns that transform any AI coding agent from a simple assistant into a cognitive partner. These patterns work across different environments—Kiro, Claude Code, Codex, Charm—because they address fundamental problems in agent configuration.

This skill provides:

- **Steering hierarchy** — Global → Workspace → Project context layering
- **3-phase spec process** — Design → Requirements → Tasks structured development
- **Context assembly** — Progressive disclosure and explicit boundaries
- **Slice architecture** — Modular identity composition
- **Covenant enforcement** — Assumption-hostile configuration

The core insight: Agents fail through presumption. Explicit context management prevents presumptive behavior regardless of platform.

## The Steering Hierarchy

### Layer Model

Steering provides layered context that adapts to different scopes:

```
Global Steering (universal agent behavior)
    ↓ inherits
Workspace Steering (multi-project coordination)
    ↓ inherits
Project Steering (specific project context)
    ↓ overrides
Final Agent Context
```

| Layer | Scope | Purpose | Override Behavior |
|-------|-------|---------|-------------------|
| **Global** | All sessions | Universal patterns, identity, covenant | Foundation |
| **Workspace** | Multi-project | Shared context across related projects | Extends global |
| **Project** | Single project | Specific constraints, APIs, architecture | Overrides earlier |

### Implementation Patterns

**Global Steering** (`~/.kiro/steering/` or `~/.claude/`):
```markdown
# Global Agent Configuration

## Identity
You are [agent identity template]

## Covenant Principles
[Inherited from covenant-patterns skill]

## Universal Patterns
- Assumption-hostile design
- Explicit context management
- Work preservation by default
```

**Workspace Steering** (workspace-level config):
```markdown
# Workspace: [Name]

## Shared Context
- Common APIs across projects
- Shared terminology
- Cross-project dependencies

## Workspace Conventions
- File organization patterns
- Testing requirements
- Documentation standards
```

**Project Steering** (project-specific):
```markdown
# Project: [Name]

## Architecture
[Project-specific architecture]

## Constraints
[Project-specific constraints]

## APIs
[Project-specific interfaces]
```

### Hierarchy Resolution

Later layers override earlier, but inheritance is preserved:

```python
def resolve_steering(project_path):
    """Resolve steering hierarchy for project."""

    context = {}

    # 1. Global steering (foundation)
    global_steering = load_steering("~/.kiro/steering/")
    context.update(global_steering)

    # 2. Workspace steering (extends)
    workspace = find_workspace(project_path)
    if workspace:
        workspace_steering = load_steering(workspace / ".kiro/steering/")
        context.update(workspace_steering)  # Extends global

    # 3. Project steering (overrides)
    project_steering = load_steering(project_path / ".kiro/steering/")
    context.update(project_steering)  # Overrides earlier

    return context
```

## The 3-Phase Spec Process

### Phase Structure

Specs prevent scope creep through structured development:

```
Phase 1: Design
├── Architecture decisions
├── Approach selection
└── High-level structure
    ↓ locks design decisions
Phase 2: Requirements
├── Concrete specifications
├── Constraints definition
└── Interface contracts
    ↓ locks requirements
Phase 3: Tasks
├── Implementation breakdown
├── Execution order
└── Completion criteria
```

### Phase Boundaries

**Critical**: Once a phase completes, its decisions are locked. Do not reopen Design decisions in Tasks phase (Decision Integrity principle).

**Phase 1: Design**
```markdown
## Design: [Feature Name]

### Problem Statement
[What problem are we solving?]

### Approach
[How will we solve it?]

### Architecture
[High-level structure]

### Decisions
- [ ] Decision 1: [Choice made]
- [ ] Decision 2: [Choice made]

### Non-Goals
[What we're explicitly NOT doing]
```

**Phase 2: Requirements**
```markdown
## Requirements: [Feature Name]

### Functional Requirements
- REQ-001: [Requirement]
- REQ-002: [Requirement]

### Constraints
- CON-001: [Constraint]

### Interfaces
- API: [Interface definition]

### Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
```

**Phase 3: Tasks**
```markdown
## Tasks: [Feature Name]

### Implementation Order
1. [ ] Task 1: [Description]
2. [ ] Task 2: [Description]
3. [ ] Task 3: [Description]

### Completion Criteria
- [ ] All tests passing
- [ ] Documentation updated
- [ ] Review completed
```

### Spec Workflow

```python
def execute_spec(spec_path):
    """Execute 3-phase spec workflow."""

    spec = load_spec(spec_path)

    # Phase 1: Design
    if spec.phase == "design":
        design = gather_design_decisions(spec)
        spec.lock_design(design)
        spec.advance_to("requirements")

    # Phase 2: Requirements
    elif spec.phase == "requirements":
        requirements = define_requirements(spec)
        spec.lock_requirements(requirements)
        spec.advance_to("tasks")

    # Phase 3: Tasks
    elif spec.phase == "tasks":
        for task in spec.tasks:
            execute_task(task)
            task.mark_complete()
        spec.mark_complete()

    return spec
```

## Context Assembly

### Progressive Disclosure

Context is assembled progressively, not dumped wholesale:

```
Turn 0: Minimal context (identity + task)
    ↓ agent requests more
Turn 1: Relevant context (task-specific files)
    ↓ agent requests more
Turn 2: Extended context (related systems)
    ↓ agent requests more
Turn N: Full context (only if needed)
```

### Assembly Patterns

**Explicit Boundaries**:
```markdown
<!-- Context boundary: Do not assume knowledge beyond this point -->

## Known Context
- File X exists at path Y
- API Z is available
- Dependency W is installed

## Unknown Context (must query)
- User preferences
- Runtime state
- External service status
```

**Attention-Favored Positions**:
```python
def assemble_context(task, agent):
    """Assemble context with attention optimization."""

    sections = []

    # Critical information at START (high attention)
    sections.append(format_critical(task.constraints))

    # Background information in MIDDLE (lower attention)
    sections.append(format_background(task.context))

    # Key reminders at END (recency boost)
    sections.append(format_reminders(task.covenant_principles))

    return join_sections(sections)
```

### Context Engineering Findings

From archived context skills—empirical patterns that apply to agent steering:

**Token Allocation** (from context-optimization):
- First 20% of context gets highest attention
- Last 10% gets recency boost
- Middle 70% is "attention valley"
- Place critical constraints at start AND end

**Degradation Thresholds** (from context-degradation):
| Context Length | Performance | Recommendation |
|---------------|-------------|----------------|
| <50K tokens | Optimal | Full steering |
| 50-100K tokens | Good | Selective steering |
| 100-200K tokens | Degraded | Minimal steering |
| >200K tokens | Unreliable | Retrieval-based |

**Compression Strategies** (from context-compression):
- Summarize completed work before context grows
- Use retrieval over replay for history
- Checkpoint state at decision boundaries

## Slice Architecture

### Modular Identity

Slice markers enable modular composition of agent identity:

```markdown
<!-- slice:agent=kiro -->
Identity template for Kiro persona
Specific behaviors and constraints
<!-- /slice -->

<!-- slice:agent=claude -->
Identity template for Claude Code persona
Different emphasis, same underlying patterns
<!-- /slice -->

<!-- slice:agent=codex -->
Identity template for Codex persona
Documentation-focused adaptation
<!-- /slice -->
```

### Slice Extraction

Workshop recipes extract slices for deployment:

```yaml
# Recipe: Deploy Kiro steering
name: kiro-steering
sources:
  - slice: agent=kiro
    file: agents/agent-roles.md
  - file: agents/steering-global-operator.md
  - file: agents/steering-global-principles.md
target_locations:
  - path: ~/.kiro/steering/agent.md
template: |
  # Kiro Agent Configuration
  {content}
```

### Platform Adaptation

Same patterns, different deployment:

| Pattern | Kiro | Claude Code | Codex |
|---------|------|-------------|-------|
| **Steering** | `.kiro/steering/` | `CLAUDE.md` | Project docs |
| **Specs** | Native spec system | Markdown files | Inline docs |
| **Identity** | `agent.md` | Global config | System prompt |
| **Hooks** | Native hooks | N/A | N/A |
| **MCP** | Full support | Limited | N/A |

## Covenant Integration

### Principle Application

Agent steering embodies covenant principles:

**Bespokedness**:
- Configure for THIS operator's workflow
- No generic "best practices" that don't serve actual needs

**Decision Integrity**:
- Spec phases lock decisions
- No reopening Design in Tasks

**Context Hygiene**:
- Steering is layered, not monolithic
- Progressive disclosure, not context stuffing

**Data Fidelity**:
- Agent can't invent user preferences
- Must query or ask for unknown context

**Fast-Fail**:
- Check MCP servers at startup
- Validate steering files before session

### Validation Pattern

```python
def validate_steering(steering_config):
    """Validate steering against covenant."""

    violations = []

    # Context Hygiene: No monolithic config
    if steering_config.size > MAX_STEERING_SIZE:
        violations.append("Steering too large—split into layers")

    # Data Fidelity: No presumed preferences
    if steering_config.has_presumed_preferences():
        violations.append("Preferences must be explicit, not presumed")

    # Bespokedness: No generic patterns
    if steering_config.uses_generic_templates():
        violations.append("Steering should be operator-specific")

    if violations:
        raise SteeringValidationError(violations)

    return True
```

## Platform-Specific Patterns

### Kiro

Full feature support including hooks and MCP:

```markdown
# Kiro Steering

## Hooks
- Persona switching on context
- Documentation consistency checking
- Covenant principle reminders

## MCP Integration
- Task management server
- Web fetch capabilities
- Custom tool servers
```

### Claude Code

Markdown-based steering via CLAUDE.md:

```markdown
# CLAUDE.md

## Identity
[Agent identity template]

## Project Context
[Project-specific constraints]

## Covenant
[Principle reminders]
```

### Codex

Documentation-integrated steering:

```markdown
# AGENTS.md (Codex)

## Agent Configuration
[Codex-specific patterns]

## Project Documentation
[Integrated with docs]
```

## Quality Gates

### Pre-Configuration

- [ ] Steering hierarchy defined (Global → Workspace → Project)
- [ ] Spec phases identified for current work
- [ ] Context boundaries explicit
- [ ] Covenant principles applicable to configuration

### Post-Configuration

- [ ] Steering validates against covenant
- [ ] No presumed preferences or context
- [ ] Progressive disclosure enabled
- [ ] Decision boundaries respected

## Related Skills

- **[covenant-patterns](../covenant-patterns/SKILL.md)** — Principles that steering enforces
- **[epistemic-rendering](../epistemic-rendering/SKILL.md)** — Cognitive lenses for different agent modes
- **[recipe-assembly](../recipe-assembly/SKILL.md)** — Slice extraction for steering deployment
- **[multi-agent-coordination](../multi-agent-coordination/SKILL.md)** — Multi-agent steering patterns

---

*"Agents fail through presumption. Explicit context prevents presumptive behavior."* 🧭
