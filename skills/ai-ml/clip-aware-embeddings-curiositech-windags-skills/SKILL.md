---
name: clip-aware-embeddings
description: Semantic image-text matching with CLIP and alternatives. Use for image search, zero-shot classification, similarity matching. NOT for counting objects, fine-grained classification (celebrities, car models), spatial reasoning, or compositional queries. Activate on "CLIP", "embeddings", "image similarity", "semantic search", "zero-shot classification", "image-text matching".
allowed-tools: Read,Write,Edit,Bash
category: AI & Machine Learning
tags:
  - clip
  - embeddings
  - vision
  - similarity
  - zero-shot
pairs-with:
  - skill: photo-content-recognition-curation-expert
    reason: Content-aware photo processing
  - skill: collage-layout-expert
    reason: Semantic image matching for layouts
---

# CLIP-Aware Image Embeddings

Smart image-text matching that knows when CLIP works and when to use alternatives.

## MCP Integrations

| MCP | Purpose |
|-----|---------|
| **Firecrawl** | Research latest CLIP alternatives and benchmarks |
| **Hugging Face** (if configured) | Access model cards and documentation |

## Quick Decision Tree

```
Your task:
├─ Semantic search ("find beach images") → CLIP ✓
├─ Zero-shot classification (broad categories) → CLIP ✓
├─ Counting objects → DETR, Faster R-CNN ✗
├─ Fine-grained ID (celebrities, car models) → Specialized model ✗
├─ Spatial relations ("cat left of dog") → GQA, SWIG ✗
└─ Compositional ("red car AND blue truck") → DCSMs, PC-CLIP ✗
```

## When to Use This Skill

✅ **Use for**:
- Semantic image search
- Broad category classification
- Image similarity matching
- Zero-shot tasks on new categories

❌ **Do NOT use for**:
- Counting objects in images
- Fine-grained classification
- Spatial understanding
- Attribute binding
- Negation handling

## Installation

```bash
pip install transformers pillow torch sentence-transformers --break-system-packages
```

**Validation**: Run `python scripts/validate_setup.py`

## Basic Usage

### Image Search

```python
from transformers import CLIPProcessor, CLIPModel
from PIL import Image

model = CLIPModel.from_pretrained("openai/clip-vit-large-patch14")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-large-patch14")

# Embed images
images = [Image.open(f"img{i}.jpg") for i in range(10)]
inputs = processor(images=images, return_tensors="pt")
image_features = model.get_image_features(**inputs)

# Search with text
text_inputs = processor(text=["a beach at sunset"], return_tensors="pt")
text_features = model.get_text_features(**text_inputs)

# Compute similarity
similarity = (image_features @ text_features.T).softmax(dim=0)
```

## Common Anti-Patterns

### Anti-Pattern 1: "CLIP for Everything"

**❌ Wrong**:
```python
# Using CLIP to count cars in an image
prompt = "How many cars are in this image?"
# CLIP cannot count - it will give nonsense results
```

**Why wrong**: CLIP's architecture collapses spatial information into a single vector. It literally cannot count.

**✓ Right**:
```python
from transformers import DetrImageProcessor, DetrForObjectDetection

processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-50")
model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-50")

# Detect objects
results = model(**processor(images=image, return_tensors="pt"))
# Filter for cars and count
car_detections = [d for d in results if d['label'] == 'car']
count = len(car_detections)
```

**How to detect**: If query contains "how many", "count", or numeric questions → Use object detection

---

### Anti-Pattern 2: Fine-Grained Classification

**❌ Wrong**:
```python
# Trying to identify specific celebrities with CLIP
prompts = ["Tom Hanks", "Brad Pitt", "Morgan Freeman"]
# CLIP will perform poorly - not trained for fine-grained face ID
```

**Why wrong**: CLIP trained on coarse categories. Fine-grained faces, car models, flower species require specialized models.

**✓ Right**:
```python
# Use a fine-tuned face recognition model
from transformers import AutoFeatureExtractor, AutoModelForImageClassification

model = AutoModelForImageClassification.from_pretrained(
    "microsoft/resnet-50"  # Then fine-tune on celebrity dataset
)
# Or use dedicated face recognition: ArcFace, CosFace
```

**How to detect**: If query asks to distinguish between similar items in same category → Use specialized model

---

### Anti-Pattern 3: Spatial Understanding

**❌ Wrong**:
```python
# CLIP cannot understand spatial relationships
prompts = [
    "cat to the left of dog",
    "cat to the right of dog"
]
# Will give nearly identical scores
```

**Why wrong**: CLIP embeddings lose spatial topology. "Left" and "right" are treated as bag-of-words.

**✓ Right**:
```python
# Use a spatial reasoning model
# Examples: GQA models, Visual Genome models, SWIG
from swig_model import SpatialRelationModel

model = SpatialRelationModel()
result = model.predict_relation(image, "cat", "dog")
# Returns: "left", "right", "above", "below", etc.
```

**How to detect**: If query contains directional words (left, right, above, under, next to) → Use spatial model

---

### Anti-Pattern 4: Attribute Binding

**❌ Wrong**:
```python
prompts = [
    "red car and blue truck",
    "blue car and red truck"
]
# CLIP often gives similar scores for both
```

**Why wrong**: CLIP cannot bind attributes to objects. It sees "red, blue, car, truck" as a bag of concepts.

**✓ Right - Use PC-CLIP or DCSMs**:
```python
# PC-CLIP: Fine-tuned for pairwise comparisons
from pc_clip import PCCLIPModel

model = PCCLIPModel.from_pretrained("pc-clip-vit-l")
# Or use DCSMs (Dense Cosine Similarity Maps)
```

**How to detect**: If query has multiple objects with different attributes → Use compositional model

---

## Evolution Timeline

### 2021: CLIP Released
- Revolutionary: zero-shot, 400M image-text pairs
- Widely adopted for everything
- Limitations not yet understood

### 2022-2023: Limitations Discovered
- Cannot count objects
- Poor at fine-grained classification
- Fails spatial reasoning
- Can't bind attributes

### 2024: Alternatives Emerge
- **DCSMs**: Preserve patch/token topology
- **PC-CLIP**: Trained on pairwise comparisons
- **SpLiCE**: Sparse interpretable embeddings

### 2025: Current Best Practices
- Use CLIP for what it's good at
- Task-specific models for limitations
- Compositional models for complex queries

**LLM Mistake**: LLMs trained on 2021-2023 data will suggest CLIP for everything because limitations weren't widely known. This skill corrects that.

---

## Validation Script

Before using CLIP, check if it's appropriate:

```bash
python scripts/validate_clip_usage.py \
    --query "your query here" \
    --check-all
```

Returns:
- ✅ CLIP is appropriate
- ❌ Use alternative (with suggestion)

## Task-Specific Guidance

### Image Search (CLIP ✓)
```python
# Good use of CLIP
queries = ["beach", "mountain", "city skyline"]
# Works well for broad semantic concepts
```

### Zero-Shot Classification (CLIP ✓)
```python
# Good: Broad categories
categories = ["indoor", "outdoor", "nature", "urban"]
# CLIP excels at this
```

### Object Counting (CLIP ✗)
```python
# Use object detection instead
from transformers import DetrImageProcessor, DetrForObjectDetection
# See /references/object_detection.md
```

### Fine-Grained Classification (CLIP ✗)
```python
# Use specialized models
# See /references/fine_grained_models.md
```

### Spatial Reasoning (CLIP ✗)
```python
# Use spatial relation models
# See /references/spatial_models.md
```

---

## Troubleshooting

### Issue: CLIP gives unexpected results

**Check**:
1. Is this a counting task? → Use object detection
2. Fine-grained classification? → Use specialized model
3. Spatial query? → Use spatial model
4. Multiple objects with attributes? → Use compositional model

**Validation**:
```bash
python scripts/diagnose_clip_issue.py --image path/to/image --query "your query"
```

### Issue: Low similarity scores

**Possible causes**:
1. Query too specific (CLIP works better with broad concepts)
2. Fine-grained task (not CLIP's strength)
3. Need to adjust threshold

**Solution**: Try broader query or use alternative model

---

## Model Selection Guide

| Model | Best For | Avoid For |
|-------|----------|-----------|
| CLIP ViT-L/14 | Semantic search, broad categories | Counting, fine-grained, spatial |
| DETR | Object detection, counting | Semantic similarity |
| DINOv2 | Fine-grained features | Text-image matching |
| PC-CLIP | Attribute binding, comparisons | General embedding |
| DCSMs | Compositional reasoning | Simple similarity |

## Performance Notes

**CLIP models**:
- ViT-B/32: Fast, lower quality
- ViT-L/14: Balanced (recommended)
- ViT-g-14: Highest quality, slower

**Inference time** (single image, CPU):
- ViT-B/32: ~100ms
- ViT-L/14: ~300ms
- ViT-g-14: ~1000ms

## Further Reading

- `/references/clip_limitations.md` - Detailed analysis of CLIP's failures
- `/references/alternatives.md` - When to use what model
- `/references/compositional_reasoning.md` - DCSMs and PC-CLIP deep dive
- `/scripts/validate_clip_usage.py` - Pre-flight validation tool
- `/scripts/diagnose_clip_issue.py` - Debug unexpected results

---

*See CHANGELOG.md for version history.*
