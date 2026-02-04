---
name: calendar-scheduling-fixer
description: This skill should be used when fixing Vue.js calendar task scheduling issues, specifically when tasks with due dates incorrectly appear in calendar grid instead of staying in calendar inbox. The skill provides comprehensive research-backed solutions for separating task management from calendar scheduling with mandatory Playwright testing.
---

# Calendar Scheduling Fixer Skill

This skill provides a comprehensive approach to fixing Vue.js calendar task scheduling issues, specifically addressing the problem where tasks with due dates incorrectly appear in calendar grid slots instead of staying in the calendar inbox.

## When to Use This Skill

Use this skill when encountering these specific issues:
- Tasks moved to "Today" smart groups appear in calendar time slots instead of calendar inbox
- Calendar grid shows tasks that should remain in inbox state
- Task due dates leak into calendar scheduling logic
- Need to separate task management (due dates) from calendar commitments (time slots)
- Calendar view shows duplicate or misplaced tasks

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

## Diagnostic Process

### Step 1: Identify the Problem Layer
Use the diagnostic script to identify where tasks are leaking into calendar:

```bash
node scripts/diagnose-calendar-leak.js
```

This script will:
- Analyze all calendar composables for task filtering logic
- Check for dueDate vs instances confusion in calendar views
- Identify data model inconsistencies
- Provide specific file locations that need fixes

### Step 2: Check Current Task State
Verify task properties using the task state analyzer:

```bash
node scripts/analyze-task-state.js
```

This will show:
- Which tasks have due dates vs instances
- Inbox state status for each task
- Canvas position data
- Scheduling status (inbox vs scheduled)

### Step 3: Test with Playwright (MANDATORY)
Always verify fixes with visual testing:

```bash
node scripts/test-calendar-behavior.js
```

This script:
- Checks if Playwright MCP server is available
- If not available, instructs user to restart it
- Runs comprehensive visual tests
- Verifies tasks stay in inbox, not calendar grid
- Tests drag-and-drop from inbox to calendar

## Implementation Guidelines

### Fix Calendar Day View
In `src/composables/calendar/useCalendarDayView.ts`:

1. **Remove dueDate from calendar event creation**
2. **Only create events for tasks with instances or legacy schedule**
3. **Maintain separate filtering for inbox vs calendar**

### Fix Calendar Week/Month Views
Ensure similar logic applies across all calendar views:
- Check `useCalendarWeekView.ts` and `useCalendarMonthView.ts`
- Apply same filtering principles
- Maintain consistency across views

### Update Calendar Inbox Filtering
In `src/components/CalendarInboxPanel.vue`:

1. **Verify "Today" filter includes tasks with dueDate === today**
2. **Ensure inbox shows tasks with dueDate but no instances**
3. **Maintain proper task state separation**

### Update Smart Group Logic
In `src/stores/tasks.ts`:

1. **Verify `moveTaskToSmartGroup` only sets dueDate**
2. **Ensure tasks maintain `isInInbox: true`**
3. **Prevent automatic instance creation**

## Testing Requirements

### Mandatory Playwright Testing
Before claiming any fix works, perform these visual tests:

1. **Today Group Test**: Move task to "Today" in canvas, verify it appears in calendar inbox "Today" filter but NOT in calendar time slots
2. **Drag Test**: Drag task from calendar inbox to calendar time slot, verify it appears as scheduled event
3. **Multi-view Test**: Verify behavior is consistent across day, week, and month views
4. **State Test**: Verify task properties (dueDate, instances, isInInbox) are correct throughout workflow

### Test Verification Checklist
- [ ] Playwright MCP server is running and accessible
- [ ] Task moved to "Today" appears in Calendar Inbox
- [ ] Task moved to "Today" does NOT appear in calendar time slots
- [ ] Manual drag from inbox to calendar works correctly
- [ ] Task state properties are correct after each operation
- [ ] Behavior is consistent across all calendar views

## Common Pitfalls to Avoid

1. **Don't use dueDate for calendar event creation** - only instances and legacy schedule should create calendar events
2. **Don't mix task and calendar logic** - keep task management separate from calendar display
3. **Don't skip visual testing** - DOM assertions are insufficient, need visual confirmation
4. **Don't ignore multi-view consistency** - fixes must work across day/week/month views
5. **Don't forget state management** - maintain proper inbox vs scheduled state transitions

## Reference Materials

### Research References
- `references/vue-calendar-best-practices.md` - Vue.js calendar implementation patterns
- `references/task-calendar-separation.md` - Data model separation principles
- `references/playwright-calendar-testing.md` - Testing strategies for calendar functionality

### Testing Scripts
- `scripts/diagnose-calendar-leak.js` - Diagnostic tool for identifying calendar scheduling issues
- `scripts/analyze-task-state.js` - Task state analyzer for debugging
- `scripts/test-calendar-behavior.js` - Comprehensive Playwright test runner
- `scripts/verify-fix.js` - Quick verification script for specific fixes

### Code Templates
- `assets/calendar-fix-template.js` - Template for calendar composable fixes
- `assets/test-template.js` - Template for Playwright calendar tests

## Usage Instructions

1. **Run diagnostic** to identify the specific problem
2. **Check task state** to understand current data model issues
3. **Apply fixes** using the implementation guidelines
4. **Test thoroughly** with Playwright (mandatory)
5. **Verify across all views** to ensure consistency
6. **Document changes** for future reference

Always prioritize visual testing and verify that tasks with due dates stay in calendar inbox until manually scheduled to specific time slots.

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
