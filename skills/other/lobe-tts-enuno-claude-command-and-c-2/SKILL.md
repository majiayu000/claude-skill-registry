---
name: lobe-tts
version: "1.0.0"
description: LobeTTS - High-quality TypeScript TTS/STT toolkit with EdgeSpeech, Microsoft, OpenAI engines, React hooks, audio visualization components, and both server and browser support
---

# LobeTTS Skill

**LobeTTS** (@lobehub/tts) is a high-quality TypeScript-based toolkit for text-to-speech (TTS) and speech-to-text (STT) functionality. It supports usage both on the server-side and in the browser, offering developers an open-source alternative to proprietary TTS solutions with quality comparable to OpenAI's TTS service.

**Key Value Proposition**: Generate high-quality speech with minimal code (~15 lines), supporting multiple TTS engines (Edge, Microsoft, OpenAI) with React hooks and audio visualization components for seamless frontend integration.

## When to Use This Skill

- Implementing text-to-speech in Node.js applications
- Adding speech synthesis to React/Next.js applications
- Building voice-enabled chatbots or assistants
- Creating audio players with visualization
- Implementing speech-to-text functionality
- Comparing or switching between TTS providers
- Building accessible applications with audio output

## When NOT to Use This Skill

- For native mobile TTS (use platform-specific APIs)
- For real-time voice streaming (use WebRTC solutions)
- For voice cloning or custom voice training
- For offline TTS without internet (Edge/Microsoft require connectivity)

---

## Core Concepts

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        @lobehub/tts                              │
│                    (TypeScript Library)                          │
└─────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│   TTS Core    │    │ React Hooks   │    │  Components   │
├───────────────┤    ├───────────────┤    ├───────────────┤
│ EdgeSpeechTTS │    │ useEdgeSpeech │    │ AudioPlayer   │
│ MicrosoftTTS  │    │ useMicrosoft  │    │ AudioVisualzr │
│ OpenAITTS     │    │ useOpenAITTS  │    │               │
│ OpenAISTT     │    │ useOpenAISTT  │    │               │
│ SpeechSynth   │    │ useTTS        │    │               │
└───────────────┘    └───────────────┘    └───────────────┘
        │                     │                     │
        ▼                     ▼                     ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│    Server     │    │   Browser     │    │   Styling     │
├───────────────┤    ├───────────────┤    ├───────────────┤
│ • Node.js     │    │ • React       │    │ • Waveforms   │
│ • Edge/Vercel │    │ • Next.js     │    │ • Progress    │
│ • File output │    │ • SPA         │    │ • Controls    │
└───────────────┘    └───────────────┘    └───────────────┘
```

### Project Statistics

| Metric | Value |
|--------|-------|
| GitHub Stars | 695+ |
| Forks | 93+ |
| Contributors | 13+ |
| Releases | 100+ |
| Dependents | ~1,500 projects |
| Primary Language | TypeScript (98.8%) |
| License | MIT |

### Supported TTS/STT Engines

| Engine | Type | Provider | Quality | Cost |
|--------|------|----------|---------|------|
| **EdgeSpeechTTS** | TTS | Microsoft Edge | High | Free |
| **MicrosoftTTS** | TTS | Azure Cognitive | Very High | Paid |
| **OpenAITTS** | TTS | OpenAI | Premium | Paid |
| **OpenAISTT** | STT | OpenAI Whisper | Premium | Paid |
| **SpeechSynthesisTTS** | TTS | Browser Native | Variable | Free |

---

## Installation

### Package Installation

```bash
# pnpm (recommended)
pnpm add @lobehub/tts

# bun
bun add @lobehub/tts

# npm
npm install @lobehub/tts

# yarn
yarn add @lobehub/tts
```

**Important**: This is an ESM-only package.

### Next.js Configuration

Add to `next.config.js`:

```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  transpilePackages: ['@lobehub/tts'],
};

module.exports = nextConfig;
```

### Node.js WebSocket Polyfill

For server-side usage, polyfill WebSocket:

```javascript
import WebSocket from 'ws';
global.WebSocket = WebSocket;
```

---

## Server-Side Usage

### EdgeSpeechTTS (Free, High Quality)

```typescript
import { EdgeSpeechTTS } from '@lobehub/tts';
import { Buffer } from 'buffer';
import fs from 'fs';
import path from 'path';

// Polyfill WebSocket for Node.js
import WebSocket from 'ws';
global.WebSocket = WebSocket;

// Initialize TTS engine
const tts = new EdgeSpeechTTS({ locale: 'en-US' });

// Create speech payload
const payload = {
  input: 'Hello! This is a speech demonstration using LobeTTS.',
  options: {
    voice: 'en-US-GuyNeural',
  },
};

// Generate speech
const response = await tts.create(payload);

// Save to file
const mp3Buffer = Buffer.from(await response.arrayBuffer());
const speechFile = path.resolve('./speech.mp3');
fs.writeFileSync(speechFile, mp3Buffer);

console.log(`Speech saved to: ${speechFile}`);
```

### MicrosoftTTS (Azure)

```typescript
import { MicrosoftSpeechTTS } from '@lobehub/tts';

const tts = new MicrosoftSpeechTTS({
  locale: 'en-US',
  subscriptionKey: process.env.AZURE_SPEECH_KEY,
  region: process.env.AZURE_SPEECH_REGION, // e.g., 'eastus'
});

const response = await tts.create({
  input: 'Premium quality speech from Azure.',
  options: {
    voice: 'en-US-JennyNeural',
    style: 'cheerful', // emotional style
    rate: '1.0',
    pitch: '0%',
  },
});
```

### OpenAI TTS

```typescript
import { OpenAITTS } from '@lobehub/tts';

const tts = new OpenAITTS({
  apiKey: process.env.OPENAI_API_KEY,
});

const response = await tts.create({
  input: 'OpenAI TTS provides natural-sounding speech.',
  options: {
    model: 'tts-1-hd', // 'tts-1' or 'tts-1-hd'
    voice: 'alloy',     // alloy, echo, fable, onyx, nova, shimmer
    speed: 1.0,         // 0.25 to 4.0
  },
});
```

### OpenAI STT (Speech-to-Text)

```typescript
import { OpenAISTT } from '@lobehub/tts';
import fs from 'fs';

const stt = new OpenAISTT({
  apiKey: process.env.OPENAI_API_KEY,
});

// From file
const audioBuffer = fs.readFileSync('./recording.mp3');
const result = await stt.create({
  file: audioBuffer,
  options: {
    model: 'whisper-1',
    language: 'en',
    response_format: 'json',
  },
});

console.log('Transcription:', result.text);
```

---

## API Routes (Next.js/Vercel)

### Edge Speech API Route

```typescript
// app/api/tts/edge/route.ts
import { EdgeSpeechTTS } from '@lobehub/tts';
import { NextRequest, NextResponse } from 'next/server';

export async function POST(req: NextRequest) {
  const { text, voice = 'en-US-GuyNeural' } = await req.json();

  const tts = new EdgeSpeechTTS({ locale: 'en-US' });

  const response = await tts.create({
    input: text,
    options: { voice },
  });

  const audioBuffer = await response.arrayBuffer();

  return new NextResponse(audioBuffer, {
    headers: {
      'Content-Type': 'audio/mpeg',
      'Content-Length': audioBuffer.byteLength.toString(),
    },
  });
}
```

### OpenAI TTS API Route

```typescript
// app/api/tts/openai/route.ts
import { OpenAITTS } from '@lobehub/tts';
import { NextRequest, NextResponse } from 'next/server';

export async function POST(req: NextRequest) {
  const { text, voice = 'alloy', model = 'tts-1' } = await req.json();

  const tts = new OpenAITTS({
    apiKey: process.env.OPENAI_API_KEY!,
  });

  const response = await tts.create({
    input: text,
    options: { voice, model },
  });

  const audioBuffer = await response.arrayBuffer();

  return new NextResponse(audioBuffer, {
    headers: {
      'Content-Type': 'audio/mpeg',
    },
  });
}
```

---

## React Components

### AudioPlayer Component

```tsx
import { AudioPlayer, useAudioPlayer } from '@lobehub/tts/react';

interface TTSPlayerProps {
  audioUrl: string;
}

export default function TTSPlayer({ audioUrl }: TTSPlayerProps) {
  const { ref, isLoading, ...audio } = useAudioPlayer(audioUrl);

  return (
    <AudioPlayer
      audio={audio}
      isLoading={isLoading}
      style={{ width: '100%' }}
    />
  );
}
```

### AudioVisualizer Component

```tsx
import { AudioPlayer, AudioVisualizer, useAudioPlayer } from '@lobehub/tts/react';
import { Flexbox } from 'react-layout-kit';

interface AudioPlayerWithVisualizerProps {
  url: string;
}

export default function AudioPlayerWithVisualizer({ url }: AudioPlayerWithVisualizerProps) {
  const { ref, isLoading, ...audio } = useAudioPlayer(url);

  return (
    <Flexbox align="center" gap={8}>
      <AudioPlayer
        audio={audio}
        isLoading={isLoading}
        style={{ width: '100%' }}
      />
      <AudioVisualizer
        audioRef={ref}
        isLoading={isLoading}
      />
    </Flexbox>
  );
}
```

### Complete TTS Component

```tsx
'use client';

import { useState } from 'react';
import { AudioPlayer, useAudioPlayer } from '@lobehub/tts/react';

export default function TextToSpeech() {
  const [text, setText] = useState('');
  const [audioUrl, setAudioUrl] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSpeak = async () => {
    setLoading(true);
    try {
      const response = await fetch('/api/tts/edge', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text }),
      });

      const blob = await response.blob();
      const url = URL.createObjectURL(blob);
      setAudioUrl(url);
    } finally {
      setLoading(false);
    }
  };

  const { ref, isLoading, ...audio } = useAudioPlayer(audioUrl || '');

  return (
    <div>
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Enter text to speak..."
        rows={4}
      />
      <button onClick={handleSpeak} disabled={loading || !text}>
        {loading ? 'Generating...' : 'Speak'}
      </button>
      {audioUrl && (
        <AudioPlayer
          audio={audio}
          isLoading={isLoading}
          style={{ width: '100%', marginTop: 16 }}
        />
      )}
    </div>
  );
}
```

---

## React Hooks

### useEdgeSpeech

```tsx
import { useEdgeSpeech } from '@lobehub/tts/react';

function EdgeSpeechComponent() {
  const { speak, stop, isLoading, error } = useEdgeSpeech({
    locale: 'en-US',
    voice: 'en-US-AriaNeural',
  });

  const handleSpeak = () => {
    speak('Hello from Edge Speech!');
  };

  return (
    <div>
      <button onClick={handleSpeak} disabled={isLoading}>
        {isLoading ? 'Speaking...' : 'Speak'}
      </button>
      <button onClick={stop}>Stop</button>
      {error && <p>Error: {error.message}</p>}
    </div>
  );
}
```

### useOpenAITTS

```tsx
import { useOpenAITTS } from '@lobehub/tts/react';

function OpenAITTSComponent() {
  const { speak, stop, isLoading, audioUrl } = useOpenAITTS({
    apiKey: process.env.NEXT_PUBLIC_OPENAI_API_KEY,
    voice: 'nova',
    model: 'tts-1-hd',
  });

  return (
    <div>
      <button onClick={() => speak('Hello from OpenAI!')}>
        Speak
      </button>
      {audioUrl && <audio src={audioUrl} controls autoPlay />}
    </div>
  );
}
```

### useOpenAISTT (Speech-to-Text)

```tsx
import { useOpenAISTT } from '@lobehub/tts/react';

function SpeechToTextComponent() {
  const {
    startRecording,
    stopRecording,
    isRecording,
    transcript,
    error
  } = useOpenAISTT({
    apiKey: process.env.NEXT_PUBLIC_OPENAI_API_KEY,
  });

  return (
    <div>
      <button onClick={isRecording ? stopRecording : startRecording}>
        {isRecording ? 'Stop Recording' : 'Start Recording'}
      </button>
      {transcript && <p>Transcript: {transcript}</p>}
      {error && <p>Error: {error.message}</p>}
    </div>
  );
}
```

### useAudioRecorder

```tsx
import { useAudioRecorder } from '@lobehub/tts/react';

function AudioRecorderComponent() {
  const {
    startRecording,
    stopRecording,
    isRecording,
    audioBlob,
    audioUrl,
    duration,
  } = useAudioRecorder();

  const handleSave = () => {
    if (audioBlob) {
      const a = document.createElement('a');
      a.href = audioUrl!;
      a.download = 'recording.webm';
      a.click();
    }
  };

  return (
    <div>
      <button onClick={isRecording ? stopRecording : startRecording}>
        {isRecording ? `Stop (${duration}s)` : 'Record'}
      </button>
      {audioUrl && (
        <>
          <audio src={audioUrl} controls />
          <button onClick={handleSave}>Download</button>
        </>
      )}
    </div>
  );
}
```

### useSpeechRecognition (Browser Native)

```tsx
import { useSpeechRecognition } from '@lobehub/tts/react';

function BrowserSTTComponent() {
  const {
    startListening,
    stopListening,
    isListening,
    transcript,
    isSupported,
  } = useSpeechRecognition({
    language: 'en-US',
    continuous: true,
  });

  if (!isSupported) {
    return <p>Speech recognition not supported in this browser.</p>;
  }

  return (
    <div>
      <button onClick={isListening ? stopListening : startListening}>
        {isListening ? 'Stop Listening' : 'Start Listening'}
      </button>
      <p>Transcript: {transcript}</p>
    </div>
  );
}
```

---

## Voice Options

### Edge Speech Voices (Free)

```typescript
// Popular English voices
const englishVoices = [
  'en-US-GuyNeural',      // Male, casual
  'en-US-AriaNeural',     // Female, friendly
  'en-US-JennyNeural',    // Female, assistant
  'en-US-DavisNeural',    // Male, deep
  'en-GB-SoniaNeural',    // Female, British
  'en-GB-RyanNeural',     // Male, British
  'en-AU-NatashaNeural',  // Female, Australian
];

// Other languages
const multilingualVoices = [
  'zh-CN-XiaoxiaoNeural', // Chinese, Female
  'ja-JP-NanamiNeural',   // Japanese, Female
  'de-DE-KatjaNeural',    // German, Female
  'fr-FR-DeniseNeural',   // French, Female
  'es-ES-ElviraNeural',   // Spanish, Female
  'ko-KR-SunHiNeural',    // Korean, Female
];
```

### OpenAI Voices

```typescript
const openaiVoices = [
  'alloy',   // Neutral, versatile
  'echo',    // Warm, conversational
  'fable',   // Expressive, storytelling
  'onyx',    // Deep, authoritative
  'nova',    // Friendly, energetic
  'shimmer', // Clear, professional
];
```

---

## Configuration Options

### EdgeSpeechTTS Options

```typescript
interface EdgeSpeechTTSOptions {
  locale: string;         // Language/region code
  pitch?: string;         // Pitch adjustment (-50% to +50%)
  rate?: string;          // Speed adjustment (0.5 to 2.0)
  volume?: string;        // Volume adjustment (0 to 100)
}

const tts = new EdgeSpeechTTS({
  locale: 'en-US',
});

const payload = {
  input: 'Text to speak',
  options: {
    voice: 'en-US-AriaNeural',
    pitch: '+5%',
    rate: '1.2',
    volume: '80',
  },
};
```

### MicrosoftTTS Options

```typescript
interface MicrosoftSpeechTTSOptions {
  locale: string;
  subscriptionKey: string;
  region: string;
}

interface MicrosoftSpeakOptions {
  voice: string;
  style?: string;        // cheerful, sad, angry, etc.
  styleDegree?: number;  // 0.01 to 2
  role?: string;         // Girl, Boy, etc.
  rate?: string;
  pitch?: string;
}
```

### OpenAI TTS Options

```typescript
interface OpenAITTSOptions {
  apiKey: string;
  baseUrl?: string;      // Custom API endpoint
}

interface OpenAISpeakOptions {
  model: 'tts-1' | 'tts-1-hd';
  voice: 'alloy' | 'echo' | 'fable' | 'onyx' | 'nova' | 'shimmer';
  speed?: number;        // 0.25 to 4.0
  response_format?: 'mp3' | 'opus' | 'aac' | 'flac';
}
```

---

## Streaming Support

### Stream TTS Response

```typescript
import { EdgeSpeechTTS } from '@lobehub/tts';

const tts = new EdgeSpeechTTS({ locale: 'en-US' });

// Get stream instead of buffer
const response = await tts.createStream({
  input: 'Long text to stream...',
  options: { voice: 'en-US-GuyNeural' },
});

// Process stream
const reader = response.body?.getReader();
if (reader) {
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    // Process chunk
    console.log('Received chunk:', value.length, 'bytes');
  }
}
```

---

## Error Handling

```typescript
import { EdgeSpeechTTS } from '@lobehub/tts';

async function generateSpeech(text: string) {
  try {
    const tts = new EdgeSpeechTTS({ locale: 'en-US' });

    const response = await tts.create({
      input: text,
      options: { voice: 'en-US-GuyNeural' },
    });

    return Buffer.from(await response.arrayBuffer());
  } catch (error) {
    if (error instanceof Error) {
      if (error.message.includes('WebSocket')) {
        console.error('WebSocket connection failed. Check network.');
      } else if (error.message.includes('voice')) {
        console.error('Invalid voice selection.');
      } else {
        console.error('TTS Error:', error.message);
      }
    }
    throw error;
  }
}
```

---

## Integration Examples

### With LobeChat

```typescript
// LobeTTS is used internally by LobeChat for voice features
import { EdgeSpeechTTS } from '@lobehub/tts';

// LobeChat voice assistant pattern
async function speakAssistantResponse(message: string) {
  const tts = new EdgeSpeechTTS({ locale: 'en-US' });
  const audio = await tts.create({
    input: message,
    options: { voice: 'en-US-AriaNeural' },
  });
  return audio;
}
```

### With AI Chatbot

```typescript
// Complete voice-enabled chatbot
import { useOpenAITTS, useOpenAISTT } from '@lobehub/tts/react';

function VoiceChatbot() {
  const { speak, isLoading: isSpeaking } = useOpenAITTS({
    apiKey: process.env.NEXT_PUBLIC_OPENAI_API_KEY!,
    voice: 'nova',
  });

  const {
    startRecording,
    stopRecording,
    isRecording,
    transcript,
  } = useOpenAISTT({
    apiKey: process.env.NEXT_PUBLIC_OPENAI_API_KEY!,
  });

  const handleChat = async () => {
    stopRecording();

    // Send transcript to AI
    const response = await fetch('/api/chat', {
      method: 'POST',
      body: JSON.stringify({ message: transcript }),
    });

    const { reply } = await response.json();

    // Speak AI response
    speak(reply);
  };

  return (
    <div>
      <button onClick={isRecording ? handleChat : startRecording}>
        {isRecording ? 'Send' : 'Record'}
      </button>
      {transcript && <p>You said: {transcript}</p>}
    </div>
  );
}
```

---

## Best Practices

### Performance

1. **Reuse TTS instances**: Create once, use multiple times
2. **Stream for long text**: Use streaming for text >500 characters
3. **Cache audio**: Store generated audio to avoid regeneration
4. **Preload voices**: Initialize TTS early in app lifecycle

### Quality

1. **Choose appropriate voice**: Match voice to content tone
2. **Use HD models**: OpenAI tts-1-hd for critical content
3. **Add SSML**: For precise pronunciation control
4. **Test across browsers**: Verify audio playback compatibility

### Cost Optimization

1. **Use Edge TTS**: Free and high quality for most use cases
2. **Batch requests**: Combine short texts when possible
3. **Implement caching**: Hash text → cached audio
4. **Rate limit**: Prevent abuse in production

---

## Troubleshooting

### "WebSocket is not defined"

```typescript
// Add to Node.js entry point
import WebSocket from 'ws';
global.WebSocket = WebSocket;
```

### "Module not found: @lobehub/tts"

```javascript
// next.config.js
module.exports = {
  transpilePackages: ['@lobehub/tts'],
};
```

### Audio not playing in browser

```typescript
// Ensure user interaction before playing
document.addEventListener('click', () => {
  audio.play();
}, { once: true });
```

### CORS errors with API routes

```typescript
// Add CORS headers
return new NextResponse(audioBuffer, {
  headers: {
    'Content-Type': 'audio/mpeg',
    'Access-Control-Allow-Origin': '*',
  },
});
```

---

## Resources

### Official Links

- **GitHub**: https://github.com/lobehub/lobe-tts
- **npm**: https://www.npmjs.com/package/@lobehub/tts
- **License**: MIT

### Related LobeHub Projects

- **LobeChat**: Extensible chatbot framework
- **LobeUI**: Component library for AI apps
- **LobeIcons**: AI/LLM brand logos
- **Lobei18n**: Internationalization tool

### Voice Resources

- [Microsoft Edge TTS Voices](https://docs.microsoft.com/azure/cognitive-services/speech-service/language-support)
- [OpenAI TTS Documentation](https://platform.openai.com/docs/guides/text-to-speech)

---

## Version History

- **Current**: 100+ releases on npm
- **Tech Stack**: TypeScript, React, ESM
- **License**: MIT © 2023 LobeHub

---

**Last Updated**: 2026-01-13
**Skill Version**: 1.0.0
**Source**: https://github.com/lobehub/lobe-tts
