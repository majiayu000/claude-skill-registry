---
name: axi
description: >
  Agent eXperience Interface (AXI) router — the main entry point for agent-ergonomic
  CLIs. Use whenever the agent needs GitHub, browser automation, human review, quota
  routing, Slack, Notion, AWS/Docker/K8s, databases, GitLab (glab-axi), Oracle DB
  (oracle-axi), tmux/herdr/WezTerm sessions (cyber-mux), or any AXI-catalog tool; when
  choosing AXI vs MCP vs raw CLI; when building or reviewing an agent-facing CLI; or
  when the user says axi, gh-axi, chrome-devtools-axi, TOON output, agent ergonomics,
  or "prefer AXI". When in doubt about which external tool interface to use, start here.
allowed-tools:
  - Bash(npx *)
  - Bash(gh-axi *)
  - Bash(chrome-devtools-axi *)
  - Bash(mktg *)
  - Bash(which *)
  - Bash(npm *)
  - Read
  - Write
---

# /axi — Agent eXperience Interface Router

AXI is not a protocol. It is **10 design principles** for agent-ergonomic CLIs that beat both raw CLI and MCP on success, cost, duration, and turns ([axi.md](https://axi.md), [kunchenguid/axi](https://github.com/kunchenguid/axi)).

This skill is the **main router** for the AXI catalog (official + community). It picks the right AXI, installs/runs it agent-first (`npx -y <axi>`), and teaches the principles when you build or review agent-facing CLIs.

## North Star

| Depth | File |
|---|---|
| 10 principles (full spec) | [rules/principles.md](rules/principles.md) |
| Official + community catalog | [rules/catalog.md](rules/catalog.md) |
| AXI vs MCP vs raw CLI vs mktg tools | [rules/prefer-axi.md](rules/prefer-axi.md) |
| Build / review an AXI | [rules/build.md](rules/build.md) |
| Benchmark numbers | [rules/benchmarks.md](rules/benchmarks.md) |
| Upstream build-skill snapshot | [references/upstream-axi-skill.md](references/upstream-axi-skill.md) |

## Workflow (escalation)

0. **Unclear** — User wants "the right tool." Detect domain → route via the table. Explain out loud.
1. **Use** — An AXI exists for the domain. Prefer `npx -y <axi> …` (zero global install). Fall back to global binary if already on PATH.
2. **Ambient** — Repeated sessions in one domain → suggest `<axi> setup hooks` (SessionStart) after explicit user opt-in.
3. **Build / review** — Designing an agent-facing CLI → load [rules/principles.md](rules/principles.md) + [rules/build.md](rules/build.md). Do not invent a parallel MCP server first.
4. **Missing AXI** — No catalog entry → prefer the least-bad existing path (mktg skill, raw CLI, MCP) per [rules/prefer-axi.md](rules/prefer-axi.md), and offer to scaffold a new AXI.

## On Activation (every time)

1. Restate the domain in one sentence ("You need GitHub PR/CI triage" / "You need live browser extraction").
2. Probe availability (non-blocking):
   - `which gh-axi chrome-devtools-axi 2>/dev/null; npx -y gh-axi --version 2>/dev/null | head -1`
   - Optional: `mktg doctor --json --fields checks` and note `cli-gh`, `cli-gh-axi`, `cli-chrome-devtools-axi`.
3. Route via the **AXI Routing Table**. Always say why: "I'm using `gh-axi` instead of raw `gh` / GitHub MCP because AXI wins on cost and success for GitHub tasks."
4. Prefer **content-first** invocation: run the AXI with no args once to see live state + `help[]` next steps, then follow those templates.
5. If the user is **building** a CLI for agents → skip catalog routing; open principles + build rules.
6. Never silently fall back to MCP when an AXI exists for that domain.

## AXI Routing Table

| Need | AXI | Install / run | Layer |
|---|---|---|---|
| GitHub issues, PRs, CI runs, releases, secrets, projects | `gh-axi` | `npx -y gh-axi` (needs `gh auth login`) | Official |
| Browse, click, fill, extract, tables, Lighthouse | `chrome-devtools-axi` | `npx -y chrome-devtools-axi` | Official |
| Human review of HTML artifacts (annotate → agent feedback) | `lavish-axi` | `npx skills add kunchenguid/lavish-axi` / see catalog | Official |
| Local Claude/Codex/Cursor/Copilot/Grok quota windows | `quota-axi` | see [rules/catalog.md](rules/catalog.md) | Official |
| Jujutsu history | `jj-axi` | community | VCS |
| npm registry inspect | `npm-axi` | community | Packages |
| SQLite inspect / capped queries | `sqlite-axi` | community | Data |
| Slack read/search/draft | `slack-axi` | community | Comms |
| Gmail/Calendar/Docs/Drive/Slides (draft-only mail) | `gws-axi` | community | Workspace |
| Harvest time tracking | `harvest-axi` | community | Ops |
| Spec-driven agent workflow (AXI-in-skill demo) | `specops` | community | Process |
| Git-backed record sheets | `gitsheets-axi` | community | Data |
| Metabase SQL/MBQL | `metabase-axi` | community | Analytics |
| Otter.ai transcripts | `otter-axi` | community | Meetings |
| Notion pages/databases | `notion-axi` | community | Docs |
| ClickUp tasks | `clickup-axi` | community | Tasks |
| Databricks jobs/runs | `databricks-axi` | community | Data |
| AWS host/deploy | `aws-axi` | community | Cloud |
| Docker app lifecycle | `docker-axi` | community | Cloud |
| DynamoDB | `dynamodb-axi` | community | Data |
| PostgreSQL | `pg-axi` | community | Data |
| MongoDB | `mongodb-axi` | community | Data |
| Elasticsearch | `elasticsearch-axi` | community | Data |
| Kubernetes workloads | `kubernetes-axi` | community | Cloud |
| Redis | `redis-axi` | community | Data |
| Celery queues | `celery-axi` | community | Cloud |
| Oracle DB | `oracle-axi` | community | Data |
| tmux / herdr / WezTerm sessions | `cyber-mux` | community (overlaps `/tmux`, `/herdr`) | Terminal |
| GitLab issues / MRs / pipelines | `glab-axi` | community | VCS |
| Design / review agent CLI ergonomics | (this skill → principles) | read rules | Meta |
| Marketing playbook (brand, content, publish) | `/cmo` | `mktg` skills | Out of scope |

Full URLs + one-liners: [rules/catalog.md](rules/catalog.md).

## Disambiguation

| User says | Route to | Not | Why |
|---|---|---|---|
| "check the PR / CI / issues" | `gh-axi` | raw `gh`, GitHub MCP | AXI: 100% success @ $0.050 vs CLI 86% / MCP ~$0.10–0.15 |
| "open this page / click / fill form / extract table" | `chrome-devtools-axi` | chrome-devtools-mcp, agent-browser | Combined ops + `--query`; 100% @ $0.074, 4.5 turns |
| "scrape this URL I already have" (static content) | `firecrawl` / `exa-contents` | `chrome-devtools-axi` | Don't pay for a browser when fetch/crawl is enough |
| "search the web for X" (unknown URLs) | `exa-search` / Exa MCP | `chrome-devtools-axi` | Semantic search ≠ browser automation |
| "automate Instagram/TikTok login post" | `/cmo` + browser profile / `mktg publish` | `chrome-devtools-axi` alone | Marketing distribution is `/cmo`'s job |
| "help me market / write copy / SEO" | `/cmo` | `/axi` | AXI routes tools; CMO routes marketing skills |
| "build a CLI for my agent" | `/axi` principles + build | MCP-first design | Principled CLI beats MCP on the published benches |
| "use MCP for GitHub/browser" | Prefer matching AXI first | Eager MCP schemas | MCP schema overhead ~2.3× input tokens in GitHub bench (185K vs 79K) |
| "what's my Cursor/Claude quota" | `quota-axi` | guessing from UI | Local-first usage windows for routing-aware agents |
| "review this HTML with humans" | `lavish-axi` | paste into chat | Annotation loop back to the agent |

## First 5 Minutes (new machine)

1. Confirm Node 20+ for `npx`.
2. For GitHub work: `gh auth login` once, then `npx -y gh-axi` (home view).
3. For browser work: `npx -y chrome-devtools-axi open https://example.com --query "Example"`.
4. Optional ambient context: `npm i -g gh-axi && gh-axi setup hooks` (restart session).
5. Tell the user which AXI you chose and the one-line why.

## Guardrails

- **Prefer AXI when a catalog entry exists** for that domain. Explain the preference; don't debate protocol religion.
- **Zero-install first:** `npx -y <axi> …` before asking the user to `npm i -g`.
- **Follow `help[]`:** AXI outputs next-step command templates — use them; don't invent flags.
- **Fail loud:** unknown flags must error (exit 2). Never invent flags and trust unscoped output.
- **No interactive prompts.** If a required value is missing, fail with a structured error + suggested command.
- **Pipe for tokens:** `| head`, `| rg` on AXI stdout is encouraged; don't dump full snapshots into context when `--query` exists.
- **Skills never call skills.** `/axi` orchestrates tool choice; leaf AXIs execute. Exception: `/cmo` owns marketing — hand off explicitly.
- **Hooks are opt-in.** Never run `setup hooks` without clear user intent.
- **TOON on the wire.** When building AXIs, stdout is TOON; keep internals on JSON. Spec: https://toonformat.dev/

## Anti-Patterns

| Anti-pattern | Why it's wrong | Do this instead |
|---|---|---|
| Loading full MCP tool schemas for GitHub/browser when an AXI exists | Schema tax balloons input tokens every turn | Route to `gh-axi` / `chrome-devtools-axi` |
| `navigate` then separate `snapshot` every click | Doubles turns; AXI combines ops | `open`, `click --query`, `fill … --submit` |
| Dumping full page snapshots into context | Burns the token budget | `--query "…"`, pipe filters, truncation + `--full` |
| Silent fallback to raw `gh` because "I know the flags" | Raw CLI loses accuracy on the GitHub bench | Use `gh-axi`; keep `gh` only for gaps AXI doesn't wrap yet |
| Building a new MCP server before an AXI CLI | Protocol choice ≠ ergonomics | Apply the 10 principles; ship CLI + optional skill + optional hooks |
| Presenting the entire catalog as a menu | Shifts the decision to the human | Recommend 1 AXI with a one-line why |
| Using browser AXI for static URL fetch | Overkill cost/latency | `firecrawl` / `exa-contents` / `curl` |

## Error Recovery

| Failure | Fix |
|---|---|
| `npx` / network blocked | Install global once: `npm i -g gh-axi` (or the needed AXI); retry |
| `gh-axi` auth error | `gh auth login` (and `gh auth refresh -s project` when Projects need scope) |
| `chrome-devtools-axi` bridge stale | `chrome-devtools-axi stop` then retry; or new `CHROME_DEVTOOLS_AXI_SESSION=…` |
| `STALE_REF` on click | Re-`snapshot` / `open --query` and use the new `@g:…` ref |
| Unknown command (`navigate`) | Read AXI `help[]` / `--help` — prefer `open`, not MCP verb names |
| No AXI for domain | Use prefer-axi fallback; offer to scaffold per [rules/build.md](rules/build.md) |

## Progressive Enhancement

| Level | What `/axi` can do |
|---|---|
| L0 | Route by domain; run via `npx -y` with no prior setup |
| L1 | Binaries on PATH; faster cold start |
| L2 | `setup hooks` ambient home views for Claude Code / Codex / OpenCode |
| L3 | Multiple community AXIs installed; quota-aware routing via `quota-axi` |
| L4 | Team ships internal AXIs using principles + contributor catalog workflow |

## Attribution

Principles, catalog, and benchmarks from [AXI](https://axi.md) / [kunchenguid/axi](https://github.com/kunchenguid/axi) (MIT). This mktg skill is the **router + catalog orchestrator** adapted for `/cmo`-style activation; the upstream build-skill snapshot lives in `references/upstream-axi-skill.md`.
