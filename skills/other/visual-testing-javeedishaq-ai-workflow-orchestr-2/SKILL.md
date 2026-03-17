---
name: "visual-testing"
description: "Run the app locally and take screenshots using Puppeteer to verify UI changes; use when validating demo pages, checking visual regressions, or capturing UI state for analysis"
version: "1.0.0"
last_updated: "2025-12-14"
---

# Visual Testing

Take screenshots of the running app to verify UI changes visually.

## When to Use This Skill

Use this skill when:
- Verifying visual changes to demo/showcase pages
- Capturing screenshots for UI review
- Debugging layout or styling issues
- Testing demo component interactions
- Checking cursor alignment in interactive demos

## Quick Start

```bash
# Check dev server status
./.claude/skills/visual-testing/scripts/visual-test.sh status

# Start dev server if needed
./.claude/skills/visual-testing/scripts/visual-test.sh start

# Screenshot a demo slide with debug markers
./.claude/skills/visual-testing/scripts/visual-test.sh demo cast-assignment --debug

# View the screenshot (Claude can read images)
# Path: /tmp/ballee-screenshots/demo-cast-assignment-TIMESTAMP.png
```

## Commands

| Command | Description |
|---------|-------------|
| `status` | Check if dev server is running on port 3012 |
| `start` | Start dev server in background |
| `stop` | Stop dev server |
| `screenshot <url>` | Take screenshot of any URL |
| `demo [slide-id]` | Screenshot demo showcase (optional slide) |
| `demo-all` | Screenshot all demo slides |
| `list-slides` | List available demo slide IDs |

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--debug` | Add `?debug=true` to URL (shows target markers) | false |
| `--viewport WxH` | Set viewport dimensions | 1200x900 |
| `--name <name>` | Custom screenshot filename | auto-generated |
| `--full-page` | Capture full scrollable height | false |
| `--wait <ms>` | Extra wait time after page load | 2000 |

## Demo Slide IDs

| ID | Interactive Demo |
|----|------------------|
| `cast-assignment` | CastAssignmentDemo |
| `contract-acceptance` | ContractAcceptanceDemo |
| `event-creation` | EventCreationDemo |
| `hire-order-view` | HireOrderViewDemo |
| `invoice-download` | InvoiceDownloadDemo |
| `invoice-validate` | InvoiceValidateDemo |
| `reimbursement-upload` | ReimbursementUploadDemo |

## Screenshot Output

Screenshots are saved to: `/tmp/ballee-screenshots/`

Naming pattern:
- Demo: `demo-{slide-id}-{timestamp}.png`
- Custom: `{custom-name}.png`
- URL: `screenshot-{timestamp}.png`

## Example Workflows

### Verify Demo After Coordinate Changes

```bash
# 1. Ensure server is running
./.claude/skills/visual-testing/scripts/visual-test.sh status

# 2. Screenshot the changed slide with debug markers
./.claude/skills/visual-testing/scripts/visual-test.sh demo cast-assignment --debug

# 3. Read the screenshot to verify cursor alignment
# Use Claude's Read tool on /tmp/ballee-screenshots/demo-cast-assignment-*.png
```

### Capture All Demo States

```bash
# Screenshot all demo slides for full review
./.claude/skills/visual-testing/scripts/visual-test.sh demo-all --debug

# Screenshots saved to /tmp/ballee-screenshots/
```

### Custom Page Screenshot

```bash
# Screenshot any page
./.claude/skills/visual-testing/scripts/visual-test.sh screenshot \
  http://localhost:3012/admin/events \
  --name "admin-events" \
  --viewport 1920x1080
```

## Troubleshooting

### "Dev server not running"

Start the dev server:
```bash
./.claude/skills/visual-testing/scripts/visual-test.sh start
# Or manually: pnpm dev
```

### "Screenshot timeout"

- Check the URL is correct
- Ensure dev server is responding: `curl http://localhost:3012`
- Try increasing wait time: `--wait 5000`

### "Puppeteer not found"

Puppeteer should be installed. If not:
```bash
cd apps/web && pnpm add -D puppeteer
```

## Related Files

- Demo showcase: `apps/web/app/demo/fever/showcase/page.tsx`
- Demo components: `apps/web/components/demo/interactive/demos/`
- Interactive demo wrapper: `apps/web/components/demo/interactive/interactive-demo.tsx`
