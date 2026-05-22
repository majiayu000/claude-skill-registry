---
name: spatial-developer
description: Expert in AR/VR, WebXR, and spatial computing for Vision Pro and web
version: 1.0.0
tags: [ar, vr, webxr, spatial-computing, visionos, three-js]
---

# Spatial Developer Skill

I help you build AR/VR experiences, spatial interfaces, and immersive 3D applications.

## What I Do

**WebXR Development:**

- AR/VR experiences in the browser
- Hand tracking and controllers
- Spatial anchors
- Immersive environments

**Vision Pro Development:**

- visionOS native apps
- Spatial UI design
- Reality Composer integration
- SharePlay experiences

**3D Web:**

- Three.js scenes
- React Three Fiber
- 3D interactions
- Spatial audio

## WebXR Basics

```bash
npm install three @react-three/fiber @react-three/drei @react-three/xr
```

### Simple VR Scene

```typescript
// components/VRScene.tsx
'use client'
import { Canvas } from '@react-three/fiber'
import { VRButton, XR, Controllers, Hands } from '@react-three/xr'
import { Box, OrbitControls } from '@react-three/drei'

export function VRScene() {
  return (
    <>
      <VRButton />
      <Canvas>
        <XR>
          <ambientLight intensity={0.5} />
          <pointLight position={[10, 10, 10]} />

          {/* 3D Content */}
          <Box position={[0, 1, -2]} args={[1, 1, 1]}>
            <meshStandardMaterial color="hotpink" />
          </Box>

          {/* VR Controllers */}
          <Controllers />

          {/* Hand Tracking */}
          <Hands />
        </XR>
      </Canvas>
    </>
  )
}
```

---

## AR on Web (WebXR)

```typescript
// components/ARScene.tsx
'use client'
import { Canvas } from '@react-three/fiber'
import { ARButton, XR } from '@react-three/xr'
import { useState } from 'react'

export function ARScene() {
  const [hitTest, setHitTest] = useState(null)

  return (
    <>
      <ARButton
        sessionInit={{
          requiredFeatures: ['hit-test'],
          optionalFeatures: ['dom-overlay']
        }}
      />

      <Canvas>
        <XR
          onHitTest={(hitMatrix, hit) => {
            setHitTest(hit)
          }}
        >
          <ambientLight />

          {hitTest && (
            <mesh position={hitTest.position}>
              <sphereGeometry args={[0.1]} />
              <meshStandardMaterial color="blue" />
            </mesh>
          )}
        </XR>
      </Canvas>
    </>
  )
}
```

---

## Vision Pro Spatial UI

```swift
// ContentView.swift
import SwiftUI
import RealityKit

struct ContentView: View {
    var body: some View {
        RealityView { content in
            // Add 3D content
            let model = ModelEntity(
                mesh: .generateSphere(radius: 0.1),
                materials: [SimpleMaterial(color: .blue, isMetallic: false)]
            )

            content.add(model)
        }
        .toolbar {
            ToolbarItem(placement: .bottomOrnament) {
                HStack {
                    Button("Reset") {
                        // Reset scene
                    }

                    Button("Share") {
                        // SharePlay
                    }
                }
            }
        }
    }
}
```

---

## 3D Interaction Patterns

### Gaze-Based Selection

```typescript
'use client'
import { useXR } from '@react-three/xr'
import { useFrame } from '@react-three/fiber'
import { useState } from 'react'

export function GazeSelect() {
  const { player } = useXR()
  const [gazing, setGazing] = useState(false)

  useFrame(() => {
    // Raycast from camera
    const direction = player.camera.getWorldDirection(new Vector3())
    // Check intersection with objects
    // If gazing for 2 seconds, select
  })

  return (
    <mesh onPointerEnter={() => setGazing(true)}>
      <boxGeometry />
      <meshStandardMaterial
        color={gazing ? 'green' : 'white'}
      />
    </mesh>
  )
}
```

### Hand Gesture Recognition

```typescript
'use client'
import { useXREvent } from '@react-three/xr'

export function GestureControl() {
  useXREvent('squeeze', (e) => {
    console.log('Pinch gesture detected')
    // Perform action
  })

  useXREvent('select', (e) => {
    console.log('Select gesture')
  })

  return (
    <mesh>
      <sphereGeometry args={[0.05]} />
      <meshStandardMaterial color="red" />
    </mesh>
  )
}
```

---

## Spatial Audio

```typescript
'use client'
import { PositionalAudio } from '@react-three/drei'
import { useRef } from 'react'

export function SpatialSound() {
  const sound = useRef()

  return (
    <mesh position={[2, 1, -3]}>
      <sphereGeometry args={[0.2]} />
      <meshStandardMaterial color="yellow" emissive="yellow" />

      <PositionalAudio
        ref={sound}
        url="/sounds/ambient.mp3"
        distance={5}
        loop
        autoplay
      />
    </mesh>
  )
}
```

---

## When to Use Me

**Perfect for:**

- Building AR/VR web experiences
- Creating Vision Pro apps
- Implementing 3D interactions
- Spatial UI design
- Immersive storytelling

**I'll help you:**

- Set up WebXR projects
- Build AR features
- Implement hand tracking
- Design spatial interfaces
- Optimize 3D performance

## What I'll Create

```
🥽 VR Experiences
📱 AR Applications
👋 Hand Tracking
🎧 Spatial Audio
🌐 WebXR Scenes
🍎 Vision Pro Apps
```

Let's build the future of spatial computing!
