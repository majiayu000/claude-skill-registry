---
name: generative-music-composer
description: Creates algorithmic music composition systems using procedural generation, Markov chains, L-systems, and neural approaches for ambient, adaptive, and experimental music.
license: MIT
---

# Generative Music Composer

This skill provides guidance for creating algorithmic and procedural music systems that generate compositions autonomously or semi-autonomously.

## Core Competencies

- **Algorithmic Composition**: Rule-based music generation
- **Stochastic Methods**: Markov chains, probability distributions
- **Formal Grammars**: L-systems, generative grammars for music
- **Adaptive Systems**: Music that responds to input/context
- **Neural Approaches**: ML-based generation techniques

## Generative Music Fundamentals

### Generation Paradigms

| Approach | Description | Best For |
|----------|-------------|----------|
| Rule-based | Explicit compositional rules | Traditional styles, controlled output |
| Stochastic | Probability-driven selection | Natural variation, surprise |
| Grammar-based | Recursive structure generation | Complex forms, self-similarity |
| Constraint-based | Satisfy musical constraints | Harmony, voice leading |
| Learning-based | Train on corpus | Style imitation, novelty |

### Musical Elements to Generate

```
┌─────────────────────────────────────────────────────────┐
│                    Music Generation Layers              │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Macro Structure    │ Form, sections, key areas         │
│  ──────────────────────────────────────────────────────│
│  Harmony            │ Chord progressions, voice leading │
│  ──────────────────────────────────────────────────────│
│  Melody             │ Pitch sequences, contour, rhythm  │
│  ──────────────────────────────────────────────────────│
│  Rhythm             │ Duration patterns, meter, groove  │
│  ──────────────────────────────────────────────────────│
│  Timbre/Texture     │ Instrumentation, dynamics         │
│  ──────────────────────────────────────────────────────│
│  Micro Variation    │ Ornaments, expression, humanize   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Stochastic Generation

### Markov Chain Melody

```python
import random
from collections import defaultdict

class MarkovMelodyGenerator:
    """Generate melodies using Markov chains"""

    def __init__(self, order=2):
        self.order = order
        self.transitions = defaultdict(list)

    def train(self, melodies):
        """Learn from existing melodies (lists of MIDI notes)"""
        for melody in melodies:
            for i in range(len(melody) - self.order):
                state = tuple(melody[i:i + self.order])
                next_note = melody[i + self.order]
                self.transitions[state].append(next_note)

    def generate(self, length, seed=None):
        """Generate a new melody"""
        if seed is None:
            seed = random.choice(list(self.transitions.keys()))

        melody = list(seed)

        for _ in range(length - self.order):
            state = tuple(melody[-self.order:])
            if state in self.transitions:
                next_note = random.choice(self.transitions[state])
            else:
                # Fallback: random from all possible next notes
                next_note = random.choice(
                    [n for notes in self.transitions.values() for n in notes]
                )
            melody.append(next_note)

        return melody
```

### Weighted Random Selection

```python
def weighted_choice(options, weights):
    """Select with custom probability distribution"""
    total = sum(weights)
    r = random.uniform(0, total)
    cumulative = 0
    for option, weight in zip(options, weights):
        cumulative += weight
        if r <= cumulative:
            return option
    return options[-1]

# Scale degree probabilities (tendency tones)
scale_weights = {
    1: 0.20,  # Tonic - stable, common
    2: 0.10,  # Supertonic - passing
    3: 0.15,  # Mediant - stable
    4: 0.10,  # Subdominant - tendency to 3
    5: 0.20,  # Dominant - stable
    6: 0.10,  # Submediant - relative major/minor
    7: 0.05,  # Leading tone - strong tendency
    8: 0.10   # Octave
}

def generate_scale_melody(length, key='C', scale='major'):
    degrees = list(scale_weights.keys())
    weights = list(scale_weights.values())
    melody = [weighted_choice(degrees, weights) for _ in range(length)]
    return [degree_to_midi(d, key, scale) for d in melody]
```

## Grammar-Based Generation

### L-System for Musical Structure

```python
class MusicalLSystem:
    """L-system for generating musical phrases"""

    def __init__(self):
        self.rules = {
            'A': 'AB',    # Antecedent expands to Antecedent + Bridge
            'B': 'CA',    # Bridge expands to Consequent + Antecedent
            'C': 'DC',    # Consequent expands to Development + Consequent
            'D': 'A'      # Development returns to Antecedent
        }
        self.interpretations = {
            'A': self._phrase_a,
            'B': self._phrase_b,
            'C': self._phrase_c,
            'D': self._phrase_d
        }

    def generate_structure(self, axiom='A', iterations=4):
        """Generate formal structure"""
        result = axiom
        for _ in range(iterations):
            result = ''.join(self.rules.get(c, c) for c in result)
        return result

    def realize(self, structure):
        """Convert structure to musical phrases"""
        phrases = []
        for symbol in structure:
            if symbol in self.interpretations:
                phrases.append(self.interpretations[symbol]())
        return phrases

    def _phrase_a(self):
        # Antecedent: tension-building phrase
        return generate_phrase(contour='ascending', cadence='half')

    def _phrase_b(self):
        # Bridge: transitional material
        return generate_phrase(contour='static', cadence='deceptive')

    def _phrase_c(self):
        # Consequent: resolution phrase
        return generate_phrase(contour='descending', cadence='authentic')

    def _phrase_d(self):
        # Development: variation material
        return generate_phrase(contour='varied', cadence='half')
```

### Generative Grammar for Rhythm

```python
class RhythmGrammar:
    """Context-free grammar for rhythm generation"""

    def __init__(self):
        # Non-terminal symbols with production rules
        self.rules = {
            'MEASURE': [
                ['HALF', 'HALF'],
                ['QUARTER', 'QUARTER', 'QUARTER', 'QUARTER'],
                ['DOTTED_HALF', 'QUARTER'],
                ['BEAT', 'BEAT', 'BEAT', 'BEAT']
            ],
            'HALF': [
                ['QUARTER', 'QUARTER'],
                ['half']
            ],
            'QUARTER': [
                ['EIGHTH', 'EIGHTH'],
                ['quarter'],
                ['SIXTEENTH', 'SIXTEENTH', 'EIGHTH']
            ],
            'BEAT': [
                ['quarter'],
                ['EIGHTH', 'EIGHTH'],
                ['TRIPLET']
            ],
            'EIGHTH': [
                ['eighth'],
                ['SIXTEENTH', 'SIXTEENTH']
            ],
            'TRIPLET': [
                ['triplet', 'triplet', 'triplet']
            ],
            'SIXTEENTH': [
                ['sixteenth']
            ]
        }

    def generate(self, symbol='MEASURE'):
        """Recursively expand grammar"""
        if symbol not in self.rules:
            return [symbol]  # Terminal symbol

        # Choose random production rule
        production = random.choice(self.rules[symbol])

        result = []
        for s in production:
            result.extend(self.generate(s))

        return result
```

## Constraint-Based Harmony

### Voice Leading Rules

```python
class HarmonyGenerator:
    """Generate chord progressions with voice leading constraints"""

    def __init__(self, key='C', mode='major'):
        self.key = key
        self.mode = mode
        self.chord_vocabulary = self._build_chords()

    def generate_progression(self, length=8):
        """Generate progression satisfying constraints"""
        progression = [self._tonic_chord()]  # Start on tonic

        for _ in range(length - 2):
            current = progression[-1]
            candidates = self._valid_next_chords(current)
            next_chord = self._select_chord(candidates, current)
            progression.append(next_chord)

        # End with cadence
        progression.append(self._dominant_chord())
        progression.append(self._tonic_chord())

        return progression

    def _valid_next_chords(self, current):
        """Filter chords by voice leading constraints"""
        candidates = []
        for chord in self.chord_vocabulary:
            if self._check_voice_leading(current, chord):
                candidates.append(chord)
        return candidates

    def _check_voice_leading(self, chord1, chord2):
        """Check voice leading rules"""
        # No parallel fifths
        if self._has_parallel_fifths(chord1, chord2):
            return False
        # No parallel octaves
        if self._has_parallel_octaves(chord1, chord2):
            return False
        # Resolve tendency tones
        if not self._resolves_tendencies(chord1, chord2):
            return False
        # Limit voice movement
        if self._excessive_movement(chord1, chord2):
            return False
        return True
```

### Functional Harmony

```python
# Chord function probabilities
PROGRESSION_TENDENCIES = {
    'I':   {'IV': 0.3, 'V': 0.3, 'vi': 0.2, 'ii': 0.1, 'iii': 0.1},
    'ii':  {'V': 0.7, 'vii': 0.2, 'IV': 0.1},
    'iii': {'vi': 0.4, 'IV': 0.3, 'ii': 0.2, 'I': 0.1},
    'IV':  {'V': 0.4, 'I': 0.2, 'ii': 0.2, 'vii': 0.1, 'vi': 0.1},
    'V':   {'I': 0.6, 'vi': 0.3, 'IV': 0.1},
    'vi':  {'IV': 0.3, 'ii': 0.3, 'V': 0.2, 'I': 0.1, 'iii': 0.1},
    'vii': {'I': 0.5, 'iii': 0.3, 'vi': 0.2}
}

def generate_functional_progression(length):
    progression = ['I']
    for _ in range(length - 1):
        current = progression[-1]
        tendencies = PROGRESSION_TENDENCIES[current]
        next_chord = weighted_choice(
            list(tendencies.keys()),
            list(tendencies.values())
        )
        progression.append(next_chord)
    return progression
```

## Adaptive and Interactive Music

### Parameter-Driven Generation

```python
class AdaptiveComposer:
    """Music that responds to external parameters"""

    def __init__(self):
        self.parameters = {
            'energy': 0.5,      # 0-1: calm to intense
            'tension': 0.5,     # 0-1: consonant to dissonant
            'density': 0.5,     # 0-1: sparse to dense
            'tempo_factor': 1.0 # Tempo multiplier
        }

    def update_parameter(self, name, value):
        self.parameters[name] = max(0, min(1, value))

    def generate_measure(self):
        """Generate music adapted to current parameters"""
        energy = self.parameters['energy']
        tension = self.parameters['tension']
        density = self.parameters['density']

        # Adapt musical elements
        note_density = int(4 + density * 12)  # 4-16 notes
        velocity_range = (40 + int(energy * 40), 80 + int(energy * 47))

        # Tension affects harmony
        if tension < 0.3:
            chord_pool = ['I', 'IV', 'V', 'vi']  # Consonant
        elif tension < 0.7:
            chord_pool = ['ii', 'iii', 'IV', 'V', 'vi']  # Mixed
        else:
            chord_pool = ['ii', 'vii', 'V7', 'bVII', 'iv']  # Tense

        # Generate with adapted parameters
        return self._generate_notes(
            density=note_density,
            velocity_range=velocity_range,
            harmonic_pool=chord_pool
        )
```

### Game Audio Adaptive System

```python
class GameMusicSystem:
    """Layered adaptive music for games"""

    def __init__(self):
        self.layers = {
            'ambient': {'volume': 1.0, 'active': True},
            'percussion': {'volume': 0.0, 'active': False},
            'melody': {'volume': 0.0, 'active': False},
            'intensity': {'volume': 0.0, 'active': False}
        }
        self.current_state = 'exploration'

    def set_game_state(self, state, transition_time=2.0):
        """Crossfade layers based on game state"""
        presets = {
            'exploration': {
                'ambient': 1.0, 'percussion': 0.0,
                'melody': 0.3, 'intensity': 0.0
            },
            'tension': {
                'ambient': 0.7, 'percussion': 0.3,
                'melody': 0.5, 'intensity': 0.3
            },
            'combat': {
                'ambient': 0.3, 'percussion': 1.0,
                'melody': 0.7, 'intensity': 1.0
            },
            'victory': {
                'ambient': 0.5, 'percussion': 0.5,
                'melody': 1.0, 'intensity': 0.0
            }
        }

        target = presets.get(state, presets['exploration'])
        self._crossfade_to(target, transition_time)
        self.current_state = state
```

## Output Formats

### MIDI Generation

```python
from midiutil import MIDIFile

def create_midi(melody, filename='output.mid', tempo=120):
    """Export melody to MIDI file"""
    midi = MIDIFile(1)  # One track
    track = 0
    channel = 0
    time = 0
    volume = 100

    midi.addTempo(track, 0, tempo)

    for note in melody:
        pitch = note['pitch']
        duration = note['duration']
        midi.addNote(track, channel, pitch, time, duration, volume)
        time += duration

    with open(filename, 'wb') as f:
        midi.writeFile(f)
```

## Best Practices

### Musical Coherence

1. **Repetition with variation**: Repeat themes but vary them
2. **Motivic development**: Transform small ideas
3. **Hierarchical structure**: Phrases → sections → movements
4. **Tension and release**: Build and resolve over time

### Avoiding Common Pitfalls

- Pure randomness sounds chaotic—add constraints
- Too many rules sound mechanical—add stochastic variation
- Test with actual audio, not just data
- Consider performance/playability

## References

- `references/music-theory-primer.md` - Essential music theory for generation
- `references/markov-music.md` - Advanced Markov chain techniques
- `references/midi-reference.md` - MIDI specification and libraries
