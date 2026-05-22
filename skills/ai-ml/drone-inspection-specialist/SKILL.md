---
name: drone-inspection-specialist
description: Advanced CV for infrastructure inspection including forest fire detection, wildfire precondition assessment, roof inspection, hail damage analysis, thermal imaging, and 3D Gaussian Splatting reconstruction. Expert in multi-modal detection, insurance risk modeling, and reinsurance data pipelines. Activate on "fire detection", "wildfire risk", "roof inspection", "hail damage", "thermal analysis", "Gaussian Splatting", "3DGS", "insurance inspection", "defensible space", "property assessment", "catastrophe modeling", "NDVI", "fuel load". NOT for general drone flight control, SLAM, path planning, or sensor fusion (use drone-cv-expert), GPU shader development (use metal-shader-expert), or generic object detection without inspection context (use clip-aware-embeddings).
allowed-tools: Read,Write,Edit,Bash(python:*,pip:*),Grep,Glob,mcp__firecrawl__firecrawl_search,WebFetch,mcp__stability-ai__stability-ai-generate-image
category: AI & Machine Learning
tags:
  - inspection
  - fire-detection
  - thermal
  - gaussian-splatting
  - insurance
pairs-with:
  - skill: drone-cv-expert
    reason: Core drone navigation and CV
  - skill: clip-aware-embeddings
    reason: Semantic understanding of inspected areas
---

# Drone Inspection Specialist

Expert in drone-based infrastructure inspection with computer vision, thermal analysis, and 3D reconstruction for insurance, property assessment, and environmental monitoring.

## Decision Tree: When to Use This Skill

```
User mentions drones/UAV?
├─ YES → Is it about inspection or assessment of something?
│        ├─ Fire detection, smoke, thermal hotspots → THIS SKILL
│        ├─ Roof damage, hail, shingles → THIS SKILL
│        ├─ Property/insurance assessment → THIS SKILL
│        ├─ 3D reconstruction for measurement → THIS SKILL
│        ├─ Wildfire risk, defensible space → THIS SKILL
│        └─ NO (flight control, navigation, general CV) → drone-cv-expert
└─ NO → Is it about fire/roof/property assessment without drones?
        ├─ YES → Still use THIS SKILL (methods apply)
        └─ NO → Different skill needed
```

## Core Competencies

### Fire Detection & Wildfire Risk
- **Multi-Modal Detection**: RGB smoke + thermal hotspot fusion
- **Precondition Assessment**: NDVI, fuel load, vegetation density
- **Defensible Space**: CAL FIRE/NFPA 1144 compliance evaluation
- **Progression Tracking**: Spread rate, direction prediction

### Roof & Structural Inspection
- **Damage Detection**: Cracks, missing shingles, wear, ponding
- **Hail Analysis**: Impact pattern recognition, size estimation
- **Thermal Analysis**: Moisture detection, insulation gaps, HVAC leaks
- **Material Classification**: Asphalt, metal, tile, slate identification

### 3D Reconstruction (Gaussian Splatting)
- **Pipeline**: Video → COLMAP SfM → 3DGS training → Web viewer
- **Measurements**: Roof area, damage dimensions, property bounds
- **Change Detection**: Before/after comparison for claims

### Insurance & Reinsurance
- **Claim Packaging**: Documentation meeting industry standards
- **Risk Modeling**: Catastrophe models, loss distributions
- **Precondition Data**: Satellite + drone + ground integration

## Anti-Patterns to Avoid

### 1. "Single-Sensor Dependence"
**Wrong**: Using only RGB for fire detection.
**Right**: Multi-modal fusion (RGB + thermal) for high-confidence alerts.
| Detection Source | Confidence | Action |
|------------------|------------|--------|
| Thermal fire only | 70% | Alert + verify |
| RGB smoke only | 60% | Alert + investigate |
| Thermal + RGB | 95% | Confirmed fire |

### 2. "Ignoring Hail Pattern"
**Wrong**: Counting damage without analyzing spatial distribution.
**Right**: True hail damage has RANDOM distribution. Linear or clustered patterns indicate other causes (foot traffic, age).

### 3. "Thermal Temperature Trust"
**Wrong**: Using raw thermal values without calibration.
**Right**: Account for:
- Emissivity of materials (roof = 0.9-0.95)
- Atmospheric transmission (humidity, distance)
- Reflected temperature from surroundings
- Time of day (thermal lag)

### 4. "3DGS Frame Overload"
**Wrong**: Extracting every frame from drone video.
**Right**: Extract 2-3 fps with 80% overlap. More frames ≠ better reconstruction.
| Video FPS | Extract Rate | Result |
|-----------|--------------|--------|
| 30 | 30 (all) | Redundant, slow processing |
| 30 | 2-3 | Optimal quality/speed |
| 30 | 0.5 | Insufficient overlap |

### 5. "Insurance Claim Speculation"
**Wrong**: Estimating costs without material identification.
**Right**: Identify material → Apply correct cost matrix.
| Material | Repair $/sqft | Replace $/sqft |
|----------|--------------|----------------|
| Asphalt shingle | $5-10 | $3-7 |
| Metal | $10-15 | $8-14 |
| Tile | $12-20 | $10-18 |
| Slate | $20-40 | $15-30 |

### 6. "Defensible Space Zone Confusion"
**Wrong**: Treating all vegetation equally regardless of distance.
**Right**: CAL FIRE zones have different requirements:
| Zone | Distance | Requirement |
|------|----------|-------------|
| 0 | 0-5 ft | Ember-resistant (no combustibles) |
| 1 | 5-30 ft | Lean, clean, green (spaced trees) |
| 2 | 30-100 ft | Reduced fuel (selective thinning) |

## Data Collection Strategy

### Satellite Data (Regional Context)
- **Sentinel-2**: 10m resolution, NDVI, fuel moisture (SWIR bands)
- **Landsat-8**: 30m resolution, historical baseline, thermal band
- **Planet**: 3m resolution daily, change detection
- **Application**: Regional risk mapping, before/after events

### Drone Data (Property Detail)
- **RGB Mapping**: 2-5cm GSD, orthomosaic, 3D model
- **Thermal Survey**: Moisture detection, heat signatures
- **Close Inspection**: Damage documentation, detail photos
- **Application**: Individual property assessment

### Ground Truth
- **Slope Measurement**: GPS transects for topographic risk
- **Soil Sampling**: Moisture content for fire risk
- **Material Verification**: Confirm roof type
- **Application**: Calibration and validation

## Quick Reference Tables

### Fire Detection Confidence Levels
| Signal Combination | Confidence | Alert Priority |
|-------------------|------------|----------------|
| Thermal &gt;150°C + Smoke | 95% | CRITICAL |
| Thermal fire model | 80% | HIGH |
| Hotspot &gt;80°C | 70% | MEDIUM |
| Smoke only | 60% | MEDIUM |
| Hotspot 60-80°C | 50% | LOW |

### Roof Damage Severity
| Type | Low | Medium | High | Critical |
|------|-----|--------|------|----------|
| Missing shingle | - | - | Always | - |
| Crack | &lt;1" | 1-3" | &gt;3" | Multiple |
| Granule loss | &lt;10% | 10-30% | &gt;30% | - |
| Ponding | - | Small | Large | Active leak |

### Wildfire Risk Factors (Weighted)
| Factor | Weight | High Risk Indicators |
|--------|--------|---------------------|
| Defensible space | 20% | Non-compliant zones |
| Vegetation density | 20% | NDVI &gt;0.6, high fuel load |
| Slope | 15% | &gt;30% grade |
| Roof material | 10% | Wood shake, Class C |
| Structure spacing | 10% | &lt;30ft between buildings |
| Access/egress | 10% | Single road, narrow |

### 3DGS Quality Settings
| Quality Level | Iterations | Time | Use Case |
|---------------|------------|------|----------|
| Preview | 7K | 5 min | Quick check |
| Standard | 30K | 30 min | General use |
| High | 50K | 60 min | Documentation |
| Inspection | 100K | 3 hrs | Damage measurement |

## Reference Files

Detailed implementations in `references/`:
- `fire-detection.md` - Multi-modal fire detection, thermal cameras, progression tracking
- `roof-inspection.md` - Damage detection, thermal analysis, material classification
- `insurance-risk-assessment.md` - Hail damage, wildfire risk, catastrophe modeling, reinsurance
- `gaussian-splatting-3d.md` - COLMAP pipeline, 3DGS training, inspection measurements

## Integration Points

- **drone-cv-expert**: Flight control, navigation, general CV algorithms
- **metal-shader-expert**: GPU-accelerated 3DGS rendering
- **collage-layout-expert**: Visual report composition
- **clip-aware-embeddings**: Material/damage classification assistance

## Insurance Workflow

```
1. Pre-Event Assessment (Underwriting)
   ├─ Satellite: Regional risk context
   ├─ Drone: Property-level risk factors
   └─ Output: Risk score, premium factors

2. Post-Event Inspection (Claims)
   ├─ Drone survey: Damage documentation
   ├─ 3DGS: Measurements, change detection
   └─ Output: Claim package, cost estimate

3. Portfolio Risk (Reinsurance)
   ├─ Aggregate: TIV, loss curves
   ├─ Model: AAL, PML, concentration
   └─ Output: Treaty pricing, structure
```

---

**Key Principle**: Inspection accuracy depends on multi-source data fusion. Single-sensor assessments miss critical context. Always correlate drone findings with satellite baseline and weather data for defensible conclusions.
