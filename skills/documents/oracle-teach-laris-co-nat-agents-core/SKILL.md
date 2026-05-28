---
name: oracle-teach
description: Generate learning materials from mature patterns. Use when user says "teach me", "explain this pattern", "create a guide", "how does X work", "document this for others". Auto-trigger when sharing knowledge with team.
---

# Oracle Teach Skill

> Transform mature knowledge into teachable materials

## Purpose

Oracle-teach generates learning materials from patterns that have reached 🌿 Pattern level or higher. It's the "สร้างคน" output — taking what we've learned and making it transferable.

## Proactive Triggers

### MUST Use Teach When:

**Knowledge Transfer:**
- User says: "teach me about", "explain the pattern"
- User says: "how does X work", "why do we do X"
- User says: "create a guide for", "document this"

**Team Sharing:**
- Onboarding new team member
- Writing documentation
- Creating training materials

**Pattern Explanation:**
- User asks about established pattern
- Need to justify a decision
- Explaining "why we do it this way"

## Teaching Formats

### Quick Explanation
```markdown
## Pattern: [Name]

**What**: One-line description
**Why**: The reasoning behind it
**How**: Steps to apply
**Example**: Concrete use case
```

### Full Guide
```markdown
# Guide: [Topic]

## Overview
What this pattern/principle is about.

## Background
Why this emerged, what problem it solves.

## The Pattern
Step-by-step application.

## Examples
### Example 1: [Context]
[Walkthrough]

### Example 2: [Context]
[Walkthrough]

## Common Mistakes
- Mistake 1: Why it's wrong
- Mistake 2: Why it's wrong

## Related Patterns
- [Link to related]

## Source
From Oracle knowledge base, maturity level: 🌿/🌳/🔮
```

### Micro-lesson (60 seconds)
```markdown
## 60-Second Lesson: [Topic]

**The Rule**: [One sentence]

**Why It Matters**: [One sentence]

**Try This**: [One action]

**Remember**: [Mnemonic or key phrase]
```

## Teaching Workflow

### 1. Find Teachable Knowledge
```javascript
oracle_search({
  type: "pattern",  // or principle, wisdom
  limit: 10
})
// Filter for teachable: true or maturity >= 🌿
```

### 2. Choose Format
| Audience | Format | Length |
|----------|--------|--------|
| Quick reminder | Micro-lesson | 60 sec |
| Team member | Quick explanation | 2 min |
| New hire | Full guide | 10 min |
| Documentation | Full guide + examples | 15 min |

### 3. Generate Material

```markdown
User: "teach me about subagent delegation"

AI checks Oracle → finds 🌿 Pattern "Subagent Delegation"

AI generates:
## Pattern: Subagent Delegation

**What**: Use Haiku subagents for bulk operations, Opus for review
**Why**: Saves context tokens, parallel execution, cost efficiency
**How**:
1. Identify bulk task (5+ files, heavy search)
2. Spawn subagent with clear instructions
3. Let subagent return summary
4. Main agent reviews and acts

**Example**: Searching 50 files for a pattern
- ❌ Main agent reads all 50 files (expensive)
- ✅ Subagent searches, returns top 5 matches
```

## Integration with Oracle Ecosystem

| Skill | Relationship |
|-------|--------------|
| oracle | Source of patterns to teach |
| oracle-incubate | Only teach mature knowledge (🌿+) |
| oracle-path | Teach is building block for paths |
| oracle-mentor | Mentor uses teach for guidance |

## Teachability Criteria

| Level | Teachable? | Confidence |
|-------|------------|------------|
| 🥒 Observation | No | Too raw |
| 🌱 Learning | Maybe | With caveats |
| 🌿 Pattern | Yes | Proven |
| 🌳 Principle | Definitely | Universal |
| 🔮 Wisdom | Core teaching | Foundational |

## Output Locations

| Material | Where |
|----------|-------|
| Quick explanation | Inline response |
| Full guide | `ψ/memory/learnings/` |
| Team docs | Project `/docs/` |
| Training | `ψ/writing/guides/` |

## Quick Reference

| User Says | Action |
|-----------|--------|
| "teach me about X" | Find pattern, generate explanation |
| "create a guide for X" | Full guide format |
| "quick explanation of X" | Micro-lesson format |
| "document this for team" | Full guide to /docs/ |
| "why do we do X" | Find principle, explain reasoning |
