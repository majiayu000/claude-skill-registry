---
name: dev-patterns-mobile-haptics
description: Haptic feedback patterns for mobile games using Vibration API. Use when adding tactile feedback.
category: patterns
---

# Mobile Haptics

> "Haptic feedback transforms flat screens into tactile experiences."

## When to Use

Use when:
- Building mobile/touch controls
- Adding game feel to actions
- Providing feedback for UI interactions
- Enhancing immersion on mobile devices

## Quick Start

```tsx
// Simple vibration feedback
function triggerHaptic(duration = 10) {
  if ('vibrate' in navigator) {
    navigator.vibrate(duration);
  }
}

// Usage
<button onClick={() => triggerHaptic(10)}>Tap</button>
```

## Browser Support

| Browser | Android | iOS | Notes |
| ------- | ------- | ----- | ----- |
| Chrome | ✅ Full | ❌ No | Full Vibration API support |
| Firefox | ✅ Full | ❌ No | Full Vibration API support |
| Safari | ✅ Full | ❌ No | Desktop only |
| Edge | ✅ Full | ❌ No | Chromium-based |

**iOS Note**: iOS does NOT support the Vibration API. Use Taptic Engine feedback via native wrappers (Capacitor, React Native) for iOS.

## Tap Feedback (UI Interactions)

```tsx
// Light tap for button presses
function tapFeedback() {
  navigator.vibrate(10); // 10ms - very subtle
}

// Medium tap for toggle switches
function toggleFeedback() {
  navigator.vibrate(25); // 25ms - noticeable
}

// Heavy tap for confirm actions
function confirmFeedback() {
  navigator.vibrate(50); // 50ms - strong
}
```

## Impact Patterns (Game Actions)

```tsx
// Light impact - shooting, collecting items
function lightImpact() {
  navigator.vibrate(15);
}

// Medium impact - jumping, landing
function mediumImpact() {
  navigator.vibrate(30);
}

// Heavy impact - explosions, damage
function heavyImpact() {
  navigator.vibrate([50, 30, 50]); // Pattern: hit, pause, hit
}
```

## Success Pattern

```tsx
// Success - triple tap pattern
function successHaptic() {
  navigator.vibrate([10, 50, 10, 50, 10]);
}

// Level complete - ascending pattern
function levelCompleteHaptic() {
  navigator.vibrate([10, 50, 20, 50, 30]);
}
```

## Error Pattern

```tsx
// Error - double tap
function errorHaptic() {
  navigator.vibrate([50, 100, 50]);
}

// Deny - single long pulse
function denyHaptic() {
  navigator.vibrate(100);
}
```

## Game-Specific Patterns

```tsx
// Shooting feedback
function shootFeedback() {
  navigator.vibrate(15);
}

// Empty ammo click
function emptyClickFeedback() {
  navigator.vibrate([10, 30, 10]);
}

// Light damage
function lightDamageFeedback() {
  navigator.vibrate(25);
}

// Heavy damage
function heavyDamageFeedback() {
  navigator.vibrate([80, 20, 80]);
}

// Death/respawn
function deathFeedback() {
  navigator.vibrate([100, 50, 100, 50, 200]);
}
```

## Movement Feedback

```tsx
// Footsteps - subtle, rhythmic
let stepCount = 0;
function stepFeedback() {
  // Only vibrate every 3rd step
  if (stepCount % 3 === 0) {
    navigator.vibrate(5);
  }
  stepCount++;
}

// Jump
function jumpFeedback() {
  navigator.vibrate([10, 20, 30]); // Ascending pattern
}

// Landing
function landFeedback() {
  const intensity = Math.min(fallDistance / 10, 1);
  navigator.vibrate(20 + intensity * 40);
}
```

## Best Practices

1. **Don't overuse** - Too much vibration desensitizes users
2. **Match action intensity** - Heavy actions = stronger haptics
3. **Consider battery** - Haptics consume battery
4. **Provide settings** - Allow users to disable or adjust intensity
5. **Test on devices** - Emulators don't show haptics

## Reference

- **[dev-patterns-ui-animations](../dev-patterns-ui-animations/SKILL.md)** — UI animation patterns
