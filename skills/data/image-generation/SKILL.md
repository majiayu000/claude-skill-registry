---
name: image-generation
description: AI image generation using Pollinations.ai with Stable Horde fallback - FREE with no API key required. Use when generating hero images, icons, logos, illustrations, mockups, or any visual assets for websites and apps. Covers product shots, avatars, placeholders, and social media images with professional quality.
allowed-tools:
  - Read
  - Write
  - WebFetch
  - Bash
context: fork
model: opus
---

# AI Image Generation Skill

Expert in generating professional-quality images using multi-provider resilience: **Pollinations.ai** (primary) with **Stable Horde** (fallback) - both FREE, no API keys required.

---

## 🛑 STEP 1: RUN THIS BASH COMMAND FIRST (MANDATORY - NO EXCEPTIONS)

**YOU MUST EXECUTE THIS BASH COMMAND BEFORE DOING ANYTHING ELSE.**

This is not optional. Do not skip. Do not generate URLs first. **RUN THIS FIRST:**

```bash
TEMP=$(mktemp) && curl -s -L -o "$TEMP" --max-time 10 "https://image.pollinations.ai/prompt/test?width=64&height=64&nologo=true" 2>/dev/null && TYPE=$(file -b "$TEMP" | cut -d',' -f1) && rm -f "$TEMP" && if [[ "$TYPE" == "PNG image data" ]] || [[ "$TYPE" == "JPEG image data" ]]; then echo "PROVIDER=pollinations"; else echo "PROVIDER=stablehorde"; echo "REASON=Got $TYPE instead of image"; fi
```

### Based on Output:

| Output | What To Do |
|--------|------------|
| `PROVIDER=pollinations` | ✅ Use Pollinations.ai URLs below |
| `PROVIDER=stablehorde` | 🔄 **SKIP Pollinations entirely** → Use Stable Horde API (see fallback section) |

**If you did NOT run the Bash command first, STOP and run it now.**

---

## ⚠️ CRITICAL: Health Check First (MANDATORY)

**BEFORE generating any image, ALWAYS run this CONTENT-BASED health check:**

⚠️ **WARNING**: HTTP 200 status is NOT sufficient! Pollinations may return 200 but with error text instead of image data. **ALWAYS verify the response is actually an image.**

```bash
# ROBUST health check - verifies actual image content (not just HTTP status)
TEMP_FILE=$(mktemp)
curl -s -L -o "$TEMP_FILE" --max-time 10 "https://image.pollinations.ai/prompt/blue%20square?width=64&height=64&nologo=true"
CONTENT_TYPE=$(file -b "$TEMP_FILE" | head -c 10)

if [[ "$CONTENT_TYPE" == "PNG image" ]] || [[ "$CONTENT_TYPE" == "JPEG image" ]]; then
    echo "✅ HEALTHY - Use Pollinations"
else
    echo "❌ BROKEN - Use Stable Horde (got: $CONTENT_TYPE)"
    cat "$TEMP_FILE"  # Show error message
fi
rm -f "$TEMP_FILE"
```

### Decision Tree Based on CONTENT (Not Just Status)

| Content Check | Meaning | Action |
|---------------|---------|--------|
| `PNG image data` | ✅ Healthy | Use Pollinations.ai |
| `JPEG image data` | ✅ Healthy | Use Pollinations.ai |
| `ASCII text` | ❌ Service error (502/503 in body) | **→ Use Stable Horde** |
| `HTML document` | ❌ Error page | **→ Use Stable Horde** |
| Empty/timeout | ❌ Network error | **→ Use Stable Horde** |

### Automated Provider Selection Script (ROBUST VERSION)

```bash
#!/bin/bash
# save as: check-image-api.sh
# IMPORTANT: This checks CONTENT, not just HTTP status!

TEMP_FILE=$(mktemp)
curl -s -L -o "$TEMP_FILE" --max-time 15 \
  "https://image.pollinations.ai/prompt/test%20square?width=64&height=64&nologo=true" 2>/dev/null

CONTENT_TYPE=$(file -b "$TEMP_FILE" 2>/dev/null | cut -d',' -f1)
rm -f "$TEMP_FILE"

if [[ "$CONTENT_TYPE" == "PNG image data" ]] || [[ "$CONTENT_TYPE" == "JPEG image data" ]]; then
    echo "PROVIDER=pollinations"
    echo "STATUS=healthy"
else
    echo "PROVIDER=stablehorde"
    echo "REASON=Pollinations returned '$CONTENT_TYPE' instead of image"
fi
```

### Why HTTP 200 Is Misleading

Pollinations.ai uses Cloudflare CDN. When the origin server is down:
- Cloudflare returns **HTTP 200** (edge responds)
- But the BODY contains: `502 Bad Gateway - Unable to reach the origin service`
- This is why **content-based checking is mandatory**

---

## 🚨 NEVER GET STUCK Protocol (Claude Code Behavior)

**This section defines how Claude Code should behave to NEVER get stuck on image generation.**

### Rule 1: Always Set Timeouts

```bash
# ALWAYS use --max-time flag (15-30 seconds max)
curl --max-time 15 "https://image.pollinations.ai/prompt/..."

# NEVER use curl without timeout (can hang forever)
curl "https://image.pollinations.ai/prompt/..."  # ❌ WRONG - can hang
```

### Rule 2: Fail Fast, Switch Immediately

If ANY of these occur, **immediately switch to Stable Horde**:
- Timeout (>15 seconds)
- Non-image response (ASCII text, HTML)
- HTTP 4xx/5xx errors
- API Error 400 "Could not process image"

**DO NOT:**
- ❌ Retry more than once
- ❌ Wait indefinitely
- ❌ Keep trying the same failing provider

### Rule 3: Check Before Acting

**ALWAYS run health check BEFORE attempting image generation:**

```bash
# Quick pre-flight check (5 second max)
TEMP=$(mktemp)
timeout 5 curl -s -o "$TEMP" "https://image.pollinations.ai/prompt/test?width=64&height=64" 2>/dev/null
if file "$TEMP" | grep -q "image"; then
    echo "Provider ready"
else
    echo "Provider down - use Stable Horde"
fi
rm -f "$TEMP"
```

### Rule 4: Structured Error Handling

When image generation fails, follow this exact flow:

```
1. Try Pollinations (timeout: 15s)
   ├── Success (image data) → Done ✅
   └── Failure (any error) → Step 2

2. Try Stable Horde (timeout: 120s for full job)
   ├── Success → Done ✅
   └── Failure → Step 3

3. Report failure and STOP
   └── Tell user: "Image generation unavailable. Both Pollinations.ai and Stable Horde are down."
   └── DO NOT keep retrying
```

### Rule 5: Exit Conditions (MANDATORY)

Claude Code MUST exit the image generation attempt when:

| Condition | Action | Max Attempts |
|-----------|--------|--------------|
| Timeout | Switch provider | 1 |
| HTTP 5xx | Switch provider | 1 |
| "Could not process image" | Switch provider | 1 |
| Non-image response | Switch provider | 1 |
| Both providers fail | **STOP and report** | 0 |

### Example: Non-Blocking Image Generation

```typescript
async function generateImageNonBlocking(prompt: string): Promise<string | null> {
  const TIMEOUT_MS = 15000;

  // Try Pollinations first
  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), TIMEOUT_MS);

    const response = await fetch(
      `https://image.pollinations.ai/prompt/${encodeURIComponent(prompt)}?width=512&height=512`,
      { signal: controller.signal }
    );
    clearTimeout(timeoutId);

    const contentType = response.headers.get('content-type');
    if (contentType?.startsWith('image/')) {
      return await response.blob().then(b => URL.createObjectURL(b));
    }
    // Not an image - fall through to Stable Horde
  } catch (e) {
    console.log('Pollinations failed, trying Stable Horde');
  }

  // Try Stable Horde
  try {
    return await generateViaStableHorde(prompt);
  } catch (e) {
    console.error('Both providers failed');
    return null; // STOP - don't keep retrying
  }
}
```

### Claude API "Could Not Process Image" Error

When you see this error:
```
API Error: 400 {"type":"error","error":{"type":"invalid_request_error","message":"Could not process image"}}
```

**This means Claude's vision API cannot process the image.** Solutions:
1. The image file may be corrupted or incomplete (502 error in disguise)
2. The image format is unsupported
3. The image URL returned an error page, not actual image data

**Action:** Do NOT retry with Claude's Read tool. Instead:
1. Download the image with curl first
2. Verify it's actually an image: `file downloaded.png`
3. If not an image → use Stable Horde fallback

## Quick Reference

### Primary: Pollinations.ai (when healthy)
```
https://image.pollinations.ai/prompt/YOUR_PROMPT_HERE
```

### Fallback: Stable Horde (when Pollinations is down)
```
POST https://stablehorde.net/api/v2/generate/async
Content-Type: application/json

{"prompt": "YOUR_PROMPT_HERE", "params": {"width": 512, "height": 512}}
```

---

## Stable Horde Fallback API (FREE, No API Key)

When Pollinations.ai returns 5xx errors, use Stable Horde - a community-powered, 100% free alternative.

### Why Stable Horde Works

- ✅ No API key required (anonymous mode)
- ✅ No rate limits for reasonable usage
- ✅ High-quality Stable Diffusion models
- ✅ Community-powered (crowdsourced GPUs)
- ⏱️ Generation time: 30-120 seconds (varies by queue)

### Step 1: Submit Generation Request

```bash
curl -X POST "https://stablehorde.net/api/v2/generate/async" \
  -H "Content-Type: application/json" \
  -H "apikey: 0000000000" \
  -d '{
    "prompt": "a majestic mountain landscape, professional photography, 8k, detailed",
    "params": {
      "width": 512,
      "height": 512,
      "steps": 30,
      "cfg_scale": 7.5,
      "sampler_name": "k_euler_a"
    },
    "nsfw": false,
    "censor_nsfw": true,
    "models": ["stable_diffusion"]
  }'
```

**Response:**
```json
{
  "id": "abc123-def456-ghi789",
  "kudos": 10
}
```

### Step 2: Poll for Completion

```bash
# Poll every 5 seconds until done
curl -s "https://stablehorde.net/api/v2/generate/check/abc123-def456-ghi789"
```

**Response when processing:**
```json
{
  "done": false,
  "wait_time": 45,
  "queue_position": 3,
  "processing": 1
}
```

**Response when complete:**
```json
{
  "done": true,
  "generations": [
    {
      "img": "base64_encoded_image_data...",
      "seed": "12345",
      "worker_id": "worker-abc",
      "model": "stable_diffusion"
    }
  ]
}
```

### Step 3: Save the Image

```bash
# Extract and save base64 image
curl -s "https://stablehorde.net/api/v2/generate/status/abc123-def456-ghi789" | \
  jq -r '.generations[0].img' | base64 -d > output.png
```

### Complete Node.js Example with Fallback

```typescript
import https from 'https';
import fs from 'fs';

interface ImageOptions {
  prompt: string;
  width?: number;
  height?: number;
  outputPath: string;
}

// Health check for Pollinations
async function checkPollinationsHealth(): Promise<boolean> {
  return new Promise((resolve) => {
    const req = https.get(
      'https://image.pollinations.ai/prompt/health?width=64&height=64',
      { timeout: 3000 },
      (res) => resolve(res.statusCode === 200)
    );
    req.on('error', () => resolve(false));
    req.on('timeout', () => { req.destroy(); resolve(false); });
  });
}

// Generate via Pollinations (primary)
async function generatePollinations(options: ImageOptions): Promise<string> {
  const { prompt, width = 1024, height = 1024, outputPath } = options;
  const url = `https://image.pollinations.ai/prompt/${encodeURIComponent(prompt)}?width=${width}&height=${height}&nologo=true`;

  return new Promise((resolve, reject) => {
    https.get(url, (res) => {
      if (res.statusCode !== 200) {
        reject(new Error(`Pollinations returned ${res.statusCode}`));
        return;
      }
      const file = fs.createWriteStream(outputPath);
      res.pipe(file);
      file.on('finish', () => { file.close(); resolve(outputPath); });
    }).on('error', reject);
  });
}

// Generate via Stable Horde (fallback)
async function generateStableHorde(options: ImageOptions): Promise<string> {
  const { prompt, width = 512, height = 512, outputPath } = options;

  // Step 1: Submit job
  const jobId = await submitHordeJob(prompt, width, height);
  console.log(`Stable Horde job submitted: ${jobId}`);

  // Step 2: Poll until done
  let done = false;
  let imageData: string | null = null;

  while (!done) {
    await new Promise(r => setTimeout(r, 5000)); // Wait 5s
    const status = await checkHordeStatus(jobId);
    console.log(`Queue position: ${status.queue_position}, Wait: ${status.wait_time}s`);

    if (status.done) {
      done = true;
      imageData = status.generations[0]?.img;
    }
  }

  // Step 3: Save image
  if (imageData) {
    fs.writeFileSync(outputPath, Buffer.from(imageData, 'base64'));
    return outputPath;
  }
  throw new Error('No image generated');
}

// Main function with automatic fallback
async function generateImage(options: ImageOptions): Promise<string> {
  console.log('Checking Pollinations.ai health...');
  const pollinationsHealthy = await checkPollinationsHealth();

  if (pollinationsHealthy) {
    console.log('✅ Pollinations healthy, using primary provider');
    try {
      return await generatePollinations(options);
    } catch (err) {
      console.log('⚠️ Pollinations failed, falling back to Stable Horde');
      return await generateStableHorde(options);
    }
  } else {
    console.log('❌ Pollinations down (502/503), using Stable Horde fallback');
    return await generateStableHorde(options);
  }
}

// Usage
generateImage({
  prompt: 'a futuristic city at sunset, cyberpunk, neon lights, 8k',
  width: 1024,
  height: 1024,
  outputPath: './generated-image.png'
}).then(path => console.log(`Image saved to: ${path}`));
```

### Stable Horde Parameters Reference

| Parameter | Values | Default | Description |
|-----------|--------|---------|-------------|
| `width` | 64-1024 (multiples of 64) | 512 | Image width |
| `height` | 64-1024 (multiples of 64) | 512 | Image height |
| `steps` | 1-150 | 30 | Diffusion steps |
| `cfg_scale` | 1-30 | 7.5 | Prompt adherence |
| `sampler_name` | k_euler_a, k_dpm_2, etc. | k_euler_a | Sampling method |
| `models` | ["stable_diffusion", "SDXL 1.0"] | auto | Model selection |

### Stable Horde Web UI Alternative

If you prefer a visual interface: **[ArtBot](https://tinybots.net/artbot)** - free web UI for Stable Horde.

---

## When This Skill Activates

This skill auto-activates when you need images for:
- **Web Development**: Hero sections, backgrounds, banners, thumbnails
- **App Design**: Splash screens, onboarding, placeholders, icons
- **Marketing**: Product mockups, social media, ads, landing pages
- **UI/UX**: Illustrations, avatars, empty states, feature graphics
- **Prototyping**: Concept visualization, wireframe assets

## Pollinations.ai API

### Basic URL Structure

```
https://image.pollinations.ai/prompt/{prompt}?{parameters}
```

### Parameters

| Parameter | Values | Default | Description |
|-----------|--------|---------|-------------|
| `width` | 256-2048 | 1024 | Image width in pixels |
| `height` | 256-2048 | 1024 | Image height in pixels |
| `model` | flux, turbo, flux-realism, flux-anime, flux-3d, flux-cablyai | flux | AI model to use |
| `seed` | any integer | random | Reproducible results |
| `nologo` | true | false | Remove watermark |
| `enhance` | true | false | Prompt enhancement |
| `safe` | true | false | Safety filter |

### Available Models

| Model | Best For | Quality | Speed |
|-------|----------|---------|-------|
| `flux` | General purpose, photorealistic | Highest | Medium |
| `flux-realism` | Ultra-realistic photos | Very High | Medium |
| `flux-anime` | Anime/illustration style | High | Fast |
| `flux-3d` | 3D renders, product mockups | High | Medium |
| `flux-cablyai` | Artistic, creative styles | High | Fast |
| `turbo` | Quick iterations, drafts | Medium | Fastest |

## Professional Prompt Engineering

### Prompt Formula (CRITICAL for Quality)

```
[Subject] + [Style/Medium] + [Lighting] + [Composition] + [Quality Modifiers]
```

### Quality Modifiers (ALWAYS Include)

For **highest quality output**, append these to prompts:

```
, professional photography, 8k uhd, high resolution, sharp focus, highly detailed
```

For **specific use cases**:

| Use Case | Quality Modifiers |
|----------|-------------------|
| **Website Hero** | `cinematic lighting, professional photography, 8k, sharp focus, volumetric lighting` |
| **Product Shot** | `studio lighting, white background, commercial photography, product photography, clean` |
| **App Icon** | `minimal, flat design, vector style, clean lines, app icon, centered, simple background` |
| **Illustration** | `digital illustration, vibrant colors, clean lines, professional artwork, detailed` |
| **Avatar** | `portrait, centered, professional headshot, neutral background, high quality` |
| **Background** | `seamless pattern, tileable, abstract, subtle, muted colors, non-distracting` |

### Aspect Ratios for Common Use Cases

| Use Case | Width | Height | Ratio |
|----------|-------|--------|-------|
| **Hero Banner** | 1920 | 1080 | 16:9 |
| **Social Media Post** | 1200 | 1200 | 1:1 |
| **Portrait/Avatar** | 800 | 1200 | 2:3 |
| **Product Card** | 800 | 600 | 4:3 |
| **Mobile Splash** | 1080 | 1920 | 9:16 |
| **App Icon** | 512 | 512 | 1:1 |
| **OG Image** | 1200 | 630 | ~1.9:1 |
| **Thumbnail** | 400 | 300 | 4:3 |

## Code Examples

### React/Next.js Integration

```tsx
// components/GeneratedImage.tsx
interface GeneratedImageProps {
  prompt: string;
  width?: number;
  height?: number;
  model?: 'flux' | 'flux-realism' | 'flux-anime' | 'flux-3d' | 'turbo';
  className?: string;
  alt: string;
}

export function GeneratedImage({
  prompt,
  width = 1024,
  height = 1024,
  model = 'flux',
  className,
  alt,
}: GeneratedImageProps) {
  const encodedPrompt = encodeURIComponent(prompt);
  const url = `https://image.pollinations.ai/prompt/${encodedPrompt}?width=${width}&height=${height}&model=${model}&nologo=true`;

  return (
    <img
      src={url}
      alt={alt}
      width={width}
      height={height}
      className={className}
      loading="lazy"
    />
  );
}

// Usage
<GeneratedImage
  prompt="Modern tech startup office, glass walls, natural lighting, professional photography, 8k"
  width={1920}
  height={1080}
  alt="Hero background"
  className="w-full h-auto object-cover"
/>
```

### With Next.js Image Optimization

```tsx
// next.config.js
module.exports = {
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'image.pollinations.ai',
      },
    ],
  },
};

// components/OptimizedGeneratedImage.tsx
import Image from 'next/image';

export function OptimizedGeneratedImage({ prompt, width, height, alt }) {
  const url = `https://image.pollinations.ai/prompt/${encodeURIComponent(prompt)}?width=${width}&height=${height}&model=flux&nologo=true`;

  return (
    <Image
      src={url}
      alt={alt}
      width={width}
      height={height}
      priority={false}
    />
  );
}
```

### HTML Direct Embed

```html
<!-- Hero Image -->
<img
  src="https://image.pollinations.ai/prompt/futuristic%20city%20skyline%20at%20sunset%2C%20cyberpunk%2C%20neon%20lights%2C%20cinematic%2C%208k?width=1920&height=1080&model=flux&nologo=true"
  alt="Hero background"
  loading="lazy"
/>

<!-- Product Mockup -->
<img
  src="https://image.pollinations.ai/prompt/smartphone%20mockup%20on%20marble%20desk%2C%20minimal%2C%20studio%20lighting%2C%20product%20photography?width=800&height=600&model=flux-3d&nologo=true"
  alt="Product mockup"
/>
```

### Markdown (for Documentation)

```markdown
![Hero Image](https://image.pollinations.ai/prompt/abstract%20geometric%20pattern%2C%20gradient%20blue%20purple%2C%20modern%2C%20clean?width=1200&height=400&nologo=true)
```

### Batch Generation Script (Node.js)

```typescript
import fs from 'fs';
import https from 'https';

async function generateImage(prompt: string, filename: string, options = {}) {
  const { width = 1024, height = 1024, model = 'flux' } = options;
  const url = `https://image.pollinations.ai/prompt/${encodeURIComponent(prompt)}?width=${width}&height=${height}&model=${model}&nologo=true`;

  return new Promise((resolve, reject) => {
    https.get(url, (response) => {
      const file = fs.createWriteStream(filename);
      response.pipe(file);
      file.on('finish', () => {
        file.close();
        resolve(filename);
      });
    }).on('error', reject);
  });
}

// Generate multiple images
const assets = [
  { prompt: 'hero background, abstract waves, blue gradient', file: 'hero.png', width: 1920, height: 1080 },
  { prompt: 'user avatar placeholder, geometric face', file: 'avatar.png', width: 200, height: 200 },
  { prompt: 'empty state illustration, no results found', file: 'empty.png', width: 400, height: 300 },
];

for (const asset of assets) {
  await generateImage(asset.prompt, asset.file, { width: asset.width, height: asset.height });
  console.log(`Generated: ${asset.file}`);
}
```

## Use Case Recipes

### 1. Landing Page Hero

```
https://image.pollinations.ai/prompt/modern%20SaaS%20dashboard%20floating%20in%20space%2C%20dark%20theme%2C%20glowing%20UI%20elements%2C%20professional%203D%20render%2C%20cinematic%20lighting%2C%208k%20uhd?width=1920&height=1080&model=flux&nologo=true
```

### 2. Team Member Avatars

```
https://image.pollinations.ai/prompt/professional%20headshot%2C%20friendly%20smile%2C%20neutral%20gray%20background%2C%20studio%20lighting%2C%20business%20casual?width=400&height=400&model=flux-realism&nologo=true
```

### 3. App Empty State

```
https://image.pollinations.ai/prompt/cute%20illustration%20of%20empty%20box%2C%20minimal%20flat%20design%2C%20soft%20pastel%20colors%2C%20friendly%2C%20vector%20style?width=400&height=300&model=flux-anime&nologo=true
```

### 4. Product Mockup

```
https://image.pollinations.ai/prompt/iPhone%2015%20mockup%20on%20wooden%20desk%2C%20coffee%20cup%2C%20minimal%2C%20lifestyle%20photography%2C%20warm%20lighting%2C%20professional?width=1200&height=800&model=flux-3d&nologo=true
```

### 5. Blog Featured Image

```
https://image.pollinations.ai/prompt/abstract%20visualization%20of%20artificial%20intelligence%2C%20neural%20networks%2C%20blue%20and%20purple%2C%20futuristic%2C%20clean?width=1200&height=630&model=flux&nologo=true
```

### 6. App Icon

```
https://image.pollinations.ai/prompt/minimalist%20app%20icon%2C%20letter%20A%2C%20gradient%20blue%20to%20purple%2C%20rounded%20corners%2C%20flat%20design%2C%20iOS%20style?width=512&height=512&model=flux&nologo=true
```

### 7. Background Pattern

```
https://image.pollinations.ai/prompt/seamless%20geometric%20pattern%2C%20subtle%20gray%20on%20white%2C%20minimalist%2C%20tileable%2C%20modern?width=512&height=512&model=flux&nologo=true
```

### 8. Feature Illustration

```
https://image.pollinations.ai/prompt/isometric%20illustration%20of%20cloud%20computing%2C%20servers%2C%20data%20flow%2C%20blue%20and%20white%2C%20clean%20vector%20style?width=800&height=600&model=flux&nologo=true
```

## Best Practices

### DO

1. **Use descriptive prompts** - More detail = better results
2. **Include quality modifiers** - "8k, professional, detailed"
3. **Specify the style** - "photograph", "illustration", "3D render"
4. **Define lighting** - "studio lighting", "natural light", "cinematic"
5. **Set appropriate dimensions** - Match your actual use case
6. **Use seeds for consistency** - Same seed = reproducible results
7. **Cache generated images** - Save to CDN for production

### DON'T

1. **Don't use generic prompts** - "a picture of something"
2. **Don't request copyrighted content** - No brand logos, celebrities
3. **Don't use in loops without throttling** - Rate limits apply
4. **Don't skip the `nologo=true` param** - Avoids watermarks
5. **Don't generate same image repeatedly** - Use seed + cache

## Rate Limits & Caching Strategy

### Pollinations Rate Limits

| Tier | Limit | Signup |
|------|-------|--------|
| Anonymous | 1 req/15s | None |
| Seed (free) | 1 req/5s | Free registration |
| Flower | 1 req/3s | Paid |

### Production Caching Strategy

```typescript
// Cache generated images to your CDN
async function getOrGenerateImage(prompt: string, options: ImageOptions) {
  const cacheKey = createHash('md5')
    .update(prompt + JSON.stringify(options))
    .digest('hex');

  // Check CDN cache first
  const cached = await cdn.get(`images/${cacheKey}.png`);
  if (cached) return cached.url;

  // Generate and cache
  const imageUrl = buildPollinationsUrl(prompt, options);
  const imageBuffer = await fetch(imageUrl).then(r => r.buffer());
  const cdnUrl = await cdn.upload(`images/${cacheKey}.png`, imageBuffer);

  return cdnUrl;
}
```

## Troubleshooting

### HTTP Error Codes & Solutions

| Error Code | Provider | Meaning | Solution |
|------------|----------|---------|----------|
| `200` | Both | ✅ Success | Image generated |
| `400` | Both | Bad Request | Fix prompt (invalid characters, too long) |
| `429` | Pollinations | Rate Limited | Wait 15s or switch to Stable Horde |
| `500` | Both | Internal Error | Retry once, then switch provider |
| `502` | Pollinations | **Bad Gateway** | **→ Use Stable Horde immediately** |
| `503` | Both | Service Unavailable | **→ Use Stable Horde immediately** |
| `504` | Pollinations | Gateway Timeout | **→ Use Stable Horde immediately** |
| `000` | Both | Network/DNS Error | Check internet, try Stable Horde |

### Common Issues & Fixes

| Issue | Solution |
|-------|----------|
| **Claude Code stuck** | Run health check first, use fallback on 5xx |
| Slow generation | Use `turbo` model (Pollinations) or reduce steps (Horde) |
| Poor quality | Add quality modifiers, use `flux` or `flux-realism` |
| Wrong style | Specify style explicitly: "photograph", "illustration" |
| Watermark appears | Add `nologo=true` parameter |
| Inconsistent results | Use same `seed` parameter |
| Rate limited | Wait 15s or use Stable Horde (no rate limits) |
| Image not loading | URL-encode the prompt properly |
| Stable Horde slow | Normal: 30-120s queue time, be patient |
| Base64 decode fails | Ensure you're getting the full `img` field |

### Quick Diagnostic Script (Content-Based)

```bash
#!/bin/bash
# diagnose-image-api.sh - Run this when image generation fails
# IMPORTANT: Uses CONTENT checking, not just HTTP status!

echo "=== Image API Diagnostics (Content-Based) ==="

# Test Pollinations with actual image download
echo -n "1. Pollinations.ai: "
TEMP_FILE=$(mktemp)
curl -s -L -o "$TEMP_FILE" --max-time 15 \
  "https://image.pollinations.ai/prompt/diagnostic%20test?width=64&height=64&nologo=true" 2>/dev/null
P_CONTENT=$(file -b "$TEMP_FILE" 2>/dev/null | cut -d',' -f1)

if [[ "$P_CONTENT" == "PNG image data" ]] || [[ "$P_CONTENT" == "JPEG image data" ]]; then
    echo "✅ HEALTHY (returns actual images)"
    P_HEALTHY=true
elif [[ "$P_CONTENT" == "ASCII text" ]]; then
    echo "❌ BROKEN (returns error text: $(head -c 50 "$TEMP_FILE"))"
    P_HEALTHY=false
elif [[ -z "$P_CONTENT" ]]; then
    echo "❌ TIMEOUT or empty response"
    P_HEALTHY=false
else
    echo "⚠️ UNKNOWN ($P_CONTENT)"
    P_HEALTHY=false
fi
rm -f "$TEMP_FILE"

# Test Stable Horde API
echo -n "2. Stable Horde: "
H_STATUS=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 \
  "https://stablehorde.net/api/v2/status/heartbeat" 2>/dev/null || echo "TIMEOUT")
if [[ "$H_STATUS" == "200" ]]; then
    echo "✅ HEALTHY (API responding)"
    H_HEALTHY=true
else
    echo "❌ ISSUE ($H_STATUS)"
    H_HEALTHY=false
fi

# Test internet
echo -n "3. Internet: "
I_STATUS=$(curl -s -o /dev/null -w "%{http_code}" --max-time 3 "https://google.com" 2>/dev/null || echo "TIMEOUT")
if [[ "$I_STATUS" == "200" || "$I_STATUS" == "301" ]]; then
    echo "✅ OK"
else
    echo "❌ NO INTERNET"
fi

echo ""
echo "=== Recommendation ==="
if [[ "$P_HEALTHY" == "true" ]]; then
    echo "✅ Use: Pollinations.ai (primary) - working normally"
elif [[ "$H_HEALTHY" == "true" ]]; then
    echo "🔄 Use: Stable Horde (fallback) - Pollinations is currently down"
    echo ""
    echo "Stable Horde usage:"
    echo "  1. POST to https://stablehorde.net/api/v2/generate/async"
    echo "  2. Poll https://stablehorde.net/api/v2/generate/check/{id}"
    echo "  3. Get result from https://stablehorde.net/api/v2/generate/status/{id}"
else
    echo "❌ Both services unavailable. Check internet connection."
fi
```

## Integration with Frontend Design

When building websites/apps, this skill works seamlessly with frontend development:

1. **During Development**: Use Pollinations URLs directly as placeholders
2. **Before Production**: Generate final images and save to your CDN
3. **For Dynamic Content**: Use the API with proper caching

```tsx
// Development: Direct URL (fast iteration)
<img src="https://image.pollinations.ai/prompt/..." />

// Production: Cached on your CDN
<img src="https://your-cdn.com/images/hero-cached.png" />
```

## Activation Keywords

This skill activates automatically when you mention:
- "generate an image", "create a picture", "make an illustration"
- "hero image for", "banner for", "background for"
- "mockup of", "product shot", "app icon"
- "placeholder image", "avatar", "thumbnail"
- "illustration of", "graphic of", "visual for"
- Any image asset request during web/app development

## Documentation Site Assets (SpecWeave Brand)

When generating images for SpecWeave documentation sites, use these brand guidelines:

### Brand Colors for Prompts

| Color | Hex | Usage |
|-------|-----|-------|
| Primary Purple | #7c3aed | Main brand color, gradients |
| Purple Dark | #6d28d9 | Accents, shadows |
| Purple Light | #a78bfa | Highlights, glows |
| Purple Darkest | #5b21b6 | Deep backgrounds |

**Include in prompts:** `purple violet gradient #7c3aed`, `professional SaaS aesthetic`

### Standard Docs Dimensions

| Asset Type | Width | Height | Model | Usage |
|------------|-------|--------|-------|-------|
| Hero Banner | 1920 | 1080 | flux | Homepage hero, landing pages |
| Feature Card | 800 | 600 | flux | Feature illustrations |
| Section Header | 1200 | 400 | flux | Section banners |
| Icon | 64 | 64 | flux | Navigation, feature icons |
| Empty State | 400 | 300 | flux-anime | Empty states, placeholders |
| Social Card | 1200 | 630 | flux | OG images, social sharing |

### Docs-Specific Prompt Templates

| Asset Type | Prompt Pattern |
|------------|---------------|
| **Hero** | `[concept] in abstract form, purple gradient #7c3aed to #a78bfa, professional SaaS, glowing nodes, dark background, 8k, clean minimal` |
| **Feature Illustration** | `isometric illustration of [feature], purple accent #7c3aed, white background, clean vector style, professional` |
| **Section Banner** | `abstract [theme] visualization, flowing lines, purple gradient #7c3aed, minimal, professional, wide format` |
| **Icon** | `minimal icon [concept], purple fill #7c3aed, white background, app icon style, centered, simple` |
| **Living Docs** | `interconnected documents with glowing purple connections #7c3aed, network visualization, professional, clean` |
| **Agent System** | `AI agents as geometric shapes in orbital formation, purple violet theme #7c3aed, futuristic, professional` |
| **Workflow** | `branching flowchart paths, glowing circuit lines, purple gradient #7c3aed, decision tree visualization, minimal` |

### SpecWeave Docs Ready-to-Use URLs

**Living Documentation Illustration:**
```
https://image.pollinations.ai/prompt/interconnected%20hexagonal%20document%20nodes%20forming%20network%2C%20glowing%20purple%20connections%20%237c3aed%2C%20gradient%20to%20%23a78bfa%2C%20professional%20SaaS%2C%20dark%20background%2C%208k%2C%20minimal%20vector?width=800&height=600&model=flux&nologo=true&seed=42
```

**Multi-Agent System Illustration:**
```
https://image.pollinations.ai/prompt/interconnected%20AI%20agents%20as%20geometric%20avatars%20in%20orbital%20formation%2C%20purple%20violet%20theme%20%237c3aed%2C%20futuristic%20holographic%2C%20professional%2C%20clean%20dark%20background%2C%208k?width=800&height=600&model=flux&nologo=true&seed=42
```

**Workflow/Decision Tree Illustration:**
```
https://image.pollinations.ai/prompt/branching%20flowchart%20paths%20made%20of%20glowing%20circuit%20lines%2C%20purple%20gradient%20%237c3aed%20to%20%23a78bfa%2C%20decision%20trees%2C%20minimal%20geometric%2C%20professional%2C%20dark%20background?width=800&height=600&model=flux&nologo=true&seed=42
```

## Related Skills

- **frontend-design**: For UI/UX design patterns
- **browser-automation**: For screenshot capture
- **docusaurus**: For documentation site setup
- **technical-writing**: For documentation content

## Project-Specific Learnings

**Before starting work, check for project-specific learnings:**

```bash
# Check if skill memory exists for this skill
cat .specweave/skill-memories/image-generation.md 2>/dev/null || echo "No project learnings yet"
```

Project learnings are automatically captured by the reflection system when corrections or patterns are identified during development. These learnings help you understand project-specific conventions and past decisions.

