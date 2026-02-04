---
name: jupyter-educational-notebook
description: Create educational and interactive Jupyter notebooks as SPAs that explain concepts, teach topics, create tutorials, illustrate ideas from text, or build blog posts. Use for interactive guides, demonstrations, explanations, documentation, or any content meant for end users and learners displayed via ipynb-viewer block. Keywords include educational notebook, tutorial notebook, interactive guide, blog notebook, SPA notebook, explain topic, illustrate concept, teach interactively.
---

# Educational Jupyter Notebook Creator

## Purpose

Create engaging, educational Jupyter notebooks designed as interactive Single Page Applications (SPAs) that explain concepts, teach topics, and illustrate ideas. These notebooks are displayed via the ipynb-viewer block and are meant for end users, learners, and clients—not for testing EDS blocks.

## When to Use This Skill

Use this skill when you need to:
- Create interactive tutorials or educational content
- Transform text content into engaging notebooks
- Build blog posts as interactive SPAs
- Explain complex concepts with demonstrations
- Create documentation with runnable examples
- Develop multi-part learning courses
- Illustrate topics from larger text pieces
- Generate interactive guides for end users

**Do NOT use this skill for:**
- Testing EDS blocks (use `jupyter-notebook-testing` skill instead)
- Debugging block decoration
- Creating test.html files
- Technical verification or QA testing

## Key Differences: Educational vs. Testing Notebooks

| Aspect | Testing Notebooks | Educational Notebooks |
|--------|-------------------|----------------------|
| **Audience** | Developers testing blocks | End users, learners, clients |
| **Purpose** | Verify block functionality | Teach and explain concepts |
| **Content ratio** | 30% markdown, 70% code | 60% markdown, 40% code |
| **Code style** | Technical verification | Illustrative examples |
| **Structure** | Ad-hoc test scenarios | Narrative flow with parts |
| **Language** | Technical jargon | Engaging, accessible |
| **Helper usage** | Always uses `testBlock()` | Uses pure JavaScript, sometimes helpers |
| **Goal** | Find bugs, verify behavior | Educate, demonstrate, engage |

## Auto-Wrapping in Notebook Mode (NEW)

When using the **notebook variation** (`| IPynb Viewer (notebook) |`), the viewer automatically wraps markdown cells with appropriate styling classes based on content patterns. This means you can write **pure markdown** without any HTML wrappers!

**How It Works:**

The viewer automatically detects cell types:

1. **Hero Cell** - First cell (index 0) with `# ` heading → wrapped with `ipynb-hero-cell`
2. **Intro Cell** - Early cells (index ≤ 2) with `## ` heading → wrapped with `ipynb-content-card` (thick 6px border)
3. **Transition Cell** - Short cells (≤3 lines) without headers → wrapped with `ipynb-transition-card`
4. **Content Cell** - All other cells → wrapped with `ipynb-content-card-thin` (thin 4px border)

**Benefits:**
- ✅ 90% less code to write
- ✅ Focus on content, not HTML wrappers
- ✅ Consistent visual presentation
- ✅ Backward compatible with existing HTML-wrapped cells

**Example:**

**Pure Markdown (Auto-Wrapped):**
```markdown
# 🎯 Tutorial Title

**Compelling tagline** with additional context
```

Automatically becomes:
```html
<div class="ipynb-hero-cell">
  <h1>🎯 Tutorial Title</h1>
  <p><strong>Compelling tagline</strong> with additional context</p>
</div>
```

**When to Use:**
- ✅ Notebook mode only (auto-wrapping doesn't activate in other modes)
- ✅ Simple content structures
- ✅ Focus on content creation speed
- ✅ Works for BOTH educational AND presentation style notebooks
- ✅ Can mix with custom HTML for fine-tuning specific cells
- ❌ Not for complex custom layouts throughout
- ❌ Not for other display modes (use manual HTML wrappers)

**Action Cards for Navigation (NEW):**

Create beautiful navigation links using pure markdown with action cards:

```markdown
# Getting Started Guide

Learn step by step.

<!-- action-cards -->

- [Installation](#)
- [Your First Block](#)
- [Advanced Topics](#)
```

**Features:**
- ✅ Pure markdown - no HTML required
- ✅ Works in any cell type (hero, content, intro, transition)
- ✅ **Smart link resolution** - Automatically finds matching headings at runtime
- ✅ No hardcoded cell IDs needed - just descriptive link text
- ✅ Consistent blue design - professional appearance
- ✅ Hover effects with animated arrows
- ✅ Perfect for navigation in hero cells or section introductions

**How it works:**
1. Add `<!-- action-cards -->` HTML comment in your markdown cell
2. Follow with a markdown list of links using `(#)` as placeholder
3. Write link text that matches heading text somewhere in your notebook
4. JavaScript automatically finds the matching cell and updates href
5. No maintenance needed when cells move or headings change

**Important:** The `<!-- action-cards -->` marker only applies to the **first list** that follows it. Any subsequent lists in the same cell will remain as normal bullet lists.

**Example matching:**
- `[Installation](#)` finds heading containing "Installation" (like "## Installation" or "### Installation Guide")
- `[Basic Concepts](#)` finds heading containing "Basic Concepts" (like "## Part 1: Basic Concepts")
- Link text doesn't need exact match - searches for headings that *contain* your link text

**Best Practices:**
- ✅ Use specific link text: `[Part 1: Introduction](#)` instead of just `[Introduction](#)`
- ✅ Make link text unique to avoid ambiguity
- ⚠️ If multiple headings match, it picks the **first one found** (in cell order)
- 💡 Tip: Use part numbers or descriptive prefixes to ensure unique matches

**When to use action cards:**
- Hero cells with navigation options
- Section introductions with quick links
- Tutorial navigation between parts
- Multi-section content flow
- Quick reference sections

### Link Types: Smart Navigation vs Repository Links

The ipynb-viewer block supports two independent link systems:

#### Smart Navigation Links (Internal Navigation)

Smart linking works for **ANY link with `(#)` as the href**, not just action cards. This makes internal navigation resilient to notebook changes.

**Activates when:** Link has `href="#"` (hash placeholder)
**Works in:** Action cards, regular markdown, inline text, tables, any link element

**Examples:**
```markdown
# Regular navigation links
Continue to [Next Section](#) or go [Back to Start](#).

# In tables
| Topic | Link |
|-------|------|
| Basics | [Learn the Basics](#) |
| Advanced | [Advanced Topics](#) |

# In lists (not action cards)
- [Introduction](#)
- [Getting Started](#)
- [Advanced Features](#)

# Action cards (same smart linking)
<!-- action-cards -->
- [Part 1](#)
- [Part 2](#)
```

**Key points:**
- No hardcoded cell IDs needed
- Links adapt when cells are reordered
- Case-insensitive matching
- Ignores emojis and special characters in headings

#### Repository Links (External Documentation)

Links ending in `.md` automatically convert to GitHub URLs using the notebook's `repo` metadata.

**Activates when:** Link ends in `.md`
**Requires:** `repo` field in notebook metadata

**Setup:**
```json
{
  "metadata": {
    "repo": "https://github.com/username/project"
  }
}
```

**Examples:**
```markdown
Learn more in [Complete Guide](docs/guide.md)

Reference the [API Documentation](docs/api-reference.md)

See [Architecture Overview](docs/architecture.md) for details
```

These convert to full GitHub URLs: `https://github.com/username/project/blob/main/docs/guide.md`

**When to use repository links:**
- Link to comprehensive documentation
- Reference API docs or technical specs
- Point to code examples in the repo
- Provide "deep dive" resources

#### Using Both Together

Both systems work independently and can be mixed:

```markdown
# 🎓 Tutorial Navigation

<!-- action-cards -->
- [Next Lesson](#)         <!-- Smart link: internal navigation -->
- [Previous Lesson](#)     <!-- Smart link: internal navigation -->

## Additional Resources
- [Architecture Guide](docs/architecture.md)  <!-- Repo link: external -->
- [API Reference](docs/api.md)               <!-- Repo link: external -->

Continue to the [practice exercises](#) when ready.  <!-- Smart link: internal -->
```

**Mixing Auto-Wrapping with Custom HTML:**
You can combine both approaches in the same notebook:
- Use pure markdown for most cells (auto-wrapped)
- Add custom HTML wrapper for specific cells needing special styling
- Example: Hero cell with custom gradient or specific color scheme

```markdown
<!-- Custom HTML for special styling -->
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px; padding: 32px; margin: 0; color: white;">

# Special Section

This cell has custom purple gradient styling

</div>
```

**Terminology clarification:**
- **"Presentation"** = non-interactive notebook (no runnable code cells)
- **"Educational"** = interactive notebook (runnable code cells for learning)
- **"Notebook mode"** = display mode setting (`| IPynb Viewer (notebook) |`)
- Auto-wrapping works in notebook mode for BOTH presentation AND educational notebooks

## Educational Notebook Structure

### Essential Components

Every educational notebook should include:

#### 1. Header Cell (Markdown)
```markdown
# Title with Emoji 📓

Brief introduction explaining what this notebook covers and who it's for.

**What you'll learn:**
- Key concept 1
- Key concept 2
- Key concept 3
```

#### 2. Table of Contents (Markdown)
```markdown
## 📋 Table of Contents

- [Part 1: Introduction](#part-1-introduction)
- [Part 2: Core Concepts](#part-2-core-concepts)
- [Part 3: Advanced Topics](#part-3-advanced-topics)
- [Resources & Next Steps](#resources-next-steps)
```

**IMPORTANT - Hash Link Format:**
- Links must match h2 header IDs exactly
- IDs are auto-generated: lowercase, spaces→hyphens, special chars removed
- Emojis are removed but don't leave leading hyphens
- Examples:
  - `## 🚀 Part 1: Introduction` → `#part-1-introduction`
  - `## Resources & Next Steps` → `#resources-next-steps`
  - `## What's New?` → `#whats-new`

#### 3. Part Sections (Markdown + Code)
```markdown
## 🚀 Part 1: Introduction

Explanation text with context and background.

Key points:
- Point 1
- Point 2

Let's see this in action...
```

#### 4. Interactive Code Cells
```javascript
// Clear, explanatory comments
const demonstration = 'Show the concept in action';
console.log('Helpful output:', demonstration);

// Return value for display
return demonstration;
```

#### 5. Summary/Resources (Markdown)
```markdown
## 📚 Resources & Next Steps

**What you learned:**
- Summary point 1
- Summary point 2

**Next steps:**
- Action item 1
- Action item 2

**Learn more:**
- [Resource 1](#)
- [Resource 2](#)
```

## Content Guidelines

### Markdown Best Practices

**Headers:**
- Use emojis sparingly for visual interest
- Create clear hierarchy (# → ## → ###)
- Make headers descriptive and scannable

**Lists:**
- Use for enumeration and key points
- Keep items parallel in structure
- Bullet lists for unordered, numbered for steps

**Tables:**
- Great for comparisons and references
- Use for quick reference guides
- Keep columns narrow and scannable

**Code Blocks:**
```markdown
Use triple backticks for syntax examples:
```javascript
const example = 'This is a syntax example, not executable';
```
```

**Links:**
- Internal navigation: `[Part 2](#part-2-title)` - Use for TOC and cross-references
- External resources: `[Documentation](https://example.com)`
- Call-to-action links at the end

**Table of Contents Navigation:**
Hash links in TOC work in paged overlay mode:
```markdown
## 📋 Table of Contents

- [Part 1: The Big Picture](#part-1-the-big-picture)
- [Part 2: Core Concepts](#part-2-core-concepts)
- [Part 3: Advanced Topics](#part-3-advanced-topics)
```

**ID Generation Rules:**
1. Convert h2 text to lowercase
2. Remove special characters (emojis, punctuation)
3. Replace spaces with hyphens
4. Remove leading/trailing hyphens
5. Examples:
   - `## 🚀 Getting Started` → `#getting-started`
   - `## Part 1: Introduction` → `#part-1-introduction`
   - `## What's New?` → `#whats-new`
   - `## Resources & Next Steps` → `#resources-next-steps`

**Emphasis:**
- **Bold** for key terms and important points
- *Italic* for emphasis and definitions
- Use sparingly for maximum impact

### Code Cell Best Practices

**Visual Block Demonstrations (RECOMMENDED):**
```javascript
// Use showPreview() to display beautiful block overlays
const { showPreview } = await import('/scripts/ipynb-helpers.js');

// Create content for the block
const content = '<div><div>Tab 1</div><div>Content 1</div><div>Tab 2</div><div>Content 2</div></div>';

console.log('✨ Displaying interactive tabs...');
await showPreview('tabs', content);

return '✓ Beautiful visual demonstration';
```

**Available blocks for demonstrations:**
- **accordion** - Collapsible Q&A, comparisons
- **cards** - Feature showcases, categories
- **tabs** - Multiple options, variations
- **grid** - Organized layouts, galleries
- **table** - Data comparisons, references
- **hero** - Important messages, highlights
- **quote** - Inspirational text, key insights
- **code-expander** - Expandable code examples

**Pure JavaScript Examples:**
```javascript
// Use for general programming concepts (no visual needed)
const data = [1, 2, 3, 4, 5];
const doubled = data.map(x => x * 2);

console.log('Original:', data);
console.log('Doubled:', doubled);

return { original: data, doubled };
```

**Interactive Exploration:**
```javascript
// Combine interactivity with visual display
const { showPreview } = await import('/scripts/ipynb-helpers.js');

// Try changing these values!
const yourName = 'World';
const emoji = '👋';

const greeting = emoji + ' Hello, ' + yourName + '!';
console.log(greeting);

const content = '<div><div>' + greeting + '</div><div>Change the variables above and run again!</div></div>';
await showPreview('hero', content);

return greeting;
```

## Choosing the Right Block for Demonstrations

**Match blocks to your content type:**

| Content Type | Best Block | Why |
|--------------|-----------|-----|
| Comparisons, Q&A | `accordion` | Collapsible sections show alternatives |
| Features, categories | `cards` | Visual grid showcases multiple items |
| Options, variations | `tabs` | Switch between different views |
| Organized data | `grid` | Clean layout for multiple elements |
| Data comparisons | `table` | Structured information display |
| Key messages | `hero` | Bold, attention-grabbing |
| Inspirational quotes | `quote` | Emphasizes important text |
| Code examples | `code-expander` | Expandable for long snippets |

**Example use cases:**
- **Tutorial steps** → tabs (Step 1, Step 2, Step 3)
- **Before/After** → accordion (expand to see transformation)
- **Pro tips** → cards (each tip as a card)
- **Statistics** → table (organized data)
- **Final message** → hero or quote (inspiration)

## Progressive Disclosure Pattern

Build complexity gradually:

### Part 1: Simple Introduction
- Basic concept with minimal code
- Clear, concrete example
- Single idea or principle
- Use **hero** or **cards** for visual impact

### Part 2: Core Concepts
- Expand on the foundation
- Introduce 2-3 related ideas
- Show practical applications
- Use **tabs** or **accordion** for options

### Part 3: Advanced Topics
- Complex scenarios
- Edge cases and gotchas
- Performance considerations
- Use **grid** or **table** for organization

### Part 4: Best Practices
- Do's and don'ts
- Common mistakes to avoid
- Pro tips and optimizations
- Use **cards** for tips, **table** for comparisons

### Part 5: Summary & Resources
- Recap what was learned
- Next steps and further reading
- Contact or support information
- Use **quote** or **hero** for final inspiration

## Content Ratio Guidelines

Aim for **60% markdown, 40% code** in educational notebooks.

**Example structure for 20 cells:**
- 12 markdown cells (explanations, headers, TOC)
- 8 code cells (demonstrations, examples)

**Balance techniques:**
- Pair explanation with demonstration
- Follow code with commentary
- Use markdown to provide context before code
- Use code output to reinforce learning

## Engagement Techniques

### Use Emojis Strategically
```markdown
## 🚀 Getting Started
## 💡 Key Insight
## ⚠️ Common Pitfall
## ✅ Best Practice
## 📚 Resources
```

Don't overuse—one per major section header is plenty.

### Create Visual Interest
- Use tables for comparisons
- Use code blocks in markdown for examples
- Use horizontal rules (`---`) to separate major sections
- Use blockquotes (`>`) for important notes

### Tell a Story
```markdown
## The Problem

Traditional approaches to X suffer from Y...

## The Solution

What if we could Z instead?

## How It Works

Let's break this down step by step...
```

### Ask Rhetorical Questions
```markdown
## Why Does This Matter?

Imagine you're building a dashboard...

## What Could Go Wrong?

Without proper validation, three things can happen...
```

## No Initialization Required

Unlike older patterns, **no Cell 1 initialization** is needed:

**✅ Modern pattern (current):**
```javascript
// Import only what you need, when you need it
const { testBlock } = await import('/scripts/ipynb-helpers.js');
const block = await testBlock('accordion', content);
return block;
```

**❌ Old pattern (outdated):**
```javascript
// Cell 1: Initialize jsdom, setup globals... (not needed anymore)
```

**Key points:**
- Each cell can import independently
- Pure JavaScript examples need no imports
- EDS helpers imported only when using blocks
- Browser APIs available directly (console, fetch, etc.)

## Common Notebook Types

### 1. Tutorial Notebook
**Purpose:** Step-by-step learning
**Structure:**
- Introduction with learning objectives
- Progressive parts building on each other
- Exercises or "try it yourself" moments
- Summary with next steps

### 2. Blog Post Notebook
**Purpose:** Engaging content with demonstrations
**Structure:**
- Catchy title and introduction
- Table of contents for scanning
- Mix of explanation and live examples
- Call-to-action at the end
- Contact or social links

### 3. Concept Explanation Notebook
**Purpose:** Deep dive into a single idea
**Structure:**
- Problem statement
- Solution explanation
- How it works (technical details)
- Practical examples
- Best practices and gotchas

### 4. Reference Guide Notebook
**Purpose:** Quick lookup and examples
**Structure:**
- Comprehensive table of contents
- Short, focused sections
- Code examples for each feature
- Quick reference tables
- Less narrative, more reference

### 5. Interactive Demo Notebook
**Purpose:** Showcase capabilities
**Structure:**
- "What can it do?" introduction
- Live demonstrations of features
- Minimal explanation, maximum showing
- Customization examples
- Links to documentation

## Working with Source Text

When creating notebooks from existing text content:

### 1. Analyze the Content
- Identify main topics and subtopics
- Find natural breaking points for parts
- Note examples or use cases
- Extract key concepts and definitions

### 2. Extract Key Points
- What are the 3-5 main ideas?
- What examples illustrate these ideas?
- What should readers remember?
- What can be demonstrated with code?

### 3. Organize Into Parts
- Part 1: Introduction and context
- Part 2-4: Main content (one topic per part)
- Part 5: Summary and resources

### 4. Add Interactivity
- Convert examples to executable code
- Add console.log() for visibility
- Create return values for display
- Let users modify and experiment

### 5. Enhance with Markdown
- Add table of contents
- Use headers for structure
- Create tables for comparisons
- Add emojis to section headers
- Include links to resources

## Metadata Best Practices

**IMPORTANT:** Always include metadata in your notebooks for professional presentation.

**Required metadata structure:**

```json
{
  "metadata": {
    "title": "{{GENERATE A GOOD TITLE}}",
    "description": "{{GENERATE A ONE-LINE DESCRIPTION THAT AMPLIFIES THE TITLE}}",
    "author": "{{PICK AUTHOR NAME}}",
    "creation-date": "{{TODAY'S DATE IN YYYY-MM-DD FORMAT}}",
    "version": "1.0",
    "last-modified": "{{TODAY'S DATE IN YYYY-MM-DD FORMAT}}",
    "category": "{{tutorial|reference|demo|concept}}",
    "difficulty": "{{beginner|intermediate|advanced}}",
    "duration": "{{ESTIMATED READING TIME}}",
    "tags": ["tutorial", "javascript", "notebook", "interactive"],
    "license": "{{MIT|CC BY 4.0|etc}}"
  }
}
```

**Field descriptions:**

- `title` - Main notebook title (required)
- `description` - One-line summary (required)
- `author` - Author name (required)
- `creation-date` - Initial creation date in YYYY-MM-DD format (required, never change after creation)
- `version` - Version tracking (required, increment on every edit)
- `last-modified` - Last modification date in YYYY-MM-DD format (required, update on every edit)
- `category` - Content type: tutorial, reference, demo, concept (optional, displayed as blue badge)
- `difficulty` - Skill level: beginner, intermediate, advanced (optional, displayed as orange badge)
- `duration` - Reading time estimate: "15 minutes", "1 hour" (optional, displayed as purple badge)
- `tags` - Keywords for searchability (optional, displayed as gray tags)
- `license` - Content license: MIT, CC BY 4.0, etc (optional)

**⚠️ CRITICAL - Version and Date Management:**
- **ALWAYS update both `version` AND `last-modified` whenever you make ANY change to an .ipynb file**
- **Version increments:**
  - Major changes (restructuring, new parts): 1.0 → 2.0
  - Minor changes (new cells, significant edits): 1.0 → 1.1
  - Patch changes (typo fixes, small tweaks): 1.0 → 1.0.1
- **Last-modified**: Update to current date (YYYY-MM-DD) on every edit
- **Creation-date**: Never change after initial creation

**Example:**

```json
{
  "metadata": {
    "title": "Interactive JavaScript Tutorial",
    "description": "Learn JavaScript fundamentals through hands-on examples and exercises",
    "author": "Tom Cranstoun",
    "creation-date": "2025-01-17",
    "version": "1.4",
    "last-modified": "2025-11-23",
    "category": "tutorial",
    "difficulty": "beginner",
    "duration": "25 minutes",
    "tags": ["tutorial", "javascript", "notebook", "interactive", "educational"],
    "license": "MIT"
  }
}
```

The ipynb-viewer block displays this metadata professionally in the header with:
- Large title and description
- Author and creation date information
- Version number
- Last modified date
- Color-coded badges for category (blue), difficulty (orange), duration (purple)
- Gray tag pills for keywords
- License information

## Display Modes

Notebooks can be displayed in multiple modes via ipynb-viewer:

### 1. Basic Mode (Default)
```
| IPynb Viewer |
|--------------|
| /notebook.ipynb |
```
- All cells visible
- Scroll through content
- Manual Run buttons on code cells
- Good for: Quick reference, scanning content

### 2. Paged Mode
```
| IPynb Viewer (paged) |
|----------------------|
| /notebook.ipynb |
```
- Full-screen overlay with Start Reading button
- Previous/Next navigation
- Smart cell grouping (markdown + code)
- Keyboard shortcuts (arrows, escape)
- Good for: Tutorials, courses, presentations

### 3. Autorun Mode (NEW)
```
| IPynb Viewer (autorun) |
|------------------------|
| /notebook.ipynb |
```
- Code cells execute automatically
- No Run buttons (cleaner interface)
- Output visible by default
- Good for: Live demonstrations, presentations with pre-validated output

### 4. Notebook Mode (NEW)
```
| IPynb Viewer (notebook) |
|--------------------------|
| /notebook.ipynb |
```
- Combines paged + autorun + manual documentation
- Start Reading button opens paged overlay with autorun
- Read the Manual button for reference docs
- Complete educational experience
- Good for: Complete tutorials, courses with reference material

### 5. Paged + Manual Mode
```
| IPynb Viewer (paged, manual) |
|-------------------------------|
| /notebook.ipynb |
```
- Paged mode + "Read the Manual" button
- Links to README.mdc documentation
- Good for: Complex topics with extensive reference docs

### Link Navigation (NEW)

All paged modes now support **hash link navigation** between pages:

```markdown
## Table of Contents

- [Part 1: Introduction](#part-1)
- [Part 2: Core Concepts](#part-2)
- [Part 3: Advanced](#part-3)

Jump to [error handling section](#error-handling) or [best practices](#best-practices).
```

**Features:**
- Click links to navigate between pages
- Searches all pages for target ID
- Supports `part-X` pattern for direct page access
- No page reload, smooth transitions
- Perfect for non-linear learning paths

**Configure display mode** in the block markup on your EDS page.

## Best Practices Summary

✅ **Structure:**
- Start with clear introduction
- Include table of contents
- Organize into logical parts
- End with summary and resources
- **NEW:** Use pure markdown with auto-wrapping in notebook mode (90% less code!)

✅ **Content:**
- 60% markdown, 40% code
- Progressive complexity
- Engaging, accessible language
- Clear explanations before code

✅ **Code:**
- Illustrative, not just functional
- Clear comments explaining "why"
- Console output for visibility
- Return values for display

✅ **Markdown:**
- Headers with optional emojis
- Tables for comparisons
- Lists for key points
- Links for navigation and resources

✅ **Engagement:**
- Tell a story
- Ask rhetorical questions
- Show, don't just tell
- Make it interactive

❌ **Avoid:**
- Technical jargon without explanation
- Long code blocks without context
- Too much code, not enough explanation
- Jumping complexity levels abruptly

## Related Resources

For more detailed information, see:

- **[EXAMPLES.md](EXAMPLES.md)** - Complete notebook patterns and examples
- **[TEMPLATES.md](TEMPLATES.md)** - Copy-paste templates for different notebook types
- **[CONTENT_PATTERNS.md](CONTENT_PATTERNS.md)** - Detailed content organization strategies

For technical implementation details:
- **ipynb-viewer block**: `blocks/ipynb-viewer/README.md`
- **Jupyter testing documentation**: `docs/for-ai/explaining-jupyter.md`
- **Testing skill** (different purpose): `.claude/skills/jupyter-notebook-testing/`

## Quick Start

1. **Use the slash command**: `/create-notebook` for guided creation
2. **Or start manually**: Create `.ipynb` file with proper structure
3. **Add content**: Use templates from TEMPLATES.md as starting point
4. **Test display**: View via ipynb-viewer block on EDS page
5. **Refine**: Adjust based on user feedback and flow

---

**Remember:** Educational notebooks are about teaching, engaging, and demonstrating—not testing or debugging. Focus on your audience and what they need to learn.
