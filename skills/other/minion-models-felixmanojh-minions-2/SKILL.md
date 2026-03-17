---
name: minion-models
description: >
  Manage Ollama models for minions. Pull new models, list available ones,
  switch presets, check disk usage. Use when setting up or changing models.
allowed-tools: Bash, Read, Write
---

# Minion Models

Manage Ollama models for your minion squad.

## Quick commands

### List installed models

```bash
ollama list
```

### Pull a model

```bash
ollama pull qwen2.5-coder:1.5b
```

### Check model info

```bash
ollama show qwen2.5-coder:1.5b
```

### Remove a model

```bash
ollama rm qwen2.5-coder:0.5b
```

## Presets

| Preset | Models | Download | RAM |
|--------|--------|----------|-----|
| nano | qwen2.5-coder:0.5b | ~350MB | ~1GB |
| small | qwen2.5-coder:1.5b | ~1GB | ~2GB |
| medium | qwen2.5-coder:7b | ~4.5GB | ~8GB |
| large | qwen2.5-coder:14b | ~9GB | ~16GB |

### Pull preset models

**nano:**
```bash
ollama pull qwen2.5-coder:0.5b
```

**small (recommended):**
```bash
ollama pull qwen2.5-coder:1.5b
```

**medium:**
```bash
ollama pull qwen2.5-coder:7b
```

**large:**
```bash
ollama pull qwen2.5-coder:14b
```

## Switch preset

Edit `llm_gc/config/models.yaml` and change the preset line:

```yaml
preset: small  # Change to: nano, small, medium, or large
```

Or use sed:
```bash
sed -i.bak 's/^preset:.*/preset: medium/' llm_gc/config/models.yaml
```

## Check disk usage

```bash
# Total Ollama storage
du -sh ~/.ollama/models

# Per-model breakdown
ls -lh ~/.ollama/models/blobs/ | head -20
```

## Recommended models

| Task | Model | Why |
|------|-------|-----|
| Quick patches | qwen2.5-coder:1.5b | Fast, good enough |
| Quality patches | qwen2.5-coder:7b | Better reasoning |
| Code review | qwen2.5-coder:7b+ | Needs context |
| Simple questions | qwen2.5-coder:0.5b | Speed matters |

## Alternative models

```bash
# DeepSeek (alternative to Qwen)
ollama pull deepseek-coder:1.3b
ollama pull deepseek-coder:6.7b

# CodeLlama (Meta)
ollama pull codellama:7b

# StarCoder
ollama pull starcoder2:3b
```

## Troubleshooting

**Model not found:**
```bash
ollama pull <model-name>
```

**Slow responses:**
- Try smaller model
- Check `htop` for RAM pressure
- Reduce `--workers` in swarm

**Out of disk space:**
```bash
# Remove unused models
ollama rm <model-name>

# Check what's installed
ollama list
```

**Model quality issues:**
- Upgrade preset: nano → small → medium
- Add more context with `--read`
- Simplify the task
