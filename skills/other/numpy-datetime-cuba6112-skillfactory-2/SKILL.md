---
name: numpy-datetime
description: Date and time handling with datetime64 and timedelta64, including business day offsets and naive time parsing. Triggers: datetime64, timedelta64, busday, time series, naive time.
---

## Overview
NumPy implements `datetime64` for fixed-point dates and `timedelta64` for durations. Unlike Python's standard `datetime`, NumPy's implementation is "naive" (no timezones) and designed for high-performance vectorized operations on time-series data.

## When to Use
- Creating uniform time grids for simulations or financial modeling.
- Calculating business day offsets while accounting for weekends and holidays.
- Performing arithmetic between dates (e.g., finding durations in hours).
- Handling timestamp datasets where timezone complexity is not required.

## Decision Tree
1. Need to create a sequence of dates?
   - Use `np.arange(start, stop, dtype='datetime64[D]')`.
2. Calculating work deadlines?
   - Use `np.busday_offset` with the `holidays` parameter.
3. Converting a duration to a numeric float (e.g., hours)?
   - Divide the `timedelta64` by `np.timedelta64(1, 'h')`.

## Workflows
1. **Generating a Custom Date Range**
   - Define a start date and end date as strings (e.g., '2023-01-01').
   - Use `np.arange(start, end, dtype='datetime64[D]')` to create the sequence.
   - Index the resulting array to select specific dates.

2. **Calculating Business Deadlines**
   - Select a start date.
   - Use `np.busday_offset(date, 10, roll='forward')` to find the date 10 business days later.
   - Pass a 'holidays' list to ensure the calculation skips known non-working days.

3. **Time-Difference Analysis**
   - Subtract two `datetime64` arrays to get a `timedelta64` result.
   - Divide the result by `np.timedelta64(1, 'h')` to convert the duration into a float of hours.
   - Perform statistical analysis (e.g., mean duration) on the numeric result.

## Non-Obvious Insights
- **Naive Assumption:** `datetime64` ignores timezones and assumes 86,400 SI seconds per day, meaning it cannot parse timestamps during positive leap seconds.
- **Unsafe Casting:** Conversion between variable-length units (Months/Years) and fixed-length units (Days) is considered "unsafe" because their relationship changes (leap years, month lengths).
- **Precision Mapping:** The unit in brackets (e.g., `[ms]`, `[D]`) determines the resolution and the maximum range the timestamp can represent.

## Evidence
- "This is a “naive” time, with no explicit notion of timezones or specific time scales." [Source](https://numpy.org/doc/stable/reference/arrays.datetime.html)
- "Timedelta day unit is equivalent to 24 hours, month and year units cannot be converted directly into days without using ‘unsafe’ casting." [Source](https://numpy.org/doc/stable/reference/arrays.datetime.html)

## Scripts
- `scripts/numpy-datetime_tool.py`: Logic for business day calculations and time delta conversion.
- `scripts/numpy-datetime_tool.js`: Simulated ISO date range generator.

## Dependencies
- `numpy` (Python)

## References
- [references/README.md](references/README.md)