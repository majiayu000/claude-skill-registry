---
name: create-slidev-presentation
description: This skill should be used when asked to create or edit Slidev (sli.dev) presentation slide decks.
---

# Slidev

## Overview

Enable creation and editing of high-quality Slidev presentations. Slidev is a web-based presentation framework that uses Markdown with Vue 3 components, providing features like live code editing, syntax highlighting, animations, and export to multiple formats.

**Key capabilities**:
- Create presentations from markdown with YAML configuration
- Use 17 built-in layouts plus custom layouts
- Add click animations, transitions, and motion effects
- Embed live code editors (Monaco) with TypeScript support
- Include diagrams (Mermaid, PlantUML), LaTeX math, and media
- Export to PDF, PPTX, PNG, or static web application

**Requirements**: Node.js >= 24.0.0

## Quick Start

### Creating a New Presentation

```bash
# Initialize project
pnpm create slidev

# Or with specific entry file
pnpm create slidev my-slides

# Start development server
cd my-slides
pnpm run dev
```

### Minimal Presentation Structure

```markdown
---
theme: default
title: My Presentation
---

# Welcome

Introduction slide

---

# Second Slide

Content here

---
layout: end
---

# Thank You
```

**Slide separator**: Three dashes (`---`) padded with new lines

## Creating Presentations

### Structure Decision Tree

**Is this a new presentation?**
- Yes → Use template from `assets/slide-templates.md` or `assets/example-configurations.md`
- No → See "Editing Presentations" section

**What type of presentation?**
- **Business/Professional** → Use `seriph` theme, simple transitions
- **Technical/Code-heavy** → Enable `monaco`, `lineNumbers`, use code templates
- **Conference/Workshop** → Enable `drawings`, `record`, `presenter` mode
- **Educational** → Use clear layouts, diagrams, progressive disclosure
- **Design-focused** → Minimalist theme, `fade` transitions, large typography

### Configuration Approach

Start with minimal headmatter, add features as needed:

**Step 1 - Minimal** (always include):
```yaml
---
theme: default
title: Presentation Title
---
```

**Step 2 - Add features** (based on content):
```yaml
---
theme: seriph
title: Presentation Title
author: Your Name
mdc: true
lineNumbers: true  # For code
monaco: dev        # For live code
transition: slide-left
---
```

**Step 3 - Optimize** (for specific use case):
- Code presentations: Add `twoslash`, higher `canvasWidth` (1200)
- Media-heavy: Set `aspectRatio: 16/9`, optimize fonts
- Export-focused: Configure `export` options, set `exportFilename`

### Layout Selection

Use appropriate layout for each slide's purpose:

| Slide Purpose    | Layout             | Example                   |
|------------------|--------------------|---------------------------|
| Title slide      | `cover`            | Opening slide             |
| Section divider  | `section`          | New topic                 |
| Standard content | `default`          | Bullet points, text       |
| Centred content  | `center`           | Short quotes              |
| Two columns      | `two-cols`         | Comparisons               |
| Image + text     | `image-left/right` | Diagrams with explanation |
| Big number/stat  | `fact`             | Key metrics               |
| Quote            | `quote`            | Testimonials              |
| Final slide      | `end`              | Thank you, Q&A            |

Specify layout in per-slide frontmatter:
```yaml
---
layout: two-cols
---
```

**Reference**: `references/layouts-reference.md` for all 17 layouts with examples

### Component Usage

Built-in components for common needs:

**Click animations**:
```markdown
<v-clicks>

- Item 1
- Item 2
- Item 3

</v-clicks>
```

**Media embedding**:
```markdown
<Youtube id="dQw4w9WgXcQ" />
<Tweet id="1234567890" />
```

**Navigation**:
```markdown
<Link to="42">Go to slide 42</Link>
<Toc minDepth="1" maxDepth="2" />
```

**Reference**: `references/components-reference.md` for complete component library

### Code Presentation

**Basic code block**:
````markdown
```typescript
const greeting: string = 'Hello, Slidev!'
console.log(greeting)
```
````

**With line highlighting** (incremental):
````markdown
```ts {1|3-4|all}
const step1 = 'First'
// Highlight line 1
const step2 = 'Second'
const step3 = 'Third'
// Then highlight lines 3-4
// Finally highlight all
```
````

**Interactive editor**:
````markdown
```ts {monaco-run}
console.log('Runs in browser!')
```
````

**Best practices**:
1. Always specify language for syntax highlighting
2. Use incremental highlighting to guide attention
3. Keep code blocks under 20 lines (use `{maxHeight:'200px'}` if longer)
4. Enable `lineNumbers: true` for code-heavy presentations

### Animations

**Progressive disclosure** (most common):
```markdown
<v-clicks>

- Point 1
- Point 2
- Point 3

</v-clicks>
```

**Element-level control**:
```markdown
<div v-click>Appears on click 1</div>
<div v-click>Appears on click 2</div>
<div v-click="3">Appears on click 3</div>
```

**Motion animations**:
```markdown
<div
  v-motion
  :initial="{ x: -80, opacity: 0 }"
  :enter="{ x: 0, opacity: 1 }"
>
  Animated entrance
</div>
```

**Slide transitions**:
```yaml
---
transition: slide-left
---
```

Options: `fade`, `slide-left`, `slide-right`, `slide-up`, `slide-down`, `view-transition`

## Editing Presentations

### Modification Strategy

**Step 1 - Read and understand**:
1. Read `slides.md` to understand structure
2. Identify headmatter (first frontmatter block)
3. Note layouts and components used

**Step 2 - Make targeted changes**:
- **Add slides**: Insert `---` separator and new content
- **Modify content**: Edit markdown between separators
- **Change layouts**: Update per-slide frontmatter
- **Adjust config**: Modify headmatter or create `slidev.config.ts`

**Step 3 - Test changes**:
```bash
slidev  # Verify in dev server
```

### Common Editing Tasks

**Add slide after specific slide**:
1. Find target slide content
2. Add separator (`---`) after it
3. Add new slide content

**Change slide layout**:
```markdown
---
layout: two-cols  # Change this
---
```

**Add click animations to list**:
```markdown
<v-clicks>

- Existing item 1
- Existing item 2

</v-clicks>
```

**Enable feature globally**:
Update headmatter:
```yaml
---
# Add/update these
monaco: dev
lineNumbers: true
---
```

**Split long presentation**:
Create `pages/section1.md`, then in main `slides.md`:
```markdown
---
src: ./pages/section1.md
---
```

## Common Patterns

Use pre-built templates from `assets/slide-templates.md`:

**Title slide pattern**:
```markdown
---
layout: cover
background: /cover.jpg
class: text-center
---

# Title

## Subtitle

Author · Date
```

**Code demo pattern**:
````markdown
---
layout: two-cols
---

```ts {monaco-run}
// Interactive code
```

::right::

# Explanation

- Point 1
- Point 2
````

**Comparison pattern**:
```markdown
---
layout: two-cols
---

# Before

Old approach

::right::

# After

New approach
```

**Section divider pattern**:
```markdown
---
layout: section
background: linear-gradient(to right, #667eea, #764ba2)
class: text-white
---

# Part 2: Implementation
```

**Complete examples**: See `assets/example-configurations.md` for full presentation templates

## Export & Build

### Export to PDF

```bash
# Basic export
slidev export

# With options
slidev export --output presentation.pdf
slidev export --with-clicks  # Include animations
slidev export --dark         # Dark mode
slidev export --range 1,4-8  # Specific slides
```

**Prerequisites**: Install playwright-chromium
```bash
pnpm add -D playwright-chromium
```

### Export to Other Formats

```bash
slidev export --format pptx   # PowerPoint
slidev export --format png    # PNG images
slidev export --format md     # Markdown with PNGs
```

### Build Static Site

```bash
slidev build
slidev build --base /slides/  # For subdirectory hosting
```

Deploy `dist/` directory to static hosting (Netlify, Vercel, GitHub Pages).

## Configuration Reference

### Essential Headmatter Options

```yaml
---
# Theme
theme: seriph  # or: default, apple-basic, carbon, dracula, nord, etc.

# Metadata
title: Presentation Title
author: Your Name
info: |
  ## Description
  Multi-line supported

# Features
mdc: true              # Enable MDC syntax
monaco: dev            # Enable Monaco editor
lineNumbers: true      # Line numbers in code
twoslash: true         # TypeScript type info
download: true         # PDF download button

# Appearance
colorSchema: auto      # auto, light, or dark
transition: slide-left # Global transition

# Layout
aspectRatio: 16/9
canvasWidth: 980

# Fonts
fonts:
  sans: Inter
  mono: JetBrains Mono
  weights: '300,400,600,700'
  provider: google

# Export
exportFilename: my-presentation
export:
  format: pdf
  withClicks: false
  dark: false
---
```

**Complete reference**: See `references/configuration-reference.md`

### Per-Slide Frontmatter

```yaml
---
layout: center           # Slide layout
background: /image.jpg   # Background image
class: text-white        # CSS classes
transition: fade         # Override global
clicks: 5                # Number of clicks
hideInToc: true         # Hide from TOC
zoom: 0.8               # Scale content
routeAlias: solutions   # Navigation alias
---
```

## Troubleshooting

### Common Issues

**Slides not updating**:
```bash
slidev --force  # Clear cache
```

**Layout not found**:
- Check layout name spelling (case-sensitive)
- Verify theme includes layout
- Create custom layout in `./layouts/`

**Code not highlighting**:
- Specify language: ` ```typescript ` not ` ``` `
- Check for syntax errors
- Clear cache: `slidev --force`

**Export fails or hangs**:
```bash
pnpm add -D playwright-chromium  # Install first
slidev export --timeout 60000    # Increase timeout
slidev export --wait 2000         # Add wait time
```

**Monaco not working**:
- Set `monaco: 'dev'` or `monaco: true` in headmatter
- Clear cache
- Check browser console for errors

**Images not loading**:
- Path must start with `/` for public folder
- Verify file in `public/` directory
- Check browser console for 404s

**Complete guide**: See `references/troubleshooting.md`

## Best Practices

### Content Organisation
1. **One idea per slide** - Don't overcrowd
2. **6x6 rule** - Max 6 lines, 6 words per line
3. **Visual hierarchy** - Use heading levels consistently
4. **Progressive disclosure** - Use `<v-clicks>` for lists
5. **Consistent styling** - Stick to theme

### Code Presentation
1. **Specify language** - Always enable syntax highlighting
2. **Line highlighting** - Guide attention: `{1|3-5|all}`
3. **Keep it short** - Under 20 lines per block
4. **Use Monaco** - For interactive demos
5. **Font size** - Ensure readability (use `zoom` if needed)

### Performance
1. **Optimise images** - Compress, use WebP
2. **Lazy load** - `preload: false` on heavy slides
3. **Limit animations** - Balance engagement vs. performance
4. **Local assets** - Use `/public` folder
5. **Disable unused features** - `monaco: false` if not needed

### Accessibility
1. **Colour contrast** - Minimum 4.5:1 ratio
2. **Alt text** - Describe images
3. **Font size** - Minimum 24pt body text
4. **Test keyboard navigation** - Arrow keys should work
5. **Avoid flashing** - No rapid animations (<3/second)

## Resources

This skill includes comprehensive documentation:

### `references/`
- **layouts-reference.md** - All 17 built-in layouts with examples
- **components-reference.md** - Complete component library and custom patterns
- **configuration-reference.md** - All configuration options and setup files
- **troubleshooting.md** - Common issues and solutions

### `assets/`
- **slide-templates.md** - Ready-to-use templates for common slide types
- **example-configurations.md** - Complete example configurations for different use cases

### Official Documentation
- Website: https://sli.dev
- Docs: https://sli.dev/guide/
- GitHub: https://github.com/slidevjs/slidev
- Themes: https://sli.dev/resources/theme-gallery

## Workflow Example

**User request**: "Create a technical presentation about TypeScript best practices"

**Step 1**: Choose template from `assets/example-configurations.md` → "Technical/Code-Heavy Presentation"

**Step 2**: Create `slides.md` with appropriate headmatter:
```yaml
---
theme: default
title: TypeScript Best Practices
author: Developer Name
monaco: dev
lineNumbers: true
twoslash: true
---
```

**Step 3**: Add slides using templates from `assets/slide-templates.md`:
- Cover slide
- Section dividers
- Code demonstration slides
- Comparison slides
- End slide

**Step 4**: Start dev server to preview:
```bash
slidev
```

**Step 5**: Export when ready:
```bash
slidev export --format pdf
```
