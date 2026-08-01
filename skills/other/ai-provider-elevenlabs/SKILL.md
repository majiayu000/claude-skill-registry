---
name: ai-provider-elevenlabs
description: ElevenLabs voice AI SDK patterns for TypeScript/Node.js -- text-to-speech, streaming, voice cloning, speech-to-speech, pronunciation control, and conversational AI
---

# ElevenLabs Patterns

> **Quick Guide:** Use the official `@elevenlabs/elevenlabs-js` package to interact with the ElevenLabs API. Use `client.textToSpeech.convert()` for full audio generation or `client.textToSpeech.stream()` for low-latency streaming. Voice settings (`stability`, `similarityBoost`, `style`) control output character. Use `eleven_v3` for best quality, `eleven_flash_v2_5` for lowest latency, or `eleven_multilingual_v2` for stable long-form content. The SDK returns `ReadableStream<Uint8Array>` -- pipe to files or HTTP responses. Use `@elevenlabs/client` for real-time conversational AI agents.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use `@elevenlabs/elevenlabs-js` for server-side TTS, voice management, and speech-to-speech -- use `@elevenlabs/client` only for conversational AI agents)**

**(You MUST never hardcode API keys -- always use environment variables via `process.env.ELEVENLABS_API_KEY` which the SDK reads automatically)**

**(You MUST consume the `ReadableStream<Uint8Array>` returned by `convert()` and `stream()` -- unconsumed streams leak resources)**

**(You MUST choose the correct model for your use case -- `eleven_v3` for quality, `eleven_flash_v2_5` for speed, `eleven_multilingual_v2` for long-form stability)**

**(You MUST pass `voiceId` as the first positional argument to all `textToSpeech` methods -- it is NOT inside the options object)**

</critical_requirements>

---

**Auto-detection:** ElevenLabs, elevenlabs, ElevenLabsClient, textToSpeech.convert, textToSpeech.stream, eleven_multilingual_v2, eleven_flash_v2_5, eleven_v3, speechToSpeech, voices.search, voice cloning, ELEVENLABS_API_KEY, @elevenlabs/elevenlabs-js, @elevenlabs/client, text-to-speech, TTS, voice synthesis

**When to use:**

- Generating speech audio from text (narration, audiobooks, announcements)
- Streaming audio in real-time for low-latency playback
- Cloning voices from audio samples (instant or professional voice cloning)
- Converting speech from one voice to another (speech-to-speech)
- Building real-time conversational AI agents with voice interaction
- Controlling pronunciation with SSML or pronunciation dictionaries
- Generating audio with character-level timestamp alignment

**Key patterns covered:**

- Client initialization and configuration (retries, timeouts, API key)
- Text-to-speech conversion and streaming (`convert`, `stream`, timestamps)
- Voice settings (`stability`, `similarityBoost`, `style`, `speed`)
- Voice selection and management (`voices.search`, `voices.get`)
- Voice cloning (instant via `voices.ivc.create`)
- Speech-to-speech voice conversion
- WebSocket input streaming for real-time text-to-speech
- Pronunciation dictionaries and SSML
- Conversational AI agents (`@elevenlabs/client`)
- Model selection, output formats, error handling

**When NOT to use:**

- You need multi-provider voice AI (multiple TTS vendors) -- use a unified abstraction
- You only need browser-side audio playback without generation -- use the Web Audio API
- You need speech-to-text transcription only -- ElevenLabs has this, but it is a separate concern

---

## Examples Index

- [Core: Setup, TTS, Streaming & Voice Settings](examples/core.md) -- Client init, convert, stream, timestamps, voice settings, output formats
- [Voices & Cloning](examples/voices.md) -- Voice search, selection, instant voice cloning, speech-to-speech
- [WebSocket & Conversational AI](examples/websocket.md) -- WebSocket input streaming, conversational AI agents, real-time patterns
- [Quick API Reference](reference.md) -- Model IDs, method signatures, output formats, error types, voice settings

---

<philosophy>

## Philosophy

The ElevenLabs SDK provides **direct access to the most advanced voice AI API** available. It wraps the ElevenLabs REST API with full TypeScript types, streaming support, and automatic retries.

**Core principles:**

1. **Streams everywhere** -- All audio methods return `ReadableStream<Uint8Array>`. You pipe them to files, HTTP responses, or audio players. The SDK never buffers entire audio files in memory.
2. **Voice settings are the primary control surface** -- `stability`, `similarityBoost`, `style`, and `speed` shape every generation. Learn these four knobs well.
3. **Model selection drives the quality/latency tradeoff** -- `eleven_v3` for best quality, `eleven_flash_v2_5` for sub-75ms latency, `eleven_multilingual_v2` for stable long-form.
4. **Two packages for two use cases** -- `@elevenlabs/elevenlabs-js` for server-side TTS/voice management, `@elevenlabs/client` for browser-side conversational AI agents.
5. **Built-in resilience** -- The SDK retries on 408, 409, 429, and 5xx errors (2 retries by default) with configurable timeouts.

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Client Setup

Initialize the ElevenLabs client. It auto-reads `ELEVENLABS_API_KEY` from the environment.

```typescript
// lib/elevenlabs.ts -- basic setup
import { ElevenLabsClient } from "@elevenlabs/elevenlabs-js";

const client = new ElevenLabsClient();
export { client };
```

```typescript
// lib/elevenlabs.ts -- production configuration
import { ElevenLabsClient } from "@elevenlabs/elevenlabs-js";

const TIMEOUT_SECONDS = 60;
const MAX_RETRIES = 3;

const client = new ElevenLabsClient({
  apiKey: process.env.ELEVENLABS_API_KEY,
  timeoutInSeconds: TIMEOUT_SECONDS,
  maxRetries: MAX_RETRIES,
});

export { client };
```

**Why good:** Minimal setup, env var auto-detected, named constants for production settings

```typescript
// BAD: Hardcoded API key
const client = new ElevenLabsClient({
  apiKey: "sk-1234567890abcdef",
});
```

**Why bad:** Hardcoded API key is a security breach risk, will leak in version control

**See:** [examples/core.md](examples/core.md) for per-request overrides, error handling

---

### Pattern 2: Text-to-Speech (Convert)

Generate complete audio from text. Returns `ReadableStream<Uint8Array>`.

```typescript
import { createWriteStream } from "node:fs";
import { Readable } from "node:stream";

const VOICE_ID = "JBFqnCBsd6RMkjVDRZzb"; // George

const audio = await client.textToSpeech.convert(VOICE_ID, {
  text: "Welcome to the application.",
  modelId: "eleven_multilingual_v2",
  outputFormat: "mp3_44100_128",
});

// Pipe to file
const readable = Readable.fromWeb(audio);
const fileStream = createWriteStream("output.mp3");
readable.pipe(fileStream);
```

**Why good:** `voiceId` as first arg (required), model and format explicit, stream piped to file without buffering

```typescript
// BAD: voiceId inside options object
const audio = await client.textToSpeech.convert({
  voiceId: VOICE_ID, // WRONG: voiceId is a positional argument
  text: "Hello",
});
```

**Why bad:** `voiceId` is the first positional argument, not an options field -- this will throw a type error

**See:** [examples/core.md](examples/core.md) for timestamps, HTTP response piping

---

### Pattern 3: Text-to-Speech (Stream)

Stream audio for real-time playback with lower latency than `convert()`.

```typescript
const VOICE_ID = "JBFqnCBsd6RMkjVDRZzb";
const LATENCY_OPTIMIZATION = 2;

const audioStream = await client.textToSpeech.stream(VOICE_ID, {
  text: "This streams with lower latency for real-time playback.",
  modelId: "eleven_flash_v2_5",
  optimizeStreamingLatency: LATENCY_OPTIMIZATION,
  outputFormat: "mp3_44100_128",
});

// Consume the stream
for await (const chunk of audioStream) {
  process.stdout.write(chunk); // Or pipe to audio player / HTTP response
}
```

**Why good:** Uses `stream()` for lower latency, `eleven_flash_v2_5` for speed, `optimizeStreamingLatency` reduces first-byte time

```typescript
// BAD: Stream created but never consumed
const audioStream = await client.textToSpeech.stream(VOICE_ID, {
  text: "This audio is lost",
  modelId: "eleven_flash_v2_5",
});
// Stream never consumed -- resources leaked
```

**Why bad:** Unconsumed streams leak resources and the audio data is silently lost

**See:** [examples/core.md](examples/core.md) for streaming to HTTP responses

---

### Pattern 4: Voice Settings

Control voice characteristics with `voiceSettings`.

```typescript
const VOICE_ID = "JBFqnCBsd6RMkjVDRZzb";

const audio = await client.textToSpeech.convert(VOICE_ID, {
  text: "Emotional and expressive delivery.",
  modelId: "eleven_v3",
  voiceSettings: {
    stability: 0.3, // Lower = more expressive/variable
    similarityBoost: 0.8, // Higher = closer to original voice
    style: 0.5, // Higher = more style exaggeration
    useSpeakerBoost: true, // Enhanced speaker similarity (adds latency)
    speed: 1.0, // 0.7-1.3 range typical
  },
});
```

**Why good:** All settings explicit with clear purpose, stability lowered for expressive content

```typescript
// BAD: Using extreme values without understanding
const audio = await client.textToSpeech.convert(VOICE_ID, {
  text: "Extreme settings cause artifacts.",
  modelId: "eleven_v3",
  voiceSettings: {
    stability: 0.0, // Too unstable -- garbled output
    similarityBoost: 1.0, // Combined with low stability = artifacts
    style: 1.0, // Maximum exaggeration -- unnatural
  },
});
```

**Why bad:** Extreme values produce artifacts; `stability: 0.0` with high `similarityBoost` is unstable. Start with defaults and adjust incrementally.

**See:** [reference.md](reference.md) for voice settings ranges and recommended starting values

---

### Pattern 5: Voice Selection and Management

Find and select voices from the ElevenLabs voice library.

```typescript
// Search all available voices
const { voices } = await client.voices.search();

for (const voice of voices) {
  console.log(`${voice.name} (${voice.voiceId}) - ${voice.category}`);
}

// Get a specific voice by ID
const VOICE_ID = "JBFqnCBsd6RMkjVDRZzb";
const voice = await client.voices.get(VOICE_ID);
console.log(voice.name, voice.settings);
```

**Why good:** Uses `voices.search()` to discover available voices, `voices.get()` for details

**See:** [examples/voices.md](examples/voices.md) for filtering, voice cloning, speech-to-speech

---

### Pattern 6: Voice Cloning (Instant)

Create an instant voice clone from audio samples.

```typescript
import { createReadStream } from "node:fs";

const voice = await client.voices.ivc.create({
  name: "My Custom Voice",
  files: [createReadStream("sample1.mp3"), createReadStream("sample2.mp3")],
  removeBackgroundNoise: true,
});

console.log(`Created voice: ${voice.voiceId}`);

// Use the cloned voice for TTS
const audio = await client.textToSpeech.convert(voice.voiceId, {
  text: "Speaking in the cloned voice.",
  modelId: "eleven_multilingual_v2",
});
```

**Why good:** `removeBackgroundNoise` improves quality, multiple samples improve accuracy, immediately usable

**See:** [examples/voices.md](examples/voices.md) for professional voice cloning, sample validation

---

### Pattern 7: Speech-to-Speech

Convert speech from one voice to another while preserving emotion and cadence.

```typescript
import { createReadStream } from "node:fs";

const TARGET_VOICE_ID = "JBFqnCBsd6RMkjVDRZzb";

const convertedAudio = await client.speechToSpeech.convert(TARGET_VOICE_ID, {
  audio: createReadStream("input-speech.mp3"),
  modelId: "eleven_multilingual_sts_v2",
  voiceSettings: {
    stability: 0.5,
    similarityBoost: 0.75,
  },
});
```

**Why good:** Uses STS-specific model, preserves source emotion, voice settings control output fidelity

**See:** [examples/voices.md](examples/voices.md) for streaming STS, English-only model

---

### Pattern 8: Error Handling

Catch SDK errors and handle specific failure modes.

```typescript
import {
  ElevenLabsError,
  ElevenLabsTimeoutError,
} from "@elevenlabs/elevenlabs-js";

const VOICE_ID = "JBFqnCBsd6RMkjVDRZzb";

try {
  const audio = await client.textToSpeech.convert(VOICE_ID, {
    text: "Hello, world.",
    modelId: "eleven_multilingual_v2",
  });
} catch (error) {
  if (error instanceof ElevenLabsTimeoutError) {
    console.error("Request timed out -- increase timeoutInSeconds or retry");
  } else if (error instanceof ElevenLabsError) {
    console.error(`ElevenLabs API error: ${error.message}`);
    console.error(`Status: ${error.statusCode}`);
    console.error(`Body: ${JSON.stringify(error.body)}`);
  } else {
    throw error; // Re-throw non-ElevenLabs errors
  }
}
```

**Why good:** Catches specific error types, logs status code and body for debugging, re-throws unknown errors

**See:** [examples/core.md](examples/core.md) for stream error handling, retry patterns

</patterns>

---

<performance>

## Performance Optimization

### Model Selection for Latency/Quality

```
Best quality + expressiveness  -> eleven_v3 (70+ languages)
Long-form stability            -> eleven_multilingual_v2 (29 languages, 10K char limit)
Lowest latency (<75ms)         -> eleven_flash_v2_5 (32 languages, 40K char limit)
English-only low latency       -> eleven_flash_v2 (English only, 30K char limit)
Voice design from text prompt  -> eleven_ttv_v3 (70+ languages)
```

### Key Optimization Patterns

- **Use `stream()` instead of `convert()`** for user-facing audio -- playback starts before generation completes
- **Set `optimizeStreamingLatency`** (0-4) on `stream()` calls -- higher values reduce latency but may affect text normalization
- **Use `eleven_flash_v2_5`** for real-time applications -- sub-75ms latency at 50% lower cost
- **Use `previous_request_ids`** for multi-part generation -- maintains voice consistency across segments
- **Batch multiple short texts** into single requests when possible -- reduces API call overhead
- **Cache generated audio** for static content -- avoid re-generating identical text
- **Use `outputFormat: "pcm_16000"`** for server-side processing pipelines -- lower bandwidth than MP3

</performance>

---

<decision_framework>

## Decision Framework

### Which Model to Choose

```
What is your priority?
+-- Best quality / expressiveness -> eleven_v3
+-- Lowest latency (<75ms) -> eleven_flash_v2_5
+-- Long-form stability (audiobooks) -> eleven_multilingual_v2
+-- English-only speed -> eleven_flash_v2
+-- Voice design from text description -> eleven_ttv_v3
+-- Speech-to-speech conversion -> eleven_multilingual_sts_v2 (or eleven_english_sts_v2)
```

### convert() vs stream()

```
Is the audio user-facing with real-time playback?
+-- YES -> Use stream() for progressive playback
|   +-- Need timestamps? -> streamWithTimestamps()
+-- NO -> Use convert() for complete audio
    +-- Need timestamps? -> convertWithTimestamps()
    +-- Saving to file? -> convert() and pipe to WriteStream
```

### Which Package to Use

```
What are you building?
+-- Server-side TTS, voice management, STS -> @elevenlabs/elevenlabs-js
+-- Browser conversational AI agent -> @elevenlabs/client
+-- React conversational AI agent -> @elevenlabs/react
+-- WebSocket text input streaming -> @elevenlabs/elevenlabs-js (or raw WebSocket)
```

### Output Format Selection

```
What is the audio destination?
+-- Web browser playback -> mp3_44100_128 (universal compatibility)
+-- Low-bandwidth streaming -> opus_48000_64 (smaller files)
+-- Audio processing pipeline -> pcm_16000 or pcm_44100 (raw audio)
+-- Telephony / IVR -> ulaw_8000 or alaw_8000 (legacy codecs)
+-- High-quality archival -> wav_44100 or mp3_44100_192
```

</decision_framework>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- Hardcoding API keys instead of using `process.env.ELEVENLABS_API_KEY` (security breach risk)
- Not consuming streams returned by `convert()` or `stream()` (resources leaked, audio lost)
- Passing `voiceId` inside the options object instead of as the first positional argument (type error)
- Using deprecated `eleven_turbo_v2_5` instead of `eleven_flash_v2_5` (migrate to Flash models)
- Using deprecated `eleven_monolingual_v1` or `eleven_multilingual_v1` (use v2+ models)

**Medium Priority Issues:**

- Not setting `timeoutInSeconds` for production (default is 240 seconds -- may be too long or too short)
- Using `stability: 0.0` or extreme voice settings without testing (produces artifacts)
- Not using `optimizeStreamingLatency` when streaming to users (adds unnecessary latency)
- Ignoring `outputFormat` and relying on the default when a specific format is needed
- Creating voice clones with a single short sample (multiple 30s+ samples improve quality)

**Common Mistakes:**

- Confusing `@elevenlabs/elevenlabs-js` (server-side TTS SDK) with `@elevenlabs/client` (conversational AI agents SDK) -- they serve different purposes
- Using `textToSpeech.convert()` for real-time playback instead of `textToSpeech.stream()` -- convert waits for full generation
- Sending text longer than the model's character limit (10K for multilingual_v2, 40K for flash_v2_5, 5K for v3) -- request will fail
- Not using `previous_request_ids` for multi-part audio -- causes voice inconsistency between segments
- Using `eleven_v3` when latency matters -- it has higher latency than Flash models

**Gotchas & Edge Cases:**

- The SDK auto-retries on 408, 409, 429, and 5xx errors -- 2 retries by default. Set `maxRetries: 0` if you handle retries yourself.
- `convert()` and `stream()` both return `ReadableStream<Uint8Array>` but `stream()` starts sending data before generation completes (lower time-to-first-byte).
- `convertWithTimestamps()` returns `{ audioBase64, alignment }` NOT a stream -- the entire audio is base64-encoded.
- `streamWithTimestamps()` returns an SSE `Stream<ChunkWithTimestamps>` -- each chunk has audio data AND character timing.
- Voice settings are optional -- if omitted, the voice's default settings are used. Override per-request for fine-tuning.
- The `play()` helper function from the SDK requires MPV and FFmpeg installed locally -- not suitable for production servers.
- WebSocket input streaming text must end with a space character for proper buffering.
- WebSocket `chunk_length_schedule` defaults to `[120, 160, 250, 290]` characters -- audio generation starts after the first threshold.
- Pronunciation dictionaries are limited to 3 per request and must be provided in the first WebSocket message.
- `enable_ssml_parsing` must be set as a query parameter on the WebSocket connection, not in the text message.
- The `speed` voice setting accepts values roughly in the 0.7-1.3 range for natural-sounding output.
- Free tier has 2-4 concurrent request limits -- higher tiers get elevated concurrency.

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use `@elevenlabs/elevenlabs-js` for server-side TTS, voice management, and speech-to-speech -- use `@elevenlabs/client` only for conversational AI agents)**

**(You MUST never hardcode API keys -- always use environment variables via `process.env.ELEVENLABS_API_KEY` which the SDK reads automatically)**

**(You MUST consume the `ReadableStream<Uint8Array>` returned by `convert()` and `stream()` -- unconsumed streams leak resources)**

**(You MUST choose the correct model for your use case -- `eleven_v3` for quality, `eleven_flash_v2_5` for speed, `eleven_multilingual_v2` for long-form stability)**

**(You MUST pass `voiceId` as the first positional argument to all `textToSpeech` methods -- it is NOT inside the options object)**

**Failure to follow these rules will produce broken, insecure, or degraded voice AI integrations.**

</critical_reminders>
