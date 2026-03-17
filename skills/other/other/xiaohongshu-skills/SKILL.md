---
name: xiaohongshu-cover-generator
description: Generate Xiaohongshu (小红书) style cover images based on user topics. Use when the user wants to create a social media cover image in Xiaohongshu style, or mentions keywords like "小红书封面", "Xiaohongshu cover", "封面生成", or provides a topic for cover image generation. The generated image will be saved to the current project directory.
---

# Xiaohongshu Cover Generator

This skill generates Xiaohongshu-style cover images based on user-provided topics.

## Usage

When a user requests a Xiaohongshu cover image:

1. Confirm the topic with the user if not clear
2. Check for API key (CANGHE_API_KEY environment variable or ask user to provide it)
3. Run the generation script with the topic
4. The image will be saved to the current working directory with filename format: `xiaohongshu-cover-{timestamp}.png`

## Running the Script

The script is located at `scripts/handler.ts` and requires:
- Topic (required): The subject for the cover image
- API Key (required): Either via environment variable `CANGHE_API_KEY` or passed as argument

Execute with:
```bash
cd ~/.codebuddy/skills/xiaohongshu-cover-generator
npx tsx scripts/handler.ts "<topic>" "<api-key-optional>"
```

Or with environment variable:
```bash
cd ~/.codebuddy/skills/xiaohongshu-cover-generator
CANGHE_API_KEY="your-api-key" npx tsx scripts/handler.ts "<topic>"
```

## API Key

Users need a valid API key from https://api.canghe.ai/

If the API key is missing or invalid, provide the user with clear instructions to obtain one.

## Output

The generated image will be saved to **the directory where the skill was invoked** (current working directory), not the skill's directory. The filename format is `xiaohongshu-cover-{timestamp}.png` where timestamp is in milliseconds.

## Style Specifications

The generated images follow these specifications:
- Aspect ratio: 3:4 (vertical, mobile-friendly)
- Style: Clean, refined, youthful aesthetic
- Automatic removal of watermarks and logos
- High-quality output suitable for mobile viewing
- Text should be clear and readable with appropriate sizing
