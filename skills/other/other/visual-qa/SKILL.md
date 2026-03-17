---
name: visual-qa
description: Complete visual QA - screenshots with full-page scroll to trigger animations, then analyze with Claude. Run after CSS/template changes.
allowed-tools: Read, Write, Edit, Bash, Task
---

# Visual QA Skill

Automated visual testing that properly handles GSAP animations by scrolling through the entire page before capturing screenshots.

## Usage

Ask Claude to run visual QA:
- "Run visual QA on the CSR site"
- "Take screenshots of all pages and analyze them"
- "Check the visual state of the website"

## What This Skill Does

1. **Full-Page Scroll** - Scrolls through entire page in increments to trigger all GSAP/ScrollTrigger animations
2. **Multi-Device Screenshots** - Desktop (1920px), Tablet (768px), Mobile (375px)
3. **Parallel Processing** - Uses Haiku sub-agents to analyze multiple pages simultaneously
4. **Visual Analysis** - Reviews screenshots for issues

## Pages Tested

| Page | URL |
|------|-----|
| Home | https://csrdevelopment.com/ |
| About | https://csrdevelopment.com/about/ |
| Portfolio | https://csrdevelopment.com/portfolio/ |
| Contact | https://csrdevelopment.com/contact/ |
| Privacy Policy | https://csrdevelopment.com/privacy-policy/ |
| Terms | https://csrdevelopment.com/terms-of-service/ |

## Screenshot Script

Location: `/root/.claude/skills/visual-qa/screenshot.py`

### Single Page
```bash
python3 /root/.claude/skills/visual-qa/screenshot.py --url https://csrdevelopment.com/about/
```

### All Pages
```bash
python3 /root/.claude/skills/visual-qa/screenshot.py --all
```

### Output
Screenshots saved to: `/home/dev/screenshots/`

## Parallel Analysis with Haiku

When running full visual QA, launch multiple Haiku agents to analyze different pages simultaneously:

```
Agent 1: Analyze Home + About screenshots
Agent 2: Analyze Portfolio + Contact screenshots
Agent 3: Analyze Legal pages screenshots
```

## Visual QA Checklist

### All Pages
- [ ] Header visible and logo centered
- [ ] Menu button works
- [ ] Footer links present
- [ ] No horizontal scroll
- [ ] Text readable at all sizes

### Home Page
- [ ] Hero video/image loaded
- [ ] Hero text visible (not opacity 0)
- [ ] Property cards show with images
- [ ] Animations completed

### About Page
- [ ] Team member photos loaded (not placeholders)
- [ ] Bio text visible
- [ ] Images have grayscale filter

### Portfolio
- [ ] Property grid displays
- [ ] Status badges visible
- [ ] Different images for each property

### Contact
- [ ] Form fields visible
- [ ] Contact info displayed
- [ ] Submit button styled

### Property Detail
- [ ] Hero image loaded
- [ ] Property details sidebar
- [ ] Inquiry form present
