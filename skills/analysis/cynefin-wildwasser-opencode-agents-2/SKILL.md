---
name: cynefin
description: Cynefin sense-making framework categorizing problems as Simple, Complicated, Complex, Chaotic, or Confused to select the right approach. Use when unsure how to tackle a problem.
user-invocable: true
---

# Cynefin Analysis

Analyze a situation through the Cynefin framework to understand what type of problem it is and choose the appropriate response.

## Instructions

Determine which Cynefin domain the problem belongs to, then apply the appropriate response approach. Be willing to recognize that parts of a problem may span multiple domains.

### Output Format

**Situation**: [What we're analyzing]

---

## Initial Assessment

**Characteristics Check**

| Characteristic | Yes/No/Maybe | Evidence |
|---------------|--------------|----------|
| Cause and effect are clear and predictable | | |
| Experts can analyze and determine the answer | | |
| Outcomes can only be understood in hindsight | | |
| The situation is unstable/in crisis | | |
| We genuinely don't know what kind of problem this is | | |

---

## Domain Classification

**Primary Domain**: [Simple/Complicated/Complex/Chaotic/Confused]

**Why this domain?**
[Reasoning for the classification]

---

## Domain-Appropriate Response

### If SIMPLE/OBVIOUS
*Sense → Categorize → Respond*

**Best Practice to Apply**: [The established approach]

### If COMPLICATED
*Sense → Analyze → Respond*

**Experts Needed**: [Who has the expertise?]
**Analysis Required**: [What to investigate?]

### If COMPLEX
*Probe → Sense → Respond*

**Safe-to-Fail Experiments**:
| Probe | What We'd Learn | Amplify if... | Dampen if... |
|-------|-----------------|---------------|---------------|
| [experiment] | [insight] | [success indicators] | [failure indicators] |

**Key Mindset**: Don't try to predict. Try things, observe, adapt.

### If CHAOTIC
*Act → Sense → Respond*

**Immediate Stabilization**: [What action do we take right now?]

### If CONFUSED
*Break down, then categorize*

| Sub-problem | Likely Domain | Why |
|-------------|---------------|-----|
| [sub-problem] | [domain] | [reasoning] |

---

## Boundary Warnings

| Transition | Warning Signs | What to Do |
|------------|--------------|------------|
| Simple → Chaotic | Complacency | Challenge assumptions |
| Complicated → Complex | Analysis not converging | Try probes instead |
| Complex → Chaotic | Loss of control | Stabilize fast |

---

## Recommended Approach

**Given this is a [DOMAIN] problem, we should:**
1. [Primary approach]
2. [Supporting action]

## Guidelines

- Most people default to Complicated (analysis) when Complex (probes) is needed
- "Best practice" is only valid in Simple domain
- In Complex, you can't predict—you can only experiment and adapt
- In Chaotic, act first, think later

$ARGUMENTS
