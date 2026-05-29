---
name: shabbat-times
description: Access Jewish calendar data and Shabbat times via Hebcal API. Use when building apps with Shabbat times, Jewish holidays, Hebrew dates, or Zmanim. Triggers on Shabbat times, Hebcal, Jewish calendar, Hebrew date, Zmanim.
---

# Jewish Calendar & Shabbat Times

Access Shabbat times and Jewish calendar data via the Hebcal API.

## Quick Start

```typescript
// Get Shabbat times for a location
const response = await fetch(
  'https://www.hebcal.com/shabbat?cfg=json&geonameid=5128581&M=on'
);
const data = await response.json();
```

## Shabbat Times API

### By GeoNames ID (Recommended)
```typescript
const url = new URL('https://www.hebcal.com/shabbat');
url.searchParams.set('cfg', 'json');
url.searchParams.set('geonameid', '5128581'); // New York
url.searchParams.set('M', 'on'); // Include Havdalah

const response = await fetch(url);
const data = await response.json();

// Response
{
  "title": "Hebcal New York January 2025",
  "items": [
    {
      "title": "Candle lighting: 4:28pm",
      "date": "2025-01-10T16:28:00-05:00",
      "category": "candles"
    },
    {
      "title": "Parashat Shemot",
      "date": "2025-01-11",
      "category": "parashat"
    },
    {
      "title": "Havdalah: 5:31pm", 
      "date": "2025-01-11T17:31:00-05:00",
      "category": "havdalah"
    }
  ]
}
```

### By Coordinates
```typescript
const url = new URL('https://www.hebcal.com/shabbat');
url.searchParams.set('cfg', 'json');
url.searchParams.set('latitude', '32.0853');
url.searchParams.set('longitude', '34.7818');
url.searchParams.set('tzid', 'Asia/Jerusalem');
```

## Jewish Calendar API

```typescript
const url = new URL('https://www.hebcal.com/hebcal');
url.searchParams.set('cfg', 'json');
url.searchParams.set('v', '1');
url.searchParams.set('year', '2025');
url.searchParams.set('month', 'x'); // All months

// Optional parameters
url.searchParams.set('maj', 'on'); // Major holidays
url.searchParams.set('min', 'on'); // Minor holidays
url.searchParams.set('mod', 'on'); // Modern holidays
url.searchParams.set('nx', 'on');  // Rosh Chodesh
url.searchParams.set('ss', 'on');  // Special Shabbatot
url.searchParams.set('s', 'on');   // Weekly parsha

const response = await fetch(url);
const holidays = await response.json();
```

## Hebrew Date Conversion

```typescript
// Gregorian to Hebrew
const url = new URL('https://www.hebcal.com/converter');
url.searchParams.set('cfg', 'json');
url.searchParams.set('gy', '2025');
url.searchParams.set('gm', '1');
url.searchParams.set('gd', '15');

const response = await fetch(url);
const data = await response.json();
// { "hy": 5785, "hm": "Tevet", "hd": 15, "hebrew": "ט״ו בטבת תשפ״ה" }
```

## React Hook

```typescript
import { useState, useEffect } from 'react';

interface ShabbatTimes {
  candleLighting: Date | null;
  havdalah: Date | null;
  parsha: string | null;
}

function useShabbatTimes(geonameid: string) {
  const [times, setTimes] = useState<ShabbatTimes | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchTimes() {
      const url = new URL('https://www.hebcal.com/shabbat');
      url.searchParams.set('cfg', 'json');
      url.searchParams.set('geonameid', geonameid);
      url.searchParams.set('M', 'on');

      const response = await fetch(url);
      const data = await response.json();

      const result: ShabbatTimes = {
        candleLighting: null,
        havdalah: null,
        parsha: null
      };

      for (const item of data.items) {
        if (item.category === 'candles') {
          result.candleLighting = new Date(item.date);
        } else if (item.category === 'havdalah') {
          result.havdalah = new Date(item.date);
        } else if (item.category === 'parashat') {
          result.parsha = item.title.replace('Parashat ', '');
        }
      }

      setTimes(result);
      setLoading(false);
    }

    fetchTimes();
  }, [geonameid]);

  return { times, loading };
}
```

## Common GeoNames IDs

| City | GeoNames ID |
|------|-------------|
| Jerusalem | 281184 |
| Tel Aviv | 293397 |
| New York | 5128581 |
| Los Angeles | 5368361 |
| London | 2643743 |
| Paris | 2988507 |

## Resources

- **Hebcal API Docs**: https://www.hebcal.com/home/developer-apis
