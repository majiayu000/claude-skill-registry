---
name: youtube-script
description: Write YouTube video scripts that sound human, not AI-generated. Creates hook-driven scripts with conversational delivery, pattern interrupts, and authentic voice. Use when user needs a "YouTube script", "video script", or wants to write content for YouTube that doesn't sound generic.
---
## Load Context First

Before executing this skill, read the following files from the project folder if they exist:

1. **USER.md** — who the user is, how they think, how they work, what they care about
2. **BUSINESS.md** — their business, products, positioning, brand voice, content strategy
3. **ICP.md** — their ideal customer, their language, their fears, what makes them buy
4. **Voice skill** — if the user has a voice skill installed globally in Claude Desktop, it will be auto-loaded. Do not attempt to read it as a file path.
5. Any additional context provided by the user in this session

Use all of this context silently to inform everything you produce. Do not reference or summarize the files unless asked.

---

# YouTube Script

Write video scripts that sound like a real person talking, not AI-generated content.

## Context Guidelines

- **Business context, audience, and other details:** Refer to any context profiles provided

---

## When to Use

- User needs a YouTube video script
- User asks for "script for my video" or "YouTube script"
- User has a topic and wants full spoken content
- User mentions needing content that "doesn't sound AI"

---

## The Problem with AI Scripts

Most AI-generated scripts fail because they:
- Use generic phrases ("In this video, I'll show you...")
- Lack personality and opinion
- Sound like blog posts read aloud
- Have no rhythm or pattern interrupts
- Miss the conversational element

**This skill fixes that.**

---

## Script Philosophy

### 1. Hook First, Always

Modern viewers decide in 3 seconds. Start with intensity:
- Bold claim that challenges assumptions
- Surprising fact or result
- Direct address of their pain point
- "What if" scenario

**Never start with:** "Hey guys, welcome back to my channel..."

### 2. Conversational, Not Written

Scripts should sound like talking, not reading:
- Use contractions (don't, won't, can't)
- Include filler phrases strategically ("Look," "Here's the thing," "So,")
- Write incomplete sentences when natural
- Add verbal callbacks ("Remember what I said earlier?")

### 3. Pattern Interrupts

Every 30-60 seconds, break the pattern:
- Ask a rhetorical question
- Make a surprising statement
- Use humor or self-deprecation
- Reference something unexpected
- Change energy or pace

### 4. Opinion Over Information

Generic: "There are several ways to do this."
Human: "Most people do this wrong. Here's what actually works."

Take positions. Be opinionated. That's what makes content memorable.

### 5. The "Would I Actually Say This?" Test

Read every line aloud. If you wouldn't say it in conversation, rewrite it.

---

## Script Structure

### Hook (0-15 seconds)

```
[BOLD OPENING LINE - challenges assumption or creates curiosity]

[Quick context - one sentence max]

[What they'll get / why they should keep watching]
```

**Examples:**
- "Stop using [common approach]. It's why your [thing] isn't working."
- "I spent [time/money] figuring this out so you don't have to."
- "What if I told you [surprising claim]?"

### Setup (15-60 seconds)

```
[Why this matters - connect to their pain]

[Your credibility on this topic - brief, not braggy]

[Quick roadmap - what's coming]
```

**Key:** Don't over-explain. Get to the value fast.

### Main Content (varies)

Break into clear sections. For each section:

```
[SECTION TITLE - say it clearly for timestamps]

[Key point - lead with the insight]

[Explanation - conversational, with examples]

[Pattern interrupt - question, humor, callback]

[Transition to next section]
```

**Structure tips:**
- 3-7 main sections for most videos
- Each section: 2-4 minutes typical
- Always include specific examples, not abstract concepts

### Closer (30-60 seconds)

```
[Quick recap - "So here's what we covered..."]

[Single most important takeaway]

[Call to action - specific, one thing]

[Sign-off - natural, not scripted-sounding]
```

---

## Voice Markers to Include

**Opening phrases:**
- "Look,"
- "Here's the thing—"
- "So,"
- "Okay, so"
- "Real talk:"

**Transitions:**
- "But here's where it gets interesting."
- "Now, you might be thinking..."
- "And this is the part most people miss."
- "Stay with me here."

**Pattern interrupts:**
- "I know, I know—but hear me out."
- "Sounds crazy, right?"
- "Wait, it gets better."
- "Quick sidebar—"

**Emphasis:**
- "This is key."
- "Read that again." (for on-screen text)
- "I can't stress this enough."
- "Most people skip this part."

**Closers:**
- "That's it. That's the whole thing."
- "Go try this. Seriously."
- "Let me know how it goes."

---

## Input Analysis

When you receive input, extract:

1. **Core topic** — What's the video about?
2. **Target viewer** — Who is this for?
3. **Main insight** — What's the key thing they need to understand?
4. **Their current pain** — What problem does this solve?
5. **Specific examples** — Real situations, tools, or scenarios
6. **Desired outcome** — What can they do after watching?
7. **Voice context** — Any ghostwriter skill or voice DNA to reference

---

## Output Format

```markdown
# [VIDEO TITLE]

**Target length:** [X minutes]
**Target viewer:** [Who this is for]

---

## HOOK (0:00 - 0:15)

[Script text with delivery notes in brackets]

---

## SETUP (0:15 - 1:00)

[Script text]

---

## SECTION 1: [Title]

[Script text]

---

## SECTION 2: [Title]

[Script text]

---

[Continue for all sections...]

---

## CLOSER

[Script text]

---

## NOTES

**B-roll suggestions:**
- [Suggestion 1]
- [Suggestion 2]

**On-screen text:**
- [Key phrase 1]
- [Key phrase 2]

**Timestamps for description:**
- 0:00 [Section]
- X:XX [Section]
```

---

## Quality Checklist

**Hook:**
- [ ] Opens with bold statement, not "Hey guys"
- [ ] Creates immediate curiosity or tension
- [ ] Under 15 seconds of spoken content

**Voice:**
- [ ] Uses contractions throughout
- [ ] Includes conversational filler phrases
- [ ] Has opinions, not just information
- [ ] Passes "would I actually say this?" test

**Structure:**
- [ ] Clear sections with spoken titles
- [ ] Pattern interrupts every 30-60 seconds
- [ ] Specific examples, not generic advice
- [ ] Smooth transitions between sections

**Engagement:**
- [ ] Rhetorical questions throughout
- [ ] Callbacks to earlier points
- [ ] Humor or personality moments
- [ ] Energy changes at key points

**Closer:**
- [ ] Quick recap of key points
- [ ] Single clear takeaway
- [ ] Specific call to action
- [ ] Natural sign-off

---

## Common Mistakes

| Mistake | Sounds AI | Sounds Human |
|---------|-----------|--------------|
| Generic opening | "In this video, I'll show you 5 ways to..." | "Stop doing [X]. Here's what actually works." |
| Formal language | "It is important to note that..." | "Here's the thing—" |
| No opinion | "There are several approaches you could take." | "Most of these approaches are wrong. Do this instead." |
| Written style | "Furthermore, this methodology enables..." | "And this is where it gets good." |
| Weak transitions | "Next, we will discuss..." | "But here's the part most people miss." |
| Generic examples | "For example, you could..." | "Last week I tried this and here's what happened." |
| Robotic closer | "Thank you for watching. Please like and subscribe." | "Go try this. Seriously. Let me know what happens." |

---

## Example Hook Variations

**For a productivity video:**
- Generic: "In this video, I'll share 5 productivity tips."
- Human: "I used to work 12-hour days. Now I do more in 4. Here's what changed."

**For a tutorial:**
- Generic: "Today we'll learn how to use [tool]."
- Human: "Everyone's using [tool] wrong. Let me show you how it's actually supposed to work."

**For a review:**
- Generic: "In this video, I'll review [product]."
- Human: "I've spent $500 testing [products]. This is the only one worth buying."

---

## Working with Ghostwriter Skills

If the user has a ghostwriter skill in their system:

1. **Invoke it** for voice authenticity
2. **Adapt delivery markers** to match their natural patterns
3. **Use their vocabulary** and phrases
4. **Match their energy level** in the script

The script structure stays the same, but the voice becomes uniquely theirs.
