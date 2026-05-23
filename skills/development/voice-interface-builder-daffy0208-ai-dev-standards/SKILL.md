---
name: voice-interface-builder
description: Expert in building voice interfaces, speech recognition, and text-to-speech systems
version: 1.0.0
tags: [voice, speech-recognition, text-to-speech, web-speech-api, accessibility]
---

# Voice Interface Builder Skill

I help you build voice-enabled interfaces using the Web Speech API and modern voice technologies.

## What I Do

**Speech Recognition:**

- Voice commands and controls
- Voice-to-text input
- Continuous dictation
- Command detection

**Text-to-Speech:**

- Reading content aloud
- Voice feedback and notifications
- Multilingual speech output
- Voice selection and customization

**Voice UI:**

- Voice-first interfaces
- Accessibility features
- Hands-free controls
- Voice search

## Web Speech API Basics

### Speech Recognition

```typescript
// hooks/useSpeechRecognition.ts
'use client'
import { useState, useEffect, useRef } from 'react'

interface SpeechRecognitionOptions {
  continuous?: boolean
  language?: string
  onResult?: (transcript: string) => void
  onError?: (error: string) => void
}

export function useSpeechRecognition({
  continuous = false,
  language = 'en-US',
  onResult,
  onError
}: SpeechRecognitionOptions = {}) {
  const [isListening, setIsListening] = useState(false)
  const [transcript, setTranscript] = useState('')
  const recognitionRef = useRef<SpeechRecognition | null>(null)

  useEffect(() => {
    if (typeof window === 'undefined') return

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition

    if (!SpeechRecognition) {
      console.warn('Speech recognition not supported')
      return
    }

    const recognition = new SpeechRecognition()
    recognition.continuous = continuous
    recognition.lang = language
    recognition.interimResults = true

    recognition.onresult = event => {
      const transcript = Array.from(event.results)
        .map(result => result[0].transcript)
        .join('')

      setTranscript(transcript)
      onResult?.(transcript)
    }

    recognition.onerror = event => {
      console.error('Speech recognition error:', event.error)
      onError?.(event.error)
      setIsListening(false)
    }

    recognition.onend = () => {
      setIsListening(false)
    }

    recognitionRef.current = recognition

    return () => {
      recognition.stop()
    }
  }, [continuous, language, onResult, onError])

  const start = () => {
    if (recognitionRef.current && !isListening) {
      recognitionRef.current.start()
      setIsListening(true)
    }
  }

  const stop = () => {
    if (recognitionRef.current && isListening) {
      recognitionRef.current.stop()
      setIsListening(false)
    }
  }

  return { isListening, transcript, start, stop }
}
```

**Usage:**

```typescript
'use client'
import { useSpeechRecognition } from '@/hooks/useSpeechRecognition'

export function VoiceInput() {
  const { isListening, transcript, start, stop } = useSpeechRecognition({
    onResult: (text) => console.log('Recognized:', text)
  })

  return (
    <div>
      <button onClick={isListening ? stop : start}>
        {isListening ? '🔴 Stop' : '🎤 Start Listening'}
      </button>
      <p>{transcript}</p>
    </div>
  )
}
```

---

### Text-to-Speech

```typescript
// hooks/useSpeechSynthesis.ts
'use client'
import { useState, useEffect } from 'react'

export function useSpeechSynthesis() {
  const [voices, setVoices] = useState<SpeechSynthesisVoice[]>([])
  const [speaking, setSpeaking] = useState(false)

  useEffect(() => {
    if (typeof window === 'undefined') return

    const loadVoices = () => {
      const availableVoices = window.speechSynthesis.getVoices()
      setVoices(availableVoices)
    }

    loadVoices()
    window.speechSynthesis.onvoiceschanged = loadVoices
  }, [])

  const speak = (
    text: string,
    options?: {
      voice?: SpeechSynthesisVoice
      rate?: number
      pitch?: number
      volume?: number
    }
  ) => {
    if (typeof window === 'undefined') return

    const utterance = new SpeechSynthesisUtterance(text)

    if (options?.voice) utterance.voice = options.voice
    if (options?.rate) utterance.rate = options.rate // 0.1 - 10
    if (options?.pitch) utterance.pitch = options.pitch // 0 - 2
    if (options?.volume) utterance.volume = options.volume // 0 - 1

    utterance.onstart = () => setSpeaking(true)
    utterance.onend = () => setSpeaking(false)
    utterance.onerror = () => setSpeaking(false)

    window.speechSynthesis.speak(utterance)
  }

  const cancel = () => {
    if (typeof window !== 'undefined') {
      window.speechSynthesis.cancel()
      setSpeaking(false)
    }
  }

  return { speak, cancel, speaking, voices }
}
```

**Usage:**

```typescript
'use client'
import { useSpeechSynthesis } from '@/hooks/useSpeechSynthesis'

export function TextToSpeech() {
  const { speak, cancel, speaking, voices } = useSpeechSynthesis()
  const [text, setText] = useState('Hello, how can I help you today?')

  return (
    <div>
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        rows={4}
      />

      <button
        onClick={() => speak(text)}
        disabled={speaking}
      >
        {speaking ? 'Speaking...' : '🔊 Speak'}
      </button>

      <button onClick={cancel} disabled={!speaking}>
        ⏹️ Stop
      </button>

      <select onChange={(e) => {
        const voice = voices.find(v => v.name === e.target.value)
        if (voice) speak(text, { voice })
      }}>
        {voices.map((voice) => (
          <option key={voice.name} value={voice.name}>
            {voice.name} ({voice.lang})
          </option>
        ))}
      </select>
    </div>
  )
}
```

---

## Voice Commands

### Command Detection

```typescript
'use client'
import { useSpeechRecognition } from '@/hooks/useSpeechRecognition'
import { useEffect } from 'react'

interface Command {
  phrase: string | RegExp
  action: () => void
}

export function VoiceCommands({ commands }: { commands: Command[] }) {
  const { isListening, transcript, start, stop } = useSpeechRecognition({
    continuous: true
  })

  useEffect(() => {
    if (!transcript) return

    const lowerTranscript = transcript.toLowerCase()

    for (const command of commands) {
      if (typeof command.phrase === 'string') {
        if (lowerTranscript.includes(command.phrase.toLowerCase())) {
          command.action()
        }
      } else {
        if (command.phrase.test(lowerTranscript)) {
          command.action()
        }
      }
    }
  }, [transcript, commands])

  return (
    <button onClick={isListening ? stop : start}>
      {isListening ? '🔴 Stop Voice Commands' : '🎤 Start Voice Commands'}
    </button>
  )
}
```

**Usage:**

```typescript
export function App() {
  const commands = [
    {
      phrase: 'go home',
      action: () => router.push('/')
    },
    {
      phrase: 'open menu',
      action: () => setMenuOpen(true)
    },
    {
      phrase: 'search for',
      action: () => {
        // Extract search query after "search for"
      }
    }
  ]

  return <VoiceCommands commands={commands} />
}
```

---

## Voice Search

```typescript
'use client'
import { useSpeechRecognition } from '@/hooks/useSpeechRecognition'
import { useState } from 'react'

export function VoiceSearch() {
  const [query, setQuery] = useState('')

  const { isListening, start, stop } = useSpeechRecognition({
    onResult: (transcript) => {
      setQuery(transcript)
    }
  })

  const handleSearch = () => {
    if (query) {
      // Perform search with query
      console.log('Searching for:', query)
    }
  }

  return (
    <div className="flex gap-2">
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Search or speak..."
        className="flex-1 px-4 py-2 border rounded"
      />

      <button
        onClick={isListening ? stop : start}
        className={`px-4 py-2 rounded ${
          isListening ? 'bg-red-600 text-white' : 'bg-gray-200'
        }`}
      >
        {isListening ? '🔴' : '🎤'}
      </button>

      <button
        onClick={handleSearch}
        className="px-4 py-2 bg-blue-600 text-white rounded"
      >
        Search
      </button>
    </div>
  )
}
```

---

## Accessibility Features

### Read Article Aloud

```typescript
'use client'
import { useSpeechSynthesis } from '@/hooks/useSpeechSynthesis'

export function ReadAloudButton({ content }: { content: string }) {
  const { speak, cancel, speaking } = useSpeechSynthesis()

  return (
    <button
      onClick={() => speaking ? cancel() : speak(content)}
      className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded"
    >
      {speaking ? '⏹️ Stop Reading' : '🔊 Read Aloud'}
    </button>
  )
}
```

### Voice Navigation

```typescript
'use client'
import { useRouter } from 'next/navigation'
import { useSpeechRecognition } from '@/hooks/useSpeechRecognition'
import { useEffect } from 'react'

export function VoiceNavigation() {
  const router = useRouter()
  const { isListening, transcript, start, stop } = useSpeechRecognition()

  useEffect(() => {
    const lower = transcript.toLowerCase()

    if (lower.includes('go to home')) router.push('/')
    else if (lower.includes('go to about')) router.push('/about')
    else if (lower.includes('go to contact')) router.push('/contact')
    else if (lower.includes('go back')) router.back()
  }, [transcript, router])

  return (
    <button onClick={isListening ? stop : start}>
      {isListening ? 'Disable Voice Nav' : 'Enable Voice Nav'}
    </button>
  )
}
```

---

## Voice Dictation

```typescript
'use client'
import { useSpeechRecognition } from '@/hooks/useSpeechRecognition'
import { useState } from 'react'

export function VoiceDictation() {
  const [text, setText] = useState('')

  const { isListening, start, stop } = useSpeechRecognition({
    continuous: true,
    onResult: (transcript) => {
      setText(transcript)
    }
  })

  return (
    <div>
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        rows={10}
        className="w-full p-4 border rounded"
        placeholder="Start dictating..."
      />

      <div className="mt-4 flex gap-2">
        <button
          onClick={isListening ? stop : start}
          className={`px-4 py-2 rounded ${
            isListening ? 'bg-red-600 text-white' : 'bg-blue-600 text-white'
          }`}
        >
          {isListening ? '🔴 Stop Dictation' : '🎤 Start Dictation'}
        </button>

        <button
          onClick={() => setText('')}
          className="px-4 py-2 bg-gray-200 rounded"
        >
          Clear
        </button>
      </div>
    </div>
  )
}
```

---

## Multilingual Support

```typescript
'use client'
import { useSpeechRecognition } from '@/hooks/useSpeechRecognition'
import { useSpeechSynthesis } from '@/hooks/useSpeechSynthesis'
import { useState } from 'react'

const languages = [
  { code: 'en-US', name: 'English (US)' },
  { code: 'es-ES', name: 'Spanish (Spain)' },
  { code: 'fr-FR', name: 'French (France)' },
  { code: 'de-DE', name: 'German (Germany)' },
  { code: 'ja-JP', name: 'Japanese' },
  { code: 'zh-CN', name: 'Chinese (Simplified)' }
]

export function MultilingualVoice() {
  const [language, setLanguage] = useState('en-US')
  const [text, setText] = useState('')

  const { isListening, transcript, start, stop } = useSpeechRecognition({
    language,
    onResult: (t) => setText(t)
  })

  const { speak } = useSpeechSynthesis()

  return (
    <div>
      <select
        value={language}
        onChange={(e) => setLanguage(e.target.value)}
        className="px-4 py-2 border rounded"
      >
        {languages.map((lang) => (
          <option key={lang.code} value={lang.code}>
            {lang.name}
          </option>
        ))}
      </select>

      <div className="mt-4">
        <button onClick={isListening ? stop : start}>
          {isListening ? '🔴 Stop' : '🎤 Speak'}
        </button>

        <button onClick={() => speak(text)}>
          🔊 Read Aloud
        </button>
      </div>

      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        rows={4}
        className="w-full mt-4 p-4 border rounded"
      />
    </div>
  )
}
```

---

## Voice Feedback

```typescript
'use client'
import { useSpeechSynthesis } from '@/hooks/useSpeechSynthesis'

export function useVoiceFeedback() {
  const { speak } = useSpeechSynthesis()

  const announce = (message: string) => {
    speak(message, { rate: 1.1, volume: 0.8 })
  }

  return {
    success: (message: string) => announce(`Success: ${message}`),
    error: (message: string) => announce(`Error: ${message}`),
    info: (message: string) => announce(message),
    confirm: (action: string) => announce(`${action} confirmed`)
  }
}

// Usage
export function Form() {
  const voice = useVoiceFeedback()

  const handleSubmit = async () => {
    try {
      await submitForm()
      voice.success('Form submitted successfully')
    } catch (error) {
      voice.error('Failed to submit form')
    }
  }

  return <form onSubmit={handleSubmit}>...</form>
}
```

---

## When to Use Me

**Perfect for:**

- Building voice-controlled interfaces
- Adding accessibility features
- Creating hands-free experiences
- Implementing voice search
- Building voice assistants

**I'll help you:**

- Implement speech recognition
- Add text-to-speech
- Build voice commands
- Support multiple languages
- Create accessible voice UI

## What I'll Create

```
🎤 Speech Recognition
🔊 Text-to-Speech
🗣️ Voice Commands
🔍 Voice Search
🌍 Multilingual Support
♿ Accessibility Features
```

Let's make your app voice-enabled!
