---
name: agents-md-generator
description: Create or update minimal AGENTS.md files in the repository root and nested module directories using progressive disclosure. Works across heterogeneous projects without assuming any fixed agent folder structure.
compatibility: Filesystem-based coding agents with read/write access. Script execution optional.
metadata:
  author: Stanislav [MADTeacher] Chernyshev
  version: "1.0"
---

# AGENTS.md Generator (Root + Nested, Portable)

## Goal
Maintain small, high-signal AGENTS.md files:

- Root AGENTS.md — purpose of repository, navigation, universal toolchain, canonical commands, links to docs and skills.
- Nested AGENTS.md — module/package purpose, local commands, module references.

Use **progressive disclosure**: keep AGENTS.md concise; push details to docs or skills.

---

## Skill location (agent-specific)
- **Do NOT assume `.agents/` or any fixed directory exists.**
- Skills may live:
  - inside the repository (embedded),
  - or in an external/global skill library (external).
- If referencing local skills, first detect an existing skill root already used by the project.
- If no local skill directory exists — **reference skills by name only (external)**.
- **Never create hidden agent directories** just to store skills.

---

## When to run
Run this skill when:

- AGENTS.md is missing, bloated, contradictory, or outdated.
- A new package/service/module appears.
- Repository structure changes (monorepo growth or split).
- Teams want consistent agent context across diverse stacks.

---

## Workflow (Deterministic)

### 1. Discover repository shape
- Identify repository root (git root if available).
- Detect language/tool markers:
  - `package.json`, `pnpm-workspace.yaml`
  - `go.mod`, `go.work`
  - `pyproject.toml`
  - `Cargo.toml`
  - `pubspec.yaml`
  - `pom.xml`, `build.gradle`
- Locate `docs/`, `README.md`, existing `AGENTS.md`.

---

### 2. Detect module boundaries
Create nested AGENTS.md if directory:

- Contains independent build/package manifest
- OR represents deployable/service unit (`apps/`, `services/`, `packages/`)
- AND differs in stack/toolchain from parent scope

---

### 3. Generate/Update Root AGENTS.md
Constraints:

- Ideal size: ≤ 60 lines
- Must include:
  - One-sentence repository purpose
  - Primary toolchain/package manager
  - Canonical commands (if non-standard)
  - Links to docs
  - Instruction to read nested AGENTS.md when inside modules
  - Optional skill references (adaptive: local or external)

---

### 4. Generate/Update Nested AGENTS.md
Constraints:

- Ideal size: ≤ 40 lines
- Must include:
  - One-sentence module purpose
  - Module-specific commands
  - Local documentation references
  - Optional skill references (adaptive)

---

### 5. Progressive Disclosure Rules
- Do not embed style guides, CI policies, or architecture details.
- Prefer links to:
  - `docs/STYLE_GUIDE.md`
  - `docs/ARCHITECTURE.md`
  - external or local skills
- Avoid “always/never” rules unless critical for correctness/security.

---

### 6. Safety / Correctness Gates
- Never invent commands.
- Infer commands from:
  - package scripts
  - Makefile
  - CI configuration
  - README
- If uncertain → write:
  “Known commands: see <file>”
- Preserve critical warnings (security, secrets, deployment).

---

## Output Contract
Create or update only:

- `<repo_root>/AGENTS.md`
- `<module_dir>/AGENTS.md`

**Do not create agent configuration folders.**

---

## Skill Referencing Strategy

When adding skill references inside AGENTS.md:

1. **If local skill directory detected**
   ```
   See: <detected-skill-root>/<skill-name>/SKILL.md
   ```

2. **If no local directory exists**
   ```
   Skill: agents-md-generator (external)
   ```

Never assume filesystem paths.
