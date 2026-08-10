---
name: agents-memory
description: "Manages AGENTS.md, CLAUDE.md, and scoped repo rules for Claude Code and Codex. Use when fixing stale memory, ignored instructions, memory audits, or model-upgrade migration."
compatibility: Claude Code + Codex. Claude Code CLAUDE.md plus Codex AGENTS.md — runtime-specific file conventions.
version: "1.2"
last_validated: 2026-07-11
---

# Project Memory for Claude Code + Codex

Configure project memory so Claude Code and Codex get stable, scoped instructions across sessions without bloating every prompt. For shared teams, keep the portable project rules in `AGENTS.md`, mirror that into `CLAUDE.md` when needed, and keep tool-specific behavior in the tool's native layer.

Treat repo memory as a **living exception file**. If an agent can reliably infer something by reading the code, config, or README, keep it out of the always-loaded layer. Put only the durable, non-inferable guidance here.

## Quick Reference

| Layer | Typical Location | Purpose |
|------|------------------|---------|
| Shared project memory | `./AGENTS.md` | Portable repo instructions for Codex and other AGENTS.md-aware tools |
| Claude project memory | `./CLAUDE.md` | Claude Code project instructions; often a symlink or mirror of `AGENTS.md` |
| Claude scoped rules | `./.claude/rules/*.md` | Modular Claude-only rules, optionally path-scoped |
| Codex personal memory | `~/.codex/AGENTS.md` | Personal defaults across repositories |
| Codex repo-local override | `./AGENTS.override.md` | Local developer override when you need a non-shared layer |
| Codex auto-memory | `~/.codex/memories/` (opt-in via `[features] memories = true`) | Machine-local accumulated recall; off by default in EEA/UK/CH; keep must-always rules in `AGENTS.md`, not here |
| Claude auto memory | `~/.claude/projects/<project>/memory/` — `MEMORY.md` index + topic files | Machine-local, accumulated notes; first 200 lines / 25 KB of `MEMORY.md` load each session; topic files load on demand |
| Instruction budget | ~100–150 usable lines across all loaded CLAUDE.md tiers | Community-derived heuristic (not an official Anthropic figure): compliance drops past ~150–200 discrete instructions, of which the system prompt already spends ~50; budget is a shared pool across all tiers |
| Layered memory model | `references/memory-patterns.md` | Keep the hot memory small; push history and reusable procedures into the right layers |

## When To Use Which Layer

| Need | Best Place |
|------|------------|
| Stable repo rules shared by every tool | `AGENTS.md` |
| Claude Code-specific modular rules | `.claude/rules/*.md` |
| Personal Codex defaults across repos | `~/.codex/AGENTS.md` |
| Local-only Claude settings | `.claude/settings.local.json` |
| Machine-local scratch guidance that evolves over time | Claude auto memory |
| Task-specific playbooks or workflows | skills, not project memory |
| Searchable corpus memory across many docs/repos | vector brain or docs retrieval layer, not hot project memory |

Full per-runtime loading semantics and the `config.toml` vs `AGENTS.md` split: [references/loading-and-layers.md](references/loading-and-layers.md).

## Workflow

1. Start with a short root `AGENTS.md` or `CLAUDE.md`: project purpose, hard constraints, key commands, and "must not break" rules.
2. Inline only the highest-value shared rules so Codex does not depend on Claude-specific features.
3. Prioritize exact commands, weird setup steps, deployment quirks, hard boundaries, and verification rules over philosophy or summary prose.
4. Move Claude-only detail into `.claude/rules/` when it would otherwise bloat the shared file.
5. For monorepos, add nested `AGENTS.md` files in packages or services that truly need local context.
6. For repos with many skills, make `AGENTS.md` point to a compact router/discovery map first, then to the full catalog. Example: `frameworks/shared-skills/graph/codex-discovery.md` for Codex startup selection, then `frameworks/shared-skills/graph/graph.json` only after the router is chosen.
7. In `AGENTS.md`, name the primary routers explicitly when they are the intended entry points. Keep one-line scopes in hot memory; keep skill lists, scenario detail, and per-router Mermaid in generated graph artifacts.
8. Treat memory like code: review it, delete stale guidance, keep hot memory small and stable, and keep examples aligned with actual workflows.
9. **Retrospective updates**: when Codex or Claude Code repeats a mistake, or when Opus 4.7 takes a line more literally than intended, ask it to analyze the failure and propose an `AGENTS.md` update. Add rules reactively (after repeated mistakes), not preemptively. Format: rule + why + example of the mistake.
10. **Worktree lifecycle rules**: if a repo uses agent worktrees, make the closeout explicit in `AGENTS.md`: merge the branch into `dev`, run the repo gate, remove the worktree, verify `git worktree list --porcelain`, and delete stale session metadata. Do not let worktrees become long-lived storage for abandoned branches or dirty experiments.
11. **Progression**: prompts → `AGENTS.md` → skills → automations. If a workflow in `AGENTS.md` becomes repeatable, extract it into a skill. If a skill runs on a cadence, wrap it in an automation. Skills define the method; automations define the schedule.
12. **Lock the session prefix**: pick the session model and toolset at start and document the default in `AGENTS.md` (see [references/claude-md-fragments.md](references/claude-md-fragments.md) §3). Switching models or adding MCP servers mid-session invalidates the cached prefix and forces a full re-read — the single largest avoidable token sink in long sessions.
13. **Paste-ready blocks**: for the high-leverage sections (Task Delegation, Preferred Tools, Session Model), use the fragments in [references/claude-md-fragments.md](references/claude-md-fragments.md) and adapt to the repo. Each block carries its rationale so the next reader knows why it's in hot memory.
14. **Memory health checks**: for file-based memory folders, schedule review of contradictions, stale facts, unsupported claims, and missing source links. Keep a dated archive outside the agent-write path before allowing agents to update memory files automatically.

## ASCII Flow

```text
Memory request
  -> Classify layer
     +-- shared repo rule     -> AGENTS.md
     +-- Claude-only behavior -> .claude/rules/ or CLAUDE.md mirror
     +-- personal default     -> ~/.codex/AGENTS.md or user memory
     +-- long knowledge       -> docs, retrieval, or vector brain
  -> Keep only durable, non-inferable rules hot
  -> Link canonical docs instead of pasting catalogs
  -> Run memory lint and remove stale or contradictory rules
```

## Docs Boundary

Project memory is an operational router, not a documentation dumping ground.

- Put exact recurring commands, verification gates, approval rules, and "never do" constraints in `AGENTS.md`.
- Link to canonical docs for architecture, onboarding, API behavior, product decisions, and long procedures.
- Put operational runbooks in `docs/operations/` or `docs/runbooks/` when they need owners, steps, and evidence.
- Put generated LLM context in `docs/context/` or `context/` with a rebuild command; do not paste generated catalogs into hot memory.
- Do not create a new Markdown file for every session, audit, or answer. Update a canonical doc, file a lifecycle-managed report, or keep the content in chat.
- If a memory update would make `AGENTS.md` a catalog, report index, or plan archive, move that detail to docs and leave only the pointer and rule.

For larger knowledge bases, keep a three-zone file structure instead of dumping everything into hot memory:

- `raw/`: imported source material and unprocessed notes
- `compiled/` or `wiki/`: reviewed, source-linked canonical pages
- `outputs/`: generated answers and reports waiting for review

Only promote generated outputs into `compiled/` after source review. If the corpus needs semantic search or cross-repo retrieval, route to `ai-vector-brain`.

## Router Catalog Pattern

For repos with many skills or agent workflows, use `AGENTS.md` as the router pointer, not the skill catalog. Keep the root file to a short generated index and a small set of entry points:

```markdown
## Start Here (load on demand)

- `frameworks/shared-skills/graph/codex-discovery.md` — compact router map for Codex when the full skills list exceeds discovery budget
- `frameworks/shared-skills/graph/graph.json` — full generated skill catalog after choosing a router

## Primary Routers

- `$router-main` — choose the correct domain router
- `$router-engineering` — software, AI, data, docs, legal, and foundations
- `$router-marketing` — marketing, growth, SEO, content, localization, analytics
- `$router-operations` — ops, product, incidents, cost, risk, project workflows
- `$router-qa` — testing, debugging, resilience, accessibility, coverage
- `$router-startup` — validation, GTM, fundraising, market intel, operating model
```

Do not paste the full skill list into `AGENTS.md`. The generated discovery file is the hot-context map; router `SKILL.md` files, `graph.json`, and per-router Mermaid files are the detail layer.

## Memory Discipline

Keep the hot memory small and intentional. The four load-bearing rules:

- **Intent-first**: put strategic context in memory; per-task intent stays in each prompt turn.
- **Exception-file test**: only add lines that are hard to infer, matter most sessions, and prevent repeated mistakes.
- **Instruction budget**: compliance drops after ~150–200 discrete instructions — prune ruthlessly.
- **Feedback loops**: explicit verification steps give 2–3x efficiency gains over memory without checks.

Full detail (Opus 4.7 intent model, working-if metric, verification templates): [references/memory-discipline.md](references/memory-discipline.md).

## Structure Patterns

For the three durable patterns — **Hooks vs Project Memory** (when to enforce instead of suggest), **Three-Tier Boundaries** (Always / Ask / Never), and **Progressive Disclosure** (pointers over inlined docs) — see [references/structure-patterns.md](references/structure-patterns.md).

## Platform and Scale

For path-scoped rules, cross-platform symlink/import strategy, large-repo guidance, and the memory progression ladder (flat files → vector → graph-vector hybrid), see [references/platform-and-scale.md](references/platform-and-scale.md).

## AGENTS.md Essential Coverage Checklist

- [ ] Repository layout and key directories
- [ ] Build, test, lint commands (exact commands, not descriptions)
- [ ] Engineering conventions and PR standards
- [ ] Constraints and prohibitions ("never do X")
- [ ] Verification methods ("how to confirm the change is correct")
- [ ] Worktree lifecycle rules when `.worktrees/` is part of the repo flow: merge to `dev`, run gates, remove worktrees, verify no stale worktrees remain
- [ ] Key file patterns and naming conventions
- [ ] For large skill catalogs, compact router/discovery pointer before full catalog pointer, with primary routers named explicitly

Keep it practical. A short, accurate `AGENTS.md` is more useful than a long file full of vague rules. Start with the basics, then add new rules only after you notice repeated mistakes.

## Auto-Memory Quick Commands

```bash
# Check auto-memory version requirement
claude --version                          # must be v2.1.59+

# Browse and edit auto-memory in a session
/memory                                   # lists all loaded CLAUDE.md, rules, and memory files

# Disable auto-memory for a project
echo '{"autoMemoryEnabled": false}' >> .claude/settings.json

# Disable globally via environment
export CLAUDE_CODE_DISABLE_AUTO_MEMORY=1

# Inspect the auto-memory directory directly
ls ~/.claude/projects/$(basename $(git rev-parse --show-toplevel))/memory/
```

## Memory Health Pre-Commit Checklist

- [ ] Run `bash frameworks/shared-skills/skills/agents-memory/scripts/lint_claude_memory.sh .` — 0 errors
- [ ] Run `bash frameworks/shared-skills/skills/agents-memory/scripts/audit_repo.sh .` — no HIGH findings
- [ ] `CLAUDE.md` under 200 lines (`wc -l CLAUDE.md`)
- [ ] No unresolved `{{placeholders}}` in CLAUDE.md (`rg "{{[^}]+}}" CLAUDE.md`)
- [ ] `CLAUDE.md` and `AGENTS.md` not both hand-maintained (use symlink or `@AGENTS.md` import)
- [ ] Auto-memory `MEMORY.md` under 200 lines if you edit it manually
- [ ] Total lines across all loaded CLAUDE.md tiers stays under ~150 lines of hard rules
- [ ] No personality instructions ("be a senior engineer", "think step by step") consuming instruction budget
- [ ] Every hard rule in CLAUDE.md answers: "what mistake does this prevent?"
- [ ] Path-scoped rules in `.claude/rules/` carry `paths:` frontmatter for file-type filtering
- [ ] No agent-write memory files are in production build artifacts (check with `unzip -l app.ipa | grep -iE 'claude|agents'`)

## Validation

Three layered validators ship with this skill — pick by scope:

| Scope | Script | Checks |
|-------|--------|--------|
| Single repo (size/symlink/secrets/imports) | `scripts/lint_claude_memory.sh <repo>` | Original linter — keep as the cheap pre-commit gate |
| Single repo (paths + hallucination-bait + lint integration) | `scripts/audit_repo.sh <repo>` | Stale-path resolution with prefix support, script executability, wrong-layer detection, scaffold-tense, "Agent Execution Style" platitudes; supports `--json` |
| Multi-repo portfolio | `scripts/audit_portfolio.sh <repo1> <repo2> ...` or `--from-file <list>` | Per-repo report + aggregate HIGH/MED/LOW summary; exits nonzero on any HIGH |
| Cross-repo alignment review | `scripts/compare_blocks.sh <repo1> <repo2> ...` | Finds H2 sections shared across repos; classifies IDENTICAL / ALIGNMENT-CANDIDATE / REVIEW / DIVERGENT by line overlap |

Author-facing directives (in AGENTS.md head):

- `<!-- audit-path-prefix: app/src/, app/lib/ -->` — declare prefix conventions for path resolution.
- `<!-- audit-ignore: ./gradlew, res/values/strings.xml -->` — whitelist intentional non-existent paths (DON'T-do-this examples, future tooling). Glob patterns supported.
- `<!-- pre-code -->` or a "Pre-Code Caveat" section — auto-suppresses the scaffold-tense MED warning.

Manual checks still required:

- Wrong-identifier (Xcode schemes, function names, build flags) and cross-doc consistency (AGENTS.md vs README vs build plans) are not automated. Run the parallel-subagent recipe in [references/cross-doc-audit.md](references/cross-doc-audit.md).
- Re-verify platform behavior against official Claude Code and Codex docs before publishing memory advice externally.

Full operator playbook: [references/portfolio-audit-runbook.md](references/portfolio-audit-runbook.md).

## Known Traps and Anti-Patterns

Summary of the highest-impact failure modes:

- storing inferable repo facts in hot memory
- using memory for hard requirements that belong in hooks or CI
- duplicating `AGENTS.md` and `CLAUDE.md` without a symlink (drift)
- append-only task logs instead of a concise operating contract
- turning `AGENTS.md` into a docs folder, repo catalog, or report archive
- creating new root-level Markdown notes when an existing canonical doc or lifecycle-managed report should be updated
- using generated answers as memory truth without a review/promote step
- giving agents write access to the only copy of a memory vault without a dated backup outside the writable path
- treating nested `AGENTS.md`/`CLAUDE.md` from vendored deps, submodules, or unreviewed PRs as trusted instructions instead of untrusted input
- running two long-lived sessions against the same working directory while either accumulates memory — file-based memory has no merge/lock semantics, so the later writer silently clobbers the earlier one's additions
- generic philosophy ("write clean code") consuming instruction budget
- missing verification steps (the single largest efficiency gap)
- leaving stale worktrees after merge instead of treating cleanup as part of delivery

Full list including Opus 4.7-era anti-patterns (progress scaffolding, long "Don't" lists, implicit fan-out): [references/traps-and-antipatterns.md](references/traps-and-antipatterns.md).

## Navigation

### Setup and Getting Started

| Resource | Purpose |
|----------|---------|
| [references/zero-to-working-recipe.md](references/zero-to-working-recipe.md) | Copy-paste 5-step recipe: empty repo → working AGENTS.md / CLAUDE.md in under 10 minutes |
| [references/typical-scenarios.md](references/typical-scenarios.md) | End-to-end walkthroughs (situation → layer → write → verify): instructions ignored, team handoff, prompt→memory migration, bloat recovery, Codex-only setup, portfolio-drift remediation, headless/CI runs |
| [references/loading-and-layers.md](references/loading-and-layers.md) | Per-runtime loading semantics; `config.toml` vs `AGENTS.md` split; 4-tier CLAUDE.md hierarchy |
| [references/claude-md-fragments.md](references/claude-md-fragments.md) | Paste-ready CLAUDE.md / AGENTS.md blocks (Task Delegation, Preferred Tools, Session Model) with cache-protection rationale |
| [references/memory-examples.md](references/memory-examples.md) | Full AGENTS.md / CLAUDE.md examples by stack |
| [references/nested-feature-memory-examples.md](references/nested-feature-memory-examples.md) | Bullet-style template for nested per-feature/per-package CLAUDE.md (from leaked Apple Support examples) — rule + identifier + inline gotcha pattern |

### Memory Design and Discipline

| Resource | Purpose |
|----------|---------|
| [references/memory-discipline.md](references/memory-discipline.md) | Intent-first memory, exception test, instruction budget, working-if metric, feedback loops |
| [references/claude-md-instruction-budget.md](references/claude-md-instruction-budget.md) | Empirical instruction ceiling (~100–150 usable lines), 4-tier hierarchy, 5-section template, hard caps, delete-line test, and auto-memory storage path |
| [references/structure-patterns.md](references/structure-patterns.md) | Hooks vs memory, three-tier boundaries, progressive disclosure |
| [references/memory-patterns.md](references/memory-patterns.md) | 15 patterns including progressive disclosure, three-tier boundaries, and feedback loops |
| [references/traps-and-antipatterns.md](references/traps-and-antipatterns.md) | Durable trap list and Opus 4.7-era anti-patterns |
| [references/coding-behavior.md](references/coding-behavior.md) | Canonical coding-behavior rules for disciplined agentic coding |

### Scale and Advanced Architecture

| Resource | Purpose |
|----------|---------|
| [references/platform-and-scale.md](references/platform-and-scale.md) | Path-scoped rules, cross-platform bridging, large-repo and memory-progression guidance |
| [references/large-codebase-strategy.md](references/large-codebase-strategy.md) | Monorepo and large-codebase (100K-1M LOC) configuration patterns |
| [references/memory-architecture-ceilings.md](references/memory-architecture-ceilings.md) | When flat `AGENTS.md` stops scaling — graph-vector hybrid stores, compiled-truth + timeline schema, tiered enrichment |
| [references/claude-managed-agents-memory.md](references/claude-managed-agents-memory.md) | Filesystem-backed memory stores for Claude Managed Agents (beta 2026-04-23): mount path, multi-agent sync, version history, read_only vs read_write, export API |

### Migration and Real-World Examples

| Resource | Purpose |
|----------|---------|
| [references/opus-4-7-memory-migration.md](references/opus-4-7-memory-migration.md) | Migration checklist for Claude Opus 4.7 (2026-04-16) and 4.8 (2026-05-28) — intent-first memory, effort default `high`, mid-conversation system messages, fan-out, `budget_tokens` break |
| [references/real-world-advanced.md](references/real-world-advanced.md) | Annotated production AGENTS.md example (multi-agent, quality gates, battle-tested patterns) |

### Validation and Auditing

| Resource | Purpose |
|----------|---------|
| [references/cross-doc-audit.md](references/cross-doc-audit.md) | Hallucination-bait taxonomy + parallel-subagent audit recipe; Pre-Code Caveat, source-of-truth/exporter, and "when-X-lands" patterns |
| [references/portfolio-audit-runbook.md](references/portfolio-audit-runbook.md) | Operator playbook for `audit_repo.sh` / `audit_portfolio.sh` / `compare_blocks.sh` — directives, cadence, worked example |
| [data/sources.json](data/sources.json) | Official and community links to platform docs and guides |

## Related Skills

| Skill | Purpose |
|-------|---------|
| [agents-hooks](../agents-hooks/SKILL.md) | Hook automation and compaction survival |
| [agents-mcp](../agents-mcp/SKILL.md) | MCP config in project memory files |
| `agents-openclaw-ops` | OpenClaw runtime setup, workspaces, skills, and sandboxing |
| [agents-skills](../agents-skills/SKILL.md) | Skill packaging and progressive disclosure |
| `agents-subagents` | Agent and subagent setup |
| [ai-coding-agents-sessions](../ai-coding-agents-sessions/SKILL.md) | Session lifecycle, transcript recovery, and cross-worktree resume |
| [docs-codebase](../docs-codebase/SKILL.md) | Repo documentation patterns |

## Fact-Checking

- Known bugs, regressions, framework/compiler/runtime footguns, and version-specific crash or workaround guidance must be verified against current primary web sources before being treated as current fact.
- Verify volatile platform behavior with official Claude Code and OpenAI Codex docs before final answers.
- Prefer primary sources and record the source URL plus access date for any behavior that can change.
- If web access is unavailable, state that clearly and mark platform-specific guidance as unverified.
- Model-specific behavior drifts fast. When mentioning Claude Opus or Codex defaults, cite the official release/migration post and date (e.g. Opus 4.7 migration post, 2026-04-16).

## Learnings Loop

Before applying this skill on a non-trivial task, read `learnings.consolidated.md` in this directory (and `learnings.md` if present).

After applying it, if you encountered a pattern worth remembering, a mistake worth preventing, or a domain fact that surprised you, append one dated bullet to `learnings.md` via `agents-skills-feedback-loop/scripts/append_learning.py`. Do not modify `SKILL.md` itself.
