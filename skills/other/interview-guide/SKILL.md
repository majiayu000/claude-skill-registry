---
name: interview-guide
description: Create JTBD-based interview guides for user research. Structured questions for discovery interviews.
disable-model-invocation: false
user-invocable: true
---

# /interview-guide - Create Interview Guides

Generate structured interview guides using Jobs-to-be-Done methodology.

## Quick Start

```
/interview-guide

Planning user research interviews? I'll create a JTBD-based interview guide.

Tell me:
1. What topic are we exploring? (e.g., "why users churn after trial")
2. Who are we interviewing? (role, context, segment)
3. What hypothesis are we testing? (optional but helpful)

I'll check your existing research first, then generate a guide that
focuses on gaps -- not re-asking what you already know.

Output: outputs/interview-guides-[topic]-[date].md
```

---

## Context Routing Logic (Internal - for Claude)

**Automatic Context Checks:**
When this skill is invoked, immediately check:

| Source | Files/Folders | Search Terms | What to Extract |
|--------|---------------|--------------|-----------------|
| Research Plan | `context-library/research/*.md` | hypothesis, problem statement, target users | Current understanding of problem |
| User Personas | `context-library/research/personas*.md` or stakeholder template | target segment, role, company size | Who to interview and their context |
| PRDs | `context-library/prds/*.md` | problem statement, user pain | Problem framing for interview hypothesis |
| Strategy | `context-library/strategy/*.md` | user segment, JTBD canvas | Jobs framework and strategic fit |
| Previous Research | `context-library/research/interviews*.md` | similar problem area, past themes | Avoid revalidating, build on insights |

**Context Priority:**
1. Current PRD and problem statement FIRST
2. Target user personas and segments SECOND
3. Previous research on related topics THIRD
4. Strategic context FOURTH

**Cross-Skill Links:**
- After interview → Link to `/user-interview` for processing transcripts
- After interview → Link to `/user-research-synthesis` for deeper synthesis
- If extracting insights → Link to `/user-research-synthesis` for analysis
- If developing strategy from findings → Link to `/write-prod-strategy`
- Note: `/interview-prep` is for PM job interviews, not user research

---

## Step 0: Understanding Your Research Objective

Before creating the guide, let me understand what you're trying to learn...

**Checking:**
- `context-library/prds/` for the feature or problem you're researching
- `context-library/research/` for previous findings on this area
- `context-library/strategy/` for strategic context
- Stakeholder profiles for interview target information

**Based on what I find, I'll show you:**

### What We Know About This Research

**Research Topic:**
- [Feature or problem you're exploring]
- [Current hypothesis: what do you think you'll find?]
- [Strategic fit: why does this research matter?]

**Target User:**
- [Role and company size from stakeholder profiles]
- [Current tools they use for this job]
- [Past interviews with similar users: what did they tell you?]

**Research Goal:**
- [Specific question you're trying to answer]
- [Assumptions you're validating]
- [What would surprise you?]

### PM-Specific Diagnosis Questions

1. **Hypothesis Confidence:** How sure are you about the problem? (Testing assumption vs validating)
2. **User Segment:** Are you talking to current users, power users, or non-users?
3. **Scope:** Is this a deep dive on one problem or broad discovery?
4. **Previous Research:** What did you learn in past interviews on this topic?
5. **Time Available:** How many interviews can you do? (Affects research scope)

---

## Step 0.5: Integrate Past Research

**Before creating the guide, check `context-library/research/` for existing interview syntheses and findings.**

Search for:
- Previous interview synthesis files (`*interview*`, `*research*`, `*synthesis*`)
- Findings related to this topic area
- Quote banks or insight repositories

**Categorize what you find into three buckets:**

```
## Research Foundation for This Interview Guide

**Based on [N] previous interviews/syntheses found in context-library/research/:**

### Well-Validated Themes (don't over-index here)
These themes have strong evidence from prior research. Include 1-2 confirmation
questions but don't spend 10 minutes re-exploring what you already know.
- [Theme 1]: Supported by [N] interviews. Evidence: "[key quote]"
- [Theme 2]: Supported by [N] interviews. Evidence: "[key quote]"

### Themes Needing More Evidence (probe deeper here)
These came up in prior research but need more data points or deeper understanding.
Allocate extra time in the guide for these areas.
- [Theme 3]: Mentioned by [N] users but unclear why. Probe: [specific angle]
- [Theme 4]: Conflicting signals from past research. Probe: [what to clarify]

### Unexplored Areas (add discovery questions)
These areas haven't been covered in prior research and represent blind spots.
Add open-ended discovery questions to surface new insights.
- [Area 1]: No prior data. Suggested opening: "[question]"
- [Area 2]: Adjacent to known themes but never directly explored.
```

**Add a note at the top of the generated guide:**
> "Based on [N] previous interviews, we already know [validated themes summary]. This guide focuses on deepening [weak evidence areas] and exploring [new areas]. Avoid spending excessive time re-validating established findings."

If no previous research is found, note: "No existing research found in context-library/research/. This is a discovery interview -- all questions are exploratory."

---

## When to Use

- Planning user research interviews
- Discovery for new features
- Understanding customer needs
- Validating problem hypotheses

---

## JTBD Interview Framework

Focus on understanding:
1. **Use Case** - What situation triggers the need?
2. **Alternatives** - What do they use today?
3. **Progress** - What does success look like?
4. **Value** - What's the impact of solving this?
5. **Price** - What would they pay/trade for a solution?

---

## Quick Start Prompt

When PM types `/interview-guide`, respond:

```
Let's create an interview guide. I'll use the JTBD framework.

Tell me:
1. What topic are we exploring?
2. Who are we interviewing? (role, context)
3. What hypothesis are we testing? (optional)

I'll generate a structured guide with opening, core, and closing questions.
```

---

## Interview Guide Structure

### Part 1: Opening (5 min)
Build rapport, set context

### Part 2: Background (10 min)
Understand their world

### Part 3: Core JTBD Questions (25 min)
Dig into the job to be done

### Part 4: Solution Exploration (10 min)
Test ideas without leading

### Part 5: Closing (5 min)
Wrap up, ask for referrals

---

## Output Template

```markdown
# Interview Guide: [Topic]

**Research Goal:** [What we want to learn]
**Target Participant:** [Who we're interviewing]
**Duration:** 45-60 minutes

---

## Part 1: Opening (5 min)

"Thanks for joining. I'm [name], a PM at [company]. We're researching [topic] to better understand [goal]. There are no right or wrong answers—I'm here to learn from your experience."

**Logistics:**
- "Is it okay if I record this for notes?"
- "Everything you share is confidential"
- "Feel free to skip any question"

---

## Part 2: Background (10 min)

1. "Tell me about your role and what you do day-to-day."

2. "How does [topic area] fit into your work?"

3. "Walk me through a typical [relevant workflow]."

---

## Part 3: Core JTBD Questions (25 min)

### Situation & Trigger
4. "Think about the last time you needed to [job]. What was happening?"

5. "What triggered that need? What were you trying to accomplish?"

### Current Solution
6. "How do you handle [job] today?"

7. "What tools or processes do you use?"

8. "What works well about your current approach?"

9. "What's frustrating or difficult about it?"

### Progress & Success
10. "When [job] goes really well, what does that look like?"

11. "How do you know when you've succeeded?"

### Impact & Value
12. "What happens when [job] goes poorly?"

13. "How does that affect you / your team / your business?"

14. "If you could wave a magic wand, what would be different?"

---

## Part 4: Solution Exploration (10 min)

**Show concept/prototype if applicable**

15. "Looking at this [concept], what stands out to you?"

16. "How would this fit into your current workflow?"

17. "What concerns would you have about using something like this?"

18. "What would make this more valuable to you?"

---

## Part 5: Closing (5 min)

19. "Is there anything else about [topic] that I should have asked?"

20. "Who else should I talk to about this?"

21. "Would you be open to a follow-up conversation?"

**Thank them and explain next steps.**

---

## Notes Template

| Question | Response | Key Quote | Insight |
|----------|----------|-----------|---------|
| Q1 | | | |
| Q2 | | | |

---

## Post-Interview
- [ ] Send thank you email
- [ ] Transcribe key quotes
- [ ] Tag themes
- [ ] Add to research repository
```

---

## Question Types to Use

**Open-ended:** "Tell me about..." / "Walk me through..."
**Follow-up:** "Why was that?" / "Can you give an example?"
**Clarifying:** "When you say X, what do you mean?"
**Emotional:** "How did that make you feel?"

## Questions to Avoid

**Leading:** "Don't you think X is annoying?"
**Binary:** "Do you like X?" (yes/no)
**Hypothetical:** "Would you use X if we built it?"
**Multiple:** "What about X and Y and Z?"

---

## Output Integration

### Where Files Go

**Interview guides:**
- Active work: `outputs/interview-guides-[topic]-[date].md`
- When finalized: Archive to `context-library/research/interview-guides/` for team reference
- Use directly: Share with interviewing team before sessions

### Link to Other Work

After creating the guide:
- **Share with team** - Use as standard guide for all interviews on this topic
- **Synthesize findings** - After interviews, use `/user-research-synthesis`
- **Update PRD** - If research validates hypothesis, update in `/prd-draft`
- **Inform strategy** - If research reveals new insights, feed to `/write-prod-strategy`

### Cross-Skill Integration

**Feeds into:**
- `/user-research-synthesis` - After interviews, synthesize the raw notes
- `/prd-draft` - Research findings go into Hypothesis section
- `/write-prod-strategy` - Deep user research informs strategic decisions

**Pulls from:**
- `context-library/research/` - Previous research on this topic
- `context-library/strategy/` - Strategic context about this user problem
- Stakeholder profiles - Information about target user segment

---

## Output Quality Self-Check

Before delivering the interview guide, verify:

| Check | Criteria | Pass? |
|-------|----------|-------|
| **Past research checked** | Searched `context-library/research/` and categorized findings into validated/needs-evidence/unexplored | [ ] |
| **Guide reflects prior knowledge** | Questions focus on gaps, not re-validating what's already known | [ ] |
| **Research foundation note included** | Top of guide states what's known and where this guide focuses | [ ] |
| **No leading questions** | Every question is open-ended, not suggesting a desired answer | [ ] |
| **JTBD framework applied** | Questions cover situation/trigger, current solution, progress/success, impact/value | [ ] |
| **Time-boxed sections** | Each section has a suggested time allocation that totals 45-60 min | [ ] |
| **Follow-up prompts included** | At least 2-3 follow-up probes per core question | [ ] |
| **Closing includes referrals** | Guide asks "Who else should I talk to?" | [ ] |
| **Output file saved** | Guide saved to `outputs/interview-guides-[topic]-[date].md` | [ ] |

**If any check fails, address it before delivering the output.**

---

## Tips

- **Listen more than talk** - 80/20 rule
- **Follow the energy** - If they light up, dig deeper
- **Capture exact quotes** - Their words > your paraphrase
- **Silence is okay** - Let them think
- **Avoid leading questions** - Don't suggest the answer you want
- **Reference past behavior** - "Last time you X, what happened?" beats "Would you use X?"
