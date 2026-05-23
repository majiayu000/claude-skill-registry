---
name: ta-networking-visual-feedback
description: Visual feedback patterns for server-authoritative multiplayer with client-side prediction. Use when implementing multiplayer visual feedback.
category: networking
---

# Networked Visual Feedback Skill

> "Show the player immediate feedback, but validate server-side for correctness."

## When to Use This Skill

Use for **EVERY gameplay feature** in multiplayer. Players need responsive feedback even when waiting for server validation.

## Critical Architecture Principle

```
┌─────────────────────────────────────────────────────────────────┐
│                    CLIENT PREDICTION + SERVER ROLLBACK          │
│                                                                  │
│  Player Action                                                   │
│       │                                                          │
│       ▼                                                          │
│  ┌─────────────────┐                                            │
│  │ IMMEDIATE FEEDBACK│  ← Show instantly for responsiveness     │
│  │ (Optimistic)     │                                            │
│  └────────┬─────────┘                                            │
│           │                                                        │
│           ▼                                                        │
│  ┌─────────────────┐                                            │
│  │ SEND TO SERVER  │  ← Request validation                      │
│  └─────────────────┘                                            │
│           │                                                        │
│           ▼ (100-300ms latency)                                   │
│  ┌─────────────────┐                                            │
│  │ SERVER RESPONSE │  ← Accept or reject                        │
│  └────────┬─────────┘                                            │
│           │                                                        │
│      ┌────┴────┐                                                  │
│      ▼         ▼                                                  │
│  [ACCEPT]  [REJECT]                                               │
│      │         │                                                  │
│      ▼         ▼                                                  │
│  Keep     Rollback visual                                        │
│  visual   + show rejection cue                                   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Quick Start: Optimistic Paint Shooting

```tsx
// src/components/game/weapons/PaintGun.tsx
function PaintGun() {
  const [pendingShots, setPendingShots] = useState<Map<number, DecalData>>(new Map());
  const shotSequence = useRef(0);

  const shoot = (aimDirection: Vector3) => {
    const sequence = ++shotSequence.current;

    // 1. IMMEDIATE: Show decal optimistically
    const optimisticDecal = createDecal(aimDirection);
    setPendingShots(prev => new Map(prev).set(sequence, optimisticDecal));

    // 2. SEND: Request server validation
    networkManager.send({
      type: 'paint_fire',
      aim: aimDirection,
      sequence,
    });
  };

  // 3. RECEIVE: Server confirmation or rejection
  useEffect(() => {
    const handlePaintResult = (result: PaintResult) => {
      const { sequence, accepted, position } = result;

      if (accepted) {
        // Keep optimistic decal, mark as confirmed
        setPendingShots(prev => {
          const updated = new Map(prev);
          const decal = updated.get(sequence);
          if (decal) {
            decal.confirmed = true;
            decal.serverPosition = position;
          }
          return updated;
        });
      } else {
        // REJECTED: Remove optimistic decal + show rejection
        setPendingShots(prev => {
          const updated = new Map(prev);
          updated.delete(sequence);
          return updated;
        });

        // Show rejection feedback
        showRejectionIndicator(aimDirection);
      }
    };

    networkManager.on('paint_result', handlePaintResult);
    return () => networkManager.off('paint_result', handlePaintResult);
  }, []);

  return (
    <group>
      {/* Render all decals - confirmed and pending */}
      {Array.from(pendingShots.values()).map(decal => (
        <PaintDecal
          key={decal.sequence}
          {...decal}
          opacity={decal.confirmed ? 1 : 0.5}  // Pending decals are semi-transparent
          showConfirming={decal.confirmed && !decal.confirmedShown}
        />
      ))}
    </group>
  );
}
```

## Visual States for Networked Actions

| State | Visual Indication | Purpose |
|-------|------------------|---------|
| **Pending** | 50% opacity, subtle outline | Shows action happened, awaiting confirmation |
| **Confirmed** | Full opacity, brief glow flash | Server validated - action is real |
| **Rejected** | Fade out + red tint | Server rejected - action didn't count |
| **Reconciling** | Smooth interpolation to server position | Correcting prediction drift |

## Prediction Confidence Indicators

### Paint Decal States

```tsx
// src/components/game/effects/PaintDecal.tsx
interface PaintDecalProps {
  position: Vector3;
  team: 'orange' | 'blue';
  confirmed: boolean;
  serverPosition?: Vector3;
}

function PaintDecal({ position, team, confirmed, serverPosition }: PaintDecalProps) {
  const meshRef = useRef<THREE.Mesh>(null);

  // Interpolate to server position if different
  const displayPosition = useMemo(() => {
    if (!serverPosition) return position;
    // Smooth lerp to server position
    return new Vector3().lerpVectors(position, serverPosition, 0.3);
  }, [position, serverPosition]);

  // Visual based on confirmation state
  const opacity = confirmed ? 1.0 : 0.6;
  const emissive = confirmed ? teamColor : new THREE.Color(0x000000);

  return (
    <mesh ref={meshRef} position={displayPosition}>
      <circleGeometry args={[0.5, 32]} />
      <meshStandardMaterial
        color={teamColor}
        opacity={opacity}
        transparent={!confirmed}
        emissive={emissive}
        emissiveIntensity={confirmed ? 0.5 : 0}
      />
    </mesh>
  );
}
```

### Movement Prediction Feedback

```tsx
// src/components/game/player/PlayerController.tsx
function PlayerController() {
  const [predictionHealth, setPredictionHealth] = useState(100);

  const reconcile = (serverState: PlayerState) => {
    const localState = getLocalPrediction();

    // Calculate prediction error
    const positionError = localState.position.distanceTo(serverState.position);

    if (positionError > 1.0) {
      // Large error - show correction happening
      setPredictionHealth(50);
    } else if (positionError > 0.1) {
      // Small drift - reduce confidence slightly
      setPredictionHealth(80);
    } else {
      // Good prediction
      setPredictionHealth(100);
    }

    // Smooth correction
    smoothReconcile(serverState);
  };

  return (
    <>
      {/* Optional: Debug visualization of prediction health */}
      {predictionHealth < 100 && (
        <Html position={[0, 2, 0]}>
          <div className={`prediction-indicator health-${predictionHealth}`}>
            {predictionHealth < 50 ? 'Syncing...' : ''}
          </div>
        </Html>
      )}
    </>
  );
}
```

## Server State Visualization

### Connection Quality Indicator

```tsx
// src/components/ui/HUD.tsx
function NetworkStatus() {
  const [ping, setPing] = useState(0);
  const [quality, setQuality] = useState<'good' | 'ok' | 'poor'>('good');

  useEffect(() => {
    networkManager.on('latency', (ms: number) => {
      setPing(ms);

      if (ms < 100) setQuality('good');
      else if (ms < 200) setQuality('ok');
      else setQuality('poor');
    });
  }, []);

  return (
    <div className={`network-status ${quality}`}>
      <div className="ping-indicator">
        <span className="ping-bars">
          {/* Animated bars based on quality */}
          {[1, 2, 3].map(i => (
            <div
              key={i}
              className={`bar ${i <= (quality === 'good' ? 3 : quality === 'ok' ? 2 : 1) ? 'active' : ''}`}
            />
          ))}
        </span>
        <span className="ping-value">{ping}ms</span>
      </div>
    </div>
  );
}
```

### Validation Feedback (Shots Rejected)

```tsx
// src/components/game/weapons/ValidationFeedback.tsx
function ValidationFeedback() {
  const [rejectedShots, setRejectedShots] = useState<RejectedShot[]>([]);

  useEffect(() => {
    networkManager.on('shot_rejected', (reason: string) => {
      // Show rejection at screen center or aim position
      setRejectedShots(prev => [
        ...prev,
        { reason, timestamp: Date.now(), position: getAimPosition() }
      ]);

      // Remove after animation
      setTimeout(() => {
        setRejectedShots(prev => prev.slice(1));
      }, 1000);
    });
  }, []);

  return (
    <>
      {rejectedShots.map(shot => (
        <Html key={shot.timestamp} position={shot.position}>
          <div className="shot-rejected">
            <div className="rejected-icon">✕</div>
            <div className="rejected-text">{shot.reason}</div>
          </div>
        </Html>
      ))}
    </>
  );
}
```

## Spawn Protection Visualization

```tsx
// Server tracks spawn protection, client visualizes
function SpawnProtection({ player, hasProtection }: Props) {
  return (
    <>
      {hasProtection && (
        <group position={player.position}>
          {/* Invulnerability shield effect */}
          <mesh>
            <sphereGeometry args={[1, 16, 16]} />
            <meshBasicMaterial
              color={player.team === 'orange' ? 0xff6b00 : 0x0088ff}
              transparent
              opacity={0.3}
              wireframe
            />
          </mesh>
          {/* Rotating ring */}
          <mesh rotation={[Math.PI / 2, 0, 0]}>
            <ringGeometry args={[1.2, 1.3, 32]} />
            <meshBasicMaterial
              color={player.team === 'orange' ? 0xff6b00 : 0x0088ff}
              transparent
              opacity={0.5}
            />
          </mesh>
        </group>
      )}
    </>
  );
}
```

## HUD Integration for Network State

### Paint Coverage Confirmation

```tsx
// When paint is confirmed by server, highlight minimap
function Minimap({ paintCoverage }: Props) {
  const [confirmedPaint, setConfirmedPaint] = useState<PaintEvent[]>([]);

  useEffect(() => {
    networkManager.on('paint_confirmed', (paint: PaintEvent) => {
      setConfirmedPaint(prev => [...prev, paint]);

      // Brief highlight effect
      setTimeout(() => {
        setConfirmedPaint(prev => prev.slice(1));
      }, 500);
    });
  }, []);

  return (
    <canvas ref={canvasRef}>
      {/* Render paint coverage */}
      {paintCoverage.map(paint => (
        <circle
          key={paint.id}
          cx={paint.x}
          cy={paint.y}
          r={paint.radius}
          fill={paint.team === 'orange' ? '#ff6b00' : '#0088ff'}
          opacity={confirmedPaint.includes(paint) ? 1 : 0.7}
        />
      ))}
    </canvas>
  );
}
```

### Team Lead Indicator

```tsx
// Emphasize which team is winning
function ScoreDisplay({ orangeScore, blueScore }: Props) {
  const lead = orangeScore > blueScore ? 'orange' : blueScore > orangeScore ? 'blue' : 'tie';

  return (
    <div className="score-container">
      <div className={`team-score orange ${lead === 'orange' ? 'leading' : ''}`}>
        {orangeScore}%
      </div>
      <div className="vs">VS</div>
      <div className={`team-score blue ${lead === 'blue' ? 'leading' : ''}`}>
        {blueScore}%
      </div>

      {lead !== 'tie' && (
        <div className={`lead-indicator ${lead}`}>
          {lead === 'orange' ? '🟠 LEADING' : '🔵 LEADING'}
        </div>
      )}
    </div>
  );
}
```

## Animation Timing for Network Feedback

| Feedback Type | Timing | Animation |
|---------------|--------|-----------|
| **Pending → Confirmed** | 100-200ms | Opacity 0.5 → 1.0 |
| **Rejected** | 300-500ms | Scale up + fade + red tint |
| **Reconciliation** | 200-300ms | Lerp to server position |
| **Spawn protection** | 3s | Pulse animation |
| **Shot confirmed** | 150ms | Brief emissive flash |

## CSS Animations for UI Feedback

```css
/* src/styles/network-feedback.css */

/* Pending state pulse */
@keyframes pending-pulse {
  0%, 100% { opacity: 0.6; transform: scale(1); }
  50% { opacity: 0.8; transform: scale(1.05); }
}

.paint-decal.pending {
  animation: pending-pulse 1s infinite;
}

/* Confirmed flash */
@keyframes confirmed-flash {
  0% { filter: brightness(1); }
  50% { filter: brightness(1.5); }
  100% { filter: brightness(1); }
}

.paint-decal.confirmed {
  animation: confirmed-flash 150ms ease-out;
}

/* Rejected feedback */
@keyframes rejected-feedback {
  0% { opacity: 1; transform: scale(1); }
  100% { opacity: 0; transform: scale(1.5); }
}

.shot-rejected {
  animation: rejected-feedback 500ms ease-out forwards;
}

/* Network status indicator */
@keyframes ping-pulse {
  0%, 100% { transform: scaleY(0.3); }
  50% { transform: scaleY(1); }
}

.ping-bar.active {
  animation: ping-pulse 500ms infinite;
}
```

## Common Mistakes

| ❌ Wrong | ✅ Right |
|----------|----------|
| No feedback until server responds | Immediate optimistic feedback |
| Can't tell if action was valid | Clear confirmed/rejected visuals |
| No indication of network issues | Ping/quality indicator |
| Rubber-banding with no explanation | "Syncing..." message during correction |
| Spawn protection invisible | Visible shield effect |

## Anti-Patterns

❌ **DON'T:**

- Wait for server before showing any feedback
- Hide network issues from player
- Skip rejection cues
- No visual distinction between pending and confirmed
- Silent server corrections

✅ **DO:**

- Show immediate optimistic feedback
- Indicate pending state (semi-transparent)
- Flash confirmed actions briefly
- Show rejection clearly (fade + red tint)
- Display network quality
- Visualize spawn protection

## Checklist

For each networked feature:

- [ ] Immediate optimistic feedback shown
- [ ] Pending state visually indicated
- [ ] Confirmed state has flash/glow
- [ ] Rejected state has clear feedback
- [ ] Network quality indicator exists
- [ ] Server corrections are smooth (not jarring)
- [ ] Spawn states are visible
- [ ] Team advantage is clearly shown
- [ ] No confusion about what's real vs predicted

## Related Skills

For visual polish patterns: `Skill("ta-ui-polish")`

## External References

- [Gaffer On Games - Networked Physics](https://gafferongames.com/post/networked_physics/) — Prediction fundamentals
