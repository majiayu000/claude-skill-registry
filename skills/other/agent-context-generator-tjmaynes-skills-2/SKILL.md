---
name: agent-context-generator
description: Generate project-level AGENTS.md guides that capture conventions, workflows, and required follow-up tasks. Use when a repository needs clear agent onboarding covering structure, tooling, testing, task flow, README expectations, and conventional commit summaries.
license: MIT
allowed-tools: Read Write Edit Bash(ls:*) Bash(git:*) Bash(just:*) Bash(make:*)
metadata:
  generated-at: "2026-01-10T00:00:00Z"
  group: "enablement"
  category: "documentation"
  difficulty: "intermediate"
  step-count: "4"
---

# Agent Context Generator

## What You'll Do
- 🔍 Inventory the repository's structure, capture a `.gitignore`-aware `tree` output, and record automation entry points (preferring `just`/`make` tasks when available)
- 🧭 Capture coding conventions, directory ownership, testing expectations, and review workflows so future agents can navigate confidently
- 🧩 Produce an `AGENTS.md` file following the opinionated section order below, honoring scope rules for nested directories
- ✅ Embed universal wrap-up tasks: ensure the README is updated after significant code changes and summarize changes per conventional commits while resolving any open questions with the developer

---

## Phase 1 · Understand the Repository
1. **Check for existing AGENTS.md**
   - Use `find` alternative (`glob` or repo tree) to discover current files. Determine scope inheritance so you can update or extend instead of duplicating.
2. **Read Core Docs**
   - Skim `README.md`, `CONTRIBUTING.md`, and other onboarding docs for project philosophy, setup, and workflows.
   - If `docs/` or `documentation/` exists, scan for architectural or process references worth surfacing.
3. **Survey Project Layout**
   - Note primary directories, languages, build targets, and ownership (e.g., "`src/ui` maintained by Frontend team").
   - Check for `plans/`, `docs/`, or other knowledge directories. Flag must-read files (ADR indexes, architecture overviews, runbooks) to reference later in AGENTS.md.
4. **Build a Git-aware Tree**
   - Use the `tree` command with the `--gitignore` flag (tree ≥ 2.0) so ignored paths stay hidden: `tree --gitignore -a -L 3 > tmp/tree.txt`.
   - If your `tree` build lacks `--gitignore`, run `tree -a -L 3 --prune` and manually prune any ignored directories noted in `.gitignore`, or install an updated version via your package manager.
   - Capture or trim the output before placing it in AGENTS.md (focus on the top 2–3 levels, and note when you omitted details for brevity).
5. **Identify Automation Runners**
   - If `Justfile` exists, run `just --list` (or `just --list --unsorted` for extra notes).
   - If `Makefile` exists (and `just` does not), run `make help` or inspect phony targets for canonical tasks.
   - Record which commands are recommended for linting, testing, building, syncing data, etc. Link the definitive task names you surface in your notes for inclusion later.
6. **Catalog Tooling & Environment**
   - List required runtimes, package managers, env vars, secrets handling, and local services.
   - Note down any `.env.example`, `config/`, or secrets documentation that agents must review.
7. **Clarify Testing & Quality Gates**
   - Identify test suites, coverage expectations, linting, formatting, and CI workflows.
8. **Resolve Ambiguities Early**
   - Whenever conventions, ownership, or workflows seem unclear, prompt the developer with focused questions before drafting the guide.
   - Ask explicitly whether existing `plans/` or documentation directories are authoritative or stale, and clarify what canon to reference.

> **Outcome:** A structured notes list describing layout, tooling, commands, testing, release process, documentation references, pending questions, and update expectations.

---

## Phase 2 · Plan the AGENTS.md Structure
Follow this opinionated order to keep files consistent and scannable:

1. **Header** — Title + short purpose statement.
2. **Quick Facts** — Table or bullet summary (languages, package manager, key scripts, CI).
3. **Repository Tour** — High-level directory map with responsibilities and ownership hints.
4. **Tooling & Setup** — Required runtimes, package managers, environment variables, secrets.
5. **Common Tasks** — Lint/test/build/deploy commands. Prefer listing `just` recipes first, then `make` targets, then raw commands.
6. **Testing & Quality** — When and how to run tests, linting, formatting, coverage, and CI expectations.
7. **Workflow Expectations** — Branching model, review norms, feature flagging, deployment cadence.
8. **Documentation Duties** — When to update `README.md`, architecture diagrams, or other docs.
9. **Finish the Task** — Mandatory wrap-up checklist for every agent task.

For deeper directories (e.g., `services/api/`), include a "Scope" note at the top clarifying inheritance from parent AGENTS instructions. Always confirm with the developer before drafting new per-directory AGENTS files so you do not duplicate existing guidance or create unnecessary overhead.

---

## Phase 3 · Compose AGENTS.md
Use the template below and adapt each section to the project:

```markdown
# Project Agent Guide

> Scope: Root project (applies to all subdirectories unless overridden)

## Quick Facts
- **Primary language:**
- **Package manager:**
- **Entrypoints:**
- **CI/CD:**

## Repository Tour
- `path/` — description & owner

## Tooling & Setup
- Install instructions (per OS)
- Required environment variables (with purpose)
- Secrets management notes

## Common Tasks
- `just <task>` — what it does (preferred)
- `make <target>` — what it does
- Raw command fallback when automation missing

## Testing & Quality Gates
- Unit/integration test commands
- Lint/format commands
- Coverage expectations & thresholds
- CI status command or dashboard link

## Workflow Expectations
- Branch naming and review rules
- Feature toggles or release cadence
- Any approval or ticket linkage requirements

## Documentation Duties
- Update `README.md` when features, setup steps, or developer ergonomics change materially
- List other docs to refresh (architecture, ADRs, etc.)

## Finish the Task Checklist
- [ ] Update relevant docs (& `README.md` if significant changes landed)
- [ ] Summarize changes in conventional commit format (e.g., `feat: ...`, `fix: ...`)
```

### Subdirectory Template (Use Only with Developer Approval)
```markdown
# <Directory Name> Agent Guide

> Scope: ./path/to/directory (inherits root AGENTS.md unless noted)

## Purpose
- What lives here
- Who owns it (team/contact)

## Key Files
- `file_or_folder/` — why it matters

## Common Tasks
- `just <task>` / `make <target>` / command snippets scoped to this directory

## Testing & Quality
- Specific tests, linters, or data fixtures for this directory

## Hand-off Notes
- Docs or runbooks to reference
- Open questions captured during discovery
```
Only create these per-directory guides after confirming with the developer which areas need dedicated context and what information should be emphasized.

**Writing Notes:**
- Keep language direct and actionable. Agents should follow commands verbatim.
- Mention the preferred order of operations (e.g., "Always run `just format` before opening a PR").
- When referencing scripts, include relative paths so agents can jump quickly (e.g., ``scripts/bootstrap.sh``).
- Incorporate a trimmed `tree --gitignore` snapshot (or link to the saved artifact) so readers grasp layout quickly.
- In the Repository Tour, highlight where `plans/`, `docs/`, design docs, or ADRs live if present.
- Call out any unanswered questions as action items, and confirm with the developer before creating any per-directory AGENTS overlays.
- If the project mixes languages/platforms, add subsections per component but keep global guidance first.

---

## Phase 4 · Validate & Wrap Up
1. **Self-review**
   - Does the file respect AGENTS scope rules? (Mention inheritance or overrides.)
   - Are all critical commands documented, especially automation entry points?
   - Is the README update expectation explicit?
   - Did you obtain developer approval before adding any per-directory AGENTS files, and is that approval reflected in the write-up?
   - Does the "Finish the Task" checklist include the conventional commit summary reminder?
2. **Formatting**
   - Ensure headings use Title Case, commands are wrapped in backticks, and lists are concise.
   - Keep sections under ~8 bullets unless a table is clearer.
3. **Handoff Summary**
   - When delivering the AGENTS.md to the user, include:
     - A short summary of major sections added/updated.
     - Confirmation that README and conventional commit reminders are present.
     - Any follow-up suggestions (e.g., missing tests or outdated scripts).

Use this skill whenever a repo lacks AGENTS context or when existing instructions are incomplete or outdated. The goal is to leave future agents with a single, trustworthy map of the project, its tooling, and the expectations for finishing tasks responsibly.
