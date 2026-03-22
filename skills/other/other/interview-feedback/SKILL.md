---
name: interview-feedback
description: Post-PM-interview debrief and continuous improvement for job search
---

**Note:** This skill is for PM career interviews (job interviews). For debriefing after conducting user research interviews, use `/user-research-synthesis` instead.

# Interview Feedback Skill

Capture insights immediately after PM job interviews. Quick retrospective to improve for next rounds and future interviews.

## Quick Start

```
/interview-feedback

Just finished a PM interview? Let's debrief while it's fresh.

Tell me:
1. Which company and role? (e.g., "Senior PM at Stripe")
2. What questions did they ask? (as many as you remember)
3. How do you think you did? (gut feeling: great / good / okay / rough)

I'll help you:
- Score your performance across 5 key dimensions
- Identify specific strengths to repeat
- Create an improvement plan for weak areas
- Track patterns across multiple interviews

For user research interview debriefs, use /user-research-synthesis instead.

Output: outputs/interview-feedback/[date]-[company]-debrief.md
```

## When to Use This Skill

- Within 15 minutes of finishing a PM job interview
- After phone screens, onsite rounds, or take-home presentations
- When you advance to next round (capture what worked)
- When you get rejected (learn for next time)

## Workflow

### Step 0: Emotional Check-In

Before scoring, acknowledge the emotional state. Interviews are stressful.

Ask: "Before we get into the analysis -- how are you feeling about it? Quick gut reaction."

**Why this matters:**
- PMs who feel terrible often performed better than they think (impostor syndrome)
- PMs who feel great sometimes missed signals (overconfidence)
- Naming the emotion first prevents it from biasing the objective scoring

**Use their response to calibrate:**
- If they say "awful" -- be extra careful to highlight what went well before diving into gaps
- If they say "great" -- still praise strengths but don't skip honest critique
- If they say "mixed" -- mirror that by leading with the strongest and weakest dimensions

---

### Step 1: Immediate Brain Dump

Right after the interview ends, capture everything while fresh:

```
## Raw Notes (Stream of consciousness)

**Questions I was asked:**
1. [Question 1 - exact wording if you remember]
2. [Question 2]
3. [Question 3]
[List all questions you can recall]

**My answers (rough outline):**
- Q1: [What I said - framework used, key points made]
- Q2: [What I said]
- Q3: [What I said]

**Follow-up questions interviewer asked:**
- [Follow-up 1 - signals they wanted more depth here]
- [Follow-up 2]

**Interviewer reactions I noticed:**
- [When they nodded, took notes, seemed engaged]
- [When they seemed confused or skeptical]
- [When they cut me off or moved on quickly]

**Things that felt good:**
- [Moment 1: e.g., "Nailed the metrics definition"]
- [Moment 2]

**Things that felt rough:**
- [Moment 1: e.g., "Stumbled on prioritization rationale"]
- [Moment 2]
```

---

### Step 2: Structured Self-Assessment (5 Key Dimensions)

Rate yourself 1-5 on these five core dimensions. Be honest -- this is for your growth, not your ego.

```
## Performance Scorecard

**Interview Type:** [Product Sense / Execution / Behavioral / Design / Technical]

**Company:** [Company name]
**Role:** [Role title]
**Interviewer:** [Name + title if you know it]
**Duration:** [Scheduled time] → [Actual time]

### The 5 Core Dimensions (1-5 scale)

**1. Framework Usage:** ___/5
- Did I use a clear structure? (5-Step, CIRCLES, AARM, STAR)
- Was my thinking organized and easy to follow?
- Did I signal my structure upfront? ("I'll approach this in 3 parts...")
- 1 = No structure, stream of consciousness
- 3 = Some structure but lost it halfway
- 5 = Crystal clear framework, interviewer could follow without notes

**2. Specificity:** ___/5
- Did I use real examples, data, and concrete details?
- Were my metrics specific? ("3.2% conversion" not "low conversion")
- Did I name real products, companies, or technologies?
- 1 = Entirely hypothetical, vague generalities
- 3 = Some specific examples but padded with hand-waving
- 5 = Every claim backed by real data or concrete examples

**3. Creativity:** ___/5
- Did my answer stand out from what 100 other candidates would say?
- Did I show unique insight or a surprising angle?
- Did I go beyond the obvious first solution?
- 1 = Textbook answer anyone could give
- 3 = Solid but predictable
- 5 = Genuinely surprising insight that made the interviewer lean in

**4. Communication:** ___/5
- Was I clear and concise?
- Did I avoid rambling, filler words, or hedging?
- Did I read the room and adjust?
- 1 = Rambled, lost the thread, interviewer looked confused
- 3 = Generally clear but some tangents
- 5 = Every sentence earned its place, confident delivery

**5. Product Sense:** ___/5
- Did I demonstrate user empathy?
- Did I connect user value to business value?
- Did I show understanding of trade-offs?
- 1 = Talked about features without understanding users
- 3 = Mentioned users but didn't deeply empathize
- 5 = Interviewer said "great point" or visibly reacted to insight

**Overall Performance:** [Average of 5 scores] / 5
```

**How to interpret your scores:**

| Average | What it means | What to do |
|---------|--------------|------------|
| 4.5-5.0 | Outstanding -- you're likely advancing | Maintain and fine-tune |
| 3.5-4.4 | Solid -- competitive but not guaranteed | Focus on your lowest dimension |
| 2.5-3.4 | Needs work -- probably won't advance | Intensive practice on 2+ dimensions |
| Below 2.5 | Major gaps -- step back and prepare more | Consider delaying next interview by 1-2 weeks |

---

### Step 3: What Went Well (2 minutes)

Capture your wins to repeat them:

```
## Strengths This Interview

✅ **Strength 1:** [What you did well]
   - Example: "Used 5-step Product Sense framework perfectly"
   - Why it worked: "Gave clear structure, interviewer followed easily"
   - Repeat next time: Yes

✅ **Strength 2:** [What you did well]
   - Example: "Asked great clarifying questions upfront"
   - Why it worked: "Avoided solving wrong problem"
   - Repeat next time: Yes

✅ **Strength 3:** [What you did well]
   - Example: "Specific metrics with targets (DAU/MAU 40% → 50%)"
   - Why it worked: "Showed data-driven thinking"
   - Repeat next time: Yes
```

---

### Step 4: What Needs Improvement (2 minutes)

Be brutally honest about weaknesses:

```
## Areas for Improvement

❌ **Weakness 1:** [What didn't go well]
   - Example: "Spent too long on problem definition (10 min)"
   - Impact: "Only 5 min left for solutions - felt rushed"
   - Fix for next time: "Cap problem def at 5 min, use timer"

❌ **Weakness 2:** [What didn't go well]
   - Example: "Didn't tie solution back to business metrics"
   - Impact: "Answer felt incomplete, interviewer asked about ROI"
   - Fix for next time: "Always end with user value → business value connection"

❌ **Weakness 3:** [What didn't go well]
   - Example: "Used vague language ('users might like this')"
   - Impact: "Sounded uncertain, not data-driven"
   - Fix for next time: "Replace 'might' with 'based on [data], I expect [outcome]'"
```

---

### Step 5: Interviewer Signals (1 minute)

Read between the lines:

```
## Interviewer Engagement Signals

**Positive signals I noticed:**
- ✅ [Signal 1: e.g., "Took detailed notes during my metrics section"]
- ✅ [Signal 2: e.g., "Asked follow-up questions showing genuine interest"]
- ✅ [Signal 3: e.g., "Smiled and nodded when I explained prioritization"]

**Concerning signals I noticed:**
- ⚠️ [Signal 1: e.g., "Cut me off twice - may have been rambling"]
- ⚠️ [Signal 2: e.g., "Didn't ask follow-ups on my solution"]
- ⚠️ [Signal 3: e.g., "Checked phone during my answer"]

**Questions they asked at the end:**
- [Question 1: e.g., "Tell me about a time you failed"]
  → Meaning: [They want to test humility/learning]
- [Question 2]

**My questions I asked:**
- [My question 1]
  → Their response: [Summary]
- [My question 2]
  → Their response: [Summary]
```

---

### Step 5.5: Prep vs Performance Comparison

If the PM ran `/interview-prep` before this interview, compare:

**Planned strengths vs Actual:**
- What frameworks did you plan to use? Did you use them?
- What company-specific research did you prepare? Did it come up?
- What stories did you plan to tell? Did you tell them?

**Format in output:**
| Planned (from /interview-prep) | Actual Performance | Gap |
|-------------------------------|-------------------|-----|
| Use CIRCLES for product sense | Used CIRCLES clearly | None |
| Cite company's 3M DAU metric | Forgot to mention specific numbers | Specificity gap |
| Tell DataStack churn reduction story | Told it but rambled (3 min vs planned 2 min) | Communication gap |

This comparison accelerates learning by making the gap between intention and execution visible.

---

### Step 6: Pattern Recognition (Multi-Interview)

**Before generating feedback, check `outputs/interview-feedback/` for previous debrief files.**

If previous debriefs are found, show a trend analysis:

```
## Cross-Interview Pattern Analysis

**Previous debriefs found:** [N] files in outputs/interview-feedback/

### Trend Report (across last [N] interviews)

| Dimension | Interview 1 | Interview 2 | Interview 3 | Trend |
|-----------|-------------|-------------|-------------|-------|
| Framework Usage | X/5 | X/5 | X/5 | Improving / Flat / Declining |
| Specificity | X/5 | X/5 | X/5 | Improving / Flat / Declining |
| Creativity | X/5 | X/5 | X/5 | Improving / Flat / Declining |
| Communication | X/5 | X/5 | X/5 | Improving / Flat / Declining |
| Product Sense | X/5 | X/5 | X/5 | Improving / Flat / Declining |

**Consistent strengths across interviews:**
- [Pattern 1: e.g., "Always strong on user segmentation"]
- [Pattern 2: e.g., "Metrics definition consistently praised"]

**Recurring weaknesses (these need focused practice):**
- [Pattern 1: e.g., "Keep running over time on execution questions"]
- [Pattern 2: e.g., "Weak on competitive analysis section"]

**Company-specific insights:**
- [Company A]: [What they cared most about]
- [Company B]: [What they cared most about]

**Interview type insights:**
- **Product Sense:** [What works for me, what doesn't]
- **Execution:** [What works for me, what doesn't]
- **Behavioral:** [What works for me, what doesn't]
```

If no previous debriefs exist, note: "This is your first tracked debrief. After 3+ debriefs, I'll show you trend analysis and patterns."

---

### Step 7: What to Improve for Next Time (Specific Drills)

Based on your lowest-scoring dimensions, here are targeted practice drills:

```
## Improvement Drills by Dimension

### If low on Framework Usage (scored 1-3):
**Practice drill:** Pick 3 products you use daily. For each, answer "How would you
improve this product?" using the 5-Step framework. Time yourself at 25 min each.
- Day 1: Practice with timer, write out structure before speaking
- Day 2: Practice out loud without notes, just framework cards
- Day 3: Record yourself answering, review for structure breaks
**Key habit:** Always say your framework out loud before diving in:
"I'll approach this in 4 steps: first the user, then the problem, then solutions, then metrics."

### If low on Specificity (scored 1-3):
**Practice drill:** Prepare 5 STAR stories with exact metrics.
- For each story, fill in: "This resulted in [X]% improvement in [metric],
  affecting [N] users, saving/generating $[amount]"
- If you don't have exact numbers, estimate and say "approximately"
- Research 5 products: know their DAU, revenue, growth rate, key metrics
**Key habit:** Before every claim, ask yourself: "Can I put a number on this?"

### If low on Creativity (scored 1-3):
**Practice drill:** For any product question, force yourself to generate 5 solutions
before evaluating. At least 2 must be "non-obvious."
- Study product teardowns (Lenny's Newsletter, First Round Review)
- Practice "second-order thinking": "If we do X, then Y happens, which causes Z"
- Look at how other industries solved similar problems
**Key habit:** After your first solution idea, ask: "What would surprise the interviewer?"

### If low on Communication (scored 1-3):
**Practice drill:** Record yourself answering 3 questions. Review for:
- Filler words count (um, uh, like, you know)
- Longest sentence (aim for under 20 words)
- Did you pause before answering? (good) or start rambling? (bad)
- Eliminate hedging: replace "I think maybe" with "I believe" or "The data suggests"
**Key habit:** Take a 5-second pause before answering. Silence is better than filler.

### If low on Product Sense (scored 1-3):
**Practice drill:** For 5 products, write a one-paragraph user story:
"[User type] needs to [job] because [motivation]. Today they [current solution]
which is painful because [friction]. A great solution would [outcome]."
- Read 10 user reviews on App Store/G2 for products you're interviewing about
- Practice explaining WHY a feature exists, not just WHAT it does
**Key habit:** Start every answer with the user, not the product.
```

---

### Step 8: Action Items for Next Interview (1 minute)

Turn insights into concrete improvements:

```
## Next Interview Action Items

**Before next interview:**
- [ ] [Action 1: e.g., "Practice 3 execution questions under 25 min"]
- [ ] [Action 2: e.g., "Prepare 2 data points about competitor products"]
- [ ] [Action 3: e.g., "Record myself answering and check for filler words"]

**During next interview:**
- [ ] [Behavior 1: e.g., "Use timer to cap problem def at 5 min"]
- [ ] [Behavior 2: e.g., "Always ask 'How much time do I have?' upfront"]
- [ ] [Behavior 3: e.g., "End every answer with business impact"]

**Follow-up needed:**
- [ ] [Task 1: e.g., "Send thank you email within 24 hours"]
- [ ] [Task 2: e.g., "Connect with interviewer on LinkedIn"]
- [ ] [Task 3: e.g., "Research their recent product launches for next round"]
```

---

## Output Format

```markdown
# Interview Debrief: [Company] - [Interview Type]

**Date:** [Date] | **Duration:** [X min] | **Interviewer:** [Name/Role]

---

## Quick Summary

**Overall feeling:** [Great / Good / Okay / Rough]

**Overall score:** ⭐⭐⭐⭐ (4/5)

**Advance to next round?** [Likely / Maybe / Unlikely]

---

## Questions Asked

1. **[Question 1]**
   - My approach: [Framework used, structure]
   - Score: ⭐⭐⭐⭐⭐
   - What went well: [Specific strength]
   - What to improve: [Specific weakness]

2. **[Question 2]**
   - My approach: [Framework used, structure]
   - Score: ⭐⭐⭐
   - What went well: [Specific strength]
   - What to improve: [Specific weakness]

[Continue for all questions]

---

## Performance Breakdown

| Dimension | Score | Notes |
|-----------|-------|-------|
| Structure & Clarity | ⭐⭐⭐⭐ | Used framework but could be crisper |
| Depth & Rigor | ⭐⭐⭐⭐⭐ | Great data points, specific examples |
| Time Management | ⭐⭐⭐ | Went over on Q1, rushed on Q2 |
| Metrics & Data | ⭐⭐⭐⭐⭐ | Specific targets, good rationale |
| Communication | ⭐⭐⭐⭐ | Clear but used filler words |

---

## What Worked

✅ Used 5-step Product Sense framework consistently
✅ Asked clarifying questions before diving in
✅ Specific metrics with targets (not vague)

---

## What to Improve

❌ Time management - spent too long on problem definition
❌ Didn't connect solution to business metrics clearly
❌ Used tentative language ("might", "could") instead of confident

---

## Interviewer Signals

**Positive:**
- Took detailed notes during metrics section
- Asked thoughtful follow-ups

**Concerning:**
- Seemed to check phone during answer
- Cut me off once (may have been rambling)

---

## Action Items

**For next interview:**
- [ ] Practice with timer - cap sections at target time
- [ ] Always end with "user value → business value" connection
- [ ] Replace tentative language with data-backed confidence

**Follow-up:**
- [ ] Send thank you email by [date]
- [ ] Connect on LinkedIn

---

**Next interview:** [Date if scheduled, or "TBD"]
**Next interview type:** [Product Sense / Execution / etc.]
```

---

## Special Cases

### After Rejection

```
## Rejection Debrief

**Rejection type:** [After screening / After onsite / After final round]

**Official reason given:** [If any]

**My hypothesis on why:**
- [Hypothesis 1: e.g., "Weak on technical depth questions"]
- [Hypothesis 2: e.g., "Better candidate with more relevant experience"]
- [Hypothesis 3: e.g., "Company culture fit concerns"]

**What I learned:**
- [Learning 1]
- [Learning 2]

**How I'll improve:**
- [Specific action 1]
- [Specific action 2]

**Apply these learnings at:** [Next company/interview]
```

---

### After Advancing to Next Round

```
## Advancement Debrief

**Next round:** [Type of interview]
**Scheduled for:** [Date/time]

**What worked in this round (do more of):**
- [Strength 1]
- [Strength 2]

**What to prepare for next round:**
- [Prep item 1: e.g., "They mentioned wanting deeper metrics analysis"]
- [Prep item 2: e.g., "Next round is with engineering - brush up on technical"]

**Research to do before next round:**
- [ ] [Task 1]
- [ ] [Task 2]
```

---

### After Take-Home Assignment Presentation

```
## Assignment Presentation Debrief

**Assignment type:** [Product spec / Data analysis / Design exercise / etc.]

**Time invested:** [Hours spent on assignment + presentation]

**Presentation format:** [Slides / Doc walkthrough / Live demo / etc.]

**Questions they asked:**
1. [Question 1 - and how I answered]
2. [Question 2 - and how I answered]

**What they liked (based on feedback/reactions):**
- [Positive 1]
- [Positive 2]

**What they pushed back on:**
- [Concern 1: e.g., "Questioned my prioritization approach"]
- [Concern 2]

**If I could redo the assignment:**
- [Change 1]
- [Change 2]
```

---

## Pro Tips

1. **Write immediately:** Don't wait 30 min or you'll forget half
2. **Be specific:** "I rambled" → "Spent 12 min on intro instead of 5 min"
3. **Track patterns:** After 5 interviews, review all debriefs for themes
4. **No sugar-coating:** Brutal honesty helps more than fake positivity
5. **Celebrate wins:** Note what worked so you can repeat it
6. **Quantify:** "Felt rushed" → "Had 5 min left, needed 10 min"
7. **Ask for feedback:** If recruiter offers, take detailed notes

---

## Common Mistakes to Avoid

❌ Waiting hours/days to debrief (memory fades)
✅ Capture within 15 minutes while fresh

❌ Generic notes ("did okay on metrics")
✅ Specific observations ("used DAU/MAU ratio, interviewer nodded")

❌ Only noting negatives (demotivating)
✅ Balance strengths and weaknesses

❌ No action items (passive reflection)
✅ Concrete improvements for next time

❌ Ignoring patterns across interviews
✅ Review all debriefs monthly for themes

---

## Questions to Ask Yourself

After every interview debrief:

1. **Preparation:** Did I do enough company research?
2. **Structure:** Did I use a framework or wing it?
3. **Specificity:** Were my metrics and examples concrete?
4. **Time:** Did I manage time well or rush/ramble?
5. **Confidence:** Did I sound certain or hedge too much?
6. **Learning:** What's the ONE thing I'll do differently next time?

---

## Integration with Other Skills

**Before interview:**
- `/interview-prep` - Preparation checklist

**During job search:**
- Track all feedback in `outputs/interview-feedback/`
- Monthly review: Look for patterns
- Adjust prep based on recurring weaknesses

**After getting offer:**
- Review all debriefs to see what worked
- Document lessons for future job searches

---

---

## Output Quality Self-Check

Before delivering the debrief, verify:

| Check | Criteria | Pass? |
|-------|----------|-------|
| **Emotional check-in completed** | Asked how the PM is feeling before diving into scoring | [ ] |
| **5 dimensions scored** | All 5 core dimensions (Framework, Specificity, Creativity, Communication, Product Sense) have a 1-5 score | [ ] |
| **Scores are honest** | Scores reflect actual performance, not what the PM wants to hear | [ ] |
| **Specific examples** | Each strength and weakness cites a specific moment from the interview, not generalities | [ ] |
| **Improvement drills provided** | At least 1 targeted drill for the lowest-scoring dimension | [ ] |
| **Pattern check done** | Checked `outputs/interview-feedback/` for prior debriefs and showed trends if found | [ ] |
| **Action items concrete** | Next steps are specific and time-bound, not vague ("practice more") | [ ] |
| **Follow-up tasks included** | Thank-you email reminder, LinkedIn connection, next round prep noted | [ ] |
| **Output file saved** | Debrief saved to `outputs/interview-feedback/[date]-[company]-debrief.md` | [ ] |

**If any check fails, address it before delivering the output.**

---

Remember: Every interview is data. Even rejections teach you something. Capture it all, learn fast, and improve between each round.

---

**Sources:**
- [Crack the Product Execution Interview](https://www.news.aakashg.com/p/crack-the-product-execution-interview)
- [Master the Product Sense Interview](https://www.news.aakashg.com/p/master-the-product-sense-interview)
- [Real Answers to Real PM Interview Questions](https://www.news.aakashg.com/p/real-answers-to-real-pm-interview)
