---
name: ta-camera-tps
description: Third-person shooter camera implementation with proper player-relative controls. Use when implementing TPS cameras, orbit controls, camera follow.
category: camera
---
# TPS Camera Skill

> "In TPS, the camera orbits the player - the player doesn't rotate to face the camera."

## When to Use This Skill

Use when:

- Implementing third-person camera controls
- Creating character controller with camera-relative movement
- Setting up Arc Raiders-style TPS gameplay

## The Critical Distinction

### WRONG: Player Rotates to Camera

```tsx
// ❌ WRONG - Player rotates toward camera direction
function PlayerController() {
  const { camera } = useThree();

  useFrame(() => {
    // Player model rotates to face where camera is looking
    player.rotation.y = camera.rotation.y;
    // This makes character spin wildly as camera orbits
  });

  return <mesh ref={playerRef}>...</mesh>;
}
```

### CORRECT: Camera Follows Player

```tsx
// ✅ CORRECT - Camera orbits behind player, player moves relative to camera
function TPSCameraController() {
  const cameraRef = useRef<THREE.PerspectiveCamera>(null);
  const playerRef = useRef<THREE.Group>(null);
  const cameraDistance = 8;
  const cameraHeight = 4;

  useFrame(({ clock }) => {
    if (!playerRef.current || !cameraRef.current) return;

    const playerPos = playerRef.current.position;
    const time = clock.getElapsedTime();

    // Camera orbits BEHIND the player (player doesn't rotate)
    const orbitAngle = Math.sin(time * 0.1) * 0.5; // Gentle orbit

    cameraRef.current.position.x = playerPos.x + Math.sin(orbitAngle) * cameraDistance;
    cameraRef.current.position.z = playerPos.z + Math.cos(orbitAngle) * cameraDistance;
    cameraRef.current.position.y = playerPos.y + cameraHeight;

    // Camera LOOKS AT player (player doesn't rotate to camera)
    cameraRef.current.lookAt(playerPos);
  });

  return (
    <>
      <perspectiveCamera ref={cameraRef} fov={60} />
      <group ref={playerRef}>
        {/* Player maintains their own rotation independent of camera */}
        <PlayerCharacter />
      </group>
    </>
  );
}
```

## Camera-Relative Movement Input

```tsx
function usePlayerMovement() {
  const { camera } = useThree();
  const keys = useRef({ w: false, a: false, s: false, d: false });

  useEffect(() => {
    const handleKey = (e: KeyboardEvent, pressed: boolean) => {
      switch (e.key.toLowerCase()) {
        case 'w': keys.current.w = pressed; break;
        case 'a': keys.current.a = pressed; break;
        case 's': keys.current.s = pressed; break;
        case 'd': keys.current.d = pressed; break;
      }
    };

    window.addEventListener('keydown', (e) => handleKey(e, true));
    window.addEventListener('keyup', (e) => handleKey(e, false));
    return () => {
      window.removeEventListener('keydown', (e) => handleKey(e, true));
      window.removeEventListener('keyup', (e) => handleKey(e, false));
    };
  }, []);

  const getMoveDirection = useCallback(() => {
    // Get camera's forward direction (flat on XZ plane)
    const forward = new THREE.Vector3();
    camera.getWorldDirection(forward);
    forward.y = 0;
    forward.normalize();

    // Get camera's right direction
    const right = new THREE.Vector3();
    right.crossVectors(forward, new THREE.Vector3(0, 1, 0));

    // Calculate movement direction relative to camera
    const moveDir = new THREE.Vector3();
    if (keys.current.w) moveDir.add(forward);
    if (keys.current.s) moveDir.sub(forward);
    if (keys.current.d) moveDir.add(right);
    if (keys.current.a) moveDir.sub(right);

    return moveDir.normalize();
  }, [camera]);

  return { getMoveDirection, keys };
}
```

## Smooth Camera Following

```tsx
function SmoothTPSCamera({ target }: { target: THREE.Object3D }) {
  const cameraRef = useRef<THREE.PerspectiveCamera>(null);
  const offset = useRef(new THREE.Vector3(0, 4, 8));
  const currentPos = useRef(new THREE.Vector3());

  useFrame((state, delta) => {
    if (!cameraRef.current || !target) return;

    // Target position with offset
    const targetPos = target.position.clone().add(offset.current);

    // Smoothly interpolate camera position (damping)
    currentPos.current.lerp(targetPos, delta * 5);

    cameraRef.current.position.copy(currentPos.current);
    cameraRef.current.lookAt(target.position);
  });

  return <perspectiveCamera ref={cameraRef} fov={60} />;
}
```

## Mouse Look (Camera Rotation)

```tsx
function MouseLookCamera() {
  const cameraRef = useRef<THREE.PerspectiveCamera>(null);
  const playerRef = useRef<THREE.Group>(null);
  const yaw = useRef(0);
  const pitch = useRef(0);
  const distance = 8;

  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      // Update yaw based on mouse X
      yaw.current -= e.movementX * 0.002;
      // Clamp pitch to prevent camera flipping
      pitch.current = Math.max(-0.5, Math.min(0.8, pitch.current - e.movementY * 0.002));
    };

    window.addEventListener('mousemove', handleMouseMove);
    return () => window.removeEventListener('mousemove', handleMouseMove);
  }, []);

  useFrame(() => {
    if (!cameraRef.current || !playerRef.current) return;

    const playerPos = playerRef.current.position;

    // Calculate camera position based on yaw and pitch
    const x = playerPos.x + Math.sin(yaw.current) * Math.cos(pitch.current) * distance;
    const y = playerPos.y + Math.sin(pitch.current) * distance + 2;
    const z = playerPos.z + Math.cos(yaw.current) * Math.cos(pitch.current) * distance;

    cameraRef.current.position.set(x, y, z);
    cameraRef.current.lookAt(playerPos);
  });

  return (
    <>
      <perspectiveCamera ref={cameraRef} fov={60} />
      <group ref={playerRef}>
        {/* Player stays stationary rotation-wise, camera orbits */}
        <PlayerCharacter />
      </group>
    </>
  );
}
```

## Comparison: Arc Raiders Style

| Feature | Wrong Approach | Correct Approach |
| ------- | -------------- | ---------------- |
| Camera movement | Fixed, player rotates to it | Orbits around player |
| Player rotation | Matches camera yaw | Independent, controlled by input |
| Input mapping | World-space directions | Camera-relative directions |
| Visual result | Character spins | Camera orbits, character faces movement direction |

## Pointer Lock API for Smooth Mouse Control

The browser Pointer Lock API is essential for FPS/TPS mouse look. It provides:

1. **Hidden cursor** - Mouse pointer disappears during gameplay
2. **Unlimited movement** - `movementX/Y` not bound by screen edges
3. **Lock state tracking** - Know when pointer is locked/unlocked
4. **ESC handling** - Native unlock on ESC press

### Basic Pointer Lock Implementation

```tsx
function TPSCameraWithPointerLock() {
  const cameraRef = useRef<THREE.PerspectiveCamera>(null);
  const isLocked = useRef(false);
  const lockedRef = useRef(false);

  // Request pointer lock on mount
  useEffect(() => {
    const requestLock = () => {
      document.body.requestPointerLock();
    };

    // Auto-request lock after short delay (allows user interaction first)
    const timeoutId = setTimeout(requestLock, 100);

    // Also request on click (fallback if auto-lock fails)
    document.addEventListener('click', requestLock);

    return () => {
      clearTimeout(timeoutId);
      document.removeEventListener('click', requestLock);
    };
  }, []);

  // Track pointer lock state changes
  useEffect(() => {
    const handlePointerLockChange = () => {
      const hasLock = document.pointerLockElement === document.body;
      lockedRef.current = hasLock;
      isLocked.current = hasLock;
    };

    document.addEventListener('pointerlockchange', handlePointerLockChange);

    return () => {
      document.removeEventListener('pointerlockchange', handlePointerLockChange);
    };
  }, []);

  // Mouse movement handler (only processes when locked)
  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      if (!lockedRef.current) return; // Only process when locked

      // Process mouse movement for camera rotation
      // Use e.movementX and e.movementY for delta
    };

    // Register on window to prevent cursor edge issues
    window.addEventListener('mousemove', handleMouseMove);

    return () => {
      window.removeEventListener('mousemove', handleMouseMove);
    };
  }, []);

  return <perspectiveCamera ref={cameraRef} fov={60} />;
}
```

### Pointer Lock with PAUSED Overlay

```tsx
function TPSCameraWithPausedOverlay() {
  const [isPaused, setIsPaused] = useState(false);
  const isLocked = useRef(false);
  const yaw = useRef(0);
  const pitch = useRef(0);

  const handlePointerLockChange = useCallback(() => {
    const wasLocked = isLocked.current;
    isLocked.current = document.pointerLockElement === document.body;

    // Show PAUSED when unlocked (ESC pressed)
    if (wasLocked && !isLocked.current) {
      setIsPaused(true);
    }
  }, []);

  const requestPointerLock = useCallback(() => {
    document.body.requestPointerLock();
  }, []);

  const handleMouseMove = useCallback((e: MouseEvent) => {
    if (!isLocked.current) return;

    // Update camera rotation
    yaw.current -= e.movementX * SENSITIVITY;
    pitch.current -= e.movementY * SENSITIVITY;
    pitch.current = clamp(pitch.current, MIN_PITCH, MAX_PITCH);
  }, []);

  useEffect(() => {
    // Auto-request lock on mount
    const timeoutId = setTimeout(requestPointerLock, 100);
    document.addEventListener('click', requestPointerLock);
    document.addEventListener('pointerlockchange', handlePointerLockChange);
    window.addEventListener('mousemove', handleMouseMove);

    return () => {
      clearTimeout(timeoutId);
      document.removeEventListener('click', requestPointerLock);
      document.removeEventListener('pointerlockchange', handlePointerLockChange);
      window.removeEventListener('mousemove', handleMouseMove);
    };
  }, [handlePointerLockChange, handleMouseMove, requestPointerLock]);

  return (
    <>
      <perspectiveCamera ref={cameraRef} fov={60} />
      {isPaused && (
        <div
          onClick={requestPointerLock}
          style={{
            position: 'fixed',
            inset: 0,
            background: 'rgba(0, 0, 0, 0.7)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            zIndex: 1000,
            cursor: 'pointer',
          }}
        >
          <h1 style={{ color: '#ff6464', textShadow: '0 0 20px rgba(255, 100, 100, 0.8)' }}>
            PAUSED
          </h1>
          <p style={{ color: 'white', marginTop: '20px' }}>
            Click to Resume
          </p>
        </div>
      )}
    </>
  );
}
```

### Different Sensitivity for Hipfire vs Aim

```tsx
const SENSITIVITY_HIPFIRE = 0.002;
const SENSITIVITY_AIM = 0.001; // Slower when aiming

function useMouseLook(isAiming: boolean) {
  const yaw = useRef(0);
  const pitch = useRef(0);

  const handleMouseMove = useCallback((e: MouseEvent) => {
    const sensitivity = isAiming ? SENSITIVITY_AIM : SENSITIVITY_HIPFIRE;
    yaw.current -= e.movementX * sensitivity;
    pitch.current -= e.movementY * sensitivity;
    pitch.current = clamp(pitch.current, MIN_PITCH, MAX_PITCH);
  }, [isAiming]);

  return { yaw, pitch, handleMouseMove };
}
```

### Key Pointer Lock Patterns

| Pattern | Purpose |
|---------|---------|
| `requestPointerLock()` | Start pointer lock (user gesture required) |
| `document.pointerLockElement` | Check if locked (equals element or null) |
| `pointerlockchange` event | Detect lock state changes (ESC pressed) |
| `e.movementX/Y` | Mouse delta since last event (unbounded) |
| Register on `window` | Prevent edge-of-screen issues with mousemove |

## Checklist

Before marking TPS camera complete:

- [ ] Camera orbits BEHIND player (player doesn't rotate to camera)
- [ ] Camera follows player position smoothly
- [ ] Movement input is camera-relative (WASD relative to camera direction)
- [ ] Player character model faces movement direction, not camera
- [ ] Mouse input rotates camera around player
- [ ] Camera pitch is clamped to prevent flipping
- [ ] Smooth damping on camera movement
- [ ] **Pointer Lock API active for mouse control**
- [ ] **Pointer hidden during gameplay**
- [ ] **ESC key shows PAUSED overlay**
- [ ] **Click-to-resume functionality**
- [ ] **Auto-lock on mount with click fallback**

## Related Skills

For R3F fundamentals: `Skill("ta-r3f-fundamentals")`

## Retrospective Learnings

**bugfix-003 (2026-01-22):**
Pointer Lock API integration for smooth FPS/TPS mouse control. Auto-lock on mount, ESC unlock handling with PAUSED overlay, click-to-resume, and proper state tracking with `pointerlockchange` event.

**bugfix-004 (2026-01-22):**
TPS camera must orbit behind player - player moves relative to camera direction. The player character should NOT rotate toward the camera. Camera orbits, player stays oriented to movement direction.
