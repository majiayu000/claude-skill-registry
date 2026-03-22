---
name: weekly
description: Friday weekly reflection for PM Extreme Ownership. Pre-fills the three mindset questions (customer value, friction removed, customer story) with real data from your issue tracker, support platform, Slack, call recordings, and the friction log. Output is formatted for the 1:1 doc with [your manager].
---

# PM Weekly Reflection — Extreme Ownership

You are generating a weekly reflection for a PM operating with Extreme Ownership. This pre-fills the three core questions with real data so the PM can add narrative and paste into their 1:1 doc.

ultrathink

## Data Gathering

Run all of the following in parallel:

### 1. Issue Tracker: What I completed this week
Use issue tracker MCP tools to list issues assigned to "me" that were completed (status: Done) in the past 7 days. Also find issues I moved from Triage to In Progress this week (I unblocked them). Note: ID, title, customer, what was done.

### 2. Issue Tracker: What I'm actively working on
List my issues currently In Progress or In Review. Note: ID, title, customer, status.

### 3. Issue Tracker: New requests I picked up
List issues assigned to me that were created in the past 7 days. Note: ID, title, customer, who created it.

### 4. Support Tickets: Trends
Use Glean search with your support platform to find:
- Tickets mentioning [your product area keywords] created in the past 7 days (this week's new tickets)
- Tickets mentioning [your product area keywords] created between 7-14 days ago (last week, for comparison)
- Any tickets with SLA breach labels
- Note patterns: which customers, which categories, repeat issues

### 5. Slack: Customer signals and stories
Use Glean search with `app: slack` in channels [your-product-channel] for messages from the past 7 days. Look for:
- Customer success stories or positive signals
- Direct customer quotes that could be the "anecdote backed by data"
- Escalations that were resolved
- New customer enablements or activations

### 6. Call Recordings: Customer conversations
Use Glean search with `app: gong` (or your recording tool) for calls from the past 7 days mentioning [your product area keywords]. Look for:
- Customer quotes about value they're getting
- Pain points or feature requests mentioned on calls
- Any notable sentiment shifts

### 7. Friction log
Read all files in the `friction/active/` and `friction/dissolved/` directories in this project. Identify:
- Friction entries dissolved this week
- Active friction entries and their current status

### 8. Weekly Action Tracker
Read the current week's action file at `actions/week-YYYY-MM-DD.md` (Monday of this week). Use it to:
- Count completed vs open action items (checked vs unchecked)
- Pull "Other Actions" logged throughout the week as evidence of work done
- Identify patterns (e.g., "5 of 8 actions were onboarding-related")
- Feed completed items into the "Building" and "Customer Engagements" sections

## Output Format

Generate output in this exact format (ready to paste into the 1:1 doc):

```markdown
## Week of [DATE]

### Thoughts and Learnings
<!-- Fill this in — but here are prompts based on this week's data: -->
- Consider: [insight from the week's patterns]
- Consider: [another pattern or learning]

### Building
[For each completed issue:]
- [completed] [Title] ([Issue ID](url)) — [one-line impact]
[For each in-progress item:]
- [in progress] [Title] ([Issue ID](url)) — [current status]

### Customer Engagements
[For each customer interaction found in call recordings/Slack/support:]
- [Customer name]: [what happened, what value was delivered or what's next] ([source](url))

---

### Extreme Ownership Scorecard

**1. What customer value did we create this week?**
_Not activities — numbers. Link each item to its source._
- [X] customer issues resolved ([Issue ID](url), [Issue ID](url), ...)
- [Y] customers unblocked
- [List specific outcomes with metrics where possible, linking to sources]

**2. What friction did we remove?**
_For the customer, not internally._
[List dissolved friction entries with how they were dissolved]
[If no friction was dissolved: "No friction dissolved this week — what's stuck?"]

**3. What's one customer story we can tell?**
_An anecdote backed by data._
[Best customer quote or story from call recordings/Slack, paired with a metric]
[If no strong story found: "No clear story this week — dig into [suggestion]"]

### Support Ticket Trends
- New tickets this week: [X] (vs [Y] last week)
- Top categories: [list top 3 patterns, linking to example tickets e.g. [#NNNNN](ticket-url)]
- SLA breaches: [count and customers, linking to each breached ticket]
- Repeat issues: [any pattern that keeps showing up, with links]
- Action: [what to do about the trends — docs to write, bugs to file, etc.]

### Adoption Gap
- [If adoption data is available, pull tenant/user counts]
- [Otherwise note: "Pull adoption metrics to fill this in"]
```

## Critical Rules

1. **Numbers, not activities.** Don't say "worked on X." Say "resolved X for [customer], unblocking [outcome]."
2. **Link EVERYTHING.** Every reference to a source must be a clickable link — issues, support tickets, Slack threads, call recordings, email threads. Use markdown link syntax `[display text](url)`. This applies to ALL sections, not just Building. Customer Engagements should link to the call or Slack thread. Support Ticket Trends should link to specific tickets. The customer story should link to its source. If a URL was returned by a tool, use it.
3. **Be honest about gaps.** If a section has no data, flag it rather than filling with fluff.
4. **Support ticket trends are mandatory.** This is how we spot systemic friction before it becomes a fire.
5. **The customer story section should be the strongest part.** Search hard for it — check call recordings first, then Slack, then support ticket resolutions.
