---
name: check-spots
description: Validate spots.json for common issues including missing fields, invalid URLs, duplicate entries, and data consistency problems
---

# Check Spots Validation Skill

Validate the `src/main/resources/spots.json` file for common issues.

## Instructions

Read the spots.json file and perform the following validations. Report all issues found, grouped by category.

### 1. Structure Validation
- Verify valid JSON syntax
- Ensure root is an array
- Each spot must be an object

### 2. Required Fields Check
For each spot, verify these fields exist and are non-empty strings:
- `name`
- `country`
- `locationUrl`

### 3. Windguru URL Validation
Each spot must have either:
- `windguruUrl` with valid windguru.cz URL (format: `https://www.windguru.cz/<station_id>`)
- OR both `windguruUrl` as empty string and `windguruFallbackUrl` as valid windguru.cz URL

### 4. Optional URL Format Validation
These fields must be either empty strings or valid URLs:
- `windfinderUrl` - should match `https://www.windfinder.com/*`
- `icmUrl` - should match `https://www.meteo.pl/*`
- `webcamUrl` - any valid URL
- `locationUrl` - should be a Google Maps URL (goo.gl, maps.app.goo.gl, or google.com/maps)

### 5. SpotInfo Validation (English)
Each spot must have `spotInfo` object with:
- `type` (non-empty string)
- `bestWind` (string with valid cardinal directions: N, NE, E, SE, S, SW, W, NW)
- `waterTemp` (format: `X-Y°C` or `X°C`)
- `experience` (non-empty string)
- `launch` (non-empty string)
- `hazards` (string, can be empty)
- `season` (non-empty string)
- `description` (non-empty string)
- `llmComment` (optional)

### 6. SpotInfoPL Validation (Polish)
Each spot must have `spotInfoPL` object with same fields as spotInfo (translations).

### 7. Duplicate Detection
Check for:
- Duplicate spot names
- Duplicate windguruUrl values (non-empty)
- Duplicate windguruFallbackUrl values

### 8. Country Name Consistency
Report any country names that appear only once (potential typos).

### 9. Cardinal Direction Validation
Validate `bestWind` contains only valid directions: N, NE, E, SE, S, SW, W, NW
Report any invalid direction values.

### 10. Temperature Format Validation
Validate `waterTemp` matches pattern like:
- `10-18°C` (range)
- `15°C` (single value)
Report any malformed temperature values.

## Output Format

Report findings in this format:

```
## Spots.json Validation Report

### Summary
- Total spots: X
- Issues found: Y
- Spots with issues: Z

### Critical Issues (must fix)
- [Spot Name] Missing required field: fieldName
- [Spot Name] Invalid Windguru URL: url

### Warnings (should fix)
- [Spot Name] Empty optional field: fieldName
- Potential duplicate country: "Countri" (appears 1 time, did you mean "Country"?)

### Info
- Countries found: A, B, C
- Spots per country: A (X), B (Y), C (Z)
```

## Running the Validation

1. Read `src/main/resources/spots.json`
2. Parse and validate each spot
3. Collect all issues
4. Generate the report
5. Suggest fixes for critical issues
