# Image Generation (Nano Banana)

Nano Banana is Gemini's native image generation model series. Generate, edit, and process images conversationally with text, images, or both. All generated images include a SynthID watermark.

## Table of Contents

- [Models](#models)
- [Text-to-Image](#text-to-image)
- [Image Editing](#image-editing)
- [Multi-turn Editing](#multi-turn-editing)
- [Gemini 3 Pro Image Features](#gemini-3-pro-image-features)
- [Thought Signatures](#thought-signatures)
- [Prompting Guide](#prompting-guide)
- [Editing Techniques](#editing-techniques)
- [Configuration](#configuration)
- [Limitations](#limitations)

---

## Models

| Model | Code | Best For | Max Resolution | Max Input Images |
|-------|------|----------|----------------|------------------|
| **Nano Banana** | `gemini-2.5-flash-image` | Speed, high-volume, low-latency | 1024px | 3 |
| **Nano Banana Pro** | `gemini-3-pro-image-preview` | Professional assets, complex instructions | 4K | 14 |

### Nano Banana (`gemini-2.5-flash-image`)

Optimized for speed and efficiency. Best for high-volume, low-latency tasks.

### Nano Banana Pro (`gemini-3-pro-image-preview`)

State-of-the-art model for professional asset production:

- **High-resolution output**: 1K, 2K, and 4K visuals
- **Advanced text rendering**: Legible, stylized text for infographics, menus, logos
- **Google Search grounding**: Verify facts and generate imagery based on real-time data
- **Thinking mode**: Reasons through complex prompts with interim "thought images"
- **Up to 14 reference images**: 6 objects (high-fidelity) + 5 humans (character consistency)

---

## Text-to-Image

### Python

```python
from google import genai
from google.genai import types

client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents="Create a picture of a nano banana dish in a fancy restaurant with a Gemini theme",
)

for part in response.parts:
    if part.text is not None:
        print(part.text)
    elif part.inline_data is not None:
        part.as_image().save("generated_image.png")
```

### JavaScript

```javascript
import { GoogleGenAI } from "@google/genai";
import * as fs from "node:fs";

const ai = new GoogleGenAI({});

const response = await ai.models.generateContent({
  model: "gemini-2.5-flash-image",
  contents: "Create a picture of a nano banana dish in a fancy restaurant with a Gemini theme",
});

for (const part of response.candidates[0].content.parts) {
  if (part.text) {
    console.log(part.text);
  } else if (part.inlineData) {
    const buffer = Buffer.from(part.inlineData.data, "base64");
    fs.writeFileSync("generated_image.png", buffer);
  }
}
```

### Go

```go
package main

import (
    "context"
    "fmt"
    "log"
    "os"

    "google.golang.org/genai"
)

func main() {
    ctx := context.Background()
    client, err := genai.NewClient(ctx, nil)
    if err != nil {
        log.Fatal(err)
    }

    result, _ := client.Models.GenerateContent(
        ctx,
        "gemini-2.5-flash-image",
        genai.Text("Create a picture of a nano banana dish in a fancy restaurant with a Gemini theme"),
    )

    for _, part := range result.Candidates[0].Content.Parts {
        if part.Text != "" {
            fmt.Println(part.Text)
        } else if part.InlineData != nil {
            os.WriteFile("generated_image.png", part.InlineData.Data, 0644)
        }
    }
}
```

### Java

```java
import com.google.genai.Client;
import com.google.genai.types.GenerateContentConfig;
import com.google.genai.types.GenerateContentResponse;
import com.google.genai.types.Part;
import java.nio.file.Files;
import java.nio.file.Paths;

try (Client client = new Client()) {
    GenerateContentConfig config = GenerateContentConfig.builder()
        .responseModalities("TEXT", "IMAGE")
        .build();

    GenerateContentResponse response = client.models.generateContent(
        "gemini-2.5-flash-image",
        "Create a picture of a nano banana dish in a fancy restaurant with a Gemini theme",
        config);

    for (Part part : response.parts()) {
        if (part.text().isPresent()) {
            System.out.println(part.text().get());
        } else if (part.inlineData().isPresent()) {
            var blob = part.inlineData().get();
            if (blob.data().isPresent()) {
                Files.write(Paths.get("generated_image.png"), blob.data().get());
            }
        }
    }
}
```

### REST

```bash
curl -s -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{
      "parts": [{"text": "Create a picture of a nano banana dish"}]
    }]
  }'
```

---

## Image Editing

Provide an image and use text prompts to add, remove, or modify elements.

### Python

```python
from PIL import Image

image = Image.open("/path/to/image.png")

response = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents=[
        "Add a sunset sky to this image",
        image,
    ],
)

for part in response.parts:
    if part.inline_data is not None:
        part.as_image().save("edited_image.png")
```

### JavaScript

```javascript
const imageData = fs.readFileSync("/path/to/image.png");
const base64Image = imageData.toString("base64");

const response = await ai.models.generateContent({
  model: "gemini-2.5-flash-image",
  contents: [
    { text: "Add a sunset sky to this image" },
    { inlineData: { mimeType: "image/png", data: base64Image } },
  ],
});
```

---

## Multi-turn Editing

Use chat for iterative image refinement with aspect ratio and resolution control.

### Python

```python
from google.genai import types

chat = client.chats.create(
    model="gemini-3-pro-image-preview",
    config=types.GenerateContentConfig(
        response_modalities=['TEXT', 'IMAGE'],
    )
)

# First turn: generate
response = chat.send_message("Create a vibrant infographic that explains photosynthesis")
for part in response.parts:
    if image := part.as_image():
        image.save("infographic.png")

# Second turn: modify with new config
aspect_ratio = "16:9"
resolution = "2K"

config = types.GenerateContentConfig(
    response_modalities=['TEXT', 'IMAGE'],
    image_config=types.ImageConfig(
        aspect_ratio=aspect_ratio,
        image_size=resolution
    ),
)

response = chat.send_message(
    "Update this infographic to be in Spanish. Do not change any other elements.",
    config=config
)

for part in response.parts:
    if image := part.as_image():
        image.save("infographic_spanish.png")
```

### JavaScript

```javascript
const chat = ai.chats.create({
  model: "gemini-3-pro-image-preview",
  config: {
    responseModalities: ['TEXT', 'IMAGE'],
  },
});

let response = await chat.sendMessage({ message: "Create an infographic about photosynthesis" });
// Save first image...

response = await chat.sendMessage({
  message: "Update this infographic to be in Spanish",
  config: {
    responseModalities: ['TEXT', 'IMAGE'],
    imageConfig: {
      aspectRatio: "16:9",
      imageSize: "2K"
    }
  }
});
```

---

## Gemini 3 Pro Image Features

### High Resolution Output (1K, 2K, 4K)

Use uppercase 'K'. Lowercase will be rejected.

```python
response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents="Da Vinci style anatomical sketch of a butterfly with detailed notes",
    config=types.GenerateContentConfig(
        response_modalities=['TEXT', 'IMAGE'],
        image_config=types.ImageConfig(
            aspect_ratio="1:1",
            image_size="4K"
        ),
    )
)
```

### Google Search Grounding

Generate images based on real-time information (weather, stock charts, current events).

```python
response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents="Visualize the current weather forecast for the next 5 days in San Francisco as a clean, modern weather chart. Add a visual on what I should wear each day",
    config=types.GenerateContentConfig(
        response_modalities=['TEXT', 'IMAGE'],
        image_config=types.ImageConfig(aspect_ratio="16:9"),
        tools=[{"google_search": {}}]
    )
)
```

The response includes `groundingMetadata` with:
- `searchEntryPoint`: HTML/CSS for required search suggestions
- `groundingChunks`: Top 3 web sources used

### Multiple Reference Images (Up to 14)

Mix up to 14 reference images:
- Up to 6 images of objects with high-fidelity
- Up to 5 images of humans for character consistency

```python
from PIL import Image

response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents=[
        "An office group photo of these people, they are making funny faces",
        Image.open('person1.png'),
        Image.open('person2.png'),
        Image.open('person3.png'),
        Image.open('person4.png'),
        Image.open('person5.png'),
    ],
    config=types.GenerateContentConfig(
        response_modalities=['TEXT', 'IMAGE'],
        image_config=types.ImageConfig(
            aspect_ratio="5:4",
            image_size="2K"
        ),
    )
)
```

### Thinking Mode

Gemini 3 Pro Image uses a "thinking" process to reason through complex prompts. It generates interim "thought images" (visible in response but not charged) to refine composition.

```python
for part in response.parts:
    if part.thought:
        if part.text:
            print("Thought:", part.text)
        elif image := part.as_image():
            image.show()  # Interim composition test
```

---

## Thought Signatures

For Gemini 3 Pro Image, thought signatures are critical for conversational editing. The model relies on signatures to understand the composition and logic of previous images.

### Signature Location

- First part after thoughts (text or image): **Always has signature**
- All subsequent `inlineData` (image) parts: **Always have signatures**
- Thought parts: **No signatures**

### Example Response Structure

```json
[
  {
    "text": "Let me think about this...",
    "thought": true
  },
  {
    "inline_data": {"data": "<thought_image>", "mime_type": "image/png"},
    "thought": true
  },
  {
    "text": "Here is the final result...",
    "thought_signature": "<Signature_A>"
  },
  {
    "inline_data": {"data": "<final_image>", "mime_type": "image/png"},
    "thought_signature": "<Signature_B>"
  }
]
```

### Editing Requests

When requesting edits, return ALL signatures in the history:

```json
{
  "contents": [
    {"role": "user", "parts": [{"text": "Generate a cyberpunk city"}]},
    {
      "role": "model",
      "parts": [
        {"text": "...", "thoughtSignature": "<Sig_A>"},
        {"inlineData": "...", "thoughtSignature": "<Sig_B>"}
      ]
    },
    {"role": "user", "parts": [{"text": "Make it daytime."}]}
  ]
}
```

**Note**: SDKs handle signatures automatically when using standard chat history.

---

## Prompting Guide

### Core Principle

**Describe the scene, don't list keywords.** A narrative paragraph produces better results than disconnected words.

### Template: Photorealistic

```
A photorealistic [shot type] of [subject], [action/expression], set in [environment].
The scene is illuminated by [lighting], creating a [mood] atmosphere.
Captured with a [camera/lens], emphasizing [key details]. [Aspect ratio].
```

**Example:**
```
A photorealistic close-up portrait of an elderly Japanese ceramicist with deep,
sun-etched wrinkles and a warm, knowing smile. He is carefully inspecting a freshly
glazed tea bowl. The setting is his rustic, sun-drenched workshop. The scene is
illuminated by soft, golden hour light streaming through a window. Captured with
an 85mm portrait lens, resulting in soft bokeh. Vertical portrait orientation.
```

### Template: Stylized/Stickers

```
A [style]-style sticker of a [subject] [action]. The design features
[characteristics] and a [color palette]. [Background].
```

**Example:**
```
A kawaii-style sticker of a happy red panda wearing a tiny bamboo hat.
It's munching on a green bamboo leaf. The design features bold, clean outlines,
simple cel-shading, and a vibrant color palette. The background must be white.
```

### Template: Text in Images

Use Gemini 3 Pro Image Preview for accurate text rendering.

```
Create a [image type] for [brand/concept] with the text "[text]" in a [font style].
The design should be [style], with a [color scheme].
```

**Example:**
```
Create a modern, minimalist logo for a coffee shop called 'The Daily Grind'.
The text should be in a clean, bold, sans-serif font. The color scheme is
black and white. Put the logo in a circle. Use a coffee bean in a clever way.
```

### Template: Product Mockups

```
A high-resolution, studio-lit product photograph of [product] on [surface].
The lighting is [setup] to [purpose]. The camera angle is [angle] to showcase [feature].
Ultra-realistic, with sharp focus on [detail]. [Aspect ratio].
```

### Template: Minimalist/Negative Space

```
A minimalist composition featuring a single [subject] positioned in the [position]
of the frame. The background is [background description] with [texture/gradient].
```

### Pro Tips

- **Be hyper-specific**: "ornate elven plate armor with silver leaf patterns" vs "fantasy armor"
- **Provide context**: "logo for a high-end minimalist skincare brand" vs "logo"
- **Iterate conversationally**: "Make the lighting warmer" or "Change the expression"
- **Use step-by-step**: Break complex scenes into sequential instructions
- **Control camera**: Use terms like `wide-angle shot`, `macro shot`, `low-angle perspective`
- **Use "semantic negative prompts"**: Describe desired scene positively instead of "no cars"

---

## Editing Techniques

### 1. Add/Remove Elements

```
Using the provided image of [subject], please [add/remove/modify] [element].
Ensure the change [integration description].
```

**Example:**
```python
response = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents=[
        "Using the provided image of my cat, please add a small, knitted wizard hat on its head. Make it look comfortable and not falling off.",
        Image.open("cat.png"),
    ],
)
```

### 2. Inpainting (Semantic Masking)

Edit specific parts while preserving the rest.

```
Using the provided image, change only the [specific element] to [new element].
Keep everything else exactly the same, preserving style, lighting, and composition.
```

**Example:**
```python
response = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents=[
        Image.open("living_room.png"),
        "Using the provided image, change only the blue sofa to a vintage brown leather chesterfield. Keep the rest unchanged.",
    ],
)
```

### 3. Style Transfer

```
Transform the provided photograph of [subject] into the artistic style of [artist/style].
Preserve the original composition but render with [stylistic elements].
```

**Example:**
```python
response = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents=[
        Image.open("city.png"),
        "Transform this into Vincent van Gogh's 'Starry Night' style with swirling brushstrokes and deep blues and bright yellows.",
    ],
)
```

### 4. Combining Multiple Images

```
Create a new image by combining elements from the provided images.
Take [element from image 1] and place it with [element from image 2].
The final image should be [description].
```

**Example:**
```python
response = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents=[
        Image.open("dress.png"),
        Image.open("model.png"),
        "Create a professional e-commerce photo. Take the blue floral dress from the first image and let the woman from the second image wear it.",
    ],
)
```

### 5. High-Fidelity Object Integration

Place objects on subjects while preserving identity.

```python
response = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents=[
        Image.open("woman.png"),
        Image.open("logo.png"),
        "Add the logo from the second image onto her black t-shirt. Ensure the woman's face remains unchanged. The logo should look naturally printed.",
    ],
)
```

### 6. Sketch to Image

Transform rough sketches into polished images.

```python
response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents=[
        Image.open("car_sketch.png"),
        "Turn this rough pencil sketch of a futuristic car into a polished photo of the finished concept car in a showroom. Keep the sleek lines but add metallic blue paint and neon rim lighting.",
    ],
)
```

### 7. Character Consistency (360 View)

Generate consistent views by including previous outputs.

```
A studio portrait of [person] against [background], [looking forward/in profile looking right/etc.]
```

```python
# Generate profile view
response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents=[
        "A studio portrait of this man against white, in profile looking right",
        Image.open("person_front.png"),
    ],
)
```

### 8. Sequential Art (Comics/Storyboards)

Use Gemini 3 Pro Image for text accuracy.

```python
response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents=[
        "Make a 3 panel comic in a gritty noir art style with high-contrast black and white inks. Put the character in a humorous scene.",
        Image.open("character_reference.png"),
    ],
)
```

---

## Configuration

### Response Modalities

```python
# Image only (no text)
config=types.GenerateContentConfig(
    response_modalities=['Image']
)

# Text and image (default)
config=types.GenerateContentConfig(
    response_modalities=['TEXT', 'IMAGE']
)
```

### Aspect Ratios

Available: `1:1`, `2:3`, `3:2`, `3:4`, `4:3`, `4:5`, `5:4`, `9:16`, `16:9`, `21:9`

```python
config=types.GenerateContentConfig(
    image_config=types.ImageConfig(
        aspect_ratio="16:9",
    )
)
```

### Image Size (Gemini 3 Pro only)

Use uppercase 'K': `"1K"`, `"2K"`, `"4K"`

```python
config=types.GenerateContentConfig(
    image_config=types.ImageConfig(
        aspect_ratio="1:1",
        image_size="2K"
    )
)
```

---

## Limitations

- **Languages**: Best in EN, ar-EG, de-DE, es-MX, fr-FR, hi-IN, id-ID, it-IT, ja-JP, ko-KR, pt-BR, ru-RU, ua-UA, vi-VN, zh-CN
- **Input**: No audio or video inputs for image generation
- **Image count**: Model may not follow exact number of requested outputs
- **Nano Banana**: Best with up to 3 input images
- **Nano Banana Pro**: Up to 5 high-fidelity images, 14 total
- **Text generation tip**: Generate text first, then ask for image with that text

---

## Batch Generation

For high-volume generation, use the [Batch API](https://ai.google.dev/gemini-api/docs/batch-api) for higher rate limits (24-hour turnaround).

---

## Resources

- [Image Generation Guide](https://ai.google.dev/gemini-api/docs/image-generation)
- [Nano Banana Cookbook](https://colab.research.google.com/github/google-gemini/cookbook/blob/main/quickstarts/Get_Started_Nano_Banana.ipynb)
- [Batch API Image Examples](https://ai.google.dev/gemini-api/docs/batch-api#image-generation)
- [Imagen (alternative model)](https://ai.google.dev/gemini-api/docs/imagen)
