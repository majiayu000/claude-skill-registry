---
name: apply-ppf
description: Apply PPF (Pension Protection Fund) brand identity derived from 2024/25 publications. Use for PPF governance documents, consultation responses, board papers, and any PPF-branded outputs.
allowed-tools: Read, Write, Glob, Bash, Edit
context: fork
agent: general-purpose
model: claude-sonnet-4-20250514
---

# apply-ppf

Apply the PPF (Pension Protection Fund) brand identity to documents and interfaces.

**Designation:** External / PPF-Branded Documents

## Brand Reference

**IMPORTANT**: Always read the brand specification first:
```
~/.45black/brand/PPF.md
```

This file contains the authoritative colour values, typography, design patterns, and implementation code (python-docx + CSS). Do NOT use hardcoded values from this skill - always reference the brand file.

## When To Use

- Creating PPF governance framework documents
- PPF board papers or committee reports
- PPF consultation responses (e.g. DWP consultations)
- PPF-branded presentations or analysis documents
- Any document that should look like it came from the PPF
- User mentions: "apply ppf", "ppf brand", "ppf style", "ppf colours"

## When NOT To Use

- For 45Black internal products (use `/apply-saville`)
- For trustee-facing products generally (use `/apply-trustee`)
- For LGPS or USS documents (different brands)

## Colour Quick Reference

| Name | Hex | Usage |
|------|-----|-------|
| **PPF Purple** | `#5B2D8E` | Covers, title bars, primary brand |
| **PPF Blue** | `#0072BC` | Headings, links, section headers |
| **PPF Teal** | `#00B2A9` | Accents, statutory references |
| **PPF Pink** | `#C51A7D` | Highlights, warnings |
| **PPF Green** | `#00875A` | Positive indicators, recommendations |
| **PPF Charcoal** | `#3D4F5F` | Subheadings, body headings |
| **Body Text** | `#333333` | Primary body copy |
| **Font** | Arial | All text |

## Workflow

### 1. Read Brand Specification
```bash
cat ~/.45black/brand/PPF.md
```
Extract current palette, typography, and design patterns.

### 2. Determine Output Type

| Output | Approach |
|--------|----------|
| **Word document (.docx)** | Use python-docx with PPF constants from brand spec |
| **Web/HTML** | Use CSS custom properties from brand spec |
| **Presentation** | Use python-pptx with PPF palette |

### 3. Apply Title Page (Word Documents)

The PPF title page follows this structure:
1. Full-width **PPF Purple** header bar with white "Pension Protection Fund" wordmark
2. Document title in PPF Purple, centred
3. Subtitle in PPF Blue
4. Teal accent line (representing the PPF arc/swoosh motif)
5. Metadata in tertiary text

### 4. Apply Typography
- Font: **Arial** (system-available, matches PPF's clean sans-serif)
- H1: PPF Blue, bold, 22-28pt
- H2: PPF Charcoal, bold, 16-20pt
- H3: PPF Blue or Teal, bold, 13-14pt
- Body: #333333, regular, 10-11pt
- Statutory references: PPF Teal, italic, 8pt

### 5. Apply Table Styles
- Header rows: PPF Blue background, white text
- Alternating rows: white / light gray (#F5F5F5)
- Borders: thin, light gray

### 6. Apply Callout Boxes

| Type | Background | Border |
|------|-----------|--------|
| Quote/Key Point | Light Blue | PPF Blue |
| Evidence | Light Teal | PPF Teal |
| Recommendation | Light Green | PPF Green |
| Warning | Light Pink | PPF Pink |
| Highlight | Light Purple | PPF Purple |

### 7. Apply Tone of Voice
- Professional yet approachable
- Member-centric ("our members", "people's futures")
- First person plural ("We", "Our")
- Plain English, explains technical terms

### 8. Verify Accessibility
- WCAG AA contrast ratios (4.5:1 minimum)
- PPF Purple on white: 7.8:1 (AAA)
- PPF Blue on white: 4.6:1 (AA)
- Touch targets: 44px minimum

## Key Design Patterns

### Two-Tone Section Headings
```
[Light weight text]
[Bold coloured keyword]
```
Example: "An unwavering commitment **to our members**"

### PPF Arc/Swoosh
Curved accent element. In documents, represent as a thin coloured accent line (teal or pink).

### People Photography
PPF publications feature real members, staff, and stakeholders prominently. Use warm, inclusive imagery.

### ICARE Values
Integrity, Collaboration, Accountability, Respect, Excellence — all styled in PPF Pink.

## Mapping from Trustee Edition

If converting an existing Trustee Edition document to PPF brand:

| Trustee Edition | PPF Brand | Notes |
|----------------|-----------|-------|
| Governance Blue (#1A4F7A) | **PPF Blue (#0072BC)** | Brighter, more vibrant |
| Neutral Slate (#455A64) | **PPF Charcoal (#3D4F5F)** | Slightly warmer |
| Trustee Teal (#00695C) | **PPF Teal (#00B2A9)** | Much brighter, vivid |
| Fiduciary Green (#2E7D32) | **PPF Green (#00875A)** | Shifted toward teal |
| Advisory Amber (#F57C00) | **PPF Pink (#C51A7D)** | Amber replaced by pink |
| Inter font | **Arial** | System-available |
| n/a | **PPF Purple (#5B2D8E)** | New primary for covers |

## Quality Gates

Before completion, verify:
- [ ] Brand spec file was read (`~/.45black/brand/PPF.md`)
- [ ] PPF Purple used for cover/title area
- [ ] PPF Blue used for main headings
- [ ] Teal accent line present (not blue separator)
- [ ] Arial font throughout
- [ ] Table headers use PPF Blue background
- [ ] Callout boxes use correct tint/border pairings
- [ ] Statutory references in PPF Teal italic
- [ ] WCAG AA contrast ratios pass
- [ ] No Trustee Edition colours remaining (#1A4F7A, #455A64, #00695C, #F57C00)

## Model Preference

**sonnet** - Design implementation is procedural, not reasoning-heavy

---
*References ~/.45black/brand/PPF.md for authoritative values*
*Derived from PPF publications 2024-2026 (ppf.co.uk)*
