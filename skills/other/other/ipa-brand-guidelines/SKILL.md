---
name: ipa-brand-guidelines
description: Applies Innovations for Poverty Action's official brand colors and typography to any sort of artifact that may benefit from having IPA's look-and-feel. Use it when brand colors or style guidelines, visual formatting, or company design standards apply.
---

# IPA's Brand Styling

## Overview

To access Innovations for Poverty Action's official brand identity and style resources, use this skill.

**Keywords**: branding, corporate identity, visual identity, post-processing, styling, brand colors, typography, IPA brand, visual formatting, visual design, writing guidelines

## Brand Guidelines

### Colors

**Primary Brand Colors:**

- **IPA Green**: `#49ac57` - Primary brand color
- **Dark Green**: `#155240` - Success states and emphasis
- **Charcoal**: `#414042` - Primary text and dark elements
- **White**: `#ffffff` - Background and light text

**Secondary Colors:**

- **Dark Blue**: `#2b4085` - Secondary accent
- **Light Blue**: `#84d0d4` - Tertiary accent
- **Red Orange**: `#f26529` - Attention and highlights
- **Secondary Gray**: `#707073` - Secondary text elements
- **Tertiary Gray**: `#C2C2C4` - Tertiary elements

**Supporting Colors:**

- **Light Grey**: `#f1f2f2` - Subtle backgrounds
- **Dark Grey**: `#c9c9c8` - Borders and dividers
- **Blue Accent**: `#ceecee` - Light backgrounds

**Categorical Colors (for data visualization):**

1. Light Blue: `#84d0d4`
2. Dark Blue: `#2b4085`
3. Red Orange: `#f26529`
4. Purple: `#be9ffa`
5. Yellow: `#f5cb57`
6. IPA Green: `#49ac57`

**Sequential Colors (for gradients and scales):**

1. IPA Green: `#49ac57`
2. `#3f9953`
3. `#35874e`
4. `#2b754a`
5. `#216345`
6. Dark Green: `#155240`

**Divergent Colors (for comparative visualizations):**

- Cool side: `#032b6c`, `#5566b0`, `#a0a9ea`
- Warm side: `#fc9757`, `#c8420a`, `#730000`

### Typography

**Official IPA Fonts:**

- **Body Text**: Arial
- **Headings**: Georgia

**Web Implementation (Google Fonts alternatives):**

- **Base Font**: Arimo (Google Fonts alternative to Arial)
- **Headings**: Gelasio (Google Fonts alternative to Georgia)
- **Monospace**: Fira Code (from Google Fonts)
- **Note**: Arimo and Gelasio are freely available Google Fonts that closely resemble IPA's official fonts and are used for consistent web availability

**Monospace Styling:**

- **Inline code**: Dark green text (`#155240`), medium weight (500)
- **Code blocks**: Dark green text on light grey background (`#f1f2f2`)

**Link Styling:**

- Color: Dark blue (`#2b4085`)
- Decoration: Underline

## Writing Guidelines

IPA follows strict writing guidelines to ensure clear, accessible, and professional communication. Key principles include:

### Core Principles

- **Keep it short and simple**: Use concise sentences averaging 15-20 words
- **Write clearly and avoid jargon**: Write for general audiences; explain technical terms on first use
- **Use active voice**: Prefer "Researchers conducted a study" over "A study was conducted"
- **Be evidence-based and objective**: Present findings neutrally without advocacy
- **Show, don't tell**: Use concrete evidence and specific examples
- **Maintain professional tone**: Avoid contractions, slang, and casual language

### Key Terminology

- ✅ Use "evaluation" instead of "experiment"
- ✅ Use "participants" or "respondents" instead of "subjects"
- ✅ Use "Low- and Middle-Income Countries (LMICs)" instead of "developing countries"
- ✅ Use "people living in poverty" instead of "poor people" or "the poor"
- ✅ Use "randomized evaluation" for general audiences instead of "RCT"
- ✅ Avoid "treatment" and "control" language - use descriptive alternatives like "enrolled in the program" vs. "did not receive the program"

### Style Standards

- Follow *Associated Press Stylebook* (56th edition)
- Use American spelling and punctuation
- Follow *Chicago Manual of Style* (17th edition) for citations
- Write out numbers one through nine; use numerals for 10 and above
- Spell out acronyms on first use: "Innovations for Poverty Action (IPA)"
- Use active voice and avoid passive constructions
- No contractions: "it is" not "it's"

For complete writing guidelines, see: `.claude/skills/ipa-brand-guidelines/references/writing_guidelines.md`

## Features

### Smart Font Application

- Applies Gelasio font to headings
- Applies Arimo font to body text
- Applies Fira Code to monospace/code elements
- Automatically loads fonts from Google Fonts
- Preserves readability and brand consistency

### Text Styling

- Headings: Gelasio font in appropriate weights
- Body text: Arimo font
- Code/monospace: Fira Code with dark green color
- Smart color selection based on background (charcoal on light, white on dark)
- Preserves text hierarchy and formatting

### Color Application

- Primary branding uses IPA Green
- Text uses charcoal for readability
- Accent colors follow categorical/sequential/divergent palettes
- Maintains visual interest while staying on-brand
- Background/foreground contrast follows accessibility standards

### Logo Integration

- Medium logo: `assets/logos/IPA-primary-color-RGB.png`
- Logo placement follows brand guidelines

## Technical Details

### Font Management

- Official IPA fonts: Arial (body text) and Georgia (headings)
- Web implementation uses Google Fonts alternatives: Arimo (resembles Arial) and Gelasio (resembles Georgia)
- Fira Code used for monospace/code elements
- Fonts loaded from Google Fonts for consistent web availability
- No local font installation required
- Fallback to system fonts (Arial, Georgia) if Google Fonts unavailable

### Color Application

- Uses RGB/hex color values for precise brand matching
- Color definitions from `assets/design-styles/light-brand.yml`
- Applied via python-pptx's RGBColor class or CSS hex values
- Maintains color fidelity across different systems
- Supports categorical, sequential, and divergent color schemes for data visualization

### Writing Style Enforcement

- Automated checks via Vale linting tool
- Style rules defined in `.vale.ini` and `styles/` directory
- Pre-commit hooks ensure compliance before committing changes
- Guidelines configurable as strict, moderate, or loose enforcement
