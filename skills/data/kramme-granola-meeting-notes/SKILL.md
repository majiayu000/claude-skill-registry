---
name: kramme:granola-meeting-notes
description: Extract and query meeting notes from Granola (macOS/Windows). Use when users ask about their meetings, meeting notes, attendees, or want to find information from past meetings. Triggers on phrases like "what meetings", "meeting notes", "who was in my meeting", "meeting with [person]", "meeting patterns", "who do I meet with most".
---

# Granola Meeting Notes

Extract and query meeting data from Granola's local cache on macOS and Windows.

## Prerequisites

- Granola must be installed (macOS or Windows)
- User must have at least one recorded meeting

**Note:** Windows support is untested. The cache path is assumed to be `%LOCALAPPDATA%\Granola\cache-v3.json`.

## Cache Location

| Platform | Path |
|----------|------|
| macOS | `~/Library/Application Support/Granola/cache-v3.json` |
| Windows | `%LOCALAPPDATA%\Granola\cache-v3.json` |

## Reading the Cache

```python
import json
import os
import platform
from datetime import datetime, timedelta, timezone
from collections import Counter

def get_cache_path():
    """Get Granola cache path for current platform."""
    if platform.system() == 'Windows':
        local_appdata = os.environ.get('LOCALAPPDATA', '')
        return os.path.join(local_appdata, 'Granola', 'cache-v3.json')
    else:  # macOS (and Linux if ever supported)
        return os.path.expanduser('~/Library/Application Support/Granola/cache-v3.json')

cache_path = get_cache_path()

if not os.path.exists(cache_path):
    raise FileNotFoundError(f"Granola cache not found at {cache_path}. Is Granola installed with recorded meetings?")

with open(cache_path, 'r') as f:
    raw = json.load(f)

# Handle nested 'cache' key containing stringified JSON
if 'cache' in raw and isinstance(raw['cache'], str):
    cache = json.loads(raw['cache'])
else:
    cache = raw

state = cache.get('state', cache)
```

## Cache Structure

| Section | Description |
|---------|-------------|
| `documents` | Meeting metadata and calendar event details |
| `transcripts` | Full transcripts with speaker identification |
| `documentPanels` | AI-generated summaries and user notes |

## Extracting Meeting Data

```python
documents = state.get('documents', {})
transcripts = state.get('transcripts', {})
panels = state.get('documentPanels', {})

meetings = []
for doc_id, doc in documents.items():
    event = doc.get('calendarEvent', {})
    panel_data = panels.get(doc_id, {})
    transcript_data = transcripts.get(doc_id, {})

    meeting = {
        'id': doc_id,
        'title': doc.get('title', 'Untitled'),
        'created_at': doc.get('createdAt'),
        'attendees': event.get('attendees', []),
        'location': event.get('location', ''),
        'organizer': event.get('organizer', {}).get('email', ''),
        'user_notes': panel_data.get('userNotes', ''),
        'ai_summary': panel_data.get('aiSummary', ''),
        'transcript': transcript_data,
    }

    # Calculate transcript statistics
    if transcript_data:
        segments = transcript_data.get('segments', [])
        meeting['transcript_stats'] = calculate_transcript_stats(segments)

    meetings.append(meeting)

# Sort by date (newest first)
meetings.sort(key=lambda m: m.get('created_at', ''), reverse=True)
```

## Transcript Statistics

```python
def calculate_transcript_stats(segments):
    """Calculate word count, speaker count, and duration from transcript segments."""
    if not segments:
        return {'word_count': 0, 'speakers': [], 'duration_seconds': 0}

    words = 0
    speakers = set()

    for seg in segments:
        text = seg.get('text', '')
        words += len(text.split())
        speaker = seg.get('speaker')
        if speaker:
            speakers.add(speaker)

    # Calculate duration from first/last segment timestamps
    duration = 0
    if len(segments) >= 2:
        try:
            start = segments[0].get('start', 0)
            end = segments[-1].get('end', 0)
            duration = end - start
        except (TypeError, KeyError):
            pass

    return {
        'word_count': words,
        'speakers': list(speakers),
        'speaker_count': len(speakers),
        'duration_seconds': duration,
        'duration_formatted': f"{duration // 60}m {duration % 60}s" if duration else 'N/A'
    }
```

## Fuzzy Search with Weighted Scoring

Use fuzzy matching for flexible search. Title matches are weighted higher than participant matches.

```python
from difflib import SequenceMatcher

def fuzzy_match(query, text, threshold=0.6):
    """Return similarity score if above threshold, else 0."""
    if not query or not text:
        return 0
    ratio = SequenceMatcher(None, query.lower(), text.lower()).ratio()
    return ratio if ratio >= threshold else 0

def search_meetings(meetings, query, search_fields=None):
    """
    Search meetings with weighted scoring.

    search_fields: list of 'title', 'attendees', 'transcript', 'notes'
    Default: ['title', 'attendees']

    Scoring:
    - Title match: 2 points * similarity
    - Attendee match: 1 point * similarity
    - Notes/summary match: 1 point * similarity
    - Transcript match: 0.5 points * similarity
    """
    if search_fields is None:
        search_fields = ['title', 'attendees']

    results = []
    query_lower = query.lower()

    for m in meetings:
        score = 0
        match_type = None

        # Title search (weight: 2x)
        if 'title' in search_fields:
            title = m.get('title', '')
            title_score = fuzzy_match(query, title)
            if title_score > 0:
                score += title_score * 2
                match_type = 'title'

        # Attendee search (weight: 1x)
        if 'attendees' in search_fields:
            for att in m.get('attendees', []):
                email = att.get('email', '')
                name = email.split('@')[0]
                att_score = max(fuzzy_match(query, email), fuzzy_match(query, name))
                if att_score > 0:
                    score += att_score
                    match_type = match_type or 'attendee'

        # Notes/summary search (weight: 1x)
        if 'notes' in search_fields:
            notes = str(m.get('user_notes', '')) + str(m.get('ai_summary', ''))
            if query_lower in notes.lower():
                score += 1
                match_type = match_type or 'notes'

        # Transcript search (weight: 0.5x)
        if 'transcript' in search_fields:
            transcript = m.get('transcript', {})
            segments = transcript.get('segments', [])
            transcript_text = ' '.join(s.get('text', '') for s in segments)
            if query_lower in transcript_text.lower():
                score += 0.5
                match_type = match_type or 'transcript'

        if score > 0:
            results.append({**m, '_score': score, '_match_type': match_type})

    # Sort by score descending, then by date
    results.sort(key=lambda x: (-x['_score'], x.get('created_at', '')))
    return results
```

## Pattern Analysis

### Participant Frequency

```python
def analyze_participant_frequency(meetings, days=30):
    """Find most frequent meeting participants in the last N days."""
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    counter = Counter()

    for m in meetings:
        created = m.get('created_at')
        if not created:
            continue
        try:
            dt = datetime.fromisoformat(created.replace('Z', '+00:00'))
            if dt < cutoff:
                continue
        except ValueError:
            continue

        for att in m.get('attendees', []):
            email = att.get('email', '')
            if email:
                counter[email] += 1

    return counter.most_common(10)
```

### Meeting Frequency by Week

```python
def analyze_meeting_frequency(meetings, weeks=8):
    """Analyze meeting count per week."""
    cutoff = datetime.now(timezone.utc) - timedelta(weeks=weeks)
    weekly = Counter()

    for m in meetings:
        created = m.get('created_at')
        if not created:
            continue
        try:
            dt = datetime.fromisoformat(created.replace('Z', '+00:00'))
            if dt < cutoff:
                continue
            week_key = dt.strftime('%Y-W%W')
            weekly[week_key] += 1
        except ValueError:
            continue

    return sorted(weekly.items())
```

### Topic Extraction

```python
def extract_topics(meetings, days=30):
    """Extract common words from meeting titles as topic indicators."""
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    words = Counter()
    stopwords = {'the', 'a', 'an', 'and', 'or', 'with', 'for', 'to', 'of', 'in', 'on', 'at', 'by'}

    for m in meetings:
        created = m.get('created_at')
        if not created:
            continue
        try:
            dt = datetime.fromisoformat(created.replace('Z', '+00:00'))
            if dt < cutoff:
                continue
        except ValueError:
            continue

        title = m.get('title', '').lower()
        for word in title.split():
            word = word.strip('.,!?:;()[]{}')
            if len(word) > 2 and word not in stopwords:
                words[word] += 1

    return words.most_common(15)
```

## Export to Markdown

```python
import re

def slugify(text):
    """Convert text to URL-friendly slug."""
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text[:50]

def export_meeting_to_markdown(meeting, output_dir='~/granola-exports'):
    """Export a meeting to a markdown file with auto-generated filename."""
    output_dir = os.path.expanduser(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    # Generate filename: YYYY-MM-DD-title-slug.md
    date_str = meeting.get('created_at', '')[:10]
    title_slug = slugify(meeting.get('title', 'untitled'))
    filename = f"{date_str}-{title_slug}.md"
    filepath = os.path.join(output_dir, filename)

    # Format attendees
    attendees = [a.get('email', '').split('@')[0] for a in meeting.get('attendees', [])]

    # Get transcript stats
    stats = meeting.get('transcript_stats', {})

    content = f"""# {meeting.get('title', 'Untitled')}

**Date:** {format_date(meeting.get('created_at'))}
**Attendees:** {', '.join(attendees) or 'N/A'}
**Location:** {meeting.get('location') or 'N/A'}
**Organizer:** {meeting.get('organizer') or 'N/A'}

## Statistics
- **Duration:** {stats.get('duration_formatted', 'N/A')}
- **Word Count:** {stats.get('word_count', 'N/A')}
- **Speakers:** {stats.get('speaker_count', 'N/A')}

## Notes
{meeting.get('user_notes') or '_No notes_'}

## AI Summary
{meeting.get('ai_summary') or '_No summary_'}
"""
    with open(filepath, 'w') as f:
        f.write(content)

    return filepath
```

## Timezone-Aware Date Formatting

```python
def format_date(iso_string, format_str='%B %d, %Y at %I:%M %p'):
    """Format ISO date string to local timezone."""
    if not iso_string:
        return 'Unknown'
    try:
        dt = datetime.fromisoformat(iso_string.replace('Z', '+00:00'))
        local_dt = dt.astimezone()  # Convert to local timezone
        return local_dt.strftime(format_str)
    except ValueError:
        return iso_string[:10]
```

## Common Queries

### List Recent Meetings

```python
days = 7
cutoff = datetime.now(timezone.utc) - timedelta(days=days)

recent = [m for m in meetings
          if m.get('created_at') and
          datetime.fromisoformat(m['created_at'].replace('Z', '+00:00')) > cutoff]

for m in recent:
    stats = m.get('transcript_stats', {})
    print(f"- {m['title']} ({format_date(m['created_at'], '%b %d')})")
    print(f"  Duration: {stats.get('duration_formatted', 'N/A')}, "
          f"Speakers: {stats.get('speaker_count', 'N/A')}")
```

### Find Meetings by Attendee

```python
results = search_meetings(meetings, 'john', search_fields=['attendees'])
```

### Search All Fields

```python
results = search_meetings(meetings, 'budget review',
                          search_fields=['title', 'attendees', 'notes', 'transcript'])
```

### Who Do I Meet With Most?

```python
top_participants = analyze_participant_frequency(meetings, days=30)
for email, count in top_participants:
    print(f"- {email}: {count} meetings")
```

### Meeting Patterns

```python
# Weekly frequency
weekly = analyze_meeting_frequency(meetings, weeks=8)
for week, count in weekly:
    print(f"- {week}: {count} meetings")

# Common topics
topics = extract_topics(meetings, days=30)
for topic, count in topics:
    print(f"- {topic}: {count} occurrences")
```

## Output Formatting

### Detailed Meeting View

```markdown
## {title}
**Date:** {formatted_date}
**Attendees:** {comma_separated_names}
**Location:** {location}
**Duration:** {duration} | **Words:** {word_count} | **Speakers:** {speaker_count}

### Notes
{user_notes}

### AI Summary
{ai_summary}
```

### Compact List View

```markdown
| Date | Meeting | Attendees | Duration |
|------|---------|-----------|----------|
| Jan 20 | Weekly Standup | alice, bob | 45m |
| Jan 19 | Product Review | dave, eve | 1h 15m |
```

### Pattern Analysis View

```markdown
## Meeting Patterns (Last 30 Days)

### Top Collaborators
1. alice@company.com - 12 meetings
2. bob@company.com - 8 meetings
3. charlie@company.com - 6 meetings

### Weekly Trend
- Week 3: 8 meetings
- Week 2: 6 meetings
- Week 1: 10 meetings

### Common Topics
- standup (15), review (8), planning (6), sync (5)
```

## Error Handling

```python
if not os.path.exists(cache_path):
    print("Granola cache not found. Is Granola installed with recorded meetings?")
elif not meetings:
    print("No meetings found in Granola cache.")
```

## Privacy Note

All data stays local. The cache file contains meeting transcripts and notes that may be sensitive. Never transmit this data externally.
