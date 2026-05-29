---
id: KABSD-TSK-0145
uid: 019ba3ef-3399-7f2e-8314-0f9fa6e244e9
type: Task
title: "Add prerequisite install script for Python deps (self-contained skill)"
state: Done
priority: P1
parent: KABSD-FTR-0003
area: devex
iteration: null
tags: ["bootstrap", "prereqs", "devex"]
created: 2026-01-10
updated: 2026-01-10
owner: null
external:
  azure_id: null
  jira_key: null
links:
  relates: []
  blocks: []
  blocked_by: []
decisions: []
---

# Context

The skill is script-heavy and evolving fast. When Python dependencies are missing, agents currently discover failures late (mid-command) and then waste tokens installing packages ad-hoc. This also reduces reproducibility across machines.

# Goal

Provide a one-shot, stdlib-only bootstrap script that:
- creates a local venv,
- installs the self-contained skill package (editable),
- optionally installs heavier indexing/embedding dependencies.

# Non-Goals

- Do not implement a server runtime.
- Do not require users to maintain a separate `requirements.txt`.
- Do not install anything globally; keep installs within a repo-local venv.

# Approach

- Add `skills/kano-agent-backlog-skill/scripts/dev/install_prereqs.py` (stdlib-only).
- Default behavior: create `.venv/` and install `skills/kano-agent-backlog-skill` with `[dev]` extras.
- Optional flag: `--with-embeddings` to install embedding/FAISS deps (best-effort).
- Document the entrypoint in repo `README.md` and `AGENTS.md`.

# Alternatives

- Let scripts fail and ask the agent to install missing deps (current; wastes tokens).
- Commit a frozen lockfile and require exact sync (too heavy for pre-alpha demo).

# Acceptance Criteria

- A single command exists that creates a venv and installs required deps for the skill scripts.
- The command is documented in `README.md` and `AGENTS.md`.
- The script uses only stdlib so it can run before any dependencies are installed.

# Risks / Dependencies

- Some embedding deps are platform-dependent; keep them optional and best-effort.

# Worklog

2026-01-10 02:05 [agent=codex] Planned: add a one-shot script to create venv and install required Python deps so agents don't waste tokens installing ad-hoc.
2026-01-10 02:11 [agent=codex] Ready: bootstrap script and docs are specified with acceptance criteria.
2026-01-10 02:11 [agent=codex] Done: added stdlib-only install script and documented usage in README.md and AGENTS.md.
