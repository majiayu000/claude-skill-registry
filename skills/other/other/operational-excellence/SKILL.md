---
name: operational-excellence
type: domain
family: executive
rigor: standard
description: "Use when designing execution systems, OKR frameworks, or operational processes."
keywords: "execution, systems, OKRs, management, processes, operations, efficiency"
compatibility: "Claude Code and compatible agent products"
requires: []
enhances: ["strategy-clarity", "team-builder", "prd-writing"]
sources_pdf: ["High Output Management (Grove)", "Measure What Matters (Doerr)", "Working Backwards (Bryar)", "An Elegant Puzzle (Larson)", "The Mythical Man-Month (Brooks)"]
sources_web: ["Stratechery: The Amazon Tax", "Google re:Work: Team Effectiveness", "Farnam Street: Second-Order Thinking"]
---

## Overview

Operational excellence is the discipline of creating high-leverage execution systems that translate strategic choices into measurable output. This skill focuses on building "Mechanisms" (not just good intentions), managing by controllable inputs, and optimizing team topology for maximum flow.

## Guiding Principles

### Principle 1: Manage by Leverage (Source: Grove, *High Output Management*)
A manager's output is the output of the units under their influence. High-leverage activities—those that affect many people for a long time—must be prioritized over low-leverage tactical "busyness."

### Principle 2: Mechanisms, Not Good Intentions (Source: Bryar, *Working Backwards*)
If a process fails, do not ask for more "effort" or "better focus." Build a Mechanism—a recurring, automated process that includes a tool, a training, and an audit to ensure the problem is solved structurally.

### Principle 3: Focus on Controllable Inputs (Source: Bryar, *Working Backwards*)
You cannot control outputs like revenue or stock price. You can only control inputs like selection, price, and convenience. Operational excellence requires identifying and obsessively measuring the inputs that drive the desired outputs.

### Principle 4: Task-Relevant Maturity (TRM) (Source: Grove, *High Output Management*)
Management style is not fixed; it must adapt to the subordinate's experience level in a *specific task*. High TRM requires a hands-off, objective-oriented approach; low TRM requires detailed, process-oriented monitoring.

### Principle 5: The Amazon Tax (Source: Stratechery, "The Amazon Tax")
Design internal operations as modular service layers (APIs). If an internal service is efficient enough to be externalized, it becomes a profit center rather than a cost center. This forces internal units to compete at market standards.

## When to Use This Skill

- When a team is "Falling Behind" or "Treading Water" and needs system redesign.
- When setting quarterly OKRs or annual planning.
- When a recurring failure occurs despite "good intentions."
- When scaling an organization from a single team to a "Team of Teams."

## When NOT to Use This Skill

- For highly creative, non-linear tasks where process would stifle innovation.
- For one-off, low-stakes activities where the "Mechanism" overhead exceeds the benefit.

## Core Process

### Step 1: Identify the Limiting Step
Model the operational flow and identify the "bottleneck" or "limiting step"—the part of the process that is most difficult, expensive, or slow. (Source: Grove, Ch. 2)
1. **Model the Breakfast Factory:** Map the steps from input to final output.
2. **Synchronize:** All other steps must be timed and resourced relative to the limiting step.

### Step 2: Define Controllable Input OKRs
Establish a measurement framework that focuses on leading indicators. (Source: Doerr, Ch. 1-5)
1. **Objectives:** Where do we want to go? (Significant, concrete, action-oriented).
2. **Key Results:** How will we know we are getting there? (Specific, time-bound, aggressive but realistic).
3. **Audit:** Ensure the KRs are "Controllable Inputs," not lagging outputs.

### Step 3: Build the Mechanism Loop
Transform a solution into a permanent system. (Source: Bryar, Ch. 1)
1. **The Tool:** Create the process/software that performs the task.
2. **The Adoption:** Train the team and integrate the tool into the daily workflow.
3. **The Inspection:** Build a recurring audit (e.g., Weekly Business Review) to ensure the tool is working as intended.

### Step 4: Optimize Team Topology
Ensure team size and structure support flow. (Source: Larson, Ch. 1)
1. **Sizing:** Aim for 6-8 people per team to minimize communication overhead. (Source: Brooks, *Mythical Man-Month*)
2. **State Check:** Is the team Falling Behind, Treading Water, Repaying Debt, or Innovating?
3. **Shift Resources:** Move resources to teams "Falling Behind" until they reach "Treading Water."

### Step 5: Second-Order Audit
Predict the consequences of operational changes. (Source: Farnam Street, "Second-Order Thinking")
1. **The "And Then What?" Test:** What will happen 10 months from now if we implement this process?
2. **System Response:** How will other departments react to this change?

## Frameworks & Models

### The Four States of a Team (Source: Larson, *An Elegant Puzzle*)
1. **Falling Behind:** Backlog is growing. *Strategy: Hire more people.*
2. **Treading Water:** Work is getting done, but no time for debt. *Strategy: Reduce WIP, consolidate.*
3. **Repaying Debt:** Making improvements to speed up future work. *Strategy: Maintain focus.*
4. **Innovating:** Most work is new value creation. *Strategy: Sustain and prevent stagnation.*

### The F.A.C.T.S. of OKRs (Source: Doerr, *Measure What Matters*)
- **Focus:** 3-5 high-impact objectives.
- **Alignment:** Cascading goals from company to individual.
- **Commitment:** Publicly stated and tracked goals.
- **Tracking:** Data-driven reviews.
- **Stretching:** Aiming for 70% achievement (The "Stretching" Goal).

## Cross-Skill Invocations

- **REQUIRED SUB-SKILL:** `non-fiction-precision` — Use written narratives (6-pagers) to describe operational plans.
- **RECOMMENDED SUB-SKILL:** `feedback-coach` — Pair OKRs with CFRs (Conversations, Feedback, Recognition).
- **RECOMMENDED SUB-SKILL:** `decision-frameworks` — To choose between competing operational priorities.

## Common Mistakes

1. **Managing by Lagging Indicators:** Focusing on revenue or profit instead of the inputs that drive them. (Source: Bryar, Ch. 4)
2. **Mistaking Activity for Output:** Assuming that being "busy" equals high leverage. (Source: Grove, Ch. 3)
3. **The "Good Intentions" Trap:** Trying to fix a systemic failure by asking people to "try harder." (Source: Bryar, Ch. 1)
4. **Over-Measuring:** Creating too many OKRs, leading to a loss of focus. (Source: Doerr, Ch. 2)

## Diagnostic Checklist

- [ ] Have we identified the "Limiting Step" in this process?
- [ ] Are our OKRs focused on "Controllable Inputs" rather than outputs?
- [ ] Is there a recurring "Mechanism" (tool + audit) in place for this process?
- [ ] Are team sizes optimized (6-8 people) to minimize communication debt?
- [ ] Have we performed a "Second-Order" audit of this operational change?

## Sources

- Grove, *High Output Management*, Ch. 1-3, 6, 11 — Leverage, Production, MBO, TRM.
- Doerr, *Measure What Matters*, Ch. 1-5, 15 — OKRs, CFRs.
- Bryar & Carr, *Working Backwards*, Ch. 1, 4, 5 — Mechanisms, Inputs, Narratives.
- Larson, *An Elegant Puzzle*, Ch. 1-2 — Team states, Systems thinking.
- Stratechery, "The Amazon Tax" — Service externalization.
