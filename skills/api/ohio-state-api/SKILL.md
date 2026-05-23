---
name: ohio-state-api
description: Get public data from The Ohio State University Content APIs (content.osu.edu) across campus services (bus, buildings, dining, events, academic calendar, libraries, rec sports, parking, directory, student orgs, athletics, food trucks, BuckID merchants). Use when you need OSU campus data, want to build an OSU data feature, or need a repeatable way to fetch/inspect OSU API JSON.
compatibility: Requires outbound internet access to content.osu.edu. Optional: Node.js + npm for the bundled MCP server.
---

## What to use

### Option A: Direct HTTP fetch (quickest)

Use the bundled fetch helper to pull JSON from OSU Content APIs.

- Fetch by full URL:
  - `node ohio-state-api/scripts/osu-fetch.mjs https://content.osu.edu/v2/api/v1/dining/locations`
- Fetch by service + path:
  - `node ohio-state-api/scripts/osu-fetch.mjs --service dining --path /locations`

Note: `--path` can be passed with or without a leading `/` (both work).

If the response is large, add `--extract <dot.path>` (e.g. `--extract data`) to print only a subtree.

### Option A2: curl (no Node required)

If you just want raw JSON and have `curl` available, reference `ohio-state-api/references/OSU_API.md`:

- Full URL:
  - `curl -sS -H 'accept: application/json' 'https://content.osu.edu/v2/api/v1/dining/locations'`
- With query params:
  - `curl -sS -H 'accept: application/json' 'https://content.osu.edu/v2/classes/search?q=cse&p=1'`

Optional: pipe to `jq` for readability:
- `curl -sS -H 'accept: application/json' 'https://content.osu.edu/v2/api/v1/dining/locations' | jq .`

### Option B: MCP server (best for MCP-compatible clients)

This skill bundles the original MCP server under `ohio-state-api/mcp-server/`.

Build it:
- `cd ohio-state-api/mcp-server && npm install && npm run build`

Then configure your MCP client to run:
- command: `node`
- args: `["/ABSOLUTE/PATH/TO/ohio-state-api/mcp-server/build/index.js"]`

After it’s running, use tools like:
- `get_bus_routes`, `get_bus_vehicles`
- `get_buildings`, `search_buildings`, `get_building_details`
- `get_dining_locations`, `get_dining_menu`
- `get_campus_events`, `get_events_by_date_range`
- `search_classes`
- `get_parking_availability`

(See `ohio-state-api/mcp-server/README.md` and the tool definitions in `ohio-state-api/mcp-server/src/` for the full list.)

## Recommended workflow for “get OSU data” requests

1. Identify the service area (dining, bus, buildings, events, etc.).
2. Prefer a list/search endpoint first, then follow IDs into detail endpoints.
3. For time-based data, always include both:
   - the query window (absolute dates/times), and
   - the retrieval timestamp.
4. When returning data to a user, summarize key fields and attach the raw JSON as an artifact when possible.

## Common base URLs (public)

These are used by the bundled MCP server and work with `osu-fetch.mjs`:

- Athletics: `https://content.osu.edu/v3/athletics`
- Bus: `https://content.osu.edu/v2/bus`
- Buildings: `https://content.osu.edu/v2/api`
- Calendar: `https://content.osu.edu/v2/calendar`
- Classes: `https://content.osu.edu/v2/classes`
- Dining: `https://content.osu.edu/v2/api/v1/dining`
- Directory: `https://content.osu.edu`
- Events: `https://content.osu.edu/v2`
- Food trucks: `https://content.osu.edu/v2/foodtruck`
- Library: `https://content.osu.edu/v2/library`
- Merchants: `https://content.osu.edu/v2`
- Parking: `https://content.osu.edu/v2/parking/garages`
- Rec sports: `https://content.osu.edu/v3`
- Student orgs: `https://content.osu.edu/v2/student-org`

## Examples (copy/paste)

- Dining locations:
  - `curl -sS -H 'accept: application/json' 'https://content.osu.edu/v2/api/v1/dining/locations'`
- Parking availability:
  - `curl -sS -H 'accept: application/json' 'https://content.osu.edu/v2/parking/garages/availability'`
- Buildings “search” (filter client-side with `jq`):
  - `curl -sS -H 'accept: application/json' 'https://content.osu.edu/v2/api/buildings' | jq -r '.data.buildings[] | select((.name // \"\") | test(\"union\";\"i\")) | \"\\(.buildingNumber)\\t\\(.name)\"'`

## Extra reference

- API reference: `ohio-state-api/references/OSU_API.md`
