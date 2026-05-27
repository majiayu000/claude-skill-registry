---
name: catskill-preview
description: Convert markdown newsletters to styled HTML matching the Catskill Crew brand and preview in browser
---

<essential_principles>
This skill converts markdown newsletters into styled HTML pages that match the Catskill Crew aesthetic. The preview uses design elements extracted from catskillcrew.com including:
- **Colors:** Cream background (#F5EAD9), dark text (#3E3E3E), tan accents (#9A9082)
- **Fonts:** Archivo for headings and body, Courier for buttons/monospace
- **Dividers:** Hand-drawn woodcut-style animal illustrations (eagle, deer, fox, bear, rabbit, fish, owl, bird, snake)
- **Layout:** 600px max-width, generous spacing, vintage/rustic aesthetic

The preview is for visual verification before sending - it shows how the newsletter will "feel" with proper branding applied.
</essential_principles>

<intake>
Before routing, determine:

1. **What does the user want?**
   - "preview the newsletter" → Preview existing markdown
   - "convert to HTML" → Same as preview
   - "refresh design" / "update design tokens" → Re-extract from website
   - "download assets" → Re-download brand images

2. **Is there a specific file?**
   - If user specifies a file, use that
   - Otherwise, use the latest `output/newsletter_*.md`

3. **Does the user want to see it in browser?**
   - Default: Yes, open via Playwright MCP
   - If user says "just generate" → Create HTML only
</intake>

<routing>
Route to the appropriate workflow:

| User Intent | Workflow |
|-------------|----------|
| Preview newsletter / see how it looks | `workflows/preview-newsletter.md` |
| Refresh design / update styles | `workflows/extract-design.md` |
| Re-download brand assets | `workflows/download-assets.md` |
</routing>

<quick_start>
**Most common usage:** User has written a newsletter and wants to see the preview.

```
User: "preview the newsletter"
→ Route to: workflows/preview-newsletter.md
```

The workflow will:
1. Find the latest newsletter markdown in `output/`
2. Convert to HTML using the template and design tokens
3. Open in browser via Playwright MCP
4. Take a screenshot for reference
</quick_start>

<available_workflows>
## workflows/preview-newsletter.md
Convert markdown to styled HTML and open in browser. This is the primary workflow.

## workflows/extract-design.md
Re-extract design elements (colors, fonts) from catskillcrew.com using Playwright. Use when the website design has changed.

## workflows/download-assets.md
Re-download brand assets (logo, divider images) from catskillcrew.com. Use when assets need refreshing.
</available_workflows>

<references>
## references/template-structure.md
Documentation on the HTML template structure and CSS variables.
</references>

<success_criteria>
Preview is successful when:
- [ ] HTML file is generated at `output/newsletter_YYYY-MM-DD.html`
- [ ] Page opens in browser showing styled newsletter
- [ ] Colors match Catskill Crew brand (cream/tan/dark gray)
- [ ] Divider images appear between sections
- [ ] Typography feels right (Archivo font, uppercase headings)
</success_criteria>
