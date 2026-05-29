---
name: learning-multi-script-design
description: Design learning materials for right-to-left languages, complex scripts, bidirectional text, and multi-script environments. Calculate text expansion factors and specify typography requirements. Use when creating content for Arabic, Hebrew, Asian scripts, or mixed-direction text. Activates on "RTL", "right-to-left", "bidirectional text", or "complex scripts".
---

# Learning Multi-Script Design

Design educational materials that properly handle multiple writing systems, right-to-left languages, and complex scripts.

## When to Use

- Creating content for RTL languages (Arabic, Hebrew, Farsi/Persian, Urdu)
- Supporting complex scripts (Devanagari, Thai, Myanmar, Khmer)
- Mixed-direction content (English + Arabic)
- Asian language learning materials
- Global multilingual platforms

## Script Categories

### 1. Right-to-Left (RTL) Languages

**Major RTL Languages**:
- Arabic (and variants)
- Hebrew
- Farsi/Persian
- Urdu
- Pashto
- Yiddish

**Design Considerations**:
- UI elements flip horizontally
- Reading direction: right to left
- Numbers may remain LTR
- Mixed text creates bidirectional (bidi) challenges

### 2. Complex Scripts

**Characteristics**:
- **Devanagari** (Hindi, Sanskrit, Marathi): Combining characters, ligatures
- **Thai**: No spaces between words, tone marks above/below
- **Myanmar**: Circular vowels, stacking
- **Khmer**: Multi-level stacking, no word boundaries
- **Tamil, Telugu, Malayalam**: Complex conjuncts

**Technical Requirements**:
- Unicode support
- Complex text layout (CTL) engines
- Proper font rendering
- Line breaking algorithms

### 3. East Asian Scripts

**CJK (Chinese, Japanese, Korean)**:
- Vertical and horizontal text
- Character spacing
- Ruby annotation (furigana)
- Mixed scripts (kanji, hiragana, katakana, romaji)

### 4. Bidirectional Text

**Challenges**:
- Embedding LTR text in RTL (e.g., English words in Arabic)
- Punctuation placement
- Number handling
- URL and code directionality

## Text Expansion Factors

**Translation Length Changes**:
| Source | Target | Expansion Factor |
|--------|--------|------------------|
| English | Arabic | +25% to +30% |
| English | German | +10% to +35% |
| English | Chinese | -20% to -30% |
| English | Spanish | +15% to +30% |
| English | Thai | +15% to +20% |

**Design Implications**:
- Button/label sizing
- Form field lengths
- Line breaks and pagination
- UI layout flexibility

## Typography Requirements

### Font Selection

**Requirements by Script**:
- **Arabic**: Must support contextual forms (initial, medial, final, isolated)
- **Devanagari**: Must include conjuncts and ligatures
- **Thai**: Requires tone mark positioning
- **CJK**: Large character sets (20,000+ glyphs)

**Web Safe Options**:
- Arabic: Noto Naskh Arabic, Arial Arabic
- Hebrew: Noto Sans Hebrew, Arial Hebrew
- Devanagari: Noto Sans Devanagari
- CJK: Noto Sans CJK

### Line Height and Spacing

**Adjustments Needed**:
- **Thai/Devanagari**: +20-30% line height for marks above/below
- **Arabic**: Account for ascenders and descenders
- **CJK**: 1.5-2x character height for vertical text

## Layout Considerations

### RTL Layout Changes

**Elements That Flip**:
- ✓ Navigation menus
- ✓ Breadcrumbs
- ✓ Progress indicators
- ✓ Carousels and sliders
- ✗ Video player controls (stay LTR)
- ✗ Mathematical formulas (stay LTR)

### Form Design

**RTL Forms**:
- Labels on right side
- Input fields align right
- Validation messages on left
- Calendar widgets flip

## Technical Implementation

### HTML/CSS

```html
<!-- Document direction -->
<html dir="rtl" lang="ar">

<!-- Mixed direction -->
<p>This is English text: <span dir="rtl">هذا نص عربي</span></p>

<!-- Bidirectional isolation -->
<bdi>User-generated content</bdi>
```

```css
/* RTL-specific styles */
[dir="rtl"] .navigation {
  text-align: right;
  direction: rtl;
}

/* Logical properties (auto-flip) */
.container {
  padding-inline-start: 20px; /* becomes right in RTL */
  margin-inline-end: 10px;     /* becomes left in RTL */
}
```

## CLI Interface

```bash
# RTL language design
/learning.multi-script-design --content "course.html" --target-lang "Arabic" --direction "RTL"

# Calculate expansion
/learning.multi-script-design --source "English course" --target-langs "Arabic,German,Russian" --estimate-expansion

# Complex script requirements
/learning.multi-script-design --content "app-ui/" --scripts "Devanagari,Thai,Myanmar" --output design-spec.md

# Typography recommendations
/learning.multi-script-design --languages "Arabic,Hebrew,Farsi" --recommend-fonts --web-safe
```

## Output

- Layout specifications for target scripts
- Text expansion estimates
- Font recommendations
- CSS/HTML directives
- Design mockups for RTL
- Bidirectional text handling guide

## Composition

**Input from**: `/learning.translation`, `/curriculum.package-web`, `/curriculum.package-pdf`
**Works with**: `/learning.localization-engineering`, `/learning.global-accessibility`
**Output to**: Multi-script ready designs and layouts

## Exit Codes

- **0**: Multi-script design complete
- **1**: Unsupported script
- **2**: Insufficient font resources
- **3**: Bidirectional conflicts
