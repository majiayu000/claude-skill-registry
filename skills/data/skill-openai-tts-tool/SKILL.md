---
name: skill-openai-tts-tool
description: CLI tool for OpenAI text-to-speech synthesis
---

# When to use
- When you need to convert text to speech using OpenAI's TTS API
- When you need to list available voices and models
- When you need to check API configuration

# OpenAI TTS Tool Skill

## Purpose

A comprehensive CLI utility for text-to-speech synthesis using OpenAI's advanced TTS models. Supports multiple voices, languages, and output formats with professional-grade audio quality.

## When to Use This Skill

**Use this skill when:**
- Converting text documents to audio for accessibility
- Creating voice-overs for presentations or videos
- Generating speech samples for testing or development
- Batch processing multiple text inputs to audio
- Needing high-quality TTS with natural-sounding voices

**Do NOT use this skill for:**
- Real-time streaming TTS (this tool processes complete text)
- Voice cloning or custom voice creation
- Speech recognition or transcription
- Audio editing or post-processing

## CLI Tool: openai-tts-tool

A modern Python CLI tool for accessing OpenAI's Text-to-Speech API with comprehensive features including multiple voice models, configurable output formats, and extensive customization options.

### Installation

```bash
# Clone repository
git clone https://github.com/dnvriend/openai-tts-tool.git
cd openai-tts-tool

# Install with mise
mise use -g python@3.14
uv sync
uv tool install .

# Or run locally
uv run openai-tts-tool --help
```

### Prerequisites

- Python 3.14+ installed
- OpenAI API key (set as OPENAI_API_KEY environment variable)
- `mise` for Python version management (recommended)
- `uv` package manager for modern Python dependency management

### Quick Start

```bash
# Basic text-to-speech conversion
openai-tts-tool synthesize "Hello, world!"

# Check API configuration
openai-tts-tool info

# List available voices
openai-tts-tool list-voices
```

## Progressive Disclosure

<details>
<summary><strong>📖 Core Commands (Click to expand)</strong></summary>

### synthesize - Convert Text to Speech

The primary command for converting text input into high-quality audio files using OpenAI's TTS models.

**Usage:**
```bash
openai-tts-tool synthesize TEXT [OPTIONS]
```

**Arguments:**
- `TEXT`: The text content to convert to speech (required). Can be a single word, sentence, or full paragraph.

**Options:**
- `--voice VOICE` / `-V VOICE`: Select voice model (default: alloy)
  - Available voices: alloy, echo, fable, onyx, nova, shimmer
- `--model MODEL` / `-m MODEL`: Choose TTS model (default: tts-1)
  - `tts-1`: Standard quality, lower latency
  - `tts-1-hd`: Higher quality, slightly higher cost
- `--output FILE` / `-o FILE`: Output audio file path (default: output.mp3)
  - Supports: .mp3, .wav, .ogg, .flac formats
- `--speed SPEED` / `-s SPEED`: Speech playback speed (default: 1.0)
  - Range: 0.25 (very slow) to 4.0 (very fast)
  - Recommended: 0.8-1.2 for natural speech

**Examples:**
```bash
# Basic usage with default settings
openai-tts-tool synthesize "Welcome to our presentation"

# Use specific voice and output file
openai-tts-tool synthesize "Chapter 1: Introduction" \
  --voice nova \
  --output chapter1.mp3

# High-quality model with slower speech
openai-tts-tool synthesize "Important safety information" \
  --model tts-1-hd \
  --speed 0.8 \
  --voice onyx

# Multiple sentences for narration
openai-tts-tool synthesize "In today's lecture, we will explore the fascinating world of artificial intelligence and its impact on modern society." \
  --voice shimmer \
  --output narration.mp3

# Batch processing (loop in shell)
for text in "Hello" "Goodbye" "Thank you"; do
  openai-tts-tool synthesize "$text" --output "${text}.mp3"
done
```

**Output:**
Generates an audio file in the specified format containing the synthesized speech. The file quality and characteristics depend on the selected model and voice options.

---

### list-voices - Display Available Voices

List all available OpenAI TTS voice models with their characteristics and language support.

**Usage:**
```bash
openai-tts-tool list-voices [OPTIONS]
```

**Options:**
- `--format FORMAT` / `-f FORMAT`: Output display format
  - `table`: Human-readable table format (default)
  - `json`: Machine-readable JSON format for scripting

**Examples:**
```bash
# Show voices in table format
openai-tts-tool list-voices

# Export voice information to JSON
openai-tts-tool list-voices --format json > voices.json

# Filter for English voices using jq
openai-tts-tool list-voices --format json | \
  jq '.[] | select(.language | startswith("en"))'

# Get voice descriptions only
openai-tts-tool list-voices --format json | \
  jq -r '.[] | "\(.name): \(.description)"'
```

**Output:**
Returns a list of available voices including:
- Voice name (alloy, echo, fable, onyx, nova, shimmer)
- Description of voice characteristics
- Supported languages and accents
- Recommended use cases

---

### list-models - Display Available TTS Models

Show all available OpenAI TTS models with their specifications and capabilities.

**Usage:**
```bash
openai-tts-tool list-models [OPTIONS]
```

**Options:**
- `--format FORMAT` / `-f FORMAT`: Output display format
  - `table`: Human-readable table format (default)
  - `json`: Machine-readable JSON format for scripting

**Examples:**
```bash
# Show models in table format
openai-tts-tool list-models

# Export model information to JSON
openai-tts-tool list-models --format json > models.json

# Compare model capabilities
openai-tts-tool list-models --format json | \
  jq '.[] | {name: .name, quality: .quality, latency: .latency}'

# Get HD model information only
openai-tts-tool list-models --format json | \
  jq '.[] | select(.name | contains("hd"))'
```

**Output:**
Returns available TTS models including:
- Model identifier (tts-1, tts-1-hd)
- Audio quality characteristics
- Latency and performance information
- Cost differences and use case recommendations

---

### info - System Configuration and Status

Display current configuration, API key status, and system information.

**Usage:**
```bash
openai-tts-tool info [OPTIONS]
```

**Options:**
- `--format FORMAT` / `-f FORMAT`: Output display format
  - `table`: Human-readable table format (default)
  - `json`: Machine-readable JSON format for scripting

**Examples:**
```bash
# Show basic system information
openai-tts-tool info

# Check API key status for automation
openai-tts-tool info --format json | jq '.api_key.status'

# Verify configuration before batch processing
if openai-tts-tool info --format json | jq -e '.api_key.valid'; then
  echo "API key valid, starting batch processing..."
else
  echo "API key invalid, please check configuration"
fi

# Get version information
openai-tts-tool info --format json | jq '.version'
```

**Output:**
Returns system configuration including:
- API key validation status
- Tool version information
- Supported output formats
- Network connectivity status
- Rate limiting information

---

### completion - Shell Auto-Completion

Generate shell completion scripts to enable tab completion for bash, zsh, and fish shells.

**Usage:**
```bash
openai-tts-tool completion SHELL
```

**Arguments:**
- `SHELL`: Target shell type (required)
  - `bash`: Generate bash completion script
  - `zsh`: Generate zsh completion script
  - `fish`: Generate fish completion script

**Examples:**
```bash
# Generate bash completion and eval immediately
eval "$(openai-tts-tool completion bash)"

# Save completion to permanent file
openai-tts-tool completion zsh > ~/.oh-my-zsh/completions/_openai-tts-tool

# Install fish completion
openai-tts-tool completion fish > ~/.config/fish/completions/openai-tts-tool.fish

# Add to bashrc for permanent installation
echo 'eval "$(openai-tts-tool completion bash)"' >> ~/.bashrc

# Test completion generation
openai-tts-tool completion bash | head -10
```

**Output:**
Returns a shell-specific completion script that provides:
- Command and subcommand completion
- Option flag completion
- Argument suggestions where applicable
- Help text display on completion

</details>

<details>
<summary><strong>⚙️ Advanced Features (Click to expand)</strong></summary>

### Multi-Level Verbosity

The tool supports progressive verbosity levels for debugging and monitoring:

```bash
# Default (WARNING level) - quiet operation
openai-tts-tool synthesize "Hello"

# INFO level (-v) - high-level operations
openai-tts-tool -v synthesize "Hello"

# DEBUG level (-vv) - detailed debugging with line numbers
openai-tts-tool -vv synthesize "Hello"

# TRACE level (-vvv) - includes OpenAI and HTTP library internals
openai-tts-tool -vvv synthesize "Hello"
```

### Environment Configuration

Configure the tool using environment variables:

```bash
# Set OpenAI API key
export OPENAI_API_KEY="sk-..."

# Set default output directory
export OPENAI_TTS_OUTPUT_DIR="./audio"

# Set default voice preference
export OPENAI_TTS_VOICE="nova"

# Enable verbose logging by default
export OPENAI_TTS_VERBOSE=2
```

### Output Format Support

Generate audio in multiple formats based on file extension:

```bash
# MP3 format (default, compressed)
openai-tts-tool synthesize "Hello" --output speech.mp3

# WAV format (uncompressed, high quality)
openai-tts-tool synthesize "Hello" --output speech.wav

# OGG format (open source, compressed)
openai-tts-tool synthesize "Hello" --output speech.ogg

# FLAC format (lossless compression)
openai-tts-tool synthesize "Hello" --output speech.flac
```

### Voice Characteristics

Different voices optimized for different use cases:

```bash
# alloy - balanced, neutral tone (default)
openai-tts-tool synthesize "Factual information" --voice alloy

# echo - conversational, friendly
openai-tts-tool synthesize "Welcome message" --voice echo

# fable - storytelling, expressive
openai-tts-tool synthesize "Once upon a time" --voice fable

# onyx - professional, deep voice
openai-tts-tool synthesize "Business presentation" --voice onyx

# nova - bright, energetic
openai-tts-tool synthesize "Exciting announcement" --voice nova

# shimmer - gentle, soothing
openai-tts-tool synthesize "Meditation guide" --voice shimmer
```

</details>

<details>
<summary><strong>🔧 Troubleshooting (Click to expand)</strong></summary>

### Common Issues

**Issue: Invalid OpenAI API key**
```bash
# Symptom
Error: Invalid OpenAI API key

# Solution
export OPENAI_API_KEY="YOUR_API_KEY"
openai-tts-tool info  # Verify the key works
```

**Issue: Audio file not created**
```bash
# Symptom
Command completes but no output file

# Solution with verbose output
openai-tts-tool -vv synthesize "test" --output test.mp3

# Check directory permissions
ls -la "$(pwd)"
touch test_write.tmp && rm test_write.tmp
```

**Issue: Network connectivity problems**
```bash
# Symptom
Connection timeout or network errors

# Solution with trace logging
openai-tts-tool -vvv synthesize "test"

# Test basic connectivity
curl -I https://api.openai.com/v1/models
```

**Issue: Voice not recognized**
```bash
# Symptom
Error: Voice 'xyz' not supported

# Solution - list available voices
openai-tts-tool list-voices

# Use a valid voice
openai-tts-tool synthesize "test" --voice alloy
```

**Issue: Audio quality poor**
```bash
# Symptom
Audio sounds robotic or low quality

# Solution - use HD model
openai-tts-tool synthesize "test" --model tts-1-hd

# Adjust speed for natural speech
openai-tts-tool synthesize "test" --speed 0.9
```

### Getting Help

```bash
# Show main help
openai-tts-tool --help

# Show command-specific help
openai-tts-tool synthesize --help
openai-tts-tool list-voices --help

# Check version and configuration
openai-tts-tool info --format json

# Test API connectivity
openai-tts-tool info --verbose
```

### Performance Tips

```bash
# Use tts-1 for faster processing (lower quality)
openai-tts-tool synthesize "quick test" --model tts-1

# Use tts-1-hd for better quality (slower)
openai-tts-tool synthesize "final version" --model tts-1-hd

# Batch process multiple texts efficiently
for file in *.txt; do
  openai-tts-tool synthesize "$(cat "$file")" --output "${file%.txt}.mp3"
done
```

</details>

## Exit Codes

- `0`: Success - operation completed successfully
- `1`: Client Error - invalid arguments, missing API key, file not found
- `2`: Server Error - OpenAI API server issues, rate limiting
- `3`: Network Error - connectivity problems, timeouts
- `4`: Configuration Error - invalid setup, permissions issues

## Output Formats

**Audio Formats:**
- **MP3**: Default format, good compression, widely supported
- **WAV**: Uncompressed, highest quality, larger file sizes
- **OGG**: Open source format, good compression quality ratio
- **FLAC**: Lossless compression, high quality, medium file sizes

**Data Formats:**
- **Table**: Human-readable format with aligned columns
- **JSON**: Machine-readable format for scripting and automation

## Best Practices

1. **API Key Security**: Never commit API keys to version control. Use environment variables or secure credential storage.

2. **Voice Selection**: Test different voices with your content type - some voices work better for specific content (e.g., onyx for professional content, fable for storytelling).

3. **Quality vs Speed**: Use `tts-1` for testing/prototyping and `tts-1-hd` for final production audio.

4. **File Organization**: Use descriptive filenames and organize output files by project or content type.

5. **Batch Processing**: For multiple files, use shell scripting to process efficiently and handle errors.

6. **Speed Optimization**: Adjust speed between 0.8-1.2 for most natural speech; extreme speeds may sound artificial.

7. **Text Preparation**: Clean input text of special characters and formatting for best synthesis results.

## Resources

- **GitHub Repository**: https://github.com/dnvriend/openai-tts-tool
- **OpenAI TTS Documentation**: https://platform.openai.com/docs/guides/text-to-speech
- **OpenAI API Reference**: https://platform.openai.com/docs/api-reference/audio/createSpeech
- **Voice Samples**: https://platform.openai.com/docs/guides/text-to-speech/voice-options
- **Pricing Information**: https://openai.com/pricing
