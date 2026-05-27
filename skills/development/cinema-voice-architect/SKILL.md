---
name: cinema-voice-architect
description: |
  Expert architect for Cinema Mode and audio/voice systems in Raamattu Nyt.

  Use when:
  (1) Building or modifying Cinema Mode full-screen verse presentation
  (2) Implementing audio playback with verse-level synchronization
  (3) Integrating ElevenLabs TTS voice generation
  (4) Creating auto-scroll functionality with or without audio
  (5) Managing audio cues and timing synchronization
  (6) Working with background music and visual effects (Ken Burns)
  (7) Implementing dual-track audio (Bible + music) controls

  Triggers: "cinema mode", "voice playback", "audio sync", "verse scrolling",
  "ElevenLabs", "TTS", "audio cues", "auto-advance", "full screen reader",
  "background music", "Ken Burns", "verse timing"
---

# Cinema Voice Architect

Expert skill for Cinema Mode and audio/voice implementation.

## Quick Reference

| Component | Location |
|-----------|----------|
| Cinema Screen | `src/features/cinema/CinemaReaderScreen.tsx` |
| Cinema Background | `src/components/cinema/CinemaBackground.tsx` |
| Audio Service | `src/lib/audioService.ts` |
| ElevenLabs Voices | `src/lib/elevenLabsVoices.ts` |
| Cinema Audio Hook | `src/hooks/useCinemaAudio.ts` |
| Bible Audio Hook | `src/hooks/useBibleAudio.ts` |
| Auto-Advance Hook | `src/hooks/useAutoAdvance.ts` |
| Audio Generation | `supabase/functions/generate-audio/index.ts` |

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                   CinemaReaderScreen                     │
│  (Orchestrator: state, audio, visuals, preferences)     │
├─────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │ useCinema-   │  │ useAuto-     │  │ useCinema-   │  │
│  │ Audio        │  │ Advance      │  │ Preferences  │  │
│  │ (dual-track) │  │ (WPM-based)  │  │ (persist)    │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
├─────────────────────────────────────────────────────────┤
│  ┌──────────────────────┐  ┌─────────────────────────┐  │
│  │ CinemaBackground     │  │ @raamattu-nyt/          │  │
│  │ (Ken Burns, video)   │  │ cinema-reader (pkg)     │  │
│  └──────────────────────┘  └─────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                    Audio Pipeline                        │
├─────────────────────────────────────────────────────────┤
│  generate-audio Edge Function                            │
│  └─→ ElevenLabs API (with timestamps)                   │
│      └─→ audio_assets table (hash-cached)               │
│          └─→ audio_cues table (verse timing)            │
└─────────────────────────────────────────────────────────┘
```

## Cinema Mode Components

### CinemaReaderScreen

Main orchestrator at `src/features/cinema/CinemaReaderScreen.tsx`:

```typescript
// Key responsibilities:
// 1. Map BundleVerse → CinemaVerse for cinema-reader package
// 2. Manage dual audio tracks (Bible narration + background music)
// 3. Handle verse navigation (index state)
// 4. Persist preferences to Supabase
// 5. Coordinate background visuals

// Critical state:
const [currentIndex, setCurrentIndex] = useState(0);
const [isPlaying, setIsPlaying] = useState(false);
const { bibleVolume, musicVolume, visualDimming } = useCinemaPreferences();
```

### Animation Modes

Five animation modes in `src/types/cinema.ts`:

| Mode | Effect |
|------|--------|
| `slide` | Verses slide horizontally |
| `zoom` | Zoom in/out transition |
| `stack` | Stack/unstack cards |
| `loopH` | Horizontal infinite loop |
| `loopV` | Vertical infinite loop |

### Ken Burns Effect

`CinemaBackground.tsx` implements Ken Burns:

```typescript
// Random transform over 25 seconds
const generateKenBurnsTransform = () => ({
  scale: 1 + Math.random() * 0.15,      // 1.0 - 1.15
  translateX: (Math.random() - 0.5) * 10, // -5% to +5%
  translateY: (Math.random() - 0.5) * 10,
});
```

## Audio System

### ElevenLabs Integration

Voices in `src/lib/elevenLabsVoices.ts`:

```typescript
export const ELEVENLABS_VOICES = {
  venla: {
    id: 'T5qAFgaL2uYxoUtojUzQ',  // Female Finnish
    name: 'Venla',
    readerKey: 'elevenlabs:T5qAFgaL2uYxoUtojUzQ'
  },
  urho: {
    id: '1WVCONUwYGulVaKg4oTr',  // Male Finnish
    name: 'Urho',
    readerKey: 'elevenlabs:1WVCONUwYGulVaKg4oTr'
  }
};
```

### Audio Generation Flow

```
1. Client calls audioService.generateChapterAudio()
2. Edge Function checks hash cache in audio_assets
3. If miss: Call ElevenLabs with timestamps
4. Parse character-level timestamps → verse cues
5. Store MP3 in Supabase Storage
6. Save metadata + cues to database
7. Return { audio_id, file_url, duration_ms, audio_cues }
```

Edge Function parameters:

```typescript
// ElevenLabs API call
const response = await fetch(
  `https://api.elevenlabs.io/v1/text-to-speech/${voiceId}/with-timestamps`,
  {
    method: 'POST',
    headers: {
      'xi-api-key': ELEVENLABS_API_KEY,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      text: verseTexts.join('\n\n'),
      model_id: 'eleven_multilingual_v2',
      voice_settings: {
        stability: 0.5,
        similarity_boost: 0.75
      }
    })
  }
);
```

### Audio Cue Format

```typescript
interface AudioCue {
  verse_number: number;  // 1-indexed
  start_ms: number;      // Milliseconds from audio start
  end_ms: number;        // End time in ms
}

// Example cues for John 3:16-17
const cues: AudioCue[] = [
  { verse_number: 16, start_ms: 0, end_ms: 8500 },
  { verse_number: 17, start_ms: 8500, end_ms: 15200 }
];
```

### Verse Sync Algorithm

Core sync in `src/lib/cinemaAudioSync.ts`:

```typescript
export function findCurrentCue(
  currentTimeMs: number,
  audioCues: AudioCue[]
): AudioCue | undefined {
  return audioCues.find(
    cue => currentTimeMs >= cue.start_ms && currentTimeMs < cue.end_ms
  );
}

// Usage in playback loop:
const currentCue = findCurrentCue(audioElement.currentTime * 1000, cues);
if (currentCue && currentCue.verse_number !== lastSyncedVerse) {
  setCurrentVerseIndex(currentCue.verse_number - 1); // 0-indexed
  lastSyncedVerse = currentCue.verse_number;
}
```

## Auto-Advance (Without Audio)

`useAutoAdvance` hook enables scrolling without audio:

```typescript
// Calculate delay based on word count
const calculateDelay = (text: string, wordsPerMinute: number) => {
  const wordCount = text.split(/\s+/).length;
  const delayMs = wordCount * (60000 / wordsPerMinute);
  return Math.max(delayMs, 1500); // Minimum 1.5 seconds
};

// Default: 150 WPM (adjustable 50-400 in preferences)
```

Priority logic:
1. **Audio playing**: Audio cues control verse timing
2. **No audio**: Auto-advance timer controls verse timing

## Dual-Track Audio

`useCinemaAudio` manages two audio tracks:

```typescript
interface CinemaAudioConfig {
  bibleAudioUrl?: string;
  audioCues?: AudioCue[];
  backgroundMusicUrl?: string;
  bibleVolume: number;      // 0-1
  musicVolume: number;      // 0-1
}

// Methods:
playAll()           // Start both tracks
pauseAll()          // Pause both
setBibleVolume(v)   // 0-1
setMusicVolume(v)   // 0-1
toggleMusic()       // On/off without affecting Bible
seekToVerse(index)  // Jump Bible audio to verse
```

## Database Schema

### Audio Tables

```sql
-- audio_assets (public)
CREATE TABLE audio_assets (
  id UUID PRIMARY KEY,
  hash TEXT UNIQUE,           -- SHA-256(chapter_id + version_id + reader_key)
  chapter_id UUID,
  version_id UUID,
  file_url TEXT,
  duration_ms INTEGER,
  reader_key TEXT,            -- e.g., "elevenlabs:T5qAFgaL2uYxoUtojUzQ"
  tts_provider TEXT,          -- "elevenlabs"
  voice TEXT
);

-- audio_cues (public)
CREATE TABLE audio_cues (
  audio_id UUID REFERENCES audio_assets(id),
  verse_id UUID,
  start_ms INTEGER,
  end_ms INTEGER
);
```

### Cinema Tables

```sql
-- bible_schema.cinema_preferences
CREATE TABLE cinema_preferences (
  user_id UUID,
  guest_session_id TEXT,
  last_track_id UUID,
  last_visual_id UUID,
  bible_volume NUMERIC(3,2) DEFAULT 1,
  music_volume NUMERIC(3,2) DEFAULT 0.3,
  visual_dimming NUMERIC(3,2) DEFAULT 0.5,
  auto_advance_speed INTEGER DEFAULT 150,  -- WPM
  animation_mode TEXT DEFAULT 'slide',
  playback_speed NUMERIC(3,2) DEFAULT 1,
  ken_burns_enabled BOOLEAN DEFAULT true
);

-- bible_schema.background_tracks
CREATE TABLE background_tracks (
  id UUID PRIMARY KEY,
  name TEXT,
  name_fi TEXT,
  file_url TEXT,
  duration_ms INTEGER,
  category TEXT,  -- ambient, worship, instrumental
  mood TEXT[],
  is_active BOOLEAN
);

-- bible_schema.background_visuals
CREATE TABLE background_visuals (
  id UUID PRIMARY KEY,
  name TEXT,
  name_fi TEXT,
  type TEXT,       -- video, image
  file_url TEXT,
  thumbnail_url TEXT,
  duration_ms INTEGER,
  category TEXT,   -- nature, sky, water, abstract, sacred
  is_active BOOLEAN
);
```

## Common Tasks

### Add New Voice

1. Get voice ID from ElevenLabs
2. Add to `src/lib/elevenLabsVoices.ts`
3. Add to admin UI in `AudioVoicesManager.tsx`
4. Use reader_key format: `elevenlabs:{voiceId}`

### Modify Animation

Cinema-reader package controls animations:
- Package: `@raamattu-nyt/cinema-reader`
- Animation configs in package's `VerseAnimator.tsx`

### Adjust Auto-Advance Timing

```typescript
// In cinema preferences or constants:
const DEFAULT_WPM = 150;      // Words per minute
const MIN_VERSE_DELAY = 1500; // Minimum ms per verse
```

### Debug Audio Sync

```typescript
// Add logging to useCinemaAudio:
useEffect(() => {
  const interval = setInterval(() => {
    const timeMs = bibleAudioRef.current?.currentTime * 1000;
    const cue = findCurrentCue(timeMs, audioCues);
    console.log(`Time: ${timeMs}ms, Verse: ${cue?.verse_number}`);
  }, 100);
  return () => clearInterval(interval);
}, [audioCues]);
```

## File Structure

```
src/
├── features/cinema/
│   └── CinemaReaderScreen.tsx    # Main orchestrator
├── components/cinema/
│   ├── CinemaBackground.tsx      # Video/image + Ken Burns
│   ├── BackgroundMusicPicker.tsx # Music selection UI
│   └── BackgroundVisualPicker.tsx # Visual selection UI
├── hooks/
│   ├── useCinemaAudio.ts         # Dual-track audio
│   ├── useBibleAudio.ts          # Single-track audio
│   ├── useAutoAdvance.ts         # WPM-based scrolling
│   ├── useCinemaPreferences.ts   # Preferences persistence
│   ├── useCinemaFullscreen.ts    # Fullscreen API
│   └── useChapterBundle.tsx      # Bundle with audio data
├── lib/
│   ├── audioService.ts           # Audio generation client
│   ├── elevenLabsVoices.ts       # Voice configurations
│   ├── cinemaAudioSync.ts        # Cue-to-verse mapping
│   └── audioEstimation.ts        # Word count timing
├── types/
│   ├── cinema.ts                 # Cinema types & defaults
│   └── reel.ts                   # Reel rendering types
supabase/functions/
└── generate-audio/
    └── index.ts                  # ElevenLabs Edge Function
```

## References

- `references/audio-cue-format.md` - Detailed cue timing specification
- `references/elevenlabs-api.md` - ElevenLabs API reference
