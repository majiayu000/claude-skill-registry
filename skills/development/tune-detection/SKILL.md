---
name: tune-detection
description: Tune exercise detection sensitivity and thresholds. Use when exercises aren't counting correctly, have false positives, or need calibration adjustments.
allowed-tools: Read, Edit, Grep
---

# Tune Detection Thresholds

## Common Issues

| Problem | Likely Cause | Fix |
|---------|--------------|-----|
| Not counting reps | Thresholds too strict | Lower `down` threshold or raise `up` threshold |
| Double counting | Thresholds too loose | Tighten thresholds, add hysteresis |
| Counts on wrong motion | Wrong landmarks | Check landmark IDs match exercise |
| Works for some people | Fixed thresholds | Use body-relative thresholds with `getBodyScale()` |

## Threshold Locations

**JSON configs** (preferred):
```
exercises/*.json → detection.thresholds
```

**Legacy functions** in `exercise_ui.html`:
- `detectLegacySquat` - DOWN_ANGLE, UP_ANGLE
- `detectLegacyPushup` - DOWN_ANGLE, UP_ANGLE
- `detectLegacyJumpingJack` - arm position relative to shoulders
- `detectLegacyCalfRaise` - legLength * 0.04 threshold
- `detectLegacySideStretch` - bodyScale * 0.4 threshold

## Detection Helpers

The codebase includes helpers for robust detection:

```javascript
// Check if landmarks are visible
isVisible(landmarks, [23, 24, 25, 26], 0.5)

// Normalize to body size
const bodyScale = getBodyScale(landmarks);
const threshold = baseThreshold * bodyScale;
```

## Testing Changes

1. Edit threshold in JSON or HTML
2. Restart tracker: `./exercise_tracker.py user_prompt_submit '{}'`
3. Watch the status text - it shows live angle/distance values
4. Adjust based on when state transitions happen

## Both-sides Averaging

For angle-based exercises, use `joint_alt` in JSON to average both sides:
```json
"landmarks": {
  "joint": [23, 25, 27],
  "joint_alt": [24, 26, 28]
}
```
