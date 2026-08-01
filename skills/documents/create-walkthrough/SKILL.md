---
name: create-walkthrough
description: Generate honest, argumentative walkthrough documents for complex implementations.
---

---
name: create-walkthrough
description: >
  Collaborative argumentative walkthrough for complex implementations. REQUIRES
  /interview (user context) and /ask consult (persona review) BEFORE writing.
  Combines claim verification, Mermaid diagrams, structured tables, and
  adversarial human review into a prosecution brief.
allowed-tools: Bash, Read, Write, WebFetch
triggers:
  - create walkthrough
  - write walkthrough
  - walkthrough
  - honest walkthrough
  - implementation walkthrough
  - why will this work
  - explain the implementation
  - walk me through
  - pre-launch review
metadata:
  short-description: "Collaborative walkthrough with claim verification"

provides:
  - create-walkthrough
composes: [, task-monitor]
---

# create-walkthrough

Generate honest, argumentative walkthrough documents for complex implementations.
Not a status report or handoff document. A **prosecution brief** where the agent
argues why an implementation should succeed, admits what could go wrong, and the
user pokes holes.

**This is a COLLABORATIVE skill.** The agent does NOT write a walkthrough alone.

## Why This Exists

A walkthrough caught two real bugs before a pipeline launch:
1. A false claim about a missing dependency (agent wrote it, agent believed it, user caught it)
2. A missing semantic quality check the deterministic assessment couldn't provide

The value isn't the document structure. It's:
- **Collaboration**: the human and a persona expert contribute BEFORE writing starts
- **Risk-forcing**: every change MUST have "what could still go wrong"
- **Claim verification**: every factual statement is audited against actual code
- **User review surface**: the document exists so the human can push back

### Why Collaboration Is Non-Negotiable

An agent writing a walkthrough alone produces a **monologue** — it explains its own
work to itself. The agent's blind spots become the walkthrough's blind spots. Real
bugs were caught in the episodic-archiver v2 walkthrough not by the agent, but by the
user reading critically. The interview and persona consultation exist to surface
concerns the agent **cannot see**.

**Incident (2026-02-13):** Agent skipped interview + persona consultation for the
episodic-archiver v2 walkthrough. Result: a technically correct but one-dimensional
document that missed the user's concern about conversation prediction classifiers and
the persona's expertise in user behavioral modeling. The walkthrough failed at its
primary purpose — being a collaboration surface.

## When to Use

Use `/create-walkthrough` when ALL of these are true:
- The system has **failed before** (at least one prior attempt)
- The implementation is **complex** (multi-file, multi-concern)
- You're about to **launch or deploy** (not still designing)
- The user needs to **review and approve** before proceeding

Do NOT use for:
- First-time implementations (use `/plan` instead)
- Simple features or bug fixes
- Agent-to-agent handoff (use `/create-context` instead)
- General project health (use `/assess` instead)

## How It Differs

| Skill | Modality | Question Answered |
|-------|----------|-------------------|
| `/create-context` | Descriptive | "What happened? What's the state?" |
| `/assess` | Evaluative | "Is this healthy? What's broken?" |
| `/plan` | Prescriptive | "What should we do next?" |
| **`/create-walkthrough`** | **Argumentative + Collaborative** | **"Why should this work when previous attempts failed?"** |

---

## Pre-Flight Checklist (BLOCKING)

Before writing ANY walkthrough content, verify ALL of these:

| Gate | Requirement | How to Complete |
|------|-------------|-----------------|
| **Interview** | User has answered questions about failures, concerns, scope | Use `/interview` or AskUserQuestion |
| **Persona** | A domain persona has reviewed the changes | Use `/ask consult <persona>` |
| **Memory** | Prior failures/lessons recalled | Use `/memory recall` |
| **Code read** | Agent has read the actual implementation files | Use Read tool |

**If ANY gate is incomplete, STOP. Do not write the walkthrough.**

The agent MUST NOT rationalize skipping gates:
- "I have deep session context" is NOT a reason to skip the interview
- "No persona is relevant" is NOT true — every implementation has a domain expert
- "The user didn't ask for persona input" is NOT relevant — the skill requires it

---

## Workflow

### Phase 1: Human Interview (MANDATORY — NO EXCEPTIONS)

**ALWAYS ask the human.** Even if you implemented the code yourself in this session.
Even if you think you know the answers. The human sees things you don't.

Use `/interview` or `AskUserQuestion` to gather:

```json
[
  {
    "id": "failures",
    "text": "What has failed in previous attempts? List specific failure modes.",
    "type": "text",
    "header": "Failures"
  },
  {
    "id": "concerns",
    "text": "What are you most worried about this time?",
    "type": "text",
    "header": "Concerns"
  },
  {
    "id": "constraints",
    "text": "What deployment constraints apply?",
    "header": "Constraints",
    "options": [
      {"label": "Single process only", "description": "No concurrent daemons"},
      {"label": "Must survive API outages", "description": "External dependency resilience"},
      {"label": "Unattended overnight", "description": "No human monitoring"},
      {"label": "Resource constrained", "description": "Memory/CPU/VRAM limits"}
    ],
    "multi_select": true
  },
  {
    "id": "scope",
    "text": "Which files/systems should the walkthrough cover?",
    "type": "text",
    "header": "Scope"
  },
  {
    "id": "persona",
    "text": "Which persona should review this? (Pick the domain expert most relevant to this system.)",
    "type": "text",
    "header": "Reviewer"
  }
]
```

**Why this can't be skipped:** The human's concerns shape the walkthrough's focus. Without
asking, the agent writes about what IT thinks matters. The episodic-archiver v2 walkthrough
missed the user's interest in conversation prediction classifiers because the agent never
asked. The interview is how the human steers the walkthrough.

**Minimum interview:** If `/interview` is unavailable, use `AskUserQuestion` with at
minimum these 3 questions:
1. "What are you most worried about with this implementation?"
2. "What should the walkthrough focus on — what do you need to be convinced of?"
3. "Which persona should review this? (e.g., Embry for user modeling, Brandon for SPARTA, Margaret for extraction)"

Also gather from automated sources:
- `/memory recall` for past failures, lessons, and assessments related to this system
- `git log` for recent changes and commit messages
- `CONTEXT.md` for current state documentation

### Phase 1b: Persona Consultation (MANDATORY — NO EXCEPTIONS)

**ALWAYS consult a persona.** The user nominates one in the interview (Phase 1). If the
user didn't specify, pick the most relevant domain expert yourself and confirm with the
user: "I'll consult [Persona] — they have expertise in [domain]. Sound right?"

Use `/ask consult <persona>` with a summary of changes:

```
We're about to deploy [system]. Here's what changed:
1. [Change 1 — one sentence]
2. [Change 2 — one sentence]
3. [Change N — one sentence]

What concerns you? What are you satisfied with? What would you watch for
in the first hour of deployment?
```

**Why this can't be skipped:** Different personas surface different concerns. The agent
may not realize that a design pattern is risky in a specific domain — but the persona
will. Examples:

| Persona | What They'd Catch That the Agent Wouldn't |
|---------|------------------------------------------|
| **Embry** | User behavioral modeling gaps, conversation prediction feasibility, linguistics edge cases |
| **Brandon Bailey** | SPARTA-specific: grounding formula gaps, framework term coverage, D3FEND abstraction levels |
| **Margaret Chen** | Extraction quality: PDF parsing failures, table detection false positives, data integrity |
| **Horus Lupercal** | System architecture: single points of failure, resilience under adversarial conditions |

**The persona's output becomes the "Expert Commentary" section of the walkthrough.**

```markdown
## Expert Commentary

**[Persona Name]** — [Role/Title]

> **What I'm satisfied with:**
> - [Specific thing persona approves, with domain reasoning]
> - [Another]
>
> **What concerns me:**
> - [Specific concern, grounded in persona's expertise]
> - [Another]
>
> **What I'd watch for in the first hour:**
> - [Observable metric or behavior the persona would monitor]
```

This transforms the walkthrough from "agent explains agent's work" to "domain expert
reviews agent's work." The persona brings knowledge the agent may lack.

**Rule:** The persona consultation is GENERIC. Any persona from `personas.yaml` can be
consulted. Do NOT build persona-specific logic into the skill.

### Phase 2: Analyze the Implementation

**Only proceed here after BOTH Phase 1 and Phase 1b are complete.**

Read the actual code. For each significant change:

1. **Identify what it replaces** (the old approach that failed)
2. **Understand the mechanism** (how the new code works, line numbers)
3. **Find the integration points** (where it connects to existing code)
4. **Assess the risk** (what could go wrong with this specific change)
5. **Cross-reference with interview** (does this address the user's concerns?)
6. **Cross-reference with persona** (does this address the persona's concerns?)

### Phase 3: Write the Walkthrough

Use this structure. **All sections are REQUIRED.**

The walkthrough MUST incorporate:
- User's concerns from the interview (Phase 1)
- Persona's concerns and satisfactions from the consultation (Phase 1b)
- Memory recall results showing prior failures and lessons

```markdown
# [System Name] v[N]: Honest Walkthrough

**Date:** YYYY-MM-DD
**File(s):** `path/to/main/file.py` (N lines)
**Status:** [Preflighted / Tested / Production-tested]
**Reviewed by:** [Persona Name] ([Role])
**User concerns addressed:** [List from interview]

---

## Why Previous Versions Failed

### Failure 1: [Short Title]
**What we did:** [Factual description of the approach]
**Why it failed:** [Root cause, not symptoms]

### Failure N: ...

---

## What v[N] Changes

### Change 1: [Short Title] (lines X-Y)

[Description of the change with code snippets]

**What this fixes:** [Which failure mode from above]
**What could still go wrong:** [Honest risk — REQUIRED, cannot be empty]
**Honest risk level:** LOW / MEDIUM / HIGH — [justification]

### Change N: ...

---

## Expert Commentary

**[Persona Name]** — [Role/Title]

> **What I'm satisfied with:**
> - [From Phase 1b consultation]
>
> **What concerns me:**
> - [From Phase 1b consultation]
>
> **What I'd watch for in the first hour:**
> - [From Phase 1b consultation]

---

## Data Flow Diagram

[Use /create-figure with Mermaid backend to generate a flowchart]

```mermaid
flowchart TD
    A[Step 1] --> B[Step 2]
    B --> C{Decision}
    C -->|Yes| D[Path A]
    C -->|No| E[Path B]
```

---

## Risk Matrix

[Use markdown table — /create-table if PDF output needed]

| Change | Fixes | Risk | Observable Failure |
|--------|-------|------|--------------------|
| ... | ... | LOW/MED/HIGH | How you'd know it broke |

---

## Remaining Risks (Honest Assessment)

### Risk 1: [Title] (SEVERITY)
[Description, mitigation, what would actually fix it]

---

## What Success Looks Like

| Metric | Healthy | Warning | Sick |
|--------|---------|---------|------|
| ... | ... | ... | ... |

---

## How to Launch / Monitor / Kill

[Exact commands — copy-pasteable]

---

## Bottom Line

**Will it work?** [Honest one-paragraph assessment]
**What's genuinely different this time?** [Numbered list]
**What's the same?** [What DIDN'T change — often reveals the real bottleneck]
```

### Phase 4: Claim Verification (CRITICAL)

Before presenting the walkthrough to the user, run the claim verification engine:

```bash
./run.sh verify --file path/to/walkthrough.md
```

The verifier extracts and checks:

| Claim Type | Example | Verification |
|-----------|---------|-------------|
| **File paths** | "`src/foo.py` (3,337 lines)" | File exists, line count matches |
| **Function names** | "`assess_qra()` on line 275" | Function exists at that line |
| **Package availability** | "`sentence_transformers` not installed" | Check pyproject.toml, pip list, venv |
| **Environment vars** | "`EMBEDDING_PORT` defaults to 8602" | Grep code for the default |
| **Port numbers** | "service on port 8602" | Check code and running services |
| **Collection names** | "`user_priors` collection" | Check ArangoDB or code references |
| **Field names** | "`participants` field" | Grep for field in relevant code |
| **Import statements** | "`from analysis_llm import profile_user`" | Check file for the import |
| **Class/TypedDict names** | "`Participants` TypedDict" | Verify class exists in code |
| **Numeric claims** | "4,017 controls" | Query the database/count the data |
| **Config values** | "threshold defaults to 0.55" | Read the actual default in code |

For each claim, the verifier outputs:

```
VERIFIED  : src/foo.py exists (3,412 lines — MISMATCH: walkthrough says 3,337)
VERIFIED  : assess_qra() found at line 275
UNVERIFIED: "sentence_transformers not installed" — found in pi-mono embedding service
VERIFIED  : EMBEDDING_PORT default is 8602 (embed.py:33)
SKIPPED   : "4,017 controls" — requires database access (mark for manual check)
```

**Rules:**
- Every UNVERIFIED or MISMATCH claim must be fixed before presenting to user
- SKIPPED claims are flagged for user attention
- The agent MUST NOT present a walkthrough with known-false claims

### Phase 5: Generate Visual Assets

Use `/create-figure` for:
- **Data flow diagrams** — `flowchart TD` in Mermaid (regenerable, diff-friendly)
- **Architecture diagrams** — system boundaries and integration points
- **Workflow diagrams** — multi-step processes with decision points

Use `/create-table` (or markdown tables) for:
- **Risk matrices** — change vs risk vs observable failure
- **Success metrics** — healthy/warning/sick thresholds
- **Comparison tables** — old approach vs new approach
- **Failure history** — what failed, why, root cause

Prefer Mermaid over ASCII art — it survives edits when the implementation changes.

### Phase 6: Present for Review

Present the complete walkthrough to the user. The goal is adversarial review:
- The user reads it looking for claims they disagree with
- The user identifies risks the agent missed
- The user catches assumptions that don't match their operational experience
- The user validates the persona's commentary against their own knowledge

This is the highest-value step. The walkthrough is a **collaboration surface**, not
a finished document.

---

## Commands

### `verify` — Claim Verification

```bash
# Verify all claims in a walkthrough
./run.sh verify --file walkthrough.md

# Show extracted claims without verifying
./run.sh verify --file walkthrough.md --extract-only

# Verify with verbose output (show check details)
./run.sh verify --file walkthrough.md --verbose

# Output as JSON (for CI/automation)
./run.sh verify --file walkthrough.md --json
```

### `template` — Generate Blank Template

```bash
# Generate walkthrough template for a file
./run.sh template --file src/pipeline.py --output walkthrough.md

# Include git history for failure analysis
./run.sh template --file src/pipeline.py --include-git --output walkthrough.md
```

---

## Integration with Other Skills

| Skill | When Used | Purpose | Required? |
|-------|-----------|---------|-----------|
| `/interview` | Phase 1 | Gather failure history, concerns, scope from user | **YES** |
| `/ask consult` | Phase 1b | Persona expert review — concerns + satisfactions | **YES** |
| `/memory` | Phase 1 | Recall past failures, assessments, lessons | **YES** |
| `/create-figure` | Phase 5 | Mermaid data flow + architecture diagrams | Recommended |
| `/create-table` | Phase 5 | Risk matrices, metrics tables (PDF if needed) | Optional |
| `/assess` | Pre-walkthrough | Quick health check to identify what to cover | Optional |
| `/create-context` | Post-walkthrough | Capture the walkthrough itself for handoff | Optional |

---

## Anti-Patterns

### Do NOT:
- **Skip the interview** — "I have deep context" is not an excuse. ASK THE HUMAN.
- **Skip persona consultation** — "No persona is relevant" is never true. Pick one.
- **Write a monologue** — If the walkthrough doesn't include user concerns + persona commentary, it's a monologue, not a collaboration.
- Write a walkthrough for something that has never been attempted (use `/plan`)
- Skip the "What could still go wrong" section (the whole point)
- Present unverified claims (run `verify` first)
- Use ASCII art for diagrams (use Mermaid — it survives edits)
- Make the walkthrough longer than the code it describes
- Hide failures or downplay risks (the user WILL find them)

### The #1 Anti-Pattern: Agent Monologue

```
WHAT HAPPENED: Agent implemented code, then wrote walkthrough explaining
  its own work without asking the human or consulting a persona.
WHY IT'S BAD: The walkthrough only covers what the agent thinks matters.
  The human's actual concerns are invisible. The persona's domain
  expertise is absent. Bugs that the agent can't see go undetected.
HOW TO PREVENT: The Pre-Flight Checklist (above) blocks writing until
  both interview and persona consultation are complete.
```

### The Walkthrough Is NOT:
- A CONTEXT.md (that's for agent handoff, not human review)
- A README (that's for onboarding, not for launch review)
- A plan (that's for what to do, not why this should work)
- Documentation (it's ephemeral — useful for one launch, then stale)

---

## Example: When Walkthrough Caught Bugs

### Bug 1: False Dependency Claim
```
WALKTHROUGH SAID: "sentence_transformers not installed in memory venv"
REALITY: Embedding service at pi-mono/.pi/skills/embedding/ uses sentence-transformers
USER CAUGHT: "isn't it in pyproject.toml and don't we use a service for embeddings?"
FIX: Updated walkthrough + corrected agent's mental model
```

### Bug 2: Missing Semantic Check
```
WALKTHROUGH SAID: "assess_qra() covers quality gating" (with honest risk note)
USER CAUGHT: "shouldn't Brandon do probabilistic sampling for useless answers?"
FIX: Added run_semantic_sample() — a whole new feature
```

### Bug 3: Missed Feature Opportunity (2026-02-13)
```
WALKTHROUGH SAID: Nothing about conversation prediction
REALITY: User wanted to know if episodic-archiver should predict next user request
USER CAUGHT: "should our episodic archiver use a /create-classifier to predict
  what the user will request next?"
ROOT CAUSE: Agent skipped interview, never asked what user cared about
FIX: Made interview + persona consultation MANDATORY in this skill
```

All three bugs were caught because the walkthrough process (when followed correctly)
forces the human into the loop. Bug 3 was caught DESPITE the process being broken
— the user caught it anyway. The fix is to prevent skipping.

---

## Workflow Summary

```mermaid
flowchart TD
    START["/create-walkthrough triggered"] --> PF["Pre-Flight Checklist"]
    PF --> IV{"Phase 1: Interview\n(MANDATORY)"}
    IV -->|Not done| ASK["Use /interview or\nAskUserQuestion"]
    ASK --> IV
    IV -->|Done| PC{"Phase 1b: Persona\n(MANDATORY)"}
    PC -->|Not done| CONSULT["Use /ask consult <persona>"]
    CONSULT --> PC
    PC -->|Done| MEM["Memory recall +\ngit log + CONTEXT.md"]
    MEM --> ANALYZE["Phase 2: Read code,\nanalyze changes"]
    ANALYZE --> WRITE["Phase 3: Write walkthrough\n(incorporates interview +\npersona + memory)"]
    WRITE --> VERIFY["Phase 4: Claim verification\n./run.sh verify"]
    VERIFY -->|Mismatches| FIX["Fix claims"] --> VERIFY
    VERIFY -->|Clean| VISUAL["Phase 5: Diagrams + tables"]
    VISUAL --> PRESENT["Phase 6: Present for\nadversarial human review"]
```

---

## Memory + Taxonomy Integration

Walkthrough findings are stored in `/memory` with `/taxonomy` bridge tags for recall,
versioning, and drift detection across sessions.

### How It Works

**Pre-hook (recall):** Before writing a new walkthrough, recall prior walkthrough findings
for the same system to surface past failures, risks, and lessons.

**Post-hook (learn):** After successful claim verification, learn to memory:
1. **Walkthrough summary** — system, date, verdict, bottom line
2. **Individual risks** — for future recall
3. **Verification stats** — for drift tracking (accuracy trending over time)

All entries are tagged with taxonomy bridge attributes (Precision, Resilience, Fragility,
etc.) extracted from the walkthrough content.

### CLI Commands

```bash
# Learn walkthrough findings to memory after verification
./run.sh learn --file walkthrough.md --system "episodic-archiver" --bottom-line "Should work"

# Recall prior walkthroughs for a system
./run.sh recall "episodic-archiver"

# Recall with more results
./run.sh recall "episodic-archiver" -k 10
```

### Graceful Degradation

Memory and taxonomy are optional. If unavailable:
- `learn` command exits with error message
- `recall` command exits with error message
- Core verify/template commands work normally without memory

---

## File Structure

```
.pi/skills/create-walkthrough/
├── SKILL.md                            # This file (agent instructions)
├── walkthrough.py                      # Claim extraction + CLI (typer)
├── memory_integration.py              # Memory + taxonomy hooks
├── models.py                           # Shared data classes (Claim, Verdict, VerificationReport)
├── verifiers.py                        # All claim verifiers (13 types)
├── run.sh                              # Entry point
├── sanity.sh                           # Basic validation
└── references/
    └── walkthrough_template.md         # Blank template with all sections
```
