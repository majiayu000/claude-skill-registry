---
name: accessibility-planning
description: Plan accessibility compliance - WCAG 2.2, Section 508, EN 301 549, inclusive design principles, audit planning, and remediation strategies.
allowed-tools: Read, Glob, Grep, Task
---

# Accessibility Planning

Plan for inclusive design and WCAG compliance before development begins.

## When to Use This Skill

Use this skill when:

- **Accessibility Planning tasks** - Working on plan accessibility compliance - wcag 2.2, section 508, en 301 549, inclusive design principles, audit planning, and remediation strategies
- **Planning or design** - Need guidance on Accessibility Planning approaches
- **Best practices** - Want to follow established patterns and standards

## MANDATORY: Skill Loading First

Before answering ANY accessibility question:

2. Use official WCAG and accessibility standards
3. Base all guidance on validated accessibility practices

## Accessibility Standards

### WCAG 2.2 Overview

| Level | Description | Typical Requirement |
|-------|-------------|---------------------|
| **A** | Minimum | Basic accessibility barriers removed |
| **AA** | Standard | Most common barriers addressed |
| **AAA** | Enhanced | Highest level of accessibility |

**Target:** Most organizations target **WCAG 2.2 Level AA**.

### Compliance Frameworks

| Standard | Region | Applies To |
|----------|--------|------------|
| **WCAG 2.2** | Global | Web content |
| **Section 508** | USA | Federal agencies, contractors |
| **EN 301 549** | Europe | Public sector, ICT products |
| **ADA** | USA | Public accommodations |
| **AODA** | Ontario, Canada | Businesses, organizations |

## WCAG 2.2 Principles (POUR)

### 1. Perceivable

Users must be able to perceive content.

| Guideline | Key Requirements |
|-----------|-----------------|
| **1.1 Text Alternatives** | Alt text for images, captions for audio |
| **1.2 Time-based Media** | Captions, audio descriptions, transcripts |
| **1.3 Adaptable** | Structure via semantic HTML, meaningful sequence |
| **1.4 Distinguishable** | Color contrast, resize text, audio control |

### 2. Operable

Users must be able to operate the interface.

| Guideline | Key Requirements |
|-----------|-----------------|
| **2.1 Keyboard Accessible** | All functionality via keyboard |
| **2.2 Enough Time** | Adjustable timing, pause/stop content |
| **2.3 Seizures** | No flashing content >3 times/second |
| **2.4 Navigable** | Skip links, page titles, focus order |
| **2.5 Input Modalities** | Pointer gestures, target size, motion |

### 3. Understandable

Content and operation must be understandable.

| Guideline | Key Requirements |
|-----------|-----------------|
| **3.1 Readable** | Language identification, abbreviations |
| **3.2 Predictable** | Consistent navigation, no unexpected changes |
| **3.3 Input Assistance** | Error identification, labels, suggestions |

### 4. Robust

Content must work with assistive technologies.

| Guideline | Key Requirements |
|-----------|-----------------|
| **4.1 Compatible** | Valid markup, name/role/value for components |

## WCAG 2.2 New Success Criteria

| Criterion | Level | Description |
|-----------|-------|-------------|
| **2.4.11 Focus Not Obscured (Min)** | AA | Focused element not entirely hidden |
| **2.4.12 Focus Not Obscured (Enhanced)** | AAA | Focused element not partially hidden |
| **2.4.13 Focus Appearance** | AAA | Visible focus indicator requirements |
| **2.5.7 Dragging Movements** | AA | Single-pointer alternative to dragging |
| **2.5.8 Target Size (Minimum)** | AA | 24x24 CSS pixels minimum |
| **3.2.6 Consistent Help** | A | Help mechanisms in consistent location |
| **3.3.7 Redundant Entry** | A | Don't require re-entering same info |
| **3.3.8 Accessible Authentication (Min)** | AA | No cognitive function tests for auth |
| **3.3.9 Accessible Authentication (Enhanced)** | AAA | Extended auth requirements |

## Accessibility Audit Planning

### Audit Types

| Type | Scope | When |
|------|-------|------|
| **Quick Audit** | High-traffic pages, key flows | Sprint review |
| **Comprehensive Audit** | Full WCAG checklist | Before launch |
| **Continuous Monitoring** | Automated scans | Ongoing |
| **User Testing** | With assistive technology users | Periodically |

### Audit Checklist Template

```markdown
# Accessibility Audit Plan

## Scope
- **Product/Site:** [Name]
- **Pages/Components:** [List or "All"]
- **Standard:** WCAG 2.2 Level AA
- **Timeline:** [Dates]

## Testing Matrix

### Automated Testing
- [ ] axe DevTools scan
- [ ] WAVE evaluation
- [ ] Lighthouse accessibility audit
- [ ] Pa11y CI integration

### Manual Testing
- [ ] Keyboard-only navigation
- [ ] Screen reader testing (NVDA, VoiceOver, JAWS)
- [ ] High contrast mode
- [ ] Browser zoom (200%)
- [ ] Color blindness simulation

### Assistive Technology Matrix

| AT | Browser | OS | Tester |
|----|---------|----|----|
| NVDA | Chrome | Windows | [Name] |
| JAWS | Chrome | Windows | [Name] |
| VoiceOver | Safari | macOS | [Name] |
| VoiceOver | Safari | iOS | [Name] |
| TalkBack | Chrome | Android | [Name] |

## Pages/Components to Test

| Priority | Page/Component | URL/Location | Status |
|----------|----------------|--------------|--------|
| High | Homepage | / | Pending |
| High | Login | /login | Pending |
| High | Checkout | /checkout | Pending |
| Medium | Product listing | /products | Pending |
| Medium | Forms | /contact | Pending |

## Issue Tracking
- **Tool:** [Jira/GitHub Issues/etc.]
- **Label:** accessibility
- **Severity Levels:** Critical, Major, Minor, Enhancement

## Deliverables
- [ ] Issue log with WCAG mapping
- [ ] Prioritized remediation plan
- [ ] VPAT/ACR (if required)
- [ ] Executive summary
```

## Common Accessibility Issues

### Critical (Level A failures)

| Issue | WCAG | Fix |
|-------|------|-----|
| **Missing alt text** | 1.1.1 | Add descriptive alt attributes |
| **No keyboard access** | 2.1.1 | Ensure all interactive elements focusable |
| **Missing form labels** | 1.3.1 | Associate labels with inputs |
| **Empty buttons/links** | 4.1.2 | Add accessible names |
| **Auto-playing media** | 1.4.2 | Provide pause/stop controls |

### Major (Level AA failures)

| Issue | WCAG | Fix |
|-------|------|-----|
| **Low color contrast** | 1.4.3 | 4.5:1 for text, 3:1 for large text |
| **No skip navigation** | 2.4.1 | Add skip link to main content |
| **Missing page titles** | 2.4.2 | Unique, descriptive titles |
| **Focus not visible** | 2.4.7 | Visible focus indicator |
| **Reflow issues** | 1.4.10 | Responsive at 400% zoom |

### .NET/Blazor Accessibility Patterns

```csharp
// Accessible button component
@code {
    [Parameter] public string AriaLabel { get; set; } = "";
    [Parameter] public bool IsDisabled { get; set; }
    [Parameter] public RenderFragment? ChildContent { get; set; }
    [Parameter] public EventCallback OnClick { get; set; }
}

<button
    type="button"
    aria-label="@AriaLabel"
    aria-disabled="@IsDisabled.ToString().ToLower()"
    disabled="@IsDisabled"
    @onclick="HandleClick"
    class="btn">
    @ChildContent
</button>

@code {
    private async Task HandleClick()
    {
        if (!IsDisabled)
        {
            await OnClick.InvokeAsync();
        }
    }
}
```

```csharp
// Accessible form field
<div class="form-group">
    <label for="@Id" class="@(IsRequired ? "required" : "")">
        @Label
        @if (IsRequired)
        {
            <span aria-hidden="true">*</span>
            <span class="visually-hidden">(required)</span>
        }
    </label>

    <input
        id="@Id"
        name="@Name"
        type="@Type"
        @bind="Value"
        aria-required="@IsRequired.ToString().ToLower()"
        aria-invalid="@(!string.IsNullOrEmpty(ErrorMessage)).ToString().ToLower()"
        aria-describedby="@(HasError ? $"{Id}-error" : HintId)"
        class="@(HasError ? "input-error" : "")" />

    @if (!string.IsNullOrEmpty(Hint))
    {
        <span id="@HintId" class="hint">@Hint</span>
    }

    @if (HasError)
    {
        <span id="@($"{Id}-error")" class="error" role="alert">
            @ErrorMessage
        </span>
    }
</div>
```

```csharp
// Skip link component
<a href="#main-content" class="skip-link">
    Skip to main content
</a>

<style>
    .skip-link {
        position: absolute;
        top: -40px;
        left: 0;
        background: #000;
        color: #fff;
        padding: 8px;
        z-index: 100;
    }

    .skip-link:focus {
        top: 0;
    }
</style>
```

## Color Contrast Requirements

### Contrast Ratios

| Element Type | WCAG AA | WCAG AAA |
|--------------|---------|----------|
| Normal text (<18pt) | 4.5:1 | 7:1 |
| Large text (≥18pt or ≥14pt bold) | 3:1 | 4.5:1 |
| UI components & graphics | 3:1 | 3:1 |

### Contrast Checker

```csharp
public class ContrastChecker
{
    public record ContrastResult(
        double Ratio,
        bool PassesAA,
        bool PassesAAA,
        bool PassesLargeTextAA,
        bool PassesLargeTextAAA
    );

    public ContrastResult Calculate(string foreground, string background)
    {
        var fgLuminance = GetRelativeLuminance(foreground);
        var bgLuminance = GetRelativeLuminance(background);

        var lighter = Math.Max(fgLuminance, bgLuminance);
        var darker = Math.Min(fgLuminance, bgLuminance);

        var ratio = (lighter + 0.05) / (darker + 0.05);
        ratio = Math.Round(ratio, 2);

        return new ContrastResult(
            Ratio: ratio,
            PassesAA: ratio >= 4.5,
            PassesAAA: ratio >= 7,
            PassesLargeTextAA: ratio >= 3,
            PassesLargeTextAAA: ratio >= 4.5
        );
    }

    private static double GetRelativeLuminance(string hex)
    {
        var rgb = ParseHex(hex);
        var r = GetLuminanceComponent(rgb.R);
        var g = GetLuminanceComponent(rgb.G);
        var b = GetLuminanceComponent(rgb.B);

        return 0.2126 * r + 0.7152 * g + 0.0722 * b;
    }

    private static double GetLuminanceComponent(byte value)
    {
        var sRGB = value / 255.0;
        return sRGB <= 0.03928
            ? sRGB / 12.92
            : Math.Pow((sRGB + 0.055) / 1.055, 2.4);
    }

    private static (byte R, byte G, byte B) ParseHex(string hex)
    {
        hex = hex.TrimStart('#');
        return (
            Convert.ToByte(hex[..2], 16),
            Convert.ToByte(hex[2..4], 16),
            Convert.ToByte(hex[4..6], 16)
        );
    }
}
```

## Keyboard Navigation Requirements

### Focus Order

```csharp
// Tab order management
public class FocusManager
{
    private readonly IJSRuntime _js;

    public async Task SetFocusTo(string elementId)
    {
        await _js.InvokeVoidAsync("focusElement", elementId);
    }

    public async Task TrapFocusInModal(string modalId)
    {
        await _js.InvokeVoidAsync("trapFocus", modalId);
    }

    public async Task RestoreFocus(string previousElementId)
    {
        await _js.InvokeVoidAsync("focusElement", previousElementId);
    }
}
```

```javascript
// Focus trap for modals
window.trapFocus = function(modalId) {
    const modal = document.getElementById(modalId);
    const focusableElements = modal.querySelectorAll(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );

    const firstElement = focusableElements[0];
    const lastElement = focusableElements[focusableElements.length - 1];

    modal.addEventListener('keydown', function(e) {
        if (e.key === 'Tab') {
            if (e.shiftKey && document.activeElement === firstElement) {
                lastElement.focus();
                e.preventDefault();
            } else if (!e.shiftKey && document.activeElement === lastElement) {
                firstElement.focus();
                e.preventDefault();
            }
        }
    });

    firstElement.focus();
};
```

### Required Keyboard Interactions

| Component | Keys | Action |
|-----------|------|--------|
| Button | Enter, Space | Activate |
| Link | Enter | Navigate |
| Checkbox | Space | Toggle |
| Radio | Arrow keys | Navigate options |
| Select | Arrow keys, Enter | Navigate, select |
| Tab panel | Arrow keys | Switch tabs |
| Menu | Arrow keys, Enter, Esc | Navigate, select, close |
| Modal | Esc | Close |

## VPAT (Voluntary Product Accessibility Template)

### VPAT Structure

```markdown
# [Product Name] Accessibility Conformance Report
## WCAG 2.2 Edition

**Report Date:** [Date]
**Product Version:** [Version]
**Contact:** [Email]

### Table 1: Success Criteria, Level A

| Criteria | Conformance Level | Remarks |
|----------|-------------------|---------|
| 1.1.1 Non-text Content | Supports | All images have alt text |
| 1.2.1 Audio-only and Video-only | Not Applicable | No pre-recorded media |
| 1.3.1 Info and Relationships | Partially Supports | [Explanation] |
| ... | ... | ... |

### Table 2: Success Criteria, Level AA
[Continue pattern]

### Conformance Levels
- **Supports:** Fully meets criterion
- **Partially Supports:** Some aspects don't meet criterion
- **Does Not Support:** Majority doesn't meet criterion
- **Not Applicable:** Criterion doesn't apply
```

## Remediation Planning

### Priority Matrix

| Priority | Criteria | Timeline |
|----------|----------|----------|
| **P0 - Critical** | Level A failures, blocks functionality | Immediate |
| **P1 - High** | Level AA failures, significant barriers | Sprint 1 |
| **P2 - Medium** | Level AA improvements, minor barriers | Sprint 2-3 |
| **P3 - Low** | Best practices, enhancements | Backlog |

### Remediation Tracking

```csharp
public class AccessibilityIssue
{
    public Guid Id { get; init; }
    public required string Title { get; init; }
    public required string Description { get; init; }
    public required WcagCriterion Criterion { get; init; }
    public required WcagLevel Level { get; init; }
    public required IssueStatus Status { get; init; }
    public required Priority Priority { get; init; }
    public required string AffectedComponent { get; init; }
    public string? Remediation { get; init; }
    public string? AssignedTo { get; init; }
    public DateOnly? TargetDate { get; init; }
}

public record WcagCriterion(string Number, string Name);

public enum WcagLevel { A, AA, AAA }

public enum Priority { Critical, High, Medium, Low }

public enum IssueStatus
{
    Open,
    InProgress,
    InReview,
    Closed,
    WontFix
}
```

## Inclusive Design Principles

### Microsoft Inclusive Design

1. **Recognize exclusion** - Understand how exclusion happens
2. **Solve for one, extend to many** - Design for edge cases first
3. **Learn from diversity** - Include diverse perspectives

### Permanent, Temporary, Situational

| Sense | Permanent | Temporary | Situational |
|-------|-----------|-----------|-------------|
| Touch | One arm | Arm injury | Holding a baby |
| See | Blind | Cataract | Bright sunlight |
| Hear | Deaf | Ear infection | Noisy environment |
| Speak | Nonverbal | Laryngitis | Heavy accent |

## Checklist: Accessibility Planning

### Strategy

- [ ] Target compliance level defined (AA recommended)
- [ ] Legal requirements identified
- [ ] Timeline established
- [ ] Resources allocated

### Design Phase

- [ ] Color contrast verified
- [ ] Touch targets sized (44x44px minimum)
- [ ] Focus states designed
- [ ] Error states accessible
- [ ] Motion preferences considered

### Development Phase

- [ ] Semantic HTML used
- [ ] ARIA used correctly (sparingly)
- [ ] Keyboard navigation works
- [ ] Focus management implemented
- [ ] Skip links added

### Testing Phase

- [ ] Automated testing integrated
- [ ] Manual testing completed
- [ ] Screen reader testing done
- [ ] Keyboard-only testing done
- [ ] Zoom/reflow tested

### Documentation

- [ ] Accessibility statement published
- [ ] VPAT completed (if required)
- [ ] Known issues documented
- [ ] Contact for feedback provided

## Related Skills

- `usability-testing` - Inclusive usability testing
- `design-system-planning` - Accessible components
- `heuristic-evaluation` - Accessibility heuristics
- `service-blueprinting` - Accessible service touchpoints
