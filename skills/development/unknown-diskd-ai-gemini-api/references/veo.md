# Video Generation (Veo)

Veo is Google's state-of-the-art model for generating high-fidelity videos with natively generated audio. Generate 8-second 720p, 1080p, or 4K videos with stunning realism.

## Table of Contents

- [Models](#models)
- [Text-to-Video](#text-to-video)
- [Image-to-Video](#image-to-video)
- [Reference Images](#reference-images)
- [Video Extension](#video-extension)
- [Native Audio (Veo 3)](#native-audio-veo-3)
- [Async Operations](#async-operations)
- [Configuration](#configuration)
- [Prompting Guide](#prompting-guide)
- [Limitations](#limitations)

---

## Models

| Model | Code | Audio | Resolution | Duration | Input |
|-------|------|-------|------------|----------|-------|
| **Veo 3.1** | `veo-3.1-generate-preview` | Native | 720p, 1080p, 4K | 4-8s | Text, Image, Video |
| **Veo 3.1 Fast** | `veo-3.1-fast-generate-preview` | Native | 720p, 1080p, 4K | 4-8s | Text, Image, Video |
| **Veo 3** | `veo-3-generate-preview` | Native | 720p, 1080p | 8s | Text, Image |
| **Veo 3 Fast** | `veo-3-fast-generate-preview` | Native | 720p, 1080p | 8s | Text, Image |
| **Veo 2** | `veo-2.0-generate-001` | Silent | 720p | 5-8s | Text, Image |

### Veo 3.1 Capabilities

- **Portrait videos**: 9:16 and 16:9 aspect ratios
- **Video extension**: Extend previously generated videos up to 148s total
- **Frame-specific generation**: Specify first and/or last frame
- **High resolution**: Up to 4K output (8s videos only)
- **Native audio**: Dialogue, sound effects, ambient noise

### Veo Fast Models

Optimized for speed and business use cases:
- Rapid A/B testing of creative concepts
- Backend services generating ads
- Quick social media content production

---

## Text-to-Video

### Python

```python
import time
from google import genai
from google.genai import types

client = genai.Client()

operation = client.models.generate_videos(
    model="veo-3.1-generate-preview",
    prompt="A cinematic shot of a majestic lion in the savannah at golden hour",
)

# Poll until complete
while not operation.done:
    print("Waiting for video generation...")
    time.sleep(10)
    operation = client.operations.get(operation)

# Download the video
video = operation.response.generated_videos[0]
client.files.download(file=video.video)
video.video.save("lion_savannah.mp4")
```

### JavaScript

```javascript
import { GoogleGenAI } from "@google/genai";

const ai = new GoogleGenAI({});

let operation = await ai.models.generateVideos({
    model: "veo-3.1-generate-preview",
    prompt: "A cinematic shot of a majestic lion in the savannah at golden hour",
});

// Poll until complete
while (!operation.done) {
    console.log("Waiting for video generation...");
    await new Promise(resolve => setTimeout(resolve, 10000));
    operation = await ai.operations.getVideosOperation({ operation });
}

// Download the video
ai.files.download({
    file: operation.response.generatedVideos[0].video,
    downloadPath: "lion_savannah.mp4",
});
```

### Go

```go
package main

import (
    "context"
    "log"
    "os"
    "time"

    "google.golang.org/genai"
)

func main() {
    ctx := context.Background()
    client, _ := genai.NewClient(ctx, nil)

    operation, _ := client.Models.GenerateVideos(
        ctx,
        "veo-3.1-generate-preview",
        "A cinematic shot of a majestic lion in the savannah at golden hour",
        nil, nil,
    )

    // Poll until complete
    for !operation.Done {
        log.Println("Waiting for video generation...")
        time.Sleep(10 * time.Second)
        operation, _ = client.Operations.GetVideosOperation(ctx, operation, nil)
    }

    // Download the video
    video := operation.Response.GeneratedVideos[0]
    client.Files.Download(ctx, video.Video, nil)
    os.WriteFile("lion_savannah.mp4", video.Video.VideoBytes, 0644)
}
```

### REST

```bash
BASE_URL="https://generativelanguage.googleapis.com/v1beta"

# Start generation
operation_name=$(curl -s "${BASE_URL}/models/veo-3.1-generate-preview:predictLongRunning" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "instances": [{"prompt": "A cinematic shot of a majestic lion in the savannah"}]
  }' | jq -r .name)

# Poll until complete
while true; do
  status=$(curl -s -H "x-goog-api-key: $GEMINI_API_KEY" "${BASE_URL}/${operation_name}")
  if [ "$(echo "$status" | jq .done)" = "true" ]; then
    video_uri=$(echo "$status" | jq -r '.response.generateVideoResponse.generatedSamples[0].video.uri')
    curl -L -o video.mp4 -H "x-goog-api-key: $GEMINI_API_KEY" "$video_uri"
    break
  fi
  sleep 10
done
```

---

## Image-to-Video

Use an image as the starting frame.

### Python

```python
import time
from google import genai

client = genai.Client()

prompt = "Panning wide shot of a calico kitten sleeping in the sunshine"

# Generate starting image with Nano Banana
image_response = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents=prompt,
    config={"response_modalities": ['IMAGE']}
)

# Generate video from image
operation = client.models.generate_videos(
    model="veo-3.1-generate-preview",
    prompt=prompt,
    image=image_response.candidates[0].content.parts[0],
)

while not operation.done:
    time.sleep(10)
    operation = client.operations.get(operation)

video = operation.response.generated_videos[0]
client.files.download(file=video.video)
video.video.save("kitten_video.mp4")
```

### JavaScript

```javascript
const ai = new GoogleGenAI({});

const prompt = "Panning wide shot of a calico kitten sleeping in the sunshine";

// Generate starting image with Nano Banana
const imageResponse = await ai.models.generateContent({
    model: "gemini-2.5-flash-image",
    contents: prompt,
    config: { responseModalities: ['IMAGE'] }
});

const image = imageResponse.candidates[0].content.parts[0];

// Generate video from image
let operation = await ai.models.generateVideos({
    model: "veo-3.1-generate-preview",
    prompt: prompt,
    image: image,
});

while (!operation.done) {
    await new Promise(resolve => setTimeout(resolve, 10000));
    operation = await ai.operations.getVideosOperation({ operation });
}

ai.files.download({
    file: operation.response.generatedVideos[0].video,
    downloadPath: "kitten_video.mp4",
});
```

---

## Reference Images

Use up to 14 reference images with `reference_type`:
- `"first_frame"`: Starting frame
- `"last_frame"`: Ending frame
- `"asset"`: Objects/characters to include

### Python

```python
from google.genai import types

prompt = """A woman walks through turquoise lagoon water wearing a pink
flamingo dress with heart-shaped sunglasses."""

dress_ref = types.VideoGenerationReferenceImage(
    image=dress_image,  # Generated with Nano Banana
    reference_type="asset"
)

glasses_ref = types.VideoGenerationReferenceImage(
    image=glasses_image,
    reference_type="asset"
)

woman_ref = types.VideoGenerationReferenceImage(
    image=woman_image,
    reference_type="asset"
)

operation = client.models.generate_videos(
    model="veo-3.1-generate-preview",
    prompt=prompt,
    config=types.GenerateVideosConfig(
        reference_images=[dress_ref, glasses_ref, woman_ref],
    ),
)
```

### JavaScript

```javascript
const dressReference = { image: dressImage, referenceType: "asset" };
const glassesReference = { image: glassesImage, referenceType: "asset" };
const womanReference = { image: womanImage, referenceType: "asset" };

let operation = await ai.models.generateVideos({
    model: "veo-3.1-generate-preview",
    prompt: prompt,
    config: {
        referenceImages: [dressReference, glassesReference, womanReference],
    },
});
```

---

## Video Extension

Extend previously generated Veo videos up to 148 seconds total.

**Requirements:**
- Input video must be from Veo generation
- Aspect ratio: 9:16 or 16:9
- Resolution: 720p only
- Input video: 141 seconds or less

### Python

```python
# butterflyVideo from previous Veo generation
operation = client.models.generate_videos(
    model="veo-3.1-generate-preview",
    video=previous_operation.response.generated_videos[0].video,
    prompt="Track the butterfly as it lands on an orange flower. A puppy runs up.",
    config=types.GenerateVideosConfig(
        number_of_videos=1,
        resolution="720p"
    ),
)
```

### JavaScript

```javascript
let operation = await ai.models.generateVideos({
    model: "veo-3.1-generate-preview",
    video: butterflyVideo,  // From previous generation
    prompt: "Track the butterfly as it lands on an orange flower.",
    config: {
        numberOfVideos: 1,
        resolution: "720p",
    },
});
```

---

## Native Audio (Veo 3)

Veo 3+ generates synchronized audio with video. Prompt cues:

- **Dialogue**: Use quotes for speech
  ```
  "This must be the key," he murmured.
  ```
- **Sound Effects**: Explicitly describe sounds
  ```
  tires screeching loudly, engine roaring
  ```
- **Ambient Noise**: Describe soundscape
  ```
  A faint, eerie hum resonates in the background.
  ```

### Example with Audio

```python
prompt = """A close up of two people staring at a cryptic drawing on a wall,
torchlight flickering. A man murmurs, 'This must be it. That's the secret code.'
The woman looks at him and whispers excitedly, 'What did you say?'"""

operation = client.models.generate_videos(
    model="veo-3.1-generate-preview",
    prompt=prompt,
)
```

---

## Async Operations

Video generation is async. Poll until `done` is true.

### Python

```python
import time

operation = client.models.generate_videos(
    model="veo-3.1-generate-preview",
    prompt="A majestic waterfall in a lush rainforest",
)

while not operation.done:
    print(f"Status: {operation.metadata}")
    time.sleep(10)
    operation = client.operations.get(operation)

if operation.response.generated_videos:
    video = operation.response.generated_videos[0]
    client.files.download(file=video.video)
    video.video.save("waterfall.mp4")
```

### JavaScript

```javascript
let operation = await ai.models.generateVideos({
    model: "veo-3.1-generate-preview",
    prompt: "A majestic waterfall in a lush rainforest",
});

while (!operation.done) {
    console.log("Generating...");
    await new Promise(resolve => setTimeout(resolve, 10000));
    operation = await ai.operations.getVideosOperation({ operation });
}

ai.files.download({
    file: operation.response.generatedVideos[0].video,
    downloadPath: "waterfall.mp4",
});
```

---

## Configuration

### Resolution

```python
config=types.GenerateVideosConfig(
    resolution="4k"  # "720p", "1080p", "4k"
)
```

**Note**: 1080p and 4K limited to 8-second videos. Video extension limited to 720p.

### Aspect Ratio

```python
config=types.GenerateVideosConfig(
    aspect_ratio="16:9"  # "16:9" (landscape), "9:16" (portrait)
)
```

### Video Duration

```python
config=types.GenerateVideosConfig(
    duration_seconds=8  # 4, 6, or 8 seconds
)
```

### Negative Prompt

```python
config=types.GenerateVideosConfig(
    negative_prompt="cartoon, drawing, low quality"
)
```

### Person Generation (Regional)

```python
config=types.GenerateVideosConfig(
    person_generation="allow_adult"  # "dont_allow", "allow_adult"
)
```

### Combined Example

```python
operation = client.models.generate_videos(
    model="veo-3.1-generate-preview",
    prompt="A cinematic shot of a majestic lion in the savannah",
    config=types.GenerateVideosConfig(
        aspect_ratio="16:9",
        resolution="1080p",
        negative_prompt="cartoon, drawing, low quality",
    ),
)
```

---

## Prompting Guide

### Elements to Include

1. **Subject**: Object, person, animal, scenery
2. **Action**: What the subject is doing (walking, running, turning)
3. **Style**: Film style keywords (sci-fi, horror, film noir, cartoon)
4. **Camera positioning**: aerial view, eye-level, top-down, dolly shot
5. **Composition**: wide shot, close-up, single-shot, two-shot
6. **Focus/lens**: shallow focus, deep focus, macro lens, wide-angle
7. **Ambiance**: blue tones, night, warm tones

### Example Prompts

**Cinematic with dialogue:**
```
A wide shot of a misty Pacific Northwest forest. Two exhausted hikers push through ferns.
Man: (Hand on knife) "That's no ordinary bear."
Woman: (Scanning the woods) "Then what is it?"
Rough bark, snapping twigs, footsteps on damp earth.
```

**Portrait video (9:16):**
```
Create a video highlighting the smooth motion of a majestic Hawaiian waterfall.
Focus on realistic water flow, detailed foliage, and natural lighting.
Capture rushing water, misty atmosphere, dappled sunlight.
Use smooth, cinematic camera movements. Peaceful, realistic tone.
```

**Landscape with style:**
```
A stylized mid-century modern kitchen, soft pastel colors and warm wood tones.
A woman in a floral apron, styled like a 50s sitcom, places a cake on the counter.
Camera slowly pushes in. Palm Springs, 1970s style.
```

### Audio Prompting Tips

- Use quotes for specific speech
- Explicitly describe sounds ("tires screeching loudly")
- Describe environment soundscape ("A faint hum resonates")

---

## Limitations

| Aspect | Limit |
|--------|-------|
| **Latency** | 11 seconds - 6 minutes |
| **Video retention** | 2 days (download within this time) |
| **Frame rate** | 24fps |
| **Max extension** | 148 seconds total |
| **Regional (EU/UK/CH/MENA)** | Veo 3: `allow_adult` only; Veo 2: `dont_allow` default |

### Feature Availability by Model

| Feature | Veo 3.1 | Veo 3 | Veo 2 |
|---------|---------|-------|-------|
| Audio | Native | Native | Silent |
| Video extension | Yes | No | No |
| 4K resolution | Yes (8s) | No | No |
| 1080p resolution | Yes (8s) | Yes (16:9) | No |
| Portrait (9:16) | Yes | Yes | Limited |

### Safety & Watermarking

- Safety filters applied across Gemini
- SynthID watermark on all generated videos
- Memorization checking for privacy/copyright

---

## Resources

- [Veo Guide](https://ai.google.dev/gemini-api/docs/video)
- [Veo Quickstart Colab](https://colab.research.google.com/github/google-gemini/cookbook/blob/main/quickstarts/Get_started_Veo.ipynb)
- [Veo 3.1 Studio](https://aistudio.google.com/apps/bundled/veo_studio)
- [Prompt Design Guide](https://ai.google.dev/gemini-api/docs/prompting-intro)
- [Pricing](https://ai.google.dev/gemini-api/docs/pricing#veo-3.1)
