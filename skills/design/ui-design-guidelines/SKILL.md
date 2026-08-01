---
name: ui-design-guidelines
description: 'UI/UX design guidelines focusing on what AI commonly overlooks or fails
  to verify. **CRITICAL**: Emphasizes concrete checklists, measurement criteria, and
  verification steps that AI tends to skip duri'
---

---
name: ui-design-guidelines
description: UI/UX design guidelines focusing on what AI commonly overlooks or fails to verify. **CRITICAL**: Emphasizes concrete checklists, measurement criteria, and verification steps that AI tends to skip during design reviews. Reference during Phase 1 (UI/UX Design Review).
---

# UI/UX Design Guidelines - What AI Overlooks

This skill focuses on concrete verification steps AI commonly skips. Trust AI for general design principles, but scrutinize these critical areas where AI consistently fails to check.

## ⚠️ Critical: AI's Common Oversights

### 1. Generic AI Aesthetics (Most Critical - Must Check First)

**Pattern AI ALWAYS falls into**: Using predictable, "safe" design choices that create cookie-cutter interfaces

**NEVER use these AI defaults:**

#### ❌ Overused Fonts
- **Inter, Roboto, Arial** - AI's go-to choices
- **System fonts** - Lazy defaults
- **Space Grotesk** - Overused across AI generations

```tsx
// ❌ AI writes: Generic font stack
<h1 className="font-['Inter']">Heading</h1>

// ✅ Better: Distinctive, contextual fonts
<h1 className="font-['Playfair_Display']">Heading</h1>
// Use unexpected, characterful fonts that elevate aesthetics
```

#### ❌ Cliched Color Schemes
- **Purple gradients on white backgrounds** - Overused AI pattern
- **Blue-to-purple gradients** - Generic SaaS aesthetic
- **Evenly-distributed palettes** - Timid color choices

```tsx
// ❌ AI writes: Generic purple gradient
<div className="bg-gradient-to-r from-purple-500 to-blue-500">

// ✅ Better: Bold, contextual color choices
<div className="bg-amber-900 text-amber-50">
// Commit to a cohesive aesthetic with dominant colors
```

#### ❌ Predictable Layouts
- **Centered hero sections** - Default pattern
- **Three-column feature grids** - Cookie-cutter structure
- **Symmetric, safe compositions** - No visual interest

```tsx
// ❌ AI writes: Generic centered layout
<section className="container mx-auto text-center">
  <h1>Hero Title</h1>
  <div className="grid grid-cols-3 gap-4">

// ✅ Better: Unexpected, asymmetric layouts
<section className="grid grid-cols-12 gap-8">
  <div className="col-span-7 col-start-2">
// Asymmetry, overlap, diagonal flow, grid-breaking
```

#### ✅ Anti-Generic Checklist
- [ ] **Font choice is distinctive** (not Inter/Roboto/Arial)
- [ ] **Color scheme is bold** (not purple gradient on white)
- [ ] **Layout is unexpected** (not centered hero + 3-column grid)
- [ ] **Design has clear aesthetic direction** (not "safe" defaults)
- [ ] **Every detail is intentional** (not convergence on common choices)

**Key Principle**: Choose a clear conceptual direction (brutally minimal, maximalist chaos, retro-futuristic, luxury/refined, brutalist/raw, etc.) and execute with precision. Bold maximalism and refined minimalism both work - the key is **intentionality**, not intensity.

---

### 2. Accessibility Verification

**Pattern AI ALWAYS skips**: Checking actual contrast ratios and keyboard navigation after implementation

```typescript
// AI writes this and assumes it's accessible:
<button className="text-gray-400 bg-gray-100">
  Submit
</button>

// Problem: Contrast ratio is only 2.5:1 (FAILS WCAG AA requirement of 4.5:1)
// AI doesn't actually measure the contrast ratio
```

**Critical Numbers**:
- **Normal text**: 4.5:1 minimum
- **Large text** (≥18pt/≥14pt bold): 3:1 minimum
- **UI components**: 3:1 minimum
- **Touch targets**: 44x44px minimum
- **Target spacing**: 8px minimum

**Verification Tools** (AI should recommend but doesn't):
- WebAIM Contrast Checker: https://webaim.org/resources/contrastchecker/
- Chrome DevTools Lighthouse
- Keyboard navigation testing (actual manual test required)

---

### 3. Performance Measurement

**Pattern AI ALWAYS skips**: Providing actual performance verification steps

**Core Web Vitals Targets**:
- **LCP**: < 2.5s
- **FID**: < 100ms
- **CLS**: < 0.1

**Image Optimization Checklist** (AI forgets to verify):
- [ ] Next.js Image component with width/height
- [ ] `priority` for above-the-fold images
- [ ] Appropriate quality (75-90)

```tsx
// ❌ AI writes: No dimensions (causes CLS)
<img src="/hero.jpg" alt="Hero" />

// ✅ Correct: Dimensions prevent layout shift
<Image src="/hero.jpg" alt="Hero" width={1200} height={600} priority />
```

---

### 4. Responsive Testing Range

**Pattern AI ALWAYS skips**: Testing at specific breakpoints

**Required Test Range**: 375px - 1920px

**Breakpoints**:
| Name | Width | Device |
|------|-------|--------|
| `sm` | 640px | Large phones |
| `md` | 768px | Tablets |
| `lg` | 1024px | Laptops |
| `xl` | 1280px | Desktops |

**Must test at**: 375px, 640px, 768px, 1024px, 1920px

---

### 5. Animation Constraints

**Pattern AI ALWAYS skips**: Using only GPU-accelerated properties

**Rule**: Animate only `transform` and `opacity` (never width/height/position)

**Timing**:
- **Standard**: 200-300ms
- **Complex motion**: 300-500ms
- **Maximum**: 500ms

```tsx
// ❌ AI writes: Causes layout recalculation
<div className="hover:w-64 transition-all">

// ✅ Correct: GPU-accelerated
<div className="hover:scale-105 transition-transform">
```

**Accessibility**: Must respect `prefers-reduced-motion`
```tsx
<div className="motion-safe:animate-in motion-safe:fade-in">
```

---

### 6. Form Accessibility

**Pattern AI ALWAYS skips**: Proper ARIA attributes

```tsx
// ❌ AI writes: Missing ARIA
<Input className={errors.email ? 'border-red-500' : ''} />
{errors.email && <p>{errors.email}</p>}

// ✅ Correct: Proper ARIA
<Input
  id="email"
  aria-invalid={!!errors.email}
  aria-describedby={errors.email ? "email-error" : undefined}
/>
{errors.email && (
  <p id="email-error" role="alert">
    {errors.email}
  </p>
)}
```

---

### 7. Semantic HTML

**Pattern AI ALWAYS skips**: Using proper elements instead of divs

```tsx
// ❌ AI writes: Div soup
<div className="header">
  <div className="nav">
    <div className="nav-item">Home</div>
  </div>
</div>

// ✅ Correct: Semantic structure
<header>
  <nav>
    <ul>
      <li><a href="/">Home</a></li>
    </ul>
  </nav>
</header>
```

**Required Elements**:
- `<header>` for page/section headers
- `<nav>` for navigation
- `<main>` for primary content (once per page)
- `<article>` for self-contained content
- `<footer>` for page/section footers

---

### 8. Feedback Timing

**Pattern AI ALWAYS skips**: Ensuring feedback < 0.4s

**Doherty Threshold**: System must respond within 0.4 seconds

```tsx
// ❌ AI writes: No loading state
<Button onClick={handleSubmit}>Submit</Button>

// ✅ Correct: Immediate feedback
<Button disabled={isLoading}>
  {isLoading ? <Loader2 className="animate-spin" /> : "Submit"}
</Button>
```

---

## Comprehensive Verification Checklist

### Accessibility ⚠️ (Most Critical)
- [ ] **Contrast tested**: 4.5:1 (text), 3:1 (UI components)
- [ ] **Touch targets**: 44x44px minimum
- [ ] **Keyboard tested**: Full page navigation with Tab/Shift+Tab
- [ ] **Focus visible**: Clear focus ring on all interactive elements
- [ ] **Screen reader tested**: NVDA, JAWS, or VoiceOver
- [ ] **Labels associated**: All inputs have `htmlFor`/`id`
- [ ] **ARIA attributes**: `aria-invalid`, `aria-describedby` on forms
- [ ] **Semantic HTML**: `<header>`, `<nav>`, `<main>`, `<footer>`

### Performance ⚠️
- [ ] **Images**: Next.js Image with width/height
- [ ] **Priority**: Above-the-fold images have `priority` attribute
- [ ] **Lighthouse**: All scores 90+
- [ ] **LCP**: < 2.5s verified
- [ ] **CLS**: < 0.1 verified (no layout shifts)
- [ ] **Font loading**: next/font with `display: 'swap'`

### Responsive ⚠️
- [ ] **375px tested**: Minimum mobile width
- [ ] **640px tested**: sm breakpoint
- [ ] **768px tested**: md breakpoint
- [ ] **1024px tested**: lg breakpoint
- [ ] **1920px tested**: Desktop maximum
- [ ] **No overflow**: All content visible
- [ ] **Touch targets**: 44x44px+ at all breakpoints

### Animation
- [ ] **Properties**: Only `transform` and `opacity`
- [ ] **Timing**: 200-500ms maximum
- [ ] **Reduced motion**: `prefers-reduced-motion` respected
- [ ] **Performance**: No simultaneous animations on many elements

### Forms
- [ ] **Labels**: All inputs have explicit `htmlFor`/`id`
- [ ] **Errors**: `aria-describedby` points to error messages
- [ ] **Validation**: `aria-invalid` reflects status
- [ ] **Required**: `aria-required` or `required` attribute

### Feedback
- [ ] **Loading states**: All async operations show indicator
- [ ] **Button states**: disabled, loading, hover, active, focus
- [ ] **Timing**: Feedback within 0.4s
- [ ] **Optimistic updates**: Immediate UI update

---

## Quick Reference: Critical Numbers

### Contrast Ratios
- Normal text: 4.5:1
- Large text: 3:1
- UI components: 3:1

### Touch Targets
- Minimum size: 44x44px
- Spacing: 8px minimum

### Performance
- LCP: < 2.5s
- FID: < 100ms
- CLS: < 0.1
- Feedback: < 0.4s

### Animation
- Standard: 200-300ms
- Complex: 300-500ms
- Maximum: 500ms
- Properties: `transform`, `opacity` only

### Responsive
- Test range: 375px - 1920px
- Breakpoints: 640, 768, 1024, 1280

### Typography
- Base: 16px minimum
- Line height: 1.5-1.6 (body), 1.2-1.4 (headings)
- Line length: 45-75 characters (max-w-prose)

### Spacing
- Base unit: 4px or 8px
- Minimum padding: 16px (interactive elements)
- Section spacing: 32-96px

---

## Integration with Development Workflow

### Phase 1: UI/UX Design Review
- Review checklist before implementation
- Identify accessibility requirements
- Plan responsive breakpoints
- Define performance budget

### Phase 4: Browser Verification
- **Run actual tests** (don't assume)
- Measure with DevTools
- Test keyboard navigation
- Test multiple viewports
- Verify performance metrics

---

## Summary: What to Watch For

AI will confidently design UI that:
1. **Uses Inter/Roboto fonts** and **purple gradients** (generic AI aesthetics)
2. **Looks good** but **fails contrast checks** (doesn't measure)
3. **Works on desktop** but **breaks on mobile** (doesn't test breakpoints)
4. **Has forms** but **missing ARIA** (skips accessibility)
5. **Shows images** but **causes layout shift** (no dimensions)
6. **Has animations** but **animates wrong properties** (width/height instead of transform)
7. **Has buttons** but **too small for touch** (< 44x44px)

**Trust AI for**:
- Visual hierarchy concepts
- Color theory basics
- Typography principles
- General UX guidelines

**Scrutinize AI for**:
- Actual measurements (contrast, size, timing)
- Testing at breakpoints
- ARIA attribute implementation
- GPU-accelerated animation properties
- Performance metric verification

**When in doubt: "Did I actually test this with tools, or am I assuming?"**

If you didn't run Lighthouse, test keyboard navigation, verify at multiple breakpoints, or measure contrast ratios, the implementation is incomplete.
