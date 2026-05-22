---
name: visual-iteration
description: "Self-scoring visual feedback loop for web UI polish. Use when user says 'iterate on design', 'polish UI', 'make it look good', '10/10', or 'visual loop'."
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, mcp__playwright__*
---

# visual-iteration (ONE_SHOT v6.0)

Self-scoring visual feedback loop for web UI development.

## When To Use

- User says "iterate on design", "polish the UI", "make it look good"
- User says "visual loop", "screenshot loop", "design until 10/10"
- User requests UI improvements on a running web app
- After initial implementation, before PR/deploy

## Requirements

1. **Playwright MCP server configured** - check with `mcp__playwright__browser_navigate`
2. **Dev server running** - app must be accessible at a URL
3. **Target page/component identified** - know what to screenshot

## Pre-Flight Check

Before starting the loop:

```
1. Verify Playwright MCP is available
2. Confirm dev server URL (ask if unclear)
3. Identify target page/route to iterate on
4. Establish criteria (from spec or ask user)
```

If Playwright MCP is not available:
> "Visual iteration requires Playwright MCP. Add to your claude_desktop_config.json or .mcp.json"

## The Loop

```
┌─────────────────────────────────────────┐
│  1. IMPLEMENT change                    │
├─────────────────────────────────────────┤
│  2. NAVIGATE to page                    │
│     mcp__playwright__browser_navigate   │
├─────────────────────────────────────────┤
│  3. SCREENSHOT full page                │
│     mcp__playwright__browser_screenshot │
├─────────────────────────────────────────┤
│  4. ASSESS against criteria             │
│     Score: X/10                         │
│     Issues: [list specific problems]    │
├─────────────────────────────────────────┤
│  5. DECIDE                              │
│     If 10/10 OR user threshold → EXIT   │
│     If < threshold → LOOP to step 1     │
└─────────────────────────────────────────┘
```

## Assessment Criteria

Default criteria (override with spec or user input):

| Criterion | Weight | What to Check |
|-----------|--------|---------------|
| Visual hierarchy | 2 | Clear focal points, logical flow |
| Spacing/whitespace | 2 | Consistent margins, breathing room |
| Typography | 1 | Readable, appropriate sizes |
| Color/contrast | 2 | Accessible, intentional palette |
| Alignment | 1 | Grid consistency, no jank |
| Responsiveness | 1 | Works at viewport size |
| Polish | 1 | No rough edges, loading states |

**Score calculation:** Sum of (criterion score 0-1) × weight, normalized to 10

## State Tracking

Track across iterations:

```markdown
## Visual Iteration Log

**Target:** /dashboard
**Threshold:** 10/10
**Criteria:** [from spec or defaults]

### Iteration 1
- Score: 5/10
- Issues:
  - Header cramped (spacing: 0.3)
  - CTA doesn't pop (contrast: 0.4)
  - Cards misaligned (alignment: 0.5)
- Changes made: Added padding, increased button contrast

### Iteration 2
- Score: 7/10
- Issues:
  - Cards still slightly off
  - Mobile nav hidden
- Changes made: Fixed grid, added hamburger menu

### Iteration 3
- Score: 10/10
- All criteria met
```

## MCP Tool Usage

### Navigate to page
```
mcp__playwright__browser_navigate
  url: "http://localhost:3000/target-page"
```

### Take screenshot
```
mcp__playwright__browser_screenshot
  name: "iteration-1"
  fullPage: true
```

### Check element (optional)
```
mcp__playwright__browser_snapshot
  # Get accessibility tree for specific checks
```

## Exit Conditions

Stop iterating when:
1. **Score reaches threshold** (default 10/10, user can set lower)
2. **User says stop** ("good enough", "ship it", "stop iterating")
3. **Max iterations reached** (default 10, prevents infinite loops)
4. **Diminishing returns** (score plateaus for 3+ iterations)

## User Communication

After each iteration, report:
```
Iteration 3/10 | Score: 7/10 | +2 from last

Fixed:
  ✓ Header spacing
  ✓ Button contrast

Remaining:
  ✗ Card alignment (affects 1 point)
  ✗ Mobile nav (affects 1 point)

Continue iterating? [Y/n]
```

## Integration with front-door

When front-door interview captures:
- `visual_polish: true`
- Project type C (Web) or F (AI Web)

Front-door should note: "Use `/visual-iteration` after implementation for UI polish"

## Quick Start

User: "iterate on the homepage design until it's 10/10"

```
1. Check Playwright MCP available → ✓
2. Dev server at http://localhost:3000 → ✓
3. Target: / (homepage)
4. Criteria: defaults
5. Threshold: 10/10

Starting visual iteration loop...
```

## Anti-Patterns

- Iterating without clear criteria (ask first)
- Changing too much per iteration (small increments)
- Ignoring user feedback mid-loop
- Not tracking what changed between iterations
- Optimizing for score vs actual UX

## Keywords

visual-iteration, visual loop, screenshot, design, polish, UI, 10/10, iterate design, make it look good, playwright, assessment, self-score
