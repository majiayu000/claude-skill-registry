---
name: livestream-engineer
description: Expert in live streaming, WebRTC, and real-time video/audio
version: 1.0.0
tags: [livestream, webrtc, real-time, streaming, broadcasting]
---

# Livestream Engineer Skill

I help you build live streaming features, implement WebRTC, and create real-time broadcasting experiences.

## What I Do

**Live Streaming:**

- WebRTC peer-to-peer video
- Live broadcasting
- Screen sharing
- Real-time chat

**Streaming Platforms:**

- Twitch-style streaming
- Video conferencing
- Live events
- Webinars

## WebRTC Basics

### Peer-to-Peer Video Call

```typescript
// lib/webrtc.ts
export class WebRTCConnection {
  private peerConnection: RTCPeerConnection
  private localStream: MediaStream | null = null

  constructor() {
    this.peerConnection = new RTCPeerConnection({
      iceServers: [{ urls: 'stun:stun.l.google.com:19302' }]
    })
  }

  async startLocalStream() {
    try {
      this.localStream = await navigator.mediaDevices.getUserMedia({
        video: true,
        audio: true
      })

      this.localStream.getTracks().forEach(track => {
        this.peerConnection.addTrack(track, this.localStream!)
      })

      return this.localStream
    } catch (error) {
      console.error('Failed to get local stream:', error)
      throw error
    }
  }

  async createOffer() {
    const offer = await this.peerConnection.createOffer()
    await this.peerConnection.setLocalDescription(offer)
    return offer
  }

  async handleAnswer(answer: RTCSessionDescriptionInit) {
    await this.peerConnection.setRemoteDescription(answer)
  }

  async handleOffer(offer: RTCSessionDescriptionInit) {
    await this.peerConnection.setRemoteDescription(offer)
    const answer = await this.peerConnection.createAnswer()
    await this.peerConnection.setLocalDescription(answer)
    return answer
  }

  addIceCandidate(candidate: RTCIceCandidateInit) {
    return this.peerConnection.addIceCandidate(candidate)
  }

  onTrack(callback: (stream: MediaStream) => void) {
    this.peerConnection.ontrack = event => {
      callback(event.streams[0])
    }
  }

  onIceCandidate(callback: (candidate: RTCIceCandidate) => void) {
    this.peerConnection.onicecandidate = event => {
      if (event.candidate) {
        callback(event.candidate)
      }
    }
  }

  close() {
    this.localStream?.getTracks().forEach(track => track.stop())
    this.peerConnection.close()
  }
}
```

**Usage:**

```typescript
'use client'
import { useEffect, useRef, useState } from 'react'
import { WebRTCConnection } from '@/lib/webrtc'

export function VideoCall() {
  const localVideoRef = useRef<HTMLVideoElement>(null)
  const remoteVideoRef = useRef<HTMLVideoElement>(null)
  const [connection] = useState(() => new WebRTCConnection())

  useEffect(() => {
    const init = async () => {
      // Start local stream
      const stream = await connection.startLocalStream()
      if (localVideoRef.current) {
        localVideoRef.current.srcObject = stream
      }

      // Handle remote stream
      connection.onTrack((remoteStream) => {
        if (remoteVideoRef.current) {
          remoteVideoRef.current.srcObject = remoteStream
        }
      })

      // Handle ICE candidates
      connection.onIceCandidate((candidate) => {
        // Send candidate to other peer via signaling server
        socket.emit('ice-candidate', candidate)
      })
    }

    init()

    return () => {
      connection.close()
    }
  }, [connection])

  return (
    <div className="grid grid-cols-2 gap-4">
      <div>
        <h3>You</h3>
        <video ref={localVideoRef} autoPlay muted className="w-full" />
      </div>
      <div>
        <h3>Remote</h3>
        <video ref={remoteVideoRef} autoPlay className="w-full" />
      </div>
    </div>
  )
}
```

---

## Screen Sharing

```typescript
'use client'
import { useRef, useState } from 'react'

export function ScreenShare() {
  const videoRef = useRef<HTMLVideoElement>(null)
  const [sharing, setSharing] = useState(false)
  const [stream, setStream] = useState<MediaStream | null>(null)

  const startSharing = async () => {
    try {
      const mediaStream = await navigator.mediaDevices.getDisplayMedia({
        video: {
          cursor: 'always'
        },
        audio: false
      })

      setStream(mediaStream)
      if (videoRef.current) {
        videoRef.current.srcObject = mediaStream
      }
      setSharing(true)

      // Handle when user stops sharing via browser UI
      mediaStream.getVideoTracks()[0].onended = () => {
        stopSharing()
      }
    } catch (error) {
      console.error('Failed to start screen sharing:', error)
    }
  }

  const stopSharing = () => {
    stream?.getTracks().forEach(track => track.stop())
    setStream(null)
    setSharing(false)
  }

  return (
    <div>
      <video ref={videoRef} autoPlay className="w-full bg-black rounded" />

      <button
        onClick={sharing ? stopSharing : startSharing}
        className={`mt-4 px-6 py-3 rounded ${
          sharing ? 'bg-red-600' : 'bg-blue-600'
        } text-white`}
      >
        {sharing ? '⏹️ Stop Sharing' : '🖥️ Share Screen'}
      </button>
    </div>
  )
}
```

---

## Live Streaming with Chat

```typescript
// components/LiveStream.tsx
'use client'
import { useState, useEffect, useRef } from 'react'
import { io, Socket } from 'socket.io-client'

interface ChatMessage {
  user: string
  message: string
  timestamp: Date
}

export function LiveStream({ streamId }: { streamId: string }) {
  const videoRef = useRef<HTMLVideoElement>(null)
  const [socket, setSocket] = useState<Socket | null>(null)
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [messageInput, setMessageInput] = useState('')
  const [viewers, setViewers] = useState(0)

  useEffect(() => {
    // Connect to streaming server
    const newSocket = io('wss://streaming-server.com')
    setSocket(newSocket)

    // Join stream room
    newSocket.emit('join-stream', streamId)

    // Receive viewer count
    newSocket.on('viewer-count', (count: number) => {
      setViewers(count)
    })

    // Receive chat messages
    newSocket.on('chat-message', (msg: ChatMessage) => {
      setMessages(prev => [...prev, msg])
    })

    // Receive video stream chunks (simplified)
    newSocket.on('stream-data', (data: ArrayBuffer) => {
      // Handle stream data
    })

    return () => {
      newSocket.disconnect()
    }
  }, [streamId])

  const sendMessage = () => {
    if (!socket || !messageInput.trim()) return

    socket.emit('chat-message', {
      user: 'Anonymous',
      message: messageInput,
      timestamp: new Date()
    })

    setMessageInput('')
  }

  return (
    <div className="grid md:grid-cols-3 gap-4">
      {/* Video Player */}
      <div className="md:col-span-2">
        <div className="bg-black rounded-lg overflow-hidden">
          <video
            ref={videoRef}
            autoPlay
            controls
            className="w-full aspect-video"
          />

          <div className="p-4 bg-gray-900 text-white">
            <h2 className="text-xl font-bold">Live Stream Title</h2>
            <p className="text-sm text-gray-400">
              🔴 {viewers} watching now
            </p>
          </div>
        </div>
      </div>

      {/* Chat */}
      <div className="flex flex-col h-[600px]">
        <div className="bg-gray-100 p-4 rounded-t-lg font-semibold">
          Live Chat
        </div>

        <div className="flex-1 overflow-y-auto p-4 bg-white border-x">
          {messages.map((msg, i) => (
            <div key={i} className="mb-3">
              <span className="font-semibold text-blue-600">{msg.user}:</span>
              <span className="ml-2">{msg.message}</span>
            </div>
          ))}
        </div>

        <div className="p-4 bg-gray-100 rounded-b-lg">
          <input
            type="text"
            value={messageInput}
            onChange={(e) => setMessageInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
            placeholder="Say something..."
            className="w-full px-4 py-2 border rounded"
          />
        </div>
      </div>
    </div>
  )
}
```

---

## Broadcasting Dashboard

```typescript
// components/BroadcastDashboard.tsx
'use client'
import { useState, useRef } from 'react'

export function BroadcastDashboard() {
  const videoRef = useRef<HTMLVideoElement>(null)
  const [broadcasting, setBroadcasting] = useState(false)
  const [stream, setStream] = useState<MediaStream | null>(null)
  const [viewers, setViewers] = useState(0)

  const startBroadcast = async () => {
    try {
      const mediaStream = await navigator.mediaDevices.getUserMedia({
        video: {
          width: { ideal: 1920 },
          height: { ideal: 1080 }
        },
        audio: {
          echoCancellation: true,
          noiseSuppression: true
        }
      })

      setStream(mediaStream)
      if (videoRef.current) {
        videoRef.current.srcObject = mediaStream
      }

      // Start broadcasting to server
      // (Implementation depends on streaming protocol)

      setBroadcasting(true)
    } catch (error) {
      console.error('Failed to start broadcast:', error)
    }
  }

  const stopBroadcast = () => {
    stream?.getTracks().forEach(track => track.stop())
    setStream(null)
    setBroadcasting(false)
  }

  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="mb-6">
        <h1 className="text-3xl font-bold">Broadcast Dashboard</h1>
        {broadcasting && (
          <p className="text-green-600 font-semibold mt-2">
            🔴 LIVE - {viewers} viewers
          </p>
        )}
      </div>

      <div className="bg-black rounded-lg overflow-hidden mb-6">
        <video
          ref={videoRef}
          autoPlay
          muted
          className="w-full aspect-video"
        />
      </div>

      <div className="flex gap-4">
        <button
          onClick={broadcasting ? stopBroadcast : startBroadcast}
          className={`flex-1 py-3 rounded-lg font-semibold ${
            broadcasting
              ? 'bg-red-600 text-white'
              : 'bg-blue-600 text-white'
          }`}
        >
          {broadcasting ? '⏹️ End Broadcast' : '🔴 Start Broadcast'}
        </button>

        {broadcasting && (
          <button className="px-6 py-3 bg-gray-200 rounded-lg">
            ⚙️ Settings
          </button>
        )}
      </div>
    </div>
  )
}
```

---

## Multi-Party Video Conference

```typescript
// components/VideoConference.tsx
'use client'
import { useEffect, useState, useRef } from 'react'

interface Participant {
  id: string
  name: string
  stream: MediaStream
}

export function VideoConference() {
  const [participants, setParticipants] = useState<Participant[]>([])
  const localVideoRef = useRef<HTMLVideoElement>(null)

  useEffect(() => {
    // Initialize local stream
    navigator.mediaDevices.getUserMedia({ video: true, audio: true })
      .then(stream => {
        if (localVideoRef.current) {
          localVideoRef.current.srcObject = stream
        }
      })
  }, [])

  return (
    <div className="p-6">
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        {/* Local video */}
        <div className="relative bg-black rounded-lg overflow-hidden">
          <video
            ref={localVideoRef}
            autoPlay
            muted
            className="w-full aspect-video object-cover"
          />
          <div className="absolute bottom-2 left-2 bg-black/70 text-white px-2 py-1 rounded text-sm">
            You
          </div>
        </div>

        {/* Remote participants */}
        {participants.map((participant) => (
          <div key={participant.id} className="relative bg-black rounded-lg overflow-hidden">
            <video
              autoPlay
              className="w-full aspect-video object-cover"
              ref={(video) => {
                if (video) video.srcObject = participant.stream
              }}
            />
            <div className="absolute bottom-2 left-2 bg-black/70 text-white px-2 py-1 rounded text-sm">
              {participant.name}
            </div>
          </div>
        ))}
      </div>

      <div className="mt-6 flex justify-center gap-4">
        <button className="px-6 py-3 bg-red-600 text-white rounded-lg">
          🎤 Mute
        </button>
        <button className="px-6 py-3 bg-red-600 text-white rounded-lg">
          📹 Stop Video
        </button>
        <button className="px-6 py-3 bg-blue-600 text-white rounded-lg">
          🖥️ Share Screen
        </button>
        <button className="px-6 py-3 bg-red-600 text-white rounded-lg">
          📞 Leave Call
        </button>
      </div>
    </div>
  )
}
```

---

## When to Use Me

**Perfect for:**

- Building video call features
- Creating livestream platforms
- Implementing screen sharing
- Building webinar tools
- Creating video conferencing apps

**I'll help you:**

- Implement WebRTC
- Build broadcast features
- Add screen sharing
- Create video conferencing
- Handle real-time chat

## What I'll Create

```
🎥 Live Streaming
📹 Video Calls
🖥️ Screen Sharing
💬 Real-Time Chat
👥 Multi-Party Conferences
🔴 Broadcasting Tools
```

Let's build amazing live experiences!
