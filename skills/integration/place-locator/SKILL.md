---
name: place-locator
description: When the user needs to find specific places, landmarks, or points of interest based on descriptive names, this skill searches for place information including exact addresses, coordinates, and place details. It's particularly useful for tourist attractions, buildings, or specific venues mentioned in documents. Triggers include queries for 'find the location of', 'where is', or when processing lists of places from documents.
---
# Instructions

## Purpose
This skill locates specific places, landmarks, or points of interest mentioned by the user or found in documents. It retrieves precise addresses, geographic coordinates (latitude/longitude), and other place details (like Place ID, rating, types) to enable downstream tasks like route planning, mapping, or information compilation.

## Core Workflow

1.  **Identify Target Places:** Extract the names of places to locate from the user's request. This often involves reading a source document (like `recommendation.md`) to get a list.
2.  **Geocode the Starting Point (if needed):** If the user provides a starting location (e.g., "I am at the University of Pennsylvania Bookstore"), use `maps_geocode` to get its coordinates. This establishes a search center.
3.  **Search for Each Place:** For each place name, use `maps_search_places`. Provide a specific query combining the place name and broader location context (e.g., "ENIAC Penn School of Engineering University of Pennsylvania Philadelphia"). Use the starting point's coordinates and a reasonable radius (e.g., 2000 meters) to constrain the search.
4.  **Handle Ambiguity & Refinement:** If a search returns multiple results or the primary result seems incorrect (e.g., searching for "ENIAC" returns general engineering buildings), you may need to:
    *   Analyze the results to pick the most relevant one based on name and type.
    *   Perform a more specific follow-up search or geocode using a more precise address derived from the context (e.g., "Moore Building, 200 S 33rd St" for ENIAC).
5.  **Compile Location Data:** Create a structured list or table containing for each place: its canonical name, formatted address, latitude, longitude, and place_id. This data is essential for subsequent steps like calculating distances or generating directions.

## Key Considerations
*   **Precision over Recall:** It's more important to find the *correct, specific* location (e.g., the exact building housing the ENIAC exhibit) than to get many general results.
*   **Context is Key:** Use all available context from the conversation and any read documents to formulate precise search queries.
*   **Output for Downstream Use:** The skill's primary output is a clean dataset of coordinates and addresses. Format this data clearly so it can be easily passed to skills like `maps_distance_matrix` or `maps_directions`.

## Common Triggers
*   User asks: "Where is [Place Name]?", "Find the location of...", "I need the address for..."
*   User provides a list of places from a document and needs them located.
*   A task requires geographic coordinates as a prerequisite (e.g., "plan a walking route between these attractions").
