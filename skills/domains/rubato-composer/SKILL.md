---
name: rubato-composer
description: Rubato Composer integration for Mazzola's mathematical music theory
---

# rubato-composer - Mazzola's Mathematical Music Theory in Code

## Overview

Integrates [Rubato Composer](https://github.com/rubato-composer/rubato-composer) - Gérard Milmeister's Java implementation of Guerino Mazzola's mathematical music theory. The software embodies the Topos of Music framework with Forms, Denotators, and a Scheme interpreter.

## The Yoneda Package

Rubato Composer implements 40 classes in `org.rubato.math.yoneda`:

```
Core Structures:
├── Form.java              - Abstract base for musical types
├── Denotator.java         - Musical objects (notes, chords, scores)
├── Morphism.java          - Transformations between forms
├── MorphismMap.java       - Functorial mappings
│
├── LimitForm.java         - Categorical limits (product types)
├── ColimitForm.java       - Categorical colimits (sum types)
├── ListForm.java          - Sequence types
├── NameForm.java          - Named reference types
│
├── LimitDenotator.java    - Instances of limit forms
├── ColimitDenotator.java  - Instances of colimit forms
├── ListDenotator.java     - Sequences of denotators
└── Diagram.java           - Categorical diagrams
```

## Scheme Integration

Rubato includes a full Scheme interpreter with musical primitives:

```java
// From org.rubato.scheme
SDenotator.java  - Denotators as Scheme values
SForm.java       - Forms as Scheme values
SExpr.java       - S-expression base class
Parser.java      - Scheme parser
RubatoPrimitives.java - Musical operations
```

### Denotator as S-Expression

```scheme
;; In Rubato's Scheme dialect
(define note (make-denotator "Note" pitch-form 60))
(define chord (make-list-denotator "Chord" (list note1 note2 note3)))

;; Morphism application
(apply-morphism transposition chord 7)
```

## Bridge to music-topos

### Form ↔ ACSet Schema

```julia
# Our ACSets correspond to Rubato Forms
@present SchNote(FreeSchema) begin
    Pitch::Ob
    Duration::Ob
    Onset::Ob
    Note::Ob
    pitch::Hom(Note, Pitch)
    duration::Hom(Note, Duration)
    onset::Hom(Note, Onset)
end

# Rubato equivalent:
# LimitForm("Note", [pitchForm, durationForm, onsetForm])
```

### Denotator ↔ ACSet Instance

```julia
# ACSet instance = Denotator
note_acset = @acset Note begin
    Pitch = [60, 64, 67]
    Duration = [1.0, 1.0, 1.0]
    Onset = [0.0, 0.0, 0.0]
    Note = [1, 2, 3]
    pitch = [1, 2, 3]
    duration = [1, 2, 3]
    onset = [1, 2, 3]
end
```

### Morphism ↔ ACSet Homomorphism

```julia
# Transposition as ACSet morphism
function transpose(notes::ACSet, semitones::Int)
    map_parts(notes, :Pitch) do p
        p + semitones
    end
end
```

## Rubato Rubettes

Rubato's plugin system (Rubettes) maps to our skills:

| Rubette | music-topos Equivalent | Description |
|---------|------------------------|-------------|
| ScorePlay | sonic_pi_renderer.rb | Score playback |
| BigBang | maximum_dynamism.rb | Gestural composition (MVC) |
| MetroRubette | Free Monad patterns | Metric structure |
| WallpaperRubette | gay_neverending.rb | Morphism-based tiling |
| MeloRubette | skill_sonification.rb | Melodic analysis |

### BigBangRubette (from source)
```java
// BigBangRubette.java - Gestural composition
BigBangModel model;        // Composition state
BigBangController controller;  // User interaction
BigBangSwingView view;     // Visualization
// → maps to MaximumDynamism::DerangementConfig
```

### WallpaperRubette (from source)
```java
// WallpaperRubette.java - Florian Thalmann
// Creates wallpapers using morphisms applied to power denotators
List<ModuleMorphism> morphisms;
PowerDenotator output = getUnitedMappedDenotators(input, morphisms);
// → maps to GayNeverending color spiral
```

## Installation

```bash
# Clone (already done)
cd ~/worlds/o
gh repo clone rubato-composer/rubato-composer

# Build
cd rubato-composer
ant

# Run
java -jar rubato.jar
```

## Connecting to Our Stack

### Rubato → SuperCollider

Rubato can export to MIDI, which SuperCollider can receive:

```clojure
;; In Overtone/our stack
(def rubato-midi (midi-in "Rubato"))

(on-event [:midi :note-on]
  (fn [e]
    (play-note (:note e) (:velocity e)))
  ::rubato-handler)
```

### Rubato → Sonic Pi

Export Rubato scores to OSC:

```ruby
# sonic_pi_rubato_bridge.rb
require 'osc-ruby'

client = OSC::Client.new('localhost', 4560)

def play_rubato_score(denotators)
  denotators.each do |d|
    client.send(OSC::Message.new('/trigger/synth',
      d[:pitch], d[:duration], d[:onset]))
  end
end
```

## TAP State Mapping

| Rubato State | TAP | Color |
|--------------|-----|-------|
| Composing | LIVE (+1) | Red |
| Analyzing | VERIFY (0) | Green |
| Archived | BACKFILL (-1) | Blue |

## Mazzola's Core Concepts in Code

### The Topos Structure

```
TOPOS(Music) = Presheaves over Form Category

Forms = Objects (types)
Denotators = Generalized elements (instances)
Morphisms = Natural transformations
```

### Rubato Formula (from Vol. II)

```
Performance = Score × Tempo × Dynamics × Articulation

Where:
  Tempo: ℝ⁺ → ℝ⁺ (time deformation)
  Dynamics: ℝ → [0,1] (amplitude envelope)
  Articulation: [0,1] (attack/release shaping)
```

## Commands

```bash
just rubato-build        # Build Rubato Composer
just rubato-run          # Launch GUI
just rubato-scheme       # Start Scheme REPL
just rubato-export       # Export to MIDI/OSC
```

## See Also

- `MAZZOLA_TOPOS_OF_MUSIC_GUIDE.md` - Mathematical framework
- `GENESIS_QUERY_PATTERN.md` - How we discovered this
- `acsets/SKILL.md` - ACSet implementation
- `OVERTONE_TO_OSC_MAPPING.md` - Sound bridge
- [Encyclospace](http://www.encyclospace.org) - Mazzola's concept encyclopedia
