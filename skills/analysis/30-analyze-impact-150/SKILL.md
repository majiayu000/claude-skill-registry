---
name: 30-analyze-impact-150
description: "[30] ANALYZE. Understand how changes impact the system — what's the core, what's affected, what depends on what. Use when planning changes, analyzing systems, debugging issues, or anytime you need to see the full picture of cause and effect. Triggers on \"what's affected\", \"impact analysis\", \"dependencies\", \"scope mapping\", or when you need to understand ripple effects."
---

# Analyze-Impact 150 Protocol

**Core Principle:** Understand the ripple effects. See how changes in one part affect the whole system.

## What This Skill Does

When you invoke this skill, you're mapping:
- **Core** — What exactly is being changed
- **Impact** — What will be affected by the change
- **Dependencies** — What the core depends on and what depends on it
- **Boundaries** — Where the effects stop

## The Impact Model

```
         [UPSTREAM]
    What the core depends on
              ↓
         [CORE]  ←── What we're changing
              ↓
        [DOWNSTREAM]
    What depends on the core
              ↓
        [BOUNDARIES]
    Where effects fade out
```

## The 150% Impact Rule

- **100% Core:** Complete understanding of what's being changed
- **50% Enhancement:** Clear view of dependencies and downstream effects

## When to Use This Skill

**Universal trigger:** Anytime you need to understand impact and dependencies.

**Specific triggers:**
- Before making changes to code/systems
- When debugging to understand cause chains
- Planning features that touch multiple parts
- Refactoring decisions
- Risk assessment
- Understanding legacy systems
- When you hear "why did changing X break Y?"

**Key insight:** Impact mapping prevents surprises. Changes don't happen in isolation.

## The Impact Layers

| Layer | Description | Coverage |
|-------|-------------|----------|
| **Core** | What's directly changing | 100% — must fully understand |
| **Immediate** | Direct dependencies and users | 50% — must assess |
| **Extended** | Secondary effects | 25% — should consider |
| **System** | Full ecosystem | 10% — be aware |

## Execution Protocol

### Step 1: DEFINE CORE
Clearly identify what's changing:
- What exactly is being modified?
- What files/components/systems?
- What's the nature of the change?

### Step 2: MAP UPSTREAM
Identify dependencies (what the core needs):
- What does this component use?
- What must exist for this to work?
- What configurations/data/services?

### Step 3: MAP DOWNSTREAM
Identify dependents (what uses the core):
- Who/what uses this component?
- What breaks if this changes?
- What needs to be updated?

### Step 4: TRACE RIPPLES
Follow the effects outward:
- What do the downstreams depend on?
- Where do effects stop?
- What's the blast radius?

### Step 5: MARK BOUNDARIES
Define where impact ends:
- What's definitely NOT affected?
- Where can we safely stop analyzing?
- What's the "fence" around the change?

## Impact Mapping Questions

**About the Core:**
- "What exactly is changing?"
- "What's the nature of the change?"
- "Is it additive, modifying, or removing?"

**About Upstream (Dependencies):**
- "What does this use/import/call?"
- "What must exist for this to work?"
- "What configs/data does it need?"

**About Downstream (Dependents):**
- "What uses/imports/calls this?"
- "What would break if this changes?"
- "Who relies on this behavior?"

**About Boundaries:**
- "Where do the ripples stop?"
- "What's definitely unaffected?"
- "What's the maximum blast radius?"

## Output Format

When using Impact-Map 150:

```
🗺️ **Impact-Map 150 Complete**

**Core Change:**
[What exactly is being changed]

**Upstream Dependencies:**
- [What this needs to work]
- [Required services/data/configs]

**Downstream Impact:**
- 🔴 Critical: [What definitely breaks]
- 🟡 Affected: [What needs checking]
- 🟢 Monitor: [What might be touched]

**Boundaries:**
- Impact stops at: [clear boundary]
- Definitely safe: [unaffected areas]

**Blast Radius:** [Small/Medium/Large/System-wide]

**Risks Identified:**
- [What could go wrong]

Ready to proceed with awareness.
```

## Visual Impact Map

```
Example: Changing User Authentication

            [Config Files]     [Environment Vars]
                   ↓                   ↓
              ┌─────────────────────────────┐
              │    🎯 CORE: Auth Module     │
              └─────────────────────────────┘
                   ↓           ↓           ↓
            [Login API]  [Session Mgmt]  [Token Gen]
                   ↓           ↓           ↓
            ┌──────────────────────────────────┐
            │ 🔴 CRITICAL: All Authenticated   │
            │    Endpoints, User Sessions      │
            └──────────────────────────────────┘
                   ↓           ↓
            ┌──────────────────────────────────┐
            │ 🟡 AFFECTED: Mobile App, Web App │
            │    Admin Panel, API Clients      │
            └──────────────────────────────────┘
                   ↓
            ┌──────────────────────────────────┐
            │ 🟢 BOUNDARY: Analytics, Logging  │
            │    (may need token format update)│
            └──────────────────────────────────┘
```

## Operational Rules

1. **CORE FIRST:** Always clearly define what's changing before mapping impact
2. **TRACE BOTH WAYS:** Map upstream (dependencies) AND downstream (dependents)
3. **MARK BOUNDARIES:** Know where the impact stops
4. **ESTIMATE BLAST RADIUS:** Understand the scale of potential effects
5. **DOCUMENT SURPRISES:** Note unexpected connections discovered
6. **VALIDATE WITH CODE:** Don't guess — check actual imports/usage

## Examples

### ❌ Without Impact Mapping
```
Task: "Update the date format in utils.js"
Action: Changed format from 'MM/DD/YYYY' to 'YYYY-MM-DD'
Result: 47 pages broke, 3 API integrations failed, customer reports corrupted
Why: Didn't map what used that utility
```

### ✅ With Impact-Map 150
```
Task: "Update the date format in utils.js"

🗺️ Impact-Map 150:

Core: formatDate() in utils.js

Upstream Dependencies:
- moment.js library
- locale config

Downstream Impact:
- 🔴 Critical: Invoice generation (uses formatDate)
- 🔴 Critical: API responses (15 endpoints)
- 🟡 Affected: All UI date displays (23 components)
- 🟢 Monitor: Log timestamps

Boundaries:
- Database stores as ISO, unaffected
- External APIs have their own formatting

Blast Radius: Large — touches most of UI

Action: Create formatDateNew(), migrate gradually, deprecate old
```

## Failure Modes & Recovery

| Failure | Detection | Recovery |
|---------|-----------|----------|
| **Missed dependency** | Something breaks unexpectedly | Expand upstream mapping |
| **Missed dependent** | Users complain after change | Trace all usages with grep/IDE |
| **Underestimated blast** | "Small change" causes chaos | Re-map with wider scope |
| **Unclear boundaries** | Don't know what's safe | Explicitly mark boundaries |

## Relationship to Other Skills

| Skill | Focus |
|-------|-------|
| **goal-clarity-150** | WHAT we want to achieve |
| **deep-think-150** | HOW to think about it |
| **impact-map-150** | WHAT it affects |
| **max-quality-150** | HOW to do it well |

**Workflow:**
```
goal-clarity-150 → impact-map-150 → deep-think-150 → max-quality-150
       ↓                 ↓                ↓                ↓
   Understand        Map what's         Think           Execute
   the goal          affected          through           well
```

---

**Remember:** Every change has ripple effects. The question isn't "will something else be affected?" but "what will be affected and how much?" Impact mapping turns surprises into planned awareness.

