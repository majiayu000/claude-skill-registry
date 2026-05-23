---
name: thinking-archetypes
description: Recognize Senge's Systems Archetypes to diagnose recurring organizational and technical problems, identify why fixes keep failing, and design interventions that address root structure.
---

# Systems Archetypes

## Overview

Systems archetypes, developed by Peter Senge in "The Fifth Discipline," are recurring patterns of behavior in organizations and systems. Like design patterns in software, once you recognize them, you see them everywhere—and more importantly, you can predict where they lead and intervene effectively.

**Core Principle:** Most organizational problems aren't unique. They follow predictable patterns with predictable consequences. Recognizing the pattern reveals the leverage points.

## When to Use

- The same problems keep recurring despite multiple "fixes"
- Quick fixes seem to make things worse over time
- Teams or departments are stuck in counterproductive cycles
- Growth has stalled without obvious cause
- Competition or conflict is escalating destructively
- Shared resources are being depleted
- Success in one area is starving others

Decision flow:

```
Problem keeps recurring despite fixes?  → yes → APPLY ARCHETYPES
Growth hit invisible ceiling?           → yes → APPLY ARCHETYPES
Competition escalating destructively?   → yes → APPLY ARCHETYPES
Shared resource degrading?              → yes → APPLY ARCHETYPES
```

## The Seven Core Archetypes

### 1. Fixes That Fail

**Pattern:** A quick fix addresses symptoms but creates side effects that eventually make the original problem worse.

```
        Problem
           │
           ▼
     ┌─────────────┐
     │  Quick Fix  │──────────────┐
     └─────────────┘              │
           │                      │
           ▼                      │
      Symptom Relief              │
      (short-term)                │
                                  ▼
                          Unintended
                          Consequence
                                  │
                                  │ (delay)
                                  │
                                  ▼
                            Problem
                            Worsens
```

**Recognition Signs:**

- "We fixed this last quarter, why is it back?"
- Solution requires repeated application with increasing doses
- New problems emerged after implementing the fix
- The fix addresses symptoms, not root cause

**Software Examples:**

- Adding more servers instead of fixing memory leak → costs spiral, leak remains
- Hiring contractors to meet deadline → knowledge loss increases future delays
- Skipping tests to ship faster → bugs multiply, requiring more hotfixes
- Silencing alerts instead of investigating → system degrades until outage

**Leverage Points:**

- Identify and address root cause, not symptoms
- Ask "What side effects might this create?"
- Build in delay to observe consequences before scaling fix
- Make unintended consequences visible early

---

### 2. Shifting the Burden

**Pattern:** A symptomatic solution is used instead of a fundamental solution, reducing pressure to address the real problem and creating dependency.

```
                 Problem Symptom
                 ┌─────┴─────┐
                 ▼           ▼
          ┌──────────┐  ┌──────────────┐
          │Symptomatic│  │ Fundamental  │
          │ Solution  │  │  Solution    │
          └────┬─────┘  └──────┬───────┘
               │               │
               │ (quick)       │ (slow, hard)
               │               │
               ▼               ▼
          Relief +          Actual
          Dependency        Resolution
               │
               ▼
          Fundamental
          Solution Atrophies
```

**Recognition Signs:**

- Heavy reliance on workarounds
- "We know the real fix, but we don't have time"
- Expertise for fundamental solution is disappearing
- External helpers (consultants, contractors) are permanent

**Software Examples:**

- Using feature flags to hide bugs → never fixing underlying issues
- Operations team manually intervening → no investment in automation
- Senior devs always fixing junior code → juniors never learn
- Buying SaaS tools instead of building core capability → vendor lock-in

**Leverage Points:**

- Make the fundamental solution visible and valued
- Track and limit use of symptomatic solutions
- Invest in building internal capability
- Ask "What capability are we not developing by using this workaround?"

---

### 3. Limits to Growth

**Pattern:** A reinforcing loop drives growth, but eventually encounters a balancing constraint that slows or stops growth.

```
     ┌───────────────────────────────────┐
     │                                   │
     ▼                                   │
  Growing        ────(+)────▶        Results
  Action                                 │
                                         │
                                         │
                    ┌────────────────────┘
                    │
                    ▼
              ┌───────────┐
              │ Limiting  │
              │ Condition │
              └─────┬─────┘
                    │
                    │ (-)
                    ▼
              Slowing
              Action
```

**Recognition Signs:**

- Growth was strong, then plateaued without obvious cause
- More effort yields diminishing returns
- A resource or capability is maxed out
- Success is creating its own bottlenecks

**Software Examples:**

- Team velocity drops as codebase grows (complexity limit)
- Adding engineers doesn't speed delivery (communication overhead)
- Feature growth slows due to technical debt (architectural limit)
- User growth outpaces database capacity (infrastructure limit)

**Leverage Points:**

- Identify the limiting factor early, before it binds
- Invest in removing constraints BEFORE they become critical
- Don't push harder on the reinforcing loop—address the constraint
- Ask "What will limit our growth at 10x scale?"

---

### 4. Tragedy of the Commons

**Pattern:** Individuals gain by using a shared resource, but collective overuse depletes the resource for everyone.

```
     ┌──────────────┐       ┌──────────────┐
     │  Actor A's   │       │  Actor B's   │
     │   Activity   │       │   Activity   │
     └──────┬───────┘       └──────┬───────┘
            │                      │
            │ (individual gain)    │ (individual gain)
            │                      │
            ▼                      ▼
       ┌────────────────────────────────┐
       │       Shared Resource          │
       │    (depletes over time)        │
       └────────────────────────────────┘
                      │
                      │ (delay)
                      ▼
              Resource Degradation
              Affects All Actors
```

**Recognition Signs:**

- Shared resources are degrading (CI/CD, staging environments, shared services)
- Everyone optimizes locally at expense of global system
- "Somebody else will fix it" mentality
- No clear ownership of shared infrastructure

**Software Examples:**

- Teams overload shared CI/CD → everyone's builds slow down
- No one invests in shared libraries → they rot
- Staging environment becomes unreliable → everyone bypasses it
- On-call knowledge isn't documented → tribal knowledge concentrates
- Cloud costs spike as teams spin up resources without cleanup

**Leverage Points:**

- Make usage visible and attributable
- Create feedback loops (chargebacks, quotas, dashboards)
- Establish shared governance with clear ownership
- Align individual incentives with collective health
- Ask "Who is responsible for the long-term health of this?"

---

### 5. Escalation

**Pattern:** Two parties perceive their success as relative to each other. Each side's actions provoke response, leading to escalating competition that harms both.

```
     ┌─────────────┐              ┌─────────────┐
     │  Actor A    │              │  Actor B    │
     │   Action    │              │   Action    │
     └──────┬──────┘              └──────┬──────┘
            │                            │
            │     ┌───────────────┐      │
            └────▶│  Relative     │◀─────┘
                  │  Standing     │
                  └───────────────┘
                          │
                          │ (perceived threat)
            ┌─────────────┴─────────────┐
            ▼                           ▼
       A Increases                 B Increases
         Action                      Action
            │                           │
            └───────────────────────────┘
                     (cycle repeats)
```

**Recognition Signs:**

- "They did X, so we have to do Y"
- Arms race dynamics in spending, features, or resources
- Each side feels defensive, not aggressive
- Win-lose framing of what could be win-win

**Software Examples:**

- Feature war with competitor → both over-invest, neither profits
- Microservices teams duplicating functionality → bloat and inconsistency
- Departments hoarding headcount → organizational inefficiency
- Interview arms race → absurd technical interviews that don't predict success

**Leverage Points:**

- Step back and question the "game" being played
- Find ways to opt out or change the rules
- Establish shared standards or agreements
- Focus on absolute value, not relative position
- Ask "What would happen if we stopped competing on this dimension?"

---

### 6. Success to the Successful

**Pattern:** If success gives access to more resources, initial advantages compound while others are starved, creating winner-take-all dynamics.

```
     ┌─────────────┐              ┌─────────────┐
     │  Actor A    │              │  Actor B    │
     │  (initial   │              │  (initial   │
     │   success)  │              │  struggle)  │
     └──────┬──────┘              └──────┬──────┘
            │                            │
            ▼                            ▼
      More Resources              Fewer Resources
      Allocated to A              Allocated to B
            │                            │
            ▼                            ▼
      A More Likely               B Less Likely
      to Succeed                  to Succeed
            │                            │
            └───────────────────────────┘
                   (cycle compounds)
```

**Recognition Signs:**

- Star performers get more opportunities, others stagnate
- Successful products get more investment, experiments are starved
- Some teams have surplus resources while others are underwater
- Past success is the main predictor of future investment

**Software Examples:**

- Legacy monolith gets all attention → new architecture never matures
- Star engineer gets all interesting projects → others disengage
- Flagship product consumes resources → innovation pipeline dies
- Cloud costs centralized → teams with budget dominate

**Leverage Points:**

- Ensure fair initial resource allocation
- Create protected space for emerging initiatives
- Evaluate on trajectory, not just current position
- Deliberately invest in "underdogs" with potential
- Ask "Are we starving future successes to feed current ones?"

---

### 7. Growth and Underinvestment

**Pattern:** Growth approaches a limit that could be addressed by investment in capacity, but the investment isn't made until performance degrades, triggering a crisis.

```
        Demand
           │
           │ (grows)
           ▼
     ┌───────────┐
     │  Capacity │ (fixed or slowly growing)
     └───────────┘
           │
           │ (demand > capacity)
           ▼
     Performance
     Degradation
           │
           │ (finally triggers)
           ▼
     Investment
     Decision
           │
           │ (but with delay)
           ▼
     Capacity
     Increase
     (too late, crisis already happened)
```

**Recognition Signs:**

- "We'll invest in X when we really need it"
- Performance degrades, then investment happens reactively
- Chronic underinvestment in infrastructure, platform, or people
- Standard is "good enough for now"

**Software Examples:**

- Database not upgraded until it crashes under load
- Security investment only after breach
- Team not grown until burnout causes attrition
- Technical debt addressed only during outages
- Documentation written only when onboarding fails

**Leverage Points:**

- Define performance standards and invest to maintain them
- Lead indicators (not lag) should trigger investment
- Calculate cost of delayed investment (opportunity cost, crisis cost)
- Build investment into growth plans proactively
- Ask "What will fail if we grow 50% without additional investment?"

---

## Archetype Diagnosis Process

### Step 1: Describe the Problem Neutrally

Document what's happening without blame:

- What symptoms are visible?
- Who is involved?
- What has been tried?
- What keeps recurring?

### Step 2: Map the Feedback Loops

Draw the causal connections:

- What causes what?
- Where are reinforcing loops (amplifying)?
- Where are balancing loops (limiting)?
- Where are delays?

### Step 3: Match to Archetype

Compare your map to the seven patterns:

| If You See... | Consider Archetype |
|---------------|-------------------|
| Fix that makes problem worse over time | Fixes That Fail |
| Workaround becoming dependency | Shifting the Burden |
| Growth hitting invisible ceiling | Limits to Growth |
| Shared resource degrading | Tragedy of the Commons |
| Competitive spiral harming both sides | Escalation |
| Winner-take-all resource dynamics | Success to the Successful |
| Reactive investment after crisis | Growth and Underinvestment |

### Step 4: Identify Leverage Points

Don't push on the obvious—find where small changes have large effects:

- Where can you break a reinforcing loop?
- Where can you remove a constraint?
- What information is missing that would change behavior?
- What incentives are misaligned?

### Step 5: Design Intervention

Target the structure, not the symptoms:

- What fundamental solution is being avoided?
- What constraint needs investment?
- What feedback loop is missing or delayed?
- How can you make the system self-correcting?

---

## Quick Reference Card

| Archetype | Pattern | Key Question |
|-----------|---------|--------------|
| Fixes That Fail | Quick fix creates long-term problems | "What side effects will this create?" |
| Shifting the Burden | Dependency on symptomatic solutions | "What capability are we not building?" |
| Limits to Growth | Reinforcing loop hits constraint | "What will limit us at 10x?" |
| Tragedy of the Commons | Individual gain depletes shared resource | "Who owns the long-term health?" |
| Escalation | Competitive loop worsens both | "Can we change the game?" |
| Success to the Successful | Winner-take-all dynamics | "Are we starving future successes?" |
| Growth and Underinvestment | Capacity lags demand until crisis | "What fails at 50% growth?" |

## Verification Checklist

- [ ] Problem described without blame
- [ ] Feedback loops mapped (reinforcing and balancing)
- [ ] Delays identified in the system
- [ ] Matched to one or more archetypes
- [ ] Leverage points identified (not just symptoms)
- [ ] Intervention targets structure, not behavior
- [ ] Unintended consequences of intervention considered

## Key Questions

- "What pattern is this system stuck in?"
- "Where would a small change have a large effect?"
- "What fundamental solution are we avoiding?"
- "What would make this system self-correcting?"
- "If we do nothing, where does this pattern lead?"
- "Who benefits from the current structure persisting?"

## Senge's Wisdom

"Structures of which we are unaware hold us prisoner. Once we can see them, they no longer have the same hold on us."

Recognizing the archetype is the first step to escaping it. The pattern will continue until someone sees it and changes the underlying structure—not the behaviors, but what's driving them.
