---
name: customer-feedback-analyzer
description: Synthesize user feedback from multiple channels and identify patterns to inform product decisions. Use when analyzing feedback, prioritizing feature requests, conducting NPS surveys, or understanding user sentiment. Covers feedback collection, categorization, prioritization frameworks, and closing the feedback loop.
---

# Customer Feedback Analyzer

Collect, analyze, and prioritize user feedback to inform product decisions.

## Core Principle

**Never collect feedback you won't act on.** Collecting feedback creates expectation of action. If you can't commit to reviewing and acting on it, don't ask for it. Destroys trust.

## Feedback Channels

### 1. In-App Feedback Widget

**Best for**: Contextual feedback, low friction

```javascript
// Contextual feedback
<FeedbackWidget
  context={{
    page: 'dashboard',
    feature: 'export',
    user_action: 'clicked_export'
  }}
  placeholder="How can we improve exports?"
/>
```

**Pros**: High quality (contextual), immediate
**Cons**: Can interrupt user flow

### 2. NPS Surveys

**Best for**: Measuring overall satisfaction and loyalty

```yaml
Question: "How likely are you to recommend [Product] to a friend or colleague?"
Scale: 0-10

Scoring:
  Promoters (9-10): Love your product, will advocate
  Passives (7-8): Satisfied but not enthusiastic
  Detractors (0-6): Unhappy, will churn

NPS = % Promoters - % Detractors

Benchmarks:
  Excellent: ≥50
  Good: 30-49
  Needs Work: <30
```

**Follow-up question**: "What's the main reason for your score?"

### 3. Support Tickets

**Best for**: Identifying recurring issues

```yaml
Pattern Recognition:
  - Same issue reported 5+ times → UX problem, not edge case
  - Support time > 10 min per ticket → Needs better docs
  - Ticket volume spike → Recent deploy likely caused issue
```

### 4. User Interviews

**Best for**: Deep qualitative insights

```yaml
Interview Structure:
  1. Background (5 min): Their role, use case
  2. Problem Discovery (10 min): Challenges they face
  3. Solution Validation (10 min): Show prototype, get reaction
  4. Wrap-up (5 min): Any other feedback?

Sample Size: 5-10 users per persona
```

### 5. Feature Request Voting

**Best for**: Prioritizing roadmap

**Tools**: Canny, ProductBoard, Upvoty

```yaml
Benefits:
  - See most requested features
  - Reduce duplicate requests
  - Public roadmap transparency
  - Close the loop automatically

Avoid:
  - Building everything requested
  - Letting voters drive strategy
```

### 6. Exit Interviews

**Best for**: Understanding why users churn

```yaml
Key Questions:
  - What made you decide to cancel?
  - What feature/change would have kept you?
  - What are you switching to?
  - What did we do well?
```

## Feedback Categorization

### By Type

```yaml
Bug: Something broken
  - "Export fails with >100 rows"
  - Priority: Fix immediately

Feature Request: New capability
  - "Add Slack integration"
  - Priority: Vote/validate

Enhancement: Improve existing feature
  - "Export should include timestamps"
  - Priority: Nice to have

Usability: Confusing UX
  - "Can't find where to invite team members"
  - Priority: High (friction)

Performance: Speed issue
  - "Dashboard loads slowly"
  - Priority: Depends on impact
```

### By Severity

```yaml
Critical: Blocks core workflow
  - "Can't save projects"
  - Action: Hotfix immediately

High: Significant friction
  - "Onboarding confusing"
  - Action: Fix this sprint

Medium: Minor annoyance
  - "Button text unclear"
  - Action: Fix next quarter

Low: Edge case or cosmetic
  - "Spacing looks off on mobile"
  - Action: Backlog
```

### By Frequency

```yaml
Widespread: 50+ reports
  → High priority

Common: 10-50 reports
  → Medium priority

Occasional: 5-10 reports
  → Low priority, monitor

Rare: <5 reports
  → Likely edge case, document workaround
```

### By User Segment

```yaml
Power Users: High engagement, experienced
  → Actionable, technical feedback

New Users: Recently signed up
  → Onboarding issues, first impressions

Churned Users: Cancelled/inactive
  → Why did they leave?

Enterprise: Paying customers
  → Security, compliance, integrations
```

## Prioritization Framework

### Priority Score Formula

```
Score = Impact (1-5) × Frequency (1-5) × Strategic Alignment (1-5)

Score ≥ 40: High Priority (next sprint)
Score 20-39: Medium Priority (next quarter)
Score < 20: Low Priority (backlog or never)
```

**Example**:

```yaml
Feedback: "Add Slack integration"
  Impact: 4 (significantly improves collaboration)
  Frequency: 5 (50+ requests)
  Strategic Alignment: 4 (fits roadmap)
  Score: 4 × 5 × 4 = 80

  Decision: HIGH PRIORITY - Build next sprint

Feedback: "Change button color"
  Impact: 1 (minor cosmetic)
  Frequency: 1 (1 person mentioned)
  Strategic Alignment: 1 (not strategic)
  Score: 1 × 1 × 1 = 1

  Decision: LOW PRIORITY - Backlog
```

## Close the Feedback Loop

### 1. Acknowledge

```markdown
Email Template:

Subject: Thanks for your feedback!

Hi [Name],

Thanks for taking the time to share your thoughts on [topic].

We review all feedback and use it to prioritize our roadmap. I've shared
your input with the product team.

You can track feature requests on our public roadmap: [link]

Thanks for helping us improve!
[Your Name]
```

### 2. Act

```yaml
Decision Tree: Is it reported 10+ times?
  Yes → Add to roadmap
  No → Monitor

  Does it align with strategy?
  Yes → Prioritize
  No → Document why not

  Can we ship in 2 weeks?
  Yes → Quick win, do it
  No → Add to backlog
```

### 3. Notify Users Who Requested It

```markdown
Email Template:

Subject: You asked for [Feature] - it's live!

Hi [Name],

Remember when you asked us to add [feature]? Good news - it's live!

[Screenshot/GIF of feature]

Here's how it works:

1. [Step 1]
2. [Step 2]

Try it now: [Link]

Thanks for the feedback that made this happen.
[Your Name]

P.S. Have more ideas? Reply to this email.
```

### 4. Public Changelog

```markdown
## [Feature] is now live!

Requested by 47 users, [Feature] lets you [benefit].

How it works:

- [Key point 1]
- [Key point 2]

Try it: [Link]
Thanks to everyone who suggested this!
```

## Common Feedback Patterns

### Squeaky Wheel Syndrome

```yaml
Problem: Vocal minority ≠ Real need

Example:
  - 1 user emails daily about dark mode
  - Analytics show 2% use dark mode

Action: Validate with data before building
```

### Silent Churn

```yaml
Problem: Users leave without complaining

Example:
  - Retention drops from 40% to 30%
  - No feedback, no complaints

Action:
  - Proactive exit interviews
  - Check analytics for drop-off points
  - Run usability tests
```

### Feature Bloat Risk

```yaml
Problem: Building everything requested leads to bloat

Example:
  - 'Add Excel export'
  - 'Add CSV export'
  - 'Add JSON export'
  - 'Add PDF export'

Action: Build generic solution, not every variant
```

## Synthesis & Reporting

### Weekly Feedback Summary

```yaml
feedback_summary:
  period: "2024-01-15 to 2024-01-22"
  total_items: 87

  top_themes:
    - theme: "Slack Integration"
      frequency: 23
      severity: high
      example_quotes:
        - "We need Slack notifications"
        - "Can't notify team without Slack"
      recommended_action: "Build Slack integration next sprint"

    - theme: "Slow Dashboard Load"
      frequency: 15
      severity: medium
      example_quotes:
        - "Dashboard takes 10+ seconds"
        - "Performance is terrible"
      recommended_action: "Optimize queries, add caching"

    - theme: "Mobile App Request"
      frequency: 8
      severity: low
      example_quotes:
        - "I want a mobile app"
      recommended_action: "Monitor, not enough demand yet"

  nps:
    score: 42
    detractor_reasons:
      - "Too expensive" (12 mentions)
      - "Missing features" (8 mentions)
      - "Slow performance" (5 mentions)

  prioritized_backlog:
    - feedback: "Add Slack integration"
      score: 80
      priority: high

    - feedback: "Optimize dashboard performance"
      score: 45
      priority: medium

    - feedback: "Mobile app"
      score: 16
      priority: low
```

## Tools & Software

```yaml
Feedback Collection:
  - In-app: Canny, UserVoice, Intercom
  - Surveys: Typeform, SurveyMonkey, Delighted (NPS)
  - User Research: Calendly, Zoom, UserTesting.com

Analysis:
  - Qualitative: Dovetail, Notion, Airtable
  - Quantitative: Excel, Google Sheets, Tableau
  - Sentiment: MonkeyLearn, Lexalytics

Roadmap Transparency:
  - Public Roadmap: Canny, ProductBoard, Trello
  - Changelog: Headway, ReleaseNotes.io, Beamer
```

## Feedback Cadence

```yaml
Daily:
  - Review support tickets
  - Monitor in-app feedback

Weekly:
  - Synthesize themes
  - Share with product team
  - Prioritize top requests

Monthly:
  - Send NPS survey
  - Review feature requests
  - Update public roadmap

Quarterly:
  - User interviews (5-10)
  - Exit surveys for churned users
  - Competitive feedback analysis
```

## Quick Start Checklist

- [ ] Set up in-app feedback widget
- [ ] Schedule NPS survey (monthly)
- [ ] Create feedback tracking spreadsheet
- [ ] Review support tickets weekly
- [ ] Conduct 2-3 user interviews
- [ ] Set up public roadmap (optional)
- [ ] Create email templates for acknowledging feedback
- [ ] Document feedback categorization process

## Common Pitfalls

❌ **Collecting feedback without acting**: Damages trust
❌ **Building everything requested**: Feature bloat
❌ **Not validating with data**: Vocal minority ≠ majority
❌ **Ignoring silent majority**: Not everyone gives feedback
❌ **No follow-up**: Users want to know you listened

## Summary

Great feedback analysis:

- ✅ Multiple channels (surveys, tickets, interviews)
- ✅ Categorize and prioritize systematically
- ✅ Act on high-priority feedback quickly
- ✅ Close the loop (notify users)
- ✅ Balance requests with strategy
- ✅ Share insights with team
