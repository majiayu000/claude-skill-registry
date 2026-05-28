---
name: photographer-lachapelle
description: Generate images in David LaChapelle's surreal pop art style. Use when users ask for LaChapelle style, pop surrealism, hyper-saturated colors, theatrical staging, baroque maximalism, kitsch aesthetic.
allowed-tools: Bash, Read, Write
---

# David LaChapelle Style Photography

Generate images in the iconic style of David LaChapelle - surreal, hyper-saturated pop art photography with theatrical staging and cultural commentary.

## Style Characteristics

David LaChapelle's photography is defined by:
- **Kitsch pop surrealism** - hyper-real dreamlike compositions
- **Fluorescent saturated colors** - electric, overwhelming color palettes
- **Elaborate theatrical staging** - baroque abundance of elements
- **Cultural commentary** - themes of consumerism, fame, divine vs profane
- **Over-the-top maximalism** - visually opulent excess

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

Always include these elements for authentic LaChapelle style:

```
in the style of David LaChapelle, pop surrealism,
hyper-saturated fluorescent colors, elaborate theatrical set design,
baroque maximalism, surreal dreamlike composition,
kitsch aesthetic, provocative staging, fantasy scenario
```

### Mood Keywords

| Category | Keywords |
|----------|----------|
| Surreal | `dreamlike`, `fantastical`, `hyper-real`, `bizarre`, `otherworldly` |
| Color | `fluorescent`, `neon`, `hyper-saturated`, `electric`, `rainbow` |
| Style | `baroque`, `maximalist`, `kitsch`, `pop art`, `theatrical` |
| Theme | `provocative`, `satirical`, `religious`, `consumerist`, `celebrity` |

## Usage

### cURL

```bash
curl -X POST "https://fal.run/fal-ai/gemini-pro" \
  -H "Authorization: Key $FAL_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "woman as modern Madonna surrounded by fast food and luxury items, in the style of David LaChapelle, pop surrealism, hyper-saturated fluorescent colors, elaborate theatrical set design, baroque maximalism, surreal dreamlike composition, kitsch aesthetic, religious iconography meets consumer culture",
    "aspect_ratio": "3:4",
    "output_format": "png"
  }'
```

### Python

```python
import fal_client

result = fal_client.subscribe(
    "fal-ai/gemini-pro",
    arguments={
        "prompt": """celebrity figure in fantastical underwater scene,
                     in the style of David LaChapelle, pop surrealism,
                     hyper-saturated electric colors, elaborate theatrical staging,
                     baroque abundance of decorative elements,
                     surreal dreamlike floating composition,
                     kitsch aesthetic with mermaids and treasure,
                     provocative fantasy scenario""",
        "aspect_ratio": "2:3",
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
    prompt: `apocalyptic garden of eden with modern celebrities,
             in the style of David LaChapelle, pop surrealism,
             hyper-saturated fluorescent neon colors,
             elaborate theatrical baroque staging,
             surreal dreamlike religious imagery,
             kitsch maximalist aesthetic, bizarre fantasy,
             provocative cultural commentary`,
    aspect_ratio: "16:9",
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

### 1. Pop Culture Satire
```
celebrity figure drowning in brand logos and dollar bills,
in the style of David LaChapelle, pop surrealism,
hyper-saturated neon colors, elaborate theatrical staging,
baroque excess of consumer goods, surreal composition,
kitsch aesthetic, satirical commentary on fame and money,
fluorescent pink and gold palette
```

### 2. Religious Pop Art
```
modern day saint figure with angel wings and halo,
surrounded by fast food and smartphones,
in the style of David LaChapelle, pop surrealism,
hyper-saturated fluorescent colors, baroque religious staging,
surreal dreamlike divine imagery, kitsch aesthetic,
provocative sacred meets profane, elaborate theatrical set
```

### 3. Underwater Fantasy
```
models in elaborate costumes floating underwater,
surrounded by tropical fish and treasure,
in the style of David LaChapelle, pop surrealism,
hyper-saturated aquamarine and coral colors,
elaborate theatrical underwater staging,
surreal dreamlike mermaid fantasy, baroque abundance,
kitsch aesthetic, fantastical scenario
```

### 4. Apocalyptic Beauty
```
fashion model amid burning paradise,
flowers and flames, beauty and destruction,
in the style of David LaChapelle, pop surrealism,
hyper-saturated fiery oranges and lush greens,
elaborate theatrical apocalyptic staging,
surreal dreamlike garden of eden burning,
baroque maximalism, provocative environmental commentary
```

### 5. Celebrity Excess
```
figure reclining on mountain of luxury goods,
designer bags, jewelry, champagne bottles,
in the style of David LaChapelle, pop surrealism,
hyper-saturated gold and pink fluorescent colors,
elaborate theatrical staging of opulence,
surreal dreamlike excess, baroque maximalism,
kitsch satirical take on wealth and celebrity
```

## Tips for Best Results

1. **Maximize color** - Use "fluorescent", "neon", "hyper-saturated", "electric colors"
2. **Go theatrical** - Add "elaborate staging", "baroque set design", "maximalist"
3. **Embrace surrealism** - Include "dreamlike", "fantastical", "bizarre", "otherworldly"
4. **Layer elements** - LaChapelle compositions are busy; describe multiple elements
5. **Add commentary** - Reference themes like "consumer culture", "celebrity worship", "sacred vs profane"
6. **Think kitsch** - Use "pop art", "kitsch aesthetic", "over-the-top"

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `401 Unauthorized` | Invalid FAL_KEY | Verify key at fal.ai dashboard |
| `429 Too Many Requests` | Rate limit exceeded | Wait 60 seconds, retry |
| `400 Bad Request` | Invalid parameters | Check aspect_ratio format (e.g., "3:4") |
| `500 Server Error` | API temporary issue | Retry after 30 seconds |
| `Timeout` | Generation taking too long | Simplify prompt or reduce resolution |

## Reference

David LaChapelle (born 1963) is an American photographer and director known for his surreal, hyper-saturated images blending pop culture, religious iconography, and social commentary. His work has appeared in magazines including Interview, Rolling Stone, and Vogue.

**Key Influences**: Pop Art, Baroque painting, religious iconography
**Signature**: Fluorescent colors, theatrical staging, cultural satire
