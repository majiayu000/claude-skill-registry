---
name: vision-multimodal
description: Vision and multimodal capabilities for Claude including image analysis, PDF processing, and document understanding. Activate for image input, base64 encoding, multiple images, and visual analysis.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Task
  - WebFetch
triggers:
  - vision
  - image
  - multimodal
  - base64
  - screenshot
  - pdf
  - document
  - ocr
  - visual
  - picture
dependencies:
  - llm-integration
related-skills:
  - extended-thinking
  - citations-retrieval
---

# Vision & Multimodal Skill

Leverage Claude's vision capabilities for image analysis, document processing, and multimodal understanding.

## When to Use This Skill

- Image analysis and description
- Document/PDF processing
- Screenshot analysis
- OCR-like text extraction
- Visual comparison
- Chart and diagram interpretation

## Supported Formats

| Format | Status | Best For |
|--------|--------|----------|
| JPEG | ✓ | Photos, natural scenes |
| PNG | ✓ | Screenshots, UI, text |
| GIF | ✓ | Animated (first frame) |
| WebP | ✓ | Modern, compressed |
| PDF | ✓ | Documents (via Files API) |

## Image Size Guidelines

- **Minimum:** 200 pixels (smaller = reduced accuracy)
- **Optimal:** 1000x1000 pixels
- **Maximum:** 8000x8000 pixels
- **Token cost:** ~(width × height) / 1000
- **Tip:** Resize to 1568px max dimension for 30-50% token savings

## Core Patterns

### Pattern 1: Single Image Analysis

```python
import anthropic
import base64

client = anthropic.Anthropic()

# Load and encode image
with open("image.jpg", "rb") as f:
    image_data = base64.standard_b64encode(f.read()).decode("utf-8")

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": [
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/jpeg",
                    "data": image_data
                }
            },
            {
                "type": "text",
                "text": "Describe this image in detail."
            }
        ]
    }]
)
```

### Pattern 2: Image from URL

```python
import httpx

# Fetch and encode from URL
image_url = "https://example.com/image.jpg"
response = httpx.get(image_url)
image_data = base64.standard_b64encode(response.content).decode("utf-8")

# Then use same pattern as above
```

### Pattern 3: Multiple Images

```python
# Compare multiple images (up to 100 per request)
messages = [{
    "role": "user",
    "content": [
        {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": image1}},
        {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": image2}},
        {"type": "text", "text": "Compare these two images and list the differences."}
    ]
}]
```

### Pattern 4: Few-Shot with Images

```python
# Teach by example
messages = [
    # Example 1
    {"role": "user", "content": [
        {"type": "image", "source": {...}},
        {"type": "text", "text": "Classify this image."}
    ]},
    {"role": "assistant", "content": "Category: Landscape\nElements: Mountains, lake, trees"},

    # Example 2
    {"role": "user", "content": [
        {"type": "image", "source": {...}},
        {"type": "text", "text": "Classify this image."}
    ]},
    {"role": "assistant", "content": "Category: Portrait\nElements: Person, indoor, professional"},

    # Target image
    {"role": "user", "content": [
        {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": target_image}},
        {"type": "text", "text": "Classify this image."}
    ]}
]
```

### Pattern 5: PDF Processing

```python
# Using Files API (beta)
with open("document.pdf", "rb") as f:
    pdf_data = base64.standard_b64encode(f.read()).decode("utf-8")

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=4096,
    messages=[{
        "role": "user",
        "content": [
            {
                "type": "document",
                "source": {
                    "type": "base64",
                    "media_type": "application/pdf",
                    "data": pdf_data
                }
            },
            {"type": "text", "text": "Summarize this document."}
        ]
    }]
)
```

## Prompt Engineering for Vision

### Strategy 1: Role Assignment

```python
prompt = """You have perfect vision and exceptional attention to detail,
making you an expert at analyzing technical diagrams.

Analyze this architecture diagram and identify:
1. All components
2. Data flow between components
3. Potential bottlenecks"""
```

### Strategy 2: Step-by-Step Thinking

```python
prompt = """Before answering, analyze the image systematically:

<thinking>
1. What is the overall subject?
2. What are the key elements?
3. How do elements relate to each other?
4. What details stand out?
</thinking>

Then provide your answer based on this analysis."""
```

### Strategy 3: Structured Output

```python
prompt = """Extract information from this receipt and return as JSON:

{
    "vendor": "",
    "date": "",
    "items": [{"name": "", "price": 0}],
    "total": 0
}"""
```

## Image Optimization

```python
from PIL import Image
import io

def optimize_for_claude(image_path, max_dimension=1568):
    """Resize image to reduce token usage by 30-50%"""
    with Image.open(image_path) as img:
        # Calculate new dimensions
        ratio = min(max_dimension / img.width, max_dimension / img.height)
        if ratio < 1:
            new_size = (int(img.width * ratio), int(img.height * ratio))
            img = img.resize(new_size, Image.LANCZOS)

        # Convert to bytes
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=85)
        return base64.standard_b64encode(buffer.getvalue()).decode("utf-8")
```

## Common Use Cases

### Text Extraction (OCR-like)

```python
prompt = """Extract all text from this image.
Preserve the original formatting and structure as much as possible.
If text is unclear, indicate with [unclear]."""
```

### Table Extraction

```python
prompt = """Extract the table data from this image.
Return as a markdown table with proper headers and alignment."""
```

### Chart Analysis

```python
prompt = """Analyze this chart:
1. What type of chart is this?
2. What are the axes/labels?
3. What are the key data points?
4. What trends or patterns are visible?"""
```

## Best Practices

### DO:
- Use high-quality images (≥1000px)
- Resize large images to save tokens
- Provide context about what to look for
- Use few-shot examples for consistent output

### DON'T:
- Send images smaller than 200px
- Expect perfect OCR for handwriting
- Send very large images (>8000px)
- Ignore token costs for multiple images

## Limitations

- Cannot identify specific individuals
- May struggle with very small text
- Animated GIFs: only first frame analyzed
- Some specialized symbols may be misread

## See Also

- [[llm-integration]] - API basics
- [[extended-thinking]] - Complex reasoning
- [[citations-retrieval]] - Document citations
