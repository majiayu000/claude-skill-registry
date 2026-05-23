---
name: star-story-extraction
description: |
  TRIGGERS: "interview prep", "STAR story", "behavioral interview", "how do I talk about this?",
  interview stories, situation task action result, tell me about a time, problem solving story.
  USE WHEN: Completing significant tasks, preparing for interviews, documenting achievements.
  PROVIDES: STAR format stories, interview-ready narratives, behavioral interview preparation.
---

# STAR Story Extraction

> "Every feature you build is an interview answer waiting to be told."

## Purpose

Transform completed work into compelling interview stories using the STAR method. These stories demonstrate real problem-solving ability.

---

## The STAR Method

| Component | Question | Focus |
|-----------|----------|-------|
| **S**ituation | "What was the context?" | Set the scene, explain the problem |
| **T**ask | "What were YOU responsible for?" | YOUR specific role and responsibility |
| **A**ction | "What did YOU do?" | Specific technical actions YOU took |
| **R**esult | "What was the outcome?" | Impact, metrics, improvements |

---

## Extraction Flow

### Step 1: Identify the Story Type

What kind of problem did you solve?

| Story Type | Good For Questions Like |
|------------|------------------------|
| Technical challenge | "Tell me about a difficult bug you solved" |
| Feature implementation | "Describe a feature you're proud of" |
| Performance optimization | "How did you improve system performance?" |
| Security fix | "Tell me about a security issue you addressed" |
| Refactoring | "Describe a time you improved code quality" |
| Learning curve | "Tell me about a time you learned something quickly" |

### Step 2: Guide Through STAR

#### Situation (2-3 sentences)
> "What was the context? What problem or challenge existed before you started?"

**Good elements:**
- Business context (why it mattered)
- Technical constraints
- Scale/impact of the problem

**Avoid:**
- Too much background
- Irrelevant details
- Blaming others

#### Task (1-2 sentences)
> "What were YOU specifically responsible for? What was your role?"

**Good elements:**
- Clear ownership
- Specific scope
- Why you were the one to do it

**Avoid:**
- "We did this" (use "I")
- Vague responsibilities

#### Action (The meat - 3-5 sentences)
> "Walk me through the specific steps YOU took. Be technical."

**Good elements:**
- Specific technologies used
- Problem-solving approach
- Trade-offs considered
- Technical decisions made

**Avoid:**
- Glossing over the how
- Buzzword soup
- "I just implemented it"

#### Result (1-2 sentences)
> "What was the outcome? Can you quantify the impact?"

**Good elements:**
- Metrics where possible (50% faster, 0 bugs in production)
- Business impact
- What you learned

**Avoid:**
- "It worked" (too vague)
- No mention of impact

---

## Story Quality Checklist

- [ ] Uses "I" not "we" (shows ownership)
- [ ] Includes specific technologies
- [ ] Demonstrates problem-solving
- [ ] Shows technical depth
- [ ] Has measurable result if possible
- [ ] Is 2-3 minutes when spoken
- [ ] Answers the implied "why hire you?"

---

## Story Template

```markdown
# STAR Story: [Feature/Problem Name]

**Date:** [When completed]
**Type:** [Technical Challenge / Feature / Performance / Security / Refactor]

## Situation
[The context. What problem existed? Why did it matter?]

## Task
[YOUR specific responsibility. What were YOU asked to do?]

## Action
[The specific steps YOU took. Be technical. Show your thought process.]

## Result
[The outcome. Metrics if possible. What impact did it have?]

---

## Interview Variations

This story can answer:
- "Tell me about a time you [X]"
- "Describe a challenging [Y] you worked on"
- "How did you approach [Z]?"

## Key Technical Points to Mention
- [Technology/pattern 1]
- [Technology/pattern 2]
- [Decision/trade-off made]
```

---

## Example: Good vs Bad STAR

### Bad Story
> "I built a login form. It had validation. It worked."

Problems: No context, no challenge, no depth, no impact.

### Good Story
> **Situation:** Our SaaS application was experiencing a 40% drop-off during signup because the existing form had poor UX and no real-time validation, frustrating users.
>
> **Task:** I was responsible for rebuilding the entire authentication flow, focusing on reducing friction while maintaining security.
>
> **Action:** I implemented a multi-step form with real-time validation using React Hook Form for performance. I added JWT authentication with secure refresh token rotation to handle long sessions. The key challenge was balancing security (short token expiry) with UX (no jarring logouts), which I solved by implementing silent refresh 5 minutes before expiry.
>
> **Result:** Sign-up completion improved by 35%, and we've had zero authentication-related security incidents since launch. The pattern I built is now used across our other products.

---

## Socratic Story Questions

Guide the junior with these:

1. **Finding the story:** "What was the hardest part of this feature?"
2. **Adding depth:** "Walk me through your debugging process when X happened."
3. **Showing ownership:** "What decision did YOU make that shaped this?"
4. **Quantifying results:** "How would you measure the impact of this work?"
5. **Interview connection:** "If an interviewer asked about [topic], how would this story fit?"

---

## Common Story Mistakes

| Mistake | Fix |
|---------|-----|
| "We built..." | Use "I implemented..." |
| Too long (10+ minutes) | Cut to 2-3 minutes |
| No technical depth | Add specific technologies and decisions |
| No result | Always end with impact |
| Only happy path | Include challenges overcome |

---

## Save Location

Stories are saved to:
```
ownyourcode/career/stories/[date]-[feature-name].md
```

Example: `ownyourcode/career/stories/2026-01-15-jwt-auth.md`
