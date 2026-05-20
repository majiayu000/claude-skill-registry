---
name: managing-blog-ideas
description: Create and develop blog post ideas. Use when asked to "create a blog idea", "start a blog post", "expand blog outline", "develop this post idea", "update blog draft", or "list blog ideas".
allowed-tools: Read, Write, Edit, Glob, Grep, AskUserQuestion
---

# Managing Blog Ideas

Create and evolve blog post ideas from initial concept to publication-ready draft.

## Location

All blog ideas live in `content/blog-ideas/` and are excluded from Nuxt Content publishing.

## Mode Detection

1. **List mode**: User asks "what blog ideas" or "list blog ideas" → list all files in `content/blog-ideas/`
2. **Update mode**: User provides slug/title that exists → load and update
3. **Create mode**: New topic → create fresh blog idea

---

## CREATE Mode

### Phase 1: Gather Information

1. If topic not provided, ask:
   ```yaml
   question: "What topic would you like to write about?"
   header: "Blog Topic"
   ```

2. Search Second Brain for related notes:
   ```text
   Grep pattern: "{topic keywords}" glob: "content/*.md"
   ```

3. Present found connections to user

### Phase 2: Generate Blog Idea

**Frontmatter:**
```yaml
---
title: "Working Title"
status: idea
tags:
  - tag-1
  - tag-2
core_idea: "Single sentence thesis"
target_audience: "Vue/Nuxt developers who..."
reader_outcome: "After reading, they will [think/feel/do X]"
created: {today YYYY-MM-DD}
updated: {today YYYY-MM-DD}
---
```

**Body structure:**
1. Core Idea section (1-2 sentences)
2. Outline with 3-5 sections (H3 headers with bullet points)
3. Source Notes (wiki-links to related Second Brain notes)
4. Open Questions (what needs research/clarification)

### Phase 3: User Review

Present the generated content and ask:
```yaml
question: "Does this blog idea look good?"
header: "Review"
multiSelect: false
options:
  - label: "Save"
    description: "Create the blog idea file"
  - label: "Edit"
    description: "Tell me what to change"
```

### Phase 4: Save

Generate slug: lowercase title, spaces to hyphens, remove special characters.
Save to `content/blog-ideas/{slug}.md`.

Confirm creation with file path and summary.

---

## UPDATE Mode

### Phase 1: Load Existing

1. Find the file:
   ```text
   Glob: content/blog-ideas/{slug}*.md
   ```
2. Read and display current state:
   - Status
   - Last updated
   - Current outline structure
   - Source notes count

### Phase 2: Choose Update Action

```yaml
question: "What would you like to do with this blog idea?"
header: "Update"
multiSelect: false
options:
  - label: "Expand outline"
    description: "Add more sections or detail to existing sections"
  - label: "Draft a section"
    description: "Write content for one of the outline sections"
  - label: "Polish & Edit"
    description: "Cut filler, tighten prose, improve skimmability"
  - label: "Find sources"
    description: "Search Second Brain for more related notes"
  - label: "Update status"
    description: "Move to next stage (idea → outline → draft → ready)"
  - label: "Refine core idea"
    description: "Sharpen the thesis or angle"
  - label: "Prep for distribution"
    description: "Create teaser, thread points, and pull quotes"
```

### Phase 3: Execute Update

**Expand outline:**
- Read current sections
- Ask which section to expand OR add new section
- Generate additional bullet points / subsections

**Draft a section:**
- Present section titles
- User picks one
- Generate draft prose following writing-style skill (especially Alexander's Voice Profile)
- Insert under `## Draft Sections`

**Polish & Edit:**
- Review draft sections for filler and bloat
- Apply the Ruthless Editing Checklist:
  - Cut 20-30% of word count
  - Remove filler phrases: "very", "really", "just", "actually", "in order to", "basically", "essentially"
  - Replace "in terms of" with direct language
  - Cut redundant qualifiers ("completely unique" → "unique")
  - Delete weak sentence starters ("I think that", "It seems like", "In my opinion")
- Improve skimmability (see Skimmability Guidelines)
- Suggest reading the draft aloud to catch awkward phrasing

**Find sources:**
- Extract keywords from title/outline
- Search Second Brain
- Present candidates
- Add selected links to Source Notes

**Update status:**
- Validate readiness for next stage
- Update frontmatter status field

**Refine core idea:**
- Present current core_idea
- Discuss with user
- Update frontmatter

**Prep for distribution:**
- Generate teaser hook (2-3 sentences to post before publishing)
- Extract 3-5 thread points (key insights as standalone posts)
- Identify 2-3 pull quote candidates (shareable insights)
- Add to `## Distribution` section

### Phase 4: Save

- Apply edits
- Update `updated` date
- Confirm changes

---

## Status Definitions

| Status | Criteria | Next Step |
|--------|----------|-----------|
| `idea` | Has title and basic core_idea | Develop outline |
| `outline` | 3+ sections with bullet points | Draft sections |
| `draft` | At least one section has prose | Complete all sections |
| `ready` | All sections drafted, reviewed | Publish to blog |

---

## Blog Idea Template

```markdown
---
title: "[Action Verb] + [Specific Outcome] + [Context/Tool]"
status: idea
tags:
  - topic-1
core_idea: "Single sentence thesis"
target_audience: "Vue/Nuxt developers who..."
reader_outcome: "After reading, they will [think/feel/do X]"
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

## Core Idea

[1-2 sentences: What's the main argument? What will readers take away?]

## Outline

### 1. [Hook: Problem Statement or Observation]
- Open with pain point or personal observation
- First person welcome
- Never "In this post, we will..."

### 2. The Problem
- Concrete example of the pain point
- Real scenario, specific details

### 3. The Solution
- High-level approach
- Why this works

### 4. [Implementation Step]
- Code + explanation
- Before/after with ❌/✅ if applicable

### 5. When to Use This
- Specific scenarios where this applies

### 6. When NOT to Use This
- Honest assessment of limitations
- Alternative approaches

### 7. Conclusion
- Key insight (1-2 sentences)
- Ask a question to spark discussion
- Clear call-to-action
- Optional: related content links

## Source Notes

[Wiki-links to Second Brain notes that inform this post]

- [[note-slug]] - How this informs the post

## Draft Sections

[Write draft content following the Drafting Guidelines below]

## Distribution

[Prepare content for social promotion]

### Teaser Hook
[2-3 sentences to post before/when publishing - create curiosity]

### Thread Points
[Key insights as standalone posts for social threads]
1.
2.
3.

### Pull Quotes
[Shareable insights that stand alone]
-

## Open Questions

- Question I need to answer before writing
- Research needed
```

---

## Title Formula

Good titles combine **curiosity + value promise**. The reader should know what they'll learn AND be intrigued enough to click.

### Formula
```
[Action Verb] + [Specific Outcome] + [Context/Tool]
```

### Examples

**Bad titles:**
- "Vue Reactivity" (too vague)
- "How I Use Composables" (no clear benefit)
- "Some Thoughts on Testing" (weak, unclear)

**Good titles:**
- "Stop Fighting Vue Reactivity: The Mental Model That Finally Clicked"
- "3 Composable Patterns That Eliminated 500 Lines of Duplicate Code"
- "Why Your E2E Tests Are Slow (And the 80/20 Fix)"

### Checklist
- [ ] Would I click this in a busy feed?
- [ ] Does it promise a specific outcome?
- [ ] Does it create curiosity?
- [ ] Is it honest about what the post delivers?

---

## Skimmability Guidelines

Most readers skim before committing to read. Make your post scannable.

### Paragraph Rules
- **2-4 lines max** per paragraph (phone screens are narrow)
- One idea per paragraph
- If a paragraph has two ideas, split it

### Subheading Rules
- Add subheading every **3-5 paragraphs**
- Subheadings should be informative, not clever ("The Fix" not "Plot Twist")
- Reader should understand the post from subheadings alone

### Emphasis Rules
- **Bold the key insight** in each major section (one per section)
- Use bold for emphasis, not ALL CAPS or italics
- Don't over-bold; if everything is bold, nothing is

### Visual Breaks
- Use bullet lists for 3+ related items
- Add code blocks, diagrams, or callouts to break up text walls
- Empty lines between sections

---

## Ruthless Editing Checklist

Apply when polishing drafts:

### Filler Phrases to Cut
- "very", "really", "just", "actually"
- "in order to" → "to"
- "basically", "essentially", "fundamentally"
- "in terms of" → rephrase directly
- "the fact that" → cut entirely
- "I think that", "I believe that" → just state it

### Redundancies to Remove
- "completely unique" → "unique"
- "absolutely essential" → "essential"
- "past experience" → "experience"
- "end result" → "result"

### Target
- Cut **20-30%** of first draft word count
- If you can remove a word without losing meaning, remove it

### The Read-Aloud Test
- Read the draft aloud
- Mark where you stumble or run out of breath
- Those spots need shorter sentences or clearer phrasing

---

## Quality Checklist

Before saving:
- [ ] Title is specific and compelling (Action Verb + Outcome + Context)
- [ ] Title creates curiosity AND promises value
- [ ] Core idea is a clear thesis (assertion, not description)
- [ ] `reader_outcome` explicitly states what they'll gain
- [ ] At least 3 outline sections
- [ ] At least 2 wiki-links to source notes
- [ ] Tags match existing taxonomy
- [ ] Status accurately reflects completeness

**For drafts, also check:**
- [ ] Opens with problem/observation, never "In this post..."
- [ ] Uses first-person where appropriate ("I", "In my experience")
- [ ] Paragraphs are 2-4 lines max
- [ ] Key insight bolded in each section
- [ ] Includes ❌/✅ markers for comparisons
- [ ] Has at least one visual element (diagram, table, or callout)
- [ ] Acknowledges limitations or alternatives
- [ ] Ends with question or clear CTA
- [ ] Uses everyday words, not jargon
- [ ] Has teaser/thread candidates identified (for `ready` status)

---

## Validation

**Wiki-link check:** Each `[[link]]` should exist in `content/`.

**Status progression:**
- Don't advance to `outline` without 3+ sections
- Don't advance to `draft` without prose content
- Don't advance to `ready` without all sections drafted

---

## Drafting Guidelines

When generating draft content, apply Alexander's voice from writing-style skill:

### Opening Paragraphs
Write openings that:
1. Start with a problem or observation, not "In this post, we will..."
2. Use first-person when sharing experience
3. Hook with a relatable developer struggle

Example openers:
- "I once worked on a project that wanted to..." (personal anecdote)
- "After [event], I started thinking about..." (observation)
- "Manual [task] gets old fast." (pain point)
- "Here's the thing: [unexpected insight]" (hook)

### Body Structure Pattern
For each major section:
1. **State the problem** this section solves
2. **Show before/after** with ❌/✅ where appropriate
3. **Provide working code** with inline comments
4. **Acknowledge limitations** or when this doesn't apply

### Code Examples
- Include realistic context (real file names, plausible data)
- Add comments explaining the "why", not just the "what"
- Show progressive refinement when teaching patterns

### Visual Elements to Include
- [ ] At least one Mermaid diagram for complex flows
- [ ] Comparison table if presenting multiple options
- [ ] File tree for architectural posts
- [ ] Callout boxes for tips and warnings

### Conclusion Pattern
End with:
1. Brief summary of key insight (1-2 sentences)
2. Honest assessment of trade-offs
3. **Ask a question** to spark discussion (e.g., "What patterns have you found for X?")
4. Clear call-to-action (try it, share feedback, etc.)
5. Optional: Link to related posts or resources
