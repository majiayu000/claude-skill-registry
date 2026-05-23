---
name: video-producer
description: Expert in video playback, streaming, and video player customization
version: 1.0.0
tags: [video, video-player, streaming, hls, adaptive-bitrate]
---

# Video Producer Skill

I help you build video players, handle video streaming, and create engaging video experiences.

## What I Do

**Video Playback:**

- Custom video players with controls
- Adaptive bitrate streaming (HLS, DASH)
- Picture-in-picture mode
- Fullscreen support

**Video Features:**

- Subtitles and captions
- Quality selection
- Playback speed control
- Thumbnail previews

**Streaming:**

- Live video streaming
- Video on demand (VOD)
- Progressive download
- Adaptive streaming

## Custom Video Player

```typescript
// components/VideoPlayer.tsx
'use client'
import { useRef, useState, useEffect } from 'react'

interface VideoPlayerProps {
  src: string
  poster?: string
  title?: string
}

export function VideoPlayer({ src, poster, title }: VideoPlayerProps) {
  const videoRef = useRef<HTMLVideoElement>(null)
  const [playing, setPlaying] = useState(false)
  const [currentTime, setCurrentTime] = useState(0)
  const [duration, setDuration] = useState(0)
  const [volume, setVolume] = useState(1)
  const [fullscreen, setFullscreen] = useState(false)
  const [showControls, setShowControls] = useState(true)

  useEffect(() => {
    const video = videoRef.current
    if (!video) return

    const updateTime = () => setCurrentTime(video.currentTime)
    const updateDuration = () => setDuration(video.duration)
    const handleEnded = () => setPlaying(false)

    video.addEventListener('timeupdate', updateTime)
    video.addEventListener('loadedmetadata', updateDuration)
    video.addEventListener('ended', handleEnded)

    return () => {
      video.removeEventListener('timeupdate', updateTime)
      video.removeEventListener('loadedmetadata', updateDuration)
      video.removeEventListener('ended', handleEnded)
    }
  }, [])

  const togglePlay = () => {
    if (!videoRef.current) return

    if (playing) {
      videoRef.current.pause()
    } else {
      videoRef.current.play()
    }
    setPlaying(!playing)
  }

  const handleSeek = (e: React.ChangeEvent<HTMLInputElement>) => {
    const time = parseFloat(e.target.value)
    setCurrentTime(time)
    if (videoRef.current) {
      videoRef.current.currentTime = time
    }
  }

  const handleVolumeChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const vol = parseFloat(e.target.value)
    setVolume(vol)
    if (videoRef.current) {
      videoRef.current.volume = vol
    }
  }

  const toggleFullscreen = () => {
    if (!videoRef.current) return

    if (!fullscreen) {
      videoRef.current.requestFullscreen()
    } else {
      document.exitFullscreen()
    }
    setFullscreen(!fullscreen)
  }

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60)
    const secs = Math.floor(seconds % 60)
    return `${mins}:${secs.toString().padStart(2, '0')}`
  }

  return (
    <div
      className="relative bg-black rounded-lg overflow-hidden"
      onMouseEnter={() => setShowControls(true)}
      onMouseLeave={() => setShowControls(playing ? false : true)}
    >
      {title && (
        <div className="absolute top-0 left-0 right-0 p-4 bg-gradient-to-b from-black/70 to-transparent z-10">
          <h3 className="text-white font-semibold">{title}</h3>
        </div>
      )}

      <video
        ref={videoRef}
        src={src}
        poster={poster}
        onClick={togglePlay}
        className="w-full"
      />

      {showControls && (
        <div className="absolute bottom-0 left-0 right-0 p-4 bg-gradient-to-t from-black/70 to-transparent">
          {/* Progress Bar */}
          <input
            type="range"
            min="0"
            max={duration || 0}
            value={currentTime}
            onChange={handleSeek}
            className="w-full mb-2"
          />

          <div className="flex items-center gap-4">
            {/* Play/Pause */}
            <button
              onClick={togglePlay}
              className="text-white text-2xl hover:scale-110 transition"
            >
              {playing ? '⏸️' : '▶️'}
            </button>

            {/* Time */}
            <span className="text-white text-sm">
              {formatTime(currentTime)} / {formatTime(duration)}
            </span>

            {/* Volume */}
            <div className="flex items-center gap-2">
              <span className="text-white">🔊</span>
              <input
                type="range"
                min="0"
                max="1"
                step="0.1"
                value={volume}
                onChange={handleVolumeChange}
                className="w-20"
              />
            </div>

            <div className="flex-1" />

            {/* Fullscreen */}
            <button
              onClick={toggleFullscreen}
              className="text-white hover:scale-110 transition"
            >
              {fullscreen ? '⬛' : '⬜'}
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
```

---

## HLS Streaming (Adaptive Bitrate)

```bash
npm install hls.js
```

```typescript
// components/HLSPlayer.tsx
'use client'
import { useEffect, useRef } from 'react'
import Hls from 'hls.js'

export function HLSPlayer({ src }: { src: string }) {
  const videoRef = useRef<HTMLVideoElement>(null)

  useEffect(() => {
    const video = videoRef.current
    if (!video) return

    if (Hls.isSupported()) {
      const hls = new Hls({
        enableWorker: true,
        lowLatencyMode: true
      })

      hls.loadSource(src)
      hls.attachMedia(video)

      hls.on(Hls.Events.MANIFEST_PARSED, () => {
        console.log('HLS manifest loaded, quality levels:', hls.levels)
      })

      hls.on(Hls.Events.ERROR, (event, data) => {
        console.error('HLS error:', data)
        if (data.fatal) {
          switch (data.type) {
            case Hls.ErrorTypes.NETWORK_ERROR:
              hls.startLoad()
              break
            case Hls.ErrorTypes.MEDIA_ERROR:
              hls.recoverMediaError()
              break
            default:
              hls.destroy()
              break
          }
        }
      })

      return () => {
        hls.destroy()
      }
    } else if (video.canPlayType('application/vnd.apple.mpegurl')) {
      // Native HLS support (Safari)
      video.src = src
    }
  }, [src])

  return <video ref={videoRef} controls className="w-full" />
}
```

---

## Picture-in-Picture

```typescript
// components/PIPVideoPlayer.tsx
'use client'
import { useRef, useState } from 'react'

export function PIPVideoPlayer({ src }: { src: string }) {
  const videoRef = useRef<HTMLVideoElement>(null)
  const [pipActive, setPipActive] = useState(false)

  const togglePIP = async () => {
    if (!videoRef.current) return

    try {
      if (!pipActive) {
        await videoRef.current.requestPictureInPicture()
        setPipActive(true)
      } else {
        await document.exitPictureInPicture()
        setPipActive(false)
      }
    } catch (error) {
      console.error('PIP error:', error)
    }
  }

  return (
    <div>
      <video ref={videoRef} src={src} controls className="w-full" />

      <button
        onClick={togglePIP}
        className="mt-4 px-4 py-2 bg-blue-600 text-white rounded"
      >
        {pipActive ? 'Exit PIP' : 'Enter PIP'}
      </button>
    </div>
  )
}
```

---

## Subtitles/Captions

```typescript
// components/VideoWithSubtitles.tsx
'use client'
export function VideoWithSubtitles() {
  return (
    <video controls className="w-full">
      <source src="/video.mp4" type="video/mp4" />

      <track
        kind="subtitles"
        src="/subtitles/en.vtt"
        srcLang="en"
        label="English"
        default
      />
      <track
        kind="subtitles"
        src="/subtitles/es.vtt"
        srcLang="es"
        label="Español"
      />
      <track
        kind="subtitles"
        src="/subtitles/fr.vtt"
        srcLang="fr"
        label="Français"
      />
    </video>
  )
}
```

**VTT Subtitle File:**

```vtt
WEBVTT

00:00:00.000 --> 00:00:02.000
Hello, welcome to our video.

00:00:02.500 --> 00:00:05.000
Today we'll learn about web development.

00:00:05.500 --> 00:00:08.000
Let's get started!
```

---

## Quality Selection

```typescript
// components/QualitySelector.tsx
'use client'
import { useState } from 'react'

const qualities = [
  { label: '1080p', src: '/video-1080p.mp4' },
  { label: '720p', src: '/video-720p.mp4' },
  { label: '480p', src: '/video-480p.mp4' },
  { label: '360p', src: '/video-360p.mp4' }
]

export function QualitySelector() {
  const [currentQuality, setCurrentQuality] = useState(qualities[1])

  return (
    <div>
      <video src={currentQuality.src} controls className="w-full" />

      <div className="mt-4">
        <label className="mr-2">Quality:</label>
        <select
          value={currentQuality.label}
          onChange={(e) => {
            const quality = qualities.find(q => q.label === e.target.value)
            if (quality) setCurrentQuality(quality)
          }}
          className="px-4 py-2 border rounded"
        >
          {qualities.map((q) => (
            <option key={q.label} value={q.label}>
              {q.label}
            </option>
          ))}
        </select>
      </div>
    </div>
  )
}
```

---

## Playback Speed Control

```typescript
// components/PlaybackSpeed.tsx
'use client'
import { useRef, useState } from 'react'

const speeds = [0.5, 0.75, 1, 1.25, 1.5, 2]

export function PlaybackSpeed({ src }: { src: string }) {
  const videoRef = useRef<HTMLVideoElement>(null)
  const [speed, setSpeed] = useState(1)

  const handleSpeedChange = (newSpeed: number) => {
    setSpeed(newSpeed)
    if (videoRef.current) {
      videoRef.current.playbackRate = newSpeed
    }
  }

  return (
    <div>
      <video ref={videoRef} src={src} controls className="w-full" />

      <div className="mt-4 flex gap-2">
        <span>Speed:</span>
        {speeds.map((s) => (
          <button
            key={s}
            onClick={() => handleSpeedChange(s)}
            className={`px-3 py-1 rounded ${
              speed === s ? 'bg-blue-600 text-white' : 'bg-gray-200'
            }`}
          >
            {s}x
          </button>
        ))}
      </div>
    </div>
  )
}
```

---

## Video Thumbnail on Hover

```typescript
// components/VideoThumbnailPreview.tsx
'use client'
import { useState } from 'react'

export function VideoThumbnailPreview({ videoSrc }: { videoSrc: string }) {
  const [thumbnailTime, setThumbnailTime] = useState(0)

  const handleProgressHover = (e: React.MouseEvent<HTMLDivElement>) => {
    const rect = e.currentTarget.getBoundingClientRect()
    const percent = (e.clientX - rect.left) / rect.width
    // Assuming 60 second video
    setThumbnailTime(percent * 60)
  }

  return (
    <div className="relative">
      <div
        onMouseMove={handleProgressHover}
        className="h-2 bg-gray-300 rounded cursor-pointer relative"
      >
        {/* Thumbnail preview */}
        <div
          className="absolute bottom-4 -translate-x-1/2 pointer-events-none"
          style={{ left: `${(thumbnailTime / 60) * 100}%` }}
        >
          <video
            src={videoSrc}
            className="w-40 h-24 object-cover rounded shadow-lg"
            muted
            currentTime={thumbnailTime}
          />
          <span className="block text-center text-sm mt-1">
            {Math.floor(thumbnailTime)}s
          </span>
        </div>
      </div>

      <video src={videoSrc} controls className="w-full mt-4" />
    </div>
  )
}
```

---

## Video Upload with Progress

```typescript
// components/VideoUpload.tsx
'use client'
import { useState } from 'react'

export function VideoUpload() {
  const [uploading, setUploading] = useState(false)
  const [progress, setProgress] = useState(0)
  const [videoURL, setVideoURL] = useState<string | null>(null)

  const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return

    setUploading(true)
    setProgress(0)

    const formData = new FormData()
    formData.append('video', file)

    const xhr = new XMLHttpRequest()

    xhr.upload.addEventListener('progress', (e) => {
      if (e.lengthComputable) {
        const percentComplete = (e.loaded / e.total) * 100
        setProgress(percentComplete)
      }
    })

    xhr.addEventListener('load', () => {
      if (xhr.status === 200) {
        const response = JSON.parse(xhr.responseText)
        setVideoURL(response.url)
      }
      setUploading(false)
    })

    xhr.open('POST', '/api/upload/video')
    xhr.send(formData)
  }

  return (
    <div>
      <input
        type="file"
        accept="video/*"
        onChange={handleUpload}
        disabled={uploading}
        className="mb-4"
      />

      {uploading && (
        <div className="mb-4">
          <div className="h-2 bg-gray-200 rounded overflow-hidden">
            <div
              className="h-full bg-blue-600 transition-all"
              style={{ width: `${progress}%` }}
            />
          </div>
          <p className="text-sm text-gray-600 mt-1">
            Uploading: {Math.round(progress)}%
          </p>
        </div>
      )}

      {videoURL && (
        <video src={videoURL} controls className="w-full" />
      )}
    </div>
  )
}
```

---

## When to Use Me

**Perfect for:**

- Building video platforms
- Adding video content
- Implementing video streaming
- Creating video courses
- Building video players

**I'll help you:**

- Build custom video players
- Implement HLS streaming
- Add subtitles/captions
- Support multiple qualities
- Handle video uploads

## What I'll Create

```
🎥 Custom Video Players
📺 HLS/Adaptive Streaming
📝 Subtitles & Captions
⚙️ Quality Selection
⏩ Playback Speed Control
🖼️ Picture-in-Picture
```

Let's create amazing video experiences!
