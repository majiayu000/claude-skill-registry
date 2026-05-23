---
name: seedance-prompter
description: >
  Expert prompt engineering for Seedance 2.0. Use when the user wants to generate a video with multimodal assets (images, videos, audio) and needs the best possible prompt.
version: 2.1.0
author: wells1137
tags: [video, generation, prompt, seedance, multimodal]
---

# Seedance Prompt Designer Skill

This skill transforms a user's scattered multimodal assets (images, videos, audio) and ambiguous creative intent into a structured, executable prompt for the Seedance 2.0 video generation model. It acts as an expert prompt engineer, ensuring the highest quality output from the underlying model.

## When to Use

- When the user provides multiple assets (images, videos, audio) for video generation.
- When the user's request is complex and requires careful prompt construction.
- When using the Seedance 2.0 model for video generation.

## Core Function

This skill analyzes all user inputs and generates a single, optimized JSON object containing the final prompt and recommended parameters. The internal workflow (Recognition, Mapping, Construction) is handled automatically and should not be exposed to the user.

## Usage Example

**User Request:** "Make the Mona Lisa drink a Coke. I want it to feel cinematic, like a close-up shot."
*User uploads `monalisa.png` and `coke.png`*

**Agent using `seedance-prompter`:**
*The agent internally processes the request and assets, then outputs the final JSON to the next skill in the chain.*

**Final Output (for internal use):**
```json
{
  "final_prompt": "A cinematic close-up shot of a woman picking up a bottle of Coke and taking a sip. The scene is lit with dramatic, high-contrast lighting. Use @monalisa as the subject reference, and the object appearing in the video is @coke.",
  "recommended_parameters": {
    "duration": 8,
    "aspect_ratio": "16:9"
  }
}
```

## Knowledge Base

This skill relies on an internal knowledge base to make informed decisions. The agent MUST consult these files during execution.

- **`/references/atomic_element_mapping.md`**: **Core Knowledge**. Contains the "Asset Type -> Atomic Element" and "Atomic Element -> Optimal Reference Method" mapping tables.
- **`/references/seedance_syntax_guide.md`**: Seedance 2.0 "@asset_name" syntax reference.
- **`/references/prompt_templates.md`**: Advanced prompt templates for different genres (e.g., Cinematic, Product Showcase, Narrative).
