---
name: audio-language-models
description: Gemini Live API, Grok Voice Agent, GPT-4o-Transcribe, AssemblyAI patterns for real-time voice, speech-to-text, and TTS. Use when implementing voice agents, audio transcription, or conversational AI.
context: fork
agent: multimodal-specialist
version: 1.1.0
author: SkillForge
user-invocable: false
tags: [audio, multimodal, gemini-live, grok-voice, whisper, tts, speech, voice-agent, 2026]
---

# Audio Language Models (2026)

Build real-time voice agents and audio processing using the latest native speech-to-speech models.

## When to Use

- Real-time voice assistants and agents
- Live conversational AI (phone agents, support bots)
- Audio transcription with speaker diarization
- Multilingual voice interactions
- Text-to-speech generation
- Voice-to-voice translation

## Model Comparison (January 2026)

### Real-Time Voice (Speech-to-Speech)

| Model | Latency | Languages | Price | Best For |
|-------|---------|-----------|-------|----------|
| **Grok Voice Agent** | <1s TTFA | 100+ | $0.05/min | Fastest, #1 Big Bench |
| **Gemini Live API** | Low | 24 (30 voices) | Usage-based | Emotional awareness |
| **OpenAI Realtime** | ~1s | 50+ | $0.10/min | Ecosystem integration |

### Speech-to-Text Only

| Model | WER | Latency | Best For |
|-------|-----|---------|----------|
| **Gemini 2.5 Pro** | ~5% | Medium | 9.5hr audio, diarization |
| **GPT-4o-Transcribe** | ~7% | Medium | Accuracy + accents |
| **AssemblyAI Universal-2** | 8.4% | 200ms | Best features |
| **Deepgram Nova-3** | ~18% | <300ms | Lowest latency |
| **Whisper Large V3** | 7.4% | Slow | Self-host, 99+ langs |

## Grok Voice Agent API (xAI) - Fastest

```python
import asyncio
import websockets
import json

async def grok_voice_agent():
    """Real-time voice agent with Grok - #1 on Big Bench Audio.

    Features:
    - <1 second time-to-first-audio (5x faster than competitors)
    - Native speech-to-speech (no transcription intermediary)
    - 100+ languages, $0.05/min
    - OpenAI Realtime API compatible
    """
    uri = "wss://api.x.ai/v1/realtime"
    headers = {"Authorization": f"Bearer {XAI_API_KEY}"}

    async with websockets.connect(uri, extra_headers=headers) as ws:
        # Configure session
        await ws.send(json.dumps({
            "type": "session.update",
            "session": {
                "model": "grok-4-voice",
                "voice": "Aria",  # or "Eve", "Leo"
                "instructions": "You are a helpful voice assistant.",
                "input_audio_format": "pcm16",
                "output_audio_format": "pcm16",
                "turn_detection": {"type": "server_vad"}
            }
        }))

        # Stream audio in/out
        async def send_audio(audio_stream):
            async for chunk in audio_stream:
                await ws.send(json.dumps({
                    "type": "input_audio_buffer.append",
                    "audio": base64.b64encode(chunk).decode()
                }))

        async def receive_audio():
            async for message in ws:
                data = json.loads(message)
                if data["type"] == "response.audio.delta":
                    yield base64.b64decode(data["delta"])

        return send_audio, receive_audio

# Expressive voice with auditory cues
async def expressive_response(ws, text: str):
    """Use auditory cues for natural speech."""
    # Supports: [whisper], [sigh], [laugh], [pause]
    await ws.send(json.dumps({
        "type": "response.create",
        "response": {
            "instructions": "[sigh] Let me think about that... [pause] Here's what I found."
        }
    }))
```

## Gemini Live API (Google) - Emotional Awareness

```python
import google.generativeai as genai
from google.generativeai import live

genai.configure(api_key="YOUR_API_KEY")

async def gemini_live_voice():
    """Real-time voice with emotional understanding.

    Features:
    - 30 HD voices in 24 languages
    - Affective dialog (understands emotions)
    - Barge-in support (interrupt anytime)
    - Proactive audio (responds only when relevant)
    """
    model = genai.GenerativeModel("gemini-2.5-flash-live")

    config = live.LiveConnectConfig(
        response_modalities=["AUDIO"],
        speech_config=live.SpeechConfig(
            voice_config=live.VoiceConfig(
                prebuilt_voice_config=live.PrebuiltVoiceConfig(
                    voice_name="Puck"  # or Charon, Kore, Fenrir, Aoede
                )
            )
        ),
        system_instruction="You are a friendly voice assistant."
    )

    async with model.connect(config=config) as session:
        # Send audio
        async def send_audio(audio_chunk: bytes):
            await session.send(
                input=live.LiveClientContent(
                    realtime_input=live.RealtimeInput(
                        media_chunks=[live.MediaChunk(
                            data=audio_chunk,
                            mime_type="audio/pcm"
                        )]
                    )
                )
            )

        # Receive audio responses
        async for response in session.receive():
            if response.data:
                yield response.data  # Audio bytes

# With transcription
async def gemini_live_with_transcript():
    """Get both audio and text transcripts."""
    async with model.connect(config=config) as session:
        async for response in session.receive():
            if response.server_content:
                # Text transcript
                if response.server_content.model_turn:
                    for part in response.server_content.model_turn.parts:
                        if part.text:
                            print(f"Transcript: {part.text}")
            if response.data:
                yield response.data  # Audio
```

## Gemini Audio Transcription (Long-Form)

```python
import google.generativeai as genai

def transcribe_with_gemini(audio_path: str) -> dict:
    """Transcribe up to 9.5 hours of audio with speaker diarization.

    Gemini 2.5 Pro handles long-form audio natively.
    """
    model = genai.GenerativeModel("gemini-2.5-pro")

    # Upload audio file
    audio_file = genai.upload_file(audio_path)

    response = model.generate_content([
        audio_file,
        """Transcribe this audio with:
        1. Speaker labels (Speaker 1, Speaker 2, etc.)
        2. Timestamps for each segment
        3. Punctuation and formatting

        Format:
        [00:00:00] Speaker 1: First statement...
        [00:00:15] Speaker 2: Response..."""
    ])

    return {
        "transcript": response.text,
        "audio_duration": audio_file.duration
    }
```

## Gemini TTS (Text-to-Speech)

```python
def gemini_text_to_speech(text: str, voice: str = "Kore") -> bytes:
    """Generate speech with Gemini 2.5 TTS.

    Features:
    - Enhanced expressivity with style prompts
    - Precision pacing (context-aware speed)
    - Multi-speaker dialogue consistency
    """
    model = genai.GenerativeModel("gemini-2.5-flash-tts")

    response = model.generate_content(
        contents=text,
        generation_config=genai.GenerationConfig(
            response_mime_type="audio/mp3",
            speech_config=genai.SpeechConfig(
                voice_config=genai.VoiceConfig(
                    prebuilt_voice_config=genai.PrebuiltVoiceConfig(
                        voice_name=voice  # Puck, Charon, Kore, Fenrir, Aoede
                    )
                )
            )
        )
    )

    return response.audio
```

## OpenAI GPT-4o-Transcribe

```python
from openai import OpenAI

client = OpenAI()

def transcribe_openai(audio_path: str, language: str = None) -> dict:
    """Transcribe with GPT-4o-Transcribe (enhanced accuracy)."""
    with open(audio_path, "rb") as audio_file:
        response = client.audio.transcriptions.create(
            model="gpt-4o-transcribe",
            file=audio_file,
            language=language,
            response_format="verbose_json",
            timestamp_granularities=["word", "segment"]
        )
    return {
        "text": response.text,
        "words": response.words,
        "segments": response.segments,
        "duration": response.duration
    }
```

## AssemblyAI (Best Features)

```python
import assemblyai as aai

aai.settings.api_key = "YOUR_API_KEY"

def transcribe_assemblyai(audio_url: str) -> dict:
    """Transcribe with speaker diarization, sentiment, entities."""
    config = aai.TranscriptionConfig(
        speaker_labels=True,
        sentiment_analysis=True,
        entity_detection=True,
        auto_highlights=True,
        language_detection=True
    )

    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_url, config=config)

    return {
        "text": transcript.text,
        "speakers": transcript.utterances,
        "sentiment": transcript.sentiment_analysis,
        "entities": transcript.entities
    }
```

## Real-Time Streaming Comparison

```python
async def choose_realtime_provider(
    requirements: dict
) -> str:
    """Select best real-time voice provider."""

    if requirements.get("fastest_latency"):
        return "grok"  # <1s TTFA, 5x faster

    if requirements.get("emotional_understanding"):
        return "gemini"  # Affective dialog

    if requirements.get("openai_ecosystem"):
        return "openai"  # Compatible tools

    if requirements.get("lowest_cost"):
        return "grok"  # $0.05/min (half of OpenAI)

    return "gemini"  # Best overall for 2026
```

## API Pricing (January 2026)

| Provider | Type | Price | Notes |
|----------|------|-------|-------|
| Grok Voice Agent | Real-time | $0.05/min | Cheapest real-time |
| Gemini Live | Real-time | Usage-based | 30 HD voices |
| OpenAI Realtime | Real-time | $0.10/min | |
| Gemini 2.5 Pro | Transcription | $1.25/M tokens | 9.5hr audio |
| GPT-4o-Transcribe | Transcription | $0.01/min | |
| AssemblyAI | Transcription | ~$0.15/hr | Best features |
| Deepgram | Transcription | ~$0.0043/min | |

## Key Decisions

| Scenario | Recommendation |
|----------|----------------|
| Voice assistant | Grok Voice Agent (fastest) |
| Emotional AI | Gemini Live API |
| Long audio (hours) | Gemini 2.5 Pro (9.5hr) |
| Speaker diarization | AssemblyAI or Gemini |
| Lowest latency STT | Deepgram Nova-3 |
| Self-hosted | Whisper Large V3 |

## Common Mistakes

- Using STT+LLM+TTS pipeline instead of native speech-to-speech
- Not leveraging emotional understanding (Gemini)
- Ignoring barge-in support for natural conversations
- Using deprecated Whisper-1 instead of GPT-4o-Transcribe
- Not testing latency with real users

## Related Skills

- `vision-language-models` - Image/video processing
- `multimodal-rag` - Audio + text retrieval
- `streaming-api-patterns` - WebSocket patterns

## Capability Details

### real-time-voice
**Keywords:** voice agent, real-time, conversational, live audio
**Solves:**
- Build voice assistants
- Phone agents and support bots
- Interactive voice response (IVR)

### speech-to-speech
**Keywords:** native audio, speech-to-speech, no transcription
**Solves:**
- Low-latency voice responses
- Natural conversation flow
- Emotional voice interactions

### transcription
**Keywords:** transcribe, speech-to-text, STT, convert audio
**Solves:**
- Convert audio files to text
- Generate meeting transcripts
- Process long-form audio

### voice-tts
**Keywords:** TTS, text-to-speech, voice synthesis
**Solves:**
- Generate natural speech
- Multi-voice dialogue
- Expressive audio output
