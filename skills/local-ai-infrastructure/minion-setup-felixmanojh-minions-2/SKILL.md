---
name: minion-setup
description: >
  Verify Ollama is running and models are configured.
  Run to diagnose minion issues.
allowed-tools: Bash
---

# Minion Setup

Verify environment and diagnose issues.

## Quick Check

```bash
source .venv/bin/activate && python scripts/minions.py setup
```

## Output

```
Checking Ollama...
✓ Ollama running with 4 models
  - qwen2.5-coder:7b
  - deepseek-coder:1.3b

Checking config...
✓ Config loaded: 3 roles
  - implementer: qwen2.5-coder:7b (ctx: 32768)
  - reviewer: deepseek-coder:1.3b (ctx: 16384)

✓ Setup OK
```

## If Setup Fails

### Ollama not running
```bash
ollama serve &
```

### No models
```bash
ollama pull qwen2.5-coder:7b
```

### Missing venv
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Model Presets

| Preset | Models | Size |
|--------|--------|------|
| lite | qwen2.5-coder:7b | ~5GB |
| medium | qwen2.5-coder:7b + deepseek-coder:1.3b | ~6GB |
| large | qwen2.5-coder:14b + deepseek-coder:33b | ~35GB |

Change preset in `llm_gc/config/models.yaml`:
```yaml
preset: medium
```
