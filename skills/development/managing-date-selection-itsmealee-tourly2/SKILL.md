---
name: managing-date-selection
description: Implements the "Restart Logic" for date range selection in the Tourly search widget. Use when building or modifying the date picker, handling check-in/check-out dates, or implementing calendar interaction algorithms.
---

# Smart Date Range Selection Logic (Tourly)

## When to use this skill
- Implementing the date range selection in the search bar or booking forms.
- Modifying `react-day-picker` or Shadcn Calendar behavior to match Tourly's custom "Restart Logic".
- Handling edge cases where users select an earlier date than the current start date.

## Workflow
- [ ] Initialize state for `startDate`, `endDate`, and `isCalendarOpen`.
- [ ] Implement the `handleDateSelect` algorithm following the Scenarios below.
- [ ] Apply visual styles to the input field and calendar cells based on the selection state.
- [ ] Ensure the popover only closes on a valid range completion.

## The Smart Range Algorithm

### Scenario A: Starting Fresh / Resetting
- **Condition:** No dates selected OR both dates selected and a new date is clicked.
- **Action:** Set `startDate` to selected, `endDate` to `null`. Keep popover **OPEN**.

### Scenario B: Valid Range Completion
- **Condition:** `startDate` exists, `endDate` is `null`, and `selectedDate > startDate`.
- **Action:** Set `endDate` to selected. **CLOSE** popover.

### Scenario C: Backwards Selection (Restart Logic)
- **Condition:** `startDate` exists, `endDate` is `null`, and `selectedDate < startDate`.
- **Action:** Set `startDate` to selected, `endDate` to `null`. Keep popover **OPEN**.
- **Note:** Do NOT swap dates. Treat this as a correction of the start date.

## Visual Requirements
- **Input Text**: Use low-opacity/gray text (e.g., `text-muted-foreground`) to match placeholder style.
- **Calendar Header**: Must display **"Select Dates"**.
- **Highlighting**:
    - **Ends**: Solid primary color circles.
    - **In-between**: Light primary background (e.g., `bg-primary/20`) for the range.

## Instructions
- **Closing Rule**: The popover **MUST NOT** close until Scenario B is met. Automatic closing on the first click is a failure.
- **Library Integration**: When using `react-day-picker`, intercept the `onSelect` or `onDayClick` events to apply this custom logic manualy rather than using the default range mode.
