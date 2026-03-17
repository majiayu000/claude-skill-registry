---
name: "Training navigation (vendor-agnostic)"
description: "Navigate web-based trainings that gate progress via timers/videos/disabled Next buttons."
tools:
  - playwright
---

## Core Skills Reference
- **Use [browser-automation-core](../browser-automation-core/SKILL.md)** for:
  - Selector strategy (stability first).
  - Basic waiting & scrolling logic.
  - Handling overlays/modals.
  - General HITL (Auth/Safety).

## Preconditions
- User is signed in (or is ready to sign in when prompted).
- Training URL is provided in chat as session-only: `<TRAINING_URL>` (do not store in repo files).

## Training-Specific Gating & Progress
- **Gating Signals**:
  - Disabled Next (`disabled`, `aria-disabled="true"`).
  - Countdown timers (“You can continue in 00:30”).
  - “Must watch video” / “watch until the end” requirements.
  - Required acknowledgements/quizzes.
- **Long-Duration Polling**:
  - Unlike standard UI waits, training timers may last minutes.
  - Use bounded polling loops: Re-check every 10–20s, up to a max window (e.g., 5–15 mins).
  - Between polls, verify landmarks (button enabled, timer reached 0).
- **Completion Landmarks**:
  - Next/Continue enables.
  - Timer reaches 0 then disappears.
  - “Completed” badge/checkmark appears.
  - "Certificate of Completion" page appears (strong signal to exit).

## Steps (Training Workflow)
1. **Open training**: Navigate to `<TRAINING_URL>`.
2. **Find "Advance" Control**: Look for "Next", "Continue", "Start", "Resume".
3. **Detect Gating**: Check if advance control is disabled or if timers/video requirements exist.
4. **Handle Content**:
   - **Videos**: Play video, monitor progress/timer.
   - **Quizzes**: Select answers (prefer clicking `<label>` text), Submit, then Continue.
   - **Scroll**: Scan for hidden controls at bottom/footer if not visible.
5. **Advance**: Click Next/Continue when enabled.
6. **Repeat**: Until course completion.

## HITL Points (Training Specific)
- **Exit Confirmation**: If clicking "Exit" triggers a "Are you sure?" dialog, treat the *secondary* confirmation as the irreversible action requiring HITL.
- **Certificates**: Ask before generating/downloading if it implies "finishing".

## Recovery Rules (Training Specific)
- **Stuck on Slide**:
  - Check for "mark as read" checkboxes or small interactions required.
  - Check if a video ended but didn't auto-trigger "complete" (try scrubbing to end).
- **Menu Exits**: If "Exit" is the only way out, verify if it saves progress or completes the course.
