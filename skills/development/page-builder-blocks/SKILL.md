---
name: page-builder-blocks
description: |
  Page builder block patterns for this Next.js application.
  Covers block structure (5 files), baseBlockSchema, field definitions, and component patterns.
  Use this skill when creating or modifying page builder blocks.
allowed-tools: Read, Glob, Grep, Bash
version: 1.0.0
---

# Page Builder Blocks Skill

Patterns for creating and managing page builder blocks in this Next.js application.

## Architecture Overview

```
contents/themes/{THEME}/blocks/
├── hero/                     # Example block
│   ├── config.ts            # Metadata (slug, name, category, icon)
│   ├── schema.ts            # Zod validation (extends baseBlockSchema)
│   ├── fields.ts            # Field definitions for admin UI
│   ├── component.tsx        # React component
│   └── index.ts             # Re-exports
├── features-grid/
├── cta-section/
└── ...

core/types/blocks.ts          # Base schemas, types, helpers
core/lib/registries/block-registry.ts  # Auto-generated registry
```

## When to Use This Skill

- Creating new page builder blocks
- Modifying existing block schemas
- Adding fields to blocks
- Understanding block component patterns
- Working with BLOCK_SELECTORS

## Block Structure (5 Required Files)

Every block requires exactly 5 files in `contents/themes/{THEME}/blocks/{slug}/`:

### File 1: config.ts

```typescript
import type { BlockConfig, BlockCategory } from '@/core/types/blocks'

export const config: Omit<BlockConfig, 'schema' | 'fieldDefinitions' | 'Component' | 'examples'> = {
  slug: 'hero',                              // kebab-case, matches folder name
  name: 'Hero Section',                      // User-facing display name
  description: 'Full-width hero with title, subtitle, and CTA',
  category: 'hero' as BlockCategory,         // From 15 categories
  icon: 'LayoutTemplate',                    // Lucide icon name
  thumbnail: '/theme/blocks/hero/thumbnail.png',  // Optional preview
  scope: ['pages'],                          // 'pages', 'posts', or both
}
```

### File 2: schema.ts

```typescript
import { z } from 'zod'
import { baseBlockSchema } from '@/core/types/blocks'

// For array fields, define item schema first
const featureItemSchema = z.object({
  icon: z.string().optional(),
  title: z.string().min(1, 'Title is required'),
  description: z.string().optional(),
})

// ALWAYS extend baseBlockSchema with .merge()
export const schema = baseBlockSchema.merge(z.object({
  // ONLY custom fields here - base fields are inherited
  features: z.array(featureItemSchema).min(1).max(12).optional(),
  columns: z.enum(['2', '3', '4']).default('3'),
  showIcons: z.boolean().default(true),
}))

export type HeroProps = z.infer<typeof schema>
```

**baseBlockSchema provides (DO NOT recreate):**

| Tab | Field | Type | Description |
|-----|-------|------|-------------|
| Content | `title` | string? | Section heading |
| Content | `content` | string? | Rich text description |
| Content | `cta` | object? | CTA button {text, link, target} |
| Design | `backgroundColor` | enum? | 10 preset colors |
| Advanced | `className` | string? | Custom CSS classes |
| Advanced | `id` | string? | HTML ID for anchors |

### File 3: fields.ts

```typescript
import type { FieldDefinition } from '@/core/types/blocks'
import {
  baseContentFields,
  baseDesignFields,
  baseAdvancedFields,
} from '@/core/types/blocks'

// Custom content fields
const customContentFields: FieldDefinition[] = [
  {
    name: 'features',
    label: 'Features',
    type: 'array',
    tab: 'content',
    required: false,
    minItems: 1,
    maxItems: 12,
    itemFields: [
      { name: 'icon', label: 'Icon', type: 'text', tab: 'content' },
      { name: 'title', label: 'Title', type: 'text', tab: 'content', required: true },
      { name: 'description', label: 'Description', type: 'textarea', tab: 'content' },
    ],
  },
]

// Custom design fields
const customDesignFields: FieldDefinition[] = [
  {
    name: 'columns',
    label: 'Grid Columns',
    type: 'select',
    tab: 'design',
    default: '3',
    options: [
      { label: '2 Columns', value: '2' },
      { label: '3 Columns', value: '3' },
      { label: '4 Columns', value: '4' },
    ],
  },
  {
    name: 'showIcons',
    label: 'Show Icons',
    type: 'checkbox',
    tab: 'design',
    default: true,
  },
]

// CRITICAL: Export in correct order
// Content → Design → Advanced (baseAdvancedFields ALWAYS last)
export const fieldDefinitions: FieldDefinition[] = [
  ...baseContentFields,
  ...customContentFields,
  ...baseDesignFields,
  ...customDesignFields,
  ...baseAdvancedFields,  // MUST be last
]

// Compatibility alias
export const fields = fieldDefinitions
```

### File 4: component.tsx

```typescript
import { buildSectionClasses } from '@/core/types/blocks'
import { sel } from '../../lib/selectors'
import type { HeroProps } from './schema'

export function HeroBlock({
  // Base content props (from baseBlockSchema)
  title,
  content,
  cta,
  // Custom props
  features = [],
  columns = '3',
  showIcons = true,
  // Base design props
  backgroundColor,
  // Base advanced props
  className,
  id,
}: HeroProps) {
  // Use buildSectionClasses helper (NEVER hardcode colors)
  const sectionClasses = buildSectionClasses('py-16 px-4 md:py-24', {
    backgroundColor,
    className,
  })

  const gridCols = {
    '2': 'grid-cols-1 md:grid-cols-2',
    '3': 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3',
    '4': 'grid-cols-1 md:grid-cols-2 lg:grid-cols-4',
  }[columns]

  return (
    <section
      id={id}
      className={sectionClasses}
      data-cy={sel('blocks.hero.container')}
    >
      <div className="container mx-auto">
        {title && (
          <h2 className="text-3xl font-bold text-center mb-4">{title}</h2>
        )}
        {content && (
          <div
            className="text-center text-muted-foreground mb-8 max-w-2xl mx-auto"
            dangerouslySetInnerHTML={{ __html: content }}
          />
        )}

        {features && features.length > 0 && (
          <div className={`grid ${gridCols} gap-6`}>
            {features.map((feature, index) => (
              <div
                key={index}
                className="p-6 rounded-lg bg-card"
                data-cy={sel('blocks.hero.feature', { index: String(index) })}
              >
                {showIcons && feature.icon && (
                  <span className="text-2xl mb-4 block">{feature.icon}</span>
                )}
                <h3 className="font-semibold mb-2">{feature.title}</h3>
                {feature.description && (
                  <p className="text-muted-foreground">{feature.description}</p>
                )}
              </div>
            ))}
          </div>
        )}

        {cta?.text && cta?.link && (
          <div className="mt-8 text-center">
            <a
              href={cta.link}
              target={cta.target || '_self'}
              className="inline-flex items-center px-6 py-3 bg-primary text-primary-foreground rounded-md"
              data-cy={sel('blocks.hero.cta')}
            >
              {cta.text}
            </a>
          </div>
        )}
      </div>
    </section>
  )
}
```

### File 5: index.ts

```typescript
export { config } from './config'
export { schema } from './schema'
export { fields, fieldDefinitions } from './fields'
export { HeroBlock as Component } from './component'

export type { HeroProps } from './schema'
```

## Field Types (16 Available)

| Type | Description | Additional Props |
|------|-------------|------------------|
| `text` | Single line text | `placeholder`, `maxLength` |
| `textarea` | Multi-line text | `rows`, `maxLength` |
| `url` | URL input | `placeholder` |
| `email` | Email input | `placeholder` |
| `number` | Numeric input | `min`, `max`, `step` |
| `select` | Dropdown | `options: [{label, value}]` |
| `checkbox` | Boolean toggle | - |
| `radio` | Radio group | `options: [{label, value}]` |
| `rich-text` | WYSIWYG editor | - |
| `image` | Image upload | `aspectRatio`, `maxSize` |
| `media-library` | Media Library modal | Opens full media browser with search, filter, tags, upload |
| `color` | Color picker | `presets` |
| `date` | Date picker | `format` |
| `time` | Time picker | `format` |
| `datetime` | DateTime picker | `format` |
| `array` | Repeatable items | `itemFields`, `minItems`, `maxItems` |

### media-library Field Type

The `media-library` field type opens the full Media Library modal instead of a basic file upload. Users can browse existing media, search, filter by type/tags, and upload new files.

**Usage in fields.ts:**

```typescript
{
  name: 'backgroundImage',
  label: 'Background Image',
  type: 'media-library',
  tab: 'design',
  required: false,
  helpText: 'Optional background image (recommended: 1920x1080px)',
}
```

**In array sub-fields:**

```typescript
{
  name: 'logos',
  type: 'array',
  itemFields: [
    {
      name: 'image',
      label: 'Logo Image',
      type: 'media-library',  // Works inside arrays too
      tab: 'content',
      required: true,
    },
  ],
}
```

**Key behavior:**
- Stores URL string (not media ID) in block data
- Zero schema changes needed (blocks use `z.string().url()`)
- Empty state: dashed border with "Browse Media Library" prompt
- With value: image preview with Change/Remove hover overlay
- Both `dynamic-form.tsx` and `array-field.tsx` handle this type

**Migration from `'image'` to `'media-library'`:**
Simply change `type: 'image'` to `type: 'media-library'` in any block's `fields.ts`. No schema or component changes required.

## Block Categories (15)

```typescript
type BlockCategory =
  | 'hero'         // Hero sections
  | 'features'     // Feature showcases
  | 'cta'          // Call to action
  | 'content'      // Text content
  | 'testimonials' // Customer testimonials
  | 'pricing'      // Pricing tables
  | 'faq'          // FAQ sections
  | 'stats'        // Statistics/metrics
  | 'gallery'      // Image galleries
  | 'timeline'     // Timelines
  | 'contact'      // Contact forms
  | 'newsletter'   // Newsletter signup
  | 'team'         // Team members
  | 'portfolio'    // Portfolio items
  | 'custom'       // Custom/other
```

## Existing Blocks (Default Theme)

| Block | Category | Description |
|-------|----------|-------------|
| `benefits` | features | 3-column grid with colored borders |
| `cta-section` | cta | Title, description, buttons |
| `faq-accordion` | faq | Expandable accordion items |
| `features-grid` | features | Grid with icons, titles |
| `hero` | hero | Full-width hero section |
| `hero-with-form` | hero | Hero with lead capture form |
| `jumbotron` | hero | Large hero with fullscreen mode |
| `logo-cloud` | content | Partner/client logos |
| `post-content` | content | Blog post editorial styling |
| `pricing-table` | pricing | Pricing comparison |
| `split-content` | content | Two-column (image + text) |
| `stats-counter` | stats | Key metrics with numbers |
| `testimonials` | testimonials | Customer testimonials grid |
| `text-content` | content | Rich text paragraphs |
| `timeline` | timeline | Vertical/horizontal timeline |
| `video-hero` | hero | Hero with YouTube/Vimeo video |

## BLOCK_SELECTORS Pattern

```typescript
// contents/themes/{theme}/lib/selectors.ts

export const BLOCK_SELECTORS = {
  hero: {
    container: 'block-hero',
    feature: 'hero-feature-{index}',
    cta: 'hero-cta',
  },
  faqAccordion: {
    container: 'block-faq-accordion',
    item: 'faq-item-{index}',
    question: 'faq-question-{index}',
    answer: 'faq-answer-{index}',
  },
  featuresGrid: {
    container: 'block-features-grid',
    item: 'feature-item-{index}',
  },
  // ... add entry for each block
} as const
```

**Using selectors in components:**
```typescript
import { sel } from '../../lib/selectors'

// Static selector
<section data-cy={sel('blocks.hero.container')}>

// Dynamic selector with placeholder
<div data-cy={sel('blocks.hero.feature', { index: String(index) })}>
```

## BLOCK_REGISTRY

```typescript
// core/lib/registries/block-registry.ts (AUTO-GENERATED)

export const BLOCK_REGISTRY: Record<string, BlockConfig> = {
  hero: {
    slug: 'hero',
    name: 'Hero Section',
    category: 'hero',
    icon: 'LayoutTemplate',
    fieldDefinitions: [...],
    examples: [...],
  },
  // ...
}
```

**Rebuild registry after creating/modifying blocks:**
```bash
node core/scripts/build/registry.mjs
```

## buildSectionClasses Helper

```typescript
import { buildSectionClasses } from '@/core/types/blocks'

// Returns combined class string with background color and custom classes
const classes = buildSectionClasses('py-16 px-4', {
  backgroundColor: 'gray-900',  // Maps to bg-gray-900
  className: 'custom-class',
})
// Output: "py-16 px-4 bg-gray-900 custom-class"
```

**Available background colors (10):**
```
white, gray-50, gray-100, gray-200, gray-300,
gray-800, gray-900, primary, secondary, accent
```

## Anti-Patterns

```typescript
// NEVER: Hardcode colors
<section className="bg-gray-900 text-white">

// CORRECT: Use buildSectionClasses with backgroundColor prop
<section className={buildSectionClasses('py-16', { backgroundColor })}>

// NEVER: Recreate base schema fields
export const schema = z.object({
  title: z.string(),  // Already in baseBlockSchema!
  content: z.string(),
})

// CORRECT: Extend baseBlockSchema
export const schema = baseBlockSchema.merge(z.object({
  // Only custom fields
  customField: z.string(),
}))

// NEVER: Wrong field order in fieldDefinitions
export const fieldDefinitions = [
  ...baseAdvancedFields,  // Wrong position!
  ...customContentFields,
  ...baseContentFields,
]

// CORRECT: content → design → advanced
export const fieldDefinitions = [
  ...baseContentFields,
  ...customContentFields,
  ...baseDesignFields,
  ...customDesignFields,
  ...baseAdvancedFields,  // Always last
]

// NEVER: Missing data-cy selectors
<section className="block-container">

// CORRECT: Include data-cy
<section data-cy={sel('blocks.myBlock.container')}>

// NEVER: Forget to rebuild registry
// Block won't appear in admin UI without registry entry

// CORRECT: Always rebuild after changes
// node core/scripts/build/registry.mjs
```

## Checklist

Before finalizing a block:

- [ ] Folder name matches slug in config.ts
- [ ] Schema extends baseBlockSchema with .merge()
- [ ] Fields in correct order: content → design → advanced
- [ ] Component uses buildSectionClasses helper
- [ ] Component has data-cy selectors
- [ ] Block selectors added to BLOCK_SELECTORS
- [ ] index.ts exports all required items
- [ ] Registry rebuilt (`node core/scripts/build/registry.mjs`)
- [ ] Block appears in BLOCK_REGISTRY
- [ ] No hardcoded colors
- [ ] TypeScript compiles without errors

## Scripts

### scaffold-block.py

Generate a new block with all 5 files:

```bash
python .claude/skills/page-builder-blocks/scripts/scaffold-block.py
```

Interactive prompts for: slug, name, description, category, icon, scope.

## Related Skills

- `cypress-selectors` - data-cy attribute patterns
- `shadcn-components` - UI component patterns
- `tailwind-theming` - CSS variable patterns
- `media-library` - Media Library system and components
