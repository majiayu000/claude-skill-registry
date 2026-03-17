---
name: "voice-ai"
description: "Production voice AI agents with sub-500ms latency. Groq LLM, Deepgram STT, Cartesia TTS, Twilio integration. No OpenAI. Use when: voice agent, phone bot, STT, TTS, Deepgram, Cartesia, Twilio, voice AI, speech to text, IVR, call center, voice latency."
---

<objective>
Build production voice AI agents with sub-500ms latency:

1. **STT** - Deepgram Nova-3 streaming transcription (~150ms)
2. **LLM** - Groq llama-3.1-8b-instant for fastest inference (~220ms)
3. **TTS** - Cartesia Sonic for ultra-realistic voice (~90ms)
4. **Telephony** - Twilio Media Streams for real-time bidirectional audio

**CRITICAL: NO OPENAI - Never use `from openai import OpenAI`**

Key deliverables:
- Streaming STT with voice activity detection
- Low-latency LLM responses optimized for voice
- Expressive TTS with emotion controls
- Twilio Media Streams WebSocket handler
</objective>

<quick_start>
**Minimal Voice Pipeline (~50 lines, <500ms):**
```python
import os
import asyncio
from groq import AsyncGroq
from deepgram import AsyncDeepgramClient
from cartesia import AsyncCartesia

# NEVER: from openai import OpenAI

async def voice_pipeline(user_audio: bytes) -> bytes:
    """Process audio input, return audio response."""

    # 1. STT: Deepgram Nova-3 (~150ms)
    dg = AsyncDeepgramClient(api_key=os.getenv("DEEPGRAM_API_KEY"))
    result = await dg.listen.rest.v1.transcribe(
        {"buffer": user_audio, "mimetype": "audio/wav"},
        {"model": "nova-3", "language": "en-US"}
    )
    user_text = result.results.channels[0].alternatives[0].transcript

    # 2. LLM: Groq (~220ms) - NOT OpenAI
    groq = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))
    response = await groq.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "Keep responses under 2 sentences."},
            {"role": "user", "content": user_text}
        ],
        max_tokens=150
    )
    response_text = response.choices[0].message.content

    # 3. TTS: Cartesia Sonic-2 (~90ms)
    cartesia = AsyncCartesia(api_key=os.getenv("CARTESIA_API_KEY"))
    audio_chunks = []
    for chunk in cartesia.tts.sse(
        model_id="sonic-2",
        transcript=response_text,
        voice={"id": "f9836c6e-a0bd-460e-9d3c-f7299fa60f94"},
        output_format={"container": "raw", "encoding": "pcm_s16le", "sample_rate": 8000}
    ):
        if chunk.audio:
            audio_chunks.append(chunk.audio)

    return b"".join(audio_chunks)  # Total: ~460ms
```
</quick_start>

<success_criteria>
A voice AI agent is successful when:
- Total latency is under 500ms (STT + LLM + TTS)
- STT correctly transcribes with utterance end detection
- TTS sounds natural and conversational
- Barge-in (interruption) works smoothly (Enterprise tier)
- Bilingual support handles language switching
</success_criteria>

<optimal_stack>
## VozLux-Tested Stack

| Component | Provider | Model | Latency | Notes |
|-----------|----------|-------|---------|-------|
| **STT** | Deepgram | Nova-3 | ~150ms | Streaming, VAD, utterance detection |
| **LLM** | Groq | llama-3.1-8b-instant | ~220ms | LPU hardware, fastest inference |
| **TTS** | Cartesia | Sonic-2 | ~90ms | Streaming, emotions, bilingual |
| **TOTAL** | - | - | **~460ms** | Sub-500ms target achieved |

### LLM Priority (Never OpenAI)
```python
LLM_PRIORITY = [
    ("groq", "GROQ_API_KEY", "~220ms"),      # Primary
    ("cerebras", "CEREBRAS_API_KEY", "~200ms"),  # Fallback
    ("anthropic", "ANTHROPIC_API_KEY", "~500ms"),  # Quality fallback
]
# NEVER: from openai import OpenAI
```

### Tier Architecture
| Tier | Latency | STT | LLM | TTS | Features |
|------|---------|-----|-----|-----|----------|
| Free | 3000ms | TwiML Gather | Groq | Polly | Basic IVR |
| Pro | 600ms | Deepgram Nova | Groq | Cartesia | Media Streams |
| Enterprise | 400ms | Deepgram + VAD | Groq | Cartesia | Barge-in |
</optimal_stack>

<deepgram_stt>
## Deepgram STT (v5 SDK)

### Streaming WebSocket Pattern
```python
from deepgram import AsyncDeepgramClient
from deepgram.core.events import EventType
from deepgram.extensions.types.sockets import (
    ListenV1SocketClientResponse,
    ListenV1MediaMessage,
    ListenV1ControlMessage
)

async def streaming_stt():
    client = AsyncDeepgramClient(api_key=os.getenv("DEEPGRAM_API_KEY"))

    async with client.listen.v1.connect(model="nova-3") as connection:
        def on_message(message: ListenV1SocketClientResponse):
            msg_type = getattr(message, "type", None)

            if msg_type == "Results":
                channel = getattr(message, "channel", None)
                if channel and channel.alternatives:
                    text = channel.alternatives[0].transcript
                    is_final = getattr(message, "is_final", False)
                    if text:
                        print(f"{'[FINAL]' if is_final else '[INTERIM]'} {text}")

            elif msg_type == "UtteranceEnd":
                print("[USER FINISHED SPEAKING]")

            elif msg_type == "SpeechStarted":
                print("[USER STARTED SPEAKING - barge-in trigger]")

        connection.on(EventType.MESSAGE, on_message)
        await connection.start_listening()

        # Send audio chunks
        await connection.send_media(ListenV1MediaMessage(data=audio_bytes))

        # Keep alive for long sessions
        await connection.send_control(ListenV1ControlMessage(type="KeepAlive"))
```

### Connection Options
```python
options = {
    "model": "nova-3",
    "language": "en-US",
    "encoding": "mulaw",      # Twilio format
    "sample_rate": 8000,      # Telephony standard
    "interim_results": True,   # Get partial transcripts
    "utterance_end_ms": 1000,  # Silence to end utterance
    "vad_events": True,        # Voice activity detection
}
```

> See `reference/deepgram-setup.md` for full streaming setup.
</deepgram_stt>

<groq_llm>
## Groq LLM (Fastest Inference)

### Voice-Optimized Pattern
```python
from groq import AsyncGroq

class GroqVoiceLLM:
    def __init__(self, model: str = "llama-3.1-8b-instant"):
        self.client = AsyncGroq()
        self.model = model
        self.system_prompt = (
            "You are a helpful voice assistant. "
            "Keep responses to 2-3 sentences max. "
            "Speak naturally as if on a phone call."
        )

    async def generate_stream(self, user_input: str):
        """Streaming for lowest TTFB."""
        stream = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_input}
            ],
            max_tokens=150,
            temperature=0.7,
            stream=True,
        )

        async for chunk in stream:
            content = chunk.choices[0].delta.content
            if content:
                yield content  # Pipe to TTS immediately
```

### Model Selection
| Model | Speed | Quality | Use Case |
|-------|-------|---------|----------|
| llama-3.1-8b-instant | ~220ms | Good | Primary voice |
| llama-3.3-70b-versatile | ~500ms | Best | Complex queries |
| mixtral-8x7b-32768 | ~300ms | Good | Long context |

> See `reference/groq-voice-llm.md` for context management.
</groq_llm>

<cartesia_tts>
## Cartesia TTS (Sonic-2)

### Streaming Pattern
```python
from cartesia import AsyncCartesia

class CartesiaTTS:
    VOICES = {
        "en": "f9836c6e-a0bd-460e-9d3c-f7299fa60f94",  # Warm female
        "es": "5c5ad5e7-1020-476b-8b91-fdcbe9cc313c",  # Mexican Spanish
    }

    EMOTIONS = {
        "greeting": "excited",
        "confirmation": "grateful",
        "info": "calm",
        "complaint": "sympathetic",
        "apology": "apologetic",
    }

    def __init__(self, api_key: str):
        self.client = AsyncCartesia(api_key=api_key)

    async def synthesize_stream(
        self,
        text: str,
        language: str = "en",
        emotion: str = "neutral"
    ):
        voice_id = self.VOICES.get(language, self.VOICES["en"])

        response = self.client.tts.sse(
            model_id="sonic-2",
            transcript=text,
            voice={
                "id": voice_id,
                "experimental_controls": {
                    "speed": "normal",
                    "emotion": [emotion] if emotion != "neutral" else []
                }
            },
            language=language,
            output_format={
                "container": "raw",
                "encoding": "pcm_s16le",
                "sample_rate": 8000,  # Telephony
            },
        )

        for chunk in response:
            if chunk.audio:
                yield chunk.audio
```

### With Timestamps
```python
response = client.tts.sse(
    model_id="sonic-2",
    transcript="Hello, world!",
    voice={"id": voice_id},
    output_format={"container": "raw", "encoding": "pcm_f32le", "sample_rate": 44100},
    add_timestamps=True,
)

for chunk in response:
    if chunk.word_timestamps:
        for word, start, end in zip(
            chunk.word_timestamps.words,
            chunk.word_timestamps.start,
            chunk.word_timestamps.end
        ):
            print(f"'{word}': {start:.2f}s - {end:.2f}s")
```

> See `reference/cartesia-tts.md` for all 57 emotions.
</cartesia_tts>

<twilio_media_streams>
## Twilio Media Streams

### WebSocket Handler (FastAPI)
```python
from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import Response
from twilio.twiml.voice_response import VoiceResponse, Connect, Stream
import json, base64, audioop

app = FastAPI()

@app.post("/voice/incoming")
async def incoming_call(request: Request):
    """Route to Media Streams WebSocket."""
    form = await request.form()
    caller = form.get("From", "")
    lang = "es" if caller.startswith("+52") else "en"

    response = VoiceResponse()
    connect = Connect()
    connect.append(Stream(url=f"wss://your-app.com/voice/stream?lang={lang}"))
    response.append(connect)

    return Response(content=str(response), media_type="application/xml")

@app.websocket("/voice/stream")
async def media_stream(websocket: WebSocket, lang: str = "en"):
    await websocket.accept()
    stream_sid = None

    while True:
        message = await websocket.receive_text()
        data = json.loads(message)

        if data["event"] == "start":
            stream_sid = data["start"]["streamSid"]
            # Initialize STT, send greeting

        elif data["event"] == "media":
            audio = base64.b64decode(data["media"]["payload"])
            # Send to Deepgram STT

        elif data["event"] == "stop":
            break

async def send_audio(websocket, stream_sid: str, pcm_audio: bytes):
    """Convert PCM to mu-law and send to Twilio."""
    mulaw = audioop.lin2ulaw(pcm_audio, 2)
    await websocket.send_text(json.dumps({
        "event": "media",
        "streamSid": stream_sid,
        "media": {"payload": base64.b64encode(mulaw).decode()}
    }))
```

> See `reference/twilio-webhooks.md` for complete handler.
</twilio_media_streams>

<bilingual_support>
## Bilingual Support (EN/ES)

### Auto-Detection
```python
def detect_language(caller_number: str) -> str:
    if caller_number.startswith("+52"):
        return "es"  # Mexico
    elif caller_number.startswith("+1"):
        return "en"  # US/Canada
    return "es"  # Default Spanish
```

### Voice Prompts
```python
GREETINGS = {
    "en": "Hello! How can I help you today?",
    "es": "Hola! En que puedo ayudarle hoy?",  # Use "usted" for respect
}
```
</bilingual_support>

<voice_prompts>
## Voice Prompt Engineering

```python
VOICE_PROMPT = """
# Role
You are a bilingual voice assistant for {business_name}.

# Tone
- 2-3 sentences max for phone clarity
- NEVER use bullet points, lists, or markdown
- Spell out emails: "john at company dot com"
- Phone numbers with pauses: "five one two... eight seven seven..."
- Spanish: Use "usted" for formal respect

# Guardrails
- Never make up information
- Transfer to human after 3 failed attempts
- Match caller's language

# Error Recovery
English: "I want to make sure I got that right. Did you say [repeat]?"
Spanish: "Quiero asegurarme de entender bien. Dijo [repetir]?"
"""
```

> See `reference/voice-prompts.md` for full template.
</voice_prompts>

<file_locations>
## Reference Files

- `reference/deepgram-setup.md` - Full streaming STT setup
- `reference/groq-voice-llm.md` - Groq patterns for voice
- `reference/cartesia-tts.md` - All 57 emotions, voice cloning
- `reference/twilio-webhooks.md` - Complete Media Streams handler
- `reference/latency-optimization.md` - Sub-500ms techniques
- `reference/voice-prompts.md` - Voice-optimized prompts
</file_locations>

<routing>
## Request Routing

**User wants voice agent:**
→ Provide full stack (Deepgram + Groq + Cartesia + Twilio)
→ Start with quick_start pipeline

**User wants STT only:**
→ Provide Deepgram streaming pattern
→ Reference: `reference/deepgram-setup.md`

**User wants TTS only:**
→ Provide Cartesia pattern with emotions
→ Reference: `reference/cartesia-tts.md`

**User wants latency optimization:**
→ Audit current stack, identify bottlenecks
→ Reference: `reference/latency-optimization.md`

**User mentions OpenAI:**
→ REDIRECT to Groq immediately
→ Explain: "NO OPENAI - Use Groq for lowest latency"
</routing>

<env_setup>
## Environment Variables

```bash
# Required (NEVER OpenAI)
DEEPGRAM_API_KEY=your_key
GROQ_API_KEY=gsk_xxxx
CARTESIA_API_KEY=your_key

# Twilio
TWILIO_ACCOUNT_SID=ACxxxx
TWILIO_AUTH_TOKEN=your_token
TWILIO_PHONE_NUMBER=+15551234567

# Fallbacks
ANTHROPIC_API_KEY=sk-ant-xxxx
CEREBRAS_API_KEY=csk_xxxx
```

```bash
pip install deepgram-sdk groq cartesia twilio fastapi
```
</env_setup>

<quick_reference>
## Quick Reference Card

```
STACK:
  STT: Deepgram Nova-3 (~150ms)
  LLM: Groq llama-3.1-8b-instant (~220ms) - NOT OPENAI
  TTS: Cartesia Sonic-2 (~90ms)

LATENCY TARGETS:
  Pro: 600ms (Media Streams)
  Enterprise: 400ms (Full streaming + barge-in)

BILINGUAL:
  +52 -> Spanish (es)
  +1 -> English (en)
  Default -> Spanish

EMOTIONS (Cartesia):
  greeting -> excited
  confirmation -> grateful
  complaint -> sympathetic
```
</quick_reference>
