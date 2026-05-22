---
name: ai-analysis
description: >
  Command-line tools that delegate analysis tasks to AI models. Includes image
  description, screenshot comparison, essay generation from text, and boolean
  condition evaluation. Use for describing images, comparing UI states,
  generating reports, evaluating conditions, or any task requiring AI inference.
  Triggers: ai analysis, describe image, compare screenshots, generate essay,
  evaluate condition, alt text, image description, UI comparison, visual diff,
  satisfies condition, boolean evaluation, gemini.
compatibility: >
  Requires curl and jq. Image tools also need base64 and magick (ImageMagick).
  Needs GEMINI_API_KEY environment variable and network access to
  generativelanguage.googleapis.com.
---

# AI Analysis Tools

## Quick Start

**Environment:** Set `GEMINI_API_KEY` before running any commands.

**Dependencies:** `curl`, `jq` (all tools); `base64`, `magick` (image tools only)

```bash
# Describe an image (generate alt-text)
scripts/screenshot-describe screenshot.png

# Compare two images for visual differences
scripts/screenshot-compare before.png after.png

# Generate essay-length analysis from text
scripts/emerson "Summarize the key changes" < documentation.md

# Evaluate a boolean condition against text
echo "Hello world" | scripts/satisfies "is a greeting"
```

## Script Overview

### screenshot-describe

Generate concise alt-text for an image. Optimized for UI captures.

```bash
scripts/screenshot-describe IMAGE [PROMPT]
```

**Exit codes:** 0 success, 1 error, 127 missing dependency

### screenshot-compare

Compare two images for visual differences. Identifies layout shifts, color changes, padding, and text updates.

```bash
scripts/screenshot-compare IMAGE1 IMAGE2 [PROMPT]
```

**Exit codes:** 0 differences found, 1 error, 2 images identical, 127 missing dependency

### emerson

Generate essay-length (~3000 words) analysis from text input. Produces authoritative, footnoted Markdown.

```bash
scripts/emerson "PROMPT" < input.txt
```

**Exit codes:** 0 success, 1 error, 127 missing dependency

### satisfies

Evaluate whether input text satisfies a condition. Returns boolean via exit code.

```bash
echo "text" | scripts/satisfies "CONDITION"
```

**Exit codes:** 0 true (satisfies), 1 false (does not satisfy), 127 missing dependency

**Examples:**
```bash
# Check if file mentions a topic
cat file.txt | scripts/satisfies "mentions Elvis" && echo "Found it"

# Validate content type
cat response.json | scripts/satisfies "is valid JSON with an 'id' field"

# Use in conditionals
if cat log.txt | scripts/satisfies "contains error messages"; then
  echo "Errors detected"
fi
```

## Raw API Fallback

When scripts fail due to missing dependencies or environment issues, use these curl commands directly.

### Describing an Image

Model: `gemini-2.5-flash`

```bash
IMAGE_BASE64=$(magick image.png -alpha off -define webp:lossless=true webp:- | base64 -w 0)

curl -s -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{
      "parts": [
        {"inlineData": {"mimeType": "image/webp", "data": "'"$IMAGE_BASE64"'"}},
        {"text": "Generate concise alt text describing this screenshot."}
      ]
    }]
  }' | jq -r '.candidates[0].content.parts[0].text'
```

### Comparing Two Images

Model: `gemini-3-flash-preview`

```bash
IMG1_B64=$(magick before.png -alpha off -define webp:lossless=true webp:- | base64 -w 0)
IMG2_B64=$(magick after.png -alpha off -define webp:lossless=true webp:- | base64 -w 0)

curl -s -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{
      "parts": [
        {"text": "Compare these two screenshots. Describe the visual differences."},
        {"inlineData": {"mimeType": "image/webp", "data": "'"$IMG1_B64"'"}},
        {"inlineData": {"mimeType": "image/webp", "data": "'"$IMG2_B64"'"}}
      ]
    }]
  }' | jq -r '.candidates[0].content.parts[0].text'
```

### Text Analysis (Emerson-style)

Model: `gemini-3-pro-preview`

```bash
INPUT_TEXT=$(cat document.txt)
PROMPT="Summarize the key points"

curl -s -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-preview:generateContent" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d "$(jq -n \
    --arg text "$INPUT_TEXT" \
    --arg prompt "$PROMPT" \
    '{
      contents: [{
        role: "user",
        parts: [
          {text: ("Reference Material:\n\n" + $text)},
          {text: ("\n\nTask/Question:\n" + $prompt)}
        ]
      }],
      generationConfig: {temperature: 1.0, maxOutputTokens: 8192}
    }')" | jq -r '.candidates[0].content.parts[0].text'
```

### Boolean Condition Evaluation

Model: `gemini-2.5-flash-lite`

```bash
INPUT_TEXT=$(cat file.txt)
CONDITION="mentions Elvis"

RESPONSE=$(curl -s -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d "$(jq -n \
    --arg input "$INPUT_TEXT" \
    --arg cond "$CONDITION" \
    '{
      contents: [{
        parts: [
          {text: $input},
          {text: ("Does the above text satisfy the condition: " + $cond)}
        ]
      }],
      generationConfig: {
        responseMimeType: "application/json",
        responseSchema: {
          type: "object",
          properties: {satisfies: {type: "boolean"}},
          required: ["satisfies"]
        }
      }
    }')")

echo "$RESPONSE" | jq -r '.candidates[0].content.parts[0].text' | jq -e '.satisfies'
```

## Image Encoding Notes

- Images converted to lossless WebP for consistent encoding
- Alpha channel removed (`-alpha off`) so transparency-only differences are ignored
- Base64: use `-w 0` (Linux) or `-b 0` (macOS) for single-line output
- Single-image prompts: image before text (Gemini best practice)
- Multi-image comparison: text before images (Gemini best practice)

## Safety Notes

- Scripts require network access to the Gemini API
- `GEMINI_API_KEY` must be set in the environment
- API calls may incur usage costs
- Large images increase request size and latency
- Scripts do not store or log input data

## References

- [Command Index](references/command-index.md) - Detailed documentation for each script
- [Troubleshooting](references/troubleshooting.md) - Common issues and solutions
