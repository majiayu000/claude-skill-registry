---
name: faion-audio-skill
user-invocable: false
description: ""
---

# Audio/Speech Processing Skill

**Comprehensive guide for text-to-speech, speech-to-text, voice cloning, and voice agent development**

---

## Quick Reference

**When to use this skill:**
- Text-to-speech synthesis (TTS)
- Speech-to-text transcription (STT)
- Voice cloning and voice design
- Real-time voice agents
- Audio transcription with speaker diarization
- Podcast/content production

---

## TTS Service Comparison

| Service | Latency | Quality | Voices | Price/1k chars | Best For |
|---------|---------|---------|--------|----------------|----------|
| **ElevenLabs** | ~200ms | Excellent | 1000+ | $0.30 | Quality, voice cloning |
| **OpenAI TTS** | ~300ms | Very Good | 6 | $0.015 | Simple, cheap |
| **Azure Speech** | ~150ms | Very Good | 400+ | $0.016 | Enterprise, SSML |
| **Cartesia Sonic** | ~75ms | Good | 100+ | $0.04 | Ultra-low latency |
| **Google Cloud TTS** | ~200ms | Very Good | 220+ | $0.016 | Multilingual |
| **Amazon Polly** | ~150ms | Good | 60+ | $0.016 | AWS integration |

---

## STT Service Comparison

| Service | Latency | WER | Languages | Price/min | Best For |
|---------|---------|-----|-----------|-----------|----------|
| **OpenAI Whisper** | ~320ms | ~10% | 100+ | $0.006 | Batch, multilingual |
| **Deepgram Nova-3** | ~200ms | ~8% | 30+ | $0.0059 | Real-time, voice agents |
| **AssemblyAI** | ~300ms | ~5% | 20+ | $0.015 | Accuracy, features |
| **ElevenLabs Scribe** | ~250ms | ~3.5% | 32 | $0.10 | Highest accuracy |
| **Azure Speech** | ~200ms | ~8% | 100+ | $0.016 | Enterprise |
| **Google STT** | ~200ms | ~9% | 125+ | $0.016 | Multilingual |
| **AWS Transcribe** | ~300ms | ~10% | 100+ | $0.024 | AWS integration |

---

## ElevenLabs TTS

### Overview

ElevenLabs offers the highest quality AI voices with voice cloning capabilities.

**Models:**
| Model | Latency | Quality | Use Case |
|-------|---------|---------|----------|
| `eleven_multilingual_v2` | ~300ms | Highest | Production, 29 languages |
| `eleven_turbo_v2_5` | ~200ms | Very High | General use |
| `eleven_flash_v2_5` | ~100ms | High | Real-time streaming |

### Installation

```bash
pip install elevenlabs
```

### Basic TTS

```python
from elevenlabs import ElevenLabs, play, save
import os

client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

# Generate audio
audio = client.text_to_speech.convert(
    voice_id="21m00Tcm4TlvDq8ikWAM",  # Rachel
    text="Hello, welcome to Faion Network!",
    model_id="eleven_turbo_v2_5",
    output_format="mp3_44100_128",
)

# Play directly
play(audio)

# Or save to file
save(audio, "output.mp3")
```

### Streaming (Low Latency)

```python
from elevenlabs import ElevenLabs

client = ElevenLabs()

# Streaming for real-time playback
audio_stream = client.text_to_speech.convert_as_stream(
    voice_id="21m00Tcm4TlvDq8ikWAM",
    text="This is streaming audio generation for low latency applications.",
    model_id="eleven_flash_v2_5",
    output_format="mp3_44100_32",  # Lower bitrate for faster streaming
)

# Process chunks as they arrive
for chunk in audio_stream:
    # Send to audio player or WebSocket
    process_audio_chunk(chunk)
```

### Voice Selection

```python
# List available voices
voices = client.voices.get_all()
for voice in voices.voices:
    print(f"{voice.name}: {voice.voice_id}")

# Popular voice IDs
VOICES = {
    "Rachel": "21m00Tcm4TlvDq8ikWAM",      # Female, American
    "Domi": "AZnzlk1XvdvUeBnXmlld",         # Female, American
    "Bella": "EXAVITQu4vr4xnSDxMaL",        # Female, American
    "Antoni": "ErXwobaYiN019PkySvjV",       # Male, American
    "Josh": "TxGEqnHWrfWFTfGW9XjX",         # Male, American
    "Arnold": "VR6AewLTigWG4xSOukaG",       # Male, American
    "Adam": "pNInz6obpgDQGcFmaJgB",         # Male, American
    "Sam": "yoZ06aMxZJJ28mfd3POQ",          # Male, American
}
```

### Voice Cloning (Instant)

```python
from elevenlabs import VoiceSettings

# Clone voice from audio sample
voice = client.clone(
    name="My Custom Voice",
    description="Voice cloned from sample audio",
    files=["sample1.mp3", "sample2.mp3"],  # 1-30 minutes of audio
)

# Use cloned voice
audio = client.text_to_speech.convert(
    voice_id=voice.voice_id,
    text="Hello, this is my cloned voice!",
    model_id="eleven_multilingual_v2",
)
```

### Voice Settings (Emotion Control)

```python
from elevenlabs import VoiceSettings

audio = client.text_to_speech.convert(
    voice_id="21m00Tcm4TlvDq8ikWAM",
    text="I am so excited about this!",
    model_id="eleven_turbo_v2_5",
    voice_settings=VoiceSettings(
        stability=0.5,          # 0-1: Lower = more expressive
        similarity_boost=0.75,  # 0-1: Higher = closer to original
        style=0.3,              # 0-1: Style exaggeration
        use_speaker_boost=True,
    ),
)
```

### Voice Design (Create from Description)

```python
# Create voice from text description
voice = client.voices.design(
    name="Custom Voice",
    description="A warm, friendly female voice with a British accent",
    text="Hello! This is a sample of the generated voice.",
)
```

### Pronunciation Dictionary

```python
# Custom pronunciation
audio = client.text_to_speech.convert_with_pronunciation_dictionaries(
    voice_id="21m00Tcm4TlvDq8ikWAM",
    text="Welcome to Faion Network!",
    model_id="eleven_turbo_v2_5",
    pronunciation_dictionary_locators=[
        {
            "pronunciation_dictionary_id": "dict_id",
            "version_id": "version_id"
        }
    ],
)
```

---

## OpenAI TTS

### Overview

OpenAI TTS offers simple integration with good quality at low cost.

**Models:**
| Model | Quality | Latency | Price/1M chars |
|-------|---------|---------|----------------|
| `tts-1` | Good | Low | $15 |
| `tts-1-hd` | High | Higher | $30 |

**Voices:** alloy, echo, fable, onyx, nova, shimmer

### Basic Usage

```python
from openai import OpenAI
from pathlib import Path

client = OpenAI()

# Generate speech
response = client.audio.speech.create(
    model="tts-1",
    voice="nova",
    input="Hello, this is OpenAI text to speech!",
    response_format="mp3",  # mp3, opus, aac, flac, wav, pcm
    speed=1.0,  # 0.25 to 4.0
)

# Save to file
response.stream_to_file(Path("output.mp3"))
```

### Streaming

```python
# Real-time streaming
response = client.audio.speech.create(
    model="tts-1",
    voice="nova",
    input="This is streaming audio from OpenAI.",
)

# Stream to file
with open("output.mp3", "wb") as f:
    for chunk in response.iter_bytes():
        f.write(chunk)
```

### Voice Characteristics

| Voice | Gender | Style |
|-------|--------|-------|
| alloy | Neutral | Balanced |
| echo | Male | Warm |
| fable | Female | British |
| onyx | Male | Deep |
| nova | Female | Friendly |
| shimmer | Female | Soft |

---

## Azure Speech Services

### Overview

Azure offers enterprise-grade TTS with SSML support and neural voices.

### Installation

```bash
pip install azure-cognitiveservices-speech
```

### Basic TTS

```python
import azure.cognitiveservices.speech as speechsdk

speech_config = speechsdk.SpeechConfig(
    subscription="your_key",
    region="eastus"
)
speech_config.speech_synthesis_voice_name = "en-US-JennyNeural"

synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

# Synthesize to speaker
result = synthesizer.speak_text_async("Hello from Azure!").get()

# Synthesize to file
audio_config = speechsdk.audio.AudioOutputConfig(filename="output.wav")
synthesizer = speechsdk.SpeechSynthesizer(
    speech_config=speech_config,
    audio_config=audio_config
)
result = synthesizer.speak_text_async("Hello from Azure!").get()
```

### SSML (Speech Synthesis Markup Language)

```python
ssml = """
<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis"
       xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="en-US">
    <voice name="en-US-JennyNeural">
        <mstts:express-as style="cheerful" styledegree="2">
            Hello! I am so happy to meet you!
        </mstts:express-as>
        <break time="500ms"/>
        <prosody rate="-10%" pitch="+5%">
            This is spoken more slowly with higher pitch.
        </prosody>
    </voice>
</speak>
"""

result = synthesizer.speak_ssml_async(ssml).get()
```

### Custom Neural Voice

```python
# Azure custom voice endpoint
speech_config.endpoint_id = "your_custom_voice_endpoint_id"
speech_config.speech_synthesis_voice_name = "YourCustomVoiceName"
```

---

## OpenAI Whisper (STT)

### Overview

Whisper provides excellent multilingual speech recognition with 100+ language support.

**Limits:**
- Max file size: 25 MB
- Supported formats: mp3, mp4, mpeg, mpga, m4a, wav, webm

### Basic Transcription

```python
from openai import OpenAI

client = OpenAI()

# Transcribe audio file
with open("audio.mp3", "rb") as audio_file:
    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        response_format="text",  # text, json, srt, verbose_json, vtt
    )

print(transcript)
```

### Word-Level Timestamps

```python
transcript = client.audio.transcriptions.create(
    model="whisper-1",
    file=audio_file,
    response_format="verbose_json",
    timestamp_granularities=["word", "segment"],
)

for word in transcript.words:
    print(f"{word.start:.2f}s - {word.end:.2f}s: {word.word}")
```

### Translation to English

```python
# Translate any language to English
translation = client.audio.translations.create(
    model="whisper-1",
    file=audio_file,
    response_format="text",
)
```

### Language Detection

```python
transcript = client.audio.transcriptions.create(
    model="whisper-1",
    file=audio_file,
    response_format="verbose_json",
)

print(f"Detected language: {transcript.language}")
```

### Prompt for Better Accuracy

```python
# Use prompt to improve accuracy for specific terms
transcript = client.audio.transcriptions.create(
    model="whisper-1",
    file=audio_file,
    prompt="Faion Network, SDD, solopreneur, Claude Code",
)
```

---

## Deepgram (Real-time STT)

### Overview

Deepgram Nova-3 offers the best real-time speech recognition for voice agents.

**Key Features:**
- Ultra-low latency (~200ms)
- Real-time streaming
- Speaker diarization
- Intent detection
- Summarization

### Installation

```bash
pip install deepgram-sdk
```

### Batch Transcription

```python
from deepgram import DeepgramClient, PrerecordedOptions

deepgram = DeepgramClient("your_api_key")

# Transcribe file
with open("audio.mp3", "rb") as file:
    buffer_data = file.read()

options = PrerecordedOptions(
    model="nova-3",
    language="en",
    smart_format=True,
    punctuate=True,
    paragraphs=True,
    diarize=True,       # Speaker identification
    utterances=True,    # Separate by speaker
    detect_language=True,
)

response = deepgram.listen.prerecorded.v("1").transcribe_file(
    {"buffer": buffer_data},
    options
)

print(response.results.channels[0].alternatives[0].transcript)
```

### Real-time Streaming

```python
from deepgram import DeepgramClient, LiveOptions, LiveTranscriptionEvents
import asyncio

deepgram = DeepgramClient("your_api_key")

async def main():
    connection = deepgram.listen.live.v("1")

    # Event handlers
    @connection.on(LiveTranscriptionEvents.Transcript)
    def on_transcript(self, result, **kwargs):
        transcript = result.channel.alternatives[0].transcript
        if transcript:
            print(f"Transcript: {transcript}")

    @connection.on(LiveTranscriptionEvents.SpeechStarted)
    def on_speech_started(self, speech_started, **kwargs):
        print("Speech started")

    @connection.on(LiveTranscriptionEvents.UtteranceEnd)
    def on_utterance_end(self, utterance_end, **kwargs):
        print("Utterance ended")

    # Configure options
    options = LiveOptions(
        model="nova-3",
        language="en",
        smart_format=True,
        interim_results=True,    # Get partial results
        endpointing=300,         # Silence detection (ms)
        vad_events=True,         # Voice activity detection
    )

    # Start connection
    await connection.start(options)

    # Send audio data (from microphone, WebSocket, etc.)
    # connection.send(audio_bytes)

    # Keep connection alive
    await asyncio.sleep(60)

    await connection.finish()

asyncio.run(main())
```

### Speaker Diarization

```python
options = PrerecordedOptions(
    model="nova-3",
    diarize=True,
    utterances=True,
)

response = deepgram.listen.prerecorded.v("1").transcribe_file(
    {"buffer": audio_data},
    options
)

# Process utterances by speaker
for utterance in response.results.utterances:
    print(f"Speaker {utterance.speaker}: {utterance.transcript}")
```

### Keyword Boosting

```python
options = PrerecordedOptions(
    model="nova-3",
    keywords=["Faion:2.0", "SDD:1.5", "solopreneur:1.5"],
)
```

---

## AssemblyAI (High Accuracy STT)

### Overview

AssemblyAI offers the highest accuracy with advanced features like sentiment analysis and topic detection.

### Installation

```bash
pip install assemblyai
```

### Basic Transcription

```python
import assemblyai as aai

aai.settings.api_key = "your_api_key"

transcriber = aai.Transcriber()

# Transcribe from URL or file
transcript = transcriber.transcribe("https://example.com/audio.mp3")
# Or: transcript = transcriber.transcribe("./audio.mp3")

print(transcript.text)
```

### Advanced Features

```python
config = aai.TranscriptionConfig(
    language_code="en",
    speech_model=aai.SpeechModel.best,

    # Speaker diarization
    speaker_labels=True,
    speakers_expected=2,

    # Content moderation
    content_safety=True,

    # Sentiment analysis
    sentiment_analysis=True,

    # Topic detection
    iab_categories=True,

    # Auto chapters
    auto_chapters=True,

    # Summarization
    summarization=True,
    summary_type=aai.SummarizationType.bullets,

    # Entity detection
    entity_detection=True,

    # Custom vocabulary
    word_boost=["Faion", "SDD", "solopreneur"],
    boost_param="high",
)

transcript = transcriber.transcribe("audio.mp3", config=config)

# Access results
print(f"Speakers: {len(transcript.utterances)}")
for utterance in transcript.utterances:
    print(f"Speaker {utterance.speaker}: {utterance.text}")

print(f"Summary: {transcript.summary}")
print(f"Chapters: {transcript.chapters}")
print(f"Sentiment: {transcript.sentiment_analysis_results}")
```

### Real-time Streaming

```python
def on_data(transcript: aai.RealtimeTranscript):
    if not transcript.text:
        return

    if isinstance(transcript, aai.RealtimeFinalTranscript):
        print(f"Final: {transcript.text}")
    else:
        print(f"Partial: {transcript.text}", end="\r")

def on_error(error: aai.RealtimeError):
    print(f"Error: {error}")

transcriber = aai.RealtimeTranscriber(
    sample_rate=16000,
    on_data=on_data,
    on_error=on_error,
)

transcriber.connect()

# Send audio chunks
# transcriber.stream(audio_bytes)

transcriber.close()
```

---

## Voice Cloning

### ElevenLabs Voice Cloning

**Types:**
| Type | Audio Required | Quality | Turnaround |
|------|----------------|---------|------------|
| Instant | 1-30 min | Good | Seconds |
| Professional | 30+ min | Excellent | Hours |

```python
from elevenlabs import ElevenLabs

client = ElevenLabs()

# Instant voice clone
voice = client.clone(
    name="My Voice Clone",
    description="Cloned from podcast recordings",
    files=[
        "sample1.mp3",
        "sample2.mp3",
        "sample3.mp3",
    ],
    labels={
        "accent": "american",
        "gender": "male",
        "age": "adult",
    }
)

print(f"Voice ID: {voice.voice_id}")
```

### Coqui TTS (Open Source)

```bash
pip install TTS
```

```python
from TTS.api import TTS

# List available models
print(TTS().list_models())

# Load model
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")

# Voice cloning with reference audio
tts.tts_to_file(
    text="Hello, this is my cloned voice!",
    speaker_wav="reference_voice.wav",
    language="en",
    file_path="output.wav",
)
```

### Tortoise TTS (High Quality Open Source)

```python
import torch
from tortoise.api import TextToSpeech
from tortoise.utils.audio import load_voice

tts = TextToSpeech()

# Load custom voice samples
voice_samples, conditioning_latents = load_voice(
    "my_voice",
    extra_voice_dirs=["./voices"]
)

# Generate with voice clone
gen = tts.tts_with_preset(
    "Hello from my cloned voice!",
    voice_samples=voice_samples,
    conditioning_latents=conditioning_latents,
    preset="fast",  # ultra_fast, fast, standard, high_quality
)
```

---

## Speaker Diarization

### pyannote-audio (Open Source)

```bash
pip install pyannote.audio
```

```python
from pyannote.audio import Pipeline

# Initialize pipeline (requires HuggingFace token)
pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization-3.1",
    use_auth_token="your_hf_token"
)

# Run diarization
diarization = pipeline("audio.wav")

# Print results
for turn, _, speaker in diarization.itertracks(yield_label=True):
    print(f"{turn.start:.1f}s - {turn.end:.1f}s: {speaker}")
```

### Combining with Whisper

```python
from pyannote.audio import Pipeline
import whisper

# Diarization
diarization_pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization-3.1"
)
diarization = diarization_pipeline("audio.wav")

# Transcription
whisper_model = whisper.load_model("large-v3")
result = whisper_model.transcribe("audio.wav")

# Combine: assign speakers to transcript segments
def assign_speakers(transcript, diarization):
    """Assign speakers to transcript segments based on timing"""
    for segment in transcript["segments"]:
        start = segment["start"]
        end = segment["end"]

        # Find speaker for this segment
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            if turn.start <= start and turn.end >= end:
                segment["speaker"] = speaker
                break

    return transcript

result = assign_speakers(result, diarization)
```

---

## Real-time Streaming Patterns

### Voice Agent Architecture

```
User Speech → STT (Deepgram) → LLM (Claude/GPT) → TTS (ElevenLabs) → Audio Output
                  ↓                    ↓                   ↓
              ~200ms              ~500ms              ~100ms

Target: < 1000ms total latency
```

### WebSocket Voice Agent

```python
import asyncio
import websockets
from deepgram import DeepgramClient, LiveOptions
from elevenlabs import ElevenLabs
from openai import OpenAI

class VoiceAgent:
    def __init__(self):
        self.deepgram = DeepgramClient()
        self.elevenlabs = ElevenLabs()
        self.openai = OpenAI()
        self.conversation_history = []

    async def handle_audio(self, websocket, path):
        """Handle incoming audio from WebSocket"""

        # Setup Deepgram connection
        dg_connection = self.deepgram.listen.live.v("1")

        async def on_transcript(result):
            transcript = result.channel.alternatives[0].transcript
            if transcript and result.is_final:
                # Process with LLM
                response = await self.process_with_llm(transcript)

                # Generate speech
                audio = self.generate_speech(response)

                # Send back to client
                await websocket.send(audio)

        dg_connection.on("transcript", on_transcript)

        await dg_connection.start(LiveOptions(
            model="nova-3",
            language="en",
            smart_format=True,
            interim_results=False,
            endpointing=300,
        ))

        # Forward audio chunks to Deepgram
        async for message in websocket:
            dg_connection.send(message)

        await dg_connection.finish()

    async def process_with_llm(self, user_input: str) -> str:
        """Process user input with LLM"""
        self.conversation_history.append({
            "role": "user",
            "content": user_input
        })

        response = self.openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful voice assistant. Keep responses concise (under 100 words)."},
                *self.conversation_history
            ],
            max_tokens=150,
        )

        assistant_message = response.choices[0].message.content
        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })

        return assistant_message

    def generate_speech(self, text: str) -> bytes:
        """Generate speech from text"""
        audio_stream = self.elevenlabs.text_to_speech.convert_as_stream(
            voice_id="21m00Tcm4TlvDq8ikWAM",
            text=text,
            model_id="eleven_flash_v2_5",
            output_format="mp3_44100_32",
        )

        return b"".join(audio_stream)

# Run server
async def main():
    agent = VoiceAgent()
    async with websockets.serve(agent.handle_audio, "localhost", 8765):
        await asyncio.Future()

asyncio.run(main())
```

### Turn-Taking Detection

```python
class TurnTakingDetector:
    def __init__(
        self,
        silence_threshold: float = 0.3,  # seconds
        energy_threshold: float = 0.01,
    ):
        self.silence_threshold = silence_threshold
        self.energy_threshold = energy_threshold
        self.last_speech_time = 0
        self.is_user_speaking = False

    def process_audio(self, audio_chunk: bytes, timestamp: float) -> str:
        """Detect turn-taking events"""
        energy = self.calculate_energy(audio_chunk)

        if energy > self.energy_threshold:
            self.is_user_speaking = True
            self.last_speech_time = timestamp
            return "speech_continued"

        elif self.is_user_speaking:
            silence_duration = timestamp - self.last_speech_time

            if silence_duration > self.silence_threshold:
                self.is_user_speaking = False
                return "turn_ended"

            return "silence"

        return "no_speech"

    def calculate_energy(self, audio_chunk: bytes) -> float:
        """Calculate RMS energy of audio chunk"""
        import numpy as np
        samples = np.frombuffer(audio_chunk, dtype=np.int16)
        return np.sqrt(np.mean(samples.astype(float) ** 2)) / 32768
```

### Interruption Handling

```python
class InterruptionHandler:
    def __init__(self, agent_audio_queue: asyncio.Queue):
        self.is_agent_speaking = False
        self.audio_queue = agent_audio_queue

    async def handle_user_speech(self, is_speaking: bool):
        """Handle user interruption during agent speech"""
        if is_speaking and self.is_agent_speaking:
            # User started speaking while agent is speaking
            await self.interrupt_agent()

    async def interrupt_agent(self):
        """Stop agent audio playback"""
        self.is_agent_speaking = False

        # Clear audio queue
        while not self.audio_queue.empty():
            try:
                self.audio_queue.get_nowait()
            except asyncio.QueueEmpty:
                break

        print("Agent interrupted by user")

    async def play_agent_response(self, audio_chunks):
        """Play agent response with interruption support"""
        self.is_agent_speaking = True

        for chunk in audio_chunks:
            if not self.is_agent_speaking:
                break  # Interrupted

            await self.audio_queue.put(chunk)
            await asyncio.sleep(0.01)

        self.is_agent_speaking = False
```

---

## Audio Editing

### pydub (Audio Manipulation)

```bash
pip install pydub
```

```python
from pydub import AudioSegment
from pydub.effects import normalize, compress_dynamic_range
from pydub.silence import split_on_silence

# Load audio
audio = AudioSegment.from_file("input.mp3")

# Basic operations
audio = audio + 10  # Increase volume by 10dB
audio = audio - 5   # Decrease volume by 5dB
audio = audio.fade_in(1000).fade_out(1000)  # Fade in/out
audio = audio.set_frame_rate(44100)  # Resample
audio = audio.set_channels(1)  # Convert to mono

# Concatenation
combined = audio1 + audio2

# Slicing
first_10_seconds = audio[:10000]  # milliseconds

# Split on silence
chunks = split_on_silence(
    audio,
    min_silence_len=500,
    silence_thresh=-40,
    keep_silence=200,
)

# Effects
audio = normalize(audio)
audio = compress_dynamic_range(audio, threshold=-20, ratio=4.0)

# Export
audio.export("output.mp3", format="mp3", bitrate="192k")
audio.export("output.wav", format="wav")
```

### librosa (Audio Analysis)

```bash
pip install librosa
```

```python
import librosa
import numpy as np

# Load audio
y, sr = librosa.load("audio.mp3", sr=None)

# Get duration
duration = librosa.get_duration(y=y, sr=sr)

# Extract features
mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)

# Pitch detection
pitches, magnitudes = librosa.piptrack(y=y, sr=sr)

# Speech/music detection
# (Use onset detection for speech segmentation)
onset_frames = librosa.onset.onset_detect(y=y, sr=sr)
onset_times = librosa.frames_to_time(onset_frames, sr=sr)
```

### soundfile (Read/Write Audio)

```python
import soundfile as sf

# Read audio
data, samplerate = sf.read("audio.wav")

# Write audio
sf.write("output.wav", data, samplerate)

# Get info without loading
info = sf.info("audio.wav")
print(f"Duration: {info.duration}s, Channels: {info.channels}")
```

---

## Latency Optimization

### Best Practices for Low Latency

| Optimization | Impact | Implementation |
|--------------|--------|----------------|
| **Streaming TTS** | -200ms | Use `eleven_flash_v2_5` with streaming |
| **Streaming STT** | -150ms | Use Deepgram Nova-3 live |
| **Sentence chunking** | -300ms | Generate TTS per sentence |
| **Prefetch** | -100ms | Start TTS before LLM completes |
| **WebSocket** | -50ms | Use persistent connections |
| **Edge deployment** | -100ms | Deploy STT/TTS at edge |

### Sentence-Level Streaming

```python
import re

def stream_by_sentence(text: str, tts_client):
    """Stream TTS generation by sentence for lower latency"""

    # Split into sentences
    sentences = re.split(r'(?<=[.!?])\s+', text)

    for sentence in sentences:
        if sentence.strip():
            audio_stream = tts_client.text_to_speech.convert_as_stream(
                voice_id="21m00Tcm4TlvDq8ikWAM",
                text=sentence,
                model_id="eleven_flash_v2_5",
            )

            for chunk in audio_stream:
                yield chunk
```

### Prefetch Pattern

```python
async def prefetch_tts(llm_stream, tts_client):
    """Start TTS generation as soon as first sentence is available"""

    buffer = ""

    async for token in llm_stream:
        buffer += token

        # Check for sentence boundary
        if any(buffer.endswith(p) for p in ['. ', '! ', '? ']):
            # Start TTS immediately
            audio_task = asyncio.create_task(
                generate_tts_async(buffer.strip(), tts_client)
            )
            yield audio_task
            buffer = ""

    # Handle remaining text
    if buffer.strip():
        audio_task = asyncio.create_task(
            generate_tts_async(buffer.strip(), tts_client)
        )
        yield audio_task
```

---

## Error Recovery

### Robust Voice Agent

```python
class RobustVoiceAgent:
    def __init__(self):
        self.fallback_responses = [
            "I'm sorry, I didn't catch that. Could you repeat?",
            "Let me think about that for a moment.",
            "I'm having trouble understanding. Can you try again?",
        ]
        self.retry_count = 0
        self.max_retries = 3

    async def process_with_fallback(self, audio_chunk: bytes) -> bytes:
        try:
            # Primary STT
            transcript = await self.stt_primary(audio_chunk)

            if not transcript or len(transcript) < 2:
                return self.get_fallback_audio("no_speech")

            # LLM processing
            response = await self.llm_process(transcript)

            # TTS
            audio = await self.tts_generate(response)

            self.retry_count = 0
            return audio

        except Exception as e:
            self.retry_count += 1

            if self.retry_count >= self.max_retries:
                return self.get_fallback_audio("error")

            # Try fallback STT service
            try:
                transcript = await self.stt_fallback(audio_chunk)
                response = await self.llm_process(transcript)
                return await self.tts_generate(response)
            except:
                return self.get_fallback_audio("retry")

    def get_fallback_audio(self, reason: str) -> bytes:
        """Return pre-generated fallback audio"""
        import random
        response = random.choice(self.fallback_responses)
        # Use cached or pre-generated audio for faster response
        return self.cached_audio.get(response)
```

---

## Cost Optimization

### Service Selection by Use Case

| Use Case | Recommended | Monthly Cost (10h audio) |
|----------|-------------|--------------------------|
| **Podcast transcription** | Whisper | $3.60 |
| **Voice agent (quality)** | Deepgram + ElevenLabs | $35 + $180 |
| **Voice agent (budget)** | Deepgram + OpenAI TTS | $35 + $9 |
| **Batch TTS** | OpenAI TTS | $9/100k chars |
| **Premium TTS** | ElevenLabs | $22/month (10k chars) |

### Caching Strategy

```python
import hashlib
from functools import lru_cache

class TTSCache:
    def __init__(self, cache_dir: str = "./tts_cache"):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)

    def get_cache_key(self, text: str, voice_id: str, model: str) -> str:
        """Generate cache key from parameters"""
        content = f"{text}:{voice_id}:{model}"
        return hashlib.md5(content.encode()).hexdigest()

    def get_cached(self, text: str, voice_id: str, model: str) -> bytes | None:
        """Get cached audio if exists"""
        key = self.get_cache_key(text, voice_id, model)
        path = os.path.join(self.cache_dir, f"{key}.mp3")

        if os.path.exists(path):
            with open(path, "rb") as f:
                return f.read()
        return None

    def cache_audio(self, text: str, voice_id: str, model: str, audio: bytes):
        """Cache generated audio"""
        key = self.get_cache_key(text, voice_id, model)
        path = os.path.join(self.cache_dir, f"{key}.mp3")

        with open(path, "wb") as f:
            f.write(audio)
```

---

## API Credentials

### Environment Variables

```bash
# ElevenLabs
export ELEVENLABS_API_KEY="your_key"

# OpenAI
export OPENAI_API_KEY="your_key"

# Azure Speech
export AZURE_SPEECH_KEY="your_key"
export AZURE_SPEECH_REGION="eastus"

# Deepgram
export DEEPGRAM_API_KEY="your_key"

# AssemblyAI
export ASSEMBLYAI_API_KEY="your_key"
```

### Loading Credentials

```python
import os
from dotenv import load_dotenv

load_dotenv()

# Or use secrets file
# source ~/.secrets/elevenlabs
# source ~/.secrets/openai
# source ~/.secrets/deepgram
```

---

## Related Agents

| Agent | Purpose |
|-------|---------|
| faion-tts-agent | Text-to-speech synthesis |
| faion-stt-agent | Speech-to-text transcription |
| faion-voice-agent-builder-agent | Build complete voice agents |

---

## References

- [ElevenLabs Docs](https://elevenlabs.io/docs)
- [OpenAI Audio API](https://platform.openai.com/docs/guides/audio)
- [Azure Speech Services](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/)
- [Deepgram Docs](https://developers.deepgram.com/docs)
- [AssemblyAI Docs](https://www.assemblyai.com/docs)
- [pyannote-audio](https://github.com/pyannote/pyannote-audio)
- [Coqui TTS](https://github.com/coqui-ai/TTS)
