---
name: taskfile-setup
description: >-
  Install Taskfile (task) and scaffold or audit Taskfile.yml configurations with
  ecosystem-aware templates. Auto-detects Node.js/pnpm, JVM/Gradle, Python/uv,
  Docker, and recommends single-file or multi-file (includes) patterns based on
  project complexity. Use when user runs /devtools:taskfile-setup, mentions
  "taskfile setup", "setup task runner", "audit taskfile", "scaffold taskfile",
  "add taskfile", "taskfile.yml", or "developer tasks".
disable-model-invocation: true
---

# Taskfile Setup

Install [Taskfile](https://taskfile.dev/) and scaffold or audit `Taskfile.yml` configurations with ecosystem-aware templates.

## Pre-flight

Run the detection script to understand current state:
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/detect_taskfile.py <project-root>
```

## Decision Flow

```
Run detector
    |
    ├── task_binary.installed = false → Install Task first
    |
    ├── taskfile.exists = true → Phase 1: Audit
    |
    └── taskfile.exists = false → Phase 2: Scaffold
```

## Phase 1: Audit (Existing Taskfile)

1. **Summarize findings** — show a status table:

   | Component | Status | Detail |
   |-----------|--------|--------|
   | task binary | installed/missing | version, path |
   | Taskfile | found/not found | path, variant |
   | Tasks | N tasks | count, has includes |
   | Ecosystems | N detected | list |
   | dotenv | configured/missing | .env files found |

2. **Present audit violations** grouped by severity (ERROR > WARNING > INFO):
   - Show rule ID, message, task name, line number, fix hint
   - Violations include: missing version, no preconditions on deploy tasks, no sources/generates on build tasks, missing desc, too many tasks in single file, no dotenv, hard-coded paths

3. **Use `AskUserQuestion`** (multiSelect: true) — ask which violations to fix

4. **Apply selected fixes** — see [WORKFLOW.md](WORKFLOW.md) for per-rule fix strategies

5. **Re-run detector** to verify fixes were applied

## Phase 2: Scaffold (No Taskfile)

1. **Install `task`** if missing — show commands based on `os` field:
   - **macOS**: `brew install go-task`
   - **Linux**: `sh -c "$(curl --location https://taskfile.dev/install.sh)" -- -d -b ~/.local/bin`
   - Verify: `task --version`

2. **Review detected ecosystems** — show what was found

3. **Choose Taskfile pattern** — use `AskUserQuestion`:
   - **Single-file** (flat namespace with `:` separators) — recommended for < 15 tasks
   - **Multi-file** (root + `taskfiles/` with includes) — recommended for 15+ tasks or monorepos

4. **Choose task groups** — use `AskUserQuestion` (multiSelect: true):

   | Ecosystem | Available Groups |
   |-----------|-----------------|
   | Node.js/pnpm | `dev`, `build`, `test`, `lint`, `format`, `check` |
   | JVM/Gradle | `build`, `test`, `lint`, `check`, `run` |
   | Python/uv | `dev`, `test`, `lint`, `format`, `check` |
   | Docker | `up`, `down`, `logs`, `build`, `clean` |
   | Generic | `setup`, `check`, `clean` |

5. **Generate Taskfile.yml** with selected groups — always include:
   - `version: "3"`
   - `desc:` on every task
   - Top-level `vars:` for directory paths
   - `dotenv:` if `.env` files exist

6. **Verify** — re-run detector, then run `task --list`

## Key Rules

- **Never overwrite** existing Taskfile.yml without asking. Offer merge/replace/skip.
- **Detect first** — skip steps already configured.
- **Use `AskUserQuestion`** for every decision. Do not assume user preferences.
- **Always use `version: "3"`** — the only supported non-deprecated schema.
- **Add `desc:`** to every task for `task --list` discoverability.
- **Wrap ecosystem tools** (pnpm, gradlew, uv) — do not duplicate their logic.
- **Use variables** for directory paths instead of hard-coding.
- **dotenv only in root** — Taskfile does not support dotenv in included files.

## Existing Runner Awareness

The detector reports existing runners (Makefile, justfile, package.json scripts, gradlew). When scaffolding:
- Note which runners exist and what they cover
- Suggest Taskfile as a **unifying layer** that wraps existing tools
- Do not duplicate what existing runners already do well

## References

- **Workflow**: See [WORKFLOW.md](WORKFLOW.md) for detailed per-step flows and templates
- **Examples**: See [EXAMPLES.md](EXAMPLES.md) for example setup and audit sessions
- **Troubleshooting**: See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues
- **Detection Script**: See [scripts/detect_taskfile.py](scripts/detect_taskfile.py) for detection logic
