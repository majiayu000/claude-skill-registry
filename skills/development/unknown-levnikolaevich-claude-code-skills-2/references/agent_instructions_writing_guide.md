<!-- SOURCE-OF-TRUTH: shared/references/agent_instructions_writing_guide.md. Edit ONLY here; run `node tools/marketplace/shared.mjs sync` -->

# Agent Instructions Writing Guide

> **SCOPE:** How to author AGENTS.md and CLAUDE.md at the root of a project. Canonical reference for `ln-014-agent-instructions-manager`, `ln-111-root-docs-creator`, `ln-611-docs-structure-auditor`, and `ln-612-semantic-content-auditor`.

## Canonical model: AGENTS.md is the single source

Each harness auto-loads only its own memory file:

| Harness | Auto-loaded file | AGENTS.md auto-loaded? |
|---------|------------------|------------------------|
| Claude Code | `CLAUDE.md` | No — Anthropic docs: *"Claude Code reads CLAUDE.md, not AGENTS.md."* |
| OpenAI Codex CLI, Cursor, Amp, Factory, OpenCode, Zed | `AGENTS.md` | Yes |

Because CLAUDE.md is the file Claude Code loads by default, the naive "put a pointer in CLAUDE.md that says 'see AGENTS.md'" pattern **does not work** — the harness will not follow the pointer automatically. The content must be in the auto-loaded file.

Claude Code solves this with a native `@path` import syntax. The imported file is expanded and loaded into context at launch, exactly as if its content were inlined.

**The pattern:** keep a single canonical `AGENTS.md` at the repo root with all shared content. Make `CLAUDE.md` a thin stub that `@AGENTS.md` and adds only harness-specific deltas. Anthropic documents this pattern verbatim with an example at <https://code.claude.com/docs/en/memory#agents-md>.

Scope boundary: this native `@path` import behavior is the right pattern for Claude Code memory/context files such as `CLAUDE.md`. It is not the repository's canonical execution contract for `SKILL.md`; skills should still use explicit `**MANDATORY READ:** Load ...` for execution-critical references.

```markdown
# CLAUDE.md
@AGENTS.md

## Claude Code

- `/compact` preservation order: architecture decisions, verification status, open TODOs.
- Auto memory is on by default — run `/memory` to inspect.
```

This makes drift structurally impossible: there is one place to edit (`AGENTS.md`) and the stubs carry only genuinely harness-specific content.

## Size budgets

| Target | Limit | Source |
|--------|-------|--------|
| AGENTS.md line count | ≤200 lines (ideally ≤150) | Anthropic official: *"target under 200 lines per CLAUDE.md file. Longer files consume more context and reduce adherence."* |
| CLAUDE.md stub line count | ≤20 lines (≤50 absolute max) | Derived: stub should only carry harness delta |
| User-added imperatives across all loaded files | ≤100 | Empirical: IFScale (arxiv 2507.11538) finds frontier LLMs peak around 150–200 total instructions and degrade past that; Claude Code's built-in system prompt already consumes a significant portion |

Count imperatives as: lines matching `^\s*- ` inside rule sections, plus any line containing `MUST`, `NEVER`, `ALWAYS`, or `DO NOT`.

When AGENTS.md grows past 200 lines, split with progressive disclosure (next section) — do not accept a bigger root file.

## Progressive disclosure: use `.claude/rules/` with `paths:` frontmatter

Anthropic ships a built-in path-scoped rules mechanism. Place markdown files in `.claude/rules/` with YAML frontmatter declaring the glob patterns they apply to. Each file loads into context only when Claude touches a matching file.

```markdown
---
paths:
  - "src/api/**/*.ts"
  - "src/api/**/*.tsx"
---

# API development rules
- All endpoints must include input validation.
- Use the standard error response format.
```

Rules without a `paths` field load unconditionally with the same priority as `.claude/CLAUDE.md`. Shared rule directories can be symlinked across projects.

**Do not invent a new `agent_docs/` or similar convention.** Anthropic's `.claude/rules/` is the supported mechanism; using anything else gives up path scoping and breaks `/memory show`.

## Auto memory is built-in — do not author a manual Self-Improvement Loop

Claude Code has a first-class auto memory system, enabled by default (`CLAUDE_CODE_DISABLE_AUTO_MEMORY=1` to disable; requires Claude Code v2.1.59+). Claude writes learnings from user corrections to `~/.claude/projects/<project>/memory/MEMORY.md` and optional topic files during every session. The first 200 lines or 25KB of `MEMORY.md` loads automatically.

Public articles sometimes recommend adding a manual `tasks/lessons.md` "Self-Improvement Loop" rule to CLAUDE.md (e.g., Hosni's *"after ANY correction from the user: update `tasks/lessons.md`"*). **Do not do this in our templates.** Claude Code's built-in auto memory already does exactly that, per Anthropic's own documentation. A manually-maintained parallel convention wastes context tokens and duplicates work. Document the equivalence; do not re-implement.

Run `/memory` to inspect or edit what Claude has saved.

## What legitimately belongs in the 50-line harness delta

Put in the CLAUDE.md stub:

- **Harness-specific command terminology**: `/compact`, `/memory show`, `/memory reload`. If it names a command that only works in Claude Code, it's a delta candidate.
- **Harness-specific storage pointers**: `~/.claude/projects/<project>/memory/` is Claude-specific.
- **Harness-specific features that don't exist elsewhere**: `.claude/rules/` with `paths:` frontmatter, nested `CLAUDE.md` on-demand loading, `CLAUDE_CODE_NEW_INIT=1`, `autoMemoryDirectory`, `claudeMdExcludes`.

Put in AGENTS.md (not the stub):

- Project architecture, tech stack, directory map.
- Critical rules that apply regardless of harness.
- Build and test commands.
- Coding standards and naming conventions.
- MCP tool preferences (hex-line, hex-graph, hex-research, etc. — these apply to any harness that can load MCP tools). Include `hex-research` only for projects with `docs/hypotheses/`, `docs/goals/`, or benchmark run manifests where graph state changes planning or validation decisions.
- Navigation tables.
- Compact-instructions preservation lists *(terminology differs per harness — but the preservation priority list itself is shared, so keep the list in AGENTS.md and mention only the command name in the stub)*.

If you find yourself writing the same rule into both AGENTS.md and CLAUDE.md, the rule belongs in AGENTS.md and the import takes care of the rest.

## Anti-patterns

| Anti-pattern | Why it's wrong | Fix |
|--------------|----------------|-----|
| Style / formatting rules (indentation, quote style, naming conventions) inside any instruction file | Instruction files are loaded into context on every session and cost tokens against the ~100-imperative budget; linters and formatters are deterministic, free, and faster | Move to Biome, Prettier, Ruff, EditorConfig, or a Claude Code Stop hook; keep the file free of style content |
| Conditional / non-universal rules (`when working on src/api/...`, `if modifying the billing service`) at the root | Claude Code injects a `<system-reminder>` around CLAUDE.md telling the model to ignore content that isn't clearly relevant; non-universal rules bias the model toward ignoring the *whole* file, not just the irrelevant parts | Move to `.claude/rules/*.md` with a `paths:` frontmatter filter (Anthropic's built-in path scoping) |
| Duplicating AGENTS.md content inside CLAUDE.md | Doubles the maintenance surface, causes drift, wastes tokens (the content is already imported via `@AGENTS.md`) | Replace the duplicated block with a single `@AGENTS.md` line; move any unique content *into* AGENTS.md |
| Hand-maintained "Self-Improvement Loop" / `tasks/lessons.md` section | Claude Code's built-in auto memory already does this (Anthropic docs); a parallel convention wastes context and diverges over time | Delete the section; rely on `~/.claude/projects/<project>/memory/` |
| Large HTML comment blocks at the top of CLAUDE.md for documentation | Block-level HTML comments are stripped before context injection *(Anthropic docs)*, so they cost zero context tokens, but they still clutter the maintainer view of the file | Short maintainer notes only; put detailed guide content in `agent_instructions_writing_guide.md` and point to it |
| Using `/init` without review | `/init` can insert boilerplate that reduces the signal-to-noise ratio of a high-leverage file; bad lines in CLAUDE.md cascade into every future session | Use `CLAUDE_CODE_NEW_INIT=1` for the interactive multi-phase flow with a reviewable proposal, or author by hand |
| Aggregate counts in instruction files (`"we have many skills"`) | Changes every time the repo grows, breaks prompt cache prefix match | Put counts only in README.md badges; everywhere else use qualitative descriptions |
| Timestamps and dates inside the rules text | Same cache-prefix problem | Keep `**Last Updated:** YYYY-MM-DD` at file end only |

## Optional Hosni workflow blocks — opt-in, not default

Hosni's article ("Level Up Your Claude Code with This CLAUDE.md", Feb 2026) proposes six Workflow Orchestration blocks. Our default `agents_md_workflow_principles.md` shard includes **Plan Mode Default**, **Verification Before Done**, **Demand Elegance**, and **Core Principles**. The remaining three are opt-in:

- **Subagent Strategy** — already covered by our orchestrator skills and `hex-line` MCP preferences. Restating at the root adds instruction-budget pressure without new behavior.
- **Self-Improvement Loop** — replaced by Claude Code built-in auto memory (see above).
- **Autonomous Bug Fixing** — requires a permission policy (allow the agent to run CI without asking) that we cannot guarantee uniformly across Claude Code and Codex. Add it manually if your environment supports it.

Users who want a block can add it to AGENTS.md themselves. The ln-014 audit will not flag it as a problem, only count it against the 100-imperative budget.

## Sources

- Anthropic: *How Claude remembers your project* — <https://code.claude.com/docs/en/memory>. Load-bearing claims: "Claude Code reads CLAUDE.md, not AGENTS.md"; the `@AGENTS.md` interop example; size target <200 lines; `.claude/rules/` with `paths:` frontmatter; auto memory at `~/.claude/projects/<project>/memory/`; block-level HTML comments stripped before injection; `CLAUDE_CODE_NEW_INIT=1` interactive flow.
- Hosni, Youssef: *Level Up Your Claude Code with This CLAUDE.md* (Level Up Coding, Feb 2026). Source of the Workflow Orchestration framing and the 6 behavioral blocks. Accessible via friend link embedded in the article.
- HumanLayer (Kyle): *Writing a good CLAUDE.md* (Nov 2025) — <https://www.humanlayer.dev/blog/writing-a-good-claude-md>. Load-bearing claims: non-universal rules bias the model toward ignoring the whole file due to the `<system-reminder>` injected around CLAUDE.md; `@path` imports for progressive disclosure; Claude is not a linter.
- IFScale benchmark — <https://arxiv.org/html/2507.11538v1>. Empirical evidence that frontier LLMs peak around 150–200 instructions then degrade uniformly; load-bearing for the ~100 user-added imperative ceiling.

**Last Updated:** 2026-04-11
