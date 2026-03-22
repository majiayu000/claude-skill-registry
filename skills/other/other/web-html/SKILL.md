---
name: web-html
cluster: web-dev
description: "HTML5: semantic markup, ARIA/WCAG accessibility, forms, Web Components, Shadow DOM, SEO"
tags: ["html","accessibility","semantic","web"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "html5 semantic accessibility aria forms web components shadow dom"
---

## Purpose
This skill enables OpenClaw to generate, edit, and optimize HTML5 code, focusing on semantic markup for structure, ARIA and WCAG compliance for accessibility, form handling, Web Components for encapsulation, Shadow DOM for styling isolation, and SEO techniques like meta tags and structured data.

## When to Use
Apply this skill when building web pages requiring accessible, semantic HTML, such as creating e-commerce product pages with ARIA roles or dynamic forms in single-page apps. Use it for SEO-heavy content like blog posts or when integrating custom Web Components to avoid global style conflicts.

## Key Capabilities
- Generate semantic HTML: Create elements like `<main>` or `<article>` for better readability and SEO. Example: Use `<header role="banner">` for accessible site headers.
- Implement ARIA/WCAG: Add attributes like `aria-label="Search"` to elements for screen reader support, ensuring WCAG 2.1 AA compliance.
- Handle forms: Build forms with required attributes, e.g., `<input type="email" required aria-invalid="false">`, including validation hooks.
- Create Web Components: Define custom elements with Shadow DOM, e.g., `<my-component>` encapsulating internal HTML and styles.
- Optimize for SEO: Insert meta tags like `<meta name="description" content="Page description">` and use headings for keyword placement.
Code snippet:
```html
<section aria-labelledby="sec-title">
  <h2 id="sec-title">Section Heading</h2>
  <p>Content with SEO keywords.</p>
</section>
```

## Usage Patterns
Invoke this skill via OpenClaw's CLI or API by specifying the skill ID ("web-html") and action parameters. For generation tasks, provide JSON configs; for edits, supply target HTML strings. Pattern 1: Use CLI for quick prototypes. Pattern 2: Chain with other skills, e.g., pass output to a CSS skill. Always include accessibility flags for WCAG compliance. Example pattern: `openclaw execute web-html --action generate --params '{"type": "page", "features": ["semantic", "aria"]}'` to produce structured code.

## Common Commands/API
- CLI Commands: Use `openclaw execute web-html --action <action> --params <JSON>`, where actions include "generate", "enhance", or "validate". For example, `openclaw execute web-html --action generate --params '{"elements": ["form"], "accessible": true}'` generates an accessible form. Include flags like `--debug` for verbose output or `--validate` to check WCAG compliance.
- API Endpoints: POST to `https://api.openclaw.ai/skills/web-html` with a JSON body, e.g., `{"action": "generate", "params": {"type": "component", "shadowDom": true}}`. Set header `Authorization: Bearer $OPENCLAW_API_KEY` for authentication. Response format: JSON with "code" (HTML string) and "errors" array.
Code snippet:
```json
{
  "action": "enhance",
  "target": "<div>Original HTML</div>",
  "params": {"addAria": true}
}
```
Use this to enhance existing HTML with ARIA attributes.

## Integration Notes
Integrate by piping outputs to other skills, e.g., use web-html output as input for web-css. Config format: JSON objects, e.g., `{"accessibility": true, "seoTags": ["description", "keywords"]}`. For Web Components, ensure compatibility by wrapping in Shadow DOM; example: Combine with web-js skill via `openclaw chain web-html web-js --input <html-code>`. If using env vars, set `$OPENCLAW_API_KEY` for API calls and handle dependencies like Node.js for local Web Component testing.

## Error Handling
Common errors: Invalid HTML (e.g., missing closing tags) returns HTTP 400 with message like "Syntax error in element"; ARIA misuse (e.g., invalid role) triggers 422 with details. Handle by checking response.status; if >=400, parse the "errors" array for specifics. For CLI, use `--retry 3` flag to attempt fixes, e.g., `openclaw execute web-html --action generate --params {...} --retry 3`. Code snippet for error checking:
```javascript
if (response.errors.length > 0) {
  console.error(response.errors[0].message); // e.g., "Missing aria-label"
  retryAction();
}
```
Always validate inputs with WCAG rules before execution.

## Concrete Usage Examples
1. Generate a semantic HTML page with SEO: Run `openclaw execute web-html --action generate --params '{"structure": "basic", "seo": true, "accessibility": true}'`. This produces a full HTML document like:
   ```html
   <!DOCTYPE html>
   <html lang="en">
     <head><meta name="description" content="SEO description"></head>
     <body><main aria-label="Main content">Content here</main></body>
   </html>
   ```
   Use this for quick prototyping of accessible web pages.

2. Enhance a form with ARIA for accessibility: First, provide a base form string, then execute `openclaw execute web-html --action enhance --target '<form><input type="text"></form>' --params '{"addAria": true}'`. Output:
   ```html
   <form aria-label="User Form">
     <label for="input1">Label:</label>
     <input id="input1" type="text" aria-required="true">
   </form>
   ```
   This ensures WCAG compliance for form elements in existing code.

## Graph Relationships
- Related Skills: web-css (for styling generated HTML), web-js (for scripting Web Components)
- In Cluster: web-dev
- Connected Tags: html, accessibility, semantic, web
- Dependencies: Requires web-dev cluster for full functionality
