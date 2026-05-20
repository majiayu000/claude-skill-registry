---
name: deal-winning-process
description: "Win competitive rounds: run a clean process, deliver value previews before asking, coordinate partners, and manage timelines. Use when you're trying to close a 'must win' deal against other funds."
license: Proprietary
compatibility: Works offline; improved with warm intros and web research; Salesforce logging recommended.
metadata:
  author: evalops
  version: "0.2"
---
# Deal winning process

## When to use
Use this skill when:
- The company is a "must win" or competitive deal
- You need to help the partner close with founder trust + speed
- You need a structured win plan (value + process + narrative)
- You're competing against other funds for a deal

## Inputs you should request (only if missing)
- Who else is in the round (competitors, likely lead)
- Founder priorities (price vs partner vs speed vs brand)
- Your firm's intended role (lead/follow) and constraints
- Timeline (term sheet date, decision date)
- What the founder is optimizing for (explicitly ask)

## Outputs you must produce
1) **Win plan** (one page with daily actions)
2) **Founder decision criteria** (written down, not guessed)
3) **Value preview list** (3 concrete actions you can deliver in 48 hours)
4) **Competitive positioning** (why us vs each competitor, in founder's language)
5) **Process timeline** (meetings + diligence + decision date + term sheet)

Templates:
- assets/win-plan.md
- assets/value-preview.md

## Core principle: Win by doing, not by pitching

The best way to win a competitive deal is to demonstrate partnership before asking for the deal. Value previews > pitch decks.

## Procedure

### 1) Identify the founder's decision criteria (ASK, DON'T GUESS)
Ask directly:
- "What does a great partner do for you in the next 6-12 months?"
- "What are you optimizing for in this round (speed, price, control, help)?"
- "What would make you *not* choose us?"
- "How are you making this decision? What's the process?"
- "Who else are you talking to and what do you like about them?"

**Write the criteria down.** If you can't articulate what the founder is optimizing for, you will lose.

### 2) Build a one-page win plan (with daily actions)

| Day | Action | Owner | Deliverable |
|---|---|---|---|
| Day 0 | Document decision criteria | You | Criteria doc |
| Day 1 | Value preview #1 delivered | You | Customer intro made |
| Day 2 | Partner call | Partner | Relationship building |
| Day 3 | Value preview #2 delivered | You | Recruiting shortlist |
| Day 4 | Diligence completed | You | Evidence pack |
| Day 5 | Terms discussion | Partner | Term sheet |
| Day 6 | Decision | Founder | Close |

Include:
- Why us (2 bullets, in founder's language)
- What we will do in the next 7 days (specific deliverables)
- Who at the firm is involved (right people, not a parade)
- Timeline with dates
- Risks the founder is worried about + how you address them

### 3) Do value previews BEFORE asking to win (within 48 hours)

**High-signal previews (pick 2-3 that match founder priorities):**

| Preview type | What it looks like | Time to deliver |
|---|---|---|
| Customer intro | Intro to a real buyer who will take a call | 24-48 hours |
| Recruiting assist | Shortlist of 5 candidates for critical role + outreach help | 48 hours |
| Operator validation | Call with operator who validates key risk + shares learnings | 24 hours |
| Technical review | Hands-on product feedback from portfolio CTO | 48 hours |
| GTM assist | Intro to channel partner or strategic partner | 48 hours |
| Market intel | Competitive intel or customer research you can share | 24 hours |

**Rules:**
- Make offers you can fulfill within 48 hours.
- The offer must be specific: "I'll intro you to [Name] at [Company] who runs [function]" not "I can make intros."
- Close the loop: "Did that help? What else is blocking?"
- Track what you offered and what you delivered.

### 4) Run a clean process (founder-centric)
- Send agendas before every call.
- Consolidate diligence asks into one request.
- Keep partner time high-quality: pre-wire internally; no surprises.
- Don't posture about leading if you aren't.
- Never miss a deadline you set.

### 5) Competitive positioning (in founder's language)

For each competitor:
| Competitor | Their strength | Our counter | Founder language |
|---|---|---|---|
| A | Brand / signaling | We do X that they don't | "If signaling matters most, they're great. If [X] matters, we're better because..." |
| B | Faster process | We move fast too + more value | "We can match timeline and deliver [specific value preview]" |
| C | Better terms | Our value > their discount | "We're not going to win on price. Here's what we do instead..." |

**Never trash competitors.** Acknowledge their strengths, then pivot to your differentiated value.

### 6) Handle terms responsibly
- Be explicit about what you can offer and what you can't.
- If you're using time pressure, ensure it's real; fake deadlines destroy trust.
- If terms are the deciding factor and you can't win on terms, pivot early: "We're not going to be the cheapest. If price is the deciding factor, you should take their deal."
- If terms aren't the deciding factor, don't lead with terms.

### 7) Track and iterate (daily during competitive process)

Daily check-in questions:
- What did we deliver today?
- What does the founder need tomorrow?
- What's blocking the decision?
- Is our timeline still accurate?
- Did anything change with competitors?

## Salesforce logging (recommended)
- Update Opportunity with competitor set in Notes.
- Log value-preview actions as Activities with outcomes.
- Track next step and owner per action (Tasks with due dates).
- Update Opportunity stage as you progress.

Use `salesforce-crm-ops` for API patterns.

## Win / loss tracking (post-decision)
After every competitive deal (win or loss):
- Document why we won / lost (founder's words, not your interpretation)
- What value previews resonated?
- What would have changed the outcome?
- Update win plan template based on learnings

## References
- Feld/Mendelson public writing is useful for what terms matter and how to keep terms "simple."
- Mark Suster is useful for fundraising dynamics and board mechanics.

## Edge cases
- If another firm is leading: your job is to be the best co-investor. Prove it with concrete help, not promises.
- If the founder is optimizing for brand: your best lever is credible operator help + partner fit, not hype.
- If you're losing on terms: decide early whether to compete or gracefully exit. Don't drag it out.
- If the founder is non-communicative: ask directly "Are we still in this process? What would we need to do to be your choice?"
