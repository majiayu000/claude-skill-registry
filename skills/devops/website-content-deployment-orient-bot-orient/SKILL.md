---
name: website-content-deployment
description: Complete workflow for deploying website content changes (documentation, legal pages, blog posts) including creating custom React pages, updating Docusaurus config, local testing with dev server, and understanding the rapid deployment process for website-only changes via GitHub Actions
---

# Website Content Deployment

This skill covers the complete workflow for creating and deploying website content changes to orient.bot using Docusaurus. Use this skill when adding documentation, custom pages (privacy, terms, about, etc.), blog posts, or updating site configuration.

## Quick Reference

### Common Tasks

```bash
# Start local dev server
cd website && npm run start
# Visit http://localhost:3000

# Production build test
cd website && npm run build && npm run serve

# Deploy changes
git add website/ && git commit -m "docs(website): description"
git push origin main
# Deployment completes in ~2-3 minutes
```

## Website Structure

```
website/
├── docs/              # Documentation markdown files
│   ├── getting-started/
│   ├── features/
│   └── ...
├── src/
│   ├── pages/         # Custom React pages
│   │   ├── index.tsx  # Homepage
│   │   ├── privacy.tsx
│   │   └── terms.tsx
│   └── css/           # Custom styles
├── static/            # Static assets (images, files)
├── docusaurus.config.ts  # Site configuration
├── sidebars.ts        # Documentation navigation
└── package.json
```

## Creating Custom React Pages

Custom pages are React components in `website/src/pages/` that become routes automatically.

### File Naming Convention

- `src/pages/privacy.tsx` → `/privacy` route
- `src/pages/terms.tsx` → `/terms` route
- `src/pages/about.tsx` → `/about` route
- `src/pages/contact.tsx` → `/contact` route

### Basic Page Template

```tsx
import React from 'react';
import Layout from '@theme/Layout';
import styles from './privacy.module.css'; // Shared CSS module

export default function YourPage(): JSX.Element {
  return (
    <Layout title="Page Title" description="Meta description for SEO">
      <div className={styles.legalPage}>
        <header className={styles.header}>
          <h1>Page Heading</h1>
          <p className={styles.lastUpdated}>Last Updated: January 22, 2026</p>
        </header>

        <div className={styles.content}>
          <h2>Section Title</h2>
          <p>Content here...</p>

          <div className={styles.highlightBox}>
            <p>
              <strong>TL;DR:</strong> Quick summary...
            </p>
          </div>
        </div>
      </div>
    </Layout>
  );
}
```

### Creating Shared CSS Modules

For pages with similar styling (e.g., legal pages), use a shared CSS module:

**`src/pages/legal.module.css`:**

```css
.legalPage {
  max-width: 800px;
  margin: 0 auto;
  padding: 4rem 2rem;
}

.header {
  margin-bottom: 3rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid var(--ifm-color-emphasis-300);
}

.header h1 {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
}

.lastUpdated {
  color: var(--ifm-color-emphasis-600);
  font-size: 0.9rem;
}

.content {
  line-height: 1.8;
}

.highlightBox {
  background-color: var(--ifm-color-emphasis-100);
  border-left: 4px solid var(--ifm-color-primary);
  padding: 1.5rem;
  margin: 2rem 0;
  border-radius: 0.375rem;
}

/* Dark mode support */
html[data-theme='dark'] .highlightBox {
  background-color: rgba(255, 255, 255, 0.05);
}

/* Responsive design */
@media (max-width: 768px) {
  .legalPage {
    padding: 2rem 1rem;
  }
  .header h1 {
    font-size: 2rem;
  }
}
```

Then import and use in multiple pages:

```tsx
import styles from './legal.module.css';
```

## Updating Docusaurus Config

### Adding Footer Links

Edit `website/docusaurus.config.ts` to add navigation links:

```typescript
footer: {
  style: 'light',
  links: [
    {
      title: 'Documentation',
      items: [
        { label: 'Getting Started', to: '/docs/getting-started' },
        { label: 'Features', to: '/docs/features' },
      ],
    },
    {
      title: 'Legal',  // New section
      items: [
        { label: 'Privacy Policy', to: '/privacy' },
        { label: 'Terms & Conditions', to: '/terms' },
        {
          label: 'MIT License',
          href: 'https://github.com/orient-bot/orient/blob/main/LICENSE'
        },
      ],
    },
  ],
  copyright: `Copyright © ${new Date().getFullYear()} Orient.`,
},
```

### Updating Navigation Bar

```typescript
navbar: {
  title: 'Orient',
  logo: {
    alt: 'Orient Logo',
    src: 'img/logo.svg',
  },
  items: [
    { to: '/docs', label: 'Docs', position: 'left' },
    { to: '/blog', label: 'Blog', position: 'left' },
    { to: '/about', label: 'About', position: 'left' },  // Custom page
    {
      href: 'https://github.com/orient-bot/orient',
      label: 'GitHub',
      position: 'right',
    },
  ],
},
```

## Local Testing

### Development Server

```bash
cd website
npm run start
```

**What it does:**

- Starts dev server on http://localhost:3000
- Hot reload on file changes
- Shows build errors in terminal and browser

**When to use:**

- Creating new pages
- Writing documentation
- Testing navigation changes
- Iterating on content

### Production Build Test

```bash
cd website
npm run build
npm run serve
```

**What it does:**

- Creates optimized production build
- Catches build-time errors (broken links, invalid markdown)
- Serves production build on http://localhost:3000

**When to use:**

- Before deploying to production
- Verifying build succeeds
- Testing production-only features (SSR, optimization)

### Common Issues

**Issue:** `Module not found: Can't resolve '@theme/Layout'`

- **Cause:** Not running from `website/` directory
- **Fix:** `cd website && npm run start`

**Issue:** Changes not appearing

- **Cause:** Browser cache or dev server cache
- **Fix:** Hard refresh (Cmd+Shift+R) or restart dev server

**Issue:** Build succeeds but route 404s

- **Cause:** File naming or routing issue
- **Fix:** Ensure file is in `src/pages/` and exports default function

## Deployment Process

### Smart Change Detection

When you push website changes to main, the CI/CD pipeline detects website-only changes and **skips Docker image builds**, resulting in fast deployments.

**Files that trigger website-only deployment:**

- `website/docs/**` - Documentation markdown
- `website/src/**` - Custom React pages
- `website/docusaurus.config.ts` - Site config
- `website/static/**` - Static assets
- `website/sidebars.ts` - Navigation

**Deployment timeline (website-only):**

1. **Detect Changes** (~8s) - Identifies website files changed
2. **Run Tests** (~40s) - Runs test suite
3. **Deploy to Oracle Cloud** (~2min) - Syncs website files, builds site, reloads nginx

**Total time: ~2-3 minutes** (vs ~20 minutes for full application deployment)

### What Gets Deployed

```bash
# On the server (~/orient/website)
npm run build

# Nginx serves the static build from:
~/orient/website/build/

# No Docker containers are restarted
# Only nginx reloads config (if changed)
```

### Deployment Workflow

```bash
# 1. Make changes locally
cd website/src/pages
# Edit or create .tsx files

# 2. Test locally
cd ../..  # Back to website/
npm run start
# Verify at http://localhost:3000

# 3. Test production build
npm run build && npm run serve
# Verify at http://localhost:3000

# 4. Commit and push
git add website/
git commit -m "docs(website): add privacy policy page"
git push origin main

# 5. Monitor deployment
gh run list --limit 1
gh run watch --exit-status

# 6. Verify live site
# Visit https://orient.bot/privacy (or your new route)
```

### Verifying Deployment

After deployment completes:

```bash
# Check if page is accessible
curl -I https://orient.bot/privacy
# Should return HTTP 200

# View in browser
open https://orient.bot/privacy

# Check footer links appear on all pages
open https://orient.bot
# Scroll to footer, verify new links
```

## Best Practices

### Content Guidelines

**1. Use Plain Language**

- Avoid jargon unless necessary
- Write for developers, but keep it conversational
- Use examples and code snippets

**2. Structure with Headings**

- H1: Page title (one per page)
- H2: Major sections
- H3: Subsections
- Keep hierarchy logical

**3. Add TL;DR Sections**

- Use highlight boxes for quick summaries
- Put them at the top of long pages
- Make them actionable

**4. Include Last Updated Date**

- Add to page header
- Update when making significant changes
- Format: "Last Updated: Month Day, Year"

### Technical Guidelines

**1. Always Use Layout Component**

```tsx
import Layout from '@theme/Layout';

export default function Page() {
  return (
    <Layout title="..." description="...">
      {/* content */}
    </Layout>
  );
}
```

**2. Provide SEO Metadata**

```tsx
<Layout
  title="Privacy Policy"  // Shows in browser tab and search results
  description="Orient's privacy policy explains our self-hosted architecture"
>
```

**3. Use CSS Modules for Styling**

```tsx
// Good - scoped to component
import styles from './page.module.css';
<div className={styles.container}>

// Avoid - global CSS conflicts
<div className="container">
```

**4. Support Dark Mode**

```css
/* Light mode */
.highlightBox {
  background-color: var(--ifm-color-emphasis-100);
}

/* Dark mode */
html[data-theme='dark'] .highlightBox {
  background-color: rgba(255, 255, 255, 0.05);
}
```

**5. Make it Responsive**

```css
/* Desktop */
.container {
  padding: 4rem 2rem;
}

/* Mobile */
@media (max-width: 768px) {
  .container {
    padding: 2rem 1rem;
  }
}
```

## Example: Adding a Contact Page

**1. Create the page:**

`website/src/pages/contact.tsx`

```tsx
import React from 'react';
import Layout from '@theme/Layout';

export default function Contact(): JSX.Element {
  return (
    <Layout title="Contact" description="Get in touch with the Orient team">
      <div style={{ maxWidth: '800px', margin: '0 auto', padding: '4rem 2rem' }}>
        <h1>Contact Us</h1>
        <p>Have questions? Want to contribute? Here's how to reach us:</p>

        <h2>GitHub</h2>
        <ul>
          <li>
            <a href="https://github.com/orient-bot/orient/issues">Issues</a> - Bug reports and
            feature requests
          </li>
          <li>
            <a href="https://github.com/orient-bot/orient/discussions">Discussions</a> - Questions
            and community chat
          </li>
        </ul>

        <h2>Community</h2>
        <ul>
          <li>
            <a href="https://discord.gg/orient">Discord</a> - Real-time chat with the community
          </li>
        </ul>
      </div>
    </Layout>
  );
}
```

**2. Test locally:**

```bash
cd website && npm run start
# Visit http://localhost:3000/contact
```

**3. Add to navbar (optional):**

Edit `website/docusaurus.config.ts`:

```typescript
navbar: {
  items: [
    { to: '/docs', label: 'Docs', position: 'left' },
    { to: '/contact', label: 'Contact', position: 'left' },  // Add this
  ],
}
```

**4. Deploy:**

```bash
git add website/
git commit -m "docs(website): add contact page"
git push origin main
```

**5. Verify:**

```bash
# After ~2-3 minutes
curl -I https://orient.bot/contact
open https://orient.bot/contact
```

## Troubleshooting

### Build Errors

**Error:** `Error: Duplicate routes found`

- **Cause:** Two files creating same route (e.g., `privacy.tsx` and `privacy.md`)
- **Fix:** Remove duplicate or rename one

**Error:** `Module parse failed: Unexpected token`

- **Cause:** Syntax error in TSX file
- **Fix:** Check for unclosed tags, missing imports, or TypeScript errors

**Error:** `Cannot find module '@theme/Layout'`

- **Cause:** Missing Docusaurus dependencies
- **Fix:** `cd website && npm install`

### Deployment Issues

**Issue:** Changes not appearing on live site

- **Check:** Deployment completed successfully (`gh run list`)
- **Check:** Hard refresh browser (bypass cache)
- **Check:** Correct URL (https://orient.bot/your-page)

**Issue:** Deployment taking too long (>5 minutes)

- **Cause:** Not a website-only change (Docker images building)
- **Check:** Did you modify code outside `website/`?
- **Fix:** If unintentional, revert non-website changes

**Issue:** 404 on new page

- **Check:** File is in `website/src/pages/`
- **Check:** File exports default function
- **Check:** Production build succeeded (`npm run build`)
- **Check:** Route matches filename (`privacy.tsx` = `/privacy`)

### Style Issues

**Issue:** Styles not applying

- **Check:** CSS module imported correctly
- **Check:** className uses `styles.className` syntax
- **Check:** CSS file in same directory or properly pathed

**Issue:** Dark mode not working

- **Check:** Using CSS variables (`var(--ifm-color-*)`)
- **Check:** Dark mode overrides defined
- **Test:** Toggle dark mode in browser

## Related Skills

- **deploy-to-production**: Full deployment workflow including Docker builds
- **git-workflow**: Branch naming, commit messages, PR creation
- **documentation-screenshots**: Adding images to documentation

## Quick Command Reference

```bash
# Start dev server
cd website && npm run start

# Production build
cd website && npm run build

# Serve production build locally
cd website && npm run serve

# Check deployment status
gh run list --limit 5

# Watch deployment
gh run watch --exit-status

# Verify live site
curl -I https://orient.bot/your-page
open https://orient.bot/your-page
```

## File Checklist

When creating a new custom page:

- [ ] Create `.tsx` file in `website/src/pages/`
- [ ] Import and use `<Layout>` component
- [ ] Add title and description for SEO
- [ ] Create or reuse CSS module for styling
- [ ] Test locally with `npm run start`
- [ ] Test production build with `npm run build`
- [ ] Add navigation links if needed (config, footer)
- [ ] Commit with clear message
- [ ] Push and monitor deployment
- [ ] Verify live site works
- [ ] Check footer links on multiple pages
- [ ] Test responsive design (mobile, tablet, desktop)
- [ ] Test dark mode toggle
