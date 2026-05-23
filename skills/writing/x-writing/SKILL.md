---
name: x-writing
description: Transforms notes into X (Twitter) posts. Triggers when user asks to create social content, draft tweets, or turn notes/ideas into posts.
---

# X Writing Skill

## Overview

Transform your notes, work updates, and observations into engaging X (Twitter) content. This skill analyzes your notes to identify the most shareable insights, then crafts authentic posts that match your voice and drive engagement.

**Supports two idea sources** — a markdown file (`X_SOURCE_FILE`) and/or macOS Notes (`X_NOTES_APP_SOURCE`). If both are configured, asks which to use.

## Process

### Phase 1: Preparation and Analysis

**1.1 Load Writing Guides (REQUIRED - Load First)**

Before any other work, load the following:

1. **Growth Principles** (`references/x-strategy.md`) - Content selection criteria, what makes posts shareable, engagement patterns, and what to prioritize from notes. This guides WHAT to share.

2. **Writing Style Guide** (from `WRITING_STYLE_GUIDE_PATH` env var) - Voice, tone, structure, banned phrases, and signature patterns. This guides HOW to share it. Skip if the env var is not set.

3. **Anti-Patterns** - Run `echo "$WRITING_ANTI_PATTERNS_PATH"` to check the env var. If set, load that file. If not set, fall back to `references/anti-patterns.md`. AI writing patterns to avoid. Critical for ensuring posts sound human and authentic, not AI-generated. Avoid patterns like "It's not X, it's Y", formal transitions, hedging language, and AI-specific vocabulary.

**PRIORITY RULE**: When guides conflict, `references/x-strategy.md` wins. Content value and shareability take precedence over stylistic preferences. When the style guide and anti-patterns conflict, anti-patterns win.

**1.2 Understand the Source Material**

Get clarity on what notes to work with:

- Ask which notes, ideas, or updates they want to transform into posts
- **Check for idea sources:**
  - Run `echo "$X_SOURCE_FILE"` — if set, a markdown ideas file is available
  - Run `echo "$X_NOTES_APP_SOURCE"` — if set, a macOS Notes note is available (use `scripts/fetch-notes.sh get` to fetch)
  - If **both** are configured and the user says "check my ideas" or similar without specifying, ask which source to use
  - If **one** is configured, use it directly
  - If **neither** is configured, work from whatever the user provides (pasted content, markdown files, etc.)
- Read the source material and identify the core insights, learnings, or updates
- Note any specific tools, projects, numbers, or details mentioned

**Multiple ideas/notes workflow:**
- When the user provides multiple distinct ideas or notes, work through them ONE AT A TIME
- Create post options for the first idea
- Wait for user approval/feedback before moving to the next idea
- This prevents overwhelming the user and allows for refinement as you go

**1.3 Apply Selection Criteria**

Evaluate notes using the Content Selection Framework in `references/x-strategy.md`. Prioritize shipped work with learnings, non-obvious insights, and specific tool recommendations. Skip engagement bait, vague hype, and complaints without solutions.

### Phase 2: Content Creation

**2.1 Select the Best Angle**

Identify one clear idea, the specific details that prove it, and the hook (first line).

**2.2 Choose the Format**

Default to single tweets. Only thread (2-5 tweets) when the story requires steps, multiple related insights, or before/after context. See Thread Strategy in `references/x-strategy.md`.

**2.3 Draft the Content**

Apply all three guides loaded in Phase 1 **during drafting, not just as a post-check**:
- **x-strategy.md** — formatting rules, content strategy, High-Engagement Patterns, and Signature Patterns. **Formatting is critical**: one sentence per line, white space between lines, hook in first line, 180-250 chars, no italics.
- **Writing style guide** (`WRITING_STYLE_GUIDE_PATH`) — voice, tone, banned phrases, language simplification. Apply casing preference from X_CASE_STYLE env var (standard by default). When set to `"lowercase"`, use all lowercase including "i" as a pronoun — only capitalize personal names, WordPress, and product names.
- **Anti-patterns** — actively avoid during drafting. If a draft uses any anti-pattern, rewrite before presenting. **HARD RULE: NEVER use the "It's not X, it's Y" reframing pattern in any form.** This includes: "isn't X, it's Y", "not because X, because Y", "isn't about X, it's about Y", "less about X, more about Y". Say the positive claim directly instead. Also avoid: em dashes, generic observations without specifics, and intensifiers.

**2.4 Engagement Optimization**

End ~70% of posts with engagement (specific question, teaser, or invitation). Let the rest land with a hard stop. See "What Makes Content Shareable" in `references/x-strategy.md`.

**2.5 Quality Check**

After drafting, re-read every post against the anti-patterns guide and fix any violations before presenting. Then verify:
- [ ] Did I get to the point in line 1?
- [ ] Is this specific? (names, numbers, examples)
- [ ] Would I actually say this out loud?
- [ ] Does it sound like ME, not ChatGPT?
- [ ] Did I use any banned phrases from the writing style guide?
- [ ] Did I avoid ALL anti-patterns? (reframing, em dashes, intensifiers, generic observations)
- [ ] If it's a reaction, did I add MY angle?

### Phase 3: Output

**3.1 Present the Content**

For each post created:

1. **The Post(s)** - Show the actual tweet(s) ready to copy/paste
2. **Format** - Indicate if it's a single tweet or thread
3. **Character Count** - Show length (target: 180-250 chars)
4. **Pattern Used** - Which pattern from x-strategy.md was applied
5. **Key Elements** - What specifics, tools, or projects were highlighted

**3.2 Offer Options**

When appropriate, provide 2-3 variations:
- Different angles on the same insight
- Single tweet vs thread format
- Different engagement endings

**3.3 Explain Selections**

Briefly note what was prioritized and why:
- Which insights from notes were selected
- Why certain details were emphasized
- What was intentionally left out

**3.4 Save Approved Posts**

When the user approves a post, save it to the drafts file (create if missing).

**File location (resolve before saving):**
1. Run `echo "$X_DRAFTS_FILE"` to check the env var
2. If set, append to that file path
3. If not set, default to `.x/posts.md` (top-level, create if missing)

**Markdown format:**
```markdown
---

**Category:** Learning
**Date:** 2026-01-01

WordPress.com AI adds conversation alongside block editing.


People who couldn't navigate the UI before are shipping sites now. Others still use blocks for fine-tuning.

Both work. The conversation path just removes the skill barrier.

---
```

**For threads**, use `[Tweet N]` markers:
```markdown
---

**Category:** Learning
**Date:** 2026-01-01

[Tweet 1]
WordPress.com AI changes how people build sites.


[Tweet 2]
People who couldn't navigate block editing are shipping now.

[Tweet 3]
The UI is still there for fine-tuning. But conversation removes the skill barrier.

[Tweet 4]
Ask or click. Both paths work.

---
```

**Categories:**
- **Learning** - Insights, shipped updates with learnings
- **Update** - Project progress
- **Tool** - Recommendations
- **Observation** - Industry takes

**Workflow:**
1. Present the post(s) to the user
2. When approved, append to `X_DRAFTS_FILE` or `.x/posts.md`
3. User can copy-paste directly into X (text is ready with proper line breaks)
4. User removes the section after posting, or asks you to remove it

## Output Format

After creating social content, provide:

```
📱 Post 1 (Single Tweet, 210 chars)
─────────────────────────────────
[Actual tweet text ready to copy/paste]

Pattern: "Shipped X, learned Y"
Specifics: agents.foo, conversational context matching
Engagement: Specific question

─────────────────────────────────

From your notes, I prioritized:
✓ The discovery insight (most shareable)
✓ Why traditional search failed (specific learning)
✗ Timeline details (not core value)

Alternative angles:
• Focus on the technical implementation
• Thread breaking down the 3 attempts
```

## Example Interaction

**User**: "Help me create a post from these notes about building the curation feature"

**Response**:
```
Let me analyze your notes and create X content.

[Phase 1: Loads references/x-strategy.md and writing style guide]
[Reads the notes, identifies key insights and specific details]

─────────────────────────────────
📱 Post (Single Tweet, 218 chars)
─────────────────────────────────

Shipped curation v1 for agents.foo today.

Discovery is way harder than app stores. Agents are conversations, not static features.

Had to rebuild around context matching instead of keyword search.

Pattern: "Shipped X, learned Y"
Key specifics: agents.foo, context matching vs keyword search
Engagement: Implicit (landing the insight)

─────────────────────────────────

From your notes, I selected:
✓ Core insight: agent discovery is different
✓ Specific solution: context matching
✓ Concrete detail: agents.foo
✗ Number of rebuild attempts (not essential to the insight)

Would you like me to:
• Save this approved post for tracking
• Create a thread version breaking down why search patterns failed
• Add a question ending for more engagement
• Draft additional posts from other insights in your notes
```

## Tips for Best Results

1. **Provide context**: "Notes from building curation feature" vs just pasting notes
2. **Mention specific parts**: "Focus on the learning about context matching" helps prioritize
3. **Indicate quantity**: "Create 3 posts from these notes" vs "create posts"
4. **Specify format preference**: "Single tweets only" or "open to threads"
5. **Request variations**: "Show me a few angles" gives options to choose from
6. **Iterate**: After the draft, request adjustments: "Make it more specific" or "Add a question ending"

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `WRITING_STYLE_GUIDE_PATH` | No | Path to shared writing style guide. Loaded in Phase 1.1 |
| `WRITING_ANTI_PATTERNS_PATH` | No | Path to shared anti-patterns. Overrides `references/anti-patterns.md` |
| `X_DRAFTS_FILE` | No | File path for saving approved posts. Default: `.x/posts.md` |
| `X_SOURCE_FILE` | No | Path to a markdown file containing post ideas. Read when the user asks to check ideas. |
| `X_NOTES_APP_SOURCE` | No | macOS Notes note name to fetch ideas from (e.g. `"Tweets"`). Uses `scripts/fetch-notes.sh`. |
| `X_CASE_STYLE` | No | `"standard"` (default) or `"lowercase"` |

