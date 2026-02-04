---
name: dev-fix-keyboard
description: DEBUG keyboard shortcuts not working, conflicting hotkeys, and event handling issues. Fix when Ctrl+Z, Ctrl+S, or other shortcuts fail. Use for global keyboard handlers, event conflicts, and shortcut key debugging.
---

# Fix Keyboard Shortcuts

## Instructions

### Keyboard Shortcut Debugging Protocol
When keyboard shortcuts aren't working, systematically debug:

#### 1. Event Handler Issues
- **Check event listener attachment** and cleanup
- **Verify event propagation** and preventDefault usage
- **Debug keyboard event timing** and component lifecycle
- **Check for conflicting event handlers**

#### 2. Key Combination Problems
- **Verify modifier key detection** (Ctrl, Alt, Shift, Meta)
- **Check browser/OS differences** in key codes
- **Debug key combinations** and sequence detection
- **Check for input field conflicts** (shortcuts disabled during typing)

#### 3. Global Handler Conflicts
- **Identify multiple keyboard handlers** competing for same keys
- **Check handler order** and event bubbling
- **Debug Vue event handling** vs native event listeners
- **Verify iframe or shadow DOM** interference

## Common Keyboard Issues & Solutions

### Basic Event Handling Debug
```typescript
const debugKeyboardEvents = () => {
  const logKeyEvent = (event) => {
    console.log('⌨️ Key event:', {
      type: event.type,
      key: event.key,
      code: event.code,
      keyCode: event.keyCode,
      ctrlKey: event.ctrlKey,
      shiftKey: event.shiftKey,
      altKey: event.altKey,
      metaKey: event.metaKey,
      target: event.target.tagName,
      timestamp: Date.now()
    })

    // Check if input field has focus
    const activeElement = document.activeElement
    const isInput = activeElement?.tagName === 'INPUT' ||
                   activeElement?.tagName === 'TEXTAREA' ||
                   activeElement?.contentEditable === 'true'

    if (isInput) {
      console.log('📝 Input field has focus - shortcuts may be disabled')
    }
  }

  document.addEventListener('keydown', logKeyEvent, true)
  document.addEventListener('keyup', logKeyEvent, true)
}
```

### VueUse Keyboard Handler Debug
```typescript
import { useMagicKeys } from '@vueuse/core'

const debugMagicKeys = () => {
  const keys = useMagicKeys()

  // Debug individual keys
  watch(keys.ctrl_z, (pressed) => {
    if (pressed) {
      console.log('🔙 Ctrl+Z detected - triggering undo')
      // Trigger undo action
    }
  })

  watch(keys.ctrl_shift_z, (pressed) => {
    if (pressed) {
      console.log('🔜 Ctrl+Shift+Z detected - triggering redo')
      // Trigger redo action
    }
  })

  // Debug all key combinations
  watchEffect(() => {
    const activeKeys = Object.keys(keys).filter(key => keys[key])
    if (activeKeys.length > 0) {
      console.log('🎹 Active key combinations:', activeKeys)
    }
  })

  return keys
}
```

### Event Conflict Detection
```typescript
const debugEventConflicts = () => {
  const handlers = new Map()

  const addDebugHandler = (element, event, handler, priority = 0) => {
    const wrappedHandler = (e) => {
      console.group(`🔍 Keyboard handler: ${event}`)
      console.log('Element:', element.tagName, element.id, element.className)
      console.log('Priority:', priority)
      console.log('Event:', e)

      const result = handler(e)

      if (e.defaultPrevented) {
        console.log('⛔ Default prevented')
      }
      if (e.stopPropagation) {
        console.log('🛑 Propagation stopped')
      }

      console.groupEnd()
      return result
    }

    element.addEventListener(event, wrappedHandler, { capture: true })
    handlers.set(`${event}-${element.tagName}`, { element, handler: wrappedHandler, priority })
  }

  // Check for multiple handlers on same element
  const detectConflicts = () => {
    const keydownHandlers = Array.from(handlers.entries())
      .filter(([key]) => key.startsWith('keydown'))

    console.log('📊 Active keyboard handlers:', keydownHandlers.length)

    if (keydownHandlers.length > 1) {
      console.warn('⚠️ Multiple keyboard handlers detected - potential conflicts')
      keydownHandlers.forEach(([key, handler]) => {
        console.log(`  - ${key}: priority ${handler.priority}`)
      })
    }
  }

  return { addDebugHandler, detectConflicts }
}
```

### Input Field Conflict Resolution
```typescript
const debugInputConflicts = () => {
  const checkInputFocus = () => {
    const activeElement = document.activeElement
    const isInputElement = activeElement?.tagName === 'INPUT' ||
                         activeElement?.tagName === 'TEXTAREA' ||
                         activeElement?.contentEditable === 'true'

    console.log('🎯 Focus check:', {
      activeElement: activeElement?.tagName,
      id: activeElement?.id,
      isInput: isInputElement,
      shouldDisableShortcuts: isInputElement
    })

    return isInputElement
  }

  // Monitor focus changes
  document.addEventListener('focusin', (e) => {
    if (checkInputFocus()) {
      console.log('📝 Input field focused - keyboard shortcuts disabled')
    }
  })

  document.addEventListener('focusout', (e) => {
    setTimeout(() => {
      if (!checkInputFocus()) {
        console.log('🖱️ Input field blurred - keyboard shortcuts enabled')
      }
    }, 10)
  })

  return { checkInputFocus }
}
```

### Browser Compatibility Debug
```typescript
const debugBrowserCompatibility = () => {
  const testKeyEvent = (key, modifiers = {}) => {
    const event = new KeyboardEvent('keydown', {
      key,
      code: key,
      ctrlKey: modifiers.ctrl || false,
      shiftKey: modifiers.shift || false,
      altKey: modifiers.alt || false,
      metaKey: modifiers.meta || false
    })

    console.log('🌐 Testing key event:', { key, modifiers })
    document.dispatchEvent(event)
  }

  // Test common shortcuts
  const testCommonShortcuts = () => {
    console.group('🧪 Testing browser compatibility')

    testKeyEvent('z', { ctrl: true })
    testKeyEvent('y', { ctrl: true })
    testKeyEvent('s', { ctrl: true })
    testKeyEvent('z', { ctrl: true, shift: true })

    console.groupEnd()
  }

  // Check browser support
  const checkBrowserSupport = () => {
    console.log('🌍 Browser info:', {
      userAgent: navigator.userAgent,
      platform: navigator.platform,
      language: navigator.language
    })

    // Test KeyboardEvent support
    const supported = typeof KeyboardEvent !== 'undefined'
    console.log('⌨️ KeyboardEvent support:', supported)

    return supported
  }

  return { testKeyEvent, testCommonShortcuts, checkBrowserSupport }
}
```

### Global Handler Management
```typescript
const createGlobalKeyboardHandler = () => {
  const shortcuts = new Map()
  let isEnabled = true

  const registerShortcut = (keyCombo, action, description) => {
    shortcuts.set(keyCombo, { action, description })
    console.log(`⌨️ Registered shortcut: ${keyCombo} - ${description}`)
  }

  const handleKeyDown = (event) => {
    if (!isEnabled) return

    // Build key combination string
    const parts = []
    if (event.ctrlKey) parts.push('ctrl')
    if (event.shiftKey) parts.push('shift')
    if (event.altKey) parts.push('alt')
    if (event.metaKey) parts.push('meta')
    parts.push(event.key.toLowerCase())

    const keyCombo = parts.join('+')

    console.log(`🎹 Key pressed: ${keyCombo}`)

    // Check if we have a handler for this combination
    if (shortcuts.has(keyCombo)) {
      const { action, description } = shortcuts.get(keyCombo)
      console.log(`✅ Executing shortcut: ${description}`)

      event.preventDefault()
      event.stopPropagation()

      action(event)
    }
  }

  const enable = () => {
    isEnabled = true
    console.log('⌨️ Keyboard shortcuts enabled')
  }

  const disable = () => {
    isEnabled = false
    console.log('⌨️ Keyboard shortcuts disabled')
  }

  // Set up global listener
  document.addEventListener('keydown', handleKeyDown, true)

  return { registerShortcut, enable, disable }
}
```

This skill activates when you mention keyboard shortcuts not working, hotkey conflicts, event handling issues, or user interaction problems.

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
