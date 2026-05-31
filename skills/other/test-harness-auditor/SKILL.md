---
name: test-harness-auditor
description: "Audit a repo's test, lint, type-check, static analysis, build, and debug infrastructure for AI coding agents. Generate scored reports and optimized configs for the lint-on-write hook. Triggers on audit tests, test harness, lint setup, check test infrastructure, entering a new repo."
argument-hint: "[path]"
user-invocable: true
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# Test Harness Auditor

Audit any repo's feedback infrastructure across six layers and generate optimized configs for AI coding agents.

## When to Run

- Entering a new repo with no `.claude/lint-rules.json`
- User asks to audit tests, lint setup, or agent infrastructure
- After cloning a repo to check what feedback loops exist
- Periodically to catch configuration drift

## Two-Phase Workflow

### Phase 1: Audit (read-only)

Run the audit script to scan the current repo:

```bash
uv run ~/.claude/skills/test-harness-auditor/scripts/audit.py
```

Or target a specific directory:

```bash
uv run ~/.claude/skills/test-harness-auditor/scripts/audit.py /path/to/repo
```

For machine-readable output (consumed by Phase 2):

```bash
uv run ~/.claude/skills/test-harness-auditor/scripts/audit.py --json > /tmp/audit.json
```

To save a snapshot for drift detection (tracks score changes over time):

```bash
uv run ~/.claude/skills/test-harness-auditor/scripts/audit.py --save
```

Combine flags: `--json --save` saves the snapshot AND outputs JSON. On subsequent `--save` runs, the report includes a drift section showing score regressions, config changes, and residue file changes.

The script produces a structured Markdown report (or JSON with `--json`) with:
- **Stack summary**: detected language, frameworks, package manager, actual scripts from package.json
- **Scorecard**: 0-3 score for each of the six layers (test, lint, type-check, SA, build, debug)
- **Findings**: per-layer details on what was detected
- **Debugging residue**: files matching `*_v2.*`, `*_backup.*`, `*_fixed.*` patterns
- **Recommendations**: prioritized by impact on agent feedback quality (P0-P3)

Present the report to the user. Ask which recommendations to implement before proceeding to Phase 2.

### Phase 1.5: Convention Extraction (optional)

Extract "never X"/"always Y" constraints from CLAUDE.md into candidate lint rules:

```bash
uv run ~/.claude/skills/test-harness-auditor/scripts/extract_conventions.py
```

Outputs JSON with candidate lint-rules.json entries derived from project constraints. Present candidates to the user for approval before merging.

### Phase 2: Config Generation (after user approval)

Run the generation script (optionally with audit JSON for accurate commands):

```bash
uv run ~/.claude/skills/test-harness-auditor/scripts/generate.py --audit /tmp/audit.json
```

Or without audit data (re-detects stack):

```bash
uv run ~/.claude/skills/test-harness-auditor/scripts/generate.py
```

When `--audit` is used, generate.py uses actual commands from package.json (vitest, playwright, biome, etc.) instead of generic templates, and detects separate E2E vs unit test runners.

This produces three outputs:

1. **`.claude/lint-rules.json`** — custom grep-based rules for the lint-on-write hook
   - Stack-specific rules (security, debugging residue, error boundaries, observability)
   - Auto-includes matching rule packs from `rule-library/` (react, rust-workspace, python-cli; functional-ts is opt-in only)
   - Merges with existing config if present (preserves user customizations)
   - Tagged rules (`_tag` field) enable idempotent re-runs

2. **CLAUDE.md testing section** — test/lint/typecheck/build/SA commands
   - Follows claude-md-manager conventions (command-first, concise)
   - **Section-aware merge**: when existing CLAUDE.md is found, surgically replaces only `## Commands` and `## Testing` sections, preserving all other content
   - Present as a proposal — do not overwrite existing CLAUDE.md content

3. **Hook recommendations** — which PostToolUse hooks to enable
   - lint-on-write (primary), test-on-fix, type-check-on-write

For each generated config, present it to the user and ask for approval before writing.

## Scoring System

| Score | Meaning |
|-------|---------|
| 0 | Absent — agent is flying blind on this layer |
| 1 | Minimal — basic tool present but not configured for agents |
| 2 | Adequate — tool configured and runnable |
| 3 | Excellent — strict mode, mutation testing, or advanced config |

## Six Assessment Layers

1. **Test suite**: framework, runner command, coverage config, mutation testing
2. **Linting**: standard linter, custom rules, agent-specific rules
3. **Type checking**: type checker, strict mode, CI integration
4. **Static analysis**: security scanners, complexity checkers, dependency audit
5. **Build/compilation**: build command, incremental build, CI validation
6. **Debugger/REPL**: debugger availability, REPL access

## Integration

- **lint-on-write hook**: generated `lint-rules.json` is consumed by `~/.claude/hooks/lint-on-write.py` (violations are severity-tiered: BLOCKING > HIGH > MEDIUM)
- **claude-md-manager**: generated CLAUDE.md sections follow its conventions (WHAT/WHY/HOW, command-first)
- **agents-md-manager**: for cross-agent compatibility, consider also generating AGENTS.md
- **agnix**: complementary tool — validates the *agent config files* themselves (385 rules for CLAUDE.md/AGENTS.md/SKILL.md stale paths, dead commands, context rot). Our skill validates the *codebase infrastructure*.

## Rule Library

44 rules across 4 domain-specific packs in `rule-library/`. Auto-loaded packs are selected by `generate.py` based on detected frameworks and stack. All patterns are single-line `grep -En` detectable.

| Pack | Matches | Rules | Highlights |
|------|---------|-------|------------|
| `react.json` | react, next frameworks | 10 | disabled-exhaustive-deps, key-index, async-use-effect, disabled-hooks-rule, context-object-literal |
| `rust-workspace.json` | rust stack | 8 | expect-empty-msg, anyhow-in-lib, dbg-macro, panic-outside-tests, println-residue |
| `python-cli.json` | python stack | 13 | shell-true, insecure-deserialization, mutable-default-arg, requests-no-timeout, commonprefix |
| `functional-ts.json` | **Opt-in only** | 13 | array-mutation, sort-reverse, delete-operator, any-type, enum-declaration, namespace-declaration |

### Opt-in packs

Packs with `"_opt_in": true` are never auto-loaded. The **functional-ts** pack enforces strict-FP immutability patterns (Open Souls paradigm). To use it, manually copy its rules into your project's `.claude/lint-rules.json`.

### Exclusion fields

Rules support two exclusion mechanisms:

- **`exclude_paths`** — glob-matched against file paths (e.g. `"*/bin/*"`, `"*/main.rs"`). Skips the file entirely before grep runs.
- **`exclude_patterns`** — regex-matched against grep output line text (e.g. `"test"`, `"// nosec"`). Filters matched lines after grep runs.

To add a custom rule pack, create a JSON file in `rule-library/` with `_frameworks` (list) and/or `_stack` (string) matching fields, plus a `rules` array. Set `"_opt_in": true` to prevent auto-loading. Pack rules use `pack:` prefix in `_tag` for dedup. See `rule-library/INDEX.md` for the full inventory.

## References

Load these on-demand when deeper context is needed:

- `references/stack-profiles.md` — per-stack detection rules and tool recommendations
- `references/factory-lint-categories.md` — 7 Factory.ai agent lint categories with grep patterns
- `references/anti-patterns.md` — 10 AI-specific anti-patterns with detection heuristics

## Scope

- First-class stacks: JavaScript/TypeScript, Rust, Python, Go, Ruby
- Other stacks get basic detection with generic recommendations
- Does not write or modify test files
- Does not install tools (recommends what to install)
- Does not modify CI/CD pipelines
