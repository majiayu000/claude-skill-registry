---
name: slidev
description: Create and edit presentation slides using Slidev framework when user requests slides, presentations, or deck modifications
---

# Slidev Skill

This skill helps create and edit presentation slides using Slidev, a markdown-based presentation framework for developers.

## When to Use This Skill

Use this skill when the user asks to:
- Create a new presentation or slide deck
- Edit existing slides
- Add or modify slide content
- Work with Slidev-specific features
- Generate presentations from content

## Project Structure

Slides are located in `packages/slides/` directory with:
- Slide files: `*.slides.md` or `slides.md`
- Components: `components/` directory for Vue components
- Configuration: `package.json` for dependencies

## Running Slidev

Start the development server:
```bash
pnpm run slides [filename]
```


The dev server runs on `http://localhost:3030` by default.

## Slidev File Format

### Frontmatter Configuration

Every Slidev file starts with YAML frontmatter:

```yaml
---
theme: seriph  # or 'default'
title: Your Presentation Title
info: |
  ## Presentation description
  Additional info here
class: text-center
drawings:
  persist: false
transition: slide-left  # fade-out, slide-up, etc.
mdc: true
duration: 10min
---
```

### Slide Separators

Slides are separated by `---`:

```markdown
---
# Slide 1

Content here

---
# Slide 2

More content
```

### Slide Configuration

Individual slides can have frontmatter:

```markdown
---
layout: center
class: text-center
---

# Centered Slide
```

## Common Layouts

- `default` - Standard layout
- `center` - Centered content
- `two-cols` - Two column layout
- `image-right` - Image on right side
- `cover` - Cover slide

### Two Column Layout Example

```markdown
---
layout: two-cols
---

# Left Column

Content here

::right::

# Right Column

Content here
```

## Interactive Features

### Click Animations

Use `v-click` for progressive reveals:

```html
<v-click>
Content appears on click
</v-click>

<v-clicks>
- Item 1
- Item 2
- Item 3
</v-clicks>
```

### Components

Use Vue components in slides:

Custom one are stored `packages/slides/components` directory

```html
<Counter :count="10" />
```

### Code Blocks

Syntax highlighting with line highlighting:

````markdown
```ts {1|3|1-3}
const message = "Hello"
console.log(message)
```
````

### Presenter Notes

Add notes in HTML comments at the end of slides:

```markdown
---
# Slide Title

Content

<!--
These are presenter notes
Only visible in presenter mode
-->
```

## Best Practices

1. **Keep slides focused** - One concept per slide
2. **Use progressive disclosure** - Reveal information with v-click
3. **Add presenter notes** - Document your talking points
4. **Leverage layouts** - Use built-in layouts for consistency
5. **Interactive components** - Enhance with Vue components when needed

## Common Commands

```bash
# Development
pnpm run slides [filename]

# Build static version
pnpm --filter @chris-towles/slides run build

# Export to PDF
pnpm --filter @chris-towles/slides run export
```

## Resources

- Slidev Documentation: https://sli.dev/
- Themes: https://sli.dev/resources/theme-gallery
- Built-in Components: https://sli.dev/builtin/components.html