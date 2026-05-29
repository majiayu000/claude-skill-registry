---
name: how-to-guide
description: Create comprehensive how-to guides and tutorials. Use when the user needs step-by-step instructional content, tutorials, documentation, or educational guides.
---

# How-To Guide Creator

Create clear, actionable how-to guides that help readers achieve specific outcomes through step-by-step instructions.

## Before Writing

1. **Read context profiles**:
   - `/context/voice-dna.json` - Maintain authentic voice
   - `/context/icp.json` - Match reader's skill level
   - `/context/business-profile.json` - Align with expertise areas

2. **Determine guide scope** and reader prerequisites

## Guide Types

### Type 1: Quick Tutorial (500-1,000 words)
For simple, focused tasks

```
- Title: How to [Do Specific Thing]
- Intro: 2-3 sentences
- Prerequisites: Bulleted list
- Steps: 3-7 steps
- Conclusion: 1-2 sentences
```

### Type 2: Comprehensive Guide (1,500-3,000 words)
For complex processes

```
- Title
- Introduction (why this matters)
- Prerequisites
- Overview of what we'll cover
- Main content (sectioned steps)
- Troubleshooting common issues
- Next steps
- Resources
```

### Type 3: Ultimate Guide (3,000+ words)
For deep-dive educational content

```
- Title
- Table of contents
- Introduction
- Background/Context
- Prerequisites
- Detailed sections with substeps
- Examples and case studies
- Common mistakes
- FAQ
- Resources and tools
- Conclusion and next steps
```

## Guide Structure Template

```markdown
# How to [Achieve Specific Outcome]

[One-paragraph introduction: what they'll learn and why it matters]

## Prerequisites

Before you start, make sure you have:
- [Requirement 1]
- [Requirement 2]
- [Requirement 3]

## Overview

In this guide, you'll learn:
1. [What they'll accomplish in section 1]
2. [What they'll accomplish in section 2]
3. [What they'll accomplish in section 3]

**Time required**: [Estimate]
**Difficulty**: [Beginner/Intermediate/Advanced]

---

## Step 1: [Action-Oriented Title]

[Brief context for why this step matters]

### What to do:

1. [Specific action]
2. [Specific action]
3. [Specific action]

### Example:

[Concrete example of this step]

### Common mistakes:

- [Mistake to avoid]
- [Mistake to avoid]

---

## Step 2: [Action-Oriented Title]

[Continue pattern...]

---

## Troubleshooting

### Issue: [Common Problem]
**Solution**: [How to fix]

### Issue: [Common Problem]
**Solution**: [How to fix]

---

## Next Steps

Now that you've [accomplished goal], you can:
- [Next logical step 1]
- [Next logical step 2]
- [Advanced option]

---

## Resources

- [Useful tool or link]
- [Useful tool or link]
- [Related guide]
```

## Writing Guidelines

### Titles
- Start with "How to"
- Include the specific outcome
- Be specific, not vague
- Examples:
  - ✓ "How to Set Up a Claude Code Writing System in 30 Minutes"
  - ✗ "How to Use AI for Writing"

### Prerequisites
- Be explicit about what's needed
- Include skill level
- List tools/accounts required
- Link to prerequisite guides if needed

### Steps
- One action per step
- Start with action verb
- Include the "why" briefly
- Show don't just tell
- Include examples/screenshots where helpful

### Examples
- Use real, specific examples
- Show before/after when possible
- Include edge cases
- Make them relatable to ICP

### Formatting
- Plenty of white space
- Headers for scanability
- Numbered steps for sequences
- Bullets for unordered items
- Bold key terms
- Code blocks for technical content

## Output Format

```
TITLE: How to [Specific Outcome]
TYPE: [Quick/Comprehensive/Ultimate]
TARGET LENGTH: [Word count]
SKILL LEVEL: [Beginner/Intermediate/Advanced]
TIME TO COMPLETE: [Estimate]

---

[FULL GUIDE CONTENT]

---

SUMMARY:
- Steps covered: [Number]
- Key outcome: [What they can now do]
- Next recommended guide: [If applicable]
```

## Quality Checklist

Before delivering:

- [ ] Clear, specific title
- [ ] Prerequisites listed
- [ ] Logical step progression
- [ ] Each step is actionable
- [ ] Examples included
- [ ] Common mistakes addressed
- [ ] Troubleshooting section
- [ ] Next steps provided
- [ ] Matches voice DNA
- [ ] Appropriate for ICP skill level

## Common Mistakes to Avoid

- Assuming knowledge not in prerequisites
- Steps that are too big (break them down)
- Missing the "why" behind steps
- No examples or visuals
- Jargon without explanation
- Skipping edge cases
- No troubleshooting help
- Weak conclusion
