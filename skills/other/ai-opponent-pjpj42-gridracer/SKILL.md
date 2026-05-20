---
name: ai-opponent
description: Implement or tune AI opponent behavior
argument-hint: "[difficulty: easy|medium|hard]"
allowed-tools:
  - Read
  - Edit
  - Write
  - Grep
  - Glob
  - Bash
model: sonnet
---

# AI Opponent Implementation

Help implement or tune AI opponent logic per the game design.

## AI Strategy (from design doc)

```swift
func chooseAcceleration(racer: Player, track: Track, opponents: [Player]) -> GridVector {
    var bestScore = Int.min
    var bestAccel = GridVector(0, 0)

    for acceleration in allAccelerations {
        let newPos = racer.position + racer.velocity + acceleration
        let newVel = racer.velocity + acceleration

        if wouldCrash(from: racer.position, to: newPos, track: track) {
            score = -1000
        } else {
            score = progressTowardFinish(newPos, track.finishLine)
            score -= distanceToTrackCenter(newPos, track) * 0.1
            score -= speed(newVel) * 0.05  // Prefer control
        }

        if score > bestScore {
            bestScore = score
            bestAccel = acceleration
        }
    }
    return bestAccel
}
```

## Difficulty Levels

| Level | Behavior |
|-------|----------|
| Easy | Random valid moves, avoids crashes |
| Medium | Greedy progress toward finish |
| Hard | Looks 2-3 moves ahead, blocks opponents |

## Implementation Tasks

1. **Basic AI**: Avoid crashes, prefer forward progress
2. **Path scoring**: Evaluate each of 9 options
3. **Lookahead**: Simulate N turns ahead (Hard mode)
4. **Opponent awareness**: Block or avoid collisions
5. **Track awareness**: Prefer center of track

## Testing
- AI should never choose crash moves when safe options exist
- Easy AI should lose to competent player
- Hard AI should provide challenge
