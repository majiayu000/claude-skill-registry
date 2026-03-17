---
name: nx-tools
type: complex
depth: base
user-invocable: false
description: >-
  Queries Nx monorepo metadata via Python CLI: workspace projects, affected detection, dependency graphs, project.json configs, generator schemas. Use when analyzing monorepo structure, optimizing CI via affected projects, or inspecting workspace topology.
---

# [H1][NX-TOOLS]
>**Dictum:** *Uniform interfaces eliminate invocation ambiguity.*

<br>

Query Nx workspace with unified Python CLI. Wraps `pnpm exec nx` commands.

[IMPORTANT] Nx 22 features: Terminal UI, continuous tasks, pnpm catalog support, AI agent configuration, Vitest 4 atomizer. All commands run with `NX_DAEMON=false` for deterministic output.

---
## [1][COMMANDS]

| [CMD]      | [ARGS]        | [PURPOSE]                              |
| ---------- | ------------- | -------------------------------------- |
| workspace  | --            | List all projects                      |
| path       | --            | Get workspace root path                |
| generators | --            | List available generators              |
| project    | `<name>`      | View project configuration             |
| run        | `<target>`    | Run target across projects             |
| schema     | `<generator>` | View generator schema                  |
| affected   | `[base]`      | List affected projects (default: main) |
| graph      | `[output]`    | Generate dependency graph              |
| tokens     | `[path]`      | Count tokens in file/directory         |
| docs       | `[topic]`     | View Nx command documentation          |

---
## [2][USAGE]

```bash
# Zero-arg commands
uv run .claude/skills/nx-tools/scripts/nx.py workspace
uv run .claude/skills/nx-tools/scripts/nx.py path
uv run .claude/skills/nx-tools/scripts/nx.py generators

# Required-arg commands
uv run .claude/skills/nx-tools/scripts/nx.py project @parametric-portal/types
uv run .claude/skills/nx-tools/scripts/nx.py run build
uv run .claude/skills/nx-tools/scripts/nx.py run typecheck
uv run .claude/skills/nx-tools/scripts/nx.py schema @nx/react:component

# Optional-arg commands (defaults shown)
uv run .claude/skills/nx-tools/scripts/nx.py affected            # base=main
uv run .claude/skills/nx-tools/scripts/nx.py affected HEAD~5
uv run .claude/skills/nx-tools/scripts/nx.py graph               # output=.nx/graph.json
uv run .claude/skills/nx-tools/scripts/nx.py graph custom.json
uv run .claude/skills/nx-tools/scripts/nx.py tokens              # path=.
uv run .claude/skills/nx-tools/scripts/nx.py tokens CLAUDE.md
uv run .claude/skills/nx-tools/scripts/nx.py docs                # topic=general
uv run .claude/skills/nx-tools/scripts/nx.py docs affected
```

---
## [3][ARGUMENTS]

**workspace**: (no arguments)
- Returns list of all project names in workspace

**path**: (no arguments)
- Returns workspace root path from `CLAUDE_PROJECT_DIR` or `cwd`

**generators**: (no arguments)
- Returns list of available Nx generators (plugins + local)

**project**: `<name>`
- `name` — Project name (required, e.g., `@parametric-portal/types`)
- Returns full project.json configuration as JSON

**run**: `<target>`
- `target` — Target to run (required, e.g., `build`, `typecheck`, `test`)
- Executes `pnpm exec nx run-many -t <target>`

**schema**: `<generator>`
- `generator` — Generator name (required, e.g., `@nx/react:component`)
- Returns generator help with all available options

**affected**: `[base]`
- `base` — Git ref to compare against (default: `main`)
- Returns JSON array of affected project names

**graph**: `[output]`
- `output` — Output file path (default: `.nx/graph.json`)
- Generates workspace dependency graph

**tokens**: `[path]`
- `path` — File or directory to count (default: `.`)
- Uses `tools/scripts/count-tokens.ts` via tsx

**docs**: `[topic]`
- `topic` — Nx command to get help for (default: general help)

---
## [4][OUTPUT]

Commands return: `{"status": "success|error", ...}`.

| [INDEX] | [CMD]        | [RESPONSE]                            |
| :-----: | ------------ | ------------------------------------- |
|   [1]   | `workspace`  | `{projects: string[]}`                |
|   [2]   | `path`       | `{path: string}`                      |
|   [3]   | `generators` | `{generators: string}`                |
|   [4]   | `project`    | `{name: string, project: object}`     |
|   [5]   | `run`        | `{target: string, output: string}`    |
|   [6]   | `schema`     | `{generator: string, schema: string}` |
|   [7]   | `affected`   | `{base: string, affected: string[]}`  |
|   [8]   | `graph`      | `{file: string}`                      |
|   [9]   | `tokens`     | `{path: string, output: string}`      |
|  [10]   | `docs`       | `{topic: string, docs: string}`       |

---
## [5][ENVIRONMENT]

| [VAR]                | [REQUIRED] | [DESCRIPTION]                          |
| -------------------- | ---------- | -------------------------------------- |
| `CLAUDE_PROJECT_DIR` | No         | Override workspace root for `path` cmd |
| `NX_DAEMON`          | No         | Force-set to `false` by script         |

---
## [6][ERROR_HANDLING]

- Nx errors print `[ERROR] <message>` and exit 1
- Project not found: `[ERROR] Cannot find project '<name>'`
- Target not found: `[ERROR] Cannot find target '<target>'` for the project
- Graph generation failure: verify Nx workspace configuration is valid
