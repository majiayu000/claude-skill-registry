---
name: ai-image-effects
description: Apply AI visual effects including Illusion Diffusion ($0.006), FLUX Fill Pro accessory replacement ($0.05), and SAM object detection (<$0.01). Use when adding AI effects, replacing image elements, detecting objects, or applying visual transformations.
allowed-tools: Read, Write, Bash(python:*)
model: claude-sonnet-4-20250514
---

# AI Image Effects

Professional AI-powered image effects using Replicate models - Illusion Diffusion, FLUX Fill Pro, and Meta SAM-2.

## Overview

Three powerful AI effects for image transformation:

| Effect | Model | Cost | Use Case |
|--------|-------|------|----------|
| **Illusion Diffusion** | ControlNet | $0.006/image | Visual illusions, patterns |
| **FLUX Fill Pro** | Black Forest Labs | $0.05/image | Smart inpainting, accessory replacement |
| **SAM Detector** | Meta SAM-2 | <$0.01/detection | Object detection, segmentation |

## Quick Start

### 1. Configure Replicate API

```bash
# Set API token
export REPLICATE_API_TOKEN="r8_xxxxxxxxxxxxx"

# Check balance
python scripts/check_credit.py
```

### 2. Run Effects

```python
# Illusion Diffusion
from src.illusion_diffusion import IllusionDiffusion

illusion = IllusionDiffusion()
result = illusion.apply(
    image_path="input.png",
    prompt="spiral pattern",
    strength=1.5
)

# FLUX Fill Pro
from src.flux_fill_pro import FluxFillPro

flux = FluxFillPro()
result = flux.replace_accessory(
    image_path="milady.png",
    accessory_type="hat",
    new_description="red baseball cap"
)

# SAM Detector
from src.sam_detector import SAMDetector

sam = SAMDetector()
bbox = sam.detect_accessory(
    image_path="milady.png",
    accessory_type="glasses"
)
```

## Effect 1: Illusion Diffusion

### What It Does

Creates optical illusions and pattern effects using ControlNet. The AI reshapes the image while maintaining recognizability from a distance.

### Use Cases

- **Spiral patterns** - Make image appear as spiral
- **QR codes** - Embed QR codes in artwork
- **Hidden text** - Text visible from afar
- **Geometric patterns** - Hexagons, triangles, waves
- **Artistic effects** - Creative distortions

### Basic Usage

```python
from src.illusion_diffusion import IllusionDiffusion

illusion = IllusionDiffusion()

# Simple spiral effect
result = illusion.apply(
    image_path="milady.png",
    prompt="spiral optical illusion"
)
# Cost: $0.006
```

### Advanced Parameters

```python
result = illusion.apply(
    image_path="milady.png",
    prompt="concentric circles optical illusion",
    control_guidance=1.5,        # 0.5-5.0 (how strong the effect)
    controlnet_conditioning=1.2, # 0.5-2.0 (pattern strength)
    steps=50,                    # 20-100 (quality vs speed)
    guidance_scale=7.5           # 0-20 (prompt adherence)
)
```

**Parameter Guide**:
- `control_guidance`: Higher = stronger illusion effect
- `controlnet_conditioning`: Higher = more visible pattern
- `steps`: More steps = higher quality (but slower)
- `guidance_scale`: Higher = follows prompt more closely

### Pattern Ideas

```python
# Spiral
illusion.apply(image, "fibonacci spiral pattern")

# Geometric
illusion.apply(image, "hexagonal tessellation")

# Wave
illusion.apply(image, "concentric wave pattern")

# QR Code
illusion.apply(image, "QR code pattern", control_guidance=2.0)

# Text
illusion.apply(image, "hidden text 'WAGMI' optical illusion")
```

### Cost Optimization

```python
# Lower quality (faster, cheaper)
result = illusion.apply(
    image,
    prompt="spiral",
    steps=20,              # Faster
    control_guidance=1.0   # Standard strength
)
# Still costs $0.006 per image

# Batch processing
results = illusion.batch_apply(
    images=["img1.png", "img2.png", "img3.png"],
    prompt="spiral pattern"
)
# Cost: $0.006 × 3 = $0.018
```

## Effect 2: FLUX Fill Pro

### What It Does

AI inpainting and accessory replacement. Intelligently fills/replaces parts of an image with new content matching the description.

### Use Cases

- **Replace accessories** - Swap hats, glasses, earrings
- **Change clothes** - Modify shirts, dresses
- **Add elements** - Insert new objects
- **Remove elements** - Inpaint to remove objects
- **Style transfer** - Change artistic style of regions

### Basic Usage

```python
from src.flux_fill_pro import FluxFillPro

flux = FluxFillPro()

# Replace hat
result = flux.replace_accessory(
    image_path="milady.png",
    accessory_type="hat",
    new_description="red baseball cap"
)
# Cost: $0.05
```

### Accessory Types

Supports 8 predefined accessory categories:

```python
ACCESSORY_TYPES = {
    "hat": (300, 180, 80),         # (y, height, width %)
    "glasses": (420, 60, 50),
    "earrings": (480, 80, 70),
    "necklace": (640, 120, 60),
    "scarf": (550, 150, 70),
    "clothes": (700, 400, 90),
    "background": (0, 1250, 100),
    "other": None  # Manual bbox
}
```

### Advanced Usage

```python
# Custom bounding box
result = flux.replace_region(
    image_path="milady.png",
    bbox=(100, 200, 300, 400),  # (x, y, width, height)
    prompt="cool futuristic visor"
)

# With mask image
result = flux.inpaint(
    image_path="milady.png",
    mask_path="mask.png",        # White = replace, Black = keep
    prompt="blue sunglasses"
)

# Batch replace multiple accessories
result = flux.batch_replace(
    image_path="milady.png",
    replacements=[
        {"type": "hat", "description": "cowboy hat"},
        {"type": "glasses", "description": "round sunglasses"}
    ]
)
# Cost: $0.05 × 2 = $0.10
```

### Quality Parameters

```python
result = flux.replace_accessory(
    image_path="milady.png",
    accessory_type="hat",
    new_description="red beanie",
    strength=0.8,           # 0-1 (how much to change)
    guidance=7.5,           # Prompt adherence
    steps=30,               # Generation steps
    seed=42                 # Reproducibility
)
```

### Best Practices

1. **Be specific in descriptions**
   ```python
   # ❌ Vague
   "hat"

   # ✅ Specific
   "red baseball cap with white logo"
   ```

2. **Use consistent lighting**
   ```python
   "blue sunglasses with same lighting as original image"
   ```

3. **Match art style**
   ```python
   "anime-style pink beret matching the character's aesthetic"
   ```

## Effect 3: SAM Detector

### What It Does

Meta's Segment Anything Model (SAM-2) for precise object detection and bounding box extraction. Used to automatically find accessories before replacement.

### Use Cases

- **Auto-detect accessories** - Find hats, glasses automatically
- **Precise segmentation** - Get exact object boundaries
- **Multi-object detection** - Detect all objects in image
- **Smart cropping** - Crop to detected objects
- **Integration with FLUX** - Auto-detect then replace

### Basic Usage

```python
from src.sam_detector import SAMDetector

sam = SAMDetector()

# Detect accessory
bbox = sam.detect_accessory(
    image_path="milady.png",
    accessory_type="hat"
)
# Returns: (x, y, width, height) or None
# Cost: <$0.01
```

### Supported Accessories

```python
ACCESSORY_CATEGORIES = {
    "hat": ["帽子", "hat", "cap", "beanie", "beret"],
    "glasses": ["眼镜", "glasses", "sunglasses", "spectacles"],
    "earrings": ["耳环", "earring", "earrings"],
    "necklace": ["项链", "necklace", "chain"],
    "scarf": ["围巾", "scarf", "bandana"],
    "clothes": ["衣服", "shirt", "dress", "top"],
    "face_decoration": ["面部装饰", "sticker", "mark"],
    "overlay": ["特效", "effect", "overlay"]
}
```

### Smart Detection

```python
# Auto-detect with smart positioning
result = sam.smart_detect(
    image_path="milady.png",
    accessory_type="glasses",
    use_position_hints=True  # Uses expected position for better accuracy
)

# Detect with confidence threshold
bbox, confidence = sam.detect_with_confidence(
    image_path="milady.png",
    accessory_type="hat",
    min_confidence=0.7
)
```

### Caching System

SAM results are cached for 7 days to save costs:

```python
# First call - runs SAM ($0.01)
bbox1 = sam.detect_accessory("milady.png", "hat")

# Second call - uses cache (FREE)
bbox2 = sam.detect_accessory("milady.png", "hat")

# Clear cache if needed
sam.clear_cache()

# Check cache stats
stats = sam.get_cache_stats()
# Returns: {"hits": 150, "misses": 50, "savings": "$0.50"}
```

### Integration with FLUX

```python
# Combo: SAM detection + FLUX replacement
from src.sam_detector import SAMDetector
from src.flux_fill_pro import FluxFillPro

sam = SAMDetector()
flux = FluxFillPro()

# Step 1: Detect hat automatically
bbox = sam.detect_accessory("milady.png", "hat")

# Step 2: Replace with FLUX
if bbox:
    result = flux.replace_region(
        image_path="milady.png",
        bbox=bbox,
        prompt="red baseball cap"
    )
# Total cost: <$0.01 + $0.05 = ~$0.05
```

### Advanced Features

```python
# Get all detected objects
all_objects = sam.detect_all_objects("milady.png")
# Returns: [{"bbox": (x,y,w,h), "label": "hat", "confidence": 0.95}, ...]

# Get segmentation mask (not just bbox)
mask = sam.get_segmentation_mask("milady.png", "glasses")
# Returns: PIL Image (binary mask)

# Batch detection
bboxes = sam.batch_detect(
    images=["img1.png", "img2.png"],
    accessory_type="hat"
)
```

## Complete Workflow Example

### Example 1: Smart Accessory Replacement

```python
from src.sam_detector import SAMDetector
from src.flux_fill_pro import FluxFillPro

sam = SAMDetector()
flux = FluxFillPro()

# Auto-detect and replace
def smart_replace(image_path, accessory_type, new_description):
    """Detect accessory with SAM, replace with FLUX"""

    # Step 1: Detect
    print(f"Detecting {accessory_type}...")
    bbox = sam.detect_accessory(image_path, accessory_type)

    if not bbox:
        print(f"No {accessory_type} detected, using default position")
        # Fallback to default
        return flux.replace_accessory(
            image_path, accessory_type, new_description
        )

    # Step 2: Replace
    print(f"Replacing {accessory_type} with: {new_description}")
    result = flux.replace_region(
        image_path=image_path,
        bbox=bbox,
        prompt=new_description
    )

    return result

# Use it
result = smart_replace(
    "milady_5050.png",
    "glasses",
    "cool futuristic visor with neon blue glow"
)
result.save("output.png")
```

### Example 2: Multi-Effect Pipeline

```python
from src.illusion_diffusion import IllusionDiffusion
from src.flux_fill_pro import FluxFillPro

illusion = IllusionDiffusion()
flux = FluxFillPro()

# Step 1: Replace accessories
print("Replacing hat...")
img = flux.replace_accessory(
    "milady.png",
    "hat",
    "red baseball cap"
)
img.save("step1.png")

# Step 2: Apply illusion effect
print("Applying spiral effect...")
final = illusion.apply(
    "step1.png",
    prompt="spiral optical illusion"
)
final.save("final.png")

print("Total cost: $0.05 + $0.006 = $0.056")
```

### Example 3: Batch Processing

```python
from src.flux_fill_pro import FluxFillPro

flux = FluxFillPro()

# Process multiple images
images = ["milady_1.png", "milady_2.png", "milady_3.png"]
accessories = ["hat", "glasses", "hat"]
descriptions = [
    "cowboy hat",
    "heart-shaped sunglasses",
    "blue beanie"
]

results = []
for img, acc, desc in zip(images, accessories, descriptions):
    print(f"Processing {img}...")
    result = flux.replace_accessory(img, acc, desc)
    results.append(result)

# Cost: $0.05 × 3 = $0.15
```

## Configuration

### Replicate Config

Located in: `config/replicate_config.py`

```python
# Model versions
MODELS = {
    "illusion": "monster-labs/control_v1p_sd15_qrcode_monster:...",
    "flux_fill": "black-forest-labs/flux-fill-pro",
    "sam": "meta/sam-2:..."
}

# Default parameters
ILLUSION_DEFAULTS = {
    "control_guidance": 1.5,
    "steps": 50
}

FLUX_DEFAULTS = {
    "strength": 0.8,
    "guidance": 7.5,
    "steps": 30
}
```

### Cost Management

```bash
# Check current balance
python scripts/check_credit.py

# Output:
# Replicate Balance: $10.50
# Recent usage: $2.30 (last 24h)
```

### Rate Limiting

```python
# Built-in rate limiting to avoid API overload
flux = FluxFillPro(max_concurrent=3)  # Max 3 simultaneous requests
```

## Cost Calculator

### Estimate Costs

```python
from src.cost_calculator import CostCalculator

calc = CostCalculator()

# Single operation
cost = calc.estimate(
    effect="flux_fill",
    count=1
)
# Returns: $0.05

# Batch operation
cost = calc.estimate_batch([
    {"effect": "illusion", "count": 10},
    {"effect": "flux_fill", "count": 5},
    {"effect": "sam", "count": 20}
])
# Returns: $0.06 + $0.25 + $0.20 = $0.51
```

### Monthly Budget Planning

```python
# Plan monthly usage
monthly_plan = {
    "illusion": 100,      # 100 images
    "flux_fill": 50,      # 50 replacements
    "sam": 200            # 200 detections
}

cost = calc.monthly_estimate(monthly_plan)
# Returns: $0.60 + $2.50 + $2.00 = $5.10/month
```

## Error Handling

### Common Issues

**1. Insufficient credits**
```python
try:
    result = flux.replace_accessory(...)
except InsufficientCreditsError:
    print("Please add credits to Replicate account")
```

**2. Model timeout**
```python
# Increase timeout for slow models
flux = FluxFillPro(timeout=300)  # 5 minutes
```

**3. Invalid bounding box**
```python
# Validate bbox before using
bbox = sam.detect_accessory(image, "hat")
if bbox and flux.validate_bbox(bbox):
    result = flux.replace_region(image, bbox, prompt)
```

## Best Practices

1. **Use SAM before FLUX** - Auto-detection is more accurate than hardcoded positions
2. **Cache SAM results** - Saves 50-70% on detection costs
3. **Batch when possible** - Process multiple images in one session
4. **Monitor spending** - Check balance regularly
5. **Test with low steps** - Use steps=20 for testing, steps=50 for production
6. **Be specific with prompts** - Better descriptions = better results

## Advanced Tips

### Combine Multiple Effects

```python
# Illusion + FLUX pipeline
def create_custom_illusion(image_path):
    # Replace accessories first
    img = flux.replace_accessory(image_path, "hat", "cool hat")

    # Then apply illusion
    final = illusion.apply(img, "spiral pattern")

    return final
```

### Quality vs Cost Trade-off

```python
# Production quality (higher cost, slower)
result = flux.replace_accessory(
    image, "hat", "red cap",
    steps=50,
    guidance=10.0
)

# Draft quality (lower cost, faster)
result = flux.replace_accessory(
    image, "hat", "red cap",
    steps=20,
    guidance=7.0
)
# Both cost $0.05, but draft is 2x faster
```

## Related Documentation

- [ILLUSION_GUIDE.md](ILLUSION_GUIDE.md) - Detailed illusion patterns
- [FLUX_FILL_GUIDE.md](FLUX_FILL_GUIDE.md) - FLUX best practices
- [SAM_DETECTOR_GUIDE.md](SAM_DETECTOR_GUIDE.md) - SAM detection guide
- [COST_CALCULATOR.md](COST_CALCULATOR.md) - Budget planning

## Related Skills

- [milady-meme-generator](../milady-meme-generator/SKILL.md) - Generate base images
- [lark-bot-integration](../lark-bot-integration/SKILL.md) - Use in Lark bot

---

**Total Costs Summary**:
- Illusion Diffusion: $0.006 per image
- FLUX Fill Pro: $0.05 per image
- SAM Detection: <$0.01 per detection
- Combined (SAM + FLUX): ~$0.05 per image
