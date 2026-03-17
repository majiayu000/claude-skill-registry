---
name: brand-guidelines
description: "Establish or analyze brand identity guidelines. Creates comprehensive brand documentation that frontend-design, testing, and other skills automatically reference for consistent execution."
---

# Brand Guidelines

## Core Principle

**Consistent brand identity across all outputs.** Establish comprehensive brand guidelines once, then automatically apply them across design, development, and testing workflows.

## Overview

This skill helps you either:
1. **Create brand guidelines** from scratch by asking strategic questions
2. **Analyze existing branding** in a project to document current state
3. **Update existing guidelines** as the brand evolves

Once established, these guidelines are automatically referenced by other skills (frontend-design, playwright-frontend-testing, etc.) to ensure brand consistency.

## When to Use This Skill

- **Starting a new project** - Establish brand identity before development
- **Rebranding** - Update guidelines for brand refresh
- **Documenting existing brand** - Analyze and codify current branding
- **Onboarding projects** - Document brand for new team members
- **Brand audit** - Review current brand consistency
- **Before design work** - Ensure frontend-design has clear guidelines

## Prerequisites

**For creating new guidelines:**
- Brand strategy or vision (if available)
- Target audience understanding
- Competitive landscape knowledge

**For analyzing existing brand:**
- Access to existing website/application
- Marketing materials (if available)
- Logo files and assets

## The Iron Laws

### 1. GUIDELINES BEFORE DESIGN

**NEVER start design work without brand guidelines established.**

❌ **FORBIDDEN sequence:**
```
Start project → Use frontend-design → Random aesthetic choices
```

✅ **REQUIRED sequence:**
```
Start project → brand-guidelines → frontend-design (with guidelines) → consistent output
```

**Authority**: 70% of brand inconsistencies stem from lack of documented guidelines.

### 2. STORE IN STANDARD LOCATION

**Brand guidelines MUST be stored at:**
- `.claude/BRAND-GUIDELINES.md` (primary file)
- `.claude/brand/` (supporting assets: color swatches, logo files, etc.)

**Why**: Consistent location allows automatic discovery by other skills.

### 3. KEEP GUIDELINES ACTIONABLE

**Guidelines must be specific and implementable:**

❌ **BAD**: "Use modern colors"
✅ **GOOD**: "Primary: #2563EB, Secondary: #7C3AED, Accent: #F59E0B"

❌ **BAD**: "Professional tone"
✅ **GOOD**: "Direct and confident. Active voice. Technical accuracy without jargon."

## Brand Guidelines Protocol

### Step 1: Announce Usage

**Template:**
```
I'm using the brand-guidelines skill to [establish/analyze/update] brand identity for this project.

This will create comprehensive guidelines at .claude/BRAND-GUIDELINES.md that other skills will automatically reference.
```

### Step 2: Choose Approach

**Option A: Create New Guidelines (Interactive Discovery)**

Ask strategic questions to establish brand identity.

**Option B: Analyze Existing Brand (Project Analysis)**

Review existing codebase, website, or materials to document current branding.

**Option C: Update Existing Guidelines**

Read `.claude/BRAND-GUIDELINES.md` and update specific sections.

## Creating New Guidelines (Interactive Discovery)

### Discovery Questions

**Identity & Positioning:**
```
1. Brand Name: What is the product/company name?
2. Tagline: Do you have a tagline or positioning statement?
3. Industry: What industry/category?
4. Target Audience: Who are your primary users/customers?
5. Brand Personality: If your brand was a person, how would you describe them?
   (Examples: Professional, Playful, Bold, Elegant, Technical, Approachable)
6. Differentiation: What makes you different from competitors?
```

**Visual Identity:**
```
7. Color Preferences: Any specific colors that represent your brand?
   - Primary color (main brand color)
   - Secondary color (supporting color)
   - Accent colors (calls-to-action, highlights)
   - Neutral colors (backgrounds, text)
   - Color meanings (why these colors?)

8. Typography Direction:
   - Display/Heading style: (Serif, Sans-serif, Geometric, Humanist, etc.)
   - Body text style: (Readability priority)
   - Technical/Monospace needs: (Code, data, technical content)
   - Character: (Modern, Classic, Playful, Professional, etc.)

9. Visual Style:
   - Minimal or Maximal?
   - Flat or Dimensional (shadows, depth)?
   - Rounded or Angular (border radius style)?
   - Photography style: (Real, Illustrations, Abstract, 3D)?
   - Icon style: (Line, Filled, Duotone)?
```

**Tone & Voice:**
```
10. Communication Style:
    - Formal or Casual?
    - Technical or Accessible?
    - Emotional or Rational?
    - Playful or Serious?

11. Brand Values: Top 3-5 values your brand embodies?
    (Examples: Innovation, Reliability, Transparency, Creativity, Speed)

12. Example Brands: Any brands whose aesthetic you admire?
    (For inspiration, not copying)
```

**Technical Constraints:**
```
13. Accessibility Requirements: WCAG level? (A, AA, AAA)
14. Browser Support: Any specific requirements?
15. Performance Priorities: Speed vs. Visual richness trade-offs?
16. Existing Assets: Logo files, brand book, style guides?
```

### Question Flow

**Use AskUserQuestion tool for efficient gathering:**

```
Ask in batches:
- Batch 1: Identity (questions 1-6)
- Batch 2: Visual Identity (questions 7-9)
- Batch 3: Communication (questions 10-12)
- Batch 4: Technical (questions 13-16)
```

## Analyzing Existing Brand (Project Analysis)

### Analysis Workflow

```
1. Scan project structure:
   - Check for existing brand documents
   - Look for style guides, design systems
   - Find logo/asset directories

2. Analyze visual implementation:
   - Extract colors from CSS/theme files
   - Identify font families in use
   - Review component patterns
   - Check spacing/sizing systems

3. Review content:
   - Analyze tone in copy
   - Check messaging consistency
   - Identify voice patterns

4. Document findings:
   - Current state documentation
   - Inconsistencies found
   - Recommendations for alignment
```

**Commands to run:**

```bash
# Find existing brand/design docs
find . -type f -name "*brand*" -o -name "*style*guide*" -o -name "*design*system*"

# Check CSS for color variables
grep -r "color\|#[0-9a-fA-F]" --include="*.css" --include="*.scss"

# Find font declarations
grep -r "font-family" --include="*.css" --include="*.scss" --include="*.js"

# Look for design tokens
find . -name "*token*" -o -name "*theme*" -o -name "*variables*"
```

## Brand Guidelines Document Structure

### Complete Template

Create `.claude/BRAND-GUIDELINES.md`:

```markdown
# Brand Guidelines: [Project Name]

**Version**: 1.0
**Last Updated**: [Date]
**Status**: Active

---

## 🎯 Brand Identity

### Name & Positioning
- **Brand Name**: [Name]
- **Tagline**: [Tagline]
- **Industry**: [Industry]
- **Target Audience**: [Primary audience description]

### Brand Personality
[Describe brand as a person - 2-3 sentences]

**Key Traits**:
- [Trait 1]
- [Trait 2]
- [Trait 3]

### Differentiation
[What makes this brand unique - 1-2 sentences]

---

## 🎨 Visual Identity

### Color Palette

**Primary Colors**:
```css
--color-brand-primary: #[HEX];        /* [Usage: Main brand color, CTAs, headers] */
--color-brand-primary-dark: #[HEX];   /* [Usage: Hover states, emphasis] */
--color-brand-primary-light: #[HEX];  /* [Usage: Backgrounds, subtle highlights] */
```

**Secondary Colors**:
```css
--color-brand-secondary: #[HEX];      /* [Usage: Supporting elements] */
--color-brand-secondary-dark: #[HEX]; /* [Usage: Contrast] */
--color-brand-secondary-light: #[HEX];/* [Usage: Backgrounds] */
```

**Accent Colors**:
```css
--color-accent-1: #[HEX];             /* [Usage: Important CTAs] */
--color-accent-2: #[HEX];             /* [Usage: Highlights, badges] */
--color-accent-3: #[HEX];             /* [Usage: Alternative actions] */
```

**Neutral Colors**:
```css
--color-neutral-black: #[HEX];        /* [Usage: Primary text] */
--color-neutral-900: #[HEX];          /* [Usage: Headings] */
--color-neutral-700: #[HEX];          /* [Usage: Body text] */
--color-neutral-500: #[HEX];          /* [Usage: Secondary text] */
--color-neutral-300: #[HEX];          /* [Usage: Borders, dividers] */
--color-neutral-100: #[HEX];          /* [Usage: Backgrounds] */
--color-neutral-white: #[HEX];        /* [Usage: White surfaces] */
```

**Semantic Colors**:
```css
--color-success: #[HEX];              /* [Usage: Success messages] */
--color-warning: #[HEX];              /* [Usage: Warnings] */
--color-error: #[HEX];                /* [Usage: Errors] */
--color-info: #[HEX];                 /* [Usage: Information] */
```

**Color Usage Rules**:
- Primary color: 60% of interface
- Secondary color: 30% of interface
- Accent colors: 10% for emphasis
- Maintain 4.5:1 contrast ratio minimum (WCAG AA)
- Never use primary on secondary without neutral buffer

### Typography

**Display/Heading Font**:
- **Family**: [Font name]
- **Weights**: [List: 700 Bold, 600 Semibold, etc.]
- **Source**: [Google Fonts/Adobe Fonts/Self-hosted]
- **Fallback**: [Fallback stack]
- **Usage**: Headings (H1-H3), Hero text, Prominent UI labels

**Body Font**:
- **Family**: [Font name]
- **Weights**: [List: 400 Regular, 500 Medium, 700 Bold]
- **Source**: [Source]
- **Fallback**: [Fallback stack]
- **Usage**: Body text, Paragraphs, Form labels, UI text

**Monospace Font** (if applicable):
- **Family**: [Font name]
- **Usage**: Code blocks, Technical data, Monospaced numbers

**Typography Scale**:
```css
--font-size-xs: 0.75rem;    /* 12px - Captions, labels */
--font-size-sm: 0.875rem;   /* 14px - Small text */
--font-size-base: 1rem;     /* 16px - Body text */
--font-size-lg: 1.125rem;   /* 18px - Large body */
--font-size-xl: 1.25rem;    /* 20px - Small headings */
--font-size-2xl: 1.5rem;    /* 24px - H3 */
--font-size-3xl: 1.875rem;  /* 30px - H2 */
--font-size-4xl: 2.25rem;   /* 36px - H1 */
--font-size-5xl: 3rem;      /* 48px - Hero */
```

**Line Heights**:
- Headings: 1.2
- Body text: 1.6
- Small text: 1.4

**Typography Rules**:
- Never use more than 2 font families
- Headings: [Display font] + [Weight]
- Body: [Body font] + Regular (400)
- Emphasis: Same font + Medium/Bold weight (not color change)

### Spacing System

```css
--space-xs: 0.25rem;   /* 4px */
--space-sm: 0.5rem;    /* 8px */
--space-md: 1rem;      /* 16px */
--space-lg: 1.5rem;    /* 24px */
--space-xl: 2rem;      /* 32px */
--space-2xl: 3rem;     /* 48px */
--space-3xl: 4rem;     /* 64px */
```

**Usage**:
- Component padding: `--space-md` to `--space-lg`
- Section spacing: `--space-2xl` to `--space-3xl`
- Element gaps: `--space-sm` to `--space-md`

### Border Radius

```css
--radius-sm: 0.25rem;   /* 4px - Subtle rounding */
--radius-md: 0.5rem;    /* 8px - Standard */
--radius-lg: 1rem;      /* 16px - Prominent */
--radius-full: 9999px;  /* Pills, circular */
```

### Shadows

```css
--shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
--shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);
--shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1);
--shadow-xl: 0 20px 25px -5px rgb(0 0 0 / 0.1);
```

### Visual Style

**Design Direction**: [Minimal/Maximal/Balanced]

**Characteristics**:
- **Shapes**: [Rounded/Angular/Mixed]
- **Depth**: [Flat/Subtle shadows/Pronounced depth]
- **Imagery**: [Photography/Illustrations/Icons/Mixed]
- **Patterns**: [Geometric/Organic/None]
- **Textures**: [Smooth/Textured/Gradients]

**Component Style**:
- Buttons: [Solid/Outlined/Ghost] with [Rounded/Square corners]
- Cards: [Flat/Elevated] with [Border/Shadow]
- Forms: [Outlined/Filled/Underlined]
- Navigation: [Solid/Transparent/Elevated]

---

## ✍️ Tone & Voice

### Voice Characteristics

**[Adjective 1] | [Adjective 2] | [Adjective 3]**

[2-3 sentence description of brand voice]

**Communication Principles**:
1. **[Principle 1]**: [Description]
2. **[Principle 2]**: [Description]
3. **[Principle 3]**: [Description]

### Writing Style

**Grammar & Structure**:
- **Person**: [First/Second/Third]
- **Tense**: [Present/Past/Future preference]
- **Active vs. Passive**: Prefer active voice
- **Sentence Length**: [Short/Medium/Varies]
- **Formality**: [Formal/Professional/Casual/Friendly]

**Word Choices**:
- ✅ **Use**: [List of preferred terms]
- ❌ **Avoid**: [List of avoided terms]

**Punctuation Style**:
- Oxford comma: [Yes/No]
- Exclamation points: [Frequent/Occasional/Rare]
- Em dashes: [Yes/No]

### Content Examples

**Headlines**:
- ✅ Good: "[Example headline]"
- ❌ Bad: "[Counter-example]"

**Body Copy**:
- ✅ Good: "[Example paragraph]"
- ❌ Bad: "[Counter-example]"

**Call-to-Action**:
- ✅ Good: "[Example CTA]"
- ❌ Bad: "[Counter-example]"

**Error Messages**:
- ✅ Good: "[Example error message]"
- ❌ Bad: "[Counter-example]"

---

## 🎭 Brand Values

1. **[Value 1]**: [How it manifests in design/content]
2. **[Value 2]**: [How it manifests in design/content]
3. **[Value 3]**: [How it manifests in design/content]

---

## 🚫 Brand Don'ts

**Visual**:
- ❌ Don't [specific visual anti-pattern]
- ❌ Don't [specific visual anti-pattern]
- ❌ Don't [specific visual anti-pattern]

**Content**:
- ❌ Don't [specific content anti-pattern]
- ❌ Don't [specific content anti-pattern]
- ❌ Don't [specific content anti-pattern]

---

## ♿ Accessibility Standards

**Target**: WCAG [A/AA/AAA]

**Requirements**:
- Contrast ratio: Minimum [4.5:1 / 7:1]
- Focus indicators: Visible on all interactive elements
- Alternative text: All images must have descriptive alt text
- Keyboard navigation: Full keyboard accessibility
- Screen reader: ARIA labels on all interactive components
- Color alone: Never rely solely on color to convey information

---

## 🔧 Technical Implementation

### CSS Variables Export

Copy this into your global CSS:

```css
:root {
  /* Colors */
  --color-brand-primary: #[HEX];
  /* ... (full variable list) */

  /* Typography */
  --font-heading: '[Font]', sans-serif;
  /* ... */

  /* Spacing */
  --space-md: 1rem;
  /* ... */
}
```

### Framework Integration

**Tailwind Config**:
```js
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        brand: {
          primary: '#[HEX]',
          // ...
        },
      },
      fontFamily: {
        heading: ['[Font]', 'sans-serif'],
        body: ['[Font]', 'sans-serif'],
      },
    },
  },
};
```

**Styled Components Theme**:
```js
export const theme = {
  colors: {
    brand: {
      primary: '#[HEX]',
      // ...
    },
  },
  fonts: {
    heading: "'[Font]', sans-serif",
    body: "'[Font]', sans-serif",
  },
};
```

---

## 📋 Usage Instructions for AI Skills

**For frontend-design skill**:
- Read this file before generating any UI components
- Apply color palette from Visual Identity section
- Use typography system exactly as specified
- Follow visual style guidelines for all design decisions
- Never override colors/fonts without explicit user request

**For playwright-frontend-testing skill**:
- Verify brand colors are implemented correctly
- Check typography matches specifications
- Validate accessibility standards are met
- Test component styles match brand guidelines

**For content generation**:
- Follow tone & voice guidelines
- Use approved word choices
- Match communication style
- Apply content examples as templates

---

## 🔄 Version History

### Version 1.0 - [Date]
- Initial brand guidelines created
- [List key decisions made]

---

**Last Review**: [Date]
**Next Review**: [Date + 6 months]
```

## Skill Integration

### How Other Skills Use Guidelines

**Automatic Discovery**:
1. Skills check for `.claude/BRAND-GUIDELINES.md` at project start
2. If found, read and apply guidelines automatically
3. If not found, proceed with skill defaults

**frontend-design Integration**:
```
When frontend-design skill starts:
1. Check if .claude/BRAND-GUIDELINES.md exists
2. If yes: Read color palette, typography, visual style sections
3. Apply brand colors instead of creating new palette
4. Use brand fonts instead of suggesting alternatives
5. Match visual style (minimal/maximal, rounded/angular, etc.)
```

**playwright-frontend-testing Integration**:
```
When testing visual elements:
1. Read brand guidelines for expected values
2. Verify colors match brand palette
3. Check typography matches specifications
4. Validate spacing/sizing matches system
5. Report deviations as test failures
```

## Best Practices

### 1. Start Early
Create guidelines before any design or development work.

### 2. Be Specific
Use exact hex codes, font names, and sizing values.

### 3. Include Examples
Show good and bad examples for clarity.

### 4. Update Regularly
Review and update guidelines every 6 months.

### 5. Version Control
Track changes to guidelines in git.

### 6. Test Application
Verify skills correctly use guidelines after creation.

## Common Patterns

### Pattern 1: New Project Setup
```
1. Use brand-guidelines skill (interactive discovery)
2. Answer all discovery questions
3. Review generated BRAND-GUIDELINES.md
4. Commit to version control
5. Use frontend-design skill (auto-applies guidelines)
```

### Pattern 2: Existing Project Documentation
```
1. Use brand-guidelines skill (analyze mode)
2. Scan project for colors/fonts/patterns
3. Document current state
4. Identify inconsistencies
5. Create guidelines based on best patterns found
6. Fix inconsistencies in subsequent work
```

### Pattern 3: Brand Refresh
```
1. Read existing .claude/BRAND-GUIDELINES.md
2. Use brand-guidelines skill (update mode)
3. Modify specific sections (colors, typography, etc.)
4. Update version number
5. Document changes in version history
6. Apply new guidelines across project
```

## Troubleshooting

### Guidelines Not Being Applied

**Check:**
1. File exists at `.claude/BRAND-GUIDELINES.md`
2. File is properly formatted markdown
3. CSS variables are valid
4. Skills explicitly mention reading guidelines

**Solution:**
```
Explicitly tell skills to use guidelines:
"Use the frontend-design skill, and apply the brand guidelines from .claude/BRAND-GUIDELINES.md"
```

### Inconsistent Application

**Cause**: Vague guidelines

**Solution**: Make guidelines more specific with exact values

### Guidelines Too Restrictive

**Solution**: Add "flexibility" section allowing creative interpretation within bounds

## Remember

**Brand guidelines are living documents.**

- Start with core essentials (colors, typography, tone)
- Add detail as brand matures
- Update based on real usage patterns
- Balance consistency with creative flexibility
- Make guidelines easy to follow

**Authority**: 75% of brand recognition comes from consistent visual application.

---

**Resources:**
- [Anthropic - Package Brand Guidelines](https://website.claude.com/resources/use-cases/package-your-brand-guidelines-in-a-skill)
- [Brand Style Guide Examples](https://www.canva.com/learn/50-meticulous-style-guides-every-startup-see-launching/)
