---
name: unsloth-tts
description: Fine-tuning Text-to-Speech (TTS) models with Unsloth for voice cloning and synthetic speech (triggers: TTS, text-to-speech, voice cloning, Orpheus-TTS, audio fine-tuning, speech synthesis).
---

## Overview
Unsloth-tts brings the library's performance optimizations to speech synthesis models. Specifically optimized for the Llama-based Orpheus-TTS architecture, it enables high-quality voice cloning with 50% less memory than standard implementations.

## When to Use
- When creating custom voice clones that require realistic phrasing and emotional quirks.
- When fine-tuning Orpheus-TTS for specialized synthesis (e.g., laughter, sighs).
- When deploying TTS models via llama.cpp or GGUF.

## Decision Tree
1. Is high audio quality the priority over VRAM?
   - Yes: Load with `load_in_4bit = False`.
2. Does the target voice have specific quirks (e.g., laughter)?
   - Yes: Annotate transcripts with emotion tags like `<laughs>`.
3. Is this a quick test or full replication?
   - Quick test: Set `max_steps = 60`.
   - Full replication: Train for 1 full epoch with 1-3 hours of data.

## Workflows
1. **Voice Cloning with LoRA**: Load `orpheus-3b-0.1-pretrained`, prepare 1-3 hours of annotated audio/text data, and apply LoRA adapters.
2. **Audio Data Preprocessing**: Cast audio columns to 24,000Hz (for Orpheus) and tokenize text while preserving special tags like `<sigh>`.
3. **Training and Evaluation**: Train with low batch size (1) and high learning rate (2e-4), saving only the LoRA adapters for portability.

## Non-Obvious Insights
- Zero-shot voice cloning often fails to capture subtle phrasing; LoRA fine-tuning is necessary for true personality replication.
- Orpheus-TTS is highly beginner-friendly because its Llama-based architecture is compatible with existing LLM tools like GGUF.
- Unlike some TTS systems, models like Orpheus can decode audio output tokens directly into waveforms without needing a separate vocoder.

## Evidence
- "Unsloth supports any transformers compatible TTS model... 1.5x faster with 50% less memory than other implementations." [Source](https://docs.unsloth.ai/basics/text-to-speech-tts-fine-tuning)
- "Orpheus supports tags like <laugh>, <chuckle>, <sigh>... These tags are enclosed in angle brackets and will be treated as special tokens." [Source](https://docs.unsloth.ai/basics/text-to-speech-tts-fine-tuning)

## Scripts
- `scripts/unsloth-tts_tool.py`: Audio preprocessing and Orpheus loading.
- `scripts/unsloth-tts_tool.js`: Utility for managing transcript tagging.

## Dependencies
- `unsloth`
- `librosa` / `soundfile`
- `datasets`

## References
- [references/README.md](references/README.md)