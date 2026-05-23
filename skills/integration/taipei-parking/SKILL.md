---
name: taipei-parking-query
description: Query real-time parking availability in Taipei City. Shows available parking spaces, capacity, status (green/available, orange/moderate, red/full), address, phone, and payment info. Supports underground/multi-level parking and street parking for cars, motorcycles, and buses. Use when user asks about parking availability, finding parking near a location, or checking parking occupancy in Taipei.
allowed-tools: Read, Bash, Glob
---

# Taipei Parking Availability Finder

Provides real-time parking availability data from Taipei City's official parking API.

## Usage Examples

Users can query in natural language:
- "台北市政府附近有停車位嗎？"
- "Show me underground parking near Taipei 101"
- "Find parking with 20+ spaces within 500 meters of 121.56, 25.04"
- "信義區路邊停車情況如何？"

## Location Input Methods

The skill accepts THREE ways to specify location:

### 1. Coordinates (Most Precise)
Format: `longitude, latitude` (WGS84)
```
Example: "121.56375, 25.03754"
```

### 2. Landmark Names (Recommended)
Common Taipei landmarks are pre-mapped. See [reference.md](reference.md) for full list:
- 台北市政府 / Taipei City Hall
- 台北 101 / Taipei 101
- 西門町 / Ximending
- 台北車站 / Taipei Main Station
- 中正紀念堂 / Chiang Kai-shek Memorial Hall
- (50+ more in reference.md)

### 3. District Names (Broader Search)
For district-level queries, prompt user to specify a more precise location:
```
User: "信義區有停車位嗎？"
Response: "信義區範圍較大，請選擇具體地點：
1. 台北市政府 (121.56375, 25.03754)
2. 台北 101 (121.5645, 25.0340)
3. 或直接提供座標"
```

## Query Process

1. **Parse Location**:
   - If coordinates provided: use directly
   - If landmark name: look up in reference.md
   - If district only: ask for clarification

2. **Execute Query**:
   ```bash
   python3 .claude/skills/taipei-parking/scripts/find_parking.py \
     --lon 121.56375 \
     --lat 25.03754 \
     --distance 500 \
     --vehicle car \
     --type both
   ```

3. **Format Results**:
   Display top 10-20 parking facilities sorted by availability

## Parameters

- `--lon` (required): Longitude (WGS84)
- `--lat` (required): Latitude (WGS84)
- `--distance`: Search radius in meters (default: 1000)
- `--vehicle`: Vehicle type - `car`, `motor`, `bus` (default: car)
- `--type`: Parking type - `underground`, `street`, `both` (default: both)

## Output Format

```
🅿️ Parking near 台北市政府 (within 500m):

1. 市府轉運站地下停車場
   📍 Address: 台北市信義區市府路1號
   🚗 Available: 45/250 spaces (充裕 - Available)
   📞 Phone: (02) 2720-8889
   💳 Payment: 現金、信用卡

2. 市民廣場路邊停車
   📍 Address: 台北市信義區仁愛路四段
   🚗 Available: 2/12 spaces (額滿 - Full)
   📞 Phone: N/A
   💳 Payment: 停車格繳費

[showing 10 results]
```

## Handling Missing Location Data

If user doesn't provide location:
```
To query parking availability, I need a location. Please provide:
1. Coordinates (e.g., "121.56, 25.04")
2. Landmark name (e.g., "台北 101", "西門町")
3. Or ask me to list common locations
```

## Technical Details

- **API Source**: https://itaipeiparking.pma.gov.taipei
- **CSRF Token**: Automatically managed by TaipeiParkingAPI class
- **Coordinate System**: WGS84 (same as Google Maps)
- **Update Frequency**: Real-time (API updates every few minutes)
- **Coverage**: All Taipei City public parking facilities

## Troubleshooting

**If query fails**:
1. Verify coordinates are within Taipei City bounds (lon: 121.4-121.7, lat: 24.9-25.2)
2. Check network connection to itaipeiparking.pma.gov.taipei
3. API may be temporarily down (rare)

**If no results returned**:
- Increase search distance (try 1000m or 2000m)
- Location may be in residential area with limited public parking
- Try different parking type (underground vs street)

## Related Commands

- See [reference.md](reference.md) for comprehensive landmark list
- Check parent project's taipei_parking_api.py for API implementation details
