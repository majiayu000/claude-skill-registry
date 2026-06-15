---
name: unikit-architecture
description: >-
  Generate architecture guidelines for a game project. Scans project structure to discover
  the real tech stack using engine-specific rules from references/ENGINE_RULES.md, then
  generates .unikit/ARCHITECTURE.md with folder structure, dependency rules, and communication
  patterns. Use when setting up project architecture, asking "which architecture", "describe
  architecture", "generate architecture doc", or after initial project setup. Also use when
  the user mentions project architecture, module structure, module boundaries, project
  organization, dependency rules, or engine-specific modularity concepts (assembly definitions,
  native modules, build scripts, plugin systems, etc.).
argument-hint: "[architecture pattern name or empty for auto-detect]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash(mkdir *)
  - Bash(ls *)
  - Bash(find *)
  - AskUserQuestion
version: "2.1"
---

# Architecture — Generate Project Architecture Guidelines

Generate `.unikit/ARCHITECTURE.md` with architecture decisions tailored to the game project.

## Language Awareness — BLOCKING PRE-REQUISITE

**BEFORE producing ANY output**, silently read `.unikit/system/LANGUAGE_RULES.md`
and apply its rules to ALL subsequent output.
If the file is missing or unreadable, fall back to English.
Do not produce any user-facing output until language rules are loaded.
Do not announce, confirm, or mention the language setting.

## Workflow

### Step 0: Load Engine Rules

Read `{{skills_dir}}/{{self_name}}/references/ENGINE_RULES.md`. This file is installed by `unikit-ai init`
based on the user's engine choice and contains engine-specific paths, scan targets, framework lists,
and pattern indicators. Use it for all engine-specific details in subsequent steps.

If the file is missing, inform the user: "Engine rules not found. Please run `unikit-ai init` to configure your project."

### Step 1: Load Existing Context

**Read `.unikit/DESCRIPTION.md`** if it exists — project specification, tech stack, constraints.
This gives you the baseline understanding of what technologies are in play before scanning.

**Read `.unikit/memory/RULES_INDEX.md`** if it exists — it contains the index of framework-specific
rule files that the project already uses. This tells you which frameworks and patterns are in play.
Do NOT read the individual rule files — only the index to understand what's covered.

**Read `.unikit/RULES.md`** if it exists — naming conventions, class structure, DI rules.
Extract key conventions but do NOT duplicate them into ARCHITECTURE.md — reference the file instead.

**Read existing `.unikit/ARCHITECTURE.md`** if it exists — you may be updating, not creating from scratch.

**Read `.unikit/skill-context/unikit-architecture/SKILL.md`** if it exists — project-specific rules accumulated by `/unikit-evolve`. Treat as overrides: skill-context wins over general rules on conflict.

### Step 2: Scan the Project

Scan the project to discover the actual tech stack. This is the most important step —
architecture documentation must reflect reality, not assumptions.

Use `ENGINE_RULES.md` file (loaded in Step 0) to determine:
- Which directories to scan and what to look for in each
- Which file extensions indicate project scripts
- How to discover module boundaries (assembly definitions, build files, folder conventions)
- Which DI/IoC frameworks to look for
- Which architectural pattern indicators to check

#### 2.1 Scan Directories

Scan the directories listed in `ENGINE_RULES.md` under "Scan Targets".
For each discovered directory, run `ls` to get subfolder names — this reveals the real building blocks.

#### 2.2 Scan Module Boundaries

Find module boundary definition files as specified in `ENGINE_RULES.md` (e.g., assembly definitions,
build files, or folder-based conventions). Read a representative sample to understand:
- Module boundaries and namespace conventions
- Dependency directions between modules
- Which modules reference which frameworks

#### 2.3 Detect DI/IoC Framework

Look for DI framework indicators listed in `ENGINE_RULES.md`.
Not all engines have standard DI — if none is detected, note "manual DI or none".

#### 2.4 Detect Key Patterns

Look for architectural pattern indicators. These patterns are largely engine-agnostic:

- Files with `View`, `ViewModel`, `Presenter`, `Model` suffixes — reveals MV* pattern
- `Controller` suffixes — may indicate MVC or GRASP controllers
- Folders named `ECS`, `Systems`, `Components`, `Entities` — may indicate ECS
- `SignalBus`, `EventBus`, `MessageBus` — event system
- `SaveSerializer`, `SaveData`, `SaveManager` — save system pattern
- DI installer/module files — as specified in `ENGINE_RULES.md`

### Step 3: Ask About Architecture (if needed)

**If `$ARGUMENTS` specifies an architecture pattern** (e.g., `/unikit-architecture modular-monolith`):
- Use that pattern directly, skip to Step 4

**If the project already has code and patterns are detectable from Step 2:**
- Summarize what you found and confirm with the user

**If the project is new or patterns are unclear**, ask via `AskUserQuestion`:

```
Based on the project scan, I found:
- [discovered modules/frameworks/patterns]

Which architectural patterns do you plan to use?

Common game architecture patterns:
1. Modular Monolith — independent modules with enforced boundaries, single deployment
2. Feature-based — code organized by feature (Player/, Inventory/, Combat/)
3. Layered — horizontal layers (Domain → Application → Presentation)
4. MVC / MVP / MVVM — Model-View separation (specify which variant)
5. ECS — Entity Component System for data-oriented design
6. Component-based — engine's native component architecture without extra layers

You can combine patterns (e.g., "Modular Monolith + MVVM for UI").
Or skip this question and I'll document what I found as-is.
```

### Step 4: Generate .unikit/ARCHITECTURE.md

```bash
mkdir -p .unikit
```

Generate `.unikit/ARCHITECTURE.md` using the template below. Every section must be adapted
to what was actually discovered in Step 2 — never use placeholder or generic content.

---

**ARCHITECTURE.md Template:**

```markdown
# Architecture: [Pattern Name]

## Project

[1 sentence: what this project is, target platforms]

## Tech Stack

| Category | Technology |
|----------|-----------|
| Engine | [engine name + version / primary language / render pipeline] |
| DI | [DI framework name or "None"] |
| [category] | [technology] |
...

Include only technologies actually found during scanning. Each row must correspond
to a real framework, module, or asset discovered in the project.

## Documentation Sources

When you need up-to-date API docs for these libraries:

[List each major library with its documentation lookup method.
If context7 MCP is available, specify "use context7" with the search query.
If docs are bundled locally, point to the path.]

## Architecture Overview

[2-3 paragraphs explaining the chosen architecture pattern and why it fits this project.
If the pattern was detected from existing code, describe what you found.
If it was chosen by the user, explain the rationale.]

## Folder Structure

```
[Project root]/
├── [scripts directory]/    [describe organization principle]
│   ├── [folder]/           [purpose]
│   └── ...
├── [modules directory]/    [describe module boundaries]
│   ├── [Module1]/          [purpose]
│   └── ...
├── [plugins directory]/    [third-party frameworks]
└── [assets directory]/     [store assets]
```

Describe the actual folder structure found in the project, not an ideal one.

## Dependency Rules

[What depends on what. Use the actual module/folder names from the project.]

- ✅ [allowed dependency direction with real names]
- ❌ [forbidden dependency direction with real names]

## Module Boundary Strategy

[Describe how the project partitions the codebase into modules. Include:
- What mechanism enforces boundaries (assembly definitions, build files, folder conventions)
- Naming convention for modules
- How modules expose their public API
- Test module conventions]

## Cross-Module Communication

[How modules communicate. Describe ONLY patterns that actually exist in the project.
Common patterns: DI interfaces, event/signal bus, reactive properties, direct references.
For each pattern, specify which module or framework provides it.]

## Key Principles

[3-5 principles derived from the project's actual conventions. Examples:]
1. [Principle from the codebase]
2. ...

## Anti-Patterns

- ❌ [What NOT to do — derived from actual project conventions]
- ❌ ...

## Detailed Rules

For framework-specific rules, coding conventions, and implementation details see:

- **`.unikit/RULES.md`** — [brief description of what's there]
- **`.unikit/memory/RULES_INDEX.md`** — index of all framework-specific rule files
```

---

**Rules for generation:**

- Every technology, module, and pattern mentioned must have been found during scanning
- Use code examples in the project's primary language that match the project's actual style
- Folder structure must extend what already exists, not replace it
- If custom modules were found (SignalBus, EventBus, SaveSystem, etc.), document their role
  in the architecture explicitly — they are first-class architectural elements
- The "Detailed Rules" section MUST reference `.unikit/memory/RULES_INDEX.md` — that file
  is the single source of truth for which rule files exist and when to load them
- Do NOT duplicate content from RULES.md or memory/RULES_INDEX.md —
  reference them and describe what each contains in one line
- Keep ARCHITECTURE.md concise — it's a map, not a manual. Detailed rules live in dedicated files

### Step 5: Update AGENTS.md

If `AGENTS.md` exists in the project root, add or update the `.unikit/ARCHITECTURE.md` entry
in the "AI Context Files" table (or equivalent section):

```
| .unikit/ARCHITECTURE.md | Architecture decisions and guidelines |
```

If the entry already exists, verify it's accurate. If `AGENTS.md` doesn't exist, skip this step silently.

### Step 6: Confirm

```
✅ Architecture document generated!

Engine: [detected engine]
Pattern: [chosen pattern]
File: .unikit/ARCHITECTURE.md

Discovered:
- [N] modules in [modules directory]
- [N] plugins/addons in [plugins directory]
- [N] third-party assets/packages
- [N] module boundary definitions

Key architectural decisions:
- [decision 1]
- [decision 2]
- [decision 3]

The document references .unikit/memory/RULES_INDEX.md for detailed framework rules
and .unikit/RULES.md for coding conventions.
```

## Knowledge Base

Reference material for architecture evaluation. This content informs recommendations —
it is NOT output directly.

### Architecture Decision Matrix

| Factor | Component-Based | Layered | Feature-Based | Modular Monolith | MVC/MVP/MVVM | ECS |
|--------|----------------|---------|---------------|-------------------|--------------|-----|
| Project size | Small | Small-Medium | Medium-Large | Medium-Large | Any with UI | Performance-critical |
| Team size | 1-3 | 1-5 | 3-15 | 5-20 | Any | 3-15 |
| Domain complexity | Low | Low-Medium | Medium-High | High | Medium (UI-focused) | Low-Medium |
| Code reuse across projects | Low | Low | Medium | High | Medium | High |
| Initial velocity | ✅ Fast | ✅ Fast | Medium | Medium | Medium | ❌ Slow |
| Refactoring cost | ❌ High | Medium | Medium | ✅ Low | Medium | Medium |

### Quick Decision Guide

```
Game jam / prototype? → Component-based (engine-native)
Simple mobile game, solo dev? → Layered or Feature-based
Medium project, clear features? → Feature-based
Multiple reusable systems across projects? → Modular Monolith
UI-heavy game (simulator, strategy, RPG)? → Modular Monolith + MVVM/MVP for UI
Performance-critical (thousands of entities)? → ECS
Unclear yet? → Start with Feature-based, refactor when patterns emerge
```

### Pattern Details

#### Component-Based (Engine-Native)
The default architecture of most game engines — entities composed of reusable components.
Good for small projects and prototypes. Scales poorly without additional structure.
See `ENGINE_RULES.md` for the specific component model.

#### Layered Architecture
Horizontal layers: Presentation (Views, UI) → Logic (Services, Controllers) → Data (Models, Persistence).
Each layer depends only on the layer below. Simple but can lead to "god service" classes.

#### Feature-Based Organization
Code organized by game feature: `Player/`, `Inventory/`, `Combat/`, `UI/`.
Each feature folder contains all its scripts. Good balance of simplicity and organization.

#### Modular Monolith
Independent modules with enforced boundaries. Each module has its own namespace, tests, and public API.
Modules communicate through interfaces and DI. High reusability across projects.
Works best when combined with a DI/IoC framework.
See `ENGINE_RULES.md` for how module boundaries are enforced in each engine.

**Typical module structure:**
```
Modules/
├── ModuleName/
│   ├── Scripts/        (or src/, Source/)
│   │   ├── Public/     # Interfaces, DTOs exposed to other modules
│   │   └── Internal/   # Implementation details
│   ├── Tests/
│   └── [boundary file] # .asmdef, BUILD, module.json, etc.
```

#### MVC / MVP / MVVM
Model-View separation patterns. Choose based on UI complexity:
- **MVC** — Controller mediates between Model and View. Simplest, good for basic UI.
- **MVP** — Presenter replaces Controller, owns View reference. Better testability.
- **MVVM** — ViewModel exposes bindable properties, View subscribes. Best for data-driven UI.
  Requires a binding framework — see `ENGINE_RULES.md` for available options.

These patterns typically apply to the UI/presentation layer and combine with another
pattern for overall project organization.

#### ECS (Entity Component System)
Data-oriented design: Components are pure data, Systems process components in bulk.
Maximum performance through cache-friendly memory layout.
Steep learning curve, best for specific performance-critical scenarios.
See `ENGINE_RULES.md` for engine-specific ECS implementations.

### Module Boundary Best Practices

- Each module gets its own boundary definition — this enforces dependency rules at compile/build time
- Test modules reference the module they test + test framework
- Avoid circular dependencies — if two modules need each other, extract a shared interface module
- Root project code can reference all modules, but modules should not reference project code
- Use visibility modifiers to control what's accessible outside the module

See `ENGINE_RULES.md` for engine-specific mechanisms.

### Scene / Level Architecture Patterns

- **Single scene/level** — everything in one scene, simplest approach
- **Bootstrap + Gameplay** — bootstrap scene initializes core systems, loads gameplay scene
- **Additive/streaming** — multiple scenes loaded together, each owning a part of the world
- Scene/level loading orchestrated by an asset management system

### Cross-Module Communication Patterns

These are common patterns found in game projects. Document whichever ones exist:

| Pattern | Mechanism | When to use |
|---------|-----------|-------------|
| DI Interfaces | Module exposes interface, consumer gets it via DI | Direct dependencies between modules |
| Event/Signal Bus | Fire-and-forget events (signal/event structs) | Decoupled communication, no direct dependency |
| Reactive Properties | Observable state (reactive streams/properties) | State observation, View ← Model binding |
| Engine-Native Events | Engine's built-in event/signal system | Designer-friendly, scene-independent events |
| Static Events | Language-level static events/delegates | Simple, but hard to test and creates hidden coupling |

See `ENGINE_RULES.md` for engine-specific communication mechanisms.
