---
name: marketing-writer
description: Writes marketing content (landing pages, tweets, emails) for product features with a casual, direct brand voice. Use when the user ships a feature, needs marketing copy, mentions "marketing content", "landing page", "tweet about", "launch email", "announce", or requests help promoting/explaining product features. Automatically analyzes the codebase to understand the product context before writing.
---

# Marketing Writer

Generate marketing content that converts, using your product's actual features and value proposition.

## Workflow

### 1. Understand the Product Context

When triggered, analyze the codebase to extract:
- **Core value proposition**: What problem does the product solve?
- **Key features**: What can users actually do?
- **Technical details**: Architecture, tech stack (for credibility if needed)
- **User workflows**: How people interact with the product

**Methods to gather context:**
- Read README.md, package.json, or similar project files
- Scan main application files (e.g., pages/, components/, src/)
- Check documentation if available
- Review route definitions or feature modules
- Examine database schemas if relevant

**If no codebase is provided:** Ask the user to either:
1. Upload the project files
2. Provide a GitHub repository URL (use github:get_file_contents)
3. Give a brief description of the product and feature

### 2. Select the Content Type

Based on user request, choose:
- **Landing page feature section**: Detailed explanation with Problem → Solution → Benefit
- **Tweet thread**: 5-7 tweets for social media announcement
- **Launch email**: Personal announcement to users
- **Social post**: Single LinkedIn/Twitter post
- **FAQ section**: Common questions answered

### 3. Load Templates and Brand Voice

**Before writing, read:**
- `references/templates.md` - Exact structure for each content type
- `references/brand-voice.md` - Tone, language rules, examples

### 4. Generate Content

**Follow these rules:**
1. Use the exact template structure from templates.md
2. Apply brand voice guidelines strictly (casual, no buzzwords, specific benefits)
3. Base content on actual product features, not assumptions
4. Include concrete numbers/outcomes when possible
5. Make the benefit obvious in the first sentence
6. Keep it scannable (short paragraphs, bullets)

**Content checklist:**
- [ ] Benefit clear in first sentence?
- [ ] No corporate buzzwords?
- [ ] Specific outcome mentioned?
- [ ] Simple language (8th-grade level)?
- [ ] Would you say this to a friend?
- [ ] CTA is obvious and easy?

### 5. Output Format

Present content ready to copy-paste:
```
[Content type header]

[Generated content following template exactly]

---
Quick edits if needed:
- [Optional: suggest 1-2 variations for key sentences]
```

## Key Principles

**Always read the codebase first.** Never guess what the product does. Real features > assumptions.

**Follow templates exactly.** They're battle-tested structures that convert.

**Brand voice is non-negotiable.** If it sounds corporate, rewrite it.

**Specific > Vague.** "Find files in 2 seconds" beats "Fast search".

**One clear benefit per section.** Don't overwhelm with feature lists.

## Examples

### User Request: "Write a landing page section for our new search feature"

**Step 1:** Scan codebase
- Found: ElasticSearch integration in `api/search.js`
- Found: Search UI in `components/SearchBar.tsx`
- Understanding: Full-text search across documents with instant results

**Step 2:** Load templates.md (Landing Page Feature Section)

**Step 3:** Load brand-voice.md

**Step 4:** Generate following template + brand voice

**Output:**
```markdown
### Instant Search

**The Problem:**
You have hundreds of files scattered across folders. Finding anything takes forever because you can't remember where you saved it.

**How It Works:**
Type what you're looking for and see results instantly. No waiting, no folder clicking. Search works on file names and content.

**What You Get:**
- Find any document in under 2 seconds
- Search across all your files at once  
- Works even if you only remember part of the name

[Try Search →]
```

---

### User Request: "Tweet thread about the feature I just shipped"

**If feature not obvious from context:** "Which feature did you ship? I'll scan the codebase to understand it first."

**Once identified, follow workflow above for Tweet Thread template.**

## Common Mistakes to Avoid

- Writing before understanding the product (read code first!)
- Using templates.md structure loosely (follow exactly)
- Ignoring brand-voice.md rules (check every sentence)
- Making up features or benefits (only use real ones)
- Being vague about outcomes (numbers matter)
- Corporate speak creeping in (friend test: would you say this?)

## When NOT to Use This Skill

- Technical documentation (that's different)
- Legal content or policies
- Internal communications (unless specifically requested)
- Customer support responses
- Blog posts or long-form content (too different in structure)
