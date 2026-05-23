---
name: vc-router
description: Intelligent skill routing with automatic selection, composition, and fallback. Use when the user doesn't specify a skill, says "just do it", or wants the AI to decide the best approach.
---

# VC Router - ULTIMATE EDITION

## Core Philosophy

```
┌─────────────────────────────────────────────────────────────┐
│                   INTELLIGENT ROUTING                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. UNDERSTAND INTENT - Not just keywords                   │
│  2. SELECT BEST FIT - With confidence scoring               │
│  3. COMPOSE IF NEEDED - Chain skills intelligently          │
│  4. FALLBACK GRACEFULLY - Always have a path forward        │
│  5. LEARN FROM RESULTS - Improve routing over time          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Quick Invoke

Any of these activate the router:
- `use vc-router: <goal>`
- `just do this: <goal>`
- `vc go <goal>` (router mode)
- `vc finish <goal>` (force end-to-end)
- `vcf: <goal>` → routes to vc-phase-loop
- `use vcf: <goal>` → same as above

---

## The Routing Engine

### Step 1: Intent Classification

```
┌─────────────────────────────────────────────────────────────┐
│              INTENT CLASSIFICATION                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Extract from user request:                                 │
│  ├─ ACTION: What to do (build, create, fix, analyze...)    │
│  ├─ DOMAIN: What area (frontend, backend, docs, git...)    │
│  ├─ OUTPUT: Expected result (file, component, document...) │
│  └─ SCOPE: Size of task (single file, multi-file, system)  │
│                                                             │
│  Example: "Build a login page with OAuth"                   │
│  ├─ ACTION: build                                           │
│  ├─ DOMAIN: frontend                                        │
│  ├─ OUTPUT: page/component                                  │
│  └─ SCOPE: multi-file                                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Step 1.5: Sub-Agent Assisted Routing (Optional)

If the request is **large, ambiguous, or multi-domain**, spawn **1–2 sub-agents** to parallelize:
- Repo scan: locate relevant code/config and constraints
- Risk scan: identify security/ops risks and validation strategy

Rules:
- Keep it lightweight (max 2) and timeboxed.
- Sub-agents report findings only; main agent makes routing decision.
- If sub-agents aren’t available, continue without them.

### Step 2: Skill Matching

```
┌─────────────────────────────────────────────────────────────┐
│              SKILL MATCHING MATRIX                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  VC-ONLY DISTRIBUTION:                                      │
│  ├─ "finish", "hands off" → vc-phase-loop                   │
│  ├─ Multi-step, open-ended → vc-phase-loop                  │
│  └─ Everything else → vc-phase-loop                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Step 3: Confidence Scoring

```
For each potential skill match, calculate confidence:

HIGH (80-100%): Clear keyword match + domain match
  → Route immediately

MEDIUM (50-79%): Partial match, some ambiguity
  → Select best fit, proceed with note

LOW (<50%): Weak match, unclear intent
  → Use vc-phase-loop as safe default
```

---

## Skill Composition

This repo intentionally ships only `vc*` skills, so there are no additional bundled skills to chain.

If the request is multi-domain or open-ended, route to `vc-phase-loop` and run the full end-to-end workflow.

---

## Fallback Strategy

### When No Skill Matches

```
┌─────────────────────────────────────────────────────────────┐
│              FALLBACK HIERARCHY                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Level 1: Route to vc-phase-loop (universal fallback)       │
│                                                             │
│  NEVER: "I don't know which skill to use"                   │
│  ALWAYS: Route to vc-phase-loop as universal fallback     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Error Recovery

### When Selected Skill Fails

```
Skill Failed
    ↓
Analyze failure reason
    ↓
Option 1: Retry same skill with adjusted approach
    ↓
Option 2: Try alternative skill from same category
    ↓
Option 3: Decompose task and route parts separately
    ↓
Option 4: Escalate to vc-phase-loop for full autonomy
    ↓
NEVER: Stop and report failure without attempting recovery
```

---

## VC Defaults

For ALL routing decisions:
- Prefer fast iteration over perfection
- Make safe default choices without pausing
- Ask questions only after delivering initial result
- Keep outputs concise and actionable
- Assume user is non-technical

---

## VC Finish Mode

When user triggers "vc finish" explicitly:
- ALWAYS route to vc-phase-loop
- Enable full autonomous execution
- No mid-stream questions
- Complete end-to-end
- Provide completion proof

Triggers:
- "vc finish", "finish it", "take it to the end"
- "plan and execute", "hands off"

---

## Execution Rules

1. **Single Pass Classification** - Decide quickly, don't overthink
2. **Best Fit Selection** - If uncertain, choose narrower scope skill
3. **Immediate Execution** - Route and run, collect questions for end
4. **Safe Defaults** - vc-phase-loop handles anything
5. **No Dead Ends** - Always have a path forward

---

## Routing Decision Log

For transparency, log routing decisions:

```markdown
## Routing Decision

Request: "Build a login page"
Classification:
  - Action: build
  - Domain: frontend
  - Output: page
  - Scope: multi-file

Candidates:
  1. vc-phase-loop (100% match)

Selected: vc-phase-loop
Reason: vc-only distribution; use the end-to-end engine as the default.

Proceeding with execution...
```

---

## The Router Promise

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   YOU SAY WHAT YOU WANT.                                    │
│                                                             │
│   WE UNDERSTAND YOUR INTENT.                                │
│   WE SELECT THE BEST SKILL.                                 │
│   WE COMPOSE IF NEEDED.                                     │
│   WE RECOVER FROM FAILURES.                                 │
│   WE ALWAYS HAVE A PATH FORWARD.                            │
│                                                             │
│   NO "I DON'T KNOW" - ALWAYS ROUTE.                         │
│   NO DEAD ENDS - ALWAYS FALLBACK.                           │
│   NO FAILURES - ALWAYS RECOVER.                             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```
