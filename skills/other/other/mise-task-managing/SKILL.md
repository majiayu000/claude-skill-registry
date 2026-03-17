---
name: mise-task-managing
description: Expert guidance for mise task runners including TOML task configuration, file-based tasks, task orchestration with dependencies, sources/outputs caching, parallel execution, and workflow patterns. Use when working with mise.toml task definitions, mise-tasks/ directory, task dependencies, build caching, or mise task automation.
---

# Mise Task Management

Expert skill for mise task runners with TOML-based and file-based task definitions.

## Task Definition Methods

Mise supports two primary approaches for defining tasks:

### 1. TOML Tasks (Recommended for Simple Tasks)

Define tasks directly in `mise.toml` under the `[tasks.*]` section:

```toml
[tasks.build]
description = "Build the project"
run = "cargo build"

[tasks.test]
description = "Run tests"
run = "cargo test"
depends = ["build"]
```

Execute: `mise run build` or `mise build`

### 2. File Tasks (Recommended for Complex Scripts)

Create executable scripts in `mise-tasks/` directory:

```bash
#!/usr/bin/env bash
#MISE description="Build the project"
#MISE depends=["lint"]
cargo build
```

Place in `mise-tasks/build` (no extension), make executable, and run identically: `mise run build`

## Configuration File Structure

```
project-root/
├── mise.toml              # Primary config with [tasks.*] section
├── mise-tasks/            # Directory for file-based tasks
│   ├── build             # Executable task script
│   ├── test              # Executable task script
│   └── deploy            # Executable task script
└── .mise/
    └── config.toml        # Alternative location for mise.toml
```

## Core Task Configuration

### TOML Task Structure

```toml
[tasks.task-name]
description = "Task description shown in mise tasks"
run = "command to execute"
depends = ["other-task"]
env = { VAR = "value" }
dir = "{{ config_root }}"
sources = ["src/**/*.rs"]
outputs = ["target/release/binary"]
```

### File Task Metadata

Use `#MISE` comments for task configuration:

```bash
#!/usr/bin/env bash
#MISE description="Deploy application"
#MISE depends=["build", "test"]
#MISE sources=["dist/**/*"]
#MISE env={ENVIRONMENT="production"}

# Task implementation
./deploy.sh
```

## Task Configuration Options

### Essential Fields

**`run`** (TOML tasks only, required)
- String: `run = "cargo build"`
- Array: `run = ["cargo build", "cargo test"]`
- Mixed with task refs: `run = [{ task = "lint" }, "cargo build"]`

**`description`**
- Used in help output, completions, and `mise tasks` listing
- Visible to users as documentation

**`depends`**
- Tasks that run before this task
- `depends = ["lint", "test"]`

**`depends_post`**
- Tasks that run after this task completes
- `depends_post = ["cleanup"]`

### Environment & Execution

**`env`**
- Task-specific environment variables
- Not propagated to dependent tasks
- `env = { NODE_ENV = "production", API_KEY = "secret" }`

**`tools`**
- Tools to install/activate before task
- Only for this task, not dependencies
- `tools = ["node@20", "python@3.12"]`

**`dir`**
- Working directory for execution
- Default: `"{{ config_root }}"` (where mise.toml lives)
- `dir = "{{ cwd }}/subdir"`

**`shell`**
- Override default shell for inline execution
- TOML tasks only
- `shell = "bash -c"`

### Caching with Sources & Outputs

**`sources`**
- Input files/globs that this task uses
- Mise skips execution if sources unchanged and outputs are newer
- `sources = ["src/**/*.rs", "Cargo.toml"]`

**`outputs`**
- Output files/directories produced by task
- Enable automatic change detection with `outputs = [{ auto = true }]`
- `outputs = ["target/release/binary"]`

**Caching behavior:**
- Mise compares modification times of oldest output vs newest source
- If outputs are newer, task is skipped
- Use `mise run --force` to bypass cache

### Control & Visibility

**`hide`**
- Hide from `mise tasks` output, help, and completions
- Useful for internal/deprecated tasks
- `hide = true`

**`quiet`**
- Suppress mise's own output (like command being run)
- `quiet = true`

**`silent`**
- Suppress all task output
- Options: `true` (both), `"stdout"`, `"stderr"`
- `silent = "stdout"`

**`raw`**
- Connect task directly to shell stdin/stdout/stderr
- Disables parallel execution
- Required for interactive tasks
- `raw = true`

**`confirm`**
- Prompt user before running
- `confirm = "Are you sure you want to deploy?"`

### Advanced: Task Arguments

Define formal arguments and flags in `usage` field:

```toml
[tasks.deploy]
run = "deploy.sh"
usage = """
{usage} [OPTIONS] <environment>

Arguments:
  <environment>  Target environment [env: ENVIRONMENT]

Options:
  --force       Skip confirmation
"""
```

## Running Tasks

### Basic Execution

```bash
mise run task-name          # Full command
mise r task-name            # Short alias
mise task-name              # Shorthand (avoid in scripts)
```

### Passing Arguments

Extra arguments pass through to the task:

```bash
mise run build --release
mise run test -- --nocapture
```

### Multiple Tasks

Run sequentially:
```bash
mise run lint build test
```

Run separate sequences with `:::` delimiter:
```bash
mise run build arg1 ::: test arg2
```

### Parallel Execution

Default: 4 parallel jobs. Control via:
- `--jobs N` flag
- `MISE_JOBS` environment variable
- `jobs` setting in mise.toml

```bash
mise run -j 8 task1 task2 task3
```

Output is line-prefixed to prevent interleaving. Use `--interleave` for direct stdout/stderr.

### Listing Tasks

```bash
mise tasks                    # List all tasks
mise tasks --hidden           # Include hidden tasks
mise tasks deps [tasks]...    # Show task dependencies
```

### Watching for Changes

```bash
mise watch task-name          # Re-run on file changes
```

Uses watchexec internally to monitor source files.

## Common Patterns

### Task Orchestration

```toml
[tasks.ci]
description = "Run CI checks"
depends = ["lint", "test", "build"]

[tasks.deploy]
description = "Deploy application"
depends = ["ci"]
depends_post = ["notify"]
run = "./deploy.sh"
```

### Environment-Specific Tasks

```toml
[tasks.build]
description = "Build for development"
run = "npm run build"
env = { NODE_ENV = "development" }

[tasks."build:prod"]
description = "Build for production"
run = "npm run build"
env = { NODE_ENV = "production" }
```

### Conditional Execution with Sources

```toml
[tasks.compile]
description = "Compile only if sources changed"
run = "gcc src/*.c -o bin/app"
sources = ["src/*.c", "src/*.h"]
outputs = ["bin/app"]
```

### File Task with Dependencies

```bash
#!/usr/bin/env bash
#MISE description="Full CI pipeline"
#MISE depends=["lint", "test"]
#MISE sources=["src/**/*"]

set -euo pipefail

echo "Running build..."
cargo build --release

echo "Running integration tests..."
cargo test --release
```

### Cross-Language Task Runner

```toml
[tasks.backend]
description = "Start backend server"
dir = "{{ config_root }}/backend"
run = "cargo run"

[tasks.frontend]
description = "Start frontend dev server"
dir = "{{ config_root }}/frontend"
run = "npm run dev"

[tasks.dev]
description = "Start full development environment"
depends = ["backend", "frontend"]
```

## Environment Variables Provided to Tasks

Mise automatically injects these variables:

- `MISE_ORIGINAL_CWD` - Initial working directory
- `MISE_CONFIG_ROOT` - Directory containing mise.toml
- `MISE_PROJECT_ROOT` - Project root directory
- `MISE_TASK_NAME` - Current task identifier
- `MISE_TASK_DIR` - Task script location (file tasks)
- `MISE_TASK_FILE` - Full task script path (file tasks)

## Workflow Commands

### Initialize Mise in Project

```bash
# 1. Create mise.toml
cat > mise.toml <<'EOF'
[tools]
# Optional: Define tool versions
# node = "20"
# python = "3.12"

[env]
PROJECT_ROOT = "{{ cwd }}"

[tasks.build]
description = "Build the project"
run = "make build"

[tasks.test]
description = "Run tests"
depends = ["build"]
run = "make test"

[tasks.clean]
description = "Clean build artifacts"
run = "make clean"
EOF

# 2. Trust the config
mise trust

# 3. Verify tasks
mise tasks
```

### Convert Makefile to Mise Tasks

For projects with Makefiles, migrate to mise for better dependency management:

```toml
# Instead of Makefile targets
[tasks.install]
description = "Install dependencies"
run = "npm install"

[tasks.build]
description = "Build project"
depends = ["install"]
sources = ["src/**/*"]
outputs = ["dist/"]
run = "npm run build"

[tasks.test]
description = "Run tests"
depends = ["build"]
run = "npm test"
```

Benefits over Make:
- Automatic parallel execution
- Built-in file watching
- Cross-platform compatibility
- Better dependency management

### Create File Task Script

```bash
# 1. Create task directory
mkdir -p mise-tasks

# 2. Create executable script
cat > mise-tasks/deploy <<'BASH'
#!/usr/bin/env bash
#MISE description="Deploy application to production"
#MISE depends=["test"]
#MISE confirm="Deploy to production?"
#MISE env={ENVIRONMENT="production"}

set -euo pipefail

echo "Deploying to production..."
./scripts/deploy.sh "$@"
BASH

# 3. Make executable
chmod +x mise-tasks/deploy

# 4. Run it
mise run deploy
```

## Best Practices

### Task Naming

- Use semantic names: `build`, `test`, `deploy`
- Group with colons: `test:unit`, `test:integration`, `test:e2e`
- Wildcard support: `mise run test:*` runs all test tasks

### Dependency Management

- Use `depends` for prerequisites: `depends = ["lint", "test"]`
- Use `depends_post` for cleanup: `depends_post = ["notify"]`
- Keep dependency chains shallow (2-3 levels max)
- Tasks run in parallel when possible

### Caching Strategy

- Define `sources` for input files
- Define `outputs` for generated artifacts
- Use globs for flexibility: `sources = ["src/**/*.rs"]`
- Use `{ auto = true }` for automatic output detection

### File Tasks vs TOML Tasks

**Use File Tasks when:**
- Script is >10 lines
- Complex bash logic required
- Multiple commands with error handling
- Script needs version control

**Use TOML Tasks when:**
- Simple one-liners
- Task orchestration (depends on other tasks)
- Environment variable setup
- Quick prototyping

### Error Handling

**In TOML tasks:**
```toml
[tasks.robust]
run = ["set -euo pipefail", "./script.sh"]
```

**In File tasks:**
```bash
#!/usr/bin/env bash
set -euo pipefail  # Exit on error, undefined vars, pipe failures

# Task implementation
```

## Troubleshooting

### Tasks Not Appearing

**Check:**
1. Syntax errors in mise.toml: `mise tasks --verbose`
2. Missing `description` field
3. Task marked `hide = true`
4. Config not trusted: `mise trust`

### Task Not Caching

**Verify:**
1. `sources` and `outputs` are defined
2. Globs match files: `ls src/**/*.rs`
3. Output files exist after task runs
4. Use `mise run --force task-name` to bypass cache once

### File Task Not Executable

```bash
chmod +x mise-tasks/task-name
```

### Tasks Running in Wrong Directory

Set explicit working directory:
```toml
[tasks.task-name]
dir = "{{ config_root }}/subdir"
run = "make build"
```

### Parallel Execution Issues

For interactive tasks or tasks requiring stdin:
```toml
[tasks.interactive]
raw = true
run = "npm run dev"
```

## Additional Resources

- Official docs: https://mise.jdx.dev/tasks/
- Task configuration: https://mise.jdx.dev/tasks/task-configuration.html
- Running tasks: https://mise.jdx.dev/tasks/running-tasks.html
