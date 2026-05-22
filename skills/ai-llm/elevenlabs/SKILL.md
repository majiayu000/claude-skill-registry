---
name: elevenlabs
description: |
  AI-powered audio generation using ElevenLabs API - text-to-speech with lifelike voices,
  sound effects generation, and music creation from text descriptions. Generate natural-sounding
  speech in 32 languages, create custom sound effects for games and videos, and compose
  royalty-free music tracks.

  Use this skill when the user requests:
  - Voice generation or text-to-speech conversion
  - Audio narration for content (videos, audiobooks, podcasts)
  - Sound effects for games, videos, or applications
  - Music generation from text descriptions
  - Multi-speaker dialogue or conversation audio
  - Voice cloning or custom voice creation
  - Audio streaming for real-time applications

  Capabilities: Text-to-speech (32 languages, 100+ voices), sound effects generation,
  music composition, voice cloning, real-time audio streaming

  Python SDK: elevenlabs (pip install elevenlabs)
allowed-tools: ["Bash", "Read", "Write", "AskUserQuestion"]
---

# ElevenLabs Audio Generation

## Purpose

This skill enables AI-powered audio generation through ElevenLabs API. Create lifelike text-to-speech in 32 languages, generate custom sound effects for games and videos, and compose royalty-free music from text descriptions. Support for 100+ professional voices, custom voice cloning, real-time streaming, and multi-speaker dialogue.

## When to Use

This skill should be invoked when the user asks to:
- Generate speech from text ("convert this to speech", "create audio narration...")
- Create voiceovers for videos, presentations, or content
- Generate audio in specific voices or languages
- Create sound effects ("generate footstep sounds", "create explosion audio...")
- Compose music from descriptions ("generate upbeat background music...")
- Build multi-speaker dialogue or conversations
- Clone voices from audio samples
- Stream audio in real-time applications
- Create audiobooks, podcasts, or audio content

## Available Capabilities

### 1. Text-to-Speech (Voice Generation)

**Models:**
- **Eleven Multilingual v2** (`eleven_multilingual_v2`) - Highest quality, 29 languages
- **Eleven Flash v2.5** (`eleven_flash_v2_5`) - Ultra-low 75ms latency, 32 languages, 50% cheaper
- **Eleven Turbo v2.5** (`eleven_turbo_v2_5`) - Balanced quality and latency

**Features:**
- 100+ premade professional voices
- Custom voice cloning from audio samples
- Multi-speaker dialogue generation
- Real-time audio streaming
- 32 language support
- Emotional and natural intonation
- Voice settings customization (stability, similarity, style)

**Output Formats:**
- MP3 (various bitrates: 32kbps to 192kbps)
- PCM (8kHz to 48kHz)
- Opus, µ-law, A-law

### 2. Sound Effects Generation

**Model:**
- **Eleven Text-to-Sound v2** (`eleven_text_to_sound_v2`)

**Features:**
- Generate sound effects from text descriptions
- Customizable duration
- Looping support for seamless audio
- Prompt influence control
- High-quality audio for games, videos, UI/UX

**Use Cases:**
- Game audio (footsteps, explosions, ambient)
- Video production sounds
- UI/UX sound design
- Nature sounds (rain, wind, waves)
- Mechanical sounds (doors, engines, machines)
- Fantasy/sci-fi effects

### 3. Music Generation

**Features:**
- Text-to-music composition
- Vocal and instrumental tracks
- Multiple genres and styles
- Customizable track duration
- Composition plans (structured music blueprints)
- Royalty-free generated music

**Parameters:**
- Text prompts describing desired music
- Duration control (milliseconds)
- Genre, style, mood specifications
- Section-level composition control

**Requirements:**
- Paid ElevenLabs account (music API not available on free tier)

**Content Policy:**
- No copyrighted material (artist names, band names, trademarks)
- Returns suggestions for restricted prompts

## Instructions

### Step 1: Understand the Request

Analyze the user's request to determine:
- **Task Type**: Text-to-speech, sound effects, or music generation
- **Content**: What text/description to convert
- **Voice/Sound**: Specific voice, language, or sound characteristics
- **Format**: Output format requirements (MP3, streaming, etc.)
- **Duration**: Length requirements (for sound effects or music)
- **Use Case**: Narration, video, game, podcast, etc.

### Step 2: Select Appropriate Model/Capability

**For Text-to-Speech:**
- **High quality needed** → `eleven_multilingual_v2`
- **Low latency/real-time** → `eleven_flash_v2_5`
- **Balanced** → `eleven_turbo_v2_5`

**For Sound Effects:**
- Use `eleven_text_to_sound_v2` model
- Consider duration and looping needs

**For Music:**
- Ensure user has paid account
- Determine track length and style

### Step 3: Set Up API Authentication

```python
import os
from elevenlabs.client import ElevenLabs

# Initialize client with API key
client = ElevenLabs(api_key=os.environ.get("ELEVENLABS_API_KEY"))
```

API key should be set as environment variable:
```bash
export ELEVENLABS_API_KEY="your-api-key-here"
```

### Step 4: Implement Based on Task Type

#### Text-to-Speech Implementation

**Basic Speech Generation:**
```python
from elevenlabs.client import ElevenLabs
from pathlib import Path

client = ElevenLabs(api_key=os.environ["ELEVENLABS_API_KEY"])

# Generate speech
audio = client.text_to_speech.convert(
    text="Your text content here",
    voice_id="JBFqnCBsd6RMkjVDRZzb",  # Default voice (George)
    model_id="eleven_multilingual_v2",
    output_format="mp3_44100_128"
)

# Save to file
output_path = Path("speech_output.mp3")
with output_path.open("wb") as f:
    for chunk in audio:
        f.write(chunk)

print(f"Audio saved to: {output_path}")
```

**Streaming Speech (Real-time):**
```python
from elevenlabs.client import ElevenLabs
from elevenlabs import stream

client = ElevenLabs(api_key=os.environ["ELEVENLABS_API_KEY"])

# Stream audio in real-time
audio_stream = client.text_to_speech.convert_as_stream(
    text="This will be streamed as it generates",
    voice_id="JBFqnCBsd6RMkjVDRZzb",
    model_id="eleven_flash_v2_5",  # Low latency model for streaming
    output_format="mp3_44100_128"
)

# Stream to speakers
stream(audio_stream)
```

**Multi-Speaker Dialogue:**
```python
# Generate conversation with multiple voices
speakers = [
    {
        "voice_id": "JBFqnCBsd6RMkjVDRZzb",  # Speaker 1
        "text": "Hello, how are you today?"
    },
    {
        "voice_id": "21m00Tcm4TlvDq8ikWAM",  # Speaker 2 (Rachel)
        "text": "I'm doing great, thanks for asking!"
    }
]

# Generate each speaker's audio and combine
from pydub import AudioSegment
combined = AudioSegment.empty()

for speaker in speakers:
    audio = client.text_to_speech.convert(
        text=speaker["text"],
        voice_id=speaker["voice_id"],
        model_id="eleven_multilingual_v2"
    )

    # Save temp file
    temp_path = Path(f"temp_{speaker['voice_id']}.mp3")
    with temp_path.open("wb") as f:
        for chunk in audio:
            f.write(chunk)

    # Add to combined audio
    segment = AudioSegment.from_mp3(str(temp_path))
    combined += segment
    temp_path.unlink()  # Clean up

# Export final dialogue
combined.export("dialogue.mp3", format="mp3")
```

**List Available Voices:**
```python
# Get all available voices
voices = client.voices.get_all()

print("Available voices:")
for voice in voices.voices:
    print(f"- {voice.name} (ID: {voice.voice_id})")
    print(f"  Labels: {voice.labels}")
    print(f"  Description: {voice.description}")
```

**Common Voice IDs:**
- `JBFqnCBsd6RMkjVDRZzb` - George (male, English, middle-aged)
- `21m00Tcm4TlvDq8ikWAM` - Rachel (female, English, young)
- `AZnzlk1XvdvUeBnXmlld` - Domi (female, English, young)
- `EXAVITQu4vr4xnSDxMaL` - Bella (female, English, young)
- `ErXwobaYiN019PkySvjV` - Antoni (male, English, young)
- `MF3mGyEYCl7XYWbV9V6O` - Elli (female, English, young)
- `TxGEqnHWrfWFTfGW9XjX` - Josh (male, English, young)

#### Sound Effects Implementation

**Basic Sound Effect Generation:**
```python
from elevenlabs.client import ElevenLabs
from pathlib import Path

client = ElevenLabs(api_key=os.environ["ELEVENLABS_API_KEY"])

# Generate sound effect
audio = client.text_to_sound_effects.convert(
    text="footsteps on wooden floor, slow paced walking",
    duration_seconds=5.0,
    prompt_influence=0.5  # How closely to follow prompt (0.0-1.0)
)

# Save to file
output_path = Path("footsteps.mp3")
with output_path.open("wb") as f:
    for chunk in audio:
        f.write(chunk)

print(f"Sound effect saved to: {output_path}")
```

**Looping Sound Effect:**
```python
# Generate seamlessly looping audio
audio = client.text_to_sound_effects.convert(
    text="gentle rain falling on leaves, ambient nature sound",
    duration_seconds=10.0,
    prompt_influence=0.5
    # Note: loop parameter may be available in newer API versions
)

output_path = Path("rain_loop.mp3")
with output_path.open("wb") as f:
    for chunk in audio:
        f.write(chunk)
```

**Multiple Sound Effects:**
```python
# Generate various sound effects for a game
sound_effects = [
    {
        "name": "explosion",
        "description": "large explosion, debris falling, action movie style",
        "duration": 3.0
    },
    {
        "name": "door_open",
        "description": "creaky wooden door slowly opening, horror atmosphere",
        "duration": 2.0
    },
    {
        "name": "ui_click",
        "description": "soft button click, UI feedback sound, pleasant tone",
        "duration": 0.5
    }
]

for sfx in sound_effects:
    audio = client.text_to_sound_effects.convert(
        text=sfx["description"],
        duration_seconds=sfx["duration"]
    )

    output_path = Path(f"{sfx['name']}.mp3")
    with output_path.open("wb") as f:
        for chunk in audio:
            f.write(chunk)

    print(f"Generated: {output_path}")
```

#### Music Generation Implementation

**Basic Music Composition:**
```python
from elevenlabs.client import ElevenLabs
from pathlib import Path

client = ElevenLabs(api_key=os.environ["ELEVENLABS_API_KEY"])

# Generate music from prompt
prompt = """Upbeat indie pop song with acoustic guitar, light drums, and cheerful
melody. Modern and energetic feel, perfect for background music in a lifestyle video.
Instrumental only, no vocals."""

try:
    audio = client.music_generation.compose(
        prompt=prompt,
        music_length_ms=30000  # 30 seconds
    )

    # Save music file
    output_path = Path("background_music.mp3")
    with output_path.open("wb") as f:
        for chunk in audio:
            f.write(chunk)

    print(f"Music saved to: {output_path}")

except Exception as e:
    if "paid" in str(e).lower() or "subscription" in str(e).lower():
        print("Error: Music generation requires a paid ElevenLabs account")
    else:
        print(f"Error: {e}")
```

**Music with Composition Plan:**
```python
# Create structured composition plan first
composition_plan = client.music_generation.composition_plan.create(
    prompt="""Electronic dance music track with energetic build-up, drop section,
    and chill outro. Progressive house style.""",
    music_length_ms=60000  # 60 seconds
)

# Generate music from plan (allows for more control)
audio = client.music_generation.compose(
    composition_plan=composition_plan
)

output_path = Path("edm_track.mp3")
with output_path.open("wb") as f:
    for chunk in audio:
        f.write(chunk)
```

**Genre-Specific Music:**
```python
# Generate music for different genres/moods
music_prompts = {
    "cinematic": """Epic cinematic orchestral music with dramatic strings, powerful
    brass, and heroic theme. Perfect for movie trailer, inspiring and grand.""",

    "lo-fi": """Chill lo-fi hip hop beats with jazz piano, vinyl crackle, and mellow
    drums. Relaxing study music atmosphere, instrumental.""",

    "ambient": """Ambient soundscape with ethereal pads, subtle textures, and peaceful
    atmosphere. Meditative and calming, perfect for relaxation.""",

    "game_menu": """Mysterious fantasy game menu music with harp, soft strings, and
    magical atmosphere. Medieval RPG feel, looping background music."""
}

for name, prompt in music_prompts.items():
    try:
        audio = client.music_generation.compose(
            prompt=prompt,
            music_length_ms=20000  # 20 seconds
        )

        output_path = Path(f"music_{name}.mp3")
        with output_path.open("wb") as f:
            for chunk in audio:
                f.write(chunk)

        print(f"Generated: {output_path}")

    except Exception as e:
        print(f"Error generating {name}: {e}")
```

### Step 5: Handle Output and Errors

**Save Audio Files:**
```python
from pathlib import Path

def save_audio(audio_generator, filename):
    """Save audio generator to file"""
    output_path = Path(filename)

    with output_path.open("wb") as f:
        for chunk in audio_generator:
            f.write(chunk)

    print(f"Saved: {output_path.absolute()}")
    return output_path
```

**Error Handling:**
```python
import os
from elevenlabs.client import ElevenLabs

def check_api_key():
    """Verify API key is set"""
    if not os.environ.get("ELEVENLABS_API_KEY"):
        raise ValueError(
            "ELEVENLABS_API_KEY not set. "
            "Please set environment variable: export ELEVENLABS_API_KEY='your-key'"
        )

def handle_elevenlabs_request(func, *args, **kwargs):
    """Wrapper for error handling"""
    try:
        return func(*args, **kwargs)

    except Exception as e:
        error_msg = str(e).lower()

        if "api key" in error_msg or "authentication" in error_msg:
            print("Error: Invalid or missing API key")
            print("Set your API key: export ELEVENLABS_API_KEY='your-key'")

        elif "quota" in error_msg or "limit" in error_msg:
            print("Error: API quota exceeded")
            print("Check your usage at https://elevenlabs.io/app/usage")

        elif "paid" in error_msg or "subscription" in error_msg:
            print("Error: This feature requires a paid subscription")

        elif "bad_prompt" in error_msg:
            print("Error: Prompt contains restricted content")
            print("Avoid copyrighted material (artist names, brands)")

        else:
            print(f"Error: {e}")

        raise
```

### Step 6: Provide Output to User

1. **Report what was generated**
2. **Show file path** where audio was saved
3. **Provide playback options** if appropriate
4. **Offer refinements** (different voice, longer duration, etc.)
5. **Display metadata** (duration, format, model used)

## Requirements

**API Key:**
- ElevenLabs API key (get from https://elevenlabs.io/app/settings/api-keys)
- Set as environment variable: `ELEVENLABS_API_KEY`

**Python Packages:**
```bash
pip install elevenlabs pydub python-dotenv
```

**System:**
- Python 3.8+
- Internet connection for API access
- Audio playback library (optional, for playing generated audio)
- ffmpeg (required by pydub for audio processing)

**Account Requirements:**
- Free tier: Text-to-speech and sound effects
- Paid tier: Music generation, higher quotas

## Best Practices

### Text-to-Speech

1. **Choose Appropriate Model:**
   - High quality narration → `eleven_multilingual_v2`
   - Real-time/streaming → `eleven_flash_v2_5`
   - Balanced use cases → `eleven_turbo_v2_5`

2. **Select Right Voice:**
   - Match voice to content (age, gender, accent)
   - Use `voices.get_all()` to explore options
   - Consider voice labels and descriptions

3. **Optimize for Use Case:**
   - Long content: Use standard conversion, not streaming
   - Real-time apps: Use Flash model with streaming
   - Dialogue: Generate separate audio per speaker

4. **Format Selection:**
   - Web/mobile: MP3 (good quality, small size)
   - High quality: Use higher bitrate (128kbps+)
   - Phone systems: µ-law or A-law format

### Sound Effects Generation

1. **Be Descriptive:**
   - Include context: "footsteps on gravel, slow walking pace"
   - Specify mood: "creepy door creak, horror atmosphere"
   - Add technical details: "deep bass explosion, action movie"

2. **Duration Control:**
   - Short sounds: 0.5-2 seconds (UI clicks, impacts)
   - Medium sounds: 2-5 seconds (footsteps, doors)
   - Ambient loops: 5-10+ seconds (rain, wind, environments)

3. **Prompt Influence:**
   - High (0.7-1.0): Follow prompt closely, more literal
   - Medium (0.4-0.6): Balanced creativity and adherence
   - Low (0.0-0.3): More creative interpretation

4. **Iteration:**
   - Generate multiple variations
   - Adjust descriptions based on results
   - Combine multiple effects if needed

### Music Generation

1. **Detailed Prompts:**
   - Specify genre, instruments, mood, tempo
   - Mention structure (intro, build-up, drop, outro)
   - Include use case context (game menu, video background)

2. **Avoid Copyrighted References:**
   - Don't mention artist names, band names, songs
   - Use generic style descriptions instead
   - Focus on characteristics, not examples

3. **Duration Planning:**
   - Short clips: 10-30 seconds (loops, backgrounds)
   - Full tracks: 60-120 seconds (complete songs)
   - Consider export time (longer = more processing)

4. **Composition Plans:**
   - Use for complex multi-section tracks
   - Better control over structure
   - Allows section-level customization

### General Best Practices

1. **API Key Security:**
   - Store in environment variables, never in code
   - Use `.env` files for local development
   - Rotate keys periodically

2. **Error Handling:**
   - Always wrap API calls in try/except
   - Check for quota limits
   - Provide helpful error messages

3. **Cost Optimization:**
   - Use Flash model when quality difference is minimal
   - Cache/reuse generated audio when possible
   - Monitor usage via dashboard

4. **File Management:**
   - Use descriptive filenames
   - Organize by type (speech, sfx, music)
   - Clean up temporary files

5. **Testing:**
   - Test with short durations first
   - Verify output quality before long generations
   - Check different voices/settings

## Examples

### Example 1: Audiobook Narration

**User request:** "Convert this chapter to audiobook format"

**Expected behavior:**
1. Select appropriate voice (e.g., narrative voice like George)
2. Use high-quality model (`eleven_multilingual_v2`)
3. Generate speech from chapter text
4. Save as MP3 with high bitrate
5. Report duration and file location

```python
audio = client.text_to_speech.convert(
    text=chapter_text,
    voice_id="JBFqnCBsd6RMkjVDRZzb",  # George
    model_id="eleven_multilingual_v2",
    output_format="mp3_44100_128"
)
save_audio(audio, "chapter_1.mp3")
```

### Example 2: Video Game Sound Effects

**User request:** "Generate sound effects for a fantasy RPG game"

**Expected behavior:**
1. Create multiple sound effects with descriptions
2. Set appropriate durations for each
3. Save with descriptive names
4. Organize in game audio folder

```python
sfx_list = [
    ("sword_swing", "sword whooshing through air, fantasy combat", 1.0),
    ("potion_drink", "drinking magical potion, gulp sound, RPG game", 0.8),
    ("spell_cast", "magical spell casting, ethereal whoosh, fantasy magic", 1.5),
    ("footsteps_stone", "footsteps on stone dungeon floor, echoing", 2.0)
]

for name, description, duration in sfx_list:
    audio = client.text_to_sound_effects.convert(
        text=description,
        duration_seconds=duration
    )
    save_audio(audio, f"sfx_{name}.mp3")
```

### Example 3: Podcast Intro with Music

**User request:** "Create a podcast intro with voice and background music"

**Expected behavior:**
1. Generate intro speech
2. Generate background music
3. Note that mixing would need external tools (pydub)
4. Provide both audio files

```python
# Generate intro speech
intro_text = "Welcome to the Tech Talk podcast, where we discuss the latest in technology and innovation."
speech = client.text_to_speech.convert(
    text=intro_text,
    voice_id="TxGEqnHWrfWFTfGW9XjX",  # Josh (energetic)
    model_id="eleven_flash_v2_5"
)
save_audio(speech, "podcast_intro_voice.mp3")

# Generate background music (requires paid account)
music = client.music_generation.compose(
    prompt="Upbeat tech podcast intro music, electronic beats, modern and energetic",
    music_length_ms=10000  # 10 seconds
)
save_audio(music, "podcast_intro_music.mp3")

print("Use audio editing software to mix voice and music")
```

### Example 4: Multilingual Content

**User request:** "Create welcome messages in English, Spanish, and French"

**Expected behavior:**
1. Generate speech in each language
2. Use multilingual model
3. Select appropriate voices for each language
4. Save with language-specific filenames

```python
messages = {
    "english": ("Hello and welcome!", "JBFqnCBsd6RMkjVDRZzb"),
    "spanish": ("¡Hola y bienvenido!", "ThT5KcBeYPX3keUQqHPh"),  # Spanish voice
    "french": ("Bonjour et bienvenue!", "XB0fDUnXU5powFXDhCwa")   # French voice
}

for lang, (text, voice_id) in messages.items():
    audio = client.text_to_speech.convert(
        text=text,
        voice_id=voice_id,
        model_id="eleven_multilingual_v2"
    )
    save_audio(audio, f"welcome_{lang}.mp3")
```

### Example 5: Real-time Voice Streaming

**User request:** "Stream this news article as audio"

**Expected behavior:**
1. Use Flash model for low latency
2. Stream audio as it generates
3. Provide real-time playback or save incrementally

```python
from elevenlabs import stream

audio_stream = client.text_to_speech.convert_as_stream(
    text=news_article_text,
    voice_id="21m00Tcm4TlvDq8ikWAM",  # Rachel
    model_id="eleven_flash_v2_5",
    output_format="mp3_44100_128"
)

# Stream to speakers in real-time
stream(audio_stream)
```

## Limitations

1. **Music Generation:**
   - Requires paid subscription
   - No copyrighted material allowed
   - Processing time increases with duration

2. **API Quotas:**
   - Character limits per month (tier-dependent)
   - Rate limits on requests
   - Different limits for free vs paid tiers

3. **Voice Cloning:**
   - Not covered in Tier 1 implementation
   - Requires voice samples and additional setup

4. **Audio Quality:**
   - Output format affects quality and file size
   - Higher quality formats may require paid tier
   - Streaming has slightly lower quality than standard

5. **Language Support:**
   - 32 languages supported but quality varies
   - Some voices are language-specific
   - Multilingual model recommended for non-English

6. **Sound Effects:**
   - Limited to description-based generation
   - No editing of generated effects via API
   - Duration limitations (typically under 22 seconds)

7. **Content Policy:**
   - No harmful or copyrighted content
   - Music generation rejects artist/band names
   - Strict content moderation on all endpoints

## Related Skills

- `image-generation` - For visual content creation
- `python-plotting` - For visualizing audio data
- `scientific-writing` - For generating narration text
- `python-best-practices` - For writing clean audio processing code

## Additional Resources

- **ElevenLabs Documentation**: https://elevenlabs.io/docs
- **Python SDK**: https://github.com/elevenlabs/elevenlabs-python
- **API Reference**: https://elevenlabs.io/docs/api-reference/introduction
- **Voice Library**: https://elevenlabs.io/voice-library
- **Pricing**: https://elevenlabs.io/pricing
- **Usage Dashboard**: https://elevenlabs.io/app/usage
