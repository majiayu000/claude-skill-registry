---
name: verify
description: Verify game mechanics match the design document
argument-hint: "[mechanic: movement|collision|laps|all]"
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - mcp__automation__screenshot
  - mcp__automation__mouseClick
model: sonnet
---

# Verify Game Mechanics

Compare implementation against design document specifications.

## Arguments
`$ARGUMENTS` - Which mechanic to verify (movement, collision, laps, or all)

## Verification Checklist

### Movement Mechanics
From design doc:
```
NewPosition = CurrentPosition + CurrentVelocity + Acceleration
NewVelocity = CurrentVelocity + Acceleration
```

Verify:
1. Read movement code in Swift
2. Confirm formula matches
3. Play-test: Start at (5,5) with vel (0,0), accel (1,1) → should be at (6,6) with vel (1,1)

### Collision Detection
From design doc:
- Use Bresenham's line algorithm
- Check ALL cells along path
- Any wall cell = crash

Verify:
1. Find collision code
2. Confirm Bresenham implementation
3. Play-test: Move toward wall, verify crash occurs

### Crash Handling
From design doc:
- Lose 1 life
- Velocity resets to (0, 0)
- Respawn at nearest valid cell

Verify:
1. Find crash handling code
2. Confirm all three effects
3. Play-test: Crash, verify life decremented

### Lap Counting
From design doc:
- Cross finish line in correct direction
- Use line segment intersection

Verify:
1. Find lap counting code
2. Confirm direction check
3. Play-test: Complete lap, verify counter

## Report Format

```
Mechanic Verification: [name]
===========================
Design Spec: [quote from doc]
Implementation: [file:line]
Match: YES / NO / PARTIAL
Issues: [any discrepancies]
```
