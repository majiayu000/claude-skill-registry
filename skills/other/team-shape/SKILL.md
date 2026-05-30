---
name: team-shape
description: "Assess team structure against Skelton's Team Topologies. Evaluate cognitive load, interaction modes, and Conway's Law alignment."
metadata:
  instruction_budget: "26"
  framework_dependency: "mycelium"
  framework_dependency_note: "This skill is designed to run within the Mycelium framework (https://github.com/haabe/mycelium). Standalone use will skip the canvas state, theory gates, and harness behavior the skill assumes. Install: /plugin install mycelium@haabe/mycelium."
---

# Team Shape Assessment

Evaluate organizational design for fast flow. Source: Skelton & Pais (Team Topologies).

## Preflight: Read target canvas file(s) before any Write/Edit

**Hard rule.** Before issuing `Write` or `Edit` against any `.claude/canvas/*.yml`, use the **Read tool** on that file in this session. Claude Code's Read-before-Write check requires the `Read` tool specifically — `cat`/`head`/`grep` via Bash do NOT satisfy it.

**Edit vs Write — different cost profiles** (verified 2026-05-14):
- **`Edit`** (exact-string replacement): `Read` with `limit: 1` satisfies the check at ~50 tokens. State-tracking is per-file, not per-byte — subsequent `Edit` calls work anywhere in the file. Use this for partial updates against large canvas files (e.g., `purpose.yml` at 800+ lines).
- **`Write`** (full replacement): do a **full Read** first. Write obliterates the file; you should see what you're about to replace. The `limit:1` shortcut is *not* appropriate here.

**ID-bearing entries — scan the ID space before assigning** (added 2026-05-15, v0.23.19): When adding a new component, opportunity, solution, or any other ID-bearing entry to a canvas file, run a Bash grep first to confirm the next ID in your prefix sequence is actually free:

```
grep "^  - id: <prefix>-" .claude/canvas/<file>.yml | sort -u
```

Replace `<prefix>` with the canvas's ID prefix (`comp` for landscape, `opp` for opportunities, `sol` for solutions, `ht` for human-tasks, etc.). Then pick the next free integer. `validate_canvas.py` has a duplicate-ID check (lines 230-239) that catches the failure on CI, but a duplicate can persist in the working tree for days if CI isn't run between edit and discovery — see roadmap-repo `corrections.md` 2026-05-15 "Duplicate canvas ID created in landscape.yml" for the worked example.

Original failure mode: anti-pattern #7 instance #5, 2026-05-09 — agent conflated Bash `head` with the Read tool, lost ~14k tokens to a Write-fail → remedial-full-Read → re-Write loop. The `limit:1` discipline (graduated 2026-05-14, v0.23.18) prevents the second-order cost where the agent *correctly* follows the rule but full-Reads every time. The ID-scan discipline (graduated 2026-05-15, v0.23.19) prevents the related class where the agent reads enough of the file to satisfy the Edit check but not enough to see existing ID assignments — kin to anti-pattern #8 (Stale State Read).

If this skill writes to multiple canvas files, register each one first (limit:1 for Edit-only paths; full Read for Write paths) AND ID-scan any prefix you intend to assign.

See `CLAUDE.md` *Canvas writes — Read before Write* for the canonical rule.

## Assessment Workflow

### 1. Map Current Teams
For each team, classify:
- **Stream-aligned**: Owns a user journey or business domain (most teams should be this)
- **Enabling**: Helps other teams acquire capabilities (temporary engagement)
- **Complicated subsystem**: Deep specialist knowledge (only when cognitive load justifies)
- **Platform**: Internal product that reduces cognitive load for stream-aligned teams

### 2. Evaluate Cognitive Load
For each team, assess:
- **Intrinsic load**: Problem complexity (can't reduce, only manage)
- **Extraneous load**: Bad tools/processes (SHOULD reduce -- platform teams help here)
- **Germane load**: Learning new relevant things (encourage)
- If team is overloaded: shrink domain, move complexity to platform, or split

### 3. Audit Interaction Modes
Between each pair of collaborating teams:
- **Collaboration**: Working closely together (time-box this -- it's expensive)
- **X-as-a-Service**: Consuming/providing via API (ideal steady state)
- **Facilitating**: Helping another team learn (enabling teams do this)

### 4. Conway's Law Check

Conway's Law (1968): "Any organization that designs a system (defined broadly) will produce a design whose structure is a copy of the organization's **communication** structure." Note: it's communication structures, not org chart hierarchy — two teams in the same org with poor communication will still produce fragmented systems.

**Inverse Conway Maneuver** (James Lewis, popularized by Skelton & Pais): Deliberately design team communication structures to match the desired system architecture, rather than letting architecture drift to match existing teams.

- Does architecture mirror team structure intentionally?
- Do team boundaries align with security boundaries?
- Do team APIs match system APIs?
- If architecture doesn't match team structure: is the mismatch intentional or a Conway's Law drift?

### 4b. Fracture Planes (Skelton & Pais)

When a team's cognitive load exceeds capacity, use fracture planes to identify the cleanest split point. The fracture plane that aligns with the most criteria wins:

| Fracture Plane | Description |
|---|---|
| Business domain | DDD bounded context boundary |
| Regulatory compliance | Different compliance requirements = different teams |
| Change cadence | Fast-moving vs stable components |
| Team location | Co-located vs distributed |
| Technology | Different tech stacks |
| User personas | Different user segments |
| Risk | High-risk vs low-risk components |
| Performance isolation | Components with different scaling/latency requirements |

*Source: Skelton & Pais (Team Topologies, Chapter 6)*

### 5. Recommendations
- Teams without clear type -> needs redesign
- Collaboration lasting > 1 quarter -> should evolve to X-as-a-Service
- Stream-aligned team with > 2 cross-team dependencies -> architecture needs decoupling
- Cognitive load exceeding capacity -> use fracture planes to identify split point

### 5. Bounded Context Alignment (DDD)
If the product has multiple domains or services:
- Are bounded contexts identified? (Check .claude/canvas/bounded-contexts.yml)
- Does each stream-aligned team own a coherent bounded context?
- If a context is split across teams: handoff friction. Fix team boundaries.
- If a team owns unrelated contexts: cognitive overload. Split the team or contexts.
- Context map relationships should match team interaction modes:
  Partnership = Collaboration, Customer-Supplier = X-as-a-Service, ACL = translation layer
*Source: Evans (DDD), "Architecture for Flow" (DDD + Wardley + Team Topologies)*

### 6. Capability Gap Diagnosis (DASA)
When DORA metrics indicate capability gaps, use the DASA DevOps Competency Framework's 12 skill areas to identify which team skills need development (e.g., courage, teambuilding, continuous improvement, business value optimization).

## Bounded Agency (Skelton, 2025-2026)

Skelton's "Infrastructure for Agency" framing describes how organizations should provide **boundaries that enable autonomy** rather than control that restricts it. Mycelium implements bounded agency for AI agents using the same structural principles:

| Skelton concept | Mycelium mechanism |
|---|---|
| Boundaries that enable | Guardrails (BLOCK/REVIEW/NUDGE — constrain without micromanaging) |
| Shared state | Canvas (single source of truth all agents read/write) |
| Stable interfaces | Theory gates (predictable checkpoints with explicit pass/fail) |
| Aligned domains | Diamonds (scoped units of work with clear ownership) |
| Bounded workers | Fan-out agents (isolated worktrees, scoped mandate, report back) |

Agency without boundaries produces chaos; boundaries without agency produces bureaucracy. The target is the middle.

*Source: Skelton (Infrastructure for Agency, 2025-2026)*

## Output

- Update `.claude/canvas/team-shape.yml` and `.claude/canvas/bounded-contexts.yml` with assessment results.
- **APPEND** a `### Team Shape Assessment` entry to `.claude/harness/decision-log.md` with: team types identified, cognitive load findings, Conway alignment, recommendations. (MANDATORY per G-P4)
