---
name: creating-demo
description: |
  Creates a demo presentation by building a content outline, verifying UI
  claims via browser, and generating a PPTX file. Use when a QA engineer
  wants to create a demo, build a demo, make demo slides, or generate a
  demo presentation for a feature.
disable-model-invocation: true
tools:
  - playwright-mcp:browser_navigate
  - playwright-mcp:browser_snapshot
  - playwright-mcp:browser_take_screenshot
---

# creating-demo

Creates a demo presentation: builds a content outline with speaker script, verifies UI claims via browser, and generates a PPTX file.

## Progress Checklist

Copy and track your progress:

```
- [ ] Step 1: Read project context
- [ ] Step 2: Create 6-slide outline with co-located speaker script
- [ ] Step 3: Browser-verify all UI claims, capture screenshots, fix mismatches
- [ ] Validate: Verified vs corrected claims count + screenshot list + new slide count
- [ ] Step 4: Generate PPTX file
- [ ] Validate: PPTX path + slide count + any [placeholder] text remaining
```

## Steps

### Step 1: Read Project Context

Read these files for context:
- `README.md` — feature summary and ticket ID
- `test_plan/README.md` — what was tested
- `test_cases/README.md` — test scenario overview
- `confluence/*.md` — HLD and design documentation

### Step 2: Create 6-Slide Outline

Run `/pm-demo-content` to create `demo/Demo_Showcase_Content.md` with 6 slides:

1. **Title** — ticket ID + feature name + one-line subtitle
2. **What We Built** — 3-4 user-facing capabilities (bullets + script)
3. **The Problem** — 3-4 user pain points (bullets + script)
4. **What's New** — UI changes and navigation steps (bullets + script)
5. **Demo** — screenshot placeholder (script: observational phrases)
6. **Questions** — Q&A closing

Each slide has co-located `**Bullets:**` and `**Script:**` sections.

### Step 3: Browser Verification

Run `/pm-demo-review` to verify UI claims via browser:
1. Navigate to the documented UI path
2. Compare actual UI against documented claims (labels, menu names, field names)
3. Capture screenshots: `demo/screenshots/NN_Description.png`
4. Fix any mismatches in Slides 1-4
5. Expand Slide 5 into per-step demo slides with actual screenshots

**MCP tools:** `playwright-mcp:browser_navigate`, `playwright-mcp:browser_snapshot`, `playwright-mcp:browser_take_screenshot`

### Validate

Report:
- Verified claims: N matched, N corrected
- Screenshots captured: list of files in `demo/screenshots/`
- Slide count: original 6 → expanded N slides

### Step 4: Generate PPTX

Run `/pm-demo-ppt` to generate the PPTX file from the verified content:

```bash
python3 scripts/md_to_pptx.py [PROJECT_PATH]/demo/Demo_Showcase_Content.md \
  --template docs/templates/Demo_Template.pptx
```

### Validate

Report:
- PPTX file path
- Number of slides generated
- Flag any remaining `[placeholder]` text

## Expected Input

Path to project folder containing README.md and test plan/test case files.

## Next Step

After creating the demo, run `/drafting-review-email` to generate the demo share email.
