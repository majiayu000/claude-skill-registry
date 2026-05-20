---
name: skogai-argc
description: Create and manage argc-powered bash CLIs and Argcfile.sh task runners. Use when creating Argcfile.sh files, converting bash scripts to argc CLIs, adding argument parsing, shell completion, or task automation to projects.
---

# Argc CLI Framework

## Purpose

This skill enables working with the argc framework - a bash-based system that transforms comment annotations into full-featured command-line interfaces with automatic argument parsing, validation, help generation, and shell completions.

Argc has two components:

1. **argc framework** - The parser/engine that reads comment tags and generates CLI functionality
2. **argc-completions** - 1000+ pre-built completion scripts for common commands, using argc as the engine

## When to Use

Trigger this skill when:

- Creating or modifying `Argcfile.sh` task runner files
- Converting existing bash scripts to use argc argument parsing
- Adding command-line argument handling to bash scripts
- Implementing shell completions for custom commands
- Building CLI tools that need subcommands, flags, options, or positional arguments
- Setting up task automation similar to Make but using bash

## How to Use This Skill

### Core Workflow

**CRITICAL: Always use `argc --argc-eval` to understand what's happening**

You're good at bash, not argc. The fastest way to learn argc is to see the bash code it generates:

```bash
# Don't just run: argc +.md process file.md
# Instead, SEE what it generates:
argc --argc-eval Argcfile.sh +.md process file.md
```

This shows you exactly what bash code argc creates. Once you see the generated code, you can understand it because it's just bash.

**Why this matters:**

- Argc is code generation, not magic
- The eval output IS the implementation
- Validation errors are generated bash (heredoc + exit 1)
- Success cases are variable assignments + function calls
- Hooks (`_argc_before`, `_argc_after`) are visible in the execution order

**Integration pattern** - Every argc script requires the eval line:

```bash
eval "$(argc --argc-eval "$0" "$@")"
```

The `argc --argc-eval` command reads comment tags, validates arguments, and generates bash code. The `eval` executes this generated code.

**Success case** - Valid arguments generate variable setup and function invocation:

```bash
$ argc --argc-eval Argcfile.sh +.md process ./argc-skill/SKILL.md
export ARGC_PWD=/home/skogix/dev/skogargc
export ARGC_VARS=YXJnY19maWxldHlwZT0ubWQ7YXJnY19vdXRwdXQ9Li9vdXQ7...
argc_filetype=.md                              # Symbol value
argc_output=./out                              # Option with default
argc_files=( ./argc-skill/SKILL.md )          # Validated argument
argc__args=( Argcfile +.md process ./argc-skill/SKILL.md )
argc__fn=process
argc__positionals=( ./argc-skill/SKILL.md )
_argc_before                                   # Hook runs first
process ./argc-skill/SKILL.md                  # Command executes
_argc_after                                    # Hook runs last
```

**Validation error** - Wrong filetype shows argc validated the symbol first, then failed on file:

```bash
$ argc --argc-eval Argcfile.sh +.sh process ./argc-skill/SKILL.md
export ARGC_PWD=/home/skogix/dev/skogargc
command cat >&2 <<-'EOF'
error: invalid value `./argc-skill/SKILL.md` for `<FILES>...`
  [possible values: ./argc-skill/examples/hooks.sh, ./argc-skill/examples/demo.sh, ...]
EOF
exit 1
```

The symbol `+.sh` set `argc_filetype=.sh`, which made `_choice_files` only return `.sh` files. The `.md` file failed validation because it wasn't in the filtered list.

**Missing required argument** - Generates error and exit:

```bash
# argc --argc-eval examples/quick-start.sh
command cat >&2 <<-'EOF'
error: the following required arguments were not provided:
  <FILE>
EOF
exit 1
```

**Key points:**

- Validation happens during `argc --argc-eval`, before your bash code runs
- Error path: heredoc to stderr + exit 1 (script never runs)
- Success path: variable setup + function execution
- Flag values are `0` or `1`, not booleans
- Multi-value arguments become bash arrays: `${argc_files[@]}`
- Built-in variables (`argc__args`, `argc__fn`, `argc__positionals`) available for advanced use

1. **Use comment tags** - Define CLI structure through bash comments prefixed with `@`:

   ```bash
   # @describe Command description
   # @flag -v --verbose        Enable verbose output
   # @option -f --file         Input file path
   # @arg name!                Required positional argument
   ```

2. **Access parsed values** - Argc generates variables with `argc_` prefix:

   ```bash
   echo $argc_verbose     # Flag value (0 or 1)
   echo $argc_file        # Option value
   echo $argc_name        # Argument value
   ```

   **Multi-value parameters become arrays:**

   ```bash
   # @arg files*
   # @option --include*

   for file in "${argc_files[@]}"; do
       echo "File: $file"
   done

   echo "Includes: ${argc_include[@]}"
   echo "Count: ${#argc_files[@]}"
   ```

   **Built-in variables for advanced use:**
   - `argc__args` - Array of all CLI arguments
   - `argc__positionals` - Array of positional arguments only (no flags/options)
   - `argc__fn` - Name of the function being executed

   **Environment variables injected by argc:**
   - `ARGC_PWD` - Original working directory (available in Argcfile.sh)
   - `ARGC_SHELL_PATH` - Path to shell executable (configurable)
   - `ARGC_SCRIPT_NAME` - Override default Argcfile.sh name (configurable)

### Available Comment Tags

Reference these tags when building argc scripts:

| Tag         | Purpose              | Example                   |
| ----------- | -------------------- | ------------------------- |
| `@describe` | Command description  | `# @describe My CLI tool` |
| `@cmd`      | Define subcommand    | `# @cmd build Build it`   |
| `@alias`    | Subcommand aliases   | `# @alias b`              |
| `@arg`      | Positional argument  | `# @arg file!`            |
| `@option`   | Option argument      | `# @option --output`      |
| `@flag`     | Boolean flag         | `# @flag -v --verbose`    |
| `@env`      | Environment variable | `# @env API_KEY!`         |
| `@meta`     | Metadata             | `# @meta version 1.0`     |

Use "!" suffix for required parameters and "\*" suffix for multi-value arrays.

### @cmd vs @describe - When to Use Which

**Use `@describe` for single-script invocations:**

```bash
#!/bin/bash
# @describe Process multiple files with validation
# @arg inputs*    Input files to process
# @option --output=./out    Output directory
# @flag -v --verbose

main() {
    [[ "$argc_verbose" == "1" ]] && echo "Processing ${#argc_inputs[@]} files"
    for file in "${argc_inputs[@]}"; do
        echo "Processing: $file -> $argc_output/$(basename "$file")"
    done
}

eval "$(argc --argc-eval "$0" "$@")"
```

Run directly: `./script.sh file1.txt file2.txt file3.txt --verbose`

**Use `@cmd` for Argcfile.sh task runners or scripts with subcommands:**

```bash
#!/bin/bash
# Argcfile.sh

# @cmd build    Build the project
build() {
    echo "Building..."
}

# @cmd test     Run tests
test() {
    echo "Testing..."
}

eval "$(argc --argc-eval "$0" "$@")"
```

Run with subcommand: `argc build` or `argc test`

**Rule:** `@describe` describes the main entry point. `@cmd` defines subcommands (tasks). Use `@cmd` when you have multiple functions that users can invoke separately.

### Argument Modifiers

Argc uses suffix symbols to modify parameter behavior:

**Basic modifiers:**

- "!" - Required parameter (must be provided)
- "\*" - Multi-value parameter (can be provided multiple times, becomes array)
- "+" - Required multi-value (combines "!" and "\*")

**Examples:**

```bash
# @arg name!              Required positional arg
# @arg files*             Optional multi-value (0 or more)
# @arg tags+              Required multi-value (1 or more)
# @option --config!       Required option
# @option --include*      Multi-value option (can use multiple times)
```

**Accessing multi-value parameters:**

```bash
# @arg files*    Input files to process
main() {
    for file in "${argc_files[@]}"; do
        echo "Processing $file"
    done
}
```

**Rest-of-arguments pattern:**

Use `<VALUE+>` in the last notation to capture "all remaining arguments":

```bash
# @arg command!         Command to run
# @arg args* <ARGS+>    All remaining arguments
main() {
    echo "Running: $argc_command ${argc_args[@]}"
    "$argc_command" "${argc_args[@]}"
}
```

Run: `./script.sh docker run -it ubuntu bash` - captures `run -it ubuntu bash` into `argc_args` array.

### Inline Choices and Default Values

**Inline choices** - Define valid values directly in the tag:

```bash
# @arg env[dev|staging|prod]           Environment choice
# @option --format[json|yaml|toml]     Output format
```

**Default choice** - Use `=` prefix to set default:

```bash
# @arg env[=dev|staging|prod]          Defaults to 'dev'
# @option --format[=json|yaml|toml]    Defaults to 'json'
```

**Default values** - Use `=value` syntax:

```bash
# @arg name=world              Defaults to 'world' if not provided
# @option --timeout=30         Defaults to 30
# @option --host=localhost     Defaults to 'localhost'
```

**When to use inline vs choice functions:**

- Use inline choices for **static lists** (3-10 items) known at script-writing time
- Use choice functions for **dynamic lists** generated at runtime (files, git branches, API data)

### Environment Variables

The `@env` tag validates and documents environment variables your script requires:

**Basic syntax:**

```bash
# @env API_KEY!             Required env var
# @env DEBUG                Optional env var
# @env PORT=8080            Optional with default value
# @env ENV[dev|prod]        Env var with choices
# @env REGION[=us|eu|asia]  Env var with choices and default
```

**Validation example:**

```bash
#!/bin/bash
# @describe API client
# @env API_KEY!              API authentication key
# @env API_TIMEOUT=30        Request timeout in seconds

main() {
    echo "Using API_KEY: ${API_KEY:0:8}..."
    echo "Timeout: $API_TIMEOUT seconds"
}

eval "$(argc --argc-eval "$0" "$@")"
```

If `API_KEY` is not set, argc generates an error before your code runs:

```bash
error: the following required environment variables were not provided:
  API_KEY
```

**Use in Argcfile.sh tasks:**

```bash
# @cmd deploy                    Deploy application
# @env DEPLOY_ENV![dev|staging|prod]    Target environment
# @env AWS_REGION=us-east-1      AWS region
deploy() {
    echo "Deploying to $DEPLOY_ENV in $AWS_REGION"
}
```

Environment variables are accessed directly by name (not via `argc_` prefix).

### Choice Functions - Dynamic Validation

**When to create choice functions:**

Choice functions should be created **almost always** when the valid input values are known at runtime. They should **always** be created when input can be validated by checking against a generated list.

**Basic pattern:**

```bash
# @arg file!`_choice_files`    File to process

_choice_files() {
    ls examples/
}
```

**How it works:**

1. The backtick syntax `` `_choice_files` `` tells argc to call this function
2. Argc captures the function's stdout (one value per line)
3. Input is validated against this list
4. Invalid input triggers automatic error with possible values shown

**Real-world examples:**

```bash
# Files in directory
_choice_files() {
    ls -1 "$EXAMPLE_FOLDER_PATH"
}

# Git branches
_choice_branches() {
    git branch --list --format='%(refname:short)'
}

# Docker containers
_choice_containers() {
    docker ps --format '{{.Names}}'
}

# GitHub repositories via gh CLI
_choice_repos() {
    gh repo list skogai --json nameWithOwner --jq ".[].nameWithOwner"
}

# API endpoints from config
_choice_endpoints() {
    jq -r '.endpoints[].name' config.json
}
```

**Key principle:** If you can generate a list of valid values, create a choice function. This enables immediate validation and helpful error messages.

### Symbols - Dynamic Choice Functions

Symbols let you use an earlier parameter to filter what values are valid for later parameters. This creates "pre-validation validation" where one choice constrains another.

**Pattern:**

```bash
# @meta symbol +filetype[`_choice_filetypes`]
# @arg files+,[`_choice_files`]    Files to process

_choice_filetypes() {
  echo ".md"
  echo ".sh"
}

_choice_files() {
  find ./src/ -type f -name "*${argc_filetype}"
}
```

**How it works:**

1. `@meta symbol +filetype` defines `+` as a symbol that takes a filetype
2. User runs: `argc +.md process file1.md file2.md`
3. Argc sets `argc_filetype=.md` **before** validating `files`
4. `_choice_files` uses `${argc_filetype}` to filter the find results
5. Only `.md` files are valid choices for `files` argument

**The validation cascade:**

```bash
# With +.md - validates successfully
$ argc --argc-eval script.sh +.md process doc.md
argc_filetype=.md
argc_files=( doc.md )
process doc.md

# With +.sh - validation fails because doc.md not in .sh file list
$ argc --argc-eval script.sh +.sh process doc.md
error: invalid value `doc.md` for `<FILES+>...`
  [possible values: script.sh, build.sh, test.sh]
exit 1
```

Symbols make choice functions dynamic based on user input, enabling complex validation logic through pure declarations.

### Task Runner Pattern (Argcfile.sh)

Argc doubles as a task runner - a bash-native alternative to Make. The `Argcfile.sh` pattern transforms bash functions into discoverable, documented CLI commands.

**Basic Setup:**

1. Create `Argcfile.sh` in the project root
2. Define tasks as bash functions with `@cmd` tags
3. Run tasks via `argc <task-name>`

**Simple Example:**

```bash
#!/bin/bash
# @cmd build  Build the project
build() {
    echo "Building..."
}

# @cmd test   Run tests
test() {
    echo "Testing..."
}

eval "$(argc --argc-eval "$0" "$@")"
```

Run: `argc build` or `argc test`

**Task Runner Capabilities:**

**1. Tasks with arguments:**

```bash
# @cmd deploy      Deploy to environment
# @arg env!        Target environment (staging/production)
deploy() {
    echo "Deploying to $argc_env"
}
```

**2. Tasks with options:**

```bash
# @cmd test                Run test suite
# @option --filter         Test name pattern to match
# @flag --verbose          Show detailed output
test() {
    local args=()
    [[ -n "$argc_filter" ]] && args+=(--filter "$argc_filter")
    [[ "$argc_verbose" == "1" ]] && args+=(--verbose)
    pytest "${args[@]}"
}
```

**3. Multi-namespace organization for large Argcfiles:**

```bash
# @cmd docker::build       Build docker image
docker::build() {
    docker build -t myapp .
}

# @cmd docker::run         Run docker container
docker::run() {
    docker run myapp
}

# @cmd k8s::deploy         Deploy to kubernetes
k8s::deploy() {
    kubectl apply -f k8s/
}
```

Run with: `argc docker::build`, `argc k8s::deploy`

**4. Environment variable management:**

```bash
# @cmd connect                    Connect to database
# @env DATABASE_URL!              Database connection string
# @env DATABASE_TIMEOUT=30        Connection timeout in seconds
connect() {
    echo "Connecting to $DATABASE_URL with ${DATABASE_TIMEOUT}s timeout"
}
```

**5. Task dependencies (manual orchestration):**

```bash
# @cmd ci       Run full CI pipeline
ci() {
    argc lint
    argc test
    argc build
}

# @cmd lint     Run linters
lint() {
    echo "Linting..."
}
```

**Why use Argcfile.sh over Make:**

- Native bash syntax - full scripting power, no Make DSL
- Automatic help generation and argument validation
- Shell autocompletion for tasks and arguments
- Environment variable integration
- No tab-vs-spaces issues
- Natural parameter passing (no Make variable gymnastics)

### Behind the Scenes

Argc is not magic - it's bash code generation all the way down. To understand what `argc --argc-eval` actually does, look at what `argc --argc-build` generates: a standalone script with all parsing logic embedded.

The quick-start example (20 lines with comment tags) becomes 280+ lines when built standalone. Here's what argc generates:

**Validation function** - This is what validates choices from `_choice_files()`:

```bash
_argc_validate_choices() {
    local render_name="$1" raw_choices="$2" choices item choice concated_choices=""
    while IFS= read -r line; do
        choices+=("$line")
    done <<<"$raw_choices"
    for choice in "${choices[@]}"; do
        if [[ -z "$concated_choices" ]]; then
            concated_choices="$choice"
        else
            concated_choices="$concated_choices, $choice"
        fi
    done
    for item in "${@:3}"; do
        local pass=0 choice
        for choice in "${choices[@]}"; do
            if [[ "$item" == "$choice" ]]; then
                pass=1
            fi
        done
        if [[ $pass -ne 1 ]]; then
            _argc_die "error: invalid value \`$item\` for $render_name"$'\n'"  [possible values: $concated_choices]"
        fi
    done
}
```

This function:

1. Takes the output from your choice function (`_choice_files`)
2. Reads it line-by-line into a bash array
3. Checks if the user's input matches any valid choice
4. If not, generates the error message with all possible values
5. Calls `_argc_die` to exit with error

**Other generated functions:**

- `_argc_parse()` - Main argument parser with case statement for all flags/options
- `_argc_usage()` - Help text generator (what you see with `--help`)
- `_argc_version()` - Version display handler
- `_argc_take_args()` - Multi-value argument collector
- `_argc_match_positionals()` - Positional argument matcher
- `_argc_maybe_flag_option()` - Flag/option detection
- `_argc_die()` - Error handler and exit
- `_argc_run()` - Entry point orchestrator

**Key insight:** When you run `argc --argc-eval`, it generates similar code but outputs it as text for `eval` instead of embedding it in the script. Same logic, different delivery mechanism.

**Trade-offs:**

- **Small script + argc binary**: 20 lines + `eval "$(argc --argc-eval ...)"` (requires argc installed)
- **Standalone script**: 280+ lines, no dependencies, works anywhere bash works

Full generated code: `@references/quick-start-built.sh`

**Structured schema export:**

Argc can also export the parsed CLI structure as JSON via `argc --argc-export`:

```json
{
  "name": "quick-start",
  "describe": "Example CLI tool",
  "flag_options": [
    { "id": "verbose", "flag": true, "required": false, ... },
    { "id": "file", "flag": false, "num_args": [1, 1], ... }
  ],
  "positionals": [
    { "id": "file", "required": true, "choice": { "type": "Fn", "data": ["_choice_files", true] } }
  ],
  "envs": [
    { "id": "EXAMPLE_FOLDER_PATH", "default": { "value": "examples/" } }
  ],
  "command_fn": "main"
}
```

This machine-readable format captures everything argc extracted from the comment tags - useful for programmatic access, tooling integration, and AI agent automation.

Full export: `@references/quick-start-export.json`

### Safety Guidelines

**Never make argc scripts executable:**

Do not use `chmod +x` on argc scripts. Instead, always execute them via:

```bash
argc --argc-run ./script.sh [args]
```

Or for Argcfile.sh task runners:

```bash
argc <task-name>
```

_Note: Detailed explanation for this guideline will be provided separately._

### Additional Resources

- @docs/ - Original argc documentation from upstream repository (source of truth)
- @examples/ - Original argc examples from upstream repository

## Quick Start Template

- @examples/quick-start.sh

```bash
./examples/quick-start.sh --help                                 # View generated help
./examples/quick-start.sh quick-start.sh                         # Basic usage
./examples/quick-start.sh quick-start.sh --verbose               # With verbose flag
./examples/quick-start.sh idontexist.sh                          # Validation error
EXAMPLE_FOLDER_PATH=/tmp/ ./examples/quick-start.sh claude -v    # Override env var
```
