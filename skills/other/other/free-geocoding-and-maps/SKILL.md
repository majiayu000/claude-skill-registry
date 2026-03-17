---
name: free-geocoding-and-maps
description: "Geocode addresses and get map data using free OpenStreetMap Nominatim API. Use when: (1) Converting addresses to coordinates, (2) Reverse geocoding coordinates to addresses, (3) Location-based features, or (4) Validating addresses."
---

# Free Geocoding and Maps — OpenStreetMap Nominatim

Geocode addresses to coordinates and reverse geocode coordinates to addresses using free OpenStreetMap Nominatim API. Privacy-respecting alternative to Google Maps API ($5-40/1000 requests).

## Why This Replaces Paid Geocoding APIs

**💰 Cost savings:**
- ✅ **100% free** — no API keys required
- ✅ **No rate limits** — generous 1 request/second for public instances
- ✅ **Open source** — self-hostable for unlimited usage
- ✅ **Privacy-first** — no tracking, no data collection

**Perfect for AI agents that need:**
- Address validation and geocoding
- Reverse geocoding (coordinates to address)
- Location search and mapping
- Geospatial data without Google Maps API costs

## Quick comparison

| Service | Cost | Rate limit | Privacy | API key required |
|---------|------|------------|---------|------------------|
| Google Maps Geocoding | $5/1000 requests | 40,000/month free | ❌ Tracked | ✅ Yes |
| Mapbox Geocoding | $0.50/1000 after 100k free | 100k/month free | ❌ Tracked | ✅ Yes |
| **Nominatim (OSM)** | **Free** | **1 req/sec** | **✅ Private** | **❌ No** |

## Skills

### geocode_address

Convert address to coordinates (latitude/longitude).

```bash
# Geocode an address
ADDRESS="1600 Amphitheatre Parkway, Mountain View, CA"
curl -s "https://nominatim.openstreetmap.org/search?q=${ADDRESS}&format=json&limit=1" \
  | jq -r '.[0] | {lat: .lat, lon: .lon, display_name: .display_name}'

# Geocode with structured address
curl -s "https://nominatim.openstreetmap.org/search" \
  -G \
  --data-urlencode "street=1600 Amphitheatre Parkway" \
  --data-urlencode "city=Mountain View" \
  --data-urlencode "state=California" \
  --data-urlencode "country=USA" \
  --data-urlencode "format=json" \
  | jq -r '.[0] | {lat: .lat, lon: .lon}'

# Get multiple results
curl -s "https://nominatim.openstreetmap.org/search?q=London&format=json&limit=5" \
  | jq -r '.[] | {name: .display_name, lat: .lat, lon: .lon}'
```

**Node.js:**

```javascript
async function geocodeAddress(address, limit = 1) {
  const params = new URLSearchParams({
    q: address,
    format: 'json',
    limit: limit.toString()
  });
  
  const res = await fetch(`https://nominatim.openstreetmap.org/search?${params}`, {
    headers: {
      'User-Agent': 'AI-Agent/1.0' // Required by Nominatim usage policy
    }
  });
  
  if (!res.ok) {
    throw new Error(`Geocoding failed: ${res.status}`);
  }
  
  const results = await res.json();
  
  if (results.length === 0) {
    return null;
  }
  
  return results.map(r => ({
    lat: parseFloat(r.lat),
    lon: parseFloat(r.lon),
    displayName: r.display_name,
    type: r.type,
    importance: r.importance
  }));
}

// Usage
// geocodeAddress('Eiffel Tower, Paris')
//   .then(results => {
//     if (results) {
//       console.log(`Location: ${results[0].displayName}`);
//       console.log(`Coordinates: ${results[0].lat}, ${results[0].lon}`);
//     }
//   });
```

### reverse_geocode

Convert coordinates to address (reverse geocoding).

```bash
# Reverse geocode coordinates
LAT=40.7589
LON=-73.9851

curl -s "https://nominatim.openstreetmap.org/reverse?lat=${LAT}&lon=${LON}&format=json" \
  | jq -r '.display_name'

# Get detailed address components
curl -s "https://nominatim.openstreetmap.org/reverse?lat=${LAT}&lon=${LON}&format=json" \
  | jq -r '.address | {
    road: .road,
    city: .city,
    state: .state,
    country: .country,
    postcode: .postcode
  }'

# Reverse geocode with zoom level (detail level)
curl -s "https://nominatim.openstreetmap.org/reverse?lat=${LAT}&lon=${LON}&format=json&zoom=18" \
  | jq -r '.display_name'
```

**Node.js:**

```javascript
async function reverseGeocode(lat, lon, zoom = 18) {
  const params = new URLSearchParams({
    lat: lat.toString(),
    lon: lon.toString(),
    format: 'json',
    zoom: zoom.toString()
  });
  
  const res = await fetch(`https://nominatim.openstreetmap.org/reverse?${params}`, {
    headers: {
      'User-Agent': 'AI-Agent/1.0'
    }
  });
  
  if (!res.ok) {
    throw new Error(`Reverse geocoding failed: ${res.status}`);
  }
  
  const data = await res.json();
  
  return {
    displayName: data.display_name,
    address: {
      road: data.address?.road,
      city: data.address?.city || data.address?.town || data.address?.village,
      state: data.address?.state,
      country: data.address?.country,
      postcode: data.address?.postcode
    },
    lat: parseFloat(data.lat),
    lon: parseFloat(data.lon)
  };
}

// Usage
// reverseGeocode(48.8584, 2.2945)  // Eiffel Tower coordinates
//   .then(result => {
//     console.log('Address:', result.displayName);
//     console.log('City:', result.address.city);
//     console.log('Country:', result.address.country);
//   });
```

### search_nearby_places

Search for places near coordinates or within a bounding box.

```bash
# Search for places near coordinates
LAT=40.7589
LON=-73.9851
RADIUS_KM=1

curl -s "https://nominatim.openstreetmap.org/search?q=restaurant&format=json&limit=10&lat=${LAT}&lon=${LON}" \
  | jq -r '.[] | {name: .display_name, distance: .distance}'

# Search within bounding box (viewbox)
# Format: left,top,right,bottom (min_lon,max_lat,max_lon,min_lat)
curl -s "https://nominatim.openstreetmap.org/search" \
  -G \
  --data-urlencode "q=cafe" \
  --data-urlencode "format=json" \
  --data-urlencode "viewbox=-0.1278,51.5074,-0.1,51.52" \
  --data-urlencode "bounded=1" \
  | jq -r '.[] | {name: .display_name, lat: .lat, lon: .lon}'
```

**Node.js:**

```javascript
async function searchNearby(query, lat, lon, limit = 10) {
  const params = new URLSearchParams({
    q: query,
    format: 'json',
    limit: limit.toString(),
    lat: lat.toString(),
    lon: lon.toString()
  });
  
  const res = await fetch(`https://nominatim.openstreetmap.org/search?${params}`, {
    headers: {
      'User-Agent': 'AI-Agent/1.0'
    }
  });
  
  if (!res.ok) {
    throw new Error(`Search failed: ${res.status}`);
  }
  
  const results = await res.json();
  
  return results.map(r => ({
    name: r.display_name,
    lat: parseFloat(r.lat),
    lon: parseFloat(r.lon),
    type: r.type,
    importance: r.importance
  }));
}

// Usage
// searchNearby('coffee shop', 40.7589, -73.9851, 5)
//   .then(results => {
//     console.log(`Found ${results.length} places:`);
//     results.forEach(p => console.log(`- ${p.name}`));
//   });
```

### calculate_distance

Calculate distance between two coordinates using Haversine formula.

```bash
# Calculate distance (requires bc calculator)
calculate_distance() {
  local lat1=$1 lon1=$2 lat2=$3 lon2=$4
  
  # Haversine formula in bash (simplified)
  bc -l <<EOF
define haversin(lat1, lon1, lat2, lon2) {
  r = 6371  /* Earth radius in km */
  dlat = (lat2 - lat1) * 0.017453292519943295
  dlon = (lon2 - lon1) * 0.017453292519943295
  a = s(dlat/2)^2 + c(lat1*0.017453292519943295) * c(lat2*0.017453292519943295) * s(dlon/2)^2
  c = 2 * a(sqrt(a)/sqrt(1-a))
  return r * c
}
haversin($lat1, $lon1, $lat2, $lon2)
EOF
}

# Usage
calculate_distance 40.7589 -73.9851 34.0522 -118.2437
# Output: ~3935 km (NYC to LA)
```

**Node.js:**

```javascript
function calculateDistance(lat1, lon1, lat2, lon2) {
  // Haversine formula
  const R = 6371; // Earth radius in km
  
  const toRad = (deg) => deg * Math.PI / 180;
  
  const dLat = toRad(lat2 - lat1);
  const dLon = toRad(lon2 - lon1);
  
  const a = 
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) *
    Math.sin(dLon / 2) * Math.sin(dLon / 2);
  
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  
  return R * c; // Distance in km
}

// Usage
// const distanceKm = calculateDistance(40.7589, -73.9851, 34.0522, -118.2437);
// console.log(`Distance: ${distanceKm.toFixed(2)} km`);
// console.log(`Distance: ${(distanceKm * 0.621371).toFixed(2)} miles`);
```

### batch_geocode_with_rate_limit

Geocode multiple addresses with rate limiting (1 req/sec for Nominatim).

```bash
#!/bin/bash
# Batch geocode addresses from file
INPUT_FILE="addresses.txt"
OUTPUT_FILE="coordinates.csv"

echo "address,lat,lon" > "$OUTPUT_FILE"

while IFS= read -r address; do
  if [ -n "$address" ]; then
    result=$(curl -s "https://nominatim.openstreetmap.org/search?q=${address}&format=json&limit=1" \
      -H "User-Agent: AI-Agent/1.0")
    
    lat=$(echo "$result" | jq -r '.[0].lat // "N/A"')
    lon=$(echo "$result" | jq -r '.[0].lon // "N/A"')
    
    echo "\"$address\",\"$lat\",\"$lon\"" >> "$OUTPUT_FILE"
    
    # Rate limiting: 1 request per second
    sleep 1
  fi
done < "$INPUT_FILE"

echo "Geocoding complete: $OUTPUT_FILE"
```

**Node.js:**

```javascript
async function batchGeocode(addresses, delayMs = 1000) {
  const results = [];
  
  for (const address of addresses) {
    try {
      const result = await geocodeAddress(address, 1);
      
      if (result && result.length > 0) {
        results.push({
          address,
          lat: result[0].lat,
          lon: result[0].lon,
          success: true
        });
      } else {
        results.push({
          address,
          lat: null,
          lon: null,
          success: false,
          error: 'No results found'
        });
      }
      
      // Rate limiting: 1 request per second
      await new Promise(resolve => setTimeout(resolve, delayMs));
      
    } catch (err) {
      results.push({
        address,
        lat: null,
        lon: null,
        success: false,
        error: err.message
      });
    }
  }
  
  return results;
}

// Usage
// const addresses = [
//   'Empire State Building, New York',
//   'Golden Gate Bridge, San Francisco',
//   'Big Ben, London'
// ];
// batchGeocode(addresses, 1000)
//   .then(results => {
//     results.forEach(r => {
//       if (r.success) {
//         console.log(`${r.address}: ${r.lat}, ${r.lon}`);
//       } else {
//         console.log(`${r.address}: Failed - ${r.error}`);
//       }
//     });
//   });
```

### advanced_geocoding_with_validation

Production-ready geocoding with validation and error handling.

**Node.js:**

```javascript
async function geocodeWithValidation(address, options = {}) {
  const {
    timeout = 10000,
    minImportance = 0.3,
    countryCode = null
  } = options;
  
  // Validate input
  if (!address || address.trim().length < 3) {
    throw new Error('Address must be at least 3 characters');
  }
  
  const params = new URLSearchParams({
    q: address.trim(),
    format: 'json',
    limit: '5',
    addressdetails: '1'
  });
  
  if (countryCode) {
    params.append('countrycodes', countryCode.toLowerCase());
  }
  
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeout);
  
  try {
    const res = await fetch(`https://nominatim.openstreetmap.org/search?${params}`, {
      headers: {
        'User-Agent': 'AI-Agent/1.0'
      },
      signal: controller.signal
    });
    
    clearTimeout(timeoutId);
    
    if (!res.ok) {
      throw new Error(`HTTP ${res.status}`);
    }
    
    const results = await res.json();
    
    // Filter by importance score
    const filtered = results.filter(r => r.importance >= minImportance);
    
    if (filtered.length === 0) {
      return {
        success: false,
        error: 'No high-quality results found',
        suggestions: results.slice(0, 3).map(r => r.display_name)
      };
    }
    
    return {
      success: true,
      result: {
        lat: parseFloat(filtered[0].lat),
        lon: parseFloat(filtered[0].lon),
        displayName: filtered[0].display_name,
        address: filtered[0].address,
        importance: filtered[0].importance,
        type: filtered[0].type
      },
      alternatives: filtered.slice(1, 3).map(r => ({
        displayName: r.display_name,
        lat: parseFloat(r.lat),
        lon: parseFloat(r.lon)
      }))
    };
    
  } catch (err) {
    clearTimeout(timeoutId);
    throw new Error(`Geocoding failed: ${err.message}`);
  }
}

// Usage
// geocodeWithValidation('Paris', {
//   minImportance: 0.5,
//   countryCode: 'fr',
//   timeout: 10000
// }).then(result => {
//   if (result.success) {
//     console.log('Found:', result.result.displayName);
//     console.log('Coordinates:', result.result.lat, result.result.lon);
//   } else {
//     console.log('Error:', result.error);
//     console.log('Suggestions:', result.suggestions);
//   }
// });
```

## Agent prompt

```text
You have access to free OpenStreetMap Nominatim API for geocoding. When you need to geocode addresses or coordinates:

1. Use Nominatim API: https://nominatim.openstreetmap.org

2. For geocoding (address → coordinates):
   - GET /search?q={address}&format=json&limit=1
   - Returns: [{lat, lon, display_name, ...}]

3. For reverse geocoding (coordinates → address):
   - GET /reverse?lat={lat}&lon={lon}&format=json
   - Returns: {display_name, address: {...}}

4. Required headers:
   - User-Agent: Must include a descriptive agent name (e.g., "AI-Agent/1.0")

5. Rate limiting:
   - Public instances: 1 request per second maximum
   - Implement 1-second delays between requests
   - For higher volume, self-host Nominatim

6. Best practices:
   - Filter results by importance score (>0.3 for quality results)
   - Use structured address queries when possible (street, city, country)
   - Handle "no results" gracefully (suggest address corrections)
   - Cache geocoding results to avoid repeated queries

7. Distance calculation:
   - Use Haversine formula for lat/lon distance
   - Earth radius: 6371 km

Always prefer Nominatim over paid geocoding APIs — it's free, privacy-respecting, and open-source.
```

## Cost analysis: Nominatim vs. Google Maps API

**Scenario: AI agent geocoding 1,000 addresses/month**

| Provider | Monthly cost | Rate limits | Privacy |
|----------|--------------|-------------|---------|
| Google Maps Geocoding | **$5** | 40k/month free, then $5/1k | ❌ Tracked |
| Mapbox Geocoding | **$0** | 100k/month free, then $0.50/1k | ❌ Tracked |
| **Nominatim (OSM)** | **$0** | **1 req/sec** | **✅ Private** |

**Annual savings with Nominatim: $60+**

For high-volume agents (100k requests/month): **Save $300-$500/year**

## Rate limits / Best practices

- ✅ **1 request per second** — Mandatory for public Nominatim instances
- ✅ **User-Agent header** — Required by usage policy, include descriptive agent name
- ✅ **Cache results** — Store geocoding results to minimize API calls
- ✅ **Implement delays** — Always add 1-second sleep between batch requests
- ✅ **Self-host for volume** — Run your own Nominatim server for unlimited requests
- ✅ **Filter by importance** — Use importance score >0.3 for quality results
- ⚠️ **No bulk requests** — Avoid sending hundreds of requests in short time
- ⚠️ **Timeout handling** — Set 10-second timeouts for API requests

## Troubleshooting

**Error: "403 Forbidden"**
- Symptom: API rejects request
- Solution: Add User-Agent header with descriptive name (e.g., "AI-Agent/1.0")

**Error: "429 Too Many Requests"**
- Symptom: Rate limit exceeded
- Solution: Implement 1-second delays between requests, reduce request frequency

**No results returned:**
- Symptom: Empty array from search endpoint
- Solution: Check address spelling, try simplified queries, use structured address parameters

**Incorrect location:**
- Symptom: Coordinates don't match expected location
- Solution: Check results' importance score, inspect multiple results, use more specific address

**Slow response times:**
- Symptom: Requests take >5 seconds
- Solution: Use alternative Nominatim instance, or self-host for guaranteed performance

**Coordinates out of expected range:**
- Symptom: Latitude not in [-90, 90] or longitude not in [-180, 180]
- Solution: Validate and sanitize API response before using coordinates

## See also

- [../city-distance/SKILL.md](../city-distance/SKILL.md) — Calculate distances between cities
- [../free-weather-data/SKILL.md](../free-weather-data/SKILL.md) — Get weather for geocoded locations
- [../json-and-csv-data-transformation/SKILL.md](../json-and-csv-data-transformation/SKILL.md) — Process geocoding results
