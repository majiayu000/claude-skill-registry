---
name: voice-channel-uwd
description: Voice Channel UWD Skill
version: 1.0.0
---

# Voice Channel UWD Skill

**Status**: ✅ Production Ready  
**Trit**: 0 (ERGODIC - balanced flow between play/coplay)  
**Principle**: Voice communication as undirected wiring diagram with GF(3) conservation  
**Source**: plurigrid/VoiceChannelUWD.jl + UnwiringDiagrams.jl + Arena Protocol

---

## Overview

**Voice Channel UWD** models real-time voice communication using the categorical framework of undirected wiring diagrams:

```
┌─────────────────────────────────────────────────────────────────────┐
│                    VOICE CHANNEL AS UWD                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   ┌──────────┐     ┌──────────┐     ┌──────────┐                   │
│   │ 🔊 Alice │     │ 👂 Bob   │     │ 🔇 Carol │   ← Boxes         │
│   │ trit: +1 │     │ trit: 0  │     │ trit: -1 │     (Participants) │
│   │ #D82626  │     │ #26D826  │     │ #2626D8  │                    │
│   └────┬─────┘     └────┬─────┘     └────┬─────┘                   │
│        │                │                │                          │
│        └───────────┬────┴────┬───────────┘                          │
│                    │         │                                      │
│              ┌─────┴─────────┴─────┐                                │
│              │   JUNCTION          │  ← Audio Mix Point             │
│              │   oapply = colimit  │    (Shared State)              │
│              └─────────────────────┘                                │
│                       │                                             │
│               ┌───────┴───────┐                                     │
│               │ OUTER PORTS   │  ← External I/O                     │
│               │ 🎙️ Record     │    (WhiteHole/NATS)                  │
│               │ 📡 Stream     │                                     │
│               └───────────────┘                                     │
│                                                                     │
│   GF(3) Conservation: (+1) + (0) + (-1) = 0 ✓                      │
└─────────────────────────────────────────────────────────────────────┘
```

## Categorical Mapping

| Voice Concept | UWD Concept | Categorical Role |
|---------------|-------------|------------------|
| Participant | Box | ResourceSharer with audio state |
| Speaking (+1) | Port out | Generative contribution |
| Listening (0) | Port in/out | Neutral transport |
| Muted (-1) | No contribution | Observation only |
| Audio Mix | Junction | Pushout gluing shared state |
| `oapply` | Composition | Colimit of audio streams |
| Play | Forward pass | Arena: Ω × X → Y |
| Coplay | Backward pass | Arena: Ω × X × R → ℧ × S |

## Core Components

### 1. VoiceChannelUWD.jl

Core undirected wiring diagram model:

```julia
using VoiceChannelUWD

# Create channel with 3 participants (GF(3) balanced)
channel = create_voice_uwd("room-1", ["alice", "bob", "charlie"])

# Compose audio via oapply (colimit)
mixed_audio = oapply_voice(channel)

# Arena play/coplay
play_result = voice_play(channel, "alice")
coplay_result = voice_coplay(channel, "alice", mixed_audio, feedback)
```

### 2. VoiceChannelNATS.jl

NATS message broker integration:

```julia
using VoiceChannelNATS

# Connect to NATS
client = NATSVoiceClient(channel, "alice")
connect!(client)

# Publish audio (play)
publish_audio(client, audio_frame)

# Subscribe to mixed audio (coplay)
subscribe_coplay!(client) do msg, feedback
    # Deliver to speakers
end
```

**NATS Topics:**
```
plurigrid.voice.{channel}.play.{participant}     # Outbound audio
plurigrid.voice.{channel}.coplay.{participant}   # Inbound mixed
plurigrid.voice.{channel}.peers                  # Peer discovery
plurigrid.voice.{channel}.meta                   # Channel metadata
```

### 3. VoiceChannelWhiteHole.jl

macOS virtual audio driver binding:

```julia
using VoiceChannelWhiteHole

# Create WhiteHole binding
binding = create_whitehole_binding(channel, "alice")

# Start audio I/O
start_input!(binding)   # Microphone → Channel
start_output!(binding)  # Channel → Speakers

# Color-tagged stream mixing
result = mix_colored_streams(streams)
```

**Stream Colors:**
- Hue 0-120°: PLUS (+1) speaking streams
- Hue 120-240°: ERGODIC (0) transport streams
- Hue 240-360°: MINUS (-1) monitoring streams

## GF(3) Trit Assignment

| State | Trit | Color | Meaning |
|-------|------|-------|---------|
| SPEAKING | +1 | `#D82626` (Red) | Generative - producing audio |
| LISTENING | 0 | `#26D826` (Green) | Ergodic - processing/routing |
| MUTED | -1 | `#2626D8` (Blue) | Observation - silent consume |

**Conservation Law:**
```
∀ channel: Σ participant.trit ≡ 0 (mod 3)
```

## Arena Protocol

From Capucci et al. "Parametrised Lenses":

```
Arena A_G : Lens_{(Ω,℧)}(X,S)(Y,R)

where:
  Ω = Π_{p∈P} {speaking, listening, muted}  (strategy profiles)
  ℧ = Π_{p∈P} ℝ                              (latency/quality)
  X = audio buffer states
  S = listening buffer costates
  Y = mixed audio output
  R = quality feedback

Play:   play_A : Ω × X → Y      (participant → channel)
Coplay: coplay_A : Ω × X × R → ℧ × S  (channel → participant)
```

## Commands

```bash
# Run voice session demo
julia plurigrid/VoiceChannelUWD.jl

# Run NATS-integrated session
julia plurigrid/VoiceChannelNATS.jl

# Run WhiteHole audio session
julia plurigrid/VoiceChannelWhiteHole.jl

# Create voice channel
just voice-channel create room-1 alice bob charlie

# Join voice channel
just voice-channel join room-1 --as alice

# Check GF(3) balance
just voice-channel gf3-check room-1
```

## Integration with Existing Skills

### unwiring-arena
```julia
# Voice channel uses same Play/Coplay protocol
using UnwiringArena

arena = VoiceArena(channel)
arena_step!(arena)  # Full play/coplay cycle
```

### oapply-colimit
```julia
# Audio mixing IS oapply
using AlgebraicDynamics

# Each participant is a ResourceSharer
participants = [ResourceSharer([:audio], produce_fn) for p in channel]

# Mix via colimit
mixed = oapply(voice_uwd, participants)
```

### gay-mcp
```julia
# Deterministic color assignment
using Gay

color = gay_color(participant.seed)
trit = color_to_trit(color)
```

## Mathematical Foundation

### Undirected Wiring Diagram

```
UWD = (B, J, π: P → J, ρ: P → B, O, o: O → J)

where:
  B = set of boxes (participants)
  J = set of junctions (mix points)
  P = set of ports (audio in/out)
  O = outer ports (external I/O)
```

### oapply as Colimit

```julia
function oapply(d::UndirectedWiringDiagram, xs::Vector{ResourceSharer})
    # 1. Coproduct of state spaces (all audio buffers)
    S = coproduct((FinSet ∘ nstates).(xs))
    
    # 2. Pushout identifies shared at junctions (audio mixing)
    S′ = pushout(portmap, junctions)
    
    # 3. Induced dynamics sum at junctions
    return ResourceSharer(induced_interface, sum_dynamics)
end
```

### GF(3) Conservation

```
For any voice channel with n participants:
  
  1. Assign trits: trit(pᵢ) ∈ {-1, 0, +1}
  2. Conservation: Σᵢ trit(pᵢ) ≡ 0 (mod 3)
  3. If n = 3k: assign k each of {-1, 0, +1}
  4. If n ≠ 3k: some participants must share trit
```

## GF(3) Triads

```
voice-channel-uwd (0) ⊗ gay-mcp (+1) ⊗ temporal-coalgebra (-1) = 0 ✓
voice-channel-uwd (0) ⊗ oapply-colimit (+1) ⊗ sheaf-cohomology (-1) = 0 ✓
unwiring-arena (0) ⊗ voice-channel-uwd (0) ⊗ bisimulation-game (0) = 0 ✓
```

## Example Session

```
═══════════════════════════════════════════════════════════════
  Voice Session via NATS + UWD
═══════════════════════════════════════════════════════════════

[1] Created voice channel: demo-room
    Participants: alice, bob, charlie

[2] Created NATS client for: alice

[3] Connected to NATS: nats://nonlocal.info:4222

[4] Announced presence

[5] Registered coplay callback

[6] Running play/coplay loop (9 frames):
    Frame 1: play=1, GF(3)=0 ✓
    Frame 2: play=1, GF(3)=0 ✓
    Frame 3: play=1, GF(3)=0 ✓
    ...

[7] Final GF(3) conservation check:
    Accumulator: 0
    Mod 3: 0
    Balanced: true

[8] Left channel

✓ Voice session complete
```

## References

- [Libkind "An Algebra of Resource Sharers"](https://arxiv.org/abs/2007.14442)
- [Capucci et al. "Parametrised Lenses"](https://arxiv.org/abs/2307.02540)
- [AlgebraicJulia/AlgebraicDynamics.jl](https://github.com/AlgebraicJulia/AlgebraicDynamics.jl)
- [plurigrid/UnwiringDiagrams.jl](https://github.com/plurigrid/UnwiringDiagrams.jl)
- [WhiteHole Audio Driver](https://github.com/ExistentialAudio/WhiteHole)

---

**Skill Name**: voice-channel-uwd  
**Type**: Real-time Communication / Compositional Audio  
**Trit**: 0 (ERGODIC)  
**Color**: `#26D826` (Green)  
**Principle**: Voice as categorical composition with GF(3) conservation



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Graph Theory
- **networkx** [○] via bicomodule
  - Universal graph hub

### Bibliography References

- `general`: 734 citations in bib.duckdb



## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 8. Degeneracy

**Concepts**: redundancy, fallback, multiple strategies, robustness

### GF(3) Balanced Triad

```
voice-channel-uwd (○) + SDF.Ch8 (−) + [balancer] (+) = 0
```

**Skill Trit**: 0 (ERGODIC - coordination)

### Secondary Chapters

- Ch3: Variations on an Arithmetic Theme
- Ch6: Layering
- Ch1: Flexibility through Abstraction
- Ch10: Adventure Game Example

### Connection Pattern

Degeneracy provides fallbacks. This skill offers redundant strategies.
## Cat# Integration

This skill maps to **Cat# = Comod(P)** as a bicomodule in the equipment structure:

```
Trit: 0 (ERGODIC)
Home: Prof
Poly Op: ⊗
Kan Role: Adj
Color: #26D826
```

### GF(3) Naturality

The skill participates in triads satisfying:
```
(-1) + (0) + (+1) ≡ 0 (mod 3)
```

This ensures compositional coherence in the Cat# equipment structure.