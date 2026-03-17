---
name: next
description: Get the next recommended problem based on your weak patterns and mistake history. Use after completing a problem.
argument-hint: [difficulty: easy|medium|hard] (optional)
allowed-tools: Read, Glob, Grep
---

# Next - What Should You Work On?

The user wants a recommendation for what to practice next.

**Difficulty preference:** $ARGUMENTS (optional - easy, medium, hard)

## Gather Context
Check:
- `data/mistakes.json` for weak areas
- `data/session.json` for recently completed problems
- What patterns they've practiced

## Give a Personalized Recommendation

Talk to them like a coach planning their training:

**If they have mistake history:**
"Looking at your history, you've been struggling with [category - e.g., "off-by-one errors" or "recognizing DP patterns"].

I'd recommend: **[Problem Name]** ([difficulty])
- It's a [pattern] problem that'll give you practice with [specific weakness]
- [One sentence about why this problem is good for them]

Other options if you want variety:
- [Problem 2] - [pattern] - [difficulty]
- [Problem 3] - [pattern] - [difficulty]

Want to start? Just say `/s [problem name]`"

**If they've been doing well:**
"Nice work on [recent problems]. Time to level up.

Try: **[Problem Name]** ([difficulty])
- It combines [pattern 1] with [pattern 2], which is common in interviews
- [Why it's a good progression]

Or if you want something different:
- [Alternative 1]
- [Alternative 2]"

**If no history:**
"Since we're just getting started, let's establish a baseline.

Start with: **Two Sum** (easy)
- It's the classic HashMap problem
- Good way to see how you approach problems

Then we can calibrate from there. `/s two sum` when you're ready."

## Be Specific About Why
Don't just list problems. Explain why each one is relevant to their growth.

## End with Action
Always make it easy to start: "Say `/s [name]` when you're ready."
