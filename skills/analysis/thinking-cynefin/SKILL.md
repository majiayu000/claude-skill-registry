---
name: thinking-cynefin
description: Classify problems by complexity domain (clear, complicated, complex, chaotic) and match approach to domain. Use for choosing methodologies, problem framing, and process design.
---

# Cynefin Framework

## Overview

The Cynefin framework, developed by Dave Snowden, classifies problems into domains based on the relationship between cause and effect. Different domains require fundamentally different approaches. Using the wrong approach for the domain leads to failure—agile doesn't fix truly complex problems, and detailed planning doesn't help in chaos.

**Core Principle:** The nature of the problem determines the nature of the solution. Match your approach to the domain.

## When to Use

- Choosing the right methodology for a project
- Understanding why an approach isn't working
- Designing processes for different problem types
- Deciding how much to plan vs. experiment
- Understanding organizational challenges
- Incident response and crisis management

Decision flow:

```
Facing a problem?
  → What's the relationship between cause and effect?
    → Obvious? → CLEAR DOMAIN
    → Requires analysis? → COMPLICATED DOMAIN
    → Only visible in retrospect? → COMPLEX DOMAIN
    → Cannot perceive? → CHAOTIC DOMAIN
```

## The Five Domains

### 1. Clear (formerly Simple/Obvious)

**Characteristics:**
- Cause and effect are obvious to everyone
- Best practices exist and work
- Repeatable processes

**Approach: Sense → Categorize → Respond**

```
Problem: Server disk is full
Sense: Alert shows disk at 100%
Categorize: Known issue with known fix
Respond: Clear old logs, add monitoring

Appropriate method:
- Standard operating procedures
- Checklists
- Best practices
- Automation
```

**Failure mode:** Complacency. Treating complex problems as clear leads to oversimplification.

### 2. Complicated

**Characteristics:**
- Cause and effect require expertise to see
- Multiple right answers exist
- Good practices (not "best" practices)
- Expert analysis needed

**Approach: Sense → Analyze → Respond**

```
Problem: Application performance degradation
Sense: Response times increased 3x
Analyze: Profile, trace, identify bottleneck (requires expertise)
Respond: Apply appropriate fix based on analysis

Appropriate method:
- Expert analysis
- Waterfall/planning
- Detailed specifications
- Engineering analysis
- Multiple valid solutions
```

**Failure mode:** Analysis paralysis. Over-analyzing when action is needed, or treating complicated problems as if they're clear.

### 3. Complex

**Characteristics:**
- Cause and effect only visible in retrospect
- Emergent behavior
- Cannot predict outcomes
- Patterns emerge from interactions

**Approach: Probe → Sense → Respond**

```
Problem: User engagement is declining
Probe: Run experiments, try interventions
Sense: See what patterns emerge
Respond: Amplify what works, dampen what doesn't

Appropriate method:
- Safe-to-fail experiments
- Agile/iterative
- Prototyping
- A/B testing
- Emergent strategy
```

**Failure mode:** Trying to analyze/plan your way through complexity. The system is too interconnected for analysis; you must probe and learn.

### 4. Chaotic

**Characteristics:**
- No perceivable cause and effect
- High turbulence
- Need to act first to create stability
- No time for analysis

**Approach: Act → Sense → Respond**

```
Problem: Production is down, cause unknown
Act: Take immediate action to stabilize (rollback, failover)
Sense: Once stable, assess what happened
Respond: Move to complex/complicated domain for investigation

Appropriate method:
- Command and control
- Decisive action
- Rapid response
- Crisis management
```

**Failure mode:** Trying to analyze during chaos. The priority is stability, not understanding.

### 5. Disorder (Center)

**Characteristics:**
- Don't know which domain you're in
- Multiple stakeholders perceive different domains
- Confusion and disagreement about approach

**Approach:** Break the problem into parts, classify each part

```
Problem: "We need to fix our development process"
Reality: Some parts are clear (coding standards)
         Some parts are complicated (architecture decisions)
         Some parts are complex (team dynamics)

Solution: Break apart, apply appropriate approach to each
```

## Domain Assessment

### Step 1: Assess Cause-Effect Relationship

```markdown
## Domain Assessment: [Problem]

Can you see clear cause-effect?
- [ ] Yes, obvious to everyone → CLEAR
- [ ] Yes, but requires expertise → COMPLICATED
- [ ] No, only visible after the fact → COMPLEX
- [ ] No, completely turbulent → CHAOTIC
- [ ] Unsure, mixed signals → DISORDER
```

### Step 2: Test Your Assessment

| Domain | Test | If yes, stay | If no, reconsider |
|--------|------|--------------|-------------------|
| Clear | Do best practices exist and work reliably? | Clear | Maybe Complicated |
| Complicated | Can experts predict outcomes? | Complicated | Maybe Complex |
| Complex | Can you run safe-to-fail experiments? | Complex | Maybe Chaotic |
| Chaotic | Is the situation too turbulent to experiment? | Chaotic | Maybe Complex |

### Step 3: Match Approach

```markdown
## Approach Selection

Domain: [Assessment result]

Appropriate approach:
- Decision-making style: [Best practice / Expert analysis / Experimentation / Crisis response]
- Planning depth: [Detailed / Moderate / Minimal / None]
- Methodology: [Process / Analysis / Agile / Command]
- Success measure: [Efficiency / Quality / Learning / Stability]
```

## Common Mismatches

### Treating Complex as Complicated

```
Symptom: Extensive planning, but outcomes keep surprising
Example: Detailed user research, perfect spec, but users don't engage
Why it fails: You can't analyze your way to understanding emergent behavior
Fix: Probe with experiments, sense patterns, iterate
```

### Treating Complicated as Clear

```
Symptom: "Just do it" approach to expert problems
Example: "Build it like they did at [Company]" without understanding why
Why it fails: Context matters; expertise reveals nuances
Fix: Engage experts, analyze the specific situation
```

### Treating Chaotic as Complex

```
Symptom: Running experiments during a crisis
Example: "Let's A/B test during the outage"
Why it fails: Chaos requires immediate stability, not learning
Fix: Act decisively first, learn later
```

### Treating Clear as Complicated

```
Symptom: Over-engineering simple problems
Example: Designing an architecture for "Hello World"
Why it fails: Wasted effort, delayed delivery
Fix: Apply best practice, don't over-analyze
```

## Domain-Appropriate Practices

### For Clear Domain

```markdown
## Clear Domain Practices

- Standard operating procedures
- Checklists (like the surgical checklist)
- Automation and scripting
- Documentation
- Training and certification
- Process compliance

Example applications:
- Deployment procedures
- Coding standards
- Basic incident response
- Onboarding checklists
```

### For Complicated Domain

```markdown
## Complicated Domain Practices

- Expert analysis and consultation
- Structured problem-solving
- Architecture reviews
- Root cause analysis
- Design specifications
- Scenario planning

Example applications:
- System architecture
- Performance optimization
- Security review
- Technology selection
```

### For Complex Domain

```markdown
## Complex Domain Practices

- Safe-to-fail experiments
- Iterative development
- Retrospectives
- Emergent design
- Short feedback loops
- Feature flags

Example applications:
- Product development
- Team process improvement
- User experience design
- Organizational change
```

### For Chaotic Domain

```markdown
## Chaotic Domain Practices

- Decisive leadership
- Clear command
- Rapid triage
- Communication of actions
- Post-incident review (later)

Example applications:
- Major outages
- Security incidents
- Crisis response
- Emergency triage
```

## Cynefin Template

```markdown
# Cynefin Analysis: [Problem/Situation]

## Problem Statement
[Describe the problem]

## Domain Assessment

### Cause-Effect Analysis
Relationship: [Clear / Requires expertise / Retrospective / Turbulent]
Evidence: [What makes you believe this]

### Domain Classification
Domain: [Clear / Complicated / Complex / Chaotic / Disorder]

### Confidence Check
Could this be a different domain? [Assessment]

## Approach

Based on [domain], the appropriate approach is:

| Aspect | Approach |
|--------|----------|
| Decision style | [Best practice / Analysis / Experimentation / Crisis response] |
| Planning | [Detailed / Moderate / Minimal / None] |
| Methodology | [Process / Waterfall / Agile / Command] |
| Success metric | [Efficiency / Quality / Learning / Stability] |

## Specific Actions
Given the domain, I will:
1. [Action]
2. [Action]
```

## Verification Checklist

- [ ] Assessed cause-effect relationship honestly
- [ ] Considered if domain assessment might be wrong
- [ ] Matched approach to domain
- [ ] Not applying complicated solutions to clear problems
- [ ] Not planning detailed solutions for complex problems
- [ ] Not experimenting during chaos
- [ ] Ready to reassess as situation evolves

## Key Questions

- "What's the relationship between cause and effect here?"
- "Can experts reliably predict the outcome?"
- "Am I applying the right approach for this domain?"
- "Is this actually complex, or am I avoiding the analysis?"
- "Is this actually complicated, or am I over-planning?"
- "Has the situation moved to a different domain?"

## Snowden's Wisdom

"Complex systems are not causal—they're dispositional. You can't predict what will happen; you can only influence what might happen."

"The only way to understand a complex system is to probe it and see how it responds."

Different problems require different thinking. The failure isn't in your methodology—it's in applying the wrong methodology to the wrong domain. Match the approach to the problem, not the other way around.
