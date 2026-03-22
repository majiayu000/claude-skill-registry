---
name: project-orchestrator:brainstorming
description: "Use this before any feature work. Full lifecycle: brainstorm, design, implement with parallel Teams, two-stage review, and compaction-safe state on disk."
user-invocable: false
---

# Feature Lifecycle

## Overview

Turn feature ideas into designs and implementations. Full lifecycle in one skill: brainstorm → design → implement → review → finish.

**Do NOT explore the entire codebase upfront.** Read architecture docs (if configured in `project.yml`) for context, then ask which services are affected. Only explore those specific service directories.

## Config Loading

Before anything else, load project config:

1. Check if `.project-orchestrator/project.yml` exists
2. If yes: parse and extract `services`, `plans_dir`, `plans_structure`, `architecture_docs`, `implementation`, `models`, `brainstorm`, `review`
3. If no: use defaults (monorepo, single service at root, `docs/plans/` flat structure)
4. Read architecture docs if paths configured: `config.architecture_docs.agent`, `config.architecture_docs.domain`
5. If architecture docs don't exist, skip — proceed without system topology context

**Config validation:**
- `brainstorm.default_depth` must be `shallow`, `medium`, or `deep` — error otherwise
- `models.explorer` and `models.implementer` must be `opus`, `sonnet`, or `haiku`
- Warning (not error) if `brainstorm.perspective_docs` key not in `brainstorm.designer_perspectives`
- `review.max_fix_iterations` must be 1-5 — error: "max_fix_iterations must be 1-5"
- `review.fix_timeout_turns` must be 5-30 — error: "fix_timeout_turns must be 5-30"

**Review config defaults (v2):**
| Key | Default | Description |
|-----|---------|-------------|
| `review.speculative_quality` | `true` | Run quality in parallel with spec on first review |
| `review.max_fix_iterations` | `2` | Max fix attempts before human escalation |
| `review.fix_timeout_turns` | `10` | Max agent turns per fix attempt |
| `review.auto_approve` | `false` | Auto-approve high-confidence passes |
| `review.auto_reject` | `false` | Auto-send-to-implementer high-confidence failures |

## Agent Preferences

| Role | Model | Type | Notes |
|------|-------|------|-------|
| Explorers | `config.models.explorer` (default: sonnet) | explorer agent (brainstorm team) | One per service, report to lead only |
| Designers | Opus | Team member (brainstorm team) | From `config.brainstorm.designer_perspectives` (default: ["simplicity", "scalability"]) |
| Implementers | `config.models.implementer` (default: opus) | implementer agent (implement team) | Max `config.implementation.max_parallel` (default 3) parallel |
| Spec reviewer | Per `config.review.strategy` | spec-reviewer agent | One-shot per task, skill auto-loaded via agent frontmatter |
| Quality reviewer | Per `config.review.strategy` | quality-reviewer agent | One-shot per task, skill auto-loaded via agent frontmatter |

- **Never run agents in background** — always foreground
- **Team naming:** `brainstorm-{feature-slug}` / `implement-{feature-slug}`
- **No peer messaging** — all team members report to lead only

## Living State Document

All important state lives on disk at `{config.plans_dir}/YYYY-MM-DD-{slug}-design.md`. This is the source of truth that survives compaction. Any agent can read it to get full context.

**Directory lifecycle** (when `config.plans_structure` is `standard`):
- `{plans_dir}/` (root) = active only (`designing` / `approved` / `in-progress`)
- `{plans_dir}/completed/` = shipped
- `{plans_dir}/backlog/` = scoped but not scheduled
- `{plans_dir}/ideas/` = explorations, no commitment

When `config.plans_structure` is `flat`, all plans stay in `{plans_dir}/` regardless of status.

When status changes (standard structure), move the file to the matching directory and update INDEX.md.

**Strict template:**

```markdown
# {Feature Name} — Design & Implementation

## Status: brainstorming | designing | approved | implementing | reviewing | complete

## Design

### Feature Type
{endpoint/scraper/UI/cross-service/infra}

### Services Affected
{list of services}

### Design Details
{design content using templates from Design Templates section below}

## Implementation Tasks

| # | Task | Service | Status | Assignee | Spec | Quality | Fix Iterations |
|---|------|---------|--------|----------|------|---------|----------------|
| 1 | ... | backend | pending | — | — | — | — |
| 2 | ... | frontend | in-progress | implement-auth | — | — | — |
| 3 | ... | backend | complete | implement-api | ✅ | ✅ | 0 |

## Implementation Log

### Task N — {title}
- **Files changed:** {service}/{path} — {what changed}
- **Commit:** {short sha}
- **Spec review:** ✅ / ❌ {notes}
- **Quality review:** ✅ / ❌ {notes}
- **Recovery:** NO_CHANGES (attempt 1), STALLED (attempt 2)  ← optional, only when recovery occurred

## Test Plan              ← optional, added during brainstorming if UI feature has browser tests
## Test Results           ← optional, filled by /project:test

## Decisions & Context
{Key decisions, gotchas, patterns chosen — helps fresh agents after compaction}
```

Update this document at every significant step. It is the coordination artifact.

---

# Phase 1: Brainstorm & Design

## 1. Minimal context gathering
- Read architecture docs if configured in `project.yml` (`config.architecture_docs.agent`, `config.architecture_docs.domain`)
- **Include relevant sections in every spawned agent's prompt** (subagents don't inherit lead context)
- Do NOT run broad codebase exploration
- Ask one question at a time, prefer multiple choice

## 2. Scope the services FIRST

Which service(s) does this affect? Present the list from `config.services[].name`. If no services configured, ask the user to describe the affected areas.

## 3. Classify the feature type

- [ ] New endpoint/API
- [ ] UI feature
- [ ] Cross-service data flow
- [ ] Configuration/infra
- [ ] Other

## 4. Choose exploration depth

- [ ] Shallow: Read architecture docs, 1-2 key files → simple changes
- [ ] Medium: Explore 1 service directory patterns → typical features
- [ ] Deep: Multiple service exploration, existing impl review → cross-cutting changes

Default: `config.brainstorm.default_depth` (default: `medium`). User can always override.

## 5. Team decision

```
services <= 2 AND depth = shallow → NO TEAM (regular Task agents)
services <= 2 AND depth = medium  → NO TEAM (regular Task agents)
services >= config.brainstorm.team_threshold (default: 3) OR depth = deep → TEAM (brainstorm-{slug})
```

## 6a. Team exploration (when team triggered)

```
TeamCreate("brainstorm-{slug}")
TaskCreate per affected service
Spawn explorer agent per service (team_name, name: "explore-{service}")
  → Prompt: user's problem/feature description + which service directory to focus on
  → Include architecture doc excerpts relevant to that service
  → Agent explores service dir, existing patterns, recent changes
  → Reports via TaskUpdate (mark completed)
  → No peer messaging
Lead waits for all exploration tasks completed
```

Each explorer captures:
- Existing patterns relevant to the feature
- API endpoints / routes affected
- Database tables / schemas involved
- Event pipelines published or consumed
- Tech debt or gotchas

## 6b. Simple exploration (no team)

- Spawn 1-2 explorer agents via Task tool (foreground)
- **Each agent prompt:** user's problem/feature description + which service directory to focus on
- Include architecture doc excerpts if available
- Only explore specific service directories identified
- Check recent commits, existing patterns

## 7. Cross-service synthesis (team path only)

Lead synthesizes after all explorers report:
- Shared patterns across services
- API contracts between services
- Event schemas needing changes
- Conflicting patterns to resolve
- Shared database tables
- Migration ordering

## 8. Multi-perspective design

**Team path:** Spawn design agents (opus) as team members — one per perspective from `config.brainstorm.designer_perspectives` (default: `["simplicity", "scalability"]`):

For each perspective:
- If `config.brainstorm.perspective_docs` has a mapping for this perspective name, `Read` the mapped file and inject its content into the designer agent's prompt
- If no mapping exists, spawn with perspective name only (no doc injection — not an error)

Each produces a proposal via TaskUpdate. Lead synthesizes one recommendation.

**Simple path:** Propose 2-3 approaches with trade-offs. Lead with recommended option.

## 8a. Test plan generation (optional)

If the feature includes UI changes, ask: "Do you want to define browser test scenarios for this feature?"

- If no: skip — user can add test scenarios later or not at all
- For non-UI features: skip this step (browser tests don't apply)
- If yes: run the **test reconnaissance** phase before writing scenarios:

**Step 1 — Route discovery:**
Grep the codebase for route definitions relevant to the designed feature:
- React Router: `path=`, `Route`, `createBrowserRouter`
- Next.js: `app/` directory structure, `page.tsx` files
- Vue Router: `routes:`, `path:`
- Other frameworks: ask user for routing convention

Document discovered routes in `### App Context` section of the test plan.

**Step 2 — Authentication analysis:**
Search for auth patterns in the codebase:
- Login pages/components (grep for "login", "signin", "auth")
- Auth middleware/guards (session checks, JWT verification, protected routes)
- Test credentials (seed scripts, fixtures, `.env.example`, test helpers)
- Session mechanism (cookies, localStorage tokens, auth headers)

Ask user to confirm findings and provide test credentials if not found in code. Document in `### Authentication` section.

**Step 3 — Page structure recon (if app is running):**
Ask user: "Is the app running? I can take snapshots of key pages to understand the UI structure."
- If yes: use Chrome DevTools MCP to `navigate_page` + `take_snapshot` on each relevant route
  - Capture form fields (input names, labels, placeholders)
  - Capture navigation elements (links, buttons, menus)
  - Capture content areas (headings, lists, data displays)
  - Document element selectors/labels that test scenarios should target
- If no: derive UI structure from component code (read relevant component files)
  - Look for form field names, button text, heading content
  - Less reliable but still useful for writing scenarios

**Step 4 — Generate test scenarios:**
Using the reconnaissance findings, generate concrete scenarios with:
- Real URLs from route discovery (not placeholder paths)
- Real form field labels/names from page structure recon
- Real auth flow from authentication analysis
- Scenarios: happy path first, then key error cases, then edge cases
- Each scenario references actual elements discovered (e.g., "Fill the 'Email address' input" not "Fill email field")

**Step 5 — Prerequisites and setup:**
Document what's needed before `/project:test` can run:
- App start command (from package.json scripts, Makefile, docker-compose)
- Seed data requirements (from seed scripts or fixtures found)
- Environment variables needed (from `.env.example` or config files)

Write the complete `## Test Plan` section in the living state doc using the test plan template (see Design Templates below).

## 9. Contract verification (cross-service only, team path)

When 2+ services share an API boundary or event:
- **Producer check** — verify endpoint/event producer matches proposed contract
- **Consumer check** — verify consumer aligns
- **Event schema check** — verify topology, payloads

All report via TaskUpdate. Skip for single-service features.

## 10. Write design to living state document

- Create `{config.plans_dir}/YYYY-MM-DD-{slug}-design.md` using strict template
- Set status to `designing`
- Fill in Design section using templates below
- If config.plans_structure is `standard`: add entry to {config.plans_dir}/INDEX.md under "## Active"
  Format: `- [{Feature Name}]({filename}) — {one-line summary}`
  Example: `- [Orchestrator Fixes](2026-02-16-orchestrator-impl-fixes-design.md) — Improve agent completeness gates and task messaging`

  If INDEX.md doesn't exist, create it with this structure:
    # Plans Index

    ## Active
    - [{Feature Name}]({filename}) — {one-line summary}

    ## Completed

    ## Backlog

    ## Ideas

  If "## Active" section exists, add the entry at the top of that section (newest first).
- Present design to user

## 11. Cleanup brainstorm team

- **Team path:** `TeamDelete("brainstorm-{slug}")`
- Suggest user run `/clear` to free context
- Suggest user run `/project:implement` to start parallel implementation
- Suggest `/project:progress` anytime to check status

**Design phase ends here.** Implementation is handled by the `/project:implement` command.

---

**Implementation is handled by `/project:implement`. See that command for details.**

---

# Design Templates

### For API Features

```markdown
### Endpoint Design
- **Method + path:** GET/POST/etc /api/v1/...
- **Request payload:** (required/optional fields)
- **Response shape:** { field: type, ... }
- **Error cases:** 400/401/404/500 scenarios
- **Consumers:** Which services call this?

### Data Flow
[ASCII diagram showing service→service flow]
```

### For UI Features

```markdown
### Component Structure
- **Hierarchy:** Page → Container → Components
- **State management:** local vs context vs query cache
- **API dependencies:** Which endpoints?
- **Error/loading states:** How handled?
```

### Cross-Service Contract (when applicable)

```markdown
### Service Contracts
| Producer | Consumer | Contract | Notes |
|----------|----------|----------|-------|
| service-a POST /api/v1/... | service-b client.post(...) | { field: type } | ... |

### Event Pipelines
| Event | Exchange | Producer | Consumers | Payload |
|-------|----------|----------|-----------|---------|
| ... | ... | ... | ... | { ... } |

### Migration Order
1. Database migrations first
2. Producers next (API endpoints, event publishers)
3. Consumers last (frontend, admin, downstream services)
```

### For Backend Services

```markdown
### Backend Design
- **Feature flag:** Which config flag controls this?
- **Async pattern:** Virtual threads / reactive / message queue?
- **Caching:** What cache? TTL? Invalidation trigger?
- **Scheduler:** Needs periodic task? Interval?
- **Config:** Application config changes needed?
```

Check the target service's CLAUDE.md for stack-specific design patterns and conventions.

### For Browser Test Scenarios

```markdown
#### T{N} — {Scenario title}
**Precondition:** {Prior scenario state or "none — self-contained"}
**Setup:** {Navigation/login steps if self-contained}
**Steps:**
1. {Action — navigate, click, fill, etc.}
2. {Action}

**Expected:**
- {Visible element, text, URL, or state}
- {Another expected outcome}
```

---

# Checklists

## Cross-Service Checklist

- [ ] API contract changes documented?
- [ ] Event schema changes?
- [ ] Shared types need updating?
- [ ] Which service handles errors?
- [ ] Migration/deploy ordering defined?
- [ ] Auto-deploy services (from `config.services[].auto_deploy`) — coordinate PR merge order

## Common Pitfalls

> Check the project's CLAUDE.md and service-level CLAUDE.md files for project-specific pitfalls.

- Verify APIs exist before designing against them

## Parallel Task Design — Avoid File Collisions

When breaking work into implementation tasks, **check if multiple tasks will edit the same file.** Parallel agents editing one file causes race conditions.

| Situation | Strategy |
|-----------|----------|
| 2 tasks share a file | Sequence them (put in separate waves) |
| 3+ UI tasks share a page/component | **Component-first isolation:** each builds standalone hooks/components in new files, then one integration task wires them in |
| Deep multi-file overlap | Git worktrees (each agent gets its own working copy) |

**During design, annotate shared files in the task table:**
```markdown
| # | Task | Shared Files | Strategy |
|---|------|-------------|----------|
| 5 | Auto-populate UI | operations/index.tsx | isolation |
| 6 | Source picker | operations/index.tsx | isolation |
| 7 | Dry-run button | operations/index.tsx | isolation |
| 8 | Integration | operations/index.tsx | sequenced after 5-7 |
```

## Design Smells (pause if any apply)

| Smell | Question to Ask |
|-------|-----------------|
| >3 services affected | Can we reduce scope? |
| >5 team members | Too many — combine related services |
| New event exchange | Is existing exchange sufficient? |
| New shared type | Can we use existing DTOs? |
| New caching layer | Can existing cache patterns apply? |
| "We'll need to..." | Are we overengineering? |
| Multiple tasks edit same file | Use isolation or sequencing (see above) |

---

# Related Skills

| When | Action |
|------|--------|
| After implementation | Suggest user run `/project:changelog` |
| Implementation complete, verify work | Suggest user run `/project:verify` |
| Implementation complete, ready to merge | Suggest user run `/project:finish` |
| Implementer teammate needs guidance | Invoke `project-orchestrator:implementer` skill (agent-only) |
| Spec compliance review needed | Invoke `project-orchestrator:spec-reviewer` skill (agent-only) |
| Code quality review needed | Invoke `project-orchestrator:quality-reviewer` skill (agent-only) |

---

# Key Principles

- **Lazy exploration** — only explore what's needed, when scoped
- **One question at a time**
- **Service scope early** — know which services before exploring
- **YAGNI ruthlessly** — check design smells
- **Check service CLAUDE.md** — for stack-specific patterns and conventions
- **Cross-service awareness** — document contracts and event schemas
- **Living state on disk** — design doc in `{plans_dir}/` is source of truth, survives compaction
- **Max parallel implementers** — from `config.implementation.max_parallel` (default 3)
- **Fresh reviewers** — spec and quality reviewers are one-shot Task agents, not team members (compaction-safe)
- **Suggest /clear between phases** — brainstorm→implement is natural context boundary
- **Teams for breadth** — use teams for 3+ services or deep cross-cutting; simple agents otherwise
- **Always clean up teams** — `TeamDelete` after every team phase
- **Design doc is the handoff** — the living state doc is the artifact, not the team state
