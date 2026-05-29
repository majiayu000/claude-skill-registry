---
name: working-day
description: Reference for the business "working day" concept that runs from 4am to 4am. Use when dealing with date filtering, reports, sales tracking, or any time-based queries.
user-invocable: false
---

# Working Day Concept

This POS system uses a "working day" that runs from **4:00 AM to 3:59 AM the next day**, not midnight to midnight.

## Why This Matters

Restaurants often operate past midnight. A sale at 1:00 AM on January 16th should count as January 15th's revenue (the previous business day).

## Implementation

### Service Location
`services/WorkingDay.php`

### Key Methods

```php
use Services\WorkingDay;

// Get today's working day range (returns [start, end] timestamps)
$range = WorkingDay::getWorkingDay();
// Returns: ['2024-01-15 04:00:00', '2024-01-16 03:59:59']

// Get working day for specific date
$range = WorkingDay::getWorkingDay(Carbon::parse('2024-01-15'));

// Get yesterday's working day
$range = WorkingDay::getWorkingDay(null, 'yesterday');

// Get range for date picker selection
$range = WorkingDay::getWorkingDayForRange('2024-01-10 to 2024-01-15');

// Get correct date for current moment (for storing)
$date = WorkingDay::setCorrectDateForWorkingDay();
// At 2:00 AM on Jan 16, returns '2024-01-15'
```

### Logic

```php
public static function getWorkingDay(Carbon $date = null, $day = null)
{
    if (!$date) $date = Carbon::now();

    // If between midnight and 4am, consider it previous day
    if($date->between("00:00:00", "03:59:59", true)) {
        $date = $date->yesterday();
    }

    if($day === 'yesterday') {
        $date = $date->subDays(1);
    }

    // Return 4am to 4am range
    return [
        $date->startOfDay()->addHours(4)->toDateTimeString(),
        $date->endOfDay()->addHours(4)->toDateTimeString()
    ];
}
```

## Where It's Used

### Invoice Queries
```php
// Get today's invoices
$invoices = Invoice::whereBetween('created_at', WorkingDay::getWorkingDay())->get();
```

### Dashboard Stats
```php
// In DashboardController
$todayRange = WorkingDay::getWorkingDay();
$revenue = Invoice::whereBetween('created_at', $todayRange)
    ->where('status', Invoice::STATUS_PAYED)
    ->sum('total');
```

### Warehouse Status
```php
// In SalesService::populateWarehouse()
'date' => WorkingDay::setCorrectDateForWorkingDay()
```

### Reports
```php
// In ReportsController
$range = WorkingDay::getWorkingDayForRange($request->date);
$sales = Sales::whereBetween('created_at', $range)->get();
```

### Tasks
```php
// In TaskController::indexForToday()
$tasks = Task::whereBetween('created_at', WorkingDay::getWorkingDay())->get();
```

## API Endpoint

```
GET /api/working-day
```
Returns the current working day range for frontend use.

## Important Considerations

1. **Always use WorkingDay** for date filtering in reports and queries
2. **Store the "business date"** using `setCorrectDateForWorkingDay()` when creating records that need date grouping
3. **Date pickers** should use `getWorkingDayForRange()` for proper range calculations
4. **Testing**: Be aware that tests run at different times may have different "working days"
