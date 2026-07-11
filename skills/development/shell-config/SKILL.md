---
name: shell-config
description: "Shell configuration: Fish and Zsh setup, PATH, completions, plugins."
user-invocable: false
allowed-tools:
  - Read
  - Write
  - Bash
  - Grep
  - Glob
  - Edit
routing:
  category: process
  force_route: true
  not_for: "fishing for bugs (debugging), fishing for feedback (asking for input), 'fish out' as 'extract/find', fish (the animal), non-fish/zsh shells — only fires for Fish or Zsh shell configuration"
  triggers:
    - fish
    - fish shell
    - config.fish
    - abbr
    - fish function
    - fish_config
    - fish_variables
    - funced
    - funcsave
    - ~/.config/fish
    - conf.d
    - fish abbreviation
    - .fish file
    - "#!/usr/bin/env fish"
    - zsh
    - zsh shell
    - .zshrc
    - zshrc
    - .zshenv
    - zshenv
    - .zprofile
    - zprofile
    - compinit
    - fpath
    - autoload -Uz
    - oh-my-zsh
    - prezto
    - zinit
    - antigen
    - p10k
    - powerlevel10k
    - setopt
    - zsh completion
    - zsh function
    - zsh plugin
    - typeset -U
    - zplug
    - configure zsh
    - zsh config
  pairs_with: []
---

# Shell Configuration Skill

Unified skill for Fish and Zsh shell configuration. Detect the target shell first, then load the appropriate reference.

## Reference Loading Table

| Shell | Signal | Load | Why |
|---|---|---|---|
| Fish | Any Fish context | `fish-shell-config.md` | Full Fish config patterns, syntax, file layout |
| Fish | Migrations from Bash | `fish-bash-migration.md` | Bash-to-Fish syntax translation |
| Fish | Variable scope, PATH, abbr, completions | `fish-quick-reference.md` | Variable scope guide, special variables, control flow |
| Fish | Error audit, broken config | `fish-preferred-patterns.md` | Failure modes with grep detection and error-fix mappings |
| Fish | Dev tool integration | `fish-tool-integrations.md` | Fish integration patterns for Go, Rust, Node, Python, Docker |
| Zsh | Any Zsh context | `zsh-shell-config.md` | Full Zsh config patterns, RC files, frameworks, hooks |
| Zsh | Migrations from Bash | `zsh-bash-migration.md` | Bash-to-Zsh syntax translation |
| Zsh | Variable scoping, expansion flags, special vars | `zsh-quick-reference.md` | Parameter expansion flags, special variables |
| Zsh | Error audit, slow startup, glob errors | `zsh-preferred-patterns.md` | Failure modes with grep detection and error-fix mappings |
| Zsh | Dev tool integration | `zsh-tool-integrations.md` | Zsh integration patterns for Go, Rust, Node, Python, Docker |

## Instructions

### Step 1: Detect Shell Type

Before loading references or writing code, determine the target shell:

- **Fish**: `$SHELL` contains `fish`, target file has `.fish` extension, or target directory is `~/.config/fish/`
- **Zsh**: `$SHELL` contains `zsh`, target file is `.zshrc`/`.zshenv`/`.zprofile`, or has `.zsh` extension

If neither Fish nor Zsh, this skill does not apply.

### Step 2: Load Shell-Specific Reference

Load the appropriate reference file from the table above based on the detected shell and the task signal. Start with the full config reference (`fish-shell-config.md` or `zsh-shell-config.md`), then load additional references as needed.

### Step 3: Follow Shell-Specific Patterns

Each reference contains complete instructions for that shell. Follow them exactly — Fish and Zsh have incompatible syntax in many areas (variable assignment, PATH handling, conditionals, completions).

**Key differences**:

| Concept | Fish | Zsh |
|---------|------|-----|
| Variable assignment | `set -gx VAR value` | `export VAR=value` |
| PATH management | `fish_add_path` | `typeset -U path; path=(...)` |
| Completions | `completions/` directory | `compinit` + `fpath` |
| Conditionals | `test`, not `[[ ]]` | `[[ ]]` preferred |
| Functions | `function name ... end` | `function name { ... }` |
| Interactive guard | `status is-interactive` | `[[ -o interactive ]]` |
