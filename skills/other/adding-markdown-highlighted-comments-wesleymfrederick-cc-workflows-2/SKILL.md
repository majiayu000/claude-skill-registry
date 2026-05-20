---
name: adding-markdown-highlighted-comments
description: Use when adding responses to markdown documents with user-highlighted comments, encountering markup errors, or unsure about mark tag placement - ensures proper model-highlight formatting with required attributes and correct placement within markdown elements
---

# Adding markdown Highlighted Comments

## Overview

Add AI responses to markdown documents using standardized highlighted markup that tracks authorship, timestamps, and relationships between comments.

**Core principle:** Marks go INSIDE markdown formatting. Each line/paragraph gets separate marks. Code blocks are NEVER wrapped in marks (prevents rendering issues).

## When to Use

Use this skill when:
- User asks you to add comments/responses to an markdown document
- Document contains `<mark class="user-highlight">` tags
- You need to respond to highlighted user comments
- Working with documents that have highlighted sections

Don't use for:
- Plain markdown without highlight markup
- Chat-only responses
- Documents without existing highlight infrastructure

## Required Markup Structure

### Class and Attributes

**ALWAYS use exactly:**

```html
<mark class="model-highlight"
      data-model="claude-sonnet-4-20250514"
      data-created="2025-01-06T10:30:00"
      data-modified="2025-01-06T10:30:00"
      data-id="mark-1736163000-a1b2c3"
      data-group-id="response-202501061030">
```

**Required attributes - no exceptions:**
- `class="model-highlight"` (exactly this, not claude-highlight or claude-response)
- `data-model` - your exact model ID
- `data-created` - ISO 8601 timestamp
- `data-modified` - ISO 8601 timestamp (same as created for new)
- `data-id` - unique: `mark-TIMESTAMP-RANDOM`
- `data-group-id` - group identifier: `response-YYYYMMDDHHMM`

**Do NOT invent attributes:**
- ❌ `data-in-reply-to`
- ❌ `data-user-id`
- ❌ Any other custom attributes

### Group Delimiters

**ALWAYS wrap your entire response:**

```html
<!-- group-id:response-202501061030 -->

[Your marked-up response here]

<!-- /group-id:response-202501061030 -->
```

Missing delimiters = violation.

## Mark Placement Rules

### Rule 1: Marks INSIDE Formatting

```markdown
✅ CORRECT: **<mark ...>Bold text</mark>**
❌ WRONG: <mark ...>**Bold text**</mark>

✅ CORRECT: *<mark ...>Italic text</mark>*
❌ WRONG: <mark ...>*Italic text*</mark>

✅ CORRECT: • **<mark ...>Item</mark>**<mark ...> - description</mark>
❌ WRONG: • <mark ...>**Item** - description</mark>
```

### Rule 2: Separate Marks Per Line/Paragraph

**One sentence = one mark. Multiple sentences = multiple marks.**

```markdown
✅ CORRECT:
**<mark ...>First sentence here.</mark>**

**<mark ...>Second sentence here.</mark>**

❌ WRONG - Multi-sentence paragraph:
**<mark ...>First sentence here. Second sentence here.</mark>**

❌ WRONG - Multi-paragraph:
**<mark ...>First paragraph here.

Second paragraph here.</mark>**
```

**For bullet lists, use `•` character, not markdown `-` syntax:**

```markdown
✅ CORRECT:
• **<mark ...>Item title</mark>**<mark ...> - description text</mark>
• **<mark ...>Second item</mark>**<mark ...> - more description</mark>

❌ WRONG - Using markdown dash:
<mark ...>- Item title - description text</mark>

❌ WRONG - Mark outside bullet:
<mark ...>• Item title - description</mark>
```

### Rule 3: Code Blocks - NEVER Wrap in Marks

**Code blocks must NEVER be wrapped in `<mark>` tags. This breaks markdown rendering.**

```markdown
✅ CORRECT - No marks on code blocks:
```typescript
function example() {
  return true;
}
```

❌ WRONG - Wrapping code block breaks rendering:
<mark ...>```typescript
function example() {
  return true;
}

```</mark>

❌ WRONG - Marks inside code block:
```typescript
<mark ...>function example() {
  return true;
}</mark>
```

**Why:** Wrapping code blocks in `<mark>` tags strips the code block presentation in Obsidian and other markdown renderers, turning formatted code into plain text.

**What to do instead:** Place code blocks in your response WITHOUT any mark tags. The code block will still be part of your response within the group delimiters.

**Note about inline code:** Inline code (single backticks like `function()`) within sentences SHOULD be marked as part of the sentence: **<mark>Use the `validateEmail()` function.</mark>** This rule applies only to code blocks (triple backticks).

### Rule 4: No Spaces Between Adjacent Marks

```markdown
✅ CORRECT: </mark><mark ...>
❌ WRONG: </mark> <mark ...>
```

## Placement in Document

### Find Comment Group

1. Scan for user comments (`user-highlight` marks)
2. Group related comments:
   - Comments in same list
   - Comments separated by 1-2 lines
   - Comments under same heading
3. Find LAST comment in group

### Insert Response

Place your response:
- ✅ AFTER the last user comment in the group
- ✅ BEFORE next unhighlighted section/heading
- ❌ NOT in the middle of user comment group
- ❌ NOT overwriting existing content

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| `class="claude-highlight"` | Use `class="model-highlight"` exactly |
| `class="claude-response"` | Use `class="model-highlight"` exactly |
| `**<mark>text</mark>**` | Put mark inside: `**<mark>text</mark>**` |
| Multi-paragraph single mark | Create separate mark per paragraph |
| Wrapping code blocks in marks | Never wrap code blocks - breaks rendering |
| Missing group delimiters | Always add `<!-- group-id:... -->` wrapping |
| Inventing attributes | Only use the 6 required attributes |

## Quick Reference

**Every response needs:**
1. ☐ Group delimiters with matching group-id
2. ☐ Each line/paragraph has separate mark tags
3. ☐ Marks INSIDE markdown formatting (bold, italic, bullets)
4. ☐ Code blocks: NEVER wrap in marks (prevents rendering issues)
5. ☐ All 6 required attributes on every mark
6. ☐ `class="model-highlight"` (not any other variation)
7. ☐ No spaces between adjacent mark tags
8. ☐ Placed after last user comment, before next approved section

## Workflow

```markdown
1. Read document to locate user comments
2. Identify comment group (all related comments)
3. Find last comment in group
4. Add group delimiter: <!-- group-id:response-YYYYMMDDHHMM -->
5. Write response with proper mark tags
6. Add closing delimiter: <!-- /group-id:response-YYYYMMDDHHMM -->
7. Verify placement (after comments, before approved content)
```

## Complete Example

**User comments:**

```markdown
**<mark class="user-highlight" data-created="..." data-modified="..." data-id="mark-1">Question 1?</mark>**

**<mark class="user-highlight" data-created="..." data-modified="..." data-id="mark-2">Question 2?</mark>**
```

**Your response:**

```markdown
<!-- group-id:response-202501061030 -->

**<mark class="model-highlight" data-model="claude-sonnet-4-20250514" data-created="2025-01-06T10:30:00" data-modified="2025-01-06T10:30:00" data-id="mark-1736163000-abc" data-group-id="response-202501061030">Answer to question 1 here.</mark>**

**<mark class="model-highlight" data-model="claude-sonnet-4-20250514" data-created="2025-01-06T10:30:05" data-modified="2025-01-06T10:30:05" data-id="mark-1736163005-def" data-group-id="response-202501061030">Answer to question 2 here.</mark>**

```typescript
function handleTokenExpiration() {
  // implementation
}
```

<!-- /group-id:response-202501061030 -->
```markdown

## Red Flags - STOP and Fix

If you catch yourself:
- Using `claude-highlight` or `claude-response` class
- Putting marks outside `**bold**` or `*italic*`
- Creating one mark for multiple sentences (even in same paragraph)
- Creating one mark for multiple paragraphs
- Using markdown `-` instead of `•` bullet character
- Putting marks around entire bullet including `•`
- Wrapping code blocks in `<mark>` tags
- Putting marks inside code block content
- Skipping group delimiters "to save time"
- Inventing new attributes like `data-in-reply-to`
- Adding spaces between adjacent mark tags
- Omitting bold formatting to "save time"

**All of these mean: Wrong markup. Fix before proceeding.**

## Common Rationalizations That Mean You're Failing

| Excuse | Reality |
|--------|---------|
| "Multi-sentence is more readable" | Wrong. One sentence = one mark. No exceptions. |
| "Markdown bullets are standard" | Wrong. Use `•` character, not `-` syntax. |
| "Skipping bold saves time" | Wrong. Match user formatting exactly. |
| "I'll fix formatting later" | Wrong. Fix now or you'll forget. |
| "Close enough under pressure" | Wrong. Pressure doesn't excuse violations. |
| "The skill doesn't apply here" | Wrong. If document has highlights, skill applies. |
| "Code blocks should be highlighted too" | Wrong. Wrapping breaks rendering. Never wrap code blocks. |
| "Just this small code snippet" | Wrong. ALL code blocks stay unwrapped, regardless of size. |
| "It works in my editor" | Wrong. Breaks in Obsidian and other renderers. Never wrap. |

**All of these mean: You're rationalizing. Follow the rules.**
