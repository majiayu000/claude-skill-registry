---
name: interview-transcription
description: Interview management, transcription workflows, and source note-taking for journalists. Use when preparing for interviews, managing recordings, transcribing audio/video, organizing source notes, creating timestamped references, or building interview databases. Essential for reporters conducting interviews and managing source relationships.
---

# Interview transcription and management

Practical workflows for journalists managing interviews from preparation through publication.

## When to activate

- Preparing questions for an interview
- Processing audio/video recordings
- Creating or managing transcripts
- Organizing notes from multiple sources
- Building a source relationship database
- Generating timestamped quotes for fact-checking
- Converting recordings to publishable quotes

## Pre-interview preparation

### Research checklist

Before recording starts, you should already know:

```markdown
## Source prep for: [Name]

### Background
- Role/title:
- Organization:
- Why they're relevant to this story:
- Previous media appearances (note inconsistencies):

### Key questions (prioritized)
1. [Must-ask question]
2. [Must-ask question]
3. [If time permits]

### Documents to reference
- [ ] Bring/share [specific document]
- [ ] Ask about [specific claim/data point]

### Red lines
- Topics they'll likely avoid:
- Sensitive areas to approach carefully:
```

### Recording setup

```python
# Standard recording configuration
RECORDING_SETTINGS = {
    'format': 'wav',           # Lossless for transcription
    'sample_rate': 44100,      # Standard quality
    'channels': 1,             # Mono is fine for speech
    'backup': True,            # Always run backup recorder
}

# File naming convention
# YYYY-MM-DD_source-lastname_topic.wav
# Example: 2024-03-15_smith_budget-hearing.wav
```

**Two-device rule**: Always record on two devices. Phone as backup minimum.

## Transcription workflows

### Automated transcription pipeline

```python
from pathlib import Path
import subprocess
import json

def transcribe_interview(audio_path: str, output_dir: str = "./transcripts") -> dict:
    """
    Transcribe using Whisper with speaker diarization.
    Returns transcript with timestamps.
    """
    Path(output_dir).mkdir(exist_ok=True)

    # Use whisper.cpp or OpenAI Whisper
    result = subprocess.run([
        'whisper',
        audio_path,
        '--model', 'medium',
        '--output_format', 'json',
        '--output_dir', output_dir,
        '--language', 'en',
        '--word_timestamps', 'True'
    ], capture_output=True)

    # Load and return structured transcript
    json_path = Path(output_dir) / f"{Path(audio_path).stem}.json"
    with open(json_path) as f:
        return json.load(f)

def format_for_editing(transcript: dict) -> str:
    """Convert to journalist-friendly format with timestamps."""
    lines = []
    for segment in transcript.get('segments', []):
        timestamp = format_timestamp(segment['start'])
        text = segment['text'].strip()
        lines.append(f"[{timestamp}] {text}")
    return '\n\n'.join(lines)

def format_timestamp(seconds: float) -> str:
    """Convert seconds to HH:MM:SS format."""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    return f"{h:02d}:{m:02d}:{s:02d}"
```

### Manual transcription template

For sensitive interviews or when AI transcription fails:

```markdown
## Transcript: [Source] - [Date]

**Recording file**: [filename]
**Duration**: [XX:XX]
**Transcribed by**: [name]
**Verified against recording**: [ ] Yes / [ ] No

---

[00:00:15] **Q**: [Your question]

[00:00:45] **A**: [Source response - verbatim, including ums, pauses noted as (...)]

[00:01:30] **Q**: [Follow-up]

[00:01:42] **A**: [Response]

---

## Notes
- [Anything not captured in audio: gestures, documents shown, etc.]

## Potential quotes
- [00:01:42] "Quote that stands out" - context: [why it matters]
```

## Quote extraction and verification

### Pull quotes workflow

```python
from dataclasses import dataclass
from typing import Optional
import re

@dataclass
class Quote:
    text: str
    timestamp: str
    speaker: str
    context: str
    verified: bool = False
    used_in: Optional[str] = None

class QuoteBank:
    """Manage quotes from interview transcripts."""

    def __init__(self):
        self.quotes = []

    def extract_quote(self, transcript: str, start_time: str,
                      end_time: str, speaker: str, context: str) -> Quote:
        """Extract and store a quote with metadata."""
        # Pull text between timestamps
        pattern = rf'\[{re.escape(start_time)}\](.+?)(?=\[\d|$)'
        match = re.search(pattern, transcript, re.DOTALL)

        if match:
            text = match.group(1).strip()
            quote = Quote(
                text=text,
                timestamp=start_time,
                speaker=speaker,
                context=context
            )
            self.quotes.append(quote)
            return quote
        return None

    def verify_quote(self, quote: Quote, audio_path: str) -> bool:
        """Mark quote as verified against original recording."""
        # In practice: listen to audio at timestamp, confirm accuracy
        quote.verified = True
        return True

    def export_for_story(self) -> str:
        """Export verified quotes ready for publication."""
        output = []
        for q in self.quotes:
            if q.verified:
                output.append(f'"{q.text}"\n— {q.speaker}\n[Timestamp: {q.timestamp}]')
        return '\n\n'.join(output)
```

### Quote accuracy checklist

Before publishing any quote:

```markdown
- [ ] Listened to original recording at timestamp
- [ ] Quote is verbatim (or clearly marked as paraphrased)
- [ ] Context preserved (not cherry-picked to change meaning)
- [ ] Speaker identified correctly
- [ ] Timestamp documented for fact-checker
- [ ] Source approved quote (if agreement made)
```

## Source management database

### Interview tracking schema

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from enum import Enum

class SourceStatus(Enum):
    ACTIVE = "active"           # Currently engaged
    DORMANT = "dormant"         # Not recently contacted
    DECLINED = "declined"       # Refused to participate
    OFF_RECORD = "off_record"   # Background only

class InterviewType(Enum):
    ON_RECORD = "on_record"
    BACKGROUND = "background"
    DEEP_BACKGROUND = "deep_background"
    OFF_RECORD = "off_record"

@dataclass
class Source:
    name: str
    organization: str
    contact_info: dict  # email, phone, signal, etc.
    beat: str
    status: SourceStatus = SourceStatus.ACTIVE
    interviews: List['Interview'] = field(default_factory=list)
    notes: str = ""

    # Relationship tracking
    first_contact: Optional[datetime] = None
    trust_level: int = 1  # 1-5 scale

@dataclass
class Interview:
    source: str
    date: datetime
    interview_type: InterviewType
    recording_path: Optional[str] = None
    transcript_path: Optional[str] = None
    story_slug: Optional[str] = None
    key_quotes: List[str] = field(default_factory=list)
    follow_up_needed: bool = False
    notes: str = ""
```

### Quick source lookup

```python
def find_sources_for_story(sources: List[Source], topic: str,
                           beat: str = None) -> List[Source]:
    """Find relevant sources for a new story."""
    matches = []
    for source in sources:
        # Filter by beat if specified
        if beat and source.beat != beat:
            continue
        # Only suggest active sources
        if source.status != SourceStatus.ACTIVE:
            continue
        # Check if they've spoken on similar topics
        for interview in source.interviews:
            if topic.lower() in interview.notes.lower():
                matches.append(source)
                break

    # Sort by trust level
    return sorted(matches, key=lambda s: s.trust_level, reverse=True)
```

## Audio/video processing

### Batch processing multiple recordings

```python
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
import json

def batch_transcribe(recordings_dir: str, output_dir: str) -> dict:
    """Process all recordings in a directory."""
    recordings = list(Path(recordings_dir).glob('*.wav')) + \
                 list(Path(recordings_dir).glob('*.mp3')) + \
                 list(Path(recordings_dir).glob('*.m4a'))

    results = {}

    with ProcessPoolExecutor(max_workers=4) as executor:
        futures = {
            executor.submit(transcribe_interview, str(rec), output_dir): rec
            for rec in recordings
        }

        for future in futures:
            rec = futures[future]
            try:
                transcript = future.result()
                results[rec.name] = {
                    'status': 'success',
                    'transcript': transcript
                }
            except Exception as e:
                results[rec.name] = {
                    'status': 'error',
                    'error': str(e)
                }

    return results
```

### Video interview extraction

```python
import subprocess

def extract_audio_from_video(video_path: str, output_path: str = None) -> str:
    """Extract audio track from video for transcription."""
    if output_path is None:
        output_path = video_path.rsplit('.', 1)[0] + '.wav'

    subprocess.run([
        'ffmpeg', '-i', video_path,
        '-vn',  # No video
        '-acodec', 'pcm_s16le',  # WAV format
        '-ar', '44100',  # Sample rate
        '-ac', '1',  # Mono
        output_path
    ], check=True)

    return output_path
```

## Legal and ethical considerations

### Consent documentation

```markdown
## Recording consent record

**Date**:
**Source name**:
**Recording type**: [ ] Audio [ ] Video
**Interview type**: [ ] On record [ ] Background [ ] Off record

### Consent obtained:
- [ ] Verbal consent recorded at start of interview
- [ ] Written consent form signed
- [ ] Email confirmation of consent

### Jurisdiction notes:
- Interview location state/country:
- One-party or two-party consent jurisdiction:
- Any specific restrictions agreed:

### Agreed terms:
- [ ] Full attribution allowed
- [ ] Organization attribution only
- [ ] Anonymous source
- [ ] Review quotes before publication
- [ ] Embargo until [date]:
```

### Two-party consent states (US)

California, Connecticut, Florida, Illinois, Maryland, Massachusetts, Michigan, Montana, Nevada, New Hampshire, Pennsylvania, Washington require all-party consent.

**Always get explicit consent on recording** regardless of jurisdiction.

## Tools and resources

| Tool | Purpose | Notes |
|------|---------|-------|
| Whisper | Local transcription | Free, accurate, private |
| Otter.ai | Cloud transcription | Real-time, speaker ID |
| Descript | Edit audio like text | Good for pulling clips |
| Rev | Human transcription | For sensitive/legal |
| Trint | Journalist-focused | Collaboration features |
| oTranscribe | Free web player | Manual transcription aid |

## Related skills

- **source-verification** - Verify source credentials before interview
- **foia-requests** - Get documents to inform interview questions
- **data-journalism** - Analyze data sources mention in interviews

---

## Skill metadata

| Field | Value |
|-------|-------|
| Version | 1.0.0 |
| Created | 2025-12-26 |
| Author | Claude Skills for Journalism |
| Domain | Journalism, Research |
| Complexity | Intermediate |
