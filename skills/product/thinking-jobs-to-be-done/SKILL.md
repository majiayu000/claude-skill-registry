---
name: thinking-jobs-to-be-done
description: Understand what "job" users hire your product to do, focusing on progress users seek rather than features. Use for product development, feature prioritization, user research, and market positioning.
---

# Jobs to Be Done

## Overview

Jobs to Be Done (JTBD), developed by Clayton Christensen, reframes product thinking around the progress customers are trying to make in their lives. People don't buy products; they "hire" products to do a job. Understanding the job reveals what you're really competing against and what success looks like.

**Core Principle:** People don't want a quarter-inch drill. They don't even want a quarter-inch hole. They want to hang a picture of their family.

## When to Use

- Product development and roadmapping
- Feature prioritization
- User research and interviews
- Competitive analysis
- Market positioning
- Understanding "surprising" competitors
- Debugging low adoption of features

Decision flow:

```
Building/improving a product?
  → Do you understand the job users hire it for? → no → DISCOVER THE JOB
  → Are features not being adopted? → yes → CHECK JOB ALIGNMENT
  → Surprising competitors winning? → yes → IDENTIFY THEIR JOB
```

## Understanding Jobs

### The Job Formula

```
When I [situation/trigger]
I want to [motivation/progress]
So I can [desired outcome/better state]
```

**Example:**
```
When I [finish a project milestone]
I want to [notify my team without disrupting their focus]
So I can [maintain team awareness while respecting their time]

Job: "Keep team informed asynchronously"
Not: "Use Slack" (that's a solution, not the job)
```

### Job Dimensions

Every job has multiple dimensions:

| Dimension | Question | Example (Project Management Tool) |
|-----------|----------|-----------------------------------|
| Functional | What task needs doing? | Track tasks, assign work, see progress |
| Emotional | How do I want to feel? | In control, not overwhelmed, confident |
| Social | How do I want to appear? | Organized, reliable, professional |

### Job Context

Jobs are situation-specific:

```
Same person, different jobs:

Morning: "Help me triage what needs attention today"
         → Simple dashboard, prioritized list

Deep work: "Get out of my way, let me focus"
           → Minimal notifications, distraction-free

End of day: "Help me hand off cleanly so I can disconnect"
            → Status summary, async update capabilities
```

## The JTBD Discovery Process

### Step 1: Identify Job Performers

Who is "hiring" your product?

```markdown
## Job Performers

Primary: Engineering managers
- Hire product for: tracking team delivery
- Frequency: daily
- Stakes: team performance visible to leadership

Secondary: Individual engineers
- Hire product for: knowing what to work on next
- Frequency: multiple times daily
- Stakes: personal productivity and recognition
```

### Step 2: Discover Jobs Through Interviews

Ask about behavior, not hypotheticals:

```markdown
## JTBD Interview Questions

About recent usage:
- "Walk me through the last time you used [product]"
- "What triggered you to open it?"
- "What were you trying to accomplish?"
- "How did you know when you were done?"

About the switch:
- "What were you using before?"
- "What wasn't working about the old solution?"
- "What finally made you switch?"
- "What did you give up by switching?"

About progress:
- "What does success look like for this task?"
- "How do you know when things are going well?"
- "What frustrates you most about this process?"
```

### Step 3: Analyze Competing Solutions

What else could do this job?

```markdown
## Competition for "Keep team informed on project status"

Direct competitors:
- Other project management tools (Asana, Monday.com)

Indirect competitors (same job, different solution):
- Email updates
- Slack messages
- Weekly standup meetings
- Walking over to someone's desk
- Spreadsheets

Non-consumption:
- Just hope everyone knows
- Let things fall through cracks

Insight: We're not competing with other tools—we're competing
        with "just send an email" and "bring it up in standup"
```

### Step 4: Map Job Steps

Break the job into stages:

```markdown
## Job Map: "Deliver working software on time"

1. Define: Understand what needs to be built
   - Sub-jobs: Clarify requirements, estimate scope, identify risks

2. Plan: Organize how to build it
   - Sub-jobs: Break into tasks, sequence work, allocate resources

3. Execute: Build the thing
   - Sub-jobs: Track progress, remove blockers, adjust course

4. Validate: Confirm it works
   - Sub-jobs: Test, get feedback, verify acceptance criteria

5. Deliver: Get it to users
   - Sub-jobs: Deploy, communicate, monitor

Pain points cluster around: #2 (scope conflicts) and #3 (blocker visibility)
```

### Step 5: Identify Outcome Metrics

What does success look like for the job?

```markdown
## Desired Outcomes: "Deliver working software on time"

Minimize:
- Time spent on status reporting
- Surprises in sprint reviews
- Blocked time waiting for others
- Rework from misunderstood requirements

Maximize:
- Confidence in delivery timeline
- Clarity on priorities
- Team awareness of blockers
- Early warning of issues
```

## JTBD Application Patterns

### Feature Prioritization

```markdown
## Feature Evaluation: Job Lens

Feature: Advanced reporting dashboard

Job it serves: "Demonstrate team value to leadership"
Job performers: ~10% of users (managers reporting up)
Job frequency: Monthly
Alternative solutions: Screenshots + slides (works fine)

Verdict: Low priority - job is infrequent, alternatives adequate

---

Feature: Blocker visibility alerts

Job it serves: "Remove obstacles before they delay delivery"
Job performers: ~60% of users (anyone managing work)
Job frequency: Daily
Alternative solutions: Manual check-ins (time-consuming, often missed)

Verdict: High priority - frequent job, poor alternatives
```

### Competitive Analysis

```markdown
## Competitive Analysis via JTBD

Our product: Developer documentation tool

Traditional competitive frame:
- Competitors: ReadMe, GitBook, Docusaurus
- Differentiation: Features, pricing, integrations

JTBD competitive frame:
Job: "Help developers integrate our API successfully"

Competitors for this job:
- Our own code examples (strongest competitor!)
- Stack Overflow answers
- Competitor's documentation
- Direct support from our team
- Just trying stuff until it works

Insight: Improving code examples in docs might beat any feature work
```

### Low Adoption Debugging

```markdown
## Why isn't Feature X being used?

Feature: Automated weekly report generation
Usage: 3% of target users

JTBD analysis:
Expected job: "Create status reports efficiently"
Actual job: "Demonstrate my judgment and insight to leadership"

Problem: Automated reports don't show judgment
         The PROCESS of creating reports is part of the job
         They want to curate, not automate

Solution: Change from "generate report" to "draft report for review"
          Support the curation job, don't replace it
```

## JTBD Template

```markdown
# Jobs to Be Done Analysis: [Product/Feature]

## Job Performers
| Performer | Hire For | Frequency | Stakes |
|-----------|----------|-----------|--------|
| | | | |

## Primary Job

When I [situation/trigger]
I want to [motivation/progress]
So I can [desired outcome]

### Job Dimensions
- Functional: [What task]
- Emotional: [How feel]
- Social: [How appear]

## Job Map
1. [Stage]: [Sub-jobs]
2. [Stage]: [Sub-jobs]
...

## Competing Solutions
| Competitor | How it does the job | Where it falls short |
|------------|---------------------|---------------------|
| | | |

## Desired Outcomes
Minimize:
- [Negative outcome]

Maximize:
- [Positive outcome]

## Implications
- Feature should: [Insight]
- Feature shouldn't: [Insight]
- Position against: [True competitor]
```

## Verification Checklist

- [ ] Identified job performers (who hires the product)
- [ ] Articulated job in When/Want/So format
- [ ] Considered functional, emotional, and social dimensions
- [ ] Mapped job steps
- [ ] Identified all competing solutions (including non-consumption)
- [ ] Defined measurable desired outcomes
- [ ] Features traced to specific jobs

## Key Questions

- "What job is the user hiring this product to do?"
- "What progress are they trying to make?"
- "What are they switching from? (Including 'nothing')"
- "What are they giving up by using this?"
- "What does success look like for this job?"
- "What surprising competitors exist for this job?"

## Christensen's Wisdom

"People don't want a quarter-inch drill bit. They want a quarter-inch hole."

Actually: They want to hang a picture. Actually: They want to enjoy their family photos. The deeper you go, the more insight you get into what "better" really means.

"The jobs that arise in people's lives are the fundamental causal driver behind everything."

Products don't fail because of features. They fail because they don't help people make progress on jobs they care about. Understand the job, and the features become obvious.
