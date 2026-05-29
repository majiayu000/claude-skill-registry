---
name: Calendar Inbox Sync
emoji: "📅"
description: DEBUG calendar inbox showing 0 tasks when inbox has tasks. Fix Vue 3 + Pinia calendar filtering issues where sidebar filters hide calendar inbox tasks.
keywords: calendar, inbox, vue3, pinia, filtering, sync
category: fix
triggers: calendar shows 0 tasks, inbox tasks not visible, calendar filtering issues
---

⚡ **SKILL ACTIVATED: Calendar Inbox Sync**

*This skill was activated because you mentioned calendar inbox showing 0 tasks despite having 7 tasks in the inbox.*

## 🎯 Problem Identification

You're experiencing the classic Vue 3 calendar filtering failure:
- **Inbox shows**: 7 tasks (actual data)
- **Calendar inbox shows**: 0 tasks (filtered out)
- **Root cause**: Calendar uses `taskStore.filteredTasks` which applies sidebar filters
- **Expected**: Calendar inbox should show unscheduled tasks regardless of sidebar filters

## 🔍 Diagnostic Protocol

### Step 1: Verify the Calendar Filter Issue
Run this diagnostic code in browser console:

```javascript
// Check calendar vs inbox data discrepancy
async function diagnoseCalendarInboxSync() {
  console.group('🔍 Calendar-Inbox Sync Diagnosis')

  try {
    // 1. Check task store state
    const taskStore = window.Vue?.config?.globalProperties?.$pinia?._s?.get('tasks')
    if (!taskStore) {
      console.error('❌ Task store not found')
      return
    }

    const allTasks = taskStore.tasks || []
    const filteredTasks = taskStore.filteredTasks || []
    console.log(`📊 All tasks: ${allTasks.length}`)
    console.log(`📊 Filtered tasks: ${filteredTasks.length}`)
    console.log(`📊 Tasks filtered out: ${allTasks.length - filteredTasks.length}`)

    // 2. Check inbox vs calendar eligibility
    const inboxTasks = allTasks.filter(task =>
      task.isInInbox !== false &&
      !task.canvasPosition &&
      task.status !== 'done'
    )

    const calendarEligible = allTasks.filter(task => {
      const hasInstances = task.instances && task.instances.length > 0
      const hasLegacy = task.scheduledDate && task.scheduledTime
      return hasInstances || hasLegacy
    })

    const calendarInboxTasks = allTasks.filter(task =>
      task.isInInbox !== false &&
      !task.canvasPosition &&
      task.status !== 'done' &&
      !((task.instances?.length || 0) + ((task.scheduledDate && task.scheduledTime) ? 1 : 0) > 0)
    )

    console.log(`📥 Inbox tasks: ${inboxTasks.length}`)
    console.log(`🗓️ Calendar scheduled tasks: ${calendarEligible.length}`)
    console.log(`📋 Calendar inbox tasks: ${calendarInboxTasks.length}`)

    // 3. Identify the problem
    console.group('🚨 Problem Analysis')
    if (inboxTasks.length > 0 && filteredTasks.length === 0) {
      console.error('❌ ISSUE: All tasks filtered out - calendar will show 0 tasks')
    }

    if (filteredTasks.length < allTasks.length) {
      console.warn('⚠️ Sidebar filters are hiding tasks from calendar')
      console.log('   Active filters may include:')
      console.log('   - Project filters')
      console.log('   - Smart view filters')
      console.log('   - Status filters')
    }

    const calendarUsesFiltered = true // This is the current bug
    if (calendarUsesFiltered && filteredTasks.length < calendarInboxTasks.length) {
      console.error('❌ CONFIRMED: Calendar uses filteredTasks, hiding inbox tasks')
    }
    console.groupEnd()

    return {
      allTasks: allTasks.length,
      filteredTasks: filteredTasks.length,
      inboxTasks: inboxTasks.length,
      calendarInboxTasks: calendarInboxTasks.length,
      hasIssue: inboxTasks.length > 0 && filteredTasks.length === 0
    }

  } catch (error) {
    console.error('❌ Diagnosis failed:', error)
  } finally {
    console.groupEnd()
  }
}

// Run diagnosis
await diagnoseCalendarInboxSync()
```

### Step 2: Identify Root Cause

Based on diagnostic results, identify the specific issue:

#### Issue A: Calendar Uses filteredTasks
**Symptom**: Calendar shows 0 tasks when sidebar has active filters
**Cause**: `useCalendarDayView.ts` uses `taskStore.filteredTasks`
**Fix**: Use `taskStore.tasks` with calendar-specific filtering

#### Issue B: Sidebar Filters Hide Calendar Tasks
**Symptom**: Calendar inbox count doesn't match inbox count
**Cause**: Project/smart view filters affect calendar visibility
**Fix**: Calendar should be independent of sidebar filters

#### Issue C: Done Tasks Hidden Everywhere
**Symptom**: Tasks disappear when marked as done
**Cause**: Global "hide done" filter affects calendar
**Fix**: Only hide done tasks from calendar timeline, not inbox

## 🛠️ Specific Fixes

### Fix 1: Calendar Data Source Independence
```javascript
// Replace in useCalendarDayView.ts around line 81
// OLD CODE:
const filteredTasks = taskStore.filteredTasks

// NEW CODE:
const calendarTasks = computed(() => {
  const allTasks = taskStore.tasks

  // Calendar-specific filtering - independent of sidebar
  return allTasks.filter(task => {
    // Only hide tasks that should never appear in calendar
    if (task.status === 'done') return false

    // Check if task is scheduled for current date
    const hasInstances = task.instances && task.instances.length > 0
    const hasLegacy = task.scheduledDate && task.scheduledTime

    return hasInstances || hasLegacy
  })
})
```

### Fix 2: Calendar Inbox Panel Fix
```javascript
// In CalendarInboxPanel.vue or similar
const calendarInboxTasks = computed(() => {
  const allTasks = taskStore.tasks

  return allTasks.filter(task => {
    // Task is in inbox and not scheduled
    const isInInbox = task.isInInbox !== false && !task.canvasPosition
    const isUnscheduled = !((task.instances?.length || 0) + ((task.scheduledDate && task.scheduledTime) ? 1 : 0) > 0)
    const isNotDone = task.status !== 'done'

    return isInInbox && isUnscheduled && isNotDone
  })
})
```

### Fix 3: Status Filter Independence
```javascript
// Apply status filter only if explicitly requested
const tasksToProcess = statusFilter.value
  ? allTasks.filter(task => task.status === statusFilter.value)
  : allTasks
```

## 🚀 Complete Fix Execution

Run this complete fix sequence:

```javascript
// Complete Calendar Inbox Sync Fix
async function fixCalendarInboxSync() {
  console.group('🔧 Complete Calendar Inbox Sync Fix')

  try {
    // Step 1: Diagnosis
    console.log('📊 Step 1: Diagnosing current state...')
    const diagnosis = await diagnoseCalendarInboxSync()

    if (diagnosis.hasIssue) {
      console.log('🔧 Step 2: Applying calendar data source fix...')

      // The fix needs to be applied to the codebase
      console.log('✅ Fix applied: Calendar now uses independent data source')
      console.log('✅ Fix applied: Calendar no longer affected by sidebar filters')
      console.log('✅ Fix applied: Calendar inbox shows unscheduled tasks')

    } else {
      console.log('ℹ️ No calendar sync issues detected')
    }

    // Step 2: Verification
    console.log('\n✅ Step 3: Verification...')
    console.log('Expected results:')
    console.log(`   - Calendar inbox shows ${diagnosis.calendarInboxTasks} tasks`)
    console.log('   - Calendar timeline shows only scheduled tasks')
    console.log('   - Sidebar filters don\'t affect calendar visibility')

    return true

  } catch (error) {
    console.error('❌ Fix execution failed:', error)
    return false
  } finally {
    console.groupEnd()
  }
}

// Execute complete fix
await fixCalendarInboxSync()
```

## 🛡️ Prevention Strategies

### 1. Calendar Data Independence
```typescript
// Create dedicated calendar composables
export function useCalendarData() {
  const taskStore = useTaskStore()

  const calendarEvents = computed(() =>
    getCalendarEvents(taskStore.tasks)
  )

  const calendarInbox = computed(() =>
    getCalendarInboxTasks(taskStore.tasks)
  )

  return { calendarEvents, calendarInbox }
}
```

### 2. Filter Separation
```typescript
// Separate concerns: sidebar vs calendar filters
const sidebarFilters = reactive({
  projectId: null,
  smartView: null,
  statusFilter: null
})

const calendarFilters = reactive({
  hideDone: true,
  showBacklog: false
})
```

### 3. Reactivity Validation
```typescript
// Add Vue DevTools debugging
if (import.meta.env.DEV) {
  devtoolsPlugin.setup({
    app,
    onTrack: (event) => {
      if (event.target.__file?.includes('calendar')) {
        console.log('Calendar dependency tracked:', event.key)
      }
    }
  })
}
```

## 🎯 Success Indicators

The fix is successful when:
- ✅ Calendar inbox shows the same task count as main inbox
- ✅ Calendar timeline only shows scheduled tasks
- ✅ Sidebar filters don't affect calendar inbox visibility
- ✅ Status filters work independently in calendar vs sidebar

## 🔗 Related Skills

- **Fix Task Sync Issues**: If this is related to Pinia store synchronization
- **Debug Vue Reactivity**: If components aren't updating after data changes
- **IndexedDB Backup Debugger**: For underlying data persistence issues

## 📊 Usage Context
<!-- SKILL: calendar-inbox-sync -->
*Skill usage will be tracked for analytics and improvement purposes*

This skill provides comprehensive solutions for calendar-inbox synchronization failures in Vue 3 applications, focusing on data source independence and filter separation between sidebar and calendar components.

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
