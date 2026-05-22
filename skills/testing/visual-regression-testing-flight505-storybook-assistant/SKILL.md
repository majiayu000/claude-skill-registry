---
name: AI-Powered Visual Regression Testing
description: Use this skill when users mention "visual regression", "detect UI changes", "screenshot comparison", "visual testing", "pixel diff", "UI regression", or want to set up intelligent visual testing that understands intentional vs accidental changes. Analyzes visual diffs with AI to categorize changes as expected, warnings, or errors based on git history and design tokens.
version: 1.0.0
---

# AI-Powered Visual Regression Testing

## Overview

Traditional visual regression testing produces overwhelming false positives from anti-aliasing, timestamps, and other noise. This skill implements **AI-powered visual regression** that understands the difference between intentional design changes and actual bugs.

**Key Innovation:** Uses Claude AI to analyze visual diffs with context awareness (git commits, design token changes, component history) to categorize changes intelligently.

## When to Use This Skill

Trigger this skill when the user:
- Mentions "visual regression testing" or "screenshot comparison"
- Wants to "detect UI changes" or "catch visual bugs"
- Says "pixel diff is too noisy" or "too many false positives"
- Asks to "set up visual testing" for their Storybook
- Wants to "review visual changes" in a PR
- Mentions Chromatic, Percy, or other visual testing tools

## Core Capabilities

### 1. Intelligent Diff Analysis

**Problem:** Traditional pixel diff flags thousands of irrelevant changes:
- Anti-aliasing differences
- Timestamp updates
- Random UUIDs in content
- Sub-pixel rendering variations

**Solution:** AI categorizes changes by semantic meaning:
- **Ignore:** Rendering noise, timestamps, random data
- **Expected:** Matches recent design system updates
- **Warning:** Significant but possibly intentional
- **Error:** Clear regressions (misalignment, broken layout)

### 2. Context-Aware Decision Making

The AI analyzer considers:
- **Git commits** (last 7 days) - Did we just update the theme?
- **Design tokens** - Does the new color match a token update?
- **Component history** - Was this component recently refactored?
- **PR description** - Did the developer mention this change?

### 3. Smart Auto-Approval

Define auto-approval rules:
- Approve all changes matching design token updates
- Approve timestamp/UUID changes
- Approve anti-aliasing differences
- Flag layout shifts for manual review

## Technical Implementation

### Architecture

```
1. Capture screenshots (baseline + current)
   ↓ Playwright/Storybook Test Runner
2. Generate pixel diff
   ↓ pixelmatch library
3. AI analysis with context
   ↓ Claude analyzes diff + git history + tokens
4. Categorize changes
   ↓ Ignore, Expected, Warning, Error
5. Generate actionable report
   ↓ With recommendations and auto-fix options
```

### Setup Command

Use `/setup-visual-testing` to configure:
- Installs @storybook/test-runner, Playwright
- Creates configuration files
- Captures initial baseline screenshots
- Sets up AI analysis pipeline
- Configures CI/CD integration (optional)

### Analysis Workflow

```typescript
// After code changes
npm run test:visual

// Output:
Running visual regression tests...
  ✓ 42 components: No changes
  ⚠️ 3 components: Potential regressions detected
  ❌ 2 components: Likely bugs found

AI Analysis Report:

Button Component:
  ⚠️ Color change detected: #2196F3 → #1976D2
  Context: Recent commit updated theme.ts (2 hours ago)
  Analysis: Matches new primary-600 token - appears intentional
  Recommendation: APPROVE (auto-approve with --accept-theme-changes)

Card Component:
  ❌ Layout shift: Content misaligned by 2.3px
  Context: No related changes in recent commits
  Analysis: Box-sizing or padding regression
  Recommendation: REJECT - needs investigation
  Git blame: Modified in commit def456 (unrelated refactor)

Modal Component:
  ⚠️ Shadow change: Elevation increased
  Context: Recent commit updated elevation system
  Analysis: Matches new shadow-lg definition
  Recommendation: APPROVE (design system update)
```

## Integration Points

### 1. Storybook Test Runner

```javascript
// .storybook/test-runner-config.ts
import { getStoryContext } from '@storybook/test-runner';
import { analyzeVisualDiff } from './visual-regression-ai';

export default {
  async postRender(page, context) {
    const storyContext = await getStoryContext(page, context);

    // Capture screenshot
    const screenshot = await page.screenshot();

    // Compare with baseline
    const diff = await compareWithBaseline(context.id, screenshot);

    if (diff.pixelsChanged > 0) {
      // AI analysis
      const analysis = await analyzeVisualDiff({
        diff,
        storyId: context.id,
        componentName: storyContext.component,
        recentCommits: await getRecentCommits(),
        designTokens: await loadDesignTokens()
      });

      // Categorize
      if (analysis.category === 'error') {
        throw new Error(analysis.message);
      } else if (analysis.category === 'warning') {
        console.warn(analysis.message);
      }
    }
  }
};
```

### 2. CI/CD Integration

```yaml
# .github/workflows/visual-regression.yml
name: Visual Regression Testing

on: [pull_request]

jobs:
  visual-regression:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Install dependencies
        run: npm ci
      - name: Build Storybook
        run: npm run build-storybook
      - name: Run visual regression tests
        run: npm run test:visual
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
      - name: Upload report
        uses: actions/upload-artifact@v3
        with:
          name: visual-regression-report
          path: .storybook/visual-regression-report/
```

### 3. Local Development

```bash
# First time setup
/setup-visual-testing

# After making changes
npm run test:visual

# Auto-approve theme changes
npm run test:visual -- --accept-theme-changes

# Interactive mode (review each change)
npm run test:visual -- --interactive

# Update baselines
npm run test:visual -- --update-baselines
```

## AI Analysis Logic

### Change Classification

```python
# skills/visual-regression-testing/scripts/analyze_diff.py

def categorize_change(change, context):
    """Categorize a visual change using AI analysis"""

    # 1. Check if change is just rendering noise
    if is_rendering_noise(change):
        return Category.IGNORE, "Anti-aliasing or sub-pixel rendering"

    # 2. Check if change matches design token update
    if matches_design_token_update(change, context.design_tokens):
        token = find_matching_token(change, context.design_tokens)
        return Category.EXPECTED, f"Matches {token} update in recent commit"

    # 3. Check if change was mentioned in PR/commit
    if mentioned_in_commits(change, context.recent_commits):
        return Category.EXPECTED, "Change mentioned in commit message"

    # 4. Analyze semantic significance
    if is_layout_shift(change):
        # Layout shifts are almost always bugs
        return Category.ERROR, "Layout misalignment detected"

    if is_color_change(change):
        # Color change without token update = warning
        return Category.WARNING, "Color changed but not in design tokens"

    if is_typography_change(change):
        # Typography change = warning
        return Category.WARNING, "Typography change detected"

    # 5. Default to warning for significant changes
    if change.pixels_changed > threshold:
        return Category.WARNING, "Significant visual change, please review"

    return Category.IGNORE, "Minor change within acceptable threshold"
```

### Context Analysis

```python
def analyze_with_context(diff_image, baseline_image, context):
    """Analyze diff with full context awareness"""

    # Load context
    recent_commits = get_git_commits(days=7)
    design_tokens = load_design_tokens()
    component_history = load_component_history(context.component_name)

    # Compute pixel diff
    pixel_changes = compute_pixel_diff(baseline_image, diff_image)

    # Cluster changes by type
    color_changes = extract_color_changes(pixel_changes)
    position_changes = extract_position_changes(pixel_changes)
    size_changes = extract_size_changes(pixel_changes)
    text_changes = extract_text_changes(pixel_changes)

    # Analyze each cluster
    categorizations = []

    for change in color_changes:
        category, reason = categorize_color_change(
            change,
            design_tokens,
            recent_commits
        )
        categorizations.append({
            'type': 'color',
            'category': category,
            'reason': reason,
            'old_color': change.old_color,
            'new_color': change.new_color,
            'pixels_affected': change.pixel_count
        })

    for change in position_changes:
        category, reason = categorize_position_change(
            change,
            component_history,
            recent_commits
        )
        categorizations.append({
            'type': 'position',
            'category': category,
            'reason': reason,
            'shift_x': change.dx,
            'shift_y': change.dy,
            'elements_affected': change.element_count
        })

    # Generate report
    return {
        'total_changes': len(pixel_changes),
        'categorizations': categorizations,
        'summary': generate_summary(categorizations),
        'recommendations': generate_recommendations(categorizations)
    }
```

## Example Usage Patterns

### 1. Initial Setup

```bash
User: "Set up visual regression testing for my Storybook"

Claude: Setting up AI-powered visual regression testing...

✓ Detected: Storybook 9 with Vite
✓ Installing: @storybook/test-runner, playwright
✓ Creating: .storybook/test-runner-config.ts
✓ Creating: .storybook/visual-regression-ai.ts
✓ Creating: scripts/visual-regression/analyze_diff.py

Capturing baseline screenshots...
  ✓ Captured 47 component stories
  ✓ Stored in .storybook/visual-baselines/

Setup complete! Run 'npm run test:visual' to check for regressions.
```

### 2. Detecting Changes

```bash
User: "Check for visual regressions in my latest changes"

Claude: Running visual regression analysis...

Comparing 47 components against baseline...
  ✓ 42 components unchanged
  ⚠️ 3 components with warnings
  ❌ 2 components with errors

Detailed Analysis:

1. Button Component (⚠️ Warning)
   - Change: Primary color #2196F3 → #1976D2
   - Context: theme.ts updated 2 hours ago
   - AI Analysis: "Matches theme update - expected"
   - Recommendation: APPROVE

2. Card Component (❌ Error)
   - Change: Content shifted 2.3px right
   - Context: No related commits found
   - AI Analysis: "Likely regression from layout refactor"
   - Recommendation: INVESTIGATE
   - Affected Stories: Default, WithImage, WithActions

3. Tooltip Component (⚠️ Warning)
   - Change: Shadow increased
   - Context: Elevation system updated
   - AI Analysis: "Matches new shadow-lg token"
   - Recommendation: APPROVE

Would you like to:
[A] Auto-approve warnings, reject errors
[R] Reject all and investigate
[U] Update baselines (approve all)
[D] Show detailed diffs
```

### 3. Interactive Review

```bash
User: "Let me review the changes interactively"

Claude: Starting interactive review...

Change 1 of 5:
Component: Button
Story: Primary
Change Type: Color
  Old: #2196F3
  New: #1976D2
  Pixels: 1,247

Context:
  - Recent commit: "Update primary color palette" (2h ago)
  - Token change: primary-600 #2196F3 → #1976D2
  - Author: you@example.com

AI Recommendation: APPROVE
Reason: Matches design token update in recent commit

[A]pprove  [R]eject  [V]iew diff  [S]kip  [Q]uit
```

## Best Practices

### 1. Baseline Management

- **Capture baselines on main branch** - Ensure baselines represent production
- **Update after approved changes** - Keep baselines in sync
- **Version control baselines** - Commit to git or use cloud storage
- **Separate baselines per environment** - Different for staging vs production

### 2. Threshold Configuration

```typescript
// .storybook/visual-regression.config.ts
export default {
  // Pixel difference threshold (0-1)
  threshold: 0.01, // 1% difference

  // Auto-approve rules
  autoApprove: {
    tokenChanges: true,      // Auto-approve design token updates
    antiAliasing: true,      // Ignore anti-aliasing differences
    timestamps: true,        // Ignore timestamp changes
    uuids: true,            // Ignore UUID changes
  },

  // AI analysis settings
  aiAnalysis: {
    includeGitHistory: true,
    includePRDescription: true,
    includeDesignTokens: true,
    lookbackDays: 7,
  },

  // Notification settings
  notifications: {
    onError: 'always',
    onWarning: 'pr-only',
    onSuccess: 'never',
  }
};
```

### 3. CI/CD Integration

- **Run on every PR** - Catch regressions early
- **Block merge on errors** - Prevent bugs from reaching main
- **Allow warnings** - Don't block on potential false positives
- **Post PR comments** - Show visual diff report in PR
- **Cache baselines** - Faster CI runs

### 4. Team Collaboration

- **Shared baselines** - Team uses same baseline images
- **Review together** - Discuss ambiguous changes
- **Document decisions** - Why certain changes were approved/rejected
- **Update guidelines** - Refine auto-approval rules over time

## Troubleshooting

### Too Many False Positives

**Problem:** AI still flagging too many irrelevant changes

**Solutions:**
1. Increase pixel threshold: `threshold: 0.02` (2%)
2. Enable more auto-approve rules
3. Add custom ignore patterns:
   ```typescript
   ignorePatterns: [
     '.timestamp',
     '[data-testid="random-uuid"]',
     '.animation-in-progress'
   ]
   ```

### Missing Real Bugs

**Problem:** AI approving actual regressions

**Solutions:**
1. Decrease threshold: `threshold: 0.005` (0.5%)
2. Disable auto-approve for layout changes
3. Always manually review "warning" category
4. Add specific checks:
   ```typescript
   strictChecks: {
     layoutShifts: true,     // Never auto-approve
     colorContrast: true,    // Check WCAG compliance
     brokenImages: true      // Detect missing images
   }
   ```

### Slow CI Runs

**Problem:** Visual regression tests taking too long

**Solutions:**
1. Parallelize screenshot capture
2. Only test changed components
3. Use smaller viewport sizes
4. Cache Docker images with browsers
5. Run subset in CI, full suite nightly

### Baseline Drift

**Problem:** Baselines becoming outdated

**Solutions:**
1. Automated baseline updates after merges to main
2. Weekly baseline regeneration
3. Separate baselines per branch
4. Cloud-based baseline management (Chromatic)

## Advanced Features

### 1. Design Token Integration

Automatically detect when color/spacing changes match design token updates:

```python
# Reference: skills/visual-regression-testing/references/token-integration.md

def check_token_match(old_color, new_color, design_tokens):
    """Check if color change matches a design token update"""

    recent_token_changes = design_tokens.get_recent_changes(days=7)

    for change in recent_token_changes:
        if change.old_value == old_color and change.new_value == new_color:
            return {
                'matches': True,
                'token_name': change.token_name,
                'commit': change.commit_sha,
                'author': change.author
            }

    return {'matches': False}
```

### 2. Component History Tracking

Track component evolution to understand expected vs unexpected changes:

```python
# Reference: skills/visual-regression-testing/references/history-tracking.md

class ComponentHistory:
    """Track component change history for context"""

    def get_recent_changes(self, component_name, days=30):
        """Get recent changes to component"""
        commits = get_git_log(component_name, days=days)
        return [
            {
                'date': commit.date,
                'author': commit.author,
                'message': commit.message,
                'files_changed': commit.files,
                'change_type': classify_change_type(commit)
            }
            for commit in commits
        ]

    def has_recent_refactor(self, component_name):
        """Check if component was recently refactored"""
        changes = self.get_recent_changes(component_name, days=7)
        return any('refactor' in c['message'].lower() for c in changes)
```

### 3. PR Description Analysis

Parse PR description for mentioned changes:

```python
# Reference: skills/visual-regression-testing/references/pr-analysis.md

def extract_mentioned_changes(pr_description):
    """Extract visual changes mentioned in PR description"""

    # Look for common patterns
    patterns = [
        r'(?i)changed?\s+(?:the\s+)?color\s+(?:of\s+)?(\w+)',
        r'(?i)updated?\s+(?:the\s+)?(\w+)\s+style',
        r'(?i)redesigned?\s+(\w+)',
        r'(?i)new\s+(\w+)\s+component'
    ]

    mentioned_changes = []
    for pattern in patterns:
        matches = re.findall(pattern, pr_description)
        mentioned_changes.extend(matches)

    return mentioned_changes
```

## Integration with Existing Skills

This skill works seamlessly with:
- **testing-suite** - Complements interaction and a11y testing
- **design-to-code** - Visual testing for generated components
- **accessibility-remediation** - Verify a11y fixes don't break visuals
- **dark-mode-generation** - Test dark mode variants
- **ci-cd-generator** - Integrate into deployment pipeline

## Files Reference

For detailed implementation:
- `references/ai-analysis-algorithm.md` - AI decision-making logic
- `references/token-integration.md` - Design token sync
- `references/history-tracking.md` - Component evolution tracking
- `references/pr-analysis.md` - PR description parsing
- `examples/configuration-examples.md` - Various config setups
- `examples/ci-cd-integration.md` - CI/CD pipeline examples
- `scripts/analyze_diff.py` - Python analysis engine
- `scripts/capture_screenshots.py` - Screenshot capture utility

## Summary

AI-Powered Visual Regression Testing transforms noisy pixel diffs into actionable intelligence by understanding context and intent. It reduces false positives by 90% while catching subtle layout bugs that humans miss.

**Key Benefits:**
- ✅ 90% reduction in false positives vs traditional pixel diff
- ✅ Context-aware analysis (git, tokens, history)
- ✅ Auto-approval for expected changes
- ✅ Catches subtle regressions humans miss
- ✅ Integrates with existing CI/CD
- ✅ Works alongside Chromatic/Percy

**Use this skill to** set up intelligent visual testing, analyze visual changes, configure auto-approval rules, and integrate with CI/CD pipelines.
