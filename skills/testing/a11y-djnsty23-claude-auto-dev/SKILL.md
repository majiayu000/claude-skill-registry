---
name: a11y
description: Accessibility audit and patterns - WCAG 2.1 AA compliance for React apps.
triggers:
  - a11y
  - accessibility
  - wcag
  - screen reader
allowed-tools: Bash, Read, Grep, Glob
model: opus
user-invocable: true
---

# Accessibility (WCAG 2.1 AA)

## Quick Audit

```bash
# Automated checks (catches ~30% of issues)
npx axe-core-cli http://localhost:3000

# Or in browser console
# Install axe DevTools extension → run scan
```

**Automated tools catch 30%. Manual testing catches the rest.**

## Critical Checklist

### 1. Keyboard Navigation (Most Common Failure)

```tsx
// ❌ Bad - click-only interaction
<div onClick={handleClick}>Click me</div>

// ✅ Good - keyboard accessible
<button onClick={handleClick}>Click me</button>

// ✅ Good - custom element with keyboard support
<div
  role="button"
  tabIndex={0}
  onClick={handleClick}
  onKeyDown={(e) => {
    if (e.key === 'Enter' || e.key === ' ') handleClick()
  }}
>
  Click me
</div>
```

**Test:** Tab through entire page. Can you reach and activate everything?

### 2. Focus Management

```tsx
// Dialog: trap focus inside, return on close
<Dialog onOpenChange={(open) => {
  if (!open) triggerRef.current?.focus()
}}>

// Page navigation: focus main content
useEffect(() => {
  document.getElementById('main-content')?.focus()
}, [pathname])

// Skip link (first element in body)
<a href="#main-content" className="sr-only focus:not-sr-only">
  Skip to main content
</a>
```

### 3. Color Contrast

| Element | Minimum Ratio | Enhanced |
|---------|---------------|----------|
| Normal text | 4.5:1 | 7:1 |
| Large text (18px+) | 3:1 | 4.5:1 |
| UI components | 3:1 | - |

```tsx
// ❌ Bad - low contrast
<p className="text-gray-400">Light text on white</p>

// ✅ Good - use semantic tokens with proper contrast
<p className="text-muted-foreground">Accessible muted text</p>
```

### 4. Images and Media

```tsx
// ❌ Bad
<img src="/artist.jpg" />

// ✅ Good - descriptive alt
<img src="/artist.jpg" alt="Artist profile photo of Luna performing on stage" />

// ✅ Good - decorative (skip by screen reader)
<img src="/divider.svg" alt="" role="presentation" />

// Audio/Video: always provide captions
<audio controls aria-label="Song preview: Midnight Drive">
```

### 5. Forms

```tsx
// ❌ Bad - no label
<input placeholder="Email" />

// ✅ Good - associated label
<label htmlFor="email">Email</label>
<input id="email" type="email" aria-required="true" />

// ✅ Good - error messaging
<input
  id="email"
  aria-invalid={!!errors.email}
  aria-describedby={errors.email ? "email-error" : undefined}
/>
{errors.email && (
  <p id="email-error" role="alert" className="text-destructive text-sm">
    {errors.email.message}
  </p>
)}
```

### 6. ARIA (Use Sparingly)

```tsx
// Live regions for dynamic content
<div aria-live="polite" aria-atomic="true">
  {status === 'generating' && 'Generating your song...'}
</div>

// Loading states
<button disabled={loading} aria-busy={loading}>
  {loading ? 'Saving...' : 'Save'}
</button>

// Custom components
<div role="tablist" aria-label="Song sections">
  <button role="tab" aria-selected={active === 'lyrics'}>Lyrics</button>
  <button role="tab" aria-selected={active === 'details'}>Details</button>
</div>
```

### 7. Semantic HTML

```tsx
// ❌ Bad - div soup
<div class="header"><div class="nav">...</div></div>

// ✅ Good - semantic landmarks
<header><nav aria-label="Main">...</nav></header>
<main id="main-content">
  <section aria-labelledby="songs-heading">
    <h2 id="songs-heading">Your Songs</h2>
  </section>
</main>
<footer>...</footer>
```

## Audit Report Format

```
Accessibility Audit (WCAG 2.1 AA)
──────────────────────────────────
Keyboard Navigation:  ✅ All interactive elements reachable
Focus Management:     ⚠️ Dialog doesn't trap focus
Color Contrast:       ✅ All text meets 4.5:1
Images:               ⚠️ 3 images missing alt text
Forms:                ✅ All inputs labeled
ARIA:                 ✅ Live regions for loading states
Semantic HTML:        ⚠️ Missing landmark roles

Score: 78/100
Critical: 0 | High: 1 | Medium: 2 | Low: 1
```

## Integration

| Skill | How It Integrates |
|-------|-------------------|
| `audit` | A11y agent uses these patterns |
| `standards` | A11y is part of "all UI states handled" |
| `design` | New UI must meet contrast + keyboard requirements |
| `review` | Flag a11y regressions |
