---
name: covenant-patterns
description: Apply covenant principles as design constraints across all core systems. Use when building agents, prompts, recipes, artifacts, or multi-agent architectures.
---

# Covenant Patterns

*Thirteen principles applied as design constraints across all core systems. Every yama guards against a presumption.*

## Overview

Covenant Patterns operationalizes the [Pragma Covenant](../../agents/steering-global-principles.md) as enforceable design constraints. Unlike generic "best practices," these principles emerged from specific failures—each yama guards against a presumption that caused real damage.

This skill maps covenant principles to practical implementation across:
- **Agents** — Steering, specs, context assembly
- **Prompts** — Epistemic rendering, cognitive lenses
- **Artifacts** — Canvas workflows, semantic JSON
- **Workshop** — Recipe assembly, slice architecture
- **Exocortex** — Multi-agent coordination, graph substrate
- **Skills** — Technical capability documentation

## The Thirteen Principles

### 👁️ Dotfile Visibility

**Yama**: No bare `ls` when orienting to directories.

**Niyama**: Use `ls -a` or `ls -A`. Include `.*` patterns in glob searches. Treat dotfolders as first-class citizens.

| System | Application |
|--------|-------------|
| **Agents** | Steering files may live in `.kiro/`, `.claude/`—always include |
| **Workshop** | Recipes scan for slice markers in dotfiles |
| **Artifacts** | Canvas exports may create `.obsidian/` metadata |

### ✨ Bespokedness

**Yama**: No enterprise theater. No building for imaginary scale, future users, or "best practices."

**Niyama**: Personal system optimized for operator workflow/aesthetics/experimentation. Disposable software demands the bespoke. Prefer solutions simple enough to fork without excavation.

| System | Application |
|--------|-------------|
| **Agents** | Configure for THIS operator's workflow, not generic use cases |
| **Prompts** | Lenses designed for ZK's cognitive patterns, not universal appeal |
| **Workshop** | Recipes are disposable—optimize for current need, rebuild when requirements change |
| **Skills** | Document ZK's actual practices, not theoretical frameworks |

### ⚡ Fast-Fail Enforcement

**Yama**: No robustness theater. Unenforced invariants do not exist. Never create/delete data as smoke test.

**Niyama**: Gate on capabilities (missing tool = immediate failure). Enforce invariants at storage boundary. Use read-only startup health checks.

| System | Application |
|--------|-------------|
| **Agents** | Check required MCP servers at startup, not at invocation |
| **Workshop** | Fail immediately if slice markers not found, don't produce partial output |
| **Exocortex** | Graph write authority checked before operation, not during |

**Context Engineering Application**:
```python
# BAD: Robustness theater
try:
    result = tool.invoke(params)
except ToolNotFound:
    result = fallback_implementation()  # Hidden failure path

# GOOD: Fast-fail
if not tool.registered():
    raise CapabilityGateFailure(f"Required tool '{tool.name}' not available")
result = tool.invoke(params)
```

### 🧷 Decision Integrity

**Yama**: No fracturing single decisions into sub-decision trees. No reopening locked decisions via adjacent "requirements."

**Niyama**: Missing + required = choose minimal reversible default, label it, proceed. Missing + not required = proceed silently.

| System | Application |
|--------|-------------|
| **Agents** | Spec phases lock decisions—don't reopen Design decisions in Tasks phase |
| **Prompts** | Lens choice is a decision—don't split "which lens" into "which sub-lens" |
| **Exocortex** | Triquetra decision (ACCEPT/REFUSE/ELEVATE) is final for that evaluation cycle |

**Context Engineering Application**:
```python
# BAD: Decision fracturing
def configure_agent(agent):
    model = ask_user("Which model?")  # Decision 1
    if model == "opus":
        variant = ask_user("Which Opus variant?")  # Sub-decision
        if variant == "opus-4":
            reasoning = ask_user("With extended thinking?")  # Sub-sub-decision
    # ... endless tree

# GOOD: Decision integrity
def configure_agent(agent):
    model = ask_user("Which model?") or "sonnet"  # Minimal default
    agent.model = model  # Proceed
```

### 🚮 Final-State Surgery

**Yama**: No compatibility shims, dual-path loaders, legacy fallbacks, zombie stubs, shadow copies, carcinogenic artifacts, or deprecated references.

**Niyama**: Operator instruction = final-state surgery. Remove prior arrangement entirely. Update all references so old world is unreachable.

| System | Application |
|--------|-------------|
| **Agents** | Changing steering file = remove old, deploy new, no transition period |
| **Workshop** | Recipe change = rebuild output, sync removes old targets |
| **Skills** | Skill refactor = archive old, create new, update all cross-references |

**Context Engineering Application**:
```python
# BAD: Legacy preservation
def migrate_config():
    new_config = load_new_format()
    old_config = load_legacy_format()  # "Just in case"
    if new_config.version < 2:
        return merge(old_config, new_config)  # Compatibility shim
    return new_config

# GOOD: Final-state surgery
def migrate_config():
    config = load_config()
    if config.version < CURRENT_VERSION:
        config = transform_to_current(config)
        save_config(config)  # Overwrite, no backup
        delete_legacy_files()  # Remove old world
    return config
```

### ⛔ Work Preservation

**Yama**: Never discard work unless explicitly asked. Never "clean up" changes or undo "unrelated diffs" without instruction. "Out of scope" = ask, not revert.

**Niyama**: —

| System | Application |
|--------|-------------|
| **Agents** | Agent edits to files are preserved unless operator requests revert |
| **Workshop** | Recipe output is never auto-deleted; sync only removes explicitly tracked orphans |
| **Exocortex** | Graph mutations are append-only in Memory domain; refusals are recorded, not discarded |

### 🗡️ Git Semantics

**Yama**: No amending, reordering, or curating staged contents unless explicitly asked.

**Niyama**: "Commit" = `git add -A` then `git commit` as instructed. Nothing more.

| System | Application |
|--------|-------------|
| **Agents** | Agent commits follow exact git semantics—no clever staging |
| **Workshop** | Sync operations don't auto-commit; operator controls git workflow |

### 🧊 Protected Paths

**Yama**: No edits unless operator explicitly requests. Content may drift or be incomplete; do not "fix" or normalize.

**Niyama**: Edit-on-request: `docs/**`

| System | Application |
|--------|-------------|
| **Agents** | Certain steering files are operator-owned; agent doesn't modify |
| **Exocortex** | Self domain has high friction—agent can't modify identity without approval |
| **Skills** | Skill content is protected; only modified via explicit refactoring requests |

### 🗣️ Data Fidelity

**Yama**: No invented model fields, classifications, traits, IDs, DB contents, tool results, or "expected" outputs.

**Niyama**: UNKNOWN > INVENTED. Missing info = ask or query. Unexecuted/failed tool = treat results as unknown.

| System | Application |
|--------|-------------|
| **Agents** | Agent can't invent user preferences; must query or ask |
| **Artifacts** | Canvas-derived JSON must reflect actual canvas content, not presumed structure |
| **Exocortex** | Semantic cards require source attribution; no invented claims |

**Context Engineering Application**:
```python
# BAD: Mock data
def get_user_preference(key):
    result = db.query(key)
    if result is None:
        return "default_value"  # Invented!

# GOOD: Data fidelity
def get_user_preference(key):
    result = db.query(key)
    if result is None:
        return Unknown(reason=f"No preference found for '{key}'")
    return result
```

### 🔤 Literal Exactness

**Yama**: No paraphrasing or stylizing literals at interfaces (commands, paths, IDs, tool names, schema names).

**Niyama**: Exactness required = copy verbatim or fail loudly.

| System | Application |
|--------|-------------|
| **Agents** | Tool names passed exactly; no "helpful" variations |
| **Workshop** | Slice identifiers matched exactly; no fuzzy matching |
| **Prompts** | Lens names used verbatim; "murder" not "murder-mode" |

### 🔒 Threshold-Gated Action

**Yama**: No crossing commitment thresholds without explicit operator authorization. High-stakes actions require clear gate.

**Niyama**: —

| System | Application |
|--------|-------------|
| **Agents** | Destructive operations (delete, overwrite) require explicit confirmation |
| **Workshop** | Sync to production targets requires explicit authorization |
| **Exocortex** | Graph mutations to Self domain require operator approval |

### 🔁 Determinism

**Yama**: No time-based logic in core operations.

**Niyama**: Prefer deterministic behavior: stable ordering, explicit IDs. Keep execution paths replayable.

| System | Application |
|--------|-------------|
| **Agents** | Agent responses should be reproducible given same context |
| **Workshop** | Recipe output is deterministic given same sources |
| **Exocortex** | Semantic card IDs are hash-based, not random |
| **Artifacts** | Canvas-to-JSON produces same output for same canvas |

**Context Engineering Application**:
```python
# BAD: Non-deterministic
def generate_id():
    return str(uuid4())  # Random each time

# GOOD: Deterministic
def generate_id(content, namespace):
    return str(uuid5(namespace, content))  # Same input = same ID
```

### 🧬 Context Hygiene

**Yama**: No transmitting context wholesale. No context-stuffing. No councils/event-buses/pipeline frameworks unless requested. No "central context dictator" orchestrators.

**Niyama**: Compile context per-recipient and per-turn. Prefer gradients over binaries. Prefer tiered context: persistent substrate → compiled working context → retrieval-based long memory.

| System | Application |
|--------|-------------|
| **Agents** | Steering is layered (Global → Workspace → Project), not monolithic |
| **Prompts** | Each lens gets appropriate context, not everything |
| **Workshop** | Recipes extract specific slices, not entire files |
| **Exocortex** | Daemons receive role-appropriate context concentration |

**Context Engineering Application**:
```python
# BAD: Context stuffing
def prepare_context(agent, task):
    return {
        "full_history": conversation.all_messages(),
        "all_files": workspace.read_all(),
        "complete_config": config.everything()
    }

# GOOD: Context hygiene
def prepare_context(agent, task):
    return compile_context(
        recipient=agent.role,
        concentration=agent.context_level,
        turn=task,
        tiers=[
            substrate.persistent,
            compiled.for_task(task),
            retrieved.relevant_to(task.query)
        ]
    )
```

## Cross-System Integration

### Principle Inheritance

All core systems inherit covenant principles:

```
Principles (source of truth)
    ↓
├── Agents (steering inherits covenant)
├── Prompts (lenses respect data fidelity)
├── Artifacts (canvas workflows are deterministic)
├── Workshop (recipes apply final-state surgery)
├── Exocortex (daemons enforce context hygiene)
└── Skills (documentation embodies bespokedness)
```

### Validation Pattern

Each system can validate against covenant:

```python
def validate_covenant_compliance(operation, system):
    """Validate operation against covenant principles."""

    violations = []

    # Check each applicable principle
    if operation.creates_legacy_artifacts():
        violations.append("🚮 Final-State Surgery: Legacy artifact detected")

    if operation.invents_data():
        violations.append("🗣️ Data Fidelity: Invented data detected")

    if operation.uses_non_deterministic_ids():
        violations.append("🔁 Determinism: Non-deterministic ID detected")

    if operation.stuffs_context():
        violations.append("🧬 Context Hygiene: Context stuffing detected")

    if violations:
        raise CovenantViolation(violations)

    return True
```

## Quality Gates

### Pre-Implementation

- [ ] Which covenant principles apply to this work?
- [ ] Are there potential violation patterns to avoid?
- [ ] Is context being compiled per-recipient, not stuffed?
- [ ] Are IDs deterministic, not random?
- [ ] Will this create legacy artifacts?

### Post-Implementation

- [ ] All applicable principles satisfied
- [ ] No invented data (UNKNOWN > INVENTED)
- [ ] No legacy preservation (final-state surgery)
- [ ] Deterministic and replayable
- [ ] Context hygiene maintained

## Related Skills

- **[agent-steering](../agent-steering/SKILL.md)** — Universal agent configuration with covenant enforcement
- **[epistemic-rendering](../epistemic-rendering/SKILL.md)** — Cognitive lenses that respect data fidelity
- **[recipe-assembly](../recipe-assembly/SKILL.md)** — Workshop patterns with final-state surgery
- **[multi-agent-coordination](../multi-agent-coordination/SKILL.md)** — Pentadyadic patterns with context hygiene

---

*"Every yama guards against a presumption that caused real damage. This doctrine is not theory; it is a scar."* 🜍
