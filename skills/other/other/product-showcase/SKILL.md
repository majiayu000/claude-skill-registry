---
name: product-showcase
description: "Generate a marketing website that shows off a web app using real screenshots. Browses the running app, captures key screens, extracts features, and produces a single deployable HTML showcase page with hero, how-it-works, feature grid, and CTAs. Like a landing page but built FROM the actual product. Triggers: 'showcase site', 'product page', 'show off the app', 'marketing site from app', 'demo page', 'product showcase', 'app showcase'."
compatibility: claude-code-only
---

# Product Showcase Generator

Generate a marketing website that shows off a running web app. Unlike the `landing-page` skill (which works from a brief), this skill **explores the actual app** via browser automation, captures real screenshots, discovers features, and builds a showcase page from what the product actually does.

## How It Differs from `landing-page`

| `landing-page` | `product-showcase` |
|---------------|--------------------|
| Works from a text brief | Works from a running app |
| Placeholder images | Real screenshots from the app |
| User describes features | Features discovered by browsing |
| No browser automation | Requires browser automation |
| Generic marketing structure | Structured around app's actual workflows |

## Depth Levels

| Depth | Sections | Screenshots | Duration |
|-------|----------|------------|----------|
| **quick** | Hero + feature grid (3-4 features) | 5-6 screenshots | 15-20 min |
| **standard** | Hero + how-it-works + feature grid + CTA | 10-15 screenshots | 30-45 min |
| **thorough** | All sections including dark mode, keyboard shortcuts, before/after, integrations | 20-30 screenshots, both light/dark | 1-2 hours |

Default: **standard**

## Browser Tool Detection

Before starting, detect available browser tools:

1. **Chrome MCP** (`mcp__claude-in-chrome__*`) — preferred for authenticated apps
2. **Playwright MCP** (`mcp__plugin_playwright_playwright__*`) — for public apps
3. **playwright-cli** — for scripted flows

## Workflow

### 1. Gather Input

| Field | Required | Example |
|-------|----------|---------|
| App URL | Yes | `https://app.example.com` or `http://localhost:5173` |
| App name | Yes | "Acme CRM" |
| Tagline | No | "The CRM that gets out of your way" |
| Target audience | No | "Small business owners" |
| Pricing info | No | Free tier, $29/mo pro |
| CTA text + URL | No | "Start Free Trial" → signup page |
| Testimonials | No | User provides or skip section |

### 2. Explore the App

Navigate the app and capture the story:

#### a. First Impression
- Load the app's main page/dashboard
- Screenshot at 1280x720 — this becomes the hero image
- Note the immediate value proposition (what does the user see first?)

#### b. Discover Features
Navigate through each major section:
- Click every nav item, tab, and major UI element
- For each feature area, take a clean screenshot showing it in action
- Note what the user can DO (actions, not just views)
- Capture 6-10 key screens that tell the product story

#### c. Identify the "How It Works" Flow
Find the main workflow (the thing a user does most):
- Screenshot 3-4 steps in sequence
- These become the "How It Works" section
- Example: "1. Add a contact → 2. Set up a pipeline → 3. Track your deals → 4. See your dashboard"

#### d. Capture Detail Shots
For the feature grid, capture focused screenshots:
- Zoom into specific UI elements that showcase polish
- Dark mode version if available (shows design quality)
- Mobile view if the app is responsive

#### e. Capture Both Modes
If the app has dark mode, capture the hero and 2-3 key screens in both light and dark. Use the best-looking mode for the hero, show the other in a "Works in dark mode too" section or as a side-by-side comparison.

#### f. Extract the Value Propositions
Don't just list features. For each one, answer: **why does the user care?**
- BAD: "Contact management page"
- GOOD: "See every client, their history, and what needs attention — in one view"
- BAD: "Search functionality"
- GOOD: "Find anything in seconds — semantic search understands what you mean, not just what you type"

### 3. Generate the Showcase

Produce a **single HTML file** with Tailwind CDN (same pattern as `landing-page`):

#### Sections

**Hero**
- App name + tagline
- Primary screenshot in a browser-frame mockup
- Primary CTA button
- Optional: secondary CTA ("Watch Demo", "View Pricing")

**How It Works**
- 3-4 steps with screenshots
- Numbered or arrowed flow
- Brief description under each step
- Shows the main user journey

**Feature Grid**
- 4-6 features in a responsive grid
- Each: screenshot + heading + 1-2 sentence description
- Screenshots in browser-frame mockups (smaller than hero)
- Features extracted from actual app exploration

**Social Proof** (if testimonials provided)
- 2-3 testimonial cards
- Or skip this section entirely if no testimonials

**Pricing** (if provided)
- 2-3 tier cards
- Or skip if not provided

**Before & After** (optional — if the app replaces a manual process)
- Side-by-side comparison: "The old way" (spreadsheet, email, paper) vs "The new way" (your app)
- Use a real screenshot of the app next to a stock representation of the old workflow
- This is the most persuasive section for apps that replace existing tools

**Dark Mode Showcase** (optional — if the app has it)
- Full-width screenshot in dark mode with a brief note: "Easy on the eyes. Dark mode built in."
- Or side-by-side light/dark comparison

**Keyboard Shortcuts / Power Features** (optional — if the app has them)
- Clean grid of shortcuts: Cmd+K search, Cmd+N new, etc.
- Shows the app is built for productivity, not just looks

**Integration / Ecosystem** (optional — if the app connects to things)
- Logo grid of connected services (Google, Slack, Stripe, etc.)
- Or "Works with your existing tools" section

**Open Source / Self-Hosted** (optional — if applicable)
- GitHub stars badge, MIT license, deploy-your-own instructions
- Trust signal for technical audiences

**CTA Banner**
- Full-width call-to-action
- Repeat the primary CTA
- Urgency or benefit statement

**Footer**
- App name, links, legal placeholders

### 4. Screenshot Presentation

Screenshots are shown in browser-frame mockups using CSS:

```css
.browser-frame {
  border-radius: 8px;
  box-shadow: 0 25px 50px -12px rgba(0,0,0,0.25);
  overflow: hidden;
  border: 1px solid rgba(0,0,0,0.1);
}
.browser-frame-bar {
  background: #f1f5f9;
  padding: 8px 12px;
  display: flex;
  gap: 6px;
}
.browser-frame-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #e2e8f0;
}
```

This gives screenshots a polished "app in a browser" look without needing to edit the images.

### 5. Output

Save to a `showcase/` directory:

```
showcase/
├── index.html          # The showcase page
└── screenshots/        # All captured screenshots
    ├── hero.png
    ├── step-1.png
    ├── step-2.png
    ├── step-3.png
    ├── feature-contacts.png
    ├── feature-reports.png
    └── ...
```

The HTML references screenshots with relative paths (`screenshots/hero.png`).

After generating, tell the user:
- Preview: `open showcase/index.html` or `python3 -m http.server -d showcase`
- Deploy: drag the `showcase/` folder to Cloudflare Pages, Netlify, or any static host
- List any placeholder content that needs replacing

## Design Patterns

**Colour**: If the app has a clear brand colour, extract it and use it as the primary. Otherwise default to a neutral palette (slate/blue).

**Typography**: System font stack (no external requests). Same approach as `landing-page`.

**Responsive**: Mobile-first, screenshots scale down gracefully. On mobile, screenshots stack vertically instead of grid.

**Dark mode**: Three-state toggle (light/dark/system) with CSS custom properties.

**Performance**: Lazy-load screenshot images. Tailwind CDN for styling. No build step.

## Making It Look Premium

### Screenshot Enhancement
- **Clean data**: Before screenshotting, make sure the app has realistic data — not "Test Client" and "asdf@example.com"
- **Consistent window size**: All screenshots at the same viewport width (1280x720)
- **No browser chrome in screenshots**: Use the CSS browser-frame mockup instead of capturing the actual Chrome toolbar
- **Highlight the action**: If a screenshot shows a feature, have that feature active/open (modal open, filter applied, item selected)

### Visual Storytelling
- **Lead with the dashboard**: The hero screenshot should show the app populated with data, looking alive and useful
- **Show the app doing work**: Screenshots of results are better than screenshots of empty forms
- **Progressive reveal**: Hero shows the big picture, how-it-works shows the flow, features show the details
- **End with the payoff**: The final section before the CTA should show the result — a report generated, a task completed, a client managed

### Mix Screenshots with Mockups
Real screenshots show the product is real. Mockups show the product is polished. Use both:
- **Hero**: Real screenshot in a browser-frame mockup — proves the app exists and looks good
- **How It Works**: Can use simplified mockup illustrations (CSS shapes, icons, arrows) for the flow steps, with real screenshots for the detail
- **Feature grid**: Real screenshots — users want to see the actual UI
- **Mobile showcase**: CSS device frame mockup (phone outline) around a mobile screenshot
- **Dashboard/overview**: Real screenshot — this is the money shot

**Phone mockup frame** (CSS):
```css
.phone-frame {
  border: 8px solid #1f2937;
  border-radius: 32px;
  overflow: hidden;
  max-width: 280px;
  box-shadow: 0 25px 50px -12px rgba(0,0,0,0.3);
}
.phone-frame-notch {
  background: #1f2937;
  height: 24px;
  border-radius: 0 0 16px 16px;
  width: 120px;
  margin: 0 auto;
}
```

### Animation (CSS-only, no JS required)
```css
/* Fade in sections as user scrolls (intersection observer via CSS) */
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
.section { animation: fadeInUp 0.6s ease-out both; }

/* Subtle float on hero screenshot */
@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-8px); }
}
.hero-screenshot { animation: float 6s ease-in-out infinite; }
```

### Gradient Accents
Extract the app's primary colour and use it for subtle gradient backgrounds on sections:
```css
.hero { background: linear-gradient(135deg, var(--primary) 0%, transparent 60%); }
.cta-banner { background: linear-gradient(135deg, var(--primary), var(--primary-dark)); color: white; }
```

## Quality Rules

1. **Only screenshot real features** — don't fabricate capabilities the app doesn't have
2. **Choose the best screenshots** — not every page is showcase-worthy. Pick the ones that tell the product story.
3. **Write benefit-focused copy** — "See all your contacts in one place" not "Contact list page"
4. **Browser frames on screenshots** — always wrap in the CSS mockup for professional appearance
5. **Consistent screenshot size** — all at 1280x720 for the captures, CSS handles display sizing
6. **No fake testimonials** — leave the section out if none provided
7. **No invented statistics** — leave stats blocks empty if no real data
