---
name: zsh-shell-config
description: "Zsh shell configuration, PATH management, completions, and framework setup."
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
  not_for: "not for non-zsh shells — only fires for Zsh configuration"
  triggers:
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
  force_route: true
---

# Zsh Shell Configuration Skill

Zsh is POSIX-compatible with powerful extensions. Every pattern here targets Zsh 5.8+ (ships with macOS 14+, Ubuntu 22.04+). All generated code must use Zsh-native syntax — `typeset`/`local` for scoping, `path` array for PATH, `compinit` for completions.

## Reference Loading Table

| Signal | Load These Files | Why |
|---|---|---|
| migrations, bash syntax, POSIX shell | `bash-migration.md` | Bash→Zsh syntax translation table with code blocks for each pattern |
| parameter expansion, scoping, special vars, fpath | `zsh-quick-reference.md` | Variable flags, expansion flags `${(f)}` `${(s)}` `${(j)}`, special variables |
| implementation patterns, failure modes, detection commands | `zsh-preferred-patterns.md` | Pattern catalog with grep detection and error-fix mappings |
| Go, Rust, Node, Python, starship, direnv, fzf, zoxide, mise | `tool-integrations.md` | Concrete zsh integration patterns for common dev tools |

## Step 1: Confirm Zsh Context

Before writing any shell code, confirm the target is Zsh:

- `$SHELL` contains `zsh`, or
- Target file has `.zsh` extension, or
- Target file is one of: `.zshrc`, `.zshenv`, `.zprofile`, `.zlogin`, `.zlogout`

If none hold, this skill does not apply — route to fish-shell-config or bash.

## Step 2: Choose the Correct RC File

Zsh sources startup files in a defined order depending on shell type (login vs. interactive).

**Load order**:

| File | Sourced when | Use for |
|------|-------------|---------|
| `~/.zshenv` | Every zsh invocation (login, interactive, script) | `$PATH`, `$EDITOR`, `$LANG` — variables needed by all processes |
| `~/.zprofile` | Login shells only (before `.zshrc`) | Login-time setup (e.g., `eval "$(brew shellenv)"`) |
| `~/.zshrc` | Interactive shells only | Aliases, functions, completions, prompt, key bindings |
| `~/.zlogin` | Login shells (after `.zshrc`) | Rarely used; message-of-the-day type hooks |
| `~/.zlogout` | Login shell exit | Cleanup on logout |

**Decision tree**:

| What you're writing | Where it goes |
|---------------------|---------------|
| `PATH`, `EDITOR`, `LANG`, `GOPATH` | `~/.zshenv` |
| Homebrew / nix / login-time init | `~/.zprofile` |
| Aliases, functions, `compinit`, prompt | `~/.zshrc` |
| Key bindings (`bindkey`) | `~/.zshrc` |
| `setopt` / `unsetopt` | `~/.zshrc` |
| Framework (oh-my-zsh, prezto) | `~/.zshrc` |

Place env vars in `~/.zshenv` not `~/.zshrc` — scripts and non-interactive shells source `.zshenv` only, so exported variables must live there to reach child processes started from scripts.

## Step 3: Manage PATH

Zsh uses `path` as an array tied to `$PATH`. Use `typeset -U path` to deduplicate automatically.

```zsh
# ~/.zshenv — PATH management
typeset -U path           # Enforce unique entries; run once at top of file

path=(
  ~/bin
  ~/.local/bin
  $path                   # Preserve existing entries
)
export PATH               # Re-export after array modification
```

**fpath and autoload**:

```zsh
# Add completion directories to fpath before compinit
typeset -U fpath
fpath=(~/.zsh/completions $fpath)

# Autoload functions from fpath
autoload -Uz compinit     # -U: no alias expansion; -z: zsh-style autoload
autoload -Uz add-zsh-hook
autoload -Uz vcs_info

# Completion cache: only re-init once per day
if [[ -n ~/.zcompdump(#qN.mh+24) ]]; then
  compinit
else
  compinit -C             # -C: skip security check, use cached dump
fi
```

`~/.zcompdump` caches completion definitions. Without the age guard, `compinit` rescans all fpath entries on every shell start — adds 100–300ms of startup time.

## Step 4: Write Variables and Functions

**Variable scoping**:

```zsh
local var="value"          # Local to current function
typeset -i count=0         # Integer
typeset -l lower="VALUE"   # Auto-lowercased
typeset -u upper="value"   # Auto-uppercased
typeset -r CONST="fixed"   # Read-only
typeset -x EXPORTED="val"  # Export (same as export)
typeset -a arr             # Indexed array
typeset -A assoc           # Associative array
```

**Functions**:

```zsh
# Regular function
mkcd() {
  mkdir -p "$1" && cd "$1"
}

# Alternative (preferred in zsh): function keyword
function mkcd {
  mkdir -p "$1" && cd "$1"
}

# Autoloaded function (place in a fpath directory as a standalone file)
# ~/.zsh/functions/mkcd — file contains only the function body:
# mkdir -p "$1" && cd "$1"
# Then in .zshrc: autoload -Uz mkcd
```

For autoloaded functions, the file must be named exactly after the function and live in a `fpath` directory.

## Step 5: Completions

```zsh
# ~/.zshrc — completions setup

# 1. Extend fpath before compinit
fpath=(~/.zsh/completions $fpath)

# 2. Initialize (with cache guard)
autoload -Uz compinit
compinit

# 3. Key completion options
setopt COMPLETE_IN_WORD     # Complete from both ends of word
setopt ALWAYS_TO_END        # Move cursor to end after completion
setopt AUTO_MENU            # Show menu on second Tab
setopt MENU_COMPLETE        # Auto-select first match
zstyle ':completion:*' menu select

# 4. Styling completions
zstyle ':completion:*' matcher-list 'm:{a-z}={A-Z}'   # Case-insensitive
zstyle ':completion:*' list-colors "${(s.:.)LS_COLORS}"
zstyle ':completion:*:descriptions' format '%B%d%b'
zstyle ':completion:*:warnings' format 'No matches for: %d'

# 5. Add a completion function for a custom command
# ~/.zsh/completions/_mycommand
# #compdef mycommand
# _mycommand() {
#   local -a commands
#   commands=('start:Start the service' 'stop:Stop the service')
#   _describe 'commands' commands
# }
```

## Step 6: Framework Awareness

Detect active framework before adding configuration — frameworks own the prompt, completion init, and plugin loading.

**Detection patterns**:

```zsh
# oh-my-zsh
[[ -n "$ZSH" ]] && echo "oh-my-zsh active (ZSH=$ZSH)"
[[ -f ~/.oh-my-zsh/oh-my-zsh.sh ]] && echo "oh-my-zsh installed"

# prezto
[[ -d ~/.zprezto ]] && echo "prezto installed"

# zinit
[[ -d ~/.zinit ]] || [[ -d ~/.local/share/zinit ]] && echo "zinit installed"

# antigen
command -v antigen &>/dev/null && echo "antigen active"

# powerlevel10k / p10k
[[ -f ~/.p10k.zsh ]] && echo "p10k config present"
```

**Framework coexistence rules**:

| Situation | Action |
|-----------|--------|
| oh-my-zsh active | Place custom config in `~/.oh-my-zsh/custom/` — not directly in `.zshrc` |
| prezto active | Use `~/.zpreztorc` modules; add extra config after `source ~/.zprezto/init.zsh` |
| zinit active | Add plugins with `zinit light`; place after zinit bootstrap block |
| p10k active | Call `[[ -f ~/.p10k.zsh ]] && source ~/.p10k.zsh` after framework init |
| No framework | Full control — structure `.zshrc` with `compinit`, prompt, plugins manually |

When a framework manages `compinit`, do not call `compinit` again — double-init causes duplicate completion definitions and slows startup.

## Step 7: Hooks

Zsh hooks fire at defined shell events. Use `add-zsh-hook` to attach — it preserves existing handlers for the same event.

```zsh
autoload -Uz add-zsh-hook

# precmd: runs before each prompt (use for vcs_info, title updates)
_my_precmd() {
  print -Pn "\e]0;%~\a"   # Set terminal title to current dir
}
add-zsh-hook precmd _my_precmd

# preexec: runs before each command (receives command string as $1)
_my_preexec() {
  print -Pn "\e]0;$1\a"   # Set terminal title to running command
}
add-zsh-hook preexec _my_preexec

# chpwd: runs when directory changes
_my_chpwd() {
  ls --color=auto           # Auto-list on cd
}
add-zsh-hook chpwd _my_chpwd

# zshaddhistory: runs before adding command to history; return 1 to suppress
_no_history() {
  [[ "$1" == " "* ]] && return 1   # Leading space = skip history
  return 0
}
add-zsh-hook zshaddhistory _no_history
```

Writing `precmd() { ... }` directly overwrites any previously defined `precmd` — `add-zsh-hook` appends to the hook array instead.

## Step 8: Zsh Options

```zsh
# History
setopt HIST_IGNORE_DUPS       # Ignore consecutive duplicates
setopt HIST_IGNORE_SPACE      # Ignore commands starting with space
setopt HIST_EXPIRE_DUPS_FIRST # Expire duplicates first when trimming
setopt HIST_FIND_NO_DUPS      # No dups in history search
setopt SHARE_HISTORY          # Share history across sessions
setopt APPEND_HISTORY         # Append rather than overwrite
setopt INC_APPEND_HISTORY     # Write immediately, not on exit
HISTFILE=~/.zsh_history
HISTSIZE=50000
SAVEHIST=50000

# Globbing
setopt EXTENDED_GLOB          # Enable (#q...) glob qualifiers and ^ ~
setopt NULL_GLOB              # No-match globs expand to empty (no error)
setopt GLOB_DOTS              # Dot files matched by * patterns

# Behavior
setopt PIPE_FAIL              # Pipeline exit code = first failed command
setopt NO_CLOBBER             # Prevent > from overwriting files
setopt AUTO_CD                # cd by typing directory name alone
setopt CORRECT                # Suggest corrections for mistyped commands
setopt NO_BEEP                # Silence

# Key options to unset
unsetopt BG_NICE              # Background jobs run at normal priority
unsetopt FLOW_CONTROL         # Disable Ctrl+S/Ctrl+Q flow control
```

**Critical options**:

| Option | Effect | Recommend |
|--------|--------|-----------|
| `PIPE_FAIL` | Pipeline returns exit code of first failed command | Always set |
| `NULL_GLOB` | Unmatched globs expand to empty list | Set to avoid "no matches" errors |
| `EXTENDED_GLOB` | Enables `^`, `~`, `(#q...)` qualifiers | Set when using glob qualifiers |
| `HIST_IGNORE_SPACE` | Commands prefixed with space skip history | Set for sensitive commands |
| `SHARE_HISTORY` | Multiple sessions share history in real time | Set for multi-terminal workflows |

## Step 9: Verify

```zsh
# 1. Syntax check without sourcing
zsh -n ~/.zshrc

# 2. Run in isolated environment (no user config)
zsh --no-rcs -c 'source ~/.zshrc; echo ok'

# 3. Profile startup time
time zsh -i -c exit

# 4. Trace file loading order
zsh --sourcetrace -i -c exit 2>&1 | head

# 5. Profile compinit specifically
zsh -i -c 'zmodload zsh/zprof; compinit; zprof' 2>&1 | head -20
```

**Glob quoting pitfalls**: With `EXTENDED_GLOB` set, `^`, `~`, and `#` are active in unquoted contexts. Quote them in strings: `echo "it's ~fine"` passes literally; `echo it's ~fine` expands `~fine` as a path.

**NULL_GLOB vs no-match error**: Without `NULL_GLOB`, `rm *.tmp` fails with "no matches" when no `.tmp` files exist. With `NULL_GLOB`, `rm *.tmp` expands to `rm` with no arguments (also an error). Use glob qualifier `(N)` for conditional expansion: `rm -- *.tmp(N)` silently does nothing when there are no matches.

---

## Error Handling

### Error: `compinit: insecure directories`

Cause: Files in `fpath` are group- or world-writable.
Solution: `compaudit` lists the offending paths. Fix with `chmod go-w /path` or pass `-u` flag: `compinit -u` (unsafe — skips ownership check).

### Error: Completions not found after adding to fpath

Cause: `compinit` was called before the `fpath` extension, or `~/.zcompdump` is stale.
Solution: Move `fpath=(~/.zsh/completions $fpath)` above `compinit`. Delete `~/.zcompdump` and restart shell to regenerate.

### Error: `add-zsh-hook: function not found`

Cause: `autoload -Uz add-zsh-hook` was not called before using the hook.
Solution: Add `autoload -Uz add-zsh-hook` before any `add-zsh-hook` call — typically at the top of `.zshrc`.

### Error: PATH additions not visible to scripts

Cause: Variables set in `~/.zshrc` are not sourced by non-interactive shells.
Solution: Move `PATH` exports to `~/.zshenv` — it is sourced by every Zsh invocation including scripts.

### Error: Slow shell startup (>300ms)

Cause: `compinit` rescanning all fpath entries on every start; heavy plugin loading.
Solution: Add the `~/.zcompdump` age guard (see Step 3). Profile with `zmodload zsh/zprof; compinit; zprof`. Use `zinit` or lazy-loading for plugins.

### Error: `zsh -n` reports syntax error in valid-looking code

Cause: `EXTENDED_GLOB` patterns like `^` or `#` in unquoted strings parsed as glob operators.
Solution: Quote strings containing these characters. Check with `setopt NO_EXTENDED_GLOB` temporarily to isolate.

---

## References

| Task Signal | Load | Why |
|-------------|------|-----|
| Migrating from Bash, converting `.bashrc`, `export VAR=`, `[[ ]]`, arrays, heredocs | `bash-migration.md` | Full Bash→Zsh syntax translation table |
| Variable scoping, `typeset` flags, `${(f)}` `${(s:,:)}` expansion, `$REPLY`, `$MATCH` | `zsh-quick-reference.md` | Parameter expansion flags, special variables, control flow cheatsheet |
| Error audit, PATH not persisting, completions slow, glob errors, hook not firing | `zsh-preferred-patterns.md` | Failure modes with grep detection commands and error-fix mappings |
| Go, Rust, Docker, Node.js, Python, pyenv, fnm, starship, direnv, fzf, zoxide, mise | `tool-integrations.md` | Concrete integration patterns for common dev tools |

- `${CLAUDE_SKILL_DIR}/references/bash-migration.md`: Complete Bash-to-Zsh syntax translation table
- `${CLAUDE_SKILL_DIR}/references/zsh-quick-reference.md`: Variable scoping, parameter expansion flags, and special variables
- `${CLAUDE_SKILL_DIR}/references/zsh-preferred-patterns.md`: Failure mode catalog with grep detection commands and error-fix mappings
- `${CLAUDE_SKILL_DIR}/references/tool-integrations.md`: Concrete integration patterns for Go, Rust, Docker, Node.js, Python, and shell enhancers
