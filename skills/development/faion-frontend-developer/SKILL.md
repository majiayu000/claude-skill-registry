---
name: faion-frontend-developer
description: "Frontend: Tailwind, CSS-in-JS, design tokens, UI libraries, PWA, accessibility."
user-invocable: false
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task, AskUserQuestion, TodoWrite, Skill
---
> **Entry point:** `/faion-net` — invoke this skill for automatic routing to the appropriate domain.

# Frontend Developer Skill

Frontend development specializing in styling, UI libraries, design systems, and modern frontend patterns.

## Purpose

Handles frontend styling, design systems, UI component libraries, accessibility, PWA, and responsive design.

---

## Context Discovery

### Auto-Investigation

Detect frontend styling setup:

| Signal | How to Check | What It Tells Us |
|--------|--------------|------------------|
| `tailwind.config.*` | `Glob("**/tailwind.config.*")` | Tailwind CSS used |
| `styled-components` | `Grep("styled-components", "package.json")` | Styled Components |
| `emotion` | `Grep("@emotion", "package.json")` | Emotion CSS-in-JS |
| `shadcn` components | `Glob("**/components/ui/*.tsx")` | shadcn/ui used |
| `.storybook/` | `Glob("**/.storybook/*")` | Storybook setup |
| Design tokens | `Glob("**/tokens.*")` | Design system exists |
| PWA manifest | `Glob("**/manifest.json")` | PWA configured |

**Read existing patterns:**
- tailwind.config for theme/tokens
- Existing components for styling patterns
- Storybook stories for component API

### Discovery Questions

#### Q1: Styling Approach

```yaml
question: "What styling approach are you using?"
header: "Styling"
multiSelect: false
options:
  - label: "Tailwind CSS"
    description: "Utility-first CSS framework"
  - label: "CSS-in-JS (Styled Components, Emotion)"
    description: "JavaScript-based styling"
  - label: "CSS Modules"
    description: "Scoped CSS files"
  - label: "Plain CSS/SCSS"
    description: "Traditional stylesheets"
  - label: "Not decided / recommend"
    description: "I'll suggest based on project"
```

#### Q2: UI Component Library

```yaml
question: "Are you using a UI component library?"
header: "UI Lib"
multiSelect: false
options:
  - label: "shadcn/ui"
    description: "Copy-paste Radix-based components"
  - label: "Material UI"
    description: "Google Material Design"
  - label: "Chakra UI"
    description: "Accessible component library"
  - label: "Custom components"
    description: "Building from scratch"
  - label: "None yet"
    description: "Need recommendation"
```

#### Q3: Design System Status

```yaml
question: "Do you have a design system?"
header: "Design"
multiSelect: false
options:
  - label: "Yes, with design tokens"
    description: "Colors, spacing, typography defined"
  - label: "Figma designs exist"
    description: "Designs to implement"
  - label: "No formal system"
    description: "Ad-hoc styling"
  - label: "Need to create one"
    description: "Want to establish system"
```

#### Q4: Accessibility Requirements

```yaml
question: "What are your accessibility requirements?"
header: "A11y"
multiSelect: false
options:
  - label: "WCAG 2.1 AA compliance"
    description: "Standard accessibility"
  - label: "WCAG 2.1 AAA compliance"
    description: "Highest accessibility"
  - label: "Basic accessibility"
    description: "Semantic HTML, keyboard nav"
  - label: "Not a priority yet"
    description: "Focus on functionality first"
```

---

## When to Use

- Tailwind CSS styling and architecture
- Design tokens and design systems
- CSS-in-JS patterns
- UI component libraries (shadcn/ui, etc.)
- Progressive Web Apps (PWA)
- Responsive and mobile design
- Accessibility (a11y)
- SEO for SPAs
- Storybook component development

## Methodologies

| Category | Methodology | File |
|----------|-------------|------|
| **Tailwind CSS** |
| Tailwind basics | Setup, utilities, responsive design | tailwind.md |
| Tailwind architecture | Component organization, theme config | tailwind-architecture.md |
| Tailwind patterns | Best practices, patterns, plugins | tailwind-patterns.md |
| **CSS-in-JS** |
| CSS-in-JS basics | Styled components, emotion basics | css-in-js-basics.md |
| CSS-in-JS advanced | Theme, SSR, performance | css-in-js-advanced.md |
| **Design Systems** |
| Design tokens basics | Token structure, naming conventions | design-tokens-basics.md |
| Design tokens implementation | Token generation, tooling | design-tokens-implementation.md |
| **UI Libraries** |
| shadcn/ui | Component setup and usage | shadcn-ui.md |
| shadcn/ui architecture | Project structure, customization | shadcn-ui-architecture.md |
| UI lib basics | Component library patterns | ui-lib-basics.md |
| UI lib patterns | Advanced component patterns | ui-lib-patterns.md |
| Storybook setup | Storybook configuration, stories | storybook-setup.md |
| **Responsive & Mobile** |
| Mobile responsive | Responsive design, breakpoints | mobile-responsive.md |
| **PWA** |
| PWA core | Service workers, caching, offline | pwa-core.md |
| PWA advanced | Push notifications, sync, install | pwa-advanced.md |
| **SEO & Accessibility** |
| SEO for SPAs | SSR, meta tags, structured data | seo-for-spas.md |
| Accessibility | ARIA, keyboard nav, screen readers | accessibility.md |
| **Frontend Design** |
| Frontend design | UI/UX implementation patterns | frontend-design.md |

## Tools

- **Styling:** Tailwind CSS, CSS-in-JS (styled-components, emotion)
- **Design tokens:** Style Dictionary, Figma Tokens
- **UI libraries:** shadcn/ui, Radix UI, Headless UI
- **Storybook:** Component development and documentation
- **Accessibility:** axe-core, WAVE, Lighthouse

## Related Sub-Skills

| Sub-skill | Relationship |
|-----------|--------------|
| faion-javascript-developer | React components, Next.js |
| faion-ux-ui-designer | Design specs and mockups |
| faion-devtools-developer | Build tools, bundlers |

## Integration

Invoked by parent skill `faion-software-developer` for frontend styling and UI work.

---

*faion-frontend-developer v1.0 | 18 methodologies*
