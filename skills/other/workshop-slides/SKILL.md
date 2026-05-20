---
name: workshop-slides
description: Create a teaching deck for a workshop or training session. Structure includes title/agenda, concept slides (1 concept per slide), exercise slides (interactive), summary/recap, and resources. Each slide has title, content, and presenter notes. Designed for 60-90 minute sessions. Use when user needs "workshop slides", "training deck", "teaching presentation", or "session slides".
---

## Load Context First

Before executing this skill, read the following files from the project folder if they exist:

1. **USER.md** — who the user is, how they think, how they work
2. **BUSINESS.md** — their business, products, positioning, brand voice, content strategy
3. **ICP.md** — their ideal customer, their language, their fears, what makes them buy
4. **Voice or brand voice skill** — look for any installed skill related to voice, tone, or brand voice and apply it automatically
5. Any additional context provided by the user in this session

Use all context silently. Do not reference or summarize files unless asked.

---

# Workshop Slides Builder

**Purpose:** Create a teaching-focused slide deck for workshops and training sessions. Unlike pitch decks (which persuade) or presentations (which inform), workshop slides teach — they include interactive exercises, concept builds, and structured learning.

## Session Design Principles

1. **One concept per slide** — don't cram
2. **Exercise every 15-20 minutes** — people learn by doing
3. **Build complexity gradually** — start simple, add layers
4. **Show, then do** — teach the concept, then let them practice
5. **Recap frequently** — summarize after each section

## Required Input

- **Workshop topic** and learning outcomes
- **Duration** (60 or 90 minutes)
- **Audience level** (beginner, intermediate, advanced)
- **Key concepts** to teach (3-5 for 60 min, 4-7 for 90 min)

## Slide Structure

### Opening Block (5-10 minutes)

**Slide 1: Title**
- Workshop name, presenter, date
- One-line description of what attendees will learn

**Slide 2: Agenda**
- Numbered list of topics/sections with time estimates
- "By the end, you'll be able to [specific outcomes]"

**Slide 3: Ground Rules / Setup**
- Any tools or materials needed
- Participation expectations
- How Q&A will work

### Teaching Blocks (15-20 minutes each)

For each core concept:

**Concept Slide:**
- **Title:** [Concept name]
- **Content:** Definition or explanation (1-3 key points)
- **Visual:** Diagram, framework, or example
- **Presenter notes:** How to explain this concept, examples to give, common questions

**Example Slide:**
- **Title:** "[Concept] in Action"
- **Content:** A specific, real-world example showing the concept applied
- **Before/After** or **Step-by-step** walkthrough
- **Presenter notes:** Walk through this example live. Point out key decisions.

**Exercise Slide:**
- **Title:** "Your Turn: [Activity Name]"
- **Instructions:** What to do (specific, numbered steps)
- **Time:** How long they have
- **Expected output:** What they should have when done
- **Presenter notes:** How to facilitate. What to look for. Common mistakes to address.

### Closing Block (5-10 minutes)

**Summary Slide:**
- Key takeaways from the entire session (numbered)
- One sentence per concept covered

**Resources Slide:**
- Links, tools, recommended reading
- How to continue learning
- Where to get help

**Q&A / CTA Slide:**
- Open for questions
- Next steps or follow-up opportunities
- Contact information

## Output Format

```markdown
# Workshop: [Title]

**Duration:** [60/90] minutes
**Audience:** [Level]
**Outcomes:** By the end, attendees will be able to:
1. [Outcome 1]
2. [Outcome 2]
3. [Outcome 3]

---

## Slide 1: Title
### [Workshop Name]
*[One-line description]*

[Presenter Name] | [Date]

**Presenter notes:** Welcome, introduce yourself, set expectations.

---

## Slide 2: Agenda
### What We'll Cover

1. [Topic 1] — [X] min
2. [Topic 2] — [X] min
3. [Exercise] — [X] min
4. [Topic 3] — [X] min
5. [Exercise] — [X] min
6. [Wrap-up & Q&A] — [X] min

**Presenter notes:** Walk through the agenda. Set time expectations.

---

## Slide 3: [Concept 1 Name]
### [Clear title]

[Content — definition, framework, or key points]

**Presenter notes:** [How to teach this — examples, analogies, common questions]

---

## Slide 4: [Concept 1] in Action
### Example

[Detailed example showing the concept applied]

**Presenter notes:** [Walk through this step by step]

---

## Slide 5: Exercise 1
### Your Turn: [Activity Name]

**Instructions:**
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Time:** [X] minutes
**Output:** [What they should produce]

**Presenter notes:** [Facilitation tips — circulate, answer questions, watch for common mistakes]

---

[Continue for all concepts and exercises...]

---

## Slide [N-2]: Key Takeaways
### What We Covered

1. [Takeaway 1]
2. [Takeaway 2]
3. [Takeaway 3]
4. [Takeaway 4]

---

## Slide [N-1]: Resources
### Continue Learning

- [Resource 1 — link/description]
- [Resource 2]
- [Resource 3]

---

## Slide [N]: Q&A
### Questions?

[Contact info]
[Follow-up opportunity]

---

## Facilitator Guide

**Timing breakdown:**
| Section | Duration | Slides |
|---------|----------|--------|
| Opening | [X] min | 1-3 |
| Concept 1 + Exercise | [X] min | 4-7 |
| Concept 2 + Exercise | [X] min | 8-11 |
| Closing | [X] min | [N-2] - [N] |

**Materials needed:** [List]
**Common challenges:** [What might go wrong and how to handle it]
```

## Quality Checklist

- [ ] One concept per slide (no cramming)
- [ ] Exercise every 15-20 minutes
- [ ] All slides have presenter notes
- [ ] Exercises have clear instructions, time limits, and expected outputs
- [ ] Summary slide recaps key takeaways
- [ ] Resources slide gives next steps
- [ ] Timing adds up to session duration
- [ ] Facilitator guide included
- [ ] Designed for audience level specified
- [ ] Based on user's expertise (not fabricated content)
