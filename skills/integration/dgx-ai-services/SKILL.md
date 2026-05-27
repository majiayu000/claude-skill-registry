---
name: dgx-ai-services
description: Integrate with Pentatonic's AI services running on DGX Spark - Ollama, Vision, Milvus, Embeddings, Pricing.
allowed-tools: Read, Grep, Glob, Edit, Write, Bash(curl:*), mcp__ssh-dgx__exec
---

# DGX AI Services Skill

## Service Overview

Pentatonic runs several AI services on a DGX Spark, exposed via Cloudflare Tunnels:

| Service | Endpoint | Purpose |
|---------|----------|---------|
| **Ollama** | dgx-ollama.pentatonic.com | LLM inference (Qwen, Llama) |
| **Vision** | dgx-vision.pentatonic.com | Image analysis (Qwen3-VL) |
| **Milvus** | dgx-milvus.pentatonic.com | Vector database |
| **Embeddings** | dgx-embeddings.pentatonic.com | Text embeddings (NV-EmbedQA) |
| **Pricing** | dgx-pricing.pentatonic.com | Dynamic pricing engine |

---

## Ollama (Text LLM)

### Generate Completion

```javascript
async function generateWithOllama(prompt, model = "qwen3:32b") {
  const response = await fetch("https://dgx-ollama.pentatonic.com/api/generate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      model,
      prompt,
      stream: false,
      options: { temperature: 0.7, top_p: 0.9 },
    }),
  });

  const result = await response.json();
  return result.response;
}
```

### Available Models

| Model | Size | Use Case |
|-------|------|----------|
| `qwen3:32b` | 32B | Best quality, complex reasoning |
| `qwen3:8b` | 8B | Fast, good for simple tasks |
| `llama3.2:3b` | 3B | Very fast, basic tasks |

---

## Vision AI (Qwen3-VL)

### Analyze Image

```javascript
async function analyzeImage(imageUrl) {
  const response = await fetch("https://dgx-ollama.pentatonic.com/api/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      model: "qwen2.5-vl:32b",
      messages: [
        {
          role: "user",
          content: `Analyze this product image and provide:
1. Brand name
2. Product type/model
3. Condition (1-10)
4. Color(s)
5. Category

Respond in JSON format.`,
          images: [imageUrl],
        },
      ],
      stream: false,
      options: { temperature: 0.3 },
    }),
  });

  const result = await response.json();
  return JSON.parse(result.message.content);
}
```

---

## Dynamic Pricing Engine

### Get Price Estimate

```javascript
async function getPriceEstimate(imageUrl, category = "general") {
  const response = await fetch("https://dgx-pricing.pentatonic.com/api/analyze-and-price", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      imageUrl,
      productCategory: category,
      mode: "full",
    }),
  });

  const result = await response.json();
  return {
    vision: result.vision_analysis,
    pricing: result.pricing,
    confidence: result.confidence,
  };
}
```

### Response Structure

```javascript
{
  vision_analysis: {
    brand: "Nike",
    model: "Air Max 90",
    condition: 8,
    category: "footwear",
    colors: ["white", "red"],
  },
  pricing: {
    list_price: 12000,      // cents
    buy_back_price: 8500,   // cents
    min_price: 9500,
    max_price: 14500,
    data_points: 47,
    sources: ["ebay_api", "stockx"],
  },
  confidence: 0.85,
}
```

---

## Fallback Strategy

```javascript
async function analyzeWithFallback(imageUrl, env) {
  // Try DGX first
  try {
    return await analyzeImage(imageUrl);
  } catch (error) {
    console.log("DGX failed, falling back to NVIDIA Cloud");
  }

  // Fallback to NVIDIA Cloud API
  const response = await fetch("https://integrate.api.nvidia.com/v1/chat/completions", {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${env.NVIDIA_API_KEY}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      model: "nvidia/llama-3.2-nv-vision-90b-instruct",
      messages: [
        {
          role: "user",
          content: [
            { type: "text", text: "Analyze this product..." },
            { type: "image_url", image_url: { url: imageUrl } },
          ],
        },
      ],
    }),
  });

  return response.json();
}
```

---

## Error Handling

```javascript
async function callWithRetry(fn, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      const delay = Math.pow(2, i) * 1000;
      await new Promise(r => setTimeout(r, delay));
    }
  }
}
```
