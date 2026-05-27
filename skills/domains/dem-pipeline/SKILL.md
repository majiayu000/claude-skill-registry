---
name: dem-pipeline
description: Run DEM lineament analysis to identify unmapped fault structures. Use when visually confirming orphan earthquake clusters, mapping fault extensions, or finding dark earthquake sources. Triggers on "DEM analysis", "lineament", "edge detection", "drainage analysis".
---

# /dem-pipeline - DEM Lineament Analysis Skill

## Purpose

Run Digital Elevation Model (DEM) analysis pipeline to identify unmapped fault structures through edge detection, drainage pattern analysis, and topographic lineament extraction. Validated in Italy where DEM revealed 25+ km unmapped fault.

## Usage

```
/dem-pipeline <region> [--dem-path PATH] [--output-dir DIR] [--overlay GEOJSON]
```

**Examples:**
```
/dem-pipeline italy --dem-path dem_tiles/tinitaly_basura.tif
/dem-pipeline san-diego --overlay data/fault_databases/scec_cfm_sandiego.geojson
/dem-pipeline turkey --dem-path dem_tiles/sofular_srtm.tif
```

## Prerequisites

### Required Data

| Data Type | Source | Format |
|-----------|--------|--------|
| DEM tiles | TINITALY, SRTM, USGS 3DEP | GeoTIFF |
| Fault database | DISS, SCEC CFM, GEM | GeoJSON |
| Microseismicity | INGV, USGS, AFAD | CSV |
| Cave location | SISAL | Coordinates |

### Python Dependencies

```
numpy, scipy, matplotlib, rasterio, geopandas,
scikit-image (edge detection), pysheds (drainage)
```

## Pipeline Steps

### Step 1: Load and Preprocess DEM

```python
# Load DEM
dem = rasterio.open(dem_path)
elevation = dem.read(1)

# Resample if needed (target: 10-30m resolution)
if resolution > 30:
    elevation = resample_dem(elevation, target_res=30)

# Fill voids/nodata
elevation = fill_voids(elevation)
```

### Step 2: Generate Hillshade

```python
# Calculate hillshade for visualization
hillshade = calculate_hillshade(
    elevation,
    azimuth=315,  # NW illumination
    altitude=45
)

# Save as GeoTIFF
save_geotiff(hillshade, 'hillshade.tif')
```

### Step 3: Edge Detection

Apply multiple edge detection algorithms:

```python
# Sobel edge detection (gradient-based)
sobel_edges = sobel(elevation)

# Canny edge detection (multi-scale)
canny_edges = canny(elevation, sigma=2)

# Save results
save_geotiff(sobel_edges, 'edge_sobel.tif')
save_geotiff(canny_edges, 'edge_canny.tif')
```

**Look for:**
- Linear features at consistent azimuths
- Edges that align with orphan earthquake clusters
- Topographic breaks/scarps

### Step 4: Drainage Network Analysis

```python
# Calculate flow direction
flow_dir = calculate_flow_direction(elevation)

# Calculate flow accumulation
flow_acc = calculate_flow_accumulation(flow_dir)

# Extract drainage network (threshold: 1000 cells)
drainage = extract_drainage(flow_acc, threshold=1000)

# Save results
save_geotiff(drainage, 'drainage.tif')
```

**Look for:**
- Drainage anomalies (right-angle bends, beheaded streams)
- Linear valley alignments
- Offset drainage patterns (strike-slip indicators)

### Step 5: Lineament Extraction

```python
# Automated lineament extraction
lineaments = extract_lineaments(
    sobel_edges,
    min_length=5000,  # 5 km minimum
    max_gap=500       # 500m max gap
)

# Calculate azimuths
for lineament in lineaments:
    lineament.azimuth = calculate_azimuth(lineament)
    lineament.length = calculate_length(lineament)

# Group by azimuth
azimuth_groups = group_by_azimuth(lineaments, bin_size=15)
```

### Step 6: Overlay Analysis

```python
# Load fault database
faults = gpd.read_file(fault_geojson)

# Load microseismicity
earthquakes = pd.read_csv(eq_csv)
orphans = earthquakes[earthquakes['is_orphan'] == True]

# Create overlay figure
fig, ax = plt.subplots(figsize=(12, 10))
ax.imshow(hillshade, cmap='gray')
faults.plot(ax=ax, color='red', linewidth=2, label='Mapped faults')
ax.scatter(orphans.lon, orphans.lat, c='yellow', s=10, label='Orphan EQs')
lineaments.plot(ax=ax, color='cyan', linewidth=1, label='DEM lineaments')

plt.savefig('overlay_analysis.png', dpi=300)
```

## Output Products

### 1. GeoTIFF Rasters

| File | Description |
|------|-------------|
| `hillshade.tif` | Hillshade visualization |
| `edge_sobel.tif` | Sobel edge detection |
| `edge_canny.tif` | Canny edge detection |
| `drainage.tif` | Drainage network |
| `slope.tif` | Slope map (optional) |
| `aspect.tif` | Aspect map (optional) |

### 2. Publication Figures (300 DPI PNG)

| Figure | Content |
|--------|---------|
| `fig_hillshade.png` | Hillshade base map |
| `fig_edge_detection.png` | Edge detection results |
| `fig_drainage.png` | Drainage network |
| `fig_overlay.png` | Full overlay (faults + EQs + lineaments) |
| `fig_azimuth_rose.png` | Rose diagram of lineament azimuths |

### 3. Analysis Report

```markdown
## DEM Lineament Analysis: [Region]

**DEM source**: [TINITALY/SRTM/etc.]
**Resolution**: [X] m
**Analysis date**: [date]

---

### Lineament Statistics

| Azimuth Bin | Count | Total Length | Avg Length |
|-------------|-------|--------------|------------|
| N-S (0-15°) | [N] | [X] km | [X] km |
| NNE (15-30°) | [N] | [X] km | [X] km |
| ... | ... | ... | ... |

### Dominant Lineament Sets

1. **[Azimuth]° trend**: [N] lineaments, [X] km total
   - Correlation with: [orphan cluster / mapped fault / etc.]

2. **[Azimuth]° trend**: ...

---

### Comparison with Mapped Faults

| Mapped Fault | Strike | DEM Lineament Match? |
|--------------|--------|---------------------|
| [fault name] | [X]° | [YES/NO] |

### Unmapped Structures Identified

| Structure | Azimuth | Length | Evidence |
|-----------|---------|--------|----------|
| NNW lineament | 340° | 25+ km | Edge + drainage + 85 orphan EQs |

---

### Interpretation

[2-3 paragraphs on geological interpretation]

---

### Files Created

| File | Path |
|------|------|
| Hillshade | `dem_tiles/[region]/hillshade.tif` |
| Edge detection | `dem_tiles/[region]/edge_sobel.tif` |
| Overlay figure | `dem_tiles/[region]/fig_overlay.png` |
```

## Example: Italy Bàsura Results

```
DEM Lineament Analysis: Ligurian Alps (Italy)

DEM: TINITALY 10m
Area: 50 km radius around Bàsura Cave

Key Finding: NNW-SSE Lineament Set

- Azimuth: 335-345° (NNW)
- Length: 25+ km
- Evidence:
  - Strong edge detection signal
  - Anomalous drainage (right-angle bends)
  - 85 orphan earthquakes aligned
  - NOT in DISS, ITHACA, or EFSM20

Interpretation:
Previously unmapped fault structure, primary candidate
for 1285/1394 dark earthquakes. Strike consistent with
regional stress field. Recommend InSAR/GPS validation.
```

## Integration with Other Skills

| Skill | Integration |
|-------|-------------|
| `/orphan-analysis` | Use orphan clusters to guide DEM interpretation |
| `/verify-dark` | DEM findings inform "unmapped fault" classification |
| `/regional-doc` | Document findings in `DEM_LINEAMENT_FINDINGS.md` |

## Scripts Reference

Existing scripts in `paleoseismic_caves/scripts/`:

| Script | Purpose |
|--------|---------|
| `dem_lineament_analysis.py` | Italy Bàsura analysis |
| `san_diego_dem_processing.py` | Rose Canyon analysis |
| `san_diego_lineament_analysis.py` | Full SD pipeline |
| `san_diego_integrated_overlay.py` | Multi-layer visualization |

## Important Notes

1. **Resolution matters** - 10-30m optimal for fault detection
2. **Multiple methods** - Sobel + Canny + drainage gives confidence
3. **Ground truth needed** - DEM alone is not proof
4. **Orphan correlation key** - Lineaments matching orphan clusters are strongest evidence
5. **Publication quality** - 300 DPI, proper color scales, scale bars

## Regional DEM Sources

| Region | Source | Resolution | Coverage |
|--------|--------|------------|----------|
| Italy | TINITALY | 10m | Complete |
| California | USGS 3DEP | 1-10m | Complete |
| Turkey | SRTM | 30m | Complete |
| Belize | SRTM | 30m | Limited |
| Brazil | SRTM | 30m | Complete |
