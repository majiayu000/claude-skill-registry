---
name: arrivelah
description: Get Singapore bus arrivals from a source location to a destination. Trigger: "bus from <source> to <destination>"
homepage: https://github.com/abhay/arrivelah
metadata: {"openclaw":{"emoji":"🚌","requires":{"bins":["curl"]},"tags":["singapore","transport","bus","sg"]}}
---

# ArriveLah - Singapore Bus Arrivals

Natural language bus lookup for Singapore.

## Trigger Format

```
bus from <source location> to <destination location>
```

Examples:
- "bus from Silat Road Sikh Temple to Queens condo"
- "bus from Tanjong Pagar MRT to VivoCity"
- "bus from my office to home"

## Step-by-Step Workflow

### Step 1: Geocode source location
Use web_fetch to resolve the source location to coordinates via OneMap API:
```
https://www.onemap.gov.sg/api/common/elastic/search?searchVal=<source>&returnGeom=Y&getAddrDetails=Y&pageNum=1
```
Extract `LATITUDE` and `LONGITUDE` from the first result.

### Step 2: Find nearest bus stops to source
Fetch the full Singapore bus stop list and find stops closest to source coordinates:
```
https://busrouter.sg/data/2/bus-stops.json
```
This returns a JSON object where each key is a bus stop code, with fields: `description`, `road`, `lat`, `lng`.

Compute distance using: `sqrt((lat2-lat1)^2 + (lng2-lng1)^2)` (approximate is fine for short distances).
Pick the **3 nearest** stops within ~300m.

### Step 3: Geocode destination location
Same as Step 1 for the destination. Extract its coordinates.

### Step 4: Find which buses go from source stops toward destination
For each of the 3 nearest source stops, fetch arrivals:
```
https://arrivelah2.busrouter.sg/?id=<stop_code>
```

Then for each bus service at those stops, check if it passes near the destination using:
```
https://busrouter.sg/data/2/routes.json
```
This maps bus service numbers to arrays of stop codes in order. Cross-reference with bus-stops.json to get coordinates of each stop on the route, and check if any stop is within ~400m of the destination coordinates.

Keep only buses that:
1. Have the source stop **before** the destination stop in their route (correct direction)
2. Pass within ~400m of the destination

### Step 5: Fetch live arrival times
For each matching bus at the source stop, get from the arrivelah2 response:
- `next.duration_ms` → minutes until next bus
- `subsequent.duration_ms` → minutes until bus after that
- `next.load` → seat availability: `SEA` = Seats Available, `SDA` = Standing Available, `LSD` = Limited Standing
- `next.feature` → `WAB` = Wheelchair accessible
- `next.type` → `DD` = Double decker, `SD` = Single deck, `BD` = Bendy

### Step 6: Format and return

```
🚌 Buses from [Source Stop Name] → [Destination]

Bus [XX]
  ⏰ Next: X min | Then: Y min
  💺 [Seats Available / Standing / Limited Standing]
  🚌 [Double Decker / Single Deck]

Bus [YY]
  ⏰ Next: X min | Then: Y min
  💺 [Seats Available / Standing / Limited Standing]

📍 Stop: [Stop Description], [Road Name] (Stop code: XXXXX)
```

If no direct bus found, say so and suggest nearest MRT or alternative.

## Load Code Reference
- `SEA` = Seats Available 🟢
- `SDA` = Standing Available 🟡  
- `LSD` = Limited Standing 🔴

## Bus Type Reference
- `DD` = Double Decker
- `SD` = Single Deck
- `BD` = Bendy Bus
- `WAB` = Wheelchair Accessible Bus

## API Endpoints (no auth needed)
- OneMap geocode: `https://www.onemap.gov.sg/api/common/elastic/search`
- Bus stops: `https://busrouter.sg/data/2/bus-stops.json`
- Routes: `https://busrouter.sg/data/2/routes.json`
- Live arrivals: `https://arrivelah2.busrouter.sg/?id=<stop_code>`
