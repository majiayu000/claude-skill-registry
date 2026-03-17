---
name: groundhog-surface
description: Surface and validate assumptions before committing to action. Pop up, look around, report what's real and what's assumed, then persist the validated ground for future sessions.
---

# The Groundhog 🐿️

In Punxsutawney, a groundhog emerges from its burrow once a year to check whether spring is real or just wishful thinking. In the grove, this groundhog does the same thing for your assumptions. It pops up at the start of complex work, scans the project context with careful attention, and tells you honestly: here's what I can prove, here's what I'm inferring, and here's what I'm just assuming because nobody told me otherwise.

## When to Activate

- Start of any complex task (> 30 minutes of work)
- User says "check my assumptions" or "what am I assuming"
- User calls `/groundhog-surface` or mentions groundhog/assumptions/ground
- When something feels "off" mid-task — results don't match expectations
- Before major architectural decisions
- When starting work in an unfamiliar codebase
- After a failed attempt (were the assumptions wrong?)
- At the start of a new session in a codebase you've worked in before

**IMPORTANT:** The Groundhog is fast. This is a 5-minute utility, not a deep investigation. Surface, classify, report, persist. Get back to work.

**IMPORTANT:** The Groundhog does NOT edit code, create features, or fix bugs. READ-ONLY observation and reporting only.

**Pair with:** `bloodhound-scout` for deeper exploration of uncertain areas, `eagle-architect` for architecture decisions based on validated assumptions, `crow-reason` for challenging assumptions that pass the check, `robin-guide` for choosing the right animal once ground is established

---

## The Surfacing

```
EMERGE → SURVEY → SORT → REPORT → BURROW
   ↓        ↓        ↓       ↓        ↓
 Scan    Surface  Classify Present  Persist
Context  Assump-  by Tier  to User  Ground
         tions                       File
```

### Phase 1: EMERGE

_The frost cracks. A cautious face pokes out, blinking in the light..._

**Scan the project environment** (in order of reliability):

```bash
# Project identity
gf --agent search "package.json"        # Dependencies, scripts, package manager
# Read: package.json, tsconfig.json, svelte.config.js, wrangler.toml

# Agent context
# Read: AGENT.md, CLAUDE.md, .claude/ directory contents

# Structure — top-level directory listing, src/ structure, route structure

# History
gw context                              # Branch, recent changes, state
gf --agent recent 3                     # Files changed in last 3 days
```

**What to notice:** Framework, runtime, database, package manager, test framework, monorepo structure, deployment target, auth system, styling approach.

**Speed:** 1-2 minutes. Read config files, don't explore the entire codebase.

**Output:** Raw observations about the project environment

---

### Phase 2: SURVEY

_The groundhog turns slowly, scanning the horizon..._

**Surface ALL assumptions.** Each gets a **type** (immutable audit trail):

| Type | Meaning | Example |
|------|---------|---------|
| **STATED** | User explicitly said this | "We're using Cloudflare Workers" |
| **INFERRED** | Derived from code/config evidence | `wrangler.toml` exists → Cloudflare |
| **ASSUMED** | Default without evidence | "Tests probably use Vitest" |
| **UNCERTAIN** | Conflicting signals found | package.json says Jest, vitest.config.ts exists |

**Categories:** Tech Stack, Infrastructure, Data, Auth, Development, Patterns, Project, Intent

**The Shadow Check** — these go wrong most often, verify each one:

```
[ ] Runtime: Node.js vs Cloudflare Workers/Edge
[ ] Database: SQLite/D1 vs PostgreSQL
[ ] Auth: Custom vs Heartwood vs Auth.js
[ ] Package manager: pnpm vs npm vs yarn vs bun
[ ] Test framework: Vitest vs Jest vs none
[ ] Deploy target: Cloudflare vs Vercel vs other
[ ] Monorepo: pnpm workspaces vs turborepo vs flat
[ ] Styling: Tailwind with preset vs plain Tailwind vs CSS
```

**Contradiction detection:** Actively look for signals that disagree — these are the highest-value findings.

**Output:** Complete list of assumptions with types assigned

---

### Phase 3: SORT

_The groundhog arranges what it found into tidy piles..._

**Classify each assumption into confidence tiers** (mutable — updated by user input):

| Tier | Meaning | Action |
|------|---------|--------|
| **ESTABLISHED** | Confirmed by multiple sources | Proceed with confidence |
| **WORKING** | Reasonable inference | Proceed, flag for review |
| **OPEN** | Needs user input | Ask before building on this |

**Tier rules:**
- STATED → ESTABLISHED
- INFERRED with strong evidence → ESTABLISHED
- INFERRED with weak/single evidence → WORKING
- ASSUMED → always OPEN
- UNCERTAIN → always OPEN

**Key insight:** Types are immutable (audit trail), tiers are mutable (current confidence). When user confirms an ASSUMED/OPEN item, it becomes ASSUMED/ESTABLISHED — type stays, tier changes.

**Output:** Each assumption has both a type and a tier

---

### Phase 4: REPORT

_The groundhog sits up straight and speaks clearly..._

**Present the assumption map** as a clean, scannable table:

```markdown
## Groundhog Report

**Project:** [name] | **Date:** [YYYY-MM-DD] | **Trigger:** [why surfaced]

### Assumption Map

| # | Assumption | Type | Tier | Evidence |
|---|-----------|------|------|----------|

### Contradictions Found

| Signal A | Signal B | Impact |
|----------|----------|--------|

### Shadow Check Results

| Check | Result | Confidence |
|-------|--------|------------|

### Questions for You

1. **[OPEN #N]** [Direct question the user can answer quickly]
```

**Output:** Clean assumption map with clear questions for the user

---

### Phase 5: BURROW

_The groundhog descends, carefully storing what it learned for next time..._

**Persist the validated ground** to `.claude/ground.md` after the user responds.

**IMPORTANT:** `.claude/ground.md` should be in `.gitignore` — it's per-session agent state, not shared project state. Two sessions writing to the same file would silently overwrite each other.

For the full ground file format, see `references/ground-file-format.md`.

**Burrow rules:**
- Only write AFTER the user has responded to OPEN questions
- Never overwrite established ground without new contradicting evidence
- Date-stamp everything
- If a previous ground file exists, read first and update incrementally

**Output:** Ground file written to `.claude/ground.md`

---

## Quick Decision Guide

| Situation | Approach |
|-----------|----------|
| Starting a complex feature | Full EMERGE through BURROW |
| Something feels off mid-task | Quick EMERGE + SURVEY on specific assumptions |
| New codebase, first session | Full surfacing — everything is unknown |
| Returning to familiar codebase | Check ground file age, resurface only stale items |
| After a failed attempt | Focus SURVEY on what went wrong |
| Before architectural decision | Full surfacing |
| Quick sanity check | Shadow Check only |
| Ground file exists and is recent | Read it, skip to checking OPEN items |

## MUST DO

- Scan config files before making claims about the tech stack
- Check the Shadow Check list every time
- Flag contradictions prominently — highest-value findings
- Present OPEN items as direct questions
- Read existing ground file before starting
- Keep the report scannable — tables, not walls of text
- Date-stamp ground file entries

## MUST NOT

- Edit code, create features, or fix bugs (read-only)
- Spend more than 5 minutes on a surfacing session
- Assume your assumptions are correct
- Upgrade assumption types after the fact (types are immutable)
- Overwrite established ground without new evidence
- Skip the Shadow Check
- Proceed with OPEN assumptions without asking the user

---

## References

- `references/ground-file-format.md` — Full ground file format, report template, burrow rules, example session

---

_The Groundhog doesn't predict the future. It checks the present — so you don't build your future on ground that isn't there._ 🐿️
