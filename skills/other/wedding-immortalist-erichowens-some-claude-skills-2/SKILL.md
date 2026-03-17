---
name: wedding-immortalist
description: Transform thousands of wedding photos and hours of footage into an immersive 3D Gaussian Splatting experience with theatre mode replay, face-clustered guest roster, and AI-curated best photos per person. Expert in 3DGS pipelines, face clustering, aesthetic scoring, and adaptive design matching the couple's wedding theme (disco, rustic, modern, LGBTQ+ celebrations). Activate on "wedding photos", "wedding video", "3D wedding", "Gaussian Splatting wedding", "wedding memory", "wedding immortalize", "face clustering wedding", "best wedding photos". NOT for general photo editing (use native-app-designer), non-wedding 3DGS (use drone-inspection-specialist), or event planning (not a wedding planner).
allowed-tools: Read,Write,Edit,Bash,Grep,Glob,WebFetch
category: AI & Machine Learning
tags:
  - wedding
  - 3dgs
  - gaussian-splatting
  - face-clustering
  - memories
pairs-with:
  - skill: photo-content-recognition-curation-expert
    reason: Curate wedding photos
  - skill: event-detection-temporal-intelligence-expert
    reason: Detect wedding events
---

# Wedding Immortalist

Transform wedding photos and video into an eternal, immersive 3D experience. Create living memories that let couples and guests relive the magic forever.

## When to Use This Skill

**Use for:**
- Processing thousands of wedding photos into 3DGS scenes
- Creating theatre-mode experiences where ceremony/reception moments play in-place
- Building face-clustered guest rosters with best-photo selection
- Matching design aesthetics to wedding themes (disco, rustic, beach, modern, queer celebrations)
- AI-curated photo selection per guest with aesthetic scoring

**NOT for:**
- General photo editing → use native-app-designer
- Non-wedding 3DGS → use drone-inspection-specialist
- Event planning → not a wedding planner
- Video editing without 3D reconstruction

## Core Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│                    WEDDING IMMORTALIST PIPELINE                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. INGEST                2. RECONSTRUCT        3. CLUSTER       │
│  ├─ Photos (1000s)        ├─ COLMAP SfM         ├─ Face detect   │
│  ├─ Video (hours)         ├─ 3DGS training      ├─ Embeddings    │
│  └─ Audio/speeches        └─ Scene merge        └─ Identity link │
│                                                                  │
│  4. CURATE                5. DESIGN             6. PRESENT       │
│  ├─ Aesthetic score       ├─ Theme extract      ├─ Web viewer    │
│  ├─ Per-person best       ├─ Color palette      ├─ Theatre mode  │
│  └─ Moment detect         └─ Typography         └─ Guest roster  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Theme-Adaptive Design

### Theme Detection & Matching

Every wedding has a unique aesthetic. Extract and honor it:

| Theme Type | Color Palette | Typography | UI Elements |
|------------|---------------|------------|-------------|
| **70s Disco** | Gold, orange, burnt sienna, deep purple | Groovy script, bold sans | Mirror balls, starbursts, warm gradients |
| **Rustic/Barn** | Earth tones, sage, cream, wood | Serif, hand-lettered | Burlap textures, wildflower accents |
| **Beach/Coastal** | Ocean blues, sand, coral, seafoam | Light sans, script | Shell motifs, wave patterns |
| **Modern Minimal** | Black, white, metallics | Clean geometric sans | Sharp lines, negative space |
| **Queer Joy** | Rainbow spectrums, bold colors | Expressive, varied | Pride elements, celebration maximalism |
| **Cultural Fusion** | Per tradition | Traditional + modern | Cultural motifs, heritage patterns |

### Extracting Theme from Photos

```python
# Theme extraction signals
THEME_SIGNALS = {
    'color_palette': 'Dominant colors from venue, florals, attire',
    'lighting_mood': 'Warm/cool, natural/dramatic, string lights/chandeliers',
    'decor_elements': 'Rustic/modern/vintage/eclectic',
    'attire_style': 'Traditional/non-traditional, formal/casual',
    'cultural_markers': 'Religious symbols, cultural traditions',
    'era_aesthetic': '70s disco, 20s gatsby, etc.'
}
```

## 3D Gaussian Splatting Pipeline

### Photo/Video Ingestion

```
Optimal Input Strategy:
├── Video: Extract 2-3 fps (80% overlap minimum)
├── Photos: Include ALL photographer shots
├── Phone photos: Guest uploads (georeferenced bonus)
└── Coverage: Ceremony + reception + all spaces

Quality Thresholds:
├── Minimum images per space: 50-100
├── Overlap requirement: 60-80%
├── Blur rejection: Laplacian variance < 100 = skip
└── Exposure: Reject severe over/underexposure
```

### COLMAP Structure from Motion

```bash
# Feature extraction
colmap feature_extractor \
  --database_path database.db \
  --image_path images/ \
  --ImageReader.single_camera 0 \
  --SiftExtraction.max_image_size 3200

# Exhaustive matching for comprehensive coverage
colmap exhaustive_matcher \
  --database_path database.db \
  --SiftMatching.guided_matching 1

# Sparse reconstruction
colmap mapper \
  --database_path database.db \
  --image_path images/ \
  --output_path sparse/

# Dense reconstruction (optional, for mesh)
colmap image_undistorter ...
colmap patch_match_stereo ...
```

### 3DGS Training

```python
# Wedding-optimized 3DGS settings
WEDDING_3DGS_CONFIG = {
    'iterations': 50_000,          # High quality for permanent archive
    'densify_from_iter': 500,
    'densify_until_iter': 15_000,
    'densification_interval': 100,
    'opacity_reset_interval': 3000,
    'sh_degree': 3,                # Full spherical harmonics for lighting
    'percent_dense': 0.01,
    'densify_grad_threshold': 0.0002,
}

# Multi-space merge strategy
SPACES = ['ceremony', 'cocktail_hour', 'reception', 'photo_booth', 'dance_floor']
# Train each separately, then create unified navigation
```

## Face Clustering System

### Pipeline

```
┌────────────────────────────────────────────────────────┐
│               FACE CLUSTERING PIPELINE                  │
├────────────────────────────────────────────────────────┤
│  1. Detection (RetinaFace/MTCNN)                       │
│     └─ All faces in all photos                         │
│  2. Alignment (5-point landmark)                       │
│     └─ Standardize for embedding                       │
│  3. Embedding (ArcFace/AdaFace)                        │
│     └─ 512-dim identity vector per face                │
│  4. Clustering (HDBSCAN)                               │
│     └─ Group by identity, handle edge cases            │
│  5. Identity Linking                                   │
│     └─ Match to couple, wedding party, family, guests  │
│  6. Best Photo Selection                               │
│     └─ Aesthetic scoring per cluster                   │
└────────────────────────────────────────────────────────┘
```

### Clustering Parameters

```python
CLUSTERING_CONFIG = {
    'min_cluster_size': 3,         # At least 3 photos to form identity
    'min_samples': 2,
    'metric': 'cosine',
    'cluster_selection_epsilon': 0.3,
    'cluster_selection_method': 'eom',
}

# Identity priority for naming
IDENTITY_PRIORITY = [
    'couple_1', 'couple_2',        # The married couple
    'wedding_party',               # Bridesmaids, groomspeople
    'parents',                     # Parents of the couple
    'grandparents',
    'siblings',
    'extended_family',
    'friends',
    'vendors',                     # Photographer, DJ, etc.
]
```

### Identity Linking Workflow

1. **Couple identification**: User tags couple in 2-3 photos
2. **Wedding party**: User identifies key people
3. **Auto-propagation**: Embeddings match across all photos
4. **Guest matching**: Optional guest list import for name assignment
5. **Manual corrections**: UI for fixing mismatches

## Aesthetic Scoring

### Per-Photo Quality Metrics

```python
AESTHETIC_FEATURES = {
    # Technical quality
    'sharpness': 'Laplacian variance, MTF analysis',
    'exposure': 'Histogram analysis, dynamic range',
    'noise': 'High-ISO detection, grain analysis',

    # Composition
    'rule_of_thirds': 'Subject placement scoring',
    'symmetry': 'For venue/group shots',
    'framing': 'Negative space, balance',

    # Face-specific
    'expression': 'Smile detection, eye openness',
    'blink_detection': 'Eyes closed penalty',
    'gaze_direction': 'Looking at camera vs. candid',
    'face_occlusion': 'Nothing blocking the face',
    'face_lighting': 'Even illumination, no harsh shadows',

    # Emotional
    'genuine_smile': 'Duchenne marker detection',
    'moment_quality': 'Laughter, tears, embraces',
}
```

### Best Photo Selection Per Person

```python
def select_best_photos(cluster_photos, n=5):
    """Select top N photos for a person across all their appearances."""

    scores = []
    for photo in cluster_photos:
        score = (
            0.25 * technical_quality(photo) +
            0.25 * composition_score(photo) +
            0.30 * expression_quality(photo) +
            0.20 * context_diversity(photo, scores)  # Avoid all similar shots
        )
        scores.append((photo, score))

    # Select top N with diversity constraint
    return diverse_top_n(scores, n, diversity_threshold=0.7)
```

## Theatre Mode

### Moment Detection & Playback

```
KEY MOMENTS (auto-detected + user-tagged):
├── Ceremony
│   ├── Processional
│   ├── Vows exchange
│   ├── Ring ceremony
│   ├── First kiss
│   └── Recessional
├── Reception
│   ├── Grand entrance
│   ├── First dance
│   ├── Parent dances
│   ├── Toasts/speeches
│   ├── Cake cutting
│   └── Bouquet/garter
├── Party
│   ├── Dance floor highlights
│   └── Exit/sendoff
└── Candids
    ├── Emotional moments (tears, laughter)
    └── Spontaneous joy
```

### In-Scene Video Projection

```
Theatre Mode Rendering:
1. User navigates 3DGS scene freely
2. Approaches "moment marker" (glowing orb/frame)
3. Video/slideshow plays IN the 3D space
   ├── On walls where projector was
   ├── Floating frames in dance floor area
   └── Photo booth backdrop location
4. Spatial audio for speeches/music
5. User can pause, scrub, exit to continue exploring
```

## Web Viewer Architecture

```javascript
// Wedding Immortalist Viewer Components
const VIEWER_FEATURES = {
  // 3DGS Navigation
  gaussianSplatting: {
    renderer: 'three-gaussian-splat',
    navigation: 'orbit + first-person',
    qualityLevels: ['preview', 'standard', 'maximum'],
  },

  // Theatre Mode
  theatreMode: {
    momentMarkers: true,
    videoInScene: true,
    spatialAudio: true,
    transitionEffects: 'theme-matched',
  },

  // Guest Roster
  guestRoster: {
    faceGrid: 'clustered by identity',
    photoGallery: 'per-person best shots',
    searchByName: true,
    shareableLinks: 'per-guest galleries',
  },

  // Theme
  theming: {
    colorPalette: 'extracted from wedding',
    typography: 'theme-matched',
    uiElements: 'aesthetic-consistent',
  },
};
```

## Anti-Patterns

### "All Frames, All the Time"
**Wrong**: Extracting every video frame for 3DGS.
**Why**: Redundant data, 10x slower processing, no quality improvement.
**Right**: 2-3 fps extraction with motion-based keyframe selection.

### "One Giant Scene"
**Wrong**: Training single 3DGS for entire venue.
**Why**: Memory explosion, quality degradation, impossible on consumer hardware.
**Right**: Train per-space, create unified navigation with seamless transitions.

### "Default Clustering Threshold"
**Wrong**: Using default HDBSCAN settings.
**Why**: Wedding photos have varying lighting, makeup, angles—need tuning.
**Right**: Tune per-wedding based on photo count and quality variance.

### "Ignoring Theme"
**Wrong**: Generic white/gray viewer UI for disco wedding.
**Why**: Destroys the personality and joy of the event.
**Right**: Extract and honor the couple's aesthetic choices.

### "Photographer Only"
**Wrong**: Using only professional photos.
**Why**: Misses candid moments, guest perspectives, coverage gaps.
**Right**: Merge professional + guest photos for complete coverage.

## Guest Experience Features

### Shareable Guest Galleries

```
Per-Guest Experience:
├── Personalized link: yourwedding.com/guests/aunt-martha
├── Their best photos (AI-curated)
├── Photos with the couple
├── Group photos they appear in
├── Download options (full-res)
└── "Add to my memories" for their own archives
```

### Collaborative Enhancement

```
Guest Contribution Portal:
├── Upload their own photos
├── Tag themselves in unidentified clusters
├── Correct misidentifications
├── Add names to unknown guests
└── Submit video moments they captured
```

## Output Deliverables

```
wedding-immortalist-output/
├── 3dgs-scenes/
│   ├── ceremony/
│   ├── cocktail/
│   ├── reception/
│   └── unified-navigation.json
├── guest-roster/
│   ├── face-clusters/
│   ├── identity-mapping.json
│   └── per-person-galleries/
├── theatre-mode/
│   ├── moment-markers.json
│   ├── video-segments/
│   └── spatial-audio/
├── web-viewer/
│   ├── index.html
│   ├── theme-config.json
│   └── assets/
└── exports/
    ├── full-resolution-photos/
    ├── guest-gallery-zips/
    └── video-compilations/
```

## Integration Points

- **drone-inspection-specialist**: 3DGS techniques, COLMAP pipeline
- **collage-layout-expert**: Photo arrangement, aesthetic composition
- **color-theory-palette-harmony-expert**: Theme color extraction
- **clip-aware-embeddings**: Photo-text matching for search
- **photo-composition-critic**: Aesthetic quality scoring

---

**Core Philosophy**: A wedding happens once. The memories should live forever. This skill transforms ephemeral moments into an eternal, explorable experience that honors the couple's unique celebration—whether it's a disco dance party, a rustic barn gathering, or two grooms celebrating their love with chosen family.
