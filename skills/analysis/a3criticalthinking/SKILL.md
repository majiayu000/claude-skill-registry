---
name: A3CriticalThinking
description: |
  Toyota-style A3 problem solving with embedded priority hierarchy: Safety First, then Customer Value, then Shareholder Value.
  Structured thinking framework for manufacturing decisions, root cause analysis, and countermeasure development.

  USE WHEN user says 'A3', 'problem solving', 'root cause', 'countermeasure', '5 whys', 'fishbone', 'ishikawa',
  'priority decision', 'safety first', 'critical thinking', or needs structured analysis of manufacturing problems.

  Integrates with AutomotiveManufacturing and HoshinKanri skills.
---

# A3 Critical Thinking

## When to Activate This Skill

- "Create an A3 for [problem]"
- "Help me think through [decision]"
- "Root cause analysis for [issue]"
- "What should take priority here?"
- "Is this safe to proceed?"
- "Evaluate tradeoffs for [options]"
- "5 Whys analysis"
- "Fishbone diagram for [defect]"

---

## The Priority Hierarchy

**Every decision must pass through this filter, in order:**

```
┌─────────────────────────────────────────────────────┐
│  1. SAFETY FIRST                                    │
│     Will anyone be harmed? Stop everything else.    │
│     • Employee safety                               │
│     • Customer safety (product in use)              │
│     • Environmental safety                          │
│     • Community safety                              │
└─────────────────────────────────────────────────────┘
                        ↓ Only if SAFE
┌─────────────────────────────────────────────────────┐
│  2. CUSTOMER VALUE                                  │
│     Does this create good products for customers?   │
│     • Quality that meets/exceeds requirements       │
│     • Reliability and durability                    │
│     • On-time delivery                              │
│     • Fitness for purpose                           │
└─────────────────────────────────────────────────────┘
                        ↓ Only if QUALITY assured
┌─────────────────────────────────────────────────────┐
│  3. SHAREHOLDER VALUE                               │
│     Now optimize for business results               │
│     • Cost efficiency                               │
│     • Productivity                                  │
│     • Return on investment                          │
│     • Growth and sustainability                     │
└─────────────────────────────────────────────────────┘
```

**Critical Rule:** Never sacrifice a higher priority for a lower one. A cost saving that compromises safety is NEVER acceptable. A delivery acceleration that reduces quality is NEVER acceptable.

---

## The Decision Test

Before any significant decision, apply this test:

### Question 1: Is it SAFE?
- Could this harm employees, customers, or the environment?
- Are all safety controls in place?
- Have we identified and mitigated risks?
- If NO: **STOP. Address safety first.**

### Question 2: Does it serve the CUSTOMER?
- Will product quality be maintained or improved?
- Does this meet customer specifications?
- Will delivery commitments be met?
- If NO: **STOP. Find an alternative that protects quality.**

### Question 3: Is it EFFICIENT?
- Only after safety and quality are assured, optimize for:
  - Cost reduction
  - Cycle time improvement
  - Resource utilization
  - Profitability

---

## A3 Problem Solving Framework

The A3 is a single-page structured approach to problem solving:

```
┌─────────────────────────────────────────────────────────────────┐
│ TITLE: [Problem Name]                    DATE:                  │
│ OWNER: [Named Individual]                REV:                   │
├─────────────────────────────────────────────────────────────────┤
│ 1. BACKGROUND/CONTEXT         │ 2. CURRENT CONDITION            │
│                               │                                  │
│ Why is this problem important?│ What is actually happening?      │
│ What triggered this A3?       │ Data, facts, observations        │
│ Business impact               │ Process map of current state     │
│                               │ Quantify the gap                 │
├───────────────────────────────┼──────────────────────────────────┤
│ 3. TARGET CONDITION/GOAL      │ 4. ROOT CAUSE ANALYSIS           │
│                               │                                  │
│ What should be happening?     │ 5 Whys                           │
│ Specific, measurable target   │ Fishbone/Ishikawa                │
│ Timeline for achievement      │ Data analysis                    │
│                               │ Verified root cause(s)           │
├───────────────────────────────┴──────────────────────────────────┤
│ 5. COUNTERMEASURES                                               │
│                                                                  │
│ # │ Action               │ Owner    │ Due Date │ Status         │
│ 1 │                      │          │          │                │
│ 2 │                      │          │          │                │
│ 3 │                      │          │          │                │
├──────────────────────────────────────────────────────────────────┤
│ 6. IMPLEMENTATION PLAN        │ 7. FOLLOW-UP/RESULTS             │
│                               │                                  │
│ Gantt or timeline             │ Verification data                │
│ Resources required            │ Before/after comparison          │
│ Risks and mitigation          │ Lessons learned                  │
│                               │ Horizontal deployment?           │
└───────────────────────────────┴──────────────────────────────────┘
```

---

## Root Cause Analysis Tools

### 5 Whys Method

Keep asking "Why?" until you reach the root cause (typically 5 levels):

```
Problem: Machine stopped producing
  Why? → Fuse blew
    Why? → Motor overheated
      Why? → Bearing failed
        Why? → Lubrication insufficient
          Why? → No preventive maintenance schedule

ROOT CAUSE: Missing PM program for bearings
```

**Rules:**
- Each "Why" must be factual, not assumed
- Verify each level before proceeding
- May branch into multiple root causes
- Stop when you reach something you can control

### Fishbone (Ishikawa) Diagram

Categorize potential causes:

```
    Man          Machine        Material
      \            |            /
       \           |           /
        \          |          /
         ─────────[EFFECT]─────────
        /          |          \
       /           |           \
      /            |            \
   Method      Measurement    Environment
```

**Manufacturing Categories:**
- **Man/People:** Training, skills, fatigue, following procedures
- **Machine:** Equipment condition, calibration, capability
- **Material:** Specifications, supplier quality, storage
- **Method:** Procedures, work instructions, sequence
- **Measurement:** Gages, accuracy, repeatability
- **Environment:** Temperature, humidity, cleanliness, lighting

---

## Countermeasure Hierarchy

When developing solutions, prefer higher levels:

| Level | Type | Description | Example |
|-------|------|-------------|---------|
| 1 | **Eliminate** | Remove the possibility entirely | Design out the feature |
| 2 | **Substitute** | Replace with inherently safer/better | Different material |
| 3 | **Engineer** | Physical barriers or controls | Interlock, guard |
| 4 | **Administrate** | Procedures, training | Work instruction |
| 5 | **PPE/Inspect** | Last resort protection | Check, verify |

**Rule:** Never rely solely on administrative controls for safety-critical issues.

---

## Quick Decision Framework

For rapid decisions under pressure:

```
┌─────────────────────────────────────────────┐
│         STOP AND ASK                        │
├─────────────────────────────────────────────┤
│ S - Safety: Is anyone at risk?              │
│ T - Target: What are we trying to achieve?  │
│ O - Options: What choices do we have?       │
│ P - Priority: Safety → Quality → Cost       │
└─────────────────────────────────────────────┘
```

If uncertain about safety: **STOP PRODUCTION** until verified safe.

---

## Integration Points

### With AutomotiveManufacturing Skill
- A3 links to PFMEA updates when new failure modes identified
- Countermeasures cascade to Work Instructions
- Control Plans updated based on A3 findings

### With HoshinKanri Skill
- Red bowling chart items trigger A3
- A3 countermeasures become improvement priorities
- Completed A3s document breakthrough achievements

### With Quality Systems (IATF 16949)
- A3 satisfies 10.2 Nonconformity and Corrective Action
- Links to 8D methodology for customer complaints
- Supports Management Review inputs

---

## Templates Available

| Template | Purpose | Location |
|----------|---------|----------|
| A3 Template | Standard problem solving | `templates/a3-template.md` |
| Quick A3 | Simplified one-pager | `templates/quick-a3.md` |
| 5 Whys | Root cause worksheet | `templates/5-whys.md` |
| Fishbone | Ishikawa diagram | `templates/fishbone.md` |
| Decision Matrix | Weighted option comparison | `templates/decision-matrix.md` |
| Priority Check | Safety-Quality-Cost verification | `templates/priority-check.md` |

---

## Common Mistakes to Avoid

1. **Jumping to Solutions** - Do root cause analysis first
2. **Blaming People** - Look at systems and processes
3. **Stopping at Symptoms** - Dig deeper with 5 Whys
4. **No Verification** - Confirm countermeasures worked
5. **Ignoring the Hierarchy** - Never shortcut Safety → Quality → Cost
6. **No Horizontal Deployment** - Share learnings across similar processes
7. **Paper Exercise** - A3 must drive real action

---

## Key Principles

1. **Go See (Genchi Genbutsu)** - Observe the actual condition yourself
2. **Facts Over Opinions** - Base analysis on data and evidence
3. **Respect for People** - Solutions should support workers, not blame them
4. **PDCA Cycle** - Plan-Do-Check-Act is embedded in the A3
5. **One Problem, One Owner** - Named individual accountability
6. **Visual Thinking** - Use diagrams, charts, photos
7. **Priority Discipline** - Safety → Customer → Shareholder, always

---

## Extended Context

For detailed methodologies and advanced techniques:
`read ~/.claude/skills/A3CriticalThinking/CLAUDE.md`

For templates:
`ls ~/.claude/skills/A3CriticalThinking/templates/`
