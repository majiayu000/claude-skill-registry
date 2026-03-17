---
name: "Post-Mortem Facilitation Skill"
description: "Learn from failures without blame. Improve systems, not shame people."
applyTo: "**/*incident*,**/*postmortem*,**/*retro*,**/*failure*,**/*outage*"
---

# Post-Mortem Facilitation Skill

> Learn from failures without blame. Improve systems, not shame people.

## Core Principle

Every incident is a gift—an opportunity to make the system stronger. Blame prevents learning.

## The Blameless Philosophy

| Blame Culture | Learning Culture |
|---------------|------------------|
| "Who messed up?" | "How did the system allow this?" |
| "They should have known" | "Why wasn't it obvious?" |
| "Follow the process!" | "Is the process followable?" |
| "Don't let it happen again" | "How do we prevent this class of problem?" |

**Key insight**: People did what made sense to them at the time, with the information they had.

## Post-Mortem Template

### 1. Summary (2-3 sentences)
What happened, when, impact.

### 2. Timeline
| Time (UTC) | Event | Actor/System |
|------------|-------|--------------|
| 14:00 | Deployment started | CI/CD |
| 14:05 | Error rate increased | Monitoring |
| 14:07 | On-call paged | PagerDuty |
| ... | ... | ... |

### 3. Impact
- **Duration**: How long?
- **Users affected**: How many?
- **Revenue impact**: If applicable
- **Data loss**: Any?
- **Reputation**: Customer communications?

### 4. Root Cause(s)
Not "human error"—go deeper:
- Why was the error possible?
- What safeguards didn't catch it?
- What systemic conditions contributed?

### 5. What Went Well
- Detection time
- Response coordination
- Communication
- Recovery speed

### 6. What Could Be Improved
- Missing alerts
- Documentation gaps
- Process friction
- Tool limitations

### 7. Action Items

| Action | Owner | Due Date | Priority |
|--------|-------|----------|----------|
| Add validation | @alice | 2026-02-15 | P1 |
| Improve runbook | @bob | 2026-02-10 | P2 |
| ... | ... | ... | ... |

**Rule**: Every action item has an owner and date. No orphan items.

## Facilitation Guide

### Before the Meeting
1. Gather timeline from logs, chat, alerts
2. Identify all participants (responders, stakeholders)
3. Set expectation: learning, not blame
4. Share draft timeline for review

### During the Meeting

**Opening (5 min)**
> "We're here to understand what happened and improve. This is blameless—we assume everyone acted reasonably with the info they had. Focus on systems and processes, not individuals."

**Timeline Walk-through (20 min)**
- Go chronologically
- Ask: "What did you know at this point?"
- Ask: "What options did you see?"
- Fill in gaps in understanding

**Root Cause Discussion (15 min)**
- Use 5 Whys technique
- Look for systemic issues
- Avoid stopping at "human error"

**Action Items (15 min)**
- Prioritize by impact and effort
- Assign owners IN the meeting
- Set realistic due dates
- Limit to 3-5 meaningful items (not 20 small ones)

**Closing (5 min)**
> "Thank you for the candid discussion. We'll share the write-up for review. Any final thoughts?"

### After the Meeting
1. Write up within 24 hours
2. Circulate for factual corrections
3. Publish to team/org
4. Track action items to completion
5. Review effectiveness in 30 days

## Anti-Patterns to Avoid

| Anti-Pattern | Why It's Harmful |
|--------------|------------------|
| Naming individuals in root cause | Creates fear, hides future problems |
| "They should have..." | Hindsight bias, doesn't fix systems |
| No action items | Wasted learning opportunity |
| Too many action items | Nothing gets done |
| Action items without owners | Nothing gets done |
| Never following up | Actions drift, cynicism grows |
| Only for big incidents | Small incidents have big lessons |

## Questions That Unlock Learning

- "What information would have helped at that moment?"
- "What made sense to do at the time?"
- "Where did our mental model differ from reality?"
- "What surprised you?"
- "What was harder than expected?"
- "If this happens again, what would we do differently?"
- "What's the smallest change that would have prevented this?"

## Severity Classification

| Severity | Criteria | Post-Mortem Required? |
|----------|----------|----------------------|
| SEV1 | Customer-facing outage > 30min | Yes, within 48 hours |
| SEV2 | Degraded service, workaround exists | Yes, within 1 week |
| SEV3 | Internal impact, no customer effect | Recommended |
| SEV4 | Near-miss, caught before impact | Optional but valuable |

## Connecting to Prevention

Post-mortems feed into:
- **Runbooks**: Better playbooks for next time
- **Monitoring**: New alerts for early detection
- **Testing**: New test cases for CI/CD
- **Architecture**: Design changes to prevent recurrence
- **Training**: Skills gaps identified

## The Phoenix Post-Mortem

*A personal example from Alex's own evolution...*

What we learned from the Phoenix incident:
- Two sources of truth caused confusion
- Testing in production (Master Alex) was risky
- Kill switches need multiple layers
- Document decisions as you make them

These lessons became: ADR-006, RISKS.md, the 5-layer protection system.

**Every failure makes the architecture stronger.**

## Synapses

See [synapses.json](synapses.json) for connections.
