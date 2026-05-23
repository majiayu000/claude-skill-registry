---
name: create-storyboard
description: >
  Transform screenplay output from /create-story into animatics with camera
  framing, visual panels, and timing. Highly collaborative - the skill acts
  as a creative cinematographer, making suggestions and asking questions
  throughout the process. Integrates with /memory for learned techniques.
triggers:
  - create storyboard
  - storyboard this screenplay
  - make an animatic
  - plan the shots
  - camera plan
  - shot breakdown
  - visualize the script
metadata:
  short-description: Collaborative screenplay-to-animatic with AI cinematographer
---

# create-storyboard

Transform screenplays into animatics through a **collaborative creative dialogue**.

> **Philosophy**: The skill acts as your cinematographer - it doesn't just execute,
> it **thinks with you**. It makes suggestions, explains rationale, asks for your
> input, and learns from completed projects.

## Quick Start

```bash
# Start a new storyboard session (will ask questions)
./run.sh start screenplay.md --json

# Continue with answers to questions
./run.sh continue --session <ID> --answers '{"camera_s1": "sounds good"}'

# Auto-approve all suggestions (non-collaborative mode)
./run.sh start screenplay.md --auto-approve
```

## Collaboration Loop

The skill operates in a **question-answer loop** with the calling agent:

```
┌─────────────────────────────────────────────────────────────┐
│                    COLLABORATION LOOP                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. Agent calls: ./run.sh start screenplay.md --json         │
│                         ↓                                    │
│  2. Skill returns: {                                         │
│       status: "needs_input",                                 │
│       suggestions: [                                         │
│         "For Scene 3 where Sarah confronts the villain,      │
│          I'm thinking a Panaflex with low-key lighting       │
│          would enhance the tension. A slow pan from her      │
│          face to the window would build suspense.            │
│          What do you think?"                                 │
│       ],                                                     │
│       session_id: "storyboard-20260129-abc123"               │
│     }                                                        │
│                         ↓                                    │
│  3. Agent/User reviews suggestions, provides feedback        │
│                         ↓                                    │
│  4. Agent calls: ./run.sh continue --session ID --answers    │
│                         ↓                                    │
│  5. Skill proceeds or asks more questions                    │
│                         ↓                                    │
│  6. Repeat until status: "complete"                          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Creative Suggestions

Instead of dry questions like "What emotion for Scene 3?", the skill offers **filmmaker suggestions**:

> 💡 **Scene 3 - Camera Suggestion**
>
> "In Scene 3 where Sarah confronts the villain, I'm thinking we should use
> a slow push-in as the tension builds. It would really draw the audience
> into the character's anxiety."
>
> _Rationale_: The cautious movement and sparse dialogue suggest building dread -
> a push-in amplifies this without words.
>
> _Alternatives_: locked-off static for uncomfortable stillness, handheld for visceral unease
>
> → sounds good / prefer static / let's try handheld / suggest something else

## Memory Integration

The skill queries `/memory` to recall learned techniques:

```python
# When screenplay references "Blade Runner 2049"
techniques = recall_film_reference("Blade Runner 2049")
# Returns learned techniques from /ingest-movie

# The skill incorporates this into suggestions:
"I see you've referenced 'Blade Runner 2049' for Scene 1.
 From my memory of that film:
 • 2049 Minimal Composition: Desolate, geometric framing...
 • 2049 Hologram Lighting: Magenta/cyan holographic glow...
 Should I apply these techniques?"
```

**Memory scopes used:**

- `horus-storyboarding` - Storyboard-specific learnings
- `horus-movies` - Techniques from ingested films

## Commands

### start

Start a new storyboard session.

```bash
./run.sh start screenplay.md [options]

Options:
  --output-dir, -o   Output directory (default: ./output)
  --fidelity, -f     Panel fidelity: sketch|reference (default: sketch)
  --format           Output format: mp4|html|panels (default: mp4)
  --auto-approve, -y Skip all questions, use defaults
  --json, -j         Output structured JSON for agent consumption
```

### continue

Continue an existing session with answers.

```bash
./run.sh continue --session <ID> --answers '<JSON>' [options]

Options:
  --search-dir       Directory to search for session files
  --json, -j         Output structured JSON
```

### status

Check status of an existing session.

```bash
./run.sh status --session <ID>
```

### demo

Run a demo with sample screenplay showing the collaboration loop.

```bash
./run.sh demo           # Interactive with questions
./run.sh demo -y        # Auto-approve, skip questions
./run.sh demo --json    # JSON output for agents
```

## Output Formats

| Format   | Description                         | Use Case                           |
| -------- | ----------------------------------- | ---------------------------------- |
| `mp4`    | Video animatic with timed panels    | Preview timing, share with team    |
| `html`   | Interactive gallery with navigation | Review, iterate, keyboard controls |
| `panels` | Directory of PNG images             | Custom assembly, integration       |

## Panel Fidelity

| Level       | Description                                  | Speed                      |
| ----------- | -------------------------------------------- | -------------------------- |
| `sketch`    | Composition guides with shot codes           | Fast                       |
| `reference` | Stick figure placeholders                    | Medium                     |
| `generated` | AI-generated images (requires /create-image) | Slow (not yet implemented) |

## Integration Points

### /create-movie

This skill is a sub-phase of `/create-movie`:

```
/create-movie workflow:
  RESEARCH → SCRIPT → [STORYBOARD] → BUILD TOOLS → GENERATE → ASSEMBLE
                ↑
         /create-storyboard
```

### /create-story

Takes screenplay output as input:

```bash
# After /create-story generates screenplay.md
./run.sh start /path/to/screenplay.md
```

### /memory

Queries for learned filmmaking techniques:

```python
from memory_bridge import recall_film_reference, learn_technique

# Recall techniques
techniques = recall_film_reference("The Godfather")

# Store new technique after project
learn_technique(
    "Tension Push-In",
    "Slow 10-second push-in during confrontation",
    source="Project: Dark Horizon"
)
```

### /ingest-movie

Techniques ingested via `/ingest-movie` become available for recall:

```bash
# Ingest a film's techniques
/ingest-movie "Blade Runner 2049"

# Later, /create-storyboard can recall:
"From my memory of Blade Runner 2049:
 • Minimal Composition: Desolate, geometric framing..."
```

## Structured JSON Output

For agent consumption, use `--json` flag. Response format:

```json
{
  "status": "needs_input",
  "phase": "camera_plan",
  "session_id": "storyboard-20260129-abc123",
  "questions": [
    {
      "id": "camera_s1",
      "scene_number": 1,
      "question_type": "creative_suggestion",
      "question": "For Scene 1, I'm thinking a slow push-in...",
      "options": ["sounds good", "prefer static", "suggest something else"],
      "context": "The cautious movement suggests building dread..."
    }
  ],
  "partial_results": {
    "total_shots": 5,
    "total_duration": 21.5,
    "shot_plan_file": "output/.../shot_plan.json"
  },
  "message": "Generated 5 shots. Please review my creative suggestions.",
  "resume_command": "./run.sh continue --session ... --answers '<JSON>'"
}
```

**Status values:**

- `needs_input` - Waiting for answers to proceed
- `in_progress` - Phase executing, will continue
- `complete` - All phases done, outputs ready
- `error` - Something failed

## File Structure

```
create-storyboard/
├── SKILL.md                 # This file
├── run.sh                   # Entry point
├── orchestrator.py          # Main CLI with collaboration loop
├── screenplay_parser.py     # Parse markdown/Fountain screenplays
├── camera_planner.py        # Auto-select shots, estimate timing
├── panel_generator.py       # Generate visual panels
├── animatic_assembler.py    # Create MP4/HTML output
├── collaboration.py         # Session state, questions, structured output
├── creative_suggestions.py  # Natural language filmmaker suggestions
├── memory_bridge.py         # /memory integration
├── shot_taxonomy.py         # Camera shot definitions
└── sanity/                  # Dependency verification
    ├── ffmpeg_concat.sh
    ├── pillow_composite.py
    └── run_all.sh
```

## Example Session

```bash
$ ./run.sh start screenplay.md

============================================================
📊 Status: NEEDS_INPUT
📍 Phase: camera_plan
🔑 Session: storyboard-20260129-134523-a1b2c3
============================================================

🎬 CREATIVE SUGGESTIONS

Here's what I'm thinking for the visual approach:

### 1. Scene 1 - Camera Suggestion

💡 For Scene 1 in the APARTMENT, I'm thinking we should use a slow
   push-in as the tension builds. It would really draw the audience
   into the character's anxiety.

   *Why*: The cautious movement and sparse dialogue suggest building
   dread - a push-in amplifies this without words.
   *Or*: locked-off static for uncomfortable stillness, handheld for
   visceral unease

   → sounds good / prefer static / let's try handheld / suggest something else

### 2. Scene 1 - Reference Suggestion

💡 I see you've referenced 'Blade Runner 2049' for Scene 1. I could
   search my memory for specific techniques from that film - the color
   grading, the shot composition, the pacing. Should I pull those details?

   *Why*: The reference to Blade Runner 2049 gives us a visual language
   to draw from.

   → yes_search_memory / no_skip / skip_all_references

============================================================
Reply with your thoughts on each, or just say 'looks good' to proceed.
============================================================

▶️  To continue: ./run.sh continue --session storyboard-20260129-134523-a1b2c3 --answers '<JSON>'
```

## Camera Shot Taxonomy

| Code | Name              | Description                   | Emotional Use          |
| ---- | ----------------- | ----------------------------- | ---------------------- |
| EWS  | Extreme Wide      | Full environment, tiny figure | Isolation, scale       |
| WS   | Wide Shot         | Full body with environment    | Establishing, action   |
| FS   | Full Shot         | Head to toe                   | Physical performance   |
| MWS  | Medium Wide       | Knees up                      | Dialogue with movement |
| MS   | Medium Shot       | Waist up                      | Standard dialogue      |
| MCU  | Medium Close-Up   | Chest up                      | Emotional dialogue     |
| CU   | Close-Up          | Face only                     | Key emotional moments  |
| ECU  | Extreme Close-Up  | Detail (eyes, hands)          | Climactic intimacy     |
| OTS  | Over-The-Shoulder | Conversation framing          | Dialogue, presence     |
| POV  | Point of View     | Character's perspective       | Empathy, discovery     |

## Dependencies

- Python 3.11+
- FFmpeg (for video assembly)
- Pillow (for panel generation)
- Typer (CLI framework)

Run sanity checks:

```bash
./sanity/run_all.sh
```
