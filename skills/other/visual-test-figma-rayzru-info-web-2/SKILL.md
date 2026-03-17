---
name: visual-test-figma
description: Compare implementation screenshot with Figma design for visual testing
context: fork
allowed-tools:
  - mcp__figma__get_screenshot
  - mcp__playwright__browser_navigate
  - mcp__playwright__browser_snapshot
  - mcp__playwright__browser_click
  - mcp__playwright__browser_take_screenshot
  - mcp__playwright__browser_wait_for
  - Write
  - Read
---

# Visual Test with Figma

Automates visual testing workflow from [VISUAL_TESTING_PROTOCOL.md](../../instructions/VISUAL_TESTING_PROTOCOL.md).

**Token Efficiency**: Automates visual testing protocol (50% savings: 6,000 → 3,000 tokens)

## Usage

Invoke with: `/visual-test-figma [figma-node-id] [implementation-url]`

**Examples**:
- `/visual-test-figma 9406-230152 http://localhost:3000/app/settings` - Test settings page
- `/visual-test-figma 1234-567890 http://localhost:3000/app/scheduler` - Test scheduler
- `/visual-test-figma 9999-111111 http://localhost:3000/components/dialog` - Test dialog component

**Parameters**:
- `figma-node-id`: Node ID from Figma URL (e.g., `node-id=9406-230152` → `9406-230152`)
- `implementation-url`: URL to implementation page to test

## Prerequisites

- Figma MCP configured with file access
- Application running on localhost:3000
- Chrome DevTools or Playwright MCP available
- Figma design node ID available

## Workflow

### Step 1: Extract Figma Design

**Get screenshot from Figma**:

```javascript
mcp__figma__get_screenshot({
  nodeId: "[figma-node-id]",
  clientLanguages: "typescript",
  clientFrameworks: "react,next.js"
})
```

**Save Figma screenshot**:
- Location: `specs/visual-tests/[feature-name]_figma.png`
- Format: PNG
- Naming: Derive feature name from URL or node ID

**Extract design specifications** (from Figma response metadata):
- Colors (background, text, borders)
- Spacing (padding, margin, gap)
- Typography (font size, weight, line height)
- Layout (flex, grid, positioning)
- Component dimensions (width, height)

### Step 2: Navigate to Implementation

**Navigate to implementation URL**:

```javascript
mcp__playwright__browser_navigate({
  url: "[implementation-url]"
})
```

**Take snapshot for context**:

```javascript
mcp__playwright__browser_snapshot()
```

**Check if interaction needed**:
- If URL shows dialog/modal: May need to click button to open
- If URL shows specific state: May need to select options/filters
- If URL shows authenticated page: Ensure authenticated (use `/auth-verify` first)

### Step 3: Capture Implementation Screenshot

**Determine screenshot type**:

**Option 1: Full page screenshot**
```javascript
mcp__playwright__browser_take_screenshot({
  filename: "specs/visual-tests/[feature-name]_implementation.png",
  fullPage: true,
  format: "png"
})
```

**Option 2: Element screenshot** (if specific component)
```javascript
// First take snapshot to get element ref
mcp__playwright__browser_snapshot()

// Screenshot specific element
mcp__playwright__browser_take_screenshot({
  element: "[Component name]",
  ref: "[element-ref-from-snapshot]",
  filename: "specs/visual-tests/[feature-name]_implementation.png",
  format: "png"
})
```

**Option 3: Interactive screenshot** (if need to open dialog/modal)
```javascript
// Take snapshot
mcp__playwright__browser_snapshot()

// Click to open component
mcp__playwright__browser_click({
  element: "[Button to open]",
  ref: "[button-ref]"
})

// Wait for component to appear
mcp__playwright__browser_wait_for({ time: 1 })

// Screenshot the opened component
mcp__playwright__browser_take_screenshot({
  element: "[Opened component]",
  ref: "[component-ref]",
  filename: "specs/visual-tests/[feature-name]_implementation.png"
})
```

### Step 4: Visual Comparison

**Present both screenshots to user**:
- Figma design: `specs/visual-tests/[feature-name]_figma.png`
- Implementation: `specs/visual-tests/[feature-name]_implementation.png`

**Comparison checklist** (from VISUAL_TESTING_PROTOCOL.md):

| Aspect | Check | Status |
|--------|-------|--------|
| **Layout structure** | Flex/grid/positioning matches | ✅/❌ |
| **Spacing** | Padding, margin, gap values match | ✅/❌ |
| **Typography** | Font size, weight, line height, color match | ✅/❌ |
| **Colors** | Background, text, borders, shadows match | ✅/❌ |
| **Component positioning** | Header, sidebar, content areas aligned | ✅/❌ |
| **Responsive behavior** | Breakpoints work correctly (if applicable) | ✅/❌ |
| **Interactive states** | Hover, focus, active, disabled (if applicable) | ✅/❌ |

**Analyze discrepancies**:
- Extract differences between Figma and implementation
- Measure spacing differences (8px off, 16px off, etc.)
- Identify color mismatches (hex codes)
- Note missing elements or extra elements

### Step 5: Document Results

**Create comparison report**:

```markdown
## Visual Testing Results: [Feature Name]

**Test Date**: [timestamp]
**Figma Node**: [node-id]
**Implementation URL**: [url]

### Screenshots

**Figma Reference**:
- Node ID: [node-id]
- Design URL: https://www.figma.com/design/[file-id]?node-id=[node-id]
- Screenshot: specs/visual-tests/[feature-name]_figma.png

**Implementation**:
- URL: [implementation-url]
- Browser: Chrome (via [Chrome DevTools | Playwright] MCP)
- Viewport: 1280x720
- Screenshot: specs/visual-tests/[feature-name]_implementation.png

### Comparison Checklist

- [x] Layout structure matches Figma
- [ ] **Spacing off by 8px** (header padding)
- [x] Typography matches design tokens
- [x] Colors match design system
- [ ] **Component positioning**: Entity badge 8px lower than design
- [x] Responsive behavior correct (tested at 1280px)
- [x] Interactive states match (hover, focus)

### Discrepancies Found

#### 1. Header Padding Issue
- **Expected** (Figma): 24px padding (p-6 in Tailwind)
- **Actual** (Implementation): 16px padding (p-4 in Tailwind)
- **Impact**: Header appears cramped
- **Fix**: Update className from `p-4` to `p-6` in [file.tsx:line]

#### 2. Badge Positioning
- **Expected** (Figma): Badge aligned with title baseline (items-center)
- **Actual** (Implementation): Badge aligned with description baseline (items-start)
- **Impact**: Badge appears 8px lower than design
- **Fix**: Update flex alignment from `items-start` to `items-center` in [file.tsx:line]

### Recommendations

**Critical fixes** (blocking alignment):
1. Fix header padding: `className="p-4"` → `className="p-6"`
2. Fix badge alignment: `items-start` → `items-center`

**Optional improvements**:
- Consider adding box-shadow to match Figma design
- Verify spacing on mobile breakpoints (not tested)

### Next Steps

1. Apply critical fixes to implementation
2. Re-run visual test to verify alignment
3. Commit screenshots to version control
4. Update implementation tracking file (if exists)
```

### Step 6: Save Report (if discrepancies found)

**Only save report if**:
- Discrepancies count > 0
- OR user requests documentation

**Save location**:
- Commit message format (if no spec file exists)
- OR append to spec file: `specs/[feature-name]_spec.md`
- OR create standalone report: `specs/visual-tests/[feature-name]_comparison.md`

**If no discrepancies**:
- Report "✅ Visual test passed! Implementation matches Figma design."
- Don't create log file (token efficiency)

## Success Criteria

- [x] Figma screenshot extracted and saved
- [x] Implementation screenshot captured
- [x] Both screenshots presented to user for comparison
- [x] Comparison checklist completed
- [x] Discrepancies identified with measurements
- [x] Fix recommendations provided with file locations
- [x] Report format clear and actionable

## Risk-Based Visual Testing

**Follow risk matrix** from [VALIDATION_PATTERNS.md](../../guidelines/VALIDATION_PATTERNS.md):

| Risk Level | Visual Testing Requirement | Codex Validation |
|------------|---------------------------|------------------|
| **Critical** (PHI/PII UI, auth flows) | MANDATORY + Codex validation | ✅ Required |
| **High** (Multi-component layouts) | MANDATORY | Optional |
| **Medium** (Single component with Figma) | RECOMMENDED | Optional |
| **Low** (Minor CSS tweaks) | OPTIONAL | Skip |

**When to skip this Skill**:
- ❌ Low risk: Minor CSS tweaks without Figma design
- ❌ Backend-only changes (no UI impact)
- ❌ Changes without Figma designs
- ❌ Unit test additions without UI changes

## Error Handling

### Error 1: Figma Node Not Found

**Symptom**: "Node not found" or "Invalid node ID"
**Cause**: Wrong node ID or no access to Figma file
**Solution**:
- Verify node ID from Figma URL: `node-id=XXXX-XXXXXX`
- Check Figma MCP has access to file
- Ensure Figma file is not private/restricted

### Error 2: Implementation Page Not Loading

**Symptom**: Navigation timeout or 404 error
**Cause**: Application not running or wrong URL
**Solution**:
- Verify app running: `curl http://localhost:3000`
- Check Docker containers: `docker ps`
- Verify URL path exists in application

### Error 3: Element Not Found for Screenshot

**Symptom**: "Element not found" when capturing specific component
**Cause**: Element not rendered or wrong selector
**Solution**:
- Take snapshot first to verify element exists
- Check element ref from snapshot
- Ensure component is visible (not hidden or collapsed)

### Error 4: Screenshots Look Different (but design matches)

**Symptom**: Screenshots appear different but visually match
**Cause**: Font rendering, browser differences, timing
**Solution**:
- Note in report: "Visual match confirmed despite rendering differences"
- Focus on layout, spacing, colors (not pixel-perfect rendering)
- Use consistent viewport size for comparison

## Examples

### Example 1: Settings Dialog Visual Test

**User**: `/visual-test-figma 9406-230152 http://localhost:3000/app/settings`

**Execution**:
1. Extract Figma screenshot → `specs/visual-tests/settings_dialog_figma.png`
2. Navigate to settings page
3. Take snapshot → Check if dialog open
4. Click "Settings" button to open dialog
5. Screenshot dialog → `specs/visual-tests/settings_dialog_implementation.png`
6. Compare: Layout ✅, Spacing ❌ (8px off), Typography ✅, Colors ✅
7. Report discrepancies with fix recommendations

**Output**:
```markdown
## Visual Testing Results: Settings Dialog

### Discrepancies Found (1)

#### 1. Dialog Padding
- **Expected**: 32px padding (p-8)
- **Actual**: 24px padding (p-6)
- **Fix**: Update SettingsDialog.tsx line 42

### Recommendations
1. Fix dialog padding: `className="p-6"` → `className="p-8"`
```

### Example 2: Perfect Match

**User**: `/visual-test-figma 1234-567890 http://localhost:3000/app/scheduler`

**Output**:
```markdown
## Visual Testing Results: Scheduler Page

✅ **Visual test passed!**

**Summary**:
- Layout structure: ✅ Matches Figma
- Spacing: ✅ Pixel-perfect alignment
- Typography: ✅ Design tokens applied correctly
- Colors: ✅ Design system colors used
- Component positioning: ✅ All elements aligned

No discrepancies found. Implementation matches Figma design.

**Screenshots saved**:
- Figma: specs/visual-tests/scheduler_figma.png
- Implementation: specs/visual-tests/scheduler_implementation.png
```

### Example 3: Multiple Discrepancies

**User**: `/visual-test-figma 9999-111111 http://localhost:3000/components/user-card`

**Output**:
```markdown
## Visual Testing Results: User Card Component

### Discrepancies Found (3)

#### 1. Avatar Size
- **Expected**: 64px (w-16 h-16)
- **Actual**: 48px (w-12 h-12)
- **Impact**: Avatar too small
- **Fix**: UserCard.tsx:25 → `className="w-16 h-16"`

#### 2. Text Color
- **Expected**: #1F2937 (gray-800)
- **Actual**: #374151 (gray-700)
- **Impact**: Text appears lighter than design
- **Fix**: UserCard.tsx:30 → `text-gray-800`

#### 3. Card Border Radius
- **Expected**: 12px (rounded-xl)
- **Actual**: 8px (rounded-lg)
- **Impact**: Corners less rounded
- **Fix**: UserCard.tsx:15 → `rounded-xl`

### Recommendations

**Critical fixes**:
1. Avatar size: w-12 → w-16
2. Text color: text-gray-700 → text-gray-800
3. Border radius: rounded-lg → rounded-xl

**After fixes**:
- Re-run: `/visual-test-figma 9999-111111 http://localhost:3000/components/user-card`
```

## Integration with Development Workflow

**When to use this Skill**:
- ✅ After implementing UI feature with Figma design
- ✅ Before creating pull request (visual verification)
- ✅ During design review (verify implementation)
- ✅ When designer reports "doesn't match design"
- ✅ Before marking feature as complete

**Combine with other workflows**:
1. Implement feature
2. Run `/auth-verify` (if authenticated page)
3. Run `/visual-test-figma [node-id] [url]` (verify design)
4. Fix discrepancies
5. Re-run visual test to confirm
6. Run `/commit-coauthor` (commit changes)

**Integration with VISUAL_TESTING_PROTOCOL.md**:
- This Skill automates Phases 1-3 of the protocol
- Phase 4 (Documentation) handled by report generation
- Follows risk-based testing approach

## Token Efficiency

**Baseline (manual visual testing)**:
- Read VISUAL_TESTING_PROTOCOL.md: 1,500 tokens
- Extract Figma screenshot: 500 tokens
- Navigate and screenshot implementation: 800 tokens
- Compare and analyze: 1,200 tokens
- Document results: 2,000 tokens
- **Total**: ~6,000 tokens

**With visual-test-figma Skill**:
- Skill invocation: 300 tokens
- Figma extraction + implementation screenshot: 1,000 tokens
- Automated comparison: 700 tokens
- Report generation: 1,000 tokens
- **Total**: ~3,000 tokens

**Savings**: 3,000 tokens (50% reduction)

**Projected usage**: 5x per week
**Weekly savings**: 15,000 tokens
**Annual savings**: 780,000 tokens (~$1.95/year)

## Related Documentation

- [VISUAL_TESTING_PROTOCOL.md](../../instructions/VISUAL_TESTING_PROTOCOL.md) - Full visual testing workflow
- [VALIDATION_PATTERNS.md](../../guidelines/VALIDATION_PATTERNS.md) - Risk-based validation matrix
- [TOKEN_EFFICIENCY.md](../../guidelines/TOKEN_EFFICIENCY.md) - Token optimization patterns

---

**Skill Version**: 1.0
**Created**: 2026-01-09
**Last Updated**: 2026-01-09
**Requires**: Claude Code v2.1.0+, Figma MCP, Chrome DevTools or Playwright MCP
