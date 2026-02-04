---
name: route-data-compiler
description: When the user requires detailed transit line information including complete station sequences between transfer points. This skill fetches comprehensive transit network data from authoritative sources, extracts station lists for specific line segments, identifies transfer stations, and organizes the information into sequential itineraries for route documentation.
---
# Instructions

## Core Objective
Compile a complete, sequential list of transit stations between origin and destination points, including all intermediate stations along each line segment and transfer points. The output should be saved to a specified file.

## Workflow

### 1. Initial Location Analysis
- Use `google_map-maps_geocode` to obtain precise coordinates for both origin and destination addresses.
- Use `google_map-maps_search_places` with query "MRT station" (or relevant transit type) and a small radius (e.g., 1000m) around the origin coordinates to identify the nearest transit station(s).
- Use `google_map-maps_distance_matrix` with mode "walking" to compare walking distances to candidate stations. Select the station with the shortest walking distance.

### 2. Route Planning
- Use `google_map-maps_directions` with mode "transit" between the origin and destination to obtain a high-level route. This provides the sequence of line segments and transfer points.
- Analyze the route steps to identify:
  - The boarding station (nearest station from step 1).
  - Each transit line segment (e.g., "Subway towards Expo").
  - Each transfer station.
  - The alighting station.

### 3. Detailed Station Data Collection
For each identified transit line segment between transfer points (or between boarding/alighting station and a transfer point):
- **Primary Method:** Use `fetch-fetch_markdown` to retrieve the Wikipedia page for the specific transit line (e.g., "Downtown Line", "East–West MRT line").
- **Fallback Method:** If Wikipedia fetch fails or is insufficient, use `local-web_search` with queries like "[Line Name] stations list" or "[Station A] to [Station B] stations".
- From the retrieved data, extract the **complete, ordered list of stations** for the relevant segment of the line. Ensure the list direction matches the travel direction (e.g., from Little India towards Bugis).

### 4. Itinerary Compilation
- Assemble the final station sequence by concatenating the lists from each segment, ensuring:
  1. The boarding station is first.
  2. Transfer stations appear only once at the point of transfer.
  3. The sequence flows logically from origin to destination.
- Verify the total count and order against the high-level route from Step 2.

### 5. Output Generation
- Use `filesystem-write_file` to save the compiled list of stations to the user-specified file path (e.g., `routine.txt`).
- Format: One station name per line, in sequential order.
- Provide a concise summary to the user confirming completion, total stations, and the save location.

## Key Considerations
- **Accuracy:** Prefer official sources (Wikipedia, transit authority pages) for station lists. Cross-verify segment endpoints with the directions result.
- **Transfers:** Pay close attention to the directions result to correctly identify where line changes occur. A transfer station marks the end of one segment and the start of another.
- **Naming:** Use consistent station naming (e.g., "Changi Airport" not "Changi Airport MRT station" unless the full name is standard).
- **Error Handling:** If a line segment's stations cannot be reliably determined, note the gap in the summary and use the transfer points as placeholders.

## Example Logic (from trajectory)
1. Geocode origin/destination.
2. Find nearest station: Little India (0.5km walk).
3. Get directions: Reveals route: Little India (DT) → Bugis → (transfer) → Tanah Merah → (transfer) → Changi Airport.
4. Fetch data: Get Downtown Line page, extract stations Little India → Rochor → Bugis. Get East–West Line page, extract stations Bugis → ... → Tanah Merah. Get Changi Airport branch info, extract Tanah Merah → Expo → Changi Airport.
5. Compile list, avoiding duplicates at Bugis and Tanah Merah.
6. Write to file.
