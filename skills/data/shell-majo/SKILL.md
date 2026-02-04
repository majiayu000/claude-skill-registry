---
name: shell-majo
description: POSIX shell scripting standards for Mark's workflow.
license: Unlicense OR 0BSD
metadata:
  author: Mark Joshwel <mark@joshwel.co>
  version: "2026.2.2"
---

# POSIX Shell Scripting Standards (Mark)

**Goal**: Write portable, defensive shell scripts using pure POSIX sh (not bash) unless a specific Bash feature is strictly required.

## When to Use This Skill

- **Writing new shell scripts** (`.sh` files)
- **Modifying existing shell scripts**
- **Choosing between POSIX sh and Bash**
- **Adding error handling to scripts**
- **Creating command-line tools**
- **Writing automation scripts**

## When NOT to Use This Skill

- **Script requires Bash-specific features** (arrays, process substitution, extglob)
- **Target environment guarantees Bash availability** AND requires Bash features
- **Complex data structures needed** that can't be flattened to strings
- **Writing Python/JS scripts instead** (prefer those for complex logic)

## Process

1. **Check script requirements** - Determine if POSIX sh is sufficient or Bash is truly needed
2. **Set shebang** - Use `#!/bin/sh` for POSIX, `#!/bin/bash` only if enumerated exception applies
3. **Add license header** - Include full Unlicense header (see File Header section)
4. **Enable error handling** - Add `set -e` at the top
5. **Define exit codes** - Document exit code ranges in comments
6. **Use proper naming** - UPPER_CASE for env vars/constants, lower_case for local vars
7. **Quote all variables** - Prevent word splitting: `"$var"` not `$var`
8. **Use printf not echo** - For portable output
9. **Test with shellcheck** - Run `shellcheck script.sh`
10. **Update AGENTS.md** - Document any project-specific shell patterns

## Constraints

- **ALWAYS default to POSIX sh** for all scripts
- **ONLY use Bash if you can explicitly enumerate** which Bash-specific feature is strictly required and impossible in POSIX sh
- **Valid Bash exceptions**: arrays (indexed/associative), extglob patterns, process substitution, controlled Bash environments
- **"Cleaner" or "fewer lines" is NOT sufficient justification** for Bash
- **Scripts must be compatible with `/bin/sh`** on any POSIX-compliant system
- **Use `#!/bin/sh`** - Never use `#!/bin/bash` or `#!/usr/bin/env bash` without enumerated exception

Shell scripting standards following pure POSIX sh (not bash).

## Core Principle

**Default to POSIX sh for all scripts unless you can explicitly enumerate which Bash-specific feature is strictly required and impossible to replicate in POSIX sh.**

Treat complexity as a cost, not a feature. Choose Bash only when:

1. **You need arrays** (indexed or associative) for data structures that cannot be reasonably flattened to strings/positional params
2. **You require glob matching** with extglob patterns
3. **You need process substitution** for feeding command output as a file descriptor
4. **You're scripting exclusively for Bash environments** (NixOS activation scripts, Git hooks on controlled systems)

**If the justification is merely "it's cleaner" or "fewer lines," that is not sufficient** — POSIX sh is the correct choice.

Scripts must be compatible with `/bin/sh` on any POSIX-compliant system unless one of the above exceptions applies.

## Shebang

Always use:
```bash
#!/bin/sh
```

Never use `#!/bin/bash` or `#!/usr/bin/env bash`.

## File Header

All shell scripts must include the full Unlicense header:

```bash
#!/bin/sh

# script_name: brief description
# --------------------------------
# by mark <mark@joshwel.co>
#
# This is free and unencumbered software released into the public domain.
#
# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.
#
# In jurisdictions that recognize copyright laws, the author or authors
# of this software dedicate any and all copyright interest in the
# software to the public domain. We make this dedication for the benefit
# of the public at large and to the detriment of our heirs and
# successors. We intend this dedication to be an overt act of
# relinquishment in perpetuity of all present and future rights to this
# software under copyright law.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# For more information, please refer to <http://unlicense.org/>
```

## Variables

### Naming

Use UPPER_CASE for environment variables and constants:

```bash
# defaults
SURPLUS_CMD_DEFAULT="surplus -td"
LOCATION_TIMEOUT=50

# environment overrides with defaults
SURPLUS_CMD="${SURPLUS_CMD:-$SURPLUS_CMD_DEFAULT}"
LOCATION_CMD="${LOCATION_CMD:-$LOCATION_CMD_DEFAULT}"
```

### Local Variables

Use lower_case for local/script variables:
```bash
status=0
bridge_failures=0
```

### Variable Expansion

Always quote variables to prevent word splitting:
```bash
# Good
mkdir -p "$SPOW_CACHE_DIR"
cat "$SPOW_NETLC_OUT" >>"$SPOW_SESH_OUT"

# Bad (unquoted)
mkdir -p $SPOW_CACHE_DIR
```

Use `${var:-default}` for defaults:
```bash
LOCATION_TIMEOUT="${LOCATION_TIMEOUT:-50}"
```

## Error Handling

### Message Format

Use the same format as `dev-standards-majo` (see that skill for full details):

```
program: level: message
```

**Examples:**
```bash
printf "s+ow: error: surplus is not installed\n" >&2
printf "s+ow: warn: using fallback location\n" >&2
printf "s+ow: info: starting location fetch\n" >&2
```

**Follow-up notes** for additional context:
```bash
printf "s+ow: error: location fetch failed\n" >&2
printf "... note: timeout was %d seconds\n" "$LOCATION_TIMEOUT" >&2
```

### Exit on Error

Use `set -e` at the top of scripts:
```bash
#!/bin/sh
set -e
```

### Command Checking

Check if commands exist before using:
```bash
if ! command -v "$SURPLUS_EXE" >/dev/null 2>&1; then
    printf "s+ow: error: surplus is not installed\n" >&2
    exit 2
fi
```

### Exit Codes

Use the grouping convention from `dev-standards-majo`:

| Range | Category |
|-------|----------|
| `0` | Success |
| `1-9` | Usage errors (bad args, missing env) |
| `10-19` | Input errors |
| `20-29` | File/IO errors |
| `255` | Runtime error |

**Example header:**
```bash
# exit codes:
# 0  - success
# 1  - bad command usage
# 2  - missing dependency
# 20 - file not found
```

## Control Structures

### Conditionals

Use POSIX test syntax:
```bash
if [ "$LOCATION_PRIORITISE_NETWORK" = "n" ]; then
    LOCATION_PRIORITISE_NETWORK=""
fi

# Check if variable is set
if [ -n "$SPOW_PRIVATE" ]; then
    SPOW_SESH_OUT="/dev/null"
fi

# Check if file exists and is non-empty
if [ -s "$SPOW_NETLC_OUT" ]; then
    printf "net"
fi
```

### Loops

Use POSIX-compliant loops:
```bash
# While loop with counter
while [ "$LOCATION_TIMEOUT" -gt 0 ]; do
    # ...
    LOCATION_TIMEOUT=$((LOCATION_TIMEOUT - 1))
done

# For loop over arguments
for arg in "$@"; do
    if [ "$arg" = "--search-here" ]; then
        search_here=true
    fi
done
```

## Functions

Define functions without the `function` keyword:
```bash
locate() {
    # spawn termux-location processes
    (
        $LOCATION_CMD -p "network" >"$SPOW_NETLC_OUT"
        if [ -s "$SPOW_NETLC_OUT" ]; then
            printf "net"
        fi
    ) &
    tl_net_pid="$!"
}
```

## Process Management

### Background Processes

Spawn background processes in subshells:
```bash
(
    $LOCATION_CMD -p "network" >"$SPOW_NETLC_OUT"
    if [ -s "$SPOW_NETLC_OUT" ]; then
        printf "net" | tee -a "$SPOW_SESH_ERR"
    fi
) &
tl_net_pid="$!"
```

### Waiting for Processes

Check if process is still running:
```bash
kill -0 "$tl_net_pid" >/dev/null 2>&1
tl_net_status="$?"

if [ "$tl_net_status" -eq 1 ]; then
    # Process finished
    break
fi
```

## Output

### printf vs echo

Always use `printf` instead of `echo`:
```bash
# Good
printf "s+ow: error: surplus is not installed.\n"
printf "running '%s'" "$LOCATION_CMD"

# Bad (non-portable)
echo "message"
```

### Redirection

Redirect stderr appropriately:
```bash
# Suppress output
command -v "$SURPLUS_EXE" >/dev/null 2>&1

# Redirect to file
cat "$SPOW_NETLC_OUT" >>"$SPOW_SESH_OUT"
```

## Common Patterns

### Checking File Existence

```bash
# File exists
if [ -e "$file" ]; then
    ...
fi

# File exists and is non-empty
if [ -s "$file" ]; then
    ...
fi

# Directory exists
if [ -d "$dir" ]; then
    ...
fi
```

### String Operations

```bash
# Extract command name
TERMUX_EXE=$(echo "$TERMUX_CMD" | awk '{print $1}')

# Pattern matching with case
case "$arg" in
    "--search-here")
        search_here=true
        ;;
    "--plumbing")
        plumbing=true
        ;;
esac
```

### Arithmetic

Use POSIX arithmetic expansion:
```bash
LOCATION_TIMEOUT=$((LOCATION_TIMEOUT - 1))

# Check numeric comparison
if [ "$count" -gt 0 ]; then
    ...
fi
```

## Avoid Bashisms

### Don't Use

```bash
# Bash arrays - not POSIX
array=("item1" "item2")
echo "${array[0]}"

# [[ ]] test - not POSIX
if [[ "$var" == "value" ]]; then
    ...
fi

# $() command substitution is POSIX, but prefer it over backticks
output=$(command)

# let for arithmetic - not POSIX
let "count=count+1"

# source - not POSIX (use . instead)
source file.sh
```

### Do Use

```bash
# POSIX command substitution
output=$(command)

# POSIX test
if [ "$var" = "value" ]; then
    ...
fi

# POSIX arithmetic
result=$((a + b))

# POSIX source
. ./file.sh
```

## Shellcheck

Use shellcheck for linting:
```bash
# Check script
shellcheck script.sh

# Disable specific warnings with comments
# shellcheck disable=SC2059
LOCATION_FALLBACK="${LOCATION_FALLBACK:-"%d%d%d\nSingapore?"}"
```

## Testing Skills

- Run `shellcheck script.sh` - Should produce no warnings/errors
- Test on multiple shells: `dash script.sh`, `bash script.sh`, `sh script.sh`
- Check exit codes: Run with invalid args, missing files, verify proper codes
- Test variable quoting: Use paths with spaces to verify no word splitting
- Verify portability: Avoid `[[`, `source`, `let`, arrays unless in Bash exception

## Integration

This skill extends `dev-standards-majo`. Always ensure `dev-standards-majo` is loaded for:
- AGENTS.md maintenance
- Universal code principles
- Documentation policies

Works alongside:
- `git-majo` — For committing shell script changes
- `writing-docs-majo` — For writing shell script documentation
- `running-windows-commands-majo` — For shell scripting on Windows (Git Bash/WSL)
- `task-planning-majo` — For planning complex shell workflows
