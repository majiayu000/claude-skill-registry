---
name: Bug Fixer General
description: General debugging and bug fixing skill. Handles general logic errors, specific domain bugs (timer, keyboard, canvas), and crash investigations.
triggers:
  - fix bug
  - debug error
  - application crash
  - timber not working
  - keyboard shortcut broken
---

# Bug Fixer General

## 🎯 **Capabilities**
- **General Debugging**: Analyze stack traces and error messages.
- **Domain Specifics**:
    - **Timer**: `useTimer`, intervals, background handling.
    - **Keyboard**: global event listeners, `useMagicKeys`.
    - **Canvas**: Node positioning, drag/drop logic.
- **Crash Resolution**: App initialization failures, memory leaks.

## 🕵️ **Debugging Protocol**
1.  **Reproduce**: Can you make it fail reliably?
2.  **Isolate**: Narrow down to the specific component/composable.
3.  **Log**: Add console logs to trace data flow.
4.  **Fix**: Apply the minimal necessary change.
5.  **Verify**: Ensure the bug is gone AND no regression occurred.

## ⚠️ **Common Pitfalls**
- **Reactivity**: Mutating props directly (Vue warning).
- **Lifecycle**: Accessing DOM elements before mount.
- **Async**: Race conditions in `await`.
