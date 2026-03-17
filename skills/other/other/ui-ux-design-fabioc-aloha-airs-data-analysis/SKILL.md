---
name: "UI/UX Design"
description: "User interface design, user experience optimization, accessibility compliance, design systems"
---

# UI/UX Design

**Domain**: User interface design, user experience optimization, accessibility compliance, design systems  
**Applicable To**: Web applications, VS Code extensions, mobile apps, desktop software  
**Skill Type**: Systematic design audit, accessibility validation, design system implementation

---

## Level 1: Quick Reference

### Core Design Principles

**Visual Hierarchy**
- Typography scale: base size ≥11px for WCAG AA compliance
- Weight progression: 400 (regular) → 500 (medium) → 600 (semibold) → 700 (bold)
- Size jumps: ~2px increments (11px → 13px → 14px → 16px → 18px → 20px)

**Spacing System**
- Base unit: 4px or 8px (8px recommended for touch interfaces)
- Scale: base × 0.5, 1, 2, 3, 4, 6, 8, 12 (e.g., 4px, 8px, 16px, 24px, 32px, 48px, 64px, 96px)
- Consistency: All margins, padding, gaps use scale values

**Color & Contrast**
- WCAG AA minimum: 4.5:1 for normal text, 3:1 for large text (≥18px or ≥14px bold)
- WCAG AAA enhanced: 7:1 for normal text, 4.5:1 for large text
- Color-blind safety: Never rely on color alone (add icons, patterns, text labels)

**Touch Targets**
- Minimum size: 44×44px (WCAG 2.1 AA Level 2.5.5)
- Recommended: 48×48px for primary actions
- Spacing: Minimum 8px between adjacent targets

### WCAG 2.1 AA Compliance Checklist

**Perceivable**
- ✓ Text alternatives (alt text, aria-label) for non-text content
- ✓ Color contrast ratio ≥4.5:1 for normal text, ≥3:1 for large text
- ✓ Text resizable up to 200% without loss of functionality
- ✓ No information conveyed by color alone

**Operable**
- ✓ All functionality available via keyboard (tabindex, focus management)
- ✓ Focus indicators visible (:focus-visible styles)
- ✓ Touch targets ≥44×44px
- ✓ No keyboard traps (can tab away from all interactive elements)

**Understandable**
- ✓ Semantic HTML (header, nav, main, article, aside, footer)
- ✓ ARIA roles for custom components (button, dialog, menu, tab, progressbar)
- ✓ Form labels associated with inputs (for/id or aria-labelledby)
- ✓ Error messages clear and actionable

**Robust**
- ✓ Valid HTML (no unclosed tags, proper nesting)
- ✓ ARIA attributes used correctly (aria-valuenow/min/max for progressbar)
- ✓ Compatible with assistive technologies (screen readers, keyboard-only)

### Design System Quick Setup

**CSS Variables Pattern**
```css
:root {
  /* Typography Scale */
  --font-xs: 11px;    /* Minimum legal size */
  --font-sm: 12px;    /* Secondary text */
  --font-md: 14px;    /* Body text (VS Code default) */
  --font-lg: 16px;    /* Headings, emphasis */
  --font-xl: 18px;    /* Large headings */
  
  /* Spacing Scale (8px base) */
  --spacing-xs: 4px;  /* Tight spacing */
  --spacing-sm: 8px;  /* Default gap */
  --spacing-md: 16px; /* Section padding */
  --spacing-lg: 24px; /* Card padding */
  --spacing-xl: 32px; /* Page margins */
  
  /* Theme-aware Colors */
  --text-primary: var(--vscode-foreground);
  --text-secondary: var(--vscode-descriptionForeground);
  --bg-primary: var(--vscode-editor-background);
  --bg-secondary: var(--vscode-sideBar-background);
  --border-color: var(--vscode-panel-border);
  --accent: var(--vscode-button-background);
}
```

---

## Level 2: Detailed Practices

### Systematic UI/UX Audit Process

**Phase 1: Visual Assessment**
1. **Typography Audit**
   - Measure all font sizes (dev tools inspector)
   - Flag sizes <11px (WCAG AA violation)
   - Check line-height: 1.4-1.6 for body text
   - Verify font-weight consistency (avoid random weights like 450, 550)

2. **Spacing Audit**
   - Inspect margins/padding across components
   - Identify spacing values (e.g., 7px, 13px, 21px = inconsistent)
   - Calculate base unit: find GCD of all spacing values
   - Normalize to scale (e.g., 13px → 12px or 16px)

3. **Color Audit**
   - Screenshot all color combinations (text on background)
   - Use contrast checker (WebAIM, Chrome DevTools)
   - Document violations with severity:
     - **P0**: <3:1 ratio (immediate fix)
     - **P1**: 3:1-4.49:1 ratio (fails AA for normal text)
     - **P2**: 4.5:1-6.99:1 ratio (passes AA, fails AAA)

4. **Touch Target Audit**
   - Measure interactive elements (buttons, links, checkboxes)
   - Flag elements <44px in either dimension
   - Check spacing between adjacent targets (<8px = risk of mis-taps)

**Phase 2: Accessibility Assessment**
1. **Keyboard Navigation Test**
   - Tab through entire interface
   - Verify focus visible on all interactive elements
   - Check focus order matches visual order
   - Ensure no keyboard traps (can tab away from modals, menus)

2. **Screen Reader Test**
   - Use NVDA (Windows), VoiceOver (Mac), or Narrator
   - Verify all interactive elements have labels
   - Check landmark regions announced (navigation, main, complementary)
   - Confirm form fields have associated labels

3. **Semantic HTML Audit**
   - Inspect DOM structure
   - Replace `<div>` buttons with `<button>` or `role="button"`
   - Use `<nav>`, `<article>`, `<aside>`, `<section>` for structure
   - Add ARIA roles only when semantic HTML insufficient

4. **Color-Blind Safety Test**
   - Use color-blindness simulator (Coblis, Chrome DevTools)
   - Check status indicators (success/warning/error) visible without color
   - Add icons, patterns, or text labels to color-coded elements

**Phase 3: Design System Implementation**
1. **Extract Design Tokens**
   - List all unique font sizes → create typography scale
   - List all unique spacing values → create spacing scale
   - List all colors → map to semantic variables (primary, secondary, accent, etc.)

2. **Create CSS Variables**
   - Define tokens in `:root` or component scope
   - Use semantic names (`--font-body`, not `--font-14px`)
   - Reference theme colors (`var(--vscode-foreground)`, not hardcoded hex)

3. **Apply Design Tokens**
   - Replace hardcoded values with variables
   - Example: `font-size: 14px` → `font-size: var(--font-md)`
   - Example: `margin: 16px` → `margin: var(--spacing-md)`

4. **Document Design System**
   - Create design system reference (README or style guide)
   - Include token table with usage guidelines
   - Add code examples for common patterns

### Accessibility Patterns Library

**Focus Indicators**
```css
/* VS Code-aware focus styling */
:focus-visible {
  outline: 2px solid var(--vscode-focusBorder);
  outline-offset: 2px;
  border-radius: 4px;
}

/* Remove outline for mouse users */
:focus:not(:focus-visible) {
  outline: none;
}
```

**Color-Blind Safe Status Indicators**
```css
/* Status dots with icons via ::after */
.status-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  position: relative;
}

.status-dot.success {
  background: #4caf50; /* Green */
}
.status-dot.success::after {
  content: '✓'; /* Checkmark icon */
  position: absolute;
  color: white;
  font-size: 10px;
  font-weight: bold;
  top: -1px;
  left: 1px;
}

.status-dot.warning {
  background: #ff9800; /* Orange */
}
.status-dot.warning::after {
  content: '⚠'; /* Warning icon */
  position: absolute;
  color: white;
  font-size: 10px;
  top: -2px;
  left: 0px;
}

.status-dot.error {
  background: #f44336; /* Red */
}
.status-dot.error::after {
  content: '✗'; /* X icon */
  position: absolute;
  color: white;
  font-size: 10px;
  font-weight: bold;
  top: -1px;
  left: 2px;
}
```

**ARIA Progressbar**
```html
<!-- Accessible progress bar -->
<div role="progressbar" 
     aria-valuenow="65" 
     aria-valuemin="0" 
     aria-valuemax="100"
     aria-label="Task completion">
  <div class="progress-fill" style="width: 65%"></div>
</div>
```

**Accessible Buttons**
```html
<!-- Semantic button with ARIA -->
<button type="button" 
        tabindex="0"
        aria-label="Generate architecture diagram"
        class="action-button">
  Generate Diagram
</button>

<!-- Div styled as button (use sparingly) -->
<div role="button" 
     tabindex="0"
     aria-label="Close panel"
     class="close-button"
     onclick="handleClick()"
     onkeypress="if(event.key==='Enter'||event.key===' ')handleClick()">
  ×
</div>
```

**Card Layout with Semantic HTML**
```html
<article class="card" role="article">
  <header>
    <h3>Skill Name</h3>
  </header>
  <div class="card-body">
    <p>Description text...</p>
  </div>
  <footer>
    <button aria-label="Activate skill">Activate</button>
  </footer>
</article>
```

### Design System Implementation Workflow

**Step 1: Audit Current State**
```bash
# Extract all font-size declarations
grep -r "font-size:" src/ | grep -oP "\d+px" | sort -u

# Extract all spacing values (margin, padding)
grep -r -E "(margin|padding):" src/ | grep -oP "\d+px" | sort -u

# Count unique colors
grep -r -E "(color|background):" src/ | grep -oP "#[0-9a-fA-F]{3,6}" | sort -u
```

**Step 2: Calculate Base Unit**
```
Spacing values found: 4px, 8px, 12px, 16px, 20px, 24px, 32px
GCD = 4px → Base unit = 4px
Scale: 1×, 2×, 3×, 4×, 5×, 6×, 8× (0.25rem, 0.5rem, 0.75rem, 1rem, 1.25rem, 1.5rem, 2rem)
```

**Step 3: Create Token System**
```javascript
// Design tokens as JavaScript object
const tokens = {
  typography: {
    xs: '11px',  // Legal minimum
    sm: '12px',  // Secondary
    md: '14px',  // Body
    lg: '16px',  // Heading
    xl: '18px'   // Large heading
  },
  spacing: {
    xs: '4px',
    sm: '8px',
    md: '16px',
    lg: '24px',
    xl: '32px'
  },
  colors: {
    primary: 'var(--vscode-button-background)',
    secondary: 'var(--vscode-button-secondaryBackground)',
    text: 'var(--vscode-foreground)',
    textMuted: 'var(--vscode-descriptionForeground)',
    border: 'var(--vscode-panel-border)',
    success: '#4caf50',
    warning: '#ff9800',
    error: '#f44336'
  }
};
```

**Step 4: Generate CSS Variables**
```css
:root {
  /* Typography */
  --font-xs: 11px;
  --font-sm: 12px;
  --font-md: 14px;
  --font-lg: 16px;
  --font-xl: 18px;
  
  /* Spacing */
  --spacing-xs: 4px;
  --spacing-sm: 8px;
  --spacing-md: 16px;
  --spacing-lg: 24px;
  --spacing-xl: 32px;
  
  /* Colors (theme-aware) */
  --color-primary: var(--vscode-button-background);
  --color-text: var(--vscode-foreground);
  --color-border: var(--vscode-panel-border);
  --color-success: #4caf50;
  --color-warning: #ff9800;
  --color-error: #f44336;
}
```

**Step 5: Apply Design Tokens**
```css
/* Before: Hardcoded values */
.button {
  font-size: 14px;
  padding: 8px 16px;
  background: #007acc;
  color: #ffffff;
}

/* After: Design tokens */
.button {
  font-size: var(--font-md);
  padding: var(--spacing-sm) var(--spacing-md);
  background: var(--color-primary);
  color: var(--color-text);
}
```

### Testing & Validation

**Manual Testing Checklist**
- [ ] Tab through all interactive elements (keyboard navigation)
- [ ] Verify focus visible on all focusable elements
- [ ] Test with screen reader (NVDA, VoiceOver, Narrator)
- [ ] Zoom to 200% (Ctrl/Cmd +) - verify no content cut off
- [ ] Test with Windows High Contrast mode
- [ ] Simulate color blindness (Deuteranopia, Protanopia, Tritanopia)
- [ ] Test on mobile device or touch simulator (Chrome DevTools)
- [ ] Verify minimum touch target size (44×44px)

**Automated Testing Tools**
- **axe DevTools**: Browser extension for WCAG violations
- **Lighthouse**: Chrome DevTools → Accessibility score
- **WAVE**: Web Accessibility Evaluation Tool
- **Color Contrast Analyzer**: Desktop app for WCAG contrast checking
- **Pa11y**: Command-line accessibility testing

**Validation Scripts**
```javascript
// Check for minimum font sizes
const elements = document.querySelectorAll('*');
elements.forEach(el => {
  const fontSize = parseFloat(window.getComputedStyle(el).fontSize);
  if (fontSize < 11 && fontSize > 0) {
    console.warn('Font too small:', el, fontSize + 'px');
  }
});

// Check for touch target sizes
const interactive = document.querySelectorAll('button, a, input, [role="button"]');
interactive.forEach(el => {
  const rect = el.getBoundingClientRect();
  if (rect.width < 44 || rect.height < 44) {
    console.warn('Touch target too small:', el, rect.width + '×' + rect.height + 'px');
  }
});

// Check for missing ARIA labels
const buttons = document.querySelectorAll('button, [role="button"]');
buttons.forEach(btn => {
  if (!btn.textContent.trim() && !btn.getAttribute('aria-label')) {
    console.error('Button missing label:', btn);
  }
});
```

---

## Level 3: Resources & References

### WCAG 2.1 Specification

**Official Documentation**
- WCAG 2.1 Guidelines: https://www.w3.org/WAI/WCAG21/quickref/
- Understanding WCAG 2.1: https://www.w3.org/WAI/WCAG21/Understanding/
- ARIA Authoring Practices: https://www.w3.org/WAI/ARIA/apg/

**Key Success Criteria**
- **1.4.3 Contrast (Minimum)** - Level AA: 4.5:1 normal text, 3:1 large text
- **1.4.6 Contrast (Enhanced)** - Level AAA: 7:1 normal text, 4.5:1 large text
- **1.4.10 Reflow** - Content reflows at 320px width (400% zoom)
- **1.4.11 Non-text Contrast** - 3:1 for UI components and graphical objects
- **1.4.12 Text Spacing** - No loss of content with increased spacing
- **2.1.1 Keyboard** - All functionality via keyboard
- **2.4.7 Focus Visible** - Keyboard focus indicator visible
- **2.5.5 Target Size** - Touch targets ≥44×44px (Level AAA)
- **4.1.2 Name, Role, Value** - ARIA attributes for custom components

### Design Systems Examples

**Material Design 3**
- Typography: 11 type scales (Display, Headline, Title, Body, Label)
- Spacing: 4px base unit, 8dp grid system
- Color: Dynamic color from seed, contrast-safe palettes
- Components: 40+ accessible components with ARIA
- Link: https://m3.material.io/

**Apple Human Interface Guidelines**
- Typography: SF Pro font family, Dynamic Type support
- Spacing: 8pt grid, consistent margins
- Touch Targets: 44pt minimum
- Accessibility: VoiceOver, Dynamic Type, Reduced Motion
- Link: https://developer.apple.com/design/human-interface-guidelines/

**Microsoft Fluent Design**
- Typography: Segoe UI Variable, type ramp
- Spacing: 4px base unit
- Components: React, Web Components, .NET
- Accessibility: Built-in ARIA, keyboard navigation
- Link: https://fluent2.microsoft.design/

**VS Code Design Guidelines**
- Colors: Theme-aware CSS variables (`--vscode-*`)
- Typography: VS Code font stack, 13px default
- Icons: Codicons icon font
- Components: Webview UI Toolkit
- Link: https://code.visualstudio.com/api/references/extension-guidelines

### Design Tools & Resources

**Accessibility Testing**
- **axe DevTools**: https://www.deque.com/axe/devtools/
- **WAVE**: https://wave.webaim.org/
- **Lighthouse**: Built into Chrome DevTools
- **Color Contrast Analyzer**: https://www.tpgi.com/color-contrast-checker/
- **WebAIM Contrast Checker**: https://webaim.org/resources/contrastchecker/

**Color-Blindness Simulators**
- **Coblis**: https://www.color-blindness.com/coblis-color-blindness-simulator/
- **Chrome DevTools**: DevTools → Rendering → Emulate vision deficiencies
- **Photoshop/Figma**: Built-in color-blind preview modes

**Design Token Tools**
- **Style Dictionary**: Build system for design tokens
- **Theo**: Salesforce design token tool
- **Tokens Studio**: Figma plugin for design tokens
- **CSS Variables Spec**: https://www.w3.org/TR/css-variables/

**Screen Readers**
- **NVDA** (Windows, free): https://www.nvaccess.org/
- **VoiceOver** (Mac, built-in): Cmd+F5 to enable
- **Narrator** (Windows, built-in): Win+Ctrl+Enter to enable
- **JAWS** (Windows, commercial): https://www.freedomscientific.com/products/software/jaws/

### Code Examples Repository

**Accessible Component Patterns**
```html
<!-- Modal Dialog -->
<div role="dialog" 
     aria-labelledby="dialog-title"
     aria-describedby="dialog-desc"
     aria-modal="true">
  <h2 id="dialog-title">Confirm Action</h2>
  <p id="dialog-desc">Are you sure you want to proceed?</p>
  <button aria-label="Confirm">OK</button>
  <button aria-label="Cancel">Cancel</button>
</div>

<!-- Tab Panel -->
<div role="tablist" aria-label="Settings tabs">
  <button role="tab" aria-selected="true" aria-controls="panel-1">General</button>
  <button role="tab" aria-selected="false" aria-controls="panel-2">Advanced</button>
</div>
<div id="panel-1" role="tabpanel">General settings...</div>
<div id="panel-2" role="tabpanel" hidden>Advanced settings...</div>

<!-- Combobox (Autocomplete) -->
<label for="search">Search</label>
<input id="search" 
       role="combobox"
       aria-autocomplete="list"
       aria-expanded="false"
       aria-controls="results">
<ul id="results" role="listbox" hidden>
  <li role="option">Result 1</li>
  <li role="option">Result 2</li>
</ul>
```

### Related Skills

**Direct Dependencies**
- **graphic-design**: Visual identity, logo design, brand consistency
- **code-review**: Accessibility code quality validation
- **testing-strategies**: Automated accessibility testing integration

**Complementary Skills**
- **markdown-mermaid**: Diagram accessibility (alt text, semantic structure)
- **vscode-extension-patterns**: Webview UI patterns, theme integration
- **localization**: Internationalization, RTL support, cultural considerations

### Common Pitfalls

**Typography Mistakes**
- Using font sizes <11px (WCAG violation)
- Inconsistent font weights (mixing 450, 500, 550)
- Line-height too tight (<1.4 for body text)
- Font color insufficient contrast

**Spacing Mistakes**
- Random spacing values (7px, 13px, 21px) instead of scale
- Inconsistent padding within similar components
- Touch targets too close together (<8px spacing)

**Accessibility Mistakes**
- Using `<div>` instead of `<button>` for clickable elements
- Missing `aria-label` on icon-only buttons
- No visible focus indicator
- Color-only status indicators (no icons/text)
- Touch targets <44×44px

**Design Token Mistakes**
- Hardcoding theme colors (breaks dark mode)
- Using presentational names (`--blue-500`) instead of semantic (`--color-primary`)
- Not using CSS variables consistently
- Missing fallback values for older browsers

### Performance Considerations

**CSS Variables Performance**
- CSS variables have minimal performance impact
- Prefer `:root` scope for global tokens
- Use component scope for component-specific overrides
- Avoid excessive `calc()` operations with variables

**Accessibility Tree Performance**
- Excessive ARIA attributes can slow screen readers
- Use semantic HTML instead of ARIA when possible
- Minimize DOM depth for better screen reader performance
- Cache accessibility tree calculations in JS

### Version History

**v1.0.0** (2026-02-15)
- Initial skill creation based on Alex v5.8.0 accessibility implementation session
- WCAG 2.1 AA compliance patterns from welcomeView.ts refactoring
- Design system implementation workflow from production experience
- Accessibility audit checklist validated against real-world deployment
