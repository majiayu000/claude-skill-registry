---
name: skill-stack-newsletter-writer
description: Format and structure skill for Skill Stack weekly newsletter. Handles frontmatter, sections, skill packages, and calls-to-action. REQUIRES writing-style skill for prose quality.
requires: [writing-style]
---

# Skill Stack Newsletter Writer

**This skill handles newsletter FORMAT only.** Writing style comes from the root `writing-style` skill.

---

## Newsletter Structure

### Frontmatter Schema

```yaml
---
title: "[Skill Name]"
issue: [number]
date: "YYYY-MM-DD"
skill: [skill-slug]
thumbnail: "/images/thumbnails/[slug].png"
description: "[SEO description: 150-160 chars, keyword + insight + deliverable]"
tags: ["tag1", "tag2", "tag3"]
---
```

**Field Notes**:
- `title`: The skill name, clean. No subtitles like "The X That Changed Y"
- `skill`: Maps to the downloadable skill package slug
- `thumbnail`: Risograph style (see image-prompt-generator)
- `description`: SEO-optimized but punchy (see writing-style for guidelines)
- `tags`: 3-5 relevant keywords, lowercase

---

## Content Sections

Each newsletter follows this rhythm:

### 1. Opening Hook (150-200 words)

Personal story or observation. Ground the reader in something real before introducing the skill concept.

- Specific place, time, sensory detail
- Something you found, discovered, encountered
- The seed that led to the insight

No throat-clearing. Start in media res.

### 2. The Discovery (100-150 words)

Bridge from story to skill. The moment you understood something about how this works.

- "Fast forward..."
- "Here's what I discovered..."
- A single key insight, stated directly

### 3. Core Mechanism (200-300 words)

Explain HOW the skill works. This is the teaching section.

- What most people get wrong
- The counterintuitive insight
- Concrete examples (actual prompts, actual output)

Use section break (---) not headers here. Let prose flow.

### 4. The Wizard/Workflow (100-150 words)

Walk through how to use it. Conversational but specific.

- Step 1, step 2, step 3
- What the user does at each stage
- What they get at the end

### 5. Skill Package (formatted block)

Always include this exact structure:

```markdown
**The skill package includes:**
- `SKILL.md` — [Brief description]
- `WIZARD.md` — [Brief description]
- `templates/` — [Brief description]
- `references/` — [Optional: examples, samples]
```

Plus setup requirements: time, inputs needed.

### 6. Ways to Use (2-4 bullet points)

Concrete applications. Three sentences max per use case.

### 7. Next Week Teaser (1-2 sentences)

Preview next skill. Build anticipation without overselling.

### 8. Closing + CTA

One sentence that lands. Then download link.

```markdown
[Download the [Skill Name] →]
```

---

## Section Breaks

Use `---` (horizontal rule) between major sections instead of headers.

Only use H1 for the title. Avoid H2/H3 within the body. Let prose breathe.

---

## Length Target

800-1200 words total. Dense but readable.

---

## Example: Issue 1 Structure

```
# Voice Matching

[Opening: Didion discovery at Berkeley, 180 words]

---

[Discovery: Client project, 120 words]

---

[Core mechanism: Why examples beat descriptions, 250 words]

---

[Wizard walkthrough, 100 words]

---

**The skill package includes:**
[Package block]

[Ways to use, 80 words]

[Next week teaser]

[Closing line + CTA]
```

---

## Checklist Before Publish

- [ ] Title is clean (no AI-tell subtitles)
- [ ] Description is 150-160 chars, SEO-optimized
- [ ] Thumbnail exists at path and uses risograph style
- [ ] Opening starts with specific scene, not abstract concept
- [ ] No headers in body (use --- breaks)
- [ ] Core mechanism includes concrete examples
- [ ] Skill package block is complete
- [ ] Next week teaser included
- [ ] CTA link present
- [ ] writing-style checklist passed (separate skill)

---

*This skill handles structure. Run writing-style for prose quality.*
