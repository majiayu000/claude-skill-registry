---
name: Asset Manager
description: Organize design assets, optimize images and fonts, maintain brand asset libraries, implement version control for assets, and enforce naming conventions. Keep design assets organized and production-ready.
version: 1.0.0
tags: [assets, images, fonts, optimization, organization]
---

# Asset Manager

Keep design assets organized, optimized, and accessible.

## Core Principle

**Organized assets = faster development.**

Assets should be:

- Easy to find
- Properly named
- Optimized for production
- Version controlled
- Consistently formatted

---

## Phase 1: Asset Organization

### Directory Structure

```
assets/
├── images/
│   ├── products/
│   ├── team/
│   ├── marketing/
│   └── ui/
├── icons/
│   ├── svg/
│   └── png/
├── fonts/
│   ├── primary/
│   └── secondary/
├── videos/
├── logos/
│   ├── svg/
│   ├── png/
│   └── variants/
└── brand/
    ├── colors.json
    ├── typography.json
    └── guidelines.pdf
```

### Naming Conventions

**Images:**

```
{category}-{description}-{size}.{format}

Examples:
product-hero-1920x1080.jpg
team-sarah-400x400.jpg
ui-background-pattern.png
```

**Icons:**

```
{icon-name}-{variant}.svg

Examples:
home-outline.svg
home-filled.svg
user-circle.svg
arrow-right.svg
```

**Fonts:**

```
{font-family}-{weight}.{format}

Examples:
Inter-Regular.woff2
Inter-Bold.woff2
Poppins-SemiBold.woff2
```

### Automated Organization Script

```typescript
// scripts/organize-assets.ts

import fs from 'fs/promises'
import path from 'path'

interface AssetRule {
  pattern: RegExp
  destination: string
}

const rules: AssetRule[] = [
  { pattern: /product-/i, destination: 'images/products' },
  { pattern: /team-/i, destination: 'images/team' },
  { pattern: /icon-/i, destination: 'icons/svg' },
  { pattern: /logo-/i, destination: 'logos' }
]

async function organizeAssets(sourceDir: string) {
  const files = await fs.readdir(sourceDir)

  for (const file of files) {
    const sourcePath = path.join(sourceDir, file)
    const stat = await fs.stat(sourcePath)

    if (stat.isDirectory()) continue

    // Find matching rule
    const rule = rules.find(r => r.pattern.test(file))

    if (rule) {
      const destDir = path.join('assets', rule.destination)
      await fs.mkdir(destDir, { recursive: true })

      const destPath = path.join(destDir, file)
      await fs.rename(sourcePath, destPath)

      console.log(`Moved: ${file} → ${rule.destination}`)
    }
  }

  console.log('Assets organized!')
}

organizeAssets('./unsorted-assets')
```

---

## Phase 2: Image Optimization

### Install Optimization Tools

```bash
npm install sharp imagemin imagemin-mozjpeg imagemin-pngquant imagemin-svgo
```

### Optimize Images Script

```typescript
// scripts/optimize-images.ts

import sharp from 'sharp'
import imagemin from 'imagemin'
import imageminMozjpeg from 'imagemin-mozjpeg'
import imageminPngquant from 'imagemin-pngquant'
import imageminSvgo from 'imagemin-svgo'
import fs from 'fs/promises'
import path from 'path'

interface OptimizeOptions {
  quality?: number
  maxWidth?: number
  formats?: ('jpg' | 'png' | 'webp' | 'avif')[]
}

async function optimizeImages(inputDir: string, outputDir: string, options: OptimizeOptions = {}) {
  const { quality = 80, maxWidth = 2000, formats = ['jpg', 'png', 'webp'] } = options

  const files = await fs.readdir(inputDir)

  for (const file of files) {
    const inputPath = path.join(inputDir, file)
    const stat = await fs.stat(inputPath)

    if (stat.isDirectory()) continue

    const ext = path.extname(file).toLowerCase()
    const name = path.basename(file, ext)

    console.log(`Processing: ${file}`)

    // Skip SVGs (handle separately)
    if (ext === '.svg') {
      await optimizeSVG(inputPath, outputDir)
      continue
    }

    // Skip non-images
    if (!['.jpg', '.jpeg', '.png'].includes(ext)) continue

    // Read image
    const image = sharp(inputPath)
    const metadata = await image.metadata()

    // Resize if too large
    if (metadata.width && metadata.width > maxWidth) {
      image.resize(maxWidth, null, {
        withoutEnlargement: true,
        fit: 'inside'
      })
    }

    // Generate formats
    for (const format of formats) {
      const outputPath = path.join(outputDir, `${name}.${format}`)

      if (format === 'jpg') {
        await image.jpeg({ quality, mozjpeg: true }).toFile(outputPath)
      } else if (format === 'png') {
        await image.png({ quality, compressionLevel: 9 }).toFile(outputPath)
      } else if (format === 'webp') {
        await image.webp({ quality }).toFile(outputPath)
      } else if (format === 'avif') {
        await image.avif({ quality }).toFile(outputPath)
      }

      console.log(`  ✓ Generated ${format}`)
    }
  }

  console.log('Images optimized!')
}

async function optimizeSVG(inputPath: string, outputDir: string) {
  const fileName = path.basename(inputPath)
  const outputPath = path.join(outputDir, fileName)

  await imagemin([inputPath], {
    destination: outputDir,
    plugins: [
      imageminSvgo({
        plugins: [
          { name: 'removeViewBox', active: false },
          { name: 'removeDimensions', active: true },
          { name: 'removeUselessStrokeAndFill', active: true }
        ]
      })
    ]
  })

  console.log(`  ✓ Optimized SVG`)
}

// Usage
optimizeImages('./assets/images/raw', './assets/images/optimized', {
  quality: 85,
  maxWidth: 1920,
  formats: ['jpg', 'webp', 'avif']
})
```

### Responsive Images Generator

```typescript
// scripts/generate-responsive-images.ts

import sharp from 'sharp'
import fs from 'fs/promises'
import path from 'path'

const breakpoints = [
  { name: 'mobile', width: 640 },
  { name: 'tablet', width: 768 },
  { name: 'desktop', width: 1920 }
]

async function generateResponsiveImages(inputPath: string) {
  const ext = path.extname(inputPath)
  const name = path.basename(inputPath, ext)
  const dir = path.dirname(inputPath)

  for (const bp of breakpoints) {
    const image = sharp(inputPath)

    // Resize
    image.resize(bp.width, null, {
      withoutEnlargement: true,
      fit: 'inside'
    })

    // Generate WebP
    const webpPath = path.join(dir, `${name}-${bp.name}.webp`)
    await image.webp({ quality: 80 }).toFile(webpPath)
    console.log(`  ✓ ${name}-${bp.name}.webp`)

    // Generate AVIF
    const avifPath = path.join(dir, `${name}-${bp.name}.avif`)
    await image.avif({ quality: 80 }).toFile(avifPath)
    console.log(`  ✓ ${name}-${bp.name}.avif`)
  }

  console.log(`Generated responsive images for: ${name}`)
}

// Usage
generateResponsiveImages('./assets/images/hero.jpg')
```

---

## Phase 3: Font Management

### Font Optimization

```typescript
// scripts/optimize-fonts.ts

import { exec } from 'child_process'
import { promisify } from 'util'
import fs from 'fs/promises'
import path from 'path'

const execAsync = promisify(exec)

async function optimizeFonts(inputDir: string, outputDir: string) {
  const files = await fs.readdir(inputDir)

  for (const file of files) {
    const inputPath = path.join(inputDir, file)
    const ext = path.extname(file).toLowerCase()

    if (ext !== '.ttf' && ext !== '.otf') continue

    const name = path.basename(file, ext)

    console.log(`Processing: ${file}`)

    // Convert to WOFF2 (best compression)
    const woff2Path = path.join(outputDir, `${name}.woff2`)
    await convertToWOFF2(inputPath, woff2Path)
    console.log(`  ✓ ${name}.woff2`)

    // Convert to WOFF (fallback)
    const woffPath = path.join(outputDir, `${name}.woff`)
    await convertToWOFF(inputPath, woffPath)
    console.log(`  ✓ ${name}.woff`)
  }

  console.log('Fonts optimized!')
}

async function convertToWOFF2(input: string, output: string) {
  // Requires woff2_compress tool
  // Install: brew install woff2
  await execAsync(`woff2_compress ${input}`)
  const woff2File = input.replace(/\.(ttf|otf)$/, '.woff2')
  await fs.rename(woff2File, output)
}

async function convertToWOFF(input: string, output: string) {
  // Requires sfnt2woff tool
  await execAsync(`sfnt2woff ${input}`)
  const woffFile = input.replace(/\.(ttf|otf)$/, '.woff')
  await fs.rename(woffFile, output)
}

optimizeFonts('./assets/fonts/raw', './assets/fonts/optimized')
```

### Font Loading Strategy

```css
/* fonts.css */

/* Preload critical fonts */
@font-face {
  font-family: 'Inter';
  src:
    url('/fonts/Inter-Regular.woff2') format('woff2'),
    url('/fonts/Inter-Regular.woff') format('woff');
  font-weight: 400;
  font-style: normal;
  font-display: swap; /* Show fallback first */
}

@font-face {
  font-family: 'Inter';
  src:
    url('/fonts/Inter-Bold.woff2') format('woff2'),
    url('/fonts/Inter-Bold.woff') format('woff');
  font-weight: 700;
  font-style: normal;
  font-display: swap;
}
```

**Preload in HTML:**

```html
<head>
  <!-- Preload critical fonts -->
  <link rel="preload" href="/fonts/Inter-Regular.woff2" as="font" type="font/woff2" crossorigin />
  <link rel="preload" href="/fonts/Inter-Bold.woff2" as="font" type="font/woff2" crossorigin />
</head>
```

---

## Phase 4: Asset Version Control

### Git LFS Setup

```bash
# Install Git LFS
brew install git-lfs
git lfs install

# Track large files
git lfs track "*.psd"
git lfs track "*.ai"
git lfs track "*.sketch"
git lfs track "*.fig"
git lfs track "*.mp4"
git lfs track "*.mov"
git lfs track "assets/images/**/*.jpg"
git lfs track "assets/images/**/*.png"

# Add .gitattributes
git add .gitattributes
git commit -m "Configure Git LFS"
```

### Asset Versioning System

```typescript
// scripts/version-assets.ts

import fs from 'fs/promises'
import path from 'path'
import crypto from 'crypto'

interface AssetVersion {
  path: string
  hash: string
  size: number
  modified: string
  version: number
}

class AssetVersionManager {
  private versionFile = 'asset-versions.json'
  private versions: Map<string, AssetVersion[]> = new Map()

  async load() {
    try {
      const data = await fs.readFile(this.versionFile, 'utf-8')
      const parsed = JSON.parse(data)

      for (const [path, versions] of Object.entries(parsed)) {
        this.versions.set(path, versions as AssetVersion[])
      }
    } catch (error) {
      // File doesn't exist yet
    }
  }

  async save() {
    const data = Object.fromEntries(this.versions)
    await fs.writeFile(this.versionFile, JSON.stringify(data, null, 2))
  }

  async trackAsset(filePath: string) {
    const buffer = await fs.readFile(filePath)
    const hash = crypto.createHash('sha256').update(buffer).digest('hex')
    const stat = await fs.stat(filePath)

    const versions = this.versions.get(filePath) || []
    const lastVersion = versions[versions.length - 1]

    // Check if changed
    if (lastVersion && lastVersion.hash === hash) {
      console.log(`No changes: ${filePath}`)
      return
    }

    // Add new version
    versions.push({
      path: filePath,
      hash,
      size: stat.size,
      modified: stat.mtime.toISOString(),
      version: versions.length + 1
    })

    this.versions.set(filePath, versions)

    console.log(`Tracked: ${filePath} (v${versions.length})`)
  }

  async trackDirectory(dirPath: string) {
    const files = await fs.readdir(dirPath, { recursive: true })

    for (const file of files) {
      const filePath = path.join(dirPath, file.toString())
      const stat = await fs.stat(filePath)

      if (stat.isDirectory()) continue

      await this.trackAsset(filePath)
    }
  }
}

// Usage
const manager = new AssetVersionManager()
await manager.load()
await manager.trackDirectory('./assets')
await manager.save()
```

---

## Phase 5: Brand Asset Library

### Brand Kit Structure

```
brand/
├── logos/
│   ├── primary/
│   │   ├── logo-full.svg
│   │   ├── logo-icon.svg
│   │   └── logo-wordmark.svg
│   ├── variations/
│   │   ├── logo-white.svg
│   │   ├── logo-black.svg
│   │   └── logo-inverted.svg
│   └── exports/
│       ├── png/
│       ├── pdf/
│       └── eps/
├── colors/
│   ├── colors.json
│   ├── colors.css
│   └── colors.scss
├── typography/
│   ├── fonts/
│   └── typography.json
└── guidelines/
    ├── brand-guidelines.pdf
    ├── logo-usage.pdf
    └── color-usage.pdf
```

### Brand Asset Manifest

```typescript
// brand/manifest.ts

export interface BrandAssets {
  version: string
  lastUpdated: string
  logos: LogoAsset[]
  colors: ColorAsset[]
  typography: TypographyAsset[]
}

export interface LogoAsset {
  name: string
  variants: {
    full: string
    icon: string
    wordmark: string
  }
  formats: {
    svg: string
    png: { [size: string]: string }
    pdf: string
  }
}

export interface ColorAsset {
  name: string
  hex: string
  rgb: { r: number; g: number; b: number }
  usage: string
}

export interface TypographyAsset {
  name: string
  family: string
  weights: number[]
  formats: string[]
}

export const brandAssets: BrandAssets = {
  version: '2.0.0',
  lastUpdated: '2024-01-15',
  logos: [
    {
      name: 'Primary Logo',
      variants: {
        full: '/brand/logos/logo-full.svg',
        icon: '/brand/logos/logo-icon.svg',
        wordmark: '/brand/logos/logo-wordmark.svg'
      },
      formats: {
        svg: '/brand/logos/logo-full.svg',
        png: {
          '1x': '/brand/logos/exports/png/logo-full@1x.png',
          '2x': '/brand/logos/exports/png/logo-full@2x.png',
          '3x': '/brand/logos/exports/png/logo-full@3x.png'
        },
        pdf: '/brand/logos/exports/pdf/logo-full.pdf'
      }
    }
  ],
  colors: [
    {
      name: 'Primary',
      hex: '#0066cc',
      rgb: { r: 0, g: 102, b: 204 },
      usage: 'Primary actions, links, brand elements'
    }
  ],
  typography: [
    {
      name: 'Inter',
      family: 'Inter',
      weights: [400, 600, 700],
      formats: ['woff2', 'woff']
    }
  ]
}
```

---

## Best Practices

### 1. Optimize for Web

- **Images:** Use WebP/AVIF with JPEG fallback
- **Icons:** Use SVG sprites for multiple icons
- **Fonts:** Use WOFF2 with WOFF fallback
- **Videos:** Compress and provide multiple formats

### 2. Lazy Loading

```tsx
// Lazy load images
;<img src="placeholder.jpg" data-src="hero.jpg" loading="lazy" alt="Hero" />

// Or use Next.js Image
import Image from 'next/image'
;<Image src="/hero.jpg" width={1920} height={1080} placeholder="blur" alt="Hero" />
```

### 3. Asset CDN

```typescript
// Use CDN for assets
const CDN_URL = process.env.CDN_URL || ''

export function getAssetUrl(path: string): string {
  if (CDN_URL) {
    return `${CDN_URL}${path}`
  }
  return path
}

// Usage
<img src={getAssetUrl('/images/hero.jpg')} alt="Hero" />
```

### 4. Automated Asset Pipeline

```typescript
// scripts/asset-pipeline.ts

async function runAssetPipeline() {
  console.log('Starting asset pipeline...')

  // 1. Organize assets
  await organizeAssets('./unsorted')

  // 2. Optimize images
  await optimizeImages('./assets/images/raw', './assets/images/optimized')

  // 3. Generate responsive images
  await generateResponsiveImages('./assets/images/optimized')

  // 4. Optimize fonts
  await optimizeFonts('./assets/fonts/raw', './assets/fonts/optimized')

  // 5. Version assets
  const manager = new AssetVersionManager()
  await manager.load()
  await manager.trackDirectory('./assets')
  await manager.save()

  console.log('Asset pipeline complete!')
}

runAssetPipeline()
```

---

## Tools & Resources

**Optimization Tools:**

- [Sharp](https://sharp.pixelplumbing.com/) - Image processing
- [ImageOptim](https://imageoptim.com/) - Image compression
- [SVGO](https://github.com/svg/svgo) - SVG optimization
- [Squoosh](https://squoosh.app/) - Online image compression

**Font Tools:**

- [Glyphhanger](https://github.com/zachleat/glyphhanger) - Font subsetting
- [Transfonter](https://transfonter.org/) - Font conversion
- [FontForge](https://fontforge.org/) - Font editor

**Related Skills:**

- `visual-designer` - Design principles
- `figma-developer` - Export from Figma
- `brand-designer` - Brand asset creation

---

**Organized assets, optimized performance.** 📦
