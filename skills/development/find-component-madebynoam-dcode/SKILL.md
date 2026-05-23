---
name: dcode:find-component
description: Find UI components from screenshots, route paths, or component names. Use when a designer asks "where does this live?", shares a screenshot and wants to find the code, needs to locate a component by its visual appearance, or wants to understand how a UI element is built. Works with React, Vue, Angular, and other component-based frameworks.
---

# Find Component

Find where UI components live in a codebase—from screenshots, routes, or names.

**For designers who ask:** "I see this button in the app... where's the code?"

## Input Types

The target can be:
1. **Screenshot path**: `/path/to/screenshot.png` - Find code from a visual
2. **Route path**: `settings/profile`, `dashboard/analytics` - Find components for a URL
3. **Component name**: `UserAvatar`, `PricingCard` - Find definition and usage

## Instructions

### 1. Determine Input Type

Check if input is:
- A file path ending in `.png`, `.jpg`, `.jpeg`, `.webp` → Screenshot
- Contains capital letters or PascalCase → Component name
- Otherwise → Route path

### 2A. For Screenshots

1. Read the screenshot using the Read tool
2. Identify visible UI elements:
   - Text content (buttons, labels, headings)
   - Distinctive patterns (cards, modals, forms)
   - Icons or images
   - Layout structure
3. Search the codebase for:
   - Exact text strings (most reliable)
   - Component patterns matching the layout
   - CSS class names or data attributes if visible
4. Cross-reference findings to narrow down the exact file

### 2B. For Route Paths

Map routes to likely component locations. Common patterns:

| Framework | Typical Structure |
|-----------|-------------------|
| Next.js | `app/{route}/page.tsx` or `pages/{route}.tsx` |
| React Router | Check route config, often `src/pages/` or `src/views/` |
| Vue | `src/views/` or `src/pages/` |
| Angular | `src/app/{feature}/` |

Search for route registration:
```bash
# Find route definitions
grep -r "path.*['\"]/{route}" --include="*.tsx" --include="*.ts" --include="*.js"
```

### 2C. For Component Names

Search for the component definition:
```bash
# Find component file
grep -r "function ComponentName\|const ComponentName\|class ComponentName" --include="*.tsx" --include="*.jsx" --include="*.vue"
```

### 3. Find Related Files

Once the main component is found, gather the full picture:

| Type | Pattern | Purpose |
|------|---------|---------|
| Main component | `index.tsx`, `ComponentName.tsx` | Core logic and JSX |
| Styles | `*.scss`, `*.css`, `*.styled.ts` | Visual styling |
| Types | `types.ts`, `*.types.ts` | TypeScript definitions |
| Tests | `*.test.tsx`, `*.spec.ts` | Test coverage |
| Hooks | `use-*.ts`, `hooks/` | Custom React hooks |
| Sub-components | Child directories | Nested components |
| Stories | `*.stories.tsx` | Storybook examples |

### 4. Output Format

Present findings clearly:

```
## Found: {target}

### Main Component
| File | Purpose |
|------|---------|
| `src/components/UserCard/index.tsx` | Main component |
| `src/components/UserCard/styles.scss` | Styling |

### Related Files
| File | Purpose |
|------|---------|
| `src/components/UserCard/Avatar.tsx` | Sub-component |
| `src/hooks/useUserData.ts` | Data fetching |

### Quick Start
- **To modify styling**: Edit `styles.scss`
- **To change behavior**: Edit `index.tsx`
- **To see examples**: Check `*.stories.tsx`
```

### 5. Provide Context for Designers

After listing files, add helpful guidance:
- Which file to start with based on likely task
- What design tokens/variables are used
- Any gotchas (e.g., "styles are using CSS modules")
- Related components that share patterns

## Examples

**Input:** Screenshot of a pricing card
**Output:** Located `PricingCard` component, styles, and data source

**Input:** `settings/notifications`
**Output:** Files for the notifications settings page

**Input:** `DatePicker`
**Output:** Component definition, styles, and usage examples
