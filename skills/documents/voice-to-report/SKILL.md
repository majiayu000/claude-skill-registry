---
name: voice-to-report
description: "Convert voice recordings to structured construction reports. Field workers speak, AI transcribes and formats. Supports daily reports, safety observations, progress updates."
---

# Voice to Report

## Overview

Field workers prefer talking over typing. This skill converts voice recordings into structured construction reports using speech-to-text and LLM processing.

## Why Voice?

| Typing | Voice |
|--------|-------|
| Slow on mobile | 3x faster |
| Requires attention | Hands-free |
| Limited in cold/rain | Works anywhere |
| Formal language | Natural expression |
| Short messages | Detailed descriptions |

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    VOICE TO REPORT PIPELINE                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  🎤 Voice      →    📝 Transcribe    →    🤖 Structure    →    📊 Report │
│  Recording         Whisper API           GPT-4o               Formatted  │
│                                                                  │
│  "We finished      "We finished         {                    Daily Report │
│   the foundation    the foundation       "activity":         ──────────── │
│   pour today,       pour today,          "foundation",       Foundation   │
│   about 500         about 500            "quantity": 500,    pour: 500m³  │
│   cubic meters"     cubic meters"        "unit": "m³"        Complete ✓   │
│                                          }                               │
└─────────────────────────────────────────────────────────────────┘
```

## Quick Start

```python
from openai import OpenAI
import json

client = OpenAI()

def voice_to_report(audio_path: str, report_type: str = "daily") -> dict:
    """Convert voice recording to structured report"""

    # Step 1: Transcribe audio
    with open(audio_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            language="en"
        )

    # Step 2: Structure with LLM
    schema = get_report_schema(report_type)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": f"""You are a construction report assistant.
                Convert the voice transcript into a structured report.
                Extract all relevant information and format as JSON.

                Report type: {report_type}
                Schema: {json.dumps(schema, indent=2)}

                Rules:
                - Extract quantities with units
                - Identify activities and locations
                - Note any issues or concerns
                - Capture weather if mentioned
                - List workers/trades if mentioned
                """
            },
            {
                "role": "user",
                "content": f"Transcript:\n{transcript.text}"
            }
        ],
        response_format={"type": "json_object"}
    )

    return {
        "transcript": transcript.text,
        "structured_report": json.loads(response.choices[0].message.content)
    }
```

## Report Schemas

### Daily Report Schema

```python
daily_report_schema = {
    "date": "YYYY-MM-DD",
    "project": "string",
    "weather": {
        "conditions": "string",
        "temperature": "number",
        "impact": "none|minor|major"
    },
    "workforce": [
        {
            "trade": "string",
            "count": "number",
            "hours": "number"
        }
    ],
    "activities": [
        {
            "description": "string",
            "location": "string",
            "quantity": "number",
            "unit": "string",
            "status": "in_progress|completed|delayed"
        }
    ],
    "equipment": [
        {
            "type": "string",
            "hours": "number"
        }
    ],
    "issues": [
        {
            "description": "string",
            "severity": "low|medium|high",
            "action_taken": "string"
        }
    ],
    "notes": "string"
}
```

### Safety Observation Schema

```python
safety_schema = {
    "date": "YYYY-MM-DD",
    "time": "HH:MM",
    "location": "string",
    "observer": "string",
    "observation_type": "positive|concern|incident",
    "description": "string",
    "people_involved": ["list of names/roles"],
    "immediate_action": "string",
    "follow_up_required": "boolean",
    "photos_attached": "boolean"
}
```

### Progress Update Schema

```python
progress_schema = {
    "date": "YYYY-MM-DD",
    "area": "string",
    "activity": "string",
    "planned_quantity": "number",
    "actual_quantity": "number",
    "unit": "string",
    "percent_complete": "number",
    "on_schedule": "boolean",
    "variance_reason": "string or null",
    "next_steps": "string"
}
```

## n8n Workflow

```json
{
  "workflow": "Voice to Report",
  "nodes": [
    {
      "name": "Telegram Trigger",
      "type": "Telegram",
      "event": "voice_message"
    },
    {
      "name": "Download Voice",
      "type": "Telegram",
      "action": "getFile"
    },
    {
      "name": "Transcribe",
      "type": "OpenAI",
      "operation": "transcribe",
      "model": "whisper-1"
    },
    {
      "name": "Detect Report Type",
      "type": "OpenAI",
      "prompt": "Classify: daily_report, safety, progress, issue"
    },
    {
      "name": "Structure Report",
      "type": "OpenAI",
      "operation": "chat",
      "model": "gpt-4o"
    },
    {
      "name": "Save to Database",
      "type": "PostgreSQL"
    },
    {
      "name": "Confirm to User",
      "type": "Telegram",
      "action": "sendMessage"
    },
    {
      "name": "Generate PDF",
      "type": "HTTP Request",
      "url": "pdf-service/generate"
    }
  ]
}
```

## Multi-Language Support

```python
def transcribe_multilingual(audio_path: str) -> dict:
    """Transcribe in any language, output in English"""

    with open(audio_path, "rb") as audio_file:
        # Detect language automatically
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
            # language parameter omitted for auto-detection
        )

    # Translate to English if needed
    if not is_english(transcript.text):
        translation = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Translate to English, preserve construction terminology."},
                {"role": "user", "content": transcript.text}
            ]
        )
        english_text = translation.choices[0].message.content
    else:
        english_text = transcript.text

    return {
        "original": transcript.text,
        "english": english_text
    }
```

## Mobile App Integration

```python
# Example: Flutter/React Native integration

# Send voice to API
async def upload_voice_report(audio_bytes, project_id):
    response = await api.post(
        "/voice-report",
        files={"audio": audio_bytes},
        data={
            "project_id": project_id,
            "report_type": "daily"
        }
    )
    return response.json()

# Response includes:
# - transcript
# - structured_report
# - report_id
# - pdf_url (if generated)
```

## Cost Optimization

```python
# Use local Whisper for high volume
import whisper

model = whisper.load_model("base")  # or "small", "medium", "large"

def transcribe_local(audio_path: str) -> str:
    """Transcribe locally to save API costs"""
    result = model.transcribe(audio_path)
    return result["text"]

# Cost comparison (per hour of audio):
# - OpenAI Whisper API: $0.36
# - Local Whisper (base): $0 (compute only)
# - Local Whisper (large): $0 (compute only, slower)
```

## Requirements

```bash
pip install openai whisper python-telegram-bot
```

## Resources

- OpenAI Whisper: https://platform.openai.com/docs/guides/speech-to-text
- Local Whisper: https://github.com/openai/whisper
- n8n Voice Processing: https://docs.n8n.io/integrations/
