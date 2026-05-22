---
name: dev-vue
description: COMPREHENSIVE Vue 3 development with Composition API, TypeScript, and advanced reactivity debugging. Create reactive components, handle props/events, implement lifecycle hooks, integrate with Pinia state management, debug reactivity issues, and optimize component performance. CRITICAL: All component changes MUST be tested with Playwright before claiming success. Use DevTools for debugging when available.
---

# Tier 1: Metadata

This skill provides Vue 3 component development with Composition API and TypeScript for the Pomo-Flow productivity application.

## Quick Context
- **Complexity**: medium
- **Duration**: 15-45 minutes
- **Dependencies**: vue, typescript, pinia, @vueuse/core

## Activation Triggers
- **Keywords**: vue, component, reactive, composable, template, script setup, props, events, lifecycle, computed, watch, ref, onmounted
- **Files**: *.vue, src/components/**, src/views/**, src/composables/**
- **Contexts**: frontend, ui-development, component-architecture, vue-js, typescript

## 🚨 CRITICAL TESTING REQUIREMENTS

### **MANDATORY Testing Protocol**
**ZERO TOLERANCE POLICY**: NEVER claim component functionality works without visual verification through testing.

#### **Before Claiming Success - MANDATORY Steps:**
1. **Start Development Server**: `npm run dev` (ensure port 5546 is available)
2. **Reactivate Playwright**: Use Playwright MCP for visual testing
3. **Reactivate DevTools**: Open browser DevTools for debugging
4. **Test Component Visually**: Verify component renders correctly
5. **Test Functionality**: Verify all interactions work as expected
6. **Test Edge Cases**: Verify error handling and boundary conditions
7. **Document Evidence**: Provide screenshots/test results as proof

#### **Testing Tool Reactivation Instructions:**
```bash
# If Playwright MCP is not available:
npm run test        # Run Playwright tests
npm run test:e2e    # Run end-to-end tests
npm run dev         # Start dev server for manual testing
```

#### **Required Testing Evidence:**
- ✅ Component renders without errors
- ✅ Props are handled correctly
- ✅ Events fire as expected
- ✅ State management works (if applicable)
- ✅ Responsive design works (if applicable)
- ✅ Accessibility features work (if applicable)

#### **Emergency Testing Recovery:**
If testing reveals issues:
1. **Stop**: Do NOT claim success
2. **Debug**: Use DevTools to identify the problem
3. **Fix**: Address the issue found during testing
4. **Retest**: Run the full testing protocol again
5. **Document**: Record the issue and resolution

## Reactivity Debugging (Integrated from dev-debug-reactivity)

### Reactivity Debugging Protocol
When Vue components don't update or state seems broken, follow this systematic approach:

#### 1. Check Reactive References
- **Always use `.value`** for `ref()` in setup()
- **Never destructure reactive objects** (breaks reactivity)
- **Use `storeToRefs()`** for Pinia store destructuring
- **Use `reactive()`** for objects, not `ref()`

#### 2. Computed Properties
- **Check dependencies** - computed should only track what it uses
- **Debug stale computed** - add console.log to see when it recalculates
- **Use `watchEffect()`** for automatic dependency tracking

#### 3. Watcher Configuration
- **Use `{ deep: true }`** for nested object changes
- **Use `{ immediate: true }`** to run watcher immediately
- **Check `flush: 'post'`** for timing issues

### Quick Debug Patterns

#### Reactivity Checker
```typescript
const debugReactivity = (ref, name) => {
  console.log(`${name} initial:`, ref.value)

  const stopWatcher = watch(ref, (newVal, oldVal) => {
    console.log(`${name} changed:`, oldVal, '→', newVal)
  }, { immediate: true })

  return stopWatcher
}
```

#### Component Update Tracker
```typescript
export default {
  setup() {
    onRenderTracked((e) => {
      console.log('Render tracked:', e.key, e.type)
    })

    onRenderTriggered((e) => {
      console.log('Render triggered:', e.key, e.type)
    })
  }
}
```

## Navigation Map
- [Implementation Guide](./IMPLEMENTATION.md)
- [Code Examples](./examples/)
- [Troubleshooting](./TROUBLESHOOTING.md)
- [Vue Development Patterns](./vue-development.md)
- [Testing Strategies](./testing.md)
- [Reactivity Debugging](./reactivity-debugging.md)

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
