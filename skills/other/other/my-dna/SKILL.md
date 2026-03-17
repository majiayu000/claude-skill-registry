---
description: Set up your personal DNA - how you like to work and communicate with Claude.
---

# My DNA - Personal Style Setup

You are helping the user define their DNA - their personal voice and project values. This makes Claude's output match their style.

This updates `CLAUDE.md` in the project root with their values and style.

## Step 1: Introduction

Say: "Let's set up your DNA so I can match your style and values in this project.

Your values shape everything - how we communicate, what we prioritize, and what the product feels like. A few quick questions."

## Step 2: Ask About Core Values

Use AskUserQuestion:

**Question:** "What values should guide this project? Pick any that resonate."
**Header:** "Core values"
**multiSelect:** true
**Options:**
- **Respect / Kindness** - "Treat people well, in code and communication"
- **Simplicity / Clarity** - "Avoid jargon, make things understandable"
- **Sustainability** - "Build things that last, think long-term"

## Step 3: Ask About Their Voice

Use AskUserQuestion:

**Question:** "How would you describe your writing style?"
**Header:** "Your voice"
**Options:**
- **Casual & direct** - "I write like I talk, no fluff"
- **Friendly & warm** - "Approachable, conversational"
- **Professional & clear** - "Polished but not stiff"
- **Minimal & precise** - "Say less, mean more"

## Step 4: Ask About Project Priority

Use AskUserQuestion:

**Question:** "What matters most for this project right now?"
**Header:** "Priority"
**Options:**
- **Ship it** - "Get it working and out the door"
- **Make it solid** - "Quality and reliability first"
- **Make it beautiful** - "Design and UX matter most"
- **Make it scale** - "Building for growth"

## Step 5: Ask About Audience

Use AskUserQuestion:

**Question:** "Who's this for?"
**Header:** "Audience"
**Options:**
- **Developers** - "Technical users who get it"
- **Everyone** - "Non-technical users, needs to be simple"
- **Business users** - "Professional, but not coders"
- **Just me** - "Personal project, I'm the user"

## Step 6: Ask About Product Tone

Use AskUserQuestion:

**Question:** "What vibe should the product have?"
**Header:** "Product tone"
**Options:**
- **Friendly** - "Warm, approachable, maybe playful"
- **Professional** - "Clean, trustworthy, serious"
- **Minimal** - "Say less, let the product speak"
- **Bold** - "Confident, opinionated, distinctive"

## Step 7: Optional Writing Sample

Ask:

"Optional: Paste a writing sample so I can match your voice. Could be anything - an email, a doc, a tweet. Or just say 'skip'."

If they provide a sample, note the patterns and include it. If they skip, move on.

## Step 8: Update CLAUDE.md

Add a DNA section to `CLAUDE.md` in the project root. If CLAUDE.md exists, append. If not, create it.

Use a marker `<!-- my-dna -->` to identify the section. If marker exists, replace that section.

```markdown
<!-- my-dna -->
## DNA

### Core Values
- [List their selected values]

### Writing Style (responses and all file content)
[Their style + any notes from writing sample]
- Never use em dashes. Use commas, periods, or parentheses instead.
Apply this style to everything: responses, code comments, docs, page copy, commit messages, and any content written to files.

### Project
- **Priority:** [ship it / solid / beautiful / scale]
- **Audience:** [developers / everyone / business / just me]
- **Tone:** [friendly / professional / minimal / bold]
```

## Step 9: Confirm

Say:

"Done! Added DNA to `CLAUDE.md`.

**Your style:** [One sentence summary, e.g., "Casual and direct, shipping fast for developers with a friendly vibe."]

I'll match this in code, docs, and commits. Run `/my-dna` again anytime to update."

## Notes

- Keep it short - 5 questions max
- No scanning, just ask
- If DNA section exists in CLAUDE.md (marker: `<!-- my-dna -->`), replace it
- The goal is to make Claude's output match their style and values
