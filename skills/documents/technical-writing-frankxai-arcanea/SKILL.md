---
name: arcanea-technical-writing
description: Technical writing excellence - documentation, API references, tutorials, and guides that users actually understand. Clear, accurate, useful.
version: 1.0.0
author: Arcanea
tags: [technical-writing, documentation, api-docs, tutorials, guides, industry]
triggers:
  - technical writing
  - documentation
  - api docs
  - tutorial
  - readme
  - user guide
---

# Technical Writing Mastery

> *"The best documentation is invisible. Users find what they need, understand it immediately, and get back to work."*

---

## The Technical Writing Philosophy

```
DOCUMENTATION IS NOT:
✗ Proof that you built something
✗ A formality to check off
✗ Something to write after shipping

DOCUMENTATION IS:
✓ Part of the product
✓ User experience in text form
✓ Force multiplier for adoption
✓ Investment that pays dividends
```

---

## The Four Types of Documentation

```
╔═══════════════════════════════════════════════════════════════════╗
║                    DOCUMENTATION TYPES                             ║
║              (Each serves different needs)                         ║
╠═══════════════════════════════════════════════════════════════════╣
║                                                                    ║
║   TUTORIALS      │ Learning-oriented    │ "Let me show you"       ║
║   HOW-TO GUIDES  │ Problem-oriented     │ "How to do X"           ║
║   REFERENCE      │ Information-oriented │ "Technical specs"        ║
║   EXPLANATION    │ Understanding-oriented│ "Why it works"         ║
║                                                                    ║
╚═══════════════════════════════════════════════════════════════════╝
```

### Tutorials (Learning)

```
PURPOSE: Teach newcomers through doing
STRUCTURE: Step-by-step journey
OUTCOME: User completes something real

CHARACTERISTICS:
• Hand-holding is appropriate
• Focus on accomplishment, not completeness
• Explain the "why" as you go
• End with something that works
```

### How-To Guides (Problem Solving)

```
PURPOSE: Help users accomplish specific tasks
STRUCTURE: Step-by-step instructions
OUTCOME: User solves their problem

CHARACTERISTICS:
• Assumes basic knowledge
• Focused on single goal
• Practical, not educational
• Skips unnecessary context
```

### Reference (Information)

```
PURPOSE: Describe the machinery
STRUCTURE: Systematic, complete
OUTCOME: User finds technical details

CHARACTERISTICS:
• Consistent format
• Complete and accurate
• No tutorial content
• Code examples for each item
```

### Explanation (Understanding)

```
PURPOSE: Clarify and illuminate
STRUCTURE: Discursive, connecting
OUTCOME: User understands deeply

CHARACTERISTICS:
• Discusses alternatives
• Explains reasoning
• Provides context
• Answers "why?"
```

---

## Writing Principles

### Clarity Over Cleverness

```
BAD:  "Leverage the paradigm-shifting capabilities..."
GOOD: "Use X to do Y."

BAD:  "The system utilizes..."
GOOD: "The system uses..."

BAD:  "It should be noted that..."
GOOD: Just say the thing.
```

### Active Voice

```
PASSIVE: "The file is created by the system."
ACTIVE:  "The system creates the file."

PASSIVE: "The configuration should be updated."
ACTIVE:  "Update the configuration."
```

### Present Tense

```
PAST:    "This function returned..."
PRESENT: "This function returns..."

FUTURE:  "This will create..."
PRESENT: "This creates..."
```

### Direct Address

```
IMPERSONAL: "One might want to..."
DIRECT:     "You might want to..."

IMPERSONAL: "The user should..."
DIRECT:     "You should..."
```

---

## Structure Patterns

### The README Template

```markdown
# Project Name

One-sentence description of what this does.

## Quick Start

The absolute minimum to get running.

## Installation

```bash
npm install project-name
```

## Basic Usage

```javascript
import { thing } from 'project-name';
thing.doSomething();
```

## API Reference

Link to full docs.

## Contributing

How to contribute.

## License

MIT (or whatever)
```

### The API Reference Template

```markdown
## functionName(param1, param2)

Brief description of what it does.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| param1 | string | Yes | What this is |
| param2 | number | No | What this is |

### Returns

`Type` - Description of return value

### Example

```javascript
const result = functionName('hello', 42);
console.log(result); // Expected output
```

### Errors

| Error | When |
|-------|------|
| InvalidParam | When param1 is empty |
```

### The Tutorial Template

```markdown
# Tutorial: [What You'll Build]

By the end of this tutorial, you will have [concrete outcome].

## Prerequisites

- What you need to know
- What you need installed

## Step 1: [First Action]

Brief explanation of what we're doing and why.

```code
Actual code to run
```

You should see [expected result].

## Step 2: [Next Action]

[Continue pattern...]

## What You've Learned

- Point 1
- Point 2

## Next Steps

Where to go from here.
```

---

## Common Mistakes

### Mistake: Assuming Knowledge

```
BAD:
"Configure the webhook endpoint."

GOOD:
"Configure the webhook endpoint. Webhooks are HTTP callbacks
that notify your server when events occur. To set one up..."
```

### Mistake: Missing Examples

```
BAD:
"The format parameter accepts a string."

GOOD:
"The format parameter accepts a string.

Example:
```javascript
const result = format('date', 'YYYY-MM-DD');
// Returns: '2024-01-15'
```"
```

### Mistake: Outdated Code

```
BAD:
Code examples that don't work with current version.

GOOD:
Version-tagged examples that are tested in CI.
```

### Mistake: Wall of Text

```
BAD:
Long paragraphs with no visual breaks.

GOOD:
• Short paragraphs
• Bullet points
• Code blocks
• Headers for scanning
```

---

## Maintenance

### Keep Docs Current

```
□ Docs updated with every feature change
□ Code examples tested automatically
□ Broken link checks automated
□ Version numbers accurate
□ Deprecation notices added
```

### Gather Feedback

```
• Track which pages have high bounce rates
• Monitor support questions (they reveal gaps)
• Include "Was this helpful?" feedback
• Watch for confusion patterns
```

---

## Quick Reference

### Writing Checklist

```
□ Used active voice
□ Used present tense
□ Addressed reader directly ("you")
□ Included working code examples
□ Tested all code examples
□ Added error handling examples
□ Linked to related topics
□ Formatted for scanning
□ Reviewed for accuracy
```

### Tone Guidelines

```
BE:
• Friendly but professional
• Confident but not arrogant
• Concise but complete
• Helpful but not patronizing

AVOID:
• Jargon without explanation
• Humor that might not translate
• Assumptions about user knowledge
• Passive-aggressive language
```

---

*"Documentation is a love letter to your future users. Write it with care."*
