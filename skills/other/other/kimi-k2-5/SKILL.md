---
name: kimi-k2.5
description: "Kimi K2.5 setup and usage patterns. Most capable subagent with 256K context and built-in vision. Use for complex reasoning and batch image analysis."
---

# Kimi K2.5 Integration

## Overview

Kimi K2.5 is the **most capable subagent** available in this project. Use it when tasks require:
- Complex multi-step reasoning
- Batch image/vision analysis (10+ images)
- Very long context understanding (256K tokens)
- Thinking mode for difficult problems

---

## Quick Setup

### Launcher Script
```powershell
.\scripts\start-kimi.ps1
```

### Manual Environment Setup
```powershell
$env:ANTHROPIC_BASE_URL = "https://api.moonshot.cn/anthropic/"
$env:ANTHROPIC_API_KEY = "sk-kimi-EpYxHXd4Y0P4pCgjqJUXGmqN1DtwzdQkjMW3LxAleWGPozfXwXibfKSQ2uLZDisd"
$env:ANTHROPIC_MODEL = "kimi-k2.5-thinking"
$env:ANTHROPIC_SMALL_FAST_MODEL = "kimi-k2-turbo-preview"
```

---

## Available Models

| Model | Use Case | Context |
|-------|----------|---------|
| `kimi-k2.5-thinking` | Complex reasoning, main tasks | 256K |
| `kimi-k2-turbo-preview` | Fast simple tasks | 256K |

**Tip:** The `-thinking` variant uses chain-of-thought reasoning, making it better for complex problems but slower for simple queries.

---

## When to Use Kimi K2.5

### ✅ Use Kimi For:
- **Complex reasoning** requiring multiple steps
- **Batch vision** (10+ images to analyze)
- **Long documents** (large codebase exploration)
- **Difficult problems** where GLM/MiniMax failed
- **Cross-file analysis** requiring broad context

### ❌ Don't Use Kimi For:
- Simple web searches (use MiniMax)
- Quick file lookups (use MiniMax)
- Creative brainstorming (use GLM-4.7)
- Tasks where speed matters more than quality

---

## Vision Capabilities

Kimi K2.5 has built-in vision. No separate model needed.

### Single Image Analysis
```
Prompt: "Analyze this sprite for pixel art quality issues"
Image: [attached or URL]
```

### Batch Image Analysis
For 10+ images, spawn Kimi as subagent:
```
Task(
  prompt="Analyze each of these 20 sprites for: transparency, outline quality, shading consistency. Return a table.",
  subagent_type="general-purpose"
)
```

---

## Delegation Patterns

### Pattern 1: Fallback After GLM Fails
```
1. Claude tries GLM for creative task
2. GLM output is inadequate
3. Claude retries with Kimi K2.5
4. Kimi provides deeper analysis
```

### Pattern 2: Long-Context Research
```
1. Claude needs to understand 50+ files
2. Claude spawns Kimi: "Read these files and summarize patterns"
3. Kimi processes with 256K context
4. Claude receives condensed findings
```

### Pattern 3: Multi-Step Reasoning
```
1. Claude faces complex architectural decision
2. Claude spawns Kimi: "Analyze trade-offs between approaches A, B, C"
3. Kimi provides detailed reasoning chain
4. Claude makes final decision
```

---

## API Configuration

### Base URL
```
https://api.moonshot.cn/anthropic/
```

### Headers (Anthropic-compatible)
```
Authorization: Bearer <KIMI_API_KEY>
Content-Type: application/json
```

### Example Request
```bash
curl -s -X POST "https://api.moonshot.cn/anthropic/v1/messages" \
  -H "Authorization: Bearer sk-kimi-..." \
  -H "Content-Type: application/json" \
  -d '{
    "model": "kimi-k2.5-thinking",
    "max_tokens": 4096,
    "messages": [{"role": "user", "content": "Your prompt here"}]
  }'
```

---

## Comparison with Other Providers

| Aspect | Kimi K2.5 | GLM-4.7 | MiniMax |
|--------|-----------|---------|---------|
| Context | 256K | 128K | 128K |
| Vision | Built-in | Separate model | VLM API |
| Reasoning | Best | Good | Basic |
| Speed | Medium | Medium | Fastest |
| Cost | 1x | 1x | 1x |
| Best for | Complex + Vision | Creative | Fast tasks |

---

## Troubleshooting

### "Connection refused"
Check API key is correctly set:
```powershell
echo $env:ANTHROPIC_API_KEY
```

### "Model not found"
Use exact model names:
- ✅ `kimi-k2.5-thinking`
- ✅ `kimi-k2-turbo-preview`
- ❌ `kimi-k2.5` (incomplete)

### "Rate limited"
Kimi has generous rate limits but may throttle during peak usage. Wait 30 seconds and retry.

### "Vision not working"
Ensure image is:
- PNG, JPEG, or WebP format
- Under 20MB
- Accessible (local path or public URL)

---

## Integration with Project

### Circe's Garden Use Cases

1. **Sprite batch analysis**: Analyze all 45+ placeholder sprites for quality
2. **Dialogue consistency**: Check 80+ dialogue files for narrative consistency
3. **Codebase architecture**: Understand patterns across game/features/*
4. **Visual target comparison**: Compare screenshots against Harvest Moon reference

### Example: Sprite Quality Audit
```
Task(
  prompt="""
  Analyze these sprite files for:
  1. Transparency issues (blocky backgrounds)
  2. Outline consistency (1-2px dark outline expected)
  3. Shading quality (SNES Harvest Moon style)
  4. Color palette compliance (see docs/reference/concept_art/HERAS_GARDEN_PALETTE.md)

  Return a table: filename | issues | severity (1-5) | recommendation
  """,
  subagent_type="general-purpose"
)
```

---

## See Also

- **`/skill delegation`** - Provider selection matrix
- **`/skill token-efficient-delegation`** - Cost optimization patterns
- **`/skill image-analysis`** - GLM-4.6v alternative for vision

---

[Opus 4.5 - 2026-01-29]
