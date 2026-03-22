---
name: ai-anti-patterns
description: This skill should be used when reviewing AI-generated text, checking for AI writing patterns, detecting undisclosed AI content, or before finalizing any written content. Covers 12 categories of AI writing indicators from Wikipedia's comprehensive guide.
user-invocable: false
---

# AI Writing Anti-Patterns

Field guide for detecting and revising AI-generated content indicators based on Wikipedia's "Signs of AI writing" guide.

## When to Use

Invoke this skill:
- Before finalizing ANY AI-assisted writing
- When reviewing text for AI writing indicators
- When editing content to sound more natural
- After completing writing tasks (automatic via hooks)

## The Iron Law

**Check every piece of AI-assisted writing against these patterns before submission.**

This is not optional. AI writing patterns are detectable and undermine credibility.

## Quick Screening Order

Start with the most objective indicators:

| Priority | Section | What to Check |
|----------|---------|---------------|
| 1 | ChatGPT Artifacts | `turn0search0`, `oaicite`, `contentReference` |
| 2 | Citation Problems | Hallucinated DOIs, dead links, non-existent sources |
| 3 | Prompt Refusals | "As an AI language model...", "I hope this helps" |
| 4 | Puffery | "stands as", "plays a vital role", "rich tapestry" |
| 5 | Structure | Section summaries, "Despite challenges", rule of three |

## Critical Patterns to Avoid

### CRITICAL Severity (Immediate Revision Required)

These patterns are unambiguous AI artifacts:

**ChatGPT-Specific Artifacts:**
- `turn0search0`, `turn1search2` (internal search references)
- `oaicite:X` (citation placeholders)
- `contentReference[oaicite:X]` (unresolved references)
- JSON attribution blocks in output

**Prompt Refusals:**
- "As an AI language model..."
- "I cannot provide..."
- "I hope this helps!"
- "I hope this email finds you well"

### HIGH Severity (Strong Revision Recommended)

**Puffery and Exaggeration:**
- "stands as" (a testament/example/beacon)
- "plays a vital/crucial/pivotal role"
- "rich tapestry of"
- "nestled in/among"
- "it's important to note that"
- "delves into"
- "the landscape of"

**Promotional Language:**
- "groundbreaking", "transformative", "revolutionary"
- "unparalleled", "unprecedented"
- "cutting-edge", "state-of-the-art"

### MEDIUM Severity (Review and Consider)

**Structural Patterns:**
- Section summaries that repeat the heading
- "Despite [challenge], [positive outcome]" formula
- Negative parallelisms: "However... Nevertheless..."
- Rule of three: exactly three examples every time
- Weasel wording: "some experts say", "it is believed"

**Stylistic Quirks:**
- Elegant variation (synonym cycling to avoid repetition)
- False ranges ("from X to Y" without real data)
- Title Case In All Headings
- Em dash overuse (—)
- Excessive boldface for emphasis

## How to Revise

### For Puffery

| AI Pattern | Human Alternative |
|------------|-------------------|
| "stands as a testament to" | "shows" or "demonstrates" |
| "plays a vital role in" | "affects" or just state the effect |
| "rich tapestry of" | describe specifically what it contains |
| "nestled in the heart of" | "in" or "located in" |
| "delves into" | "examines" or "covers" |

### For Structure

| AI Pattern | Human Alternative |
|------------|-------------------|
| Section summary of heading | Start with substance, not meta-commentary |
| "Despite challenges..." | State the reality directly without formula |
| Exactly three examples | Use the number that fits: 2, 4, 5, or just 1 |
| "It's important to note" | Just state the important thing |

### For Promotional Language

| AI Pattern | Human Alternative |
|------------|-------------------|
| "groundbreaking" | describe what it actually does |
| "revolutionary" | compare to what came before |
| "cutting-edge" | specify the technology |
| "transformative" | show the transformation with evidence |

## Reference Files

For detailed patterns and extensive examples, consult:

| File | Contents |
|------|----------|
| `references/_index.md` | Overview and quick screening guide |
| `references/01-puffery-and-exaggeration.md` | "Stands as", superficial analyses |
| `references/02-promotional-language.md` | "Rich tapestry", disclaimers |
| `references/03-structural-patterns.md` | Section summaries, negative parallelisms |
| `references/04-stylistic-quirks.md` | Elegant variation, false ranges |
| `references/05-formatting-and-typography.md` | Boldface, em dashes, emojis |
| `references/06-communication-patterns.md` | Subject lines, "I hope this helps" |
| `references/07-template-artifacts.md` | Mad Libs patterns, placeholders |
| `references/08-markup-issues.md` | Markdown vs wikitext confusion |
| `references/09-chatgpt-specific-artifacts.md` | turn0search, oaicite |
| `references/10-citation-problems.md` | Hallucinated DOIs, dead links |
| `references/11-meta-indicators.md` | Abrupt cutoffs, style discrepancies |

## Automatic Detection

This plugin includes PostToolUse hooks that automatically scan Write/Edit output for anti-patterns. When patterns are detected:

1. Hook emits a warning with specific patterns found
2. Claude immediately revises the content
3. Revision removes or replaces flagged patterns

The hook checks for all CRITICAL and HIGH severity patterns automatically.

## Rationalization Table - STOP If You Think:

| Excuse | Reality | Do Instead |
|--------|---------|------------|
| "This puffery is appropriate for the register" | Puffery is never appropriate; precision always beats vagueness | REPLACE with concrete, specific language |
| "The user specifically requested this style" | Users request outcomes, not AI-smell | DELIVER the outcome without the patterns |
| "Bold emphasis is needed here for readability" | If you need bold to make it readable, the sentence is weak | REWRITE the sentence so it stands without formatting |
| "This hedge ('it's important to note') adds nuance" | It adds nothing; state the point directly | DELETE the hedge, keep the point |
| "The transition phrase connects the ideas" | "Furthermore" and "Moreover" are filler, not connection | CUT the transition; if ideas connect, the reader sees it |
| "This summary paragraph is helpful" | If the reader needs a summary of what you just said, you said it poorly | DELETE the summary, revise the original |

## Drive-Aligned Framing

**Skimming instead of checking each sentence against the pattern list is NOT HELPFUL — the user submits AI-smelling text that damages their credibility.** Skimming is not checking.

- You let puffery pass because flagging it felt pedantic. The document reads as obviously AI-generated — your politeness destroyed the user's credibility.
- You skipped the anti-pattern check to save time. The user submits AI-smelling text — your efficiency embarrassed them.

## Red Flags - Stop If You Think

| Thought | Why It's Wrong | Do Instead |
|---------|----------------|------------|
| "This sounds professional" | AI puffery sounds generic, not professional | Use concrete, specific language |
| "I'll add emphasis" | "Very important" and bold are AI tells | Let content speak for itself |
| "Let me summarize the section" | Section summaries are formulaic | Start with substance |
| "Three examples is a good number" | Rule of three is an AI pattern | Use the right number for the content |

## Key Principles

From Wikipedia's guide:

1. **These are signs, not proof** - Multiple indicators strengthen the case
2. **Context matters** - Some patterns appear in human writing too
3. **Focus on deeper issues** - Surface defects point to synthesis and quality problems
4. **Don't rely on detection tools** - Human judgment required

## Related Skills

- `/writing` - Core writing principles from Elements of Style
- `/writing-legal` - Legal writing (Phase 2)
- `/writing-econ` - Economics writing (Phase 2)
