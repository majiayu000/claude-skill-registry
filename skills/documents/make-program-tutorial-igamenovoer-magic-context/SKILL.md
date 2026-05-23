---
name: make-program-tutorial
description: Manual invocation only; use only when the user explicitly requests `make-program-tutorial` by exact name, OR when the user asks to use a skill to create an SDK/API/library tutorial. Create a clear, reproducible, step-by-step tutorial for a specific API/SDK/library (or a set of functions/classes), with runnable examples, expected outputs, and basic troubleshooting.
---

# Make Program Tutorial

## Inputs to Collect (ask if missing)

- Target topic:
  - Library/SDK name (version optional), or
  - The specific functions/classes/modules to cover
- Target audience (beginner vs experienced) and target language/runtime (Python/JS/etc.)
- Execution environment assumptions (OS, GPU/CPU, required services)
- Output directory (default: `<workspace>/tmp/tutorials/<tutorial-name>`; if the user specifies a dir, prefer the user-provided one)
- Any constraints (no network, no secrets, offline-only, time budget, etc.)

## Outputs (what to produce)

Default output directory:

- `<workspace>/tmp/tutorials/<tutorial-name>`

Create the output directory with:

- `tut-<what>.md`
- `scripts/` (end-to-end runnable scripts for this tutorial)
- `inputs/` (small tutorial-specific inputs, if applicable)
- `outputs/` (tutorial-specific outputs, if applicable)

In `tut-<what>.md`, include a YAML front matter block that records the runtime environment at the time the tutorial is created, including the base git commit hash of the workspace/repo.

Always provide end-to-end runnable scripts under `scripts/` and have the tutorial instruct users to run those scripts (instead of embedding long code blocks in the doc).

## Workflow

### 1) Identify the canonical sources

- Determine the authoritative docs/repo for the target API/library.
- Do not pin versions unless the user asks for it.
- If the tutorial is for a set of functions/classes in a local repo, read the source and identify:
  - Import paths, initialization patterns, and required config
  - Any side effects (I/O, network calls, GPU usage)

### 2) Choose a minimal “happy path”

- Define the smallest end-to-end example that demonstrates value:
  - Inputs → processing → outputs
- Prefer real inputs if available; otherwise synthesize minimal inputs that satisfy the API contract.
- Record the exact commands used to run the example and the resulting artifacts.

### 3) Implement end-to-end scripts in `scripts/`

- Create one or more runnable scripts under `scripts/` that demonstrate the full “happy path”.
- Scripts must:
  - Read inputs from `inputs/` (prefer real files; synthesize only if necessary and explain why)
  - Write artifacts to `outputs/`
  - Print a concise success summary (paths written, key shapes/counts)
- Keep scripts as small as practical but runnable; prefer a single `scripts/run.py` unless multiple steps are clearer.

### 4) Write `tut-<what>.md` (tutorial doc)

Choose a short, specific `<what>` (e.g., `tut-httpx-basics.md`, `tut-onnxruntime-infer.md`).

Follow the template in `templates/tut-what.md`:
- Start with a concrete **Question** (“How do I … using …?”).
- Add a **Prerequisites** checklist (do not teach setup in detail; assume prerequisites are already met).
- Add an **Implementation Idea** section with a short, high-level approach.
- Add **Critical Example Code** that is copy/pasteable and heavily commented to explain the usage step-by-step.
- Add **Input and Output** sections documenting the contract and showing representative examples (requests/responses, logs, artifacts).
- Keep code blocks self-contained and small; for the full implementation, point to `scripts/...` and show the exact command(s) to run.
- Add YAML front matter capturing:
  - `created_at` (ISO8601), `tutorial_name`, `topic`
  - `base_commit` (workspace git commit hash)
  - `runtime` (OS, CPU/GPU, Python version, key package versions if relevant)

### 5) Include tutorial inputs/outputs

- Place tutorial-ready inputs under `inputs/`.
- Place tutorial outputs under `outputs/`.
- Keep them minimal and (when relevant) redistributable.

### 6) Add troubleshooting and verification

- Add a short “Troubleshooting” section with the top failure modes:
  - Missing deps, version mismatches, device selection issues, path errors
- Add a “Verification” section:
  - Exactly how to confirm outputs are correct (shapes, counts, sample prints, checksums)

## Guardrails

- Do not include secrets/tokens or require users to paste credentials into the tutorial.
- Avoid “works on my machine” ambiguity: always include the exact commands and expected outputs/paths.
- Prefer stable, minimal dependencies; if multiple installation methods exist, pick one and mention alternatives briefly.
