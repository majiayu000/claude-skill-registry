---
name: managing-date-time
description: Standardizes date handling and timezone logic (UTC/PKT) for travel bookings. Use when displaying or saving tour dates.
---

# Date and Time Handling

## When to use this skill
- Displaying departure/arrival times.
- Calculating trip duration.
- Saving booking dates to Appwrite.

## Standard Practices
- **Storage**: Always save dates as **ISO 8601 Strings** in UTC.
- **Display**: Use the user's local time or a fixed PKT (Pakistan Standard Time) if the tour is localized.
- **Library**: Use `date-fns` for complex math (e.g., `addDays`, `differenceInDays`).

## Example (Date-fns)
```typescript
import { format, parseISO } from 'date-fns';

export const formatTourDate = (isoString: string) => {
    const date = parseISO(isoString);
    return format(date, 'MMM dd, yyyy'); // e.g., "Jan 15, 2026"
};
```

## Instructions
- **Input**: Use `<input type="date">` or a custom calendar component (see `managing-date-selection`).
- **Validation**: Ensure end date is not before start date.
