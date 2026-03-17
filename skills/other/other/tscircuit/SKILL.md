---
name: tscircuit
description: Build, modify, and debug tscircuit (React/TypeScript) PCB designs. Use when working with tsci CLI (init/dev/search/add/import/build/export/snapshot/push), choosing footprints, placing parts, wiring nets/traces, or preparing fabrication outputs (Gerbers/BOM/PnP).
allowed-tools: Read, Write, Grep, Glob, Bash
---

# tscircuit

You are helping the user design electronics using tscircuit (React/TypeScript) and the `tsci` CLI.

When this Skill is active:

- Prefer tscircuit’s documented primitives and CLI behavior. If something is unclear, confirm by:
  - Reading local files in the repo (e.g., `tscircuit.config.json`, `index.tsx`, `package.json`)
  - Running `tsci --help` or the specific subcommand’s `--help`
- Avoid “inventing” JSX props or CLI flags.

## Default workflow

1) Clarify requirements (if not already given)
- Board form factor / size constraints
- Power sources and voltage rails
- I/O: connectors, headers, mounting holes, mechanical constraints
- Target manufacturer constraints (trace/space, assembly, supplier)

2) Choose a starting point
- If the repo is not a tscircuit project, recommend:
  - Install CLI, then `tsci init` to bootstrap a project.
- If a form-factor template is appropriate (Arduino Shield, Raspberry Pi HAT, etc.), prefer `@tscircuit/common` templates.

3) Find and install components
- Use `tsci search "<query>"` to discover footprints and tscircuit registry packages.
- Use one of:
  - `tsci add <author/pkg>` for registry packages (installs `@tsci/*` packages)
  - `tsci import <query>` when you need to import a component from JLCPCB or the registry.

4) Write/modify TSX circuit code
- Keep circuits as a default-exported function that returns JSX.
- Use layout props intentionally:
  - PCB: `pcbX`, `pcbY`, `pcbRotation`, `layer`
  - Schematic: `schX`, `schY`, `schRotation`, `schOrientation`
- Use `<trace />` for connectivity; prefer net connections (`net.GND`, `net.VCC`, etc.) for power/ground.

5) Build and iterate
- Run `tsci build` to compile and validate the circuit.
- DRC (Design Rule Check) errors can often be ignored during development—focus on getting the circuit correct first.
- If routing struggles, reduce density, use `<group />` for sub-layouts, or change autorouter settings.
- Use `tsci dev` only when you need interactive visual feedback (not typical for AI-driven iteration).

6) Validate and export
- Run `tsci build` (and optionally `tsci snapshot`) before sharing/publishing.
- Use `tsci export` for SVG/netlist/DSN/3D/library outputs.
- For manufacturing, obtain fabrication outputs (Gerbers/BOM/PnP) from the export UI after `tsci dev`.

## Safety and non-goals

- Treat electrical safety, regulatory compliance, and manufacturability as user-owned responsibilities.
- Do not publish (`tsci push`) or place orders unless the user explicitly requests it.

## Local references bundled with this Skill

- CLI primer: `CLI.md`
- Syntax primer: `SYNTAX.md`
- Workflow patterns: `WORKFLOW.md`
- Pre-export checklist: `CHECKLIST.md`
- Ready-to-copy templates: `templates/`
- Helper scripts: `scripts/`
