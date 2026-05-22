---
name: Figma Developer
description: Extract components from Figma, convert designs to React components, sync design tokens, and generate code from designs. Bridge the gap between design and code with automated workflows.
version: 1.0.0
tags: [figma, design-to-code, design-tokens, component-generation]
---

# Figma Developer

Turn Figma designs into production-ready code.

## Core Principle

**Design is the single source of truth.**

Designers work in Figma. Developers build from Figma. The bridge between them should be automated, not manual.

---

## Phase 1: Setup & Authentication

### Get Figma Access Token

1. Go to [Figma Settings](https://www.figma.com/settings)
2. Scroll to "Personal access tokens"
3. Click "Generate new token"
4. Name it (e.g., "Development")
5. Copy and save securely

### Environment Setup

```bash
# .env
FIGMA_ACCESS_TOKEN=figd_...
```

### Install Figma Client

```bash
npm install node-fetch
```

### Test Connection

```typescript
import { FigmaClient } from '@/integrations/design-tools/figma/client'

const client = new FigmaClient({
  accessToken: process.env.FIGMA_ACCESS_TOKEN
})

// Test with a public file
const file = await client.getFile('abc123xyz')
console.log('Connected! File:', file.name)
```

---

## Phase 2: Extract Design Tokens

### What Are Design Tokens?

Design tokens are design decisions (colors, typography, spacing) stored as code.

**Benefits:**

- Single source of truth
- Consistent across platforms
- Easy to update
- Type-safe

### Extract Tokens from Figma

```typescript
// scripts/sync-design-tokens.ts

import { FigmaClient } from '@/integrations/design-tools/figma/client'
import fs from 'fs/promises'

async function syncDesignTokens() {
  const client = new FigmaClient()
  const fileKey = 'YOUR_FIGMA_FILE_KEY'

  console.log('Extracting design tokens...')

  // Extract tokens
  const tokens = await client.extractDesignTokens(fileKey)

  console.log(`Found:`)
  console.log(`  ${tokens.colors.length} colors`)
  console.log(`  ${tokens.typography.length} text styles`)
  console.log(`  ${tokens.spacing.length} spacing values`)

  // Export as CSS
  const css = await client.exportTokensAsCSS(fileKey)
  await fs.writeFile('src/styles/design-tokens.css', css)

  // Export as JSON
  const json = await client.exportTokensAsJSON(fileKey)
  await fs.writeFile('src/styles/design-tokens.json', json)

  console.log('Design tokens synced!')
}

syncDesignTokens()
```

### Use Tokens in Code

```typescript
// src/styles/design-tokens.css
:root {
  /* Colors */
  --color-primary: #0066cc;
  --color-secondary: #10b981;
  --color-neutral-100: #f9fafb;
  --color-neutral-900: #111827;

  /* Typography */
  --font-heading-family: Inter;
  --font-heading-size: 48px;
  --font-heading-weight: 700;

  /* Spacing */
  --space-4: 16px;
  --space-8: 32px;
}
```

**Usage in React:**

```tsx
// components/Button.tsx

export function Button({ children }: { children: React.ReactNode }) {
  return (
    <button
      style={{
        backgroundColor: 'var(--color-primary)',
        color: 'white',
        padding: 'var(--space-4)',
        fontFamily: 'var(--font-heading-family)',
        fontWeight: 'var(--font-heading-weight)',
        border: 'none',
        borderRadius: '8px',
        cursor: 'pointer'
      }}
    >
      {children}
    </button>
  )
}
```

---

## Phase 3: Export Assets

### Export Icons as SVG

```typescript
// scripts/export-icons.ts

import { FigmaClient } from '@/integrations/design-tools/figma/client'
import fs from 'fs/promises'

async function exportIcons() {
  const client = new FigmaClient()
  const fileKey = 'YOUR_FIGMA_FILE_KEY'

  // Get file
  const file = await client.getFile(fileKey)

  // Find "Icons" frame
  const iconsFrame = findNode(file.document, 'Icons')

  if (!iconsFrame || !iconsFrame.children) {
    throw new Error('Icons frame not found')
  }

  console.log(`Found ${iconsFrame.children.length} icons`)

  // Export as SVG
  const iconIds = iconsFrame.children.map(child => child.id)
  const svgs = await client.exportImages(fileKey, iconIds, {
    format: 'svg'
  })

  // Save each SVG
  for (const svg of svgs) {
    const response = await fetch(svg.url)
    const content = await response.text()
    await fs.writeFile(`public/icons/${svg.name}.svg`, content)
    console.log(`  ✓ ${svg.name}.svg`)
  }

  console.log('Icons exported!')
}

function findNode(node: any, name: string): any {
  if (node.name === name) return node
  if (node.children) {
    for (const child of node.children) {
      const found = findNode(child, name)
      if (found) return found
    }
  }
  return null
}

exportIcons()
```

### Generate React Icon Components

```typescript
// scripts/generate-icon-components.ts

import { FigmaClient } from '@/integrations/design-tools/figma/client'
import fs from 'fs/promises'

async function generateIconComponents() {
  const client = new FigmaClient()
  const fileKey = 'YOUR_FIGMA_FILE_KEY'

  const file = await client.getFile(fileKey)
  const iconsFrame = findNode(file.document, 'Icons')

  if (!iconsFrame || !iconsFrame.children) {
    throw new Error('Icons frame not found')
  }

  // Export icons
  const iconIds = iconsFrame.children.map(child => child.id)
  const svgs = await client.exportImages(fileKey, iconIds, {
    format: 'svg'
  })

  // Generate React components
  for (const svg of svgs) {
    const response = await fetch(svg.url)
    const svgContent = await response.text()

    // Convert to React component
    const componentName = toPascalCase(svg.name)
    const component = `
import React from 'react'

export function ${componentName}Icon(props: React.SVGProps<SVGSVGElement>) {
  return (
    ${svgContent.replace('<svg', '<svg {...props}')}
  )
}
    `.trim()

    await fs.writeFile(`components/icons/${componentName}Icon.tsx`, component)
    console.log(`  ✓ ${componentName}Icon.tsx`)
  }

  // Generate index file
  const indexContent = svgs
    .map(svg => {
      const componentName = toPascalCase(svg.name)
      return `export { ${componentName}Icon } from './${componentName}Icon'`
    })
    .join('\n')

  await fs.writeFile('components/icons/index.ts', indexContent)

  console.log('Icon components generated!')
}

function toPascalCase(str: string): string {
  return str
    .split(/[-_\s]+/)
    .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
    .join('')
}

function findNode(node: any, name: string): any {
  if (node.name === name) return node
  if (node.children) {
    for (const child of node.children) {
      const found = findNode(child, name)
      if (found) return found
    }
  }
  return null
}

generateIconComponents()
```

**Usage:**

```tsx
import { HomeIcon, UserIcon, SettingsIcon } from '@/components/icons'

export function Navigation() {
  return (
    <nav>
      <HomeIcon width={24} height={24} />
      <UserIcon width={24} height={24} />
      <SettingsIcon width={24} height={24} />
    </nav>
  )
}
```

---

## Phase 4: Component Generation

### Extract Component Structure

```typescript
// scripts/extract-components.ts

import { FigmaClient } from '@/integrations/design-tools/figma/client'

async function extractComponents() {
  const client = new FigmaClient()
  const fileKey = 'YOUR_FIGMA_FILE_KEY'

  // Get components
  const components = await client.getFileComponents(fileKey)

  console.log('Components:')
  for (const [key, component] of Object.entries(components)) {
    console.log(`  ${component.name}`)
    console.log(`    Key: ${component.key}`)
    console.log(`    Description: ${component.description}`)
  }

  // Get component sets (variants)
  const componentSets = await client.getComponentSets(fileKey)

  console.log('\nComponent Sets:')
  for (const [setId, variants] of Object.entries(componentSets)) {
    console.log(`  Set: ${setId}`)
    for (const variant of variants) {
      console.log(`    - ${variant.name}`)
    }
  }
}

extractComponents()
```

### Generate Button Component from Figma

```typescript
// scripts/generate-button.ts

import { FigmaClient } from '@/integrations/design-tools/figma/client'
import fs from 'fs/promises'

async function generateButtonComponent() {
  const client = new FigmaClient()
  const fileKey = 'YOUR_FIGMA_FILE_KEY'

  // Get button component
  const components = await client.getFileComponents(fileKey)
  const buttonComponent = Object.values(components).find(c =>
    c.name.toLowerCase().includes('button')
  )

  if (!buttonComponent) {
    throw new Error('Button component not found')
  }

  // Get component node
  const file = await client.getFile(fileKey)
  const buttonNode = findNodeById(file.document, buttonComponent.key)

  if (!buttonNode) {
    throw new Error('Button node not found')
  }

  // Extract styles
  const styles = extractStyles(buttonNode)

  // Generate React component
  const component = `
import React from 'react'

interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'ghost'
  size?: 'sm' | 'md' | 'lg'
  children: React.ReactNode
  onClick?: () => void
}

export function Button({
  variant = 'primary',
  size = 'md',
  children,
  onClick
}: ButtonProps) {
  const baseStyles = {
    fontFamily: '${styles.fontFamily}',
    fontWeight: ${styles.fontWeight},
    fontSize: '${styles.fontSize}px',
    padding: '${styles.padding}',
    borderRadius: '${styles.borderRadius}px',
    border: 'none',
    cursor: 'pointer',
    transition: 'all 0.2s'
  }

  const variantStyles = {
    primary: {
      backgroundColor: '${styles.backgroundColor}',
      color: '${styles.color}'
    },
    secondary: {
      backgroundColor: 'transparent',
      color: '${styles.backgroundColor}',
      border: '2px solid ${styles.backgroundColor}'
    },
    ghost: {
      backgroundColor: 'transparent',
      color: '${styles.color}'
    }
  }

  return (
    <button
      style={{ ...baseStyles, ...variantStyles[variant] }}
      onClick={onClick}
    >
      {children}
    </button>
  )
}
  `.trim()

  await fs.writeFile('components/Button.tsx', component)
  console.log('Button component generated!')
}

function findNodeById(node: any, id: string): any {
  if (node.id === id) return node
  if (node.children) {
    for (const child of node.children) {
      const found = findNodeById(child, id)
      if (found) return found
    }
  }
  return null
}

function extractStyles(node: any) {
  return {
    fontFamily: node.style?.fontFamily || 'Inter',
    fontWeight: node.style?.fontWeight || 600,
    fontSize: node.style?.fontSize || 16,
    padding: '12px 24px',
    borderRadius: node.cornerRadius || 8,
    backgroundColor: rgbToHex(node.fills?.[0]?.color || { r: 0, g: 0.4, b: 0.8 }),
    color: '#ffffff'
  }
}

function rgbToHex(color: any): string {
  const r = Math.round(color.r * 255)
    .toString(16)
    .padStart(2, '0')
  const g = Math.round(color.g * 255)
    .toString(16)
    .padStart(2, '0')
  const b = Math.round(color.b * 255)
    .toString(16)
    .padStart(2, '0')
  return `#${r}${g}${b}`
}

generateButtonComponent()
```

---

## Phase 5: Automated Workflows

### Set Up GitHub Actions

```yaml
# .github/workflows/sync-figma.yml

name: Sync Figma Design Tokens

on:
  schedule:
    - cron: '0 9 * * *' # Every day at 9am
  workflow_dispatch: # Manual trigger

jobs:
  sync:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - uses: actions/setup-node@v3
        with:
          node-version: 18

      - run: npm install

      - name: Sync design tokens
        env:
          FIGMA_ACCESS_TOKEN: ${{ secrets.FIGMA_ACCESS_TOKEN }}
        run: npm run sync:design-tokens

      - name: Create Pull Request
        uses: peter-evans/create-pull-request@v5
        with:
          title: 'chore: sync design tokens from Figma'
          body: 'Automated sync of design tokens from Figma'
          branch: 'figma/sync-tokens'
          commit-message: 'chore: sync design tokens'
```

### Package.json Scripts

```json
{
  "scripts": {
    "sync:design-tokens": "tsx scripts/sync-design-tokens.ts",
    "export:icons": "tsx scripts/export-icons.ts",
    "generate:icons": "tsx scripts/generate-icon-components.ts",
    "figma:sync-all": "npm run sync:design-tokens && npm run generate:icons"
  }
}
```

---

## Best Practices

### 1. Organize Figma Files

**Structure:**

```
Design System File
├── 📄 Cover (description)
├── 🎨 Colors (all color styles)
├── 📝 Typography (all text styles)
├── 📏 Spacing (spacing guide)
├── 🧩 Components
│   ├── Buttons
│   ├── Forms
│   └── Cards
└── 🖼️ Icons (all icons in one frame)
```

### 2. Naming Conventions

**Colors:**

```
Primary/500
Secondary/500
Neutral/100
Neutral/900
Success
Error
```

**Typography:**

```
Heading/Large
Heading/Medium
Body/Regular
Body/Small
```

**Components:**

```
Button/Primary
Button/Secondary
Card/Default
Card/Elevated
```

### 3. Use Figma Variables (Beta)

Figma now supports variables natively. Use them for:

- Colors
- Spacing
- Border radius
- Typography sizes

Extract these automatically with the API.

### 4. Version Control

```typescript
// Check for Figma updates
async function checkForUpdates() {
  const client = new FigmaClient()
  const fileKey = 'YOUR_FIGMA_FILE_KEY'

  const file = await client.getFile(fileKey)
  const currentVersion = file.version

  // Store in database or file
  const previousVersion = await getPreviousVersion()

  if (currentVersion !== previousVersion) {
    console.log('Figma file updated!')
    console.log(`Version: ${previousVersion} → ${currentVersion}`)

    // Trigger sync
    await syncDesignTokens()
    await savePreviousVersion(currentVersion)
  } else {
    console.log('No updates')
  }
}
```

---

## Common Patterns

### Pattern 1: Token-Based Development

```typescript
// 1. Extract tokens
const tokens = await client.extractDesignTokens(fileKey)

// 2. Generate CSS variables
const css = generateCSS(tokens)

// 3. Generate TypeScript types
const types = `
export type ColorToken =
  ${tokens.colors.map(c => `| '${c.name}'`).join('\n  ')}

export type SpacingToken =
  ${tokens.spacing.map(s => `| '${s.name}'`).join('\n  ')}
`.trim()

await fs.writeFile('src/types/tokens.ts', types)

// 4. Use in components
import { ColorToken } from '@/types/tokens'

interface ButtonProps {
  color: ColorToken
}
```

### Pattern 2: Component Sync

```typescript
// Keep components in sync with Figma
async function syncComponent(componentName: string) {
  const client = new FigmaClient()
  const fileKey = 'YOUR_FIGMA_FILE_KEY'

  // Get component from Figma
  const components = await client.getFileComponents(fileKey)
  const component = Object.values(components).find(c => c.name === componentName)

  if (!component) {
    throw new Error(`Component not found: ${componentName}`)
  }

  // Generate code
  const code = await generateComponentCode(component)

  // Write to file
  await fs.writeFile(`components/${componentName}.tsx`, code)

  console.log(`Synced: ${componentName}`)
}
```

---

## Troubleshooting

### Issue: Token Names Don't Match

**Problem:** Figma style names have spaces/special characters

**Solution:** Normalize names

```typescript
function normalizeTokenName(name: string): string {
  return name
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-|-$/g, '')
}
```

### Issue: Colors Look Different

**Problem:** RGB values need conversion

**Solution:** Use proper color space conversion

```typescript
function rgbToHex(color: { r: number; g: number; b: number }): string {
  const r = Math.round(color.r * 255)
  const g = Math.round(color.g * 255)
  const b = Math.round(color.b * 255)
  return `#${r.toString(16).padStart(2, '0')}${g.toString(16).padStart(2, '0')}${b.toString(16).padStart(2, '0')}`
}
```

### Issue: API Rate Limiting

**Problem:** Too many requests

**Solution:** Cache responses

```typescript
const cache = new Map<string, { data: any; timestamp: number }>()

async function getCachedFile(fileKey: string) {
  const cached = cache.get(fileKey)

  if (cached && Date.now() - cached.timestamp < 60000) {
    return cached.data
  }

  const file = await client.getFile(fileKey)
  cache.set(fileKey, { data: file, timestamp: Date.now() })
  return file
}
```

---

## Tools & Resources

**Figma Plugins:**

- Figma Tokens - Manage design tokens
- Design Tokens - Export tokens
- Figma to Code - Generate code

**Libraries:**

- `@figma/rest-api-spec` - TypeScript types
- `figma-api` - Alternative client
- `style-dictionary` - Transform tokens

**Related Skills:**

- `design-system-architect` - Building design systems
- `visual-designer` - Design principles
- `asset-manager` - Managing exported assets

---

**Turn designs into code, automatically.** 🎨→💻
