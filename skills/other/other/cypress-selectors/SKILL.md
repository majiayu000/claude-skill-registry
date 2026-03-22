---
name: cypress-selectors
description: |
  3-level selector system for testing: CORE_SELECTORS + BLOCK_SELECTORS + THEME_SELECTORS.
  Provides helpers sel(), cySelector(), entitySelectors() for components and POMs.
  Use this skill when working with data-cy attributes, POMs, or Cypress tests.
allowed-tools: Read, Glob, Grep, Bash(python:*)
version: 1.1.0
---

# Cypress Selectors System

Centralized `data-cy` selector system for Cypress testing.

## Architecture Overview

```
┌─────────────────────────────────────────┐
│           CORE (Read-Only)              │
│  core/lib/test/core-selectors.ts        │
│  core/lib/test/selector-factory.ts      │
└─────────────────┬───────────────────────┘
                  │ imports
                  ▼
┌─────────────────────────────────────────┐
│         THEME (Editable)                │
│  contents/themes/{theme}/lib/selectors.ts│
│  ├── BLOCK_SELECTORS                    │
│  ├── DEVTOOLS_SELECTORS                 │
│  ├── THEME_SELECTORS = {                │
│  │     ...CORE_SELECTORS,               │
│  │     blocks: BLOCK_SELECTORS,         │
│  │     devtools: DEVTOOLS_SELECTORS     │
│  │   }                                  │
│  └── exports: sel, cySelector, etc.     │
└─────────────────┬───────────────────────┘
                  │ re-exports
                  ▼
┌─────────────────────────────────────────┐
│  tests/cypress/src/selectors.ts         │
│  (re-exports for test files)            │
└─────────────────┬───────────────────────┘
                  │ imports
        ┌─────────┴─────────┐
        ▼                   ▼
┌───────────────┐   ┌───────────────┐
│  Components   │   │     POMs      │
│  sel('x.y')   │   │ cySelector()  │
└───────────────┘   └───────────────┘
```

## When to Use This Skill

- Adding `data-cy` attributes to components
- Creating new BLOCK_SELECTORS for a block
- Working with Page Object Models (POMs)
- Validating selector coverage in UI
- Writing Cypress E2E tests

## Key Functions

### `sel(path: string, replacements?: object)`

Use in **components** to get the selector string for `data-cy`:

```typescript
// In block component: contents/themes/{theme}/blocks/{block-name}/component.tsx
import { sel } from '../../lib/selectors'

// Static selector - note the 'blocks.' prefix for block selectors
<section data-cy={sel('blocks.hero.container')}>
  <h2 data-cy={sel('blocks.hero.title')}>{title}</h2>
</section>

// Dynamic selector with replacement
{items.map((item, index) => (
  <div data-cy={sel('blocks.faqAccordion.item', { index: String(index) })}>
    {item.content}
  </div>
))}

// Core selectors (no 'blocks.' prefix)
<button data-cy={sel('auth.login.submit')}>Login</button>
```

### `cySelector(path: string, replacements?: object)`

Use in **POMs and Cypress tests** to get the CSS selector `[data-cy="..."]`:

```typescript
// In POM: contents/themes/{theme}/tests/cypress/src/features/MyPOM.ts
import { BasePOM } from '../core/BasePOM'
import { cySelector } from '../selectors'

export class HeroPOM extends BasePOM {
  get selectors() {
    return {
      container: cySelector('blocks.hero.container'),
      title: cySelector('blocks.hero.title'),
    }
  }

  // Dynamic selectors
  getItem(index: number) {
    return cy.get(cySelector('blocks.faqAccordion.item', { index: String(index) }))
  }

  // Factory method
  static create(): HeroPOM {
    return new HeroPOM()
  }
}
```

```typescript
// In test file: contents/themes/{theme}/tests/cypress/e2e/blocks/hero.cy.ts
import { cySelector } from '../../src/selectors'

describe('Hero Block', () => {
  it('should display the hero', () => {
    cy.get(cySelector('blocks.hero.container')).should('be.visible')
  })
})
```

### `entitySelectors(slug: string)`

Get all selectors for a specific entity:

```typescript
import { entitySelectors } from '../../src/selectors'

const taskSelectors = entitySelectors('tasks')
// Returns: { table, row, createBtn, editBtn, ... }
```

## Selector Paths

**IMPORTANT:** Block selectors use the `blocks.` prefix because BLOCK_SELECTORS is nested under `blocks:` in THEME_SELECTORS:

```typescript
// Block selectors - use 'blocks.' prefix
sel('blocks.hero.container')           // → 'block-hero'
sel('blocks.faqAccordion.item', { index: '0' })  // → 'faq-item-0'
sel('blocks.pricingTable.plan', { index: '1' }) // → 'pricing-plan-1'

// Core selectors - no prefix
sel('auth.login.form')                 // → 'login-form'
sel('entity.table', { slug: 'tasks' }) // → 'tasks-table'

// Devtools selectors - use 'devtools.' prefix
sel('devtools.scheduledActions.table') // → 'scheduled-actions-table'
```

## Naming Conventions

### Static Selectors
```
domain-element
```
Examples:
- `block-hero` (block container)
- `login-form` (core component)
- `nav-main` (navigation element)

### Dynamic Selectors with Placeholders
```
{placeholder}-element-{placeholder}
```
Placeholders:
- `{index}` - Array index (most common for blocks)
- `{slug}` - Entity slug (tasks, customers, pages)
- `{id}` - Record ID
- `{name}` - Field name
- `{action}` - Action name (edit, delete)

Examples:
- `faq-item-{index}` → `faq-item-0`
- `{slug}-row-{id}` → `tasks-row-123`
- `field-{name}` → `field-email`

## File Locations

| Type | Location | Who Modifies |
|------|----------|--------------|
| Core selectors | `core/lib/test/core-selectors.ts` | Core maintainers only |
| Selector factory | `core/lib/test/selector-factory.ts` | Core maintainers only |
| Block selectors | `contents/themes/{theme}/lib/selectors.ts` | Theme developers |
| Test re-exports | `contents/themes/{theme}/tests/cypress/src/selectors.ts` | Auto (re-exports) |
| POMs | `contents/themes/{theme}/tests/cypress/src/features/*POM.ts` | Test developers |

## Adding New Selectors

### For Block Components

Edit `contents/themes/{theme}/lib/selectors.ts`, add to BLOCK_SELECTORS:

```typescript
export const BLOCK_SELECTORS = {
  // ... existing blocks
  myNewBlock: {
    container: 'block-my-new-block',
    title: 'my-block-title',
    item: 'my-block-item-{index}',
  }
}
```

Then use in component with `blocks.` prefix:
```tsx
// contents/themes/{theme}/blocks/my-new-block/component.tsx
import { sel } from '../../lib/selectors'

<section data-cy={sel('blocks.myNewBlock.container')}>
  <h2 data-cy={sel('blocks.myNewBlock.title')}>{title}</h2>
</section>
```

### For Core Components

Edit `core/lib/test/core-selectors.ts`:

```typescript
export const CORE_SELECTORS = {
  // ... existing selectors
  myNewFeature: {
    container: 'my-feature-container',
    list: 'my-feature-list',
    item: 'my-feature-item-{id}',
  }
}
```

### For DevTools Components

Edit `contents/themes/{theme}/lib/selectors.ts`, add to DEVTOOLS_SELECTORS:

```typescript
export const DEVTOOLS_SELECTORS = {
  // ... existing selectors
  myDevTool: {
    page: 'devtools-my-tool-page',
    table: 'my-tool-table',
  }
}
```

## Anti-Patterns

```typescript
// ❌ NEVER: Hardcoded data-cy in component
<button data-cy="submit-btn">

// ❌ NEVER: Direct selector string in test
cy.get('[data-cy="submit-btn"]')

// ❌ NEVER: Missing 'blocks.' prefix for block selectors
sel('hero.container')  // Wrong!
sel('blocks.hero.container')  // Correct!

// ❌ NEVER: Import from core in theme components
import { sel } from '@/core/lib/test'  // Wrong!
import { sel } from '../../lib/selectors'  // Correct!

// ❌ NEVER: Add selector without UI element
// Only add selectors for existing UI elements
```

## Validation Scripts

### Validate all selectors use sel()
```bash
python .claude/skills/cypress-selectors/scripts/validate-selectors.py
```

### Find elements missing data-cy
```bash
python .claude/skills/cypress-selectors/scripts/extract-missing.py --path contents/themes/default/blocks/
```

### Generate block selectors for new block
```bash
# Basic generation
python .claude/skills/cypress-selectors/scripts/generate-block-selectors.py --block my-new-block

# Analyze existing block and generate full example
python .claude/skills/cypress-selectors/scripts/generate-block-selectors.py --block faq-accordion --analyze --full

# Just show selector entry without instructions
python .claude/skills/cypress-selectors/scripts/generate-block-selectors.py --block my-block --dry-run
```

## Checklist

Before committing UI changes:

- [ ] All interactive elements have `data-cy={sel('...')}`
- [ ] Block selectors use `sel('blocks.{blockName}.{element}')` path
- [ ] New selectors added to BLOCK_SELECTORS or CORE_SELECTORS
- [ ] POM updated with new selectors using `cySelector()`
- [ ] Selector validation test created in `_selectors/*.cy.ts`
- [ ] No hardcoded `data-cy` strings in components
- [ ] No direct core imports in theme files

## References

- Load `references/architecture.md` for detailed architecture
- Load `references/naming-conventions.md` for naming rules
- Load `references/anti-patterns.md` for common mistakes
