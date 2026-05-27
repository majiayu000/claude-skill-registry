---
document_name: "design-tokens.skill.md"
location: ".claude/skills/design-tokens.skill.md"
codebook_id: "CB-SKILL-TOKENS-001"
version: "1.0.0"
date_created: "2026-01-04"
date_last_edited: "2026-01-04"
document_type: "skill"
purpose: "Procedures for design token management"
skill_metadata:
  category: "design"
  complexity: "intermediate"
  estimated_time: "varies"
  prerequisites:
    - "CSS/styling knowledge"
    - "Design system understanding"
category: "skills"
status: "active"
tags:
  - "skill"
  - "design"
  - "tokens"
  - "css"
ai_parser_instructions: |
  This skill defines procedures for design tokens.
  Used by UI Designer agent.
---

# Design Tokens Skill

=== PURPOSE ===

Procedures for creating and managing design tokens.

=== USED BY ===

| Agent | Purpose |
|-------|---------|
| @agent(ui-designer) @ref(CB-AGENT-UIDESIGN-001) | Primary skill for tokens |

=== PROCEDURE: Token Structure ===

**Token Hierarchy:**
```
Global Tokens (Primitives)
    └── Semantic Tokens (Decisions)
        └── Component Tokens (Specifics)
```

**Example:**
```
Global:     color-blue-500: #3B82F6
Semantic:   color-primary: {color-blue-500}
Component:  button-primary-bg: {color-primary}
```

=== PROCEDURE: Token Naming ===

**Format:**
```
{category}-{property}-{variant}-{state}

Examples:
color-text-primary
color-bg-surface
space-padding-md
font-size-lg
shadow-elevation-md
```

**Categories:**
| Category | Properties |
|----------|------------|
| color | text, bg, border, icon |
| space | padding, margin, gap |
| font | size, weight, family, line-height |
| shadow | elevation levels |
| border | width, radius |
| motion | duration, easing |
| z-index | layer levels |

=== PROCEDURE: Token Formats ===

**JSON (Source of Truth):**
```json
{
  "color": {
    "primary": {
      "50": { "value": "#EEF2FF" },
      "500": { "value": "#6366F1" },
      "600": { "value": "#4F46E5" }
    },
    "text": {
      "primary": { "value": "{color.gray.900}" },
      "secondary": { "value": "{color.gray.600}" }
    }
  },
  "space": {
    "1": { "value": "4px" },
    "2": { "value": "8px" },
    "4": { "value": "16px" }
  }
}
```

**CSS Variables:**
```css
:root {
  /* Colors */
  --color-primary-50: #EEF2FF;
  --color-primary-500: #6366F1;
  --color-primary-600: #4F46E5;

  --color-text-primary: var(--color-gray-900);
  --color-text-secondary: var(--color-gray-600);

  /* Spacing */
  --space-1: 4px;
  --space-2: 8px;
  --space-4: 16px;

  /* Typography */
  --font-size-sm: 14px;
  --font-size-base: 16px;
  --font-size-lg: 18px;
}
```

**JavaScript/TypeScript:**
```typescript
export const tokens = {
  color: {
    primary: {
      50: '#EEF2FF',
      500: '#6366F1',
      600: '#4F46E5',
    },
    text: {
      primary: '#111827',
      secondary: '#4B5563',
    },
  },
  space: {
    1: '4px',
    2: '8px',
    4: '16px',
  },
} as const;
```

=== PROCEDURE: Color Tokens ===

**Complete Color Token Set:**
```json
{
  "color": {
    "brand": {
      "primary": { "value": "#6366F1" },
      "secondary": { "value": "#EC4899" }
    },
    "text": {
      "primary": { "value": "#111827" },
      "secondary": { "value": "#6B7280" },
      "disabled": { "value": "#9CA3AF" },
      "inverse": { "value": "#FFFFFF" },
      "link": { "value": "#3B82F6" }
    },
    "bg": {
      "primary": { "value": "#FFFFFF" },
      "secondary": { "value": "#F9FAFB" },
      "tertiary": { "value": "#F3F4F6" },
      "inverse": { "value": "#111827" }
    },
    "border": {
      "default": { "value": "#E5E7EB" },
      "focus": { "value": "#6366F1" },
      "error": { "value": "#EF4444" }
    },
    "status": {
      "success": { "value": "#10B981" },
      "warning": { "value": "#F59E0B" },
      "error": { "value": "#EF4444" },
      "info": { "value": "#3B82F6" }
    }
  }
}
```

=== PROCEDURE: Typography Tokens ===

```json
{
  "font": {
    "family": {
      "sans": { "value": "Inter, system-ui, sans-serif" },
      "mono": { "value": "JetBrains Mono, monospace" }
    },
    "size": {
      "xs": { "value": "12px" },
      "sm": { "value": "14px" },
      "base": { "value": "16px" },
      "lg": { "value": "18px" },
      "xl": { "value": "20px" },
      "2xl": { "value": "24px" },
      "3xl": { "value": "30px" },
      "4xl": { "value": "36px" }
    },
    "weight": {
      "regular": { "value": "400" },
      "medium": { "value": "500" },
      "semibold": { "value": "600" },
      "bold": { "value": "700" }
    },
    "lineHeight": {
      "tight": { "value": "1.25" },
      "normal": { "value": "1.5" },
      "relaxed": { "value": "1.75" }
    }
  }
}
```

=== PROCEDURE: Spacing Tokens ===

```json
{
  "space": {
    "0": { "value": "0" },
    "px": { "value": "1px" },
    "0.5": { "value": "2px" },
    "1": { "value": "4px" },
    "2": { "value": "8px" },
    "3": { "value": "12px" },
    "4": { "value": "16px" },
    "5": { "value": "20px" },
    "6": { "value": "24px" },
    "8": { "value": "32px" },
    "10": { "value": "40px" },
    "12": { "value": "48px" },
    "16": { "value": "64px" },
    "20": { "value": "80px" }
  }
}
```

=== PROCEDURE: Shadow Tokens ===

```json
{
  "shadow": {
    "sm": { "value": "0 1px 2px 0 rgba(0, 0, 0, 0.05)" },
    "base": { "value": "0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)" },
    "md": { "value": "0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)" },
    "lg": { "value": "0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)" },
    "xl": { "value": "0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)" }
  }
}
```

=== PROCEDURE: Token Documentation ===

**Document Location:** `devdocs/ui/tokens.md`

**Format:**
```markdown
# Design Tokens

## Color Tokens

### Text Colors
| Token | Value | Usage |
|-------|-------|-------|
| color-text-primary | #111827 | Main body text |
| color-text-secondary | #6B7280 | Supporting text |

## Usage in Code

### CSS
```css
.element {
  color: var(--color-text-primary);
  padding: var(--space-4);
}
```

### Tailwind (if configured)
```html
<div class="text-text-primary p-4">
```
```

=== RELATED SKILLS ===

| Skill | Relationship |
|-------|--------------|
| @skill(design-system) | System context |
| @skill(visual-design) | Visual application |
