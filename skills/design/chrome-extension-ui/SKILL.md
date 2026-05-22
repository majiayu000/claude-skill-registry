---
name: chrome-extension-ui
description: Chrome Extensions UX/UI design and implementation guidelines for popups, side panels, content scripts, and options pages. Triggers on tasks involving browser extension UI, manifest v3, chrome APIs.
---

# Chrome Extensions UX/UI Best Practices

Comprehensive UX/UI design guide for Chrome Extensions, optimized for Manifest V3. Contains 42 rules across 8 categories, prioritized by impact to guide extension UI development and code review.

## When to Apply

Reference these guidelines when:
- Building new Chrome extension user interfaces
- Choosing between popup, side panel, or content script UI
- Implementing accessible, keyboard-navigable interfaces
- Designing loading states, error handling, and feedback patterns
- Creating options pages and settings persistence

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Component Selection | CRITICAL | `comp-` |
| 2 | Accessibility & Navigation | CRITICAL | `access-` |
| 3 | Popup Design | HIGH | `popup-` |
| 4 | Side Panel UX | HIGH | `panel-` |
| 5 | Content Script UI | MEDIUM-HIGH | `inject-` |
| 6 | Visual Feedback | MEDIUM | `feedback-` |
| 7 | Options & Settings | MEDIUM | `options-` |
| 8 | Icons & Branding | LOW-MEDIUM | `brand-` |

## Quick Reference

### 1. Component Selection (CRITICAL)

- [`comp-popup-vs-sidepanel`](references/comp-popup-vs-sidepanel.md) - Choose Side Panel for Persistent Tasks
- [`comp-content-script-ui`](references/comp-content-script-ui.md) - Use Content Scripts for In-Page UI
- [`comp-single-purpose`](references/comp-single-purpose.md) - Design for Single Purpose
- [`comp-minimal-permissions`](references/comp-minimal-permissions.md) - Request Minimal Permissions
- [`comp-action-tooltip`](references/comp-action-tooltip.md) - Provide Descriptive Action Tooltips

### 2. Accessibility & Navigation (CRITICAL)

- [`access-keyboard-navigation`](references/access-keyboard-navigation.md) - Enable Complete Keyboard Navigation
- [`access-focus-visible`](references/access-focus-visible.md) - Maintain Visible Focus Indicators
- [`access-aria-labels`](references/access-aria-labels.md) - Use ARIA Labels for Icon-Only Buttons
- [`access-color-contrast`](references/access-color-contrast.md) - Ensure Sufficient Color Contrast
- [`access-focus-trap`](references/access-focus-trap.md) - Avoid Keyboard Focus Traps
- [`access-semantic-html`](references/access-semantic-html.md) - Use Semantic HTML Elements

### 3. Popup Design (HIGH)

- [`popup-size-constraints`](references/popup-size-constraints.md) - Design Within Popup Size Limits
- [`popup-instant-render`](references/popup-instant-render.md) - Render Popup Content Instantly
- [`popup-primary-action`](references/popup-primary-action.md) - Make the Primary Action Obvious
- [`popup-auto-close`](references/popup-auto-close.md) - Handle Popup Auto-Close Gracefully
- [`popup-external-js`](references/popup-external-js.md) - Keep JavaScript in External Files
- [`popup-dynamic-switch`](references/popup-dynamic-switch.md) - Use Dynamic Popups for State-Based UI

### 4. Side Panel UX (HIGH)

- [`panel-non-distracting`](references/panel-non-distracting.md) - Design Non-Distracting Side Panels
- [`panel-tab-vs-window`](references/panel-tab-vs-window.md) - Choose Tab-Specific vs Window-Wide Panels
- [`panel-responsive-width`](references/panel-responsive-width.md) - Design for Variable Panel Widths
- [`panel-page-context`](references/panel-page-context.md) - Sync Panel Content with Page Context
- [`panel-lazy-sections`](references/panel-lazy-sections.md) - Lazy Load Panel Sections

### 5. Content Script UI (MEDIUM-HIGH)

- [`inject-shadow-dom`](references/inject-shadow-dom.md) - Use Shadow DOM for Style Isolation
- [`inject-z-index`](references/inject-z-index.md) - Use Maximum Z-Index for Overlays
- [`inject-document-ready`](references/inject-document-ready.md) - Inject UI After DOM Ready
- [`inject-unique-ids`](references/inject-unique-ids.md) - Use Unique IDs to Prevent Conflicts
- [`inject-cleanup`](references/inject-cleanup.md) - Clean Up Injected Elements on Removal

### 6. Visual Feedback (MEDIUM)

- [`feedback-loading-states`](references/feedback-loading-states.md) - Show Loading States for Async Operations
- [`feedback-error-messages`](references/feedback-error-messages.md) - Write Actionable Error Messages
- [`feedback-badge-status`](references/feedback-badge-status.md) - Use Badge for At-a-Glance Status
- [`feedback-success-confirmation`](references/feedback-success-confirmation.md) - Confirm Successful Actions
- [`feedback-notifications`](references/feedback-notifications.md) - Use Notifications Sparingly
- [`feedback-progress-indication`](references/feedback-progress-indication.md) - Show Progress for Long Operations

### 7. Options & Settings (MEDIUM)

- [`options-embedded-page`](references/options-embedded-page.md) - Use Embedded Options for Simple Settings
- [`options-sync-storage`](references/options-sync-storage.md) - Sync Settings Across Devices
- [`options-auto-save`](references/options-auto-save.md) - Auto-Save Settings on Change
- [`options-sensible-defaults`](references/options-sensible-defaults.md) - Provide Sensible Default Settings

### 8. Icons & Branding (LOW-MEDIUM)

- [`brand-icon-sizes`](references/brand-icon-sizes.md) - Provide All Required Icon Sizes
- [`brand-distinctive-icon`](references/brand-distinctive-icon.md) - Design a Distinctive Toolbar Icon
- [`brand-badge-text`](references/brand-badge-text.md) - Keep Badge Text Under 4 Characters
- [`brand-consistent-styling`](references/brand-consistent-styling.md) - Maintain Consistent Visual Style
- [`brand-web-store-assets`](references/brand-web-store-assets.md) - Create Quality Web Store Assets

## How to Use

Read individual reference files for detailed explanations and code examples:

- [Section definitions](references/_sections.md) - Category structure and impact levels
- [Rule template](assets/templates/_template.md) - Template for adding new rules

## Reference Files

| File | Description |
|------|-------------|
| [references/_sections.md](references/_sections.md) | Category definitions and ordering |
| [assets/templates/_template.md](assets/templates/_template.md) | Template for new rules |
| [metadata.json](metadata.json) | Version and reference information |
