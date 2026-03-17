---
activation_code: VISUAL_REGRESSION_V1
phase: 10
version: 1.0.0
description: |
  Validates visual consistency across UI changes using screenshot comparison.
  Uses MCP browser tools for automated screenshot capture and diff analysis.
---

# Visual Regression Validator Skill

## Activation Method

This skill activates when:
- UI changes are ready for visual validation
- E2E testing phase requires visual consistency checks
- Design system updates need visual verification

Activation trigger: `[ACTIVATE:VISUAL_REGRESSION_V1]`

## What This Skill Does

Automates visual regression testing using MCP browser tools:

- **Screenshot capture** across viewports and browsers
- **Baseline comparison** for detecting unintended visual changes
- **Diff generation** highlighting pixel differences
- **Responsive validation** across device sizes
- **Dark mode verification** for theme consistency

## MCP Browser Tools Required

This skill requires the Playwright MCP browser tools:

```yaml
required_tools:
  - browser_navigate: Navigate to pages for testing
  - browser_take_screenshot: Capture full page or element screenshots
  - browser_resize: Test different viewport sizes
  - browser_evaluate: Execute theme switching scripts
```

## Execution Flow

```
Stage 1: Setup
         - Read baseline screenshots from .visual-regression/baselines/
         - Configure viewport matrix (mobile, tablet, desktop)
         - Identify pages/components to test

Stage 2: Capture Current State
         - browser_navigate to each test URL
         - browser_resize for each viewport
         - browser_take_screenshot for each state
         - Store in .visual-regression/current/

Stage 3: Compare & Diff
         - Pixel-by-pixel comparison with baselines
         - Generate diff images highlighting changes
         - Calculate diff percentage per screenshot

Stage 4: Report Generation
         - Create visual regression report
         - Flag screenshots exceeding threshold (default: 0.1%)
         - Generate approval workflow for intentional changes

Stage 5: Decision
         - All diffs < threshold → PASS
         - Any diff > threshold → REQUIRES REVIEW
```

## Viewport Matrix

| Device | Width | Height | Scale |
|--------|-------|--------|-------|
| Mobile S | 320 | 568 | 2x |
| Mobile M | 375 | 667 | 2x |
| Mobile L | 425 | 812 | 3x |
| Tablet | 768 | 1024 | 2x |
| Desktop | 1280 | 800 | 1x |
| Desktop L | 1920 | 1080 | 1x |

## Directory Structure

```
.visual-regression/
├── baselines/           # Approved baseline screenshots
│   ├── desktop/
│   ├── tablet/
│   └── mobile/
├── current/             # Current test run screenshots
├── diffs/               # Generated diff images
└── reports/
    └── visual-regression-report.html
```

## Screenshot Naming Convention

```
{page-name}_{component}_{viewport}_{theme}.png

Examples:
- homepage_hero_desktop_light.png
- login_form_mobile_dark.png
- dashboard_sidebar_tablet_light.png
```

## Threshold Configuration

```json
{
  "globalThreshold": 0.1,
  "pageThresholds": {
    "homepage": 0.05,
    "dashboard": 0.2
  },
  "ignoreRegions": [
    { "page": "dashboard", "selector": ".timestamp" },
    { "page": "profile", "selector": ".avatar" }
  ]
}
```

## Integration with E2E Validator

This skill integrates with `E2E_VALIDATOR_V1`:

1. E2E Validator triggers visual regression after functional tests pass
2. Visual Regression captures screenshots at key workflow points
3. Results feed into production readiness scoring

## Workflow Commands

### Capture New Baselines
```bash
# When intentional UI changes are approved
mv .visual-regression/current/* .visual-regression/baselines/
```

### Run Visual Regression
```bash
# Execute through skill activation
[ACTIVATE:VISUAL_REGRESSION_V1]
```

### Review Diffs
```bash
# Open diff report
open .visual-regression/reports/visual-regression-report.html
```

## Output Signals

| Signal | Condition |
|--------|-----------|
| `VISUAL_REGRESSION_PASSED` | All diffs within threshold |
| `VISUAL_REGRESSION_REVIEW` | Diffs require human approval |
| `VISUAL_REGRESSION_FAILED` | Unexpected visual changes detected |

## Human Gate

Visual regression results requiring review trigger a human gate:

```
╔═══════════════════════════════════════════════════════════════════════╗
║  VISUAL REGRESSION REVIEW REQUIRED                                     ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                        ║
║  Screenshots with differences detected:                                ║
║  • homepage_hero_desktop_light.png (2.3% diff)                        ║
║  • dashboard_chart_tablet_dark.png (1.8% diff)                        ║
║                                                                        ║
║  Review diff images in .visual-regression/diffs/                       ║
║                                                                        ║
║  [A] APPROVE (update baselines)  [R] REJECT (fix UI)                  ║
╚═══════════════════════════════════════════════════════════════════════╝
```
