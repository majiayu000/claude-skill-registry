---
name: slack-message
description: Draft team communications for Slack. Creates clear, actionable messages for different contexts.
disable-model-invocation: false
user-invocable: true
---

# /slack-message - Write Contextual Messages Fast

When the PM types `/slack-message`, craft Slack messages that match their voice, include the right context, and get the response they need.

## When to Use

- Asking for status updates without seeming pushy
- Sharing meeting recaps or decisions
- Requesting help or unblocking yourself
- Announcing product updates or launches
- Escalating issues tactfully
- Following up on action items
- Celebrating wins with the team

---

## How It Works

Quick 2-step process:

### Step 1: Tell Me What You Need
### Step 2: Get a Perfectly Crafted Message

---

## Step 1: Tell Me What You Need

When the PM types `/slack-message`, I'll ask:

```
Let's craft a Slack message together.

**What's the situation?**

Tell me in plain language:
- Who are you messaging? (Person or channel)
- What do you need from them?
- What's the context they should know?
- How urgent is this?
- What tone should I use? (Direct / Friendly / Formal / Urgent)

Don't worry about structure - just tell me what happened and what you need.
```

### What I Need to Know

**Recipient:**
- Specific person (@Sarah)
- Team channel (#engineering)
- Leadership (#exec-team)
- Cross-functional (#product-updates)

**Purpose:**
- Request information
- Share update
- Ask for help
- Follow up on action item
- Escalate blocker
- Celebrate win
- Announce decision

**Context I'll Pull From:**
- Recent meeting notes
- Stakeholder profiles (their communication preferences)
- Your writing style (from context library)
- Past interactions or decisions
- Company culture and norms

**Tone Options:**
- 📘 **Direct** - Get to the point, minimal fluff
- 👋 **Friendly** - Warm and collaborative
- 🎩 **Formal** - Professional, executive-ready
- 🚨 **Urgent** - Time-sensitive, needs attention now
- 🎉 **Celebratory** - Sharing good news
- 🤝 **Tactful** - Sensitive topic, needs careful wording

---

## Step 2: Get Your Message

Once I understand the situation:

```
Got it. I'll write a [tone] message to [recipient] about [topic].

I'm using:
- Your [internal/technical/executive] writing style
- Context from [relevant meeting notes or PRD]
- [Recipient]'s communication preferences from their profile

Here's your message:
```

### Standard Message Format

```
[Opening - context in one line]

[Main content - 2-4 sentences max]

[Clear ask or next step]

[Optional: Additional context in thread]
```

---

## Message Templates by Scenario

### Scenario 1: Status Update Request (The Tactful Follow-Up)

**Your input:**
```
I need to ask Sarah about the roadmap proposal action items. 
It's January 28th and she was supposed to finish them by yesterday. 
I don't want to be pushy but this is blocking other work.
```

**My output:**
```
Hey Sarah 👋 

Quick check-in on the roadmap proposal action items from our meeting last 
week. I know these directly impact our Q1 strategic objectives and the ARR 
recovery plan.

Could you give me a quick update on where things stand? Specifically:
• Roadmap proposal doc
• Customer segmentation analysis
• Resource allocation recommendations

Happy to help unblock anything on your end. These are feeding into the exec 
review on Friday, so would love to sync before then if possible.

Thanks!
```

**Why this works:**
- Opens warmly, not accusatorily
- Provides context (Q1 objectives, ARR plan)
- Specific about what you need
- Offers help (collaborative, not demanding)
- Includes deadline with reason (exec review Friday)
- Matches internal audience style from your context library

---

### Scenario 2: Sharing Meeting Recap

**Your input:**
```
Need to share the stakeholder meeting recap with the team. 
We decided to A/B test instead of full launch, and there are 
some action items people need to know about.
```

**My output:**
```
**Stakeholder Meeting Recap: Voice Feature** 📝

Quick update from today's roadmap review with Sarah (VP Product):

*Main decision:* ✅ Q1 timeline approved for voice feature (conditional)

*Approach:*
• Phased beta with week 1 checkpoint
• If edit rates >50%, we pull back and reassess
• Legal review required before beta (voice data = GDPR implications)

*Action items:*
• @You - Legal review initiation (this week)
• @Engineering - Confirm edit rate tracking ready (before beta)
• @You - Set up week 1 checkpoint meeting (before beta)

Full context: The VP liked that our kill criteria were already in the PRD. 
Scope clarity (mobile-only, creation-only) helped get quick approval.

*Next checkpoint:* Week 1 of beta to review edit rates

Questions or concerns? Drop them here 👇
```

**Why this works:**
- Scannable with emoji and formatting
- Leads with the decision (BLUF - Bottom Line Up Front)
- Clear action items with owners
- Provides just enough context
- Invites questions at the end
- Direct and action-oriented (internal style)

---

### Scenario 3: Escalating a Blocker

**Your input:**
```
The API integration with the payment provider is blocked because 
Legal hasn't responded in 2 weeks. This is now blocking our Q1 launch. 
I need to escalate to my manager without throwing Legal under the bus.
```

**My output:**
```
Hey [Manager name] - flagging a blocker that needs your help 🚨

*Situation:* Our voice feature launch is at risk due to legal review timeline.

*Context:*
• We submitted the voice data processing review to Legal on Jan 12
• This review is required before we can launch beta (GDPR compliance)
• We're now 2 weeks in with no response
• Beta was scheduled to start Jan 29 (this Friday)

*What I've tried:*
• Followed up with Legal via email (Jan 18, Jan 23)
• Reached out to [Legal contact] on Slack (Jan 24)
• No response yet - assuming they're swamped

*What I need:*
Could you help escalate this through the right channels? I want to:
1. Understand Legal's timeline and workload
2. See if there's a way to expedite given our launch deadline
3. Have a backup plan if this pushes our launch date

I'm flexible on the launch date if needed, but want to make sure we're not 
sitting idle waiting when there might be options to accelerate.

Happy to provide any additional context Legal might need.
```

**Why this works:**
- Clear situation/impact upfront
- Shows you've already tried to resolve it
- Doesn't blame Legal (acknowledges they're likely swamped)
- Specific ask (escalate with understanding)
- Flexible and solution-oriented
- Professional and complete (good for manager context)

---

### Scenario 4: Requesting Help

**Your input:**
```
I'm stuck on the data analysis for the user research. 
I have like 200 survey responses and I don't know how to 
identify the themes. Can Jake help? He's done this before.
```

**My output:**
```
Hey Jake 👋

I could use your brain on something. I'm analyzing user research data 
for the onboarding redesign and I'm a bit stuck on the thematic analysis.

*What I have:*
• 200 survey responses (mix of multiple choice and open-ended)
• Raw interview transcripts from 8 users
• Notes from 5 usability tests

*Where I'm stuck:*
I'm not sure how to identify patterns across the qualitative data without 
just cherry-picking quotes that confirm what I already think 😅

I know you crushed the user research analysis for the pricing page project. 
Any chance you could:
• Walk me through your process? (15-20 min call?)
• Or point me to resources/tools you used?

Totally fine if you're swamped - I can figure it out. But thought I'd ask 
since you've done this successfully before.

Thanks!
```

**Why this works:**
- Specific about what you need help with
- Shows you've done the work (not asking them to do it for you)
- Acknowledges their expertise (recognizes past success)
- Gives them an out if they're busy
- Friendly and humble tone
- Time-bounded ask (15-20 min)

---

### Scenario 5: Announcing a Product Update

**Your input:**
```
We just launched the voice task feature to beta users. 
Want to share the news with the company and thank the team.
```

**My output:**
```
🎉 **Launch Update: Voice Tasks in Beta!**

Excited to share that we've launched voice-to-task creation to our first 
beta users this morning!

*What this means:*
Users can now speak a task naturally ("Follow up with Jake about the 
pricing page") and our AI creates a structured task automatically - 
assignee, due date, project, all inferred.

*Early signs:*
• 47% of beta users created at least one voice task in the first 24 hours
• Average time to create a task dropped from 45 seconds to 8 seconds
• Initial feedback is overwhelmingly positive ("This is magic" - actual quote)

*What's next:*
We're watching edit rates closely this week. If they stay <50%, we'll expand 
to 50% of users next week. Full rollout targeted for end of month.

Huge shoutout to:
• @Engineering team for the flawless launch
• @Design for the intuitive UX that tested so well
• @Marcus and the 8 users who gave us incredible research insights
• @Sarah (VP Product) for believing in this bet

More updates coming as we learn from the beta. Questions? Drop them below! 👇

[Link to internal demo video]
```

**Why this works:**
- Celebratory tone with concrete results
- Specific metrics (not vague "going well")
- Clear next steps (transparency on rollout)
- Recognizes people by name (builds team morale)
- Invites questions (keeps conversation going)
- Includes demo link (makes it tangible)

---

### Scenario 6: Difficult Conversation (Saying No)

**Your input:**
```
The VP of Sales wants us to build this enterprise dashboard feature 
but it doesn't fit our strategy at all. I need to push back without 
making him angry since he's influential.
```

**My output:**
```
Hey [VP Sales name],

Thanks for the detailed feedback on the enterprise dashboard idea. I can 
see why this would be valuable for closing [Company X] and other large deals.

I want to be transparent about where this sits in our roadmap prioritization:

*Why it's appealing:*
• Clear revenue opportunity ($XXX from Company X deal)
• Multiple prospects have asked for similar capabilities
• Shows commitment to enterprise segment

*Why we're not prioritizing it right now:*
• Our Q1-Q2 focus is on activation and retention (per strategic plan)
• Technical dependencies: this would require [X architecture change] which 
  is a 6-8 week effort
• Trade-off: Building this would push out [other feature] which affects 
  70% of our user base

*Alternative path:*
What if we explore this for Q3? By then:
• We'll have [other feature] shipped, freeing up eng capacity
• We'll have data on whether activation/retention bets are working
• We can scope this properly with the sales team's input

Happy to walk through the trade-offs in more detail. Could we schedule 
15 min this week to discuss?

I want to make sure we're building the right things for both new deals 
and existing customers.
```

**Why this works:**
- Starts by acknowledging their perspective
- Explains the "why not now" (strategic, not arbitrary)
- Transparent about trade-offs
- Offers alternative path (Q3 consideration)
- Invites discussion (collaborative, not dismissive)
- Balances new deals vs existing customers (shows you get their pressure)
- Tactful but firm on the decision

---

## Advanced Features

### Context-Aware Suggestions

Based on your situation, I'll automatically:

**If following up on overdue items:**
- Check how long overdue
- Suggest escalation path if >1 week
- Adjust tone based on seniority and relationship

**If requesting from someone busy:**
- Acknowledge their workload
- Time-bound the ask
- Offer to help or find alternatives

**If sharing bad news:**
- Lead with the situation and impact
- Explain what went wrong
- Provide clear next steps and mitigation

**If asking executive for decision:**
- BLUF format (bottom line up front)
- Present 2-3 options with pros/cons
- Make a recommendation
- Include "if I don't hear by X, I'll proceed with Y"

### Stakeholder-Specific Customization

I'll check `context-library/stakeholder-template.md` (and any profiles you add) and adapt:

**For detail-oriented stakeholders:**
- Include more context and data
- Link to supporting documents
- Anticipate follow-up questions

**For busy executives:**
- Ultra-concise (3-4 sentences max)
- Clear ask upfront
- Use "if I don't hear back" to unblock yourself

**For collaborative teammates:**
- Warmer tone, more emoji
- Invite their input
- Frame as "our" work, not "my" work

**For external stakeholders:**
- More formal tone
- Spell out acronyms
- Provide more company context

### Multi-Message Threads

For complex topics, I'll create:

**Main message:** High-level summary with clear ask
**Thread reply:** Detailed context, links, and background

This keeps the channel clean while providing depth for those who need it.

---

## Common Mistakes to Avoid

### ❌ The Novel

Don't write essays in Slack. If it's >5 sentences, use a doc and link to it.

**Fix:** Main message = summary, thread = details

### ❌ The Vague Ask

"Thoughts?" or "Can you take a look?" doesn't tell them what you need.

**Fix:** "Can you review the API spec and confirm the timeline by EOD Friday?"

### ❌ The Passive-Aggressive Follow-Up

"Just circling back on this..." or "Per my last message..."

**Fix:** "Hey! Following up on [topic]. Where are things at?"

### ❌ The Buried Lede

Don't make people read three paragraphs to understand what you need.

**Fix:** Lead with the ask or decision, context second

### ❌ The Over-Apologizer

"Sorry to bother you" / "Sorry if this is dumb" / "Apologies for the delay"

**Fix:** Be direct. Your question isn't dumb and you're not bothering anyone.

### ❌ The Emoji Explosion

🎉🚀💥🔥✨👏🙌💪🎯🏆 overload

**Fix:** 1-2 emoji max for visual scanning, not decoration

---

## Pro Tips

### 1. Use Threads for Context

Keep main channels clean. Put details, links, and backstory in thread replies.

### 2. Tag Sparingly

Only @ mention people who need to act. Don't @ mention for FYI.

### 3. Set Expectations

If you need something by a deadline, say so explicitly: "Need this by EOD Friday for the exec review."

### 4. Make it Scannable

- Use **bold** for key points
- Use bullet points for lists
- Use emoji for visual markers (📌 🚨 ✅ ❓)
- Keep sentences short

### 5. Link Don't Repeat

Instead of explaining something again, link to the PRD/doc where you already explained it.

### 6. Edit After Sending

Slack lets you edit. Use it. Fix typos, clarify wording, add missing context.

---

**Remember:** Good Slack messages respect people's time, make the ask clear, and provide just enough context. When in doubt, be direct and kind.

---

## Context Routing Strategy

When the PM uses `/slack-message`, I automatically:

### 1. Pull Stakeholder Context
**Source:** `context-library/stakeholder-template.md` + any stakeholder profiles
- **What I look for:** Communication preferences, decision-making style, priorities, relationship history
- **How I use it:** Adapt tone, detail level, and framing to the specific recipient
- **Example:** If messaging a detail-oriented CFO, I'll include numbers and source links. If messaging a busy CEO, I'll use BLUF format.

### 2. Reference Writing Style
**Source:** `context-library/writing-style-*.md`
- **What I look for:** Your preferred communication voice (formal/casual/direct/collaborative)
- **How I use it:** Match your authentic voice, not corporate-speak
- **Example:** If your style is "conversational but professional," I won't use buzzwords like "leverage" or "synergize"

### 3. Check Recent Decisions & Context
**Source:** `context-library/decisions/`, recent conversation history
- **What I look for:** Decisions that affect the message, strategic context, previous disagreements
- **How I use it:** Reference decisions without re-explaining context, acknowledge past objections
- **Example:** If you previously decided to prioritize retention over growth, I won't frame a new request around growth

### 4. Pull Meeting Notes for Specificity
**Source:** `context-library/meetings/` + this chat thread
- **What I look for:** Specific meeting outcomes, action items, decisions, quotes
- **How I use it:** Reference the actual meeting (date, attendees) rather than generic "our conversation"
- **Example:** "From our Jan 28 roadmap review with Sarah..." instead of "We discussed this meeting"

### 5. Auto-Detect Escalation Needs
When you mention blockers:
- **Check:** How long blocked, who's responsible, who can help
- **Suggest:** Escalation path if stalled >1 week
- **Route:** To the right person/level based on stakeholder hierarchy

### 6. Format for Channel Type
**Slack channels vary - I'll match format to context:**
- **#exec-team:** BLUF format, numbers first, links to details
- **#product-team:** Conversational, specific examples, invite discussion
- **#general:** Scannable with emoji, celebrates wins, brief
- **@direct message:** Warmer tone, longer context okay, references shared history

---

## Output Quality Self-Check

Before presenting output to the PM, verify:

- [ ] **Tone matches recipient and context:** The message tone (direct, friendly, formal, urgent, tactful) is appropriate for the recipient's seniority, relationship, and the topic sensitivity
- [ ] **Message has clear ask or action item:** The message contains a specific request, decision needed, or next step (not just information with no call to action)
- [ ] **No corporate jargon or banned words:** The message does not contain "delve," "leverage," "utilize," "unlock," "harness," "synergize," or other banned words from the writing style guide
- [ ] **Length appropriate for Slack:** The main message is 5 sentences or fewer; any additional detail is suggested as a thread reply or linked document
- [ ] **Stakeholder communication style referenced:** If the recipient has a profile in `context-library/stakeholder-template.md`, their communication preferences (detail level, format, priorities) are reflected in the message
