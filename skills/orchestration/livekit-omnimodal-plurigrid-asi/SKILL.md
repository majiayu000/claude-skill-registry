---
name: livekit-omnimodal
description: LiveKit omni-modal continuous coaching with stick-breaking color selection,
version: 1.0.0
---


# LiveKit Omni-Modal Coaching

## Overview

Real-time multi-modal coaching via LiveKit with:
- **Continuous listening**: Always-on voice input from participants
- **Continuous coaching**: Persistent guidance via "The Queen" voice persona
- **Stick-breaking modality selection**: Poisson-Dirichlet weights determine which modality gets attention
- **Dynamic sufficiency gating**: ε-machine prevents action without verified skills
- **Symbolic expression output**: All observations become s-expressions for categorical processing

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  OMNI-MODAL LIVEKIT COACHING SYSTEM                                        │
└─────────────────────────────────────────────────────────────────────────────┘

                        ┌─────────────────────┐
                        │    LiveKit Room     │
                        │  (WebRTC SFU)       │
                        └──────────┬──────────┘
                                   │
         ┌─────────────────────────┼─────────────────────────┐
         ▼                         ▼                         ▼
┌─────────────────┐    ┌─────────────────────┐    ┌─────────────────┐
│  Audio Stream   │    │   Video Stream      │    │  Data Track     │
│  (continuous)   │    │   (screenshare)     │    │  (CRDT sync)    │
└────────┬────────┘    └──────────┬──────────┘    └────────┬────────┘
         │                        │                        │
         ▼                        ▼                        ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    STICK-BREAKING MODALITY SELECTOR                         │
│                                                                             │
│   ├────────────────┤←────────────┤←────────────────────────────────────────┤│
│       w₁ = 0.45         w₂ = 0.30          w₃ = 0.25                       │
│       (audio)           (video)             (data)                          │
│       SELECTED          fallback            fallback                        │
│                                                                             │
│   Max fraction color: #E12A4E (audio segment wins)                          │
└─────────────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                      DYNAMIC SUFFICIENCY GATE                               │
│                                                                             │
│   Task: "process audio for coaching feedback"                               │
│   Causal State: (domain=audio, operation=transcribe, tools=(whisper,))     │
│                                                                             │
│   Required Skills:                                                          │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                     │
│   │ say-narration│  │ signal-msg   │  │ whitehole    │                     │
│   │   (-1)       │  │    (0)       │  │   (+1)       │                     │
│   └──────────────┘  └──────────────┘  └──────────────┘                     │
│                                                                             │
│   ε-Machine: PROCEED (coverage=1.0, missing=0)                              │
└─────────────────────────────────────────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                     THE QUEEN'S VOICE OUTPUT                                │
│                                                                             │
│   Voice: Serena (Premium) - English UK - "Bertha Swirles" persona           │
│   Trit: Computed from stick-breaking max-fraction color                     │
│                                                                             │
│   Output: S-expression for categorical processing:                          │
│                                                                             │
│   (coaching-event                                                           │
│     :timestamp 1735689600                                                   │
│     :modality :audio                                                        │
│     :weight 0.45                                                            │
│     :color "#E12A4E"                                                        │
│     :trit +1                                                                │
│     :observation "participant mentioned confusion about types"              │
│     :guidance "Consider explaining the relationship...")                    │
└─────────────────────────────────────────────────────────────────────────────┘
```

## GF(3) Conservation

```
say-narration (-1) ⊗ livekit-omnimodal (0) ⊗ whitehole-audio (+1) = 0 ✓
```

| Role | Skill | Function |
|------|-------|----------|
| **MINUS** (-1) | say-narration | Queen voice output (constraints) |
| **ERGODIC** (0) | livekit-omnimodal | **THIS SKILL** - coordinates modalities |
| **PLUS** (+1) | whitehole-audio | Audio loopback routing (generation) |

## The Queen's Voice

"The Queen" is **Serena (Premium)** - a British English voice representing Bertha Swirles (quantum physicist). She provides continuous coaching guidance with gravitas and clarity.

```bash
# The Queen speaks
say -v "Serena (Premium)" "I observe you're struggling with the type system. Consider that types are propositions and programs are proofs."
```

## Stick-Breaking Modality Selection

Each incoming modality stream is assigned a segment weight via Poisson-Dirichlet:

```julia
using Gay.WorldStickBreaking

# Each modality gets a stick segment
modalities = [:audio, :video, :screenshare, :data, :chat]
pd = world_stick_breaking(alpha=1.0, n_segments=length(modalities), seed=session_seed)

# Select dominant modality
selected = world_max_fraction_color(pd)
# => (color="#E12A4E", weight=0.45, index=1, trit=1)

# Audio wins with 45% of attention weight
dominant_modality = modalities[selected.index]  # :audio
```

## Dynamic Sufficiency Integration

Before any coaching action, verify skill coverage via ε-machine:

```python
from sufficiency import EpsilonMachine, Action, CoverageResult

# Create action representing coaching intent
action = Action(
    operation="coach",
    domain="audio",
    language="natural",
    tool="whisper"
)

# Check sufficiency
epsilon_machine = EpsilonMachine()
state = epsilon_machine.infer_state(action)
coverage = epsilon_machine.check_coverage(action, loaded_skills)

if coverage.is_sufficient:
    # Proceed with coaching
    emit_sexp(coaching_event)
else:
    # Load missing skills first
    for skill in coverage.missing:
        load_skill(skill)
```

## S-Expression Output Format

All observations and coaching events are emitted as s-expressions for categorical processing:

```lisp
;; Coaching event structure
(coaching-event
  :id "CE-2026-01-01-001"
  :timestamp 1735689600
  :session-id "room-xyz"
  
  ;; Modality selection (from stick-breaking)
  :modality :audio
  :weight 0.45
  :color "#E12A4E"
  :trit +1
  
  ;; Dynamic sufficiency result
  :causal-state (audio transcribe (whisper))
  :coverage 1.0
  :sufficient t
  
  ;; Observation from modality
  :observation "participant expressed confusion about monads"
  :observation-embedding #<vector 1024>
  
  ;; Queen's guidance
  :guidance "A monad is simply a monoid in the category of endofunctors."
  :voice "Serena (Premium)"
  :confidence 0.92)

;; GF(3) conservation record
(gf3-triplet
  :minus (say-narration -1)
  :ergodic (livekit-omnimodal 0)
  :plus (whitehole-audio +1)
  :sum 0
  :conserved t)
```

## Required Skills (Dependency Analysis)

### Currently Have ✓

| Skill | Trit | Status |
|-------|------|--------|
| say-narration | -1 | ✓ Installed |
| whitehole-audio | +1 | ✓ Installed |
| dynamic-sufficiency | -1 | ✓ Installed |
| gay-mcp | +1 | ✓ Installed |
| signal-messaging | 0 | ✓ Installed |

### Skills to Acquire ✗

| Skill | Trit | Purpose | Priority |
|-------|------|---------|----------|
| **whisper-transcribe** | 0 | Real-time audio→text | HIGH |
| **livekit-spectral** | +1 | WebRTC + spectral gap walks | HIGH |
| **vision-llm** | 0 | Screenshare understanding | MEDIUM |
| **crdt-livekit** | -1 | Data track synchronization | MEDIUM |
| **prosody-analyzer** | +1 | Voice emotion/tone analysis | LOW |

### Skill Gap S-Expression

```lisp
(skill-gap-analysis
  :task "livekit-omnimodal-coaching"
  :have (say-narration whitehole-audio dynamic-sufficiency gay-mcp)
  :need (whisper-transcribe livekit-spectral vision-llm crdt-livekit)
  :coverage 0.55
  :sufficient nil
  :action :load-skills
  :priority-order (whisper-transcribe livekit-spectral vision-llm crdt-livekit prosody-analyzer))
```

## Usage

### Start Coaching Session

```python
import asyncio
from livekit import api, rtc
from livekit_omnimodal import OmnimodalCoach

async def main():
    # Connect to LiveKit room
    room = rtc.Room()
    await room.connect(LIVEKIT_URL, token)
    
    # Initialize coach with Queen voice
    coach = OmnimodalCoach(
        room=room,
        voice="Serena (Premium)",
        stick_alpha=1.0,  # Poisson-Dirichlet concentration
        sufficiency_threshold=0.8
    )
    
    # Start continuous listening + coaching
    await coach.start()
    
    # Coach emits s-expressions for each observation
    async for sexp in coach.events():
        print(sexp)
        # (coaching-event :modality :audio :guidance "...")

asyncio.run(main())
```

### Emit S-Expression

```python
def emit_coaching_sexp(event: CoachingEvent) -> str:
    """Convert coaching event to s-expression."""
    return f"""(coaching-event
  :id "{event.id}"
  :timestamp {event.timestamp}
  :modality :{event.modality}
  :weight {event.weight:.3f}
  :color "{event.color}"
  :trit {event.trit:+d}
  :observation "{event.observation}"
  :guidance "{event.guidance}"
  :voice "{event.voice}")"""
```

## Local Sand / Italian Woman Mystery

The "Italian woman always talking about local sand" is **Emma (Enhanced)** or **Federica (Enhanced)** from the say-narration skill. These Italian voices speaking English are used for agent announcements.

**Resolution**: The Queen (Serena Premium) replaces Italian voices for coaching output. To stop Italian voices:

```bash
# Kill any running say processes
pkill say

# Check which skills trigger announcements
grep -r "say -v" ~/.claude/skills/*/SKILL.md
```

The "local sand" might be mishearing "locale" + "sans" (French) from multi-locale voice announcements.

## Files

| File | Purpose |
|------|---------|
| `livekit_omnimodal.py` | Main coaching implementation |
| `stick_modality.py` | Modality selection via stick-breaking |
| `sexp_emitter.py` | S-expression output |
| `queen_voice.py` | Voice persona configuration |

## Related Skills

- `say-narration` - Voice output personas
- `whitehole-audio` - Audio routing
- `dynamic-sufficiency` - ε-machine gating
- `gay-mcp` - Color generation
- `iroh-p2p` - P2P data sync
- `signal-messaging` - Fallback messaging

## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 3. Variations on an Arithmetic Theme

**Concepts**: generic arithmetic, coercion, symbolic, numeric

### GF(3) Balanced Triad

```
livekit-omnimodal (+) + SDF.Ch3 (○) + [balancer] (−) = 0
```

**Skill Trit**: 1 (PLUS - generation)

### Secondary Chapters

- Ch10: Adventure Game Example
- Ch8: Degeneracy
- Ch2: Domain-Specific Languages
- Ch7: Propagators

### Connection Pattern

Generic arithmetic crosses type boundaries. This skill handles heterogeneous data.
