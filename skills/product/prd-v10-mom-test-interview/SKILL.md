---
name: prd-v10-mom-test-interview
description: >
  Apply Rob Fitzpatrick's Mom Test discipline to customer interviews during PRD v1.0 Market
  Adoption. Triggers on requests to interview customers, run discovery calls, validate ideas
  with users, or when user asks "how do I interview customers?", "Mom Test", "Rob Fitzpatrick",
  "customer interview", "user research without lies", "talking to humans", "discovery
  conversation". Outputs CFD-* discovery entries with Mom Test-calibrated confidence.
context: fork
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep

execution_modes:
  default: standard
  supports: [quick, standard, deep]
---

# Mom Test Interview Discipline

Position in workflow: v1.0 Continuous Discovery (Torres) → **v1.0 Mom Test Interview** → v1.0 Case Study Builder, Testimonial Collector

## Execution Mode

Default is **standard**. See [`.claude/rules/08-skill-execution-modes.md`](../../rules/08-skill-execution-modes.md) for selection logic.

| Mode | What this skill produces |
|------|--------------------------|
| **quick** | Single interview prep + question list + CFD-* discovery entry post-interview |
| **standard** | Interview prep + scripted opening + 5–7 questions + CFD-* entry with confidence calibration + Bad Data flagged |
| **deep** | Multi-interview cohort plan + cross-interview synthesis + pattern flagging at 3-mention threshold + assumption-test handoff |

## Framework: The Mom Test

From *The Mom Test: How to Talk to Customers and Learn If Your Business is a Good Idea When Everyone is Lying to You* (Rob Fitzpatrick, 2013). Premise: People lie to spare your feelings — especially about your business idea. Learn to ask questions that get truth.

### The three Mom Test rules

1. **Talk about their life, not your idea.** Ask about how they actually live and work, not whether they'd like your hypothetical feature.
2. **Ask about specifics in the past, not generics or opinions about the future.** "Last time you faced X, what did you do?" beats "Would you use a tool that does Y?"
3. **Talk less and listen more.** If you're talking more than 30% of the time, you're pitching, not learning.

### Three types of Bad Data to avoid

| Bad Data type | Example | Why it's bad | What to do |
|---------------|---------|--------------|------------|
| **Compliments** | "That sounds awesome!" | Politeness; not predictive | Discard; don't update confidence |
| **Fluff** | "I usually..." "I would probably..." | Generics, future hypotheticals | Anchor to specifics: "When did you last do that?" |
| **Ideas** | "You should add X" | Solution suggestions disguised as needs | Note as IDEA; ask "what would solving X enable you to do?" — get the underlying job |

### Confidence calibration

Mom Test-disciplined interviews produce **higher-confidence CFD- entries** because the data is grounded in observed past behavior, not opinion. Confidence floors per P4:

- 2/5 — Generic statement ("I sometimes have this problem")
- 3/5 — Specific past instance ("Last Tuesday, I spent 2 hours doing X")
- 4/5 — Specific past instance + paid-money-for-a-workaround / hired-a-person / built-a-script ("I'm paying $30/mo for a tool that almost solves this")
- 5/5 — Repeated specific past instances + ongoing willingness to invest in better solution (commit > talk)

## Consumes

- **ADO-BEACHHEAD-\* and PER-\* personas** — Defines the interview pool; non-segment interviews are still useful but get lower weight
- **Opportunity Solution Tree** (from prd-v10-continuous-discovery-torres) — Interview goals trace to specific opportunities being tested
- **CFD-\* prior research** — Patterns to validate or contradict
- **KPI-\* outcomes** — Why we're interviewing (anchor to what we're trying to move)

## Produces

- **CFD-\* discovery interview entries** — One per interview, with confidence calibrated by Mom Test rules
- **CFD-\* pattern entries** — When 3+ interviews mention the same specific behavior, promote to a pattern entry with frequency
- **Bad Data inventory** — Compliments, fluff, ideas captured for context but not data
- **Discovery Tree updates** — Each interview either strengthens an opportunity, weakens an opportunity, or surfaces a new one

## Execution

### Step 1: Define the goal of this interview

Not "validate the idea." Specifically: which opportunity / assumption from the Opportunity Solution Tree is this interview testing?

| Goal | Example |
|------|---------|
| Validate opportunity exists | "Do beachhead pragmatists actually struggle with pricing-tier selection?" |
| Test assumption | "Will users engage with a pricing wizard before signup?" |
| Map workaround | "How are they solving this today?" |
| Quantify pain | "How much time/money does this cost them currently?" |

Write the goal at the top of the interview notes.

### Step 2: Prep the question list (Mom Test-shaped)

Use specifics-in-the-past form. Avoid hypotheticals.

| Bad question | Better (Mom Test) version |
|--------------|---------------------------|
| "Would you use a pricing wizard?" | "Walk me through how you picked the tier when you signed up." |
| "Do you think analytics is important?" | "Tell me about the last time you looked at analytics." |
| "What features do you wish we had?" | "Tell me about the last time the tool didn't do what you needed." |
| "How would you describe X?" | "Tell me about the last time X came up at work." |

5–7 questions is plenty for a 25–30 minute interview. Leave room to follow threads.

### Step 3: Run the interview

- **Open** with a short framing: who you are, why this conversation, no sales pitch
- **Ask the past-behavior questions**, listen, follow threads
- **Probe specifics** when they generalize: "When was that specifically?" / "What was the dollar / time cost?" / "What did you do next?"
- **Flag Bad Data internally**: when they compliment, smile and move on; when they fluff, anchor to specifics; when they suggest ideas, note as IDEA and dig for the underlying job
- **Talk less than 30%** of the total minutes
- **Don't pitch.** If they ask what you're building, give a one-sentence answer and pivot back

### Step 4: Write up the CFD-* entry within 4 hours

Memory decays fast. Within 4 hours of the interview, write up the CFD- entry. Include:
- Verbatim quotes (the best evidence)
- Specific past instances (the gold)
- Bad Data inventory (compliments, fluff, ideas) — kept for context but not counted as data
- Confidence per P4 calibration

### Step 5: Update the Opportunity Solution Tree [standard+]

Did this interview:
- **Strengthen** an existing opportunity (add to frequency count)?
- **Contradict** an existing opportunity (note dissenting evidence)?
- **Surface** a new opportunity (add to tree)?

Promote a pattern to "Active" focus when 3+ interviews mention the same specific behavior.

### Step 6: Cross-interview synthesis [deep only]

After every cohort of 5–8 interviews, synthesize:
- What patterns emerged at the 3+ mention threshold?
- What hypotheses were contradicted?
- What new opportunities surfaced?
- What's the next interview cohort target?

## Output Template

```
CFD-XXX: Mom Test Interview — [Brief title]
Type: Discovery-Interview
Date: YYYY-MM-DD
Length: [minutes]
Interviewee: [PER-XXX + in-beachhead: yes/no]
Interviewer: [Name]
Goal: [Specific opportunity/assumption being tested]

Specific past instances captured (the gold):
  - "[Verbatim quote — describes a specific past behavior]"
    Context: [When, where, what they did, what it cost]
    Confidence: 3/5 or 4/5 (per P4 calibration)

Workarounds observed:
  - [What they currently do; tools/spend/time invested]

Bad Data (logged but not counted):
  - Compliments: ["That sounds awesome"]
  - Fluff: ["I'd probably use that"]
  - Ideas: ["You should add X"]  → underlying job: [What X would enable]

Pattern strengthening:
  - O1 [opportunity]: +1 mention (now N total)

New opportunity surfaced (if any):
  - [Description]

Overall confidence of this interview's data: X/5
Linked IDs: PER-XXX, ADO-BEACHHEAD-XXX, KPI-XXX, Opportunity-Tree-Node
```

## Anti-Patterns

| Pattern | Signal | Fix |
|---------|--------|-----|
| **Pitching disguised as interview** | Interviewer talking >40% of the time | Talk less; ask follow-ups; let silence happen |
| **Future-hypothetical questions** | "Would you use..." | Reframe to past-behavior |
| **Treating compliments as data** | "5 people said it sounds great → strong signal" | Compliments are not data; discount |
| **Recording feature requests as opportunities** | "User asked for dark mode → opportunity: dark mode" | Dark mode is a solution; the opportunity is the underlying job (e.g., late-night use, eye strain) |
| **No specifics-probe** | Interview ends without a single "what specifically" follow-up | Build the habit; specifics are the gold |
| **Writing up days later** | Interview Friday, CFD- entry Monday | Memory decays; write within 4 hours |
| **No goal for interview** | "Just talking to users" | Each interview tests one specific opportunity or assumption |
| **All interviews from outside beachhead** | Strong patterns but not in segment | In-segment interviews dominate; out-of-segment is supplementary |

## Quality Gates

For each interview:

- [ ] Goal stated before interview (which opportunity/assumption is being tested)
- [ ] Question list is past-behavior shaped, not hypothetical
- [ ] Interviewer talked <30% of minutes
- [ ] At least one "what specifically" follow-up was asked
- [ ] Bad Data inventory exists (compliments / fluff / ideas — even if empty)
- [ ] CFD- entry written within 4 hours
- [ ] Confidence per P4 calibration (not "feels good")
- [ ] Discovery Tree updated (pattern strengthen / contradict / new opportunity)

## Downstream Connections

| Consumer | What it uses | Example |
|----------|--------------|---------|
| **Continuous Discovery (Torres)** | Every interview updates the Opportunity Solution Tree | This skill is the *how*; Torres is the *what to do with* |
| **Chasm Adoption (Moore)** | In-beachhead interviews update ADO-STAGE-* and ADO-BEACHHEAD-* | Patterns strengthen stage assessment |
| **Case Study Builder** | High-impact interviewees become case-study candidates | CFD- with 5/5 confidence + outcome → ADO-REF-* |
| **Testimonial Collector** | Strong endorsement interviews become testimonial sources | Specific past-instance quote + consent → testimonial |
| **Feedback Loop Setup** | Mom Test is the discipline for the structured-interview arm | Inbound feedback ≠ Mom Test (still useful, lower confidence) |

## Detailed References

- Rob Fitzpatrick, *The Mom Test* (2013) — canonical source, short and readable
- Rob Fitzpatrick, *The Workshop Survival Guide* (companion)
- Steve Portigal, *Interviewing Users* (complementary depth)
- wondelai's `mom-test` skill (wondelai/skills)
- (No bundled `references/` — read the book; it's 130 pages)
