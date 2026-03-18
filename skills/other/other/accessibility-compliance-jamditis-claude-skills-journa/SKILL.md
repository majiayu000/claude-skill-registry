---
name: accessibility-compliance
description: Web accessibility patterns for news sites, journalism tools, and academic platforms. Use when building accessible interfaces, auditing existing sites for WCAG compliance, writing alt text for news images, creating accessible data visualizations, or ensuring content reaches all readers including those using assistive technologies. Essential for newsroom developers and anyone publishing web content.
---

# Accessibility compliance

Practical accessibility patterns for journalism and academic web publishing.

## When to activate

- Building or auditing news websites
- Writing alt text for article images
- Creating accessible data visualizations
- Developing tools that journalists use
- Ensuring multimedia content is accessible
- Meeting legal accessibility requirements
- Publishing academic content online

## WCAG essentials for news sites

### The four principles (POUR)

```markdown
## WCAG 2.1 AA checklist (journalism focus)

### Perceivable
- [ ] Images have meaningful alt text
- [ ] Videos have captions
- [ ] Audio has transcripts
- [ ] Color isn't the only way to convey info
- [ ] Text can be resized to 200% without breaking

### Operable
- [ ] All functions work with keyboard only
- [ ] No keyboard traps
- [ ] Skip links to main content
- [ ] Page titles describe content
- [ ] Focus visible on all interactive elements

### Understandable
- [ ] Language is declared in HTML
- [ ] Navigation is consistent
- [ ] Error messages are clear
- [ ] Labels describe form fields

### Robust
- [ ] Valid HTML
- [ ] ARIA used correctly (or not at all)
- [ ] Works with screen readers
- [ ] Doesn't break with zoom/text resize
```

## Image accessibility

### Alt text for journalism

```markdown
## Alt text decision tree

### News photos
- **WHO** is in the image (if identifiable and relevant)
- **WHAT** is happening (the action or situation)
- **WHERE** (if location matters to story)
- **Don't**: Repeat caption text verbatim

### Examples

PHOTO: Protesters holding signs outside courthouse

BAD: "Protesters"
BAD: "Image of protest" (redundant "image of")
GOOD: "Approximately 50 protesters hold signs reading 'Justice Now' outside the federal courthouse in downtown Seattle"

PHOTO: Headshot of interview subject

BAD: "Photo"
GOOD: "Dr. Sarah Chen, epidemiologist at Johns Hopkins"

PHOTO: Chart embedded as image

BAD: "Chart showing data"
GOOD: "Bar chart showing unemployment rising from 3.5% to 8.2% between March and June 2020. Full data in table below."
```

### Alt text Python helper

```python
def generate_alt_text_prompt(context: dict) -> str:
    """Generate prompt for AI alt text assistance."""
    return f"""
    Write alt text for a news image.

    Story context: {context.get('headline', 'Unknown')}
    Image type: {context.get('image_type', 'photo')}
    Caption (if any): {context.get('caption', 'None')}

    Guidelines:
    - Be concise (under 125 characters if possible)
    - Don't start with "Image of" or "Photo of"
    - Include relevant details for story context
    - Don't duplicate caption exactly
    - Describe what's visually important

    If this is decorative only, respond: ""
    """

def is_decorative(image_context: str) -> bool:
    """Check if image is purely decorative (empty alt appropriate)."""
    decorative_indicators = [
        'decorative',
        'separator',
        'background',
        'spacer',
        'border'
    ]
    return any(ind in image_context.lower() for ind in decorative_indicators)
```

## Accessible data visualization

### Chart accessibility checklist

```markdown
## Making charts accessible

### Essential elements
- [ ] Text alternative describing the key insight
- [ ] Data table available (visible or linked)
- [ ] Colors have sufficient contrast
- [ ] Patterns/textures supplement color coding
- [ ] Labels directly on chart (not legend-only)
- [ ] Title describes what chart shows

### Interactive charts
- [ ] Keyboard navigable
- [ ] Focus indicators visible
- [ ] Screen reader announces data points
- [ ] Tooltips accessible via keyboard
- [ ] Zooming doesn't break layout
```

### Accessible chart component

```html
<!-- Accessible chart pattern -->
<figure role="figure" aria-labelledby="chart-title" aria-describedby="chart-desc">
  <figcaption>
    <h3 id="chart-title">Unemployment Rate 2020-2024</h3>
    <p id="chart-desc">
      Line chart showing unemployment starting at 3.5% in January 2020,
      spiking to 14.7% in April 2020, and gradually declining to 3.9% by 2024.
    </p>
  </figcaption>

  <!-- The chart itself -->
  <div id="chart" role="img" aria-label="Interactive line chart. Data table available below.">
    <!-- Chart renders here -->
  </div>

  <!-- Always provide data table -->
  <details>
    <summary>View data table</summary>
    <table>
      <caption>Monthly unemployment rate data</caption>
      <thead>
        <tr>
          <th scope="col">Month</th>
          <th scope="col">Unemployment Rate (%)</th>
        </tr>
      </thead>
      <tbody>
        <tr><td>Jan 2020</td><td>3.5</td></tr>
        <tr><td>Apr 2020</td><td>14.7</td></tr>
        <!-- etc -->
      </tbody>
    </table>
  </details>
</figure>
```

### Color-blind safe palettes

```python
# Safe color palettes for data visualization
COLOR_PALETTES = {
    # Paul Tol's color schemes - widely tested for accessibility
    'bright': [
        '#4477AA',  # Blue
        '#EE6677',  # Red
        '#228833',  # Green
        '#CCBB44',  # Yellow
        '#66CCEE',  # Cyan
        '#AA3377',  # Purple
        '#BBBBBB',  # Grey
    ],

    # Categorical (safe for most color blindness)
    'categorical': [
        '#332288',  # Indigo
        '#88CCEE',  # Cyan
        '#44AA99',  # Teal
        '#117733',  # Green
        '#999933',  # Olive
        '#DDCC77',  # Sand
        '#CC6677',  # Rose
        '#882255',  # Wine
    ],

    # Sequential (single hue)
    'sequential_blue': [
        '#f7fbff',
        '#deebf7',
        '#c6dbef',
        '#9ecae1',
        '#6baed6',
        '#4292c6',
        '#2171b5',
        '#084594',
    ],

    # Diverging (for data with meaningful midpoint)
    'diverging': [
        '#d73027',  # Red (negative)
        '#f46d43',
        '#fdae61',
        '#fee08b',
        '#ffffbf',  # Neutral
        '#d9ef8b',
        '#a6d96a',
        '#66bd63',
        '#1a9850',  # Green (positive)
    ]
}

def validate_contrast(color1: str, color2: str) -> float:
    """Calculate WCAG contrast ratio between two colors."""
    def hex_to_rgb(hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def relative_luminance(rgb):
        r, g, b = [x / 255.0 for x in rgb]
        r = r / 12.92 if r <= 0.03928 else ((r + 0.055) / 1.055) ** 2.4
        g = g / 12.92 if g <= 0.03928 else ((g + 0.055) / 1.055) ** 2.4
        b = b / 12.92 if b <= 0.03928 else ((b + 0.055) / 1.055) ** 2.4
        return 0.2126 * r + 0.7152 * g + 0.0722 * b

    l1 = relative_luminance(hex_to_rgb(color1))
    l2 = relative_luminance(hex_to_rgb(color2))

    lighter = max(l1, l2)
    darker = min(l1, l2)

    return (lighter + 0.05) / (darker + 0.05)

# WCAG requirements:
# Normal text: 4.5:1 minimum (AA), 7:1 enhanced (AAA)
# Large text (18pt+): 3:1 minimum (AA), 4.5:1 enhanced (AAA)
# UI components: 3:1 minimum
```

## Video and audio accessibility

### Caption requirements

```markdown
## Video caption checklist

### Quality standards
- [ ] 99%+ accuracy
- [ ] Synchronized with audio (within 1 second)
- [ ] Speaker identification for multiple speakers
- [ ] Sound effects described [applause] [music]
- [ ] Non-speech audio described when relevant

### Technical requirements
- [ ] Captions available in player controls
- [ ] Can be toggled on/off
- [ ] Styling doesn't overlap video content
- [ ] Readable font size and contrast

### Caption format (SRT example)
1
00:00:01,000 --> 00:00:04,500
[NEWS ANCHOR] Good evening. Breaking news tonight
from downtown where protesters have gathered.

2
00:00:04,600 --> 00:00:08,200
We're going live to reporter Jane Smith
at the scene. Jane?
```

### Audio description for video

```markdown
## When audio description is needed

### Required
- [ ] Key visual information not in dialogue
- [ ] Actions crucial to understanding story
- [ ] Text on screen not read aloud
- [ ] Identifying information for speakers

### Example script

ORIGINAL VIDEO: [Reporter stands in front of burning building]
DIALOGUE: "The fire started around 3am..."

AUDIO DESCRIPTION VERSION:
[A reporter in a red jacket stands before a five-story
apartment building engulfed in flames. Fire trucks
visible in background]
DIALOGUE: "The fire started around 3am..."
```

## Keyboard accessibility

### Focus management patterns

```javascript
// Skip link implementation
document.addEventListener('DOMContentLoaded', () => {
  const skipLink = document.querySelector('.skip-link');
  const mainContent = document.querySelector('main');

  skipLink.addEventListener('click', (e) => {
    e.preventDefault();
    mainContent.setAttribute('tabindex', '-1');
    mainContent.focus();
  });
});

// Keyboard trap prevention in modals
function createAccessibleModal(modalElement) {
  const focusableElements = modalElement.querySelectorAll(
    'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
  );
  const firstFocusable = focusableElements[0];
  const lastFocusable = focusableElements[focusableElements.length - 1];

  modalElement.addEventListener('keydown', (e) => {
    if (e.key === 'Tab') {
      if (e.shiftKey && document.activeElement === firstFocusable) {
        e.preventDefault();
        lastFocusable.focus();
      } else if (!e.shiftKey && document.activeElement === lastFocusable) {
        e.preventDefault();
        firstFocusable.focus();
      }
    }

    if (e.key === 'Escape') {
      closeModal();
    }
  });
}

// Focus indicator styles (never remove outlines without replacement)
/*
:focus {
  outline: 2px solid #005fcc;
  outline-offset: 2px;
}

:focus:not(:focus-visible) {
  outline: none;  // Remove for mouse users
}

:focus-visible {
  outline: 2px solid #005fcc;  // Keep for keyboard users
  outline-offset: 2px;
}
*/
```

## Forms and error handling

### Accessible form patterns

```html
<!-- Accessible form field -->
<div class="form-group">
  <label for="email">
    Email address
    <span class="required" aria-hidden="true">*</span>
    <span class="visually-hidden">(required)</span>
  </label>
  <input
    type="email"
    id="email"
    name="email"
    required
    aria-describedby="email-hint email-error"
    aria-invalid="false"
  >
  <p id="email-hint" class="hint">
    We'll use this to send you the newsletter.
  </p>
  <p id="email-error" class="error" role="alert" hidden>
    Please enter a valid email address.
  </p>
</div>

<style>
  /* Visually hidden but accessible to screen readers */
  .visually-hidden {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border: 0;
  }
</style>
```

### Error message patterns

```javascript
function showError(inputElement, message) {
  const errorElement = document.getElementById(
    inputElement.getAttribute('aria-describedby').split(' ').find(id =>
      id.includes('error')
    )
  );

  inputElement.setAttribute('aria-invalid', 'true');
  errorElement.textContent = message;
  errorElement.hidden = false;

  // Announce error to screen readers
  errorElement.setAttribute('role', 'alert');
}

function clearError(inputElement) {
  const errorId = inputElement.getAttribute('aria-describedby')
    .split(' ')
    .find(id => id.includes('error'));
  const errorElement = document.getElementById(errorId);

  inputElement.setAttribute('aria-invalid', 'false');
  errorElement.hidden = true;
  errorElement.removeAttribute('role');
}
```

## Testing tools

### Automated testing

```python
# Accessibility audit with axe-core (via Playwright)
from playwright.sync_api import sync_playwright

def run_accessibility_audit(url: str) -> dict:
    """Run automated accessibility tests."""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)

        # Inject axe-core
        page.add_script_tag(
            url='https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.7.2/axe.min.js'
        )

        # Run audit
        results = page.evaluate('''
            async () => {
                return await axe.run();
            }
        ''')

        browser.close()

        return {
            'violations': results['violations'],
            'passes': len(results['passes']),
            'incomplete': results['incomplete'],
            'url': url
        }

def format_violations(results: dict) -> str:
    """Format violations for review."""
    output = []
    for v in results['violations']:
        output.append(f"\n## {v['id']}: {v['description']}")
        output.append(f"Impact: {v['impact']}")
        output.append(f"WCAG: {', '.join(v.get('tags', []))}")
        for node in v['nodes'][:3]:  # First 3 examples
            output.append(f"  - {node['html'][:100]}")
    return '\n'.join(output)
```

### Manual testing checklist

```markdown
## Manual accessibility tests

### Keyboard navigation
- [ ] Tab through entire page
- [ ] Can reach all interactive elements
- [ ] Focus order makes sense
- [ ] No keyboard traps
- [ ] Skip link works

### Screen reader testing
- [ ] Headings announce in logical order
- [ ] Images have meaningful descriptions
- [ ] Form labels announce correctly
- [ ] Error messages announced
- [ ] Dynamic content updates announced

### Zoom testing
- [ ] 200% zoom, no horizontal scrolling
- [ ] 400% zoom, content still usable
- [ ] Text spacing adjustments don't break layout

### Color and contrast
- [ ] Works in grayscale
- [ ] Links distinguishable from text
- [ ] Error states not color-only
- [ ] Contrast checker passes (4.5:1 minimum)
```

## Legal requirements

```markdown
## Accessibility law summary

### United States
- **Section 508**: Federal agencies must be accessible
- **ADA**: Increasingly applied to websites
- **State laws**: Many states have additional requirements

### European Union
- **European Accessibility Act**: From 2025
- **EN 301 549**: Technical standard

### Best practice
WCAG 2.1 AA is the global standard. Meet this and you'll
likely satisfy most legal requirements.
```

## Related skills

- **zero-build-frontend** - Build accessible static sites
- **data-journalism** - Create accessible visualizations
- **web-scraping** - Ensure scraped content preserves accessibility

---

## Skill metadata

| Field | Value |
|-------|-------|
| Version | 1.0.0 |
| Created | 2025-12-26 |
| Author | Claude Skills for Journalism |
| Domain | Development, Publishing |
| Complexity | Intermediate |
