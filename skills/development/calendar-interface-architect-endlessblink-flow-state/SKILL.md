---
complexity: high
confidence_boost:
  calendar_interface_errors: 0.6
  event_interface_missing: 0.4
  scheduling_problems: 0.5
  temporal_type_issues: 0.5
  inbox_sync_issues: 0.5
  task_scheduling_leaks: 0.5
dependencies:
- typescript
- vue
- pinia
- '@vue/runtime-core'
- vite
- date-fns
- luxon
description: COMPREHENSIVE calendar system skill combining TypeScript interface architecture,
  inbox synchronization debugging, and task scheduling fixes. Handles CalendarEvent
  interface issues, inbox showing 0 tasks problems, and tasks incorrectly appearing
  in calendar grid instead of inbox.
estimated_duration: 25-45 minutes
name: calendar-interface-architect
prerequisites:
- typescript interfaces
- temporal data types
- calendar systems
- date handling
- scheduling algorithms
- vue 3 reactivity
- pinia stores
skill_id: calendar-interface-architect
skill_name: Calendar Interface Architect
tags:
- typescript
- calendar
- interface
- temporal
- scheduling
- event
- date
- time
- architectural
- inbox
- sync
- filtering
token_budget: 5000
triggers:
  contexts:
  - typescript
  - calendar
  - interface
  - temporal
  - scheduling
  - event
  - date
  - time
  - inbox
  - filtering
  file_patterns:
  - src/composables/calendar/*.ts
  - src/views/CalendarView*.vue
  - src/types/recurrence.ts
  - src/stores/taskScheduler.ts
  - src/stores/tasks.ts
  - src/components/CalendarInboxPanel.vue
  keywords:
  - calendar
  - CalendarEvent
  - isDueDate
  - task instance
  - temporal
  - date
  - time
  - scheduling
  - event interface
  - calendar type
  - TaskInstance
  - inbox shows 0 tasks
  - calendar inbox
  - calendar filtering
  - tasks in calendar grid
  - dueDate vs instances
version: 2.0
merged_from:
- calendar-inbox-sync
- calendar-scheduling-fixer
---

# Calendar Interface Architect

This comprehensive skill handles all calendar-related issues in the Pomo-Flow application:
- **TypeScript Interface Architecture**: Fix CalendarEvent and TaskInstance type issues
- **Inbox Synchronization**: Debug calendar inbox showing 0 tasks
- **Scheduling Fixes**: Prevent tasks with due dates from incorrectly appearing in calendar grid

## Quick Context
- **Complexity**: high
- **Duration**: 25-45 minutes
- **Dependencies**: typescript, vue, pinia, @vue/runtime-core, vite, date-fns, luxon

## Activation Triggers
- **Keywords**: calendar, CalendarEvent, isDueDate, task instance, temporal, inbox shows 0 tasks, calendar filtering
- **Files**: src/composables/calendar/*.ts, src/views/CalendarView*.vue, src/types/recurrence.ts
- **Contexts**: typescript, calendar, interface, temporal, scheduling, inbox, filtering

---

# SECTION 1: TypeScript Calendar Interface Architecture

## Critical Calendar Interface Issues

### **IMMEDIATE Calendar Blocking Issues**
**CURRENT COMPILATION ERRORS:**
1. **Property 'isDueDate' does not exist in type 'CalendarEvent'**
2. **TaskInstance type mismatches** in calendar operations
3. **Missing temporal interface properties** for scheduling
4. **Calendar composables failing** due to interface problems

### **Why Calendar Issues Block Application:**
```typescript
// PROBLEM: Missing properties in CalendarEvent interface
const calendarEvent: CalendarEvent = {
  title: 'Task',
  date: '2024-01-01',
  isDueDate: true  // Property does not exist on CalendarEvent
}

// CONSEQUENCE: Calendar functionality breaks, rendering fails
```

## Phase 1: Temporal Type Analysis (Critical)
```typescript
// Comprehensive temporal type system
export interface BaseTemporalEntity {
  id: string
  title: string
  description?: string
  createdAt: Date
  updatedAt: Date
}

export interface CalendarEvent extends BaseTemporalEntity {
  date: string // YYYY-MM-DD format
  time?: string // HH:MM format
  duration?: number // Duration in minutes
  isDueDate: boolean // Whether this represents a task due date
  isAllDay: boolean // Whether this is an all-day event
  color?: string // Event color for UI
  location?: string // Event location
  attendees?: string[] // Event attendees
  recurrencePattern?: RecurrencePattern
  metadata?: Record<string, unknown> // Additional event data
}

export interface TaskCalendarEvent extends CalendarEvent {
  taskId: string // Reference to the original task
  taskStatus: Task['status']
  taskPriority: Task['priority']
  taskProgress: number // Task completion progress
  subtaskProgress?: number[] // Individual subtask progress
  isRecurring: boolean // Whether this is a recurring task instance
  parentTaskId?: string // For recurring task instances
  instanceId?: string // Unique instance identifier
}
```

## Phase 2: TaskInstance Type System (Critical)
```typescript
// Complete TaskInstance interface for calendar operations
export interface TaskInstance {
  id: string // Unique instance identifier
  parentTaskId: string // Reference to original task
  scheduledDate: string // YYYY-MM-DD format
  scheduledTime?: string // HH:MM format
  duration?: number // Duration in minutes
  status: 'scheduled' | 'completed' | 'skipped' | 'in_progress'
  isRecurring: boolean // True for recurring task instances
  isModified?: boolean // True if this instance was modified from pattern
  isSkipped?: boolean // True if this instance is skipped
  recurrenceExceptionId?: string // Link to exception if this is an exception
  pomodoroTracking?: {
    completed: number
    total: number
    duration: number // Duration per pomodoro
  }
  completionData?: {
    completedAt?: Date
    completedBy?: string
    notes?: string
    actualDuration?: number
  }
  metadata?: Record<string, unknown>
}

// Task factory for calendar instances
export interface TaskInstanceFactory {
  createFromTask: (task: Task, date: string, time?: string) => TaskInstance
  createRecurringInstance: (task: Task, pattern: RecurrenceRule, date: string) => TaskInstance
  createException: (instance: TaskInstance, modifications: Partial<TaskInstance>) => TaskInstance
}
```

## Phase 3: Calendar State Management (Critical)
```typescript
// Calendar-specific state management
export interface CalendarState {
  currentDate: Date
  selectedDate: Date | null
  viewMode: 'month' | 'week' | 'day' | 'agenda'
  events: CalendarEvent[]
  taskInstances: TaskInstance[]
  loading: boolean
  error: string | null
  filters: CalendarFilters
}

export interface CalendarFilters {
  showCompleted: boolean
  showInbox: boolean
  projectIds: string[]
  priorities: Task['priority'][]
  statuses: Task['status'][]
}

export interface CalendarActions {
  setCurrentDate: (date: Date) => void
  setSelectedDate: (date: Date | null) => void
  setViewMode: (mode: CalendarState['viewMode']) => void
  addEvent: (event: CalendarEvent) => void
  removeEvent: (eventId: string) => void
  updateEvent: (eventId: string, updates: Partial<CalendarEvent>) => void
  loadTaskInstances: (startDate: Date, endDate: Date) => Promise<void>
  createTaskInstance: (task: Task, date: string, time?: string) => Promise<void>
}
```

---

# SECTION 2: Calendar Inbox Synchronization

## Problem Identification

You're experiencing the classic Vue 3 calendar filtering failure:
- **Inbox shows**: 7 tasks (actual data)
- **Calendar inbox shows**: 0 tasks (filtered out)
- **Root cause**: Calendar uses `taskStore.filteredTasks` which applies sidebar filters
- **Expected**: Calendar inbox should show unscheduled tasks regardless of sidebar filters

## Diagnostic Protocol

### Step 1: Verify the Calendar Filter Issue
Run this diagnostic code in browser console:

```javascript
// Check calendar vs inbox data discrepancy
async function diagnoseCalendarInboxSync() {
  console.group('Calendar-Inbox Sync Diagnosis')

  try {
    // 1. Check task store state
    const taskStore = window.Vue?.config?.globalProperties?.$pinia?._s?.get('tasks')
    if (!taskStore) {
      console.error('Task store not found')
      return
    }

    const allTasks = taskStore.tasks || []
    const filteredTasks = taskStore.filteredTasks || []
    console.log(`All tasks: ${allTasks.length}`)
    console.log(`Filtered tasks: ${filteredTasks.length}`)
    console.log(`Tasks filtered out: ${allTasks.length - filteredTasks.length}`)

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

    console.log(`Inbox tasks: ${inboxTasks.length}`)
    console.log(`Calendar scheduled tasks: ${calendarEligible.length}`)
    console.log(`Calendar inbox tasks: ${calendarInboxTasks.length}`)

    // 3. Identify the problem
    console.group('Problem Analysis')
    if (inboxTasks.length > 0 && filteredTasks.length === 0) {
      console.error('ISSUE: All tasks filtered out - calendar will show 0 tasks')
    }

    if (filteredTasks.length < allTasks.length) {
      console.warn('Sidebar filters are hiding tasks from calendar')
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
    console.error('Diagnosis failed:', error)
  } finally {
    console.groupEnd()
  }
}

// Run diagnosis
await diagnoseCalendarInboxSync()
```

### Issue Types

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

## Specific Fixes

### Fix 1: Calendar Data Source Independence
```typescript
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
```typescript
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

---

# SECTION 3: Calendar Scheduling Fixes

## Core Principles

### 1. Data Model Separation
- **Tasks**: Use `dueDate` field for deadline metadata, stay in inbox until manually scheduled
- **Calendar Events**: Use `instances` array for time-specific commitments with scheduled dates/times
- **State Management**: Maintain clear distinction between inbox state (`isInInbox: true`) and scheduled state

### 2. Visual Separation
- **Inbox Tasks**: Show as cards/panels, draggable to calendar for scheduling
- **Calendar Events**: Show as time blocks with specific start/end times
- **Visual Cues**: Use different styling, icons, and interaction patterns

### 3. Workflow Separation
- **Canvas Smart Groups**: Organize tasks by relevance (Today, Tomorrow, etc.)
- **Calendar Inbox**: Action queue for tasks that need scheduling
- **Calendar Grid**: Commitments with specific time slots

## State Flow Architecture

```
Task Creation -> Smart Groups -> Calendar Inbox -> Manual Scheduling -> Calendar Grid
     |              |              |                    |              |
  New Task     dueDate=Today   isInInbox=true    Create Instance   Show in Calendar
```

### Smart Group Behavior (Canvas "Today" Group)

```typescript
// When task is moved to "Today" smart group:
moveTaskToSmartGroup(taskId, 'today') {
  const updates = {
    dueDate: '2025-11-08',    // Set deadline for organization
    isInInbox: true,          // Keep in inbox for manual scheduling
    // CRITICAL: Do NOT create instances
  }

  updateTask(taskId, updates)
}
```

### Inbox to Calendar Flow

```typescript
// When task is manually scheduled from inbox:
scheduleTaskFromInbox(taskId, date, time) {
  // 1. Create calendar instance
  createTaskInstance(taskId, {
    scheduledDate: date,
    scheduledTime: time
  })

  // 2. Remove from inbox state
  updateTask(taskId, { isInInbox: false })

  // 3. Task now appears in calendar grid
}
```

## Common Violations and Solutions

### Violation 1: Tasks with dueDate appear in calendar

**Problem:**
```typescript
// Wrong: Creating calendar events from dueDate
if (task.dueDate === today) {
  createCalendarEvent(task)  // This should NOT happen
}
```

**Solution:**
```typescript
// Correct: Only create events from instances
if (task.instances?.some(inst => inst.scheduledDate === today)) {
  createCalendarEvent(task)  // Only for explicitly scheduled tasks
}
```

### Violation 2: Tasks in both inbox and calendar

**Problem:**
```typescript
// Wrong: Task appears in both places
const updates = {
  dueDate: today,
  isInInbox: true,
  instances: [{ scheduledDate: today, scheduledTime: '09:00' }]
}
```

**Solution:**
```typescript
// Correct: Clear state transition
const updates = {
  dueDate: today,
  isInInbox: false,      // Remove from inbox
  instances: [{ scheduledDate: today, scheduledTime: '09:00' }]
}
```

### Violation 3: Smart groups create scheduling

**Problem:**
```typescript
// Wrong: Smart group creates time-based scheduling
moveTaskToSmartGroup(taskId, 'today') {
  createTaskInstance(taskId, { scheduledDate: today, scheduledTime: '09:00' })
}
```

**Solution:**
```typescript
// Correct: Smart group only sets deadline
moveTaskToSmartGroup(taskId, 'today') {
  updateTask(taskId, { dueDate: today })
  // Task stays in inbox for manual scheduling
}
```

---

# Implementation Patterns

## Pattern 1: Calendar Event Factory
```typescript
// Factory for creating calendar events from different sources
export class CalendarEventFactory {
  static fromTask(task: Task, date: string, time?: string): TaskCalendarEvent {
    return {
      id: generateId(),
      title: task.title,
      description: task.description,
      date,
      time,
      duration: task.estimatedDuration || 25,
      isDueDate: true,
      isAllDay: !time,
      color: this.getTaskEventColor(task.priority),
      taskId: task.id,
      taskStatus: task.status,
      taskPriority: task.priority,
      taskProgress: task.progress,
      isRecurring: false,
      createdAt: new Date(),
      updatedAt: new Date()
    }
  }

  static fromTaskInstance(instance: TaskInstance): TaskCalendarEvent {
    const task = taskStore.getTask(instance.parentTaskId)
    if (!task) {
      throw new Error(`Task not found: ${instance.parentTaskId}`)
    }

    return {
      id: instance.id,
      title: task.title,
      description: task.description,
      date: instance.scheduledDate,
      time: instance.scheduledTime,
      duration: instance.duration,
      isDueDate: true,
      isAllDay: !instance.scheduledTime,
      color: this.getTaskEventColor(task.priority),
      taskId: task.id,
      taskStatus: task.status,
      taskPriority: task.priority,
      taskProgress: task.progress,
      isRecurring: instance.isRecurring,
      parentTaskId: instance.parentTaskId,
      instanceId: instance.id,
      createdAt: new Date(),
      updatedAt: new Date()
    }
  }

  private static getTaskEventColor(priority: Task['priority']): string {
    switch (priority) {
      case 'high': return '#ef4444'
      case 'medium': return '#f59e0b'
      case 'low': return '#10b981'
      default: return '#6b7280'
    }
  }
}
```

## Pattern 2: Type-Safe Calendar Store
```typescript
// Pinia store for calendar state with full type safety
export const useCalendarStore = defineStore('calendar', () => {
  const state = ref<CalendarState>({
    currentDate: new Date(),
    selectedDate: null,
    viewMode: 'month',
    events: [],
    taskInstances: [],
    loading: false,
    error: null,
    filters: {
      showCompleted: true,
      showInbox: true,
      projectIds: [],
      priorities: [],
      statuses: []
    }
  })

  const actions: CalendarActions = {
    setCurrentDate: (date: Date) => {
      state.value.currentDate = date
    },

    addEvent: (event: CalendarEvent) => {
      state.value.events.push(event)
    },

    async createTaskInstance(task: Task, date: string, time?: string): Promise<void> {
      try {
        const instance = taskStore.createTaskInstance(task, date, time)
        state.value.taskInstances.push(instance)
      } catch (error) {
        state.value.error = error instanceof Error ? error.message : 'Failed to create instance'
      }
    }
  }

  // Computed properties
  const filteredEvents = computed((): TaskCalendarEvent[] => {
    return state.value.taskInstances
      .filter(instance => passesFilters(instance, state.value.filters))
      .map(instance => CalendarEventFactory.fromTaskInstance(instance))
  })

  return {
    state: readonly(state),
    actions,
    filteredEvents
  }
})
```

## Pattern 3: Date Type Safety
```typescript
// Type-safe date utilities for calendar operations
export class CalendarDateUtils {
  static parseDateKey(dateKey: string): Date {
    const [year, month, day] = dateKey.split('-').map(Number)
    if (isNaN(year) || isNaN(month) || isNaN(day)) {
      throw new Error(`Invalid date format: ${dateKey}`)
    }
    return new Date(year, month - 1, day)
  }

  static formatDateKey(date: Date): string {
    return format(date, 'yyyy-MM-dd')
  }

  static isValidTime(time: string): boolean {
    const timeRegex = /^([01]?[0-9]|2[0-3]):[0-5][0-9]$/
    return timeRegex.test(time)
  }

  static parseTime(time: string): { hours: number; minutes: number } {
    if (!this.isValidTime(time)) {
      throw new Error(`Invalid time format: ${time}`)
    }

    const [hours, minutes] = time.split(':').map(Number)
    return { hours, minutes }
  }

  static addTimeToDate(date: string, time: string, duration: number): Date {
    const baseDate = this.parseDateKey(date)
    const { hours, minutes } = this.parseTime(time)

    const result = new Date(baseDate)
    result.setHours(hours, minutes, 0, 0)
    result.setMinutes(result.getMinutes() + duration)

    return result
  }
}
```

---

# Testing Requirements

## Mandatory Playwright Testing
Before claiming any fix works, perform these visual tests:

1. **Today Group Test**: Move task to "Today" in canvas, verify it appears in calendar inbox "Today" filter but NOT in calendar time slots
2. **Drag Test**: Drag task from calendar inbox to calendar time slot, verify it appears as scheduled event
3. **Multi-view Test**: Verify behavior is consistent across day, week, and month views
4. **State Test**: Verify task properties (dueDate, instances, isInInbox) are correct throughout workflow
5. **Inbox Count Test**: Verify calendar inbox shows same count as main inbox

## Test Verification Checklist
- [ ] Playwright MCP server is running and accessible
- [ ] Task moved to "Today" appears in Calendar Inbox
- [ ] Task moved to "Today" does NOT appear in calendar time slots
- [ ] Manual drag from inbox to calendar works correctly
- [ ] Task state properties are correct after each operation
- [ ] Behavior is consistent across all calendar views
- [ ] Calendar inbox shows correct task count regardless of sidebar filters

## Validation Commands
```bash
# TypeScript compilation check
npx tsc --noEmit --skipLibCheck

# Calendar-specific tests
npm run test -- --grep "calendar"

# Development server test
npm run dev
```

---

# Reference Materials

See the `references/` directory for detailed documentation:
- `task-calendar-separation.md` - Data model separation principles
- `vue-calendar-best-practices.md` - Vue.js calendar implementation patterns

---

# Expected Outcomes

After successful execution:
- Complete CalendarEvent Interface: All required properties including isDueDate
- TaskInstance Type System: Full type safety for task instances
- Calendar Functionality: All calendar views work properly
- Scheduling Integration: Tasks can be scheduled on calendar
- Temporal Type Safety: All date/time operations are type-safe
- Inbox Sync: Calendar inbox shows correct task count
- Task-Calendar Separation: Tasks with dueDate stay in inbox until manually scheduled

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
