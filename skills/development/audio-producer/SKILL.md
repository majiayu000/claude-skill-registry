---
name: audio-producer
description: Expert in web audio, audio processing, and interactive sound design
version: 1.0.0
tags: [audio, web-audio-api, sound-design, audio-player, podcasts]
---

# Audio Producer Skill

I help you build audio players, process audio, and create interactive sound experiences for the web.

## What I Do

**Audio Playback:**

- Custom audio players
- Playlist management
- Playback controls (play, pause, seek, volume)
- Waveform visualization

**Audio Processing:**

- Audio effects (reverb, delay, filters)
- Equalization and mixing
- Audio recording
- Real-time audio manipulation

**Interactive Audio:**

- Background music and sound effects
- User interaction sounds
- Spatial audio
- Audio notifications

## Custom Audio Player

```typescript
// components/AudioPlayer.tsx
'use client'
import { useState, useRef, useEffect } from 'react'

interface AudioPlayerProps {
  src: string
  title?: string
  artist?: string
}

export function AudioPlayer({ src, title, artist }: AudioPlayerProps) {
  const audioRef = useRef<HTMLAudioElement>(null)
  const [playing, setPlaying] = useState(false)
  const [currentTime, setCurrentTime] = useState(0)
  const [duration, setDuration] = useState(0)
  const [volume, setVolume] = useState(1)

  useEffect(() => {
    const audio = audioRef.current
    if (!audio) return

    const updateTime = () => setCurrentTime(audio.currentTime)
    const updateDuration = () => setDuration(audio.duration)

    audio.addEventListener('timeupdate', updateTime)
    audio.addEventListener('loadedmetadata', updateDuration)
    audio.addEventListener('ended', () => setPlaying(false))

    return () => {
      audio.removeEventListener('timeupdate', updateTime)
      audio.removeEventListener('loadedmetadata', updateDuration)
      audio.removeEventListener('ended', () => setPlaying(false))
    }
  }, [])

  const togglePlay = () => {
    if (!audioRef.current) return

    if (playing) {
      audioRef.current.pause()
    } else {
      audioRef.current.play()
    }
    setPlaying(!playing)
  }

  const handleSeek = (e: React.ChangeEvent<HTMLInputElement>) => {
    const time = parseFloat(e.target.value)
    setCurrentTime(time)
    if (audioRef.current) {
      audioRef.current.currentTime = time
    }
  }

  const handleVolumeChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const vol = parseFloat(e.target.value)
    setVolume(vol)
    if (audioRef.current) {
      audioRef.current.volume = vol
    }
  }

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60)
    const secs = Math.floor(seconds % 60)
    return `${mins}:${secs.toString().padStart(2, '0')}`
  }

  return (
    <div className="bg-white rounded-lg shadow-lg p-6 max-w-md">
      <audio ref={audioRef} src={src} />

      {/* Track Info */}
      {(title || artist) && (
        <div className="mb-4">
          {title && <h3 className="font-semibold text-lg">{title}</h3>}
          {artist && <p className="text-gray-600 text-sm">{artist}</p>}
        </div>
      )}

      {/* Progress Bar */}
      <div className="mb-4">
        <input
          type="range"
          min="0"
          max={duration || 0}
          value={currentTime}
          onChange={handleSeek}
          className="w-full"
        />
        <div className="flex justify-between text-sm text-gray-600 mt-1">
          <span>{formatTime(currentTime)}</span>
          <span>{formatTime(duration)}</span>
        </div>
      </div>

      {/* Controls */}
      <div className="flex items-center gap-4">
        <button
          onClick={togglePlay}
          className="w-12 h-12 bg-blue-600 text-white rounded-full flex items-center justify-center hover:bg-blue-700"
        >
          {playing ? '⏸️' : '▶️'}
        </button>

        <div className="flex items-center gap-2 flex-1">
          <span className="text-sm">🔊</span>
          <input
            type="range"
            min="0"
            max="1"
            step="0.1"
            value={volume}
            onChange={handleVolumeChange}
            className="flex-1"
          />
        </div>
      </div>
    </div>
  )
}
```

---

## Podcast Player

```typescript
// components/PodcastPlayer.tsx
'use client'
import { useState } from 'react'
import { AudioPlayer } from './AudioPlayer'

interface Episode {
  id: string
  title: string
  description: string
  audioUrl: string
  duration: number
  publishedAt: string
}

export function PodcastPlayer({ episodes }: { episodes: Episode[] }) {
  const [currentEpisode, setCurrentEpisode] = useState<Episode>(episodes[0])

  return (
    <div>
      <AudioPlayer
        src={currentEpisode.audioUrl}
        title={currentEpisode.title}
      />

      <div className="mt-6">
        <h3 className="font-semibold mb-4">Episodes</h3>
        <div className="space-y-2">
          {episodes.map((episode) => (
            <button
              key={episode.id}
              onClick={() => setCurrentEpisode(episode)}
              className={`w-full text-left p-4 rounded-lg ${
                currentEpisode.id === episode.id
                  ? 'bg-blue-100 border-2 border-blue-600'
                  : 'bg-gray-100'
              }`}
            >
              <h4 className="font-medium">{episode.title}</h4>
              <p className="text-sm text-gray-600 mt-1">
                {episode.description}
              </p>
              <p className="text-xs text-gray-500 mt-2">
                {new Date(episode.publishedAt).toLocaleDateString()}
              </p>
            </button>
          ))}
        </div>
      </div>
    </div>
  )
}
```

---

## Waveform Visualization

```typescript
// components/Waveform.tsx
'use client'
import { useEffect, useRef } from 'react'

export function Waveform({ audioSrc }: { audioSrc: string }) {
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const audioRef = useRef<HTMLAudioElement>(null)

  useEffect(() => {
    const canvas = canvasRef.current
    const audio = audioRef.current
    if (!canvas || !audio) return

    const ctx = canvas.getContext('2d')
    if (!ctx) return

    const audioContext = new AudioContext()
    const source = audioContext.createMediaElementSource(audio)
    const analyser = audioContext.createAnalyser()

    source.connect(analyser)
    analyser.connect(audioContext.destination)

    analyser.fftSize = 256
    const bufferLength = analyser.frequencyBinCount
    const dataArray = new Uint8Array(bufferLength)

    const draw = () => {
      requestAnimationFrame(draw)

      analyser.getByteFrequencyData(dataArray)

      ctx.fillStyle = 'rgb(0, 0, 0)'
      ctx.fillRect(0, 0, canvas.width, canvas.height)

      const barWidth = (canvas.width / bufferLength) * 2.5
      let x = 0

      for (let i = 0; i < bufferLength; i++) {
        const barHeight = (dataArray[i] / 255) * canvas.height

        ctx.fillStyle = `rgb(${barHeight + 100}, 50, 50)`
        ctx.fillRect(x, canvas.height - barHeight, barWidth, barHeight)

        x += barWidth + 1
      }
    }

    draw()
  }, [audioSrc])

  return (
    <div>
      <audio ref={audioRef} src={audioSrc} controls />
      <canvas ref={canvasRef} width={600} height={200} />
    </div>
  )
}
```

---

## Audio Recording

```typescript
// hooks/useAudioRecorder.ts
'use client'
import { useState, useRef } from 'react'

export function useAudioRecorder() {
  const [recording, setRecording] = useState(false)
  const [audioURL, setAudioURL] = useState<string | null>(null)
  const mediaRecorderRef = useRef<MediaRecorder | null>(null)
  const chunksRef = useRef<Blob[]>([])

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      const mediaRecorder = new MediaRecorder(stream)

      mediaRecorder.ondataavailable = e => {
        chunksRef.current.push(e.data)
      }

      mediaRecorder.onstop = () => {
        const blob = new Blob(chunksRef.current, { type: 'audio/webm' })
        const url = URL.createObjectURL(blob)
        setAudioURL(url)
        chunksRef.current = []
      }

      mediaRecorder.start()
      mediaRecorderRef.current = mediaRecorder
      setRecording(true)
    } catch (error) {
      console.error('Failed to start recording:', error)
    }
  }

  const stopRecording = () => {
    if (mediaRecorderRef.current && recording) {
      mediaRecorderRef.current.stop()
      mediaRecorderRef.current.stream.getTracks().forEach(track => track.stop())
      setRecording(false)
    }
  }

  return { recording, audioURL, startRecording, stopRecording }
}
```

**Usage:**

```typescript
'use client'
import { useAudioRecorder } from '@/hooks/useAudioRecorder'

export function VoiceRecorder() {
  const { recording, audioURL, startRecording, stopRecording } = useAudioRecorder()

  return (
    <div>
      <button
        onClick={recording ? stopRecording : startRecording}
        className={`px-6 py-3 rounded-lg ${
          recording ? 'bg-red-600' : 'bg-blue-600'
        } text-white`}
      >
        {recording ? '⏹️ Stop Recording' : '🎤 Start Recording'}
      </button>

      {audioURL && (
        <div className="mt-4">
          <audio src={audioURL} controls />
          <a
            href={audioURL}
            download="recording.webm"
            className="mt-2 inline-block px-4 py-2 bg-green-600 text-white rounded"
          >
            Download Recording
          </a>
        </div>
      )}
    </div>
  )
}
```

---

## Audio Effects

```typescript
// lib/audio-effects.ts

export class AudioEffects {
  private audioContext: AudioContext
  private source: MediaElementAudioSourceNode
  private gainNode: GainNode
  private filterNode: BiquadFilterNode

  constructor(audioElement: HTMLAudioElement) {
    this.audioContext = new AudioContext()
    this.source = this.audioContext.createMediaElementSource(audioElement)
    this.gainNode = this.audioContext.createGain()
    this.filterNode = this.audioContext.createBiquadFilter()

    // Connect: source -> filter -> gain -> destination
    this.source.connect(this.filterNode)
    this.filterNode.connect(this.gainNode)
    this.gainNode.connect(this.audioContext.destination)
  }

  setVolume(value: number) {
    this.gainNode.gain.value = value
  }

  setLowPassFilter(frequency: number) {
    this.filterNode.type = 'lowpass'
    this.filterNode.frequency.value = frequency
  }

  setHighPassFilter(frequency: number) {
    this.filterNode.type = 'highpass'
    this.filterNode.frequency.value = frequency
  }

  setBandPassFilter(frequency: number) {
    this.filterNode.type = 'bandpass'
    this.filterNode.frequency.value = frequency
  }
}
```

---

## Spatial Audio

```typescript
// components/SpatialAudio.tsx
'use client'
import { useEffect, useRef, useState } from 'react'

export function SpatialAudio({ audioSrc }: { audioSrc: string }) {
  const audioRef = useRef<HTMLAudioElement>(null)
  const [position, setPosition] = useState({ x: 0, y: 0 })

  useEffect(() => {
    const audio = audioRef.current
    if (!audio) return

    const audioContext = new AudioContext()
    const source = audioContext.createMediaElementSource(audio)
    const panner = audioContext.createPanner()

    panner.panningModel = 'HRTF'
    panner.distanceModel = 'inverse'
    panner.refDistance = 1
    panner.maxDistance = 10000

    source.connect(panner)
    panner.connect(audioContext.destination)

    // Update panner position based on mouse/touch
    panner.setPosition(position.x, position.y, 0)
  }, [position])

  return (
    <div
      onMouseMove={(e) => {
        const rect = e.currentTarget.getBoundingClientRect()
        const x = ((e.clientX - rect.left) / rect.width) * 2 - 1
        const y = ((e.clientY - rect.top) / rect.height) * 2 - 1
        setPosition({ x, y })
      }}
      className="w-full h-96 bg-gray-100 rounded-lg flex items-center justify-center cursor-crosshair"
    >
      <audio ref={audioRef} src={audioSrc} controls />
      <p className="absolute text-center text-sm text-gray-600">
        Move your mouse to change sound position
      </p>
    </div>
  )
}
```

---

## When to Use Me

**Perfect for:**

- Building audio players
- Creating podcast platforms
- Adding sound effects
- Implementing voice recording
- Processing audio in real-time

**I'll help you:**

- Build custom audio players
- Add waveform visualizations
- Implement audio recording
- Apply audio effects
- Create spatial audio experiences

## What I'll Create

```
🎵 Audio Players
🎙️ Voice Recorders
📊 Waveform Visualizations
🎛️ Audio Effects
🎧 Spatial Audio
🎼 Playlist Management
```

Let's create amazing audio experiences!
