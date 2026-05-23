---
name: medium-posts-creator
description: "Transform arbitrary text into well-structured Medium article drafts following a four-part structure: three variations of article title, Benefits from solution, Problem description, and Solution itself. Use when user requests: creating a Medium article from text, writing a blog post about a topic, transforming content into a Medium draft, or any request to transform text into a publishable article format. Includes Medium formatting guidelines, optional writing style suggestions, and enhancement tips for SEO, CTAs, and engagement."
---

# Medium Posts Creator

## Quick Start

Transform text into a Medium article draft by generating the required 4-part structure with title variations, benefits, problem description, and solution.

## Workflow

### Step 1: Analyze Input Text

Read and understand the provided text:
- Extract core message or topic
- Identify the problem being discussed
- Understand the solution being proposed
- Note key benefits or outcomes

### Step 2: Generate Title Variations

Create 3 distinct title options:

**Title 1**: Direct and descriptive
- Clearly states the topic
- Includes primary keyword if applicable
- Example: "How to Optimize React Performance With These 5 Techniques"

**Title 2**: Benefit-oriented
- Focuses on what the reader gains
- Uses emotional or actionable language
- Example: "Speed Up Your React App: 5 Performance Techniques That Work"

**Title 3**: Curiosity-driven
- Creates intrigue without clickbait
- Uses questions or contrasts
- Example: "Why Your React App Is Slow (and 5 Ways to Fix It)"

For title optimization strategies, see [enhancement-tips.md](enhancement-tips.md#title-optimization).

### Step 3: Structure the Article

Create the 4-part structure in this exact order:

**Benefits Section**
- List 3-5 key benefits of the solution
- Use bullet points for readability
- Focus on outcomes and improvements
- Keep benefits specific and measurable

**Problem Section**
- Clearly describe the problem being solved
- Explain why the problem matters
- Include personal experience or examples if applicable
- Build urgency or relevance

**Solution Section**
- Present the solution step-by-step
- Provide code examples if technical
- Explain *why* the solution works
- Include implementation details

### Step 4: Apply Medium Formatting

Format the article for Medium readability:

Use headers:
- `##` for "Benefits", "Problem", "Solution" sections
- `###` for subsections within each section
- Keep headers clear and descriptive

Apply text formatting:
- Use `**bold**` for key terms and benefits
- Use `*italic*` for emphasis
- Use code blocks for technical content

Structure for readability:
- Use lists (ordered or unordered) for multiple items
- Keep paragraphs short (2-4 sentences)
- Add visual breaks every 150-200 words

For complete formatting guidelines, see [formatting.md](formatting.md).

### Step 5: Enhance with Style and Engagement

Optional improvements to consider:

**Writing Style**
- Choose an appropriate tone (conversational, professional, enthusiastic)
- Mix short and medium sentences for rhythm
- Use personal voice ("I", "my experience")
- Add opening hooks and transitions

For style guidelines, see [writing-style.md](writing-style.md).

**Engagement Elements**
- Add questions throughout the article
- Include personal anecdotes or examples
- Use rhetorical questions to maintain interest
- Add a call-to-action at the end

**SEO and Optimization**
- Include primary keyword in title and content
- Write a compelling first paragraph
- Use benefit-oriented language
- Consider title keywords for searchability

For enhancement tips (SEO, CTAs, engagement hooks), see [enhancement-tips.md](enhancement-tips.md).

## Output Format

The final article draft should follow this structure:

```markdown
# [Title 1: Direct]

[Optional: Brief intro paragraph]

## Benefits

- [Benefit 1]
- [Benefit 2]
- [Benefit 3]

## Problem

[Problem description with context and relevance]

## Solution

[Step-by-step solution with examples]

[Optional: Conclusion or CTA]
```

## Title Options Presentation

Present all 3 title variations at the start:

```markdown
# Title Options:
1. [Title 1 - Direct]
2. [Title 2 - Benefit-oriented]
3. [Title 3 - Curiosity-driven]

# [Selected Title]
```

Let the user know they can choose or modify titles.

## When to Reference Additional Guides

- **Formatting questions**: See [formatting.md](formatting.md) for Markdown syntax and structure
- **Style guidance**: See [writing-style.md](writing-style.md) for tone, readability, and audience considerations
- **SEO/CTA/engagement**: See [enhancement-tips.md](enhancement-tips.md) for optimization strategies and engagement techniques

Load these references when specific guidance is needed. Don't load them all by default - keep the workflow efficient.
