# 02 - Agency Researcher Skill

## Overview

This skill instructs Claude Code to find and qualify real estate agencies in a given suburb. It uses web search and browser automation to gather comprehensive agency data.

---

## Skill File Location

```
.claude/skills/agency-researcher/SKILL.md
```

---

## SKILL.md Content

```markdown
---
name: agency-researcher
description: Find and qualify real estate agencies in a given suburb
---

# Agency Researcher Skill

You are an expert real estate industry researcher. Your task is to find, analyze, and qualify real estate agencies in Australian suburbs.

## Your Mission

Given a suburb name, find the top real estate agencies operating in that area and gather comprehensive data about each one. This data will be used to generate personalized demo pages.

## Research Process

### Step 1: Initial Search

Search for real estate agencies in the target suburb:

```
Search queries to use:
- "[suburb] real estate agents"
- "[suburb] real estate agencies"
- "best real estate agents [suburb] Sydney"
- "property agents [suburb]"
```

Use WebSearch tool to find agencies. Aim to identify 8-12 agencies initially.

### Step 2: For Each Agency, Gather Data

Visit each agency's website using Chrome browser tools and extract:

#### Basic Information
- **Agency Name**: Official business name
- **Website URL**: Main website
- **Phone Number**: Primary contact (look in header, footer, contact page)
- **Email**: General enquiry email
- **Address**: Physical office location

#### Branding (CRITICAL - needed for demo pages)
- **Logo URL**: Direct URL to logo image
  - Check: header, footer, about page
  - Right-click logo → "Copy image address"
  - Prefer PNG or SVG, fallback to JPG
  - Must be publicly accessible URL

- **Primary Brand Color**: Main color used in branding
  - Check: header background, buttons, headings
  - Extract hex code (e.g., #1a365d)
  - Use browser dev tools if needed: inspect element → computed styles

- **Secondary Color**: Accent/secondary color
  - Check: hover states, borders, secondary buttons
  - Extract hex code

#### Team & Size Indicators
- **Team Size**: Number of agents
  - Check "Our Team" or "Meet the Team" page
  - Count agent profiles
  - If no team page, estimate from listings ("Listed by X agents")

- **Principal/Owner Name**: Decision maker if findable
  - Look for "Principal", "Director", "Owner" in team page
  - Note their name for personalization

#### Listing Activity
- **Active Listings Count**: Current properties for sale/rent
  - Check "Properties" or "Listings" page
  - Count or note the displayed total
  - Note mix of sales vs rentals if visible

- **Has Property Management**: Do they offer PM services?
  - Check services page
  - Look for "Property Management", "Rentals", "Landlords"
  - Boolean: true/false

#### Current Solutions (Pain Indicators)
- **Has After-Hours Number**: Do they have 24/7 contact?
  - Check contact page for "after hours", "emergency", "24/7"
  - If only business hours listed = false

- **Has Chat Widget**: Live chat on website?
  - Check for chat bubble/widget on homepage
  - Look for Intercom, Drift, LiveChat, etc.
  - Boolean: true/false

- **Has Online Booking**: Can visitors book inspections online?
  - Check listing pages for booking buttons
  - Boolean: true/false

#### Review Analysis (Optional but valuable)
- Search Google for "[Agency Name] reviews"
- Check Google Business Profile rating
- Note any reviews mentioning:
  - "couldn't reach", "didn't answer", "no response"
  - These indicate communication pain points

### Step 3: Calculate Pain Score

For each agency, calculate a "pain score" (0-100) indicating likelihood to need Voqo:

```
Pain Score Formula:

Base Score: 0

+ High Listing Volume:
  - 30+ listings: +20 points
  - 20-29 listings: +15 points
  - 10-19 listings: +10 points

+ Has Property Management: +25 points
  (PM means more after-hours calls)

+ Understaffed (high volume, small team):
  - <5 agents AND 20+ listings: +20 points
  - <3 agents AND 10+ listings: +15 points

+ No After-Hours Solution: +15 points

+ No Chat Widget: +10 points

+ No Online Booking: +5 points

+ Bad Review Signals: +10 points
  (If reviews mention communication issues)

Maximum possible: 100 points
```

### Step 4: Generate Pain Reasons

For each agency, create a list of specific pain points:

```
Examples:
- "45 active listings generating high call volume"
- "Team of only 4 agents managing 30+ properties"
- "No after-hours contact solution"
- "Property management adds rental enquiries"
- "No chat widget to capture web leads"
```

### Step 5: Output Format

Save results to `/data/agencies/[suburb-slug].json`:

```json
{
  "suburb": "Surry Hills",
  "searchedAt": "2025-01-15T10:30:00Z",
  "agencies": [
    {
      "id": "ray-white-surry-hills",
      "name": "Ray White Surry Hills",
      "website": "https://raywhitesurryhills.com.au",
      "phone": "+61 2 9361 6000",
      "email": "surryhills.nsw@raywhite.com",
      "address": "123 Crown Street, Surry Hills NSW 2010",

      "branding": {
        "logoUrl": "https://raywhitesurryhills.com.au/logo.png",
        "primaryColor": "#ffe512",
        "secondaryColor": "#1a1a1a"
      },

      "metrics": {
        "teamSize": 6,
        "listingCount": 45,
        "hasPropertyManagement": true,
        "hasAfterHoursNumber": false,
        "hasChatWidget": false,
        "hasOnlineBooking": true,
        "principalName": "John Smith"
      },

      "painScore": 87,
      "painReasons": [
        "45 active listings generating high call volume",
        "No after-hours contact solution",
        "Property management adds rental enquiries",
        "No chat widget to capture web leads"
      ],

      "notes": "Major franchise, likely high-quality lead"
    }
  ]
}
```

Also save individual agency files to `/data/agencies/[agency-id].json` for quick lookup.

## Quality Guidelines

### Logo URL Validation
- Must be direct image URL (ends in .png, .jpg, .svg, or served with image content-type)
- Must be publicly accessible (test in incognito)
- If logo not findable, use placeholder: leave field as null

### Color Extraction
- Use actual hex values, not color names
- Verify colors are visible (not white on white)
- Primary color should be distinctive brand color

### Data Accuracy
- Double-check phone numbers (should start with +61 or 02/03/07/08)
- Verify website URLs are correct
- Count listings manually if automated count unavailable

### Handling Missing Data
- If data unavailable, use null not empty string
- Note in "notes" field what couldn't be found
- Don't make up data

## Example Usage

When invoked with prompt:
```
"Research real estate agencies in Surry Hills, Sydney. Find top 10 agencies and gather full data for each."
```

Execute the full research process and save results to:
- `/data/agencies/surry-hills.json` (full list)
- `/data/agencies/ray-white-surry-hills.json` (individual)
- `/data/agencies/lj-hooker-surry-hills.json` (individual)
- etc.

Return summary:
```
Found 10 agencies in Surry Hills:
1. Ray White Surry Hills - Pain Score: 87
2. LJ Hooker Darlinghurst - Pain Score: 82
3. ...

Data saved to /data/agencies/surry-hills.json
```
```

---

## Invocation from Next.js

The API route `/api/search` will invoke Claude Code with this skill:

```typescript
// Pseudocode for API route
async function searchAgencies(suburb: string) {
  // Invoke Claude Code with the skill
  const result = await invokeClaudeCode({
    prompt: `Use the agency-researcher skill to find and qualify real estate agencies in ${suburb}, Sydney. Find top 10 agencies and save results to /data/agencies/${slugify(suburb)}.json`,
    tools: ['WebSearch', 'WebFetch', 'Read', 'Write', 'Bash', 'Glob'],
    permissionMode: 'bypassPermissions',
    skills: ['agency-researcher']
  });

  // Read results from saved file
  const agencies = await readFile(`/data/agencies/${slugify(suburb)}.json`);
  return JSON.parse(agencies);
}
```

---

## Expected Output Quality

A high-quality agency research should include:

1. **8-10 agencies** from the suburb
2. **Complete branding** for at least 80% (logo, colors)
3. **Accurate metrics** (team size, listings)
4. **Calculated pain scores** with reasoning
5. **Proper JSON format** for downstream use

---

## Troubleshooting

### Can't find logo URL
- Try right-clicking logo in Chrome → Copy image address
- Check page source for og:image meta tag
- Look in favicon/apple-touch-icon as fallback
- Check brand guidelines page if exists

### Can't determine colors
- Use Chrome DevTools → pick element → Computed styles
- Look for CSS variables (--primary-color)
- Check stylesheets for brand colors
- Screenshot and use color picker tool

### Website blocks scraping
- Try using WebFetch with different user agent
- Check if site has API or feed
- Note in data that full scraping wasn't possible
- Gather what you can from Google Business listing

### Team size unclear
- Count agent profiles on team page
- Check "our agents" or "meet the team"
- Look at recent listings for unique agent names
- Estimate from LinkedIn company page
