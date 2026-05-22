---
name: ux-usability-expert
description: Best-in-class usability designer specializing in UX principles, readability optimization, and user-centered design. Use when improving user interfaces, enhancing readability, applying accessibility standards, or when user asks about UX design, usability improvements, or text readability.
---

# UX & Usability Expert

This skill provides world-class UX design guidance with a strong focus on readability, accessibility, and user-centered design principles. Every recommendation is backed by research and proven usability standards.

## Core Philosophy

**"Design is not just what it looks like and feels like. Design is how it works."** - Steve Jobs

**"Good design is obvious. Great design is transparent."** - Joe Sparano

The UX expert follows these principles:
1. **User First**: Design for users, not designers
2. **Readability is King**: Text must be effortlessly readable
3. **Accessibility for All**: Design for everyone, including those with disabilities
4. **Cognitive Load**: Minimize mental effort required
5. **Consistency**: Predictable patterns reduce learning curve
6. **Feedback**: Users should always know what's happening

## Readability Fundamentals

### Typography Rules (Based on Research)

#### Font Size
**Minimum standards**:
- **Body text**: 16px minimum (never below 14px)
- **Mobile body text**: 16px minimum (prevents zoom on iOS)
- **Small text**: 14px minimum (for captions, footnotes)
- **Large text**: 18px+ for comfortable reading

**Science**: Studies show 16px is the optimal size for web readability. Smaller text causes eye strain and reduces comprehension by up to 30%.

```css
/* ✅ GOOD: Readable text sizes */
body {
    font-size: 16px;        /* Base readable size */
    line-height: 1.6;       /* Comfortable spacing */
}

h1 { font-size: 32px; }     /* Clear hierarchy */
h2 { font-size: 24px; }
h3 { font-size: 20px; }

small {
    font-size: 14px;        /* Still readable */
}

/* ❌ BAD: Too small */
body {
    font-size: 12px;        /* Eye strain, poor readability */
}
```

#### Line Height (Leading)
**Optimal ratios**:
- **Body text**: 1.5 to 1.8 (150% to 180%)
- **Headings**: 1.2 to 1.4
- **Short lines**: Higher line-height (1.7-1.8)
- **Long lines**: Lower line-height (1.5-1.6)

**Science**: WCAG recommends minimum 1.5 line-height. Research shows 1.6 is optimal for comprehension.

```css
/* ✅ GOOD: Comfortable reading */
body {
    line-height: 1.6;       /* 160% - optimal for most text */
}

p {
    line-height: 1.7;       /* Generous spacing for paragraphs */
    margin-bottom: 1.5em;   /* Clear paragraph separation */
}

h1, h2, h3 {
    line-height: 1.3;       /* Tighter for headings */
}

/* ❌ BAD: Cramped text */
p {
    line-height: 1.2;       /* Lines too close, hard to read */
}
```

#### Line Length (Measure)
**Optimal character count per line**:
- **Ideal**: 50-75 characters
- **Acceptable**: 45-85 characters
- **Maximum**: 90 characters
- **Mobile**: 35-50 characters

**Science**: Baymard Institute found 50-75 CPL increases reading speed by 20% and comprehension by 12%.

```css
/* ✅ GOOD: Optimal line length */
.content {
    max-width: 65ch;        /* ~65 characters per line */
    margin: 0 auto;
}

.article-text {
    max-width: 700px;       /* Comfortable reading width */
}

/* ❌ BAD: Too wide */
.content {
    max-width: 100%;        /* Lines too long, eye strain */
}
```

#### Font Weight
**Readability standards**:
- **Body text**: 400 (regular) or 450
- **Emphasis**: 500-600 (medium/semibold)
- **Headings**: 600-700 (semibold/bold)
- **Never use**: 100-200 (too light, poor contrast)

```css
/* ✅ GOOD: Clear hierarchy */
body {
    font-weight: 400;       /* Regular, readable */
}

strong, b {
    font-weight: 600;       /* Clear emphasis */
}

h1, h2, h3 {
    font-weight: 600;       /* Strong but not heavy */
}

/* ❌ BAD: Thin fonts */
body {
    font-weight: 300;       /* Too light, hard to read */
}
```

#### Letter Spacing (Tracking)
**Optimal values**:
- **Body text**: 0 to 0.03em (normal)
- **ALL CAPS**: 0.05em to 0.1em (slightly wider)
- **Headings**: -0.02em to 0.02em
- **Never**: Negative values for body text

```css
/* ✅ GOOD: Comfortable spacing */
body {
    letter-spacing: 0.01em; /* Slightly open */
}

.all-caps {
    text-transform: uppercase;
    letter-spacing: 0.08em; /* Wider for readability */
}

/* ❌ BAD: Cramped or too wide */
body {
    letter-spacing: -0.02em; /* Too tight */
}

.spaced-out {
    letter-spacing: 0.2em;   /* Too wide, slow reading */
}
```

### Font Selection

#### Best Fonts for Readability

**Sans-serif (Screen Reading)**:
1. **System fonts** (fastest, most readable):
   - `-apple-system` (macOS/iOS)
   - `BlinkMacSystemFont` (Chrome on macOS)
   - `Segoe UI` (Windows)
   - `Roboto` (Android)

2. **Web fonts** (excellent readability):
   - Inter
   - Source Sans Pro
   - Open Sans
   - Lato
   - Nunito Sans

**Serif (Long-form Reading)**:
- Georgia
- Merriweather
- Source Serif Pro
- Crimson Text

**Monospace (Code)**:
- Fira Code
- JetBrains Mono
- Consolas
- Monaco

```css
/* ✅ BEST: System font stack for maximum readability */
body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI',
                 'Roboto', 'Helvetica Neue', Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}

/* ✅ GOOD: High-quality web font */
body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* ❌ BAD: Hard-to-read fonts */
body {
    font-family: 'Lobster', cursive;      /* Decorative, poor readability */
    font-family: 'Comic Sans MS', cursive; /* Unprofessional */
    font-family: 'Impact', fantasy;        /* Low readability */
}
```

## Color & Contrast

### WCAG Contrast Standards

**Minimum requirements**:
- **AA (Minimum)**: 4.5:1 for normal text, 3:1 for large text
- **AAA (Enhanced)**: 7:1 for normal text, 4.5:1 for large text
- **Large text**: 18px+ regular or 14px+ bold

**Always aim for AA minimum, AAA when possible.**

```css
/* ✅ EXCELLENT: AAA contrast (7:1+) */
body {
    color: #1a1a1a;        /* Near black */
    background: #ffffff;   /* White */
    /* Contrast ratio: 16.1:1 */
}

/* ✅ GOOD: AA contrast (4.5:1+) */
.muted-text {
    color: #595959;        /* Medium gray */
    background: #ffffff;   /* White */
    /* Contrast ratio: 7.5:1 */
}

/* ⚠️ CAUTION: Minimum AA */
.light-text {
    color: #767676;        /* Light gray */
    background: #ffffff;   /* White */
    /* Contrast ratio: 4.54:1 - just passes */
}

/* ❌ FAILS: Below AA standard */
.fail-text {
    color: #999999;        /* Too light */
    background: #ffffff;   /* White */
    /* Contrast ratio: 2.8:1 - WCAG failure */
}
```

### Color for Meaning

**Never rely on color alone** - always provide additional indicators.

```html
<!-- ❌ BAD: Color only -->
<p style="color: red;">Error: Invalid email</p>
<p style="color: green;">Success: Form submitted</p>

<!-- ✅ GOOD: Icon + color + text -->
<p class="error">
    <span class="icon" aria-label="Error">⚠️</span>
    <strong>Error:</strong> Invalid email address
</p>

<p class="success">
    <span class="icon" aria-label="Success">✓</span>
    <strong>Success:</strong> Form submitted successfully
</p>
```

### Color Blindness Considerations

**8% of men and 0.5% of women** have color vision deficiency.

**Safe color combinations**:
- Blue + Orange (works for all types)
- Blue + Yellow
- Black + White + Blue
- Avoid: Red + Green (most common deficiency)

```css
/* ✅ GOOD: Colorblind-safe palette */
:root {
    --color-primary: #0066cc;    /* Blue - universally visible */
    --color-success: #0066cc;    /* Blue instead of green */
    --color-warning: #ff9500;    /* Orange - visible to all */
    --color-error: #dc3545;      /* Red with icon/text context */
}

/* ❌ BAD: Problematic for colorblind users */
.success { color: #00ff00; }     /* Pure green */
.error { color: #ff0000; }       /* Pure red */
/* Red/green appear similar to colorblind users */
```

## UX Principles & Patterns

### 1. F-Pattern & Z-Pattern Reading

**F-Pattern** (for text-heavy pages):
- Users scan in an F-shape
- Most important info on left
- Headings and first words matter most

**Z-Pattern** (for minimal text):
- Users scan in a Z-shape
- Logo top-left
- CTA top-right
- Content middle
- Secondary CTA bottom-right

```html
<!-- ✅ F-Pattern Layout -->
<article class="f-pattern">
    <h1>Most Important Heading</h1>
    <p><strong>Key information</strong> at start of paragraph...</p>
    <h2>Secondary Heading</h2>
    <p><strong>Another key point</strong> in first words...</p>
</article>

<style>
.f-pattern {
    max-width: 65ch;
}

.f-pattern h1,
.f-pattern h2,
.f-pattern p strong {
    /* These get the most attention in F-pattern */
}
</style>
```

### 2. Hick's Law (Choice Paradox)

**Principle**: Time to make decision increases with number of choices.

**Rule**: Limit choices to 5-7 items maximum.

```html
<!-- ❌ BAD: Too many choices -->
<nav>
    <a href="#">Home</a>
    <a href="#">About</a>
    <a href="#">Services</a>
    <a href="#">Products</a>
    <a href="#">Solutions</a>
    <a href="#">Resources</a>
    <a href="#">Blog</a>
    <a href="#">News</a>
    <a href="#">Events</a>
    <a href="#">Support</a>
    <a href="#">Contact</a>
    <!-- 11 items - overwhelming -->
</nav>

<!-- ✅ GOOD: Grouped, limited choices -->
<nav>
    <a href="#">Home</a>
    <a href="#">About</a>
    <a href="#">Services</a>
    <a href="#">Resources</a>
    <a href="#">Contact</a>
    <!-- 5 items - easy to scan -->
</nav>
```

### 3. Fitts's Law (Target Size)

**Principle**: Time to reach target depends on distance and size.

**Minimum touch targets**:
- **Mobile**: 44x44px minimum (Apple), 48x48px (Google)
- **Desktop**: 32x32px minimum for clickable elements
- **Spacing**: 8px minimum between targets

```css
/* ✅ GOOD: Properly sized touch targets */
.btn {
    min-height: 44px;
    min-width: 44px;
    padding: 12px 24px;
    margin: 8px;
}

.mobile-nav-item {
    min-height: 48px;       /* Easy to tap */
    padding: 12px 16px;
}

/* ❌ BAD: Too small to tap reliably */
.tiny-button {
    height: 20px;
    width: 20px;
    padding: 2px;
    /* Frustrating on mobile */
}
```

### 4. Miller's Law (Cognitive Load)

**Principle**: Average person can hold 7±2 items in working memory.

**Application**: Group information into 5-9 chunks.

```html
<!-- ❌ BAD: Too many ungrouped items -->
<ul>
    <li>Item 1</li>
    <li>Item 2</li>
    <li>Item 3</li>
    <!-- ... 15 items total - overwhelming -->
    <li>Item 15</li>
</ul>

<!-- ✅ GOOD: Chunked into categories -->
<div class="grouped-list">
    <h3>Category A</h3>
    <ul>
        <li>Item 1</li>
        <li>Item 2</li>
        <li>Item 3</li>
    </ul>

    <h3>Category B</h3>
    <ul>
        <li>Item 4</li>
        <li>Item 5</li>
        <li>Item 6</li>
    </ul>
</div>
```

### 5. Jakob's Law

**Principle**: Users prefer your site to work like other sites they know.

**Application**: Follow established patterns.

```html
<!-- ✅ GOOD: Standard patterns -->
<header>
    <div class="logo">Brand</div>      <!-- Logo left -->
    <nav>Menu</nav>                     <!-- Nav center/right -->
    <button class="login">Login</button><!-- Account right -->
</header>

<!-- ❌ BAD: Unconventional layout -->
<header>
    <button class="login">Login</button><!-- Confusing placement -->
    <nav>Menu</nav>
    <div class="logo">Brand</div>      <!-- Logo on right? -->
</header>
```

### 6. Progressive Disclosure

**Principle**: Show only what's necessary, reveal more as needed.

```html
<!-- ✅ GOOD: Progressive disclosure -->
<div class="form-section">
    <h3>Basic Information</h3>
    <!-- Essential fields visible -->
    <input type="text" name="name" placeholder="Name">
    <input type="email" name="email" placeholder="Email">

    <details>
        <summary>Advanced Options</summary>
        <!-- Optional fields hidden by default -->
        <input type="text" name="company" placeholder="Company">
        <input type="text" name="phone" placeholder="Phone">
    </details>
</div>

<!-- ❌ BAD: All fields at once -->
<form>
    <!-- 20 fields shown immediately - overwhelming -->
</form>
```

## Accessibility (A11y) Best Practices

### Semantic HTML

**Always use semantic elements** - they provide meaning to screen readers.

```html
<!-- ✅ EXCELLENT: Semantic HTML -->
<header>
    <nav aria-label="Main navigation">
        <ul>
            <li><a href="#home">Home</a></li>
            <li><a href="#about">About</a></li>
        </ul>
    </nav>
</header>

<main>
    <article>
        <h1>Article Title</h1>
        <p>Content...</p>
    </article>

    <aside aria-label="Related articles">
        <h2>Related</h2>
    </aside>
</main>

<footer>
    <p>&copy; 2026 Company</p>
</footer>

<!-- ❌ BAD: Div soup -->
<div class="header">
    <div class="nav">
        <div class="item">Home</div>
        <div class="item">About</div>
    </div>
</div>

<div class="content">
    <div class="article">...</div>
</div>
```

### ARIA Labels

**Use ARIA when HTML semantics aren't enough.**

```html
<!-- ✅ GOOD: Descriptive ARIA -->
<button aria-label="Close dialog">
    <span aria-hidden="true">×</span>
</button>

<input
    type="search"
    aria-label="Search products"
    placeholder="Search...">

<nav aria-label="Breadcrumb">
    <ol>
        <li><a href="/">Home</a></li>
        <li><a href="/products">Products</a></li>
        <li aria-current="page">Item</li>
    </ol>
</nav>

<!-- Icons with meaning -->
<span class="icon" aria-label="Warning">⚠️</span>
<span class="icon" aria-label="Success">✓</span>

<!-- Decorative icons hidden from screen readers -->
<span aria-hidden="true">🎨</span>
```

### Keyboard Navigation

**All interactive elements must be keyboard accessible.**

```css
/* ✅ GOOD: Visible focus indicators */
a:focus,
button:focus,
input:focus {
    outline: 3px solid #0066cc;
    outline-offset: 2px;
}

/* NEVER remove focus outline without replacement */
:focus {
    outline: none; /* ❌ NEVER do this alone */
}

/* ✅ If you must remove default, provide better alternative */
:focus {
    outline: none;
    box-shadow: 0 0 0 3px rgba(0, 102, 204, 0.5);
}

/* ✅ Skip to main content link */
.skip-link {
    position: absolute;
    top: -40px;
    left: 0;
    background: #000;
    color: #fff;
    padding: 8px;
    text-decoration: none;
    z-index: 100;
}

.skip-link:focus {
    top: 0;
}
```

```html
<!-- ✅ Skip link for keyboard users -->
<a href="#main-content" class="skip-link">
    Skip to main content
</a>

<main id="main-content">
    <!-- Content -->
</main>
```

### Alt Text

**Every image needs appropriate alt text.**

```html
<!-- ✅ GOOD: Descriptive alt text -->
<img
    src="product.jpg"
    alt="Blue ceramic coffee mug with white handle">

<!-- ✅ Decorative image -->
<img
    src="decorative-line.png"
    alt=""
    role="presentation">

<!-- ✅ Complex image with description -->
<figure>
    <img
        src="chart.png"
        alt="Bar chart showing sales growth">
    <figcaption>
        Sales increased from $10k in Q1 to $50k in Q4.
    </figcaption>
</figure>

<!-- ❌ BAD: Missing or poor alt text -->
<img src="product.jpg">              <!-- No alt -->
<img src="product.jpg" alt="image">  <!-- Not descriptive -->
<img src="product.jpg" alt="product.jpg"> <!-- Filename not helpful -->
```

## Form Design & Usability

### Form Best Practices

```html
<!-- ✅ EXCELLENT: Accessible, usable form -->
<form class="accessible-form">
    <!-- Clear fieldset grouping -->
    <fieldset>
        <legend>Personal Information</legend>

        <!-- Proper label association -->
        <div class="form-group">
            <label for="full-name">
                Full Name
                <span class="required" aria-label="required">*</span>
            </label>
            <input
                type="text"
                id="full-name"
                name="full-name"
                required
                aria-required="true"
                aria-describedby="name-help"
                autocomplete="name">
            <small id="name-help" class="help-text">
                Enter your first and last name
            </small>
        </div>

        <!-- Error state -->
        <div class="form-group error">
            <label for="email">
                Email Address
                <span class="required" aria-label="required">*</span>
            </label>
            <input
                type="email"
                id="email"
                name="email"
                required
                aria-required="true"
                aria-invalid="true"
                aria-describedby="email-error"
                autocomplete="email">
            <span id="email-error" class="error-message" role="alert">
                <span aria-hidden="true">⚠️</span>
                Please enter a valid email address
            </span>
        </div>
    </fieldset>

    <!-- Clear submit button -->
    <button type="submit" class="btn btn-primary">
        Submit Form
    </button>
</form>

<style>
.form-group {
    margin-bottom: 24px;
}

.form-group label {
    display: block;
    margin-bottom: 8px;
    font-weight: 600;
    color: #1a1a1a;
}

.form-group input {
    width: 100%;
    padding: 12px 16px;
    font-size: 16px;         /* Prevent iOS zoom */
    border: 2px solid #d1d1d1;
    border-radius: 4px;
    transition: border-color 0.2s;
}

.form-group input:focus {
    outline: none;
    border-color: #0066cc;
    box-shadow: 0 0 0 3px rgba(0, 102, 204, 0.1);
}

.form-group.error input {
    border-color: #dc3545;
}

.error-message {
    display: block;
    margin-top: 8px;
    color: #dc3545;
    font-size: 14px;
}

.help-text {
    display: block;
    margin-top: 4px;
    color: #666;
    font-size: 14px;
}

.required {
    color: #dc3545;
}
</style>
```

### Input Types & Autocomplete

**Use appropriate input types** for better mobile experience.

```html
<!-- ✅ GOOD: Proper input types -->
<input type="email" autocomplete="email">
<input type="tel" autocomplete="tel">
<input type="url" autocomplete="url">
<input type="number" inputmode="numeric">
<input type="date">
<input type="search" autocomplete="off">

<!-- Autocomplete for common fields -->
<input type="text" autocomplete="name">
<input type="text" autocomplete="given-name">
<input type="text" autocomplete="family-name">
<input type="text" autocomplete="street-address">
<input type="text" autocomplete="postal-code">
<input type="text" autocomplete="country">
```

## Responsive Design Principles

### Mobile-First Approach

```css
/* ✅ GOOD: Mobile-first */
/* Base styles for mobile */
.container {
    padding: 16px;
    font-size: 16px;
}

/* Enhance for larger screens */
@media (min-width: 768px) {
    .container {
        padding: 32px;
        font-size: 18px;
    }
}

@media (min-width: 1024px) {
    .container {
        padding: 48px;
        max-width: 1200px;
        margin: 0 auto;
    }
}
```

### Touch-Friendly Spacing

```css
/* ✅ GOOD: Touch-friendly */
.mobile-menu-item {
    min-height: 48px;
    padding: 12px 16px;
    margin-bottom: 8px;     /* Space between tap targets */
}

.mobile-button {
    min-height: 44px;
    min-width: 44px;
    padding: 12px 24px;
}
```

## Content Hierarchy

### Visual Hierarchy

**Use size, weight, color, and spacing** to create clear hierarchy.

```css
/* ✅ EXCELLENT: Clear hierarchy */
h1 {
    font-size: 32px;
    font-weight: 700;
    color: #1a1a1a;
    margin-bottom: 16px;
    line-height: 1.2;
}

h2 {
    font-size: 24px;
    font-weight: 600;
    color: #2a2a2a;
    margin-top: 32px;
    margin-bottom: 12px;
    line-height: 1.3;
}

p {
    font-size: 16px;
    font-weight: 400;
    color: #4a4a4a;
    line-height: 1.6;
    margin-bottom: 16px;
}

.caption {
    font-size: 14px;
    color: #666;
    line-height: 1.5;
}
```

## Loading States & Feedback

### Always Provide Feedback

```html
<!-- ✅ GOOD: Clear loading states -->
<button class="btn" aria-busy="false">
    Submit Form
</button>

<!-- When loading -->
<button class="btn btn-loading" aria-busy="true" disabled>
    <span class="spinner" aria-hidden="true"></span>
    <span>Submitting...</span>
</button>

<!-- Success state -->
<button class="btn btn-success" disabled>
    <span aria-hidden="true">✓</span>
    <span>Submitted!</span>
</button>

<style>
.btn {
    position: relative;
    transition: all 0.2s;
}

.btn-loading {
    opacity: 0.7;
    cursor: wait;
}

.spinner {
    display: inline-block;
    width: 16px;
    height: 16px;
    border: 2px solid rgba(255,255,255,0.3);
    border-top-color: white;
    border-radius: 50%;
    animation: spin 0.6s linear infinite;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

.btn-success {
    background: #28a745;
}
</style>
```

## Error Prevention & Recovery

### Helpful Error Messages

```html
<!-- ❌ BAD: Vague error -->
<span class="error">Invalid input</span>

<!-- ✅ GOOD: Specific, helpful error -->
<span class="error" role="alert">
    <strong>Email format error:</strong>
    Please enter a valid email address (example: user@domain.com)
</span>

<!-- ✅ EXCELLENT: Error with suggestion -->
<span class="error" role="alert">
    <strong>Password too weak:</strong>
    Your password must contain at least:
    <ul>
        <li>8 characters</li>
        <li>One uppercase letter</li>
        <li>One number</li>
    </ul>
</span>
```

## Performance & UX

### Perceived Performance

```html
<!-- ✅ Skeleton loading (better than spinners) -->
<div class="skeleton-card" aria-busy="true" aria-label="Loading content">
    <div class="skeleton-image"></div>
    <div class="skeleton-text"></div>
    <div class="skeleton-text short"></div>
</div>

<style>
.skeleton-card {
    padding: 20px;
    background: white;
    border-radius: 8px;
}

.skeleton-image,
.skeleton-text {
    background: linear-gradient(
        90deg,
        #f0f0f0 25%,
        #e0e0e0 50%,
        #f0f0f0 75%
    );
    background-size: 200% 100%;
    animation: loading 1.5s infinite;
}

.skeleton-image {
    height: 200px;
    margin-bottom: 16px;
    border-radius: 4px;
}

.skeleton-text {
    height: 16px;
    margin-bottom: 12px;
    border-radius: 4px;
}

.skeleton-text.short {
    width: 60%;
}

@keyframes loading {
    0% { background-position: 200% 0; }
    100% { background-position: -200% 0; }
}
</style>
```

## Micro-interactions

### Enhance UX with Subtle Animations

```css
/* ✅ Smooth, purposeful transitions */
.card {
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 16px rgba(0,0,0,0.1);
}

.button {
    transition: background-color 0.2s ease, transform 0.1s ease;
}

.button:hover {
    background-color: #0052a3;
}

.button:active {
    transform: scale(0.98);
}

/* Respect user preferences */
@media (prefers-reduced-motion: reduce) {
    *,
    *::before,
    *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
    }
}
```

## Usability Checklist

### Essential Checks

**Readability**:
- [ ] Body text minimum 16px
- [ ] Line height 1.5-1.8 for body text
- [ ] Line length 50-75 characters
- [ ] Color contrast minimum 4.5:1 (AA)
- [ ] Readable font family (system or web font)

**Accessibility**:
- [ ] All images have alt text
- [ ] Form inputs have labels
- [ ] Focus indicators visible
- [ ] Keyboard navigation works
- [ ] ARIA labels where needed
- [ ] Semantic HTML used
- [ ] Color not sole indicator
- [ ] Headings in logical order (h1→h2→h3)

**Touch Targets**:
- [ ] Minimum 44x44px on mobile
- [ ] 8px spacing between targets
- [ ] Buttons clearly tappable

**Forms**:
- [ ] Labels above inputs
- [ ] Input type matches content
- [ ] Autocomplete enabled
- [ ] Clear error messages
- [ ] Error prevention (validation)

**Feedback**:
- [ ] Loading states shown
- [ ] Success/error confirmations
- [ ] Hover states on interactive elements
- [ ] Disabled states clearly indicated

**Content**:
- [ ] Clear hierarchy (headings, size, weight)
- [ ] Short paragraphs (3-5 sentences)
- [ ] Scannable content (headings, lists, bold)
- [ ] Clear call-to-actions

## Implementation Example

### Before (Poor UX):
```html
<div class="page">
    <div class="title">Login</div>
    <div class="box">
        <div>Email</div>
        <input type="text">
        <div>Password</div>
        <input type="text">
        <div class="btn">Submit</div>
    </div>
</div>

<style>
.page { font-family: Arial; font-size: 12px; }
.title { font-size: 14px; }
input { height: 20px; font-size: 11px; }
.btn { background: red; color: pink; padding: 2px; }
</style>
```

### After (Excellent UX):
```html
<main class="login-page">
    <h1>Welcome Back</h1>

    <form class="login-form" aria-label="Login form">
        <div class="form-group">
            <label for="email">Email Address</label>
            <input
                type="email"
                id="email"
                name="email"
                autocomplete="email"
                required
                aria-required="true"
                placeholder="you@example.com">
        </div>

        <div class="form-group">
            <label for="password">Password</label>
            <input
                type="password"
                id="password"
                name="password"
                autocomplete="current-password"
                required
                aria-required="true">
        </div>

        <button type="submit" class="btn btn-primary">
            Sign In
        </button>
    </form>
</main>

<style>
.login-page {
    max-width: 400px;
    margin: 0 auto;
    padding: 48px 24px;
}

h1 {
    font-size: 32px;
    font-weight: 600;
    color: #1a1a1a;
    margin-bottom: 32px;
    line-height: 1.2;
}

.login-form {
    background: white;
    padding: 32px;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.form-group {
    margin-bottom: 24px;
}

.form-group label {
    display: block;
    margin-bottom: 8px;
    font-size: 16px;
    font-weight: 600;
    color: #2a2a2a;
}

.form-group input {
    width: 100%;
    padding: 12px 16px;
    font-size: 16px;
    line-height: 1.5;
    border: 2px solid #d1d1d1;
    border-radius: 4px;
    transition: border-color 0.2s;
}

.form-group input:focus {
    outline: none;
    border-color: #0066cc;
    box-shadow: 0 0 0 3px rgba(0,102,204,0.1);
}

.btn-primary {
    width: 100%;
    padding: 14px 24px;
    font-size: 16px;
    font-weight: 600;
    color: white;
    background: #0066cc;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.2s;
    min-height: 48px;
}

.btn-primary:hover {
    background: #0052a3;
}

.btn-primary:focus {
    outline: none;
    box-shadow: 0 0 0 3px rgba(0,102,204,0.3);
}

.btn-primary:active {
    transform: scale(0.98);
}
</style>
```

## Remember

- **Readability First**: 16px+ font, 1.6 line-height, 50-75ch line length
- **Accessibility Always**: WCAG AA minimum, keyboard navigation, ARIA labels
- **User Feedback**: Loading states, error messages, success confirmations
- **Touch-Friendly**: 44x44px minimum, 8px spacing
- **Cognitive Load**: Limit choices, chunk information, clear hierarchy
- **Test with Users**: Real users find real problems
- **Iterate**: Good UX is never finished

---

*"Good design is as little design as possible."* - Dieter Rams
