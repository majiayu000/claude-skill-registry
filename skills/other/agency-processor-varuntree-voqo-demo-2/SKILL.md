---
name: agency-processor
description: Extract agency data and generate a branded demo landing page with real-time progress updates. Optimized for speed and conversion.
---

# Agency Processor Skill (Single Agency)

<!--
================================================================================
CHANGELOG (2026-01-18 v2)
================================================================================
Clarified page purpose and fixed design issues:

PURPOSE CLARIFICATION:
- Page is a DEMO INVITATION for Voqo AI voice platform
- Agency branding shows personalization, but page is about TRYING THE DEMO
- NOT a lead gen page, NOT an agency info page, NOT generic SaaS marketing

COLOR/READABILITY FIXES:
- Added explicit COLOR CONTRAST RULES section
- Banned gradient backgrounds in hero sections
- Brand colors should be accents only, not full backgrounds
- Added specific rules: light bg = dark text, dark bg = light text
- Explicitly banned white text on yellow backgrounds

CONTENT FIXES:
- Removed stats/metrics sections (team size, listings) - distracts from demo
- Removed pain point / opportunity analysis sections
- Headlines should invite to demo, not promise business outcomes
- Sections renamed: "Value Proposition" → "What You'll Experience"

IMAGE HANDLING:
- Added strict image URL validation rules (reject relative paths, placeholders, SVGs, etc.)
- Removed teamImageUrl and officeImageUrl extraction (rarely work)
- Explicit guidance: "When in doubt, no image"
- Prefer solid color backgrounds over potentially broken images

BANNED ADDITIONS:
- Added #7a00df, #6200b3 to banned purple colors
- Added gradient hero backgrounds to banned layouts
- Added pain point cards to banned layouts
- Added stats grids to banned layouts

================================================================================
CHANGELOG (2026-01-18 v1)
================================================================================
Major refactor to improve speed and landing page quality:

REMOVED:
- Pain score calculation (Phase 2 deleted) - was slow and not useful for conversion
- WebSearch for metrics - unnecessary extra step
- Complex metrics: painScore, painReasons, hasPropertyManagement, hasChatWidget,
  hasAfterHoursNumber, hasOnlineBooking, soldCount, forRentCount, priceRangeMin/max
- Multiple WebFetch calls - now single fetch only

ADDED:
- Design System Selection - 7 design systems to choose from based on agency type
- Voqo branding requirement - "Presented by Voqo" on all pages
- Image extraction - heroImageUrl, teamImageUrl, officeImageUrl
- Tagline extraction - for personalized hero copy
- Landing Page Structure - focused on demo conversion, not information
- Banned elements list - avoid AI-slop colors, fonts, layouts
- Explicit extraction format - consistent data across all agencies

CHANGED:
- Workflow: 5 phases → 4 phases (removed pain score phase)
- WebFetch budget: ≤3 → ≤1 (homepage only)
- WebSearch budget: ≤1 → 0 (none)
- Landing page purpose: informational → conversion-focused
- Schema: simplified, removed unused fields

UNCHANGED:
- Activity streaming format and behavior
- Progress file update mechanics
- File paths and inputs
- Demo phone number requirement
- Error handling approach
================================================================================
-->

You process exactly one real-estate agency end-to-end:
1) Quickly extract branding + contact + images from homepage (single fetch).
2) Select appropriate design system based on agency type.
3) Generate a conversion-focused demo landing page.
4) Continuously update progress + activity so the UI streams smoothly.

## Hard Rules
- Do not spawn other agents.
- Do not use emojis in any text you write.
- Use only the absolute paths provided in the prompt.
- Do NOT use WebSearch - extract only from the homepage.
- Maximum 1 WebFetch call (homepage only).

## Inputs (from the prompt)
- `agencyId`: URL-safe slug (example: `ray-white-surry-hills`)
- `sessionId`: pipeline session ID
- `name`: agency name (best-effort)
- `website`: agency website URL
- `progressFilePath`: absolute path to `data/progress/agency-{agencyId}.json`
- `activityFilePath`: absolute path to `data/progress/agency-activity-{agencyId}.json`
- `demoHtmlPath`: absolute path to `public/demo/{agencyId}.html`
- `agencyDataPath`: absolute path to `data/agencies/{agencyId}.json`

## Tools Allowed
- Use only: `WebFetch`, `Read`, `Write`, `Glob`
- Do NOT use: `WebSearch`, browser automation tools

---

## Output Files (must write all)

### 1) Activity Stream (`activityFilePath`)

Store a single JSON object and append to `messages`:
```json
{
  "sessionId": "pipe-...",
  "agencyId": "ray-white-surry-hills",
  "agencyName": "Ray White Surry Hills",
  "messages": [
    {
      "id": "msg-<timestamp>-<rand>",
      "type": "thinking|tool|fetch|results|identified|warning",
      "text": "Short, user-facing update",
      "detail": "Optional: URL or query",
      "source": "Subagent",
      "timestamp": "2026-01-17T12:34:56.789Z"
    }
  ]
}
```

Rules:
- Every `id` must be unique (use timestamp + random suffix).
- Before `WebFetch`, append a `fetch` message with `detail` set to the URL.
- After each milestone, append a short `identified/results/thinking` message.
- Keep only the last 250 messages.

### 2) Progress File (`progressFilePath`)

<!-- CHANGED: Removed painScore, simplified metrics, added designSystem and image fields -->

Always write valid JSON with stable keys:
```json
{
  "agencyId": "...",
  "sessionId": "...",
  "status": "skeleton|extracting|generating|complete|error",
  "updatedAt": "ISO timestamp",
  "name": "...",
  "website": "...",
  "phone": null,
  "address": null,
  "email": null,
  "logoUrl": null,
  "primaryColor": null,
  "secondaryColor": null,
  "tagline": null,
  "heroImageUrl": null,
  "teamSize": null,
  "listingCount": null,
  "designSystem": null,
  "htmlProgress": 0,
  "demoUrl": null,
  "steps": [
    { "id": "website", "label": "Found website", "status": "pending|in_progress|complete|error" },
    { "id": "details", "label": "Extracted details", "status": "pending|in_progress|complete|error" },
    { "id": "generating", "label": "Generating demo page", "status": "pending|in_progress|complete|error" },
    { "id": "complete", "label": "Ready", "status": "pending|in_progress|complete|error" }
  ],
  "error": null
}
```

Rules:
- Update `updatedAt` on every write.
- Never remove keys; set missing fields to `null`.

### 3) Agency Record (`agencyDataPath`)

<!-- CHANGED: Removed painScore, painReasons, complex metrics. Added images and designSystem. -->

Write the durable record used by the rest of the system:
```json
{
  "id": "ray-white-surry-hills",
  "name": "Ray White Surry Hills",
  "website": "https://...",
  "phone": "02 ...",
  "email": null,
  "address": "Full street address",
  "tagline": null,
  "branding": {
    "logoUrl": null,
    "primaryColor": "#0f172a",
    "secondaryColor": "#ffffff",
    "heroImageUrl": null
  },
  "metrics": {
    "teamSize": null,
    "listingCount": null
  },
  "researchedAt": "ISO timestamp",
  "dataQuality": "complete|partial|minimal",
  "notes": null,
  "demoPage": {
    "generated": true,
    "generatedAt": "ISO timestamp",
    "url": "/demo/ray-white-surry-hills",
    "designSystem": "editorial-prestige"
  }
}
```

---

## Performance Targets

<!-- CHANGED: Reduced from 3 WebFetch + 1 WebSearch to just 1 WebFetch -->

| Metric | Target |
|--------|--------|
| WebFetch calls | 1 (homepage only) |
| WebSearch calls | 0 (none) |
| Progress file writes | 4-5 |
| Total time per agency | <30 seconds |

If data is unclear after fetching homepage, set unknown fields to `null` and proceed.
Do NOT do additional fetches for missing data.

---

## Information Extraction Format

<!-- NEW: Explicit extraction format for consistency across all agencies -->

Extract these fields from the homepage HTML in a single pass:

### Required (must find or set null)

| Field | Where to Look | Format |
|-------|---------------|--------|
| `logoUrl` | `<img>` with "logo" in src/alt/class, `<link rel="icon">` | Full URL |
| `phone` | Links with `tel:`, text matching phone patterns (02, 04, 1300, 1800) | Australian format |
| `address` | Footer, contact section, schema.org LocalBusiness markup | Full street address |

### Best-effort (extract if visible on homepage)

| Field | Where to Look | Format |
|-------|---------------|--------|
| `email` | Links with `mailto:`, visible email text | email@domain.com |
| `primaryColor` | Header/nav background, brand elements, logo colors | Hex (#RRGGBB) |
| `secondaryColor` | CTA buttons, accent elements, links | Hex (#RRGGBB) |
| `tagline` | Hero section text, `<meta name="description">`, slogan | Short string |
| `teamSize` | "X agents" text, team count if visible | Number or null |
| `listingCount` | "X properties" text, listing count if visible | Number or null |

### Images (STRICT VALIDATION REQUIRED)

**IMPORTANT: Most extracted image URLs will NOT work.** Only use images that pass ALL these checks:

#### Image URL Validation Rules
```
REJECT if URL:
- Is a relative path (doesn't start with http:// or https://)
- Contains "placeholder", "default", "blank", "spacer"
- Is from a CDN that requires auth (cloudinary transforms, imgix with tokens)
- Is a base64 data URI
- Is an SVG file (often icons, not photos)
- Is smaller than 100x100 (likely an icon)
- Contains tracking parameters (?utm_, ?ref=, etc.)
- Is from social media CDNs (fbcdn, twimg) - often expire

PREFER URLs that:
- Are from the agency's own domain
- Are from stable CDNs (amazonaws, cloudfront without signed URLs)
- Have common image extensions (.jpg, .jpeg, .png, .webp)
- Are clearly named (hero.jpg, team-photo.png, office.jpg)
```

#### Extraction Priority
| Field | Where to Look | Format |
|-------|---------------|--------|
| `logoUrl` | `<img>` with "logo" in src/alt/class, `<link rel="icon">` | Full URL (validated) |
| `heroImageUrl` | Hero section background, main banner `<img>` | Full URL (validated) |

**DO NOT extract these** (rarely work, clutter the page):
- `teamImageUrl` - usually broken or requires auth
- `officeImageUrl` - usually broken or requires auth

#### When In Doubt: NO IMAGE
If you're not confident an image URL will load, **do not include it**.
A clean page with no images is better than a broken page with missing images.
Use solid color backgrounds instead of potentially broken hero images.

### DO NOT extract (removed for speed)
- soldCount, forRentCount, priceRangeMin, priceRangeMax
- painScore, painReasons
- hasPropertyManagement, hasChatWidget, hasAfterHoursNumber, hasOnlineBooking

---

## Design System Selection

<!-- NEW: Choose design system based on agency type for better visual quality -->

Before generating HTML, select ONE design system based on the agency:

### Selection Logic

```
AGENCY TYPE                                    → DESIGN SYSTEM
─────────────────────────────────────────────────────────────────
National franchise (Ray White, LJ Hooker,      → "swiss-precision"
Century 21, Raine & Horne, McGrath, Belle)       (clean, professional)

Boutique/independent agency                    → "editorial-prestige"
                                                 (distinctive, premium)

Luxury/prestige market indicators              → "quiet-luxury"
(words like "prestige", "exclusive", "luxury")   (refined, exclusive)

Modern/tech-forward agency                     → "cinematic-reveal"
(sleek website, modern branding)                 (dramatic, impactful)

Traditional/established agency                 → "warm-authority"
(est. dates, community focus)                    (trustworthy, approachable)

DEFAULT (when unsure)                          → "editorial-prestige"
                                                 (works for most)
```

Write the selected design system to `progress.designSystem` and `agencyRecord.demoPage.designSystem`.

### Design System Constraints (MUST FOLLOW)

#### Banned Colors (AI-slop - NEVER use these)
```
- ANY purple/violet/indigo: #6366F1, #8B5CF6, #A855F7, #7C3AED, #7a00df, #6200b3
- Neon cyan/teal: #00FF88, #00DDFF, #06B6D4
- ChatGPT green: #10A37F
- Any purple + green combinations
- Any blue-to-purple gradients
- ANY gradient backgrounds in hero sections
```

#### Banned Fonts (overused - NEVER use these)
```
- Inter (the #1 AI-slop font)
- Roboto, Open Sans, Lato
- Poppins, Montserrat
```

#### Approved Fonts (use these instead)
```
Headlines: Playfair Display, Space Grotesk, Cabinet Grotesk, Fraunces
Body: Source Serif 4, DM Sans, IBM Plex Sans, Outfit
```

#### Banned Layouts (AI-slop patterns)
```
- Three equal cards with icons in a horizontal row
- Symmetric 2x2 or 3x3 grids without hierarchy
- Gradient hero backgrounds (use solid colors instead)
- Generic "feature cards" with icon + title + description
- Pain point cards or "opportunity analysis" sections
- Stats/metrics grids (team size, listings, etc.)
```

#### COLOR CONTRAST RULES (CRITICAL)
```
Text must ALWAYS be readable. Follow these rules:

LIGHT BACKGROUNDS (white, cream, light gray):
  - Use dark text: #1a1a1a, #333333, slate-900
  - Never use white or light text

DARK BACKGROUNDS (navy, charcoal, black):
  - Use white or very light text: #ffffff, #f5f5f5
  - Never use dark text

BRAND COLOR BACKGROUNDS:
  - If brand color is LIGHT (yellow, light blue, beige): use DARK text
  - If brand color is DARK (navy, forest green, burgundy): use LIGHT text
  - When in doubt, use light background with dark text

NEVER DO:
  - White text on yellow/gold backgrounds
  - Light gray text on white backgrounds
  - Dark text on dark backgrounds
  - Any text color that doesn't have at least 4.5:1 contrast ratio
```

#### Required
- Light theme by default (warm whites: #FAFAF9, #F8F6F1, #ffffff)
- Use agency's extracted brand colors ONLY for accents (buttons, borders), not backgrounds
- Fallback accent colors: navy (#1E3A5F), terracotta (#C2703A), forest green (#2D5A47)
- Body text: always dark (#1a1a1a or slate-900) on light backgrounds
- Mobile-responsive (test at 375px width)
- No emojis anywhere

---

## Landing Page Purpose & Structure

### Primary Goal

**This is a DEMO INVITATION page for Voqo AI's voice agent platform.**

The page exists to invite this specific agency to EXPERIENCE the Voqo voice AI by calling the demo number. They will hear an AI receptionist answer as their agency.

This is NOT:
- A lead gen landing page for the agency
- An informational page about the agency's services
- A generic SaaS product page

### Content Philosophy

The page should feel like a personalized demo invitation:
- "We built a voice AI demo just for {Agency Name}"
- "Call now and hear how Voqo sounds when answering as your agency"
- The agency branding shows we've customized the demo FOR THEM

### Required Sections (in order)

#### 1. Hero Section
- Agency logo (if extracted) prominently displayed
- Agency name as context (not headline)
- Headline: Direct invitation to try the demo
  - GOOD: "Hear How Voqo Answers Your Calls"
  - GOOD: "Your AI Receptionist Demo is Ready"
  - BAD: "Scale Your Agency" (too generic)
  - BAD: "Never Miss a Lead" (feature-focused, not demo-focused)
- Subheadline: What happens when they call
  - Example: "Call now and our AI will answer as {Agency Name}"
- Primary CTA: Large call button with phone number visible
- Background: Light/neutral - ensure text is ALWAYS readable

#### 2. What You'll Experience (not "value proposition")
- Frame as what happens IN THE DEMO CALL:
  - "AI answers with your agency name"
  - "Natural conversation about property inquiries"
  - "See the caller summary page after"
- This is about the DEMO EXPERIENCE, not product benefits

#### 3. How the Demo Works (3 steps)
- Step 1: "Call the number below"
- Step 2: "Our AI answers as {Agency Name}"
- Step 3: "After the call, see your personalized results page"
- Emphasize this is a LIVE demo they can try RIGHT NOW

#### 4. Call-to-Action Section (prominent)
- Large call button: `tel:+614832945767`
- Display number clearly: `04832945767`
- Trust text: "30 seconds" • "No signup" • "Try it now"
- Secondary: "I already called" button (uses window.registerDemoCall)

#### 5. Footer
- "Presented by Voqo" with link to https://voqo.ai
- "AI Voice Agents for Real Estate"
- Agency name + location for context
- Keep minimal

### NOT Included
- Pain scores, pain reasons, or "opportunity analysis"
- Agency metrics (team size, listings, etc.) - this distracts from demo
- Feature comparison tables
- Pricing information
- Generic SaaS marketing copy

---

## Demo Phone Number (CRITICAL)

Every landing page MUST use this exact phone number for the demo CTA:

| Format | Value |
|--------|-------|
| Display | `04832945767` |
| E.164 (for tel: links) | `+614832945767` |
| tel: href | `tel:+614832945767` |

DO NOT use:
- The agency's actual phone number
- Any other phone number
- Placeholder numbers

This number is configured in ElevenLabs to run the demo voice agent.

### CTA Button Implementation

```html
<!-- Primary CTA -->
<a href="tel:+614832945767" class="...primary button styles...">
  Try the Demo: 04832945767
</a>

<!-- Secondary CTA -->
<button onclick="window.registerDemoCall && window.registerDemoCall()" class="...secondary styles...">
  I already called
</button>
```

---

## Voqo Branding

<!-- NEW: Required branding on all generated pages -->

Every landing page must include "Presented by Voqo" branding:

### Placement
- **Footer** (required): "Presented by Voqo" with link
- **Optional**: Small "Voqo" text in hero subtitle

### Style
- Subtle, not competing with agency branding
- Use neutral gray (#6B7280) or design system secondary color
- Font size: 12-14px
- Link to: https://voqo.ai

### Example Implementation

```html
<footer class="py-8 text-center">
  <p class="text-sm text-gray-500">
    Demo for {Agency Name} · {Suburb}
  </p>
  <p class="text-xs text-gray-400 mt-2">
    Presented by <a href="https://voqo.ai" target="_blank" rel="noopener" class="underline hover:text-gray-600">Voqo</a>
  </p>
</footer>
```

---

## Workflow (4 Phases)

<!-- CHANGED: Reduced from 5 phases to 4. Removed pain score phase. Single WebFetch. -->

### Phase 0: Initialize

1) Append activity message:
   - `type: "thinking"`, `text: "Starting agency processing"`

2) Write progress file:
   - `status = "extracting"`
   - In the `steps` array, set the step with `id: "website"` to `status = "in_progress"` (keep `steps` as an array; never convert it to an object).

### Phase 1: Fetch + Extract (SINGLE WebFetch)

1) Append activity message:
   - `type: "fetch"`, `text: "Fetching website"`, `detail: <website URL>`

2) WebFetch the homepage URL

3) Extract ALL fields in one pass (see Information Extraction Format):
   - Logo, colors, phone, address, email, tagline
   - Hero image, team image, office image
   - Team size, listing count (if visible)

4) Update progress file:
   - In the `steps` array, set `id: "website"` to `status = "complete"`
   - In the `steps` array, set `id: "details"` to `status = "in_progress"`
   - Write all extracted fields

5) Append activity message:
   - `type: "identified"`, `text: "Extracted agency details"`

6) Update progress file:
   - In the `steps` array, set `id: "details"` to `status = "complete"`

NOTE: Do NOT do additional WebFetch for missing fields. Set to null and proceed.

### Phase 2: Select Design System + Generate HTML

1) Select design system based on agency type (see Selection Logic)

2) Append activity message:
   - `type: "thinking"`, `text: "Generating demo page"`

3) Update progress file:
   - `status = "generating"`
   - In the `steps` array, set `id: "generating"` to `status = "in_progress"`
   - `designSystem = "<selected-system>"`
   - `htmlProgress = 10`

4) Generate HTML following:
   - Selected design system constraints (colors, fonts, layouts)
   - Landing page structure (5 sections)
   - Fixed demo phone number
   - Voqo branding in footer
   - Mobile-responsive design
   - Tailwind CSS via CDN

5) Update progress file:
   - `htmlProgress = 70`

6) Write HTML to `demoHtmlPath`

7) Update progress file:
   - `htmlProgress = 100`

8) Append activity message:
   - `type: "results"`, `text: "Demo page generated"`, `detail: "/demo/{agencyId}"`

### Phase 3: Finalize

1) Write agency record to `agencyDataPath` (see schema above)

2) Update progress file:
   - In the `steps` array, set `id: "generating"` to `status = "complete"`
   - In the `steps` array, set `id: "complete"` to `status = "complete"`
   - `status = "complete"`
   - `demoUrl = "/demo/{agencyId}"`

3) Append activity message:
   - `type: "identified"`, `text: "Agency processing complete"`

---

## Error Handling

If the WebFetch fails:
1) Append activity message:
   - `type: "warning"`, `text: "Failed to fetch website"`, `detail: <error reason>`

2) Write progress file:
   - `status = "error"`
   - In the `steps` array, set `id: "website"` to `status = "error"`
   - `error = "<error message>"`

3) Stop processing (no retries).

If HTML generation fails:
1) Append activity message with warning
2) Write progress with `status = "error"` and in the `steps` array set `id: "generating"` to `status = "error"`
3) Stop processing.

---

## HTML Template Requirements

### Head Section
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{Agency Name} - AI Voice Demo | Voqo</title>
  <meta name="description" content="Try the AI voice receptionist demo for {Agency Name}. Professional call handling powered by Voqo.">
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family={Selected+Font}&display=swap" rel="stylesheet">
</head>
```

### Script Inclusion (before closing body)
```html
  <script src="/voqo-demo-call.js"></script>
</body>
</html>
```

This script handles:
- Demo call registration with the server
- "I already called" button functionality
- Context passing to the voice agent

Do NOT implement these yourself. Just include the script.

---

## Quick Reference

| Item | Value |
|------|-------|
| Demo phone (display) | `04832945767` |
| Demo phone (E.164) | `+614832945767` |
| Voqo link | `https://voqo.ai` |
| Tailwind CDN | `https://cdn.tailwindcss.com` |
| Max WebFetch | 1 |
| Max WebSearch | 0 |
| Default design system | `editorial-prestige` |
| Light theme background | `#FAFAF9` or `#F8F6F1` |
