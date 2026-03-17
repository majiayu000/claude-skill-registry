---
name: documentation-screenshots
description: Capture browser screenshots and add them to documentation. Use this skill when asked to "add screenshots to docs", "capture screenshots for documentation", "take screenshots of the dashboard", "replace TODO screenshots", or any task involving browser screenshot capture and documentation image embedding.
---

# Documentation Screenshots

Workflow for capturing browser screenshots and embedding them in documentation.

## Before Taking Screenshots

**Hide browser automation UI elements** before capturing:

1. **Claude tab group banner** - Click the X on "Claude is active in this tab group" notification
2. **Extension popups** - Close any browser extension UI
3. **DevTools** - Close developer tools if open
4. **Tooltips/notifications** - Wait for transient UI to disappear

This ensures clean, professional screenshots for documentation.

## Prettier MDX Parser Configuration

**Critical**: Docusaurus uses MDX which requires JSX comment syntax `{/* */}`. Prettier's default markdown parser converts this to `{/_ _/}`, breaking the build.

Add this override to `.prettierrc`:

```json
{
  "overrides": [
    {
      "files": "website/**/*.md",
      "options": {
        "parser": "mdx"
      }
    }
  ]
}
```

This ensures Prettier preserves `{/* TODO */}` syntax in documentation files.

## Screenshot Capture with dom-to-image

Use dom-to-image library (preferred over html2canvas for better content capture):

```javascript
(async () => {
  // Load dom-to-image if not already loaded
  if (typeof domtoimage === 'undefined') {
    await new Promise((resolve, reject) => {
      const script = document.createElement('script');
      script.src = 'https://cdnjs.cloudflare.com/ajax/libs/dom-to-image/2.6.0/dom-to-image.min.js';
      script.onload = resolve;
      script.onerror = reject;
      document.head.appendChild(script);
    });
  }

  // Wait for content to fully render
  await new Promise((r) => setTimeout(r, 500));

  // Capture and download
  const dataUrl = await domtoimage.toPng(document.body, {
    quality: 1,
    bgcolor: '#ffffff',
  });

  const link = document.createElement('a');
  link.download = 'screenshot-name.png';
  link.href = dataUrl;
  link.click();

  return 'Downloaded screenshot-name.png';
})();
```

**Important notes**:

- dom-to-image must be reloaded after each page navigation
- Wait for page content to fully load before capturing (use delay or check for elements)
- **Always verify screenshots** on the actual docs site (localhost:3000) before committing
- html2canvas may fail to capture dynamic content - use dom-to-image instead

## Workflow

1. **Plan screenshots** - Find TODO comments or identify needed screenshots
2. **Navigate systematically** - Use browser tools to visit each page/view
3. **Capture with descriptive names** - Use consistent naming (e.g., `feature-view-name.png`)
4. **Move files to static folder** - Copy from Downloads to `website/static/img/screenshots/`
5. **Update markdown files** - Replace TODOs with image embeds
6. **Commit and PR** - Create branch `docs/add-*-screenshots`

## Moving Downloaded Screenshots

```bash
# Create target directory
mkdir -p website/static/img/screenshots/getting-started/

# Move screenshots (use wildcards for batch)
cp ~/Downloads/feature-*.png website/static/img/screenshots/getting-started/
```

## Image Embed Syntax (JSX/MDX)

For Docusaurus/MDX documentation:

```jsx
<div style={{ textAlign: 'center', marginBottom: '1.5rem' }}>
  <img
    src="/img/screenshots/getting-started/screenshot-name.png"
    alt="Description"
    style={{ maxWidth: '100%', borderRadius: '8px', boxShadow: '0 4px 12px rgba(0,0,0,0.15)' }}
  />
</div>
```

## Replacing TODO Comments

Find and replace patterns:

```
// Before (old syntax)
{/_ TODO: Add screenshot - Feature Name _/}

// Before (new syntax)
{/* TODO: Add screenshot - Feature Name */}

// After
<div style={{textAlign: 'center', marginBottom: '1.5rem'}}>
  <img src="/img/screenshots/getting-started/feature-name.png" alt="Feature Name" style={{maxWidth: '100%', borderRadius: '8px', boxShadow: '0 4px 12px rgba(0,0,0,0.15)'}} />
</div>
```

## File Naming Convention

- Use kebab-case: `whatsapp-qr-code.png`
- Include section prefix: `webhooks-dashboard.png`
- Be descriptive: `webhooks-create-form.png` not `form.png`

## Git Workflow

```bash
# Create branch
git checkout -b docs/add-feature-screenshots

# Stage files
git add website/static/img/screenshots/ website/docs/

# Commit
git commit -m "docs: add screenshots to feature documentation"

# Push and create PR
git push -u origin docs/add-feature-screenshots
gh pr create --title "docs: add screenshots" --base main
```

## Handling Screenshots Requiring Specific State

Some screenshots require app state that may not be available:

- Connected services (WhatsApp paired, Slack connected)
- Existing data (webhook events, audit logs)
- External platforms (Google Cloud Console, Slack API)

Leave these as TODOs with a note, or capture from staging/demo environments when available.
