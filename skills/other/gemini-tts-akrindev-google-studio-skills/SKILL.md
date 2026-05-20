---
name: gemini-tts
description: Generate speech from text using Google Gemini TTS models via scripts/. Use for text-to-speech, audio generation, voice synthesis, multi-speaker conversations, and creating audio content. Supports multiple voices and streaming. Triggers on "text to speech", "TTS", "generate audio", "voice synthesis", "speak this text".
license: MIT
version: 1.0.0
keywords: text-to-speech, TTS, audio generation, voice synthesis, multi-speaker, streaming, Kore, Puck, Charon, Fenrir, Aoede, Zephyr
---

# Gemini Text-to-Speech

Generate natural-sounding speech from text using Gemini's TTS models through executable scripts with support for multiple voices and multi-speaker conversations.

## When to Use This Skill

Use this skill when you need to:
- Convert text to natural speech
- Create audio for podcasts, audiobooks, or videos
- Generate multi-speaker conversations
- Stream audio for long content
- Choose from multiple voice options
- Create accessible audio content
- Generate voiceovers for presentations
- Batch convert text to audio files

## Available Scripts

### scripts/tts.py
**Purpose**: Convert text to speech using Gemini TTS models

**When to use**:
- Any text-to-speech conversion
- Multi-speaker conversation generation
- Streaming audio for long texts
- Voiceovers for content creation
- Accessible audio generation

**Key parameters**:
| Parameter | Description | Example |
|-----------|-------------|---------|
| `text` | Text to convert (required) | `"Hello, world!"` |
| `--voice`, `-v` | Voice name | `Kore` |
| `--output`, `-o` | Base name for output file | `welcome` |
| `--output-dir` | Output directory for audio | `audio/` |
| `--no-timestamp` | Disable auto timestamp | Flag |
| `--model`, `-m` | TTS model | `gemini-2.5-flash-preview-tts` |
| `--stream`, `-s` | Enable streaming | Flag |
| `--speakers` | Multi-speaker mapping | `"Joe:Kore,Jane:Puck"` |

**Output**: WAV audio file path

## Workflows

### Workflow 1: Basic Text-to-Speech
```bash
python scripts/tts.py "Hello, world! Have a wonderful day."
```
- Best for: Quick audio generation, simple messages
- Voice: `Kore` (default, clear and professional)
- Output: `audio/tts_output_YYYYMMDD_HHMMSS.wav` (auto timestamp)

### Workflow 2: Choose Different Voice
```bash
python scripts/tts.py "Welcome to our podcast about technology trends" --voice Puck --output welcome
```
- Best for: Friendly, conversational content
- Voice options: Kore, Puck, Charon, Fenrir, Aoede, Zephyr, Sulafat
- Output: `audio/welcome_YYYYMMDD_HHMMSS.wav`

### Workflow 3: Multi-Speaker Conversation
```bash
python scripts/tts.py "TTS the following conversation:
Joe: How's it going today?
Jane: Not too bad, how about you?
Joe: I'm working on a new project.
Jane: Sounds exciting, tell me more!" --speakers "Joe:Kore,Jane:Puck" --output conversation
```
- Best for: Dialogues, interviews, role-playing content
- Format: Marked conversation with speaker names
- Script automatically routes text to appropriate voices
- Output: `audio/conversation_YYYYMMDD_HHMMSS.wav`

### Workflow 4: Long Content with Streaming
```bash
python scripts/tts.py "This is a very long text that would benefit from streaming..." --stream --output long-form
```
- Best for: Podcasts, audiobooks, long articles
- Streaming: Processes audio in chunks for long texts
- Output: `audio/long-form_YYYYMMDD_HHMMSS.wav`

### Workflow 5: Professional Voiceover
```bash
python scripts/tts.py "Welcome to our quarterly earnings presentation. Today we'll discuss our growth metrics and future plans." --voice Charon --output voiceover
```
- Best for: Corporate content, presentations, formal announcements
- Voice: `Charon` (deep, authoritative)
- Use when: Professional, serious tone required

### Workflow 6: Custom Output Directory
```bash
python scripts/tts.py "Save to specific folder." --output-dir ./my-projects/podcasts/ --output episode1
```
- Best for: Organized project structures
- Directory created automatically if it doesn't exist
- Output: `./my-projects/podcasts/episode1_YYYYMMDD_HHMMSS.wav`

### Workflow 7: Content Creation Pipeline (Text → Audio)
```bash
# 1. Generate script (gemini-text skill)
python skills/gemini-text/scripts/generate.py "Write a 2-minute podcast intro about sustainable energy"

# 2. Generate audio (this skill)
python scripts/tts.py "[Paste generated script]" --voice Fenrir --output podcast-intro

# 3. Use in video or podcast
```
- Best for: Podcasts, audiobooks, video narration
- Combines with: gemini-text for script generation

### Workflow 8: Accessible Content
```bash
python scripts/tts.py "Welcome to our accessible website. This audio describes our main navigation options." --voice Aoede --output accessibility
```
- Best for: Web accessibility, screen reader alternatives
- Voice: `Aoede` (melodic, pleasant)
- Use when: Making content accessible to visually impaired users

### Workflow 9: Educational Content
```bash
python scripts/tts.py "Chapter 1: Introduction to Quantum Computing. Let's explore the fundamental principles..." --voice Zephyr --output chapter1
```
- Best for: Educational materials, tutorials, e-learning
- Voice: `Zephyr` (light, airy)
- Combines well with: gemini-text for content generation

### Workflow 10: Disable Timestamp
```bash
python scripts/tts.py "Fixed filename." --output my-audio --no-timestamp
```
- Best for: When you want complete control over filename
- Output: `audio/my-audio.wav` (no timestamp)
- Use when: Generating files for specific naming schemes

## Parameters Reference

### Model Selection

| Model | Quality | Speed | Best For |
|-------|---------|-------|----------|
| `gemini-2.5-flash-preview-tts` | Good | Fast | General use, high volume |
| `gemini-2.5-pro-preview-tts` | Higher | Slower | Premium content, voiceovers |

### Voice Selection

| Voice | Characteristics | Best For |
|-------|----------------|----------|
| **Kore** | Clear, professional | Announcements, general purpose (default) |
| **Puck** | Friendly, conversational | Casual content, interviews |
| **Charon** | Deep, authoritative | Corporate, serious content |
| **Fenrir** | Warm, expressive | Storytelling, narratives |
| **Aoede** | Melodic, pleasant | Educational, accessibility |
| **Zephyr** | Light, airy | Gentle content, tutorials |
| **Sulafat** | Neutral, balanced | Documentaries, factual content |

### Audio Format

| Specification | Value |
|--------------|-------|
| Format | WAV (PCM) |
| Sample rate | 24000 Hz |
| Channels | 1 (mono) |
| Bit depth | 16-bit |

### Token Limits

| Limit | Type | Description |
|-------|------|-------------|
| 8,192 | Input | Maximum input text tokens |
| 16,384 | Output | Maximum output audio tokens |

## Output Interpretation

### Audio File
- Format: WAV (compatible with most players)
- Mono channel (single audio track)
- Sample rate: 24000 Hz (broadcast quality)
- Can be converted to MP3/AAC if needed

### Multi-Speaker Files
- Single WAV file with multiple voices
- Voices separated by timing within file
- Use `--speakers` parameter to map speakers to voices

### Streaming Output
- Audio processed in chunks during generation
- Script shows "Streaming audio..." message
- Useful for very long texts or real-time applications

## Common Issues

### "google-genai not installed"
```bash
pip install google-genai
```

### "Voice name not found"
- Check voice name spelling
- Use available voices: Kore, Puck, Charon, Fenrir, Aoede, Zephyr, Sulafat
- Voice names are case-sensitive

### "No audio generated"
- Check text is not empty
- Verify text doesn't exceed token limit (8,192)
- Try shorter text segments
- Check API quota limits

### "Multi-speaker format error"
- Format: `SpeakerName:VoiceName,Speaker2:Voice2`
- Separate speakers with commas
- Use colon between speaker and voice
- Example: `"Joe:Kore,Jane:Puck,Host:Charon"`

### "Output file already exists"
- Script will overwrite existing files
- Change `--output` filename to avoid conflicts
- Use unique names for batch generation

### Audio quality issues
- Check input text for unusual characters
- Try different voice for better pronunciation
- Consider splitting long text into smaller segments
- Verify audio playback software compatibility

## Best Practices

### Voice Selection
- **Kore**: General purpose, clear articulation
- **Puck**: Conversational, engaging tone
- **Charon**: Professional, authoritative
- **Fenrir**: Emotional, storytelling
- **Aoede**: Soft, gentle for accessibility
- **Zephyr**: Educational, clear explanations

### Text Preparation
- Use natural language and punctuation
- Include pauses with commas and periods
- Spell out difficult words if needed
- Break very long text into logical segments
- Add speaker labels for multi-speaker content

### Performance Optimization
- Use streaming for very long texts
- Generate shorter segments for better control
- Use flash model for faster generation
- Batch process multiple files for efficiency

### Quality Tips
- Test different voices for your content type
- Use appropriate pacing with punctuation
- Consider context when selecting voice
- Listen to output before final use
- Multi-speaker requires clear speaker labeling

### Use Cases by Voice

| Voice | Ideal Use Cases |
|-------|-----------------|
| Kore | Announcements, navigation, general info |
| Puck | Podcasts, interviews, casual content |
| Charon | Corporate, news, formal presentations |
| Fenrir | Audiobooks, stories, emotional content |
| Aoede | Accessibility, educational, gentle content |
| Zephyr | Tutorials, explanations, guides |
| Sulafat | Documentaries, factual presentations |

## Related Skills

- **gemini-text**: Generate scripts and text for TTS
- **gemini-image**: Create visuals to accompany audio
- **gemini-batch**: Process multiple TTS requests efficiently
- **gemini-files**: Upload audio files for processing

## Quick Reference

```bash
# Basic
python scripts/tts.py "Your text here"

# Custom voice
python scripts/tts.py "Your text" --voice Puck --output audio.wav

# Multi-speaker
python scripts/tts.py "Joe: Hi. Jane: Hello!" --speakers "Joe:Kore,Jane:Puck"

# Streaming
python scripts/tts.py "Long text..." --stream --output long.wav

# Professional
python scripts/tts.py "Corporate announcement" --voice Charon
```

## Reference

- See `references/voices.md` for complete voice documentation
- Get API key: https://aistudio.google.com/apikey
- Documentation: https://ai.google.dev/gemini-api/docs/text-to-speech
- Sample rate: 24000 Hz standard for most applications
