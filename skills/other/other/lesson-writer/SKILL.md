---
name: lesson-writer
description: Write an individual course lesson with learning objectives, teaching content with examples, key takeaways, exercise/action step, and transition to next lesson. Use when user wants to "write a lesson", "create lesson content", or needs to flesh out a specific lesson from a course outline.
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

# Lesson Writer

**Purpose:** Write a complete, engaging course lesson that teaches one specific skill or concept. The lesson should be clear enough for a beginner yet valuable enough for someone with experience.

## Required Input

- **Lesson title and number** (e.g., "Lesson 2.3: Building Your First Content Calendar")
- **Learning objective** (what the student will be able to do)
- **Module context** (what came before, what comes after)
- **Key content** (the knowledge to teach — from user's expertise)

## Lesson Structure

```markdown
# Lesson [X.X]: [Title]

**Module:** [Module Name]
**Learning objective:** By the end of this lesson, you will be able to [specific, measurable skill].
**Estimated time:** [X] minutes

---

## Why This Matters

[2-3 sentences connecting this lesson to the student's goals. Answer: "Why should I care about this?" before they ask it.]

---

## The Concept

[Core teaching content — 300-600 words]

**Structure the teaching as:**
1. **Introduction** — What is this concept? (Define it simply)
2. **Why it works** — The reasoning behind it
3. **How to do it** — Step-by-step instructions or framework
4. **Example** — A concrete example showing the concept in action
5. **Common mistakes** — What to watch out for

[Use headers, bullets, and visual breaks for scannability]

---

## Example in Action

[A detailed, specific example showing the concept applied. Walk through it step by step so the student can see exactly what "doing it right" looks like.]

**Before:** [What it looks like without this skill]
**After:** [What it looks like with this skill applied]

---

## Key Takeaways

1. [Takeaway #1 — one sentence]
2. [Takeaway #2 — one sentence]
3. [Takeaway #3 — one sentence]
4. [Takeaway #4 — one sentence (optional)]
5. [Takeaway #5 — one sentence (optional)]

---

## Your Action Step

**Do this now:** [Specific exercise or action the student completes before moving on]

[Detailed instructions for the exercise — clear enough to follow without help]

**Expected outcome:** [What they should have when done]
**Time needed:** [X] minutes

---

## Up Next

[1-2 sentences transitioning to the next lesson. Create a natural bridge — "Now that you can [this lesson's skill], you're ready to [next lesson's topic]..."]
```

## Quality Checklist

- [ ] Learning objective is specific and measurable
- [ ] "Why This Matters" connects to student's real-world goals
- [ ] Teaching content is clear, structured, and scannable
- [ ] At least one detailed example showing the concept in action
- [ ] Before/after comparison demonstrates the difference
- [ ] Key takeaways are concise and actionable (3-5 bullets)
- [ ] Action step is specific enough to complete independently
- [ ] Transition to next lesson creates momentum
- [ ] Tone is encouraging and clear (teacher, not lecturer)
- [ ] Based on user's actual expertise (not fabricated)
