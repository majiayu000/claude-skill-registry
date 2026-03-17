---
name: document-studio
description: Create and update professional HTML documents (proposals, flyers, sponsor packets, one-pagers) with consistent NGM branding, voice, and messaging. Maintains institutional knowledge about NGM programs and design standards.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# NGM Document Studio

## Overview

Document Studio is the unified system for creating and updating all NGM professional documents. It maintains consistency across:
- **Voice & Tone**: Professional yet personable, confident without being salesy
- **Visual Design**: The NGM editorial design system (gold accents, Newsreader/Inter fonts, clean hierarchy)
- **Messaging**: Accurate, up-to-date descriptions of NGM programs, credentials, and value propositions

## Document Types Supported

| Type | Use Case | Output Location |
|------|----------|-----------------|
| **Proposal** | Client-specific proposals from meetings/transcripts | `content/docs/proposal-[client]-[date].html` |
| **Flyer** | 1-2 page print-ready marketing materials | `content/docs/[name]-flyer.html` |
| **Sponsor Packet** | Multi-page event sponsorship materials | `content/docs/[event]-sponsor-packet.html` |
| **One-Pager** | Single-page overviews of programs/services | `content/docs/[topic]-one-pager.html` |

---

## Pre-Generation Steps (ALWAYS DO THIS)

Before creating or updating ANY document:

### 1. Check Existing Documents
```
Glob: content/docs/*.html
```

### 2. Read Reference Materials
- **Voice Guide**: `.claude/skills/document-studio/voice-and-style.md`
- **NGM Programs**: `.claude/skills/document-studio/ngm-programs.md`
- **Design System**: `.claude/skills/document-studio/design-system.md`

### 3. For Updates, Read the Existing Document
Read the full document to understand current structure before making changes.

### 4. For New Documents, Read 1-2 Similar Examples
Learn from existing documents of the same type to maintain consistency.

---

## Voice & Style Summary

**Core Principles:**
1. **Confident, not salesy** — We state facts and outcomes, not hype
2. **Specific, not vague** — Concrete numbers, real credentials, specific outcomes
3. **First-principles reasoning** — We explain WHY, not just what
4. **Personable authority** — Expert but approachable, never condescending
5. **Outcome-focused** — Lead with transformation, not features

**Avoid:**
- Marketing buzzwords ("revolutionary", "game-changing", "cutting-edge")
- Vague claims ("best-in-class", "world-class")
- Hyperbole and superlatives
- Salesy urgency ("Act now!", "Limited time!")
- Feature dumping without context

**Use:**
- Specific metrics and outcomes
- Third-person references to Dr. Vinjamoori in formal docs
- First-person "I/we" in proposals after initial meeting
- Evidence-backed claims with context
- Clear value propositions tied to recipient needs

See `voice-and-style.md` for complete guidance.

---

## NGM Programs Reference

Always reference programs accurately. Key offerings:

### Longevity Intelligence Platform (LIP)
- AI-powered clinical intelligence for longevity practitioners
- 50,000+ peer-reviewed studies synthesized
- Combines research + protocols + proprietary frameworks
- "As I get smarter, you get smarter"

### AI Lab Report Generator
- Transforms raw labs into publication-quality patient reports
- 5-minute turnaround vs 45-minute manual process
- Customizable to practice philosophy and branding
- Handles metabolic, endocrine, longevity markers

### Educational Curriculum
- 150+ deep-dive modules
- Topics: hormones, peptides, GLP-1s, diagnostics, aging frameworks, AI
- Monthly live lectures with latest research
- NGM Certification pathway

### NGM Community & Mentorship
- 240+ member private practitioner community
- Weekly live sessions with Dr. Vinjamoori
- Real-time case feedback
- Expert network access

### NGM Commons
- Vendor intelligence platform for longevity clinicians
- Research-driven, AI-native vendor profiles
- Helps clinicians evaluate solutions before buying

### NGM Summit
- Global forum on healthspan medicine and clinical innovation
- Inaugural event: Japan 2026
- Partnership with Nakanoshima Qross (Osaka's medical innovation district)

See `ngm-programs.md` for complete details, pricing, and positioning.

---

## Design System Summary

### Color Palette
```css
--paper: #FFFFFF;        /* Main background */
--paper-alt: #FAFAF8;    /* Secondary background */
--ink-900: #0A0B0C;      /* Darkest text, headings */
--ink-700: #1F2124;      /* Body text */
--ink-500: #5C626B;      /* Secondary text */
--ink-400: #8B909A;      /* Muted text */
--line: #E5E3DE;         /* Borders, dividers */
--gold: #C5A572;         /* Accent color (use sparingly) */
--vermillion: #E03E2F;   /* Alert/CTA accent (rare) */
```

### Typography
- **Headings**: Newsreader (serif) - elegant, editorial feel
- **Body**: Inter (sans-serif) - clean, readable
- **Labels**: Inter, uppercase, letter-spacing 0.08-0.12em

### Key Components
- **Section numbers**: Black square with white number
- **Highlight boxes**: Paper-alt background, gold left border
- **Pricing tables**: Clean borders, recommended row highlighted
- **Tier cards**: Border cards, featured tier in ink-900 with gold border
- **Credential items**: Gold arrow + text

See `design-system.md` for complete CSS and component patterns.

---

## Creating New Documents

### Proposals

**Required inputs:**
1. Client name
2. Meeting transcript or notes
3. Proposal type (consulting/enterprise) - can be inferred

**Process:**
1. Read `voice-and-style.md` and `ngm-programs.md`
2. Read 1-2 recent proposals from `content/docs/`
3. Extract from transcript: client info, pain points, goals, budget signals
4. Generate proposal following section framework
5. Save to `content/docs/proposal-[client-slug]-[YYYY-MM-DD].html`

**Section Framework:**
1. Header (NGM wordmark, date, client name)
2. Executive Summary (2-3 sentences max)
3. Understanding Your Situation (from transcript)
4. Proposed Solution (scope, deliverables)
5. Why NGM (relevant credentials only)
6. Investment (pricing with justification)
7. Next Steps (clear CTA)

### Flyers

**Required inputs:**
1. Topic/program to promote
2. Target audience
3. Call-to-action (what should reader do?)

**Process:**
1. Read `voice-and-style.md` and `ngm-programs.md`
2. Read existing flyers from `content/docs/`
3. Design for 8.5x11" print (use `.page` container)
4. Keep to 1-2 pages maximum
5. Save to `content/docs/[topic]-flyer.html`

**Must include:**
- NGM header with logo mark
- Clear value proposition headline
- 3-4 key benefits/features
- Pricing tiers (if applicable)
- Contact/CTA section

### Sponsor Packets

**Required inputs:**
1. Event name and details
2. Sponsorship tiers and pricing
3. Value propositions for sponsors

**Process:**
1. Read `voice-and-style.md` and existing sponsor packets
2. Design as multi-page document (use page breaks)
3. Include: cover, opportunity, tiers, leadership, contact
4. Save to `content/docs/[event]-sponsor-packet.html`

### One-Pagers

**Required inputs:**
1. Topic/program
2. Target audience
3. Key points to convey

**Process:**
1. Single page, scannable format
2. Use visual hierarchy heavily
3. Focus on outcomes and benefits
4. Clear CTA at bottom

---

## Updating Existing Documents

When asked to update a document:

1. **Read the full document first**
2. **Understand the change request** - what specifically needs updating?
3. **Preserve structure and styling** - don't reformat unnecessarily
4. **Update consistently** - if changing a date, check for all date references
5. **Verify accuracy** - cross-reference `ngm-programs.md` for current info

### Common Update Types

**Content updates:**
- Refresh dates and timelines
- Update pricing or tiers
- Add/remove sections
- Update credentials or outcomes

**Styling updates:**
- Apply latest design system
- Fix print formatting
- Improve mobile responsiveness

**Repurposing:**
- Adapt proposal for different client
- Create variant of flyer for different audience
- Generate new sponsor packet from existing template

---

## Quality Checklist

Before finalizing any document:

- [ ] Voice matches NGM tone (confident, specific, outcome-focused)
- [ ] All NGM programs described accurately (check `ngm-programs.md`)
- [ ] Credentials are current and relevant to audience
- [ ] Pricing matches current framework
- [ ] Design follows system (colors, fonts, spacing)
- [ ] HTML renders correctly in browser
- [ ] Prints cleanly to PDF (if applicable)
- [ ] No placeholder text remains
- [ ] Clear CTA with contact info
- [ ] Date and recipient info correct

---

## Anti-Patterns to Avoid

1. **Credential dumping** — Select what's relevant, don't list everything
2. **Generic content** — Every document should feel custom
3. **Salesy language** — Professional confidence, not marketing hype
4. **Feature focus** — Lead with outcomes and transformation
5. **Wall of text** — Use white space, headers, visual hierarchy
6. **Vague pricing** — Be specific about what's included
7. **Weak CTAs** — "Let me know what you think" is not a CTA
8. **Outdated info** — Always verify against `ngm-programs.md`

---

## Usage Examples

### Create a proposal
```
Create a proposal for Acme Health based on our meeting. Here's the transcript: [paste]
```

### Create a flyer
```
Create a 1-page flyer for NGM Commons targeting longevity vendors at conferences.
```

### Update existing document
```
Update the NGM Summit sponsor packet - change the date to October 2026 and add a new "Founding Partner" tier at $25,000.
```

### Repurpose a document
```
Take the Trellis proposal and adapt it for a similar company called MedTech Labs.
```

