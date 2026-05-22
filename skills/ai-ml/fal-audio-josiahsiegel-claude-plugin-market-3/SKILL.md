---
name: fal-audio
description: Complete fal.ai audio system. PROACTIVELY activate for: (1) Whisper speech-to-text, (2) Transcription with timestamps, (3) Translation to English, (4) F5-TTS voice cloning, (5) ElevenLabs premium TTS, (6) Kokoro multi-language TTS, (7) XTTS open-source cloning, (8) Subtitle generation (SRT), (9) Audio file formats. Provides: STT/TTS endpoints, language codes, voice cloning setup, timestamp formatting. Ensures accurate transcription and natural speech synthesis.
---

## Quick Reference

| STT Model | Endpoint | Speed | Accuracy |
|-----------|----------|-------|----------|
| Whisper | `fal-ai/whisper` | Medium | Highest |
| Whisper Turbo | `fal-ai/whisper-turbo` | Fast | High |
| Whisper Large v3 | `fal-ai/whisper-large-v3` | Slow | Highest |

| TTS Model | Endpoint | Voice Clone | Quality |
|-----------|----------|-------------|---------|
| F5-TTS | `fal-ai/f5-tts` | Yes | High |
| ElevenLabs | `fal-ai/elevenlabs/tts` | Via API | Highest |
| Kokoro | `fal-ai/kokoro/american-english` | No | Good |
| XTTS | `fal-ai/xtts` | Yes | Good |

| Whisper Task | Use Case |
|--------------|----------|
| `transcribe` | Same language text |
| `translate` | Non-English → English |

| Whisper Parameter | Value |
|-------------------|-------|
| `chunk_level` | `"segment"` for timestamps |
| `language` | ISO code (e.g., `"en"`) |

## When to Use This Skill

Use for **audio processing**:
- Transcribing audio/video to text
- Generating subtitles with timestamps
- Translating speech to English
- Cloning voices from reference audio
- Generating natural speech from text

**Related skills:**
- For video with audio: see `fal-text-to-video`
- For API integration: see `fal-api-reference`
- For model comparison: see `fal-model-guide`

---

# fal.ai Audio Models

Complete reference for speech-to-text (STT) and text-to-speech (TTS) models on fal.ai.

## Speech-to-Text Models

### Whisper (OpenAI)
**Endpoint:** `fal-ai/whisper`
**Best For:** Accurate transcription and translation

The industry-standard speech recognition model with support for 99+ languages.

```typescript
import { fal } from "@fal-ai/client";

const result = await fal.subscribe("fal-ai/whisper", {
  input: {
    audio_url: "https://example.com/speech.mp3",
    task: "transcribe",
    language: "en",
    chunk_level: "segment"
  }
});

console.log(result.text);
console.log(result.chunks);  // With timestamps
```

```python
import fal_client

result = fal_client.subscribe(
    "fal-ai/whisper",
    arguments={
        "audio_url": "https://example.com/speech.mp3",
        "task": "transcribe",
        "language": "en",
        "chunk_level": "segment"
    }
)
print(result["text"])
for chunk in result["chunks"]:
    print(f"[{chunk['timestamp'][0]:.2f}-{chunk['timestamp'][1]:.2f}] {chunk['text']}")
```

**Whisper Parameters:**

| Parameter | Type | Values | Description |
|-----------|------|--------|-------------|
| `audio_url` | string | - | Audio file URL |
| `task` | string | "transcribe", "translate" | Transcribe or translate to English |
| `language` | string | ISO code | Source language (optional, auto-detected) |
| `chunk_level` | string | "segment" | Return timestamps |
| `version` | string | "3" | Whisper version |

**Response Structure:**

```typescript
interface WhisperOutput {
  text: string;  // Full transcription
  chunks?: Array<{
    text: string;
    timestamp: [number, number];  // [start, end] in seconds
  }>;
}
```

### Whisper Turbo
**Endpoint:** `fal-ai/whisper-turbo`
**Best For:** Fast transcription

```typescript
const result = await fal.subscribe("fal-ai/whisper-turbo", {
  input: {
    audio_url: "https://example.com/podcast.mp3",
    task: "transcribe"
  }
});
```

### Whisper Large v3
**Endpoint:** `fal-ai/whisper-large-v3`
**Best For:** Maximum accuracy

```typescript
const result = await fal.subscribe("fal-ai/whisper-large-v3", {
  input: {
    audio_url: "https://example.com/meeting.mp3",
    task: "transcribe",
    language: "en"
  }
});
```

### Whisper Usage Examples

**Transcription with Timestamps:**
```typescript
const result = await fal.subscribe("fal-ai/whisper", {
  input: {
    audio_url: audioUrl,
    task: "transcribe",
    chunk_level: "segment"
  }
});

// Format as SRT subtitles
result.chunks.forEach((chunk, i) => {
  const start = formatTime(chunk.timestamp[0]);
  const end = formatTime(chunk.timestamp[1]);
  console.log(`${i + 1}\n${start} --> ${end}\n${chunk.text}\n`);
});

function formatTime(seconds: number): string {
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  const s = Math.floor(seconds % 60);
  const ms = Math.floor((seconds % 1) * 1000);
  return `${h.toString().padStart(2, '0')}:${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')},${ms.toString().padStart(3, '0')}`;
}
```

**Translation (Non-English to English):**
```typescript
const result = await fal.subscribe("fal-ai/whisper", {
  input: {
    audio_url: "https://example.com/french-speech.mp3",
    task: "translate",  // Translates to English
    language: "fr"
  }
});

console.log(result.text);  // English translation
```

**Multi-Language Detection:**
```typescript
// Whisper auto-detects language if not specified
const result = await fal.subscribe("fal-ai/whisper", {
  input: {
    audio_url: "https://example.com/unknown-language.mp3",
    task: "transcribe"
    // language omitted - auto-detect
  }
});
```

## Text-to-Speech Models

### F5-TTS
**Endpoint:** `fal-ai/f5-tts`
**Best For:** Voice cloning from reference audio

```typescript
const result = await fal.subscribe("fal-ai/f5-tts", {
  input: {
    gen_text: "Hello! Welcome to our product demonstration. We're excited to show you what we've built.",
    ref_audio_url: "https://example.com/voice-sample.wav",
    ref_text: "This is a sample of my voice for cloning purposes.",
    model_type: "F5-TTS"
  }
});

console.log(result.audio_url);
```

```python
result = fal_client.subscribe(
    "fal-ai/f5-tts",
    arguments={
        "gen_text": "Hello! Welcome to our product.",
        "ref_audio_url": "https://example.com/voice-sample.wav",
        "ref_text": "This is a sample of my voice."
    }
)
print(result["audio_url"])
```

**F5-TTS Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `gen_text` | string | Text to synthesize |
| `ref_audio_url` | string | Reference voice audio URL |
| `ref_text` | string | Transcript of reference audio |
| `model_type` | string | "F5-TTS" or "E2-TTS" |
| `remove_silence` | boolean | Remove silence from output |

### ElevenLabs TTS
**Endpoint:** `fal-ai/elevenlabs/tts`
**Best For:** Premium voice quality

```typescript
const result = await fal.subscribe("fal-ai/elevenlabs/tts", {
  input: {
    text: "Welcome to fal.ai! Let me tell you about our amazing AI models.",
    voice_id: "21m00Tcm4TlvDq8ikWAM",  // ElevenLabs voice ID
    model_id: "eleven_multilingual_v2"
  }
});

console.log(result.audio.url);
```

**ElevenLabs Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `text` | string | Text to synthesize |
| `voice_id` | string | ElevenLabs voice ID |
| `model_id` | string | TTS model version |
| `stability` | number | Voice stability (0-1) |
| `similarity_boost` | number | Voice similarity (0-1) |

**ElevenLabs Voice IDs (examples):**
- `21m00Tcm4TlvDq8ikWAM` - Rachel (female)
- `AZnzlk1XvdvUeBnXmlld` - Domi (female)
- `EXAVITQu4vr4xnSDxMaL` - Bella (female)
- `ErXwobaYiN019PkySvjV` - Antoni (male)
- `VR6AewLTigWG4xSOukaG` - Arnold (male)

### Kokoro TTS
**Endpoint:** `fal-ai/kokoro/american-english`
**Best For:** Multi-language, natural sounding

```typescript
const result = await fal.subscribe("fal-ai/kokoro/american-english", {
  input: {
    text: "This is a test of the Kokoro text-to-speech system.",
    voice: "af_bella"  // Voice style
  }
});

console.log(result.audio.url);
```

**Kokoro Variants:**
- `fal-ai/kokoro/american-english` - American English
- `fal-ai/kokoro/british-english` - British English
- `fal-ai/kokoro/japanese` - Japanese
- `fal-ai/kokoro/mandarin` - Mandarin Chinese

**Kokoro Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `text` | string | Text to synthesize |
| `voice` | string | Voice style identifier |
| `speed` | number | Speech speed multiplier |

### XTTS (Coqui)
**Endpoint:** `fal-ai/xtts`
**Best For:** Open-source voice cloning

```typescript
const result = await fal.subscribe("fal-ai/xtts", {
  input: {
    text: "Hello, this is a cloned voice speaking.",
    audio_url: "https://example.com/voice-reference.wav",
    language: "en"
  }
});
```

**XTTS Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `text` | string | Text to synthesize |
| `audio_url` | string | Reference audio for cloning |
| `language` | string | Target language |

## Model Comparison

### Speech-to-Text

| Model | Speed | Accuracy | Languages | Best For |
|-------|-------|----------|-----------|----------|
| Whisper | Medium | Highest | 99+ | Accuracy critical |
| Whisper Turbo | Fast | High | 99+ | Speed needed |
| Whisper Large v3 | Slow | Highest | 99+ | Maximum quality |

### Text-to-Speech

| Model | Quality | Voice Clone | Languages | Best For |
|-------|---------|-------------|-----------|----------|
| F5-TTS | High | Yes | Multiple | Voice cloning |
| ElevenLabs | Highest | Via API | Many | Premium quality |
| Kokoro | Good | No | Multiple | Multi-language |
| XTTS | Good | Yes | 16 | Open-source |

## Workflow Examples

### Transcribe and Translate Pipeline

```typescript
async function processAudio(audioUrl: string, targetLanguage: string = 'en') {
  // 1. Transcribe
  const transcription = await fal.subscribe("fal-ai/whisper", {
    input: {
      audio_url: audioUrl,
      task: "transcribe",
      chunk_level: "segment"
    }
  });

  // 2. If not English, translate
  let translation = null;
  if (targetLanguage === 'en') {
    translation = await fal.subscribe("fal-ai/whisper", {
      input: {
        audio_url: audioUrl,
        task: "translate"
      }
    });
  }

  return {
    original: transcription.text,
    translated: translation?.text,
    chunks: transcription.chunks
  };
}
```

### Voice Cloning Pipeline

```typescript
async function cloneVoiceAndSpeak(
  referenceAudioUrl: string,
  referenceText: string,
  textToSpeak: string
) {
  // Use F5-TTS for voice cloning
  const result = await fal.subscribe("fal-ai/f5-tts", {
    input: {
      gen_text: textToSpeak,
      ref_audio_url: referenceAudioUrl,
      ref_text: referenceText,
      remove_silence: true
    }
  });

  return result.audio_url;
}
```

### Subtitle Generation

```typescript
async function generateSubtitles(videoUrl: string): Promise<string> {
  // Extract audio and transcribe
  const result = await fal.subscribe("fal-ai/whisper", {
    input: {
      audio_url: videoUrl,  // Works with video URLs too
      task: "transcribe",
      chunk_level: "segment"
    }
  });

  // Generate SRT format
  let srt = '';
  result.chunks.forEach((chunk, i) => {
    srt += `${i + 1}\n`;
    srt += `${formatSrtTime(chunk.timestamp[0])} --> ${formatSrtTime(chunk.timestamp[1])}\n`;
    srt += `${chunk.text}\n\n`;
  });

  return srt;
}

function formatSrtTime(seconds: number): string {
  const date = new Date(seconds * 1000);
  return date.toISOString().substr(11, 12).replace('.', ',');
}
```

### Audio Book Generation

```typescript
async function generateAudioBook(chapters: string[], voiceId: string) {
  const audioUrls = [];

  for (const chapter of chapters) {
    // Split into manageable chunks
    const chunks = splitText(chapter, 5000);

    for (const chunk of chunks) {
      const result = await fal.subscribe("fal-ai/elevenlabs/tts", {
        input: {
          text: chunk,
          voice_id: voiceId,
          model_id: "eleven_multilingual_v2"
        }
      });
      audioUrls.push(result.audio.url);
    }
  }

  return audioUrls;
}

function splitText(text: string, maxLength: number): string[] {
  const chunks = [];
  let current = '';

  text.split('. ').forEach(sentence => {
    if ((current + sentence).length < maxLength) {
      current += sentence + '. ';
    } else {
      chunks.push(current.trim());
      current = sentence + '. ';
    }
  });

  if (current) chunks.push(current.trim());
  return chunks;
}
```

## Parameter Reference

### Speech-to-Text Input

```typescript
interface STTInput {
  audio_url: string;
  task?: "transcribe" | "translate";
  language?: string;  // ISO 639-1 code
  chunk_level?: "segment";
  version?: string;
}
```

### Text-to-Speech Input

```typescript
interface TTSInput {
  // Common
  text?: string;
  gen_text?: string;

  // Voice cloning
  ref_audio_url?: string;
  ref_text?: string;
  audio_url?: string;  // XTTS

  // Voice selection
  voice_id?: string;  // ElevenLabs
  voice?: string;     // Kokoro
  model_type?: string; // F5-TTS

  // Control
  speed?: number;
  stability?: number;
  similarity_boost?: number;
  language?: string;
  remove_silence?: boolean;
}
```

## Best Practices

### Speech-to-Text

1. **Audio Quality**: Clean audio = better transcription
2. **Specify Language**: Provide language hint when known
3. **Use Timestamps**: Request `chunk_level: "segment"` for subtitles
4. **Handle Long Audio**: Whisper handles long files automatically
5. **Translation**: Use `task: "translate"` for non-English to English

### Text-to-Speech

1. **Reference Quality**: For voice cloning, use 10-30 second clear samples
2. **Reference Transcript**: Accurate transcript improves cloning quality
3. **Text Length**: Split very long text into chunks
4. **Punctuation**: Proper punctuation improves prosody
5. **Emotion Hints**: Use punctuation (!, ?) to convey emotion

### Common Supported Languages

| Language | Code | STT | TTS |
|----------|------|-----|-----|
| English | en | Yes | Yes |
| Spanish | es | Yes | Yes |
| French | fr | Yes | Yes |
| German | de | Yes | Yes |
| Italian | it | Yes | Yes |
| Portuguese | pt | Yes | Yes |
| Japanese | ja | Yes | Yes |
| Chinese | zh | Yes | Yes |
| Korean | ko | Yes | Yes |
| Russian | ru | Yes | Limited |

## File Format Support

### Input Formats (STT)

| Format | Extension | Supported |
|--------|-----------|-----------|
| MP3 | .mp3 | Yes |
| WAV | .wav | Yes |
| M4A | .m4a | Yes |
| FLAC | .flac | Yes |
| OGG | .ogg | Yes |
| WebM | .webm | Yes |
| Video | .mp4 | Yes (audio extracted) |

### Output Formats (TTS)

| Model | Output Format |
|-------|---------------|
| F5-TTS | WAV |
| ElevenLabs | MP3 |
| Kokoro | WAV |
| XTTS | WAV |

## Error Handling

```typescript
try {
  const result = await fal.subscribe("fal-ai/whisper", {
    input: { audio_url: audioUrl, task: "transcribe" }
  });
} catch (error) {
  if (error.status === 400) {
    console.error("Invalid audio file or URL");
  } else if (error.status === 413) {
    console.error("Audio file too large");
  } else {
    console.error("Transcription failed:", error.message);
  }
}
```
