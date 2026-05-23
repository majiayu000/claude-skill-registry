---
name: postcall-page-builder
description: Generate personalized post-call landing pages from voice transcripts using the Brutalist Confidence design system.
---

# Post-Call Page Builder Skill

<!--
================================================================================
CHANGELOG (2026-01-18)
================================================================================
Design system update - functionality and schema UNCHANGED:

CHANGED:
- Design system: Generic warm design → Brutalist Confidence
- Typography: Tailwind defaults → Space Grotesk, extreme scale contrast
- Colors: Agency brand colors → Pure black/white, minimal brand accents
- Layout: Soft cards → 4px borders, no rounded corners, alternating listings
- Hover states: Smooth transitions → Instant color inversion
- Hero: Warm greeting → Bold, massive typography with outlined text
- Requirements: Cards with icons → Grid blocks with hover inversion

UNCHANGED:
- Transcript extraction logic
- Listing search process
- Output file paths and formats
- Call JSON schema and fields
- All data mapping
================================================================================
-->

> Generate personalized post-call landing pages from voice transcripts using the Brutalist Confidence design system.

---

## Mission

Transform a raw call transcript into a stunning, personalized HTML page that:
1. Makes the caller feel genuinely heard
2. Reflects their specific requirements back to them
3. Presents relevant property listings
4. Drives clear next-step action

The page should feel like a bold, confident response — not a generic template.

---

## Input Data

You receive:
```json
{
  "callId": "call-abc123",
  "transcript": "Agent: Hi! Thanks for calling...\nCaller: Hi, I'm looking to buy...",
  "agencyData": {
    "id": "agency-id",
    "name": "Agency Name",
    "phone": "02 9211 2222",
    "email": "hello@agency.com",
    "address": "123 Main Street, Suburb NSW 2000",
    "branding": {
      "logoUrl": "...",
      "primaryColor": "#ffe512",
      "secondaryColor": "#1a1a1a"
    }
  }
}
```

**IMPORTANT:** Extract ALL data from the raw transcript. Do not rely on pre-extracted fields.

---

## Processing Steps

### Step 1: Extract Requirements from Transcript

**IMPORTANT:** Always parse the full transcript to extract ALL requirements. Do NOT rely on any pre-extracted data.

#### Primary fields (always look for)
- Caller name: "My name is...", "I'm...", "This is...", "It's [name] here"
- Intent: buy, sell, rent, lease, invest
- Location: suburbs, areas, regions, "near [place]"
- Budget: dollar amounts, ranges, "around", "up to", "between"
- Property type: house, apartment, unit, townhouse, villa, land
- Bedrooms: number mentioned
- Timeframe: "as soon as possible", "in 3 months", "next year"

#### Secondary fields (extract if mentioned)
- Parking requirements
- Pet-friendliness
- Outdoor space (balcony, garden, yard)
- Building features (pool, gym, security)
- Accessibility needs
- School zones
- Commute preferences ("close to work", "near station")
- Current situation ("currently renting", "selling our house")
- Motivation ("growing family", "downsizing", "investment")

#### Personality signals (note for tone)
- Communication style: formal, casual, rushed, chatty
- Specific phrases they used (for reflection)
- Questions they asked
- Concerns they expressed

### Step 2: Search for Listings

Use web search to find matching properties:

1. Primary: Agency website listings page
2. Fallback: realestate.com.au, domain.com.au
3. Search: "[location] [type] for [intent] [budget]"

For each listing extract:
- Property address
- Price/guide
- Bedrooms, bathrooms, parking
- Image URL (main photo)
- Listing URL
- Key features (brief)

### Step 3: Generate Page

Create a bold, personalized HTML page using the Brutalist Confidence design system.

---

## Design System: Brutalist Confidence

### Philosophy

Bold. Stark. Unapologetic. The design commands attention through extreme typography, thick borders, and high contrast. No soft edges, no gradients, no decoration — just confident presentation of information.

### Theme

```
ALWAYS: Light theme (white background, black text)
NEVER: Dark theme, gradients, soft shadows
```

### Colors

```css
--background: #FFFFFF;
--text: #000000;
--border: #000000;
--muted: #666666;
--highlight-bg: #000000;
--highlight-text: #FFFFFF;

/* Agency brand color: USE SPARINGLY */
/* Only for small accents if needed, never as backgrounds */
```

**Rules:**
- Pure black and white only for primary content
- Agency brand color may be used for tiny accents (a line, a dot) but never prominently
- Hover states: instant color inversion (black ↔ white)
- No gradients anywhere
- No colored backgrounds except black

### Typography

```css
/* Font stack */
font-family: 'Space Grotesk', -apple-system, sans-serif;

/* Hierarchy */
--hero-text: clamp(64px, 15vw, 140px), weight 700, line-height 0.85
--section-title: clamp(36px, 8vw, 80px), weight 700, line-height 0.9
--listing-title: clamp(24px, 4vw, 36px), weight 700
--body: 16-18px, weight 400-500
--label: 10-11px, weight 700, letter-spacing 0.15em, uppercase
--price: clamp(32px, 6vw, 48px), weight 700

/* Text treatments */
- ALL CAPS for labels and emphasis
- Outlined text (-webkit-text-stroke: 2px #000) for dramatic variation
- Extreme scale contrast (11px labels next to 140px headlines)
- Tight letter-spacing on large text (-0.04em)
- Wide letter-spacing on labels (0.1-0.2em)
```

**Rules:**
- Never use: Inter, Roboto, Open Sans, Poppins
- Always load Space Grotesk from Google Fonts
- Use weight 700 predominantly, 400-500 for body only
- Headlines should feel massive and confrontational

### Borders & Edges

```css
--border-thick: 4px solid #000000;
--border-standard: 2px solid #000000;

/* All corners are sharp */
border-radius: 0;
```

**Rules:**
- 4px borders for major section dividers
- 2px borders for interactive elements (buttons, tags)
- NO rounded corners anywhere
- NO subtle 1px borders — go bold or none

### Layout Principles

```
STRUCTURE:
├── Edge-to-edge content (minimal padding on sides: 1.5rem)
├── Broken grid — elements can alternate, overlap conceptually
├── Extreme whitespace OR extreme density (no medium)
├── Listings alternate left/right for visual rhythm
├── Giant decorative numbers (01, 02, 03) as design elements
└── Sticky header with thick bottom border
```

**Section Patterns:**
- Full-width sections divided by 4px black borders
- Grid sections for requirements (hover to invert colors)
- Alternating image/content layout for listings
- Black background sections for emphasis (invert all colors)

### Hover & Interaction

```css
/* INSTANT state changes — no transitions */
transition: none;

/* Hover = color inversion */
element:hover {
  background: #000000;
  color: #FFFFFF;
}

/* Buttons */
.button {
  border: 4px solid #000;
  background: #000;
  color: #fff;
}
.button:hover {
  background: #fff;
  color: #000;
}
```

**Rules:**
- All hovers are instant (transition: none)
- Primary interaction pattern: color inversion
- No opacity changes, no scale transforms, no shadows

### Forbidden Elements

```
NEVER USE:
├── Colors: Purple, indigo, cyan, teal, neon anything
├── Borders: Rounded corners, 1px subtle borders
├── Effects: Gradients, shadows, glows, blur
├── Animation: Transitions, fades, transforms
├── Icons: Emoji as decoration, generic icon libraries
├── Layout: Cards with icons, symmetric grids, centered everything
└── Fonts: Inter, Roboto, Open Sans, system defaults
```

---

## Page Structure

The page structure should be FLEXIBLE based on what was extracted. Not all sections are required — include only what's relevant.

### Required Sections

**1. Header (sticky)**
```
[Agency Name]                    [FOR CALLER_NAME]
─────────────────────────────────────────────────── (4px border)
```

**2. Hero**
The first thing they see. Make it personal and bold.

Must include:
- Their name, LARGE
- Acknowledgment that we listened
- What we found for them

Example patterns:
```
SARAH,
WE FOUND
YOUR NEXT
HOME

or

[NAME],
[NUMBER] PROPERTIES
MATCH WHAT YOU
DESCRIBED

or

HEY [NAME],
WE HEARD
EVERY
WORD
```

Use outlined text (`-webkit-text-stroke`) for one line to create visual contrast.

**3. Requirements Display**

Show their criteria back to them. Use a grid of hoverable blocks.

Only show fields that were actually extracted:
```
┌─────────────┬─────────────┬─────────────┐
│ BUDGET      │ LOCATION    │ SIZE        │
│ $800K-$1.2M │ SURRY HILLS │ 2 BED APT   │
└─────────────┴─────────────┴─────────────┘
```

Each block:
- Label (tiny, uppercase, muted)
- Value (large, bold)
- Hover: invert colors instantly

Adapt grid columns to number of requirements (2-4 recommended).

**4. Listings Section**

Header with count:
```
3 PROPERTIES
───────────────────
All within your budget · All pet-friendly
```

Each listing:
- Giant number (01, 02, 03) as decorative element
- Property image placeholder
- Address (large, bold)
- Suburb
- Specs in bordered tags (2 BED, 1 BATH, 1 CAR)
- Price (very large)
- CTA button

**Alternate layout direction** for each listing:
- Listing 1: Image left, content right
- Listing 2: Image right, content left
- Listing 3: Image left, content right

**5. Footer**
```
[Agency Name]                    Powered by Voqo AI
```

### Conditional Sections

Include these ONLY if relevant data was extracted:

**"We Remembered" / Personalization Section**

If transcript contained specific personal details (pet, commute, preferences), create a black-background section:

```
───────────────────────────────────────────────────
WE REMEMBERED

You mentioned wanting to [specific detail from call],
needing [another detail], and [third detail].
Property #X might be perfect because [reason].
───────────────────────────────────────────────────
```

Use `<span>` with underline/highlight on the specific extracted details.

**Match Indicators**

If you can determine why each listing matches, show it:
- "Matches: Location · Budget · Pet-friendly"
- Or as a subtitle under the listing header

**Timeline/Urgency Section**

If they mentioned timeframe:
```
YOU MENTIONED: MOVING IN 3 MONTHS
These properties are all available for [timeframe].
```

---

## Personalization Depth

### Levels of Personalization

**Level 1 — Basic (minimum):**
- Use their name in hero
- Display extracted requirements
- Show matching listings

**Level 2 — Good:**
- Reference specific things from transcript
- Explain WHY each listing matches
- Adapt tone to their communication style

**Level 3 — Excellent (target):**
- Pull exact quotes or details ("your dog", "walking to work")
- Create a "We Remembered" section with surprising detail
- Match the energy of how they spoke
- Anticipate their next questions

### Tone Matching

Based on transcript signals:

| If they were... | Page should feel... |
|-----------------|---------------------|
| Rushed/busy | Punchy, scannable, minimal |
| Chatty/warm | Personal, conversational |
| Formal/professional | Structured, precise |
| Uncertain/nervous | Reassuring, clear next steps |
| Excited | Energetic, exclamation-worthy |

### Copy Guidelines

**DO:**
- Use their name 2-3 times naturally
- Reference specific details they mentioned
- Be direct and confident
- Use active voice
- Keep sentences short and punchy

**DON'T:**
- Use generic phrases: "tailored just for you", "your dream home awaits"
- Over-explain or pad with fluff
- Use exclamation marks excessively
- Sound robotic or templated
- Make promises you can't keep

---

## Listing Display

### Information Hierarchy

For each listing, display in this order:
1. Listing number (giant, decorative)
2. Match reason (if determinable)
3. Address (primary focus)
4. Suburb + postcode
5. Specs (bed/bath/car/size)
6. Price (prominent)
7. CTA

### Spec Tags

Display as inline bordered elements:
```html
<span class="spec">2 BED</span>
<span class="spec">1 BATH</span>
<span class="spec">1 CAR</span>
<span class="spec">78M²</span>
```

### Price Display

- Always prominent (32-48px)
- Use monospace or tabular figures if available
- Include price type if known: "Guide", "Offers over", "Auction"

### Image Handling

```html
<div class="listing-image">
  <!-- If image URL available -->
  <img src="[url]" alt="[address]" loading="lazy">

  <!-- If no image, styled placeholder -->
  <span>IMAGE</span>
</div>
```

Image placeholder styling:
```css
.listing-image {
  aspect-ratio: 4/3;
  background: linear-gradient(135deg, #F0F0F0 0%, #E0E0E0 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  letter-spacing: 0.1em;
  color: #999;
}
```

### CTA Buttons

Each listing should have:
```html
<a href="[listing_url]" class="listing-cta">VIEW PROPERTY →</a>
```

Optionally:
```html
<a href="[booking_url]" class="listing-cta-secondary">BOOK INSPECTION</a>
```

---

## Technical Requirements

### HTML Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[CALLER_NAME] — Property Results | [AGENCY_NAME]</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    /* All styles embedded */
  </style>
</head>
<body>
  <!-- Content -->
</body>
</html>
```

### Required CSS Reset

```css
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: 'Space Grotesk', -apple-system, sans-serif;
  background: #FFFFFF;
  color: #000000;
  font-size: 16px;
  line-height: 1.4;
}

::selection {
  background: #000;
  color: #fff;
}

a {
  color: inherit;
  text-decoration: none;
}
```

### Responsive Breakpoints

```css
@media (max-width: 768px) {
  /* Stack grids to single column */
  /* Maintain 4px borders between stacked sections */
  /* Reduce hero text size */
  /* Full-width images */
  /* Stack listing layout (image above content) */
}
```

### Performance

- Single HTML file, all CSS embedded
- No external dependencies except Google Fonts
- Lazy load images: `loading="lazy"`
- Minimize DOM depth

---

## Data Mapping

- caller_name → greeting, page title, hero
- intent → requirements display, "Buy"/"Sell"/"Rent"
- preferred_location → requirements display
- budget_range → requirements display
- agencyData.name → header, footer
- agencyData.branding.* → minimal accent colors only
- agencyData.phone → contact CTA

---

## Output Files

### 1. HTML Page

Save to the provided `postcallHtmlPath`.

### 2. Update Call JSON

Update the existing file at `callDataPath` with:

```json
{
  "callId": "existing",
  "timestamp": "existing",
  "agencyId": "existing",

  "callerName": "Sarah",
  "extractedData": {
    "caller_name": "Sarah",
    "caller_intent": "buy",
    "preferred_location": "Surry Hills or Darlinghurst",
    "budget_range": "$800k-$1.2M",
    "property_type": "apartment",
    "bedrooms": "2",
    "additional_requirements": ["pet-friendly", "natural light", "walk to CBD"],
    "timeframe": null,
    "communication_style": "friendly, detailed"
  },
  "intent": "buy",
  "location": "Surry Hills or Darlinghurst",
  "budget": "$800k-$1.2M",
  "requirements": {
    "intent": "buy",
    "location": "Surry Hills or Darlinghurst",
    "budget": "$800k-$1.2M",
    "propertyType": "apartment",
    "bedrooms": "2",
    "additional": ["pet-friendly", "natural light", "walk to CBD"]
  },
  "listingsShown": [
    {
      "address": "12/45 Crown Street",
      "suburb": "Surry Hills",
      "price": "$950,000",
      "beds": 2,
      "baths": 1,
      "cars": 1,
      "url": "https://..."
    }
  ],
  "personalizationUsed": [
    "Referenced caller's dog",
    "Mentioned walking to work preference",
    "Highlighted north-facing for natural light"
  ],
  "pageUrl": "/call/[call-id]",
  "pageStatus": "completed",
  "generatedAt": "2026-01-18T14:32:00Z"
}
```

---

## Quality Checklist

Before finalizing, verify:

### Design
- [ ] Space Grotesk font loaded and applied
- [ ] 4px black borders on major sections
- [ ] No rounded corners anywhere
- [ ] Hero text is appropriately massive
- [ ] Hover states invert colors instantly (no transitions)
- [ ] No gradients, shadows, or soft effects
- [ ] Listings alternate left/right layout

### Personalization
- [ ] Caller's name appears in hero
- [ ] All extracted requirements are displayed
- [ ] At least one specific transcript detail is referenced
- [ ] Tone matches caller's communication style

### Content
- [ ] 3-5 listings displayed (not overwhelming)
- [ ] Each listing has address, price, specs, CTA
- [ ] Prices match the stated budget range
- [ ] Locations match the stated preference
- [ ] Clear next-step CTA at bottom

### Technical
- [ ] Valid HTML5
- [ ] All styles embedded (no external CSS)
- [ ] Responsive on mobile
- [ ] Images have loading="lazy"
- [ ] No console errors

---

## Examples

### Hero Variations

**For someone named "James" looking to buy:**
```
JAMES,
WE FOUND
3 PLACES
YOU'LL LOVE
```

**For someone named "Sarah" looking to rent:**
```
SARAH,
YOUR NEW
RENTAL IS
WAITING
```

**For someone named "Mike" selling:**
```
MIKE,
HERE'S WHAT
YOUR HOME
IS WORTH
```

### Requirements Grid Variations

**2 requirements:**
```
┌──────────────────┬──────────────────┐
│ BUDGET           │ LOCATION         │
│ $1.5M-$2M        │ NORTHERN BEACHES │
└──────────────────┴──────────────────┘
```

**4 requirements:**
```
┌────────────┬────────────┬────────────┬────────────┐
│ INTENT     │ BUDGET     │ LOCATION   │ SIZE       │
│ BUY        │ $800K-$1M  │ INNER WEST │ 3 BED      │
└────────────┴────────────┴────────────┴────────────┘
```

### "We Remembered" Section

```html
<section class="remembered">
  <div class="remembered-label">WE REMEMBERED</div>
  <p class="remembered-content">
    You mentioned needing space for your <span>two kids</span>,
    wanting to be in the <span>Newtown Public School catchment</span>,
    and having a <span>maximum commute of 30 minutes to Circular Quay</span>.
    All three properties tick these boxes.
  </p>
</section>
```

---

## Final Notes

The goal is not just to show listings — it's to make the caller feel that we actually listened. The Brutalist design makes a bold first impression; the personalization makes it memorable.

Every page should feel like it was crafted specifically for that one person, not generated from a template. The design system is rigid; the content is fluid and human.
