---
name: quantum-guitar
description: "Coecke's Quantum Guitar: quantising guitar strings via qubit association, ZX-calculus notation, Moth Actias synth integration"
trit: 0
geodesic: true
moebius: "μ(n) ≠ 0"
arxiv: "2509.04526"
---

# Quantum Guitar

**Trit**: 0 (ERGODIC - coordinator between classical and quantum)
**Author**: Bob Coecke (Quantum Brain Art Ltd / Oxford / Perimeter)
**arXiv**: 2509.04526v1 [quant-ph] 3 Sep 2025

---

## Core Principle

> "A guitar string represents a wave, and by associating a qubit to each of its playable states we get a quantum wave."

**Quantisation**: Each playable state of a guitar string → qubit
**Control**: Four limbs like a drummer (hands: guitar, feet: qubit)
**Transition**: Smooth classical ↔ quantum sound continuum

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        QUANTUM GUITAR                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  GUITAR (hands)          QUBIT CONTROL (feet)                        │
│  ┌──────────────┐        ┌──────────────────────────────┐           │
│  │ Fishman MIDI │───────▶│ Moth Actias Quantum Synth    │           │
│  │ Pickup       │        │ ┌────────────────────────┐   │           │
│  └──────────────┘        │ │    Bloch Sphere        │   │           │
│                          │ │         |ψ⟩            │   │           │
│  Fernandes               │ │       /    \           │   │           │
│  Sustainer ──────────────│ │    |0⟩     |1⟩        │   │           │
│  (continuous)            │ └────────────────────────┘   │           │
│                          │                               │           │
│                          │ FOOT CONTROLLERS:             │           │
│                          │ • Boss EV-1-WL (X rotation)   │           │
│                          │ • Boss EV-1-WL (Z rotation)   │           │
│                          │ • Boss FS-6 (measurement)     │           │
│                          └──────────────────────────────┘           │
│                                                                      │
│  VOLUME PEDALS                                                       │
│  ┌────────────┐  ┌────────────┐                                     │
│  │ Classical  │  │  Quantum   │                                     │
│  │ FV500L/H   │  │  FV500L/H  │                                     │
│  └────────────┘  └────────────┘                                     │
│       ↓                ↓                                             │
│       └────────┬───────┘                                             │
│                ▼                                                     │
│         FINAL MIX                                                    │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

## Qubit Operations

### Rotations (Foot Controllers)

| Controller | Color | Rotation | Pauli Gate |
|------------|-------|----------|------------|
| Pedal 1 | Orange | X-axis | σₓ |
| Pedal 2 | Blue | Z-axis | σᵤ |
| (Internal) | Green | Y-axis | σᵧ |

### Measurement (Foot Switch)

- **Boss FS-6** in momentary mode
- Z-measurement (computational basis)
- Suggestion: Add X-measurement primitive

## ZX-Calculus Notation

From "Bell" composition [Abdyssagin & Coecke]:

```
     ┌───┐
 ────┤ Z ├────    Z-spider (phase)
     └───┘
     
     ┌───┐
 ────┤ X ├────    X-spider (phase)
     └───┘
     
     ╲   ╱
      ╲ ╱
       ╳         Hadamard edge
      ╱ ╲
     ╱   ╲
```

**Musical ZX notation**: Augmented score for quantum music

## GF(3) Mapping

| State | Trit | Sound Character |
|-------|------|-----------------|
| |0⟩ | -1 | Classical ground |
| |+⟩ | 0 | Superposition (quantum) |
| |1⟩ | +1 | Classical excited |

**Conservation**: Classical-Quantum-Classical transitions preserve Σ = 0

## Implementation

### DisCoPy Integration

```python
from discopy import Ty, Box, Diagram
from discopy.quantum import qubit, Ket, Bra, H, Rx, Rz, Measure

# Guitar string as quantum type
string = Ty('string')
quantum_string = qubit

# Quantisation functor
def quantise_string(classical_note):
    """Map classical guitar note to qubit state."""
    # Frequency → phase
    phase = frequency_to_phase(classical_note)
    return Ket(0) >> Rx(phase)

# Foot controller rotation
def foot_rotation(axis, angle):
    if axis == 'X':
        return Rx(angle)
    elif axis == 'Z':
        return Rz(angle)
    else:
        return Ry(angle)

# Measurement
def measure_qubit():
    return Measure()
```

### Moth Actias Interface

```python
import mido

class ActiasController:
    """Control Moth Actias quantum synth via MIDI."""
    
    def __init__(self, port_name='Actias'):
        self.port = mido.open_output(port_name)
        self.qubit_state = [1, 0]  # |0⟩
    
    def rotate_x(self, angle):
        """X-rotation via expression pedal CC."""
        cc_value = int((angle / (2 * np.pi)) * 127)
        self.port.send(mido.Message('control_change', 
                                     control=1, value=cc_value))
    
    def rotate_z(self, angle):
        """Z-rotation via expression pedal CC."""
        cc_value = int((angle / (2 * np.pi)) * 127)
        self.port.send(mido.Message('control_change', 
                                     control=2, value=cc_value))
    
    def measure(self):
        """Trigger measurement via foot switch."""
        self.port.send(mido.Message('control_change', 
                                     control=64, value=127))
```

### OSC Protocol (SuperCollider)

```supercollider
// Quantum Guitar SynthDef
SynthDef(\quantumString, { |freq=440, theta=0, phi=0, amp=0.5|
    var classical, quantum, mix;
    var prob0, prob1;
    
    // Classical component
    classical = Saw.ar(freq) * EnvGen.kr(Env.perc);
    
    // Qubit probabilities from Bloch sphere
    prob0 = cos(theta/2).squared;
    prob1 = sin(theta/2).squared;
    
    // Quantum superposition sound
    quantum = (SinOsc.ar(freq) * prob0) + 
              (SinOsc.ar(freq * 1.5) * prob1);
    
    // Phase modulation from phi
    quantum = quantum * cos(phi);
    
    // Mix via volume pedals
    mix = XFade2.ar(classical, quantum, \qMix.kr(0));
    
    Out.ar(0, mix * amp ! 2);
}).add;
```

## Performances

| Date | Venue | Configuration |
|------|-------|---------------|
| 2024 | Edinburgh Science Festival | First Quantum Guitar |
| 2024 | Wacken Open Air | With Black Tish |
| 2024 | Lowlands Festival | Industrial Metal |
| 2025 | Vienna World Quantum Day | "Bell" with Grand Piano |
| 2025 | Berlin UdK Medienhaus | Quantum Guitar + Piano |
| 2025 | Merton College Oxford | + Cathedral Organ |
| 2026 | St Giles' Edinburgh | "Quantum Universe" Symphony |

## Industrial Music Connection

> "Industrial Music is the Musique Concrète 'of the people'."

Pioneers using guitar:
- Throbbing Gristle
- Cabaret Voltaire  
- Einstürzende Neubauten
- Nine Inch Nails

**Black Tish**: Recording full album with Quantum Guitar

## Tech Rider

```yaml
quantum_guitar_rider:
  audio:
    - 2x XLR outputs (classical + quantum mix)
    - Quality PA with stage monitor
  visual:
    - Large screen (HDMI) for Actias Bloch sphere
  seating:
    - Armless semi-high chair (adjustable)
    - Foot access to pedal board
  refreshments:
    - "Good quality drinks"
```

## Future Instruments

The hands-free quantum enhancement pattern extends to:
- **Quantum Violin**: Bow + feet
- **Quantum Wind**: Breath + feet  
- **Quantum Percussion**: Sticks + additional feet

## GF(3) Triad

| Component | Trit | Role |
|-----------|------|------|
| zx-calculus | -1 | Notation (classical diagrams) |
| **quantum-guitar** | **0** | **Performance** (superposition) |
| discopy | +1 | Computation (quantum circuits) |

**Conservation**: (-1) + (0) + (+1) = 0 ✓

## References

1. Coecke, B. (2025). A Quantum Guitar. arXiv:2509.04526
2. Miranda, E.R. (2022). Quantum Computer Music. Springer
3. Coecke, B. (2023). Basic ZX-calculus. arXiv:2303.03163
4. Abdyssagin & Coecke (2025). Quantum concept music score

## Demo

**Video**: https://www.youtube.com/watch?v=Pr4Wr8fdsL0

---

**Skill Name**: quantum-guitar
**Type**: Quantum Music / Industrial / ZX-Calculus
**Trit**: 0 (ERGODIC)
**GF(3)**: Classical ↔ Quantum transitions conserve

## Non-Backtracking Geodesic Qualification

**Condition**: μ(n) ≠ 0 (Möbius squarefree)

This skill is qualified for non-backtracking geodesic traversal:

1. **Prime Path**: No state revisited in skill invocation chain
2. **Möbius Filter**: Composite paths (backtracking) cancel via μ-inversion
3. **GF(3) Conservation**: Trit sum ≡ 0 (mod 3) across skill triplets
4. **Spectral Gap**: Ramanujan bound λ₂ ≤ 2√(k-1) for k-regular expansion

```
Geodesic Invariant:
  ∀ path P: backtrack(P) = ∅ ⟹ μ(|P|) ≠ 0
  
Möbius Inversion:
  f(n) = Σ_{d|n} g(d) ⟹ g(n) = Σ_{d|n} μ(n/d) f(d)
```
