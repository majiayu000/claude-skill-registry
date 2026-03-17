---
name: multi-model-writer
description: "Unified writing system with intelligent model routing. Default: Claude. Options: GLM-4.7 (cheapest), GPT-4o/mini, Gemini, Grok. Includes browser automation for web interfaces. Cost-aware routing based on task complexity."
---

# Multi-Model Writer

Intelligent model routing for all writing tasks. **Default is Claude** (you), with fallback to other models when requested or when specific capabilities are needed.

---

## Model Arsenal

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        MULTI-MODEL WRITING SYSTEM                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌────────────────┐                                                     │
│  │  DEFAULT       │                                                     │
│  │  Claude        │ ← All writing goes here first                       │
│  │  (You)         │   Best quality, medical accuracy                    │
│  └───────┬────────┘                                                     │
│          │                                                               │
│          ▼                                                               │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    ALTERNATIVE MODELS                            │   │
│  ├──────────────┬──────────────┬──────────────┬──────────────────┤   │
│  │  GLM-4.7     │  GPT-4o      │  Gemini      │  Grok            │   │
│  │  $0.10/M     │  $10/M       │  FREE tier   │  $15/M           │   │
│  │  Bulk drafts │  Quality     │  1500/day    │  Real-time       │   │
│  │  Comparison  │  Editorial   │  Research    │  X/Twitter       │   │
│  └──────────────┴──────────────┴──────────────┴──────────────────┘   │
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │                    BROWSER AUTOMATION                            │   │
│  │  ChatGPT Web │ Gemini Web │ Uses your Pro subscriptions         │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## When to Use Which Model

### Claude (DEFAULT) - Use for Everything
- All medical/cardiology content
- YouTube scripts (Hinglish)
- Twitter/X content (English)
- Editorials and newsletters
- Anything requiring accuracy

### GLM-4.7 (Z.AI) - Bulk & Comparison
**Cost:** $0.10/M tokens (100x cheaper than Claude)
**Use when:**
- Generating multiple draft variations
- A/B testing content angles
- Bulk social media post generation
- First drafts for quick iteration
- Cost is a primary concern

```
/write-glm "Generate 5 different hooks for a video about statin myths"
```

### GPT-4o / GPT-4o-mini - Quality Alternative
**Cost:** $0.60/M (mini) or $10/M (4o)
**Use when:**
- You want to compare Claude vs GPT style
- Specific OpenAI capabilities needed
- User explicitly requests "GPT style"

```
/write-gpt "Write an editorial on SGLT2 inhibitors" --model=4o-mini
```

### Gemini - Research & Free Tier
**Cost:** FREE (1500 requests/day via AI Studio)
**Use when:**
- Web research integration
- Fact-checking
- You want Google's knowledge
- Budget is zero

```
/write-gemini "Summarize recent GLP-1 agonist research"
```

### Grok (xAI) - Real-time & X/Twitter
**Cost:** $15/M tokens (expensive)
**Use when:**
- Real-time X/Twitter trends
- Content specifically for X platform
- You want Grok's "unfiltered" style

```
/write-grok "What's trending in cardiology on X right now?"
```

---

## API Configuration

All APIs are configured in `.env`:

```bash
# Check which APIs are configured
cat .env | grep -E "API_KEY|_KEY"
```

### Required Environment Variables

| Variable | Model | Get From |
|----------|-------|----------|
| `ANTHROPIC_API_KEY` | Claude | console.anthropic.com |
| `ZAI_API_KEY` | GLM-4.7 | z.ai |
| `OPENAI_API_KEY` | GPT-4o | platform.openai.com |
| `GOOGLE_API_KEY` | Gemini | aistudio.google.com (FREE) |
| `XAI_API_KEY` | Grok | console.x.ai |

---

## Python Integration

### Direct API Calls

```python
from multi_model_writer import ModelRouter

router = ModelRouter()

# Default (Claude via current session)
response = router.write("Your prompt here")

# Specific model
response = router.write("Your prompt", model="glm-4.7")
response = router.write("Your prompt", model="gpt-4o-mini")
response = router.write("Your prompt", model="gemini")
response = router.write("Your prompt", model="grok")

# Cost-optimized (auto-selects cheapest)
response = router.write("Your prompt", optimize="cost")

# Quality-optimized (auto-selects best for task)
response = router.write("Your prompt", optimize="quality")
```

### Batch Comparison

```python
# Generate same content across multiple models for comparison
results = router.compare(
    prompt="Write a tweet about the EMPEROR-Preserved trial",
    models=["claude", "glm-4.7", "gpt-4o-mini"]
)

for model, output in results.items():
    print(f"\n=== {model} ===")
    print(output)
```

---

## Browser Automation (Web Interfaces)

For using your ChatGPT Plus and Gemini Advanced subscriptions:

### Setup

```bash
# Ensure Playwright is installed
pip install playwright
playwright install chromium
```

### Usage

See `browser-automation` skill for detailed instructions.

```
/browser-chat "Your prompt" --target=chatgpt
/browser-chat "Your prompt" --target=gemini
```

---

## Cost Tracking

### Per-Task Estimates

| Task | Tokens | GLM-4.7 | GPT-4o-mini | GPT-4o | Claude |
|------|--------|---------|-------------|--------|--------|
| Tweet | 200 | $0.00004 | $0.00012 | $0.002 | $0.003 |
| Thread (10 tweets) | 2,000 | $0.0004 | $0.0012 | $0.02 | $0.03 |
| Article (1500 words) | 2,500 | $0.0005 | $0.0015 | $0.025 | $0.0375 |
| YouTube Script | 8,000 | $0.0016 | $0.0048 | $0.08 | $0.12 |
| Newsletter | 5,000 | $0.001 | $0.003 | $0.05 | $0.075 |

### Monthly Budget Planning

With $5/month on each:

| Model | Monthly Output |
|-------|----------------|
| GLM-4.7 | ~20,000 articles |
| GPT-4o-mini | ~3,300 articles |
| GPT-4o | ~200 articles |
| Grok | ~130 articles |
| Gemini | UNLIMITED (free tier) |

---

## Slash Commands

| Command | Action |
|---------|--------|
| `/write [prompt]` | Write with Claude (default) |
| `/write-glm [prompt]` | Write with GLM-4.7 |
| `/write-gpt [prompt]` | Write with GPT-4o-mini |
| `/write-gemini [prompt]` | Write with Gemini |
| `/write-grok [prompt]` | Write with Grok |
| `/compare [prompt]` | Compare outputs across models |
| `/browser-chat [prompt]` | Use browser automation |

---

## Workflow Examples

### 1. Draft Iteration (Cost-Optimized)

```
Step 1: Generate 5 hook variations with GLM-4.7 ($0.001)
Step 2: Pick best 2, refine with Claude (default)
Step 3: Final polish with Claude
```

### 2. Quality Comparison

```
Step 1: Write same content with Claude, GPT-4o, GLM-4.7
Step 2: Compare outputs side-by-side
Step 3: Learn which model suits which content type
```

### 3. Bulk Social Media

```
Step 1: Generate 50 tweet variations with GLM-4.7 ($0.001)
Step 2: Filter top 10 manually
Step 3: Polish top 3 with Claude
Step 4: Schedule via your social tools
```

---

## Model Characteristics

### Writing Style Comparison

| Model | Style | Best For |
|-------|-------|----------|
| **Claude** | Precise, nuanced, follows instructions exactly | Medical content, accuracy-critical |
| **GLM-4.7** | Efficient, code-oriented, concise | Bulk generation, structured content |
| **GPT-4o** | Conversational, creative, verbose | Editorials, storytelling |
| **Gemini** | Research-integrated, factual | Summaries, fact-based content |
| **Grok** | Direct, irreverent, real-time aware | Twitter/X content, trending topics |

---

## Integration with Existing Skills

This skill works WITH your existing cardiology skills:

```
1. Use `youtube-script-master` → Routes to Claude by default
2. Use `cardiology-editorial` → Routes to Claude by default
3. Add `--model=glm-4.7` → Overrides to cheaper model
4. Use `/compare` → See all models side-by-side
```

---

*This skill gives you a full arsenal of AI models while keeping Claude as your primary, trusted writing partner.*
