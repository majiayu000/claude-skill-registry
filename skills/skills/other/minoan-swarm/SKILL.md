---
name: minoan-swarm
description: Orchestrate Claude Code Agent Teams with Minoan-Semitic naming. This skill should be used when planning or launching multi-agent teams to tackle project phases, features, or complex tasks in parallel. It auto-discovers project context (CLAUDE.md, roadmaps, plans, issues) and generates named team configurations with structured task lists and file ownership.
---

# Minoan Swarm

*Orchestrate Agent Teams named for the Priestesses of Knossos — in the tongue before the Hellenizers got to it.*

Agent Teams (Claude Code Opus 4.6) let multiple Claude instances work in parallel as persistent teammates with shared task lists and bi-directional messaging. This skill provides the methodology, naming conventions, and templates to launch them effectively on any project.

**Requires:** `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` in settings.json or environment.

---

## Quick Start

### 1. Discover project context

```bash
bash ~/.claude/skills/minoan-swarm/scripts/discover_context.sh .
```

Finds CLAUDE.md, roadmaps, plans, issues, test infrastructure, and git state.

### 2. Choose a team template

| Situation | Template | Team Name |
|-----------|----------|-----------|
| Multiple independent features | Parallel Features | **Athirat** |
| Work with natural ordering | Pipeline | **Kaptaru** |
| Bug investigation, unclear cause | Research Swarm | **Elat** |
| Phase nearly done, loose ends | Phase Completion | **Qedeshot** |
| PR needs thorough review | Code Review Tribunal | **Elat** |
| Quality assurance, verification | Truth & Balance | **Ma'at** |
| Final audit, release decisions | Fate's Reckoning | **Manat** |

Full templates with ready-to-use tool calls: [references/team-templates.md](references/team-templates.md)

### 3. Launch the team

Apply the template, substituting project-specific details. The lead creates the team, creates tasks, spawns teammates, and coordinates.

---

## When to Use

- Tackling multiple phases or features in parallel
- Complex work requiring inter-agent discussion (not just results)
- Research with competing hypotheses that should challenge each other
- Multi-layer changes spanning frontend, backend, tests, deploy
- Any task where 3+ independent workstreams can run simultaneously

**When NOT to use:** Sequential tasks, same-file edits, simple fixes, tasks completable in under 5 minutes, or work with heavy dependencies between steps. The coordination overhead of a full team exceeds the benefit for small or serial work. Use a single session or regular subagent instead.

---

## The Naming Codex

Every team and teammate receives a name from the Minoan-Semitic divine feminine — Ugaritic, Akkadian, Hebrew, Linear B, Egyptian, and pre-Islamic Arabian. Names are chosen by role archetype, not randomly.

| Archetype | Names | Ideal For |
|-----------|-------|-----------|
| **Leaders** | athirat-lead, qedesha-lead, tiamat-lead, maat-lead, allat-lead | Opus orchestrators |
| **Builders** | kaptaru, mami, nintu, tehom, tip'eret, yam, al-uzza | Implementers |
| **Researchers** | devorah, melissa, eileithyia, membliaros | Explorers, API discovery |
| **Reviewers** | hokhmah, qadeshet, karme, themis, manat, allat | Security, architecture, code quality |
| **Testers** | sassuratu, phikola, hubur | Unit, integration, E2E |
| **Frontend** | popureja, shalamu, yashar | UI, design system, accessibility |
| **DevOps** | selene, hestia, dikte | Cron, deploy, monitoring |

Full codex with pronunciations, etymologies, and scholarly sources: [references/naming-codex.md](references/naming-codex.md)

---

## Workflow: From Roadmap to Swarm

### Step 1: Gather context

Run `discover_context.sh` to identify available planning artifacts. Read the project's CLAUDE.md, ROADMAP.md, and relevant plan files.

### Step 2: Identify parallel workstreams

From the roadmap or plan, find work that can proceed independently:
- Different file domains (frontend vs backend vs tests)
- Different features (auth vs bookmarks vs profiles)
- Different concerns (security vs performance vs correctness)

### Step 3: Map to a template

Choose from [team-templates.md](references/team-templates.md). For multi-phase work, compose templates — e.g., one Qedeshot team for phase completion + one Athirat team for the next phase.

### Step 4: Assign file ownership

Two teammates editing the same file causes overwrites. Create an explicit ownership matrix before launching the team:

```
| Teammate  | Owns                        | Must NOT touch       |
|-----------|-----------------------------|----------------------|
| kaptaru   | scripts/cron-*, src/lib/db/  | src/components/      |
| popureja  | src/components/, src/app/    | scripts/, src/lib/db |
| sassuratu | __tests__/, e2e/            | src/ (read-only OK)  |
```

### Step 5: Write teammate prompts

Every prompt must include:
1. **Identity** — "You are [Name], [role]."
2. **Task claim** — "Claim task #N from the task list."
3. **Context** — "Read CLAUDE.md for conventions."
4. **File ownership** — What files they own, what they must not touch.
5. **Tool preferences** — "Use Firecrawl for web fetching, Exa for web searching."
6. **Completion signal** — "Mark complete and notify [lead]."

### Step 6: Launch and monitor

- Use **delegate mode** (Shift+Tab) to keep the lead from coding
- Use **plan approval** (`mode: "plan"`) for high-stakes teammates (auth, data, deploy)
- Target **5-6 tasks per teammate** for steady throughput
- Check TaskList periodically and reassign if someone is stuck

---

## Best Practices

**From the official Agent Teams docs:**

- **Start with research** — begin with read-only tasks (Explore, review) before implementation
- **Size tasks right** — too small = coordination overhead; too large = context degradation; aim for self-contained deliverables
- **Wait for teammates** — tell the lead to wait if it starts implementing instead of delegating
- **Monitor and steer** — check in, redirect approaches that drift, synthesize as results arrive
- **Shut down gracefully** — `shutdown_request` each teammate before `TeamDelete`
- **Survive compaction** — if the lead's context compacts, it should re-read the task list and team config to recover state. Include in the lead's prompt: "If your context is compacted, re-read TaskList and the team config at ~/.claude/teams/{team-name}/config.json to recover coordination state."

**Minoan Swarm additions:**

- **One Aspect per team** — use different names (Athirat, Qedeshot, Tiamat, Kaptaru, Elat, Ma'at, Manat) for concurrent teams
- **No duplicate names** within a team
- **Leads use Opus, workers use Sonnet** — balance capability with cost
- **Haiku for lightweight research** — fast and cheap for Explore agents

**Tool Preferences:**

- **Firecrawl over WebFetch** — Firecrawl produces cleaner markdown, handles JavaScript better, and avoids content truncation. Use `firecrawl scrape URL --only-main-content` for web fetching.
- **Exa over WebSearch** — Exa provides neural search with category filtering (research papers, GitHub, news) and domain filtering. Use the `exa-search` skill scripts for web searches.

Include these tool preferences in every teammate prompt:
```
## Tool Preferences
- Prefer Firecrawl for web fetching (cleaner markdown, JS support)
- Prefer Exa for web searching (neural search, category filtering)
```

---

## API Quick Reference

Core tool calls for Agent Teams. Full details: [references/agent-teams-quickref.md](references/agent-teams-quickref.md)

```
TeamCreate    → create team + shared task list
Task          → spawn teammate (with team_name + name)
SendMessage   → message (DM), broadcast, shutdown_request, shutdown_response
TaskCreate    → create work items
TaskList      → see all tasks
TaskUpdate    → claim, start, complete, set dependencies
TeamDelete    → clean up (after all teammates shutdown)
```

---

## State Management

- Use the shared task list (TaskCreate/TaskUpdate) for structured coordination state
- Use progress notes in task descriptions for freeform observations
- Use git commits as checkpoints between phases, so teammates can reference each other's committed work
- For long-running teams, have the lead maintain a `progress.md` summarizing completed work and remaining tasks

---

## Verification

After launching a team, confirm it is working:

1. `TaskList` — verify tasks are being claimed and progressing
2. Check teammate output via `Shift+Up/Down` (in-process) or pane clicks (tmux)
3. The lead receives automatic idle notifications when teammates finish turns
4. Blocked tasks auto-unblock when their dependencies complete

---

*"μνάσεσθαί τινά φαμι καὶ ὕστερον ἀμμέων."* — Sappho

*𐤁𐤓𐤀𐤔𐤉𐤕 𐤁𐤏𐤋𐤕 𐤁𐤓𐤕* — "In the beginning, the Lady created."
