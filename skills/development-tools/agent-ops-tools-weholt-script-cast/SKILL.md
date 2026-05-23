---
name: agent-ops-tools
description: "Detect available development tools at session start. Saves to .agent/tools.json and warns about missing required tools. Works with or without aoc CLI installed."
category: state
invokes: [agent-ops-state]
invoked_by: [agent-ops-constitution, agent-ops-baseline]
state_files:
  read: [constitution.md]
  write: [tools.json]
---

# Tool Detection Skill

Discover available development tools and save to `.agent/tools.json` for use by other skills.

**Works with or without `aoc` CLI installed.** If `aoc` is not available, use the pure skill procedure below.

## CLI Integration (when aoc is installed)

This skill wraps the `aoc tools` CLI commands:

| Command | Purpose |
|---------|---------|
| `aoc tools scan` | Detect all available tools |
| `aoc tools show <tool>` | Show details for specific tool |
| `aoc tools export` | Export to JSON file |

## When to Invoke

### Automatic Invocation

The skill runs automatically during:

1. **Session start** — detect tools before any work begins
2. **Constitution creation** — populate available build/test commands
3. **Baseline capture** — verify required tools exist

### Manual Invocation

```
/tools-detect
/tools-check <tool-name>
/tools-require <tool-list>
```

## Procedure (with aoc CLI)

### 1. Detect Available Tools

```bash
# Run tool detection
aoc tools scan --json > .agent/tools.json
```

### 2. Display Summary

```
🔧 Tool Detection Results

| Category | Tool | Version | Status |
|----------|------|---------|--------|
| Version Control | git | 2.43.0 | ✅ Available |
| Version Control | gh | 2.40.0 | ✅ Available |
| Node.js | node | 20.10.0 | ✅ Available |
| Node.js | npm | 10.2.3 | ✅ Available |
| Node.js | pnpm | ❌ | Not found |
| Python | python | 3.12.0 | ✅ Available |
| Python | uv | 0.4.0 | ✅ Available |
| Python | pip | 23.3.1 | ✅ Available |
| Container | docker | 24.0.7 | ✅ Available |
| Container | kubectl | ❌ | Not found |

Detected: 8/14 common tools
```

### 3. Check Required Tools

If the project has requirements (from constitution or package files):

```
⚠️ Missing Required Tools

Based on project configuration:
- `pyproject.toml` requires: python, uv
- `package.json` requires: node, npm
- `Dockerfile` requires: docker

Missing:
- ❌ kubectl (referenced in k8s/ manifests)

Action: Install missing tools or remove references.
```

### 4. Save to tools.json

```json
{
  "tools": [
    {
      "name": "Git",
      "command": "git",
      "available": true,
      "category": "vcs",
      "version": "2.43.0",
      "path": "C:\\Program Files\\Git\\cmd\\git.exe"
    },
    {
      "name": "Node.js",
      "command": "node",
      "available": true,
      "category": "javascript",
      "version": "20.10.0",
      "path": "C:\\Program Files\\nodejs\\node.exe"
    },
    {
      "name": "Python",
      "command": "python",
      "available": true,
      "category": "python",
      "version": "3.12.0",
      "path": "C:\\Users\\...\\python.exe"
    },
    {
      "name": "Docker",
      "command": "docker",
      "available": true,
      "category": "containers",
      "version": "24.0.7",
      "path": "C:\\Program Files\\Docker\\Docker\\resources\\bin\\docker.exe"
    },
    {
      "name": "kubectl",
      "command": "kubectl",
      "available": false,
      "category": "containers"
    },
    {
      "name": "aoc",
      "command": "aoc",
      "available": true,
      "category": "agentops",
      "version": "0.1.24",
      "path": "C:\\Users\\...\\aoc.exe"
    }
  ],
  "summary": {
    "total": 46,
    "available": 18,
    "categories": {
      "agentops": 1,
      "vcs": 1,
      "python": 7,
      "javascript": 3,
      "dotnet": 1,
      "containers": 2,
      "editors": 1,
      "utilities": 1
    }
  }
}
```

## JSON Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://agentops.dev/schemas/tools.json",
  "title": "AgentOps Tools Manifest",
  "type": "object",
  "properties": {
    "tools": {
      "type": "array",
      "description": "List of detected tools",
      "items": {
        "type": "object",
        "properties": {
          "name": { "type": "string", "description": "Display name of the tool" },
          "command": { "type": "string", "description": "CLI command name" },
          "available": { "type": "boolean", "description": "Whether tool is installed and accessible" },
          "category": { "type": "string", "description": "Tool category (vcs, python, javascript, etc.)" },
          "version": { "type": ["string", "null"], "description": "Detected version (null if unavailable)" },
          "path": { "type": ["string", "null"], "description": "Full path to executable (null if unavailable)" }
        },
        "required": ["name", "command", "available", "category"]
      }
    },
    "summary": {
      "type": "object",
      "description": "Summary statistics",
      "properties": {
        "total": { "type": "integer", "description": "Total tools checked" },
        "available": { "type": "integer", "description": "Number of available tools" },
        "categories": { 
          "type": "object",
          "description": "Count of available tools per category",
          "additionalProperties": { "type": "integer" }
        }
      },
      "required": ["total", "available", "categories"]
    }
  },
  "required": ["tools", "summary"]
}
```

### Tool Categories

| Category | Description | Example Tools |
|----------|-------------|---------------|
| `agentops` | AgentOps CLI tools | aoc |
| `vcs` | Version control | git, gh, glab |
| `python` | Python ecosystem | python, pip, uv, ruff, mypy, pytest |
| `javascript` | Node.js ecosystem | node, npm, pnpm, yarn, bun, deno |
| `dotnet` | .NET ecosystem | dotnet, nuget |
| `rust` | Rust toolchain | rustc, cargo |
| `go` | Go toolchain | go |
| `java` | Java ecosystem | java, mvn, gradle |
| `containers` | Container tools | docker, podman, kubectl, helm |
| `cloud` | Cloud CLIs | aws, az, gcloud |
| `editors` | Editor CLIs | code, nvim, vim |
| `build` | Build tools | make, cmake, ninja |
| `utilities` | General utilities | jq, curl, wget, rg, fd, fzf |

## Supported Tools

The skill detects these common development tools:

### Version Control
- `git` — Git version control
- `gh` — GitHub CLI

### Node.js Ecosystem
- `node` — Node.js runtime
- `npm` — Node package manager
- `pnpm` — Fast package manager
- `yarn` — Yarn package manager
- `bun` — Bun runtime

### Python Ecosystem
- `python` — Python interpreter
- `pip` — Python package installer
- `uv` — Fast Python package manager
- `poetry` — Python dependency management
- `pipenv` — Python dev workflow

### .NET Ecosystem
- `dotnet` — .NET SDK

### Container/Cloud
- `docker` — Container runtime
- `kubectl` — Kubernetes CLI
- `helm` — Kubernetes package manager
- `terraform` — Infrastructure as code

### Other Languages
- `go` — Go compiler
- `cargo` / `rustc` — Rust toolchain
- `java` / `mvn` / `gradle` — Java ecosystem

## Procedure (without aoc CLI)

When `aoc` is not installed, the agent can perform tool detection directly using shell commands.

### Step 1: Run Detection Commands

**PowerShell (Windows):**
```powershell
# Version Control
git --version 2>$null | Select-Object -First 1
gh --version 2>$null | Select-Object -First 1

# Node.js Ecosystem
node --version 2>$null
npm --version 2>$null
pnpm --version 2>$null
yarn --version 2>$null
bun --version 2>$null

# Python Ecosystem
python --version 2>$null
pip --version 2>$null
uv --version 2>$null
poetry --version 2>$null

# .NET Ecosystem
dotnet --version 2>$null

# Container/Cloud
docker --version 2>$null
kubectl version --client --short 2>$null
helm version --short 2>$null
terraform --version 2>$null | Select-Object -First 1

# Other Languages
go version 2>$null
cargo --version 2>$null
rustc --version 2>$null
java --version 2>$null | Select-Object -First 1
mvn --version 2>$null | Select-Object -First 1
gradle --version 2>$null | Select-Object -First 1
```

**Bash (Linux/macOS):**
```bash
# Version Control
git --version 2>/dev/null | head -1
gh --version 2>/dev/null | head -1

# Node.js Ecosystem
node --version 2>/dev/null
npm --version 2>/dev/null
pnpm --version 2>/dev/null
yarn --version 2>/dev/null
bun --version 2>/dev/null

# Python Ecosystem
python --version 2>/dev/null || python3 --version 2>/dev/null
pip --version 2>/dev/null || pip3 --version 2>/dev/null
uv --version 2>/dev/null
poetry --version 2>/dev/null

# .NET Ecosystem
dotnet --version 2>/dev/null

# Container/Cloud
docker --version 2>/dev/null
kubectl version --client --short 2>/dev/null
helm version --short 2>/dev/null
terraform --version 2>/dev/null | head -1

# Other Languages
go version 2>/dev/null
cargo --version 2>/dev/null
rustc --version 2>/dev/null
java --version 2>/dev/null | head -1
mvn --version 2>/dev/null | head -1
gradle --version 2>/dev/null | head -1
```

### Step 2: Parse Output and Generate tools.json

After running the detection commands, parse the output and create `.agent/tools.json`:

```json
{
  "tools": [
    {
      "name": "Git",
      "command": "git",
      "available": true,
      "category": "vcs",
      "version": "2.43.0",
      "path": null
    },
    {
      "name": "Node.js",
      "command": "node",
      "available": true,
      "category": "javascript",
      "version": "20.10.0",
      "path": null
    },
    {
      "name": "uv",
      "command": "uv",
      "available": false,
      "category": "python"
    }
  ],
  "summary": {
    "total": 20,
    "available": 8,
    "categories": {
      "vcs": 1,
      "javascript": 1,
      "python": 0
    }
  }
}
```

### Step 3: Display Results

Present the detection results in the standard format (see "Display Summary" above).

### Notes for Pure Skill Detection

- **Path detection**: Without `aoc`, paths are not resolved (set to `null`)
- **Version parsing**: Extract version from output (e.g., `git version 2.43.0` → `2.43.0`)
- **Error handling**: If command fails, mark tool as `available: false`
- **Category assignment**: Use standard categories (vcs, python, javascript, dotnet, etc.)
- **Summary calculation**: Count available tools per category

## Integration with Other Skills

### agent-ops-constitution

When creating constitution, auto-populate commands:

```markdown
## Commands

### Build
- DETECTED: `uv run python scripts/build.py` (uv available)
- FALLBACK: `pip install -e . && python -m build` (pip available)

### Lint
- DETECTED: `uv run ruff check .` (ruff available via uv)
```

### agent-ops-baseline

Before capturing baseline, verify tools:

```
⚠️ Baseline Pre-check

Required tools for build commands:
- ✅ uv (required by: build, lint, test)
- ✅ python (required by: scripts)
- ❌ mypy (required by: lint) — install with: uv pip install mypy

Fix missing tools before capturing baseline.
```

### agent-ops-docker-review

Check for Docker-related tools:

```
🔧 Docker Tools Available:
- ✅ docker (24.0.7)
- ✅ docker-compose (2.23.0)
- ❌ hadolint — enhanced linting unavailable
- ❌ trivy — vulnerability scanning unavailable
- ❌ dive — layer analysis unavailable

Running with: docker only (basic features)
```

## Requirements Definition

Projects can define required tools in `.agent/requirements.json`:

```json
{
  "required": ["git", "python", "uv"],
  "optional": ["docker", "kubectl"],
  "build_tools": {
    "python": ">=3.10",
    "uv": ">=0.1.0"
  }
}
```

Or infer from project files:
- `pyproject.toml` → python, uv/pip
- `package.json` → node, npm/yarn/pnpm
- `Dockerfile` → docker
- `*.csproj` → dotnet
- `go.mod` → go
- `Cargo.toml` → cargo/rustc

## Caching

- Tools are cached in `.agent/tools.json`
- Re-scan if cache is older than 24 hours
- Force re-scan with `/tools-detect --force`

## Forbidden Behaviors

- Never install tools automatically
- Never modify system PATH
- Never run arbitrary executables from detection
- Only check version via safe commands (e.g., `git --version`)
