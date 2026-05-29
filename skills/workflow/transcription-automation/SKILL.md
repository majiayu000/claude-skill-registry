---
name: Transcription Automation
description: Automate audio/video transcription, meeting notes, subtitle generation, and content processing
version: 1.0.0
author: Claude Office Skills
category: multimedia
tags:
  - transcription
  - audio
  - video
  - meetings
  - subtitles
department: content
models:
  - claude-3-opus
  - claude-3-sonnet
  - gpt-4
  - whisper
mcp:
  server: media-mcp
  tools:
    - whisper_transcribe
    - assembly_ai
    - deepgram_api
    - subtitle_generate
capabilities:
  - Speech-to-text conversion
  - Meeting transcription
  - Subtitle generation
  - Speaker diarization
input:
  - Audio files
  - Video files
  - Live streams
  - Meeting recordings
output:
  - Text transcripts
  - SRT/VTT subtitles
  - Meeting notes
  - Searchable archives
languages:
  - en
  - zh
  - multi
related_skills:
  - youtube-automation
  - podcast-automation
  - meeting-notes
---

# Transcription Automation

Comprehensive skill for automating audio/video transcription and content processing.

## Core Workflows

### 1. Transcription Pipeline

```
TRANSCRIPTION FLOW:
┌─────────────────┐
│  Audio/Video    │
│     Input       │
└────────┬────────┘
         ▼
┌─────────────────┐
│  Pre-Processing │
│  - Convert      │
│  - Enhance      │
│  - Split        │
└────────┬────────┘
         ▼
┌─────────────────┐
│  Transcription  │
│  - STT Engine   │
│  - Diarization  │
└────────┬────────┘
         ▼
┌─────────────────┐
│ Post-Processing │
│  - Format       │
│  - Timestamps   │
│  - Speakers     │
└────────┬────────┘
         ▼
┌─────────────────┐
│     Output      │
│  - Text/SRT/VTT │
│  - Summary      │
└─────────────────┘
```

### 2. Transcription Configuration

```yaml
transcription_config:
  engine: whisper  # whisper, assembly_ai, deepgram
  
  audio_settings:
    sample_rate: 16000
    channels: mono
    format: wav
    
  transcription:
    language: auto  # or specific: en, zh, es
    model: large  # tiny, base, small, medium, large
    task: transcribe  # transcribe or translate
    
  features:
    speaker_diarization: true
    word_timestamps: true
    punctuation: true
    profanity_filter: false
    
  output:
    formats:
      - txt
      - srt
      - vtt
      - json
    include_confidence: true
    include_timestamps: true
```

## Meeting Transcription

### Meeting Notes Template

```yaml
meeting_transcript:
  metadata:
    title: "{{meeting_title}}"
    date: "{{date}}"
    duration: "{{duration}}"
    attendees: "{{speakers}}"
    
  output_template: |
    # {{title}}
    
    **Date:** {{date}}
    **Duration:** {{duration}}
    **Attendees:** {{attendees}}
    
    ## Summary
    {{ai_summary}}
    
    ## Key Points
    {{#each key_points}}
    - {{this}}
    {{/each}}
    
    ## Action Items
    {{#each action_items}}
    - [ ] {{task}} - @{{assignee}} - Due: {{due_date}}
    {{/each}}
    
    ## Full Transcript
    {{#each segments}}
    **[{{timestamp}}] {{speaker}}:** {{text}}
    
    {{/each}}
```

### Speaker Diarization

```yaml
diarization_config:
  min_speakers: 2
  max_speakers: 10
  
  speaker_labels:
    - name: "Speaker 1"
      voice_sample: "sample_1.wav"  # Optional
    - name: "Speaker 2"
      voice_sample: "sample_2.wav"
      
  output_format:
    speaker_prefix: true
    speaker_timestamps: true
    
  example_output: |
    [00:00:05] SPEAKER_1: Welcome everyone to today's meeting.
    [00:00:12] SPEAKER_2: Thanks for having us.
    [00:00:18] SPEAKER_1: Let's start with the agenda.
```

## Subtitle Generation

### SRT Format

```yaml
subtitle_config:
  format: srt
  
  timing:
    max_duration: 7  # seconds per subtitle
    min_gap: 0.1     # seconds between subtitles
    chars_per_line: 42
    max_lines: 2
    
  style:
    case: sentence  # sentence, upper, lower
    numbers: words  # words, digits
    
  example_output: |
    1
    00:00:05,000 --> 00:00:08,500
    Welcome to today's presentation
    about transcription automation.
    
    2
    00:00:09,000 --> 00:00:12,000
    Let me start by explaining
    the basic concepts.
```

### VTT Format

```yaml
vtt_config:
  format: vtt
  
  features:
    cue_settings: true
    styling: true
    
  example_output: |
    WEBVTT
    
    00:00:05.000 --> 00:00:08.500 align:center
    Welcome to today's presentation
    about transcription automation.
    
    00:00:09.000 --> 00:00:12.000 align:center
    <v Speaker 1>Let me start by explaining
    the basic concepts.
```

## Integration Workflows

### Zoom Integration

```yaml
zoom_transcription:
  trigger:
    event: recording_completed
    
  workflow:
    - step: download_recording
      source: zoom_cloud
      
    - step: transcribe
      engine: whisper
      language: auto
      
    - step: diarize
      identify_speakers: true
      
    - step: generate_notes
      template: meeting_notes
      include_summary: true
      extract_action_items: true
      
    - step: distribute
      destinations:
        - notion_page
        - slack_channel
        - email_attendees
```

### YouTube Integration

```yaml
youtube_subtitles:
  trigger:
    event: video_uploaded
    
  workflow:
    - step: download_audio
      source: youtube_video
      
    - step: transcribe
      engine: whisper
      task: transcribe
      
    - step: generate_subtitles
      formats: [srt, vtt]
      
    - step: translate
      target_languages: [es, zh, ja, de, fr]
      
    - step: upload_subtitles
      destination: youtube
      as_cc: true
```

### Podcast Processing

```yaml
podcast_workflow:
  input:
    source: rss_feed
    format: audio/mp3
    
  processing:
    - transcribe:
        engine: whisper
        model: large
        
    - generate_chapters:
        detect_topics: true
        min_duration: 60  # seconds
        
    - create_show_notes:
        summarize: true
        extract_links: true
        highlight_quotes: true
        
    - create_searchable_index:
        full_text: true
        timestamps: true
        
  output:
    - transcript_txt
    - chapters_json
    - show_notes_md
    - search_index
```

## Language Support

### Multi-Language Transcription

```yaml
multilingual:
  auto_detect: true
  
  supported_languages:
    - code: en
      name: English
      model: large
      
    - code: zh
      name: Chinese
      model: large
      
    - code: es
      name: Spanish
      model: large
      
    - code: ja
      name: Japanese
      model: medium
      
  translation:
    enabled: true
    target: en
    preserve_original: true
```

### Code-Switching

```yaml
code_switching:
  enabled: true
  primary_language: en
  secondary_languages: [zh, es]
  
  output: |
    [00:01:23] The next topic is about 人工智能,
    which has been muy importante in recent years.
    
  handling:
    detect_language_per_segment: true
    tag_language_switches: true
```

## Quality Enhancement

### Post-Processing

```yaml
post_processing:
  text_cleanup:
    - remove_filler_words: ["um", "uh", "like"]
    - fix_common_errors: true
    - normalize_numbers: true
    
  formatting:
    - add_punctuation: true
    - capitalize_sentences: true
    - paragraph_breaks: true
    
  speaker_attribution:
    - merge_short_segments: true
    - min_segment_duration: 1.0
    
  output_enhancement:
    - add_timestamps: true
    - highlight_keywords: true
    - generate_summary: true
```

### Accuracy Metrics

```
TRANSCRIPTION QUALITY REPORT
═══════════════════════════════════════

File: meeting_2024_01_15.mp3
Duration: 45:32
Engine: Whisper Large

METRICS:
Word Error Rate (WER):  4.2%
Character Error Rate:   2.8%
Confidence Score:       0.94

SPEAKER DIARIZATION:
Speakers Detected: 4
Diarization Accuracy: 91%

PROCESSING TIME:
Total: 8m 23s
Real-time Factor: 0.18x

DETECTED ISSUES:
• Low confidence at 12:34 (background noise)
• Overlapping speech at 23:45
• Unknown speaker at 34:12
```

## API Examples

### OpenAI Whisper

```python
import openai

# Transcribe audio
with open("meeting.mp3", "rb") as audio_file:
    transcript = openai.Audio.transcribe(
        model="whisper-1",
        file=audio_file,
        response_format="verbose_json",
        timestamp_granularities=["word", "segment"]
    )

# Access results
for segment in transcript.segments:
    print(f"[{segment.start:.2f}] {segment.text}")
```

### AssemblyAI

```python
import assemblyai as aai

transcriber = aai.Transcriber()

config = aai.TranscriptionConfig(
    speaker_labels=True,
    auto_chapters=True,
    entity_detection=True
)

transcript = transcriber.transcribe(
    "https://example.com/meeting.mp3",
    config=config
)

for utterance in transcript.utterances:
    print(f"Speaker {utterance.speaker}: {utterance.text}")
```

## Best Practices

1. **Quality Audio**: Clean input = better output
2. **Choose Right Model**: Balance speed vs accuracy
3. **Use Diarization**: Identify speakers clearly
4. **Post-Process**: Clean up automated output
5. **Verify Critical Content**: Human review important
6. **Consider Privacy**: Handle sensitive content
7. **Store Efficiently**: Compress and index
8. **Provide Context**: Vocabulary hints help
