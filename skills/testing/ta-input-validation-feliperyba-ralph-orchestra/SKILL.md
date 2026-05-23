---
name: ta-input-validation
description: Player input validation testing patterns for WASD, mouse, and touch controls. Use when testing input systems, validating controls.
category: architectural
---

# Input Validation Pattern Skill

> "Test input systems early – inverted controls make games unplayable."

## When to Use This Skill

Use **whenever implementing or modifying player input systems** (WASD, mouse, touch, gamepad).

## Quick Start

```bash
# After input changes, always verify:
npm run type-check && npm run lint

# Manual testing checklist:
# 1. W = forward, S = backward, A = left, D = right
# 2. Diagonal movement (W+A, W+D, S+A, S+D)
# 3. Movement relative to camera direction
```

## The Input Validation Framework

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Implementation │───▶│  Unit Tests     │───▶│  Manual Verify  │
│  (WASD/Mouse)   │    │  (getInputDir)  │    │  (Play test)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
       │                       │                       │
       ▼                       ▼                       ▼
   Type-safe code          Prevent regression    User experience
```

## Critical Input Tests

### WASD Movement (P0 - Game Breaking)

**Test Cases:**

| Input | Expected Output | Bug Risk |
|-------|----------------|----------|
| W key | Move forward (away from camera) | HIGH |
| S key | Move backward (toward camera) | HIGH |
| A key | Move left (screen left) | HIGH |
| D key | Move right (screen right) | HIGH |
| W+A | Move forward-left (diagonal) | MEDIUM |
| W+D | Move forward-right (diagonal) | MEDIUM |
| S+A | Move backward-left (diagonal) | MEDIUM |
| S+D | Move backward-right (diagonal) | MEDIUM |

### Camera-Relative Movement

Movement MUST be relative to camera direction, not world axes:

```typescript
// ❌ WRONG: World-space movement (classic bug)
const direction = new Vector3(x, 0, z);

// ✅ CORRECT: Camera-relative movement
const forward = new Vector3();
camera.getWorldDirection(forward);
forward.y = 0;
forward.normalize();

const right = new Vector3();
right.crossVectors(forward, new Vector3(0, 1, 0));

const direction = new Vector3();
direction.addScaledVector(forward, -z);  // W/S
direction.addScaledVector(right, x);     // A/D
```

### Mouse Look Validation

| Test Case | Expected Behavior |
|-----------|-------------------|
| Mouse left | Camera rotates left |
| Mouse right | Camera rotates right |
| Mouse up | Camera looks up (clamped) |
| Mouse down | Camera looks down (clamped) |
| Sensitivity | ~180°/second rotation speed |

## Progressive Guide

### Level 1: Implementation Checklist

When implementing input systems:

```typescript
// ✅ DO: Create input helper with clear types
interface InputState {
  forward: boolean;
  backward: boolean;
  left: boolean;
  right: boolean;
  jump: boolean;
  sprint: boolean;
  crouch: boolean;
}

function getInputDirection(input: InputState, camera: Camera3D): Vector3 {
  // Implementation...
}
```

```typescript
// ❌ DON'T: Use magic numbers or implicit axes
const dir = new Vector3(
  keys['KeyD'] ? 1 : keys['KeyA'] ? -1 : 0,  // Wrong! Non-obvious
  0,
  keys['KeyS'] ? 1 : keys['KeyW'] ? -1 : 0   // Wrong! Inverted
);
```

### Level 2: Unit Testing

Create unit tests for input functions:

```typescript
// tests/unit/input.test.ts
import { describe, it, expect } from 'vitest';
import { getInputDirection } from '../PlayerController';

describe('getInputDirection', () => {
  it('returns forward vector for W key', () => {
    const input = { forward: true, backward: false, left: false, right: false };
    const result = getInputDirection(input, mockCamera);
    expect(result.z).toBeCloseTo(-1);  // Forward is negative Z
  });

  it('returns backward vector for S key', () => {
    const input = { forward: false, backward: true, left: false, right: false };
    const result = getInputDirection(input, mockCamera);
    expect(result.z).toBeCloseTo(1);  // Backward is positive Z
  });

  it('returns left vector for A key', () => {
    const input = { forward: false, backward: false, left: true, right: false };
    const result = getInputDirection(input, mockCamera);
    expect(result.x).toBeCloseTo(-1);  // Left is negative X
  });

  it('returns right vector for D key', () => {
    const input = { forward: false, backward: false, left: false, right: true };
    const result = getInputDirection(input, mockCamera);
    expect(result.x).toBeCloseTo(1);  // Right is positive X
  });

  it('handles diagonal input correctly', () => {
    const input = { forward: true, backward: false, left: true, right: false };
    const result = getInputDirection(input, mockCamera);
    expect(result.length()).toBeCloseTo(1);  // Normalized
    expect(result.x).toBeCloseTo(-0.707);    // Diagonal
    expect(result.z).toBeCloseTo(-0.707);
  });
});
```

### Level 3: Visual Debug Mode

Add debug visualization for input direction:

```typescript
// In PlayerController.tsx
const showDebug = useDebugStore(state => state.showInputDebug);

useEffect(() => {
  if (showDebug) {
    // Add arrow helper to show input direction
    const arrowHelper = new ArrowHelper(
      inputDirection.clone().normalize(),
      playerPosition,
      2,  // Length
      0x00ff00  // Green color
    );
    scene.add(arrowHelper);
    return () => scene.remove(arrowHelper);
  }
}, [inputDirection, showDebug]);
```

### Level 4: Regression Prevention

After fixing input bugs (like bugfix-002):

1. **Add unit test** covering the exact bug scenario
2. **Add E2E test** for manual verification
3. **Document** in PRD validation steps

## Common Input Bugs

| Bug | Symptom | Fix |
|-----|---------|-----|
| Inverted WASD | W moves backward | Swap vector signs |
| World-space movement | W moves north regardless of camera | Use camera direction |
| Non-normalized diagonal | Diagonal faster than cardinal | Normalize vector |
| Wrong key mapping | Keys don't match labels | Check KeyCode names |

## Anti-Patterns

❌ **DON'T:**

- Commit input changes without manual testing
- Assume keyboard layouts are consistent (use `KeyW` not `code: "KeyW"`)
- Mix up forward/backward vector signs
- Skip diagonal testing
- Use hardcoded world directions for WASD

✅ **DO:**

- Always test WASD manually before commit
- Add unit tests for getInputDirection()
- Use camera-relative movement
- Test all diagonal combinations
- Add debug visualization for development

## Checklist

Before committing input changes:

- [ ] W = forward (away from camera)
- [ ] S = backward (toward camera)
- [ ] A = left (screen left)
- [ ] D = right (screen right)
- [ ] All diagonals work (W+A, W+D, S+A, S+D)
- [ ] Movement is camera-relative
- [ ] Diagonal speed equals cardinal speed
- [ ] Unit tests added for getInputDirection()
- [ ] Debug mode shows input direction
- [ ] `npm run type-check && npm run lint` passes

## Related Skills

For camera controls: `Skill("ta-camera-tps")`
For physics input: `Skill("ta-r3f-physics")`

## External References

- [Three.js Camera Direction](https://threejs.org/docs/#api/en/core/Camera.getWorldDirection)
- [KeyboardEvent.code values](https://developer.mozilla.org/en-US/docs/Web/API/KeyboardEvent/code)
- [Vitest Testing](https://vitest.dev/)
