---
name: web-basics
description: >
  HTML, CSS, and how browsers work. Activated when Claude creates or edits .html or .css files.
  Provides teaching context for CodeSensei to explain web fundamentals.
---

# Web Basics — CodeSensei Teaching Module

## HTML
- **Analogy:** HTML is the skeleton of a webpage. It defines the structure — where the heading goes, where the paragraph goes, where the image goes. Like the blueprint of a house showing where rooms are.
- **Key insight:** HTML uses "tags" that come in pairs: `<tag>content</tag>`. The tag tells the browser what KIND of content it is.
- **Key tags to teach:**
  - `<h1>` to `<h6>` — headings (h1 is the biggest, like a newspaper headline)
  - `<p>` — paragraph (a block of text)
  - `<a>` — link (a door to another page)
  - `<img>` — image (a picture on the wall)
  - `<div>` — container (a box that groups things together)
  - `<form>` — form (like a paper form you fill out)
  - `<button>` — a clickable button
- **Quiz idea:** "If you wanted to add a clickable link to Google, which tag would you use?"

## CSS
- **Analogy:** CSS is the paint, wallpaper, and furniture of the house. HTML says "there's a heading here," CSS says "make it blue, centered, and 32px big."
- **Key insight:** CSS works by SELECTING an HTML element and then STYLING it. It's always: "who are you targeting?" + "what should they look like?"
- **Key concepts:**
  - Selectors (which elements to style)
  - Properties (what to change: color, size, position)
  - Values (the specific setting: red, 16px, center)
  - Classes (reusable style labels, like "VIP" or "highlighted")
- **Quiz idea:** "If the text is too small, which file would you change — the HTML or the CSS?"

## How Browsers Work
- **Analogy:** A browser is like a translator + artist. It reads your HTML (the instructions), applies your CSS (the design specs), and paints the result on screen.
- **Key insight:** When someone visits your site, the browser downloads your files and assembles them in real-time. That's why you see the page "load."
- **Teaching flow:** User types URL → Browser requests files from server → Server sends HTML/CSS/JS → Browser assembles and displays the page

## The Relationship
```
HTML = Structure (what's on the page)
CSS  = Style (how it looks)
JS   = Behavior (what it does)
```
Think of it as: HTML is the house frame, CSS is the interior design, JavaScript is the electricity and plumbing that makes things work.
