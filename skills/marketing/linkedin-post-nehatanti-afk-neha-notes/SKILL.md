---
name: linkedin-post
description: Generate LinkedIn posts about work sessions and technical accomplishments. Use when creating developer-focused content or sharing technical insights.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
user-invocable: true
---

# LinkedIn Post

## Purpose

Generate a LinkedIn post based on the current work session - what was built, changed, or accomplished.

## When to Use

- When user runs `/linkedin` or asks for a LinkedIn post
- After completing a significant feature or task
- To share technical learnings or insights

## Workflow

### Phase 1: Analyze Session Context

**Extract from conversation history:**

1. What task was accomplished?
2. What files were changed/created?
3. What problem was solved?
4. What approach was taken?
5. Any interesting technical decisions?

**Run git commands to understand scope:**

```bash
git diff --stat HEAD~5
git log --oneline -5
```

### Phase 2: Identify the Story

Based on session analysis, identify:

| Element          | Question to Answer                       |
| ---------------- | ---------------------------------------- |
| **The Hook**     | What's the surprising/interesting angle? |
| **The Problem**  | What challenge was being solved?         |
| **The Insight**  | What did you learn or realize?           |
| **The Takeaway** | What can others learn from this?         |

### Phase 3: Draft Post

**Structure:**

```
[Hook - 1-2 lines that stop the scroll]

[Context - What you were working on]

[The interesting part - Technical insight, unexpected learning, or aha moment]

[Takeaway - What others can learn]

[Engagement prompt - Question or call to discussion]
```

**Length:** 150-300 words (LinkedIn sweet spot)

### Phase 4: Self-Review

Apply anti-patterns check:

- [ ] No "Excited to announce" or marketing clichés
- [ ] No buzzwords without substance
- [ ] Has a clear hook in the first line
- [ ] Creates insight, not just description
- [ ] Invites conversation
- [ ] Appropriate technical depth for LinkedIn audience

### Phase 5: Present Options

Offer the user:

1. **Draft post** - Ready to copy
2. **Alternate angles** - 2-3 different hooks/approaches
3. **Revision requests** - Ask what to adjust

## Output Format

```markdown
## 📝 LinkedIn Post Draft

{post content}

---

### Alternative Angles

**Option A:** {different hook focusing on X}
**Option B:** {different hook focusing on Y}

---

**Want me to:** Adjust tone? | Add more detail? | Make it shorter? | Try a different angle?
```

## Dynamic Content Sources

The skill derives ALL content from:

| Source                | What to Extract                    |
| --------------------- | ---------------------------------- |
| Conversation history  | Task accomplished, problems solved |
| Git diff/log          | Files changed, commit messages     |
| File contents read    | Technical details, code patterns   |
| User's explicit input | Any additional context provided    |

**Never hardcode** project names, tech stack, or domain assumptions - discover them from the session.

## Anti-Patterns to Avoid

- "Excited to announce" and similar marketing clichés
- Buzzwords without substance (synergy, leverage, cutting-edge)
- Posts that only describe without creating insight
- Missing hook in the first line
- No clear call to engagement
- Too technical for the platform audience
- Too vague to be interesting
