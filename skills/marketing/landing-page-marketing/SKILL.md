---
name: landing-page-marketing
description: Automate landing page updates and marketing asset capture following established patterns
version: 1.0.0
author: Saberloop Project
usage: |
  Use this skill for landing page and marketing tasks:
  - Capturing screenshots for landing page
  - Adding new feature cards or sections
  - Updating marketing copy and CTAs
  - Processing images for web optimization
  - Deploying landing page changes

  Examples:
  "Update landing page for new feature using the landing-page-marketing skill"
  "Capture screenshots for landing page using the landing-page-marketing skill"
  "Deploy landing page to staging using the landing-page-marketing skill"
---

# Landing Page Marketing Skill

## Overview

This skill automates the complete workflow for updating the Saberloop landing page and capturing marketing assets. It consolidates screenshot capture, image processing, HTML updates, and deployment into a standardized process.

## Landing Page Architecture

```
saberloop.com/
├── index.html          # Landing page (from ./landing/)
├── app/                # PWA application
├── app-staging/        # Staging PWA
└── [other endpoints]

./landing/
├── index.html          # Main landing page HTML
├── images/             # Landing page images (304x584 for mobile screenshots)
│   ├── demo.webm
│   ├── landing-*.png
│   └── party-demo.webm
└── [deployed to root]
```

## When to Use This Skill

Use this skill when ANY of these are true:
- [ ] Adding a new feature to showcase on landing page
- [ ] Updating marketing copy or CTAs
- [ ] Capturing new app screenshots
- [ ] Creating demo videos
- [ ] Refreshing existing screenshots after UI changes
- [ ] Deploying landing page updates

## Landing Page Sections

| Section | Location (lines) | Purpose |
|---------|------------------|---------|
| Hero | ~668-694 | Main headline, video demo, primary CTAs |
| Features | ~697-733 | Feature cards grid (6-7 cards) |
| Party Mode | ~736-759 | Dedicated party mode section |
| How It Works | ~762-788 | 4-step process explanation |
| Screenshots | ~791-803 | App screenshot gallery |
| Share Section | ~806-819 | Social sharing preview |
| CTA | ~822-848 | Final call-to-action columns |
| Footer | ~851-862 | Links and copyright |

## Complete Workflow

### Phase 1: Screenshot Capture

#### Step 1.1: Create Capture Script

**File:** `tests/e2e/capture-[feature]-screenshots.spec.js`

```javascript
import { test, expect } from '@playwright/test';
import { setupAuthenticatedState, clearSessions } from './helpers.js';

const MOBILE_VIEWPORT = { width: 375, height: 667 };
const SCREENSHOT_DIR = 'landing/images';

test.use({ viewport: MOBILE_VIEWPORT });

test.describe('Capture [Feature] Screenshots', () => {

  test('[Feature] screenshot', async ({ page }) => {
    // Setup authenticated state if needed
    await setupAuthenticatedState(page);
    await clearSessions(page);
    await page.reload();
    await page.waitForSelector('[data-testid="welcome-heading"]', { timeout: 10000 });

    // Navigate to the screen to capture
    await page.goto('/#/[route]');
    await page.waitForTimeout(500);

    // Setup the UI state (scroll, open modals, etc.)
    // ...

    // Capture screenshot
    await page.screenshot({
      path: `${SCREENSHOT_DIR}/landing-[feature-name].png`,
      fullPage: false
    });

    console.log('✓ Captured: [Feature] screenshot');
  });

});
```

#### Step 1.2: Run Capture Script

```bash
# Run with visible browser
npx playwright test tests/e2e/capture-[feature]-screenshots.spec.js --headed

# Or run all capture scripts
npm run test:e2e:capture
```

#### Step 1.3: Process Images

```bash
# Resize to landing page dimensions (304x584)
# Option 1: Using Sharp CLI
npx sharp-cli landing/images/landing-[feature].png -o landing/images/landing-[feature].png resize 304 584

# Option 2: Using ImageMagick
convert landing/images/landing-[feature].png -resize 304x584 landing/images/landing-[feature].png

# Verify file size (should be <50KB for fast loading)
ls -la landing/images/landing-[feature].png
```

### Phase 2: HTML Updates

#### Step 2.1: Add Feature Card

**Location:** Features grid in `landing/index.html` (~line 700)

```html
<!-- Add after existing feature cards -->
<div class="feature-card">
    <div class="feature-icon">[EMOJI]</div>
    <h3>[Feature Name]</h3>
    <p>[Short description - 1-2 sentences]</p>
</div>
```

**Available emojis for consistency:**
- 🧠 AI/Learning
- 🌍 Languages/Global
- 🎓 Education/Levels
- 📱 Mobile/Offline
- 🔒 Privacy/Security
- 🎉 Social/Party
- 🤖 AI Models/Tech
- ⚡ Performance
- 💰 Pricing/Value

#### Step 2.2: Update CTA Section

**Location:** CTA columns in `landing/index.html` (~line 822)

```html
<div class="cta-column">
    <h3>[Column Title]</h3>
    <ul>
        <li>[Benefit 1]</li>
        <li>[Benefit 2]</li>
        <li>[Benefit 3]</li>
        <li>[Benefit 4]</li>
    </ul>
    <a href="[URL]" class="btn btn-secondary" data-track="[tracking_id]">[Button Text]</a>
</div>
```

#### Step 2.3: Add Screenshot to Gallery

**Location:** Screenshots grid in `landing/index.html` (~line 794)

```html
<img src="images/landing-[feature].png"
     alt="[Descriptive alt text]"
     width="304" height="584"
     loading="lazy">
```

#### Step 2.4: Update Structured Data

**Location:** JSON-LD in `<head>` (~line 52)

```json
{
    "@context": "https://schema.org",
    "@type": "SoftwareApplication",
    "name": "Saberloop",
    "description": "[Updated description including new feature]",
    "featureList": [
        "AI-powered quiz generation",
        "[New feature description]",
        "Multi-language support",
        "Offline mode",
        "Party Mode multiplayer"
    ]
}
```

### Phase 3: Testing

#### Step 3.1: Local Preview

```bash
# Serve landing page locally
npx serve landing -p 8080

# Or use Python
cd landing && python -m http.server 8080
```

#### Step 3.2: Responsive Testing

Test at these breakpoints:
- Mobile: 375px (primary)
- Tablet: 768px
- Desktop: 1200px+

```bash
# Use Playwright for responsive screenshots
npx playwright test tests/e2e/capture-landing-responsive.spec.js
```

### Phase 4: Deployment

#### Step 4.1: Deploy to Staging

```bash
# Build and deploy to staging first
npm run deploy:landing -- --staging

# Staging URL: https://saberloop.com/staging/ (if configured)
# Or test via: https://saberloop.com/app-staging/
```

#### Step 4.2: Verify Staging

Checklist:
- [ ] All images load correctly
- [ ] Feature cards display properly
- [ ] CTA buttons work
- [ ] Mobile layout is correct
- [ ] No console errors
- [ ] Tracking events fire (check GA)

#### Step 4.3: Deploy to Production

```bash
# Deploy landing page to production
npm run deploy:landing

# Production URL: https://saberloop.com/
```

#### Step 4.4: Post-Deploy Verification

```bash
# Clear CDN cache if needed (depends on hosting)
# Verify in incognito/private browsing
# Test on actual mobile device
```

## Templates

### Feature Card Template

```html
<div class="feature-card">
    <div class="feature-icon">🤖</div>
    <h3>Feature Name</h3>
    <p>Brief description of the feature benefit to users. Keep it to 1-2 sentences.</p>
</div>
```

### Hero Button Template

```html
<a href="/app/" class="btn btn-primary" data-track="[tracking_id]">
    <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
        <!-- SVG path here -->
    </svg>
    Button Text
</a>
```

### Screenshot Capture Script Template

```javascript
import { test, expect } from '@playwright/test';
import { setupAuthenticatedState, clearSessions } from './helpers.js';

const MOBILE_VIEWPORT = { width: 375, height: 667 };
const SCREENSHOT_DIR = 'landing/images';

test.use({ viewport: MOBILE_VIEWPORT });

test.describe('Capture Screenshots for Landing Page', () => {

  test.beforeEach(async ({ page }) => {
    await setupAuthenticatedState(page);
    await clearSessions(page);
    await page.reload();
    await page.waitForSelector('[data-testid="welcome-heading"]', { timeout: 10000 });
  });

  test('Screenshot 1: [Description]', async ({ page }) => {
    await page.goto('/#/[route]');
    await page.waitForTimeout(500);

    // Setup UI state...

    await page.screenshot({
      path: `${SCREENSHOT_DIR}/landing-[name].png`,
      fullPage: false
    });
    console.log('✓ Captured: [Description]');
  });

});
```

## CSS Reference

### Feature Card Styles

```css
.feature-card {
    background: var(--background-light);  /* #252542 */
    padding: 32px;
    border-radius: 20px;
    text-align: center;
}

.feature-icon {
    font-size: 3rem;
    margin-bottom: 16px;
}

.feature-card h3 {
    font-size: 1.25rem;
    margin-bottom: 12px;
}

.feature-card p {
    color: var(--text-muted);  /* #a0a0b0 */
    font-size: 0.95rem;
}
```

### Button Styles

```css
.btn {
    padding: 16px 32px;
    border-radius: 50px;
    font-weight: 600;
    font-size: 1rem;
    text-decoration: none;
}

.btn-primary {
    background: var(--primary);  /* #FF6B35 */
    color: white;
}

.btn-secondary {
    background: var(--background-light);
    color: var(--text);
    border: 2px solid var(--background-light);
}
```

### Color Variables

```css
:root {
    --primary: #FF6B35;
    --primary-dark: #e55a2b;
    --background: #1a1a2e;
    --background-light: #252542;
    --text: #ffffff;
    --text-muted: #a0a0b0;
}
```

## Tracking Events

All clickable elements should have `data-track` attribute:

```html
<a href="/app/" data-track="web_app_hero">Try in Browser</a>
```

Events are automatically tracked via the script at the bottom of the landing page:

```javascript
document.addEventListener('click', function(e) {
    const trackable = e.target.closest('[data-track]');
    if (trackable && typeof gtag === 'function') {
        gtag('event', trackable.dataset.track, {
            'event_category': 'engagement',
            'event_label': trackable.dataset.track
        });
    }
});
```

## Image Specifications

| Type | Dimensions | Format | Max Size | Location |
|------|------------|--------|----------|----------|
| App Screenshot | 304x584 | PNG | 50KB | `landing/images/` |
| Demo Video | 375x667 | WebM | 500KB | `landing/images/` |
| Hero Video | 300x600 | WebM | 500KB | `landing/images/` |

## Deployment Commands

```bash
# Landing page only
npm run deploy:landing

# With staging flag (if configured)
npm run deploy:landing -- --staging

# Full app + landing
npm run deploy && npm run deploy:landing
```

## Troubleshooting

### Images Not Loading
1. Check file path is correct (relative to landing/index.html)
2. Verify file was uploaded (FTP deployment)
3. Clear browser cache
4. Check file permissions on server

### Layout Issues
1. Test at all breakpoints (375, 768, 1200)
2. Check CSS grid/flexbox rules
3. Verify image dimensions match expected
4. Check for overflow issues

### Tracking Not Working
1. Verify `data-track` attribute exists
2. Check GA is loaded (no ad blockers)
3. Verify gtag function is available
4. Check browser console for errors

## Integration with Other Skills

This skill integrates with:
- **testing-suite-management** - For E2E capture scripts
- **cicd-pipeline-management** - For deployment workflows
- **documentation-generation** - For marketing docs

## References

### Developer Guides
- [E2E Testing Guide](../../../docs/developer-guide/E2E_TESTING.md)
- [Deployment Guide](../../../docs/architecture/DEPLOYMENT.md)
- [Staging Deployment](../../../docs/developer-guide/STAGING_DEPLOYMENT.md)

### Existing Capture Scripts
- `tests/e2e/capture-landing-assets.spec.js`
- `tests/e2e/capture-playstore-screenshots.spec.js`
- `tests/e2e/capture-party-demo.spec.js`

### Previous Landing Updates
- [Epic 6: Party Mode Update](../../../docs/learning/epic06_sharing/LANDING_PAGE_PARTY_UPDATE.md)
- [Epic 11 Phase 6: Multi-Provider](../../../docs/learning/epic11_llm_support/PHASE6_MARKETING_UPDATE.md)

---

**Version:** 1.0.0
**Last Updated:** 2026-01-23
**Compatible with:** Saberloop v2.0.0+
