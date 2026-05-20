# Narration Build

Generate voice narration scripts and audio files using ElevenLabs API.

---

## Frontmatter

```yaml
context: main
allowed-tools: Read, Write, Edit, Bash, AskUserQuestion
```

---

## Prerequisites

- Presentation must exist and pass all gates (review complete)
- `reviewlog.md` must show READY FOR NARRATION status
- ElevenLabs API key must be configured
- ELEVENLABS_API_KEY environment variable set

---

## Instructions

You are generating voice narration for a presentation. This involves creating a speaker script and then generating audio files.

### Usage

```
/narration-build {topic}
```

### Step 1: Verify Prerequisites

Check that:
1. Presentation passed all gates
2. ElevenLabs is configured in `rpiv-config.json`
3. API key is available

### Step 2: Extract Speaker Notes

Read the presentation file and extract all speaker notes:
- From HTML comments: `<!-- Speaker notes: ... -->`
- From data attributes: `data-notes="..."`
- From spec file if embedded in slides

### Step 3: Create Narration Script

Write `src/pages/class-{n}-{topic}/script.md`:

```markdown
# Narration Script: {Topic Title}

Class: {N}
Voice: {voice name from config}
Generated: {date}

## Script Guidelines

- Conversational, not robotic
- Pause notation: [pause] for 0.5s, [long pause] for 1s
- Emphasis: *word* for stress
- Speed: Default pace, adjust with [slower] or [faster]

## Slide Scripts

### Slide 1: {Title}

**Duration**: ~{X} seconds

```text
{Narration text for this slide}
```

**Notes**: {Any generation notes}

---

### Slide 2: {Title}

**Duration**: ~{X} seconds

```text
{Narration text}
```

---

{Continue for all slides}

## Audio Files

| Slide | File | Duration |
|-------|------|----------|
| 1 | slide-01.mp3 | {X}s |
| 2 | slide-02.mp3 | {X}s |
| ... | ... | ... |

## Total Duration

Estimated: {X} minutes
```

### Step 4: Review Script Quality

Before generating audio, verify:
- [ ] Natural conversational tone
- [ ] Matches what's on slides (doesn't just read them)
- [ ] Adds context and explanation
- [ ] Appropriate pacing for students
- [ ] Technical terms pronounced correctly
- [ ] Transitions between concepts smooth

### Step 5: Generate Audio Files

Create audio directory:
```bash
mkdir -p public/audio/class-{n}
```

For each slide script, call ElevenLabs API:

```bash
curl -X POST "https://api.elevenlabs.io/v1/text-to-speech/{voice_id}" \
  -H "xi-api-key: $ELEVENLABS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "{slide script text}",
    "model_id": "eleven_multilingual_v2",
    "voice_settings": {
      "stability": 0.5,
      "similarity_boost": 0.75
    }
  }' \
  --output "public/audio/class-{n}/slide-{nn}.mp3"
```

### Step 6: Update Presentation

Add audio integration to presentation:

```javascript
// Audio playback integration
const slideAudio = {
  1: 'slide-01.mp3',
  2: 'slide-02.mp3',
  // ...
};

let currentAudio = null;

function playSlideAudio(slideNum) {
  if (currentAudio) {
    currentAudio.pause();
  }
  const audioFile = slideAudio[slideNum];
  if (audioFile) {
    currentAudio = new Audio(`/audio/class-{n}/${audioFile}`);
    currentAudio.play();
  }
}

// Hook into navigation
const originalGoToSlide = window.Presentation.goToSlide;
window.Presentation.goToSlide = function(n) {
  originalGoToSlide(n);
  playSlideAudio(n + 1); // Slides are 1-indexed in audio
};
```

Add playback controls:
```html
<div class="audio-controls">
  <button onclick="toggleAudio()" id="audio-toggle">🔊</button>
  <button onclick="replayAudio()">↻</button>
</div>
```

### Step 7: Generate Manifest

Create `public/audio/class-{n}/manifest.json`:

```json
{
  "class": {N},
  "topic": "{topic}",
  "voice": "{voice name}",
  "generated": "{date}",
  "totalDuration": "{X:XX}",
  "slides": [
    {
      "slide": 1,
      "file": "slide-01.mp3",
      "duration": 45,
      "text": "{first 50 chars}..."
    }
  ]
}
```

### Step 8: Test Playback

Verify:
- [ ] All audio files play
- [ ] Timing matches slide content
- [ ] Volume is consistent
- [ ] No artifacts or glitches
- [ ] Controls work (play/pause/replay)

---

## Output Specification

This skill produces:

- **Script**: `src/pages/class-{n}-{topic}/script.md`
- **Audio files**: `public/audio/class-{n}/slide-XX.mp3`
- **Manifest**: `public/audio/class-{n}/manifest.json`
- **Code update**: Audio integration in presentation

---

## Voice Selection

Available voices (from ElevenLabs):

| Voice | ID | Character | Best For |
|-------|-----|-----------|----------|
| Rachel | default | Clear, professional | General education |
| Adam | ... | Deep, authoritative | Technical content |
| Bella | ... | Warm, friendly | Conversational |

Configure in `rpiv-config.json`:
```json
{
  "narration": {
    "provider": "elevenlabs",
    "voiceId": "{voice-id}",
    "defaultVoice": "Rachel"
  }
}
```

---

## Script Writing Guidelines

### DO
- Expand on slide content, don't just read it
- Use conversational language
- Include brief pauses for processing
- Pronounce acronyms (TAM as "tam" not "T-A-M")
- Add transitions: "Now let's look at...", "Building on this..."

### DON'T
- Read bullet points verbatim
- Use overly formal language
- Rush through complex concepts
- Include visual references student can see
- Say "click to advance" or similar

### Example Script Entry

**Slide content**:
```
TAM: Total Addressable Market
The total revenue opportunity if you achieved 100% market share
```

**Bad narration**:
```
TAM stands for Total Addressable Market. It's the total revenue
opportunity if you achieved 100% market share.
```

**Good narration**:
```
Let's start with TAM [pause] your Total Addressable Market.
Think of this as the absolute maximum [pause] the total pie
if somehow every single potential customer bought from you.
[pause] Now, this is a theoretical ceiling, not a goal.
No company actually captures 100% of their TAM.
```

---

## Error Handling

### API Errors

If ElevenLabs returns an error:
1. Check API key validity
2. Check quota/usage limits
3. Retry with exponential backoff
4. Log error and continue with remaining slides

### Audio Quality Issues

If generated audio has issues:
1. Adjust voice settings (stability, similarity)
2. Modify script (simplify sentences)
3. Use SSML for pronunciation control
4. Regenerate specific slides

---

## Examples

### Example: Script Generation

```markdown
# Narration Script: Market Sizing

Class: 4
Voice: Rachel
Generated: 2026-01-20

## Slide Scripts

### Slide 1: Title

**Duration**: ~10 seconds

```text
Welcome to Class Four [pause] where we're going to tackle
one of the most important questions in entrepreneurship:
[pause] How big is your market?
```

---

### Slide 6: TAM/SAM/SOM Funnel

**Duration**: ~45 seconds

```text
Now here's a visualization that will help you remember these
three levels. [pause]

At the top, we have TAM [pause] your Total Addressable Market.
It's the widest part of the funnel because it represents
everyone who could theoretically use your product.

[pause]

As we narrow down, we get to SAM [pause] your Serviceable
Available Market. This is the portion you can actually reach
with your current business model.

[pause]

And finally, SOM [pause] your Serviceable Obtainable Market.
This is your realistic first-year target [pause] the slice
you can actually capture given your resources.
```
```
