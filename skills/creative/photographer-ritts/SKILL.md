---
name: photographer-ritts
description: Generate images in Herb Ritts' sculptural black and white style. Use when users ask for Ritts style, classical Greek aesthetic, sculptural body photography, California golden hour, minimalist athletic portraits.
allowed-tools: Bash, Read, Write
---

# Herb Ritts Style Photography

Generate images in the iconic style of Herb Ritts - sculptural, minimalist photography that treats the human form like classical Greek marble.

## Style Characteristics

Herb Ritts defined a distinctive aesthetic through:
- **Sculptural forms** - bodies treated like classical Greek marble statues
- **California golden hour** - warm, natural outdoor illumination
- **Minimalist elegance** - uncluttered frames, clean lines, essential elements only
- **Graphic bold contours** - strong shadows defining form and shape
- **Desert/beach aesthetic** - outdoor locations with stark, simple backgrounds

## Prerequisites

Set your fal.ai API key:
```bash
export FAL_KEY="your-fal-api-key"
```

## API Endpoint

```
POST https://fal.run/fal-ai/gemini-pro
```

## Prompt Construction

### Core Style Elements

Always include these elements for authentic Ritts style:

```
in the style of Herb Ritts, black and white photography,
sculptural lighting, California golden hour, classical Greek influence,
strong shadows, clean lines, minimalist composition, athletic form
```

### Mood Keywords

| Category | Keywords |
|----------|----------|
| Form | `sculptural`, `athletic`, `statuesque`, `muscular`, `elegant` |
| Light | `golden hour`, `California sun`, `backlighting`, `rim light` |
| Aesthetic | `classical`, `Greek`, `minimalist`, `heroic`, `eternal` |
| Setting | `desert`, `beach`, `outdoor`, `stark background`, `negative space` |

## Usage

### cURL

```bash
curl -X POST "https://fal.run/fal-ai/gemini-pro" \
  -H "Authorization: Key $FAL_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "athletic male figure in desert landscape, in the style of Herb Ritts, black and white photography, sculptural lighting, California golden hour, classical Greek influence, strong shadows defining muscles, clean lines, minimalist composition, heroic pose",
    "aspect_ratio": "2:3",
    "output_format": "png"
  }'
```

### Python

```python
import fal_client

result = fal_client.subscribe(
    "fal-ai/gemini-pro",
    arguments={
        "prompt": """dancer in flowing fabric on beach, in the style of Herb Ritts,
                     black and white photography, sculptural lighting, golden hour,
                     classical Greek marble aesthetic, dramatic backlighting,
                     silhouette with rim light, minimalist composition,
                     eternal beauty, elegant movement captured""",
        "aspect_ratio": "3:4",
        "output_format": "png"
    }
)
print(result["images"][0]["url"])
```

### JavaScript

```javascript
import { fal } from "@fal-ai/client";

const result = await fal.subscribe("fal-ai/gemini-pro", {
  input: {
    prompt: `nude figure study, artistic, in the style of Herb Ritts,
             black and white photography, sculptural form,
             strong shadows carving the body, California sunlight,
             classical Greek statue quality, minimalist desert background,
             athletic physique, timeless elegance`,
    aspect_ratio: "4:5",
    output_format: "png"
  }
});
console.log(result.images[0].url);
```

## Response Format

```json
{
  "images": [
    {
      "url": "https://fal.media/files/...",
      "content_type": "image/png"
    }
  ]
}
```

## Examples

### 1. Classic Ritts Silhouette
```
athletic figure silhouette against bright sky,
in the style of Herb Ritts, black and white photography,
dramatic backlighting, golden hour, perfect body contours,
stark minimalist composition, California desert setting,
sculptural shadows, heroic pose, classical beauty
```

### 2. Beach Editorial
```
model lying on wet sand, ocean waves,
in the style of Herb Ritts, black and white photography,
natural sunlight sculpting form, water droplets on skin,
clean lines and negative space, athletic elegance,
minimalist beach aesthetic, sensual yet classical,
strong graphic shadows
```

### 3. Dynamic Movement
```
dancer mid-leap against plain sky,
in the style of Herb Ritts, black and white photography,
frozen motion, sculptural form in flight,
California golden hour backlighting, athletic grace,
classical Greek influence, dramatic shadows,
minimalist composition, powerful elegance
```

### 4. Portrait Study
```
close-up portrait with strong bone structure,
in the style of Herb Ritts, black and white photography,
sculptural lighting from side, sharp cheekbones,
classical beauty like Greek sculpture,
clean background, high contrast shadows,
timeless and elegant, California natural light
```

### 5. Couple or Group
```
two figures intertwined, artistic nude study,
in the style of Herb Ritts, black and white photography,
bodies as sculptural forms, complementary poses,
California outdoor lighting, marble-like skin tones,
minimalist desert background, classical composition,
eternal beauty, strong graphic shadows
```

## Tips for Best Results

1. **Emphasize form** - Use "sculptural", "athletic", "statuesque", "muscular contours"
2. **Golden hour lighting** - Specify "California sun", "golden hour", "backlighting", "rim light"
3. **Minimalist settings** - Add "desert", "beach", "stark background", "negative space"
4. **Classical references** - Include "Greek sculpture", "classical beauty", "marble-like"
5. **Strong shadows** - Use "shadows defining form", "high contrast", "bold contours"
6. **Simple compositions** - Keep backgrounds minimal, focus on the figure

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `401 Unauthorized` | Invalid FAL_KEY | Verify key at fal.ai dashboard |
| `429 Too Many Requests` | Rate limit exceeded | Wait 60 seconds, retry |
| `400 Bad Request` | Invalid parameters | Check aspect_ratio format (e.g., "2:3") |
| `500 Server Error` | API temporary issue | Retry after 30 seconds |
| `Timeout` | Generation taking too long | Simplify prompt or reduce resolution |

## Reference

Herb Ritts (1952-2002) was an American fashion photographer and director known for his striking black-and-white images that combined classical Greek aesthetics with California sun. He photographed celebrities including Madonna, Cindy Crawford, and Naomi Campbell.

**Key Influences**: Classical Greek sculpture, California landscape
**Signature**: Sculptural lighting, athletic forms, minimalist outdoor settings
