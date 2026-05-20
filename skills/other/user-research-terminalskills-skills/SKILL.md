---
name: user-research
description: Expert guidance for user research, helping product teams conduct interviews, create personas, design surveys, run usability tests, and synthesize findings into actionable insights. Applies both qualitative methods (interviews, contextual inquiry) and quantitative methods (surveys, analytics) to build deep understanding of user needs, behaviors, and motivations.
license: Apache-2.0
compatibility: No special requirements
metadata:
  author: terminal-skills
  version: 1.0.0
  category: business
  tags:
  - user-research
  - interviews
  - personas
  - surveys
  - usability-testing
---

# User Research — Understanding Users Through Evidence


## Overview


User research, helping product teams conduct interviews, create personas, design surveys, run usability tests, and synthesize findings into actionable insights. This skill applies both qualitative methods (interviews, contextual inquiry) and quantitative methods (surveys, analytics) to build deep understanding of user needs, behaviors, and motivations.


## Instructions

### User Interviews

```markdown
## Conduct User Interviews

### Interview Types
- **Exploratory**: Discover problems and needs (early stage, open-ended)
- **Evaluative**: Test a solution or prototype (have something to show)
- **Contextual**: Watch users in their environment (richest data)

### Interview Guide

**Warm-up (3 min)**
"Tell me about your role. What does a typical day look like?"
Goal: Build rapport, understand context.

**Current behavior (10 min)**
"Walk me through the last time you [did the relevant activity]."
"What tools did you use? What was the sequence?"
"What was the most frustrating part?"
"How long did it take?"

Follow-up probes:
- "Why did you choose to do it that way?"
- "What happened next?"
- "Can you show me?" (contextual interviews)

**Pain points (10 min)**
"What's the biggest challenge you face with [topic]?"
"Have you tried any workarounds?"
"What did you try that didn't work?"
"If this took 10x longer than it should, which part is the bottleneck?"

**Desired outcomes (5 min)**
"What would 'great' look like for you?"
"If you could change one thing, what would it be?"
"How would you know if this problem was solved?"

**Closing (2 min)**
"Is there anything I should have asked but didn't?"
"Who else should I talk to about this?"
"Would you be open to testing something we're building?"

### Interview Rules
1. **No leading questions**: ❌ "Don't you think X would be better?"
2. **Past behavior > future intent**: ❌ "Would you use..." ✅ "When was the last time you..."
3. **Silence is data**: Don't fill pauses — let them think
4. **Record with permission**: Take notes AND record (you'll miss things in real-time)
5. **5 interviews = 80% of insights**: Diminishing returns after 5-8 per segment
```

### Personas

```markdown
## Create Research-Based Personas

Personas are fictional characters based on REAL research data.
Not: your imagined ideal user. Based on: interview patterns.

### Persona Template

**Name**: "Operational Olga"
**Role**: Operations Manager at a 30-person agency
**Demographics**: 32, 5 years in ops, manages 3 teams

**Goals**:
- Reduce time spent on manual reporting (currently 6 hrs/week)
- Ensure nothing falls through the cracks during client handoffs
- Have visibility into team workload without asking for status updates

**Frustrations**:
- "I spend Monday mornings rebuilding the same spreadsheet every week"
- "I only find out about blockers in the Thursday standup — too late"
- "Our tools don't talk to each other — Asana, Slack, Google Sheets, email"

**Current tools**: Asana (project management), Google Sheets (reporting), Slack
**Tech comfort**: Comfortable with SaaS tools, not technical enough for APIs
**Decision process**: Evaluates tools herself, gets budget approval from COO

**Key quote** (from interview):
"I don't need another tool. I need the tools I have to actually work together."

**Behavioral patterns** (from data):
- Logs in 3x/day, mostly on mobile during commute
- Exports data to spreadsheets weekly
- Primary workflow: check status → identify blockers → reassign work

### Rules for Good Personas
- Based on interviews (minimum 5), not assumptions
- Include behavioral patterns, not just demographics
- Update quarterly as you learn more
- Maximum 3-4 personas — more means you haven't segmented enough
- Include anti-personas (who you're NOT building for)
```

### Surveys

```markdown
## Design Effective Surveys

### When to Survey (vs Interview)
- **Survey**: Validate at scale what you discovered in interviews
- **Interview**: Discover new insights you didn't know to ask about

Sequence: Interviews first → Survey to quantify → Interviews to deepen

### Survey Design Rules

1. **Under 5 minutes**: Response rates drop 50% after 5 minutes
2. **One topic per survey**: Don't combine satisfaction + feature requests + NPS
3. **Specific questions**: ❌ "How satisfied are you?" ✅ "How easy was it to complete [specific task]?"
4. **Avoid double-barreled**: ❌ "How fast and reliable is the product?" (those are two questions)
5. **Randomize options**: Prevent order bias on multiple choice
6. **Include "Other"**: Your options never cover everything

### Question Types by Goal

**Satisfaction**: "How would you rate your experience with [feature]?" (1-7 scale)
**Effort**: "How easy was it to [task]?" (CES — Customer Effort Score, 1-7)
**Loyalty**: "How likely are you to recommend to a colleague?" (NPS, 0-10)
**Priority**: "Rank these features by importance to your workflow" (forced ranking)
**Open-ended**: "What's the one thing you'd change?" (limit to 1-2 open questions)

### Sample Sizes
- Directional insight: 30-50 responses
- Statistically significant: 200+ responses
- Segment comparison: 100+ per segment
```

### Usability Testing

```markdown
## Run Usability Tests

### Setup
- **Participants**: 5 per round (catches ~85% of issues)
- **Tasks**: 3-5 realistic scenarios
- **Method**: Think-aloud protocol ("narrate your thoughts as you go")
- **Recording**: Screen + face (tools: Lookback, UserTesting, Maze)

### Task Design
Write tasks as goals, not instructions:

❌ "Click the Settings icon, then go to Billing, then click Upgrade"
(This tests whether they can follow instructions, not whether the UI is usable)

✅ "You want to upgrade your account to the Pro plan. Please do that now."
(This tests whether they can figure out the path)

### What to Measure
- **Task completion rate**: % who finish without help
- **Time on task**: How long to complete (benchmark against target)
- **Errors**: Wrong clicks, backtracking, confusion points
- **Severity**: Is the issue a blocker (can't proceed) or an annoyance?
- **Satisfaction**: Post-task rating ("How easy was that?" 1-7)

### Severity Scale
- **Critical**: User cannot complete the task at all
- **Major**: User completes but with significant difficulty or errors
- **Minor**: User notices but works around it easily
- **Cosmetic**: User doesn't notice but it violates best practices

### After Testing
1. List all issues found, sorted by severity
2. For each issue: what happened, why, and recommended fix
3. Fix critical/major issues before launch
4. Test again after fixes (verification round)
```


## Examples


### Example 1: Creating a user interviews for a new product

**User request:**

```
We're launching a project management tool for remote design teams. Help me create a user interviews.
```

The agent applies the User Research framework, asking clarifying questions about target audience, market positioning, and business model. It produces a structured deliverable with specific, actionable recommendations tailored to the design-tools market, including competitive positioning and key metrics to track.

### Example 2: Synthesizing interview findings into personas

**User request:**

```
I've done 12 user interviews for our project management tool. Help me synthesize the findings into actionable personas.
```

The agent analyzes the existing work against user research best practices, identifies missing elements, weak assumptions, and areas that need validation. It provides specific suggestions with reasoning, not generic advice, referencing the frameworks and patterns from the instructions above.


## Guidelines

1. **Research before building** — Talk to users before writing a single line of code; every week spent on research saves a month of building the wrong thing
2. **5 interviews = 80% of insights** — You don't need 50 interviews; 5 per segment reveals the major patterns
3. **Behavior over opinions** — Ask about what people DID, not what they WOULD do; past behavior predicts future behavior
4. **Personas from data** — Base personas on interview patterns, not marketing assumptions; update them as you learn
5. **Survey to quantify, not discover** — Use surveys to measure how many people have a problem you discovered in interviews
6. **Think-aloud usability tests** — 5 users talking through tasks reveals more than 500 survey responses about "satisfaction"
7. **Synthesize within 24 hours** — Interview insights fade fast; extract key quotes, opportunities, and patterns the same day
8. **Share findings widely** — Research is wasted if it stays in a document; present findings to engineering, design, and leadership
