---
name: add-exercise
description: Add a new exercise to vibereps. Use when the user wants to create a new exercise type with pose detection. Handles creating the JSON config file and detection logic.
allowed-tools: Read, Write, Glob, Grep
---

# Add New Exercise

## Instructions

When adding a new exercise to vibereps:

1. **Read the template** at `exercises/_template.json` for the JSON structure
2. **Choose a detection type** based on the exercise motion:
   - `angle` - Joint angle changes (squats, pushups)
   - `height_baseline` - Vertical movement from baseline (calf raises)
   - `height_relative` - Position relative to reference point (jumping jacks)
   - `tilt` - Torso lean (side stretches)
   - `distance` - Body parts approaching each other (standing crunches)
   - `width_ratio` - Shoulder/hip width ratio (torso twists)
   - `quadrant_tracking` - Circular arm motion (arm circles)

3. **Create the JSON config** in `exercises/{exercise_name}.json`

4. **Test detection** by running the tracker

## MediaPipe Landmark IDs

Key landmarks for detection:
- Shoulders: 11 (left), 12 (right)
- Elbows: 13 (left), 14 (right)
- Wrists: 15 (left), 16 (right)
- Hips: 23 (left), 24 (right)
- Knees: 25 (left), 26 (right)
- Ankles: 27 (left), 28 (right)

## Example: Angle-based exercise

```json
{
  "id": "squats",
  "name": "Squats",
  "description": "Strengthens legs",
  "category": "strength",
  "reps": { "normal": 10, "quick": 5 },
  "detection": {
    "type": "angle",
    "landmarks": {
      "joint": [23, 25, 27],
      "joint_alt": [24, 26, 28]
    },
    "thresholds": { "down": 120, "up": 150 }
  },
  "instructions": {
    "ready": "Squat down below {down}°",
    "down": "Good! Now stand up"
  }
}
```

## Testing

Run the tracker to test:
```bash
./exercise_tracker.py user_prompt_submit '{}'
```
