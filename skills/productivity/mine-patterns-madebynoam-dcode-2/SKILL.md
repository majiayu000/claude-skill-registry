---
name: dcode:mine-patterns
description: Analyze a work session to identify repeatable patterns that could become reusable skills or commands. Use at the end of a productive session to capture workflows worth automating, when noticing repetitive multi-step tasks, or when wanting to improve personal productivity with Claude Code.
---

# Mine Patterns

Turn productive sessions into reusable skills.

**For designers who think:** "I keep doing this same thing... there must be a better way."

## Why This Matters

Every time you solve a problem, you're creating a workflow. Most workflows get forgotten. This skill helps you capture the good ones before they disappear.

## Instructions

### 1. Review Session Activities

Look at what was accomplished:
- What tasks were repeated or could be repeated?
- What multi-step workflows were performed?
- What required specific domain knowledge?
- What felt tedious or error-prone?

### 2. Identify Skill Candidates

Good skills have these traits:

| Trait | Why It Matters |
|-------|----------------|
| **Repeatable** | Will be done again in future sessions |
| **Multi-step** | More than a single action |
| **Generalizable** | Works across different contexts |
| **Time-saving** | Automates tedious or error-prone work |
| **Knowledge-heavy** | Requires remembering specific patterns |

### 3. Categorize by Value

**High value** - Build these first:
- Complex workflows done frequently
- Tasks where mistakes are costly
- Processes that require specific conventions

**Medium value** - Build when you have time:
- Useful but less frequent tasks
- Nice-to-have automations

**Lower value** - Maybe don't bother:
- One-off investigations
- Highly context-specific tasks

### 4. Present Suggestions

For each potential skill, document:

```
## Suggested Skill: {name}

**Problem it solves:** {What pain point does this address?}

**Trigger:** {When would someone invoke this?}

**Steps it automates:**
1. {Step 1}
2. {Step 2}
3. {Step 3}

**Value:** High / Medium / Low

**Complexity to build:** Quick (1-2 hrs) / Medium (half-day) / Complex (day+)
```

### 5. Help Build the Chosen Skills

If the user wants to create a skill:

1. Draft the SKILL.md with proper frontmatter:
```yaml
---
name: skill-name
description: Clear description of what it does and when to use it
---
```

2. Write clear instructions
3. Include examples
4. Test it on a real task

## Example Output

Based on this session, here are potential skills:

### High Value

**1. design-token-audit**
- **Problem:** Finding inconsistent colors/spacing across a codebase
- **Trigger:** "Audit this component for design system compliance"
- **Steps:** Scan for hardcoded values, compare against tokens, report violations
- **Complexity:** Medium

**2. responsive-check**
- **Problem:** Verifying components work at all breakpoints
- **Trigger:** Before PR, after styling changes
- **Steps:** Identify breakpoints, list what changes at each, flag potential issues
- **Complexity:** Quick

### Medium Value

**3. figma-to-code-notes**
- **Problem:** Translating design specs into implementation notes
- **Trigger:** Starting implementation of a new design
- **Steps:** Extract spacing, colors, typography, create implementation checklist
- **Complexity:** Medium

---

**Which of these would you like to create?**

## Meta Note

This skill is itself an example of workflow mining—it was created by noticing that "identifying reusable patterns" was a repeatable, valuable task.
