---
name: bash-script-generator
type: standard
depth: extended
description: >-
  Generates production-ready bash 5.2+/5.3 scripts with strict mode, immutable locals, dispatch tables, and functional patterns.
  Use when creating new .sh scripts, CLI tools, cron jobs, deployment automation, text processing workflows, or log analyzers.
---

# [H1][BASH-SCRIPT-GENERATOR]
>**Dictum:** *Functional patterns and strict mode produce maintainable shell automation.*

<br>

Generate bash scripts with immutable locals, dispatch tables, pure functions, and zero mutable state.

**Tasks:**
1. Clarify requirements — Purpose, I/O, shell type, args, error strategy, performance constraints.
2. Read [bash-scripting-guide.md](./docs/bash-scripting-guide.md) — Strict mode, parameter expansion, arrays, bash 5.2/5.3 features.
3. Read [script-patterns.md](./docs/script-patterns.md) — Argument parsing, logging, parallel processing, retry, signals.
4. Read [text-processing-guide.md](./docs/text-processing-guide.md) — rg/awk/sd selection, pipeline patterns, performance.
5. Structure script — Shebang + strict mode + readonly constants + trap + main.
6. Implement — Core functions, business logic, main entry point.
7. Validate — `bash -n script.sh`, ShellCheck 0.11.0+, re-validate until clean.

---
## [1][REQUIREMENTS]
>**Dictum:** *Ambiguity resolution prevents rework.*

<br>

Clarify before generating:

| [INDEX] | [AMBIGUITY]    | [QUESTION]                                        |
| :-----: | -------------- | ------------------------------------------------- |
|   [1]   | Data format    | Input format? (nginx combined, JSON, CSV, custom) |
|   [2]   | Large files    | Files >100MB? Optimize for memory/performance?    |
|   [3]   | Error handling | Fail fast, continue with warnings, or retry?      |
|   [4]   | Portability    | POSIX sh portability or bash 5.2+/5.3?            |
|   [5]   | Output format  | Human-readable, JSON, or CSV?                     |

**Guidance:**
- *Architecture First:* Explain design, tool selection rationale, key tradeoffs before writing code.
- *Data Format Routing:* JSON? `jq`. YAML? `yq eval`. CSV/TSV? `miller` (mlr). Interactive exploration? `jnv`.
- *Template:* Reference `assets/templates/standard-template.sh` for production boilerplate.

---
## [2][STRICT_MODE]
>**Dictum:** *Strict mode prevents silent failures.*

<br>

```bash
#!/usr/bin/env bash
set -Eeuo pipefail          # -E = errtrace (ERR trap inherits into functions/subshells)
shopt -s inherit_errexit    # Command substitutions inherit errexit
IFS=$'\n\t'
```

**Guidance:**
- *Scope:* Every generated script includes this block. No exceptions.
- *Disable:* Temporarily suppress — `output=$(cmd 2>&1) || handle_error "${output}"`.

---
## [3][FUNCTIONAL_STYLE]
>**Dictum:** *Immutability and dispatch tables eliminate mutable state.*

<br>

| [INDEX] | [RULE]                | [PATTERN]                                                                  |
| :-----: | --------------------- | -------------------------------------------------------------------------- |
|   [1]   | Immutable locals      | `local -r` for all non-mutating variables inside functions                 |
|   [2]   | Immutable globals     | `readonly` for all module-level constants                                  |
|   [3]   | Pure functions        | Input via args, output via stdout or nameref (`local -n`), no global state |
|   [4]   | Dispatch tables       | `declare -Ar` for O(1) routing; `case/esac` only for pattern matching      |
|   [5]   | Higher-order          | Pass function names as args; `local -n` nameref for array parameters       |
|   [6]   | Inline trivials       | Single-use < 3 lines: inline at call site                                  |
|   [7]   | Brace grouping        | `{ cmd1; cmd2; } > file` over `( ... )` (no subshell)                      |
|   [8]   | No mutable counters   | `${#arr[@]}`, `rg -c`, or `awk` pipelines for counting                     |
|   [9]   | `mapfile`/`readarray` | Over `while read` loops for array population (3-5x faster)                 |
|  [10]   | `printf` everywhere   | Over `echo` (handles escapes, format strings, no ambiguity)                |
|  [11]   | `$(<file)`            | Over `$(cat file)` (no fork)                                               |
|  [12]   | `printf -v`           | `printf -v var '%(%F %T)T' -1` over `$(date ...)` (no subshell)            |
|  [13]   | Here-strings          | `<<<` over `echo x \| cmd` pipelines                                       |
|  [14]   | BASH_REMATCH          | `[[ str =~ regex ]]` + `${BASH_REMATCH[N]}` over `rg -oP` / `sd`           |
|  [15]   | Assoc set             | `declare -Ar SET=([k]=1)` + `[[ -v SET[key] ]]` for O(1) membership        |
|  [16]   | IFS splitting         | `IFS=, read -ra parts <<< "$csv"` over `cut` / `awk -F,` for simple delim  |

**Best-Practices:**
- *Nameref Constraint:* Array variables cannot be namerefs, but namerefs can reference arrays.
- *Dispatch Declaration:* `declare -Ar` assigns on declaration line; separate assignment fails for readonly.
- *Structured Checks:* `declare -Ar CHECKS=([name]="pattern\|msg\|level")` + `IFS=\| read -r` for data-driven validation.

---
## [4][QUALITY_GATE]
>**Dictum:** *Checklists prevent omissions.*

<br>

[VERIFY] Generation:
- [ ] `#!/usr/bin/env bash` + `set -Eeuo pipefail` + `shopt -s inherit_errexit` + `IFS=$'\n\t'`.
- [ ] All variables quoted: `"${var}"`.
- [ ] Constants: `readonly UPPER_SNAKE`; locals: `local -r`; functions: `lower_snake()`.
- [ ] `printf -v var '%(%F %T)T' -1` for timestamps (no `$(date)` subshell).
- [ ] `[[ ]]` over `[ ]`; `<<<` over `echo |`; `<()` over temp files.
- [ ] Cleanup: `trap cleanup EXIT` (single trap, EXIT covers normal + signal exits).
- [ ] ShellCheck 0.11.0+ clean; no `eval` with user input; `$()` over backticks.
- [ ] Usage/help with examples; post-generation summary with tool selection rationale.

[REFERENCE]: [docs/bash-scripting-guide.md](./docs/bash-scripting-guide.md) — Language features, parameter expansion, arrays.
[REFERENCE]: [docs/script-patterns.md](./docs/script-patterns.md) — Argument parsing, logging, parallel, retry.
[REFERENCE]: [docs/text-processing-guide.md](./docs/text-processing-guide.md) — Tool selection, rg/awk/sd, performance.
