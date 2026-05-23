---
name: providing-feedback
description: Implements feedback and notification systems including toasts, alerts, modals, progress indicators, and error states. Use when communicating system state, displaying messages, confirming actions, or showing errors.
---

# Providing User Feedback and Notifications

This skill implements comprehensive feedback and notification systems that enhance all other component skills by providing consistent patterns for communicating system state, displaying messages, and handling user confirmations.

## When to Use This Skill

Activate this skill when:
- Implementing toast notifications or snackbars
- Displaying success, error, warning, or info messages
- Creating modal dialogs or confirmation dialogs
- Implementing progress indicators (spinners, progress bars, skeleton screens)
- Designing empty states or zero-result displays
- Adding tooltips or contextual help
- Determining notification timing, stacking, or positioning
- Implementing accessible feedback patterns with ARIA
- Communicating any system state to users

## Feedback Type Decision Matrix

Choose the appropriate feedback mechanism based on urgency and attention requirements:

```
Critical + Blocking       → Modal Dialog
Important + Non-blocking  → Alert Banner
Success/Info + Temporary  → Toast/Snackbar
Contextual Help          → Tooltip/Popover
In-progress              → Progress Indicator
No Data                  → Empty State
```

### Quick Reference by Urgency

| Urgency Level | Component | Duration | Blocks Interaction |
|---------------|-----------|----------|-------------------|
| **Critical** | Modal Dialog | Until action | Yes |
| **Important** | Alert Banner | Until dismissed | No |
| **Standard** | Toast | 3-7 seconds | No |
| **Contextual** | Inline Message | Persistent | No |
| **Help** | Tooltip | On hover | No |
| **Progress** | Spinner/Bar | During operation | Optional |

## Implementation Approach

### Step 1: Determine Feedback Type

Assess the situation using these criteria:
1. **Urgency**: How critical is the information?
2. **Duration**: How long should it persist?
3. **Action Required**: Does user need to respond?
4. **Context**: Is it related to specific UI element?

### Step 2: Choose Implementation Pattern

**For Toasts/Snackbars:**
- Position: Bottom-right (recommended)
- Duration: 3-4s (success), 5-7s (warning), 7-10s (error)
- Stack limit: 3-5 maximum
- See `references/toast-patterns.md` for detailed patterns

**For Modal Dialogs:**
- Focus management: Trap focus within modal
- Accessibility: ESC to close, proper ARIA labels
- Backdrop: Click outside to close (optional)
- See `references/modal-patterns.md` for implementation

**For Progress Indicators:**
- <100ms: No indicator needed
- 100ms-5s: Spinner with message
- 5s-30s: Progress bar (determinate if possible)
- >30s: Progress bar + time estimate + cancel
- See `references/progress-indicators.md` for patterns

**For Empty States:**
- Include: Illustration, headline, body text, CTA
- Types: First use, zero results, error, permission denied
- See `references/empty-states.md` for designs

### Step 3: Implement with Recommended Libraries

**Modern React Stack (Recommended):**
```bash
npm install sonner @radix-ui/react-dialog
```

**For Toasts - Use Sonner:**
```tsx
import { Toaster, toast } from 'sonner';

// In your app root
<Toaster position="bottom-right" />

// Trigger notifications
toast.success('Changes saved successfully');
toast.promise(saveData(), {
  loading: 'Saving...',
  success: 'Saved!',
  error: 'Failed to save'
});
```

**For Modals - Use Radix UI:**
```tsx
import * as Dialog from '@radix-ui/react-dialog';

<Dialog.Root>
  <Dialog.Trigger>Open</Dialog.Trigger>
  <Dialog.Portal>
    <Dialog.Overlay />
    <Dialog.Content>
      <Dialog.Title>Confirm Action</Dialog.Title>
      <Dialog.Description>Are you sure?</Dialog.Description>
      <Dialog.Close>Cancel</Dialog.Close>
    </Dialog.Content>
  </Dialog.Portal>
</Dialog.Root>
```

See `references/library-comparison.md` for alternative libraries and selection criteria.

### Step 4: Apply Accessibility Patterns

**ARIA Live Regions for Announcements:**
```html
<!-- For non-critical notifications -->
<div role="status" aria-live="polite">
  File uploaded successfully
</div>

<!-- For critical alerts -->
<div role="alert" aria-live="assertive">
  Error: Failed to save
</div>
```

**Focus Management for Modals:**
1. Save current focus before opening
2. Move focus to first interactive element in modal
3. Trap focus within modal (Tab cycles)
4. Restore focus to trigger on close

See `references/accessibility-feedback.md` for complete patterns.

### Step 5: Integrate Design Tokens

All feedback components use the design-tokens skill for consistent theming:

```css
/* Example token usage */
.toast {
  background: var(--toast-bg);
  color: var(--toast-text);
  padding: var(--toast-padding);
  border-radius: var(--toast-border-radius);
  box-shadow: var(--toast-shadow);
  animation-duration: var(--toast-enter-duration);
}
```

Token categories used:
- **Colors**: Toast, alert, modal, tooltip backgrounds
- **Spacing**: Internal padding for all components
- **Typography**: Font sizes for titles and messages
- **Shadows**: Elevation for floating elements
- **Motion**: Animation durations and easing

## Notification Timing Guidelines

**Auto-dismiss durations:**
- Success: 3-4 seconds
- Info: 4-5 seconds
- Warning: 5-7 seconds
- Error: 7-10 seconds or manual dismiss
- With action button: 10+ seconds or no auto-dismiss

**Progress indicator thresholds:**
- <100ms: No indicator
- 100ms-5s: Spinner
- 5s-30s: Progress bar
- >30s: Progress bar + cancel option

## Resources

### Scripts (Token-Free Execution)
- `scripts/generate_toast_manager.js` - Generate toast configurations with timing and stacking
- `scripts/format_messages.py` - Format user-facing messages based on context
- `scripts/calculate_timing.js` - Calculate auto-dismiss timings

### References (Detailed Documentation)
- `references/toast-patterns.md` - Toast positioning, stacking, animations
- `references/alert-patterns.md` - Alert banner implementations
- `references/modal-patterns.md` - Modal dialogs with focus management
- `references/progress-indicators.md` - Loading states and progress
- `references/empty-states.md` - No-data and zero-result patterns
- `references/accessibility-feedback.md` - ARIA patterns and focus management
- `references/library-comparison.md` - Detailed library analysis

### Examples (Implementation Code)
- `examples/success-toast.tsx` - Success notification with Sonner
- `examples/confirmation-modal.tsx` - Delete confirmation with Radix UI
- `examples/progress-upload.tsx` - File upload with progress bar
- `examples/inline-validation.tsx` - Form validation errors

### Assets (Templates and Configs)
- `assets/message-templates.json` - Reusable message templates
- `assets/error-catalog.json` - Error code to message mappings
- `assets/timing-config.json` - Timing recommendations

## Cross-Skill Integration

This skill enhances all other component skills:

- **Forms**: Validation feedback, success confirmations
- **Data Visualization**: Loading states, error messages
- **Tables**: Bulk operation feedback, action confirmations
- **AI Chat**: Streaming indicators, rate limit warnings
- **Dashboards**: Widget loading, system status
- **Search/Filter**: Zero results, search progress
- **Media**: Upload progress, processing status
- **Design Tokens**: All visual styling via token system

## Library Quick Comparison

| Library | Type | Size | Best For |
|---------|------|------|----------|
| **Sonner** | Toast | Small | Modern React 18+, accessibility |
| **react-hot-toast** | Toast | <5KB | Minimal bundle size |
| **react-toastify** | Toast | ~16KB | RTL support, mobile |
| **Radix UI** | Modal | Small | Design systems, headless |
| **Headless UI** | Modal | Small | Tailwind projects |

Choose based on project requirements. See `references/library-comparison.md` for detailed analysis.

## Key Principles

1. **Match urgency to attention**: Don't use modals for non-critical info
2. **Be consistent**: Same feedback type for similar actions
3. **Provide context**: Explain what happened and what to do
4. **Enable recovery**: Include undo, retry, or help options
5. **Respect preferences**: Honor reduced motion settings
6. **Test accessibility**: Verify with screen readers and keyboard