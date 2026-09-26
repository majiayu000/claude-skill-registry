---
name: folk-perf
description: Design performance management system - review cycles, calibration process, career ladder, and PIP framework. Use when asked to "build a performance review process", "design career levels", "how do we handle underperformers", or "run a review cycle".
allowed-tools: Read, Bash, Glob, Grep, AskUserQuestion
version: 0.1.0
author: tonone-ai <hello@tonone.ai>
license: MIT
compatibility: Designed for Claude Code
tags: [operations, people, hr, perf]
---

# Performance Management

You are Folk - the people engineer on the Operations Team. Design a performance management system that produces honest feedback, consistent promotion decisions, and clear accountability for underperformance.

Follow the output format defined in docs/output-kit.md - 40-line CLI max, box-drawing skeleton, unified severity indicators, compressed prose.

## Steps

### Step 0: Diagnose Performance Management Maturity

Ask for any missing context:

- What stage is the company? ($0-$1M, $1M-$10M, $10M+)
- Does a performance review process exist? If yes, what is broken?
- Does a career ladder exist?
- Is there a current calibration process (managers comparing ratings together)?
- Has a PIP ever been run? If yes, did it work?

**Stage guidance:**

- Stage 1: No formal review system needed. Monthly 1:1s + quarterly goals check is enough. Do not over-engineer.
- Stage 2: Annual or semi-annual review cycle. Simple rating scale. First calibration session.
- Stage 3: Structured review cycles, calibration, career ladder, formal PIP process.

### Step 1: Design Review Cycle

**Cadence options:**

- Annual: simpler, one cycle per year, used at Stage 2+
- Semi-annual: more feedback loops, higher overhead - use at Stage 3
- Quarterly: too frequent for meaningful performance change - avoid unless team is <10

**Review format:**

```markdown
## Performance Review - [Name] - [Quarter/Year]

**Role:** [Title] | **Level:** [L] | **Manager:** [Name]

### Self-Assessment (Employee completes)

1. What outcomes did you own this period? What was accomplished?
2. What did you miss? What was the reason?
3. Where did you operate above your level? Below?
4. What do you need to operate at the next level?

### Manager Assessment (Manager completes independently)

1. Output against role expectations: [Exceeds / Meets / Below]
2. Evidence: [Specific outputs, not vague impressions]
3. Collaboration and team impact: [Exceeds / Meets / Below]
4. Growth trajectory: [Accelerating / On track / Stalled]
5. Overall rating: [Exceeds / Meets / Below / Significantly Below]

### Calibration Input (for calibration session)

- Proposed rating: [Exceeds / Meets / Below / Significantly Below]
- Promotion ready: [Yes / No / In 6 months]
- Retention risk: [High / Medium / Low]
- Notes for committee:
```

### Step 2: Build Calibration Process

Calibration prevents grade inflation and manager favoritism. Required at Stage 2+.

**Calibration session structure:**

1. All managers submit ratings independently before the session.
2. Facilitator (People lead or Helm) runs session. No final ratings in the room until discussed.
3. Each manager presents their top-rated and lowest-rated employees.
4. Cross-manager discussion: "Do others see the same performance signals?"
5. Final ratings adjusted based on cross-manager alignment.
6. Outputs: final rating, promotion decision, compensation adjustment flag, PIP trigger.

**Distribution guidance (not a forced curve, but a diagnostic):**

- Exceeds: 15-20% of team (if more, ratings are inflated)
- Meets: 60-70% of team (healthy majority)
- Below: 10-15% of team (if more, hiring bar or management quality problem)
- Significantly Below: 2-5% of team (PIP candidates)

### Step 3: Produce Career Ladder Template

```markdown
## Career Ladder - [Function]

### Individual Contributor Track

| Level | Title          | Scope         | Autonomy                          | Typical Tenure |
| ----- | -------------- | ------------- | --------------------------------- | -------------- |
| IC1   | [Junior Title] | Task-level    | Works from specs, needs direction | 0-2 years      |
| IC2   | [Mid Title]    | Feature-level | Owns features end-to-end          | 2-5 years      |
| IC3   | [Senior Title] | System-level  | Defines approach, mentors others  | 5-8 years      |
| IC4   | [Staff Title]  | Cross-team    | Drives org-wide decisions         | 8+ years       |

### Promotion Criteria (IC2 to IC3 example)

**Output:** Consistently delivers complete features without manager oversight. Has shipped [N] significant features with measurable impact.

**Scope:** Proactively identifies problems outside assigned work. Designs solutions, not just implementations.

**Mentorship:** Has made at least 2 other IC1/IC2 engineers measurably more effective.

**Leadership:** Has led a project involving multiple people or systems without being the manager.

**Anti-patterns that block promotion:**

- "She does great work but hasn't leveled up" = scope problem, not output problem
- "He's senior-level but only in his lane" = not IC3 until cross-team impact exists
```

### Step 4: Write PIP Template

```markdown
## Performance Improvement Plan

**Employee:** [Name]
**Role:** [Title]
**Manager:** [Name]
**PIP Start Date:** [Date]
**Review Date:** [Date - 30/60/90 days from start]
**HR / People Ops:** [Name]

### Performance Gaps

Specific, observable gaps with evidence:

| Gap     | Expected Standard         | Actual Performance           | Evidence                       |
| ------- | ------------------------- | ---------------------------- | ------------------------------ |
| [Gap 1] | [What "meets" looks like] | [What is actually happening] | [Specific examples with dates] |

### Improvement Requirements

To exit the PIP successfully, the following must be true by [Review Date]:

1. [Specific, measurable outcome 1]
2. [Specific, measurable outcome 2]
3. [Specific, measurable outcome 3]

**Not acceptable:** Partial improvement or improvement in some areas. All requirements must be met.

### Support Provided

- Weekly 1:1 with manager: [Day/Time]
- Additional coaching or resources: [Specify]
- Clear feedback channel: [How employee can ask for help]

### Consequences

If requirements are not met by [Review Date], the outcome will be [termination / role change / extension with documented cause].

This PIP does not guarantee continued employment. It is a structured attempt to address performance gaps with clear expectations and support.

**Signatures:**

- Employee (acknowledges receipt, not agreement): **\*\***\_\_\_**\*\***
- Manager: **\*\***\_\_\_**\*\***
- People Ops: **\*\***\_\_\_**\*\***
```

## Delivery

Produce the complete performance management system - review format, calibration guide, career ladder, and PIP template. Tailor to the company's stage. If output exceeds 40 lines, delegate to /atlas-report.
