---
name: command-prompt
description: >
  · Write/debug shell commands, scripts, dotfiles, completions for zsh, bash, POSIX sh, fish. Triggers: 'shell', 'script', '.zshrc', '.bashrc', 'alias', 'completion', 'trap'. Not for CI blocks (use ci-cd).
license: MIT
compatibility: "Requires a POSIX-compatible shell. Zsh, bash, fish, or nushell for shell-specific features"
metadata:
  source: iuliandita/skills
  date_added: "2026-03-25"
  effort: medium
  argument_hint: "<task-or-shell>"
---

# Command Prompt: Shell Scripting and Configuration

Reference skill for writing commands, scripts, and configuration across Unix shells. Detects
the target shell from context and routes to the appropriate reference.

**Target versions** (May 2026):
- Zsh: 5.10
- Bash: 5.3
- Fish: 4.6
- Nushell: 0.111
- Tcsh: 6.24
- Dash: 0.5.13

## When to use

- Writing shell commands, scripts, or one-liners
- Configuring dotfiles (`.zshrc`, `.bashrc`, `.profile`, `config.fish`)
- Writing completions, shell functions, or aliases
- Porting scripts between shells
- Debugging shell-specific behavior (globbing, arrays, expansion, quoting)
- Setting up oh-my-zsh, starship, p10k, or other shell frameworks
- Choosing which shell to target for a new script
- Writing interactive commands on the user's local machine (zsh)

## When NOT to use

- Remote FreeBSD/OPNsense/pfSense commands - use **firewall-appliance** (handles tcsh/csh in the BSD context)
- Ansible shell/command modules - use **ansible** (module gotchas differ from raw shell)
- CI/CD pipeline shell blocks - use **ci-cd** (restricted environments, no interactive features)
- General Linux sysadmin that isn't shell-specific - just do the task directly

---

## AI Self-Check

Before returning any generated shell script or command, verify:

- [ ] Shebang matches the detected target shell (not assumed bash)
- [ ] `set -euo pipefail` (bash/zsh) or `set -eu` (POSIX sh) present in scripts
- [ ] All variables double-quoted (`"$var"`) unless word splitting is intentional
- [ ] No shell-isms from the wrong shell (no `[[ ]]` in `#!/bin/sh`, no `BASH_SOURCE` in zsh)
- [ ] Array indexing correct for the target shell (bash: 0-indexed, zsh: 1-indexed)
- [ ] `printf` used over `echo` for non-trivial output
- [ ] Glob safety guards in place (empty-glob case handled)
- [ ] No hardcoded paths for tools (`/usr/bin/git`) - use `command -v` or bare command names
- [ ] Temp files use `mktemp` with cleanup traps, not hardcoded `/tmp/foo`
- [ ] No secrets in command history (use `read -s` or environment variables)
- [ ] **Current source checked**: dated versions, CLI flags, API names, and support windows are verified against primary docs before repeating them
- [ ] **Hidden state identified**: local config, credentials, caches, contexts, branches, cluster targets, or previous runs are made explicit before acting
- [ ] **Verification is real**: final checks exercise the actual runtime, parser, service, or integration point instead of only linting prose or happy paths
- [ ] **Routing overlap checked**: overlapping skills, trigger terms, and "When NOT to use" boundaries are checked before returning guidance
- [ ] **Spec claims verified**: claims about tool behavior, output contracts, or repo conventions are checked against current docs, scripts, or skill files
- [ ] **Shell identified**: examples match POSIX sh, Bash, Zsh, or Fish semantics intentionally
- [ ] **Quoting tested**: paths with spaces, empty variables, and glob characters behave safely

---

## Performance

- Use builtins and stream processing for large inputs; avoid command substitution that buffers entire files.
- Prefer `rg`, `fd`, and targeted file lists when available, with portable fallbacks noted.
- Avoid spawning subshells inside tight loops when `xargs`, arrays, or shell builtins fit.


---

## Best Practices

- Default to `set -euo pipefail` only when the script is written to handle those semantics.
- Use `--` before user-controlled paths for commands that support it.
- Preview destructive expansions before `rm`, `mv`, `chmod`, `chown`, or recursive edits.


## Workflow

### Step 1: Detect the target shell

Before writing any shell code, determine the target shell. Check these signals in order:

| Signal | How to check | Routes to |
|--------|-------------|-----------|
| **Shebang** | First line of existing script | `#!/usr/bin/env zsh` -> zsh, `#!/usr/bin/env bash` -> bash, `#!/bin/sh` -> posix-sh |
| **File name/extension** | `.zsh`, `.zshrc`, `.zprofile`, `.zshenv` -> zsh; `.bash`, `.bashrc`, `.bash_profile` -> bash; `.fish`, `config.fish` -> fish |  |
| **User's shell** | Conversation context, `$SHELL` | User's local machine = zsh |
| **Task type** | What the script does | See routing below |

### Task-based routing

| Task | Target shell | Why |
|------|-------------|-----|
| Interactive commands on user's machine | **zsh** | User's default shell |
| Portable scripts (new) | **bash** | Widest deployment, good feature set |
| Docker/CI containers | **bash** or **sh** | Containers often lack zsh |
| Minimal Alpine/BusyBox scripts | **POSIX sh** | Only `ash`/`dash` available |
| BSD system administration | **tcsh** | FreeBSD default (but see firewall-appliance skill) |
| Cross-shell startup (env vars, PATH) | **POSIX sh** | `.profile` sourced by all POSIX shells |
| Maximum portability requirement | **POSIX sh** | Only standard guaranteed on all Unixes |

### Step 2: Load the right reference

| Target shell | Reference file |
|-------------|---------------|
| Zsh | `references/zsh.md` (~680 lines, 14 sections) |
| Bash | `references/bash.md` (~710 lines, 13 sections) |
| POSIX sh | `references/posix-sh.md` (~490 lines, 10 sections) |
| Fish, tcsh, nushell, others | `references/alt-shells.md` (~420 lines, 4 shells) |

**Don't load all references.** Pick the one that matches. If porting between two shells, load both.

### Step 3: Write code, then verify

Use the cross-shell comparison below for quick lookups. After writing, run through the
Verification Checklist at the bottom of this section.

---

## Quick Cross-Shell Comparison

| Feature | POSIX sh | Bash | Zsh | Fish |
|---------|----------|------|-----|------|
| Arrays | no (use `$@`) | 0-indexed | **1-indexed** | lists (1-indexed) |
| Assoc arrays | no | `declare -A` (4.0+) | `typeset -A` | no |
| Glob `**/` | no | `shopt -s globstar` | built-in | built-in |
| Failed glob | passes literal | passes literal | **error** | no match |
| `[[ ]]` | no | yes | yes | no (use `test`) |
| Process sub `<()` | no | yes | yes + `=()` | `(command \| psub)` |
| Word splitting | on unquoted `$var` | on unquoted `$var` | **no** | **no** |
| Arithmetic | `$(( ))` only | `$(( ))`, `(( ))`, `let` | `$(( ))`, `(( ))` | `math` |
| String lowercase | - | `${var,,}` | `${var:l}` | `string lower` |
| Completions | none | basic (bash-completion) | powerful (compsys) | powerful (built-in) |
| Config file | `.profile` | `.bashrc` | `.zshrc` | `config.fish` |
| Shebang | `#!/bin/sh` | `#!/usr/bin/env bash` | `#!/usr/bin/env zsh` | `#!/usr/bin/env fish` |
| Script safety | `set -eu` | `set -euo pipefail` | `set -euo pipefail` | N/A (strict by default) |
| Non-forking cmd sub | no | `${ cmd; }` (5.3+) | `${ cmd }` (5.10+) | no |

---

## Universal Patterns (All POSIX Shells)

These work in sh, bash, and zsh. Fish has different syntax for most of these - see the
alt-shells reference.

### Piping and redirection

| Pattern | Effect |
|---------|--------|
| `cmd1 \| cmd2` | Pipe stdout of cmd1 to stdin of cmd2 |
| `cmd > file` | Redirect stdout to file (overwrite) |
| `cmd >> file` | Redirect stdout to file (append) |
| `cmd 2> file` | Redirect stderr to file |
| `cmd &> file` | Redirect both stdout and stderr (bash/zsh, not POSIX) |
| `cmd 2>&1` | Redirect stderr to stdout |
| `cmd > /dev/null 2>&1` | Silence all output (POSIX-portable) |
| `cmd < file` | Feed file as stdin |
| `cmd <<'EOF'` | Here document (single-quoted delimiter = no expansion) |
| `cmd <<< "string"` | Here string (bash/zsh, not POSIX) |
| `cmd1 \| tee file \| cmd2` | Send stdout to both file and cmd2 |

### Chaining

| Pattern | Behavior |
|---------|----------|
| `cmd1 ; cmd2` | Run sequentially, ignore exit codes |
| `cmd1 && cmd2` | Run cmd2 only if cmd1 succeeds (exit 0) |
| `cmd1 \|\| cmd2` | Run cmd2 only if cmd1 fails (exit non-0) |
| `cmd &` | Run in background |
| `cmd1 && cmd2 \|\| cmd3` | Poor man's if/else (**not reliable** - cmd3 runs if cmd2 fails too) |

### Job control

| Command | Effect |
|---------|--------|
| `Ctrl+Z` | Suspend foreground job |
| `bg` / `bg %N` | Resume job in background |
| `fg` / `fg %N` | Resume job in foreground |
| `jobs` | List background jobs |
| `kill %N` | Kill job by number |
| `wait` | Wait for all background jobs |
| `wait $PID` | Wait for specific PID |
| `disown %N` | Detach job from shell (survives logout) |

### Signals and traps

```sh
# Cleanup on exit (works in sh, bash, zsh)
cleanup() {
    rm -f "$tmpfile"
}
trap cleanup EXIT INT TERM

# Ignore a signal
trap '' HUP

# Common signals: EXIT (0), HUP (1), INT (2), TERM (15), USR1 (10), USR2 (12)

# Graceful kill with SIGTERM -> wait -> SIGKILL escalation
kill_gracefully() {
    local pid=$1 timeout=${2:-5}
    kill -TERM "$pid" 2>/dev/null || return
    local i=0
    while kill -0 "$pid" 2>/dev/null && [ $i -lt $timeout ]; do
        sleep 1; i=$((i+1))
    done
    kill -0 "$pid" 2>/dev/null && kill -KILL "$pid"
}
```

**Interactive "kill by name" (zsh)** - covers search, space-safe names, confirm, TERM->KILL escalation:

```zsh
pk() {                                           # usage: pk <pattern>
    local pattern=$1 pids
    pids=(${(f)"$(pgrep -af -- "$pattern")"})    # -f matches full cmdline (spaces ok)
    (( $#pids )) || { print -u2 "no match"; return 1 }
    printf '%s\n' "${pids[@]}"                   # show PID + cmdline
    read -q "?kill these? [y/N] " || { print; return 1 }
    print
    for line in $pids; do kill_gracefully ${line%% *} 3; done
}
```

### Quoting rules

| Syntax | Expansion | Use for |
|--------|-----------|---------|
| `"double"` | `$var`, `$(cmd)`, `${param}` expand; `\` escapes | Most strings with variables |
| `'single'` | Nothing expands, completely literal | Regexes, JSON, strings with `$` or `!` |
| `$'ansi'` | `\n`, `\t`, `\'` interpreted (bash/zsh) | Strings needing literal control chars |
| `\char` | Escapes one character | Single special chars in unquoted context |

**Golden rule**: when in doubt, double-quote. `"$var"` is almost always correct. Unquoted `$var`
causes word splitting (in sh/bash) or glob expansion.

### Exit codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error |
| 2 | Misuse of shell builtin |
| 126 | Command found but not executable |
| 127 | Command not found |
| 128+N | Killed by signal N (e.g., 130 = Ctrl+C / SIGINT) |

### Common portable idioms

```sh
# Check if command exists
command -v git >/dev/null 2>&1 || { echo "git required" >&2; exit 1; }

# Default variable value
: "${VAR:=default}"       # set VAR to "default" if unset or empty
name="${1:-anonymous}"     # parameter default

# Temporary file (portable)
tmpfile=$(mktemp) || exit 1
trap 'rm -f "$tmpfile"' EXIT

# Read file line by line
while IFS= read -r line; do
    printf '%s\n' "$line"
done < file.txt

# Loop over glob results
for f in *.txt; do
    [ -e "$f" ] || continue    # guard against no matches (POSIX sh)
    echo "$f"
done
```

---

## Completions Quick Reference (Zsh)

Zsh's completion system (`compsys`) handles subcommand routing natively. Minimal working
example for a CLI tool with subcommands:

```zsh
#compdef mycli

_mycli() {
  local -a subcmds=(
    'init:Initialize a new project'
    'build:Build the project'
    'deploy:Deploy to target environment'
  )

  _arguments -C \
    '(-h --help)'{-h,--help}'[Show help]' \
    '1:command:->subcmd' \
    '*::arg:->args'

  case $state in
    subcmd) _describe 'command' subcmds ;;
    args)
      case $words[1] in
        deploy) _arguments '--env[Target environment]:env:(dev staging prod)' ;;
      esac
      ;;
  esac
}
```

Place in a file named `_mycli` on your `fpath`, then ensure the directory is registered:

```zsh
# In .zshrc, BEFORE compinit:
fpath=(~/.zsh/completions $fpath)
autoload -Uz compinit && compinit
```

Or source inline with `compdef _mycli mycli` (no fpath needed). The reference files have
deeper coverage: glob-qualified completions, `_files`, `_hosts`, `_values`, and async
completion patterns.

---

## Verification Checklist

Before returning any shell script, check:

- [ ] **Shebang matches the target shell.** `#!/usr/bin/env bash` for bash, `#!/usr/bin/env zsh` for zsh, `#!/bin/sh` for POSIX sh. Never `#!/bin/bash` (not portable across distros).
- [ ] **`set -euo pipefail`** present for bash and zsh scripts. For POSIX sh: `set -eu` (no `pipefail`).
- [ ] **Variables are quoted.** `"$var"` not `$var`, unless word splitting is intentional.
- [ ] **No shell-isms in the wrong shell.** No `[[ ]]` in `#!/bin/sh`. No `BASH_SOURCE` in zsh. No bash arrays in POSIX sh.
- [ ] **Glob safety.** POSIX sh: guard with `[ -e "$f" ] || continue`. Zsh: use `(N)` qualifier. Bash: `shopt -s nullglob` or guard.
- [ ] **Array indexing matches the shell.** Bash: 0-indexed. Zsh: 1-indexed. POSIX sh: no arrays.
- [ ] **`printf` over `echo`** for anything non-trivial (echo behavior varies across shells and platforms).

---

## Reference Files

- `references/zsh.md` - Zsh 5.9/5.10 patterns, glob qualifiers, arrays, parameter expansion, completions, autoloading, dotfile config, prompt hooks, zsh-only features, 5.10 additions (non-forking `${ }`, namerefs, SRANDOM), bash porting matrix
- `references/bash.md` - Bash 5.3 patterns, parameter expansion, arrays, conditionals, process substitution, error handling, traps, heredocs, coprocesses, bash 5.x features (non-forking `${ cmd; }`, GLOBSORT, SRANDOM), script template
- `references/posix-sh.md` - Portable POSIX sh patterns, what's POSIX and what's not, bashism avoidance checklist, which-sh-am-I, arithmetic, parameter expansion, portable conditionals
- `references/alt-shells.md` - Fish 4.6 (syntax, functions, completions, config, 4.6 additions), tcsh/csh 6.24 (syntax, when you'll encounter it), nushell 0.111 (structured pipelines, types), elvish 0.22/oils 0.37 (brief)
- `references/ssh-tmux-autostart.md` - safe shell startup pattern for interactive SSH sessions that attach to tmux without breaking non-interactive commands

## Output Contract

See `skills/_shared/output-contract.md` for the full contract.

- **Skill name:** COMMAND-PROMPT
- **Deliverable bucket:** `audits`
- **Mode:** conditional. When invoked to **analyze, review, audit, or improve** existing repo content, emit the full contract - boxed inline header, body summary inline plus per-finding detail in the deliverable file, boxed conclusion, conclusion table - and write the deliverable to `docs/local/audits/command-prompt/<YYYY-MM-DD>-<slug>.md`. When invoked to **write a script, dotfile, or completion / answer a question / teach a concept**, respond freely: deliver the artifact or explanation inline without the contract, deliverable file, or conclusion table.
- **Severity scale:** `P0 | P1 | P2 | P3 | info` (see shared contract; only used in audit/review mode).

## Related Skills

- **firewall-appliance** - OPNsense/pfSense uses tcsh/csh on FreeBSD. That skill handles the BSD firewall context; this skill covers tcsh syntax in general.
- **ansible** - Ansible `shell`/`command` modules have their own idiosyncrasies beyond raw shell scripting. Use ansible for playbook work.
- **ci-cd** - CI shell blocks run in restricted environments (no interactive features, possibly no bash). Use ci-cd for pipeline design; use this skill for the shell syntax within them.
- **networking** - Linux network configuration (interfaces, routes, firewalls, DNS). Use networking for service and protocol administration; use this skill for the shell scripts that wrap or automate those tasks.
- **debian-ubuntu** - Debian/Ubuntu system administration (packages, services, cloud-init). Use debian-ubuntu for distro-level operations; use this skill for the shell scripting patterns within those tasks.
- **rhel-fedora** - RHEL/Fedora system administration (dnf, systemd, SELinux, subscription-manager). Use rhel-fedora for distro-level operations; use this skill for the shell scripting patterns within those tasks.

## Rules

1. **Detect the shell first.** Check shebang, file extension, or ask. Don't assume bash when the user might mean zsh.
2. **Load the right reference.** Don't wing zsh arrays or bash parameter expansion from memory - the subtle differences justify loading the reference every time.
3. **Shebang is `#!/usr/bin/env <shell>`.** Not `#!/bin/bash`. The env form is portable across distros. Exception: `#!/bin/sh` for POSIX scripts (this IS the standard form).
4. **`set -euo pipefail` in every bash/zsh script.** No exceptions for scripts beyond a one-liner.
5. **User's interactive shell is zsh.** When writing commands for the user to run locally, use zsh syntax. Bash for scripts and remote machines unless the script specifically needs zsh.
6. **Don't mix shell syntaxes.** A bash script uses bash idioms. A zsh script uses zsh idioms. "Works in both" compromises use neither well and confuse readers.
7. **Quote your variables.** `"$var"` is the default. Unquoted `$var` is the exception that needs justification.
