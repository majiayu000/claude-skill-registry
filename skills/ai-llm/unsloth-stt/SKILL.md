---
name: unsloth-stt
description: Fine-tuning Speech-to-Text models like Whisper using Unsloth's optimized LoRA pipeline. Triggers: stt, whisper, transcription, audio fine-tuning, speech-to-text, audio normalization.
---

## Overview
Unsloth supports fine-tuning for Speech-to-Text (STT) models like OpenAI Whisper. By applying its optimized LoRA pipeline to Whisper architecture, Unsloth achieves 1.5x faster training with 50% less memory usage compared to standard methods.

## When to Use
- When you need to capture specialized terminology (medical, legal) that base Whisper misses.
- When adapting models to specific accents or dialects.
- When fine-tuning large models (like whisper-large-v3) on limited consumer hardware.

## Decision Tree
1. Is transcription accuracy low on zero-shot inference?
   - Yes: Proceed with STT fine-tuning.
2. Is audio recorded at a non-standard sample rate?
   - Yes: Resample to 16kHz before training.
3. Using large-v3?
   - Yes: Load in 4-bit and apply LoRA to cross-attention layers.

## Workflows

### Whisper STT Data Preprocessing
1. Load audio files using `datasets.Audio` feature to handle on-the-fly decoding.
2. Resample all training audio to 16kHz to avoid sample rate mismatch.
3. Normalize transcripts to remove characters not present in Whisper's vocabulary.

### Fine-tuning Whisper with Unsloth
1. Load `whisper-large-v3` using `FastLanguageModel.from_pretrained` with `load_in_4bit=True`.
2. Apply LoRA weights to cross-attention and self-attention layers of the encoder and decoder.
3. Train using `Seq2SeqTrainer` or standard `Trainer` if audio is flattened to tokens.

## Non-Obvious Insights
- Whisper fine-tuning in Unsloth uses the same PEFT/LoRA pipeline as LLMs, which is why it can handle large models on consumer GPUs.
- Capturing vocal nuances like accents is significantly more effective through fine-tuning than zero-shot, as the model learns to map specific acoustic features to text tokens.
- Proper audio normalization (16kHz resampling) is the single most important preprocessing step; Whisper's architecture is hard-coded for this sample rate.

## Evidence
- "Unsloth supports any transformers compatible TTS/STT model... 1.5x faster with 50% less memory." [Source](https://docs.unsloth.ai/basics/text-to-speech-tts-fine-tuning)
- "Fine-tuning delivers far more accurate and realistic voice replication than zero-shot." [Source](https://docs.unsloth.ai/basics/text-to-speech-tts-fine-tuning)

## Scripts
- `scripts/unsloth-stt_tool.py`: Script for resampling and preprocessing audio datasets for Whisper.
- `scripts/unsloth-stt_tool.js`: Utility for cleaning transcription strings.

## Dependencies
- unsloth
- datasets
- librosa
- transformers

## References
- [[references/README.md]]