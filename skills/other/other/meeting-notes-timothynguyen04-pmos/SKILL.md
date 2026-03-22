---
name: meeting-notes
description: Transform meeting transcripts into structured action items, decisions, and key insights. Processes raw notes, voice memos, or recordings.
disable-model-invocation: false
user-invocable: true
---

## Quick Start

**What to provide:** Raw meeting content in any format.

```
/meeting-notes                           → I'll ask for your content
/meeting-notes [paste transcript]        → Process immediately
/meeting-notes [paste notes] --minimal   → Quick-capture format
/meeting-notes [paste notes] --slack     → Slack-friendly format
```

**Accepted inputs:** Zoom/Otter/Grain transcripts, bullet-point notes, voice memo dictation, Slack threads, email chains, or just "tell me what happened."

**What you get:** Structured notes with decisions, action items (with owners and dates), key insights, open questions, and next steps. Saved to `outputs/meeting-notes/[date]-[topic].md`.

**Time:** 2-5 minutes per meeting.

---

## Input Length Guidance

| Transcript Length | Approach |
|------------------|----------|
| < 30 min (under ~5,000 words) | Process normally in one pass |
| 30-60 min (~5,000-10,000 words) | Process normally, may compress detail |
| 60-90 min (~10,000-15,000 words) | Split into logical segments (by topic or agenda item) and process each |
| 90+ min (15,000+ words) | Ask the PM to provide the transcript in chunks, or identify the most important 30-min segment to process first |

**For very long transcripts:** "This is a long transcript. I can process it all, but the output will be more accurate if we focus. Which approach do you prefer?
1. **Full processing** - I'll cover everything but may compress less important sections
2. **Key segments only** - Tell me which agenda items or topics matter most
3. **Chunked processing** - Paste the transcript in 2-3 parts and I'll process each"

---

# /meeting-notes - Transform Meeting Transcripts Into Action

When the PM types `/meeting-notes`, process raw meeting notes, transcripts, or recordings and extract structured action items, decisions, and key insights.

## Context Routing Logic (Internal - for Claude)

**Automatic Context Checks:**
When this skill is invoked, immediately check:

| Source | Files/Folders | Search Terms | What to Extract |
|--------|---------------|--------------|-----------------|
| Related PRDs | `context-library/prds/*.md` | feature from meeting | PRD context, decisions already made |
| Stakeholder Profiles | Stakeholder templates | attendees from meeting | Communication style, preferences, concerns |
| Strategy | `context-library/strategy/*.md` | feature or decision from meeting | Strategic alignment context |
| Previous Meetings | `context-library/meetings/*.md` | topic from this meeting | Historical context, related decisions |
| Action Items | Previous meeting notes | same owners, same topics | Recurring blockers or items |

**Context Priority:**
1. Stakeholder context and communication style FIRST
2. Related PRDs and decisions SECOND
3. Strategic context THIRD
4. Historical meeting context FOURTH

**Cross-Skill Links:**
- If customer interview → Auto-flag for `/user-research-synthesis` if > 3 customer conversations
- If decision about feature → Update related PRD in `/prd-draft`
- If action items about research → Link to `/interview-guide` or `/user-research-synthesis`
- If strategy discussion → Update `/write-prod-strategy` context

---

## Step 0: Understanding Meeting Context

Before processing, let me check if there's relevant context...

**Checking:**
- `context-library/meetings/` for any previous meetings on this topic
- Stakeholder profiles for communication style of attendees
- `context-library/prds/` for related feature context
- `context-library/strategy/` for strategic alignment

**Based on what I find, I'll show you:**

### Meeting Context

**Type:** [Customer interview / Stakeholder review / Team planning / 1:1 / Design review / Engineering sync / other?]

**Topic:** [Feature or area being discussed]

**Key Participants:**
- [Who was there and their role]
- [Communication style from stakeholder profiles: what matters to them?]

**Related Context:**
- [PRDs: any feature PRDs this relates to?]
- [Previous decisions: any decisions already made on this topic?]
- [Strategic fit: how does this relate to Q# goals?]

### PM-Specific Diagnosis Questions

1. **Decision Type:** Is this a decision-making meeting or information-sharing?
2. **Stakeholders:** Who are the decision-makers vs. advisors?
3. **Dependencies:** What other meetings or decisions does this depend on?
4. **Urgency:** Are there time-sensitive decisions or deadlines?
5. **Follow-up Needed:** What needs to happen before next steps?

---

## When to Use

- After any customer interview, stakeholder meeting, or team sync
- Processing a day's worth of back-to-back meetings
- Converting rambling voice memos into clear next steps
- Extracting decisions and action items from Slack threads
- Creating meeting summaries for people who couldn't attend

---

## How It Works

This is a 2-step process:

### Step 1: Upload or Paste Your Raw Content
### Step 2: Get Structured Output in Your Format

---

## Step 1: Upload Raw Content

When the PM types `/meeting-notes`, start with:

```
Let's transform your meeting notes into structured action items.

**What do you have?**

You can give me:
- Raw transcript (from Zoom, Grain, Otter.ai, Google Meet)
- Your quick notes (bullet points, fragments, whatever you captured)
- Voice memo or dictation
- Slack thread or email chain
- Just talk it out - tell me what happened in the meeting

**What kind of meeting was this?**
- Customer interview
- Stakeholder review
- Team planning session
- 1:1 with manager
- Design review
- Engineering sync
- Other: [specify]

**Who was there?**
[Names help me assign action items correctly]

Paste or upload your content, and I'll structure it for you.
```

### What I'm Looking For

As you share, I'll automatically extract:

✅ **Action items** - Clear next steps with owners
✅ **Decisions made** - What was decided and why
✅ **Open questions** - Unresolved issues that need follow-up
✅ **Key insights** - Important context or quotes
✅ **Blockers** - Things preventing progress
✅ **Next steps** - What happens next and when

---

## Step 2: Structured Output

Once I have your content, I'll say:

```
Got it. I'm processing your [meeting type] notes.

I'll create a structured summary with:
- Action items (with owners and due dates)
- Decisions made
- Key insights
- Open questions
- Next steps

Output format: [Standard / Detailed / Minimal]
(I'll use your preferred writing style from context-library/writing-style-*.md)

Processing now...
```

### Standard Format Output

```markdown
# Meeting Notes: [Meeting Title/Topic]

**Date:** [Date]
**Attendees:** [Names]
**Meeting Type:** [Customer Interview / Stakeholder Review / etc.]
**Duration:** [Time]

---

## Summary

[2-3 sentence overview of what was discussed and the main outcome]

---

## Decisions Made

1. **[Decision]**
   - **Why:** [Rationale]
   - **Who decided:** [Name]
   - **Impact:** [What this affects]

2. **[Decision]**
   - **Why:** [Rationale]
   - **Who decided:** [Name]
   - **Impact:** [What this affects]

---

## Action Items

| Task | Owner | Due Date | Priority | Status |
|------|-------|----------|----------|--------|
| [Specific action item] | @[Name] | [Date] | High | 🔴 Not Started |
| [Specific action item] | @[Name] | [Date] | Medium | 🟡 In Progress |
| [Specific action item] | @[Name] | [Date] | Low | 🟢 Complete |

**Notes:**
- Items marked with 🔴 are blocking other work
- Items with no due date should be scheduled within 48 hours

---

## Key Insights & Quotes

**Customer Pain Points:** (if customer interview)
- "[Direct quote]" - [Customer Name]
- [Paraphrased insight about user behavior]

**Technical Constraints:** (if engineering discussion)
- [Specific technical limitation]
- [Workaround or solution proposed]

**Strategic Considerations:** (if stakeholder meeting)
- [Important context about company priorities]
- [Political dynamics to be aware of]

---

## Open Questions

- [ ] [Question that needs answering] - **Owner:** @[Name] - **By:** [Date]
- [ ] [Question that needs answering] - **Owner:** @[Name] - **By:** [Date]
- [ ] [Question that needs answering] - **Owner:** @[Name] - **By:** [Date]

---

## Blockers

1. **[Blocker description]**
   - **Blocked by:** [What/who]
   - **Impact:** [What this is preventing]
   - **Resolution:** [How to unblock]

---

## Next Steps

**Immediate (This Week):**
- [Action item 1]
- [Action item 2]

**Short-term (Next 2 weeks):**
- [Action item 3]
- [Action item 4]

**Follow-up Meeting:**
- **Date:** [When to reconvene]
- **Purpose:** [What to discuss]
- **Attendees:** [Who needs to be there]

---

## Context for Future Reference

[Any additional background information, links to documents, or relevant history that someone reading this later would need]

---

## Appendix: Raw Notes

<details>
<summary>Click to expand raw transcript/notes</summary>

[Original unstructured content for reference]

</details>
```

---

## Customization Options

### By Meeting Type

I'll automatically adjust the format based on meeting type:

**Customer Interview:**
- Emphasize direct quotes and pain points
- Include "Jobs to be Done" section
- Flag insights that validate/invalidate assumptions
- Note emotion and body language cues

**Stakeholder Review:**
- Lead with decisions and action items
- Include "Concerns Raised" section
- Note political dynamics or objections
- Flag approvals needed

**Team Planning:**
- Focus on action items and ownership
- Include estimated effort/complexity
- Note dependencies between tasks
- Track commitments made

**1:1 with Manager:**
- Include "Feedback Received" section
- Note career development topics
- Track commitments from both sides
- Keep confidential items clearly marked

**Design Review:**
- Include "Design Decisions" section
- Note alternatives considered
- Track open design questions
- Link to Figma files or prototypes

**Engineering Sync:**
- Emphasize technical decisions and tradeoffs
- Include "Technical Debt" section
- Note architectural implications
- Track spikes or investigations needed

### By Writing Style

I'll match your preferred style from `context-library/writing-style-*.md`:

**Internal Audience:**
- Conversational, direct tone
- Use "we" language
- Bullet points preferred
- Emoji for quick visual scanning 🎯 ✅ 🚨

**Executive Communication:**
- Start with "so what"
- Bottom-line-up-front (BLUF)
- Quantify impact where possible
- Minimal detail, maximum clarity

**Technical Documentation:**
- Precise terminology
- Include edge cases and assumptions
- Link to relevant specs or tickets
- Code snippets or technical details where relevant

---

## Advanced Features

### Batch Processing Multiple Meetings

If you had a day full of meetings:

```
I have 5 meetings from today. Can you process them all at once?

Meeting 1: Customer call with Acme Corp
Meeting 2: Design review for new onboarding
Meeting 3: 1:1 with Sarah (my manager)
Meeting 4: Sprint planning
Meeting 5: Stakeholder update with VP Product

[Paste all transcripts]
```

I'll create:
1. Individual summaries for each meeting
2. A "Daily Digest" that rolls up all action items by owner
3. Cross-meeting insights (patterns, contradictions, themes)
4. Consolidated list of everything YOU need to do

### Smart Action Item Assignment

If you don't specify who owns an action item, I'll:
- Look at stakeholder info in `context-library/stakeholder-template.md` (or any profiles you add)
- Check who has context on similar work
- Suggest the right owner with reasoning
- Flag items that need clarification

Example:
```
**Action:** Update pricing page with new tier
**Suggested Owner:** @Maria (Design) - She owns the marketing site redesign
**Needs Confirmation:** Check if this should be @Jake (Eng) if it requires backend changes
```

### Context Linking

I'll automatically:
- Link to related PRDs in `context-library/prds/`
- Reference relevant strategy docs in `context-library/`
- Connect to similar past meetings or decisions
- Pull in stakeholder preferences

Example:
```
**Decision:** We'll launch this as an A/B test, not full rollout

**Context:** This aligns with our [Q2 Strategy] of de-risking launches. 
Also see: [Voice Task PRD] which used similar rollout approach successfully.

**Stakeholder Note:** @VP-Engineering prefers A/B tests for all AI features 
(per stakeholder profile: "Always wants data before full launch")
```

### Timeline Conflict Detection

**After extracting action items and decisions, perform a timeline sanity check:**

Compare all time estimates and deadlines mentioned in the meeting against known dates from:
- PRDs in `context-library/prds/*.md` and `outputs/prds/*.md` (launch dates, milestone dates)
- Previous meeting notes in `context-library/meetings/*.md` (prior commitments, deadlines)
- Strategy docs in `context-library/strategy/*.md` (quarter end dates, OKR deadlines)
- Calendar context if available (upcoming reviews, stakeholder meetings)

If any estimates conflict with known deadlines, flag explicitly in the output:

```
## Timeline Risks

- **TIMELINE RISK:** [Person] said "[Feature X] will take 3 weeks to build" but the PRD for [Feature X] has beta launch scheduled in 5 days (from [PRD filename]). These dates conflict -- clarify with engineering before committing.

- **TIMELINE RISK:** Team agreed to "deliver by end of sprint" but no sprint end date was stated. Previous meeting on [date] referenced sprint ending [date]. Confirm this is the same sprint.

- **TIMELINE RISK:** [Person] committed to "[deliverable] by Friday" but they also have a commitment from [previous meeting] to deliver [other thing] by Thursday. Check capacity.
```

If no timeline conflicts are found, skip this section silently (don't add an empty section).

---

### Experiment Design Prompt

**When a "test both" or "A/B test" decision is captured:**

If the meeting notes contain language like "let's test both," "we should A/B test this," "run an experiment," or similar, automatically add a prompt after the relevant decision:

```
**Experiment Design Needed:**
You agreed to test [Option A vs Option B], but the meeting didn't define:
- **Comparison metric:** What metric determines which option wins?
- **Sample size:** How many users/sessions do you need for significance?
- **Success threshold:** What difference between options counts as meaningful?
- **Duration:** How long should the test run?

Consider defining these before the test starts. Run `/experiment-metrics` for the STEDII framework, or `/experiment-decision` to determine if an A/B test is even the right approach.
```

Only trigger this when an experiment is decided but the specifics are missing. If the team already defined the metric, sample size, and threshold, skip this prompt.

---

### Auto-Create Follow-Up Tasks

After processing, I'll offer:

```
Notes processed! I extracted 7 action items.

**Want me to:**
- [ ] Create Linear/Jira tickets for each action item?
- [ ] Draft a Slack update to share with the team?
- [ ] Schedule a follow-up meeting?
- [ ] Add insights to your PRD or context library?
- [ ] Flag items that need executive approval?

Just let me know what you need.
```

---

## Special Handling

### Customer Interview Notes

For customer interviews, I'll add:

**Jobs-to-be-Done:**
When [situation], I want to [motivation], so I can [outcome].

**Pain Points Validated:**
- ✅ [Hypothesis we confirmed]
- ❌ [Hypothesis we disproved]
- ❓ [Hypothesis still unclear]

**Quotes to Remember:**
"[Powerful verbatim quote]" - [Customer Name]
→ Use this in: [PRD / Presentation / Stakeholder Update]

**Recommended Next Steps:**
- Talk to [X more users in this segment]
- Test [specific solution hypothesis]
- Explore [unexpected insight that emerged]

### Handling Sensitive Information

If I detect sensitive topics:

```
⚠️ Sensitive Content Detected

This meeting included:
- Confidential company strategy
- Personal performance feedback
- Unannounced product plans
- Competitive intelligence

**Recommendation:** 
- Mark this document as [Confidential - Internal Only]
- Store in [secure location, not Slack]
- Consider creating a "sanitized" version for wider sharing

Should I create two versions?
```

### Multi-Language Support

If transcript is in another language or mixed:

```
I detected [Spanish/French/Mandarin] in this transcript.

Would you like me to:
- Translate to English and provide both versions
- Summarize in English only
- Keep original language for quotes
```

---

## Output Options

### Minimal Format (Quick Capture)

```markdown
# Quick Notes: [Meeting Topic]

**Main Outcome:** [One sentence]

**Action Items:**
- [ ] [Task] - @Owner - [Date]
- [ ] [Task] - @Owner - [Date]

**Key Quote:**
"[Most important thing said]"

**Next Step:**
[What happens next]
```

### Detailed Format (Comprehensive)

Includes everything in standard format plus:
- Detailed context and background
- Meeting objectives vs. outcomes
- Attendee contributions
- Timeline of discussion
- Related documents and links
- Full verbatim transcript in appendix

### Slack-Friendly Format

Optimized for pasting into Slack:

```markdown
**Meeting Recap: [Topic]** 📝

*Main outcome:* [One sentence]

*Decisions:*
• [Decision 1]
• [Decision 2]

*Action items:*
✅ [Task] - @Owner - Due [Date]
✅ [Task] - @Owner - Due [Date]

*Open questions:*
❓ [Question] - @Owner to resolve

*Next meeting:* [Date] to discuss [Topic]

Full notes: [Link to doc]
```

---

## Integration With Other Commands

### Flows Into PRD

After meeting notes, you might:

```
These insights from the customer interview should go into a PRD.

Use `/prd-draft` and I'll auto-populate:
- User quotes → Hypothesis section
- Pain points → Problem statement
- Decisions made → Non-goals and trade-offs
- Action items → Open questions
```

### Updates Status

After processing meeting notes:

```
You have action items from this meeting.

Use `/status-update` and I'll:
- Include completed action items in your update
- Flag overdue items from previous meetings
- Show progress on open questions
```

### Creates Slack Messages

After any meeting:

```
Use `/slack-message` to:
- Share meeting recap with attendees
- Loop in stakeholders who missed it
- Ask for help on open questions
- Confirm action item ownership
```

---

## Pro Tips

### 1. Voice Memo Your Thoughts

After a meeting, open Claude Code mobile and just talk:

"Okay, I just met with the VP of Sales. Here's what happened..."

I'll structure it into proper notes automatically.

### 2. Same-Day Processing

Process meetings within 24 hours while they're fresh. The quality is dramatically better.

### 3. Include Context

Tell me:
- What the meeting was about
- What you were hoping to accomplish
- Any relevant background I should know

This helps me extract the RIGHT insights, not just ANY insights.

### 4. Correct and Refine

After I create the notes, review and edit:
- Add context I might have missed
- Correct any misinterpreted names or terms
- Adjust priority levels
- Add due dates if they weren't mentioned

### 5. Archive and Learn

Save processed meeting notes to:
- `outputs/meeting-notes/[date]-[topic].md`

Over time, I'll spot patterns:
- Recurring topics that never get resolved
- Action items that keep slipping
- Decisions that get reversed
- Stakeholders who always raise the same concerns

---

## Common Mistakes to Avoid

### ❌ Waiting Too Long to Process

Don't let notes pile up for a week. Context decays fast.

**Fix:** Process same day or next morning at latest.

### ❌ Not Capturing Decisions

Action items without decisions lack context.

**Fix:** Always note WHY something was decided, not just WHAT.

### ❌ Vague Action Items

"Follow up on that thing" is useless.

**Fix:** Make action items specific with clear owners and dates.

### ❌ Missing the Subtext

Sometimes what WASN'T said is more important than what was.

**Fix:** Add a "Context" section with political dynamics, concerns, or hesitations you observed.

### ❌ Not Sharing the Notes

Meeting notes that sit in your private doc help no one.

**Fix:** Share with attendees within 24 hours. Use `/slack-message` to make it easy.

---

## Example Inputs and Outputs

### Example 1: Raw Voice Memo

**Input:**
```
Okay so I just talked to Marcus from Spotify. He's a PM there and he was 
telling me about how they manage tasks and dude they have like 47 voice memos 
on their phone that are just tasks they need to do but they never convert them 
into their task manager because it's such a pain. He showed me his workaround 
where he just like emails himself but then he forgets to check those emails. 
This is exactly the problem we're trying to solve with the voice feature. 
He said he'd definitely pay for something that just like let him speak and 
it would automatically create a structured task. I asked him about the last 
time this cost him something and he said last week he completely forgot to 
follow up with their design team on a critical feature because the task was 
just in a voice memo. So yeah, pretty clear validation of the problem.
```

**Output:**
```markdown
# Customer Interview Notes: Marcus (Spotify PM)

**Date:** January 5, 2026
**Interviewee:** Marcus (PM at Spotify)
**Interviewer:** [Your name]
**Type:** Problem validation interview

---

## Summary

Strong validation of task capture friction. Marcus has 47 voice memos of 
uncaptured tasks, uses email-to-self workaround, and recently missed a 
critical follow-up due to task not being in his system. Willing to pay for 
voice-to-task solution.

---

## Key Insights

**Problem Validated:** ✅ Task capture friction
- Has 47 voice memos that never get converted to tasks
- "It's such a pain" to manually structure tasks
- Current workaround: emails himself, but forgets to check

**Pain Impact:**
- Last week: Missed critical follow-up with design team
- Reason: Task was stuck in voice memo, not in task manager
- Real cost: Blocked team progress on critical feature

**User Quote:**
"I'd definitely pay for something that just let me speak and it would 
automatically create a structured task." - Marcus

**Jobs-to-be-Done:**
When I have a task from a meeting or conversation, I want to capture it 
instantly without manual structuring, so I don't lose track of commitments.

---

## Validation Status

| Hypothesis | Status | Evidence |
|------------|--------|----------|
| Users lose tasks captured in voice memos | ✅ Confirmed | 47 unconverted voice memos |
| Manual structuring is the friction point | ✅ Confirmed | "It's such a pain" |
| This causes real business impact | ✅ Confirmed | Missed critical design follow-up |
| Users willing to pay for solution | ✅ Confirmed | "I'd definitely pay for..." |

---

## Action Items

- [ ] Add Marcus quote to Voice Task PRD - @You - Tomorrow
- [ ] Schedule follow-up to test prototype - @You - This week
- [ ] Ask Marcus for intro to other Spotify PMs - @You - This week

---

## Next Steps

**Recommended:**
1. Test prototype with Marcus to validate solution approach
2. Ask about specific task attributes he needs (due dates, assignees, etc.)
3. Understand Spotify's task management tools to ensure compatibility

**Add to PRD:**
This interview strongly validates the hypothesis in [Voice Task PRD]. 
Update "Supporting Evidence" section with Marcus's quote and impact story.
```

### Example 2: Stakeholder Meeting Transcript

**Input:**
```
[Zoom transcript pasted]
VP Product: So I'm looking at this roadmap and I'm concerned about the 
timeline for the voice feature. Can we really ship this in Q1?

You: Based on the research we've done, the scope is pretty contained. 
It's mobile-only for v1, creation-only, no editing.

VP Product: Okay but what about the AI accuracy? If users have to edit 
every task it creates, that's actually worse than manual entry.

You: Good point. We're targeting 80% accuracy with quick edit capability. 
The research showed users are willing to do light edits if it saves the 
structuring work.

VP Product: Alright. I'm tentatively okay with Q1 but let's have a go/no-go 
checkpoint after the first week of beta. If edit rates exceed 50%, we pull back.

You: Agreed. That's actually already in the PRD as a kill criterion.

VP Product: Perfect. One more thing - make sure Legal reviews before beta. 
We're processing voice data and I don't want any GDPR surprises.

You: Will do. I'll loop them in this week.
```

**Output:**
```markdown
# Stakeholder Meeting: Q1 Roadmap Review - Voice Feature

**Date:** January 5, 2026
**Attendees:** VP Product (Sarah Chen), You
**Type:** Roadmap review / Go-no-go decision
**Duration:** 15 minutes

---

## Summary

VP Product approved Q1 timeline for voice feature with conditions: 
go/no-go checkpoint after week 1 of beta based on edit rates, and 
mandatory legal review before launch due to voice data processing.

---

## Decisions Made

1. **Q1 Timeline Approved (Conditional)**
   - **Rationale:** Scope is contained (mobile-only, creation-only, no editing)
   - **Condition:** Go/no-go checkpoint after week 1 of beta
   - **Kill Criterion:** If edit rates exceed 50%, pull back and reassess

2. **Beta Structure Confirmed**
   - **Approach:** Phased rollout with week 1 checkpoint
   - **Success Metric:** Edit rate must stay below 50%
   - **Already documented:** This matches PRD kill criteria

3. **Legal Review Required**
   - **Why:** Voice data processing = GDPR implications
   - **Timing:** Before beta launch
   - **Owner:** You to initiate

---

## Action Items

| Task | Owner | Due Date | Priority | Blocker |
|------|-------|----------|----------|---------|
| Schedule legal review of voice feature | @You | This week | 🔴 High | Blocks beta |
| Set up week 1 beta checkpoint meeting | @You | Before beta | 🟡 Medium | - |
| Confirm edit rate tracking is instrumented | @Engineering | Before beta | 🔴 High | Blocks launch |

---

## Concerns Raised

**VP Product's Main Concern:** AI accuracy
- Worried that poor accuracy could make feature worse than manual entry
- Wants hard data from beta before full rollout
- Edit rate >50% = kill criterion

**Risk Mitigation:**
- Targeting 80% accuracy based on research
- Users validated they're willing to do light edits
- Quick edit capability is part of UX design

---

## Stakeholder Notes

**Sarah Chen (VP Product) - Communication Style:**
- Wants quantitative success criteria (edit rate <50%)
- Appreciates that kill criteria are already in PRD
- Risk-aware, especially around compliance/legal
- Prefers phased rollouts with checkpoints

*→ Update stakeholder profile: Emphasize data-driven go/no-go decisions*

---

## Open Questions

- [ ] What specifically does Legal need to review? - @You to ask Legal - This week
- [ ] Do we need consent flow for voice processing? - @Design + Legal - This week

---

## Next Steps

**Immediate:**
1. Email Legal team with voice feature overview and GDPR question
2. Set up week 1 beta checkpoint with VP Product and Engineering
3. Confirm with Engineering that edit rate tracking is ready

**Before Beta:**
- Legal approval received
- Edit rate instrumentation tested
- Checkpoint meeting scheduled

---

## Context for Future Reference

This conversation went smoothly because:
- Kill criteria were already documented in PRD
- Scope was clearly defined (mobile-only, creation-only)
- Research validated user willingness to edit

**Lesson:** Having quantitative success metrics in the PRD preemptively 
addressed stakeholder concerns and shortened the approval conversation.

*→ Add to lessons-learned: VPs appreciate when PMs anticipate their questions*
```

---

## When to Use Each Format

**Minimal:** Quick team syncs, daily standups, informal check-ins
**Standard:** Most meetings - customer interviews, planning sessions, reviews
**Detailed:** Critical decisions, stakeholder approvals, complex technical discussions
**Slack-Friendly:** Any meeting where you need to broadcast outcomes to a channel

---

## Output Integration

### Where Files Go

**Meeting notes:**
- Quick capture: `outputs/meeting-notes/[date]-[topic].md` (raw processing)
- When finalized: Archive to `context-library/meetings/[date]-[topic].md` for historical reference
- Use as templates: Your meeting notes become template for team

### Link to Other Work

After processing meeting notes:
- **Update PRDs** - If feature decision was made, update `/prd-draft`
- **Create action items** - Use `/create-tickets` for engineering tasks from meeting
- **Status updates** - Reference meeting decisions in `/status-update`
- **Research synthesis** - If customer interview, add to `/user-research-synthesis` batch
- **Slack share** - Use `/slack-message` to share recap with broader team

### Cross-Skill Integration

**Feeds into:**
- `/prd-draft` - Meeting decisions go into PRD sections
- `/status-update` - Meeting action items appear in weekly updates
- `/user-research-synthesis` - Customer interviews add to research synthesis
- `/create-tickets` - Action items become engineering tickets

**Pulls from:**
- `context-library/prds/` - Feature context for meeting
- Stakeholder profiles - Communication preferences and concerns
- `context-library/strategy/` - Strategic alignment context
- `context-library/meetings/` - Previous decisions and context

---

---

## Output Quality Self-Check

Before presenting the meeting notes, verify:

- [ ] **Every action item has an owner:** No orphan tasks with "TBD" owners (suggest an owner if unclear)
- [ ] **Every action item has a due date:** If not mentioned, flag it: "No due date mentioned -- schedule within 48 hours"
- [ ] **Decisions include rationale:** Each decision says WHY, not just WHAT was decided
- [ ] **Timeline conflicts checked:** All deadlines compared against PRDs, previous meetings, and known dates
- [ ] **Experiment details prompted:** If "A/B test" or "test both" was decided, missing experiment design is flagged
- [ ] **Context cross-reference done:** At least one check against PRDs, strategy, or previous meetings was performed
- [ ] **Key quotes are verbatim:** Customer quotes use exact wording from transcript, not paraphrased
- [ ] **Sensitive content flagged:** If confidential topics detected, recommendation to mark as internal-only is included
- [ ] **File saved correctly:** `outputs/meeting-notes/[YYYY-MM-DD]-[topic-kebab-case].md`
- [ ] **Next steps are actionable:** Someone reading "Next Steps" knows exactly what to do without re-reading the full notes

---

**Remember:** The best meeting notes are the ones you actually create. Don't let perfect be the enemy of done. Process them quickly, share them widely, and use them to drive action.
