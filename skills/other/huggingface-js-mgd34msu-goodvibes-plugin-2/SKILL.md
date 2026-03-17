---
name: huggingface-js
description: Runs ML models in the browser and Node.js with Transformers.js and Hugging Face Inference API. Use when adding local inference, embeddings, or calling hosted models without GPU servers.
---

# Hugging Face JavaScript

Run ML models locally with Transformers.js or via the Inference API. Supports text generation, embeddings, image classification, speech recognition, and more.

## Transformers.js (Local Inference)

Run models directly in browser or Node.js using ONNX Runtime.

```bash
npm install @huggingface/transformers
```

### Text Generation

```typescript
import { pipeline } from '@huggingface/transformers';

const generator = await pipeline('text-generation', 'Xenova/gpt2');

const result = await generator('The quick brown fox', {
  max_new_tokens: 50,
});

console.log(result[0].generated_text);
```

### Text Classification (Sentiment)

```typescript
import { pipeline } from '@huggingface/transformers';

const classifier = await pipeline(
  'text-classification',
  'Xenova/distilbert-base-uncased-finetuned-sst-2-english'
);

const result = await classifier('I love this product!');
// [{ label: 'POSITIVE', score: 0.9998 }]
```

### Embeddings

```typescript
import { pipeline } from '@huggingface/transformers';

const embedder = await pipeline(
  'feature-extraction',
  'Xenova/all-MiniLM-L6-v2'
);

const result = await embedder('Hello, world!', {
  pooling: 'mean',
  normalize: true,
});

const embedding = Array.from(result.data);
// [0.123, -0.456, ...] - 384 dimensions
```

### Question Answering

```typescript
import { pipeline } from '@huggingface/transformers';

const qa = await pipeline(
  'question-answering',
  'Xenova/distilbert-base-cased-distilled-squad'
);

const result = await qa({
  question: 'What is the capital of France?',
  context: 'France is a country in Europe. Paris is the capital of France.',
});

console.log(result);
// { answer: 'Paris', score: 0.98, start: 42, end: 47 }
```

### Translation

```typescript
import { pipeline } from '@huggingface/transformers';

const translator = await pipeline(
  'translation',
  'Xenova/nllb-200-distilled-600M'
);

const result = await translator('Hello, how are you?', {
  src_lang: 'eng_Latn',
  tgt_lang: 'fra_Latn',
});

console.log(result[0].translation_text);
```

### Speech Recognition (Whisper)

```typescript
import { pipeline } from '@huggingface/transformers';

const transcriber = await pipeline(
  'automatic-speech-recognition',
  'Xenova/whisper-tiny.en'
);

const result = await transcriber('./audio.mp3');
console.log(result.text);
```

### Image Classification

```typescript
import { pipeline } from '@huggingface/transformers';

const classifier = await pipeline(
  'image-classification',
  'Xenova/vit-base-patch16-224'
);

const result = await classifier('https://example.com/cat.jpg');
// [{ label: 'tabby cat', score: 0.95 }, ...]
```

### Object Detection

```typescript
import { pipeline } from '@huggingface/transformers';

const detector = await pipeline(
  'object-detection',
  'Xenova/detr-resnet-50'
);

const result = await detector('https://example.com/image.jpg');
// [{ label: 'cat', score: 0.98, box: { xmin, ymin, xmax, ymax } }, ...]
```

### Zero-Shot Classification

```typescript
import { pipeline } from '@huggingface/transformers';

const classifier = await pipeline(
  'zero-shot-classification',
  'Xenova/bart-large-mnli'
);

const result = await classifier(
  'This is a tutorial about machine learning',
  ['education', 'politics', 'sports']
);

console.log(result);
// { labels: ['education', ...], scores: [0.95, ...] }
```

## Hugging Face Inference API

Call hosted models without local computation.

```bash
npm install @huggingface/inference
```

### Setup

```typescript
import { HfInference } from '@huggingface/inference';

const hf = new HfInference(process.env.HF_ACCESS_TOKEN);
```

### Text Generation

```typescript
const result = await hf.textGeneration({
  model: 'meta-llama/Llama-2-7b-chat-hf',
  inputs: 'What is the meaning of life?',
  parameters: {
    max_new_tokens: 100,
    temperature: 0.7,
  },
});

console.log(result.generated_text);
```

### Streaming Text Generation

```typescript
const stream = hf.textGenerationStream({
  model: 'meta-llama/Llama-2-7b-chat-hf',
  inputs: 'Tell me a story',
  parameters: {
    max_new_tokens: 200,
  },
});

for await (const chunk of stream) {
  process.stdout.write(chunk.token.text);
}
```

### Chat Completion

```typescript
const result = await hf.chatCompletion({
  model: 'meta-llama/Llama-2-7b-chat-hf',
  messages: [
    { role: 'user', content: 'Hello!' },
  ],
  max_tokens: 100,
});

console.log(result.choices[0].message.content);
```

### Embeddings

```typescript
const result = await hf.featureExtraction({
  model: 'sentence-transformers/all-MiniLM-L6-v2',
  inputs: 'Hello, world!',
});

console.log(result); // embedding vector
```

### Image Generation

```typescript
const result = await hf.textToImage({
  model: 'stabilityai/stable-diffusion-2',
  inputs: 'A futuristic city at sunset',
  parameters: {
    negative_prompt: 'blurry, low quality',
  },
});

// result is a Blob
const buffer = Buffer.from(await result.arrayBuffer());
fs.writeFileSync('output.png', buffer);
```

### Image Classification

```typescript
const result = await hf.imageClassification({
  model: 'google/vit-base-patch16-224',
  data: await fs.openAsBlob('cat.jpg'),
});

console.log(result);
// [{ label: 'tabby cat', score: 0.95 }, ...]
```

### Speech Recognition

```typescript
const result = await hf.automaticSpeechRecognition({
  model: 'openai/whisper-large-v3',
  data: await fs.openAsBlob('audio.mp3'),
});

console.log(result.text);
```

## Inference Endpoints

For dedicated hosted models.

```typescript
import { InferenceClient } from '@huggingface/inference';

const client = new InferenceClient(process.env.HF_ACCESS_TOKEN);
const endpoint = client.endpoint('https://your-endpoint.endpoints.huggingface.cloud');

const result = await endpoint.textGeneration({
  inputs: 'Hello, world!',
});
```

## Next.js Integration

```typescript
// app/api/generate/route.ts
import { HfInference } from '@huggingface/inference';
import { NextResponse } from 'next/server';

const hf = new HfInference(process.env.HF_ACCESS_TOKEN);

export async function POST(request: Request) {
  const { prompt } = await request.json();

  const result = await hf.textGeneration({
    model: 'meta-llama/Llama-2-7b-chat-hf',
    inputs: prompt,
    parameters: {
      max_new_tokens: 200,
    },
  });

  return NextResponse.json({ text: result.generated_text });
}
```

### Streaming Response

```typescript
// app/api/stream/route.ts
import { HfInference } from '@huggingface/inference';

const hf = new HfInference(process.env.HF_ACCESS_TOKEN);

export async function POST(request: Request) {
  const { prompt } = await request.json();

  const stream = hf.textGenerationStream({
    model: 'meta-llama/Llama-2-7b-chat-hf',
    inputs: prompt,
    parameters: { max_new_tokens: 200 },
  });

  const encoder = new TextEncoder();
  const readable = new ReadableStream({
    async start(controller) {
      for await (const chunk of stream) {
        controller.enqueue(encoder.encode(chunk.token.text));
      }
      controller.close();
    },
  });

  return new Response(readable, {
    headers: { 'Content-Type': 'text/plain' },
  });
}
```

## Browser Usage

Transformers.js works in the browser with WebGPU acceleration.

```html
<script type="module">
  import { pipeline } from 'https://cdn.jsdelivr.net/npm/@huggingface/transformers';

  const classifier = await pipeline('text-classification');
  const result = await classifier('I love this!');
  console.log(result);
</script>
```

### With WebGPU

```typescript
import { pipeline, env } from '@huggingface/transformers';

// Enable WebGPU
env.backends.onnx.wasm.proxy = true;

const classifier = await pipeline('text-classification', 'model-name', {
  device: 'webgpu',
});
```

## Configuration

```typescript
import { env } from '@huggingface/transformers';

// Cache settings
env.cacheDir = './models';
env.localModelPath = './local-models';

// Disable remote models (offline mode)
env.allowRemoteModels = false;

// Disable local models
env.allowLocalModels = false;
```

## Available Tasks

| Task | Pipeline | Example Model |
|------|----------|---------------|
| Text Classification | text-classification | distilbert-base-uncased-finetuned-sst-2-english |
| Text Generation | text-generation | gpt2, llama |
| Question Answering | question-answering | distilbert-base-cased-distilled-squad |
| Summarization | summarization | t5-small |
| Translation | translation | nllb-200-distilled-600M |
| Feature Extraction | feature-extraction | all-MiniLM-L6-v2 |
| Image Classification | image-classification | vit-base-patch16-224 |
| Object Detection | object-detection | detr-resnet-50 |
| Speech Recognition | automatic-speech-recognition | whisper-tiny |
| Zero-Shot Classification | zero-shot-classification | bart-large-mnli |

## Environment Variables

```bash
HF_ACCESS_TOKEN=hf_xxxxxxxx
```

## Best Practices

1. **Cache models** - Download once, reuse
2. **Use WebGPU** - Faster inference in browsers
3. **Choose small models** - For client-side use
4. **Stream responses** - Better UX for generation
5. **Use Inference API** - For large models
6. **Consider endpoints** - For production workloads
7. **Quantized models** - Smaller, faster (look for ONNX models)
