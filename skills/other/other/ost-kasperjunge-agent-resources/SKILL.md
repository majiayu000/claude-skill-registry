---
name: ost
description: Use when running or maintaining an Opportunity Solution Tree (OST) workflow with a lightweight graph store and CLI. Provides a single entry skill that routes to outcome, opportunity, solution, and assumption/experiment phases via progressive disclosure.
---

# OST

Run a full Opportunity Solution Tree workflow from a single skill, backed by a lightweight graph database and CLI.

## Entry Flow (Minimize File Loading)

Goal: Start a session, pick a workspace, and select or create an outcome.

1) Ensure DB exists
- If `.agr/ost.db` is missing, initialize it:
  - `uv run python scripts/ost.py init --path .agr/ost.db`

2) Select workspace
- List workspaces:
  - `uv run python scripts/ost.py workspace list`
- If needed, create one:
  - `uv run python scripts/ost.py workspace create \"<name>\"`

3) Select outcome
- List outcomes:
  - `uv run python scripts/ost.py outcome list --workspace <name>`
- If needed, create one:
  - `uv run python scripts/ost.py outcome add --workspace <name> \"<title>\"`

4) Route to phase (load only the relevant file)
- Outcomes: `references/outcomes.md`
- Opportunities: `references/opportunities.md`
- Solutions: `references/solutions.md`
- Assumptions/Experiments: `references/assumptions.md`

## Data Model + Storage

Use a lightweight graph DB at `.agr/ost.db` with multi-workspace support.
The CLI manages nodes and edges; do not edit DB files manually.

## CLI

Use the CLI to read/write the OST graph. The CLI is expected to live in this skill’s `scripts/` directory and be run via `uv run`.

Commands (intended):
- `uv run python scripts/ost.py init --path .agr/ost.db`
- `uv run python scripts/ost.py workspace list`
- `uv run python scripts/ost.py workspace create "<name>"`
- `uv run python scripts/ost.py outcome list --workspace <name>`
- `uv run python scripts/ost.py outcome add --workspace <name> "<title>"`
- `uv run python scripts/ost.py opportunity add --outcome <id> "<title>"`
- `uv run python scripts/ost.py solution add --opportunity <id> "<title>"`
- `uv run python scripts/ost.py assumption add --solution <id> "<title>"`
- `uv run python scripts/ost.py show --outcome <id>`

If the CLI is not yet implemented, document the intended command and proceed with non-destructive guidance only.

## Output Format

```
## OST Session

### Selected Workspace
- Name: ...

### Selected Outcome
- ID: ...
- Title: ...

### Next Action
- [What the user wants to do next]

### Next Step
- Load the relevant phase reference file
```

## What NOT to Do

- Do NOT edit `.agr/ost.db` directly.
- Do NOT invent node IDs.
- Do NOT run destructive commands without explicit user intent.
