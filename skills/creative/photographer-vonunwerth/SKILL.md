---
name: photographer-vonunwerth
description: Generate images in Ellen von Unwerth's playful vintage style. Use when users ask for von Unwerth style, playful sensuality, vintage film noir, whimsical feminine photography, retro glamour, narrative storytelling.
allowed-tools: Bash, Read, Write
---

# Ellen von Unwerth Style Photography

Generate images in the iconic style of Ellen von Unwerth - playful, vintage-inspired photography celebrating feminine empowerment and whimsical sensuality.

## Style Characteristics

Ellen von Unwerth's photography is defined by:
- **Playful sensuality** - whimsical, flirtatious energy
- **Vintage cinematic** - film noir influences, classic Hollywood glamour
- **Narrative storytelling** - each image tells a story with characters
- **Empowered femininity** - women as subjects, not objects
- **High-energy dynamism** - movement, spontaneity, joy

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

Always include these elements for authentic von Unwerth style:

```
in the style of Ellen von Unwerth, playful fashion photography,
vintage cinematic aesthetic, film noir lighting, narrative scene,
whimsical and flirtatious mood, feminine empowerment,
retro glamour, storytelling composition, dramatic light and shadow
```

### Mood Keywords

| Category | Keywords |
|----------|----------|
| Energy | `playful`, `flirtatious`, `whimsical`, `mischievous`, `joyful` |
| Style | `vintage`, `retro`, `film noir`, `Hollywood`, `cinematic` |
| Femininity | `empowering`, `sensual`, `feminine`, `provocative`, `confident` |
| Narrative | `storytelling`, `character`, `scene`, `dramatic`, `theatrical` |

## Usage

### cURL

```bash
curl -X POST "https://fal.run/fal-ai/gemini-pro" \
  -H "Authorization: Key $FAL_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "woman in vintage lingerie looking mischievously over shoulder, in the style of Ellen von Unwerth, playful fashion photography, vintage cinematic aesthetic, film noir dramatic lighting, whimsical flirtatious mood, feminine empowerment, retro Hollywood glamour, storytelling narrative scene",
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
        "prompt": """two women in 1950s style dresses, sharing secret and laughing,
                     in the style of Ellen von Unwerth, playful fashion photography,
                     vintage cinematic black and white, film noir lighting,
                     whimsical feminine narrative, best friends moment,
                     retro glamour aesthetic, mischievous energy,
                     storytelling composition, dramatic shadows""",
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
    prompt: `woman in vintage car, wind in hair, joyful expression,
             in the style of Ellen von Unwerth, playful fashion photography,
             vintage cinematic warm tones, golden hour lighting,
             whimsical carefree mood, feminine freedom,
             retro 1960s glamour, road trip narrative,
             dynamic movement, flirtatious energy`,
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

### 1. Boudoir Playfulness
```
woman in vintage lingerie on rumpled bed sheets,
playful expression, caught mid-laugh,
in the style of Ellen von Unwerth, playful fashion photography,
vintage cinematic aesthetic, soft film noir lighting,
whimsical flirtatious mood, sensual yet fun,
feminine empowerment, retro boudoir glamour,
intimate storytelling moment
```

### 2. Retro Adventure
```
woman on vintage motorcycle, leather jacket,
wind-blown hair, adventurous spirit,
in the style of Ellen von Unwerth, playful fashion photography,
vintage cinematic warm tones, dynamic action,
whimsical rebellious mood, feminine power,
retro 1960s glamour, road trip narrative,
empowering energy, mischievous smile
```

### 3. Hollywood Noir
```
woman in satin dress at vanity mirror, applying lipstick,
dramatic shadows, mysterious mood,
in the style of Ellen von Unwerth, playful fashion photography,
vintage film noir black and white, dramatic lighting,
whimsical old Hollywood aesthetic, femme fatale character,
retro 1940s glamour, cinematic storytelling,
sensual and powerful
```

### 4. Best Friends Narrative
```
two women in cocktail dresses, champagne glasses,
whispering and giggling, party scene,
in the style of Ellen von Unwerth, playful fashion photography,
vintage cinematic aesthetic, warm ambient lighting,
whimsical friendship narrative, joyful energy,
retro glamour, feminine celebration,
storytelling composition, flirtatious mood
```

### 5. Pin-Up Revival
```
woman in vintage swimsuit, beach cabana,
playful pin-up pose, confident smile,
in the style of Ellen von Unwerth, playful fashion photography,
vintage 1950s color aesthetic, sunny lighting,
whimsical summer mood, empowered femininity,
retro beach glamour, playful narrative,
flirtatious energy, mischievous charm
```

## Tips for Best Results

1. **Keep it playful** - Use "whimsical", "flirtatious", "mischievous", "joyful"
2. **Add narrative** - Describe a scene or story, not just a pose
3. **Vintage references** - Include "film noir", "1950s", "Hollywood", "retro"
4. **Feminine energy** - Use "empowered", "confident", "sensual", "playful"
5. **Lighting drama** - Specify "film noir lighting", "dramatic shadows", "vintage aesthetic"
6. **Movement and life** - Add "dynamic", "caught moment", "spontaneous", "wind-blown"

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `401 Unauthorized` | Invalid FAL_KEY | Verify key at fal.ai dashboard |
| `429 Too Many Requests` | Rate limit exceeded | Wait 60 seconds, retry |
| `400 Bad Request` | Invalid parameters | Check aspect_ratio format (e.g., "2:3") |
| `500 Server Error` | API temporary issue | Retry after 30 seconds |
| `Timeout` | Generation taking too long | Simplify prompt or reduce resolution |

## Reference

Ellen von Unwerth (born 1954) is a German photographer and director known for her playful, feminine images that empower women through sensuality and storytelling. A former model herself, she brings an insider's perspective to fashion photography.

**Key Influences**: Classic Hollywood, Film Noir, 1950s pin-up
**Signature**: Playful sensuality, vintage aesthetics, narrative storytelling, feminine empowerment
