---
name: slack-writing
description: |
  Generates Slack messages in user's authentic voice: direct, concise, data-driven.
  Use when user needs to write, draft, compose, or rewrite Slack messages, DMs, or channel posts.
  Adapts style based on channel type (public vs DM) and message type.
---

# Slack Message Writer Skill

## Purpose
Generate Slack messages in your authentic voice: direct, concise, data-driven, and confidently human. Adapts style based on channel type (public vs DM) and message type (status, decision, concern, etc.).

---

## Voice Profile

### Core Characteristics
- **Direct and concise**: Short punchy sentences. No fluff.
- **Data-driven**: Specific metrics presented in bullet format with context.
- **Confident**: Clear opinions stated directly. Explicit confidence levels when uncertain.
- **Action-oriented**: Every message ends with clear next steps and deadlines.
- **Structured**: Bullets and line breaks for organization.
- **Professional but human**: Occasional emojis for emphasis (✅ 🔴 📈), minimal contractions.

### Style Rules

1. **Short, punchy sentences** - Get to the point fast
2. **No hedging words** - Avoid "maybe", "possibly", "I think perhaps", "it seems like"
3. **Confidence levels for uncertainty** - "Medium confidence here" / "High confidence this works"
4. **Bullet format for data/lists** - Always contextualize metrics
5. **Action-oriented closings** - Include deadlines and owners
6. **Occasional emojis** - ✅ 🔴 📈 for emphasis only
7. **Minimal contractions** - Prefer "it is" over "it's", "we are" over "we're"
8. **Pronoun usage** - "I" for opinions, "we" for team actions
9. **@mentions for urgency** - Not "URGENT:" labels

---

## Channel Type Detection

### Public Channels (team-wide, project channels)
- **Opening**: Use context setter - "Quick update:" / "FYI:" / "Heads up:"
- **Tone**: Same direct style, slightly more structured
- **Example opener**: "Quick update: shipped the landing page redesign yesterday."

### DMs or Small Groups
- **Opening**: Jump straight to content - no prefix needed
- **Tone**: Same direct style
- **Example opener**: "Shipped the landing page redesign yesterday."

### Thread Responses
- **Opening**: Quote or reference original message
- **Pattern**: "You mentioned X - here is my take..." or "On the API decision:"
- **Tone**: Conversational but still direct

---

## Message Type Templates

### 1. Status Update
```
Quick update: [what happened in one line].

[Metrics if applicable:]
• [Metric 1]: [Value] ([context - above/below target])
• [Metric 2]: [Value]

Next steps:
• [Action 1] - [Owner] - [Deadline]
• [Action 2] - [Owner] - [Deadline]
```

**Example:**
```
Quick update: shipped landing page redesign yesterday.

Early metrics:
• Adoption: 15% (below 20% target)
• Page load: 1.2s (within goal)

Next steps:
• @sarah run user interviews by Friday
• @mike pull funnel analytics by EOD Thursday

Will synthesize findings and share action plan Monday.
```

### 2. Asking for Input/Decision
```
Need input on [topic].

Context: [1-2 sentences of essential background]

Options:
• Option 1: [Brief description] - [Trade-off]
• Option 2: [Brief description] - [Trade-off]

[Your position]: Leaning toward [option] because [reason].

@[person] need your call by [deadline].
```

**Example:**
```
Need input on API approach.

Context: Building the integration layer. Two viable paths with different trade-offs.

Options:
• Option 1: REST - faster to ship (2 weeks), creates tech debt
• Option 2: GraphQL - cleaner long-term, delays launch by 2 weeks

My take: Leaning toward Option 1 given our Q1 timeline pressure.

@david need your call by EOD Wednesday.
```

### 3. Raising Concern/Risk
```
Flagging a risk: [one-line summary].

Context: [Why this matters]

Impact: [What happens if not addressed]

Recommendation: [Proposed action]

[Confidence level if uncertain]: Medium confidence this is the right call.
```

**Example:**
```
Flagging a risk: Legal approval timeline is tight.

Context: Current plan assumes 5-day Legal review. Based on past reviews, that is optimistic.

Impact: Can slip launch by 2+ weeks if not addressed now.

Recommendation: Either add 2-week buffer or start Legal review this week.

High confidence this needs attention.
```

### 4. Disagreeing/Alternative View
```
Different take: [your position in one line].

[Why you see it differently - 2-3 sentences max]

Trade-off to consider: [What your approach gains/loses]

Open to discussing if helpful.
```

**Example:**
```
Different take: we should prioritize mobile over desktop.

Usage data shows 65% of our users are on mobile during site visits. Desktop-first means we are optimizing for the minority. The mobile experience is also where we are losing users in the funnel.

Trade-off: Desktop gets delayed by 1 sprint, but we capture the bigger audience first.

Open to discussing if helpful.
```

### 5. Positive Feedback/Celebrating Wins
```
[Impact statement]. Well done.

What this unlocks: [Customer/business value]

[Specific callout if applicable]: @[person] [specific contribution]
```

**Example:**
```
This unlocks real-time collaboration for our largest customer segment. Well done.

What this unlocks: Enterprise teams can now work simultaneously without sync delays.

@lisa your work on the conflict resolution logic made this possible.
```

### 6. Follow-up/Check-in
```
Checking in on [topic].

Last status: [What was agreed/expected]

Need by: [Deadline]

Let me know if anything is blocking progress.
```

**Example:**
```
Checking in on the API documentation.

Last status: Draft was due yesterday per our sync.

Need by: Friday to unblock partner integration testing.

Let me know if anything is blocking progress.
```

### 7. Announcement
```
FYI: [What is happening in one line].

Key details:
• [Detail 1]
• [Detail 2]
• [Detail 3]

What this means for you: [Specific impact/action needed]

Questions? Thread here or DM me.
```

**Example:**
```
FYI: Launching the new dashboard to all users next Monday.

Key details:
• Rollout: 10% Monday, 50% Wednesday, 100% Friday
• Training: Self-serve guide in Help Center
• Support: #dashboard-questions for issues

What this means for you: Review the guide before Monday. Flag concerns by Friday.

Questions? Thread here or DM me.
```

---

## Thread Response Patterns

### Agreeing and Adding
```
+1 on this. Adding: [your contribution]
```

### Providing Requested Input
```
You asked about [topic]. Here is my take:

[Your input in bullet format if multiple points]
```

### Clarifying a Question
```
On your question about [topic]:

[Direct answer]

[Context if needed - 1 sentence max]
```

---

## Anti-Patterns to Avoid

- ❌ **Hedge words**: "I think maybe we could possibly consider..."
- ❌ **Over-explaining**: Long paragraphs of context before the point
- ❌ **Burying the ask**: Action item hidden at the end
- ❌ **Vague deadlines**: "soon" / "when you get a chance" / "ASAP"
- ❌ **Excessive emojis**: 🎉🚀💪🔥 everywhere
- ❌ **URGENT labels**: Use @mentions instead
- ❌ **Multiple unrelated topics**: One message, one topic
- ❌ **Passive voice**: "It was decided that..." instead of "We decided..."
- ❌ **Unnecessary greetings**: "Hey! Hope you are having a great day!"

---

## Quality Checklist

Before sending, verify:
- [ ] Point is clear in first line
- [ ] Action/ask is explicit with owner and deadline
- [ ] Data has context (vs target, vs last period, etc.)
- [ ] No hedge words or passive voice
- [ ] Length is appropriate (shorter is better)
- [ ] Emojis used sparingly for emphasis only
- [ ] Would a PM leader approve this level of clarity?

---

## Confidence Level Expressions

Use these when uncertain:

- **High confidence**: "High confidence this is the right call."
- **Medium confidence**: "Medium confidence here. Worth validating with [person/data]."
- **Low confidence**: "Low confidence - flagging for discussion, not recommending action yet."

---

## Organizational Context

For product-specific context (product name, key terms, stakeholders), see `CLAUDE.local.md`.

When drafting Slack messages:
- **Stakeholders**: Reference `Reference/corporate-strategy/` for org context
- **Initiatives**: Reference `Initiatives/*/CLAUDE.md` for project context
- **Colleagues**: Reference `Reference/colleagues.json` for name verification