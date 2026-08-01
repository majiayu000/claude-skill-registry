# Music Generation (Lyria RealTime)

Lyria RealTime generates continuous, high-quality instrumental music in real-time. Stream and steer music generation dynamically using text prompts and configuration parameters.

## Table of Contents

- [Overview](#overview)
- [Basic Usage](#basic-usage)
- [Steering Music](#steering-music)
- [Configuration](#configuration)
- [Prompting Guide](#prompting-guide)
- [Best Practices](#best-practices)
- [Technical Details](#technical-details)

---

## Overview

| Property | Value |
|----------|-------|
| **Model** | `lyria-realtime-exp` |
| **Output** | Raw 16-bit PCM Audio |
| **Sample Rate** | 48kHz |
| **Channels** | 2 (stereo) |
| **Type** | Instrumental only |

**Key Features:**
- Real-time continuous music generation
- Dynamic steering with weighted prompts
- Configurable BPM, scale, density, brightness
- Safety-filtered prompts
- Watermarked output

---

## Basic Usage

### Python

```python
import asyncio
from google import genai
from google.genai import types

client = genai.Client()

async def receive_audio(session):
    """Receive and process audio chunks from the session."""
    async for message in session.receive():
        if message.server_content and message.server_content.audio_chunks:
            audio_data = message.server_content.audio_chunks[0].data
            # Process audio (e.g., write to file, play through speakers)
            await asyncio.sleep(10**-12)

async def main():
    async with (
        client.aio.live.music.connect(model='models/lyria-realtime-exp') as session,
        asyncio.TaskGroup() as tg,
    ):
        # Set up task to receive server messages
        tg.create_task(receive_audio(session))

        # Set initial prompts
        await session.set_weighted_prompts(
            prompts=[
                types.WeightedPrompt(text='minimal techno', weight=1.0),
            ]
        )

        # Configure generation
        await session.set_music_generation_config(
            config=types.LiveMusicGenerationConfig(bpm=90, temperature=1.0)
        )

        # Start streaming
        await session.play()

if __name__ == "__main__":
    asyncio.run(main())
```

### JavaScript

```javascript
import { GoogleGenAI } from "@google/genai";
import Speaker from "speaker";

const ai = new GoogleGenAI({});

async function main() {
    const speaker = new Speaker({
        channels: 2,
        bitDepth: 16,
        sampleRate: 48000,
    });

    const session = await ai.live.music.connect({
        model: "models/lyria-realtime-exp",
        callbacks: {
            onmessage: (message) => {
                if (message.serverContent?.audioChunks) {
                    for (const chunk of message.serverContent.audioChunks) {
                        const audioBuffer = Buffer.from(chunk.data, "base64");
                        speaker.write(audioBuffer);
                    }
                }
            },
            onerror: (error) => console.error("music session error:", error),
            onclose: () => console.log("Lyria RealTime stream closed."),
        },
    });

    await session.setWeightedPrompts({
        weightedPrompts: [
            { text: "Minimal techno with deep bass", weight: 1.0 },
        ],
    });

    await session.setMusicGenerationConfig({
        musicGenerationConfig: {
            bpm: 90,
            temperature: 1.0,
            audioFormat: "pcm16",
            sampleRateHz: 44100,
        },
    });

    await session.play();
}

main().catch(console.error);
```

---

## Steering Music

Change the music dynamically during generation by updating prompts and config.

### Python

```python
# Initial prompt
await session.set_weighted_prompts(
    prompts=[types.WeightedPrompt(text='ambient electronic', weight=1.0)]
)
await session.play()

# Later: blend in a new element
await session.set_weighted_prompts(
    prompts=[
        types.WeightedPrompt(text='ambient electronic', weight=0.7),
        types.WeightedPrompt(text='driving drums', weight=0.3),
    ]
)

# Morph further
await session.set_weighted_prompts(
    prompts=[
        types.WeightedPrompt(text='ambient electronic', weight=0.3),
        types.WeightedPrompt(text='driving drums', weight=0.7),
    ]
)
```

### JavaScript

```javascript
// Start with ambient
await session.setWeightedPrompts({
    weightedPrompts: [
        { text: "ambient electronic", weight: 1.0 },
    ],
});

// Blend in drums
await session.setWeightedPrompts({
    weightedPrompts: [
        { text: "ambient electronic", weight: 0.7 },
        { text: "driving drums", weight: 0.3 },
    ],
});
```

---

## Configuration

### MusicGenerationConfig Parameters

| Parameter | Type | Range | Default | Description |
|-----------|------|-------|---------|-------------|
| `guidance` | float | [0.0, 6.0] | 4.0 | How strictly model follows prompts. Higher = better adherence, more abrupt transitions |
| `bpm` | int | [60, 200] | - | Beats Per Minute. Requires stop/play to take effect |
| `density` | float | [0.0, 1.0] | - | Note density. Lower = sparser, higher = busier |
| `brightness` | float | [0.0, 1.0] | - | Tonal quality. Higher = brighter, more high frequencies |
| `scale` | Enum | See below | UNSPECIFIED | Musical scale/key. Requires stop/play to take effect |
| `temperature` | float | - | 1.0 | Randomness in generation |

### Python Config Example

```python
await session.set_music_generation_config(
    config=types.LiveMusicGenerationConfig(
        bpm=120,
        density=0.7,
        brightness=0.6,
        guidance=4.0,
        scale=types.Scale.C_MAJOR_A_MINOR,
        temperature=1.0,
    )
)
```

### JavaScript Config Example

```javascript
await session.setMusicGenerationConfig({
    musicGenerationConfig: {
        bpm: 120,
        density: 0.7,
        brightness: 0.6,
        guidance: 4.0,
        scale: "C_MAJOR_A_MINOR",
        temperature: 1.0,
    },
});
```

### Scale Enum Values

| Enum Value | Scale / Key |
|------------|-------------|
| `C_MAJOR_A_MINOR` | C major / A minor |
| `D_FLAT_MAJOR_B_FLAT_MINOR` | D-flat major / B-flat minor |
| `D_MAJOR_B_MINOR` | D major / B minor |
| `E_FLAT_MAJOR_C_MINOR` | E-flat major / C minor |
| `E_MAJOR_D_FLAT_MINOR` | E major / C-sharp minor |
| `F_MAJOR_D_MINOR` | F major / D minor |
| `G_FLAT_MAJOR_E_FLAT_MINOR` | G-flat major / E-flat minor |
| `G_MAJOR_E_MINOR` | G major / E minor |
| `A_FLAT_MAJOR_F_MINOR` | A-flat major / F minor |
| `A_MAJOR_G_FLAT_MINOR` | A major / F-sharp minor |
| `B_FLAT_MAJOR_G_MINOR` | B-flat major / G minor |
| `B_MAJOR_A_FLAT_MINOR` | B major / G-sharp minor |
| `SCALE_UNSPECIFIED` | Model decides |

**Note**: The model does not distinguish between relative major/minor keys. Each enum corresponds to both.

---

## Prompting Guide

### Prompt Categories

**Instruments:**
```
808 Drums, Acoustic Drums, Acoustic Guitar, Bagpipe, Banjo, Bass Synth,
Bassoon, Bells, Brass Section, Cello, Clarinet, Classical Guitar, Clavinet,
Clean Electric Guitar, Dirty Funk Bass, Distorted Guitar, Fiddle, Flute,
French Horn, Funk Drums, Guitar, Hang Drum, Harmonica, Harp, Harpsichord,
Kalimba, Koto, Mandolin, Marimba, Mellotron, Moog Oscillations, Ocarina,
Piano, Rhodes Piano, Shamisen, Sitar, Slide Guitar, Synth Pads, Tabla,
TR-909 Drum Machine, Trumpet, Tuba, Vibraphone, Viola Ensemble, ...
```

**Genres:**
```
Acid Jazz, Afrobeat, Baroque, Bhangra, Bluegrass, Blues Rock, Bossa Nova,
Breakbeat, Celtic Folk, Chillout, Chiptune, Classic Rock, Contemporary R&B,
Cumbia, Deep House, Disco Funk, Drum & Bass, Dubstep, EDM, Electro Swing,
Funk Metal, Garage Rock, Glitch Hop, Grime, Hyperpop, Indie Electronic,
Indie Folk, Indie Pop, Jazz Fusion, Lo-Fi Hip Hop, Minimal Techno,
Neo-Soul, Orchestral Score, Piano Ballad, Post-Punk, Psytrance, R&B,
Reggae, Reggaeton, Salsa, Shoegaze, Ska, Surf Rock, Synthpop, Techno,
Trance, Trap Beat, Trip Hop, Vaporwave, ...
```

**Mood/Description:**
```
Ambient, Bright Tones, Chill, Danceable, Dreamy, Emotional, Ethereal,
Experimental, Funky, Glitchy Effects, Lo-fi, Ominous, Psychedelic,
Rich Orchestration, Subdued Melody, Tight Groove, Unsettling, Upbeat,
Virtuoso, ...
```

### Example Prompts

```python
# Electronic
types.WeightedPrompt(text="Minimal techno with deep bass, sparse percussion, and atmospheric synths", weight=1.0)

# Orchestral
types.WeightedPrompt(text="Cinematic orchestral score, sweeping strings, triumphant brass", weight=1.0)

# Lo-fi
types.WeightedPrompt(text="Lo-fi hip hop, vinyl crackle, mellow piano, lazy drums", weight=1.0)

# Jazz
types.WeightedPrompt(text="Smooth jazz fusion, Rhodes piano, walking bass, brush drums", weight=1.0)
```

---

## Best Practices

1. **Audio Buffering**: Implement robust audio buffering for smooth playback to handle network jitter and generation latency variations.

2. **Gradual Steering**: Rather than completely changing prompts, add or modify elements gradually for smoother morphing.

3. **Weight Experimentation**: Use `weight` on `WeightedPrompt` to control how strongly a prompt influences generation.

4. **Descriptive Prompts**: Use adjectives describing mood, genre, and instrumentation for better results.

5. **BPM/Scale Changes**: Remember that `bpm` and `scale` require stop/play or context reset to take effect.

---

## Technical Details

### Specifications

| Property | Value |
|----------|-------|
| Output Format | Raw 16-bit PCM Audio |
| Sample Rate | 48kHz |
| Channels | 2 (stereo) |

### Limitations

- **Instrumental only**: No vocals or singing
- **Safety filters**: Prompts are checked; filtered prompts are ignored with explanation in `filtered_prompt` field
- **Watermarking**: Output is always watermarked per Responsible AI principles

---

## Resources

- [Music Generation Guide](https://ai.google.dev/gemini-api/docs/music-generation)
- [Lyria RealTime Cookbook](https://github.com/google-gemini/cookbook)
- [Live API](https://ai.google.dev/gemini-api/docs/live)
