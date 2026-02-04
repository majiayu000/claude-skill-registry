---
name: piper-tts-training
description: Train custom TTS voices for Piper (ONNX format) using fine-tuning or from-scratch approaches. Use when creating new synthetic voices, fine-tuning existing Piper checkpoints, preparing audio datasets for TTS training, or deploying voice models to devices like Raspberry Pi or Home Assistant. Covers dataset preparation, Whisper-based validation, training configuration, and ONNX export.
# model: inherit
# allowed-tools: Read,Write,Bash,Grep
---

# Piper TTS Voice Training

Train custom text-to-speech voices compatible with Piper's lightweight ONNX runtime.

## Overview

Piper produces fast, offline TTS suitable for embedded devices. Training involves:
1. Corpus preparation (text covering phonetic range)
2. Audio generation or recording
3. Quality validation via Whisper transcription
4. Fine-tuning from existing checkpoint (recommended) or training from scratch
5. ONNX export for deployment

**Fine-tuning vs from-scratch:**
- Fine-tuning: ~1,300 phrases + 1,000 epochs (days on modest GPU)
- From scratch: ~13,000+ phrases + 2,000+ epochs (weeks/months)

## Workflow

### 1. Corpus Preparation

Gather 1,300-1,500+ phrases covering broad phonetic range:
- Use piper-recording-studio corpus as base
- Add domain-specific phrases for your use case
- Include varied sentence structures and lengths

**Critical for non-US English:** Ensure corpus uses correct regional spelling. See [Localisation](#localisation-for-australian-new-zealand-and-uk-english).

### 2. Audio Generation

Generate or record training audio at 22050Hz mono WAV.

**If using voice cloning (e.g., Chatterbox TTS):**
- Generate at source sample rate (often 24kHz)
- Convert to 22050Hz: `sox -v 0.95 input.wav -r 22050 -t wav output.wav`
- The `-v 0.95` prevents clipping during resampling

**Recording requirements:**
- Consistent microphone position and room acoustics
- Minimal background noise
- Natural speaking pace (not reading voice)

### 3. Quality Validation with Whisper

Automate quality checks rather than manual listening:

```python
import whisper
from piper_phonemize import phonemize_text

model = whisper.load_model("base")

def validate_sample(audio_path, expected_text):
    result = model.transcribe(audio_path)
    transcribed = result["text"].strip()

    # Compare phonemically to handle spelling/punctuation differences
    expected_phonemes = phonemize_text(expected_text, "en-gb")
    transcribed_phonemes = phonemize_text(transcribed, "en-gb")

    return expected_phonemes == transcribed_phonemes
```

Retry failed samples up to 3 times. Target 95%+ dataset coverage.

### 4. Dataset Format (LJSpeech)

Structure your dataset:
```
dataset/
├── metadata.csv
└── wavs/
    ├── sample_0001.wav
    ├── sample_0002.wav
    └── ...
```

**metadata.csv format:** `{id}|{text}` (pipe-separated, no headers)
```
sample_0001|The quick brown fox jumps over the lazy dog.
sample_0002|Pack my box with five dozen liquor jugs.
```

### 5. Preprocessing

Convert to PyTorch tensors:
```bash
python3 -m piper_train.preprocess \
    --language en-gb \
    --input-dir dataset/ \
    --output-dir piper_training_dir/ \
    --dataset-format ljspeech
```

Use `en-gb` for Australian/NZ/UK voices (espeak-ng phoneme set).

### 6. Training

**Fine-tuning (recommended):**
```bash
python3 -m piper_train \
    --dataset-dir piper_training_dir/ \
    --accelerator gpu \
    --devices 1 \
    --batch-size 12 \
    --max_epochs 3000 \
    --resume_from_checkpoint ljspeech-2000.ckpt \
    --checkpoint-epochs 100 \
    --quality high \
    --precision 32
```

**Key parameters:**
- `--batch-size`: Reduce if VRAM limited (12 works on 8GB)
- `--resume_from_checkpoint`: Start from LJSpeech high-quality checkpoint
- `--precision 32`: More stable than mixed precision
- `--validation-split 0.0 --num-test-examples 0`: Skip validation for small datasets

Monitor with TensorBoard: watch `loss_disc_all` for convergence.

### 7. ONNX Export

```bash
python3 -m piper_train.export_onnx checkpoint.ckpt output.onnx.unoptimized
onnxsim output.onnx.unoptimized output.onnx
```

Create metadata file `output.onnx.json` from training `config.json`.

## Localisation for Australian, New Zealand and UK English

Piper uses espeak-ng for phonemisation. American pronunciations in training data cause accent drift.

**Corpus preparation:**
- Run `scripts/convert_spelling.py` on corpus text before training
- Use `en-gb` or `en-au` espeak-ng voice for phonemisation
- Review generated phonemes for Americanisms

**Common spelling conversions:**
| American | Australian/UK |
|----------|---------------|
| -ize | -ise |
| -or | -our |
| -er | -re |
| -og | -ogue |
| -ense | -ence |

**Phoneme considerations:**
- /r/ linking and intrusion patterns differ
- Vowel sounds in words like "dance", "bath", "castle"
- Final -ile pronunciation (hostile, missile)

For complete word lists and phonetic details, see [references/localisation.md](references/localisation.md).

**Validation:** Use Whisper with `language="en"` and verify transcriptions match expected regional forms.

## Dependencies

Pin versions to avoid API breakage:
```
pytorch-lightning==1.9.3
torch<2.6.0
piper-phonemize
onnxruntime-gpu
onnxsim
```

Docker containerisation recommended for reproducibility.

## Hardware Requirements

**Minimum (fine-tuning):**
- 8GB VRAM GPU (Pascal or newer)
- 8GB system RAM
- ~5 days for 1,000 epochs on Tesla P4

**From scratch:** Multiply time by ~200x.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| CUDA OOM | Reduce batch-size (try 8 or 4) |
| Checkpoint won't load | Check pytorch-lightning version matches checkpoint |
| Garbled output | Insufficient training epochs or dataset too small |
| Wrong accent | Check espeak-ng language code and corpus spelling |
