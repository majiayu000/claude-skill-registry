---
name: bash-script-generator
description: Generate Bash 3.2-compatible scripts with a standardized check_requirements guardrail, friendly validation errors, and optional shfmt formatting. Use when writing or updating bash scripts that need consistent argument validation, dependency checks, and portability.
license: MIT
allowed-tools: Read Write Edit Bash(shfmt:*)
metadata:
  generated-at: "2026-01-10T00:00:00Z"
  group: "automation"
  category: "scripting"
  difficulty: "intermediate"
  step-count: "4"
---

# Structured Bash Script Generator

## What You'll Do
- 📥 Gather the script's goal, required positional/flag arguments, environment variables, and external program dependencies
- 🧱 Produce a Bash 3.2-compatible script skeleton with a `check_requirements` function that validates inputs and dependencies kindly
- 🛡️ Ensure the script sets safe defaults (`set -euo pipefail`), quotes expansions, and keeps logic portable to macOS/Linux Bash 3.2
- ✨ Format the script with `shfmt` when available and return a polished result ready for immediate use

---

## When to Use This Skill
Use this skill whenever the user asks for a new bash script or a major refactor of an existing script and they expect:
- Guardrails around required arguments, environment variables, or external tools
- Friendly, actionable error messages when prerequisites are missing
- Compatibility with older Bash versions (macOS default 3.2)

Do **not** use this skill for:
- POSIX `sh`-only scripts (no Bash-specific features allowed)
- Small one-liners or trivial command snippets (respond inline instead)
- Advanced Bash (>3.2) needs such as associative arrays or `coproc`

---

## Phase 1 · Clarify the Script Brief
1. Confirm the script's purpose, expected inputs, outputs, and typical usage examples.
2. Identify all positional arguments and flags that must be provided. Capture human-friendly labels for each so the usage text and errors are clear.
3. List required environment variables (names + meaning) and external commands (e.g., `curl`, `jq`). Note install hints when useful.
4. Ask about optional inputs or defaults that should be applied when values are omitted.
5. Determine whether the script writes files, consumes stdin/stdout, or needs cleanup logic.

> **Deliverable:** A short table (in notes or your head) of arguments, env vars, and commands you will feed into `check_requirements` and `usage` messaging.

---

## Phase 2 · Plan the Script Structure
Lay out the sections before writing code:

1. **Header & Safety**
   - `#!/usr/bin/env bash`
   - `set -euo pipefail`
   - `IFS=$'\n\t'` only if tighter word splitting is needed.

2. **Metadata Comments (optional)**
   - Summarize script purpose and prerequisites in commented lines for discoverability.

3. **Usage Helper**
   - A `usage()` function that prints how to run the script, expected args, environment variables, and examples.

4. **Requirement Configuration**
   - Define `REQUIRED_ARGS`, `REQUIRED_ENV_VARS`, and `REQUIRED_PROGRAMS` as indexed arrays (compatible with Bash 3.2). When nothing is required, keep the arrays empty but present.
   - Optionally define associative-looking notes via comments or simple `case` statements; do **not** use `declare -A` (requires Bash ≥4).

5. **check_requirements Function** (see Phase 3 for exact pattern)
   - Accepts parsed arguments (or a struct) and validates all prerequisites.
   - Emits kind, actionable errors to STDERR and returns non-zero on failure.

6. **Argument Parsing**
   - Prefer `getopts` for short flags. For long options, parse manually with a `while` loop; avoid `getopt` if portability is uncertain.
   - Populate variables for downstream logic (use `${VAR:-}` to coexist with `set -u`).

7. **Main Logic**
   - Encapsulate primary workflow in `main()` and finish with `main "$@"`.

---

## Phase 3 · Compose the Script
Follow this recipe while writing the actual script content.

### Required Guardrail: `check_requirements`
```bash
check_requirements() {
  local -r provided_arg_count=$1
  local missing=0

  if [ ${#REQUIRED_ARGS[@]} -gt 0 ] && [ "$provided_arg_count" -lt ${#REQUIRED_ARGS[@]} ]; then
    printf 'Error: Expected %s arguments (%s) but received %s.\n' \
      ${#REQUIRED_ARGS[@]} "${REQUIRED_ARGS[*]}" "$provided_arg_count" >&2
    missing=1
  fi

  local env_var
  for env_var in "${REQUIRED_ENV_VARS[@]}"; do
    if [ -z "${!env_var:-}" ]; then
      printf 'Error: Missing required environment variable %s. Please set it before rerunning.\n' "$env_var" >&2
      missing=1
    fi
  done

  local program
  for program in "${REQUIRED_PROGRAMS[@]}"; do
    if ! command -v "$program" >/dev/null 2>&1; then
      printf 'Error: Required program %s is not installed or not on PATH. Please install it first.\n' "$program" >&2
      missing=1
    fi
  done

  if [ "$missing" -ne 0 ]; then
    printf '\n' >&2
    usage >&2
    return 1
  fi
}
```

**Implementation notes:**
- Always invoke `check_requirements` right after argument parsing, e.g. `check_requirements "$#"`.
- If the script allows optional trailing arguments, keep `REQUIRED_ARGS` limited to the mandatory ones and validate optional parameters separately after `check_requirements "$#"` succeeds.
- Keep error language supportive (“Please install…”) rather than punitive.
- Route any diagnostics to STDERR (`>&2`) and exit gracefully with `return 1` so the caller can `exit 1` or handle it.
- Only call `usage` from error paths (like failed requirement checks) so successful runs stay quiet unless the user explicitly asks for help.

### Bash 3.2 Compatibility Guardrails
- Use indexed arrays only; no associative arrays or namerefs (`local -n`).
- Avoid `[[ string =~ regex ]]` with capture groups that rely on Bash ≥3.2. Basic regex is fine, but keep patterns simple.
- Do not rely on `mapfile`, `readarray`, `coproc`, `printf -v`, or process substitution that requires `/dev/fd` (often missing on macOS).
- Prefer `$( command )` subshells over backticks and quote every expansion.
- Use `printf` instead of `echo -e` for reliable escape handling.

### Usage Function Pattern
```bash
usage() {
  cat <<'EOF'
Usage: my_script.sh <source> <destination> [--dry-run]

Required arguments:
  source        Path to the input file (must exist)
  destination   Output directory (will be created if missing)

Environment variables:
  API_TOKEN     Token used to authenticate API requests

External tools:
  curl, jq

Examples:
  my_script.sh ./input.csv ./out --dry-run
EOF
}
```
Tailor the body to the specific script; keep instructions kind and explicit.

### Script Assembly Checklist
1. Write header, safety settings, and optional metadata comments.
2. Define requirement arrays (even if empty) and defaults for optional values.
3. Implement `usage()` and `check_requirements()` exactly once.
4. Parse arguments safely (`getopts` or manual loop) and convert into named variables.
5. Call `check_requirements` immediately after parsing. If it fails, exit with `exit 1`.
6. Implement `main()` with clear, modular helpers; rely on functions instead of sprawling inline code.
7. End with `main "$@"` and ensure the script returns appropriate exit codes.

---

## Phase 4 · Validate, Format, and Hand Off
1. **Self-check**
   - Does the script run without arguments and show `usage`?
   - Do missing env vars and programs produce the friendly errors described earlier?
   - Do all branches respect `set -euo pipefail` (guard nullable variables with `${VAR:-}`)?

2. **Formatting via `shfmt`**
   - Detect availability: `if command -v shfmt >/dev/null 2>&1; then ... fi`
   - Run `shfmt -i 2 -bn -ci -sr -w <path-to-script>` after writing the file.
   - Mention in your response whether formatting ran or was skipped (and why).

3. **Final Response Checklist**
   - Provide the complete script in a fenced code block (label it `bash`).
   - Summarize how requirements are enforced.
   - If manual formatting was necessary (no `shfmt`), note it explicitly.
   - Suggest any quick validation commands (dry runs, linting) if relevant.

---

## Reference Template
Use this skeleton as a starting point and adapt each section based on the user's requirements:

```bash
#!/usr/bin/env bash
set -euo pipefail

# Script: <name>
# Purpose: <one-line description>
# Requirements: <short summary of args/env/programs>

REQUIRED_ARGS=("arg1" "arg2")
REQUIRED_ENV_VARS=("ENV_VAR")
REQUIRED_PROGRAMS=("curl" "jq")

usage() {
  cat <<'EOF'
Usage: <script-name> <arg1> <arg2>

Required arguments:
  arg1   <describe>
  arg2   <describe>

Environment variables:
  ENV_VAR   <describe>

External tools:
  curl, jq
EOF
}

check_requirements() {
  local -r provided_arg_count=$1
  local missing=0

  if [ ${#REQUIRED_ARGS[@]} -gt 0 ] && [ "$provided_arg_count" -lt ${#REQUIRED_ARGS[@]} ]; then
    printf 'Error: Expected %s arguments (%s) but received %s.\n' \
      ${#REQUIRED_ARGS[@]} "${REQUIRED_ARGS[*]}" "$provided_arg_count" >&2
    missing=1
  fi

  local env_var
  for env_var in "${REQUIRED_ENV_VARS[@]}"; do
    if [ -z "${!env_var:-}" ]; then
      printf 'Error: Missing required environment variable %s. Please set it before rerunning.\n' "$env_var" >&2
      missing=1
    fi
  done

  local program
  for program in "${REQUIRED_PROGRAMS[@]}"; do
    if ! command -v "$program" >/dev/null 2>&1; then
      printf 'Error: Required program %s is not installed or not on PATH. Please install it first.\n' "$program" >&2
      missing=1
    fi
  done

  if [ "$missing" -ne 0 ]; then
    printf '\n' >&2
    usage >&2
    return 1
  fi
}

parse_args() {
  # TODO: replace with real parsing
  SOURCE=${1:-}
  DEST=${2:-}
}

main() {
  parse_args "$@"
  check_requirements "$#" || exit 1

  # TODO: script logic goes here
  printf 'Running with source=%s dest=%s\n' "$SOURCE" "$DEST"
}

main "$@"
```

Update placeholders, replace `TODO` sections, and adjust arrays when a requirement does not apply (leave the array empty—do not delete it).

---

## Quality Checklist Before Finishing
- [ ] Script declares all requirement arrays and the `check_requirements` function
- [ ] Error messages are friendly, specific, and routed to STDERR
- [ ] Script avoids Bash ≥4 features and has been reviewed for 3.2 compatibility
- [ ] `usage()` accurately reflects arguments, env vars, and dependencies
- [ ] Formatting completed with `shfmt` (or explicitly noted why it was skipped)
- [ ] Final response contains both summary guidance and the full script for copy/paste
