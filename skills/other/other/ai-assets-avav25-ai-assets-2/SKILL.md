---
name: ai-assets
description: Create, modify, validate, and analyze Codex AI assets such as AGENTS.md files, Codex skills, templates, and supporting scripts. Use when building or maintaining the repository's Codex-specific AI component package.
---

# AI Assets

Build and maintain Codex-native AI assets for this repository. Treat every asset as prompt surface for ChatGPT Codex.

## 1. Determine Scope

Identify:

- Operation: `create` | `modify` | `validate` | `analyze`
- Asset type: `agents-md` | `skill` | `template` | `checklist` | `script`
- Target path or asset name

If the request is ambiguous, resolve it from repository context before asking the user.

## 2. Gather Context

Read only the assets needed for the task:

1. The target asset, if it exists
2. Root `AGENTS.md`
3. Relevant scoped `AGENTS.md` files
4. Relevant `.agents/skills/*/SKILL.md` files
5. Relevant files under `.codex/`
6. `context-engineering` skill when the asset affects prompt layering, memory, RAG, or orchestration

## 3. Build a Dependency Map

Map outgoing and incoming references.

Check for:

- References to `AGENTS.md`
- References to `.agents/skills/<name>/`
- References to `.codex/templates/`, `.codex/checklists/`, or explicit support scripts
- Missing files
- Orphaned assets
- Circular references that add confusion

For `analyze`, stop after presenting the dependency map.

## 4. Choose the Right Codex Primitive

Use the smallest asset that matches the job:

- Repository or directory policy -> `AGENTS.md`
- Reusable task workflow or knowledge -> `.agents/skills/<name>/SKILL.md`
- Reusable authoring scaffold -> `.codex/templates/`
- Validation procedure -> `.codex/checklists/` or `.agents/skills/.../*.md`
- Repeatable local automation -> explicit support scripts owned by the target package

Do not recreate Claude-specific primitives such as agent files, Claude settings, or Claude hook configs.

## 5. Authoring Rules

### `AGENTS.md`

- Put hard constraints first
- Keep project facts concrete and current
- Keep global policy in the root file and local conventions in scoped files
- Avoid repeating parent guidance verbatim

### `SKILL.md`

- Include `name` and a specific `description`
- Optimize `description` for correct progressive disclosure
- Keep the workflow executable with minimal ambiguity
- Move bulky references and checklists into companion markdown files

### Templates and Checklists

- Prefer short, reusable structures
- Separate policy from examples
- Make completion criteria explicit

### Scripts

- Keep scripts visible and optional
- Never hide critical behavior behind implicit automation
- Prefer PowerShell for this repository's local automation

## 6. Prompt Engineering Review

Review the asset as live Codex context:

1. What part of Codex behavior does it shape?
2. What failure mode does it prevent or enable?
3. Is the instruction hierarchy clear?
4. Is critical information front-loaded?
5. Is the token cost justified?

Use `review-checklist.md` for the full validation pass.

## 7. Validate

Run these checks on every create or modify operation:

- Asset uses Codex-native concepts only
- References resolve
- No machine-specific paths unless intentionally local documentation
- No secrets or credentials
- English only
- `SKILL.md` remains concise enough for progressive disclosure
- `AGENTS.md` guidance is specific, not generic

If the asset changes the Codex package structure, update the package README or mapping docs.

## 8. Finalize

Report:

- What changed
- Dependency status
- Validation result
- Remaining follow-up items
