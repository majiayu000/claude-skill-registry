---
name: holydocs-writing
description: Best practices for writing high-quality documentation with HolyDocs. Use when the user wants to write docs, improve documentation quality, add new pages, review doc content, follow documentation style guides, or ask about how to write effective technical documentation. Also use when writing or editing any .mdx file in a docs project, creating changelogs, or structuring documentation content. This skill makes docs clearer, more scannable, and more effective.
---

# HolyDocs Documentation Writing Skill

## Core Philosophy

Documentation exists to help readers accomplish tasks. Every page should answer "what can I do here and how?" -- not describe features abstractly.

Good documentation is:
- **Task-oriented**: Readers arrive with a goal. Help them achieve it.
- **Scannable**: Most readers skim. Structure content so skimming works.
- **Concise**: Every sentence earns its place. Cut anything that doesn't help.
- **Accurate**: Wrong documentation is worse than no documentation.
- **Current**: Stale docs erode trust. Keep them in sync with the product.

Write for the reader who is in the middle of building something and needs an answer fast.

## The Diataxis Framework

Every HolyDocs page belongs to exactly one of four types. Don't mix them.

### 1. Tutorial (Learning-Oriented)

Teaches through doing. The reader follows along and builds something.

- Starts from zero, assumes nothing
- Has a clear end state the reader can verify
- Every step produces a visible result
- Never explains "why" at length -- save that for Explanation pages

Example titles: "Build your first docs site", "Deploy documentation in 5 minutes"

### 2. How-To Guide (Task-Oriented)

Solves a specific problem. The reader already knows what they want to do.

- Starts with the goal, not background
- Steps are practical and direct
- Covers edge cases and common errors
- Can assume basic product knowledge

Example titles: "How to add a custom domain", "How to configure OpenAPI integration"

### 3. Reference (Information-Oriented)

Describes the system precisely. The reader looks up specific details.

- Complete and accurate -- every option, every field
- Consistent structure (tables, parameter lists)
- No step-by-step instructions
- Organized for lookup, not reading

Example titles: "docs.json configuration reference", "MDX component props"

### 4. Explanation (Understanding-Oriented)

Builds mental models. The reader wants to understand how and why.

- Discusses concepts, trade-offs, and architecture
- Can reference other page types but doesn't replicate them
- Provides context that makes other pages more useful
- Answers "why is it this way?"

Example titles: "How the build pipeline works", "Understanding edge rendering"

## Page Structure Template

Every MDX page follows this structure:

```mdx
---
title: Clear, Specific Title
description: One sentence that tells the reader what they'll learn. 120-160 chars for SEO.
---

## Overview

2-3 sentences explaining what this page covers and why it matters.

## [Main Content Sections]

The substance of the page. Use components to break up walls of text.

## Next Steps

<CardGroup cols={2}>
  <Card title="Related Page" icon="arrow-right" href="/path">
    Brief description of where to go next.
  </Card>
</CardGroup>
```

### Frontmatter Requirements

Every page must have:
- `title`: Under 60 characters, includes primary keyword
- `description`: 120-160 characters, specific about what the reader learns

Optional but recommended:
- `icon`: Lucide icon name for sidebar
- `sidebarTitle`: Shorter title if the full title is long

## Writing Style Rules

### Voice

- **Active voice**: "HolyDocs deploys your docs" not "Your docs are deployed by HolyDocs"
- **Second person**: "You can configure..." not "Users can configure..."
- **Present tense**: "This creates a file" not "This will create a file"
- **Imperative for instructions**: "Run the command" not "You should run the command"

### Brevity

- **Short sentences**: 25 words max. Break complex sentences into two.
- **Short paragraphs**: 3 sentences max. Readers scan, not read.
- **No filler words**: Cut "basically", "simply", "just", "actually", "really", "very"
- **Specific over vague**: "Takes 30 seconds" not "Takes a moment"

### Formatting

- **Bold** for UI elements: **Settings > Domains**
- `Code` for: file names, commands, config values, API paths
- *Italics*: rarely, only for emphasis
- Links: descriptive text, never "click here"

### Grammar

- Oxford comma: always
- Contractions: allowed (it's, don't, you'll)
- Abbreviations: spell out on first use, then abbreviate
- Numbers: spell out one through nine, use digits for 10+
- Headings: sentence case ("Getting started") not title case ("Getting Started")
- Don't use "please" in instructions
- Don't start sentences with "Note:" -- use a Callout instead

For full grammar rules and word list, read `references/style-guide.md`.

## Component Usage Patterns

HolyDocs ships 38 MDX components. Here's when to use the most important ones.

### Callout

Highlighted message box for supplementary information.

```mdx
<Callout type="warning">
  Changing your project slug invalidates all existing URLs. Set up redirects first.
</Callout>
```

**Types**: `note`, `warning`, `tip`, `info`, `caution`, `check`, `danger`

**Rules**:
- One callout per section max
- Don't put critical information in callouts -- if it's critical, it belongs in the main text
- Don't stack callouts back to back
- Use `warning` and `danger` only when there's genuine risk

### CardGroup and Card

Grid of clickable cards for navigation and feature overviews.

```mdx
<CardGroup cols={2}>
  <Card title="Authentication" icon="lock" href="/guides/auth">
    Set up user authentication with OAuth or API keys.
  </Card>
  <Card title="Deployment" icon="rocket" href="/guides/deploy">
    Deploy your docs to production in one command.
  </Card>
</CardGroup>
```

**Rules**:
- Use `cols={2}` for 2-4 cards, `cols={3}` for 5-6
- Never more than 6 cards in a group
- Use at page top for feature overviews, at page bottom for next steps
- Every card needs an `href` -- decorative cards are a waste

### Tabs and Tab

Tabbed content switcher for alternatives.

```mdx
<Tabs>
  <Tab title="npm">
    ```bash
    npm install @holydocs/cli
    ```
  </Tab>
  <Tab title="pnpm">
    ```bash
    pnpm add @holydocs/cli
    ```
  </Tab>
  <Tab title="yarn">
    ```bash
    yarn add @holydocs/cli
    ```
  </Tab>
</Tabs>
```

**Use for**: language alternatives, platform alternatives, mode alternatives (Dashboard/CLI/API)

**Rules**:
- Never nest Tabs inside Tabs
- Tab titles should be short (one or two words)
- All tabs should show equivalent content

### Steps and Step

Numbered sequential instructions.

```mdx
<Steps>
  <Step title="Install the CLI">
    ```bash
    npm install -g @holydocs/cli
    ```
  </Step>
  <Step title="Authenticate">
    ```bash
    holydocs login
    ```
  </Step>
  <Step title="Deploy">
    ```bash
    holydocs deploy
    ```
  </Step>
</Steps>
```

**Rules**:
- Use for 3-7 sequential steps
- Each step must be completable and verifiable
- Don't use Steps for non-sequential lists
- Don't use Steps with only 2 steps -- use a paragraph instead

### Accordion and AccordionGroup

Collapsible content for optional details.

```mdx
<AccordionGroup>
  <Accordion title="Why is my build failing?">
    Check that your `docs.json` is valid JSON and all referenced pages exist.
  </Accordion>
  <Accordion title="How do I clear the cache?">
    Run `holydocs cache clear` or trigger a redeploy from the dashboard.
  </Accordion>
</AccordionGroup>
```

**Use for**: FAQ sections, troubleshooting, optional reference details

**Rules**:
- Don't use AccordionGroup with only 1 accordion
- Don't hide critical information inside accordions
- Good for long reference content that most readers skip

### CodeGroup

Multiple code blocks shown in tabs.

```mdx
<CodeGroup>
  ```javascript index.js
  const holydocs = require('@holydocs/sdk');
  ```
  ```python main.py
  import holydocs
  ```
</CodeGroup>
```

**Use for**: same logic in multiple languages, same operation with different tools

### Tables

Use for reference data: props, config options, API parameters.

```mdx
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Project display name |
| `theme` | string | No | Visual theme (default: `mint`) |
```

**Rules**:
- Always include headers
- Keep columns to 3-5
- Align content left, except for boolean/status columns

For all component patterns with detailed examples, read `references/component-patterns.md`.

## Code Examples

- Always specify the language: ` ```javascript ` not just ` ``` `
- Add titles for file names: ` ```typescript docs.json `
- Keep examples under 20 lines. Show only what's relevant.
- Use realistic values, not "foo/bar" placeholders
- Show complete working examples, not fragments that need assembly
- If an example needs context, add a one-line comment at the top

Bad:
```javascript
const x = createThing({ a: "b" });
```

Good:
```javascript
const client = createHolyDocs({
  projectId: "my-docs-site",
  apiKey: process.env.HOLYDOCS_API_KEY,
});
```

## Headings

- Use `##` for main sections (these generate TOC entries)
- Use `###` for subsections
- Never skip levels (don't go from `##` to `####`)
- Maximum 6-8 `##` headings per page
- Headings should be scannable -- a reader should understand the page from headings alone
- Keep headings specific: "Configure custom domains" not "Configuration"

## Page Length

- Tutorials: 800-1500 words. Long enough to be complete, short enough to finish.
- How-to guides: 400-800 words. Get to the point.
- Reference: As long as needed. Completeness matters more than brevity.
- Explanation: 600-1200 words. Deep enough to be useful, focused enough to hold attention.

If a page exceeds these ranges, consider splitting it into multiple pages.

## SEO

- Every page needs `title` (under 60 chars) and `description` (120-160 chars)
- Include the primary keyword in the title and first paragraph
- Use descriptive internal link text (not "click here")
- Structure content with headings that target search queries
- Headings should include relevant keywords naturally
- Images need alt text

For the full SEO checklist, read `references/seo-checklist.md`.

## Common Anti-Patterns

### Wall of Text
Problem: Paragraphs of 5+ sentences with no visual breaks.
Fix: Add headings, use components, break into shorter paragraphs.

### Callout Abuse
Problem: Three or more callouts in a section.
Fix: Move most information to the main text. Keep one callout max.

### Vague Openings
Problem: "In this guide, we will explore the various aspects of configuring..."
Fix: "This guide covers domain configuration: adding custom domains, setting up SSL, and configuring redirects."

### Missing Next Steps
Problem: Page ends abruptly after the last section.
Fix: Add a CardGroup linking to related pages.

### Screenshots Over Code
Problem: Screenshot of a terminal command or config file.
Fix: Use a code block. Readers need to copy-paste.

### Outdated Content
Problem: Examples reference deprecated APIs or old UI.
Fix: Review docs every release. Add a changelog entry when docs change.

## Quality Checklist

Before publishing any page:

- [ ] Page type is clear (tutorial/how-to/reference/explanation)
- [ ] Title under 60 chars with primary keyword
- [ ] Description 120-160 chars
- [ ] Overview section explains what and why
- [ ] Headings are scannable
- [ ] No paragraphs longer than 3 sentences
- [ ] Code examples are complete and use realistic values
- [ ] Components are used appropriately (not overused)
- [ ] Page ends with next steps or related links
- [ ] All links work
- [ ] No filler words

## Reference Pointers

- For component patterns with examples, read `references/component-patterns.md`
- For the SEO checklist, read `references/seo-checklist.md`
- For the style guide details, read `references/style-guide.md`
