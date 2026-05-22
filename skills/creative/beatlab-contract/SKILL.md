---
name: beatlab-contract
description: BeatLab JSON contract for 16-step (0-15) pianoSequence & drumSequence. Use when generating or editing beats.
user-invocable: false
---

# BeatLab Contract (v1)

You must follow this exact contract (Mastra AI Beats Lab compatible):
- Steps: 16 (0-15)
- Output JSON must include:
  - "pianoSequence": object mapping each allowed note -> array of step numbers (0-15)
  - "drumSequence": object mapping each allowed drum sound -> array of step numbers (0-15)

Allowed piano notes (fixed):
C5, B4, A4, G4, F4, E4, D4, C4, B3, A3, G3

Allowed drum sounds (fixed):
Kick, Snare, HiHat, Clap, OpenHat, Tom, Crash, Ride, Shaker, Cowbell

Musical defaults (helpful heuristics):
- Kick often on 0 and/or 8
- Snare often on 4 and/or 12
- HiHat can be steady (e.g., every 2 steps) but avoid over-density
- Keep melody minimal (few notes, repeating motif)

Output should be ONLY JSON when asked for Beat JSON.
