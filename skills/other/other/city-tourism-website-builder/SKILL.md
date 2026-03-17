---
name: city-tourism-website-builder
description: Research and create modern, animated tourism websites for cities with historical facts, places to visit, and colorful designs.
---

# City Tourism Website Builder

Create stunning, modern tourism websites for any city with comprehensive research, historical facts, and beautiful animations.

## Overview

This skill enables the creation of professional city tourism websites featuring:
- Deep research on city history, facts, and tourist attractions
- Modern, colorful designs with white backgrounds
- Smooth animations and hover effects
- Responsive layouts for all devices
- Interactive OpenStreetMap centered on the city
- Optional map snapshot download as PNG
- IPFS hosting for permanent availability

## Workflow

### 1. Research Phase

Gather comprehensive information about the city:

```bash
# Search for city information
websearch query="CITY_NAME history facts tourist places visiting sites"
websearch query="CITY_NAME famous temples monuments landmarks"
websearch query="CITY_NAME best time to visit how to reach"
```

**Key Information to Collect:**
- Historical origins and etymology
- Famous personalities associated
- Religious/spiritual significance
- Major tourist attractions
- Geography and climate
- Cultural heritage
- Quick facts (population, distance from major cities, etc.)

### 2. Design Principles

**Color Scheme:**
- White background for clean, modern look
- Vibrant gradient accents (coral, teal, yellow, mint)
- Dark text for readability
- Colorful cards with hover effects

**Animations:**
- Floating background shapes
- Fade-in on scroll
- Card hover lift effects
- Smooth scroll navigation
- Gradient text animations
- Pulse effects on badges

### 3. Website Structure

**Sections:**
1. **Hero Header**
   - Large gradient text city name
   - Tagline
   - Animated badge
   - Scroll indicator

2. **History Section**
   - Historical facts in card grid
   - Interactive timeline
   - Origin stories

3. **Places to Visit**
   - Categorized cards (Religious, Nature, Adventure, Historic)
   - Icons and emojis for visual appeal
   - Distance information

4. **Quick Facts**
   - Animated number counters
   - Grid layout
   - Key statistics

5. **Interactive City Map**
   - OpenStreetMap map centered on city coordinates
   - Marker in city center with popup details
   - "Download Map PNG" action

6. **Visual Gallery**
   - Colorful placeholder grid
   - Hover zoom effects

7. **Footer**
   - Navigation links
   - Copyright

### 4. Technical Implementation

**CSS Features:**
```css
/* Animated gradient text */
background: linear-gradient(135deg, #FF6B6B, #4ECDC4);
-webkit-background-clip: text;
-webkit-text-fill-color: transparent;

/* Floating shapes */
animation: float 20s infinite ease-in-out;

/* Card hover effects */
transform: translateY(-10px);
box-shadow: 0 20px 60px rgba(0,0,0,0.15);

/* Scroll-triggered animations */
IntersectionObserver for fade-in effects
```

**JavaScript Features:**
- Smooth scroll navigation
- Navbar hide/show on scroll
- Intersection Observer for reveal animations
- Mobile-responsive menu
- Interactive OpenStreetMap (Leaflet)
- City-center marker and popup
- Download map image as PNG (with fallback)

### 4.1 OpenStreetMap integration (required)

Use free OpenStreetMap tiles through Leaflet.

```html
<!-- In <head> -->
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>

<!-- In body -->
<section id="map" aria-label="City map section">
   <h2>Explore the City Map</h2>
   <div id="cityMap" style="height: 420px; border-radius: 16px;"></div>
   <button id="downloadMapBtn" type="button" aria-label="Download Map PNG">Download Map PNG</button>
</section>
```

```javascript
// Example city center (replace per city)
const city = {
   name: 'Kathua',
   lat: 32.3693,
   lon: 75.5254,
   zoom: 12
};

const map = L.map('cityMap').setView([city.lat, city.lon], city.zoom);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
   maxZoom: 19,
   attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

L.marker([city.lat, city.lon])
   .addTo(map)
   .bindPopup(`${city.name} City Center`)
   .openPopup();
```

### 4.2 Download map as PNG (if possible)

Client-side PNG export from interactive tiles can fail in some browsers due to canvas/CORS restrictions.

**Reliable fallback (recommended):** download a static PNG from the free OSM static map endpoint.

```javascript
document.getElementById('downloadMapBtn').addEventListener('click', () => {
   const url = `https://staticmap.openstreetmap.de/staticmap.php?center=${city.lat},${city.lon}&zoom=${city.zoom}&size=1280x720&markers=${city.lat},${city.lon},red-pushpin`;
   const link = document.createElement('a');
   link.href = url;
   link.download = `${city.name.toLowerCase().replace(/\s+/g, '-')}-map.png`;
   link.click();
});
```

**CLI option (same free endpoint):**

```bash
CITY_LAT="32.3693"
CITY_LON="75.5254"
CITY_NAME="kathua"

curl -fsS "https://staticmap.openstreetmap.de/staticmap.php?center=${CITY_LAT},${CITY_LON}&zoom=12&size=1280x720&markers=${CITY_LAT},${CITY_LON},red-pushpin" \
   -o "${CITY_NAME}-map.png"
```

### 5. Example Implementation

**File Structure:**
```
city-website.html
├── Animated background shapes
├── Fixed navigation with blur effect
├── Hero section with gradient text
├── History cards with top accent line
├── Timeline with alternating layout
├── Places grid with category badges
├── Facts section with large numbers
├── Interactive OpenStreetMap section (city-centered)
├── Download Map PNG button
├── Gallery grid with color blocks
└── Dark footer
```

**Key CSS Variables:**
```css
:root {
  --primary: #FF6B6B;      /* Coral */
  --secondary: #4ECDC4;    /* Teal */
  --accent: #FFE66D;       /* Yellow */
  --purple: #A8E6CF;       /* Mint */
  --dark: #2C3E50;         /* Dark text */
  --light: #F7F9FC;        /* Light bg */
}
```

### 6. Content Guidelines

**History Section:**
- 4 key historical cards
- 3-timeline items
- Focus on origin stories
- Include royal/religious heritage

**Places Section:**
- 6-8 major attractions
- Categorize: Religious, Nature, Adventure, Historic
- Include distances from city center
- Add emojis for visual appeal

**Facts Section:**
- 6 key statistics
- Large numbers with gradient
- Mix of distances, heights, years

### 7. Upload & Deployment

```bash
# Upload to IPFS via Originless
curl -fsS -X POST -F "file=@city-website.html" https://filedrop.besoeasy.com/upload

# Response includes:
# - IPFS URL: https://dweb.link/ipfs/{CID}
# - CID for permanent access
```

## Example Output

**Kathua Tourism Website:**
- URL: https://dweb.link/ipfs/QmRBGRAKvuaVNqNoyvokx2S4H7vWMiHHKsb5EMBzNEkHMB
- Features: 2000+ years of history, 8 tourist places, animated timeline
- Theme: Colorful gradients on white

## Best Practices

1. **Research Thoroughly**
   - Use multiple sources
   - Verify historical facts
   - Include local legends

2. **Design for All Devices**
   - Mobile-first approach
   - Responsive grids
   - Touch-friendly interactions
   - Map container sized for mobile and desktop

3. **Performance**
   - Minimize external dependencies
   - Use CSS animations (GPU accelerated)
   - Lazy load below-fold content

4. **Accessibility**
   - Semantic HTML structure
   - ARIA labels where needed
   - Keyboard navigation support
   - Map controls remain keyboard reachable

5. **Content Quality**
   - Engaging copy
   - Accurate information
   - Local context and flavor

6. **Map Quality**
   - Keep city marker exactly at city center coordinates
   - Include attribution for OpenStreetMap contributors
   - Prefer static-map fallback for guaranteed PNG download

## Variations

**Theme Options:**
- **Colorful Modern** (default): Gradients on white
- **Elegant Dark**: Dark mode with gold accents
- **Minimal**: Clean monochrome
- **Cultural**: Colors reflecting local culture

**Layout Options:**
- **Standard**: Header → History → Places → Facts → Gallery
- **Parallax**: Scroll-triggered depth effects
- **Single Page**: All content in vertical scroll
- **Multi-page**: Separate pages for sections

## Resources

**Color Palettes:**
- https://coolors.co/ for gradient generation
- Vibrant cities: coral (#FF6B6B), teal (#4ECDC4), yellow (#FFE66D), mint (#A8E6CF)

**Icons:**
- Emojis for universal recognition
- Lucide icons (lightweight)
- Custom SVG for specific landmarks

**Hosting:**
- Originless/IPFS for permanent storage
- GitHub Pages for traditional hosting
- Netlify for continuous deployment

---

This skill combines research, design, and technical implementation to create professional city tourism websites that showcase the best of any destination.