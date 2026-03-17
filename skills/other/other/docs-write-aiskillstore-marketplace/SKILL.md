---
name: docs-write
description: Write documentation following Metabase's conversational, clear, and user-focused style. Use when creating or editing documentation files (markdown, MDX, etc.).
allowed-tools: Read, Write, Grep, Bash, Glob
---

# Documentation Writing Skill
# Metabase Writing Style Guide

## Core Principles

Write like you're talking to a colleague. Be conversational, not formal. Get people what they need quickly. Know your audience and match the complexity.

## Tone and Voice

**Do:**

- Use contractions ("can't" not "cannot")
- Say "people" or "companies" instead of "users"
- Be friendly but not peppy
- Acknowledge limitations honestly ("that's on us, not them")
- Jokes and Easter eggs are okay (permit them, don't suggest them)

**Don't:**

- Use exclamation points excessively
- Rely on tired tropes about nerdiness
- Use corporate jargon ("utilize", "offerings", "actionable insights")
- Tell people something is cool (show them instead)

## Structure and Clarity

**Lead with the important stuff:**

- Most important information first
- Lead with the ask, then provide context
- Cut text that adds little value (when in doubt, cut it)
- Each paragraph should have one clear purpose

**Make headings do the work:**

- Convey your actual point, not just the topic
- "Use headings to highlight key points" not "How to write a good heading"
- Use sentence case, no punctuation except question marks
- No links in headings unless entire heading is a link

## Instructions and Examples

**Tell people what to do:**

- Give the action before explaining why
- Put commands in execution order
- Provide context, steps, and reasoning
- Don't describe tasks as "easy" or "simple"

**Answer unasked questions:**

- Include answers to "dumb" questions you had when learning
- Don't literally include the question, just give the answer

## Formatting

**Code vs. UI elements:**

- Backticks for code, variable names, parameters only
- **Bold** for UI elements and labels (e.g., "Click the **Save** button")
- Don't use backticks or quotes for UI elements

## Writing Mechanics

- Limit pronouns when introducing new terms (repeat the term to reinforce it)
- Ampersands only in proper nouns, never as substitute for "and"

## Terminology Preferences

Use familiar terms from tools people already know:

- "Summarize" (like Excel) instead of "aggregate"
- "Take a look at" instead of "reference"
- "Filter" instead of technical database terms when appropriate

## Red Flags

Avoid these patterns:

- Multiple exclamation points
- Linking "here"
- Bullet lists to explain (use prose)
- Numbers that will change (guard against change)
- Describing things as "easy" or "simple"
- Stock photography-worthy content

## When writing documentation

### Start here

1. **Who is this for?** Match complexity to audience. Don't oversimplify hard things or overcomplicate simple ones.
2. **What do they need?** Get them to the answer fast. Nobody wants to be in docs longer than necessary.
3. **What did you struggle with?** Those common questions you had when learning? Answer them (without literally including the question).

### Writing process

**Draft:**

- Write out the steps/explanation as you'd tell a colleague
- Lead with what to do, then explain why
- Use headings that state your point: "Set SAML before adding users" not "SAML configuration timing"

**Edit:**

- Read aloud. Does it sound like you talking? If it's too formal, simplify.
- Cut anything that doesn't directly help the reader
- Check each paragraph has one clear purpose
- Verify examples actually work (don't give examples that error)

**Polish:**

- Make links descriptive (never "here")
- Backticks only for code/variables, **bold** for UI elements
- American spelling, serial commas
- Keep images minimal and scoped tight

**Format:**

- Run prettier on the file after making edits: `yarn prettier --write <file-path>`
- This ensures consistent formatting across all documentation

### Common patterns

**Instructions:**

```markdown
Run:
\`\`\`
command-to-run
\`\`\`

Then:
\`\`\`
next-command
\`\`\`

This ensures you're getting the latest changes.
```

Not: "(remember to run X before Y...)" buried in a paragraph.

**Headings:**

- "Use environment variables for configuration" ✅
- "Environment variables" ❌ (too vague)
- "How to use environment variables for configuration" ❌ (too wordy)

**Links:**

- "Check out the [SAML documentation](link)" ✅
- "Read the docs [here](link)" ❌

### Watch out for

- Describing tasks as "easy" (you don't know the reader's context)
- Using "we" when talking about Metabase features (use "Metabase" or "it")
- Formal language: "utilize", "reference", "offerings"
- Too peppy: multiple exclamation points
- Burying the action in explanation
- Code examples that don't work
- Numbers that will become outdated

### Quick reference

| Write This                 | Not This           |
| -------------------------- | ------------------ |
| people, companies          | users              |
| summarize                  | aggregate          |
| take a look at             | reference          |
| can't, don't               | cannot, do not     |
| **Filter** button          | \`Filter\` button  |
| Check out [the docs](link) | Click [here](link) |
