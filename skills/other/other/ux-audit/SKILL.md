---
name: ux-audit
description: Perform comprehensive UX audits on pages, components, or features. Use when the user asks to "audit UX", "review usability", "evaluate the interface", "UX review", or wants a systematic evaluation of user experience quality.
---

# UX Audit Skill

Perform systematic UX audits using Nielsen's heuristics and UX best practices.

## When to Use

- Reviewing a page or feature before release
- Identifying usability issues
- Evaluating design decisions
- Comparing against UX standards
- Preparing for user testing

## Audit Framework

### 1. Heuristic Evaluation

Evaluate against Nielsen's 10 usability heuristics:

| Heuristic | Question to Ask |
|-----------|-----------------|
| System status | Does the user know what's happening? |
| Real world match | Does it speak the user's language? |
| User control | Can users undo/escape easily? |
| Consistency | Does it follow conventions? |
| Error prevention | Does design prevent mistakes? |
| Recognition | Is information visible vs. remembered? |
| Flexibility | Are there shortcuts for experts? |
| Minimalism | Is every element necessary? |
| Error recovery | Are errors clear and recoverable? |
| Help | Is assistance available when needed? |

### 2. Visual Hierarchy Check

- Is the most important element most prominent?
- Does the eye flow logically?
- Are related items grouped?
- Is there appropriate white space?

### 3. Interaction Audit

- Are clickable elements obvious?
- Is feedback immediate?
- Are loading states handled?
- Are empty states designed?

### 4. Content Evaluation

- Is copy clear and concise?
- Is terminology user-friendly?
- Are labels descriptive?
- Are CTAs action-oriented?

## Output Format

```markdown
## UX Audit: [Feature/Page Name]

### Summary Score
[Overall usability rating: Poor / Fair / Good / Excellent]

### Heuristic Scores
| Heuristic | Score (1-5) | Key Issue |
|-----------|-------------|-----------|

### Critical Issues
- [Issue requiring immediate attention]

### Recommendations
| Priority | Issue | Recommendation | Effort |
|----------|-------|----------------|--------|
| P0 | ... | ... | Low/Med/High |

### Positive Patterns
- [What's working well]
```

## Integration

Works best with:
- `ux-expert` agent for deep analysis
- `accessibility-check` skill for WCAG compliance
- `journey-map` skill for flow context
