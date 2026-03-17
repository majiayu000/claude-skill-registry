---
name: _util-resolve-date
description: Resolve flexible time expressions (tomorrow, next monday, last week) to concrete dates
disable-model-invocation: true
---

# Resolve Dates

Parse flexible time expressions and resolve to concrete dates for skill execution.

## Inputs

- `$1` (time_expression) — Optional. Time expression to resolve. Can be:
  - Empty or "today" — Resolves to current date
  - "tomorrow" — Next day
  - "next monday" (or any weekday) — Next occurrence of that weekday
  - "last week" — Previous week's workdays (Monday-Friday)
  - "YYYY-MM-DD" — Specific ISO date (validated)
- `$2` (session_dir) — Required. Session directory path where dates.md will be written

## Task

Resolve the time expression using macOS date commands and write results to `dates.md` in the session directory.

```bash
#!/bin/bash
set -euo pipefail

time_expr="${1:-today}"
session_dir="${2:?Error: session directory required}"

# Ensure session directory exists
if [[ ! -d "$session_dir" ]]; then
    echo "Error: Session directory does not exist: $session_dir" >&2
    exit 1
fi

# Initialize variables
target_date=""
scope="day"
relative=""
day_of_week=""
week_start=""
week_end=""
declare -a workdays=()

# Normalize input: lowercase and trim whitespace
time_expr_lower=$(echo "$time_expr" | tr '[:upper:]' '[:lower:]')
time_expr_lower="${time_expr_lower#"${time_expr_lower%%[![:space:]]*}"}"  # trim leading
time_expr_lower="${time_expr_lower%"${time_expr_lower##*[![:space:]]}"}"  # trim trailing

# Resolve based on expression
case "$time_expr_lower" in
    ""|"today")
        target_date=$(date +"%Y-%m-%d")
        scope="day"
        relative="today"
        ;;

    "tomorrow")
        target_date=$(date -v+1d +"%Y-%m-%d")
        scope="day"
        relative="tomorrow"
        ;;

    "next monday"|"next tuesday"|"next wednesday"|"next thursday"|"next friday"|"next saturday"|"next sunday")
        # Extract day name
        day_name=$(echo "$time_expr_lower" | cut -d' ' -f2)

        # Validate day name is not empty
        if [[ -z "$day_name" ]]; then
            echo "Error: Day name required after 'next' (e.g., 'next monday')" >&2
            exit 1
        fi

        # Map day names to macOS date -v weekday flags
        case "$day_name" in
            "sunday")    target_date=$(date -v+sunday +"%Y-%m-%d"); day_of_week="Sunday" ;;
            "monday")    target_date=$(date -v+monday +"%Y-%m-%d"); day_of_week="Monday" ;;
            "tuesday")   target_date=$(date -v+tuesday +"%Y-%m-%d"); day_of_week="Tuesday" ;;
            "wednesday") target_date=$(date -v+wednesday +"%Y-%m-%d"); day_of_week="Wednesday" ;;
            "thursday")  target_date=$(date -v+thursday +"%Y-%m-%d"); day_of_week="Thursday" ;;
            "friday")    target_date=$(date -v+friday +"%Y-%m-%d"); day_of_week="Friday" ;;
            "saturday")  target_date=$(date -v+saturday +"%Y-%m-%d"); day_of_week="Saturday" ;;
            *)
                echo "Error: Invalid day name: $day_name" >&2
                exit 1
                ;;
        esac

        # macOS date -v+weekday returns current day if today is that weekday
        # For "next monday", we want the NEXT occurrence, so add 7 days if result is today
        if [[ "$target_date" == "$(date +"%Y-%m-%d")" ]]; then
            target_date=$(date -j -f "%Y-%m-%d" -v+7d "$target_date" +"%Y-%m-%d")
        fi

        scope="day"
        relative="next $day_name"
        ;;

    "last week")
        # Calculate previous week's Monday-Friday range
        # Strategy: Go to most recent Monday, then back 7 days to get last week's Monday
        week_start=$(date -v-monday -v-7d +"%Y-%m-%d")
        week_end=$(date -v-monday -v-7d -v+4d +"%Y-%m-%d")

        target_date="$week_start"
        scope="week"
        relative="last week"

        # Generate array of workdays (Monday through Friday of last week)
        base_date="$week_start"
        workdays+=($(date -j -v+0d -f "%Y-%m-%d" "$base_date" +"%Y-%m-%d"))
        workdays+=($(date -j -v+1d -f "%Y-%m-%d" "$base_date" +"%Y-%m-%d"))
        workdays+=($(date -j -v+2d -f "%Y-%m-%d" "$base_date" +"%Y-%m-%d"))
        workdays+=($(date -j -v+3d -f "%Y-%m-%d" "$base_date" +"%Y-%m-%d"))
        workdays+=($(date -j -v+4d -f "%Y-%m-%d" "$base_date" +"%Y-%m-%d"))
        ;;

    [0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9])
        # Validate ISO date format
        if date -j -f "%Y-%m-%d" "$time_expr_lower" >/dev/null 2>&1; then
            target_date="$time_expr_lower"
            scope="day"
            relative="$time_expr_lower"
        else
            echo "Error: Invalid date format: $time_expr_lower (expected YYYY-MM-DD)" >&2
            exit 1
        fi
        ;;

    *)
        echo "Error: Unsupported time expression: $time_expr_lower" >&2
        echo "Supported: today, tomorrow, next <weekday>, last week, YYYY-MM-DD" >&2
        exit 1
        ;;
esac

# Write dates.md
dates_file="$session_dir/dates.md"
{
    echo "# Date Context"
    echo ""
    echo "target_date: $target_date"
    echo "scope: $scope"
    echo "relative: $relative"

    if [[ -n "$day_of_week" ]]; then
        echo "day_of_week: $day_of_week"
    fi

    if [[ -n "$week_start" ]]; then
        echo "week_start: $week_start"
    fi

    if [[ -n "$week_end" ]]; then
        echo "week_end: $week_end"
    fi

    if [[ ${#workdays[@]} -gt 0 ]]; then
        echo "workdays:"
        for workday in "${workdays[@]}"; do
            echo "  - $workday"
        done
    fi
} > "$dates_file"

# Output confirmation
echo "Resolved '$time_expr' to dates.md:"
cat "$dates_file"
```

## Output Format

The skill writes `dates.md` to the session directory with this structure:

```markdown
# Date Context

target_date: 2026-02-15
scope: day
relative: today
```

For "next monday":
```markdown
# Date Context

target_date: 2026-02-17
scope: day
relative: next monday
day_of_week: Monday
```

For "last week":
```markdown
# Date Context

target_date: 2026-02-03
scope: week
relative: last week
week_start: 2026-02-03
week_end: 2026-02-07
workdays:
  - 2026-02-03
  - 2026-02-04
  - 2026-02-05
  - 2026-02-06
  - 2026-02-07
```

## Error Handling

The skill exits with non-zero status and writes to stderr for:
- Missing session directory argument
- Non-existent session directory
- Missing day name after "next" keyword
- Invalid day name (not a recognized weekday)
- Invalid date format (malformed YYYY-MM-DD)
- Unsupported time expression

## Examples

```bash
# Today
session_dir=$(mktemp -d)
claude skill run resolve-dates -- "" "$session_dir"

# Tomorrow
session_dir=$(mktemp -d)
claude skill run resolve-dates -- "tomorrow" "$session_dir"

# Next Monday
session_dir=$(mktemp -d)
claude skill run resolve-dates -- "next monday" "$session_dir"

# Last week
session_dir=$(mktemp -d)
claude skill run resolve-dates -- "last week" "$session_dir"

# Specific date
session_dir=$(mktemp -d)
claude skill run resolve-dates -- "2026-03-15" "$session_dir"
```

## Notes

- Uses macOS `date -v` flags for date arithmetic
- Uses system timezone for all date calculations
- The `-v+monday` syntax finds the next Monday, OR returns current day if today is Monday
- For "next monday", we explicitly check if result equals today and add 7 days to ensure NEXT occurrence
- "last week" resolves to previous Monday-Friday range (workdays only)
- All dates output in ISO 8601 format (YYYY-MM-DD)
