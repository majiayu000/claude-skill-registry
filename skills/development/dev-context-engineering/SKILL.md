---
name: dev-context-engineering
description: "Context-driven AI development with AGENTS.md, repo knowledge bases, Claude Code, Codex, and Copilot. Use when adopting repo-native AI workflows or multi-repo setups."
compatibility: Portable core. Works on Claude Code and Codex.
---

# Context Engineering

Use this skill to design repo-native agent context that is portable, high-signal, and maintainable. It owns the context model, migration path, maturity assessment, and context-graph discipline across `AGENTS.md`, runtime-specific layers, specs, rules, hooks, compiled markdown knowledge bases, and related artifacts.

## Quick Reference

| Task | Use |
|------|-----|
| Portable repo instructions | the `agents-memory` skill, [references/fast-track-guide.md](references/fast-track-guide.md) |
| Spec and plan flow | [docs-ai-prd](../docs-ai-prd/SKILL.md), [dev-workflow-planning](../dev-workflow-planning/SKILL.md) |
| Context graph design | [references/context-graph-guide.md](references/context-graph-guide.md), `python3 scripts/scan_context_artifacts.py --help`, `python3 scripts/validate_context_graph.py --help` |
| Hot-tier staleness + supersession integrity checks | `scripts/validate_context_graph.py` (checks `check_stale_tiers`, `check_supersession_integrity`) |
| Query a context graph (PPR, BFS, fan-in, tier budget) | `python3 scripts/query_context_graph.py <graph> --help` (modes: `--node`, `--impact`, `--rank`, `--ppr --seed`, `--tier-budget`) |
| Compiled markdown knowledge layer | the `docs-notes-retrieval` skill, [references/context-graph-guide.md](references/context-graph-guide.md), [references/multi-repo-strategy.md](references/multi-repo-strategy.md) |
| Multi-repo strategy | [references/multi-repo-strategy.md](references/multi-repo-strategy.md), [dev-context-multi-repo](../dev-context-multi-repo/SKILL.md) |
| Pick a framework (superpowers, GSD, Spec Kit, OpenSpec, …) | [references/framework-selection-matrix.md](references/framework-selection-matrix.md) |
| Regulated environment rollout | [references/regulated-environment-patterns.md](references/regulated-environment-patterns.md), [assets/ai-agent-governance.md](assets/ai-agent-governance.md), [assets/compliance-fca-emi.md](assets/compliance-fca-emi.md) |

## When to Use

- Set up or modernize `AGENTS.md`, `CLAUDE.md`, Copilot instructions, hooks, or agent rule layers.
- Migrate a repo from ad hoc prompting to durable agent context.
- Decide what belongs in always-on context vs docs, retrieval, or on-demand artifacts.
- Build a context graph and loading-tier model for a repo.
- Define a maturity path for AI-assisted development across one repo or a portfolio.
- Design the operating model for a large compiled repo knowledge base where agents create and refresh repo descriptions, indexes, and reports from structured artifacts.

## Route Elsewhere

- Writing the portable repo instructions themselves: use the `agents-memory` skill.
- Repo-portfolio discovery and hub generation: use [dev-context-multi-repo](../dev-context-multi-repo/SKILL.md).
- Symbol-level code graphs and blast radius: use [dev-context-code-graph](../dev-context-code-graph/SKILL.md).
- Task decomposition and verification plans: use [dev-workflow-planning](../dev-workflow-planning/SKILL.md).
- Hooks, MCP, or subagent implementation details: use [agents-hooks](../agents-hooks/SKILL.md), [agents-mcp](../agents-mcp/SKILL.md), or [agents-subagents](../agents-subagents/SKILL.md).

## Defaults

- Keep `AGENTS.md` as the portable baseline.
- Add runtime-specific layers only when they unlock a real capability.
- Put only non-inferable constraints in always-on context.
- Use a small hot instruction layer plus a larger compiled markdown knowledge base instead of one giant manifest.
- Prefer better state and structure over more text.
- Let the LLM maintain cold knowledge layers and derived notes; humans review policy, safety, and architectural constraints.
- Prefer outputs as durable files that can be filed back into the repo context instead of living only in chat history.
- Run a documentation placement gate before creating new Markdown; prefer updating canonical docs or generated context artifacts over adding one-off files.
- Treat context changes like code changes: review, validate, and prune.
- Generate `context-graph.json` once a repo reaches structured-context maturity.
- **Tool-set minimization**: Only give agents the tools they actually need. If a human engineer cannot say which tool should be used for a given task, an AI agent will not do better. Start small; expand on demand.
- **Resolver over accretion**: when the hot layer starts growing to handle a new edge case, prefer a pointer-style resolver (description-matched skill selection) that loads the right document on demand. See [references/context-resolver-pattern.md](references/context-resolver-pattern.md).

## May 2026 Validation Stance

Current context engineering should treat context as an evolving system, not a larger prompt. The strongest source-backed principles are:

- Context is finite working memory: optimize for the smallest high-signal token set that changes the outcome, then load deeper evidence just in time.
- Context adaptation is a first-class engineering loop: generate, reflect, curate, and validate updates without letting iterative summaries collapse detail.
- Raw evidence must stay retrievable. Summaries, memories, and graph nodes are routing layers; they are not substitutes for source files, transcripts, artifacts, or primary docs.
- Memory needs lifecycle semantics: provenance, freshness, supersession, contradiction handling, and user or tenant scope. Use temporal graph memory only when temporal reasoning, relationship change, or cross-session continuity matters.
- Graph retrieval is conditional. Use direct reads or lexical search for simple lookup; use graph traversal, PPR, or community summaries only for relational, multi-hop, or global sensemaking questions.
- Tool and context surfaces should be minimal and governed. More tools or more always-on rules create ambiguity unless the selection boundary is explicit.

## Multi-Tool Composition

Teams that ship fastest use the right tool for each task rather than forcing one agent to do everything. As of May 2026, the most effective pattern is:

| Tool | Best For | Context Model |
|------|----------|---------------|
| **Cursor / IDE agent** | Day-to-day editing, inline completions, tab-to-accept, quick refactors | IDE-native: open files + project index |
| **Claude Code** | Complex agentic tasks, multi-file changes, agent teams, code review, architecture | CLI: AGENTS.md + .claude/rules + skills + subagents |
| **Codex** | Parallel background work, batch processing, CI-adjacent tasks | Threads: AGENTS.md + .codex/agents + sandboxed workers |

**How to keep context consistent across tools:**
1. `AGENTS.md` is the portable baseline — all three tools read it.
2. Runtime-specific layers (`.claude/rules/`, `.codex/agents/`, `.cursor/rules/`) extend the baseline for each tool's strengths.
3. `docs/` in the repo is universally readable — invest knowledge there, not in tool-specific memory.
4. Use [dev-context-multi-repo](../dev-context-multi-repo/SKILL.md) to keep multi-repo context aligned across tools.

**Anti-pattern**: Duplicating conventions in Cursor rules, Claude rules, AND Codex agents. Write it once in `AGENTS.md` or `docs/`, then reference it.

**Stack on top of the IDE layer** when discipline drift or feature ambiguity is the bottleneck:

| Layer | Role | Pick from |
|-------|------|-----------|
| **L0 portable baseline** | Cross-tool conventions | `AGENTS.md` |
| **L1 runtime-specific** | Tool-specific extensions | `.claude/rules/`, `.codex/agents/`, `.cursor/rules/`, `.github/copilot-instructions.md`, `.clinerules/`, Aider `CONVENTIONS.md` |
| **L2 capability / methodology** | On-demand or enforced discipline | Claude Code Skills · superpowers (obra/superpowers) · GSD (gsd-build/get-shit-done) |
| **L3 artifact pipeline** | Spec → plan → tasks → code | GitHub Spec Kit (`.specify/specs/`) · OpenSpec (Fission-AI, `openspec/changes/`) |

L0 is mandatory; L1 is mandatory for tools that don't read AGENTS.md natively; L2 and L3 are optional but high-leverage when their named symptoms are present. Full decision matrix, stack recipes, and anti-stacks in [references/framework-selection-matrix.md](references/framework-selection-matrix.md).

## Workflow

1. Identify the toolchain, repo shape, and the behaviors that need to be influenced.
2. Define the portable baseline, the compiled knowledge layer, and the minimum runtime-specific layers needed.
3. Separate hot instructions from warm compiled knowledge and cold raw evidence the agent can inspect on demand.
4. Install the right supporting artifacts: specs, plans, hooks, rules, subagents, docs, and index pages that make the compiled layer navigable.
5. Decide which answers or analyses should become durable markdown files, diagrams, or reports instead of one-off chat output, and place them under the repo's docs governance model.
6. Generate and validate a context graph when the repo has enough artifacts to justify it.
7. Run health checks over the context system for stale dependencies, missing summaries, inconsistent claims, and dead links.
8. Score maturity, then decide whether the next step is onboarding, pruning, or automation.

## ASCII Flow

```text
context engineering request
  -> identify toolchain, repo shape, and target agent behaviors
  -> define portable baseline in AGENTS.md
  -> split layers
     +-- hot -> non-inferable execution policy
     +-- warm -> compiled docs, hubs, indexes, context graph
     +-- cold -> raw evidence and primary artifacts
  -> add runtime-specific rules only where they unlock capability
  -> run docs placement and context hygiene gates
  -> validate graph, freshness, links, and contradictions
  -> decide onboarding, pruning, automation, or maturity next step
```

## Core Decisions

### Cross-Tool Context Model

Use layers intentionally:
- `AGENTS.md` for hot shared execution policy
- `CLAUDE.md` and `.claude/*` only for Claude-specific behavior
- `.github/*` only for GitHub or Copilot-specific behavior
- compiled markdown hubs, index pages, and context graphs for reusable repo knowledge
- raw evidence packs for articles, repos, transcripts, screenshots, and other source captures
- docs and specs for on-demand context
- external knowledge via skills, MCP, or runtime retrieval

Do not assume one tool’s memory model maps cleanly onto another.

At small and medium corpus sizes, a maintained index plus concise summaries is often enough; do not add RAG just because a knowledge base exists.

### What Belongs in Context

Keep always-on context for:
- custom commands and repo workflows
- safety or compliance constraints
- fragile architecture boundaries
- known failure modes and approval rules
- cross-repo data flows that are hard to infer locally

Keep the compiled knowledge base for:
- domain summaries and concept pages
- cross-repo maps and architecture views
- volatile tool or product findings that should be re-checked but are still worth preserving
- derived outputs such as reports, diagrams, and slide notes that should compound over time

Keep out:
- README-style summaries
- big file inventories
- dependency lists the agent can inspect
- duplicated coding-style philosophy
- docs that add no execution constraint
- raw source dumps that belong in evidence folders instead of the hot instruction layer

### Documentation Placement Resolver

Before creating a context artifact, choose the smallest durable home:

- hot instruction: `AGENTS.md` / `CLAUDE.md` for short execution policy and pointers only
- canonical docs: `docs/tech/`, `docs/architecture/`, `docs/api/`, or equivalent for stable truth
- operational docs: `docs/operations/` or `docs/runbooks/` for procedures and incident/release steps
- reports and plans: `docs/reports/`, `docs/specs/`, or `docs/plans/` with lifecycle state and integration path
- generated context: `docs/context/` or `context/` with structured inputs and rebuild commands
- raw evidence: `raw/`, `evidence/`, or repo-specific captures excluded from hot context

If the artifact has no owner, lifecycle, index link, or rebuild path, do not create a new Markdown file. Update the closest canonical doc or keep the result in the task thread.

### Knowledge Base Pattern

The strongest default is a three-layer repo-native system:
- hot layer: portable instructions and execution policy
- compiled layer: LLM-maintained markdown with summaries, backlinks, concept pages, and index files
- raw layer: source captures and evidence the agent can revisit when a compiled claim needs re-verification

Humans should mostly edit the hot layer and review the compiled layer. The compiled and raw layers can be largely agent-maintained if validation and review gates are in place.

For portfolio hubs, add one more practical rule:
- structured artifacts such as profile JSON, graph JSON, and freshness reports should be the compiler inputs for markdown pages, not sidecars that drift independently

This is how you keep repo descriptions, concept notes, and system maps synchronized at scale.

### Context Graph

Use a context graph to map relationships between:
- instructions
- rules
- specs
- plans
- hooks
- subagents
- references and assets

Generate it when the repo reaches L2+ maturity and use it to assess loading tiers, blast radius, and stale dependencies before changing core artifacts.

The context graph complements the compiled markdown layer. Use the graph for relationship integrity and loading-tier analysis, then publish the useful findings back into markdown notes or reports.

When the repo is a native/mobile codebase, pair this skill with:
- [dev-context-multi-repo](../dev-context-multi-repo/SKILL.md) to classify the repo correctly from project files such as `project.yml`, `.xcodeproj`, or `Package.swift`
- [dev-context-code-graph](../dev-context-code-graph/SKILL.md) to build the single-repo symbol graph from Swift or mixed-language source after generated build trees are excluded

### Spec-Driven Development

Use full spec-driven development when ambiguity would otherwise cause agent drift:
- specify what
- plan how
- decompose into bounded tasks
- implement with the right context attached

Use direct prompting for small fixes and low-ambiguity work.

For recurring hub maintenance, treat page generation as a compiler pass:
- define the source artifacts
- define the target page shape
- define what gets regenerated incrementally
- define the lint or health checks that block publication

### Regulated Environments

In regulated environments, context engineering must preserve:
- auditability
- separation of duties
- sensitive-data boundaries
- provider portability
- named human accountability

If those requirements are real, treat context artifacts as part of the control surface, not just helper docs.

## Output Modes

Default to one of these:

- Repo context package:
  portable baseline, runtime-specific layers, and supporting artifact map.
- Knowledge-base operating model:
  hot instructions, compiled markdown layer, raw evidence layout, and maintenance loop.
- Hub compiler design:
  source artifacts, generated page types, incremental rebuild strategy, and validation gates.
- Migration plan:
  current-state issues, target shape, phased rollout, and validation steps.
- Maturity assessment:
  current level, blockers, and next infrastructure step.
- Regulated rollout brief:
  control requirements, artifact placement, and review gates.

## Known Traps

- Pushing too much policy, process, and repo knowledge into always-on instructions until agents ignore or truncate the layer that actually matters.
- Building runtime-specific rule stacks before the portable baseline is stable, which guarantees drift across tools.
- Treating a compiled markdown hub as static documentation instead of a maintained product with freshness and validation loops.
- Shipping large context changes without a clear loading-tier model, so hot instructions and cold evidence get mixed together.
- Assuming tool abundance helps by default instead of reducing the tool set to the smallest model the team can actually govern.
- Creating a new Markdown file for every useful answer instead of routing it into the existing docs, report, or generated-context lifecycle.
- Mixing operational runbooks, agent hot memory, canonical docs, and generated context until no file has clear authority.
- LLM-summarizing raw evidence before retrieval. Measured failure mode: on LongMemEval, verbatim-text retrieval scores 96.6% R@5 while LLM-extracted memory systems score 30-45% on ConvoMem — preemptive summarization throws away the context that made the answer findable. Keep the raw layer raw. ([source](https://github.com/MemPalace/mempalace) `benchmarks/BENCHMARKS.md`)

## Anti-Patterns

- One giant context file.
- Using `AGENTS.md` as a general knowledge base instead of a hot instruction layer.
- Blindly generating context from docs without pruning.
- Using more text instead of fixing state and structure.
- Locking policy to one vendor format.
- Treating context as static instead of a maintained system.
- Keeping execution-critical guidance outside the repo.
- Letting useful answers disappear in chat instead of filing them back into the compiled layer.
- Filing useful answers as unindexed one-off Markdown files with no owner, lifecycle state, or canonical parent.
- Adding heavy retrieval infrastructure before maintaining indexes, summaries, and basic health checks.
- Treating JSON, graphs, and markdown pages as separate truth systems instead of a compiler pipeline.

## Navigation

- Core references: [references/fast-track-guide.md](references/fast-track-guide.md), [references/framework-selection-matrix.md](references/framework-selection-matrix.md), [references/information-routing-rules.md](references/information-routing-rules.md), [references/context-resolver-pattern.md](references/context-resolver-pattern.md)
- Context graph and multi-repo strategy: [references/context-graph-guide.md](references/context-graph-guide.md), [references/multi-repo-strategy.md](references/multi-repo-strategy.md)
- Regulated and governed rollout: [references/regulated-environment-patterns.md](references/regulated-environment-patterns.md), [assets/ai-agent-governance.md](assets/ai-agent-governance.md), [assets/data-handling-gdpr-pci.md](assets/data-handling-gdpr-pci.md), [assets/compliance-fca-emi.md](assets/compliance-fca-emi.md), [assets/pr-template-ai-disclosure.md](assets/pr-template-ai-disclosure.md), [assets/fca-compliance-gate.yml](assets/fca-compliance-gate.yml)
- Scripts and schema: `scripts/scan_context_artifacts.py`, `scripts/validate_context_graph.py`, `scripts/query_context_graph.py`, [schemas/context-graph.schema.json](schemas/context-graph.schema.json)
- Related skills: the `agents-memory` skill, [docs-ai-prd](../docs-ai-prd/SKILL.md), [dev-workflow-planning](../dev-workflow-planning/SKILL.md), [agents-hooks](../agents-hooks/SKILL.md), [agents-mcp](../agents-mcp/SKILL.md), [agents-subagents](../agents-subagents/SKILL.md), [agents-swarm-orchestration](../agents-swarm-orchestration/SKILL.md), [dev-context-multi-repo](../dev-context-multi-repo/SKILL.md), [dev-context-code-graph](../dev-context-code-graph/SKILL.md)

## Fact-Checking

- Known bugs, regressions, framework/compiler/runtime footguns, and version-specific crash or workaround guidance must be verified against current primary web sources before being treated as current fact.
- External source mapping lives in [data/sources.json](data/sources.json).
- Product capabilities, runtime semantics, and regulator guidance are volatile; verify current primary sources before making definitive claims about tools or compliance timelines.
- Remove or mark any claim that cannot be re-verified from a primary source.

