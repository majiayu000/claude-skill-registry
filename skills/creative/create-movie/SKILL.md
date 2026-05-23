---
name: create-movie
description: >
  Orchestrated movie creation for Horus persona. Guides through phases:
  Research → Script → Build Tools → Generate → Assemble. Uses Docker-isolated
  coding environment, free/open-source tools only, with full memory integration.
allowed-tools: [Bash, Read, Write, Task, WebFetch, WebSearch]
triggers:
  - create movie
  - make movie
  - make film
  - create film
  - horus filmmaking
  - horus movie
  - create mockumentary
  - create short film
  - create music video
  - vibe coding movie
  - ai movie creation
  - study filmmaking
  - learn cinematography
  - horus study
  - horus learn filmmaking
metadata:
  short-description: "Orchestrated movie creation (Research → Script → Build → Generate → Assemble)"
  author: "Horus"
  version: "0.1.0"
---

# create-movie

Orchestrated movie creation for Horus persona. Creates mockumentaries, short films, music videos, and educational content through a phased workflow.

## Philosophy

> "AI isn't the artist, it's the amplifier" - Nobody & The Computer

Horus uses AI to turn imagination into audiovisual reality. He doesn't just use pre-built tools - he writes code to create his own tools.

## Phases

```
HARDWARE CHECK → RESEARCH → SCRIPT → BUILD TOOLS → GENERATE → ASSEMBLE → LEARN
```

### Phase 0: Hardware Detection (Automatic)

Before any generation, the orchestrator automatically detects hardware via `/ops-workstation`:

```bash
# Automatic hardware check on startup
./run.sh create "prompt"
# → Calls /ops-workstation gpu to detect VRAM
# → Calls /ops-workstation memory to detect RAM
# → Auto-selects optimal model variant
```

**Auto-Selection Logic:**

| Detected VRAM | Model Selected | Settings |
|---------------|----------------|----------|
| ≥24GB | LTX-2 19B FP8 | 720p/1080p, audio on, batch=1 |
| 16-23GB | LTX-2 19B FP4 | 720p only, audio on, batch=1 |
| 12-15GB | LTX-2 Distilled 2B | 720p, audio optional, batch=1 |
| <12GB | **RunPod suggested** | Prompts to use `/ops-runpod` |

**RAM-Based Optimizations:**

| Detected RAM | Optimization |
|--------------|--------------|
| ≥128GB | Weight streaming enabled (offload to RAM) |
| 64-127GB | Partial offloading |
| <64GB | No offloading, strict VRAM limits |

**Override Auto-Detection:**
```bash
# Force specific model variant
./run.sh create "prompt" --model ltx2-fp4
./run.sh create "prompt" --model ltx2-distilled
./run.sh create "prompt" --runpod  # Force cloud generation
```

### Phase 1: Research (Library-First)
1. **Check Horus's Library First:**
   - `horus-filmmaking` scope (past techniques, learnings)
   - `horus_lore` scope (YouTube transcripts, film analysis)
   - Ingested movies with emotion tags
   - Episodic archive (past filmmaking sessions)
2. **Search for New Resources:**
   - `/ingest-movie search` for films to watch
   - `/ingest-youtube search` for tutorials
3. **Deep Web Research:**
   - `/dogpile` for comprehensive multi-source search
   - `/surf` for specific tutorials/references

### Phase 2: Script (via /create-story)
- Integrates with `/create-story` skill for screenplay generation
- Uses Chutes models (chimera, qwen, deepseek-r1) for creative writing
- Parses INT./EXT. headings, dialogue, action, audio cues
- Outputs structured scene breakdown with visual descriptions

**Format Options:**
- `screenplay` (default) - Standard INT./EXT. scene headings
- `mockumentary` - Interview segments with talking heads + B-roll
- `reconstruction` - Historical recreation with narrator framing

### Phase 3: Build Tools
- Write code in Docker-isolated sandbox
- Create custom tools for specific effects
- Iterate on approaches

### Phase 4: Generate
- Use ComfyUI, Stable Diffusion for images
- Use **auto-selected video model** based on hardware (LTX-2 FP8/FP4/Distilled)
- Use Whisper, IndexTTS2 for audio
- If hardware insufficient, automatically suggests `/ops-runpod`

### Phase 5: Assemble
- Combine assets with FFmpeg
- Output MP4 video or interactive HTML

### Phase 6: Learn
- Store successful techniques in /memory
- Remember what worked for future movies

## Quick Start

```bash
cd .pi/skills/create-movie

# Full orchestrated workflow (recommended)
./run.sh create "A 30-second film about discovering colors"

# With options
./run.sh create "film noir detective" \
    --duration 60 \
    --style "high contrast, shadows, venetian blinds" \
    --format mp4 \
    --work-dir ./noir_project

# Individual phases (for manual control)
./run.sh research "film noir lighting techniques"
./run.sh script --from-research research.json --duration 30 --use-create-story
./run.sh build-tools --script script.json
./run.sh generate --tools ./tools --script script.json --style "cinematic"
./run.sh assemble --assets ./assets --output movie.mp4 --format mp4
./run.sh learn --project-dir ./movie_project
```

## CLI Commands

### create
Full orchestrated workflow through all phases.
```bash
./run.sh create PROMPT [OPTIONS]
  --output, -o       Output file (default: movie.mp4)
  --work-dir, -w     Working directory (default: ./movie_project)
  --duration, -d     Target duration in seconds (default: 30)
  --style, -s        Visual style (e.g., 'cinematic', 'film noir')
  --format, -f       Output format: mp4 or html (default: mp4)
  --store-learnings  Store learnings in memory (default: true)
  --skip-research    Skip research phase if research.json exists
```

### research
Library-first research: checks Horus's memory and ingested content before external search.
```bash
./run.sh research TOPIC [OPTIONS]
  --output, -o       Output file (default: research.json)
  --skip-external    Only search library, skip external sources
```

### script
Generate screenplay with scene breakdown. Integrates with `/create-story`.
```bash
./run.sh script [OPTIONS]
  --from-research, -r  Research JSON file (required)
  --prompt, -p         Override topic from research
  --duration, -d       Target duration in seconds
  --use-create-story   Use /create-story skill for screenplay
  --model, -m          LLM model (default: chimera)
  --output, -o         Output file (default: script.json)
```

### build-tools
Generate custom tools in Docker sandbox.
```bash
./run.sh build-tools [OPTIONS]
  --script, -s       Script JSON file (required)
  --output-dir, -o   Output directory (default: ./tools)
  --skip-docker      Use host instead of Docker sandbox
```

### generate
Create images, video, and audio assets.
```bash
./run.sh generate [OPTIONS]
  --tools, -t        Tools directory (default: ./tools)
  --script, -s       Script JSON file (required)
  --output-dir, -o   Assets output directory (default: ./assets)
  --style            Visual style to apply
```

### assemble
Combine assets into final output.
```bash
./run.sh assemble [OPTIONS]
  --assets, -a       Assets directory (required)
  --output, -o       Output file/directory (required)
  --format, -f       Output format: mp4 or html (default: mp4)
  --fps              Frames per second for MP4 (default: 24)
```

### learn
Store filmmaking insights in memory after a project.
```bash
./run.sh learn [OPTIONS]
  --project-dir, -p  Project directory (required)
  --scope            Memory scope (default: horus-filmmaking)
  --dry-run          Show learnings without storing
```

### study
Pre-phase: Learn filmmaking topics BEFORE creating movies. Targeted /dogpile with internal (memory) + external (web) search, then stores via `/memory learn`.
```bash
./run.sh study TOPIC [OPTIONS]
  --scope            Memory scope (default: horus-filmmaking)
  --deep/--quick     Deep research (dogpile) vs quick (YouTube search)
  --list-topics      Show suggested filmmaking topics

# Examples:
./run.sh study "cinematography lighting techniques" --deep
./run.sh study "camera framing composition" --deep
./run.sh study --list-topics
```

### study-all
Comprehensive learning session - studies all core filmmaking topics.
```bash
./run.sh study-all [OPTIONS]
  --scope            Memory scope (default: horus-filmmaking)
```

## Output Formats

### MP4 Video
Standard video file, playable anywhere.

### Interactive HTML
Web-based experience with:
- Frame-by-frame navigation
- Audio controls
- Scene metadata viewer

## Available Skills

Horus has access to all skills in `.pi/skills/`:

| Skill | Purpose in Movie Creation |
|-------|---------------------------|
| `/dogpile` | Deep research on techniques, references |
| `/surf` | Visit websites, tutorials, references |
| `/memory` | Recall prior techniques, store learnings |
| `/create-image` | Generate images for scenes |
| `/tts-train` | Horus's voice for narration |
| `/ingest-movie` | Ingest reference movies for style analysis |
| `/create-paper` | Write stories, scripts, creative content |
| `/episodic-archiver` | Archive movie creation sessions |
| `/anvil` | Debug and harden custom tools |
| `/ingest-book` | Search books for story inspiration |

## Free/Open-Source Tools

| Purpose | Tool |
|---------|------|
| Image Generation | Stable Diffusion (ComfyUI) |
| Video Generation | **LTX-2** (recommended), Mochi 1, CogVideoX (fallbacks) |
| Video Processing | FFmpeg |
| Speech-to-Text | faster-whisper |
| Text-to-Speech | IndexTTS2 |

## Video Model Selection Guide

Choose video model based on your GPU VRAM and use case. VRAM figures include 3-5GB headroom for pipeline overhead (ComfyUI/loader/audio), batch=1, FP8/FP4 where noted.

| VRAM | Recommended Models | Best For |
|------|-------------------|----------|
| 12GB (RTX 3060/4070) | LTX-2 Distilled (2B), CogVideoX-2B | Quick iterations, pre-viz |
| 16GB (RTX 4080/A4000) | LTX-2 19B FP4 (720p, ≤10s), WAN 2.2, SVD | Medium quality production |
| 24GB (RTX 4090/A5000) | **LTX-2 19B FP8** (recommended), WAN 2.2, Mochi | High quality production |
| 40GB+ (A100/H100) | LTX-2 BF16 (43GB), Full Mochi, Open-Sora 2.0 | Maximum quality |

### Safe Defaults (RTX A5000 24GB)

```
Model: LTX-2 19B FP8
Resolution: 720p
Clip length: 10s
Batch size: 1
Seed: fixed
Audio: on
```

If runtime VRAM >22GB or instability occurs: lower resolution to 540p, disable audio, or shorten clips. Avoid parallel jobs on 24GB.

### Model Characteristics

| Model | Speed | Quality | Audio | Best Use Case |
|-------|-------|---------|-------|---------------|
| **LTX-2 19B FP8** ⭐ | Fast | High | Yes | **Recommended** - Camera controls, audio sync |
| **LTX-2 Distilled** | Fastest | Medium | Yes | Rapid iteration, light VRAM |
| **WAN 2.2 14B** | Slow | Very High | No | Silent films, German Expressionism, art films |
| **Mochi 1** | Slow | High | No | Final renders, prompt adherence |
| **HunyuanVideo** | Medium | High | No | Production quality |
| **CogVideoX-5B** | Medium | High | No | General purpose (fallback) |

**Recommendation:**
- Use **LTX-2 19B FP8** for production work with audio sync and camera controls
- Use **WAN 2.2** for silent films or when audio isn't needed (higher visual quality for same VRAM)
- Fallback to Mochi for maximum quality or CogVideoX for compatibility

### LTX-2: Recommended Video Model

[LTX-2](https://github.com/Lightricks/LTX-Video) is a 19B parameter DiT-based audio-video foundation model.

**Model Variants:**

| Model | Size | VRAM | Quality | Recommended For |
|-------|------|------|---------|-----------------|
| **LTX-2 19B FP8** ⭐ | ~19GB (+3-5GB overhead) | 24GB | High | Production (A5000, 720p/1080p ≤12-15s, batch=1) |
| LTX-2 19B FP4 | ~12GB (+3-5GB overhead) | 16GB | High | Faster, slightly less quality (720p ≤10s) |
| LTX-2 BF16 (full) | ~43GB | 40GB+ | Highest | RunPod/A100 only |
| LTX-2 Distilled 2B | ~4GB | 12GB | Medium | Rapid iteration |

**FP8 Compatibility:** Requires compatible CUDA/cuDNN/PyTorch builds. Follow LTX-Video docs for driver requirements.

**Key Features:**
- **Synchronized Audio-Video Generation**: Generates coherent audio + video together
- **Camera Controls**: Dolly, jib, static shots with natural camera motion
- **IC-LoRA**: Style transformations (anime, sketch, etc.) with ~1GB VRAM
- **Keyframe Interpolation**: Morphing between keyframes
- **Pose/Depth/Canny Controls**: Precise composition control (Canny edge detection)
- **Text-to-Video and Image-to-Video**: Both workflows supported

**ComfyUI Templates:**

| Template | Use Case |
|----------|----------|
| `LTX2 Text-to-Video` | Generate from text prompts |
| `LTX2 Image-to-Video` | Animate a still image |
| `LTX2 Canny-to-Video` | Edge detection guided generation |
| `LTX2 Distilled` | Fast iteration, lower VRAM |

**Installation:**
```bash
# ComfyUI (recommended)
# Install "LTX-Video" from ComfyUI Manager
# Templates appear automatically

# Or standalone
pip install ltx-video
```

**ComfyUI VRAM Optimization Flags:**
```bash
# Reserve VRAM for other operations (prevents OOM during generation)
python -m main --reserve-vram 5

# Low VRAM mode - offloads to system RAM (slower but prevents OOM)
python -m main --lowvram

# Weight streaming - NVIDIA/ComfyUI collaboration for 256GB RAM systems
# Automatically offloads model weights to system RAM when VRAM exhausted
```

**Additional Resources:**
- [ComfyUI_LTX-2_VRAM_Memory_Management](https://github.com/RandomInternetPreson/ComfyUI_LTX-2_VRAM_Memory_Management) - Nodes for long videos on consumer GPUs

### Camera Control Reference (LTX-2)

LTX-2 supports cinematic camera movements via prompt keywords:

| Movement | Prompt Keywords | Effect |
|----------|-----------------|--------|
| **Static** | `static shot`, `locked camera` | Fixed camera position |
| **Dolly** | `dolly in`, `dolly out`, `push in` | Camera moves toward/away from subject |
| **Jib/Crane** | `jib up`, `jib down`, `crane shot` | Vertical camera sweep |
| **Pan** | `pan left`, `pan right` | Horizontal rotation |
| **Tilt** | `tilt up`, `tilt down` | Vertical rotation |
| **Tracking** | `tracking shot`, `follow shot` | Camera follows subject |
| **Zoom** | `zoom in`, `zoom out` | Focal length change |

**Example Prompts:**
```
# Dramatic reveal
"Dolly in slowly to a detective examining evidence, noir lighting, static hold on face"

# Action sequence
"Tracking shot following runner through city streets, handheld, dynamic"

# Interview setup
"Static medium shot, subject centered, shallow depth of field, jib down to hands"
```

**Combining Movements:**
```
"Jib up while dolly out, revealing vast landscape, golden hour, cinematic"
```

### WAN 2.2: Silent Film Alternative

[WAN 2.2](https://github.com/Wan-Video/Wan2.2) is a 14B parameter model optimized for visual quality without audio:

**Best For:**
- Silent films and art cinema
- German Expressionism era aesthetics (Nosferatu, Metropolis, Cabinet of Dr. Caligari)
- High visual fidelity when audio isn't needed
- Projects where audio will be added separately

**Comparison to LTX-2:**
| Aspect | LTX-2 19B FP8 | WAN 2.2 14B |
|--------|---------------|-------------|
| Audio | Synchronized | None |
| Speed (10-sec HD, A5000) | ~3.5-4.5 min | ~5-6 min |
| Visual Quality | High | Very High |
| VRAM (24GB) | Works | Works |

**When to Choose WAN 2.2:**
- Creating silent films with intertitles
- German Expressionism homages
- Music videos where audio is pre-recorded
- Art films with separate sound design

**Practical Notes:** Seed control recommended for stable multi-shot outputs. 720p preferred on 24GB for consistent speeds.

## Performance Expectations

Video generation is compute-intensive. Plan for overnight batch processing rather than real-time iteration.

### Local Generation Times (RTX A5000, 24GB VRAM)

| Video Length | Resolution | Model | Time |
|--------------|------------|-------|------|
| 5 seconds | HD (720p) | LTX-2 19B FP8 | ~1-1.5 min |
| 10 seconds | HD (720p) | LTX-2 19B FP8 | ~3.5-4.5 min |
| 10 seconds | Full HD (1080p) | LTX-2 19B FP8 | ~5-6.5 min |
| 15 seconds | HD (720p) | LTX-2 19B FP8 | ~6-7.5 min |
| 10 seconds | HD (720p) | WAN 2.2 | ~5-6 min |

**Notes:**
- Timings based on Alex Ziskind's benchmarks (RTX 5080) with +15-25% buffer for A5000
- Audio synchronization adds ~10-15% time vs video-only runs
- IO/storage affects throughput; prefer local NVMe, avoid network mounts

### Realistic Workflow

For a **2-minute film** (12 x 10-second clips):
- Generation time: ~42-54 min (LTX-2, 720p) to ~60-72 min (WAN 2.2)
- With retakes and iterations: **2-4 hours**
- Full production with assembly: **overnight task**

**Recommendation:** Queue video generation as overnight background tasks. Use `/task-monitor` to track progress.

```bash
# Example: Run generation overnight
./run.sh generate --script script.json --output-dir ./assets &
# Check progress next morning
```

## RunPod for Large Tasks

Use `/ops-runpod` when local generation would cause OOM errors.

### When to Use RunPod

| Scenario | Local (A5000 24GB) | RunPod Needed |
|----------|-------------------|---------------|
| LTX-2 19B FP8, 10-sec HD | Works | No |
| LTX-2 19B FP8, 15-sec 1080p | Works (batch=1) | No |
| 1080p clips >12-15 sec (FP8) | May OOM | Prefer 720p or split; RunPod optional |
| LTX-2 BF16 (43GB full model) | OOM | Yes (A100 40GB+) |
| Very long videos (>20 sec 1080p) | Likely OOM | Yes |
| Batch processing (10+ clips) | Slow but works | Optional (faster) |
| WAN 2.2 + LTX-2 parallel | High OOM risk | Prefer sequential or RunPod |

**OOM Threshold Guidance (A5000 24GB):**
- LTX-2 FP8: 1080p clips over ~12-15s may OOM with audio; use 720p, shorten clips, or disable audio
- Control nets (pose/depth/canny) and multiple LoRAs increase memory; enable selectively
- Monitor runtime VRAM; keep ≤22GB to avoid instability

### RunPod Workflow

```bash
# Provision GPU for large task
/ops-runpod provision --gpu a100-40gb --task "LTX-2 BF16 generation"

# Run generation on RunPod
/ops-runpod run --script generate.sh

# Download results and terminate
/ops-runpod download --output ./assets
/ops-runpod terminate
```

**RunPod GPU Options:**
- BF16/full precision: A100 40-80GB, H100 (required)
- FP8/FP4 tasks: L40S 48GB, A10G 24GB (cheaper alternatives)

**Cost Consideration:** RunPod charges by the hour. For overnight tasks, local generation is more cost-effective. Consider spot/preemptible instances for savings.

### Troubleshooting & Fallbacks

**OOM Mitigation:**
1. Reduce resolution (720p → 540p)
2. Shorten clip length
3. Set batch=1
4. Switch FP mode (BF16 → FP8 → FP4)
5. Disable audio
6. Split long clips into segments

**Stability:**
- Fix seed for reproducibility
- Avoid parallel jobs on 24GB
- Reduce control nets and LoRA stacks

**Fallback Path:** If LTX-2 fails, switch to WAN 2.2 (video-only) or CogVideoX; add audio separately in post.

## Memory Integration

After each movie, stores:
- Successful prompts
- Working tool code
- Technique insights
- Concept relationships

Scope: `horus-filmmaking`

## Workflow Patterns (from Nobody & The Computer)

### Multi-Model Collaboration
Different AI models handle different creative aspects, inspired by "Bach x Coltrane x Kuti x Takemitsu":
- **Model A (Claude)**: Structure, composition, narrative arc
- **Model B (GPT)**: Improvisation, dialogue, variation
- **Model C (Grok)**: Energy, rhythm, pacing
- **Model D (DeepSeek)**: Texture, atmosphere, silence

Each model builds on previous work. Constraints: 100 words max per turn for focused output.

### Critique Loop
From "A.I.thoven" sessions - "roast the piece with love":
1. Generate initial draft
2. Critique constructively (what works, what doesn't)
3. Iterate based on feedback
4. Repeat until satisfied

### Iteration Speed
Use **LTX-2 Distilled** for rapid iterations during creative exploration.
Use **LTX-2 13B** for production with camera controls and audio sync.
Fallback to Mochi for maximum quality when camera control isn't needed.

## Example Session

```
Horus: I want to create a mockumentary about AI learning to paint.

[RESEARCH] Searching for documentary interview techniques, AI art history...
[SCRIPT] Breaking into 5 scenes: intro, discovery, struggle, breakthrough, reflection
[BUILD TOOLS] Writing code for interview framing effect, paint brush animation...
[GENERATE] Creating 45 frames, 3 audio tracks, 2 voice segments...
[ASSEMBLE] Combining into 2-minute video with transitions...
[LEARN] Storing 8 insights in memory for future films.

Output: ai_painter_mockumentary.mp4 (2:14)
```

## Dependencies

- Docker (for isolated code execution)
- FFmpeg (video processing)
- Python 3.11+ (orchestrator)
- GPU recommended (for Stable Diffusion, video models)
