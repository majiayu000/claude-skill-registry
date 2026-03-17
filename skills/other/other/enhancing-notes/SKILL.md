---
name: enhancing-notes
description: Enhance book notes with Blinkist-style summaries. Use when asked to "enhance notes", "improve book notes", "add key insights", "expand notes", or "make notes better". Adds Core Message, Key Insights, Notable Quotes, and Who Should Read sections via parallel web research.
allowed-tools: Read, Write, Edit, Bash, WebFetch, Glob, Grep, Task, TaskOutput, WebSearch, AskUserQuestion
---

# Enhancing Book Notes

This skill transforms basic book notes into Blinkist-style summaries with Key Insights, Notable Quotes, Core Message, and Who Should Read sections.

## Workflow Overview

```text
Phase 1: Book Identification
   └─ Find and validate book note

Phase 2: Parallel Research
   ├─ WebSearch agent 1: key insights
   ├─ WebSearch agent 2: main ideas
   ├─ WebSearch agent 3: takeaways
   └─ WebSearch agent 4: notable quotes

Phase 3: Content Synthesis
   ├─ Core Message (1-2 sentences)
   ├─ Key Insights (8-12 blinks)
   ├─ Notable Quotes (3 quotes)
   └─ Who Should Read

Phase 4: User Review (BLOCKING GATE)
   └─ Present content, await approval

Phase 5: Save Enhanced Note
   └─ Insert sections, preserve original

Phase 6: Quality Check
   └─ Run pnpm lint:fix && pnpm typecheck
```

---

## Phase 1: Book Identification

### 1.1 Find the Book Note

Accept a book slug, title, or partial name as argument:

1. **Try exact slug match first**: Check if `content/{slug}.md` exists (convert spaces to hyphens, lowercase)
2. **If no exact match**: Use Grep to search for the title in book notes:
   ```text
   Grep pattern: "title:.*{search term}" with glob: "content/*.md"
   ```
3. **Filter to books only**: Read matching files and verify `type: book` in frontmatter

**Outcomes:**
- Single match → proceed with that file
- Multiple matches → list options for user to choose
- No match → list available books with `type: book`

### 1.2 Validate and Extract

Read the note and verify:
1. Frontmatter has `type: book`
2. Has required fields: `title`, `authors`

Extract and store:
- **Frontmatter**: title, authors, summary
- **Opening paragraph**: First paragraph before any `##` heading
- **Body sections**: All content from first `##` heading onwards

If not a book, inform user this skill only works on book notes.

---

## Phase 2: Parallel Research

Spawn **4 WebSearch agents in parallel** to gather book summary content:

```markdown
**Agent 1 - Key Insights:**
Task tool with subagent_type: "general-purpose"
prompt: "Use WebSearch to find key insights for the book '[Title]' by [Author].
  Query: '[Title]' key insights summary
  Extract: Main ideas, key concepts, important lessons.
  Return: Bullet list of 10-15 potential insights."

**Agent 2 - Main Ideas:**
Task tool with subagent_type: "general-purpose"
prompt: "Use WebSearch to find the main ideas of '[Title]' by [Author].
  Query: '[Title]' by [Author] main ideas book summary
  Extract: Core arguments, central thesis, framework.
  Return: The book's main message and supporting ideas."

**Agent 3 - Audience & Takeaways:**
Task tool with subagent_type: "general-purpose"
prompt: "Use WebSearch to find who should read '[Title]' and practical takeaways.
  Query: '[Title]' book review who should read
  Extract: Target audience, prerequisites, practical applications.
  Return: Audience description and actionable takeaways."

**Agent 4 - Notable Quotes:**
Task tool with subagent_type: "general-purpose"
prompt: "Use WebSearch to find the most popular quotes from '[Title]' by [Author].
  Query: '[Title]' [Author] best quotes site:goodreads.com
  Extract: The top 3 most impactful, memorable quotes from the book.
  Return: Exactly 3 quotes, each as a standalone blockquote."
```

Collect all results via `TaskOutput` (blocking).

### Writing Style Reference

Before generating content, read `.claude/skills/writing-style/SKILL.md` for the full writing guidelines. Key points:
- **Active voice**: "The author argues..." not "It is argued..."
- **No boilerplate**: Jump straight to insights, no "This book explores..."
- **End with emphasis**: Put the key point at the end of sentences
- **Everyday words**: "use" not "utilize", "help" not "facilitate"
- **No vague pronouns**: Name the thing, don't say "this leads to that"

---

## Phase 3: Content Synthesis

Using research results, generate four new sections:

### 3.1 Core Message

Write the book's thesis in 1-2 sentences:
- Capture the central argument
- Be concise (under 50 words)
- Make it memorable and quotable

**Example:**
> Small daily improvements compound into remarkable results. Success is not about massive action but consistent 1% gains that accumulate over time.

### 3.2 Key Insights

Generate 8-12 numbered insights (Blinkist-style "blinks"):

**Format:**
```markdown
1. **[Insight Title]** - [2-3 sentence explanation with specific detail]
```

**Guidelines:**
- Each insight should be standalone and valuable
- Use bold title for scannability
- Include concrete examples or data when available
- Progress from foundational to advanced concepts
- Avoid generic statements - be specific

**Example:**
```markdown
1. **The 1% Rule** - Improving by just 1% each day leads to being 37 times better after one year. This compound effect works because small gains build on each other, turning marginal improvements into transformative results.

2. **Systems Over Goals** - Goals are about the results you want; systems are about the processes that lead to results. Winners and losers often have the same goals—what differs is the systems they follow.
```

### 3.3 Notable Quotes

Select 3 quotes that:
- Capture the book's core philosophy
- Are memorable and shareable
- Represent different aspects of the book

**Format:**
```markdown
> "Quote text here."
```

Just clean blockquotes, no context needed.

### 3.4 Who Should Read This

Write 1-2 paragraphs describing the ideal reader:
- Professional context (entrepreneurs, managers, students)
- Problems they're trying to solve
- What they'll gain from the book
- Any prerequisites or related reading

**Example:**
> This book is essential for anyone who feels stuck in unproductive patterns or struggles to make lasting changes. It's particularly valuable for professionals looking to build better work habits, athletes seeking incremental performance gains, and anyone skeptical of "overnight success" narratives. No prior reading required—the concepts are accessible yet profound.

---

## Phase 4: User Review (BLOCKING GATE)

**This is a mandatory approval step.** Present the generated content to the user before saving.

### 4.1 Present Content

Display the four generated sections in a formatted preview:

```markdown
## Preview of Enhanced Content

### Core Message
[Generated core message]

### Key Insights
[Generated 8-12 insights]

### Notable Quotes
[3 blockquotes]

### Who Should Read This
[Generated audience description]
```

### 4.2 Request Approval

Use the `AskUserQuestion` tool:

```yaml
question: "Does this enhancement look good?"
header: "Review"
multiSelect: false
options:
  - label: "Save"
    description: "Add these sections to the book note"
  - label: "Regenerate"
    description: "Try again with different focus"
  - label: "Edit"
    description: "Tell me what to change"
  - label: "Cancel"
    description: "Don't modify the note"
```

### 4.3 Handle Response

- **Save**: Proceed to Phase 5
- **Regenerate**: Return to Phase 2 with modified queries
- **Edit**: Apply user feedback, show updated preview
- **Cancel**: Exit without changes

**Do NOT proceed to Phase 5 without explicit user approval.**

---

## Phase 5: Save Enhanced Note

### 5.1 Structure the Enhanced Content

Insert new sections after the opening paragraph, before existing headings:

```markdown
---
(existing frontmatter unchanged)
---

(existing opening paragraph preserved)

## Core Message

[Generated core message]

## Key Insights

1. **[Title]** - [Explanation]
2. **[Title]** - [Explanation]
...

## Notable Quotes

> "Quote 1 here."

> "Quote 2 here."

> "Quote 3 here."

## Who Should Read This

[Generated audience description]

---

(original body content preserved below)

## [Original sections]
...
```

### 5.2 Preserve Original Content

**Critical:** Never delete existing content:
- Keep all frontmatter fields
- Keep opening paragraph
- Keep all original `##` sections and their content
- Keep all wiki-links `[[slug]]`

The `---` separator clearly divides generated content from original notes.

### 5.3 Write the File

Use the Edit tool to insert the new sections at the correct position.

### 5.4 Confirmation

Report to user:
```markdown
✓ Enhanced: content/{slug}.md
  - Core Message: [word count] words
  - Key Insights: [count] insights
  - Notable Quotes: 3 quotes
  - Who Should Read: added
  - Original content: preserved
```

---

## Phase 6: Quality Check

Run linter and type check to catch any issues:

```bash
pnpm lint:fix && pnpm typecheck
```

If errors are found, fix them before completing the task.

---

## Error Recovery

| Error | Recovery |
|-------|----------|
| Book not found | List available books with `type: book` |
| Not a book type | Inform user skill only works on books |
| WebSearch fails | Retry with alternative query patterns |
| User rejects content | Allow regeneration with feedback |
| No insights found | Try broader search terms |

---

## Quality Checklist

Before saving, verify:
- [ ] Book note exists and has `type: book`
- [ ] Core Message is under 50 words
- [ ] Generated 8-12 Key Insights
- [ ] Each insight has bold title and explanation
- [ ] 3 notable quotes included
- [ ] Who Should Read section is present
- [ ] Original content preserved
- [ ] User explicitly approved changes
- [ ] Markdown formatting is valid
