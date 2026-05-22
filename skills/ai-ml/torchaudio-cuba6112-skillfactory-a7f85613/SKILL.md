---
name: torchaudio
description: Audio signal processing library for PyTorch. Covers feature extraction (spectrograms, mel-scale), waveform manipulation, and GPU-accelerated data augmentation techniques. (torchaudio, melscale, spectrogram, pitchshift, specaugment, waveform, resample)
---

## Overview

TorchAudio provides signal processing tools for PyTorch, enabling users to treat audio processing as part of the neural network graph. This allow transforms to be run on GPUs and handled via `nn.Sequential` pipelines.

## When to Use

Use TorchAudio for converting raw audio waveforms into features like Mel Spectrograms, performing data augmentation (SpecAugment), or when high-performance resampling is required.

## Decision Tree

1. Do you need to transform many audio files quickly?
   - MOVE: The transform module to GPU using `.to('cuda')`.
2. Are you training an Automatic Speech Recognition (ASR) model?
   - USE: SpecAugment (TimeMasking, FrequencyMasking) on the spectrogram.
3. Do you need to align text to audio?
   - USE: The `forced_align` functional API with a Wav2Vec2 model.

## Workflows

1. **Audio Feature Extraction Pipeline**
   1. Load the waveform as a PyTorch tensor.
   2. Apply `Resample` to match the target frequency (e.g., 16000Hz).
   3. Use `Spectrogram` to convert to a power/amplitude scale.
   4. Convert the spectrogram to mel-scale using `MelScale`.
   5. Optionally apply `AmplitudeToDB` to get decibel values.

2. **GPU-Accelerated Data Augmentation**
   1. Define an augmentation pipeline using `nn.Sequential` (e.g., `TimeStretch`, `FrequencyMasking`).
   2. Move the pipeline to the GPU (`.to('cuda')`).
   3. Process batches of spectrograms directly on the device to avoid CPU bottlenecks.

3. **Pitch and Speed Perturbation**
   1. Use `torchaudio.transforms.PitchShift` for pitch changes without affecting duration.
   2. Apply `torchaudio.transforms.Speed` for speed changes (which also affects pitch).
   3. Iterate through a range of factors to create a diverse augmented dataset for speech recognition.

## Non-Obvious Insights

- **GPU Efficiency**: Moving audio transformations like `MelScale` to the GPU allows the entire feature extraction process to happen in parallel with model training, eliminating CPU data-loading bottlenecks.
- **ASR Robustness**: SpecAugment techniques (Time/Frequency Masking) should be applied to the **spectrogram**, not the raw waveform, as they are designed to simulate missing acoustic information in the frequency domain.
- **Library Evolution**: Starting with version 2.8, TorchAudio has entered maintenance, with some low-level decoding capabilities consolidated into the `TorchCodec` project.

## Evidence

- "Transforms are implemented using torch.nn.Module... common ways to build a processing pipeline are to chain Modules together using torch.nn.Sequential." (https://pytorch.org/audio/stable/transforms.html)
- "PitchShift: Shift the pitch of a waveform by n_steps steps." (https://pytorch.org/audio/stable/transforms.html)

## Scripts

- `scripts/torchaudio_tool.py`: Utility for building an audio feature pipeline.
- `scripts/torchaudio_tool.js`: Node.js wrapper for processing audio files via TorchAudio.

## Dependencies

- torchaudio
- torch

## References

- [TorchAudio Reference](references/README.md)