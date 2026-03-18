---
name: project-retrospective
description: Generate LESSONS.md retrospective files that capture institutional knowledge, especially failures. Use when closing out journalism projects, investigations, events, or publications. Includes templates for research projects, event post-mortems, editorial tools, and publications.
---

# Project retrospective writer

Create LESSONS.md files that capture institutional knowledge, especially failures. Think like a journalist writing about your own project—be specific, be honest, name the actual mistakes.

## When to use

- After completing an investigation or project
- When shutting down or pausing a publication
- Post-mortem for events
- Handing off a project to someone else
- Annual review of ongoing initiatives

## The critical section: "The real problem"

This is the most valuable part of any retrospective. It answers:

> "What did we THINK we were building vs. what was ACTUALLY needed?"

**Good example:**
> We built a comprehensive tagging system when users just needed full-text search. Three weeks on features no one used.

**Bad example (too generic):**
> We learned the importance of user research.

## Template structure

```markdown
# LESSONS.md

## Project
- **Name:** [Project name]
- **Dates:** [Start - End]
- **Status:** [Completed / Abandoned / Ongoing]
- **Author:** [Your name]

## Summary
[One paragraph: what it did, what impact it had, why it matters]

## What worked

### Technical wins
- [Specific decision and WHY it worked]
- [Tool/pattern that saved time]

### Process wins
- [Methodology that helped]
- [Communication pattern that worked]

## What didn't work

### Critical failures
- [Thing that blocked progress - be specific]
- [Wrong assumption and its cost]

### Technical debt
- [Shortcut that hurt later]
- [Complexity that wasn't needed]

### External factors
- [Things outside your control that impacted project]

## The real problem
[This is the most important section]

What we thought: [Initial assumption]
What was actually needed: [Reality]
The gap cost us: [Time/effort/money wasted]

## Recommendations

### If continuing this project
1. [First priority]
2. [Second priority]
3. [Third priority]

### If starting fresh
- [What to do differently]
- [What to skip entirely]

### Tech stack verdict
- **Keep:** [Tools that worked well]
- **Replace:** [Tools that caused problems]
- **Add:** [Tools you wished you had]

## Reusable artifacts

| Component | Why it's valuable |
|-----------|------------------|
| [Name] | [Specific reuse potential] |
| [Name] | [Why someone else should use this] |

## Questions for next time
- [Unanswered questions worth investigating]
- [Things you'd research before starting]
```

## Voice guidelines

- Honest, specific, slightly self-deprecating
- Like explaining to a friend why the project took twice as long
- No corporate speak or blame-shifting
- Name specific mistakes, not vague "challenges"

## What to include vs exclude

| Include | Exclude |
|---------|---------|
| Specific failures with context | Vague "learnings" |
| Actual time/cost of mistakes | Blame for individuals |
| Tools that helped or hurt | Generic best practices |
| Decisions you'd reverse | Obvious statements |
| Surprising discoveries | Information in other docs |

## The specificity test

For each item in "What didn't work," ask:
- Can I name the specific decision?
- Can I quantify the impact?
- Would this help someone avoid the same mistake?

If no to any → Be more specific.

## Examples of good vs bad entries

**Bad - too vague:**
> - Communication could have been better
> - We underestimated the complexity
> - Testing was insufficient

**Good - specific and actionable:**
> - Skipped schema validation on data files. Cost: 3 hours debugging a typo that caused silent failures.
> - Built custom date picker when browser native input would have worked. 2 days wasted.
> - No error messages when data fails to load—users just see blank screen.

## "The real problem" examples

**Weak:**
> We learned that requirements can change.

**Strong:**
> We built an admin dashboard for editors when they actually needed a Slack bot. They live in Slack—forcing them to open a web app was friction they'd never accept. The dashboard has 2 monthly active users; the Slack bot prototype we built in a day has 47.

## Red flags in your writing

If you find yourself writing these, stop and be more specific:
- "Communication is key"
- "We learned the importance of..."
- "Going forward, we should..."
- "Challenges included..."
- "There were some issues with..."

These are placeholders for real insights. Replace them.

## Journalism-specific templates

Templates are in the `templates/` directory:

| Template | Use for |
|----------|---------|
| `research-project.md` | Investigations, data journalism projects |
| `event.md` | Conferences, workshops, campaigns |
| `publication.md` | Newsletters, podcasts, ongoing content |
| `editorial-tool.md` | Newsroom software, AI tools |

### Template selection

```
What kind of project?
├── Investigation/analysis → research-project.md
├── Conference/workshop → event.md
├── Newsletter/podcast → publication.md
└── Newsroom tool → editorial-tool.md
```

---

*The best retrospectives are written by people who got burned and want to save others from the same fate.*
