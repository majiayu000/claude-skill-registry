---
name: dev-vueuse
description: IMPLEMENT VueUse composables for browser APIs, event handling, and performance optimization. Add keyboard shortcuts, local storage, clipboard functionality, drag-and-drop, and responsive design. Use when you need browser integration or enhanced reactivity.
---

# VueUse Development

## Instructions

### VueUse Integration Pattern
Always use VueUse composables when working with browser APIs, complex event handling, or performance optimizations:

```typescript
import {
  useMagicKeys,
  useClipboard,
  useLocalStorage,
  useThrottleFn,
  useWindowSize,
  useEventListener
} from '@vueuse/core'

// Enhanced keyboard shortcuts
const { ctrl, shift, space } = useMagicKeys()

// Clipboard functionality
const { copy, copied, isSupported } = useClipboard()

// Persistent storage
const settings = useLocalStorage('app-settings', defaults)

// Performance optimization
const throttledUpdate = useThrottleFn(() => {
  updateCanvas()
}, 16)

// Responsive behavior
const { width, height } = useWindowSize()

// Event handling with cleanup
useEventListener('keydown', handleKeydown, { passive: true })
```

### Key Requirements
- Always check browser compatibility: `if (typeof window !== 'undefined')`
- Use proper TypeScript interfaces for all props and returns
- Handle permissions for browser APIs (notifications, clipboard)
- Implement fallbacks for unsupported features
- Use throttling/debouncing for performance-critical operations
- Clean up resources automatically with VueUse's built-in cleanup

### Common Patterns
- **Event Handling**: useEventListener for global events with automatic cleanup
- **Storage**: useLocalStorage/useSessionStorage for persistent state
- **Performance**: useThrottleFn/useDebounceFn for optimization
- **Browser APIs**: useClipboard, useNotification, useNetwork for web features
- **Responsive Design**: useWindowSize, useBreakpoints for adaptive layouts
- **Keyboard Shortcuts**: useMagicKeys for enhanced keyboard interactions

This skill ensures modern, efficient use of VueUse composables throughout the productivity application while maintaining performance and browser compatibility.

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
