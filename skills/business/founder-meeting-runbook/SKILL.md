---
name: founder-meeting-runbook
description: "Run high-signal founder meetings: prep with kill questions, structure the conversation, capture decision-relevant notes, and send crisp follow-ups within 2 hours. Use when taking first meetings, doing partner prep, or screening deals."
license: Proprietary
compatibility: Works offline; improved with web access; Salesforce logging recommended.
metadata:
  author: evalops
  version: "0.2"
---
# Founder meeting runbook

## When to use
Use this skill for:
- First meetings / second meetings with founders
- Prepping a partner for a meeting
- Turning a conversation into a clear "next step" (diligence or pass)

## Inputs you should request (only if missing)
- Company deck / website / demo link (if available)
- Stage and what the founder is raising
- Your firm's investment criteria (check size, ownership, etc.)
- Any prior interactions (intro path, prior passes)

## Outputs you must produce
1) **Meeting brief** (5 bullets + 3 kill questions) before the call
2) **Meeting notes** (decision-oriented, with "must be true" + risks) within 2 hours
3) **Follow-up email** (value + next steps) same day
4) **Pass note** (if passing) that is direct and helpful
5) **Salesforce logging** within 2 hours

**Hard rule:** Every meeting must have a 5-bullet recap logged within 2 hours.

Templates:
- assets/meeting-brief.md
- assets/meeting-notes.md
- assets/follow-up-email.md
- assets/pass-note.md

## Procedure

### 1) Pre-meeting prep (15-25 minutes)

**Do:**
- Read everything public (site, docs, pricing, 2-3 customer quotes if possible).
- Write 5 questions you truly don't know the answer to.
- Identify 3 "kill questions" (if answered badly, likely a pass).
- Write your wedge hypothesis: "Why might this be 10x?"
- Write your initial "must be true" (what needs to be true for this to work?).

**Avoid:**
- Writing a long summary nobody uses.
- Asking questions the deck already answers (unless testing honesty).
- Going in without a point of view.

### 2) Meeting structure (45 minutes, keep time)

| Section | Time | Focus |
|---|---|---|
| Founder story + why this problem | 5 min | Motivation, insight |
| Product + why now | 10 min | Wedge, differentiation |
| Buyer + GTM motion | 10 min | ICP, cycle, pricing |
| Traction + retention + cycle time | 10 min | Evidence of pull |
| Risks / unknowns | 5 min | What founder is worried about |
| Next steps | 5 min | Clear actions |

### 3) High-signal questions (pick 8-12)

**Buyer / pain (establish ICP + trigger)**
- Who is the buyer with budget authority?
- What is the trigger event that causes purchase now?
- What are they doing today instead?
- What is the "do nothing" competitor?
- What happens if they don't buy this? (cost of inaction)

**GTM (establish repeatability)**
- How do the first 10 customers find you?
- What is the sales cycle length and who blocks it?
- What is the onboarding path and time-to-value?
- What's your pricing and how did you arrive at it?
- What's your churn and why do people leave?

**Traction / truth (establish evidence)**
- What's the best evidence this is repeatable?
- What's the hardest churn story you've had?
- What surprised you since launch?
- What metric would you want us to check in 6 months?

**Team / learning rate (establish adaptability)**
- Tell me about a major internal disagreement and how you resolved it.
- What's an example of something you changed your mind about based on evidence?
- What do you believe that most people in the space disagree with?
- What's your biggest gap as a team right now?

**Kill questions (must ask)**
Your 3 kill questions from prep. If the answers are bad, you should pass.

### 4) Note-taking rules (decision oriented)

Your notes must include these sections:
```
## One-line summary
[Company] does [what] for [who] at [stage]. Recommend: [advance/pass/watch]

## Must be true (3 bullets)
1. 
2. 
3. 

## Strengths (3 bullets)
1. 
2. 
3. 

## Risks (3 bullets, ranked)
1. [Highest impact]
2. 
3. 

## Kill question answers
1. Q: / A: / Signal:
2. Q: / A: / Signal:
3. Q: / A: / Signal:

## Next step (if advancing)
- Diligence item 1:
- Diligence item 2:
- Owner:
- Deadline:

## Pass reason (if passing)
- Primary reason:
- What would change our mind:
- Recheck date:
```

### 5) Follow-up (same day, within 2 hours)

**If advancing:**
Send:
- A crisp recap of what you heard (so they can correct it)
- 1-2 specific intros you can make (customers/operators/candidates) - named, not generic
- The diligence items needed next (explicit, max 3)
- A proposed timeline for next steps with dates

**If passing:**
- Be direct ("we're going to pass")
- Name 1-2 concrete reasons (avoid "not a fit")
- Offer 1 actionable suggestion (ICP change, wedge, metric to hit, etc.)
- State what would change your mind (and when to reconnect)

### 6) Passing well

**Rules for passing:**
- Pass quickly (within 48 hours of decision)
- Be direct in the first sentence
- Give a real reason, not "timing" or "fit"
- Leave the door open with specifics

**Good pass:**
"After discussing internally, we're going to pass on this round. Our main concern is [specific reason]. If we saw [specific evidence], we'd love to reconnect. In the meantime, [one helpful suggestion]."

**Bad pass:**
"Unfortunately, this isn't the right fit for us at this time. Best of luck with your fundraise!"

## Salesforce logging (REQUIRED, within 2 hours)

**Minimum logging per meeting:**
- **Event/Activity** with 5-bullet notes attached
- **Opportunity** created or updated with current stage
- **Task** for next step with owner and due date
- **Pass reason** (if passing) + "what would change our mind" + recheck date

Use `salesforce-crm-ops` for API-level logging.

## Interview craft (advanced)

**Building rapport without wasting time:**
- One genuine observation from your prep (not generic flattery)
- Let them talk 70% of the time
- Take notes visibly (shows you're listening)

**Handling evasive answers:**
- If vague: "Can you give me a specific example?"
- If no data: "What's the closest proxy you have?"
- If deflecting: "I want to make sure I understand - [restate question]"
- If still evasive after 2 attempts: note it as a red flag, move on

**Handling overselling:**
- Acknowledge the positive, then probe
- "That's great. What's the hardest part of that?"
- "What would have to go wrong for that to fail?"

**Silence is useful:**
- After a question, let them think
- Don't fill awkward silences - founders often add important context

## References to keep you sharp
- Paul Graham essays for founder patterns and early-stage behavior (e.g., "Do Things That Don't Scale").
- Mark Suster's writing for board and fundraising dynamics.

(These are reading aids, not a substitute for evidence from the company.)

## Edge cases
- If the founder is evasive: ask for specifics (numbers, names, timelines). If still evasive after 2 attempts, treat as a red flag and document.
- If you're missing data: propose the smallest next step that would resolve the top risk.
- If the meeting runs long: protect the "next steps" section. End on clarity, not ambiguity.
- If the founder asks for feedback: be honest and specific, even if uncomfortable.
