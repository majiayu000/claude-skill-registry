---
name: openai-whisper
cluster: community
description: "Local Whisper: audio transcription, multi-language, word timestamps, speaker diarization"
tags: ["whisper","transcription","audio","local"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "whisper local transcription audio speech to text timestamps"
---

## Purpose

This skill enables local audio transcription using the OpenAI Whisper model, processing files directly on the device for privacy and speed. It's ideal for converting speech to text with features like multi-language support, word-level timestamps, and speaker diarization.

## When to Use

Use this skill for tasks involving local audio files, such as transcribing interviews, podcasts, or meetings, when you need offline processing to avoid network dependencies or data privacy concerns. Apply it in workflows requiring accurate timestamps or speaker identification, like content creation or analysis.

## Key Capabilities

- **Transcription**: Converts audio to text in over 90 languages; specify language via `--language` flag (e.g., `--language en` for English).
- **Timestamps**: Outputs word-level timings; enable with `--word-level` for detailed segments (e.g., each word's start/end in seconds).
- **Speaker Diarization**: Identifies speakers in audio; requires additional setup like Pyannote library; use `--diarize` flag if configured.
- **Multi-Format Support**: Handles input formats like MP3, WAV, or FLAC; outputs JSON or SRT for easy parsing.
- **Model Selection**: Choose from models like tiny, base, small, medium, or large; larger models improve accuracy but increase compute needs (e.g., `--model medium`).

## Usage Patterns

Always run Whisper in a Python environment with the library installed. For basic transcription, load an audio file and specify options via CLI. Use it in pipelines by piping output to other tools, like text analysis skills. For speaker diarization, ensure dependencies are installed first. Example 1: Transcribe a short audio clip for note-taking. Example 2: Process a multi-speaker recording for meeting summaries.

To accomplish transcription:
1. Install dependencies: Run `pip install git+https://github.com/openai/whisper.git pyannote.audio` in your environment.
2. Load and process audio: Use the Whisper CLI to handle files directly.
3. Handle outputs: Parse JSON results for timestamps and integrate into larger scripts.

## Common Commands/API

Use the Whisper CLI for quick tasks. For API integration, call the Python library directly.

- **CLI Command for Basic Transcription**:  
  `whisper path/to/audio.mp3 --model base --language en --output_format json`  
  This transcribes the file, saves output as JSON, and includes timestamps.

- **CLI with Timestamps and Diarization**:  
  `whisper path/to/audio.wav --model medium --word-level --diarize`  
  Generates word-level timings and speaker labels; ensure diarization is configured via Pyannote.

- **Python API Snippet**:  
  ```python  
  import whisper  
  model = whisper.load_model("base")  
  result = model.transcribe("path/to/audio.mp3", language="en")  
  print(result["text"])  # Outputs transcribed text
  ```

- **Config Format**: Whisper uses a simple JSON config for batch processing; example:  
  `{ "model": "small", "language": "es", "task": "transcribe" }`  
  Pass via `--config config.json` in CLI. No auth keys needed for local use; if extending to cloud services, use env vars like `$WHISPER_API_KEY` for external APIs.

To use in code: Import the library, load the model, and call `transcribe()` with parameters like `fp` for file path and `task` for mode (e.g., `task="transcribe"`).

## Integration Notes

Integrate Whisper into AI workflows by wrapping it in Python scripts or CLI calls. For example, chain with text processing tools: Pipe JSON output to a sentiment analysis skill. Use in Jupyter notebooks for interactive transcription. Ensure your environment has GPU support for faster processing (e.g., via CUDA). To embed in larger applications, handle file I/O explicitly: Read audio files using `soundfile` library, then pass to Whisper. For multi-step tasks, use subprocess to call Whisper CLI from other scripts, capturing stdout for JSON parsing.

## Error Handling

Common errors include missing dependencies, invalid audio formats, or out-of-memory issues with large models. To handle:
- **File Not Found**: Check file paths before running; use try-except in Python:  
  ```python  
  try:  
      result = model.transcribe("path/to/audio.mp3")  
  except FileNotFoundError:  
      print("Audio file missing; verify path.")  
  ```
- **Model Load Failures**: Ensure sufficient RAM; fallback to smaller models if needed (e.g., switch `--model large` to `--model base`).
- **Diarization Errors**: If Pyannote fails, verify installation with `pip check pyannote.audio`; log errors and retry with basic transcription.
- **General Pattern**: Wrap CLI calls in scripts using `subprocess` and check return codes; for API, catch exceptions like `whisper.utils.DecodeError` and retry with different parameters.

Always log detailed errors (e.g., via Python's logging module) and provide user-friendly messages, such as "Error: Audio too long for selected model; try a smaller one."

## Graph Relationships

- Relates to: "audio-processing" cluster for upstream tasks like noise reduction.
- Connected to: "text-analysis" skills for downstream processing of transcription outputs.
- Links with: "openai-gpt" for enhancing transcripts with AI summaries.
