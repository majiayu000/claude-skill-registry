---
name: procedural-generation
cluster: game-dev
description: "Algorithmic technique for generating game content like terrains and levels using noise functions and rules."
tags: ["procedural-generation","game-algorithms","content-generation"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "procedural generation game dev algorithms noise perlin"
---

## Purpose
This skill allows OpenClaw to programmatically generate game content, such as terrains and levels, using algorithms like Perlin noise and rule-based systems, reducing manual design effort.

## When to Use
Apply this skill for dynamic content in games where variability is key, like procedural worlds in roguelikes or infinite runners, or when optimizing for replayability and asset efficiency in resource-constrained projects.

## Key Capabilities
- Generate 2D/3D terrains via noise functions (e.g., Perlin, Simplex) with parameters for scale, octaves, and persistence.
- Create levels using rule-based algorithms, such as cellular automata for cave generation or binary space partitioning for dungeons.
- Support custom seed values for reproducible outputs, integrating with game engines like Unity or Godot.
- Handle multi-threaded generation for performance in real-time applications.
- Export results in formats like JSON for meshes or PNG for heightmaps.

## Usage Patterns
Always initialize with a seed for consistency; use CLI for quick prototyping and API for integration. Provide exact parameters to avoid defaults.

Example 1: Generating a Perlin terrain for a game world:
- CLI command: `openclaw generate terrain --noise perlin --seed 42 --width 256 --height 256 --output terrain.json`
- In code (Python): `import openclaw; terrain_data = openclaw.api.generate_terrain({'noise': 'perlin', 'seed': 42, 'width': 256})`

Example 2: Creating a procedural level with rules:
- CLI command: `openclaw generate level --rules '{"min_rooms": 5, "max_rooms": 10}' --seed 123 --output level.yaml`
- In code (JavaScript): `const openclaw = require('openclaw'); const level = openclaw.api.generate_level({rules: {min_rooms: 5}, seed: 123});`

Follow patterns by chaining commands, e.g., generate then validate: `openclaw generate terrain ... && openclaw validate output.json`.

## Common Commands/API
Use the OpenClaw CLI or REST API; authenticate via `$OPENCLAW_API_KEY` environment variable.

- CLI Commands:
  - `openclaw generate terrain [flags]`: Flags include `--noise [type]` (e.g., perlin), `--seed [int]`, `--scale [float]`; e.g., `openclaw generate terrain --noise perlin --seed 42`.
  - `openclaw generate level [flags]`: Flags include `--rules [JSON string]`; e.g., `openclaw generate level --rules '{"type": "dungeon"}'`.
  - `openclaw validate [file]`: Checks generated output; e.g., `openclaw validate terrain.json --check integrity`.

- API Endpoints:
  - POST /api/procedural/generate: Body as JSON, e.g., `{"type": "terrain", "params": {"noise": "perlin", "seed": 42}}`; requires header `Authorization: Bearer $OPENCLAW_API_KEY`.
  - GET /api/procedural/status: Query job status; e.g., `GET /api/procedural/status?job_id=123` with auth header.

Config formats: Use JSON for API bodies, e.g., `{"noise": "perlin", "octaves": 4}`; for CLI, pass as flags or files, e.g., `--config config.json` where config.json is `{"seed": 42}`.

## Integration Notes
Set `$OPENCLAW_API_KEY` in your environment before calls; integrate into game loops by importing the OpenClaw SDK and calling async functions. For Unity, use a C# wrapper: `OpenClawAPI.GenerateTerrain(new Dictionary<string, object> { {"noise", "perlin"} });`. In Godot, hook into scripts: `var result = OpenClaw.generate_level({"rules": {"min_rooms": 5}})`. Ensure error logging is enabled via SDK config, e.g., set `openclaw.config.log_level = 'debug'`.

## Error Handling
Always wrap API/CLI calls in try-catch blocks; check for common errors like invalid parameters or network issues.

- For CLI: Parse errors from stdout, e.g., if `--noise` is invalid, it returns "Error: Unknown noise type"; handle with scripts: `if [ $? -ne 0 ]; then echo "Generation failed"; fi`.
- For API: Catch HTTP errors, e.g., in Python: `try: response = openclaw.api.generate_terrain({...}) except openclaw.APIError as e: print(e.code)  # e.g., 400 for bad request`.
- Specific cases: If seed is non-integer, API returns 422; validate inputs first, e.g., `if not isinstance(seed, int): raise ValueError("Seed must be an integer")`.
- Use retries for transient errors: In code, `for attempt in range(3): try: openclaw.api.generate(...) except: time.sleep(1)`.

## Graph Relationships
- Related to: level-design (shares game-dev cluster for combined level building), asset-creation (uses generated content as inputs).
- Depends on: noise-libraries (for underlying noise functions), game-engines (for integration hooks).
