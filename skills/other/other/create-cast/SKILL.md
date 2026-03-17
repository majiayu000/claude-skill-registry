---
name: create-cast
description: >
  Multi-round character casting orchestrator for the Horus movie pipeline.
  Extracts characters from scripts, discovers reference actors, generates
  identity images, and assigns voices. Runs as Phase 2.5 in create-movie.
triggers:
  - cast characters
  - create cast
  - character casting
  - identity pack
  - cast the movie
  - assign actors
allowed-tools:
  - Bash
  - Python
metadata:
  short-description: "Character casting with identity packs for Veo"

provides:
  - create-cast
composes:
  - create-score
  - create-storyboard
  - create-sound-design
  - create-story
  - memory
  - task-monitor
---

# Create Cast Skill

Multi-round collaborative workflow for casting characters in AI-generated movies.

## Quick Start

```bash
cd .pi/skills/create-cast

# Start a new casting session
./run.sh start path/to/script.json

# Continue with answers to questions
./run.sh continue --session casting-20260204-abc123 --answers '{"q1": "approve"}'

# Check session status
./run.sh status --session casting-20260204-abc123

# Export identity packs
./run.sh export --session casting-20260204-abc123 --output ./characters
```

## Philosophy

**Casting is collaborative.** The skill extracts characters, proposes specs, discovers
reference actors, generates identity images, and assigns voices - but asks questions
at each step to ensure alignment with the creator's vision.

**Identity consistency is the goal.** The output is a set of "identity packs" that
Veo can use to maintain character consistency across multiple shots.

## Casting Rounds

```
Round 1: Script Analysis
├── Parse script for character mentions
├── Extract dialogue to identify speakers
├── Infer physical descriptions from action text
├── Estimate screen time per character
└── Questions: Confirm character list and traits

Round 2: Reference Discovery (optional)
├── Call discover-talent for each main character
├── Build mood board of reference actors
└── Questions: Select reference actors or skip

Round 3: Identity Generation
├── Generate candidate looks via create-image
├── 3-5 options per character
└── Questions: Select best look or iterate

Round 4: Identity Pack Build
├── Generate front view (neutral lighting)
├── Generate 3/4 view (same lighting)
├── Generate full-body (outfit reference)
└── Questions: Approve angles or regenerate

Round 5: Voice Casting
├── Search existing voice models (learn-artist/tts-train)
├── Match voice type to available models
└── Questions: Approve voice or queue training
```

## Commands

### Start Casting Session

```bash
./run.sh start <script.json> [--json] [--auto-approve]
```

Begins a new casting session from a script file. Returns questions for Round 1.

Options:
- `--json`: Output structured JSON for agent parsing
- `--auto-approve`: Skip questions and use defaults (for automation)

### Continue Session

```bash
./run.sh continue --session <ID> --answers '<JSON>'
```

Provide answers to questions and advance to the next round.

The answers JSON maps question IDs to responses:
```json
{
  "confirm_characters": "approve",
  "sarah_trait_age": "early 30s",
  "villain_reference": "skip"
}
```

### Check Status

```bash
./run.sh status --session <ID> [--json]
```

Get current session status: phase, pending questions, completed characters.

### Export Identity Packs

```bash
./run.sh export --session <ID> --output <directory>
```

Export completed identity packs to a directory:
```
characters/
├── SARAH/
│   ├── identity_pack/
│   │   ├── front.png
│   │   ├── three_quarter.png
│   │   └── full_body.png
│   ├── character_bible.yaml
│   └── mood_board/
└── VILLAIN/
    └── ...
```

### List Sessions

```bash
./run.sh list
```

List all active and completed casting sessions.

## Character Spec Schema

```yaml
name: SARAH
role: protagonist
screen_time_estimate: 45.0  # seconds
physical:
  age_range: "early 30s"
  gender: "female"
  build: "athletic"
  hair: "short dark"
  distinguishing: "determined expression"
personality:
  - determined
  - resourceful
  - guarded
voice_type: "confident, measured"
dialogue_count: 12
scenes: [1, 3, 5, 7]
bridge_attributes:
  - Resilience
  - Precision
```

## Identity Pack Schema

```yaml
character_name: SARAH
images:
  front: characters/SARAH/identity_pack/front.png
  three_quarter: characters/SARAH/identity_pack/three_quarter.png
  full_body: characters/SARAH/identity_pack/full_body.png
prompt_descriptors:
  - "early 30s woman"
  - "athletic build"
  - "short dark hair"
  - "determined expression"
  - "wearing practical clothing"
lighting_notes: "Neutral studio lighting for Veo reference"
voice_model: "florence-pugh-rvc"
created_at: "2026-02-04T12:34:56Z"
```

## Integration with create-movie

This skill runs as **Phase 2.5** in the create-movie pipeline:

```
Phase 2: Script (create-story)
    ↓
Phase 2.5: CASTING (create-cast) ← THIS SKILL
    ↓
Phase 3: Storyboard (create-storyboard)
```

The identity packs flow into Phase 4 (Generate) where Veo uses them
for character consistency.

### Automatic Invocation

```python
# In create-movie orchestrator (after script phase)
from create_cast import run_casting_session

casting_result = run_casting_session(
    script_path=script_file,
    output_dir=characters_dir,
    model=model,
    auto_approve=auto_approve,
)
```

## Skill Dependencies

| Skill | Purpose | Required |
|-------|---------|----------|
| discover-talent | Reference actor search | Optional |
| create-image | Identity image generation | Required |
| learn-artist | Voice/instrument model lookup | Optional |
| tts-train | Voice model listing | Optional |
| memory | Store learned preferences | Optional |

## Configuration

Environment variables:

```bash
TMDB_API_KEY=xxx           # For discover-talent
OPENAI_API_KEY=xxx         # For create-image (if using DALL-E)
FLUX_API_KEY=xxx           # For create-image (if using FLUX)
```

## Example Workflow

```
Agent: "./run.sh start script.json"

Output: 
{
  "status": "needs_input",
  "phase": "ANALYSIS",
  "questions": [
    {
      "id": "confirm_characters",
      "question": "I found 3 characters: SARAH (45s), VILLAIN (30s), GUARD (10s). Confirm?",
      "options": ["approve", "add_character", "remove_character"]
    },
    {
      "id": "sarah_age",
      "question": "SARAH's age isn't specified. What age range?",
      "options": ["20s", "early 30s", "late 30s", "40s"]
    }
  ],
  "resume_command": "./run.sh continue --session casting-20260204-abc123 --answers '{...}'"
}

Agent: "./run.sh continue --session casting-20260204-abc123 --answers '{\"confirm_characters\": \"approve\", \"sarah_age\": \"early 30s\"}'"

Output:
{
  "status": "needs_input",
  "phase": "DISCOVERY",
  "questions": [
    {
      "id": "sarah_reference",
      "question": "For SARAH, I found these reference actors: [Florence Pugh, Mackenzie Davis]. Select one or skip?",
      "options": ["Florence Pugh", "Mackenzie Davis", "skip_reference"]
    }
  ]
}
```

## Sanity Checks

```bash
./run.sh sanity
# or
./sanity/sanity.sh
```

Verifies:
1. Python syntax for all modules
2. Imports work correctly
3. CLI help displays
4. Schema validation
5. discover-talent integration (if available)
