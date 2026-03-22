---
name: fish-shell-scripting
description: Fish shell scripting judgment frameworks and critical idioms. Use when writing Fish scripts or shell automation. Focuses on when to use Fish vs bash, macOS/Fedora compatibility requirements, and Fish-specific patterns that prevent bugs (universal variable anti-patterns, wrapper functions, interactive guards).
---

# Fish Shell Scripting

**Related skills:**
- `software-engineer` - General scripting design principles
- `python-programmer` - When shell complexity exceeds ~100 lines, consider Python

<core_philosophy>
**Fish is a user-friendly shell that prioritizes correctness over POSIX compatibility.** Its lists-not-strings semantics eliminates entire classes of bugs common in bash/zsh. The limitation is portability, not capability.

**Key insight**: Fish handles sophisticated automation well. Choose Fish when you control the environment; choose bash when you don't.
</core_philosophy>

## Platform Requirements

<platform_requirements>
**Compatibility**: All Fish scripts MUST work on both macOS and Fedora Linux. Handle platform differences via `uname` detection.

**Quote paths with spaces**: Always quote file paths even though Fish has no word splitting. Fish doesn't need quotes technically (no word splitting), but quoting anyway: (1) makes intent explicit for readability, (2) builds consistent habits when switching between shells, (3) ensures compatibility when passing to external commands that may interpret spaces.

**Shebang**: Use `#!/usr/bin/env fish` for portability across installation locations.
</platform_requirements>

## When to Use Fish vs Other Tools

<fish_vs_alternatives>
**Use Fish for:**
- Automation on systems where Fish is installed (dev environments, personal machines, containers you control)
- Scripts benefiting from lists-not-strings semantics and strong scoping
- Complex CLI tools requiring argument parsing (`argparse` + `fish_opt`)
- Docker/container orchestration, dotfiles, local tooling

**Use bash for:**
- POSIX compliance requirements or `/bin/sh` compatibility
- CI/CD pipelines in uncontrolled environments
- Distribution to users who may not have Fish

**Use a programming language for:**
- Heavy data structure manipulation or API processing
- When shell semantics aren't the primary concern
- Scripts exceeding ~100 lines with complex logic
</fish_vs_alternatives>

## Critical Differences from POSIX Shells

<posix_differences>
**No word splitting**: Variables don't split on spaces. `set name "foo bar"; echo $name` is one argument. This eliminates a major source of bugs in bash/zsh.

**All variables are lists**: A "string" is a one-element list. Indexing is 1-based: `$PATH[1]`, `$PATH[-1]`.

**No `VAR=value` syntax**: Use `set` command. `set -gx VAR value` (global exported), `set -lx VAR value` (local exported).

**Command substitution splits on newlines only**: `set lines (cat file)` creates one element per line. For space-splitting: `string split " "`.
</posix_differences>

## Scoping

<scoping_decision>
**Choosing a scope:**

| Need | Scope | Example Use Case |
|------|-------|------------------|
| Temporary within function/block | `-l` | Loop variables, intermediate results |
| Shared across session | `-g` | Current project settings, temporary overrides |
| Available to child processes | `-gx` or `-lx` | PATH, EDITOR, build flags |
| Persist across sessions (Fish UI only) | `-U` | fish_color_*, key bindings, prompt config |

**Flag combinations:**
- **`-l`** (local): Dies when block ends
- **`-g`** (global): Session-scoped, not inherited by child processes
- **`-x`** (exported): Available to child processes (combine with `-g` or `-l`)
- **`-U`** (universal): Persists across all sessions, survives reboots

**Example**: `set -gx EDITOR vim` (global + exported), `set -lx DEBUG 1` (local + exported to children).

**CRITICAL**: Environment variables (PATH, EDITOR, etc.) should NEVER be universal. Universal scope is for Fish UI config only.
</scoping_decision>

## Universal Variable Anti-Pattern

<universal_variable_antipattern>
**NEVER use universal variables for PATH or environment variables**. Universal scope is for Fish UI config only (colors, key bindings, prompt).

**Why this matters**: Universal variables persist to disk and are shared across all Fish sessions. If you append to PATH in config.fish using universal variables, it grows indefinitely on every shell start because:
1. config.fish runs on every session
2. Universal variable already contains previous value
3. Append adds duplicate entries
4. This compounds across reboots

```fish
# WRONG: Grows PATH indefinitely on every shell start
set -U fish_user_paths ~/bin $fish_user_paths

# RIGHT: Session-scoped (recalculated fresh each session)
set -gx PATH ~/bin $PATH

# RIGHT: Use fish_add_path once interactively (idempotent, uses universal internally)
fish_add_path ~/bin
```

**Safe universal variable uses**: `fish_color_*`, `fish_key_bindings`, `fish_prompt`, `fish_greeting`.
</universal_variable_antipattern>

## Cross-Platform Patterns

<cross_platform>
**OS detection**: `switch (uname); case Darwin; ...; case Linux; ...; end`

**Conditional PATH**: `test -d ~/.cargo/bin; and fish_add_path ~/.cargo/bin`

**Platform-specific utilities to watch for**:
- GNU vs BSD commands: `sed`, `find`, `date`, `stat`, `readlink` behave differently
- Package managers: Homebrew (macOS) vs DNF (Fedora)
- Paths: `/usr/local/bin` (macOS Homebrew) vs `/usr/bin` (Fedora)
</cross_platform>

## Critical Idioms

<critical_idioms>
**Wrapper functions require `--wraps` and `$argv`**:
```fish
function ls --wraps=ls --description "ls with color"
    command ls --color=auto $argv
end
```
- Without `--wraps=ls`: Completions break (Fish doesn't know what command to complete for)
- Without `$argv`: Arguments are swallowed (user's flags/paths ignored)

**Argument parsing**: Use `argparse` + `fish_opt` for complex CLI tools. Check flags with `set -q _flag_name`.

**Guard interactive code**: Non-interactive shells (SSH, rsync) execute config.fish. Guard output:
```fish
if status is-interactive
    echo "Welcome!"
end
```
Without this guard: SSH file transfers, rsync, and scp can fail because unexpected output corrupts the protocol.

**Use `string` builtin**: Prefer `string match`, `string split` over external `grep`/`cut`. Benefits: faster execution (no fork), consistent cross-platform behavior, proper exit codes.

**and/or for control flow**: Chain commands with `and`/`or`, not just `&&`/`||`. Both work, but `and`/`or` are Fish's native idiom.
</critical_idioms>

## Organization

<organization_decisions>
| Content Type | Location | Why |
|--------------|----------|-----|
| Functions (reusable commands) | `~/.config/fish/functions/name.fish` | Autoloaded on first use, not at startup—keeps shell fast |
| Topical config (per-tool setup) | `~/.config/fish/conf.d/tool.fish` | Auto-sourced alphabetically, keeps concerns separated |
| Interactive-only setup | `config.fish` with `status is-interactive` | Guards against breaking non-interactive use |
| Environment variables | `conf.d/` with `set -gx` | Session-scoped, recalculated fresh each session |

**Minimal `config.fish`**: Keep it to ~15 lines of orchestration. Put actual config in `conf.d/` files.

**Autoload advantage**: Functions in `functions/` are loaded only when first called, not at startup. This keeps shell startup fast even with many custom functions.
</organization_decisions>

## Common Mistakes

<common_mistakes>
### From Bash Users

<from_bash>
- **Using `VAR=value` syntax**: Fish uses `set VAR value`. The `VAR=value command` pattern doesn't exist.
- **Expecting word splitting**: `set x "foo bar"; echo $x` is ONE argument in Fish. This is a feature, not a bug.
- **Using `export VAR=value`**: Fish uses `set -gx VAR value` (global exported).
- **Using `$(...)`**: Fish uses `(...)` for command substitution, not `$(...)`.
- **Using `&&`/`||` exclusively**: Works in Fish, but `and`/`or` are the native idiom.
- **Using `[[...]]` tests**: Fish uses `test` or `[...]`, not bash's `[[...]]`.
</from_bash>

### From Zsh Users

<from_zsh>
- **Array indexing from 0**: Fish arrays are 1-indexed like zsh, but syntax differs: `$array[1]` not `$array[1]` or `${array[1]}`.
- **Expecting `setopt`/`unsetopt`**: Fish configuration works differently—use `set -U` for persistent settings.
- **Using zsh-specific globbing**: Fish globbing is simpler; complex patterns may need different approaches.
</from_zsh>

### From Any Shell Background

<from_any_shell>
- **Appending to universal variables in config.fish**: Creates infinite PATH growth. Use `set -gx` or one-time `fish_add_path`.
- **Not guarding interactive code**: Breaks SSH/rsync file transfers with protocol errors.
- **Forgetting `$argv` in wrapper functions**: Silently swallows all user arguments.
- **Using `(whoami)` instead of `$USER`**: Unnecessary subshell; environment variable is faster.
- **Using `(hostname)` instead of `$hostname`**: Same issue—use the variable.
- **Using `alias` instead of `abbr`**: Abbreviations expand visibly in history, making commands reproducible. Aliases hide what actually ran.
- **Treating universal variables like environment variables**: Universal is for Fish UI config only (colors, bindings, prompt).
</from_any_shell>
</common_mistakes>

## Resources

<resources>
**Online Documentation:**
- **Fish Documentation**: https://fishshell.com/docs/current/
- **Fish Tutorial**: https://fishshell.com/docs/current/tutorial.html
- **Fish FAQ (common gotchas)**: https://fishshell.com/docs/current/faq.html
- **Fish for Bash Users**: https://fishshell.com/docs/current/fish_for_bash_users.html

**Local Documentation:**

Typical locations (check these paths directly):
- macOS (Homebrew Apple Silicon): `/opt/homebrew/share/doc/fish/`
- macOS (Homebrew Intel): `/usr/local/share/doc/fish/`
- Fedora/Linux: `/usr/share/doc/fish/`

Man pages:
- macOS (Homebrew Apple Silicon): `/opt/homebrew/share/man/man1/fish*.1`
- macOS (Homebrew Intel): `/usr/local/share/man/man1/fish*.1`
- Fedora/Linux: `/usr/share/man/man1/fish*.1`

To find dynamically (from Fish shell):
```fish
ls "$(dirname (realpath (command -s fish)))/../share/doc/fish"
```
</resources>
