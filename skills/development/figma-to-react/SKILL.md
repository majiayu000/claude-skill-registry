---
name: figma-to-react
description: Extract Figma designs and generate production-ready React/Next.js components with TypeScript, Tailwind CSS, and pixel-perfect accuracy.
---

# Figma to React - Production-Ready Component Generator

## 🎯 Purpose

Extract **complete, lossless** design information from Figma and generate production-ready React/Next.js components with TypeScript and Tailwind CSS.

---

## 🚨 CRITICAL RULES - Read First!

### **Rule 1: NEVER Truncate Code**

Use **100% of Figma MCP output**. Every className, every property matters.

```tsx
// ✅ CORRECT: Keep ALL className from Figma MCP
<div className="absolute font-source-serif h-[108px] leading-[1.8] left-[100px] not-italic text-[20px] text-[rgba(29,38,45,0.8)] text-justify top-[210px] w-[1096px] whitespace-pre-wrap">

// ❌ WRONG: Removing any className
<div className="absolute left-[100px] top-[210px] font-source-serif text-[20px]">
```

### **Rule 2: Flatten `absolute contents` Structures**

**🔥 CRITICAL: Figma MCP returns nested `absolute contents` containers. `display: contents` makes the parent "disappear" - children are positioned relative to the nearest positioned ancestor (root)!**

**Key Insight: Children's positions are ALREADY absolute - DO NOT add parent's top/left!**

```tsx
// ❌ WRONG: Figma MCP output (has redundant parent wrapper)
<div className="absolute contents left-0 top-[41px]">
  <p className="absolute left-[100px] top-[41px]">TITLE</p>
  <div className="absolute left-0 top-[100px]">Line</div>
</div>

// ✅ CORRECT: Just remove the parent wrapper, keep children's positions AS-IS
<>
  <p className="absolute left-[100px] top-[41px]">TITLE</p>
  <div className="absolute left-0 top-[100px] w-[1920px] h-[1px] bg-[#C5CBCE] opacity-30" />
</>
```

**Position Handling Rules:**

| Parent Type | Child Position | Action |
|-------------|----------------|--------|
| `absolute contents` | Child has own `top/left` | **Keep child position AS-IS**, just remove parent |
| `absolute` (no contents) | Child has relative `top/left` | Calculate: `parent + child` |
| `relative` | Child has `top/left` | Calculate: `parent + child` |

**🔥 The Golden Rule:**
```
If parent has "contents" class → Child positions are already absolute → Keep AS-IS
If parent has NO "contents" class → Child positions are relative → Add parent + child
```

**Reference: Verified correct positions (from production HTML):**
- Header text: `top-[41px]` (not 82px)
- Header line: `top-[100px]` (not 141px)
- Footer line: `top-[980px]`
- Page number: `top-[1004px]`

### **Rule 3: Extract Dimensions from Metadata**

**NEVER hardcode dimensions!**

```typescript
// 1. Get metadata first
const metadata = await mcp__figma__get_metadata({
  fileKey: 'xxx',
  nodeId: '11:1420'
})

// 2. Extract from XML
// <frame width="1920" height="1080">
const pageWidth = 1920
const pageHeight = 1080

// 3. Use extracted values
<div className="w-[1920px] h-[1080px]">
```

### **Rule 4: Font Loading & Name Mapping**

**🔥 CRITICAL: Use Google Fonts CDN directly, NOT `next/font/google`!**

`next/font/google` generates CSS variables and self-hosts fonts, but the font rendering may differ from reference HTML that uses Google Fonts CDN directly. This causes:
- Different character widths (text wrapping issues)
- Different optical size handling for variable fonts

#### **4.1 Font Loading (layout.tsx)**

```tsx
// ❌ WRONG: Using next/font/google
import { Source_Serif_4, Kaisei_Tokumin } from 'next/font/google'
const sourceSerif = Source_Serif_4({ subsets: ['latin'], variable: '--font-source-serif' })
// This may render fonts differently than Google Fonts CDN!

// ✅ CORRECT: Use Google Fonts CDN directly in layout.tsx
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link
          href="https://fonts.googleapis.com/css2?family=Source+Serif+4:ital,opsz,wght@0,8..60,200..900;1,8..60,200..900&family=Kaisei+Tokumin:wght@400;500;700;800&display=swap"
          rel="stylesheet"
        />
      </head>
      <body>{children}</body>
    </html>
  )
}
```

**Key:** Include `opsz` (optical size) axis for Source Serif 4 - this affects character widths!

#### **4.2 Font CSS (globals.css)**

```css
@layer utilities {
  /* Use direct font-family names, NOT CSS variables */
  .font-source-serif {
    font-family: 'Source Serif 4', serif;
  }
  .font-kaisei {
    font-family: 'Kaisei Tokumin', serif;
  }
}
```

#### **4.3 Font Name Mapping**

```typescript
// Figma MCP returns:
font-['Kaisei_Tokumin:ExtraBold',sans-serif]
font-['Source_Serif_Pro:SemiBold',sans-serif]

// ✅ Convert to Tailwind classes:
font-kaisei font-extrabold
font-source-serif font-semibold

// Font name corrections (Google Fonts 2024):
'Source Serif Pro' → 'Source Serif 4'
'Source Sans Pro' → 'Source Sans 3'
```

#### **4.4 Font Weight Mismatch Warning**

**⚠️ Figma's font weight names may NOT match CSS font-weights!**

Figma renders fonts differently than browsers. What Figma calls "Bold" might visually appear lighter than CSS `font-weight: 700`.

| Figma Weight Name | Expected CSS | May Actually Need |
|-------------------|--------------|-------------------|
| Regular | 400 | 400 |
| Medium | 500 | 500 |
| Bold | 700 | **500 or 600** (test visually!) |
| ExtraBold | 800 | **700** (test visually!) |

**Solution:** Always compare with Figma screenshot. If text looks too bold, try one weight lighter:
- `font-bold` (700) → try `font-medium` (500)
- `font-extrabold` (800) → try `font-bold` (700)

### **Rule 5: Critical CSS**

**Must add to globals.css:**

```css
body {
  overflow-x: auto; /* Allow horizontal scroll */
}

.page-container {
  min-width: max-content;  /* Prevent compression */
  display: inline-block;   /* Keep layout intact */
}
```

### **Rule 6: Replace Simple Images with CSS**

**Optimize line images:**

```tsx
// ❌ Before: Image-based line
<div className="absolute h-0 left-0 top-[100px] w-[1920px]">
  <div className="absolute inset-[-1px_0_0_0]">
    <img src={imgLine} />
  </div>
</div>

// ✅ After: CSS-based line
<div className="absolute left-0 top-[141px] w-[1920px] h-[1px] bg-[#C5CBCE] opacity-30" />
```

### **Rule 7: Inline SVG Assets**

```tsx
// ❌ Before: External image
<img src={imgVector} />

// ✅ After: Inline SVG
<svg viewBox="0 0 35 34" fill="none">
  <path d="M17.5 0L0 34..." fill="#1d262d"/>
</svg>
```

### **Rule 7.5: Remove Fixed Heights from Text Blocks**

**🔥 CRITICAL: Figma MCP outputs fixed heights for text blocks, but this causes line-wrapping issues!**

Font metrics differ between Figma's rendering and browser rendering (even with the same font family). Fixed heights can cause:
- Text overflow or clipping
- Different line counts than expected
- Layout breaks when font rendering differs slightly

```tsx
// ❌ WRONG: Figma MCP output with fixed height
<p className="absolute h-[72px] leading-[1.8] left-[100px] text-[20px] top-[570px] w-[1096px]">
  Long text that might wrap differently in browser...
</p>

// ✅ CORRECT: Remove h-[Xpx], let text flow naturally
<div className="absolute leading-[1.8] left-[100px] text-[20px] top-[570px] w-[1096px]">
  <p className="mb-0">Long text that might wrap differently in browser...</p>
</div>
```

**When to keep fixed heights:**
- Container elements (cards, boxes) - keep dimensions
- Table rows with single-line content - keep `h-[34px]`
- Images and icons - keep dimensions

**When to remove fixed heights:**
- Multi-line text paragraphs - ALWAYS remove `h-[Xpx]`
- Text blocks with `text-justify` - especially important
- Any text that could wrap differently

**Pattern: Use `<div>` wrapper with `<p className="mb-0">`:**
```tsx
// This matches reference HTML structure and ensures proper text flow
<div className="absolute font-source-serif leading-[1.8] left-[100px] text-[20px] top-[570px] w-[1096px]">
  <p className="mb-0">Text content here...</p>
</div>
```


## Extended Reference

Detailed material starting at `### **Rule 8: Table Pattern Detection & Conversion**` has been moved to [`reference/extended.md`](reference/extended.md) to keep this skill concise. Load that reference when the task requires the moved examples, command catalogs, checklists, platform details, or implementation templates.
