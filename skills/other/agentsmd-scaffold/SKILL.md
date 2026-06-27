---
name: agentsmd-scaffold
description: Generate or update repository-specific AGENTS.md instruction files from real repo evidence. Use when asked to create, design, scaffold, split, or improve root or scoped AGENTS.md files for Codex/Claude/agent workflows, especially when a repo needs directory-specific rules, validation commands, generated-file boundaries, or a short agent onboarding router.
---

# AGENTS.md Scaffold

Use this skill to generate a small, evidence-backed `AGENTS.md` stack for a
repository. The output may be a plan, exact proposed file contents, or applied
files when the user explicitly asks to write them.

This skill is for instruction scaffolding. Use `repo-agent-context-audit` first
when the user only asks whether the repo's agent context is healthy.

## Operating Contract

Default to a scoped plan before editing. Only write or modify `AGENTS.md`,
`CLAUDE.md`, `WARP.md`, hooks, settings, or generated docs when the user has
explicitly asked to apply the scaffold.

Direct actions:
- Run read-only discovery, scanner commands, and repo command inspection.
- Produce a scoped `AGENTS.md` plan with evidence and validation commands.
- Draft exact file contents when the user asks for proposed text.

Escalate before:
- Creating or editing high-context files when the user only asked for an audit.
- Rewriting existing `AGENTS.md`, `CLAUDE.md`, or `WARP.md` instead of adding a
  short pointer or scoped complement.
- Batch-normalizing multiple repositories.

Evidence-backed pushback:
- Challenge new scoped files when the directory has no distinct local rules.
- Challenge guessed commands, ownership, or generated-file rules unless repo
  evidence supports them.

Feedback loop:
- Promote repeated false starts into `references/scaffold-agents.md`, scanner
  signals, or eval prompts.

## Workflow

### 1. Discover Existing Context

Run the scanner from this skill directory when possible:

```bash
python3 scripts/scan_repo_context.py <repo-root>
python3 scripts/scan_repo_context.py <repo-root> --json
```

Then inspect the files that matter:

- existing `AGENTS.md`, `CLAUDE.md`, `WARP.md`, `.claude/instructions.md`, and
  `.github/copilot-instructions.md`
- `README.md`, `CONTRIBUTING.md`, package manifests, Makefiles, CI workflows,
  and documented test commands
- generated files and their generators
- high-risk directories such as migrations, deploy scripts, auth, secrets,
  payments, registry metadata, generated clients, and production operations

Do not infer commands or ownership from names alone. Use scanner output as a
lead, then verify with actual files.

### 2. Choose The Instruction Stack

Read `references/scaffold-agents.md` before proposing files. Choose the
smallest stack that changes agent behavior:

- root `AGENTS.md` for repo-wide routing and validation
- nested `AGENTS.md` only where directory rules differ from root
- no nested file for directories that only need ordinary README context
- no bulk normalization across multiple repos until a few examples have been
  manually validated

### 3. Produce A Candidate Plan

Before editing, report:

```markdown
## Scoped AGENTS Plan

| Path | Why here | Rules to include | Validation |
|---|---|---|---|
| `AGENTS.md` | <repo evidence> | <root topics> | `<command>` |
| `<dir>/AGENTS.md` | <repo evidence> | <scoped topics> | `<command>` |

## Files To Preserve

- `<existing high-context file>` - <how it will be referenced or left alone>

## Open Facts

- <missing command or ownership fact that cannot be inferred>
```

### 4. Scaffold On Request

When applying the scaffold:

- keep root files short, normally 80-150 lines
- keep nested files focused on that directory's ownership, source-of-truth
  rules, and validation commands
- include real commands and paths, not placeholders, unless the fact is truly
  missing
- preserve existing high-context files unless the user requested a rewrite
- pair every prohibition with a concrete alternative, helper, generator, or
  command

## Decision Gates

| Situation | Action |
|---|---|
| Existing `CLAUDE.md` or `WARP.md` is already a good router | Add a short `AGENTS.md` pointer only if cross-runtime routing helps. |
| Root instruction file exceeds roughly 200 lines | Propose root router plus scoped files or references. |
| Directory has generated outputs | Add scoped rules naming source of truth and regenerate/check commands. |
| Directory has distinct safety rules | Add scoped rules with escalation boundaries. |
| Directory has ordinary implementation files only | Keep guidance in root unless conventions differ. |
| Commands cannot be verified from repo evidence | Leave an open fact instead of guessing. |

## Gotchas

- Do not add nested `AGENTS.md` files for every directory. Add them only where
  local rules differ from root.
- Do not guess build, test, lint, or generator commands from framework names.
  Cite the manifest, CI workflow, script, or docs that prove the command.
- Do not overwrite an existing `CLAUDE.md`, `WARP.md`, or `AGENTS.md` just to
  normalize naming. Preserve it, point to it, or propose a split first.
- Do not put long architecture explanations in root `AGENTS.md`; route to
  references or existing docs instead.

## Verification

After applying changes:

- run the repo's narrow validation command for the affected scope
- run any repo-wide registry, docs, typecheck, lint, or test command named in
  the new instructions when practical
- rerun `python3 scripts/scan_repo_context.py <repo-root>` if using the bundled
  scanner to confirm scoped files are discoverable

If verification cannot run, report the exact missing precondition and the
command that should be run later.

## Resources

- `scripts/scan_repo_context.py`: read-only scanner for high-context files,
  command hints, specs, local skills, and scoped `AGENTS.md` candidates.
- `references/scaffold-agents.md`: scaffold selection rules and templates for
  root, generated metadata, scripts/tools, skill libraries, and tests.
- `evals/evals.json`: lightweight prompts for future behavior checks.
