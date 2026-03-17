---
name: add-tts
description: Adds text-to-speech audio help to a feature using the TTS system. Use when adding voice narration, audio feedback, or spoken instructions to any part of the app.
allowed-tools: Bash, Read, Glob, Grep, Edit, Write
---

# Adding TTS Audio to a Feature

This skill walks you through adding text-to-speech audio to a feature in the app. The TTS system plays audio via a **voice chain** (pregenerated mp3 → on-demand generation via OpenAI → browser SpeechSynthesis → subtitles). Clips are collected at runtime, persisted to the database, and generated as high-quality OpenAI TTS mp3s — either on-the-fly during playback (if the `generate` chain entry is configured) or in batch from the admin panel.

## Before You Start

**Read the integration guide:** `apps/web/.claude/reference/tts-audio-system.md`

It contains the full API reference, patterns, anti-patterns, and existing implementations.

## Your Job

1. Understand what text the feature needs spoken and when
2. Create a feature-specific audio hook
3. Wire it into the component
4. Verify with TypeScript

## Step 1: Design the Utterances

For each piece of audio the feature needs, determine:

- **What** text to speak (static string or dynamic from state/props)
- **When** to speak it (on mount, on state change, on user action, on completion)
- **How** it should sound (tone — write as voice-actor stage directions)

## Step 2: Create a Feature Audio Hook

Create a hook in the feature's `hooks/` directory. This hook owns text construction, tone strings, auto-play logic, and cleanup.

**Read the reference implementation first:**
```
apps/web/src/components/practice/hooks/usePracticeAudioHelp.ts
```

**Key rules:**

1. **Tone strings must be module-level constants** — never compute them dynamically per render
2. **Always clean up on unmount** — call `stop()` in a cleanup effect
3. **Use refs to track previous values** — prevents re-playing on every render
4. **Guard with `isEnabled`** — respect the user's audio toggle

**Template:**

```typescript
'use client'

import { useEffect, useRef } from 'react'
import { useTTS } from '@/hooks/useTTS'
import { useAudioManager } from '@/hooks/useAudioManager'

// Stable tone constants — changing these creates new clips
const INSTRUCTION_TONE =
  'Patiently guiding a young child. Clear, slow, friendly.'
const CELEBRATION_TONE =
  'Warmly congratulating a child. Genuinely encouraging and happy.'

interface UseMyFeatureAudioHelpOptions {
  currentStep: string
  isComplete: boolean
}

export function useMyFeatureAudioHelp({
  currentStep,
  isComplete,
}: UseMyFeatureAudioHelpOptions) {
  const { isEnabled, stop } = useAudioManager()

  // Declare utterances
  const sayInstruction = useTTS(currentStep, { tone: INSTRUCTION_TONE })
  const sayCelebration = useTTS(
    isComplete ? 'Well done!' : '',
    { tone: CELEBRATION_TONE },
  )

  // Auto-play when step changes
  const prevStepRef = useRef<string>('')
  useEffect(() => {
    if (!isEnabled || !currentStep || currentStep === prevStepRef.current) return
    prevStepRef.current = currentStep
    sayInstruction()
  }, [isEnabled, currentStep, sayInstruction])

  // Auto-play celebration on completion
  useEffect(() => {
    if (!isEnabled || !isComplete) return
    sayCelebration()
  }, [isEnabled, isComplete, sayCelebration])

  // Stop audio on unmount
  useEffect(() => {
    return () => stop()
  }, [stop])

  return { replay: sayInstruction }
}
```

## Step 3: Wire Into the Component

```typescript
import { useMyFeatureAudioHelp } from './hooks/useMyFeatureAudioHelp'
import { useAudioManager } from '@/hooks/useAudioManager'

function MyFeature() {
  const { isEnabled, isPlaying } = useAudioManager()
  const { replay } = useMyFeatureAudioHelp({
    currentStep: 'Tap the bead to move it up',
    isComplete: false,
  })

  return (
    <div>
      {isEnabled && (
        <button onClick={replay} disabled={isPlaying}>
          {isPlaying ? 'Speaking...' : 'Replay'}
        </button>
      )}
    </div>
  )
}
```

## Step 4: Verify

```bash
cd apps/web && npx tsc --noEmit
```

## Common Patterns

### Dynamic text from state

```typescript
const text = useMemo(
  () => (terms ? termsToSentence(terms) : ''),
  [terms],
)
const sayProblem = useTTS(text, { tone: MATH_TONE })
```

### One-shot playback (play once, don't repeat)

```typescript
const playedRef = useRef(false)
useEffect(() => {
  if (!shouldPlay || playedRef.current) return
  playedRef.current = true
  sayIt()
}, [shouldPlay, sayIt])

// Reset when trigger resets
useEffect(() => {
  if (!shouldPlay) playedRef.current = false
}, [shouldPlay])
```

### Multiple utterances — play the right one

```typescript
const sayStep1 = useTTS('First, look at the abacus', { tone: INST })
const sayStep2 = useTTS('Now tap the bead', { tone: INST })

// speak() stops previous before starting
if (step === 0) sayStep1()
if (step === 1) sayStep2()
```

## Tone String Guidelines

Write tones as **voice-actor stage directions**. Be specific about emotion, pace, and audience.

**Good examples:**
- `'Speaking clearly and steadily, reading a math problem to a young child. Pause slightly between each number and operator.'`
- `'Warmly congratulating a child. Genuinely encouraging and happy.'`
- `'Gently guiding a child after a wrong answer. Kind, not disappointed.'`
- `'Patiently guiding a young child through an abacus tutorial. Clear, slow, friendly.'`

**Bad examples:**
- `'Read this text'` — too vague
- `` `Speaking ${mood}` `` — dynamic per render, creates new clips every time

## Anti-Patterns to Avoid

1. **Never use raw `speechSynthesis`** — always go through `useTTS` so the voice chain and collection work
2. **Never forget cleanup** — always `useEffect(() => () => stop(), [stop])`
3. **Never use dynamic tone strings** — keep them as module-level constants
4. **Never call `speak()` unconditionally in render** — always guard with refs and `isEnabled`

## Key Files

| File | Role |
|------|------|
| `src/hooks/useTTS.ts` | Primary hook — declare (text, tone), get speak function |
| `src/hooks/useAudioManager.ts` | Reactive state — isEnabled, isPlaying, volume, subtitles, stop() |
| `src/lib/audio/TtsAudioManager.ts` | Core engine — voice chain, playback, collection, subtitles |
| `src/lib/audio/voiceSource.ts` | Voice source class hierarchy — polymorphic `generate()` per voice type |
| `src/contexts/AudioManagerContext.tsx` | React context — singleton manager, boot-time manifest loading |
| `src/lib/audio/termsToSentence.ts` | `[5, 3]` → `"five plus three"` |
| `src/lib/audio/buildFeedbackText.ts` | Correct/incorrect feedback sentences |
| `src/lib/audio/numberToEnglish.ts` | `42` → `"forty two"` |

## Voice Chain

Audio plays through the voice chain in order. The typical chain is:

```
pregenerated voice (nova) → auto-generate → browser TTS → subtitles
```

- **Pregenerated**: instant playback from pre-generated mp3 on disk
- **Auto-generate**: calls OpenAI on-the-fly if the pregenerated mp3 is missing, caches result
- **Browser TTS**: uses the browser's built-in speech synthesis
- **Subtitles**: shows text on screen with a reading-time timer

You don't need to think about this when adding TTS to a feature — just use `useTTS()` and the chain handles fallback automatically. The admin configures the chain at `/admin/audio`.

## Reference Implementations

| Hook | Location | What it does |
|------|----------|-------------|
| `usePracticeAudioHelp` | `src/components/practice/hooks/` | Reads math problems, correct/incorrect feedback |
| `useTutorialAudioHelp` | `src/components/tutorial/hooks/` | Speaks tutorial step instructions |

Follow `usePracticeAudioHelp` as the most complete example.
