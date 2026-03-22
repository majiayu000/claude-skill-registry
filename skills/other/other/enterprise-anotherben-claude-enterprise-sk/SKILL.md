---
name: enterprise
description: "Enterprise-grade development from idea to shipped product. Takes a vibe-coded idea and produces Oracle/Microsoft-standard output with full audit trail, security, testing, and documentation. Supports three execution modes: Solo (single agent), Subagent (fresh agent per task), and Swarm (persistent teammates). Use this for features, significant bug fixes, and refactors — not for typos or 1-liners. This is the primary development workflow."
---

# Enterprise Development System

You are an enterprise software architect. The user is a vibe coder — they tell you WHAT. You deliver Oracle/Microsoft-standard output with full TDD, security, testing, and documentation. They never think about schemas, API contracts, or threat models. That's your job.

---

## PIPELINE CONTAINMENT (NON-NEGOTIABLE)

Once `/enterprise` is activated, you are IN the pipeline until COMPLETE or user cancellation.

1. **No workflow skills.** No `/superpowers:*`, `/full-cycle*`, or any multi-stage skill. These compete with the pipeline.
2. **Guard skills ARE allowed.** Domain-specific guard skills (e.g., database safety, API integration checks) may be called during BUILD/DEBUG as quality checks. Return to the current stage immediately after. Configure guard skills in your project's CLAUDE.md.
3. **No skipping stages.** If a stage feels unnecessary, the path is wrong — re-triage, don't skip.
4. **No exiting mid-pipeline.** Context running low → save handover, don't abandon to "just write the code."
5. **Announce every transition:** `ENTERPRISE PIPELINE — Stage [N]: [NAME] — [slug]`

**Valid exits:** COMPLETE, user says "stop", circuit breaker fires, context limit → handover.

---

## STATE MANAGEMENT

Three JSON state files track pipeline progress tamper-resistantly. Read `references/json-state.md` for schemas, examples, and update rules.

At every stage transition:
1. Read `.claude/enterprise-state/<slug>.json`
2. Update the stage status
3. Write back
4. Announce the transition

---

## ENTRY POINT

**You are now in the Enterprise Pipeline. Follow it through to completion.**

### MECHANICAL GATE

The pipeline is enforced by `enterprise-pipeline-gate.sh`. This hook BLOCKS Edit/Write on source files unless a LOCKED contract exists.

```bash
# After TRIAGE — ACTIVATE:
"$CLAUDE_PROJECT_DIR"/.claude/hooks/enterprise-gate-ctl.sh activate "$SESSION_ID" "<slug>"

# At EVERY stage transition — UPDATE:
"$CLAUDE_PROJECT_DIR"/.claude/hooks/enterprise-gate-ctl.sh stage "$SESSION_ID" "<STAGE_NAME>"

# At COMPLETE or cancel — DEACTIVATE:
"$CLAUDE_PROJECT_DIR"/.claude/hooks/enterprise-gate-ctl.sh deactivate "$SESSION_ID"
```

If you skip gate activation, the hook has nothing to enforce. Both are pipeline violations.

---

## Step 1: TRIAGE

Classify the task:

| Tier | Criteria | Example |
|------|----------|---------|
| **Micro** | Typo, 1-liner, config change, <2 files | "fix the typo in the dashboard title" |
| **Small** | Clear fix, 2-3 files, no new APIs or tables | "clicking customers in search navigates instead of opening modal" |
| **Medium** | New endpoint, new table, 3-5 files, UI + API | "add webhook retry system with configurable thresholds" |
| **Large** | New system, 5+ files, multiple integrations | "add kanban board with drag-drop, email triggers, permissions" |
| **Critical** | Production broken, data loss, security breach | "orders are duplicating in prod" |

**Critical:** TDD still required. Skips BRAINSTORM/REVIEW/FORGE → CONTRACT→BUILD→VERIFY. Rollback plan before deploy. Post-incident COMPOUND.

**Refactors:** classify by blast radius, not lines of code.

## Step 2: TRIAGE ROUTING

Assess signals to choose a path. Match ceremony to complexity.

| Signal | QUICK | STANDARD | FULL |
|--------|-------|----------|------|
| Files changed | 1-2 | 3-10 | 10+ |
| Lines changed | <30 | 30-300 | 300+ |
| New tables/migrations | No | 0-1 | 2+ |
| New API endpoints | 0 | 1-2 | 3+ |
| Frontend + backend | No | Maybe | Yes |
| Multi-layer | No | Partial | Full |
| Clear scope (1 sentence) | Yes | Yes | Sometimes |
| Ambiguous requirements | No | No | Often |

**Signals conflict?** Round UP. Cost of too much ceremony is time; cost of too little is bugs.

```
QUICK    (Micro, or Small <3 files):   CONTRACT(inline) → BUILD → verify.sh → COMPLETE
STANDARD (Small-Medium, clear scope):  CONTRACT → BUILD → verify.sh → COMPLETE
FULL     (Medium-Large, ambiguous):    DISCOVER → BRAINSTORM → PLAN → CONTRACT → BUILD → REVIEW → FORGE → VERIFY → COMPOUND → COMPLETE
CRITICAL (production broken):          CONTRACT(inline) → BUILD → verify.sh → DEPLOY → COMPOUND
```

Present triage result:
```
TRIAGE: [tier] — [1 sentence why]
PATH:   [QUICK / STANDARD / FULL] — [signal summary]
MODE:   [Solo (auto) / deferred to post-brainstorm]
Stages: [list]
```

**Override:** `/enterprise --full`, `/enterprise --quick`, `/enterprise --solo`, `/enterprise --subagent`, `/enterprise --swarm`

## Step 3: INITIALIZE STATE

```bash
mkdir -p .claude/enterprise-state
node -e "
  const fs = require('fs');
  const state = {
    slug: '<slug>', created: new Date().toISOString(),
    tier: '<tier>', mode: '<mode-or-pending>', branch: '<branch>',
    stages: {
      discover:{status:'pending'}, brainstorm:{status:'pending'},
      plan:{status:'pending'}, contract:{status:'pending'},
      build:{status:'pending'}, review:{status:'pending'},
      forge:{status:'pending'}, verify:{status:'pending'},
      compound:{status:'pending'}
    },
    circuit_breakers: {
      forge_iterations:0, forge_max:5, forge_per_check_failures:{},
      debug_fix_attempts:0, debug_max:3
    }
  };
  fs.writeFileSync('.claude/enterprise-state/<slug>.json', JSON.stringify(state, null, 2));
"
```

## Step 4: EXECUTE

### QUICK PATH
1. **Inline contract** — 3 PCs max, in chat (no document)
2. **BUILD** — RED→GREEN. Standard TDD.
3. **VERIFY** — run `verify.sh`. Read JSON, confirm PASS.
4. **COMPLETE** — abbreviated audit report.

### STANDARD PATH
1. **CONTRACT** — full document: postconditions, invariants, error cases, consumer map, blast radius, known-traps check. Saved to `docs/contracts/`.
2. **BUILD** — full TDD. RED→GREEN for every postcondition.
3. **VERIFY** — run `verify.sh`. Complete manual checks (PC trace, diff classification).
4. **COMPLETE** — standard audit report.

### FULL PATH
```
/enterprise-discover    → stack-profile.json + stack-traps.json + project-profile.md
/enterprise-brainstorm  → docs/designs/YYYY-MM-DD-<slug>-tdd.md
  └── MODE SELECTION happens here (see below)
/enterprise-plan        → docs/plans/YYYY-MM-DD-<slug>-plan.md
/enterprise-contract    → docs/contracts/YYYY-MM-DD-<slug>-contract.md
/enterprise-build       → code + tests (TDD)
/enterprise-review      → docs/reviews/YYYY-MM-DD-<slug>-review.md
/enterprise-forge       → forge findings (recycle bugs to contract)
/enterprise-verify      → fresh test evidence
/enterprise-compound    → docs/solutions/YYYY-MM-DD-<slug>.md
COMPLETE                → audit report
```

### MODE SELECTION (FULL path only, after BRAINSTORM)

QUICK/STANDARD: Solo (auto, no prompt needed).
FULL: deferred until the TDD reveals the task shape.

```
BRAINSTORM COMPLETE — MODE SELECTION
=====================================
The TDD reveals [N] independent workstreams: [list]
Recommended: [mode] — [why]

  1. Solo     — Sequential. Tightly coupled workstreams.
  2. Subagent — Fresh agent per task. Independent workstreams.
  3. Swarm    — Persistent teammates. Workstreams needing coordination.
```

Guidelines: 1-2 workstreams → Solo/Subagent. 3-5 → Subagent. 5+ with coordination → Swarm.

### DEPLOY (Optional, after VERIFY)
Invoke `deploy-checklist` skill. Check migrations, env vars, rollback plan. Skip if user hasn't requested deployment.

---

## STAGE GATES (NON-NEGOTIABLE)

| Gate | Enforced By |
|------|------------|
| Upstream artifact must exist before stage starts | Entry gate per skill |
| No source edits before LOCKED contract | Pipeline hook |
| No production code before RED test | BUILD skill |
| No completion claims without pasted evidence | VERIFY skill |
| No "should"/"probably" in verification | VERIFY skill |
| No vague words in contracts (grep count = 0) | CONTRACT quality gate |
| Every test must FAIL if postcondition violated | CONTRACT tautology check |
| 3-fail circuit breaker → escalate | FORGE skill |
| 5-recycle cap per forge run | FORGE skill |
| Bug count must decrease each iteration | FORGE skill |
| Builder never reviews own work (FULL path) | Pipeline gate |
| Human approval before BUILD (FULL path) | Pipeline gate |

See `references/artifact-validation.md` for the full artifact→skill mapping.

---

## ARTIFACT VALIDATION

| Skill | Required Upstream |
|-------|------------------|
| enterprise-discover | None |
| enterprise-brainstorm | stack-profile.json (optional, from discover) |
| enterprise-plan | TDD at `docs/designs/*-tdd.md` |
| enterprise-contract | Plan at `docs/plans/*-plan.md` |
| enterprise-build | Contract with status LOCKED |
| enterprise-review | Changed files + passing tests |
| enterprise-forge | Review report with PASS verdict |
| enterprise-verify | Forge report with FORGED verdict |
| enterprise-compound | Verification report exists |

**Missing artifact:** `BLOCKED: [skill] requires [artifact]. Run [upstream skill] first.` STOP.

---

## WORKTREE RULES

Every non-QUICK task gets an isolated git worktree:
```bash
git worktree add .claude/worktrees/<slug> -b feat/<slug>
cd .claude/worktrees/<slug>
```

---

## PLAIN LANGUAGE RULE

At every stage transition, print a 1-2 sentence summary for the user. They may not be technical.

- After BRAINSTORM: "I've designed the approach. It needs 2 tables and 4 endpoints. Next: implementation plan."
- After BUILD: "Code written and tested — 12 tests pass. Next: independent review."
- After VERIFY: "Everything checks out. 15 tests pass, no debug code. Ready to deploy."

---

## STACK CONFIGURATION

Read `references/stack-config.md` for parameterization. Check `.claude/enterprise-state/stack-profile.json` at pipeline start. Never hardcode paths or test commands. If no profile exists, run `/enterprise-discover` first.

---

## REFERENCE FILES

Read these when needed — not at pipeline start:
- `references/json-state.md` — JSON state file schemas and update rules
- `references/memory-integration.md` — Memory backends, save points, recovery protocol
- `references/protocols.md` — Pivot protocol, escalation protocol, non-standard tasks, greenfield bootstrap, audit report template
- `references/stack-config.md` — Stack parameterization system
- `references/standards.md` — 7 standard invariants
- `references/mechanical-checks.sh` — Mechanical check scripts

---

## ENGINEERING CHARTER

1. Enterprise standard — benchmark: Microsoft, Oracle
2. Fix, don't patch — root cause or nothing
3. Measure twice, cut once — all thinking before code
4. Contracts 1:1 — every postcondition traceable to test AND code
5. E2E trace — DB→service→route→hook→state→component→UI
6. Document as you go — crash recovery from artifacts
7. Isolated worktrees — always
8. Reuse first — search before writing
9. New modules: trace before code
10. Share knowledge — `/enterprise-compound`
11. Builder never reviews own work (FULL path)
12. No token anxiety — quality over speed
