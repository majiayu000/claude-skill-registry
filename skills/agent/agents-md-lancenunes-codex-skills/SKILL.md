---
name: agents-md
description: Create or update root and nested AGENTS.md files that document scoped conventions, monorepo module maps, cross-domain workflows, and (optionally) per-module feature maps (feature -> paths, entrypoints, tests, docs). Use when the user asks for AGENTS.md, nested agent instructions, or a module/feature map.
---

# AGENTS.md builder

## Goal
Add lightweight, scoped guidance for an AI agent (and humans) by placing AGENTS.md files at key directory boundaries:
- root: cross-domain guidance + a module map (for monorepos)
- nested: tech-specific instructions for each component/module
- optional: feature maps at the module level

Optimize for concise and precise instructions (short bullets, minimal prose). Link to docs for depth.

## Inputs to ask for (if missing)
- Is this a monorepo (multiple independently-built modules) or a single project?
- Repo layout: where backend, frontend, docs, infra live; list the major modules/subprojects.
- Cross-domain workflows to document (e.g., frontend calling backend API, auth flow, shared types, local dev).
- If you want feature maps: top 5-15 user-facing features (names) and which module owns them.
- Any rules about MCP usage to capture in root AGENTS.md (allowed servers/tools, safety constraints).
- Any hard rules (do not touch X, required commands, style rules).

## Where to put AGENTS.md (heuristics)
Create AGENTS.md at:
- repo root (global rules + module map + cross-domain workflows)
- each major component/module root (e.g., `backend/`, `frontend/`, `docs/`, `infra/`)
- any subdirectory that has different conventions, ownership, or high risk (payments, auth, data migrations)

Avoid placing AGENTS.md too deep unless there is a real boundary; too many files become noise.

## Workflow (checklist)
1) Inventory the repo
   - List top-level directories and build files (Gradle/Maven, Node/Next, docs site).
   - Identify the natural "component roots" and any critical submodules.
2) Draft root `AGENTS.md`
   - State global rules only (things that apply everywhere).
   - If monorepo: add a module/subproject map (not a feature map) and links to each nested AGENTS.md.
   - Keep tech-specific instructions out of root; push them into the owning module's AGENTS.md.
   - Docs: do not open/read `docs/` by default; consult only when asked or required.
   - Add cross-domain workflows (how modules connect): frontend <-> backend API, auth/session, contract location (OpenAPI/GraphQL), "run together" local dev.
   - Add cross-repo verification guidance: where to run per module + prereqs; quiet first run; re-run narrowed failures with verbose logs when debugging.
3) Draft nested AGENTS.md per component
   - Put tech-specific instructions in the module that owns them:
     - Backend: how to run, test, migrate DB; key modules and entrypoints.
     - Frontend: how to run, build, test; env vars; key routes/areas.
     - Docs: docs structure, where to add ADRs/runbooks, how to preview/build docs.
4) Build maps (as needed)
   - If monorepo: module map goes in root (use `references/module-map-format.md`).
   - Feature maps should live in the owning module AGENTS.md (use `references/feature-map-format.md`).
5) Verify consistency
   - Ensure guidance does not conflict between parent/child scopes.
   - Keep each AGENTS.md short and actionable; move long detail into docs under `docs/`.

## Templates
Use these templates:
- Root + module AGENTS.md: `references/agents-template.md`
- Module map format: `references/module-map-format.md`
- Feature map table format (per module): `references/feature-map-format.md`
- Suggested `docs/` layout (Spring + Next): `references/docs-structure.md`

## Deliverable
Provide:
- Root `AGENTS.md` (if requested) with module map and cross-domain workflows.
- Nested `AGENTS.md` per component/module with tech-specific guidance.
- Optional feature map tables per module (if requested).
- A list of files created/updated and any open questions.
