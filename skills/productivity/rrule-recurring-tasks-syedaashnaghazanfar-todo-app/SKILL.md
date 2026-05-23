---
name: rrule-recurring-tasks
description: RRULE pattern parsing and next occurrence calculation for recurring tasks. Uses python-dateutil for RFC 5545 RRULE support, simplified patterns (daily, weekly, monthly, yearly), and UTC-only time handling.
---

# RRULE Recurring Tasks Skill

RRULE pattern parsing and next occurrence calculation for recurring task management.

## Quick Start

### Installation

```bash
pip install python-dateutil
```

## 1. Basic RRULE Patterns

### Simplified Patterns

```python
from dateutil.rrule import rrule, DAILY, WEEKLY, MONTHLY, YEARLY
from dateutil.parser import parse
from datetime import datetime

# Daily
daily_rule = rrule(DAILY, dtstart=parse("2025-12-29T10:00:00Z"), count=10)

# Weekly
weekly_rule = rrule(WEEKLY, dtstart=parse("2025-12-29T10:00:00Z"), count=10)

# Monthly
monthly_rule = rrule(MONTHLY, dtstart=parse("2025-12-29T10:00:00Z"), count=10)

# Yearly
yearly_rule = rrule(YEARLY, dtstart=parse("2025-12-29T10:00:00Z"), count=10)
```

### Parse RRULE String

```python
from dateutil.rrule import rrulestr

# Parse RFC 5545 RRULE string
rrule_string = """
DTSTART:20251229T100000Z
RRULE:FREQ=DAILY;INTERVAL=1;COUNT=10
"""

rule = rrulestr(rrule_string)
occurrences = list(rule)
```

## 2. Next Occurrence Calculation

### Calculate Next Occurrence

```python
from dateutil.rrule import rrule, DAILY, WEEKLY, MONTHLY, YEARLY
from dateutil.parser import parse
from datetime import datetime, timezone

def calculate_next_occurrence(
    recurring_pattern: str,
    current_occurrence: datetime,
    recurring_end_date: datetime | None = None
) -> datetime | None:
    """Calculate next occurrence from recurring pattern."""
    # Parse pattern
    if recurring_pattern.startswith("FREQ="):
        # Full RRULE string
        rule = rrulestr(
            f"DTSTART:{current_occurrence.strftime('%Y%m%dT%H%M%SZ')}\n"
            f"RRULE:{recurring_pattern}"
        )
    else:
        # Simplified pattern (DAILY, WEEKLY, MONTHLY, YEARLY)
        freq_map = {
            "DAILY": DAILY,
            "WEEKLY": WEEKLY,
            "MONTHLY": MONTHLY,
            "YEARLY": YEARLY
        }
        freq = freq_map.get(recurring_pattern.upper())
        if not freq:
            return None
        
        rule = rrule(
            freq,
            dtstart=current_occurrence,
            count=1,
            interval=1
        )
    
    # Get next occurrence
    next_occurrences = list(rule)
    if not next_occurrences:
        return None
    
    next_occurrence = next_occurrences[0]
    
    # Check if past end date
    if recurring_end_date and next_occurrence > recurring_end_date:
        return None
    
    return next_occurrence.replace(tzinfo=timezone.utc)
```

### Example Usage

```python
from datetime import datetime, timezone

# Current occurrence (task completed)
current = datetime(2025, 12, 29, 10, 0, 0, tzinfo=timezone.utc)

# Calculate next daily occurrence
next_occurrence = calculate_next_occurrence(
    recurring_pattern="DAILY",
    current_occurrence=current
)
# Result: 2025-12-30T10:00:00Z

# With end date
end_date = datetime(2026, 1, 31, 23, 59, 59, tzinfo=timezone.utc)
next_occurrence = calculate_next_occurrence(
    recurring_pattern="WEEKLY",
    current_occurrence=current,
    recurring_end_date=end_date
)
```

## 3. RRULE Parser Service

### Complete Parser

```python
from dateutil.rrule import rrule, rrulestr, DAILY, WEEKLY, MONTHLY, YEARLY
from dateutil.parser import parse
from datetime import datetime, timezone
from typing import Literal

class RRuleParser:
    """Parse RRULE patterns and calculate next occurrences."""
    
    SIMPLIFIED_PATTERNS = {
        "DAILY": DAILY,
        "WEEKLY": WEEKLY,
        "MONTHLY": MONTHLY,
        "YEARLY": YEARLY
    }
    
    def parse_pattern(self, pattern: str) -> rrule:
        """Parse RRULE pattern (simplified or full RFC 5545)."""
        pattern_upper = pattern.upper()
        
        # Check if simplified pattern
        if pattern_upper in self.SIMPLIFIED_PATTERNS:
            freq = self.SIMPLIFIED_PATTERNS[pattern_upper]
            return rrule(freq, interval=1)
        
        # Full RRULE string
        if pattern.startswith("FREQ="):
            return rrulestr(f"RRULE:{pattern}")
        
        # Try parsing as full RRULE
        try:
            return rrulestr(pattern)
        except Exception:
            raise ValueError(f"Invalid RRULE pattern: {pattern}")
    
    def calculate_next(
        self,
        pattern: str,
        dtstart: datetime,
        end_date: datetime | None = None
    ) -> datetime | None:
        """Calculate next occurrence from pattern."""
        rule = self.parse_pattern(pattern)
        
        # Set dtstart
        rule.dtstart = dtstart.replace(tzinfo=timezone.utc)
        
        # Get next occurrence
        occurrences = list(rule)
        if not occurrences:
            return None
        
        next_occurrence = occurrences[0]
        
        # Check end date
        if end_date and next_occurrence > end_date.replace(tzinfo=timezone.utc):
            return None
        
        return next_occurrence
    
    def validate_pattern(self, pattern: str) -> bool:
        """Validate RRULE pattern."""
        try:
            self.parse_pattern(pattern)
            return True
        except Exception:
            return False
```

## 4. Simplified Pattern Generation

### Generate Simplified Patterns

```python
def generate_simplified_pattern(
    frequency: Literal["DAILY", "WEEKLY", "MONTHLY", "YEARLY"],
    interval: int = 1,
    byweekday: str | None = None
) -> str:
    """Generate simplified RRULE pattern."""
    if frequency == "DAILY":
        if interval == 1:
            return "DAILY"
        return f"FREQ=DAILY;INTERVAL={interval}"
    
    if frequency == "WEEKLY":
        pattern = f"FREQ=WEEKLY;INTERVAL={interval}"
        if byweekday:
            pattern += f";BYDAY={byweekday}"
        return pattern
    
    if frequency == "MONTHLY":
        return f"FREQ=MONTHLY;INTERVAL={interval}"
    
    if frequency == "YEARLY":
        return f"FREQ=YEARLY;INTERVAL={interval}"
    
    raise ValueError(f"Unknown frequency: {frequency}")
```

## 5. UTC-Only Time Handling

### Always Use UTC

```python
from datetime import datetime, timezone

# ✅ Good: UTC timestamps
current = datetime.utcnow().replace(tzinfo=timezone.utc)
next_occurrence = calculate_next_occurrence("DAILY", current)

# ❌ Bad: Timezone-aware without UTC
current = datetime.now()  # Local timezone
```

### Convert to UTC

```python
from dateutil.parser import parse

# Parse and convert to UTC
dt = parse("2025-12-29T10:00:00-05:00")  # EST
dt_utc = dt.astimezone(timezone.utc)
```

## 6. Recurring End Date Handling

### Check End Date

```python
def should_create_next_occurrence(
    next_occurrence: datetime,
    recurring_end_date: datetime | None
) -> bool:
    """Check if next occurrence should be created."""
    if not recurring_end_date:
        return True  # No end date, infinite recurrence
    
    return next_occurrence <= recurring_end_date.replace(tzinfo=timezone.utc)
```

## 7. Edge Cases

### DST Transitions

```python
# RRULE handles DST automatically
# Use UTC to avoid DST issues
rule = rrule(
    DAILY,
    dtstart=datetime(2025, 3, 9, 10, 0, 0, tzinfo=timezone.utc),  # DST change day
    count=5
)
```

### Leap Years

```python
# RRULE handles leap years automatically
rule = rrule(
    YEARLY,
    dtstart=datetime(2024, 2, 29, 10, 0, 0, tzinfo=timezone.utc),  # Leap year
    count=5
)
```

## 8. Integration with Task Service

### Update Next Occurrence

```python
from sqlmodel import Session, select

async def update_next_occurrence(
    session: Session,
    task_id: int,
    parser: RRuleParser
) -> datetime | None:
    """Update next_occurrence field for recurring task."""
    task = session.get(Task, task_id)
    
    if not task or not task.recurring_pattern:
        return None
    
    # Calculate next occurrence
    next_occurrence = parser.calculate_next(
        pattern=task.recurring_pattern,
        dtstart=datetime.utcnow().replace(tzinfo=timezone.utc),
        end_date=task.recurring_end_date
    )
    
    if next_occurrence:
        task.next_occurrence = next_occurrence
        session.add(task)
        session.commit()
    
    return next_occurrence
```

## Best Practices

### 1. Always Use UTC

```python
# ✅ Good
dt = datetime.utcnow().replace(tzinfo=timezone.utc)

# ❌ Bad
dt = datetime.now()  # Local timezone
```

### 2. Validate Patterns

```python
parser = RRuleParser()
if not parser.validate_pattern(pattern):
    raise ValueError(f"Invalid pattern: {pattern}")
```

### 3. Handle End Dates

```python
if recurring_end_date and next_occurrence > recurring_end_date:
    return None  # Don't create next occurrence
```

### 4. Cache Parsed Rules

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def get_cached_rule(pattern: str):
    """Cache parsed RRULE patterns."""
    parser = RRuleParser()
    return parser.parse_pattern(pattern)
```

## References

- [python-dateutil RRULE](https://dateutil.readthedocs.io/en/stable/rrule.html)
- [RFC 5545 RRULE](https://www.rfc-editor.org/rfc/rfc5545#section-3.3.10)

