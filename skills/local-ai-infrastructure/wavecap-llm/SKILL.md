---
name: wavecap-llm
description: Configure WaveCap LLM-based transcription correction. Use when the user wants to enable/disable LLM correction, change models, tune prompts, or optimize correction quality on Apple Silicon.
---

# WaveCap LLM Correction Tuning Skill

Use this skill to configure the optional LLM-based post-processing that corrects Whisper transcription errors using local models on Apple Silicon.

## Requirements

- Apple Silicon Mac (M1/M2/M3/M4)
- mlx-lm package installed: `pip install mlx-lm`
- Sufficient RAM for model (1B=2GB, 3B=6GB, 8B=16GB)

## Configuration Location

LLM settings are in the `llm:` section:
- **User config:** `/Users/thw/Projects/WaveCap/state/config.yaml`

## Basic Configuration

### Enable/Disable LLM Correction

```yaml
llm:
  enabled: true  # false to disable
```

### Model Selection

```yaml
llm:
  model: llama-3.2-3b  # Model name or HuggingFace path
```

| Model | Size | RAM | Speed | Quality | Use Case |
|-------|------|-----|-------|---------|----------|
| llama-3.2-1b | 1B | ~2GB | Fastest | Good | Low RAM, quick fixes |
| qwen-2.5-1.5b | 1.5B | ~3GB | Very fast | Good | Balanced small model |
| **llama-3.2-3b** | 3B | ~6GB | Fast | Very good | **Recommended** |
| qwen-2.5-3b | 3B | ~6GB | Fast | Very good | Alternative to Llama |
| llama-3.1-8b | 8B | ~16GB | Moderate | Excellent | High quality |
| llama-3.2-8b | 8B | ~16GB | Moderate | Excellent | Latest 8B |

### Generation Parameters

```yaml
llm:
  temperature: 0.1      # 0.0-1.0, lower = more deterministic
  maxTokens: 256        # Max output tokens
  minTextLength: 10     # Skip texts shorter than this
```

| Parameter | Default | Effect |
|-----------|---------|--------|
| temperature | 0.1 | Lower = consistent, higher = creative |
| maxTokens | 256 | Enough for single sentence corrections |
| minTextLength | 10 | Skip very short texts |

## Domain Terms

Add domain-specific vocabulary to preserve:

```yaml
llm:
  domainTerms:
    - SITREP
    - SAPOL
    - SES
    - CFS
    - Adelaide
    - Noarlunga
    - Para Hills
```

These terms are injected into the correction prompt to prevent the LLM from "fixing" correct jargon.

## View Current Settings

```bash
grep -A20 "^llm:" /Users/thw/Projects/WaveCap/state/config.yaml
```

## Check LLM Status

```bash
curl -s http://localhost:8000/api/health | jq
```

## Full Configuration Example

```yaml
llm:
  enabled: true
  model: llama-3.2-3b
  temperature: 0.1
  maxTokens: 256
  minTextLength: 10
  domainTerms:
    - SITREP
    - SAPOL
    - SES
    - CFS
    - MFS
    - Adelaide
    - Noarlunga
    - Aldinga
    - Para Hills
    - Gawler
    - Sturt
    - Metro
    - Roger
    - Wilco
    - Over
    - Out
```

## Tuning Scenarios

### Maximum Quality (8GB+ RAM)
```yaml
llm:
  enabled: true
  model: llama-3.1-8b
  temperature: 0.05
  maxTokens: 300
```

### Balanced (6GB RAM)
```yaml
llm:
  enabled: true
  model: llama-3.2-3b
  temperature: 0.1
  maxTokens: 256
```

### Low Memory (4GB RAM)
```yaml
llm:
  enabled: true
  model: llama-3.2-1b
  temperature: 0.1
  maxTokens: 200
```

### Disabled (Whisper only)
```yaml
llm:
  enabled: false
```

## Apply Changes

```bash
launchctl stop com.wavecap.server && sleep 2 && launchctl start com.wavecap.server
```

## Compare Before/After Correction

The LLM corrector stores both original and corrected text. Check improvements:

```bash
curl -s http://localhost:8000/api/transcriptions/export | \
  jq '[.[] | select(.llmCorrectedText != null and .llmCorrectedText != .text)] |
      .[:5] | .[] | {
        original: .text,
        corrected: .llmCorrectedText
      }'
```

## Monitor LLM Performance

### Check correction rate
```bash
curl -s http://localhost:8000/api/transcriptions/export | \
  jq '{
    total: length,
    with_llm_correction: [.[] | select(.llmCorrectedText != null)] | length,
    actually_changed: [.[] | select(.llmCorrectedText != null and .llmCorrectedText != .text)] | length
  }'
```

### Check for over-correction
Look for cases where LLM made unwanted changes:

```bash
curl -s http://localhost:8000/api/transcriptions/export | \
  jq '[.[] | select(.llmCorrectedText != null and .llmCorrectedText != .text)] |
      .[-10:] | .[] | {
        original: (.text | .[0:60]),
        corrected: (.llmCorrectedText | .[0:60])
      }'
```

## Troubleshooting

### Model Download Issues

Models are downloaded from HuggingFace on first use. Check downloads:

```bash
ls -la ~/.cache/huggingface/hub/ | grep mlx
```

### Memory Issues

If you see memory errors, try a smaller model:

```yaml
llm:
  model: llama-3.2-1b  # Smallest option
```

### Slow Corrections

1. Use a smaller model
2. Reduce maxTokens
3. Check Activity Monitor for GPU usage

### LLM Not Correcting

Check if enabled and model loaded:

```bash
curl -s http://localhost:8000/api/health | jq
tail -50 /Users/thw/Projects/WaveCap/state/logs/backend.log | grep -i llm
```

## Available Models (MLX Hub)

The following models are pre-configured:

| Alias | HuggingFace Repo |
|-------|------------------|
| llama-3.2-1b | mlx-community/Llama-3.2-1B-Instruct-4bit |
| llama-3.2-3b | mlx-community/Llama-3.2-3B-Instruct-4bit |
| llama-3.1-8b | mlx-community/Meta-Llama-3.1-8B-Instruct-4bit |
| llama-3.2-8b | mlx-community/Llama-3.2-8B-Instruct-4bit |
| qwen-2.5-1.5b | mlx-community/Qwen2.5-1.5B-Instruct-4bit |
| qwen-2.5-3b | mlx-community/Qwen2.5-3B-Instruct-4bit |

You can also use any MLX-compatible model path directly:

```yaml
llm:
  model: mlx-community/Mistral-7B-Instruct-v0.3-4bit
```

## Tips

- Start with `llama-3.2-3b` for best balance of speed and quality
- Keep temperature low (0.05-0.15) for consistent corrections
- Add all domain-specific terms to prevent unwanted "corrections"
- Monitor the correction diff to ensure quality
- LLM correction adds ~100-500ms latency per transcription
- Disable if running on Intel Mac or limited RAM
