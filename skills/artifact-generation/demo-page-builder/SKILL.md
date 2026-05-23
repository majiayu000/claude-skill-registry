---
name: demo-page-builder
description: Generate branded demo landing pages for real estate agencies
---

# Demo Page Builder Skill

You are an expert landing page designer. Create stunning, conversion-focused demo pages showcasing Voqo AI voice agent capabilities.

## Design Philosophy

- **Brand Authenticity**: Page feels like it belongs to the agency
- **Professional Polish**: Premium look that impresses decision-makers
- **Clear Value Prop**: Immediately show why they need Voqo
- **Single CTA Focus**: One action - call the demo number
- **Mobile First**: Perfect on phones (agents browse mobile)
- **Modern & Clean**: Smooth animations, elegant transitions, contemporary design patterns

## Technical Requirements

- Single HTML file, fully self-contained
- Tailwind CSS via CDN
- Minimal JavaScript (call registration + polling only)
- No external dependencies beyond CDN

## Page Design Requirements

Create a beautiful, modern landing page with these sections. Design freely - use your creativity for layout, animations, and visual hierarchy. Make it feel premium.

### 1. Header
- Agency logo + "× Voqo AI" co-branding
- Sticky navigation
- Prominent "Call Demo" button
- Clean, minimal design

### 2. Hero Section
- Bold headline: convey "Never miss another enquiry"
- Subheadline personalized with agency name
- Large, eye-catching CTA button with phone icon
- Use agency brand colors as gradient or solid background
- Consider subtle animations (fade-in, gentle pulse on CTA)

### 3. Pain Points Section
- Title: "Why [Agency Name] Needs This"
- 3 cards highlighting specific pain points from agency data
- Generate cards dynamically based on:
  - High listing count → call volume pain
  - No after-hours → missed evening/weekend calls
  - Has PM → rental enquiry overload
  - Small team + many listings → understaffed
  - No chat → web lead capture gap
- Use icons, clean typography, subtle hover effects

### 4. ROI Calculator Section
- Side-by-side comparison: "The Problem" vs "The Solution"
- Calculate and display:
  - Active listings (from data)
  - Est. calls/month (listings × 8)
  - Est. missed calls (calls × 0.35)
  - Lost revenue/month (missed × $150)
  - Voqo cost ($199/mo)
  - Revenue saved
  - ROI multiplier
- Visual contrast between red (problem) and green (solution)
- Make the ROI number prominent and satisfying

### 5. How It Works Section
- 3 steps with numbered indicators:
  1. Caller dials number → AI answers when busy/after hours
  2. AI handles conversation → understands property needs
  3. Instant follow-up → personalized recommendations sent
- Consider timeline or connected step design
- Keep explanations concise

### 6. Final CTA Section
- Compelling headline: "Experience It Yourself"
- Large call button with phone number
- Agency brand colors
- Create urgency without being pushy

### 7. Footer
- "Demo powered by Voqo AI"
- "AI Voice Agents for Real Estate"
- Minimal, professional

### 8. Recent Calls Section
- Add a section titled "Recent Calls"
- Fetch `/api/agency-calls?agency={id}` on page load
- Render a list of call entries with:
  - callerName (fallback to "Caller" if missing)
  - summary (fallback to "Call completed")
  - link to pageUrl
- If no calls, show a friendly empty state

### 9. Required JavaScript Functionality

Embed this functionality (implement cleanly):

```javascript
// Agency data object with: id, name, location, phone, teamSize, listingCount, hasPropertyManagement

// registerCall() function:
// - POST to /api/register-call with agencyData + timestamp
// - On success, start pollForResults()

// pollForResults() function:
// - Poll /api/call-status?agency={id} every 3 seconds
// - When status=completed && pageUrl exists, show result notification
// - Stop after 5 minutes

// showCallResult(data) function:
// - Display success notification with link to pageUrl
// - Smooth scroll to notification

// loadRecentCalls() function:
// - GET /api/agency-calls?agency={id}
// - Render call list into "Recent Calls" section
// - Show empty state if no calls
```

### Results Container
- Hidden initially
- When call completes, show elegant success notification
- Link to personalized post-call page
- Smooth animation on appearance

## Data Mapping

Use agency data to populate:
- agency.name → agency name throughout
- agency.id → for API calls
- agency.address → extract suburb/city for location
- agency.phone → agency contact
- agency.branding.logoUrl → header logo
- agency.branding.primaryColor → brand color theming
- agency.branding.secondaryColor → gradients, accents
- agency.metrics.listingCount → ROI calculations
- agency.metrics.teamSize → pain cards if relevant
- agency.metrics.hasPropertyManagement → pain cards
- agency.metrics.hasAfterHoursNumber → pain cards
- agency.metrics.hasChatWidget → pain cards
- agency.painReasons → pain card content

Demo phone number comes from environment: NEXT_PUBLIC_DEMO_PHONE

## Output

Save to: `demoHtmlPath` (absolute path provided in the prompt)

## Quality Checklist

- Logo loads correctly
- Colors are visible, not clashing
- Phone number clickable (tel: link)
- Pain points relevant to this agency
- ROI numbers calculated correctly
- Fully responsive
- No JavaScript errors
- Animations smooth, not distracting
- Agency data embedded in script
