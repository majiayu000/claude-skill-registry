---
name: dev-assets-audio-loading
description: Audio loading patterns for R3F/Three.js. Use when adding sound effects.
category: assets
---

# Audio Loading

Sound and music loading for React Three Fiber.

## When to Use

Use when:
- Adding sound effects
- Playing background music
- Positional audio for 3D scenes

## Quick Start

```typescript
import { useRef, useEffect } from 'react';
import { PositionalAudio } from '@react-three/drei';

function SoundEffect({ url, volume = 1 }) {
  const audioRef = useRef();

  useEffect(() => {
    if (!audioRef.current) return;

    const audio = audioRef.current;
    audio.load(url);
    audio.setVolume(volume);
    audio.setRefDistance(1);
    audio.setMaxDistance(20);

    return () => {
      audio.stop();
    };
  }, [url, volume]);

  return (
    <PositionalAudio
      ref={audioRef}
      position={[0, 0, 0]}
      autoplay={false}
    />
  );
}
```

## HTML Audio (Simple)

```typescript
function SimpleSound({ url, volume = 1 }) {
  const audioRef = useRef<HTMLAudioElement>(null);

  useEffect(() => {
    const audio = new Audio(url);
    audio.volume = volume;
    audio.loop = false;

    audio.onended = () => {
      audio.currentTime = 0;
    };

    audio.play().catch(err => {
      console.error('Audio play error:', err);
    });

    return () => {
      audio.pause();
      audio.src = '';
    };
  }, [url, volume]);

  return null;
}
```

## Three.js Positional Audio

```typescript
import { PositionalAudio } from '@react-three/drei';

function PositionalSound() {
  return (
    <PositionalAudio
      url="/sounds/footstep.ogg"
      distance={5}
      loop={false}
      autoplay={false}
    />
  );
}
```

## Audio Listener

```typescript
import { AudioListener } from '@react-three/drei';

function Scene() {
  return (
    <>
      <AudioListener />
      <PositionalAudio url="/sounds/explosion.ogg" position={[0, 0, 0]} />
    </>
  );
}
```

## Audio Manager

```typescript
class AudioManager {
  private sounds: Map<string, HTMLAudioElement> = new Map();
  private volume: number = 1;

  preload(url: string, id: string) {
    const audio = new Audio(url);
    audio.preload = 'auto';
    this.sounds.set(id, audio);
  }

  play(id: string) {
    const audio = this.sounds.get(id);
    if (audio) {
      audio.currentTime = 0;
      audio.play();
    }
  }

  stop(id: string) {
    const audio = this.sounds.get(id);
    if (audio) {
      audio.pause();
      audio.currentTime = 0;
    }
  }

  setVolume(volume: number) {
    this.volume = volume;
    this.sounds.forEach(audio => {
      audio.volume = volume;
    });
  }
}
```

## Audio Formats

| Format | Browser Support | Use Case |
|--------|-----------------|----------|
| MP3 | Universal | Music, long sounds |
| OGG | Good | Sound effects |
| AAC | Excellent (Apple) | Mobile |
| WAV | Poor | Short effects (uncompressed) |

## Common Mistakes

| ❌ Wrong | ✅ Right |
|----------|----------|
| Not cleaning up audio | Always pause/cleanup in useEffect |
| Using uncompressed WAV | Use MP3/OGG for production |
| No volume control | Add volume slider |
| Loading on every play | Preload common sounds |

## Mobile Considerations

```typescript
// iOS requires user interaction to play audio
const [audioEnabled, setAudioEnabled] = useState(false);

function EnableAudioButton() {
  const enable = () => {
    // Play silent sound to unlock audio
    const audio = new Audio('/sounds/silent.mp3');
    audio.play();
    setAudioEnabled(true);
  };

  return <button onClick={enable}>Enable Audio</button>;
}
```

## Reference

- **[dev-assets-model-loading](../dev-assets-model-loading/SKILL.md)** — FBX model loading
- **[dev-assets-texture-loading](../dev-assets-texture-loading/SKILL.md)** — Texture loading
- **[dev-assets-vite-asset-loading](../dev-assets-vite-asset-loading/SKILL.md)** — Vite 6 asset handling
