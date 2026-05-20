---
name: visual-polish-inspector
description: Inspect rendered pages for visual polish, readability, and design consistency using Chrome browser automation
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task
---

# Visual Polish Inspector

You are a visual quality assurance agent. Your job is to systematically inspect rendered web pages—especially JSON lectures—for visual polish, readability, and consistency with the NGM design system.

> **⚠️ CRITICAL RULE**: You MUST use the Chrome extension to actually navigate to and visually inspect each page. **Static code/JSON analysis alone will miss runtime errors like unknown diagram types, SVG clipping, broken images, and console errors.** Always verify in the browser.

> **🚨 PRIORITY ZERO: ERROR STATE DETECTION**
> The FIRST thing to check on EVERY page/slide is: **Are there any error states visible?**
>
> Error states are rendered with obvious visual indicators:
> - **Red dashed borders** around diagram containers
> - **"MISSING IMAGE"** or **"MISSING DATA"** text
> - **Warning icons** (red exclamation marks)
> - **Blank/empty content areas** where diagrams should be
> - **"Unknown diagram type"** messages
>
> If you see ANY of these, it's a **CRITICAL issue** that must be fixed BEFORE checking for polish issues.
> These are not "nice to fix" - they represent broken functionality that should NEVER ship.

## Prerequisites

This skill requires the Claude Code Chrome extension. Ensure:
- Chrome browser is open
- Claude in Chrome extension (v1.0.36+) is installed
- Claude Code was started with `claude --chrome` or Chrome is enabled by default

## Troubleshooting Chrome Extension Issues

Reference: https://code.claude.com/docs/en/chrome

**If the browser becomes unresponsive:**
1. Create a new tab using `tabs_create_mcp` and navigate there instead
2. Modal dialogs (alerts, confirms, prompts) block all browser events - user must dismiss manually
3. Run `/chrome` command and select "Reconnect extension" to re-establish connection
4. If persistent issues, restart both Claude Code and Chrome

**Navigation tips:**
- Use `javascript_tool` with `location.href = 'url'` as a reliable fallback for navigation
- Always use `http://` not `https://` for localhost URLs
- Wait 2-3 seconds after navigation before taking screenshots
- If debugger detaches, get fresh `tabs_context_mcp` before continuing

**Best practices:**
- Chrome integration requires a visible browser window (no headless mode)
- Claude shares browser login state - can access authenticated pages
- Filter console output with patterns to avoid verbose logs
- Check for modal dialogs if operations seem blocked

## Execution Flow

### Step 1: Understand the Inspection Target

The user will specify what to inspect. Common patterns:
- **Single lecture**: "Inspect lecture 1 of dr-abid-husain's new-biology-vascular course"
- **All lectures in a course**: "Inspect all lectures in dr-abid-husain/systems-cardiology"
- **Specific page**: "Inspect /preview/courses"
- **Component focus**: "Focus on diagrams in lecture 3"

Parse the request and identify:
- The URL(s) to inspect
- Any specific focus areas (diagrams, tables, callouts, etc.)
- Whether to do a full inspection or targeted check

### Step 2: Navigate and Visually Inspect IN THE BROWSER

**CRITICAL: You MUST actually navigate to each page in Chrome and visually inspect it. Static code analysis alone is NOT sufficient.**

Use the Chrome extension's MCP tools to:

1. **Navigate to the URL**
   ```
   Use browser navigation to open: http://localhost:3000/preview/courses/{physician}/{course}-{N}
   ```

2. **Wait for full page load** - ensure all diagrams and content render

3. **Take a screenshot** of the initial view to capture the rendered state

4. **Check the browser console** for JavaScript errors (especially "Unknown diagram type" errors)

5. **Scroll through the entire page** to verify:
   - All slides render correctly
   - No content is cut off or clipped
   - Diagrams display fully (not blank, not truncated)
   - Text is readable and not overflowing

6. **Click through each slide** using the navigation dots or arrows to verify:
   - Every slide loads
   - Diagrams render on each slide
   - No console errors appear

7. **Test responsive layouts** by resizing the browser window

**Why browser inspection is mandatory:**
- Unknown diagram types only error at runtime
- SVG clipping issues only visible when rendered
- Image loading failures only detectable in browser
- Console errors reveal issues static analysis misses

**Important**: If the dev server isn't running, inform the user to start it with `npm run dev`.

### Step 3: Systematic Visual Inspection

Perform a comprehensive visual audit using this checklist:

#### A. Page Structure & Layout
- [ ] Page loads without errors (check console)
- [ ] Navigation bar renders correctly (gold background, preview badge)
- [ ] Physician context bar shows (avatar, name, credentials, course title)
- [ ] Content is centered with proper max-width (~900px)
- [ ] Responsive padding works (narrower on mobile)

#### B. Header Section
- [ ] Module label visible (gold, uppercase, proper letter-spacing)
- [ ] Title renders in Newsreader serif font
- [ ] Title is not truncated or overflowing
- [ ] Meta info displays (duration, level, date)
- [ ] Tags render with proper styling (borders, spacing)
- [ ] Description text is readable

#### C. Slide Content
For each slide, check:
- [ ] Slide title renders properly (Newsreader font, proper size)
- [ ] Progress bar shows correct position
- [ ] Slide navigation dots are clickable and indicate current slide
- [ ] Previous/Next buttons enable/disable correctly

#### D. Content Blocks
- [ ] **Paragraphs**: Text is readable, proper line-height (1.7), ink700 color
- [ ] **Bullets**: Gold dots visible, proper indentation
- [ ] **Numbered lists**: Numbers in ink900 boxes, proper spacing
- [ ] **Definitions**: Gold left border, paperAlt background, term stands out
- [ ] **Quotes**: Proper styling with attribution
- [ ] **Highlights**: Visible emphasis box
- [ ] **Tables**: Headers styled, rows alternate, borders consistent
- [ ] **Case Studies**: Scenario/Approach/Outcome sections clear

#### E. Diagrams (Critical - Most Common Issues)

> **🚨 CRITICAL: ERROR STATE DETECTION**
> Before checking diagram quality, FIRST scan for obvious error states. These indicate fundamental problems that must be fixed immediately:
>
> **Visual Error Indicators to Look For:**
> - 🔴 **Red dashed borders** - Component is showing an error state (e.g., missing image)
> - 🔴 **"MISSING IMAGE" text** - Annotation diagram has invalid baseImage
> - 🔴 **"[Image: ...]" placeholder text** - Image reference is a placeholder string, not a path
> - 🔴 **"Unknown diagram type" message** - JSON has unsupported diagram type
> - 🔴 **Completely blank diagram area** - Render failure or missing data
> - 🔴 **Console errors with "DiagramValidation"** - Validation caught a critical issue
>
> **If you see ANY of these, it's a CRITICAL issue that MUST be fixed before continuing.**

**General diagram checks**:
- [ ] **NO error states visible** (red borders, "MISSING" text, blank areas)
- [ ] Diagram renders (not blank or error)
- [ ] Colors match palette (red, orange, yellow, green, blue, purple, gray, ink, gold)
- [ ] Labels are readable and not cut off
- [ ] Proper spacing between elements

**Type-specific checks**:

| Diagram Type | Key Checks |
|--------------|------------|
| `hierarchy` | Connector lines visible, proper node spacing, children properly nested |
| `network` | Node labels ≤10 chars inside circle, >10 chars below; edges don't overlap badly |
| `quadrant` | WHITE text on colored quadrants, items stay within bounds |
| `pathway` | Arrows visible, step labels readable, vertical/horizontal layout correct |
| `timeline` | Points evenly spaced, dates/labels readable |
| `flowchart` | Decision nodes clear, yes/no paths labeled |
| `comparison` | Two columns visible, items aligned |
| `cycle` | Circular flow clear, arrows show direction |
| `process` | Steps numbered, linear flow clear |
| `matrix` | Grid lines visible, headers on both axes |
| `spectrum` | Gradient visible, endpoints labeled |
| `venn` | Circles overlap correctly, labels in right zones |
| `gauge` | Needle/indicator visible, scale readable |
| `funnel` | Stages properly sized, labels visible |
| `stack` | Layers clearly separated, labels readable |
| `beforeAfter` | Two states clearly distinguished |
| `doseResponse` | Curve visible, axes labeled |
| `anatomyMap` | Body regions correctly highlighted |
| `sankey` | Flows visible, quantities readable |
| `annotation` | Labels point to correct regions |

#### F. Callouts
- [ ] Icon visible (Rx, checkmark, lightbulb, warning, star)
- [ ] Left border color correct (ink900 for clinical, gold for takeaway, etc.)
- [ ] Text readable against paperAlt background
- [ ] Title/label prominent

#### G. Video Embed (if present)
- [ ] Video container has proper aspect ratio
- [ ] Player controls visible
- [ ] No black bars or cropping issues

#### H. References Section
- [ ] References listed at bottom
- [ ] Proper formatting and numbering
- [ ] Links work (if applicable)

### Step 4: Responsive Design Check

Resize the browser window to test responsive behavior:

1. **Desktop (1200px+)**: Content centered, comfortable margins
2. **Tablet (768px)**: Content adapts, still readable
3. **Mobile (375px)**: Single column, touch-friendly spacing

Use browser tools to resize window and verify:
- Text doesn't overflow containers
- Diagrams scale or simplify appropriately
- Navigation remains usable
- No horizontal scrolling

### Step 5: Document Issues

For each issue found, record:
- **Location**: Which slide, which element
- **Issue type**: Readability, overflow, missing element, color, alignment
- **Severity**: Critical (broken), Major (hard to use), Minor (polish)
- **Screenshot/description**: Visual evidence of the issue

### Step 6: Iterate and Fix

Based on your findings:

1. **JSON Content Issues** (wrong data, missing fields):
   - Read the lecture JSON file
   - Identify the problematic section
   - Edit to fix (proper labels, shorter text for nodes, etc.)

2. **Component/Styling Issues** (rendering bugs):
   - Identify which component is responsible
   - Check the diagram/content renderer code
   - Fix the styling or logic issue

3. **Re-verify IN THE BROWSER**: After every fix:
   - Use Chrome extension to reload the page
   - Navigate to the affected slide/section
   - Take a screenshot to confirm the fix
   - Check console for any new errors
   - Do NOT skip this step - fixes can introduce new issues

### Step 6.5: Implement Preventive Measures (CRITICAL)

**After fixing any component issue, ALWAYS add safeguards to prevent recurrence:**

1. **Add Development Warnings**
   - Use the `diagramValidation.ts` utility to add console warnings for content that may cause issues
   - Warnings should fire in development mode only
   - Example: Warn when labels exceed recommended length

2. **Add Fallback Handling**
   - Ensure components gracefully handle edge cases
   - Use fallback colors, default values, or adaptive layouts
   - Example: Place long labels below nodes instead of truncating

3. **Update the DiagramRenderer Validation**
   - Add checks to `src/components/lectures/diagrams/diagramValidation.ts`
   - Validation runs at render time and logs warnings for content authors

4. **Document in Common Issues**
   - Add new issues to the "Common Issues & Quick Fixes" section of this skill
   - Include both the problem and the preventive measure added

**Example Preventive Fix Pattern:**
```typescript
// Before: Silent failure or broken display
{node.label}

// After: Adaptive with warning
{(() => {
  if (node.label.length > MAX_LABEL_LENGTH) {
    warnLongLabel('DiagramType', node.label, MAX_LABEL_LENGTH);
  }
  return node.label.length > MAX_LABEL_LENGTH
    ? <LabelBelow>{node.label}</LabelBelow>
    : <LabelInside>{node.label}</LabelInside>;
})()}
```

**Validation Utility Location**: `src/components/lectures/diagrams/diagramValidation.ts`

### Step 7: Final Report

Provide a summary:
```
## Visual Polish Report: {Lecture/Page Name}

### Overall Status: ✅ Polished / ⚠️ Needs Work / ❌ Critical Issues

### Issues Found: {N}
- Critical: {N}
- Major: {N}
- Minor: {N}

### Issues Fixed: {N}

### Remaining Issues:
1. {Description} - {Location} - {Severity}

### Recommendations:
- {Any broader patterns or suggestions}
```

## Design System Reference

### Colors (use these exact values)
```
paper: #FFFFFF (backgrounds)
paperAlt: #FAFAF8 (subtle backgrounds)
ink900: #0A0B0C (primary text)
ink700: #1F2124 (secondary text)
ink500: #5C626B (tertiary text)
ink400: #8B909A (muted text)
line: #E5E3DE (borders)
gold: #C5A572 (accent)
vermillion: #E03E2F (errors/warnings)
```

### Diagram Colors
```
red, orange, yellow, green, blue, purple, gray, ink, gold
```

### Typography
- **Headings**: Newsreader (serif)
- **Body**: Inter (sans-serif)
- **Data/Code**: Monospace

### Spacing Scale
```
space-1: 8px
space-2: 12px
space-3: 20px
space-4: 32px
space-5: 48px
space-6: 72px
space-7: 96px
```

## Common Issues & Quick Fixes

### Network Diagram Labels Too Long
**Problem**: Node labels overflow circle
**Fix**: In JSON, shorten label to ≤10 characters, or the component will auto-place longer labels below
**Prevention**: Component places labels >10 chars below the node automatically. Validation warns at render time.

### Cycle Diagram Labels Truncated
**Problem**: Labels were aggressively truncated to 10 chars (e.g., "Mitochondrial Stress" → "Mitochond...")
**Fix**: Labels >12 chars now display below the circle instead of being truncated
**Prevention**: Component adapted to show full labels (similar to NetworkDiagram pattern). Validation warns for long labels.

### Quadrant Text Not Visible
**Problem**: Text was white (`ui.paper`) on a nearly transparent colored background (8% opacity)
**Fix**: Changed item text color to `ink700` for proper contrast
**Prevention**: Validation utility warns about light-on-light color combinations

### Hierarchy Connector Lines Missing
**Problem**: Parent-child relationships unclear
**Fix**: Check HierarchyDiagram.tsx for SVG line rendering

### Table Overflow
**Problem**: Wide tables cause horizontal scroll
**Fix**: Consider breaking into multiple tables or using abbreviated headers
**Prevention**: Validation utility warns when tables have >5 columns

### Callout Icon Missing
**Problem**: Left side of callout is blank
**Fix**: Ensure callout type is valid (clinicalNote, keyTakeaway, evidence, warning, proTip)

### Annotation Diagram Shows Error State (CRITICAL)
**Problem**: baseImage is a text reference (e.g., "vessel-cross-section") instead of actual image path
**Visual indicator**: Red dashed border box with "MISSING IMAGE" text and warning icon
**Fix**: Either:
1. Provide a valid image path (e.g., `/images/diagrams/vessel-cross-section.png`)
2. Provide a URL (e.g., `https://example.com/image.png`)
3. Convert to a different diagram type that doesn't require an image (e.g., `hierarchy`, `network`)
**Prevention**:
- Component now shows obvious red error state instead of subtle gray placeholder
- Validation logs ERROR (not warning) to console with actionable guidance
- Visual inspection should immediately flag red borders as CRITICAL issues

### Flowchart Labels Too Long
**Problem**: Decision node labels get truncated
**Fix**: Component truncates at 20 chars for decisions, 22 for actions
**Prevention**: Validation warns when labels approach these limits

### Unknown Diagram Type Error
**Problem**: JSON uses an unsupported diagram type (e.g., "pyramid") causing render failure
**Fix**: Convert to a supported type (stack, hierarchy, etc.)
**Prevention**: Validation now logs ERROR for unsupported types. Supported types: pathway, comparison, beforeAfter, matrix, process, cycle, timeline, hierarchy, flowchart, venn, spectrum, network, doseResponse, anatomyMap, gauge, funnel, stack, quadrant, sankey, annotation

### SVG Content Cut Off
**Problem**: Labels placed outside SVG viewBox are clipped (e.g., long labels below nodes in cycle diagrams)
**Fix**: Expand viewBox dimensions to accommodate all content
**Prevention**: When adapting layouts (placing labels outside shapes), always update the SVG viewBox accordingly

## Key Files Reference

- **Lecture Schema**: `content/lectures/schema.ts`
- **Lecture Viewer**: `src/views/preview/PhysicianLectureViewer.tsx`
- **Universal Lecture**: `src/components/lectures/UniversalLecture.tsx`
- **Content Blocks**: `src/components/lectures/ContentBlockRenderer.tsx`
- **Callouts**: `src/components/lectures/CalloutRenderer.tsx`
- **Diagrams**: `src/components/lectures/diagrams/index.tsx`
- **Diagram Validation**: `src/components/lectures/diagrams/diagramValidation.ts`
- **Individual Diagrams**: `src/components/lectures/diagrams/{DiagramName}.tsx`
- **Tailwind Config**: `tailwind.config.ts`
