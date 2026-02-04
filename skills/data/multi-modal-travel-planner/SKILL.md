---
name: multi-modal-travel-planner
description: When the user requests a complete travel itinerary involving multiple modes of transportation with specific waypoints and preferences. This skill handles end-to-end journey planning including 1) Finding nearby points of interest (like coffee shops) relative to departure points, 2) Calculating optimal transit routes between locations with cost and duration information, 3) Determining walking routes from arrival points to final destinations, and 4) Formatting the complete plan into structured output. Triggers include requests for 'travel plans', 'route planning', 'journey from X to Y', or when users specify multiple destinations with preferences like 'direct route', 'shortest distance', or 'nearest [business type]'.
---
# Instructions

## 1. Interpret the Request
- Identify the **departure point**, **final destination**, and any **intermediate waypoints** (e.g., "buy a Starbucks").
- Note specific user preferences: "direct route," "shortest possible distance," "as close as possible to [location]."
- Clarify the required **output format** if specified (e.g., `format.json`).

## 2. Gather Location Data
- Use `google_map-maps_geocode` to get coordinates and canonical addresses for all named locations (departure, destination, waypoints).
- If a waypoint is a generic business type (e.g., "Starbucks"), use `google_map-maps_search_places` with the departure location as a reference point and a reasonable radius (e.g., 500m).
- For the closest match, use `google_map-maps_place_details` to get the full address and confirm proximity.

## 3. Plan the Main Transit Route
- Use `google_map-maps_directions` in `transit` mode between the departure and final destination.
- **If the API returns `ZERO_RESULTS`**, use the `playwright_with_chunk` browser tool to navigate to `https://www.google.com/maps/dir/[ORIGIN]/[DESTINATION]` and scrape the transit information from the page. Look for the "Best" or "Transit" option.
- Extract key details: **line name** (e.g., "Yokosuka Line"), **duration**, and **cost**.

## 4. Plan the Final Walking Route
- Use `google_map-maps_directions` in `walking` mode from the arrival station/point to the final destination.
- If the optimal exit from the arrival point is ambiguous (e.g., different station exits), use `google_map-maps_distance_matrix` to compare walking distances from plausible exits (e.g., "East Exit" vs. "West Exit") to the destination. Recommend the exit with the shortest distance.

## 5. Assemble and Format the Plan
- Compile all gathered data into a structured JSON object matching the user's requested format.
- Use `filesystem-write_file` to save the final plan to the specified path.
- Optionally, use `filesystem-read_file` to verify the output and present a concise summary to the user.

## Key Principles
- **Progressive Disclosure**: Use the bundled `reference/format_guide.md` for complex output schema details.
- **Direct Route Priority**: When the user asks for a "direct route," prioritize transit options with no transfers.
- **Closest Point of Interest**: For requests like "as close as possible," filter search results by distance from the reference point.
