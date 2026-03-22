---
name: create-postmortem
description: Create a blameless postmortem when the user asks to write a postmortem, document what went wrong, analyze an incident, or run a 5 Whys analysis
author: chalk
version: "1.0.0"
metadata-version: "3"
allowed-tools: Read, Glob, Grep, Write
argument-hint: "[incident description or reference to incident report]"
read-only: false
destructive: false
idempotent: false
open-world: false
user-invocable: true
tags: incident, postmortem, learning
---

# Create Postmortem

## Overview

Generate a blameless postmortem following Google SRE principles, combining 5 Whys root cause analysis with the Swiss cheese model for safety barrier analysis. Postmortems focus on systemic contributing factors rather than a single root cause, and refer to roles rather than individuals to maintain a blameless culture.

## Workflow

1. **Read incident context** — Scan `.chalk/docs/engineering/` for incident reports matching the described incident. If an incident report exists, use its timeline, impact data, and preliminary root cause as input. Also check for previous postmortems to identify recurring patterns.

2. **Parse the incident** — Extract from `$ARGUMENTS` and any linked incident report: what happened, when, what was affected, and how it was resolved. If details are insufficient, ask one round of clarifying questions covering the timeline, impact scope, and resolution steps.

3. **Verify blamelessness** — Before writing, review all input for named individuals. Replace names with roles (e.g., "the on-call engineer" instead of "Alice"). The postmortem describes systems, processes, and decisions — not people.

4. **Identify contributing factors** — Avoid naming a single "root cause." Most incidents result from multiple contributing factors that align (Swiss cheese model). Identify each layer that failed: process, tooling, monitoring, testing, communication, architecture.

5. **Run 5 Whys per contributing factor** — For each contributing factor, ask "Why?" five times to trace from the symptom to the systemic issue. Stop when you reach a factor that is actionable and systemic, not when you reach a person's decision.

6. **Analyze safety barriers** — Using the Swiss cheese model, document which safety barriers existed and which failed. Categories: Detection (monitoring, alerting), Prevention (code review, testing, feature flags), Mitigation (rollback, circuit breakers, graceful degradation), Communication (status pages, incident channels, escalation paths).

7. **Check for recurrence** — Search `.chalk/docs/engineering/` for previous postmortems or incident reports with similar contributing factors. If this is a recurring theme, flag it explicitly and reference previous documents.

8. **Write action items** — Every action item must be categorized as Detect, Prevent, or Mitigate. Each must have an owner (role or team, not individual name) and a due date. Prioritize actions that address the deepest systemic issues, not just the immediate trigger.

9. **Document what went well** — Identify aspects of the response that worked: fast detection, effective communication, successful rollback, team coordination. This section is mandatory.

10. **Determine the next file number** — List files in `.chalk/docs/engineering/` to find the highest numbered file. Increment by 1.

11. **Write the file** — Save to `.chalk/docs/engineering/<n>_postmortem_<incident>.md`.

12. **Confirm** — Present the postmortem with a summary of contributing factors, the number of action items, and any recurrence warnings.

## Postmortem Structure

```markdown
# Postmortem: <Incident Title>

**Date of Incident**: <YYYY-MM-DD>
**Postmortem Date**: <YYYY-MM-DD>
**Status**: Draft | Reviewed | Final
**Severity**: SEV-1 | SEV-2 | SEV-3 | SEV-4
**Related Incident Report**: <link or filename, if available>

## Summary

<2-3 sentences: What happened, what was the impact, and how was it resolved. Written for someone encountering this postmortem without prior context.>

## Impact

| Dimension | Measurement |
|-----------|-------------|
| Users Affected | <number or percentage> |
| Duration (user-facing) | <total time users experienced the issue> |
| Revenue Impact | <estimated amount or "not measurable"> |
| Data Impact | <records affected or "no data impact"> |
| SLA Breach | <Yes — details / No> |

## Timeline

All times in <timezone>.

| Time | Event |
|------|-------|
| <HH:MM> | <event description> |
| <HH:MM> | <event description> |

## Contributing Factors

> There is rarely a single root cause. The following factors combined to produce this incident.

### Factor 1: <Name>

<Description of this contributing factor and how it contributed to the incident.>

#### 5 Whys

1. **Why** <symptom>? → <answer>
2. **Why** <answer>? → <deeper answer>
3. **Why** <deeper answer>? → <systemic issue>
4. **Why** <systemic issue>? → <organizational gap>
5. **Why** <organizational gap>? → <actionable root>

### Factor 2: <Name>

<Description and 5 Whys for this factor.>

## What Safety Barriers Failed

Using the Swiss cheese model: each barrier is a layer of defense. When holes in multiple layers align, incidents occur.

### Detection
- <What monitoring or alerting should have caught this? Did alerts fire? Were they actionable?>

### Prevention
- <What process or tooling should have prevented this from reaching production? Code review, testing, feature flags, validation?>

### Mitigation
- <What mechanisms should have limited the blast radius? Rollback, circuit breakers, rate limiting, graceful degradation?>

### Communication
- <Was the right information communicated to the right people at the right time? Status pages, incident channels, customer communication?>

## Action Items

### Detect

| ID | Action | Owner | Due Date |
|----|--------|-------|----------|
| D-1 | <action> | <team or role> | <YYYY-MM-DD> |

### Prevent

| ID | Action | Owner | Due Date |
|----|--------|-------|----------|
| P-1 | <action> | <team or role> | <YYYY-MM-DD> |

### Mitigate

| ID | Action | Owner | Due Date |
|----|--------|-------|----------|
| M-1 | <action> | <team or role> | <YYYY-MM-DD> |

## What Went Well

- <Positive aspects of the incident response>
- <Practices that should be reinforced>

## Recurrence Check

<Have similar incidents occurred before? If yes, reference the previous postmortem/incident report and explain why prior action items did not prevent recurrence. If no prior incidents, state that explicitly.>
```

## Output

- **File**: `.chalk/docs/engineering/<n>_postmortem_<incident>.md`
- **Format**: Plain markdown, no YAML frontmatter
- **First line**: `# Postmortem: <Incident Title>`

## Anti-patterns

- **Blame language** — "The deploy engineer pushed broken code" assigns personal blame. "A deployment introduced a regression that was not caught by existing test coverage" describes the system failure. Refer to roles, not names. Focus on what the system allowed, not what a person did.
- **Single root cause** — Declaring one root cause oversimplifies complex system failures. Incidents almost always have multiple contributing factors. If you find yourself writing "Root Cause:" (singular), stop and look for what else had to be true for this incident to occur.
- **Action items without owners or due dates** — "We should improve monitoring" is a wish. "Add latency alerting for payment service P99 > 2s — Owner: Platform Team — Due: 2024-12-20" is an action item. Every action item must have both an owner and a due date.
- **No "what went well" section** — Postmortems that only catalog failures demoralize teams and discourage incident reporting. Always acknowledge what worked: fast detection, effective rollback, clear communication, team coordination.
- **Not checking for recurrence** — If a similar incident happened before, the most important question is: why didn't the previous action items prevent this one? Failing to check previous postmortems misses the systemic pattern.
- **Shallow 5 Whys** — Stopping at "because the test was missing" instead of asking why the testing process didn't require that test. Keep asking until you reach a systemic or organizational factor that can be addressed with a process or tooling change.
- **Postmortem without follow-through** — Writing a thorough postmortem and never completing the action items is worse than not writing one at all. Action items must be tracked to completion.
