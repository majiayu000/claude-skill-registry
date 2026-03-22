---
name: api-ai-openai-whisper
description: Speech-to-text transcription and translation via OpenAI Audio API -- models, response formats, timestamps, prompting, streaming, chunking, and diarization
---

# OpenAI Whisper Patterns

> **Quick Guide:** Use `client.audio.transcriptions.create()` for speech-to-text and `client.audio.translations.create()` for non-English audio to English text. Choose `gpt-4o-transcribe` for highest accuracy, `gpt-4o-mini-transcribe` for cost-efficiency, `whisper-1` for timestamps/SRT/VTT, or `gpt-4o-transcribe-diarize` for speaker identification. Files must be under 25 MB -- chunk larger files. Use `prompt` to guide vocabulary and style. Streaming is available via `stream: true` for progressive output on `gpt-4o-transcribe` models.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST choose the correct model for the use case -- `gpt-4o-transcribe` for accuracy, `whisper-1` for timestamps/SRT/VTT output, `gpt-4o-transcribe-diarize` for speaker labels)**

**(You MUST chunk audio files larger than 25 MB before sending to the API -- the API rejects files exceeding this limit)**

**(You MUST pass `response_format: "verbose_json"` when using `timestamp_granularities` -- timestamps only work with this format on `whisper-1`)**

**(You MUST set `chunking_strategy: "auto"` when using `gpt-4o-transcribe-diarize` with audio longer than 30 seconds -- the API requires it)**

</critical_requirements>

---

**Auto-detection:** Whisper, whisper-1, gpt-4o-transcribe, gpt-4o-mini-transcribe, gpt-4o-transcribe-diarize, audio.transcriptions, audio.translations, transcription, speech-to-text, diarization, diarized_json, timestamp_granularities, verbose_json

**When to use:**

- Transcribing audio files (meetings, interviews, podcasts, voice notes) to text
- Translating non-English audio to English text
- Generating subtitles in SRT or VTT format from audio
- Getting word-level or segment-level timestamps for video editing
- Identifying speakers in multi-speaker audio (diarization)
- Streaming transcription results progressively as the model processes audio

**Key patterns covered:**

- Model selection (whisper-1 vs gpt-4o-transcribe vs gpt-4o-mini-transcribe vs gpt-4o-transcribe-diarize)
- Response formats (json, text, srt, vtt, verbose_json, diarized_json)
- Timestamps (word-level, segment-level) and subtitle generation
- Prompting for vocabulary, acronyms, and style
- Chunking large files (> 25 MB) with context preservation
- Streaming transcription with `stream: true`
- Translation to English via `audio.translations.create()`
- Speaker diarization with speaker references

**When NOT to use:**

- Text-to-speech (TTS) -- use the OpenAI TTS API (`client.audio.speech.create()`)
- Real-time bidirectional voice conversations -- use the OpenAI Realtime API
- Transcription with non-OpenAI providers -- use a provider-agnostic speech SDK

---

## Examples Index

- [Core: Transcription, Translation, Timestamps, Chunking, Streaming, Diarization](examples/core.md) -- All audio API patterns

---

<philosophy>

## Philosophy

The OpenAI Audio API provides **speech-to-text transcription and translation** through multiple models optimized for different needs. The API is simple -- you send an audio file and get text back -- but choosing the right model, response format, and parameters is critical for quality results.

**Core principles:**

1. **Model selection matters** -- `gpt-4o-transcribe` produces the highest accuracy with lower hallucination rates. `whisper-1` is the only model supporting SRT/VTT/verbose_json with timestamps. `gpt-4o-transcribe-diarize` adds speaker identification.
2. **File size is the primary constraint** -- 25 MB limit means you must chunk longer audio. Split at sentence boundaries to preserve context.
3. **Prompting improves accuracy** -- The `prompt` parameter guides vocabulary, acronyms, and formatting style. It does not give instructions -- it provides context the model matches against.
4. **Response format determines available features** -- Timestamps require `verbose_json` on `whisper-1`. Diarization requires `diarized_json`. SRT/VTT are only on `whisper-1`.

**When to use the Audio API:**

- You need accurate transcription of recorded audio files
- You need subtitles (SRT/VTT) from audio
- You need to identify who is speaking in a conversation
- You need to translate non-English speech to English text

**When NOT to use:**

- Real-time voice chat -- use the Realtime API instead
- Text-to-speech -- use `client.audio.speech.create()`
- You need transcription in a non-English target language (translation only outputs English)

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Basic Transcription

Send an audio file and receive text back. The model auto-detects the language.

```typescript
const transcription = await client.audio.transcriptions.create({
  model: "gpt-4o-transcribe",
  file: createReadStream(audioPath),
});
```

Use `gpt-4o-transcribe` for highest accuracy. Do not use `whisper-1` with `verbose_json` when you only need plain text -- it adds overhead and has higher hallucination rates. See [core.md](examples/core.md) for full examples.

---

### Pattern 2: Model Selection

Each model has distinct capabilities and tradeoffs.

```
What do you need?
+-- Highest accuracy, plain text -> gpt-4o-transcribe
+-- Cost-efficient, plain text -> gpt-4o-mini-transcribe
+-- Timestamps (word/segment) -> whisper-1 (verbose_json)
+-- SRT or VTT subtitles -> whisper-1 (srt/vtt format)
+-- Speaker identification -> gpt-4o-transcribe-diarize
+-- Streaming output -> gpt-4o-transcribe or gpt-4o-mini-transcribe
```

#### Model Capabilities Matrix

| Feature          | whisper-1                          | gpt-4o-transcribe | gpt-4o-mini-transcribe | gpt-4o-transcribe-diarize |
| ---------------- | ---------------------------------- | ----------------- | ---------------------- | ------------------------- |
| Response formats | json, text, srt, vtt, verbose_json | json, text        | json, text             | json, text, diarized_json |
| Timestamps       | word + segment                     | No                | No                     | No                        |
| Streaming        | No                                 | Yes               | Yes                    | No                        |
| Prompt support   | Yes (224 tokens)                   | Yes               | Yes                    | No                        |
| Logprobs         | No                                 | Yes               | Yes                    | No                        |
| Speaker labels   | No                                 | No                | No                     | Yes                       |
| Language param   | Yes                                | Yes               | Yes                    | Yes                       |

---

### Pattern 3: Prompting for Vocabulary and Style

The `prompt` parameter provides context -- not instructions. It guides spelling of names, acronyms, and formatting style. Do not use it to give instructions like "please transcribe carefully" -- it matches style and vocabulary context.

```typescript
const VOCABULARY_PROMPT = "Kubernetes, kubectl, etcd, NGINX, gRPC, PostgreSQL";

const transcription = await client.audio.transcriptions.create({
  model: "gpt-4o-transcribe",
  file: createReadStream(audioPath),
  prompt: VOCABULARY_PROMPT,
});
```

**Use cases:** Acronyms/proper nouns, preserving context across chunks (pass tail of previous transcript), maintaining filler words, writing style guidance. See [core.md](examples/core.md) for detailed vocabulary examples.

---

### Pattern 4: Chunking Large Files

Audio files exceeding 25 MB must be split before transcription. Split at sentence boundaries (e.g., via ffmpeg) to preserve context. Pass the tail of the previous transcript as `prompt` for continuity across chunks.

```typescript
const MAX_FILE_SIZE_BYTES = 25 * 1024 * 1024; // 25 MB
// Split with ffmpeg: ffmpeg -i long.mp3 -f segment -segment_time 600 -c copy chunk_%03d.mp3
// Then transcribe sequentially, passing previous context via prompt
```

See [core.md](examples/core.md) for the full chunking implementation with size validation and context preservation.

---

### Pattern 5: Streaming Transcription

Stream partial transcription results as the model processes audio. Only `gpt-4o-transcribe` and `gpt-4o-mini-transcribe` support `stream: true`. Listen for `transcript.text.delta` events for progressive output and `transcript.text.done` for completion. Do NOT use `stream: true` with `whisper-1` -- it is not supported.

```typescript
const stream = await client.audio.transcriptions.create({
  model: "gpt-4o-transcribe",
  file: createReadStream(audioPath),
  stream: true,
});
for await (const event of stream) {
  if (event.type === "transcript.text.delta") process.stdout.write(event.delta);
}
```

See [core.md](examples/core.md) for full streaming and logprob examples.

---

### Pattern 6: Translation to English

Translate non-English audio to English text. Only `whisper-1` is supported via `audio.translations.create()`. For same-language transcription, use `audio.transcriptions.create()` instead. Translation only outputs English -- there is no way to translate to other languages.

```typescript
const translation = await client.audio.translations.create({
  model: "whisper-1",
  file: createReadStream(audioPath),
});
```

See [core.md](examples/core.md) for full translation examples including vocabulary prompting.

---

### Pattern 7: Speaker Diarization

Identify who is speaking in multi-speaker audio. Use `gpt-4o-transcribe-diarize` with `response_format: "diarized_json"` and `chunking_strategy: "auto"` (required for audio > 30s). Diarization does not support `prompt`, `logprobs`, or `timestamp_granularities`.

```typescript
const transcription = await client.audio.transcriptions.create({
  model: "gpt-4o-transcribe-diarize",
  file: createReadStream(audioPath),
  response_format: "diarized_json",
  chunking_strategy: "auto",
});
```

Optionally supply `known_speaker_names` and `known_speaker_references` (2-10 second audio clips as data URLs) to map segments to known speakers (up to 4). See [core.md](examples/core.md) for full diarization examples.

</patterns>

---

<decision_framework>

## Decision Framework

### Which Model to Choose

```
What do you need from the transcription?
+-- Just text (highest accuracy) -> gpt-4o-transcribe
+-- Just text (cost-sensitive) -> gpt-4o-mini-transcribe
+-- Word/segment timestamps -> whisper-1 (verbose_json)
+-- SRT or VTT subtitle files -> whisper-1 (srt or vtt)
+-- Speaker identification -> gpt-4o-transcribe-diarize
+-- Progressive/streaming output -> gpt-4o-transcribe (stream: true)
```

### Which Response Format to Use

```
What output do you need?
+-- Plain text string -> "text"
+-- JSON with text field -> "json" (default)
+-- Subtitles for video -> "srt" or "vtt" (whisper-1 only)
+-- Timestamps (word/segment) -> "verbose_json" (whisper-1 only)
+-- Speaker-labeled segments -> "diarized_json" (gpt-4o-transcribe-diarize only)
```

### Transcription vs Translation

```
Is the audio in English?
+-- YES -> Use audio.transcriptions.create()
+-- NO -> Do you want the output in the original language?
    +-- YES -> Use audio.transcriptions.create() (auto-detects language)
    +-- NO (want English) -> Use audio.translations.create() (whisper-1 only)
```

</decision_framework>

---

<red_flags>

## RED FLAGS

**High Priority Issues:**

- Using `timestamp_granularities` without `response_format: "verbose_json"` on `whisper-1` (silently ignored)
- Sending files larger than 25 MB (API returns error)
- Using `gpt-4o-transcribe-diarize` without `chunking_strategy` on audio > 30 seconds (API returns error)
- Using `stream: true` with `whisper-1` (not supported)

**Medium Priority Issues:**

- Using `whisper-1` when `gpt-4o-transcribe` would produce higher accuracy (whisper-1 has higher hallucination rates)
- Not passing `language` parameter when you know the language (auto-detection may be wrong for short or noisy audio)
- Using `audio.translations.create()` when you want same-language transcription (translation always outputs English)
- Splitting audio mid-sentence when chunking (loses context at boundaries)

**Common Mistakes:**

- Treating the `prompt` parameter as an instruction ("please transcribe carefully") -- it is context for vocabulary and style matching
- Using `gpt-4o-transcribe` when you need SRT/VTT output -- only `whisper-1` supports those formats
- Expecting `gpt-4o-transcribe-diarize` to support prompts or logprobs (it does not)
- Using the translations endpoint for English audio (it only translates non-English to English)
- Not providing previous chunk context when transcribing split files (reduces accuracy at boundaries)

**Gotchas & Edge Cases:**

- The `prompt` parameter is limited to approximately 224 tokens on `whisper-1`. Longer prompts are truncated.
- `whisper-1` can hallucinate text for silent or near-silent audio segments. Use `no_speech_prob` from `verbose_json` to detect this.
- `gpt-4o-transcribe` and `gpt-4o-mini-transcribe` only support `json` and `text` response formats -- not `srt`, `vtt`, or `verbose_json`.
- The `language` parameter uses ISO 639-1 codes (e.g., `"en"`, `"fr"`, `"ja"`). Setting it improves accuracy for short audio.
- Supported file formats: flac, mp3, mp4, mpeg, mpga, m4a, ogg, wav, webm. Other formats must be converted first.
- `gpt-4o-transcribe-diarize` labels speakers as "A", "B", "C" unless you provide `known_speaker_names` and `known_speaker_references` with short audio clips.
- Translation endpoint only supports `whisper-1` and only outputs English -- there is no way to translate to other languages via this API.
- Streaming transcription emits `transcript.text.delta` events with a `delta` string property, plus a final `transcript.text.done` event.

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST choose the correct model for the use case -- `gpt-4o-transcribe` for accuracy, `whisper-1` for timestamps/SRT/VTT output, `gpt-4o-transcribe-diarize` for speaker labels)**

**(You MUST chunk audio files larger than 25 MB before sending to the API -- the API rejects files exceeding this limit)**

**(You MUST pass `response_format: "verbose_json"` when using `timestamp_granularities` -- timestamps only work with this format on `whisper-1`)**

**(You MUST set `chunking_strategy: "auto"` when using `gpt-4o-transcribe-diarize` with audio longer than 30 seconds -- the API requires it)**

**Failure to follow these rules will produce failed API calls or degraded transcription quality.**

</critical_reminders>
