---
name: seo-fundamentals
description: |
  TRIGGERS: "SEO check", "will this rank?", "meta tags", "search optimization", "Google",
  "adding meta", "page title", "search ranking", "Next.js page", "building page",
  "head section", "og:image", "social sharing", "sitemap", "robots.txt",
  SEO, meta description, title tags, Open Graph, semantic HTML, sitemap, structured data.
  USE WHEN: Junior is BUILDING pages, adding meta tags, or working on public-facing content.
  PROVIDES: Meta tag standards, semantic HTML patterns, Open Graph setup, SEO best practices.
  PROACTIVE: Triggers when junior mentions building pages or public-facing features.
---

# SEO Fundamentals Review

> "Good SEO is good UX. If search engines can't understand your page, users might not find it."

## When to Apply

Activate this skill when:
- Reviewing HTML `<head>` sections
- Seeing meta tags in code
- Next.js/Remix page components
- HTML structure with headings
- Any page that should be indexed

---

## The SEO Checklist

### Must Have (Every Page)

- [ ] **Title tag** — 50-60 characters, unique per page
- [ ] **Meta description** — 150-160 characters, compelling
- [ ] **Single H1** — One per page, describes main content
- [ ] **Logical heading hierarchy** — H1 → H2 → H3 (no skipping)
- [ ] **Semantic HTML** — `<header>`, `<main>`, `<nav>`, `<article>`, `<footer>`
- [ ] **Image alt text** — Descriptive, not "image1.jpg"

### Should Have (Marketing Pages)

- [ ] **Open Graph tags** — og:title, og:description, og:image
- [ ] **Twitter Card** — twitter:card, twitter:title
- [ ] **Canonical URL** — Prevent duplicate content issues
- [ ] **Structured data** — JSON-LD for rich snippets

### Performance (Affects SEO)

- [ ] **Core Web Vitals awareness**
  - LCP (Largest Contentful Paint) < 2.5s
  - FID (First Input Delay) < 100ms
  - CLS (Cumulative Layout Shift) < 0.1

---

## Common Mistakes (Anti-Patterns)

### 1. Multiple H1 Tags

```html
<!-- ❌ BAD: Multiple H1s confuse search engines -->
<h1>Welcome</h1>
<h1>Our Products</h1>
<h1>Contact Us</h1>

<!-- ✅ GOOD: One H1, logical hierarchy -->
<h1>Welcome to Our Store</h1>
<h2>Our Products</h2>
<h2>Contact Us</h2>
```

### 2. Missing Alt Text

```html
<!-- ❌ BAD: Empty or useless alt -->
<img src="hero.jpg" alt="">
<img src="team.jpg" alt="image">

<!-- ✅ GOOD: Descriptive alt text -->
<img src="hero.jpg" alt="Software engineer working at laptop">
<img src="team.jpg" alt="Our founding team of 5 engineers">
```

### 3. Div Soup (No Semantic HTML)

```html
<!-- ❌ BAD: No semantic meaning -->
<div class="header">
  <div class="nav">...</div>
</div>
<div class="content">...</div>
<div class="footer">...</div>

<!-- ✅ GOOD: Semantic HTML -->
<header>
  <nav>...</nav>
</header>
<main>...</main>
<footer>...</footer>
```

### 4. Skipping Heading Levels

```html
<!-- ❌ BAD: Jumps from H1 to H4 -->
<h1>Page Title</h1>
<h4>Some Section</h4>

<!-- ✅ GOOD: Sequential hierarchy -->
<h1>Page Title</h1>
<h2>Main Section</h2>
<h3>Subsection</h3>
```

### 5. Generic Title Tags

```html
<!-- ❌ BAD: Not descriptive -->
<title>Home</title>
<title>Page</title>

<!-- ✅ GOOD: Descriptive with keywords -->
<title>Daniel Lamb - Full Stack Developer Portfolio</title>
<title>Contact Us | Acme Software Solutions</title>
```

---

## Socratic Questions

Ask these instead of giving answers:

1. **Title**: "If someone sees this title in Google results, would they click it?"
2. **H1**: "How many H1 tags does this page have? What happens if there are multiple?"
3. **Alt Text**: "If the image doesn't load, what information is lost?"
4. **Semantic HTML**: "Can a screen reader understand the structure of this page?"
5. **Meta Description**: "Does this description make you want to click?"

---

## Stack-Specific Guidance

### Next.js (App Router)

```tsx
// Pattern: Metadata export
export const metadata = {
  title: 'Page Title',
  description: 'Page description',
  // Your implementation will differ
};
```

### Next.js (Pages Router)

```tsx
// Pattern: Next Head
import Head from 'next/head';

<Head>
  <title>Your title here</title>
  <meta name="description" content="Your description" />
</Head>
```

### Plain HTML/React

```html
<!-- In index.html or via react-helmet -->
<head>
  <title>Title here</title>
  <meta name="description" content="Description here">
</head>
```

---

## Red Flags to Call Out

| Flag | Question |
|------|----------|
| Missing title tag | "What will this page show in search results?" |
| Multiple H1s | "Which heading is the main topic? Search engines are confused." |
| No meta description | "How will Google summarize this page?" |
| Empty alt text | "What if the image doesn't load? What info is lost?" |
| All divs, no semantics | "Can a screen reader navigate this page?" |
| Title over 60 chars | "This will be cut off in search results. Can you shorten it?" |

---

## Open Graph Template

```html
<!-- Minimum viable Open Graph -->
<meta property="og:title" content="Your Page Title">
<meta property="og:description" content="Your page description">
<meta property="og:image" content="https://yoursite.com/og-image.jpg">
<meta property="og:url" content="https://yoursite.com/page">
<meta property="og:type" content="website">
```

---

## Interview Connection

> "I implemented SEO best practices including semantic HTML, proper heading hierarchy, and meta tags, improving our page's discoverability."

When reviewing their code:
- "What's your SEO strategy for this page?"
- "How would Google understand what this page is about?"
- "Show me your heading structure"

---

## MCP Usage

### Context7 - Framework Docs
```
Fetch: Next.js metadata documentation
Fetch: Semantic HTML best practices
```

### Octocode - Real Examples
```
Search: "metadata" + "title" + "description" in Next.js repos
Search: Open Graph implementation patterns
```
