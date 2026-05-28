---
name: whitehole-audio
description: Modern macOS + tripos audio loopback driver for inter-application audio
version: 1.0.0
---


# WhiteHole - Zero-Latency Audio Loopback

Modern macOS + tripos audio loopback driver for inter-application audio routing with minimal latency.

## Repository
- **Source**: https://github.com/bmorphism/WhiteHole
- **Language**: C (CoreAudio driver)
- **Platform**: macOS (AudioServerPlugin)

## Core Concept

WhiteHole creates virtual audio devices that pass audio between applications with "hex color #000000 latency" - effectively zero perceptible delay.

```
┌─────────────┐     WhiteHole     ┌─────────────┐
│   DAW       │ ───────────────▶  │   Streamer  │
│ (Ableton)   │   virtual device  │   (OBS)     │
└─────────────┘                   └─────────────┘
```

## Installation

```bash
# Clone and build
git clone https://github.com/bmorphism/WhiteHole
cd WhiteHole
xcodebuild -project WhiteHole.xcodeproj

# Install driver
sudo cp -R build/Release/WhiteHole.driver /Library/Audio/Plug-Ins/HAL/
sudo launchctl kickstart -kp system/com.apple.audio.coreaudiod
```

## Integration with Gay.jl Colors

WhiteHole devices can be color-coded using Gay.jl deterministic colors:

```julia
using Gay

# Assign deterministic color to audio channel
channel_seed = hash("WhiteHole:Channel1")
channel_color = gay_color(channel_seed)  # e.g., LCH(72, 45, 280)
```

## Use Cases

1. **Multi-app audio routing** - Route DAW output to streaming software
2. **Audio analysis** - Tap system audio for visualization
3. **Virtual soundcards** - Create multiple virtual devices
4. **music-topos integration** - Route SuperCollider to analysis tools

## Tripos Integration

The "tripos" in the description refers to the three-way (GF(3)) audio routing:

| Channel | GF(3) Trit | Purpose |
|---------|------------|---------|
| Left | MINUS | Primary signal |
| Right | PLUS | Secondary signal |
| Center | ERGODIC | Mixed/balanced |

## Related Skills
- `gay-mcp` - Color assignment for devices
- `rubato-composer` - Mazzola's music theory integration
- `algorithmic-art` - Audio-reactive visuals



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Graph Theory
- **networkx** [○] via bicomodule
  - Universal graph hub

### Bibliography References

- `general`: 734 citations in bib.duckdb

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