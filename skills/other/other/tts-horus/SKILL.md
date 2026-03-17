---
name: tts-horus
description: >
  Build and operate the Horus TTS pipeline from cleared audiobooks.
  Includes dataset prep, WhisperX alignment, XTTS training, voice coloring,
  and persona inference helpers.
allowed-tools: Bash, Read
triggers:
  - horus tts
  - build horus voice
  - voice coloring
  - tts pipeline
metadata:
  short-description: Horus TTS dataset + training + inference pipeline

provides:
  - tts-horus
composes: [, task-monitor]
---

# Horus TTS Pipeline

This skill standardizes the end-to-end Horus voice workflow using `uvx`-style
invocations so dependencies are isolated per command. It assumes recordings
live under `persona/data/audiobooks/` with per-book `clean/` folders.

## Commands

### `dataset`
Builds the Horus dataset from Horus Rising using faster-whisper segmentation.

```bash
# Step 1: Transcribe and segment
python run/tts/ingest_audiobook.py \
  --audio persona/data/audiobooks/Horus_Rising_The_Horus_Heresy_Book_1-LC_64_22050_stereo/audio.m4b \
  --book-name Horus_Rising \
  --output-dir datasets/horus_voice \
  --max-hours 0

# Step 2: Extract clips (CPU-bound, uses ffmpeg)
python run/tts/extract_clips.py \
  --segments datasets/horus_voice/segments_merged.jsonl \
  --audio persona/data/audiobooks/Horus_Rising_The_Horus_Heresy_Book_1-LC_64_22050_stereo/audio.m4b \
  --output-dir datasets/horus_voice/clips \
  --manifest datasets/horus_voice/full_manifest.jsonl \
  --min-sec 1.5 --max-sec 15.0 --sample-rate 24000 --max-hours 0
```

### `align`
Runs WhisperX alignment with lexicon overrides.

```bash
python run/tts/align_transcripts.py \
  --manifest datasets/horus_voice/train_manifest.jsonl \
  --output datasets/horus_voice/train_aligned.jsonl \
  --dataset-root datasets/horus_voice \
  --lexicon persona/docs/lexicon_overrides.json \
  --strategy whisperx --device cuda
```

### `train`
Fine-tunes XTTS-v2 using GPTTrainer (local A5000 by default).

```bash
python run/tts/train_xtts_coqui.py --config configs/tts/horus_xtts.yaml
```

**Important**: Uses `train_xtts_coqui.py` with GPTTrainer (not generic Trainer).
Must use `mixed_precision=False` to avoid NaN losses.

### `say`
CLI synthesis (writes `.artifacts/tts/output.wav` by default).

```bash
python run/tts/say.py "Lupercal speaks."
```

### `server`
FastAPI server for low-latency synthesis.

```bash
python run/tts/server.py
```

### `color`
Voice coloring helper (to be implemented in Task 5).

```bash
python run/tts/color_voice.py --base horus --color warm --alpha 0.4
```

## Notes

- WhisperX is installed in the project `.venv`; for standalone runs, use `uvx whisperx` if needed.
- Golden samples live in `tests/fixtures/tts/golden/` (Git LFS).
- Orchestrate-ready task plan lives at `persona/docs/tasks/0N_voice_coloring.md`.

## Gotchas

| Issue | Solution |
|-------|----------|
| NaN losses from step 0 | Use `mixed_precision=False`, `precision="float32"` |
| Model size mismatch (1026 vs 8194) | Use GPTTrainer with GPTArgs, not XttsConfig |
| Missing dvae.pth | Download from HuggingFace: `wget https://huggingface.co/coqui/XTTS-v2/resolve/main/dvae.pth` |
| Clips too short (rejected) | Merge adjacent segments: MIN_TARGET=2.0s, MAX_GAP=0.5s |
| Clip extraction slow | Normal - uses ffmpeg (CPU-bound), GPU only for training |
| Learning rate | Use 5e-6 (official recipe), NOT default 2e-4 |
| Batch size | batch_size * grad_accumulation >= 252 for efficient training |
| LR milestones never reached | Script now auto-calculates based on dataset size |

## Learning Rate Schedule

The training script uses professional ML best practices:

```
LR Schedule: CosineAnnealingWarmRestarts (recommended for XTTS)
- T_0: ~20% of total steps (first annealing cycle)
- T_mult: 2 (each subsequent cycle doubles in length)
- eta_min: 1e-7 (minimum LR floor)
- Gradient clipping: 1.0
- Optimizer: AdamW with weight decay 1e-2
```

**Why CosineAnnealingWarmRestarts over MultiStepLR:**
- Smoother LR decay (better for fine-tuning)
- Periodic restarts help escape local minima
- Recommended by Coqui community for XTTS

**Double descent** is less relevant for fine-tuning because:
1. Model already trained - we're adapting, not learning from scratch
2. Single speaker - we want specialization to Horus's voice
3. Risk is memorization, mitigated by diverse training data (~18k clips)

Sources:
- [AllTalk TTS Finetuning Guide](https://github.com/erew123/alltalk_tts/wiki/XTTS-Model-Finetuning-Guide-(Advanced-Version))
- [Coqui TTS Discussion #3773](https://github.com/coqui-ai/TTS/discussions/3773)

## Automated Pipeline

The TTS pipeline can run fully automated from extraction to training:

```bash
# Start extraction, then auto-train when complete
./run/tts/auto_train_after_extraction.sh [extraction_pid]

# Or run the full pipeline from scratch
python run/tts/horus_pipeline.py --skip-align
```

The auto script will:
1. Monitor extraction progress (logs every 60s)
2. Create train/val manifests (98%/2% split)
3. Build Coqui metadata.csv
4. Start XTTS training (200 epochs)

Logs: `logs/tts/pipeline_*.log`

## Current Status (2026-01-23)

- **Audiobook**: Horus Rising (~12h)
- **Extraction**: In progress (~9,400 / ~21,975 clips)
- **Auto-monitor**: Running (PID in `logs/tts/auto_pipeline.log`)
- **Config**: `configs/tts/horus_xtts.yaml` (200 epochs, 5e-6 LR)
- **Training**: Will auto-start after extraction
