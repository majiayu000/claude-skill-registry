---
name: cli-design
description: "Design a CLI interface: args, flags, help, output, errors, exit codes, config."
user_invocable: false  # default -- router-dispatched, not user-typed
allowed-tools:
  - Read
  - Write
  - Grep
  - Glob
  - Bash
routing:
  triggers:
    - "design a CLI"
    - "CLI interface"
    - "command line tool design"
    - "CLI flags"
    - "CLI spec"
    - "argument parsing design"
    - "exit codes"
  category: engineering
  pairs_with:
    - test-driven-development
    - python-quality-gate
---

# CLI Design

Design a command-line tool's interface before implementation: human-first, script-friendly, Linux-only. Output is a compact spec the user or an agent can implement directly. Rubric source: clig.dev (rebuilt as `references/clig-checklist.md`).

## Workflow

### Phase 1: SCOPE

Lock the interface with the minimum questions. Proceed with the conventions in Phase 2 when the user is unsure.

- Command name and one-sentence purpose.
- Primary user: humans, scripts, or both.
- Input sources: args vs stdin; files vs URLs. Secrets travel via file or stdin, because flags leak through `ps` and shell history.
- Output contract: human text, `--json`, `--plain`, exit codes.
- Interactivity: prompts allowed? `--no-input` needed? confirmation for destructive ops?
- Config model: flags, env, config file; precedence.

**Gate:** name, purpose, and I/O contract are known. Proceed only when gate passes.

### Phase 2: DESIGN

Load [references/clig-checklist.md](references/clig-checklist.md) and apply it as the default rubric. For each section, pick the convention and record it in the spec. Diverge from a convention only deliberately, and document the divergence in the spec — interfaces are contracts, and surprising contracts break scripts.

### Phase 3: DELIVER

Produce the spec from this skeleton. Drop a section only when it genuinely has no content; fill every other section.

1. **Name and one-liner**: command name plus a single sentence of purpose
2. **Usage line**: the synopsis as `--help` will print it, global flags and subcommand slot included
3. **Subcommands**: purpose of each, whether it mutates state, whether re-running it is safe
4. **Args/flags table**: columns for name, type, default, required?, example
5. **I/O contract**: primary data and machine-readable output on stdout; everything else (errors, progress, logs) on stderr
6. **Exit codes**: map each failure mode to a code — success `0`, failure `1`, bad usage `2`; mint extra codes only for cases scripts must distinguish
7. **Safety**: `--dry-run`, confirmation rules, `--force`, `--no-input`
8. **Env/config**: env vars; config file path; precedence order with flags highest, then env, project config, user config, system
9. **Examples**: enough invocations to cover the common flows; show at least one pipeline or stdin use

**Gate:** every flag used in the examples appears in the flags table, and every failure mode shown maps to an exit code.

## Constraints

- Stay at spec altitude: when the request is "design the interface," deliver the spec and stop. Implementation is a separate task.
- Keep the spec language-agnostic. Recommend a parsing library only when asked.
- Target Linux. Skip Windows/macOS path, signal, and packaging concerns.

## Error handling

### Request mixes design and implementation
Cause: user says "design and build."
Solution: deliver the spec first, get confirmation, then implement against it.

### Spec balloons past one page
Cause: subcommand sprawl or speculative flags.
Solution: cut flags that lack a named user need; defaults should serve most users without aliases.
