---
name: quiz-audit
description: Optimize quiz funnel questions by analyzing flow, checking first question for curiosity hook, evaluating pacing, and identifying dropout points. Use when quiz conversion is low, optimizing existing quizzes, or building new quiz funnels.
---

# Quiz Audit

Optimize quiz funnels for maximum completion and conversion.

## Process

### Step 1: Analyze Current Question Flow

**Map the Quiz:**
- Total number of questions
- Question types (multiple choice, slider, text)
- Time to complete
- Current completion rate
- Drop-off by question

### Step 2: Check First Question

**First Question Rules (Jason K):**

The first question is the MOST important. It must:
- Drive curiosity (not just qualify)
- Be easy to answer
- Create psychological buy-in
- NOT be "Are you male or female?" (boring, seen 1000x)

**Good First Questions:**
- "Do you drink coffee?" (curiosity: what does coffee have to do with this?)
- "Have you tried [common solution] before?" (validates their journey)
- Something unexpected that relates to the offer

**Bad First Questions:**
- Gender selection (no curiosity)
- Age brackets (feels like a form)
- Location (administrative feel)

### Step 3: Evaluate Question Pacing

**Rhythm Check:**
Questions should build psychological momentum.

**Yes Rhythm Strategy:**
Design questions to get "yes" or positive responses:
- Q1: Yes → Q2: Yes → Q3: Yes → Q4: Yes
- NOT: Q1: Yes → Q2: No → Q3: No → Q4: ???

**Question Reframing:**
| Bad (Creates "No") | Good (Creates "Yes/Sometimes") |
|-------------------|-------------------------------|
| "Do you have X problem?" | "Do you sometimes experience X?" |
| "Have you failed at X?" | "Have you tried X before?" |

**Length Rules:**
- Keep questions SHORT
- If they take long to read, they won't complete
- Mobile users especially need brevity

### Step 4: Identify Dropout Points

**Analyze Drop-offs:**
- Which question has highest abandonment?
- Why might people leave there?
- Is the question too personal? Too long? Confusing?

**Common Dropout Causes:**
- Question breaks the "yes" rhythm
- Question feels invasive
- Question is confusing
- Progress feels slow
- Fatigue from length

### Step 5: Output Optimized Sequence

```
## QUIZ AUDIT: [Quiz Name/Offer]

### CURRENT STATE

**Quiz Stats:**
- Questions: [#]
- Avg completion time: [X min]
- Start rate: [X%]
- Completion rate: [X%]
- Lead capture rate: [X%]

**Funnel:**
Ad → Quiz Start: [X%]
Q1 → Q2: [X%]
Q2 → Q3: [X%]
...
Final → Lead: [X%]

---

### QUESTION-BY-QUESTION ANALYSIS

**Q1: [Current question text]**
- Type: [MC/Slider/Text]
- Completion: [X%]
- Issue: [Problem identified]
- Recommendation: [Fix]
- Revised: "[New question text]"

**Q2: [Current question text]**
...

---

### FIRST QUESTION AUDIT

**Current:** "[Question text]"
**Score:** [X/10]

**Issues:**
- [ ] Creates curiosity: [Yes/No]
- [ ] Easy to answer: [Yes/No]
- [ ] Drives engagement: [Yes/No]
- [ ] Avoids clichés: [Yes/No]

**Recommended Replacement:**
"[New first question]"
- Why: [Reasoning]

---

### YES RHYTHM ANALYSIS

| Question | Expected Response | Actual | Fix Needed |
|----------|------------------|--------|------------|
| Q1 | Yes/Positive | [Actual] | [Y/N] |
| Q2 | Yes/Positive | [Actual] | [Y/N] |
| Q3 | Yes/Positive | [Actual] | [Y/N] |
...

**Rhythm Breaks Identified:**
- Q[X]: Changes from Yes to No pattern
- Fix: [How to reframe]

---

### DROPOUT ANALYSIS

**Biggest Drop-off:** Q[X] ([X%] abandon)
**Likely Cause:** [Analysis]
**Solution:** [Recommendation]

**Secondary Issue:** Q[X]
...

---

### LENGTH & PACING

**Current Duration:** [X minutes]
**Recommended:** [X minutes]

**Questions to Remove:**
- Q[X]: Reason: [Why unnecessary]

**Questions to Shorten:**
- Q[X]: Current: "[Long text]" → "[Shorter text]"

**Questions to Add:**
- [If missing key qualification]

---

### OPTIMIZED QUIZ FLOW

**Recommended Question Sequence:**

**Q1 (Curiosity Hook):**
"[Question]"
- Purpose: Create curiosity, easy yes
- Options: [A] [B] [C]

**Q2 (Pain Acknowledgment):**
"[Question]"
- Purpose: Validate their problem
- Options: [A] [B] [C]

**Q3 (Desire Confirmation):**
"[Question]"
- Purpose: Paint future state
- Options: [A] [B] [C]

**Q4 (Qualification):**
"[Question]"
- Purpose: Ensure fit
- Options: [A] [B] [C]

**Q5 (Commitment):**
"[Question]"
- Purpose: Final buy-in before results
- Options: [A] [B] [C]

**Results Page:**
- Personalized based on answers
- Strong CTA

---

### PSYCHOLOGICAL PRINCIPLES APPLIED

**Pain → Future State Journey:**
- Early questions: Acknowledge pain
- Middle questions: Relate to struggles
- Late questions: Paint desired outcome

**Micro-commitments:**
Each "yes" builds investment in completing

**Personalization:**
Use answers to customize results page language

---

### A/B TESTS TO RUN

1. **Test:** [Current Q1] vs [New Q1]
   - Hypothesis: [Expected outcome]

2. **Test:** [X questions] vs [Y questions]
   - Hypothesis: Shorter completes better

3. **Test:** [Question order variation]
   - Hypothesis: [Expected outcome]

---

### IMPLEMENTATION PRIORITY

**High Impact (Do First):**
1. [ ] Replace first question
2. [ ] Fix rhythm breaks at Q[X]

**Medium Impact:**
1. [ ] Shorten questions [X, Y, Z]
2. [ ] Remove unnecessary Q[X]

**Test Later:**
1. [ ] Alternative flows
```

## Quiz Psychology (Jason K)

**Why Quizzes Work:**
- Low bounce rates (engagement)
- Builds investment through micro-commitments
- Feels personalized
- Lower perceived friction than forms

**Quiz as Advertorial:**
Use quiz to hit same points as advertorial:
- Pain point acknowledgment
- Why prior solutions failed (not your fault)
- Unique mechanism tease
- Scarcity/urgency
- CTA

**Never Capture Email Mid-Quiz:**
- Let them complete for the "result"
- Capture AFTER they're invested
- Higher quality leads

Source: Jason K
