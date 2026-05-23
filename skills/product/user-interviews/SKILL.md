---
name: User Interviews
description: Comprehensive guide to conducting effective user interviews for problem discovery, solution validation, and continuous learning
---

# User Interviews

## Why User Interviews Matter

### 1. Understand Problems Deeply

**Surface-Level:**
> "Users want a faster checkout."

**Deep Understanding (From Interviews):**
> "Users abandon checkout because they're forced to create an account. They're on mobile, in a hurry, and don't want to remember another password. They'd prefer guest checkout or social login."

**Difference:** Interviews reveal the "why" behind behavior.

### 2. Validate Assumptions

**Assumption:**
> "Users want dark mode because it looks cool."

**Reality (From Interviews):**
> "Users want dark mode because they use the app at night and bright screens hurt their eyes."

**Learning:** Assumption was partially wrong (reason was different).

### 3. Uncover Needs Users Can't Articulate

**User Says:**
> "I want faster search."

**What They Actually Need (Observed in Interview):**
> "I want better filters so I don't have to search multiple times."

**Why:** Users describe symptoms, not root causes.

### 4. Build Empathy

**Without Interviews:**
- Build features based on data/assumptions
- Don't understand user context
- Miss emotional aspects

**With Interviews:**
- See users struggle in real-time
- Understand their workflow
- Feel their pain points
- Build better solutions

---

## When to Conduct Interviews

### 1. Problem Discovery (Before Building)

**Goal:** Understand what problems users have

**Questions:**
- What are you trying to accomplish?
- What's frustrating about current solutions?
- How do you work around this problem?

**Output:** Problem statement, user needs

### 2. Solution Validation (Prototype Testing)

**Goal:** Test if proposed solution solves the problem

**Questions:**
- What do you think of this approach?
- How would you use this?
- What's missing?

**Output:** Solution feedback, usability issues

### 3. Usability Testing (After Building)

**Goal:** Observe how users interact with product

**Questions:**
- Can you complete [task]?
- What did you expect to happen?
- Where did you get stuck?

**Output:** Usability issues, UX improvements

### 4. Continuous Learning (Ongoing)

**Goal:** Stay connected to users, discover new opportunities

**Questions:**
- How has your workflow changed?
- What new challenges are you facing?
- What are you excited about?

**Output:** New feature ideas, product roadmap

---

## Types of User Interviews

### 1. Problem Interviews (Discover Problems)

**Purpose:** Understand user problems before building anything

**Structure:**
- Background: Who is the user?
- Current behavior: How do they solve this today?
- Pain points: What's frustrating?
- Workarounds: What have they tried?

**Example Questions:**
- "Tell me about the last time you [struggled with X]."
- "What have you tried to solve this?"
- "If you had a magic wand, what would you change?"

**Output:** Problem validation, user needs

### 2. Solution Interviews (Test Solutions)

**Purpose:** Validate proposed solution with users

**Structure:**
- Recap problem (ensure alignment)
- Show solution (prototype, mockup, description)
- Get feedback
- Measure willingness to pay

**Example Questions:**
- "What do you think of this approach?"
- "How would you use this?"
- "What's missing?"
- "Would you pay for this? How much?"

**Output:** Solution validation, feature priorities

### 3. Usability Tests (Observe Product Use)

**Purpose:** Watch users interact with product

**Structure:**
- Give task (e.g., "Complete checkout")
- Observe (don't help!)
- Ask follow-up questions

**Example Questions:**
- "Can you show me how you would [complete task]?"
- "What did you expect to happen here?"
- "Why did you click that?"

**Output:** Usability issues, UX improvements

### 4. Jobs-to-be-Done Interviews (Deep Context)

**Purpose:** Understand the "job" users are hiring your product to do

**Structure:**
- First thought: When did you first think about solving this?
- Passive looking: What did you research?
- Active looking: What solutions did you try?
- Decision: Why did you choose this product?
- Consumption: How are you using it now?

**Example Questions:**
- "When did you first realize you needed a solution for this?"
- "What other products did you consider?"
- "What made you choose this product over alternatives?"

**Output:** User motivations, competitive insights, positioning

---

## Recruiting Participants

### 1. Current Users (Easiest)

**Pros:**
- Already using product
- Easy to reach (email, in-app)
- Understand context

**Cons:**
- May be biased (already like product)
- Miss non-user perspective

**How to Recruit:**
- In-app message: "Help us improve! 30-min interview, $50 gift card"
- Email to active users
- Reach out to power users directly

### 2. Target Users (Not Yet Customers)

**Pros:**
- Unbiased (no loyalty)
- Represent potential customers
- Fresh perspective

**Cons:**
- Harder to find
- May not understand product

**How to Recruit:**
- LinkedIn outreach (search for job titles)
- Communities (Reddit, Slack, Discord)
- User research platforms (UserTesting, Respondent.io)

### 3. Lost Users (Churned)

**Pros:**
- Understand why they left
- Honest feedback (no loyalty)
- Identify retention issues

**Cons:**
- May be bitter/negative
- Hard to reach (not engaged)

**How to Recruit:**
- Email churned users
- Offer incentive ($100+ gift card)
- Be empathetic (not defensive)

### 4. Non-Users (Why They Don't Use Product)

**Pros:**
- Understand barriers to adoption
- Identify market gaps
- Competitive insights

**Cons:**
- May not be target market
- Less relevant feedback

**How to Recruit:**
- Survey: "Why haven't you tried [product]?"
- Competitor users (LinkedIn, communities)

### Sample Size: 5-10 Per Segment

**Why 5-10:**
- Diminishing returns after 5-7 interviews
- Most patterns emerge by interview 5
- 10 is enough for confidence

**Example:**
- 5 interviews with power users
- 5 interviews with casual users
- 5 interviews with churned users
- **Total:** 15 interviews

---

## Interview Preparation

### 1. Research Question (What to Learn)

**Bad (Too Vague):**
> "Learn about users."

**Good (Specific):**
> "Understand why users abandon checkout at the payment step."

**Framework:**
- What do we want to learn?
- What decisions will this inform?
- What assumptions are we testing?

### 2. Interview Guide (Questions, Not Script)

**Structure:**
```
1. Intro (5 min)
   - Build rapport
   - Explain purpose
   - Get consent to record

2. Background (10 min)
   - Who are you?
   - What do you do?
   - How do you currently solve [problem]?

3. Main Questions (35 min)
   - Core topics
   - Follow-up questions
   - Dig deeper with "5 Whys"

4. Demo/Test (if applicable) (5 min)
   - Show prototype
   - Observe interaction

5. Wrap-up (5 min)
   - Any questions for us?
   - Thank you
   - Next steps
```

**Example Guide:**
```markdown
# Interview Guide: Checkout Abandonment

## Intro (5 min)
- Thanks for joining!
- We're trying to understand why users abandon checkout
- This will take about 60 minutes
- OK to record? (for notes only, not shared)

## Background (10 min)
- Tell me about yourself
- How often do you shop online?
- What devices do you use?

## Main Questions (35 min)
- Tell me about the last time you abandoned a checkout
- What made you abandon?
- What were you thinking at that moment?
- Have you ever completed a purchase on our site? Why/why not?
- What would make you more likely to complete checkout?

## Demo (5 min)
- [Show new checkout flow]
- What do you think of this?
- Would this solve your problem?

## Wrap-up (5 min)
- Anything else you'd like to share?
- Thank you! $50 gift card sent via email
```

### 3. Recording Setup (With Permission)

**Tools:**
- Zoom (with recording)
- Google Meet (with recording)
- Otter.ai (transcription)

**Best Practices:**
- Ask permission: "Is it OK if I record this for note-taking?"
- Explain: "Recording is for internal use only, not shared"
- Offer opt-out: "If you'd prefer not to be recorded, that's fine"

### 4. Note-Taking Plan

**Options:**

**Option 1: Solo (You Take Notes)**
- Record interview
- Take brief notes during
- Detailed notes after

**Option 2: Pair (Second Person Takes Notes)**
- You focus on interview
- Second person takes detailed notes
- Better quality notes

**Option 3: Transcription (Otter.ai)**
- Auto-transcribe
- Review transcript after
- Highlight key quotes

**Recommended:** Pair (if possible) or Transcription

---

## Interview Structure (60 Minutes)

### Intro (5 min): Build Rapport

**Goals:**
- Make interviewee comfortable
- Explain purpose
- Set expectations

**Script:**
```
"Hi [Name], thanks for joining! I'm [Your Name] from [Company].

We're trying to understand [problem area] better, and your perspective would be really helpful.

This will take about 60 minutes. There are no right or wrong answers—we just want to learn from your experience.

Is it OK if I record this for note-taking? It's just for internal use, not shared externally.

Great! Let's get started."
```

### Background (10 min): Context About User

**Goals:**
- Understand who they are
- Build context for later questions
- Warm up conversation

**Questions:**
- "Tell me a bit about yourself and what you do."
- "How long have you been in this role?"
- "What does a typical day look like for you?"
- "How do you currently solve [problem area]?"

### Main Questions (35 min): Core Topics

**Goals:**
- Understand problem deeply
- Uncover pain points
- Validate assumptions

**Techniques:**
- Open-ended questions
- "5 Whys" to dig deeper
- Silence (let them think)
- Follow-up on interesting points

**Example:**
```
Q: "Tell me about the last time you tried to [complete task]."
A: "I tried to checkout but gave up."

Q: "What made you give up?"
A: "It asked for too much information."

Q: "What information did it ask for?"
A: "Phone number, address, credit card..."

Q: "Which part was most frustrating?"
A: "The phone number. I don't want marketing calls."

Q: "Have you abandoned other checkouts for similar reasons?"
A: "Yes, always. I hate giving my phone number."
```

### Demo/Test (if applicable) (5 min)

**Goals:**
- Show prototype/solution
- Get feedback
- Observe interaction

**Script:**
```
"I'd like to show you something we're working on. This is just a prototype, so it's not perfect.

[Show prototype]

What do you think of this approach?"
```

### Wrap-up (5 min): Thank You

**Goals:**
- Thank participant
- Ask if they have questions
- Explain next steps

**Script:**
```
"This has been really helpful, thank you!

Do you have any questions for me?

We'll send you a $50 Amazon gift card via email within 24 hours.

If you're interested, I can follow up with what we learn from these interviews.

Thanks again!"
```

---

## Asking Good Questions

### 1. Open-Ended ("Tell me about..." not "Do you...")

**Bad (Closed-Ended):**
> "Do you like the new design?"

**Good (Open-Ended):**
> "What do you think of the new design?"

**Why:** Open-ended questions get richer answers.

### 2. Avoid Leading Questions

**Bad (Leading):**
> "Don't you think the checkout is too long?"

**Good (Neutral):**
> "What do you think about the checkout process?"

**Why:** Leading questions bias the answer.

### 3. Ask About Past Behavior (Not Future Hypotheticals)

**Bad (Hypothetical):**
> "Would you use dark mode if we added it?"

**Good (Past Behavior):**
> "Tell me about the last time you used dark mode in an app."

**Why:** People are bad at predicting future behavior.

### 4. "5 Whys" to Dig Deeper

**Technique:** Ask "why" 5 times to get to root cause

**Example:**
```
Q: "Why did you abandon checkout?"
A: "It was too slow."

Q: "Why was it too slow?"
A: "It took forever to load."

Q: "Why did it take forever?"
A: "I was on mobile with bad connection."

Q: "Why were you on mobile?"
A: "I was commuting, saw an ad, wanted to buy immediately."

Q: "Why didn't you wait until you got home?"
A: "I'd forget. I need to buy in the moment."
```

**Learning:** Mobile performance is critical for impulse purchases.

### 5. Silence is Okay (Let Them Think)

**Technique:** After asking a question, wait 5-10 seconds

**Why:**
- Gives them time to think
- Often leads to deeper insights
- Uncomfortable silence prompts them to elaborate

**Example:**
```
Q: "What's the most frustrating part of your workflow?"
A: "Hmm..." [5 seconds of silence]
A: "Actually, now that I think about it, it's the manual data entry. I spend 2 hours a day on it."
```

---

## Problem Interview Questions

### Background

- "Tell me about your role and what you do day-to-day."
- "How long have you been doing this?"
- "What tools do you currently use?"

### Problem Discovery

- "Tell me about the last time you [struggled with X]."
- "What's the most frustrating part of [process]?"
- "How much time do you spend on [task]?"
- "What have you tried to solve this problem?"

### Workarounds

- "How do you currently work around this issue?"
- "What manual steps do you take?"
- "Have you tried any other solutions?"

### Impact

- "How often does this problem occur?"
- "What's the cost of this problem? (time, money, stress)"
- "If this problem went away, what would change for you?"

### Ideal Solution

- "If you had a magic wand, what would you change?"
- "What would the perfect solution look like?"
- "Who else deals with this problem?"

---

## Solution Interview Questions

### Recap Problem

- "Just to confirm, the main problem you face is [X], right?"
- "And you currently solve it by [Y]?"

### Show Solution

- "I'd like to show you an approach we're considering."
- [Show prototype/mockup/description]

### Get Feedback

- "What do you think of this approach?"
- "How would you use this in your workflow?"
- "What's missing?"
- "What would you change?"
- "On a scale of 1-10, how likely would you be to use this?"

### Willingness to Pay

- "Would you pay for this?"
- "How much would you expect to pay?"
- "How does that compare to what you currently spend on [alternative]?"

### Comparison

- "How does this compare to [competitor/current solution]?"
- "What would make you switch from [current solution] to this?"

---

## Usability Testing

### Give Task, Observe (Don't Help)

**Task:**
> "Imagine you want to buy a blue t-shirt in size medium. Can you show me how you'd do that?"

**Observe:**
- Where do they click?
- Where do they hesitate?
- What do they say out loud?
- Where do they get stuck?

**Don't Help:**
- Resist urge to guide them
- Let them struggle (that's the learning)
- Only intervene if completely stuck for >2 minutes

### Think-Aloud Protocol

**Instruction:**
> "As you go through this, please think out loud. Tell me what you're looking for, what you're thinking, what you expect to happen."

**Benefits:**
- Understand their mental model
- Hear their expectations
- Identify confusion points

**Example:**
```
User: "OK, I'm looking for the search bar... I see it, top right. I'll type 'blue t-shirt'... OK, results are loading... Hmm, these are all different shades of blue. I want a specific blue, like navy. How do I filter? I don't see a filter option... Maybe it's in this menu? No... I'm stuck."
```

**Learning:** Need better filtering options.

### Note Where They Struggle

**Red Flags:**
- Long pauses (>10 seconds)
- Clicking wrong elements
- Backtracking
- Verbal frustration ("Where is...?", "This doesn't make sense")

**Example Notes:**
```
- User couldn't find filter button (looked for 3 minutes)
- User clicked "Sort" thinking it was "Filter"
- User gave up on filtering, scrolled through all results
```

### Ask What They Expected vs What Happened

**Questions:**
- "What did you expect to happen when you clicked that?"
- "What were you looking for?"
- "Why did you click there?"

**Example:**
```
Q: "What did you expect when you clicked 'Sort'?"
A: "I thought it would let me filter by color and size."

Q: "What actually happened?"
A: "It just sorted by price. Not what I wanted."
```

**Learning:** "Sort" and "Filter" are confusing. Rename or combine.

---

## Interview Anti-Patterns

### 1. Pitching Your Solution

**Bad:**
> "We built this amazing feature that solves all your problems! Don't you love it?"

**Good:**
> "We're exploring different approaches to solve [problem]. I'd love your honest feedback."

**Why:** You're there to learn, not to sell.

### 2. Asking Leading Questions

**Bad:**
> "Don't you think the checkout is too complicated?"

**Good:**
> "What do you think about the checkout process?"

**Why:** Leading questions bias the answer.

### 3. Ignoring Body Language/Tone

**Red Flags:**
- User says "I like it" but sounds unenthusiastic
- User hesitates before answering
- User's body language is closed (arms crossed)

**Action:**
- Dig deeper: "You said you like it, but you don't sound sure. What's your hesitation?"

### 4. Not Following Up on Interesting Points

**Example:**
```
User: "I tried to use the feature but gave up."
Interviewer: "OK, next question..."
```

**Better:**
```
User: "I tried to use the feature but gave up."
Interviewer: "Tell me more about that. What made you give up?"
```

**Why:** Interesting points often lead to biggest insights.

### 5. Interviewing Only Friendly Users

**Problem:**
- Only talk to users who love your product
- Miss critical feedback
- Get biased view

**Solution:**
- Interview churned users
- Interview users who gave low NPS scores
- Interview non-users

---

## Taking Notes

### 1. Record Audio (With Permission)

**Benefits:**
- Can focus on conversation (not note-taking)
- Can review later
- Capture exact quotes

**How:**
- Zoom: Click "Record"
- Google Meet: Click "Record meeting"
- Otter.ai: Auto-transcribe

**Best Practice:**
- Always ask permission
- Explain it's for internal use only

### 2. Take Written Notes (Key Quotes, Observations)

**What to Note:**
- Key quotes (verbatim)
- Surprising insights
- Pain points
- Workarounds
- Feature requests

**Template:**
```
Interview: [Name], [Date]

Key Quotes:
- "I spend 2 hours a day on manual data entry"
- "I'd pay $100/month if it saved me that time"

Pain Points:
- Manual data entry is tedious
- No way to bulk import
- Errors are common

Workarounds:
- Uses Excel to prepare data, then copy-paste
- Hired VA to do data entry

Feature Requests:
- CSV import
- Bulk edit
- Validation rules
```

### 3. Note Non-Verbal Cues

**What to Note:**
- Tone of voice (enthusiastic, frustrated, hesitant)
- Pauses (thinking, uncomfortable)
- Body language (leaning in, arms crossed)

**Example:**
```
Q: "Would you pay for this?"
A: "Yeah, sure..." [hesitant tone, long pause]

Note: User said yes but didn't sound confident. Might not actually pay.
```

### 4. Flag Surprises/Contradictions

**Surprises:**
- Unexpected pain points
- Different use cases than expected
- Features they don't use

**Contradictions:**
- User says one thing, does another
- Behavior doesn't match stated preferences

**Example:**
```
Surprise: User said they use feature daily, but analytics show weekly usage.
Contradiction: User said they want more features, but doesn't use existing ones.
```

---

## Analysis and Synthesis

### 1. Transcribe Key Parts

**Tools:**
- Otter.ai (auto-transcription)
- Rev.com (human transcription, $1.50/min)
- Manual (time-consuming but thorough)

**What to Transcribe:**
- Key quotes
- Surprising insights
- Detailed explanations

**Don't Transcribe:**
- Small talk
- Off-topic discussions

### 2. Highlight Insights

**What to Highlight:**
- Pain points
- Workarounds
- Unmet needs
- Feature requests
- Willingness to pay

**Example:**
```
"I spend 2 hours a day on manual data entry" ← Pain point
"I'd pay $100/month if it saved me that time" ← Willingness to pay
"I use Excel to prepare data, then copy-paste" ← Workaround
```

### 3. Look for Patterns (Themes Across Interviews)

**Process:**
1. Review all interviews
2. Group similar insights
3. Identify themes

**Example:**
```
Theme: Checkout Friction
- 8 out of 10 users mentioned checkout is too long
- 6 out of 10 users abandoned due to account creation
- 5 out of 10 users want guest checkout

Theme: Mobile Performance
- 7 out of 10 users shop on mobile
- 5 out of 10 users complained about slow loading
- 4 out of 10 users abandoned due to performance
```

### 4. Create User Personas or Journey Maps

**User Persona:**
```
Name: Busy Beth
Age: 32
Role: Marketing Manager
Goals: Shop quickly during lunch break
Pain Points: Checkout takes too long, forced account creation
Behaviors: Shops on mobile, impulse buyer
Quote: "I need to buy in the moment or I'll forget"
```

**Journey Map:**
```
1. See ad on Instagram → 2. Click to product page → 3. Add to cart → 4. Start checkout → 5. Forced to create account → 6. Abandon (too much friction)
```

### 5. Share Findings with Team

**Format:**
- Presentation (slides)
- Document (Google Doc, Notion)
- Video clips (highlight reel)

**What to Include:**
- Key themes
- Quotes (with user permission)
- Recommendations
- Next steps

**Example:**
```
# User Interview Findings: Checkout Abandonment

## Key Themes
1. Checkout is too long (8/10 users)
2. Forced account creation is a barrier (6/10 users)
3. Mobile performance is poor (5/10 users)

## Quotes
- "I don't want to create another account. I just want to buy."
- "The checkout took forever to load on my phone."

## Recommendations
1. Add guest checkout
2. Optimize mobile performance
3. Reduce checkout steps from 5 to 3

## Next Steps
- Prototype guest checkout flow
- A/B test 3-step checkout
- Investigate mobile performance issues
```

---

## From Interviews to Action

### 1. What Did We Learn?

**Summarize:**
- What problems did users describe?
- What solutions did they suggest?
- What surprised us?

**Example:**
```
Learned:
- Users abandon checkout due to forced account creation (not payment friction as we assumed)
- Users want guest checkout (mentioned by 6/10 users)
- Mobile performance is critical (7/10 shop on mobile)
```

### 2. What Hypotheses Were Validated/Invalidated?

**Hypothesis:**
> "Users abandon checkout due to payment friction."

**Result:**
- Invalidated ❌
- Actual reason: Forced account creation

**New Hypothesis:**
> "If we add guest checkout, abandonment will decrease by 30%."

### 3. What Should We Build/Change/Kill?

**Build:**
- Guest checkout (high demand, clear pain point)
- Mobile performance improvements (critical for 70% of users)

**Change:**
- Reduce checkout steps from 5 to 3 (mentioned by 4/10 users)

**Kill:**
- Social login (only 1/10 users mentioned, low priority)

---

## Tools

### Recording

**Zoom:**
- Built-in recording
- Transcription (paid plan)
- Easy to share

**Google Meet:**
- Built-in recording (Workspace accounts)
- Auto-save to Google Drive

**Consent:**
- Always ask permission
- Explain usage ("internal notes only")

### Transcription

**Otter.ai:**
- Auto-transcription
- Real-time
- $10/month for 6000 min

**Rev.com:**
- Human transcription
- $1.50/min
- High accuracy

**Manual:**
- Free
- Time-consuming
- Most control

### Analysis

**Dovetail:**
- User research platform
- Tag insights
- Find patterns
- $25/user/month

**Miro:**
- Visual collaboration
- Affinity mapping
- Synthesis workshops
- Free tier

**Notion:**
- Document interviews
- Tag themes
- Share with team
- Free tier

---

## Interview Scripts and Templates

### Problem Interview Script

```markdown
# Problem Interview: [Topic]

## Intro (5 min)
Hi [Name], thanks for joining! I'm [Your Name] from [Company].

We're trying to understand [problem area] better. This will take about 60 minutes. There are no right or wrong answers.

Is it OK if I record for note-taking? (Internal use only)

## Background (10 min)
- Tell me about yourself and what you do
- How long have you been in this role?
- What does a typical day look like?

## Problem Discovery (35 min)
- Tell me about the last time you [struggled with X]
- What made that frustrating?
- How often does this happen?
- What have you tried to solve this?
- How do you currently work around it?
- If you had a magic wand, what would you change?

## Wrap-up (5 min)
This has been really helpful, thank you!

Any questions for me?

We'll send a $50 gift card via email within 24 hours.
```

### Solution Interview Script

```markdown
# Solution Interview: [Feature]

## Intro (5 min)
[Same as problem interview]

## Recap Problem (5 min)
- Just to confirm, the main problem you face is [X], right?
- And you currently solve it by [Y]?

## Show Solution (10 min)
I'd like to show you an approach we're considering.

[Show prototype]

## Get Feedback (30 min)
- What do you think of this approach?
- How would you use this?
- What's missing?
- What would you change?
- On a scale of 1-10, how likely would you be to use this?
- Would you pay for this? How much?

## Wrap-up (5 min)
[Same as problem interview]
```

### Usability Test Script

```markdown
# Usability Test: [Feature]

## Intro (5 min)
[Same as problem interview]

## Background (5 min)
- Have you used [product] before?
- How often do you use it?

## Tasks (40 min)
I'm going to give you some tasks. Please think out loud as you go.

Remember, we're testing the product, not you. If you get stuck, that's valuable feedback.

Task 1: [Specific task]
- [Observe, don't help]
- What did you expect to happen?
- What actually happened?

Task 2: [Specific task]
- [Repeat]

## Debrief (10 min)
- What was most confusing?
- What did you like?
- What would you change?

## Wrap-up (5 min)
[Same as problem interview]
```

---

## Real Interview Examples and Learnings

### Example 1: Airbnb (2009)

**Problem:** Low bookings in NYC

**Interview Insight:**
- Visited hosts in NYC
- Noticed photos were terrible (amateur, dark, blurry)
- Hosts didn't realize photos mattered

**Action:**
- Hired professional photographers
- Offered free photography to hosts

**Result:**
- Bookings increased 2-3x
- Photo quality became core to Airbnb's success

**Learning:** Sometimes you need to see the problem in person.

### Example 2: Slack (2014)

**Problem:** How to measure product-market fit?

**Interview Insight:**
- Asked users: "How would you feel if you could no longer use Slack?"
  - Very disappointed
  - Somewhat disappointed
  - Not disappointed
- Found 51% said "very disappointed"

**Action:**
- Focused on increasing "very disappointed" percentage
- Targeted features for those users

**Result:**
- Achieved product-market fit
- "Very disappointed" became key metric

**Learning:** Simple question can reveal product-market fit.

### Example 3: Superhuman (2019)

**Problem:** How to achieve product-market fit?

**Interview Insight:**
- Same question as Slack: "How would you feel if you could no longer use Superhuman?"
- Found 22% said "very disappointed" (below 40% threshold)

**Action:**
- Interviewed "very disappointed" users (what they loved)
- Interviewed "somewhat disappointed" users (what was missing)
- Doubled down on features "very disappointed" users loved

**Result:**
- Increased "very disappointed" from 22% to 58%
- Achieved product-market fit

**Learning:** Focus on users who love you, not everyone.

### Example 4: Dropbox (2008)

**Problem:** People didn't understand what Dropbox was

**Interview Insight:**
- Users couldn't articulate the problem Dropbox solved
- Needed to see it to understand it

**Action:**
- Created 3-minute explainer video
- Showed exactly how Dropbox works

**Result:**
- Signups increased from 5,000 to 75,000 overnight

**Learning:** Sometimes users need to see the solution to understand the problem.

---

## Summary

### Quick Reference

**Why Interviews Matter:**
- Understand problems deeply
- Validate assumptions
- Uncover unarticulated needs
- Build empathy

**When to Interview:**
- Problem discovery (before building)
- Solution validation (prototype testing)
- Usability testing (after building)
- Continuous learning (ongoing)

**Interview Types:**
- Problem interviews (discover problems)
- Solution interviews (test solutions)
- Usability tests (observe product use)
- Jobs-to-be-Done (deep context)

**Recruiting:**
- Current users (easiest)
- Target users (unbiased)
- Lost users (understand churn)
- Non-users (barriers to adoption)
- Sample size: 5-10 per segment

**Good Questions:**
- Open-ended ("Tell me about...")
- Avoid leading questions
- Ask about past behavior (not hypotheticals)
- "5 Whys" to dig deeper
- Silence is okay

**Interview Structure:**
- Intro (5 min)
- Background (10 min)
- Main questions (35 min)
- Demo/test (5 min)
- Wrap-up (5 min)

**Anti-Patterns:**
- Pitching your solution
- Leading questions
- Ignoring body language
- Not following up on interesting points
- Only interviewing friendly users

**Analysis:**
- Transcribe key parts
- Highlight insights
- Look for patterns
- Create personas/journey maps
- Share findings with team

**Tools:**
- Recording: Zoom, Google Meet
- Transcription: Otter.ai, Rev
- Analysis: Dovetail, Miro, Notion
