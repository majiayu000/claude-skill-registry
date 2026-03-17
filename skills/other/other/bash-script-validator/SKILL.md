---
name: bash-script-validator
type: standard
depth: extended
description: >-
  Validates existing .sh/.bash scripts via ShellCheck 0.11.0+ static analysis, syntax/security/portability
  checks. Use when debugging SC codes, auditing shell scripts, or checking shell best practices.
---

# [H1][BASH-SCRIPT-VALIDATOR]
>**Dictum:** *Layered validation catches defects that single-pass analysis misses.*

<br>

Validate bash scripts via syntax check, ShellCheck 0.11.0+ static analysis, and data-driven custom checks.

**Tasks:**
1. Run `bash scripts/validate.sh <script-path>` — Syntax, static analysis, custom checks.
2. Review errors/warnings/info from output.
3. Reference docs/ for fix patterns:
   - [→shell-reference.md](./docs/shell-reference.md) — Bash 5.2+/5.3 vs POSIX sh, parameter expansion, FP patterns.
   - [→shellcheck-reference.md](./docs/shellcheck-reference.md) — SC codes, v0.11.0 additions, directives, CI integration.
   - [→text-tools.md](./docs/text-tools.md) — rg/sd/awk/regex, bash-native alternatives.
4. Suggest fixes — Before/after with line numbers.

---
## [1][VALIDATION_LAYERS]
>**Dictum:** *Each layer targets a distinct defect class.*

<br>

| [INDEX] | [LAYER]             | [CHECK]                                               | [TOOL]                              |
| :-----: | ------------------- | ----------------------------------------------------- | ----------------------------------- |
|   [1]   | **Syntax**          | `bash -n` / `sh -n`                                   | Built-in                            |
|   [2]   | **Static analysis** | SC codes, 4 severity levels (SC2327-SC2335 in 0.11)   | ShellCheck 0.11.0+                  |
|   [3]   | **Security**        | eval injection, unsafe rm, pipe-to-shell, dyn source  | `_SECURITY_CHECKS` dispatch table   |
|   [4]   | **Performance**     | UUOC, `$(cat)` -> `$(<)`, date subshell               | `_PERF_CHECKS` dispatch table       |
|   [5]   | **Portability**     | Bashisms in sh scripts (`[[`, arrays, `source`, `==`) | `_SH_BASHISM_CHECKS` dispatch table |
|   [6]   | **Best practice**   | printf > echo, `[[ ]]` > `[ ]`, mapfile > while-read  | `_PRACTICE_CHECKS` dispatch table   |

**Guidance:**<br>
- *Data-Driven:* Custom checks use `declare -Ar` tables with `"pattern|message|level"` format and generic nameref runner.
- *Architecture:* `_run_check_set()` iterates via `local -n _checks=$1`, splitting each entry with `IFS='|' read -r`.

---
## [2][EXIT_CODES]
>**Dictum:** *Exit codes enable pipeline composition.*

<br>

| [INDEX] | [CODE] | [MEANING]     |
| :-----: | :----: | ------------- |
|   [1]   | **0**  | Clean         |
|   [2]   | **1**  | Warnings only |
|   [3]   | **2**  | Errors found  |

---
## [3][FILE_MAP]
>**Dictum:** *File inventory enables targeted loading.*

<br>

| [INDEX] | [FILE]                             | [PURPOSE]                                                     |
| :-----: | ---------------------------------- | ------------------------------------------------------------- |
|   [1]   | **`scripts/validate.sh`**          | Main validator (shebang detection, assoc array counters).     |
|   [2]   | **`scripts/ensure_shellcheck.sh`** | Asserts shellcheck presence (Nix-provided; apt/dnf fallback). |
|   [3]   | **`docs/shell-reference.md`**      | Bash 5.2+/5.3 vs POSIX sh, FP patterns, data structures.      |
|   [4]   | **`docs/shellcheck-reference.md`** | SC codes, v0.11.0 additions, directives, CI.                  |
|   [5]   | **`docs/text-tools.md`**           | rg/sd/awk/regex, bash-native alternatives.                    |
|   [6]   | **`examples/good.sh`**             | Best practices (bash + POSIX).                                |
|   [7]   | **`examples/bad.sh`**              | Anti-patterns (bash + POSIX).                                 |

[REFERENCE]: [→shell-reference.md](./docs/shell-reference.md) — Language features, FP patterns.<br>
[REFERENCE]: [→shellcheck-reference.md](./docs/shellcheck-reference.md) — ShellCheck codes, directives.<br>
[REFERENCE]: [→text-tools.md](./docs/text-tools.md) — Modern text tools (rg/sd/awk), bash-native alternatives.
