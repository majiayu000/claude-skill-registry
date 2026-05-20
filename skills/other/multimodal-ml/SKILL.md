---
name: multimodal-ml
description: Vision-language model patterns including CLIP, LLaVA, cross-modal alignment, and embedding fusion. Use when building or integrating multimodal ML systems.
---

# Multimodal ML Patterns

## Fusion Strategy Selection

| Strategy | Architecture | Pros | Cons | Use When |
|----------|-------------|------|------|----------|
| **Late Fusion** | Separate encoders, merge at output | Simple, modular, can swap encoders | Limited cross-modal reasoning | Classification, retrieval, CLIP-style |
| **Early Fusion** | Concatenate raw tokens, single model | Deep cross-modal interaction | Expensive, needs lots of data | LLMs with image tokens (LLaVA, GPT-4V) |
| **Cross-Attention** | Separate encoders + cross-attn layers | Good balance of depth and modularity | More params, harder to train | Flamingo, image captioning, VQA |
| **Q-Former** | Learnable queries cross-attend to visual features | Fixed # of visual tokens, efficient | Requires pretraining Q-Former | BLIP-2, InstructBLIP |
| **Bottleneck/Perceiver** | Learnable queries attend to both modalities | Fixed compute regardless of input size | May lose fine-grained detail | Long sequences, many modalities |

Default recommendation: Late fusion (contrastive) for retrieval/matching. Early fusion (projector + LLM) for generation tasks.

## API-First Vision-Language Models

### Model Selection

| Model | Strength | Best For |
|-------|----------|----------|
| Claude (Anthropic) | Best document/chart understanding, long context | Document analysis, structured extraction, multi-image reasoning |
| GPT-4V/4o (OpenAI) | Strong general vision, function calling | General VQA, tool use with images |
| Gemini 1.5 Pro | Longest context (1M tokens), video support | Video understanding, many-image tasks |

### SDK Examples

```python
# Anthropic -- image analysis
import anthropic, base64

client = anthropic.Anthropic()
with open("chart.png", "rb") as f:
    image_data = base64.standard_b64encode(f.read()).decode()

response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": [
            {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": image_data}},
            {"type": "text", "text": "Extract all data points from this chart as JSON."},
        ],
    }],
)
```

```python
# OpenAI -- image analysis
from openai import OpenAI

client = OpenAI()
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{
        "role": "user",
        "content": [
            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_data}"}},
            {"type": "text", "text": "Extract all data points from this chart as JSON."},
        ],
    }],
)
```

### Open-Source Vision-Language Models

| Model | Base LLM | Key Feature |
|-------|----------|-------------|
| LLaVA-NeXT / OneVision | Qwen2, LLaMA | AnyRes (dynamic resolution), strong general VQA |
| InternVL2 | InternLM2 | Best open-source on many benchmarks, scales to 76B |
| Qwen-VL / Qwen2-VL | Qwen2 | Strong multilingual vision, native video support |
| PaliGemma | Gemma | Compact, good for fine-tuning specific tasks |

## CLIP-Style Contrastive Training

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class CLIPModel(nn.Module):
    def __init__(self, vision_encoder, text_encoder, embed_dim=512):
        super().__init__()
        self.vision_encoder = vision_encoder
        self.text_encoder = text_encoder
        self.vision_proj = nn.Linear(vision_encoder.output_dim, embed_dim)
        self.text_proj = nn.Linear(text_encoder.output_dim, embed_dim)
        self.logit_scale = nn.Parameter(torch.ones([]) * 2.6592)  # ln(1/0.07)

    def forward(self, images, input_ids, attention_mask):
        img_emb = F.normalize(self.vision_proj(self.vision_encoder(images)), dim=-1)
        txt_emb = F.normalize(self.text_proj(
            self.text_encoder(input_ids, attention_mask).pooler_output
        ), dim=-1)

        logit_scale = self.logit_scale.exp().clamp(max=100.0)
        logits = logit_scale * img_emb @ txt_emb.T

        labels = torch.arange(len(images), device=images.device)
        loss_i2t = F.cross_entropy(logits, labels)
        loss_t2i = F.cross_entropy(logits.T, labels)
        return (loss_i2t + loss_t2i) / 2
```

### Contrastive Training Tips

| Parameter | Typical Value | Notes |
|-----------|---------------|-------|
| Temperature (init) | 0.07 (logit_scale ~2.66) | Learnable; clamp max to prevent explosion |
| Batch size | 4096-32768 | Larger is better; use gradient accumulation or multi-GPU |
| LR (vision) | 1e-5 to 5e-6 | Lower than text encoder when using pretrained ViT |
| LR (text) | 5e-5 to 1e-5 | Standard BERT-range fine-tuning |
| Embed dim | 256-768 | 512 is a good default |

## Vision Encoder Integration with LLMs (LLaVA Pattern)

```python
class VisionLanguageModel(nn.Module):
    """LLaVA-style: vision encoder -> projector -> LLM input embedding space."""

    def __init__(self, vision_encoder, llm, vision_dim, llm_dim):
        super().__init__()
        self.vision_encoder = vision_encoder
        self.llm = llm
        # MLP projector (LLaVA v1.5 pattern -- better than linear)
        self.projector = nn.Sequential(
            nn.Linear(vision_dim, llm_dim),
            nn.GELU(),
            nn.Linear(llm_dim, llm_dim),
        )

    def encode_image(self, images):
        with torch.no_grad():
            # Use intermediate features, not CLS token
            features = self.vision_encoder(images, output_hidden_states=True)
            # Second-to-last layer often works best
            img_features = features.hidden_states[-2][:, 1:]  # drop CLS
        return self.projector(img_features)  # (B, num_patches, llm_dim)

    def forward(self, images, input_ids, attention_mask, labels):
        img_tokens = self.encode_image(images)     # (B, N_img, D)
        text_embeds = self.llm.get_input_embeddings()(input_ids)  # (B, N_txt, D)

        # Replace <image> placeholder tokens with visual tokens
        inputs_embeds = merge_image_text_tokens(
            text_embeds, img_tokens, input_ids, image_token_id=32000
        )
        return self.llm(inputs_embeds=inputs_embeds, attention_mask=attention_mask,
                        labels=labels)

def merge_image_text_tokens(text_embeds, img_tokens, input_ids, image_token_id):
    """Replace image placeholder tokens with actual vision embeddings."""
    batch_size = text_embeds.shape[0]
    merged = []
    for b in range(batch_size):
        img_mask = input_ids[b] == image_token_id
        n_img = img_mask.sum()

        # Find insertion point and splice
        img_pos = img_mask.nonzero(as_tuple=True)[0][0]
        merged_seq = torch.cat([
            text_embeds[b][:img_pos],
            img_tokens[b][:n_img],
            text_embeds[b][img_pos + n_img:],
        ], dim=0)
        merged.append(merged_seq)
    return torch.nn.utils.rnn.pad_sequence(merged, batch_first=True)
```

## Cross-Attention Fusion (Flamingo Pattern)

```python
class GatedCrossAttentionBlock(nn.Module):
    """Flamingo-style: cross-attend from LLM hidden states to visual features."""

    def __init__(self, llm_dim, num_heads=8):
        super().__init__()
        self.cross_attn = nn.MultiheadAttention(llm_dim, num_heads, batch_first=True)
        self.ff = nn.Sequential(
            nn.Linear(llm_dim, llm_dim * 4), nn.GELU(), nn.Linear(llm_dim * 4, llm_dim)
        )
        self.ln1 = nn.LayerNorm(llm_dim)
        self.ln2 = nn.LayerNorm(llm_dim)
        # Gating: initialize to zero so cross-attn has no effect initially
        self.gate_attn = nn.Parameter(torch.zeros(1))
        self.gate_ff = nn.Parameter(torch.zeros(1))

    def forward(self, text_hidden, visual_features):
        # text_hidden: (B, T, D), visual_features: (B, N_img, D)
        attn_out, _ = self.cross_attn(
            query=self.ln1(text_hidden),
            key=visual_features, value=visual_features
        )
        text_hidden = text_hidden + self.gate_attn.tanh() * attn_out
        text_hidden = text_hidden + self.gate_ff.tanh() * self.ff(self.ln2(text_hidden))
        return text_hidden
```

## Multimodal Data Loading

```python
from torch.utils.data import Dataset
from torchvision import transforms
from transformers import AutoTokenizer
from PIL import Image

class MultimodalDataset(Dataset):
    def __init__(self, data, tokenizer_name, image_size=336):
        self.data = data
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)
        self.transform = transforms.Compose([
            transforms.Resize((image_size, image_size)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.48145466, 0.4578275, 0.40821073],
                                 std=[0.26862954, 0.26130258, 0.27577711]),
        ])

    def __getitem__(self, idx):
        item = self.data[idx]
        image = self.transform(Image.open(item["image_path"]).convert("RGB"))
        text = self.tokenizer(
            item["text"], max_length=512, padding="max_length",
            truncation=True, return_tensors="pt"
        )
        return {
            "image": image,
            "input_ids": text["input_ids"].squeeze(0),
            "attention_mask": text["attention_mask"].squeeze(0),
            "label": item.get("label"),
        }
```

## Training Recipes

### Stage 1: Alignment Pretraining (LLaVA pattern)
```python
# Freeze vision encoder + LLM, train only projector
for p in model.vision_encoder.parameters(): p.requires_grad = False
for p in model.llm.parameters(): p.requires_grad = False
for p in model.projector.parameters(): p.requires_grad = True

# ~600K image-caption pairs, LR=1e-3, 1 epoch
optimizer = torch.optim.AdamW(model.projector.parameters(), lr=1e-3)
```

### Stage 2: Instruction Tuning
```python
# Freeze vision encoder, unfreeze LLM + projector
for p in model.vision_encoder.parameters(): p.requires_grad = False
for p in model.llm.parameters(): p.requires_grad = True
for p in model.projector.parameters(): p.requires_grad = True

# ~700K instruction-following data, LR=2e-5, 1 epoch
optimizer = torch.optim.AdamW(
    [{"params": model.llm.parameters(), "lr": 2e-5},
     {"params": model.projector.parameters(), "lr": 2e-5}],
    weight_decay=0.0,
)
```

## Gotchas and Anti-Patterns

### Modality Imbalance
- Vision encoders produce 256-576 tokens per image vs 20-200 text tokens. LLM attention cost is O(n^2)
- Use pooling/resampling (Perceiver, Q-Former) to reduce visual tokens to 32-128 for efficiency
- **Anti-pattern**: feeding raw ViT patches (576 tokens) into a 7B LLM for every image -- prohibitive for multi-image

### Resolution vs Compute
- ViT-L/14@336px: 576 patches. ViT-L/14@224px: 196 patches. 3x tokens for 1.5x resolution
- AnyRes/dynamic resolution (LLaVA-NeXT): splits high-res images into tiles, encodes each separately
- Diminishing returns above 384px for most tasks; go higher only for OCR/document understanding

### Tokenization of Images
- Patch-based (ViT): fixed grid, uniform treatment. Simple but wastes compute on background
- Region-based: object proposals + RoI features. Better for detection-oriented tasks but complex
- Discrete tokens (VQ-VAE): enables autoregressive image generation but lossy

### Frozen vs Unfrozen Encoders

| Setup | Pros | Cons | When |
|-------|------|------|------|
| Both frozen | Fast, stable | Limited adaptation | Alignment pretraining (stage 1) |
| Vision frozen, LLM unfrozen | Preserves visual features | LLM may overfit to visual noise | Instruction tuning (stage 2) |
| Both unfrozen | Maximum flexibility | Catastrophic forgetting, expensive | Large dataset, long training |
| Vision LoRA + LLM LoRA | Efficient adaptation | May underfit on complex tasks | Fine-tuning with limited compute |

### Common Mistakes
- Not normalizing embeddings before contrastive loss -- training diverges immediately
- Using CLS token from ViT instead of patch tokens for VLMs -- loses spatial information
- Same learning rate for vision and text encoders -- vision encoder usually needs 5-10x lower
- Not padding/truncating to consistent sequence lengths within batch -- silent shape bugs
- Training projector and LLM simultaneously from scratch -- projector should be aligned first
- Ignoring image aspect ratio (center-crop everything) -- destroys information for documents/charts
