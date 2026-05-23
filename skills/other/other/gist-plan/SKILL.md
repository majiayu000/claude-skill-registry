---
name: gist-plan
description: "GIST planning workflow. Structure goals into ideas, steps, and tasks using Gilad's evidence-guided framework."
metadata:
  instruction_budget: "32"
---

# GIST Planning

Replace opinion-based roadmaps with evidence-guided planning. Source: Gilad (Evidence Guided).

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

## Workflow

### 1. Set Goals (Quarterly)
- Derive from North Star input metrics or OKRs
- Format: "Improve [metric] from [current] to [target] by [date]"
- Maximum 3 goals per quarter
- Update .claude/canvas/gist.yml goals section

### 2. Generate Ideas (Ongoing)
- Ideas are hypothetical ways to achieve goals
- Most ideas fail (>80%) -- this is expected and planned for
- Generate many, hold loosely
- Store in .claude/canvas/gist.yml idea bank with ICE scores
- Never commit to an idea until evidence supports it

### 3. Score with ICE + Confidence Meter
Use `/mycelium:ice-score` to prioritize. ICE scoring (Ellis; confidence dimension added by Gilad):
- Confidence is NOT gut feel -- it maps to evidence levels
- 0.1 = opinion only | 0.5 = data supports | 0.7 = tested | 0.9 = launched
- Rescore after every experiment
> *Mycelium uses 0.0-1.0 (adapted from Gilad's 0-10 non-linear Confidence Meter). See `/mycelium:ice-score` for details.*

### 4. Design Steps (per top idea)
- Steps are small, time-boxed activities that build evidence
- Each step has: hypothesis, method, success criteria, **MoSCoW priority**
- Tag each step as **Must** / **Should** / **Could** / **Won't** (DSDM):
  - **Must**: Non-negotiable. Delivery fails without this. All REVIEW checks apply.
  - **Should**: Important. Ship if time allows. All REVIEW checks apply.
  - **Could**: Nice-to-have. Cut first when timebox runs out. NUDGE checks only.
  - **Won't**: Explicitly out of scope for this cycle. Documented for future reference.
- Steps follow a confidence ladder: assessment -> exploratory experiment -> feature experiment -> launch
- Each step produces evidence that increases or decreases confidence
- If evidence is negative: pivot or kill the idea (sunk cost is irrelevant)
- For user-facing ideas, frame hypotheses in Lean UX format: "We believe [outcome] for [users] if [change]." (Gothelf)
- **When a delivery timebox is exceeded**: Flex scope using MoSCoW — cut Could/Won't before compromising Must/Should

### 5. Execute Tasks (Sprint-level)
- Tasks belong to the CURRENT step only
- Don't plan tasks for future steps
- Standard agile execution

### 6. Reprioritize (Continuous)
After each step completes:
- Update ICE scores based on new evidence
- Re-rank ideas
- Kill ideas below threshold
- Surface new ideas from discovery work

### Shape Up: Appetite Over Estimates
Instead of asking "how long will this take?", ask "how much is this worth?" (Shape Up by Basecamp). Set an **appetite** — the maximum time you're willing to invest — then design the solution to fit within it. If the solution can't fit, narrow the scope, don't extend the timebox. This connects naturally to MoSCoW: appetite defines the timebox, MoSCoW decides what fits within it.

## Anti-Pattern: The Feature Roadmap
If your GIST board looks like a feature list with dates, you're doing it wrong. Goals are outcomes, ideas are hypotheses, steps are experiments.
