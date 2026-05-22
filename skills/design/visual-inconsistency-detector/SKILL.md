---
name: visual-inconsistency-detector
description: "Comprehensive visual UI/UX inconsistency detector for design system validation, accessibility compliance, and cross-view consistency analysis"
keywords: visual analysis, design system, accessibility, UI consistency, UX validation, visual regression, cross-view testing
category: specialized
triggers: visual inconsistencies, design system violations, accessibility issues, UI/UX validation, visual testing
---

# Visual UI/UX Inconsistency Detector

## Purpose
This skill provides comprehensive visual analysis and inconsistency detection for Vue.js applications, focusing on design system compliance, accessibility standards, and cross-view UI consistency that are invisible to standard functional testing.

## Quick Context
- **Complexity**: high
- **Duration**: 45-90 minutes
- **Dependencies**: playwright, sharp, canvas, color-diff, accessibility testing libraries

## Activation Triggers
- **Keywords**: visual inconsistencies, design system violations, accessibility issues, UI consistency, UX validation, visual testing, cross-view analysis
- **Files**: src/assets/**/*.css, src/components/**/*.vue, src/views/**/*.vue, design tokens
- **Contexts**: visual design, accessibility, UX consistency, design system validation

## 🎯 Core Mission: Detect What Users See That Tests Miss

### The Problem We Solve
Standard functional testing completely misses:
- **Visual Inconsistencies**: Components that look different across views or states
- **Design System Violations**: Elements that don't follow established design patterns
- **Accessibility Breakdowns**: Visual accessibility issues that affect users with disabilities
- **Cross-View Inconsistencies**: Same functionality looking different in different views
- **Responsive Design Issues**: Breaks at different screen sizes
- **Color Contrast Problems**: Text that's hard to read due to poor contrast
- **Spacing and Typography Issues**: Inconsistent margins, padding, and font usage

## Implementation Strategy

### Phase 1: Visual Design System Analysis
```typescript
interface VisualDesignSystemReport {
  designSystemScore: number           // Overall design system compliance (0-100)
  colorConsistencyIssues: ColorIssue[]
  typographyIssues: TypographyIssue[]
  spacingIssues: SpacingIssue[]
  componentInconsistencies: ComponentInconsistency[]
  responsiveDesignIssues: ResponsiveIssue[]
  accessibilityViolations: AccessibilityViolation[]
  crossViewInconsistencies: CrossViewIssue[]
}

interface ColorIssue {
  severity: 'critical' | 'high' | 'medium' | 'low'
  type: 'contrast' | 'brand_violation' | 'inconsistency' | 'accessibility'
  description: string
  elements: string[]                // Elements with the issue
  expectedColor: string            // What it should be
  actualColor: string              // What it actually is
  wcagLevel: 'AA' | 'AAA' | 'fail' // For contrast issues
  visualEvidence: string           // Screenshot showing the issue
}
```

### Phase 2: PomoFlow-Specific Visual Validation
**Critical PomoFlow Visual Areas to Test:**

#### Board View Visual Consistency
- **Task Cards**: Consistent styling, status indicators, priority colors
- **Swimlanes**: Uniform column headers, consistent spacing
- **Drag-Drop Visual Feedback**: Hover states, drop zones, ghost images
- **Navigation Tabs**: Active/inactive states, responsive behavior
- **Quick Add Input**: Consistent styling across all views

#### Calendar View Visual Validation
- **Calendar Grid**: Consistent day cell sizes, proper date formatting
- **Task Events**: Color coding, time display, event styling
- **Month/Week/Day Views**: Consistent navigation and layout
- **Responsive Behavior**: Mobile vs desktop layouts
- **Task Overlap Handling**: Visual stacking and collision detection

#### Canvas View Visual Analysis
- **Task Nodes**: Consistent sizing, status colors, typography
- **Connection Lines**: Proper visual hierarchy, color coding
- **Section Containers**: Consistent styling, collapse indicators
- **Viewport Controls**: Zoom controls, minimap positioning
- **Selection Indicators**: Multi-selection visual feedback

#### Timer Component Visual Consistency
- **Timer Display**: Consistent font sizing, color states (running/paused)
- **Control Buttons**: Consistent button styling and icon usage
- **Progress Indicators**: Visual progress representation
- **Notification Overlays**: Consistent modal styling
- **Task Integration**: Visual link between timer and current task

### Phase 3: Advanced Visual Analysis Engine

#### Color Consistency Analysis
```typescript
class ColorConsistencyAnalyzer {
  async analyzeColorConsistency(): Promise<ColorIssue[]> {
    const issues: ColorIssue[] = [];

    // Extract design system colors
    const designColors = await this.extractDesignSystemColors();

    // Analyze page elements
    const elements = await this.page.$$('*:not(style):not(script)');

    for (const element of elements) {
      const styles = await this.getComputedStyles(element);

      // Check for design system violations
      if (!this.isValidDesignColor(styles.color, designColors.textColors)) {
        issues.push(this.createColorIssue({
          element,
          type: 'brand_violation',
          property: 'color',
          actual: styles.color,
          expected: designColors.textColors
        }));
      }

      // Check contrast ratios
      const contrast = this.calculateContrastRatio(
        styles.color,
        styles.backgroundColor
      );

      if (contrast < 4.5) { // WCAG AA standard
        issues.push(this.createColorIssue({
          element,
          type: 'contrast',
          property: 'color',
          contrast,
          wcagLevel: contrast >= 3 ? 'AA' : 'fail'
        }));
      }
    }

    return issues;
  }
}
```

#### Typography Consistency Analysis
```typescript
class TypographyAnalyzer {
  async analyzeTypographyConsistency(): Promise<TypographyIssue[]> {
    const issues: TypographyIssue[] = [];

    // Extract typography design tokens
    const typographySystem = await this.extractTypographyTokens();

    // Analyze text elements
    const textElements = await this.page.$$('h1, h2, h3, h4, h5, h6, p, span, div');

    for (const element of textElements) {
      const styles = await this.getComputedStyles(element);
      const textContent = await element.textContent();

      if (!textContent || textContent.trim().length === 0) continue;

      // Check for font family consistency
      if (!typographySystem.fontFamilies.includes(styles.fontFamily)) {
        issues.push({
          element: await this.getElementSelector(element),
          type: 'invalid_font_family',
          severity: 'medium',
          actual: styles.fontFamily,
          expected: typographySystem.fontFamilies,
          textContent: textContent.substring(0, 50)
        });
      }

      // Check for font size consistency
      if (!this.isValidFontSize(styles.fontSize, typographySystem.fontSizes)) {
        issues.push({
          element: await this.getElementSelector(element),
          type: 'invalid_font_size',
          severity: 'low',
          actual: styles.fontSize,
          expected: typographySystem.fontSizes,
          textContent: textContent.substring(0, 50)
        });
      }
    }

    return issues;
  }
}
```

### Phase 4: Cross-View Visual Comparison

#### Visual Regression Testing
```typescript
class CrossViewComparator {
  async compareViews(): Promise<CrossViewIssue[]> {
    const issues: CrossViewIssue[] = [];
    const views = ['board', 'calendar', 'canvas'];
    const componentScreenshots = new Map<string, Map<string, Buffer>>();

    // Capture consistent components across views
    const consistentComponents = [
      '.nav-tabs',           // Navigation tabs
      '.app-header',         // Application header
      '.task-card',          // Task cards
      '.button',             // Buttons
      '.timer-display'       // Timer display
    ];

    for (const view of views) {
      await this.page.click(`[data-view="${view}"]`);
      await this.page.waitForTimeout(2000);

      componentScreenshots.set(view, new Map());

      for (const componentSelector of consistentComponents) {
        const elements = await this.page.$$(componentSelector);
        if (elements.length > 0) {
          const screenshot = await elements[0].screenshot();
          componentScreenshots.get(view)!.set(componentSelector, screenshot);
        }
      }
    }

    // Compare component screenshots across views
    for (const componentSelector of consistentComponents) {
      const screenshots = Array.from(componentScreenshots.values())
        .map(view => view.get(componentSelector))
        .filter(Boolean);

      if (screenshots.length >= 2) {
        const differences = await this.compareScreenshots(screenshots);

        if (differences.length > 0) {
          issues.push({
            component: componentSelector,
            type: 'visual_inconsistency',
            severity: 'medium',
            differences,
            affectedViews: views.filter(view =>
              componentScreenshots.get(view)?.has(componentSelector)
            )
          });
        }
      }
    }

    return issues;
  }
}
```

### Phase 5: Accessibility Visual Analysis

#### Visual Accessibility Testing
```typescript
class VisualAccessibilityAnalyzer {
  async analyzeVisualAccessibility(): Promise<AccessibilityViolation[]> {
    const violations: AccessibilityViolation[] = [];

    // Check focus indicators
    const focusableElements = await this.page.$$('button, input, select, textarea, a, [tabindex]');

    for (const element of focusableElements) {
      // Focus the element
      await element.focus();
      await this.page.waitForTimeout(100);

      // Check if focus indicator is visible
      const focusStyles = await this.getComputedStyles(element);
      const hasVisibleFocus = this.hasVisibleFocusIndicator(focusStyles);

      if (!hasVisibleFocus) {
        violations.push({
          element: await this.getElementSelector(element),
          type: 'missing_focus_indicator',
          severity: 'high',
          wcagCriterion: '2.4.7 Focus Visible',
          description: 'Element does not have a visible focus indicator'
        });
      }
    }

    // Check color contrast for all text elements
    const textElements = await this.page.$$('p, h1, h2, h3, h4, h5, h6, span, div');

    for (const element of textElements) {
      const textContent = await element.textContent();
      if (!textContent || textContent.trim().length === 0) continue;

      const styles = await this.getComputedStyles(element);
      const contrast = this.calculateContrastRatio(
        styles.color,
        styles.backgroundColor
      );

      const isLargeText = parseFloat(styles.fontSize) >= 18 ||
                        parseFloat(styles.fontSize) >= 14 && styles.fontWeight >= 700;

      const requiredContrast = isLargeText ? 3 : 4.5;

      if (contrast < requiredContrast) {
        violations.push({
          element: await this.getElementSelector(element),
          type: 'insufficient_contrast',
          severity: 'high',
          wcagCriterion: '1.4.3 Contrast (Minimum)',
          contrast,
          requiredContrast,
          isLargeText,
          textContent: textContent.substring(0, 50)
        });
      }
    }

    return violations;
  }
}
```

### Phase 6: Responsive Design Analysis

#### Multi-Viewport Testing
```typescript
class ResponsiveDesignAnalyzer {
  async analyzeResponsiveDesign(): Promise<ResponsiveIssue[]> {
    const issues: ResponsiveIssue[] = [];
    const viewports = [
      { name: 'mobile', width: 375, height: 667 },
      { name: 'tablet', width: 768, height: 1024 },
      { name: 'desktop', width: 1920, height: 1080 }
    ];

    for (const viewport of viewports) {
      await this.page.setViewportSize({ width: viewport.width, height: viewport.height });
      await this.page.waitForTimeout(1000);

      // Check for horizontal scrolling
      const hasHorizontalScroll = await this.page.evaluate(() => {
        return document.body.scrollWidth > document.body.clientWidth;
      });

      if (hasHorizontalScroll) {
        issues.push({
          type: 'horizontal_scroll',
          severity: 'high',
          viewport: viewport.name,
          description: `Page has horizontal scroll on ${viewport.name} viewport`
        });
      }

      // Check for overlapping elements
      const overlaps = await this.detectOverlappingElements();
      if (overlaps.length > 0) {
        issues.push({
          type: 'overlapping_elements',
          severity: 'medium',
          viewport: viewport.name,
          overlaps
        });
      }

      // Check text readability
      const tinyText = await this.findTinyTextElements();
      if (tinyText.length > 0) {
        issues.push({
          type: 'unreadable_text',
          severity: 'medium',
          viewport: viewport.name,
          elements: tinyText
        });
      }

      // Take screenshot for visual reference
      await this.takeScreenshot(`responsive-${viewport.name}`);
    }

    return issues;
  }
}
```

## PomoFlow-Specific Visual Tests

### Board View Visual Validation
```typescript
const boardViewTests = {
  taskCardConsistency: {
    test: async () => {
      // Check all task cards have consistent styling
      const taskCards = await page.$$('.task-card');
      const baseStyles = await getComputedStyles(taskCards[0]);

      for (let i = 1; i < taskCards.length; i++) {
        const styles = await getComputedStyles(taskCards[i]);
        const inconsistencies = compareStyles(baseStyles, styles, [
          'backgroundColor', 'borderColor', 'borderRadius', 'fontFamily'
        ]);

        if (inconsistencies.length > 0) {
          return {
            passed: false,
            inconsistencies,
            elementIndex: i
          };
        }
      }

      return { passed: true };
    }
  },

  statusIndicatorConsistency: {
    test: async () => {
      // Check status indicators use consistent colors
      const statusElements = await page.$$('[data-status]');
      const statusColors = new Map();

      for (const element of statusElements) {
        const status = await element.getAttribute('data-status');
        const bgColor = await getComputedStyle(element, 'backgroundColor');

        if (statusColors.has(status) && statusColors.get(status) !== bgColor) {
          return {
            passed: false,
            status,
            expectedColor: statusColors.get(status),
            actualColor: bgColor
          };
        }

        statusColors.set(status, bgColor);
      }

      return { passed: true, statusColors: Object.fromEntries(statusColors) };
    }
  }
}
```

### Calendar View Visual Validation
```typescript
const calendarViewTests = {
  calendarGridConsistency: {
    test: async () => {
      // Check calendar grid cells are uniform
      const dayCells = await page.$$('.calendar-day, .day-cell');
      const baseDimensions = await dayCells[0].boundingBox();

      const inconsistentCells = [];
      for (let i = 1; i < dayCells.length; i++) {
        const dimensions = await dayCells[i].boundingBox();

        if (Math.abs(dimensions!.width - baseDimensions!.width) > 2 ||
            Math.abs(dimensions!.height - baseDimensions!.height) > 2) {
          inconsistentCells.push({
            index: i,
            expected: baseDimensions,
            actual: dimensions
          });
        }
      }

      return {
        passed: inconsistentCells.length === 0,
        inconsistentCells
      };
    }
  },

  eventColorConsistency: {
    test: async () => {
      // Check task events use consistent colors based on status/priority
      const taskEvents = await page.$$('.task-event, .calendar-event');
      const eventColors = new Map();

      for (const event of taskEvents) {
        const bgColor = await getComputedStyle(event, 'backgroundColor');
        const taskTitle = await event.$('.task-title')?.textContent();

        if (taskTitle) {
          eventColors.set(taskTitle, bgColor);
        }
      }

      // Analyze color patterns
      const colorGroups = groupSimilarColors(Array.from(eventColors.values()));

      return {
        passed: colorGroups.length <= 10, // Reasonable number of color groups
        colorGroups,
        totalEvents: taskEvents.length
      };
    }
  }
}
```

### Canvas View Visual Validation
```typescript
const canvasViewTests = {
  taskNodeConsistency: {
    test: async () => {
      // Check task nodes have consistent visual styling
      const taskNodes = await page.$$('.vue-flow__node, .task-node');
      const nodeStyles = new Map();

      for (const node of taskNodes) {
        const styles = await getComputedStyles(node);
        const styleKey = `${styles.backgroundColor}|${styles.borderColor}|${styles.borderRadius}`;

        nodeStyles.set(styleKey, (nodeStyles.get(styleKey) || 0) + 1);
      }

      const mostCommonStyle = Math.max(...nodeStyles.values());
      const totalNodes = taskNodes.length;
      const consistency = mostCommonStyle / totalNodes;

      return {
        passed: consistency >= 0.8, // 80% consistency
        consistency,
        styleVariations: nodeStyles.size,
        mostCommonStyle,
        totalNodes
      };
    }
  },

  connectionLineConsistency: {
    test: async () => {
      // Check connection lines use consistent styling
      const connections = await page.$$('.vue-flow__edge, .task-connection');
      const connectionStyles = new Map();

      for (const connection of connections) {
        const strokeColor = await getComputedStyle(connection, 'stroke');
        const strokeWidth = await getComputedStyle(connection, 'strokeWidth');

        const styleKey = `${strokeColor}|${strokeWidth}`;
        connectionStyles.set(styleKey, (connectionStyles.get(styleKey) || 0) + 1);
      }

      return {
        passed: connectionStyles.size <= 3, // Allow for different connection types
        styleVariations: connectionStyles.size,
        totalConnections: connections.length,
        styles: Object.fromEntries(connectionStyles)
      };
    }
  }
}
```

## Analysis Engine Implementation

### Main Visual Analyzer Class
```typescript
class VisualInconsistencyDetector {
  async analyzeApplication(baseUrl: string = 'http://localhost:5546'): Promise<VisualAnalysisReport> {
    const report: VisualAnalysisReport = {
      timestamp: new Date().toISOString(),
      applicationUrl: baseUrl,
      designSystemScore: 0,
      colorConsistencyIssues: [],
      typographyIssues: [],
      spacingIssues: [],
      componentInconsistencies: [],
      responsiveDesignIssues: [],
      accessibilityViolations: [],
      crossViewInconsistencies: [],
      testResults: {},
      screenshots: []
    };

    // Initialize browser
    await this.initializeBrowser();

    try {
      // Navigate to application
      await this.page.goto(baseUrl);
      await this.page.waitForSelector('#app');

      // Run visual analysis phases
      await this.analyzeColorConsistency();
      await this.analyzeTypographyConsistency();
      await this.analyzeSpacingConsistency();
      await this.analyzeComponentConsistency();
      await this.analyzeCrossViewConsistency();
      await this.analyzeResponsiveDesign();
      await this.analyzeVisualAccessibility();

      // Run PomoFlow-specific tests
      await this.runPomoFlowVisualTests();

      // Calculate overall score
      this.calculateDesignSystemScore();

      return report;

    } finally {
      await this.cleanup();
    }
  }
}
```

## Usage Examples

### Comprehensive Visual Analysis
```bash
# Run full visual inconsistency detection
node .claude/skills/visual-inconsistency-detector/detect.js

# Analyze specific visual aspects
node .claude/skills/visual-inconsistency-detector/detect.js --focus=colors,typography

# Generate detailed visual report
node .claude/skills/visual-inconsistency-detector/detect.js --report=detailed --output=visual-report.json
```

### PomoFlow-Specific Visual Testing
```bash
# Test PomoFlow visual consistency
node .claude/skills/visual-inconsistency-detector/pomoflow-visual-test.js

# Compare views visually
node .claude/skills/visual-inconsistency-detector/pomoflow-visual-test.js --compare-views

# Test accessibility compliance
node .claude/skills/visual-inconsistency-detector/pomoflow-visual-test.js --accessibility
```

### Continuous Visual Testing
```bash
# Run visual regression testing
node .claude/skills/visual-inconsistency-detector/regression-test.js

# Compare with baseline screenshots
node .claude/skills/visual-inconsistency-detector/regression-test.js --baseline

# Generate visual diff report
node .claude/skills/visual-inconsistency-detector/regression-test.js --diff
```

## Expected Outcomes
After successful execution:
- ✅ **Complete Design System Analysis**: Every visual aspect systematically checked against design tokens
- ✅ **Color Consistency Validation**: All colors validated against design system and WCAG standards
- ✅ **Typography Consistency Check**: Font usage and sizing validated across all components
- ✅ **Cross-View Visual Comparison**: Consistency verified across Board/Calendar/Canvas views
- ✅ **Accessibility Compliance**: Visual accessibility issues identified and documented
- ✅ **Responsive Design Analysis**: Layout tested across mobile, tablet, and desktop viewports
- ✅ **Visual Regression Detection**: Changes from baseline screenshots identified and flagged
- ✅ **Actionable Visual Report**: Prioritized list of visual issues with fix suggestions

## Success Criteria
- [ ] Design system compliance score above 85%
- [ ] No critical accessibility violations (WCAG AA)
- [ ] Cross-view consistency maintained for all shared components
- [ ] Responsive design works across all target viewports
- [ ] Color contrast meets WCAG AA standards for all text
- [ ] Typography follows established design tokens
- [ ] Visual regression baseline established and monitored
- [ ] All visual issues documented with screenshots and fix suggestions

## 🚨 CRITICAL VISUAL TESTING REQUIREMENTS

### **Comprehensive Visual Validation Protocol**
**EVERY visual analysis result MUST be validated through:**

1. **Screenshot Evidence**: Every visual issue must include screenshot evidence
2. **Design Token Comparison**: Actual styles compared against expected design system values
3. **Cross-Viewport Testing**: Visual consistency verified across all screen sizes
4. **Accessibility Measurement**: WCAG compliance measured with objective tools
5. **Cross-View Comparison**: Same components compared across different views
6. **Baseline Regression**: Current state compared against established visual baseline

### **Visual Analysis Validation Checklist**
Before claiming visual analysis is complete:
- [ ] All color schemes validated against design system
- [ ] Typography consistency verified across all components
- [ ] Cross-view visual differences documented and prioritized
- [ ] Accessibility compliance measured and documented
- [ ] Responsive design tested across all target viewports
- [ ] Visual regression baseline captured and stored
- [ ] All visual issues include actionable fix suggestions
- [ ] Analysis results include visual evidence for every finding

## 🚨 CRITICAL REMINDER

**NEVER claim visual analysis is complete without comprehensive visual evidence:**
1. **Screenshot Evidence**: Every issue must include clear visual evidence
2. **Measurement Data**: Color contrast, font sizes, spacing measurements must be provided
3. **Cross-View Documentation**: Differences between views must be documented with evidence
4. **Accessibility Measurements**: WCAG compliance must be measured, not estimated
5. **Responsive Validation**: All viewport variations must be tested and documented

**ONLY claim visual consistency is validated after comprehensive measurement and evidence collection proves it actually works for real users.**

---

## MANDATORY USER VERIFICATION REQUIREMENT

### Policy: No Fix Claims Without User Confirmation

**CRITICAL**: Before claiming ANY issue, bug, or problem is "fixed", "resolved", "working", or "complete", the following verification protocol is MANDATORY:

#### Step 1: Technical Verification
- Run all relevant tests (build, type-check, unit tests)
- Verify no console errors
- Take screenshots/evidence of the fix

#### Step 2: User Verification Request
**REQUIRED**: Use the `AskUserQuestion` tool to explicitly ask the user to verify the fix:

```
"I've implemented [description of fix]. Before I mark this as complete, please verify:
1. [Specific thing to check #1]
2. [Specific thing to check #2]
3. Does this fix the issue you were experiencing?

Please confirm the fix works as expected, or let me know what's still not working."
```

#### Step 3: Wait for User Confirmation
- **DO NOT** proceed with claims of success until user responds
- **DO NOT** mark tasks as "completed" without user confirmation
- **DO NOT** use phrases like "fixed", "resolved", "working" without user verification

#### Step 4: Handle User Feedback
- If user confirms: Document the fix and mark as complete
- If user reports issues: Continue debugging, repeat verification cycle

### Prohibited Actions (Without User Verification)
- Claiming a bug is "fixed"
- Stating functionality is "working"
- Marking issues as "resolved"
- Declaring features as "complete"
- Any success claims about fixes

### Required Evidence Before User Verification Request
1. Technical tests passing
2. Visual confirmation via Playwright/screenshots
3. Specific test scenarios executed
4. Clear description of what was changed

**Remember: The user is the final authority on whether something is fixed. No exceptions.**
