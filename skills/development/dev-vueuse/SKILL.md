---
name: Implement VueUse Features
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