---
name: cartography-gis
description: Map design, spatial analysis, and Geographic Information Systems. Covers map projections and their distortion trade-offs, coordinate systems, thematic mapping techniques (choropleth, proportional symbol, dot density, isoline), remote sensing and satellite imagery, GIS data models (vector and raster), spatial analysis operations (overlay, buffer, interpolation, network analysis), and cartographic design principles. Use when creating maps, analyzing spatial data, selecting projections, interpreting satellite imagery, or reasoning about spatial relationships in any domain.
type: skill
category: geography
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-11
first_path: examples/skills/geography/cartography-gis/SKILL.md
superseded_by: null
---
# Cartography & GIS

Cartography is the science and art of map-making. Geographic Information Systems (GIS) extend cartography into a computational framework for storing, analyzing, and visualizing spatial data. Together they provide the tools for every other branch of geography to represent and reason about spatial patterns.

**Agent affinity:** tobler (cartographic projection, spatial relationships, first law of geography), reclus (physical features), massey (social data mapping)

**Concept IDs:** geo-map-projections, geo-coordinates-scale, geo-thematic-mapping, geo-gis-remote-sensing

## Part I -- Map Projections

### The Fundamental Problem

A sphere cannot be flattened onto a plane without distortion. Every map projection preserves some properties at the expense of others. The four properties that can be distorted are:

| Property | Definition | Projection type that preserves it |
|---|---|---|
| **Area** | Relative sizes of regions | Equal-area (equivalent) projections |
| **Shape** | Local angles and small shapes | Conformal projections |
| **Distance** | True distances from one or two points | Equidistant projections |
| **Direction** | True bearings from a central point | Azimuthal projections |

No projection preserves all four simultaneously. Choosing a projection means choosing which distortion is acceptable for the map's purpose.

### Major Projection Families

**Cylindrical projections** wrap a cylinder around the globe:
- *Mercator* (1569): Conformal. Preserves angles and shapes locally. Extreme area distortion at high latitudes (Greenland appears larger than Africa). Used for navigation because rhumb lines are straight lines.
- *Transverse Mercator:* Conformal, centered on a meridian. Basis for UTM (Universal Transverse Mercator) coordinate system. Used for large-scale topographic maps.
- *Peters/Gall-Peters:* Equal-area. Corrects Mercator's area bias but severely distorts shapes at high and low latitudes. Politically motivated as a counter to Mercator's Eurocentric visual emphasis.

**Conic projections** project onto a cone tangent or secant to the globe:
- *Albers equal-area conic:* Preserves area. Standard for thematic maps of mid-latitude countries (US, Europe).
- *Lambert conformal conic:* Preserves shape. Used for aeronautical charts and weather maps.

**Azimuthal projections** project onto a plane tangent to the globe:
- *Stereographic:* Conformal. Used for polar regions.
- *Azimuthal equidistant:* True distances from center point. Used for radio propagation maps and UN emblem.

**Compromise projections** minimize all distortions without eliminating any:
- *Robinson* (1963): Neither conformal nor equal-area. Visually balanced for world maps.
- *Winkel Tripel:* Adopted by National Geographic in 1998 for world maps. Minimizes combined area, distance, and direction distortion.

### Tobler's First Law and Projection Choice

Waldo Tobler's first law of geography -- "everything is related to everything else, but near things are more related than distant things" -- has direct implications for projection choice. Maps must preserve the spatial relationships that matter for the analysis. A choropleth map of population density must use an equal-area projection (distorted areas produce distorted densities). A navigation chart must use a conformal projection (distorted angles produce wrong headings).

## Part II -- Coordinate Systems

### Geographic Coordinates

**Latitude** measures angular distance north or south of the equator (0 to 90 degrees N/S). **Longitude** measures angular distance east or west of the Prime Meridian (0 to 180 degrees E/W). Together they define a unique position on the globe.

**Datum:** A mathematical model of Earth's shape. WGS 84 (World Geodetic System 1984) is the standard for GPS and most global datasets. NAD 83 (North American Datum 1983) is the standard for US surveys. Coordinates in different datums can differ by tens of meters.

### Projected Coordinates

**UTM (Universal Transverse Mercator):** Divides Earth into 60 zones of 6 degrees longitude each. Within each zone, positions are given as easting (meters from a false origin) and northing (meters from the equator). Minimizes distortion within each zone. Standard for large-scale mapping and military grids.

**State Plane Coordinate System (SPCS):** US-specific system with zones designed to keep distortion under 1:10,000. Uses Lambert conformal conic for east-west-oriented states and transverse Mercator for north-south-oriented states.

### Scale

Map scale = map distance / ground distance. Expressed as a representative fraction (1:24,000), a verbal statement ("1 inch = 2,000 feet"), or a graphic bar. Large scale (1:24,000) shows small areas in detail; small scale (1:1,000,000) shows large areas with less detail. The terminology is counterintuitive: "large scale" means the fraction 1/24,000 is larger than 1/1,000,000.

## Part III -- Thematic Mapping

Thematic maps display the spatial distribution of a specific attribute or phenomenon.

### Thematic Map Types

| Type | Data type | Best for | Pitfall |
|---|---|---|---|
| **Choropleth** | Ratio/rate data by area | Population density, income per capita, election results | Must normalize by area or population; raw counts on choropleths are misleading |
| **Proportional symbol** | Count or magnitude at points | City populations, earthquake magnitudes, facility production | Overlapping symbols in dense areas; perception of circle area is non-linear |
| **Dot density** | Counts distributed across areas | Crop production, livestock, population distribution | Dot placement within polygons is arbitrary; choose dot value carefully |
| **Isoline (contour)** | Continuous phenomena | Elevation, temperature, atmospheric pressure, rainfall | Assumes smooth spatial variation; breaks down with abrupt boundaries |
| **Flow** | Movement between origins and destinations | Migration, trade, commuting | Line width must be proportional to flow volume; avoid spaghetti |
| **Cartogram** | Any variable, distorting area | Election results, GDP comparison | Distorted shapes can be disorienting; always provide reference map |

### Design Principles

**Visual hierarchy:** The most important information should be most visually prominent. Background (base map) recedes; foreground (thematic data) advances.

**Color:** Use sequential palettes (light to dark) for ordered data, diverging palettes (two hues from a neutral midpoint) for data with a meaningful center, and qualitative palettes (distinct hues) for categorical data. Avoid rainbow color schemes -- they create false boundaries and are inaccessible to colorblind readers.

**Classification:** How continuous data is binned into classes affects the map's message. Equal interval, quantile, natural breaks (Jenks), and standard deviation methods produce different visual patterns from the same data. Report the method.

## Part IV -- Remote Sensing

Remote sensing acquires information about Earth's surface from a distance, typically via satellite or aircraft sensors.

**Electromagnetic spectrum:** Sensors detect energy in visible (0.4--0.7 micrometers), near-infrared (0.7--1.3 micrometers), shortwave infrared (1.3--3 micrometers), thermal infrared (3--14 micrometers), and microwave (1 mm--1 m) wavelengths.

**Key satellite platforms:**
- *Landsat* (1972--present): 30m resolution, multispectral. Longest continuous Earth observation record. Free and open data.
- *Sentinel-2* (2015--present): 10--60m resolution, 13 bands. Part of EU Copernicus program. Free and open.
- *MODIS* (1999--present): 250m--1km resolution, daily global coverage. Used for vegetation, fire, ocean color, atmospheric monitoring.

**Spectral indices:**
- *NDVI* (Normalized Difference Vegetation Index): (NIR - Red) / (NIR + Red). Measures vegetation health and density. Values range from -1 to +1; healthy vegetation >0.3.
- *NDWI* (Normalized Difference Water Index): Identifies water bodies and soil moisture.
- *NDBI* (Normalized Difference Built-up Index): Identifies urban/built-up areas.

## Part V -- GIS

### Data Models

**Vector model:** Represents features as points, lines, and polygons with associated attribute tables. Points for wells, cities; lines for rivers, roads; polygons for countries, land parcels. Precise boundaries. Efficient for discrete features.

**Raster model:** Represents space as a grid of cells (pixels), each with a value. Elevation, temperature, satellite imagery, land cover classification. Efficient for continuous phenomena. Resolution = cell size.

### Spatial Analysis Operations

| Operation | Description | Example |
|---|---|---|
| **Overlay** | Combine two or more layers to identify spatial relationships | Find areas that are both within a flood zone AND zoned residential |
| **Buffer** | Create a zone of specified distance around features | Identify all parcels within 500m of a highway |
| **Interpolation** | Estimate values at unsampled locations from known points | Create a temperature surface from weather station readings |
| **Network analysis** | Optimize routes, find shortest paths, define service areas | Find the fastest ambulance route to a hospital |
| **Spatial join** | Attach attributes from one layer to another based on location | Assign census tract demographics to school point locations |
| **Reclassification** | Reassign raster cell values to new categories | Combine slope, aspect, and soil type into a landslide risk index |

### Spatial Statistics

- **Spatial autocorrelation (Moran's I):** Tests whether nearby values are more similar (positive autocorrelation) or more different (negative) than expected by chance. Foundational test -- most geographic data is positively autocorrelated (Tobler's first law).
- **Hot spot analysis (Getis-Ord Gi*):** Identifies statistically significant clusters of high and low values.
- **Kernel density estimation:** Converts point data to a continuous density surface.
- **Geographically weighted regression (GWR):** Allows regression coefficients to vary spatially, revealing how relationships change across the study area.

## Cross-References

- **tobler agent:** Primary agent for cartography and GIS questions. Projection selection, spatial analysis design, and cartographic critique.
- **reclus agent:** Physical feature mapping and Earth observation interpretation.
- **massey agent:** Social data mapping, power-geometry of spatial representation, and critical cartography.
- **carson agent:** Environmental data visualization and communication of geographic findings to non-specialist audiences.
- **physical-geography skill:** The phenomena being mapped and analyzed.
- **human-geography skill:** The social data represented in thematic maps.
- **fieldwork-methods skill:** Data collection that feeds into GIS analysis.

## References

- Slocum, T. A. et al. (2022). *Thematic Cartography and Geovisualization*. 4th edition. CRC Press.
- Longley, P. A. et al. (2015). *Geographic Information Science and Systems*. 4th edition. Wiley.
- Tobler, W. R. (1970). "A Computer Movie Simulating Urban Growth in the Detroit Region." *Economic Geography*, 46(sup1), 234--240.
- Monmonier, M. (2018). *How to Lie with Maps*. 3rd edition. University of Chicago Press.
- Robinson, A. H. et al. (1995). *Elements of Cartography*. 6th edition. Wiley.
- Jensen, J. R. (2015). *Introductory Digital Image Processing*. 4th edition. Pearson.
