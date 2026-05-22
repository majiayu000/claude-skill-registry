---
name: browser-debugger
description: Systematically tests UI functionality, validates design fidelity with AI visual analysis, monitors console output, tracks network requests, and provides debugging reports using Chrome DevTools MCP. Use after implementing UI features, for design validation, when investigating console errors, for regression testing, or when user mentions testing, browser bugs, console errors, or UI verification.
allowed-tools: Task, Bash
---

# Browser Debugger

This Skill provides comprehensive browser-based UI testing, visual analysis, and debugging capabilities using Chrome DevTools MCP server and optional external vision models via Claudish.

## When to Use This Skill

Claude and agents (developer, reviewer, tester, ui-developer) should invoke this Skill when:

- **Validating Own Work**: After implementing UI features, agents should verify their work in a real browser
- **Design Fidelity Checks**: Comparing implementation screenshots against design references
- **Visual Regression Testing**: Detecting layout shifts, styling issues, or visual bugs
- **Console Error Investigation**: User reports console errors or warnings
- **Form/Interaction Testing**: Verifying user interactions work correctly
- **Pre-Commit Verification**: Before committing or deploying code
- **Bug Reproduction**: User describes UI bugs that need investigation

## Prerequisites

### Required: Chrome DevTools MCP

This skill requires Chrome DevTools MCP. Check availability and install if needed:

```bash
# Check if available
mcp__chrome-devtools__list_pages 2>/dev/null && echo "Available" || echo "Not available"

# Install via claudeup (recommended)
npm install -g claudeup@latest
claudeup mcp add chrome-devtools
```

### Optional: External Vision Models (via OpenRouter)

For advanced visual analysis, use external vision-language models via Claudish:

```bash
# Check OpenRouter API key
[[ -n "${OPENROUTER_API_KEY}" ]] && echo "OpenRouter configured" || echo "Not configured"

# Install claudish
npm install -g claudish
```

---

## Visual Analysis Models (Recommended)

For best visual analysis of UI screenshots, use these models via Claudish:

### Tier 1: Best Quality (Recommended for Design Validation)

| Model | Strengths | Cost | Best For |
|-------|-----------|------|----------|
| **qwen/qwen3-vl-32b-instruct** | Best OCR, spatial reasoning, GUI automation, 32+ languages | ~$0.06/1M input | Design fidelity, OCR, element detection |
| **google/gemini-2.5-flash** | Fast, excellent price/performance, 1M context | ~$0.05/1M input | Real-time validation, large pages |
| **openai/gpt-4o** | Most fluid multimodal, strong all-around | ~$0.15/1M input | Complex visual reasoning |

### Tier 2: Fast & Affordable

| Model | Strengths | Cost | Best For |
|-------|-----------|------|----------|
| **qwen/qwen3-vl-30b-a3b-instruct** | Good balance, MoE architecture | ~$0.04/1M input | Quick checks, multiple iterations |
| **google/gemini-2.5-flash-lite** | Ultrafast, very cheap | ~$0.01/1M input | High-volume testing |

### Tier 3: Free Options

| Model | Notes |
|-------|-------|
| **openrouter/polaris-alpha** | FREE, good for testing workflows |

### Model Selection Guide

```
Design Fidelity Validation → qwen/qwen3-vl-32b-instruct (best OCR & spatial)
Quick Smoke Tests → google/gemini-2.5-flash (fast & cheap)
Complex Layout Analysis → openai/gpt-4o (best reasoning)
High Volume Testing → google/gemini-2.5-flash-lite (ultrafast)
Budget Conscious → openrouter/polaris-alpha (free)
```

---

## Visual Analysis Model Selection (Interactive)

**Before the first screenshot analysis in a session, ask the user which model to use.**

### Step 1: Check for Saved Preference

First, check if user has a saved model preference:

```bash
# Check for saved preference in project settings
SAVED_MODEL=$(cat .claude/settings.json 2>/dev/null | jq -r '.pluginSettings.frontend.visualAnalysisModel // empty')

# Or check session-specific preference
if [[ -f "ai-docs/sessions/${SESSION_ID}/session-meta.json" ]]; then
  SESSION_MODEL=$(jq -r '.visualAnalysisModel // empty' "ai-docs/sessions/${SESSION_ID}/session-meta.json")
fi
```

### Step 2: If No Saved Preference, Ask User

Use **AskUserQuestion** with these options:

```markdown
## Visual Analysis Model Selection

For screenshot analysis and design validation, which AI vision model would you like to use?

**Your choice will be remembered for this session.**
```

**AskUserQuestion options:**

| Option | Label | Description |
|--------|-------|-------------|
| 1 | `qwen/qwen3-vl-32b-instruct` (Recommended) | Best for design fidelity - excellent OCR, spatial reasoning, detailed analysis. ~$0.06/1M tokens |
| 2 | `google/gemini-2.5-flash` | Fast & affordable - great balance of speed and quality. ~$0.05/1M tokens |
| 3 | `openai/gpt-4o` | Most capable - best for complex visual reasoning. ~$0.15/1M tokens |
| 4 | `openrouter/polaris-alpha` (Free) | No cost - good for testing, basic analysis |
| 5 | Skip visual analysis | Use embedded Claude only (no external models) |

**Recommended based on task type:**
- Design validation → Option 1 (Qwen VL)
- Quick iterations → Option 2 (Gemini Flash)
- Complex layouts → Option 3 (GPT-4o)
- Budget-conscious → Option 4 (Free)

### Step 3: Save User's Choice

After user selects, save their preference:

**Option A: Save to Session (temporary)**
```bash
# Update session metadata
jq --arg model "$SELECTED_MODEL" '.visualAnalysisModel = $model' \
  "ai-docs/sessions/${SESSION_ID}/session-meta.json" > tmp.json && \
  mv tmp.json "ai-docs/sessions/${SESSION_ID}/session-meta.json"
```

**Option B: Save to Project Settings (persistent)**
```bash
# Update project settings for future sessions
jq --arg model "$SELECTED_MODEL" \
  '.pluginSettings.frontend.visualAnalysisModel = $model' \
  .claude/settings.json > tmp.json && mv tmp.json .claude/settings.json
```

### Step 4: Use Selected Model

Store the selected model in a variable and use it for all subsequent visual analysis:

```bash
# VISUAL_MODEL is now set to user's choice
# Use it in all claudish calls:

npx claudish --model "$VISUAL_MODEL" --stdin --quiet <<EOF
[visual analysis prompt]
EOF
```

### Model Selection Flow (Decision Tree)

```
┌─────────────────────────────────────────────────────┐
│ Screenshot Analysis Requested                        │
└─────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────┐
│ Check: Is VISUAL_MODEL already set this session?    │
└─────────────────────────────────────────────────────┘
                        │
            ┌───────────┴───────────┐
            │ YES                   │ NO
            ▼                       ▼
┌───────────────────┐   ┌─────────────────────────────┐
│ Use saved model   │   │ Check project settings      │
│ Skip to analysis  │   │ .claude/settings.json       │
└───────────────────┘   └─────────────────────────────┘
                                    │
                        ┌───────────┴───────────┐
                        │ FOUND                 │ NOT FOUND
                        ▼                       ▼
            ┌───────────────────┐   ┌─────────────────────────┐
            │ Use saved model   │   │ Check OpenRouter API    │
            │ Remember for      │   │ key availability        │
            │ session           │   └─────────────────────────┘
            └───────────────────┘               │
                                    ┌───────────┴───────────┐
                                    │ AVAILABLE             │ NOT AVAILABLE
                                    ▼                       ▼
                        ┌───────────────────┐   ┌─────────────────────┐
                        │ AskUserQuestion:  │   │ Inform user:        │
                        │ Select vision     │   │ "Using embedded     │
                        │ model             │   │ Claude only"        │
                        └───────────────────┘   └─────────────────────┘
                                    │
                                    ▼
                        ┌───────────────────────────────────┐
                        │ Save choice to session            │
                        │ Ask: "Save as default?" (optional)│
                        └───────────────────────────────────┘
                                    │
                                    ▼
                        ┌───────────────────────────────────┐
                        │ Proceed with visual analysis      │
                        └───────────────────────────────────┘
```

### Example: AskUserQuestion Implementation

When prompting the user, use this format:

```
Use AskUserQuestion tool with:

question: "Which vision model should I use for screenshot analysis?"
header: "Vision Model"
multiSelect: false
options:
  - label: "Qwen VL 32B (Recommended)"
    description: "Best for design fidelity - excellent OCR & spatial reasoning. ~$0.06/1M tokens"
  - label: "Gemini 2.5 Flash"
    description: "Fast & affordable - great for quick iterations. ~$0.05/1M tokens"
  - label: "GPT-4o"
    description: "Most capable - best for complex visual reasoning. ~$0.15/1M tokens"
  - label: "Free (Polaris Alpha)"
    description: "No cost - good for testing and basic analysis"
```

### Mapping User Choice to Model ID

```bash
case "$USER_CHOICE" in
  "Qwen VL 32B (Recommended)")
    VISUAL_MODEL="qwen/qwen3-vl-32b-instruct"
    ;;
  "Gemini 2.5 Flash")
    VISUAL_MODEL="google/gemini-2.5-flash"
    ;;
  "GPT-4o")
    VISUAL_MODEL="openai/gpt-4o"
    ;;
  "Free (Polaris Alpha)")
    VISUAL_MODEL="openrouter/polaris-alpha"
    ;;
  *)
    VISUAL_MODEL=""  # Skip external analysis
    ;;
esac
```

### Remember for Future Sessions

After first selection, optionally ask:

```
Use AskUserQuestion tool with:

question: "Save this as your default vision model for future sessions?"
header: "Save Default"
multiSelect: false
options:
  - label: "Yes, save as default"
    description: "Use this model automatically in future sessions"
  - label: "No, ask each time"
    description: "Let me choose each session"
```

If user chooses "Yes", update `.claude/settings.json`:

```json
{
  "pluginSettings": {
    "frontend": {
      "visualAnalysisModel": "qwen/qwen3-vl-32b-instruct"
    }
  }
}
```

---

## Recipe 1: Agent Self-Validation (After Implementation)

**Use Case**: Developer/UI-Developer agent validates their own work after implementing a feature.

### Pattern: Implement → Screenshot → Analyze → Report

```markdown
## After Implementing UI Feature

1. **Save file changes** (Edit tool)

2. **Capture implementation screenshot**:
   ```
   mcp__chrome-devtools__navigate_page(url: "http://localhost:5173/your-route")
   # Wait for page load
   mcp__chrome-devtools__take_screenshot(filePath: "/tmp/implementation.png")
   ```

3. **Analyze with embedded Claude** (always available):
   - Describe what you see in the screenshot
   - Check for obvious layout issues
   - Verify expected elements are present

4. **Optional: Enhanced analysis with vision model**:
   ```bash
   # Use Qwen VL for detailed visual analysis
   npx claudish --model qwen/qwen3-vl-32b-instruct --stdin --quiet <<EOF
   Analyze this UI screenshot and identify any visual issues:

   IMAGE: /tmp/implementation.png

   Check for:
   - Layout alignment issues
   - Spacing inconsistencies
   - Typography problems (font sizes, weights)
   - Color contrast issues
   - Missing or broken elements
   - Responsive design problems

   Provide specific, actionable feedback.
   EOF
   ```

5. **Check console for errors**:
   ```
   mcp__chrome-devtools__list_console_messages(types: ["error", "warn"])
   ```

6. **Report results to orchestrator**
```

### Quick Self-Check (5-Point Validation)

Agents should perform this quick check after any UI implementation:

```markdown
## Quick Self-Validation Checklist

□ 1. Screenshot shows expected UI elements
□ 2. No console errors (check: mcp__chrome-devtools__list_console_messages)
□ 3. No network failures (check: mcp__chrome-devtools__list_network_requests)
□ 4. Interactive elements respond correctly
□ 5. Visual styling matches expectations
```

---

## Recipe 2: Design Fidelity Validation

**Use Case**: Compare implementation against Figma design or design reference.

### Pattern: Design Reference → Implementation → Visual Diff

```markdown
## Design Fidelity Check

### Step 1: Capture Design Reference

**From Figma**:
```
# Use Figma MCP to export design
mcp__figma__get_file_image(fileKey: "abc123", nodeId: "136-5051")
# Save to: /tmp/design-reference.png
```

**From URL**:
```
mcp__chrome-devtools__new_page(url: "https://figma.com/proto/...")
mcp__chrome-devtools__take_screenshot(filePath: "/tmp/design-reference.png")
```

**From Local File**:
```
# Already have reference at: /path/to/design.png
```

### Step 2: Capture Implementation

```
mcp__chrome-devtools__navigate_page(url: "http://localhost:5173/component")
mcp__chrome-devtools__resize_page(width: 1440, height: 900)  # Match design viewport
mcp__chrome-devtools__take_screenshot(filePath: "/tmp/implementation.png")
```

### Step 3: Visual Analysis with Vision Model

```bash
npx claudish --model qwen/qwen3-vl-32b-instruct --stdin --quiet <<EOF
Compare these two UI screenshots and identify design fidelity issues:

DESIGN REFERENCE: /tmp/design-reference.png
IMPLEMENTATION: /tmp/implementation.png

Analyze and report differences in:

## Colors & Theming
- Background colors (exact hex values)
- Text colors (headings, body, muted)
- Border and divider colors
- Button/interactive element colors

## Typography
- Font families
- Font sizes (px values)
- Font weights (regular, medium, bold)
- Line heights
- Letter spacing

## Spacing & Layout
- Padding (top, right, bottom, left)
- Margins between elements
- Gap spacing in flex/grid
- Container max-widths
- Alignment (center, left, right)

## Visual Elements
- Border radius values
- Box shadows (blur, spread, color)
- Icon sizes and colors
- Image aspect ratios

## Component Structure
- Missing elements
- Extra elements
- Wrong element order

For EACH difference found, provide:
1. Category (colors/typography/spacing/visual/structure)
2. Severity (CRITICAL/MEDIUM/LOW)
3. Expected value (from design)
4. Actual value (from implementation)
5. Specific Tailwind CSS fix

Output as structured markdown.
EOF
```

### Step 4: Generate Fix Recommendations

Parse vision model output and create actionable fixes for ui-developer agent.
```

### Design Fidelity Scoring

```markdown
## Design Fidelity Score Card

| Category | Score | Issues |
|----------|-------|--------|
| Colors & Theming | X/10 | [list] |
| Typography | X/10 | [list] |
| Spacing & Layout | X/10 | [list] |
| Visual Elements | X/10 | [list] |
| Responsive | X/10 | [list] |
| **Overall** | **X/50** | |

Assessment: PASS (≥40) | NEEDS WORK (30-39) | FAIL (<30)
```

---

## Recipe 3: Interactive Element Testing

**Use Case**: Verify buttons, forms, and interactive components work correctly.

### Pattern: Snapshot → Interact → Verify → Report

```markdown
## Interactive Testing Flow

### Step 1: Get Page Structure
```
mcp__chrome-devtools__take_snapshot()
# Returns all elements with UIDs
```

### Step 2: Test Each Interactive Element

**Button Test**:
```
# Before
mcp__chrome-devtools__take_screenshot(filePath: "/tmp/before-click.png")

# Click
mcp__chrome-devtools__click(uid: "button-submit-123")

# After (wait for response)
mcp__chrome-devtools__wait_for(text: "Success", timeout: 5000)
mcp__chrome-devtools__take_screenshot(filePath: "/tmp/after-click.png")

# Check results
mcp__chrome-devtools__list_console_messages(types: ["error"])
mcp__chrome-devtools__list_network_requests(resourceTypes: ["fetch", "xhr"])
```

**Form Test**:
```
# Fill form
mcp__chrome-devtools__fill_form(elements: [
  { uid: "input-email", value: "test@example.com" },
  { uid: "input-password", value: "SecurePass123!" }
])

# Submit
mcp__chrome-devtools__click(uid: "button-submit")

# Verify
mcp__chrome-devtools__wait_for(text: "Welcome", timeout: 5000)
```

**Hover State Test**:
```
mcp__chrome-devtools__take_screenshot(filePath: "/tmp/before-hover.png")
mcp__chrome-devtools__hover(uid: "button-primary")
mcp__chrome-devtools__take_screenshot(filePath: "/tmp/after-hover.png")
# Compare screenshots for hover state changes
```

### Step 3: Analyze Interaction Results

Use vision model to compare before/after screenshots:
```bash
npx claudish --model google/gemini-2.5-flash --stdin --quiet <<EOF
Compare these before/after screenshots and verify the interaction worked:

BEFORE: /tmp/before-click.png
AFTER: /tmp/after-click.png

Expected behavior: [describe what should happen]

Verify:
1. Did the expected UI change occur?
2. Are there any error states visible?
3. Did loading states appear/disappear correctly?
4. Is the final state correct?

Report: PASS/FAIL with specific observations.
EOF
```
```

---

## Recipe 4: Responsive Design Validation

**Use Case**: Verify UI works across different screen sizes.

### Pattern: Resize → Screenshot → Analyze

```markdown
## Responsive Testing

### Breakpoints to Test

| Breakpoint | Width | Description |
|------------|-------|-------------|
| Mobile | 375px | iPhone SE |
| Mobile L | 428px | iPhone 14 Pro Max |
| Tablet | 768px | iPad |
| Desktop | 1280px | Laptop |
| Desktop L | 1920px | Full HD |

### Automated Responsive Check

```bash
#!/bin/bash
# Test all breakpoints

BREAKPOINTS=(375 428 768 1280 1920)
URL="http://localhost:5173/your-route"

for width in "${BREAKPOINTS[@]}"; do
  echo "Testing ${width}px..."

  # Resize and screenshot
  mcp__chrome-devtools__resize_page(width: $width, height: 900)
  mcp__chrome-devtools__take_screenshot(filePath: "/tmp/responsive-${width}.png")
done
```

### Visual Analysis for Responsive Issues

```bash
npx claudish --model qwen/qwen3-vl-32b-instruct --stdin --quiet <<EOF
Analyze these responsive screenshots for layout issues:

MOBILE (375px): /tmp/responsive-375.png
TABLET (768px): /tmp/responsive-768.png
DESKTOP (1280px): /tmp/responsive-1280.png

Check for:
1. Text overflow or truncation
2. Elements overlapping
3. Improper stacking on mobile
4. Touch targets too small (<44px)
5. Hidden content that shouldn't be hidden
6. Horizontal scroll issues
7. Image scaling problems

Report issues by breakpoint with specific CSS fixes.
EOF
```
```

---

## Recipe 5: Accessibility Validation

**Use Case**: Verify accessibility standards (WCAG 2.1 AA).

### Pattern: Snapshot → Analyze → Check Contrast

```markdown
## Accessibility Check

### Automated A11y Testing

```
# Get full accessibility tree
mcp__chrome-devtools__take_snapshot(verbose: true)

# Check for common issues:
# - Missing alt text
# - Missing ARIA labels
# - Incorrect heading hierarchy
# - Missing form labels
```

### Visual Contrast Analysis

```bash
npx claudish --model qwen/qwen3-vl-32b-instruct --stdin --quiet <<EOF
Analyze this screenshot for accessibility issues:

IMAGE: /tmp/implementation.png

Check WCAG 2.1 AA compliance:

1. **Color Contrast**
   - Text contrast ratio (need 4.5:1 for normal, 3:1 for large)
   - Interactive element contrast
   - Focus indicator visibility

2. **Visual Cues**
   - Do links have underlines or other visual differentiation?
   - Are error states clearly visible?
   - Are required fields indicated?

3. **Text Readability**
   - Font size (minimum 16px for body)
   - Line height (minimum 1.5)
   - Line length (max 80 characters)

4. **Touch Targets**
   - Minimum 44x44px for interactive elements
   - Adequate spacing between targets

Report violations with severity and specific fixes.
EOF
```
```

---

## Recipe 6: Console & Network Debugging

**Use Case**: Investigate runtime errors and API issues.

### Pattern: Monitor → Capture → Analyze

```markdown
## Debug Session

### Real-Time Console Monitoring

```
# Get all console messages
mcp__chrome-devtools__list_console_messages(includePreservedMessages: true)

# Filter by type
mcp__chrome-devtools__list_console_messages(types: ["error", "warn"])

# Get specific error details
mcp__chrome-devtools__get_console_message(msgid: 123)
```

### Network Request Analysis

```
# Get all requests
mcp__chrome-devtools__list_network_requests()

# Filter API calls only
mcp__chrome-devtools__list_network_requests(resourceTypes: ["fetch", "xhr"])

# Get failed request details
mcp__chrome-devtools__get_network_request(reqid: 456)
```

### Error Pattern Analysis

Common error patterns to look for:

| Error Type | Pattern | Common Cause |
|------------|---------|--------------|
| React Error | "Cannot read property" | Missing null check |
| React Error | "Invalid hook call" | Hook rules violation |
| Network Error | "CORS" | Missing CORS headers |
| Network Error | "401" | Auth token expired |
| Network Error | "404" | Wrong API endpoint |
| Network Error | "500" | Server error |
```

---

## Integration with Agents

### For Developer Agent

After implementing any UI feature, the developer agent should:

```markdown
## Developer Self-Validation Protocol

1. Save code changes
2. Navigate to the page: `mcp__chrome-devtools__navigate_page`
3. Take screenshot: `mcp__chrome-devtools__take_screenshot`
4. Check console: `mcp__chrome-devtools__list_console_messages(types: ["error"])`
5. Check network: `mcp__chrome-devtools__list_network_requests`
6. Report: "Implementation verified - [X] console errors, [Y] network failures"
```

### For Reviewer Agent

When reviewing UI changes:

```markdown
## Reviewer Validation Protocol

1. Read the code changes
2. Navigate to affected pages
3. Take screenshots of all changed components
4. Use vision model for visual analysis (if design reference available)
5. Check console for new errors introduced
6. Verify no regression in existing functionality
7. Report: "Visual review complete - [findings]"
```

### For Tester Agent

Comprehensive testing:

```markdown
## Tester Validation Protocol

1. Navigate to test target
2. Get page snapshot for element UIDs
3. Execute test scenarios (interactions, forms, navigation)
4. Capture before/after screenshots for each action
5. Monitor console throughout
6. Monitor network throughout
7. Use vision model for visual regression detection
8. Generate detailed test report
```

### For UI-Developer Agent

After fixing UI issues:

```markdown
## UI-Developer Validation Protocol

1. Apply CSS/styling fixes
2. Take screenshot of fixed component
3. Compare with design reference using vision model
4. Verify fix doesn't break other viewports (responsive check)
5. Check console for any styling-related errors
6. Report: "Fix applied and verified - [before/after comparison]"
```

---

## Quick Reference: Chrome DevTools MCP Tools

### Navigation
- `navigate_page` - Load URL or navigate back/forward/reload
- `new_page` - Open new browser tab
- `select_page` - Switch between tabs
- `close_page` - Close a tab

### Inspection
- `take_snapshot` - Get DOM structure with element UIDs (for interaction)
- `take_screenshot` - Capture visual state (PNG/JPEG/WebP)
- `list_pages` - List all open tabs

### Interaction
- `click` - Click element by UID
- `fill` - Type into input by UID
- `fill_form` - Fill multiple form fields
- `hover` - Hover over element
- `drag` - Drag and drop
- `press_key` - Keyboard input
- `handle_dialog` - Accept/dismiss alerts

### Console & Network
- `list_console_messages` - Get console output
- `get_console_message` - Get message details
- `list_network_requests` - Get network activity
- `get_network_request` - Get request details

### Advanced
- `evaluate_script` - Run JavaScript in page
- `resize_page` - Change viewport size
- `emulate` - CPU throttling, network conditions, geolocation
- `performance_start_trace` / `performance_stop_trace` - Performance profiling

---

## Example: Complete Validation Flow

```markdown
## Full Validation Example: User Profile Component

### Setup
```
URL: http://localhost:5173/profile
Component: UserProfileCard
Design Reference: /designs/profile-card.png
```

### Step 1: Capture Implementation
```
mcp__chrome-devtools__navigate_page(url: "http://localhost:5173/profile")
mcp__chrome-devtools__resize_page(width: 1440, height: 900)
mcp__chrome-devtools__take_screenshot(filePath: "/tmp/profile-impl.png")
```

### Step 2: Design Fidelity Check (Qwen VL)
```bash
npx claudish --model qwen/qwen3-vl-32b-instruct --stdin --quiet <<EOF
Compare design vs implementation:
DESIGN: /designs/profile-card.png
IMPLEMENTATION: /tmp/profile-impl.png

Report all visual differences with severity and Tailwind CSS fixes.
EOF
```

### Step 3: Interactive Testing
```
# Get elements
mcp__chrome-devtools__take_snapshot()

# Test edit button
mcp__chrome-devtools__click(uid: "edit-profile-btn")
mcp__chrome-devtools__wait_for(text: "Edit Profile", timeout: 3000)
mcp__chrome-devtools__take_screenshot(filePath: "/tmp/profile-edit-modal.png")
```

### Step 4: Console & Network Check
```
mcp__chrome-devtools__list_console_messages(types: ["error", "warn"])
mcp__chrome-devtools__list_network_requests(resourceTypes: ["fetch"])
```

### Step 5: Responsive Check (Gemini Flash - fast)
```bash
for width in 375 768 1280; do
  mcp__chrome-devtools__resize_page(width: $width, height: 900)
  mcp__chrome-devtools__take_screenshot(filePath: "/tmp/profile-${width}.png")
done

npx claudish --model google/gemini-2.5-flash --stdin --quiet <<EOF
Check responsive layout issues across these screenshots:
/tmp/profile-375.png (mobile)
/tmp/profile-768.png (tablet)
/tmp/profile-1280.png (desktop)
EOF
```

### Step 6: Generate Report
```
## Validation Report: UserProfileCard

### Design Fidelity: 45/50 (PASS)
- Colors: 10/10 ✓
- Typography: 9/10 (font-weight mismatch on heading)
- Spacing: 8/10 (padding-bottom needs increase)
- Visual: 10/10 ✓
- Responsive: 8/10 (mobile text truncation)

### Interactive Testing: PASS
- Edit button: ✓ Opens modal
- Save button: ✓ Saves changes
- Cancel button: ✓ Closes modal

### Console: CLEAN
- Errors: 0
- Warnings: 0

### Network: HEALTHY
- GET /api/user: 200 OK (145ms)
- PUT /api/user: 200 OK (234ms)

### Recommendation: READY TO DEPLOY
Minor fixes recommended but not blocking.
```
```

---

## Sources

Research and best practices compiled from:
- [OpenRouter Models](https://openrouter.ai/models) - Vision model pricing and capabilities
- [Browser-Use Framework](https://browser-use.com/) - Browser automation patterns
- [Qwen VL Documentation](https://openrouter.ai/qwen) - Visual language model specs
- [Amazon Nova Act](https://aws.amazon.com/blogs/aws/build-reliable-ai-agents-for-ui-workflow-automation-with-amazon-nova-act-now-generally-available/) - Agent validation patterns
- [BrowserStack Visual Testing](https://www.browserstack.com/guide/how-ai-in-visual-testing-is-evolving) - AI visual testing evolution
- [DataCamp VLM Comparison](https://www.datacamp.com/blog/top-vision-language-models) - Vision model benchmarks
