---
name: dev-slides
description: >-
  Create developer-friendly presentations using Slidev. Build Vue-powered
  slides with live code execution, syntax highlighting, and diagrams.
  Use when a user asks to create a presentation, build slides, make a
  tech talk, create a slide deck, or prepare a developer presentation.
license: Apache-2.0
compatibility: "Requires Node.js 18+ and npm"
metadata:
  author: terminal-skills
  version: "1.0.0"
  category: development
  tags: ["slides", "presentations", "slidev", "vue", "developer-tools"]
  use-cases:
    - "Create a technical presentation with live code examples"
    - "Build a slide deck for a conference talk or team demo"
    - "Generate slides from a topic outline with code samples and diagrams"
  agents: [claude-code, openai-codex, gemini-cli, cursor]
---

# Dev Slides

## Overview

Create developer-friendly presentations using Slidev, a markdown-based slide framework powered by Vue. Supports live code execution, syntax highlighting, Mermaid diagrams, LaTeX math, and speaker notes. Ideal for tech talks, team demos, and conference presentations.

## Instructions

When a user asks you to create a presentation or slide deck, follow this process:

### Step 1: Set up the Slidev project

Check if Slidev is available, and scaffold a project if needed:

```bash
# Check if slidev is installed
npx slidev --version 2>/dev/null || echo "Will use npx to run slidev"

# Create a new slidev project directory
mkdir -p slides-project && cd slides-project

# Initialize with a slides.md file
touch slides.md
```

### Step 2: Gather the presentation requirements

Before writing slides, determine:
- **Topic:** What is the presentation about?
- **Audience:** Developers, managers, mixed?
- **Length:** How many slides? (Typical: 10-20 for a talk)
- **Style:** Technical deep-dive, overview, tutorial, demo?
- **Code focus:** Which languages and frameworks?

### Step 3: Write the slides in Markdown

Slidev uses Markdown with YAML frontmatter and `---` separators between slides.

**Basic structure:**

```markdown
---
theme: default
title: "Your Presentation Title"
info: |
  Presentation description
class: text-center
drawings:
  persist: false
transition: slide-left
---

# Your Presentation Title

Subtitle or tagline

---

## Slide Title

- Bullet point one
- Bullet point two
- Bullet point three

---
```

**Code blocks with syntax highlighting:**

```markdown
---

## API Example

\`\`\`typescript {2-4|6-8} {lines:true}
async function fetchUsers() {
  const response = await fetch('/api/users');
  const data = await response.json();
  return data;

  // With error handling
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`);
  }
}
\`\`\`

---
```

The `{2-4|6-8}` syntax enables click-through line highlighting.

**Mermaid diagrams:**

```markdown
---

## Architecture

\`\`\`mermaid
graph LR
  A[Client] --> B[API Gateway]
  B --> C[Auth Service]
  B --> D[Data Service]
  D --> E[(Database)]
\`\`\`

---
```

**Two-column layouts:**

```markdown
---

## Comparison

::left::

### Before
- Manual deploys
- No tests
- 2-hour releases

::right::

### After
- CI/CD pipeline
- 95% coverage
- 5-minute releases

---
```

**Speaker notes:**

```markdown
---

## Key Metrics

- 99.9% uptime
- 50ms p99 latency

<!--
Speaker notes go here.
Mention that we achieved this after the migration in Q3.
-->

---
```

### Step 4: Add theme and configuration

Configure the frontmatter for styling:

```yaml
---
theme: seriph          # or: default, apple-basic, dracula, etc.
background: /cover.jpg # optional cover image
class: text-center
highlighter: shiki
lineNumbers: true
drawings:
  persist: false
transition: slide-left
css: unocss
---
```

### Step 5: Preview and export

```bash
# Start the dev server with live preview
npx slidev slides.md --open

# Export to PDF
npx slidev export slides.md --output presentation.pdf

# Export to PNG images
npx slidev export slides.md --format png --output slides-images/

# Build as static SPA
npx slidev build slides.md
```

## Examples

### Example 1: Create a tech talk on API design

**User request:** "Create slides for a talk on REST API best practices"

**Output:** Write `slides.md` with approximately 12-15 slides covering:
1. Title slide with talk info
2. Agenda / outline
3. What makes a good API (principles)
4. Resource naming conventions with examples
5. HTTP methods and status codes (code table)
6. Request/response design with code blocks
7. Pagination patterns with code
8. Error handling with JSON examples
9. Versioning strategies
10. Authentication overview (diagram)
11. Rate limiting
12. Documentation tools
13. Summary and key takeaways

Each slide uses appropriate Slidev features: code blocks for examples, Mermaid for architecture diagrams, two-column layouts for comparisons.

### Example 2: Create an internal team demo

**User request:** "Make slides for demoing our new auth system to the team"

**Output:** Write `slides.md` with 8-10 slides:
1. Title: "New Auth System Demo"
2. Problem statement (what was wrong with the old system)
3. Architecture diagram (Mermaid flowchart)
4. Code walkthrough: login flow with highlighted steps
5. Code walkthrough: token refresh mechanism
6. Before/after metrics comparison (two-column layout)
7. Migration plan timeline
8. Q&A slide

### Example 3: Generate slides from an outline

**User request:** "Turn this outline into slides: Intro to Docker - what it is, images vs containers, Dockerfile basics, docker-compose, best practices"

**Output:** Convert each outline item into 2-3 slides with:
- Explanatory text and bullet points
- Relevant code blocks (Dockerfile syntax, docker-compose.yml)
- A Mermaid diagram showing the image-to-container lifecycle
- A best practices checklist slide

## Guidelines

- Keep each slide focused on one idea. If a slide has more than 5 bullet points, split it.
- Use code blocks liberally for developer audiences. Highlight key lines with the `{lines}` syntax.
- Add Mermaid diagrams for architecture, flows, and relationships instead of describing them in text.
- Use speaker notes for context you want to say but not display.
- Prefer the `seriph` or `default` theme for professional presentations.
- For live demos, use Slidev's Monaco editor integration for editable code blocks.
- Always structure slides with a clear narrative: problem, solution, details, summary.
- Export to PDF before sharing to ensure consistent rendering.
- Keep total slide count reasonable: 1-2 minutes per slide is typical pacing.
