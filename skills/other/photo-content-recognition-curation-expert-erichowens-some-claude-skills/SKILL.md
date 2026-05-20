---
name: photo-content-recognition-curation-expert
description: Expert in photo content recognition, intelligent curation, and quality filtering. Specializes in face/animal/place recognition, perceptual hashing for de-duplication, screenshot/meme detection, burst photo selection, and quick indexing strategies. Activate on 'face recognition', 'face clustering', 'perceptual hash', 'near-duplicate', 'burst photo', 'screenshot detection', 'photo curation', 'photo indexing', 'NSFW detection', 'pet recognition', 'DINOHash', 'HDBSCAN faces'. NOT for GPS-based location clustering (use event-detection-temporal-intelligence-expert), color palette extraction (use color-theory-palette-harmony-expert), semantic image-text matching (use clip-aware-embeddings), or video analysis/frame extraction.
allowed-tools: Read,Write,Edit,Bash,Grep,Glob,mcp__firecrawl__firecrawl_search,WebFetch
category: AI & Machine Learning
tags:
  - face-recognition
  - deduplication
  - curation
  - indexing
  - nsfw
pairs-with:
  - skill: event-detection-temporal-intelligence-expert
    reason: Temporal context for photos
  - skill: wedding-immortalist
    reason: Curate wedding photo collections
---

# Photo Content Recognition & Curation Expert

Expert in photo content analysis and intelligent curation. Combines classical computer vision with modern deep learning for comprehensive photo analysis.

## When to Use This Skill

✅ **Use for:**
- Face recognition and clustering (identifying important people)
- Animal/pet detection and clustering
- Near-duplicate detection using perceptual hashing (DINOHash, pHash, dHash)
- Burst photo selection (finding best frame from 10-50 shots)
- Screenshot vs photo classification
- Meme/download filtering
- NSFW content detection
- Quick indexing for large photo libraries (10K+)
- Aesthetic quality scoring (NIMA)

❌ **NOT for:**
- GPS-based location clustering → `event-detection-temporal-intelligence-expert`
- Color palette extraction → `color-theory-palette-harmony-expert`
- Semantic image-text matching → `clip-aware-embeddings`
- Video analysis or frame extraction

## Quick Decision Tree

```
What do you need to recognize/filter?
│
├─ Duplicate photos? ─────────────────────────────── Perceptual Hashing
│   ├─ Exact duplicates? ──────────────────────────── dHash (fastest)
│   ├─ Brightness/contrast changes? ───────────────── pHash (DCT-based)
│   ├─ Heavy crops/compression? ───────────────────── DINOHash (2025 SOTA)
│   └─ Production system? ─────────────────────────── Hybrid (pHash → DINOHash)
│
├─ People in photos? ─────────────────────────────── Face Clustering
│   ├─ Known thresholds? ──────────────────────────── Apple-style Agglomerative
│   └─ Unknown data distribution? ─────────────────── HDBSCAN
│
├─ Pets/Animals? ─────────────────────────────────── Pet Recognition
│   ├─ Detection? ─────────────────────────────────── YOLOv8
│   └─ Individual clustering? ─────────────────────── CLIP + HDBSCAN
│
├─ Best from burst? ──────────────────────────────── Burst Selection
│   └─ Score: sharpness + face quality + aesthetics
│
└─ Filter junk? ──────────────────────────────────── Content Detection
    ├─ Screenshots? ───────────────────────────────── Multi-signal classifier
    └─ NSFW? ──────────────────────────────────────── Safety classifier
```

---

## Core Concepts

### 1. Perceptual Hashing for Near-Duplicate Detection

**Problem:** Camera bursts, re-saved images, and minor edits create near-duplicates.

**Solution:** Perceptual hashes generate similar values for visually similar images.

**Method Comparison:**

| Method | Speed | Robustness | Best For |
|--------|-------|------------|----------|
| dHash | Fastest | Low | Exact duplicates |
| pHash | Fast | Medium | Brightness/contrast changes |
| DINOHash | Slower | High | Heavy crops, compression |
| Hybrid | Medium | Very High | Production systems |

**Hybrid Pipeline (2025 Best Practice):**
1. **Stage 1:** Fast pHash filtering (eliminates obvious non-duplicates)
2. **Stage 2:** DINOHash refinement (accurate detection)
3. **Stage 3:** Optional Siamese ViT verification

**Hamming Distance Thresholds:**
- Conservative: ≤5 bits different = duplicates
- Aggressive: ≤10 bits different = duplicates

→ **Deep dive**: `references/perceptual-hashing.md`

---

### 2. Face Recognition & Clustering

**Goal:** Group photos by person without user labeling.

**Apple Photos Strategy (2021-2025):**
1. Extract face + upper body embeddings (FaceNet, 512-dim)
2. Two-pass agglomerative clustering
3. Conservative first pass (threshold=0.4, high precision)
4. HAC second pass (threshold=0.6, increase recall)
5. Incremental updates for new photos

**HDBSCAN Alternative:**
- No threshold tuning required
- Robust to noise
- Better for unknown data distributions

**Parameters:**

| Setting | Agglomerative | HDBSCAN |
|---------|---------------|---------|
| Pass 1 threshold | 0.4 (cosine) | - |
| Pass 2 threshold | 0.6 (cosine) | - |
| Min cluster size | - | 3 photos |
| Metric | cosine | cosine |

→ **Deep dive**: `references/face-clustering.md`

---

### 3. Burst Photo Selection

**Problem:** Burst mode creates 10-50 nearly identical photos.

**Multi-Criteria Scoring:**

| Criterion | Weight | Measurement |
|-----------|--------|-------------|
| Sharpness | 30% | Laplacian variance |
| Face Quality | 35% | Eyes open, smiling, face sharpness |
| Aesthetics | 20% | NIMA score |
| Position | 10% | Middle frames bonus |
| Exposure | 5% | Histogram clipping check |

**Burst Detection:** Photos within 0.5 seconds of each other.

→ **Deep dive**: `references/content-detection.md`

---

### 4. Screenshot Detection

**Multi-Signal Approach:**

| Signal | Confidence | Description |
|--------|------------|-------------|
| UI elements | 0.85 | Status bars, buttons detected |
| Perfect rectangles | 0.75 | &gt;5 UI buttons (90° angles) |
| High text | 0.70 | &gt;25% text coverage (OCR) |
| No camera EXIF | 0.60 | Missing Make/Model/Lens |
| Device aspect | 0.60 | Exact phone screen ratio |
| Perfect sharpness | 0.50 | &gt;2000 Laplacian variance |

**Decision:** Confidence &gt;0.6 = screenshot

→ **Deep dive**: `references/content-detection.md`

---

### 5. Quick Indexing Pipeline

**Goal:** Index 10K+ photos efficiently with caching.

**Features Extracted:**
- Perceptual hashes (de-duplication)
- Face embeddings (people clustering)
- CLIP embeddings (semantic search)
- Color palettes
- Aesthetic scores

**Performance (10K photos, M1 MacBook Pro):**

| Operation | Time |
|-----------|------|
| Perceptual hashing | 2 min |
| CLIP embeddings | 3 min (GPU) |
| Face detection | 4 min |
| Color palettes | 1 min |
| Aesthetic scoring | 2 min (GPU) |
| Clustering + dedup | 1 min |
| **Total (first run)** | **~13 min** |
| **Incremental** | **&lt;1 min** |

→ **Deep dive**: `references/photo-indexing.md`

---

## Common Anti-Patterns

### Anti-Pattern: Euclidean Distance for Face Embeddings

**What it looks like:**
```python
distance = np.linalg.norm(embedding1 - embedding2)  # WRONG
```

**Why it's wrong:** Face embeddings are normalized; cosine similarity is the correct metric.

**What to do instead:**
```python
from scipy.spatial.distance import cosine
distance = cosine(embedding1, embedding2)  # Correct
```

### Anti-Pattern: Fixed Clustering Thresholds

**What it looks like:** Using same distance threshold for all face clusters.

**Why it's wrong:** Different people have varying intra-class variance (twins vs. diverse ages).

**What to do instead:** Use HDBSCAN for automatic threshold discovery, or two-pass clustering with conservative + relaxed passes.

### Anti-Pattern: Raw Pixel Comparison for Duplicates

**What it looks like:**
```python
is_duplicate = np.allclose(img1, img2)  # WRONG
```

**Why it's wrong:** Re-saved JPEGs, crops, brightness changes create pixel differences.

**What to do instead:** Perceptual hashing (pHash or DINOHash) with Hamming distance.

### Anti-Pattern: Sequential Face Detection

**What it looks like:** Processing faces one photo at a time without batching.

**Why it's wrong:** GPU underutilization, 10x slower than batched.

**What to do instead:** Batch process images (batch_size=32) with GPU acceleration.

### Anti-Pattern: No Confidence Filtering

**What it looks like:**
```python
for face in all_detected_faces:
    cluster(face)  # No filtering
```

**Why it's wrong:** Low-confidence detections create noise clusters (hands, objects).

**What to do instead:** Filter by confidence (threshold 0.9 for faces).

### Anti-Pattern: Forcing Every Photo into Clusters

**What it looks like:** Assigning noise points to nearest cluster.

**Why it's wrong:** Solo appearances shouldn't pollute person clusters.

**What to do instead:** HDBSCAN/DBSCAN naturally identifies noise (label=-1). Keep noise separate.

---

## Quick Start

```python
from photo_curation import PhotoCurationPipeline

pipeline = PhotoCurationPipeline()

# Index photo library
index = pipeline.index_library('/path/to/photos')

# De-duplicate
duplicates = index.find_duplicates()
print(f"Found {len(duplicates)} duplicate groups")

# Cluster faces
face_clusters = index.cluster_faces()
print(f"Found {len(face_clusters)} people")

# Select best from bursts
best_photos = pipeline.select_best_from_bursts(index)

# Filter screenshots
real_photos = pipeline.filter_screenshots(index)

# Curate for collage
collage_photos = pipeline.curate_for_collage(index, target_count=100)
```

---

## Python Dependencies

```
torch transformers facenet-pytorch ultralytics hdbscan opencv-python scipy numpy scikit-learn pillow pytesseract
```

---

## Integration Points

- **event-detection-temporal-intelligence-expert**: Provides temporal event clustering for event-aware curation
- **color-theory-palette-harmony-expert**: Extracts color palettes for visual diversity
- **collage-layout-expert**: Receives curated photos for assembly
- **clip-aware-embeddings**: Provides CLIP embeddings for semantic search and DeepDBSCAN

---

## References

1. **DINOHash (2025)**: "Adversarially Fine-Tuned DINOv2 Features for Perceptual Hashing"
2. **Apple Photos (2021)**: "Recognizing People in Photos Through Private On-Device ML"
3. **HDBSCAN**: "Hierarchical Density-Based Spatial Clustering" (2013-2025)
4. **Perceptual Hashing**: dHash (Neal Krawetz), DCT-based pHash

---

**Version**: 2.0.0
**Last Updated**: November 2025
