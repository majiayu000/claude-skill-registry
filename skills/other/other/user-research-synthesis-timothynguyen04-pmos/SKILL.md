---
name: user-research-synthesis
description: Turn user interviews into actionable insights. Advanced synthesis techniques and frameworks.
disable-model-invocation: false
user-invocable: true
---

# /user-research-synthesis - Turn Interview Data Into Insights

When the PM types `/user-research-synthesis`, transform raw user interview notes, transcripts, and observations into actionable product insights.

## Context Routing Logic (Internal - for Claude)

**Automatic Context Checks:**
When this skill is invoked, immediately check:

| Source | Files/Folders | Search Terms | What to Extract |
|--------|---------------|--------------|-----------------|
| Existing Research | `context-library/research/*.md` | topic from chat, user segments | Previous findings to avoid duplication |
| Related PRDs | `context-library/prds/*.md` | problem related to interviews | Problem framing and hypothesis |
| Strategy Context | `context-library/strategy/*.md` | user segment, strategic fit | How findings ladder to strategy |
| Previous Synthesis | `outputs/research-synthesis/` | topic name | Past research to build on |
| Interview Guides | `context-library/research/interview-guides/` | topic | What questions were asked |

**Context Priority:**
1. Raw interview data FIRST (always use verbatim quotes)
2. Related PRDs and problem statements SECOND
3. Previous research on related topics THIRD
4. Strategic context FOURTH

**Cross-Skill Links:**
- After synthesis → Link to `/prd-draft` to turn insights into feature spec
- If about competitor mentions → Link to `/competitor-analysis`
- If about retention → Link to `/retention-analysis` for churn patterns
- If informing strategy → Link to `/write-prod-strategy`

---

## Step 0: Understanding Your Research Context

Before we synthesize, let me understand what you've learned...

**Checking:**
- `context-library/research/` for previous findings on this topic
- `context-library/prds/` for the problem statement
- Interview guides used: what were you trying to validate?
- Previous synthesis on related topics

**Based on what I find, I'll show you:**

### What You Were Researching

**Topic:**
- [What problem or feature were you exploring?]
- [Your original hypothesis: what did you expect to find?]

**Sample:**
- [Who did you interview? # of participants, roles, segments]
- [Notable characteristics: power users? churn risk? non-users?]

**Context from Previous Research:**
- [What do we already know about this problem?]
- [What did you expect research to confirm/disprove?]

### PM-Specific Diagnosis Questions

1. **Research Quality:** Are these high-quality interviews with right users, or preliminary conversations?
2. **Saturation:** How many interviews did you do? (5-8 = good, 3-4 = preliminary, 10+ = very deep)
3. **Bias Risk:** Are you interviewing customers who love you, or a balanced sample?
4. **Surprise Factor:** What surprised you? (Best insights often contradict expectations)
5. **Action Threshold:** Do you have enough evidence to make decisions, or need more research?

---

## When to Use

- After completing 5-8 user interviews
- Processing customer feedback from multiple sources
- Synthesizing usability test results
- Analyzing support tickets or sales call notes
- Converting qualitative data into product decisions

---

## How It Works

This is a 4-step process:

### Step 1: Upload Your Raw Data
### Step 2: Extract Key Observations  
### Step 3: Cluster Into Themes (Affinity Mapping)
### Step 4: Generate Actionable Recommendations

---

## Step 1: Upload Your Raw Data

When the PM types `/user-research-synthesis`, start with:

```
Let's turn your user research into actionable insights.

**What data do you have?**

Upload or paste any combination of:
- Interview transcripts (from Grain, Otter.ai, or manual notes)
- Usability test recordings or notes
- Customer support tickets
- Sales call summaries
- Survey responses (open-ended)
- Slack messages from customer channels

You can upload multiple files or just paste everything into this chat.

**How many interviews/data points?**
[Let me know so I can gauge the scope]

**What were you trying to learn?**
(e.g., "Why users churn after the first week" or "Pain points in the onboarding flow")
```

### What to Look For in the Data

As you upload, I'll automatically start flagging:
- **Direct quotes** - Verbatim user language (the most powerful stuff)
- **Behavioral patterns** - What users actually did (not what they said they'd do)
- **Pain points** - Explicit frustrations or workarounds
- **Jobs to be done** - What users are trying to accomplish
- **Unexpected use cases** - How they're using the product in ways you didn't anticipate
- **Emotion signals** - Moments of frustration, delight, confusion

---

## Step 2: Extract Key Observations

Once I have your data, I'll say:

```
Great, I've reviewed [X] interviews/data points.

I'm going to extract individual observations - each one gets its own "sticky note."

This will take a few minutes. I'll create:
- User quotes (in their exact words)
- Observed behaviors (what they actually did)
- Pain points (explicit problems they mentioned)
- Workarounds (clever hacks they've built)
- Context (their role, goals, environment)

Processing now...
```

### Output Format

I'll create a structured list like this:

```markdown
## Observation #1
**Type:** Pain Point  
**User:** Marcus (PM, Spotify)  
**Quote:** "I have 47 voice memos on my phone that are just 'remember to follow up with design about X.' I never convert them."  
**Context:** Uses multiple task managers, frustrated with manual entry  
**Emotion:** Frustration (high)

## Observation #2
**Type:** Behavior  
**User:** Priya (PM, Notion)  
**Quote:** "Half my tasks come from casual hallway conversations."  
**Behavior:** Captures ideas verbally but loses them before writing down  
**Context:** Fast-paced startup environment

[... continues for all observations]
```

### Quality Checks

As I extract, I'll flag:
- ⚠️ **Vague statements** - "Users want a better experience" (not actionable)
- ⚠️ **Future predictions** - "I would definitely use this" (unreliable)
- ⚠️ **Leading question responses** - If I detect the interviewer asked a leading question
- ✅ **High-quality signals** - Specific stories, concrete examples, strong emotion

---

## Step 3: Cluster Into Themes (Affinity Mapping)

After extraction, I'll say:

```
I've extracted [X] observations from your data.

Now I'm going to group these into themes using affinity mapping.

I'll look for:
- Patterns that appear across multiple users
- Contradictions (where users disagree)
- Underlying needs beneath surface-level requests
- Jobs-to-be-done that aren't being solved

Clustering now...
```

### The Clustering Process

I'll create theme clusters like this:

```markdown
## Theme 1: "Task Capture Friction"
**Frequency:** 6 out of 8 users mentioned this  
**Severity:** High (blocks daily workflow)

**Key Observations:**
- [Observation #1: Marcus voice memos]
- [Observation #2: Priya hallway conversations]
- [Observation #5: Jake loses tasks from Slack]
- [Observation #12: Sarah Excel spreadsheet workaround]

**Pattern:**
Users capture tasks in the moment (voice, text, conversation) but face friction converting them into their task manager. The "structuring" step is the bottleneck.

**Direct Quotes:**
- "I never convert them." - Marcus
- "Then 3 days later I'm like... wait, what API thing?" - Priya

**Jobs-to-be-done:**
When I have a spontaneous task idea, I want to capture it instantly without thinking about structure, so that I don't lose track of commitments.

---

## Theme 2: "Context Loss Between Tools"
**Frequency:** 5 out of 8 users  
**Severity:** Medium

[... continues for each theme]
```

### Handling Contradictions

When users disagree, I'll explicitly call it out:

```markdown
## 🔴 Contradiction Detected: "Manual Control vs Automation"

**User Group A (3 users):** Want AI to automatically assign tasks
- "Just figure out who it should go to" - Jake
- "I don't want to think about it" - Maria

**User Group B (5 users):** Want full manual control
- "AI might get this wrong" - Priya
- "I need to decide priority myself" - Marcus

**Recommendation:**
Default to manual with an "AI suggestion" that users can accept/reject. This preserves control while reducing friction.
```

---

## Step 4: Generate Actionable Recommendations

After clustering, I'll create your final output:

```
I've identified [X] major themes from your research.

Now I'll translate these into actionable recommendations with:
- What to build (prioritized)
- What NOT to build (non-goals)
- Open questions (what you still need to learn)
- Success metrics (how to measure if you solved the problem)

Generating recommendations...
```

### Recommendation Format

```markdown
# User Research Synthesis: [Topic]
**Date:** [Today's date]  
**Interviews:** [X participants]  
**Synthesized by:** [PM name]

---

## Executive Summary

**Top 3 Insights:**
1. [Insight with impact]
2. [Insight with impact]
3. [Insight with impact]

**Recommended Actions:**
1. [Build this first]
2. [Explore this next]
3. [Deprioritize this]

---

## Theme 1: [Theme Name]
**User Impact:** [% of users affected]  
**Severity:** [High/Medium/Low]  
**Current Workaround:** [How users solve this today]

### The Problem
[Describe the core issue in user language]

### Supporting Evidence
- **Direct Quote:** "[Exact user words]" - [User name]
- **Observed Behavior:** [What you saw them do]
- **Frequency:** [X out of Y users mentioned this]

### Recommended Solution
**Build:** [Specific feature/change]

**Why this solution:**
- Addresses the root cause: [explain]
- Fits into existing workflow: [explain]
- Validated by user behavior: [explain]

**What NOT to build:**
- [Alternative you considered but rejected]
- [Why it won't work]

**Success Metrics:**
- Primary: [How you'll measure success]
- Guardrail: [Metric that can't get worse]

**Open Questions:**
- [ ] [What you still need to validate] - @[who to ask]
- [ ] [Edge case to test]

---

[Repeat for each theme]

---

## Themes We're NOT Addressing (And Why)

### Theme X: [Lower priority theme]
**Why we're not prioritizing:**
- Only 2 out of 8 users mentioned it
- Workarounds exist and aren't too painful
- Doesn't align with our Q2 strategy

---

## Contradictions & Open Questions

[List any conflicts in the data]
[List assumptions that need more validation]

---

## Appendix: Raw Observations

[All extracted observations for reference]
```

---

## Advanced Techniques

### The Mom Test Check

As I analyze, I'll flag any data that might be unreliable:

❌ **Future predictions:** "I would definitely use this"
❌ **Hypotheticals:** "If you built X, I would Y"
❌ **Compliments:** "This is great!" (without specifics)
❌ **Feature requests:** "You should add Z" (without context)

✅ **Past behaviors:** "Last time I tried to do X, I had to Y"
✅ **Specific stories:** "Here's exactly what happened..."
✅ **Observed patterns:** "Every single time I do this..."
✅ **Workarounds:** "Here's my hack for this problem"

### Advanced Interview Question Patterns

**From Aakash Gupta's Customer Interview Framework:**

**1. The Time Machine Question**
- **Ask:** "Walk me through the last time you [did this task]. What happened first, then what?"
- **Why:** Gets specific, grounded stories instead of generalized opinions
- **Example:** "Walk me through the last time you tried to book a meeting with your team"

**2. The Money Question**
- **Ask:** "Have you paid for a solution to this problem? What did you buy?"
- **Why:** Actual purchasing behavior reveals true pain severity
- **Red flag:** If they haven't spent money/time, the pain might not be real

**3. The Workaround Deep-Dive**
- **Ask:** "Show me how you're solving this today. Can you share your screen?"
- **Why:** Existing workarounds reveal the real job-to-be-done
- **Look for:** Complex Excel sheets, manual processes, duct-taped integrations

**4. The Switching Cost Question**
- **Ask:** "What would it take for you to stop using [current solution] and switch to something new?"
- **Why:** Reveals switching barriers and minimum viable features
- **Red flag:** "Oh I'd switch immediately!" = probably won't

**5. The Budget Authority Question**
- **Ask:** "If you wanted to buy a solution tomorrow, what's your process? Who needs to approve?"
- **Why:** Identifies if you're talking to the decision-maker
- **Critical for B2B:** Understanding org structure and buying process

**6. The Failure Story**
- **Ask:** "Tell me about a time this went wrong. What broke? What did you do?"
- **Why:** Failure moments reveal pain intensity and consequences
- **Example:** "When was the last time you missed a deadline because of this issue?"

**7. The Champion Question**
- **Ask:** "Who else at your company has this problem? Can you introduce me?"
- **Why:** Tests if problem is widespread, gets referrals
- **Red flag:** "Just me, I think" = niche problem

**8. The Recent Purchase Question**
- **Ask:** "What other tools/products have you bought in the last 6 months? What made you buy?"
- **Why:** Reveals buying patterns and decision criteria
- **Look for:** Procurement process, evaluation criteria, deal-breakers

### Five Whys Technique

**When users give surface-level answers, dig deeper:**

```
User: "I want better search"
You: "Why do you need better search?"
User: "I can't find my old tasks"
You: "Why do you need to find old tasks?"
User: "Because I reference them for new projects"
You: "Why do you reference old tasks?"
User: "Because I repeat similar patterns"
You: "Why don't you have templates?"
User: "I DO have templates, but they're scattered across 3 tools"

→ Real problem: Template organization, not search
```

**Apply this during synthesis - I'll automatically run "5 Whys" on pain points to find root causes.**

### The Silent Segments Framework

**Who you DIDN'T talk to matters as much as who you did.**

After interviews, I'll create a "Missing Voices" section:

```markdown
## 🚨 Missing Segments (Research Gaps)

**Who we talked to:**
- 8 enterprise PMs (large companies, >1000 employees)
- All technical backgrounds
- All English-speaking, US-based

**Who we DIDN'T talk to:**
- Small company PMs (<100 employees)
- Non-technical PMs (marketing, ops)
- International users (Asia, Europe, LatAm)
- Free tier users (only talked to paid)

**Risks:**
- Our insights may not apply to SMB market
- May miss non-technical user pain points
- International workflows might differ significantly
- Free users might have different needs

**Recommendation:**
- Next round: 5 interviews with SMB PMs
- Test prototypes with non-technical users
- Consider international user research
```

**This prevents building for a narrow segment while claiming broad applicability.**

### Sentiment Analysis

For each theme, I'll assess emotional intensity:

- **😤 High frustration** - Active blocker, considering alternatives
- **😕 Medium pain** - Annoying but manageable
- **🤷 Low priority** - Nice-to-have, not urgent

This helps prioritize which problems to solve first.

### Job-to-be-Done Framing

For each theme, I'll translate into JTBD format:

**When** [situation],  
**I want to** [motivation],  
**So I can** [outcome].

Example:
- **When** I'm in a meeting and someone mentions an action item,
- **I want to** capture it instantly without disrupting the conversation,
- **So I can** ensure I don't forget commitments and follow through.

---

## Common Mistakes to Avoid

### Mistake 1: Treating All Feedback Equally
Not all user feedback is equally valuable. I'll help you:
- Weight feedback by frequency (how many users mentioned it)
- Consider severity (how painful the problem is)
- Factor in strategic fit (does this align with your roadmap)

### Mistake 2: Building Exactly What Users Ask For
Users are great at describing problems, terrible at designing solutions.

When I see a feature request, I'll dig into:
- What problem are they really trying to solve?
- What's the job-to-be-done?
- Are there simpler solutions?

### Mistake 3: Confirmation Bias
If you went into interviews with a hypothesis, I'll flag:
- Evidence that supports your hypothesis
- Evidence that contradicts it
- **Contradictory evidence gets extra weight** (it's harder to see)

### Mistake 4: The Silent Majority
Remember: the users who agreed to be interviewed are not representative of all users.

I'll remind you:
- Who did you NOT talk to?
- What segments are missing from this research?
- What assumptions are you making about non-participants?

---

## Output Integration

### Where Files Go

**Research synthesis:**
- Active work: `outputs/research-synthesis/[topic]-[date].md`
- When finalized: Archive to `context-library/research/[topic]-synthesis.md` for future reference
- Executive summary: Can be shared directly with stakeholders

### Link to Other Work

After synthesis:
- **Create PRD** - Use `/prd-draft` to turn top themes into feature spec
- **Inform strategy** - If findings affect multiple features, feed to `/write-prod-strategy`
- **Update roadmap** - Which themes map to Q# priorities?
- **Competitive context** - If competitor mentions appear, link to `/competitor-analysis`

### Cross-Skill Integration

**Feeds into:**
- `/prd-draft` - Auto-populate Hypothesis with user quotes and insights
- `/write-prod-strategy` - Themes inform strategic pillars
- `/status-update` - Key research findings go in stakeholder updates
- `/competitor-analysis` - If competitors mentioned, extract those mentions

**Pulls from:**
- `context-library/research/` - What questions were asked?
- `context-library/prds/` - What was the original problem hypothesis?
- `/interview-guide` - Questions asked in the interview
- `context-library/meetings/` - Past conversations about this problem

---

## Integration With Your PRD

After synthesis, I'll offer:

```
Your research synthesis is complete!

**Next steps:**

1. **Create a PRD** - Use `/prd-draft` to turn these insights into a spec
2. **Update roadmap** - Which themes should we prioritize this quarter?
3. **Share with stakeholders** - I can help draft a summary for leadership
4. **Plan follow-up research** - What open questions need validation?

What would you like to do first?
```

### Auto-Populate PRD Sections

When you use `/prd-draft` after synthesis, I'll automatically:
- Pull user quotes into the "Hypothesis" section
- Add frequency data to "Strategic Fit"
- Suggest success metrics based on pain points
- Flag non-goals from lower-priority themes

---

## Tips for Better Synthesis

### 1. Synthesize Quickly
Do this within 24 hours of your last interview while insights are fresh.

### 2. Involve Your Team
Share the raw observations with designers and engineers. Let them help cluster themes. They'll spot patterns you might miss.

### 3. Look for the "Why"
Don't stop at surface-level problems. Keep asking "Why?" until you get to the root cause.

Bad: "Users want a faster app"
Good: "Users abandon tasks mid-flow because load times break their mental model of the workflow"

### 4. Preserve User Language
Use exact quotes. Don't paraphrase into "product-speak." User language is powerful for presentations.

### 5. Note What Surprised You
The most valuable insights are often the ones that contradicted your assumptions.

---

## Output Deliverables

When synthesis is complete, I'll create:

1. **Executive Summary** (1 page) - For leadership and stakeholders
2. **Full Synthesis Report** (Markdown file) - Complete analysis with all themes
3. **Insight Highlights** (Video clips or quotes) - For sharing with the team
4. **Research Archive** (Appendix) - Raw observations for future reference

All files will be saved to:
- `outputs/research-synthesis/[topic]-[date].md`
- `context-library/personal-context-pm-background.md` (updated)

---

## When to Do More Research

After synthesis, I might recommend additional research if:

- Themes lack depth (not enough examples)
- Major contradictions remain unresolved
- You talked to <5 users (not enough for saturation)
- Critical segments are missing from your sample
- Open questions outnumber clear insights

**Rule of thumb:** After 5-8 interviews with the right users, you should have 3-5 clear themes with strong supporting evidence. If not, talk to more people.

---

Remember: User research isn't about validation. It's about discovery. The goal isn't to hear what you want; it's to learn what you need to know.

---

## Output Quality Self-Check

Before presenting output to the PM, verify:

- [ ] **File saved to correct location:** Output saved to `outputs/research-synthesis/[topic]-[date].md`
- [ ] **Context routing table was checked:** Reviewed `context-library/research/` for past findings, `context-library/prds/` for related problem statements, and `context-library/strategy/` for strategic fit
- [ ] **Themes backed by 2+ sources:** Every theme in the synthesis is supported by observations from at least 2 different interview participants (not a single anecdote)
- [ ] **Direct user quotes included:** Each key finding includes at least one verbatim user quote with attribution (participant name or identifier)
- [ ] **Insight severity/frequency rated:** Every theme has a frequency count (e.g., "6 out of 8 users") and a severity rating (High/Medium/Low)
- [ ] **Recommendations linked to specific product areas:** Each recommendation names a concrete feature, flow, or product area it applies to (not "improve the experience")
- [ ] **Contradictory findings explicitly flagged:** Any cases where users disagreed or data conflicted are called out in a dedicated section with both perspectives presented
- [ ] **Handoff to `/prd-draft` suggested:** If actionable findings exist that could become features, the output explicitly suggests running `/prd-draft` as a next step
