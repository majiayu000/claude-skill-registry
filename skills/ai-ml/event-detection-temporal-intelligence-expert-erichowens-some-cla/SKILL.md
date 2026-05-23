---
name: event-detection-temporal-intelligence-expert
description: Expert in temporal event detection, spatio-temporal clustering (ST-DBSCAN), and photo context understanding. Use for detecting photo events, clustering by time/location, shareability prediction, place recognition, event significance scoring, and life event detection. Activate on 'event detection', 'temporal clustering', 'ST-DBSCAN', 'spatio-temporal', 'shareability prediction', 'place recognition', 'life events', 'photo events', 'temporal diversity'. NOT for individual photo aesthetic quality (use photo-composition-critic), color palette analysis (use color-theory-palette-harmony-expert), face recognition implementation (use photo-content-recognition-curation-expert), or basic EXIF timestamp extraction.
allowed-tools: Read,Write,Edit,Bash,Grep,Glob,mcp__firecrawl__firecrawl_search,WebFetch
category: AI & Machine Learning
tags:
  - temporal
  - clustering
  - events
  - spatio-temporal
  - photo-context
pairs-with:
  - skill: photo-content-recognition-curation-expert
    reason: Content + temporal understanding
  - skill: wedding-immortalist
    reason: Event detection for wedding albums
---

# Event Detection & Temporal Intelligence Expert

Expert in detecting meaningful events from photo collections using spatio-temporal clustering, significance scoring, and intelligent photo selection for collages.

## When to Use This Skill

✅ **Use for:**
- Detecting events from photo timestamps + GPS coordinates
- Clustering photos by time, location, and visual content (ST-DBSCAN, DeepDBSCAN)
- Scoring event significance (birthday > commute)
- Predicting photo shareability for social media
- Recognizing life events (graduations, weddings, births, moves)
- Temporal diversity optimization (avoid all photos from one day)
- Event-aware collage photo selection

❌ **NOT for:**
- Individual photo aesthetic quality → `photo-composition-critic`
- Color palette analysis → `color-theory-palette-harmony-expert`
- Face clustering/recognition → `photo-content-recognition-curation-expert`
- CLIP embedding generation → `clip-aware-embeddings`
- Single-photo timestamp extraction (basic EXIF parsing)

## Quick Decision Tree

```
Need to group photos into meaningful events?
├─ Have GPS + timestamps? ──────────────────── ST-DBSCAN
│   ├─ Also need visual similarity? ────────── DeepDBSCAN (add CLIP)
│   └─ Need hierarchical events? ───────────── Multi-level cascading
│
├─ No GPS, only timestamps? ────────────────── Temporal binning
│   └─ With visual content? ─────────────────── CLIP + temporal
│
└─ Photos have faces + want groups? ─────────── Face clustering first
    └─ Then event detection per person
```

## Core Concepts

### 1. ST-DBSCAN: Spatio-Temporal Clustering

**The Problem**: Standard clustering fails for photos—same location on different days shouldn't be grouped.

**Key Insight**: 100 meters apart in same hour = same event. 100 meters apart 3 days later = different events.

**ST-DBSCAN Parameters**:
```
ε_spatial:   50m (indoor) → 500m (outdoor festival) → 5km (city tour)
ε_temporal:  1hr (short event) → 8hr (day trip) → 24hr (multi-day)
min_pts:     3 (small gathering) → 10 (large event)
```

**Algorithm**: Both spatial AND temporal constraints must be satisfied:
```
Neighbor(p) = {q | distance(p,q) ≤ ε_spatial AND |time(p)-time(q)| ≤ ε_temporal}
```

→ **Deep dive**: `references/st-dbscan-implementation.md`

### 2. DeepDBSCAN: Adding Visual Content

**Problem**: Photos at same time/place can be different subjects (ceremony vs empty chairs).

**Solution**: Add CLIP embeddings as third dimension:
```
Neighbor(p) = {q | spatial_ok AND temporal_ok AND cosine_sim(clip_p, clip_q) > threshold}
```

**eps_visual**: 0.3 (similar subjects) → 0.5 (diverse event content)

### 3. Hierarchical Event Detection

**Use case**: "Paris Vacation" contains "Day 1: Louvre", "Day 2: Eiffel Tower"

**Approach**: Cascade ST-DBSCAN with expanding thresholds:
1. **High-level** (vacations): eps_spatial=50km, eps_temporal=72hr
2. **Mid-level** (daily): eps_spatial=5km, eps_temporal=12hr
3. **Low-level** (moments): eps_spatial=500m, eps_temporal=1hr

---

## Event Significance Scoring

**Goal**: Birthday party > Daily commute photos

**Multi-Factor Model** (weights sum to 1.0):

| Factor | Weight | Description |
|--------|--------|-------------|
| location_rarity | 0.20 | Exotic location > home |
| people_presence | 0.15 | Photos with people score higher |
| photo_density | 0.15 | More photos/hour = more memorable |
| content_rarity | 0.15 | Landmarks, celebrations detected via CLIP |
| visual_diversity | 0.10 | Varied shots = special event |
| duration | 0.10 | Longer events score higher |
| engagement | 0.10 | Shared/edited/favorited photos |
| temporal_rarity | 0.05 | Annual patterns (birthdays, holidays) |

→ **Deep dive**: `references/event-scoring-shareability.md`

---

## Shareability Prediction

**Goal**: Predict which photos will be shared on social media.

**High-Signal Features** (2025 research):
1. **Smiling faces** (+0.3 base score)
2. **Group photos** (3+ people, +0.2)
3. **Famous landmarks** (+0.25)
4. **Food scenes** (+0.15)
5. **Moderate visual complexity** (0.4-0.6 optimal)
6. **Recency** (decays over 30 days)

**Shareability Threshold**: &gt;0.6 = "Highly Shareable"

→ **Deep dive**: `references/event-scoring-shareability.md`

---

## Life Event Detection

Automatically detect major life events using multi-modal signals:

| Event Type | Primary Signals | Threshold |
|------------|-----------------|-----------|
| **Graduation** | Cap/gown, diploma, auditorium | 0.6 |
| **Wedding** | Formal attire, bouquet, cake, rings | 0.7 |
| **Birth** | New infant face cluster, hospital setting | 0.8 |
| **Residential Move** | 50km+ location shift, &gt;30 days | 0.8 |
| **Travel Milestone** | First visit to new country | 1.0 |

→ **Deep dive**: `references/place-recognition-life-events.md`

---

## Temporal Diversity for Selection

**Problem**: Without constraints, collage might be all vacation photos.

### Method Comparison

| Method | Best For | Use When |
|--------|----------|----------|
| **Temporal Binning** | Even time coverage | Need chronological spread |
| **Temporal MMR** | Quality + diversity balance | Balanced selection |
| **Event-Based** | Event representation | Each event matters |

### Temporal MMR Formula

```
MMR(photo) = λ × quality + (1-λ) × min_temporal_distance_to_selected
```
- λ=0.5: Balanced
- λ=0.7: Prefer quality
- λ=0.3: Prefer diversity

→ **Deep dive**: `references/temporal-diversity-pipeline.md`

---

## Common Anti-Patterns

### Anti-Pattern: Time-Only Clustering

**What it looks like**: Using K-means or basic DBSCAN on timestamps only
```python
clusters = KMeans(n_clusters=10).fit(timestamps)  # WRONG
```

**Why it's wrong**: Multi-day trips at same location get split; same-day different-location events get merged.

**What to do instead**: Use ST-DBSCAN with both spatial AND temporal constraints.

### Anti-Pattern: Fixed Epsilon Values

**What it looks like**: Using same eps_spatial=100m for all events

**Why it's wrong**: Indoor events need 50m, city tours need 5km.

**What to do instead**: Adaptive thresholds based on event type detection, or hierarchical clustering with multiple scales.

### Anti-Pattern: Ignoring Visual Content

**What it looks like**: ST-DBSCAN alone for event detection

**Why it's wrong**: Wedding ceremony and empty chairs setup—same time/place, completely different importance.

**What to do instead**: DeepDBSCAN with CLIP embeddings for content-aware clustering.

### Anti-Pattern: Euclidean Distance for GPS

**What it looks like**:
```python
distance = sqrt((lat2-lat1)**2 + (lon2-lon1)**2)  # WRONG
```

**Why it's wrong**: Degrees ≠ meters. 1° latitude = 111km, but 1° longitude varies by latitude.

**What to do instead**: Haversine formula for great-circle distance:
```python
from geopy.distance import geodesic
distance_meters = geodesic((lat1, lon1), (lat2, lon2)).meters
```

### Anti-Pattern: No Noise Handling

**What it looks like**: Forcing every photo into a cluster

**Why it's wrong**: Solo commute photos pollute event clusters.

**What to do instead**: DBSCAN naturally identifies noise (label=-1). Keep noise separate—don't force into nearest cluster.

### Anti-Pattern: Shareability Without Event Context

**What it looks like**: Predicting shareability from photo features alone

**Why it's wrong**: A mediocre photo from your wedding is more shareable than a great photo from Tuesday's lunch.

**What to do instead**: Include event significance as feature:
```python
features['event_significance'] = photo.event.significance_score
```

---

## Quick Start: Event Detection Pipeline

```python
from event_detection import EventDetectionPipeline

pipeline = EventDetectionPipeline()

# Process photo corpus
results = pipeline.process_photo_corpus(photos)

# Access events
for event in results['events']:
    print(f"{event.label}: {len(event.photos)} photos, significance={event.significance_score:.2f}")

# Access life events
for life_event in results['life_events']:
    print(f"{life_event.type} detected on {life_event.timestamp}")

# Select for collage with diversity
collage_photos = pipeline.select_for_collage(results, target_count=100)
```

---

## Performance Targets

| Operation | Target |
|-----------|--------|
| ST-DBSCAN (10K photos) | &lt; 2 seconds |
| Event significance scoring | &lt; 100ms/event |
| Shareability prediction | &lt; 50ms/photo |
| Place recognition (cached) | &lt; 10ms/photo |
| Full pipeline (10K photos) | &lt; 5 seconds |

---

## Python Dependencies

```
numpy scipy scikit-learn hdbscan geopy transformers xgboost pandas opencv-python
```

---

## Integration Points

- **collage-layout-expert**: Pass event clusters for diversity-aware placement
- **photo-content-recognition-curation-expert**: Get face clusters before event detection
- **color-theory-palette-harmony-expert**: Use for visual diversity within events
- **clip-aware-embeddings**: Generate embeddings for DeepDBSCAN

---

## References

1. **ST-DBSCAN**: Birant & Kut (2007), "ST-DBSCAN: An algorithm for clustering spatial-temporal data"
2. **DeepDBSCAN**: ISPRS 2021, "Deep Density-Based Clustering for Geo-Tagged Photos"
3. **Shareability**: arXiv 2025, "Predicting Social Media Engagement from Emotional and Temporal Features"
4. **GeoNames/OpenStreetMap**: Reverse geocoding for place recognition

---

**Version**: 2.0.0
**Last Updated**: November 2025
