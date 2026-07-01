---
name: enhance
description: Audit and tighten agent/plugin surfaces with certainty-graded findings. Use when the user says "enhance my plugin", "improve my agents or skills", "audit plugin config", "enhance CLAUDE.md", or "improve agent definitions".
metadata:
  short-description: Certainty-graded surface enhancer
---

# Enhance — certainty-graded surface correction

Run a `correct` op over AI-facing project surfaces. The invariant: plugin manifests, agents, skills, prompts, docs, command definitions, hooks, and project memory must be explicit, bounded, and internally consistent.

Native shape: no external analyzer binary, no persistent suppression learning, no model routing. Use ODIN discovery tools plus parallel generic `task` agents. Each analyzer emits structured findings with `certainty`, `autoFix`, `file`, `line`, `check`, `evidence`, `fix`. The orchestrator aggregates, deduplicates, and reports.

## When to Apply / NOT

Apply when the user asks to enhance, improve, audit, or tighten plugin config, agent definitions, skills, CLAUDE.md/AGENTS.md, docs, prompts, commands, or hooks.

NOT when the user asks for general code assessment, runtime bug fixing, visual design, performance profiling, or content rewriting without configuration/agent-surface analysis.

## Flags

- `--apply`: apply only HIGH-certainty findings with `autoFix: yes`. No flag → report only.
- `--verbose`: include MEDIUM and LOW findings. Default report shows HIGH plus summary counts for MEDIUM/LOW.
- `--focus=<type>`: optional narrowing to one or more comma-separated analyzer families: `plugin`, `agent`, `skill`, `docs`, `prompt`, `claudemd`, `hooks`, `cross-file`.

Deleted on purpose: auto-suppression learning, reset/export suppression flags, editor-platform adapters, model pins, binary cache state.

## Discovery

Resolve the target path from the first non-flag argument; default `.`. Use `find` for names and `read` for the exact files each analyzer needs.

| Analyzer | Discovery globs |
|---|---|
| plugin | `plugins/*/.claude-plugin/plugin.json`, `.claude-plugin/plugin.json`, `**/.claude-plugin/plugin.json` |
| agent | `**/agents/*.md` |
| skill | `**/SKILL.md` |
| claudemd | `CLAUDE.md`, `AGENTS.md`, `**/CLAUDE.md`, `**/AGENTS.md` |
| docs | `docs/**`, `README.md`, `CHANGELOG.md` |
| prompt | `commands/**`, `prompts/**`, `**/commands/*.md`, `**/prompts/*.md` |
| hooks | `hooks/**`, `**/hooks/**` |
| cross-file | enabled when two or more of plugin/agent/skill/claudemd/prompt are present |

Skip analyzers with no files. For `--focus`, skip all non-focused analyzers even if files exist.

## Workflow

1. **Parse intent.** Extract `target`, `--apply`, `--verbose`, `--focus`. Reject unknown focus values with the valid set above.
2. **Discover files.** Run the discovery table. Keep concrete path lists; do not pass globs to worker agents as the target contract.
3. **Launch parallel analyzers.** In one `task` batch, dispatch one generic `task` worker per analyzer family that has files. Each worker receives:
   - target analyzer name;
   - exact file list;
   - `--verbose` state;
   - the applicable section of `references/analyzer-checks.md`;
   - required JSON return shape.
4. **Analyzer contract.** Each worker reports only observed findings:
   ```json
   {
     "analyzer": "plugin|agent|skill|docs|prompt|claudemd|hooks|cross-file",
     "findings": [
       {"file":"path","line":1,"check":"missing_description","certainty":"HIGH","autoFix":false,"evidence":"...","fix":"..."}
     ],
     "summary": {"high":0,"medium":0,"low":0,"autoFixableHigh":0}
   }
   ```
5. **Deduplicate.** Stable key: `analyzer|file|line|check|normalized evidence`. If two analyzers report the same underlying defect, keep the higher certainty; if equal, keep the one with narrower file/line evidence.
6. **Aggregate.** Sort by `certainty`: HIGH → MEDIUM → LOW, then analyzer, file, line. Count totals by analyzer and certainty.
7. **Report.** Default output includes executive summary, all HIGH findings, MEDIUM/LOW counts, and HIGH auto-fixable list. With `--verbose`, include MEDIUM and LOW sections with rejection-ground labels: **Excess**, **Graft**, **Sprawl**, or **Correctness**.
8. **Apply guarded fixes.** Only when `--apply` is present:
   - filter to `certainty === HIGH && autoFix === true`;
   - group by analyzer;
   - edit the minimal lines required;
   - re-read changed files after each edit;
   - never apply MEDIUM/LOW fixes automatically.
9. **Verify the fix set.** Re-run only the analyzers whose files changed. A fix passes if the exact HIGH finding is gone and no new HIGH finding appears in the changed file. If a fix introduces a new HIGH issue, revert that fix and keep the finding in the report as manual.

## Native analyzer recipes

Use ODIN tools directly:

- File presence and frontmatter: `find` → `read` exact files.
- Regex/field checks: `search` scoped to discovered files; parse YAML/JSON by direct read and reasoning.
- Structured code-ish checks: `ast-grep` for command snippets, shell patterns, hook script bodies when syntax matters.
- Cross-file links: codegraph MCP when indexed for symbols/callers/impact; fallback to `ast-grep` plus text search scoped to discovered files.
- Whole-surface context, only for large repos: repomix (`pack_codebase` or `npx -y repomix --compress`) to build a digest for the analyzer workers.

Fallback commands to embed in worker prompts when MCP indexing is unavailable:

```bash
# symbol/name lookup fallback
git grep -n "<symbol-or-rule>" -- ':!node_modules' ':!dist' ':!build'

# structural Markdown/frontmatter lookup fallback
ast-grep --lang yaml -p 'name: $X' <file>

# broad changed-surface scan fallback
git --no-pager log --format='%h%x09%ad%x09%an%x09%s' --date=short -- <file>
```

## Report format

```markdown
# Enhancement Analysis Report

Target: <path>
Flags: apply=<true|false>, verbose=<true|false>, focus=<value|all>
Analyzers run: plugin, agent, skill, docs, prompt, claudemd, hooks, cross-file

## Executive Summary

| Analyzer | HIGH | MEDIUM | LOW | HIGH Auto-Fixable |
|---|---:|---:|---:|---:|
| plugin | 0 | 0 | 0 | 0 |
| Total | 0 | 0 | 0 | 0 |

## HIGH Certainty Findings

- `<file>:<line>` — `<check>` — Evidence: `<observed>` — Fix: `<minimal correction>`

## Deferred Findings

MEDIUM and LOW hidden unless `--verbose`. They require human inspection; never auto-apply.

## Auto-Fix

`--apply` absent: list commands/edits that would be safe.
`--apply` present: list edits applied and re-analysis result.
```

## Anti-patterns

- **Learning suppressions.** False positives are reported, gated, or fixed in the check table. Do not hide future findings behind state.
- **Medium auto-fix.** MEDIUM means context-dependent; applying it automatically is Sprawl.
- **Parallel by file.** Parallelize by analyzer family, not file shards. Cross-surface consistency depends on seeing all relevant files.
- **Generic advice.** Every finding needs path, line or section, observed evidence, and a concrete fix.
- **Cross-skill delegation.** This skill is self-contained; use its own reference table and native tools.
- **Tool overcorrection.** Do not add broad `Bash`, `Read`, or wildcard permissions as a convenience fix.

## Validation Gates

- Frontmatter parses; `name` matches the directory.
- Analyzer coverage matches discovery; skipped analyzers have zero discovered files or are excluded by `--focus`.
- HIGH findings are complete in default output.
- MEDIUM/LOW appear only under `--verbose`.
- `--apply` changes only HIGH + `autoFix: yes` findings.
- Re-analysis removes each applied finding without creating a new HIGH issue.
- No suppression-learning files or suppression state are created.
