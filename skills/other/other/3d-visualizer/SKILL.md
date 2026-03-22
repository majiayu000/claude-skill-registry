---
name: 3d-visualizer
description: Expert in Three.js, 3D graphics, and interactive 3D visualizations
version: 1.0.0
tags: [three-js, 3d, webgl, react-three-fiber, visualization]
---

# 3D Visualizer Skill

I help you create 3D visualizations, interactive 3D graphics, and immersive web experiences using Three.js.

## What I Do

**3D Graphics:**

- 3D models and scenes
- Materials and lighting
- Animations and interactions
- Camera controls

**3D Data Visualization:**

- 3D charts and graphs
- Network visualizations
- Geospatial data
- Scientific visualization

**Interactive 3D:**

- Product viewers (360°)
- Configurators
- Interactive demos
- 3D games

## Three.js with React Three Fiber

```bash
npm install three @react-three/fiber @react-three/drei
```

### Basic 3D Scene

```typescript
// components/Scene3D.tsx
'use client'
import { Canvas } from '@react-three/fiber'
import { OrbitControls, Box, Sphere } from '@react-three/drei'

export function Scene3D() {
  return (
    <Canvas camera={{ position: [5, 5, 5], fov: 50 }}>
      {/* Lighting */}
      <ambientLight intensity={0.5} />
      <pointLight position={[10, 10, 10]} />

      {/* 3D Objects */}
      <Box position={[-2, 0, 0]} args={[1, 1, 1]}>
        <meshStandardMaterial color="hotpink" />
      </Box>

      <Sphere position={[2, 0, 0]} args={[0.7, 32, 32]}>
        <meshStandardMaterial color="cyan" metalness={0.8} roughness={0.2} />
      </Sphere>

      {/* Camera Controls */}
      <OrbitControls />
    </Canvas>
  )
}
```

---

## 3D Model Loader

```typescript
'use client'
import { useGLTF } from '@react-three/drei'
import { Canvas } from '@react-three/fiber'

function Model() {
  const { scene } = useGLTF('/models/product.glb')
  return <primitive object={scene} />
}

export function ProductViewer() {
  return (
    <Canvas>
      <ambientLight intensity={0.5} />
      <spotLight position={[10, 10, 10]} angle={0.15} />

      <Model />

      <OrbitControls
        enableZoom={true}
        enablePan={false}
        minPolarAngle={Math.PI / 4}
        maxPolarAngle={Math.PI / 2}
      />
    </Canvas>
  )
}
```

---

## Animated 3D

```typescript
'use client'
import { useRef } from 'react'
import { useFrame } from '@react-three/fiber'
import { Mesh } from 'three'

function RotatingCube() {
  const meshRef = useRef<Mesh>(null)

  useFrame((state, delta) => {
    if (meshRef.current) {
      meshRef.current.rotation.x += delta
      meshRef.current.rotation.y += delta * 0.5
    }
  })

  return (
    <mesh ref={meshRef}>
      <boxGeometry args={[2, 2, 2]} />
      <meshStandardMaterial color="orange" />
    </mesh>
  )
}

export function AnimatedScene() {
  return (
    <Canvas>
      <ambientLight />
      <pointLight position={[10, 10, 10]} />
      <RotatingCube />
    </Canvas>
  )
}
```

---

## 3D Chart (Bar Chart)

```typescript
'use client'
import { Canvas } from '@react-three/fiber'
import { OrbitControls, Text } from '@react-three/drei'

interface DataPoint {
  label: string
  value: number
  color: string
}

function Bar3D({ position, height, color, label }: {
  position: [number, number, number]
  height: number
  color: string
  label: string
}) {
  return (
    <group position={position}>
      <mesh position={[0, height / 2, 0]}>
        <boxGeometry args={[0.8, height, 0.8]} />
        <meshStandardMaterial color={color} />
      </mesh>

      <Text
        position={[0, -0.5, 0]}
        fontSize={0.3}
        color="black"
      >
        {label}
      </Text>
    </group>
  )
}

export function BarChart3D({ data }: { data: DataPoint[] }) {
  return (
    <Canvas camera={{ position: [5, 5, 8] }}>
      <ambientLight intensity={0.5} />
      <pointLight position={[10, 10, 10]} />

      {data.map((item, i) => (
        <Bar3D
          key={i}
          position={[i * 1.5 - (data.length * 1.5) / 2, 0, 0]}
          height={item.value}
          color={item.color}
          label={item.label}
        />
      ))}

      <OrbitControls />
    </Canvas>
  )
}

// Usage
const salesData = [
  { label: 'Jan', value: 4, color: '#3b82f6' },
  { label: 'Feb', value: 3, color: '#3b82f6' },
  { label: 'Mar', value: 6, color: '#3b82f6' },
  { label: 'Apr', value: 8, color: '#3b82f6' }
]

<BarChart3D data={salesData} />
```

---

## Interactive 3D Product Configurator

```typescript
'use client'
import { useState } from 'react'
import { Canvas } from '@react-three/fiber'
import { OrbitControls } from '@react-three/drei'

const colors = {
  red: '#ef4444',
  blue: '#3b82f6',
  green: '#10b981',
  yellow: '#f59e0b'
}

function Product({ color }: { color: string }) {
  return (
    <mesh>
      <boxGeometry args={[2, 2, 2]} />
      <meshStandardMaterial color={color} metalness={0.5} roughness={0.3} />
    </mesh>
  )
}

export function ProductConfigurator() {
  const [selectedColor, setSelectedColor] = useState('blue')

  return (
    <div className="flex gap-4">
      <div className="w-2/3">
        <Canvas camera={{ position: [3, 3, 3] }}>
          <ambientLight intensity={0.5} />
          <spotLight position={[10, 10, 10]} />

          <Product color={colors[selectedColor]} />

          <OrbitControls />
        </Canvas>
      </div>

      <div className="w-1/3">
        <h3 className="font-bold mb-4">Choose Color</h3>
        <div className="grid grid-cols-2 gap-2">
          {Object.entries(colors).map(([name, hex]) => (
            <button
              key={name}
              onClick={() => setSelectedColor(name)}
              className={`p-4 rounded border-2 ${
                selectedColor === name ? 'border-black' : 'border-gray-300'
              }`}
              style={{ backgroundColor: hex }}
            >
              {name}
            </button>
          ))}
        </div>
      </div>
    </div>
  )
}
```

---

## Network Graph 3D

```typescript
'use client'
import { Canvas } from '@react-three/fiber'
import { Line } from '@react-three/drei'

interface Node {
  id: string
  position: [number, number, number]
}

interface Edge {
  from: string
  to: string
}

function NetworkGraph({ nodes, edges }: {
  nodes: Node[]
  edges: Edge[]
}) {
  const nodeMap = new Map(nodes.map(n => [n.id, n]))

  return (
    <>
      {/* Nodes */}
      {nodes.map((node) => (
        <mesh key={node.id} position={node.position}>
          <sphereGeometry args={[0.2]} />
          <meshStandardMaterial color="cyan" />
        </mesh>
      ))}

      {/* Edges */}
      {edges.map((edge, i) => {
        const from = nodeMap.get(edge.from)
        const to = nodeMap.get(edge.to)
        if (!from || !to) return null

        return (
          <Line
            key={i}
            points={[from.position, to.position]}
            color="white"
            lineWidth={1}
          />
        )
      })}
    </>
  )
}

export function Network3DVisualization() {
  const nodes = [
    { id: 'A', position: [0, 0, 0] },
    { id: 'B', position: [2, 1, 0] },
    { id: 'C', position: [-2, 1, 0] },
    { id: 'D', position: [0, 2, 1] }
  ]

  const edges = [
    { from: 'A', to: 'B' },
    { from: 'A', to: 'C' },
    { from: 'B', to: 'D' },
    { from: 'C', to: 'D' }
  ]

  return (
    <Canvas camera={{ position: [0, 0, 8] }}>
      <ambientLight />
      <pointLight position={[10, 10, 10]} />

      <NetworkGraph nodes={nodes} edges={edges} />

      <OrbitControls />
    </Canvas>
  )
}
```

---

## Performance Tips

### Instanced Mesh (Many Objects)

```typescript
'use client'
import { useRef, useMemo } from 'react'
import { useFrame } from '@react-three/fiber'
import * as THREE from 'three'

export function Particles({ count = 1000 }: { count?: number }) {
  const meshRef = useRef<THREE.InstancedMesh>(null)

  const particles = useMemo(() => {
    const temp = []
    for (let i = 0; i < count; i++) {
      const t = Math.random() * 100
      const factor = 20 + Math.random() * 100
      const speed = 0.01 + Math.random() / 200
      temp.push({ t, factor, speed, mx: 0, my: 0 })
    }
    return temp
  }, [count])

  useFrame((state) => {
    if (meshRef.current) {
      particles.forEach((particle, i) => {
        let { t, factor, speed, mx, my } = particle

        t = particle.t += speed
        const a = Math.cos(t) + Math.sin(t * 1) / 10
        const b = Math.sin(t) + Math.cos(t * 2) / 10
        const s = Math.cos(t)

        const dummy = new THREE.Object3D()
        dummy.position.set(
          (mx / 10) * a + Math.cos((t / 10) * factor) + (Math.sin(t * 1) * factor) / 10,
          (my / 10) * b + Math.sin((t / 10) * factor) + (Math.cos(t * 2) * factor) / 10,
          (my / 10) * b + Math.cos((t / 10) * factor) + (Math.sin(t * 3) * factor) / 10
        )
        dummy.scale.set(s, s, s)
        dummy.updateMatrix()
        meshRef.current!.setMatrixAt(i, dummy.matrix)
      })
      meshRef.current.instanceMatrix.needsUpdate = true
    }
  })

  return (
    <instancedMesh ref={meshRef} args={[undefined, undefined, count]}>
      <sphereGeometry args={[0.05, 16, 16]} />
      <meshPhongMaterial color="cyan" />
    </instancedMesh>
  )
}
```

---

## When to Use Me

**Perfect for:**

- Building 3D product viewers
- Creating data visualizations
- Interactive 3D experiences
- Scientific visualization
- 3D game prototypes

**I'll help you:**

- Set up Three.js projects
- Load 3D models
- Create interactive 3D
- Optimize 3D performance
- Build 3D charts

## What I'll Create

```
🎨 3D Scenes
📦 Product Viewers
📊 3D Charts
🌐 Network Graphs
🎮 Interactive 3D
⚡ Performance-Optimized 3D
```

Let's bring your data and products to life in 3D!
