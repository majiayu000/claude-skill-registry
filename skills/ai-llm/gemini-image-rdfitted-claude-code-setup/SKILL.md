---
name: gemini-image
description: Invoke Google Gemini for image generation and understanding using the Python google-genai SDK. Supports gemini-3-pro-image-preview (generation + understanding), gemini-2.5-flash-image (fast generation), and vision models for analysis.
---

# Gemini Image Skill

Invoke Google Gemini models for image generation, image understanding, and visual analysis using the Python `google-genai` SDK.

## Available Models

| Model ID | Description | Best For | Output Format |
|----------|-------------|----------|---------------|
| `gemini-3-pro-image-preview` | Best image generation + understanding | High-quality image gen, complex visual analysis | JPEG |
| `gemini-2.5-flash-image` | Fast image generation | Quick image creation | PNG |
| `gemini-3-pro-preview` | Multimodal understanding | Image analysis without generation | N/A |
| `gemini-2.5-flash` | Fast vision | Quick image analysis | N/A |

## Configuration

**API Key**: `${GEMINI_API_KEY}`

## Usage

### Image Generation

```bash
python -c "
from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

response = client.models.generate_content(
    model='gemini-3-pro-image-preview',  # Returns JPEG | Use gemini-2.5-flash-image for PNG
    contents='Generate an image of a sunset over mountains',
    config=types.GenerateContentConfig(
        response_modalities=['IMAGE', 'TEXT']
    )
)

# Map mime types to file extensions
mime_to_ext = {'image/png': '.png', 'image/jpeg': '.jpg', 'image/gif': '.gif', 'image/webp': '.webp'}

# Save generated image
if response.candidates and response.candidates[0].content:
    for part in response.candidates[0].content.parts:
        if hasattr(part, 'inline_data') and part.inline_data:
            ext = mime_to_ext.get(part.inline_data.mime_type, '.png')
            filename = f'output{ext}'
            # Data is already raw bytes - no base64 decode needed
            with open(filename, 'wb') as f:
                f.write(part.inline_data.data)
            print(f'Image saved to {filename} ({part.inline_data.mime_type})')
        elif hasattr(part, 'text'):
            print(part.text)
"
```

### Image Understanding (Analyze Image from File)

```bash
python -c "
from google import genai
from google.genai import types
import base64

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# Read image file - must be base64 encoded for INPUT
with open('IMAGE_PATH', 'rb') as f:
    image_data = base64.b64encode(f.read()).decode('utf-8')

response = client.models.generate_content(
    model='gemini-3-pro-preview',
    contents=[
        types.Content(parts=[
            types.Part(text='Describe this image in detail'),
            types.Part(inline_data=types.Blob(mime_type='image/png', data=image_data))
        ])
    ]
)
print(response.text)
"
```

### Image Understanding (From URL)

```bash
python -c "
from google import genai
from google.genai import types
import urllib.request
import base64

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# Fetch image from URL - must be base64 encoded for INPUT
url = 'IMAGE_URL_HERE'
with urllib.request.urlopen(url) as response:
    image_data = base64.b64encode(response.read()).decode('utf-8')

response = client.models.generate_content(
    model='gemini-3-pro-preview',
    contents=[
        types.Content(parts=[
            types.Part(text='What is in this image?'),
            types.Part(inline_data=types.Blob(mime_type='image/jpeg', data=image_data))
        ])
    ]
)
print(response.text)
"
```

## Workflow

When this skill is invoked:

1. **Determine the task type**:
   - **Image Generation**: User wants to create an image
   - **Image Understanding**: User wants to analyze an existing image
   - **Image Editing**: User wants to modify an image (generation with reference)

2. **Select the appropriate model**:
   - Image generation → `gemini-3-pro-image-preview` (JPEG) or `gemini-2.5-flash-image` (PNG)
   - Image analysis → `gemini-3-pro-preview` or `gemini-2.5-flash`

3. **Prepare the input**:
   - For generation: Text prompt describing desired image
   - For understanding: Load image file as base64

4. **Execute and handle output**:
   - Generation: Save binary image data to file
   - Understanding: Return text description

## Example Invocations

### Generate Product Image
```bash
python -c "
from google import genai
from google.genai import types

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

response = client.models.generate_content(
    model='gemini-3-pro-image-preview',
    contents='Create a professional product photo of a sleek wireless headphone on a white background, studio lighting',
    config=types.GenerateContentConfig(
        response_modalities=['IMAGE', 'TEXT']
    )
)

mime_to_ext = {'image/png': '.png', 'image/jpeg': '.jpg', 'image/gif': '.gif', 'image/webp': '.webp'}

if response.candidates and response.candidates[0].content:
    for part in response.candidates[0].content.parts:
        if hasattr(part, 'inline_data') and part.inline_data:
            ext = mime_to_ext.get(part.inline_data.mime_type, '.png')
            with open(f'headphone{ext}', 'wb') as f:
                f.write(part.inline_data.data)
            print(f'Image saved to headphone{ext}')
"
```

### Analyze Screenshot
```bash
python -c "
from google import genai
from google.genai import types
import base64

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

with open('screenshot.png', 'rb') as f:
    image_data = base64.b64encode(f.read()).decode('utf-8')

response = client.models.generate_content(
    model='gemini-3-pro-preview',
    contents=[
        types.Content(parts=[
            types.Part(text='Analyze this UI screenshot. Identify any usability issues and suggest improvements.'),
            types.Part(inline_data=types.Blob(mime_type='image/png', data=image_data))
        ])
    ]
)
print(response.text)
"
```

### OCR / Extract Text from Image
```bash
python -c "
from google import genai
from google.genai import types
import base64

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

with open('document.png', 'rb') as f:
    image_data = base64.b64encode(f.read()).decode('utf-8')

response = client.models.generate_content(
    model='gemini-3-pro-preview',
    contents=[
        types.Content(parts=[
            types.Part(text='Extract all text from this image. Preserve formatting where possible.'),
            types.Part(inline_data=types.Blob(mime_type='image/png', data=image_data))
        ])
    ]
)
print(response.text)
"
```

### Compare Two Images
```bash
python -c "
from google import genai
from google.genai import types
import base64

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

with open('image1.png', 'rb') as f:
    img1_data = base64.b64encode(f.read()).decode('utf-8')
with open('image2.png', 'rb') as f:
    img2_data = base64.b64encode(f.read()).decode('utf-8')

response = client.models.generate_content(
    model='gemini-3-pro-preview',
    contents=[
        types.Content(parts=[
            types.Part(text='Compare these two images. What are the key differences?'),
            types.Part(inline_data=types.Blob(mime_type='image/png', data=img1_data)),
            types.Part(inline_data=types.Blob(mime_type='image/png', data=img2_data))
        ])
    ]
)
print(response.text)
"
```

## Image Generation Parameters

When generating images, you can customize:

```python
config=types.GenerateContentConfig(
    response_modalities=['IMAGE', 'TEXT'],  # Request both image and description
    temperature=1.0,  # Higher = more creative
    # Additional parameters may be model-specific
)
```

## Supported Image Formats

**Input (for understanding)**:
- PNG (`image/png`)
- JPEG (`image/jpeg`)
- GIF (`image/gif`)
- WebP (`image/webp`)

**Output (from generation)**:
- PNG (default, `image/png`)
- The API returns raw bytes in `part.inline_data.data` (NOT base64 encoded)
- Check `part.inline_data.mime_type` to determine the actual format returned

## Error Handling

Common errors and solutions:
- **Image too large**: Resize image before sending (max varies by model)
- **Unsupported format**: Convert to PNG/JPEG
- **Generation blocked**: Adjust prompt to comply with safety guidelines
- **Rate limiting**: Implement retry with exponential backoff

## Notes

- Image generation requires `response_modalities=['IMAGE', 'TEXT']` in config
- For best results with generation, be specific and descriptive in prompts
- Image understanding works with both local files and URLs
- Multiple images can be sent in a single request for comparison
- Gemini 3 Pro Image is NOT available via CLI - must use Python SDK

## Tools to Use

- **Bash**: Execute Python commands
- **Read**: Load image files (binary mode)
- **Write**: Save generated images
- **Glob**: Find image files in directories
