---
name: shell-guide
description: |
  Shell/Bash scripting guardrails, patterns, and best practices for AI-assisted development.
  Use when working with shell scripts (.sh, .bash), Makefiles, or when the user mentions Bash/Shell.
  Provides POSIX compliance guidelines, error handling patterns, and ShellCheck rules
  specific to this project's coding standards.
license: MIT
metadata:
  author: samuel
  version: "1.0"
  category: language
  language: shell
  extensions: ".sh,.bash,.zsh"
---

# Shell/Bash Guide

> Applies to: Bash 4+, POSIX sh, Automation Scripts, CI/CD Pipelines, Makefiles

## Core Principles

1. **Strict Mode Always**: Every script starts with `set -euo pipefail` to fail fast on errors
2. **Quote Everything**: All variable expansions must be double-quoted to prevent word splitting and globbing
3. **Explicit Over Implicit**: Use `[[ ]]` for conditionals, `local` for function variables, named constants for magic values
4. **Fail Loudly**: Never swallow errors silently; use `trap` for cleanup and meaningful exit codes
5. **ShellCheck Clean**: All scripts pass `shellcheck` with zero warnings before commit

## Guardrails

### Shebang and Strict Mode

- Every script: `#!/usr/bin/env bash` (or `#!/bin/sh` for POSIX)
- Immediately follow with `set -euo pipefail`
- Use `set -x` only for debugging, never in production scripts
- POSIX scripts must not use bash-specific features (`[[ ]]`, arrays, `local`)

```bash
#!/usr/bin/env bash
set -euo pipefail
[[ "${TRACE:-}" == "1" ]] && set -x
```

### Quoting

- Always double-quote: `"$var"`, `"$@"`, `"${arr[@]}"`, `"$(command)"`
- Single quotes for literals that must not be interpolated
- Only omit quotes in arithmetic: `$(( count + 1 ))`

```bash
# Correct
grep -r "$pattern" "$directory"
for arg in "$@"; do process "$arg"; done

# Wrong - word splitting and globbing bugs
grep -r $pattern $directory
for arg in $@; do process $arg; done
```

### Error Handling

- Check return codes: `if ! command; then handle_error; fi`
- Inline: `critical_cmd || { echo "Failed" >&2; exit 1; }`
- Never use `set +e` (restructure logic instead)
- Exit codes: 0 = success, 1 = general error, 2 = usage error
- Errors to stderr: `echo "Error: message" >&2`

### Portability

- `#!/usr/bin/env bash` over `#!/bin/bash` (varies across systems)
- `command -v` instead of `which` for executable checks
- `$(command)` instead of backticks
- `printf` over `echo` for portable output (flags/escapes differ)

### Security

- Never use `eval` (use arrays for dynamic command building)
- Validate all external input (arguments, env vars, file contents)
- `mktemp` for temp files, never hardcoded `/tmp/myapp.tmp`
- No secrets in script files; read from environment or secret managers
- `umask 077` before creating sensitive files

```bash
# Safe temp file
tmpfile="$(mktemp)" || exit 1
trap 'rm -f "$tmpfile"' EXIT

# Never do this
eval "$user_input"        # Command injection
password="hunter2"        # Hardcoded secret
```

## Script Structure

```
#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly SCRIPT_NAME="$(basename "${BASH_SOURCE[0]}")"

# ── Configuration (with defaults) ─────────────────────
LOG_LEVEL="${LOG_LEVEL:-info}"
OUTPUT_DIR="${OUTPUT_DIR:-./output}"

# ── Functions ──────────────────────────────────────────
usage() { ... }
cleanup() { ... }
main() { ... }

# ── Traps & Entry ─────────────────────────────────────
trap cleanup EXIT
main "$@"
```

## Key Patterns

### Parameter Expansion

```bash
db_host="${DB_HOST:-localhost}"              # Default value
api_key="${API_KEY:?Error: API_KEY required}" # Required (fail if unset)

filename="archive.tar.gz"
name="${filename%%.*}"         # "archive"    (longest suffix removal)
ext="${filename#*.}"           # "tar.gz"     (shortest prefix removal)
path="/usr/local/bin/tool"
dir="${path%/*}"               # "/usr/local/bin"
base="${path##*/}"             # "tool"
upper="${var^^}"               # UPPERCASE (Bash 4+)
lower="${var,,}"               # lowercase (Bash 4+)
```

### Trap for Cleanup

```bash
cleanup() {
    local exit_code=$?
    rm -f "$tmpfile"
    exit "$exit_code"         # Preserve original exit code
}
trap cleanup EXIT
trap 'echo "Interrupted" >&2; exit 130' INT TERM
```

### Arrays (Avoid eval)

```bash
declare -a files=()
files+=("first.txt" "second.txt")
for file in "${files[@]}"; do echo "$file"; done

# Build commands safely with arrays
cmd=(curl --silent --fail)
[[ -n "${TOKEN:-}" ]] && cmd+=(--header "Authorization: Bearer $TOKEN")
"${cmd[@]}" "$url"
```

### Functions

```bash
process_file() {
    local file="$1"
    local -r max_lines=1000
    local line_count
    line_count="$(wc -l < "$file")"
    if (( line_count > max_lines )); then
        echo "Warning: $file exceeds $max_lines lines" >&2
    fi
}
```

All variables inside functions must be declared `local`.

### Here Documents

```bash
cat <<EOF                     # Interpolated
Hello, $USER at $(hostname)
EOF

cat <<'EOF'                   # Literal (no expansion)
This $variable stays literal.
EOF
```

### Safe File Iteration

```bash
# Handles spaces, newlines, special characters
while IFS= read -r -d '' file; do
    process "$file"
done < <(find "$dir" -type f -name "*.log" -print0)

# Simple globs (Bash 4+)
shopt -s nullglob globstar
for file in "$dir"/**/*.sh; do process "$file"; done
```

Never use `for file in $(find ...)` -- it breaks on spaces.

### Process Substitution

```bash
diff <(sort file1.txt) <(sort file2.txt)
```

## Testing

### bats-core

```bash
# test/deploy.bats
setup()    { export TMPDIR="$(mktemp -d)"; }
teardown() { rm -rf "$TMPDIR"; }

@test "deploy requires environment argument" {
    run ./deploy.sh
    [ "$status" -ne 0 ]
    [[ "$output" == *"Usage:"* ]]
}
```

### Testing Standards

- Test with `bats-core` (preferred) or `shellspec`
- Test files in `test/` or `spec/` directory
- Test names describe behavior: `"deploy requires environment argument"`
- Use `setup`/`teardown` for temp dirs and fixtures
- Coverage: >80% library functions, >60% scripts
- Each test must be independent

## Tooling

### ShellCheck

```bash
shellcheck script.sh                        # Single file
find . -name "*.sh" -exec shellcheck {} +   # All scripts

# Suppress with justification
# shellcheck disable=SC2034  # Variable used by sourced script
unused_looking_var="value"
```

### shfmt

```bash
shfmt -w -i 4 -bn script.sh     # Format in place (4-space indent)
shfmt -d -i 4 script.sh         # Check only (diff output)
```

### Essential Commands

```bash
shellcheck *.sh              # Lint
shfmt -d -i 4 *.sh           # Check formatting
bats test/                   # Run tests
bash -n script.sh            # Syntax check (no execution)
```

## References

For detailed patterns and examples, see:

- [references/patterns.md](references/patterns.md) -- Script templates, trap patterns, portable scripting examples

## External References

- [Bash Reference Manual](https://www.gnu.org/software/bash/manual/)
- [POSIX Shell Specification](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/V3_chap02.html)
- [ShellCheck Wiki](https://www.shellcheck.net/wiki/)
- [Google Shell Style Guide](https://google.github.io/styleguide/shellguide.html)
- [bats-core](https://github.com/bats-core/bats-core)
- [shellspec](https://shellspec.info/)
- [shfmt](https://github.com/mvdan/sh)
- [Pure Bash Bible](https://github.com/dylanaraps/pure-bash-bible)
