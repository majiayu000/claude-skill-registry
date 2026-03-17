---
name: install-sections
description: Build pages by installing shadcnblocks sections and implementing i18n. Use for each page after branding is defined. Takes page route and list of sections to install. Installs sections in order, creates page file, extracts text to de.json/en.json, and adds useTranslations.
---

# Page Builder

Install shadcnblocks sections and implement i18n for a page.

## Workflow

1. **Install Sections** - Install only NEW sections
   - Check if component file exists in `components/`
   - If exists: Skip installation, reuse existing component, do it with prop-based consolidation with variant prop if needed
   - If new: Run `pnpm dlx shadcn add @shadcnblocks/[section]`
   - **Never overwrite existing files**
2. **Create Page File** - Create/update app/[locale]/[route]/page.tsx
3. **Import Sections** - Import all installed components
4. **Arrange Sections** - Place in order as specified
5. **Extract Text** - Find all hardcoded text in sections
6. **Add to i18n** - Add text to messages/de.json and messages/en.json
7. **Replace with t()** - Use useTranslations hook in components

## Installing Sections

Install each section in the order provided:

```bash
pnpm dlx shadcn add @shadcnblocks/hero145
pnpm dlx shadcn add @shadcnblocks/feature139
pnpm dlx shadcn add @shadcnblocks/pricing1
```

If sections are navbar or footer, ensure only one instance per project and add it in the layout if not already present.

Sections are installed to `components/` directory.
Do not move components in subdirectories.
Do not create custom components, only modify installed ones for i18n.

## Preserving Existing Components

**CRITICAL: Never overwrite existing components.**

When `shadcn add` prompts about existing files, always choose to KEEP the existing version.

### Protected Components (if they exist):
- `components/ui/button.tsx` - Custom button styles from /init
- `components/ui/*.tsx` - Any existing UI components
- `components/*.tsx` - Any existing block components

### Installation Rule:
1. Before running `pnpm dlx shadcn add`, check if the component already exists
2. If component exists in `components/`, skip installation and reuse existing
3. Only install components that don't exist yet

### Example:
```bash
# Check if hero145 exists
# If components/hero145.tsx exists → Skip, reuse existing
# If not → Install with: pnpm dlx shadcn add @shadcnblocks/hero145
```

### Handling shadcn Prompts:
When shadcn asks about overwriting:
- Always select "No" / "Keep existing"
- Never overwrite custom-styled components

## Reuse of Components

If a section is already installed from a previous page, do not reinstall.
Simply import and use the existing component.
Make it reusable across pages by ensuring no hardcoded text remains.

## Page Structure

Add navbar and footer to layout if not already present.
Everything else goes into the page file.

```tsx
// app/[locale]/page.tsx (homepage)
// app/[locale]/leistungen/page.tsx (services)
// app/[locale]/kontakt/page.tsx (contact)

import { Hero145 } from '@/components/hero145'
import { Feature139 } from '@/components/feature139'

export default function Page() {
    return (
        <>
            <Hero145 />
            <Feature139 />
        </>
    )
}
```

## i18n Implementation

### 1. Extract Text

Find all hardcoded strings in the section component.

### 2. Add to JSON files

```json
// messages/de.json
{
	"hero": {
		"title": "Willkommen",
		"subtitle": "Beschreibung hier",
		"cta": "Jetzt starten"
	}
}

// messages/en.json
{
	"hero": {
		"title": "Welcome",
		"subtitle": "Description here",
		"cta": "Get Started"
	}
}
```

### 3. Use in Component

```tsx
'use client'
import { useTranslations } from 'next-intl'

export function Hero145() {
    const t = useTranslations('hero')

    return (
        <section>
            <h1>{ t('title') }</h1>
            <p>{ t('subtitle') }</p>
            <button>{ t('cta') }</button>
        </section>
    )
}
```

## Key Naming Convention

Use consistent key structure:

- `{section}.title`
- `{section}.subtitle`
- `{section}.description`
- `{section}.cta`
- `{section}.items.0.title`
- `{section}.items.0.description`

## Links and Navigation

See `/internal-links` command for connecting buttons to pages and sections.
See `/smooth-scroll` command for smooth scrolling setup.

## Output

- Sections installed in components/
- Page created at app/[locale]/[route]/page.tsx
- Text added to messages/de.json
- Text added to messages/en.json
- Components using useTranslations
