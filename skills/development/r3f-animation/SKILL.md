---
name: r3f-animation
description: React Three Fiber animation - useFrame, useAnimations, spring physics, morph targets. Use when animating objects, playing GLTF animations, or implementing physics-based movement.
---

# React Three Fiber Animation

## useFrame Animation

```tsx
import { useFrame } from '@react-three/fiber'

function AnimatedMesh() {
  const ref = useRef()

  useFrame((state, delta) => {
    ref.current.rotation.y += delta
    ref.current.position.y = Math.sin(state.clock.elapsedTime) * 2
  })

  return <mesh ref={ref}><boxGeometry /><meshStandardMaterial /></mesh>
}
```

## GLTF Animations

```tsx
import { useGLTF, useAnimations } from '@react-three/drei'

function AnimatedModel() {
  const group = useRef()
  const { scene, animations } = useGLTF('/models/character.glb')
  const { actions, names } = useAnimations(animations, group)

  useEffect(() => {
    actions[names[0]]?.play()
  }, [actions, names])

  return <primitive ref={group} object={scene} />
}
```

## Animation Crossfade

```tsx
function Character({ animation }) {
  const { actions } = useAnimations(animations, group)

  useEffect(() => {
    Object.values(actions).forEach(action => action?.fadeOut(0.5))
    actions[animation]?.reset().fadeIn(0.5).play()
  }, [animation, actions])
}
```

## Spring Animation

```tsx
import { useSpring, animated } from '@react-spring/three'

function SpringBox() {
  const [active, setActive] = useState(false)

  const { scale, color } = useSpring({
    scale: active ? 1.5 : 1,
    color: active ? '#ff6b6b' : '#4ecdc4',
    config: { mass: 1, tension: 280, friction: 60 }
  })

  return (
    <animated.mesh scale={scale} onClick={() => setActive(!active)}>
      <boxGeometry />
      <animated.meshStandardMaterial color={color} />
    </animated.mesh>
  )
}
```

## Drei Helpers

```tsx
import { Float, MeshWobbleMaterial, Trail } from '@react-three/drei'

// Floating effect
<Float speed={1} rotationIntensity={1} floatIntensity={1}>
  <mesh>...</mesh>
</Float>

// Wobbly material
<mesh>
  <torusKnotGeometry />
  <MeshWobbleMaterial factor={1} speed={2} color="hotpink" />
</mesh>

// Motion trail
<Trail width={2} length={8} color="hotpink">
  <mesh ref={movingMeshRef}>...</mesh>
</Trail>
```

## Morph Targets

```tsx
function MorphingMesh() {
  const ref = useRef()

  useFrame(({ clock }) => {
    const t = clock.elapsedTime
    const index = ref.current.morphTargetDictionary['smile']
    ref.current.morphTargetInfluences[index] = (Math.sin(t) + 1) / 2
  })

  return <primitive ref={ref} object={mesh} />
}
```

## Procedural Patterns

```tsx
// Smooth follow
function SmoothFollow({ target }) {
  const ref = useRef()
  const pos = useRef(new THREE.Vector3())

  useFrame((_, delta) => {
    pos.current.lerp(target, delta * 5)
    ref.current.position.copy(pos.current)
  })

  return <mesh ref={ref}>...</mesh>
}

// Oscillation
useFrame(({ clock }) => {
  const t = clock.elapsedTime
  ref.current.position.y = Math.sin(t * 2) * 0.5
  ref.current.position.x = Math.cos(t) * 2
  ref.current.position.z = Math.sin(t) * 2
})
```

## State Management Performance

```tsx
// Use getState() in useFrame for zero overhead
useFrame(() => {
  const { playerPosition } = useGameStore.getState()
  ref.current.position.lerp(playerPosition, 0.1)
})
```
