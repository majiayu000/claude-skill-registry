---
name: michael-d1-swimming
description: 'Michael Shapira''s D1 swimming pathway tracking for Life OS. Manages
  swim times, nutrition protocol (kosher keto), recruiting outreach, and rival comparison.
  Events: 50/100/200 Free, 100 Fly, 100 Back.'
---

---
name: michael-d1-swimming
description: Michael Shapira's D1 swimming pathway tracking for Life OS. Manages swim times, nutrition protocol (kosher keto), recruiting outreach, and rival comparison. Events: 50/100/200 Free, 100 Fly, 100 Back. SwimCloud ID: 3250085. Use when tracking swim performance, analyzing times, managing nutrition, planning recruiting, or comparing against rivals (Soto PI:47, Gordon PI:90, Domboru PI:102).
---

# Michael Shapira D1 Swimming

## Athlete Profile

- **Name:** Michael Shapira
- **DOB:** July 22, 2009 (16 years old)
- **School:** Satellite Beach High School, Class of 2027
- **SwimCloud ID:** 3250085
- **Primary Events:** 50 Free, 100 Free, 200 Free, 100 Fly, 100 Back
- **Course:** Primarily SCY (Short Course Yards)

## D1 Time Standards (SCY)

| Event | D1 Min | Michael Current | Gap |
|-------|--------|-----------------|-----|
| 50 Free | 20.00 | TBD | TBD |
| 100 Free | 44.00 | TBD | TBD |
| 200 Free | 1:36.00 | TBD | TBD |
| 100 Fly | 48.00 | TBD | TBD |
| 100 Back | 48.00 | TBD | TBD |

## Verified Rivals

| Name | SwimCloud ID | Power Index | Primary Events |
|------|--------------|-------------|----------------|
| Soto | 2928537 | 47 | Sprint Free |
| Gordon | 1733035 | 90 | IM, Distance |
| Domboru | 1518102 | 102 | Sprint Free |

## Nutrition Protocol

Following Michael Andrew's kosher-adapted keto diet:

### Monday-Thursday (Strict Keto)
- **Macros:** 75% fat, 20% protein, 5% carbs
- **Breakfast:** Eggs, avocado, kosher salmon
- **Lunch:** Salad with olive oil, grilled chicken
- **Dinner:** Steak/fish, non-starchy vegetables
- **Snacks:** Nuts, cheese, olives

### Friday-Sunday (Moderate for Shabbat)
- **Allowed:** Challah, moderate carbs with Shabbat meals
- **Target:** <100g carbs/day
- **Hydration:** Maintain electrolytes

### Pre-Race Protocol
- 48 hours out: Standard keto
- 24 hours out: Light carb load if major meet
- Morning of: Easy digestible protein + minimal carbs

## Recruiting Timeline (Class of 2027)

| Date | Milestone |
|------|-----------|
| Jan 2025 | NCAA ID registration |
| Spring 2025 | Unofficial visits begin |
| Summer 2025 | Camp attendance |
| Sep 2025 | Official contact allowed |
| Nov 2025 | Official visits |
| Spring 2026 | Commit window |

## SwimCloud Data Parsing

```python
def parse_swimcloud_times(swimmer_id: str = "3250085") -> dict:
    """Parse latest times from SwimCloud."""
    url = f"https://www.swimcloud.com/swimmer/{swimmer_id}/"
    # Implementation uses requests + BeautifulSoup
    # Returns: {'50 Free': 22.45, '100 Free': 49.87, ...}
```

## Logging to Supabase

Log times to `michael_swim_times` table:

```python
def log_swim_time(event: str, time: float, meet: str, is_pb: bool):
    supabase.table('michael_swim_times').insert({
        'date': datetime.now().date(),
        'event': event,
        'time_seconds': time,
        'time_formatted': format_swim_time(time),
        'meet_name': meet,
        'course': 'SCY',
        'is_pb': is_pb
    }).execute()
```

## Progress Tracking

### Improvement Metrics
```sql
SELECT
  event,
  MIN(time_seconds) as best,
  MAX(time_seconds) as worst,
  AVG(time_seconds) as average,
  COUNT(*) as races
FROM michael_swim_times
WHERE date > NOW() - INTERVAL '6 months'
GROUP BY event;
```

### PB History
```sql
SELECT event, time_formatted, meet_name, date
FROM michael_swim_times
WHERE is_pb = true
ORDER BY date DESC;
```

## Meet Schedule

Track upcoming meets in `family_events` table:
- Harry Meisel: Dec 13-14, 2025
- State Championships: TBD
- Sectionals: TBD

## References

- `references/d1-cut-times.md` - Complete D1/D2/D3 standards
- `references/rivals-analysis.md` - Detailed rival comparison
- `references/recruiting-contacts.md` - Coach contact database
- `data/` - Historical times and meet results
