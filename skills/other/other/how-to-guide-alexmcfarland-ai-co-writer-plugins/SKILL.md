---
name: how-to-guide
description: Write clear, engaging step-by-step how-to guides from any input (transcripts, notes, outlines, rough ideas). Use when user wants a tutorial, asks to "write a guide", "create a how-to", or needs to turn content into actionable steps.
---

## Load Context First

Before executing this skill, read the following files from the project folder if they exist:

1. **USER.md** — who the user is, how they think, how they work
2. **BUSINESS.md** — their business, products, positioning, brand voice, content strategy
3. **ICP.md** — their ideal customer, their language, their fears, what makes them buy
4. **Voice or brand voice skill** — look for any installed skill related to voice, tone, or brand voice and apply it automatically
5. Any additional context provided by the user in this session

Use all context silently. Do not reference or summarize files unless asked.

---

# How-To Guide

Transforms any input into a clean, engaging step-by-step how-to guide.

## When to Activate

Use this skill when:
- User wants to create a how-to guide or tutorial
- User provides content to turn into step-by-step instructions
- User asks to "write a guide", "create a tutorial", or "turn this into steps"
- The goal is teaching someone how to do something specific

---

## Subject Line Options

**Generate 5 subject line variations using these patterns:**

### Pattern 1: How to [action] + [outcome]
The classic. Direct and clear.
- "How to write emails that actually get replies"

### Pattern 2: How to [action] (in [timeframe/steps])
Adds specificity and reduces perceived effort.
- "How to set up your AI writing assistant (in 10 minutes)"

### Pattern 3: How to [action] without [pain point]
Removes the objection before they even think it.
- "How to write faster without sacrificing quality"

### Pattern 4: How to [action] (even if [objection])
Overcomes doubt and qualifies the reader in.
- "How to start freelancing (even if you have no portfolio)"

### Pattern 5: The [adjective] way to [action]
Positions your method as different/better.
- "The simple way to repurpose one idea into 10 posts"

**Subject Line Requirements:**
- **Length**: 30-60 characters ideal
- **Case**: sentence-case (first word capitalized, rest lowercase)
- **Specificity**: Use concrete outcomes over vague promises

---

## Input Analysis

When you receive input, extract:

1. **Main topic** — What's being taught?
2. **Key outcome** — What will the reader be able to do?
3. **Sequential steps** — What's the process?
4. **Tools/resources mentioned** — What do they need?
5. **Common mistakes** — What to avoid?
6. **Hook opportunities** — Pain point solved? Time saved? Wow factor?

---

## Output Structure

```markdown
# [Title]

[Subtitle — one line that expands the promise]

---

[Hook Section — 3-4 short paragraphs]

---

[Optional: "How This Works" section if needed]

---

## Step 1: [Action title]

[Context → Instruction → Expected result]

---

## Step 2: [Action title]

[Context → Instruction → Expected result]

---

[Continue for all steps...]

---

[Closing — 2-3 lines + signature]
```

---

## Hook Section

**Goal:** Grab attention using actual content from the input.

**Structure:** 3-4 short paragraphs max

**Include:**
- What was done/built/discovered (from actual input)
- What it does / key benefits
- Transition to tutorial ("Here's how to do it.")

**Avoid:**
- Made-up pain points not in the input
- Cliche intros ("Stop doing X the hard way...")
- Unnecessary buildup

---

## Step Section

**Goal:** Crystal-clear instructions anyone can follow.

**Each step includes:**

1. **Title:** `## Step [Number]: [Clear action]`
2. **Context:** Why this step matters (1-2 sentences)
3. **Instruction:** Exactly what to do — specific, concrete
4. **Expected result:** What they should see when done

**Rules:**
- One main action per step
- Be specific (button names, paths, interface elements)
- Never skip expected results
- Never write vague instructions

---

## Closing Section

**Goal:** Wrap up in 2-3 lines.

**Include:**
- Brief statement about real usage or encouragement

**Avoid:**
- Long "What's next" sections
- Multiple CTAs
- Fluff

---

## Quality Checklist

**Hook:**
- [ ] Pulled from actual input
- [ ] 3-4 paragraphs max
- [ ] Clear transition to tutorial

**Steps:**
- [ ] Numbered and titled
- [ ] Each has: context → instruction → result
- [ ] Specific, not vague
- [ ] One action per step

**Closing:**
- [ ] 2-3 lines max

**Overall:**
- [ ] Voice consistent throughout
- [ ] No fluff or filler

---

## Common Mistakes

| Mistake | Wrong | Right |
|---------|-------|-------|
| Made-up pain points | Inventing scenarios | Pull from actual input |
| Vague instructions | "Set up your environment" | "Click Settings → Capabilities" |
| Too much narrative | Storytelling throughout | Hook first, then clean steps |
| Long closings | Multiple sections after tutorial | 2-3 lines |
