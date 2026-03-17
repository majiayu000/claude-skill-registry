---
name: video-timeline
description: Generate and validate timeline.json using a builder + validator team.
disable-model-invocation: true
---

# Video Timeline Pipeline

Generate and validate timeline.json using a builder + validator team. The builder generates the timeline, the validator enforces quality gates. Max 3 validation rounds.

## Team Structure

Create an agent team called "timeline-edit" with these teammates:

### builder (general-purpose agent)
**Role:** Generate timeline.json from script + transcript + assets.
**Skills to preload:** Load the timeline-builder agent instructions.
**MCP servers needed:** giphy, pexels
**Tasks:**
1. Read the prompter/script file (or READ each slide image if no prompter exists)
2. Read the transcript (transcript-clean.json > transcript.json > SRT)
3. List available slides, GIFs, and B-roll in the video directory
4. If GIFs are missing or below density minimum, search and download via Giphy MCP
5. If B-roll is missing or below density minimum, search and download via Pexels MCP
6. Match slides to speech moments using content understanding
7. Generate creative edit decisions with ~20% distribution per layout type
8. Write timeline.json to the video directory
9. Mark task complete and notify the lead

### validator (general-purpose agent)
**Role:** Validate timeline.json against 21 quality checks.
**Skills to preload:** Load the timeline-validator agent instructions.
**Model preference:** haiku (cheap and fast - just counting and checking rules)
**Tasks (run AFTER builder completes):**
1. Read timeline.json from the video directory
2. Read transcript-clean.json (or transcript.json)
3. List files in slides/, gifs/, broll/ directories
4. Run all 21 quality checks (structural, density, speech alignment)
5. Output PASS or FAIL verdict with specific fix instructions

## Workflow

1. Create team "timeline-edit"
2. Create task "Build timeline" and assign to builder
3. Builder generates timeline.json, marks task complete
4. Create task "Validate timeline" and assign to validator
5. Validator reads timeline.json + transcript, runs 21 checks
6. **If PASS:** clean up team, report success
7. **If FAIL:** create task "Fix timeline" for builder with the validator's specific feedback
8. Builder applies targeted fixes, marks task complete
9. Create task "Re-validate timeline" for validator
10. **Max 3 rounds** (build + validate). If still failing after 3, report remaining issues to user.

## Input

Provide the video project directory:

$ARGUMENTS
