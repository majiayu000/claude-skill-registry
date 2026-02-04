---
name: location-geocoder
description: When the user provides location names, addresses, or landmarks that need to be converted to precise geographic coordinates. This skill uses mapping APIs to geocode locations, returning latitude/longitude coordinates, formatted addresses, and place IDs for subsequent spatial analysis or route planning tasks.
---
# Skill: Location Geocoder

## Purpose
Convert user-provided location descriptions (names, addresses, landmarks) into precise geographic coordinates and structured location data using mapping APIs. This provides the foundational location data needed for subsequent tasks like route planning, distance calculations, or spatial analysis.

## Core Workflow

### 1. Input Processing
- **Accept**: Location descriptions in natural language (e.g., "Singapore Mobility Gallery", "Changi Airport MRT station, Singapore")
- **Normalize**: Clean and standardize input for API consumption
- **Validate**: Ensure location descriptions are complete enough for geocoding

### 2. Geocoding Execution
- **Primary Tool**: Use `google_map-maps_geocode` function
- **Input Format**: Provide address/location string in natural language
- **Output Capture**: Extract and structure:
  - `location.lat`: Latitude coordinate
  - `location.lng`: Longitude coordinate  
  - `formatted_address`: Standardized complete address
  - `place_id`: Unique identifier for the location

### 3. Output Delivery
- **Structured Data**: Present coordinates and address in clear format
- **Error Handling**: Provide helpful feedback if geocoding fails
- **Next Steps**: Suggest how the geocoded data can be used (e.g., "Now I have the coordinates, I can calculate routes between these points")

## Key Principles

### Accuracy First
- Always verify the returned address matches the intended location
- Use specific location descriptors when available (include city/country)
- Cross-reference with known landmarks if coordinates seem questionable

### Efficiency
- Geocode multiple locations in parallel when possible
- Cache frequently requested locations to avoid redundant API calls
- Batch process when user provides multiple location inputs

### Context Awareness
- Consider the user's broader task (route planning, distance calculation, etc.)
- Provide geocoded data in formats useful for next steps
- Include place_id for API interoperability with other mapping functions

## Common Use Cases

### Route Planning (as seen in trajectory)
1. Geocode origin: "Singapore Mobility Gallery, Singapore"
2. Geocode destination: "Changi Airport MRT station, Singapore"
3. Use coordinates for subsequent route calculation

### Distance Calculations
- Geocode multiple points for distance matrix analysis
- Provide precise coordinates for accurate distance measurements

### Location Validation
- Confirm address existence and format
- Resolve ambiguous location names to specific coordinates

## Error Handling
- **No Results**: Suggest alternative phrasing or more specific location details
- **Multiple Results**: Ask user to clarify which specific location they mean
- **API Errors**: Retry with modified parameters or suggest manual coordinate input

## Integration Notes
This skill typically serves as the first step in location-based workflows. The output (coordinates, place_id) should be preserved for use with:
- Route planning functions
- Distance matrix calculations
- Nearby place searches
- Spatial analysis tools
