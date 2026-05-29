---
name: movement-notation-systems
description: Designs systems for encoding, scoring, and generating choreographic movement using Laban notation, computational geometry, and procedural animation principles.
license: MIT
---

# Movement Notation Systems

This skill provides guidance for creating systems that encode, analyze, and generate human movement for choreography, animation, and movement analysis.

## Core Competencies

- **Movement Notation**: Labanotation, Benesh, Motif notation
- **Computational Geometry**: Skeletal representation, joint angles
- **Procedural Animation**: Rule-based movement generation
- **Effort-Shape Analysis**: Laban Movement Analysis (LMA)
- **Temporal Structures**: Rhythm, phrasing, dynamics

## Movement Notation Fundamentals

### The Challenge of Movement

Movement is inherently multidimensional:
- 3D spatial paths
- Temporal evolution
- Body part coordination
- Qualitative dynamics (effort)
- Relational context (other bodies, objects, space)

### Major Notation Systems

| System | Strengths | Use Cases |
|--------|-----------|-----------|
| Labanotation | Complete, precise | Archival, reconstruction |
| Benesh | Compact, visual | Ballet, therapy |
| Motif | Abstract, readable | Teaching, analysis |
| Motion Capture | Exact coordinates | Animation, research |

## Laban Movement Analysis Framework

### Body Component

What body parts are moving:

```
Body Organization:
├── Core-Distal (center outward)
├── Head-Tail (spinal connection)
├── Upper-Lower (horizontal division)
├── Body-Half (left-right)
└── Cross-Lateral (diagonal connections)

Body Parts Hierarchy:
Center (pelvis)
├── Torso (spine, chest)
│   ├── Head
│   ├── Shoulders
│   └── Arms → Elbows → Hands → Fingers
└── Hips
    └── Legs → Knees → Feet → Toes
```

### Space Component

Where the body moves:

```python
class KinesphereModel:
    """The reachable space around the body"""

    DIMENSIONS = {
        'vertical': {'up', 'down'},
        'horizontal': {'left', 'right'},
        'sagittal': {'forward', 'backward'}
    }

    LEVELS = ['low', 'middle', 'high']

    # 27 directions in the kinesphere
    DIRECTION_SYMBOLS = {
        'place_high': (0, 1, 0),
        'place_middle': (0, 0, 0),
        'place_low': (0, -1, 0),
        'forward_high': (0, 1, 1),
        'forward_middle': (0, 0, 1),
        'forward_low': (0, -1, 1),
        # ... all 27 combinations
    }

    # Spatial scales
    SCALES = {
        'near': 0.3,    # Close to body center
        'mid': 0.6,     # General reach
        'far': 1.0      # Full extension
    }
```

### Effort Component

How movement is performed (qualitative dynamics):

```python
class EffortFactors:
    """Laban Effort qualities"""

    FACTORS = {
        'weight': {
            'light': {'sensation': 'buoyant', 'value': -1},
            'strong': {'sensation': 'powerful', 'value': 1}
        },
        'time': {
            'sustained': {'sensation': 'leisurely', 'value': -1},
            'quick': {'sensation': 'urgent', 'value': 1}
        },
        'space': {
            'indirect': {'sensation': 'flexible', 'value': -1},
            'direct': {'sensation': 'focused', 'value': 1}
        },
        'flow': {
            'free': {'sensation': 'fluent', 'value': -1},
            'bound': {'sensation': 'controlled', 'value': 1}
        }
    }

    # Basic Effort Actions (combinations of weight, time, space)
    ACTIONS = {
        'punch': {'weight': 'strong', 'time': 'quick', 'space': 'direct'},
        'dab': {'weight': 'light', 'time': 'quick', 'space': 'direct'},
        'slash': {'weight': 'strong', 'time': 'quick', 'space': 'indirect'},
        'flick': {'weight': 'light', 'time': 'quick', 'space': 'indirect'},
        'press': {'weight': 'strong', 'time': 'sustained', 'space': 'direct'},
        'glide': {'weight': 'light', 'time': 'sustained', 'space': 'direct'},
        'wring': {'weight': 'strong', 'time': 'sustained', 'space': 'indirect'},
        'float': {'weight': 'light', 'time': 'sustained', 'space': 'indirect'}
    }
```

### Shape Component

How the body changes form:

```python
class ShapeQualities:
    """Body shape changes"""

    MODES = {
        'shape_flow': {
            'description': 'Internal shaping, self-oriented',
            'examples': ['breathing', 'growing/shrinking']
        },
        'directional': {
            'description': 'Bridge to environment',
            'subtypes': ['spoke-like', 'arc-like']
        },
        'carving': {
            'description': 'Sculpting 3D space',
            'relationship': 'Interacting with environment'
        }
    }

    AFFINITIES = {
        'rising': {'effort': 'light', 'direction': 'up'},
        'sinking': {'effort': 'strong', 'direction': 'down'},
        'spreading': {'effort': 'indirect', 'direction': 'horizontal'},
        'enclosing': {'effort': 'direct', 'direction': 'in'},
        'advancing': {'effort': 'sustained', 'direction': 'forward'},
        'retreating': {'effort': 'quick', 'direction': 'back'}
    }
```

## Computational Movement Representation

### Skeletal Data Structure

```python
class Skeleton:
    """Hierarchical skeletal representation"""

    def __init__(self):
        self.joints = {
            'pelvis': Joint('pelvis', parent=None),
            'spine': Joint('spine', parent='pelvis'),
            'chest': Joint('chest', parent='spine'),
            'neck': Joint('neck', parent='chest'),
            'head': Joint('head', parent='neck'),
            'l_shoulder': Joint('l_shoulder', parent='chest'),
            'l_elbow': Joint('l_elbow', parent='l_shoulder'),
            'l_wrist': Joint('l_wrist', parent='l_elbow'),
            'r_shoulder': Joint('r_shoulder', parent='chest'),
            # ... etc
        }

    def get_world_position(self, joint_name):
        """Compute global position from local transforms"""
        joint = self.joints[joint_name]
        position = joint.local_position

        current = joint
        while current.parent:
            parent = self.joints[current.parent]
            position = parent.rotation.apply(position) + parent.local_position
            current = parent

        return position

    def compute_joint_angles(self):
        """Extract joint angles for analysis"""
        angles = {}
        for name, joint in self.joints.items():
            if joint.parent:
                angles[name] = joint.rotation.as_euler('xyz')
        return angles


class Joint:
    """Single joint in skeleton hierarchy"""

    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.local_position = np.array([0, 0, 0])
        self.rotation = Rotation.identity()
        self.constraints = {}  # Joint limits
```

### Motion Trajectory

```python
class MotionTrajectory:
    """Temporal sequence of poses"""

    def __init__(self, fps=30):
        self.fps = fps
        self.frames = []  # List of Skeleton states
        self.annotations = []  # Qualitative markers

    def duration(self):
        return len(self.frames) / self.fps

    def get_velocity(self, joint_name, frame_idx):
        """Compute instantaneous velocity"""
        if frame_idx < 1:
            return np.zeros(3)

        pos_current = self.frames[frame_idx].get_world_position(joint_name)
        pos_prev = self.frames[frame_idx - 1].get_world_position(joint_name)

        return (pos_current - pos_prev) * self.fps

    def extract_effort_features(self, joint_name, window=10):
        """Estimate Laban Effort qualities from motion"""
        features = {
            'weight': self._compute_acceleration_magnitude(joint_name, window),
            'time': self._compute_temporal_change_rate(joint_name, window),
            'space': self._compute_path_directness(joint_name, window),
            'flow': self._compute_flow_continuity(joint_name, window)
        }
        return features
```

## Procedural Movement Generation

### Rule-Based Choreography

```python
class ChoreographyGenerator:
    """Generate movement sequences from rules"""

    def __init__(self):
        self.vocabulary = self._load_movement_vocabulary()
        self.grammar = self._load_grammar_rules()

    def generate_phrase(self, theme, duration_beats=16):
        """Generate choreographic phrase"""

        # Start with motif based on theme
        motif = self._select_motif(theme)

        # Develop through phrase
        phrase = [motif]
        current_beats = motif.duration_beats

        while current_beats < duration_beats:
            # Apply development rules
            if random.random() < 0.3:
                # Repeat with variation
                variation = self._vary_motif(phrase[-1])
                phrase.append(variation)
            elif random.random() < 0.5:
                # Contrast
                contrast = self._generate_contrast(phrase[-1])
                phrase.append(contrast)
            else:
                # Transition
                transition = self._smooth_transition(phrase[-1])
                phrase.append(transition)

            current_beats += phrase[-1].duration_beats

        return phrase

    def _vary_motif(self, motif):
        """Create variation of movement"""
        variations = [
            self._change_level,      # Same movement, different level
            self._mirror,            # Left-right reversal
            self._change_size,       # Larger or smaller
            self._change_tempo,      # Faster or slower
            self._change_direction,  # Face different direction
            self._fragment,          # Part of the movement
            self._extend,            # Add onto the movement
        ]
        return random.choice(variations)(motif)
```

### Effort-Driven Animation

```python
class EffortAnimator:
    """Generate movement with specified Effort qualities"""

    def animate_action(self, skeleton, target_position, effort_state):
        """Move body part with specified Effort"""

        # Time factor affects duration
        if effort_state['time'] == 'quick':
            duration = 0.3
            ease_type = 'exponential'
        else:  # sustained
            duration = 1.2
            ease_type = 'sine'

        # Weight factor affects acceleration
        if effort_state['weight'] == 'strong':
            acceleration_curve = self._strong_curve()
        else:  # light
            acceleration_curve = self._light_curve()

        # Space factor affects path
        if effort_state['space'] == 'direct':
            path = self._linear_path(skeleton.current, target_position)
        else:  # indirect
            path = self._curved_path(skeleton.current, target_position)

        # Flow factor affects continuity
        if effort_state['flow'] == 'bound':
            path = self._add_micro_pauses(path)
        # free flow is smooth by default

        return self._create_animation(
            path=path,
            duration=duration,
            acceleration=acceleration_curve
        )
```

### Spatial Pattern Generation

```python
class FloorPatternGenerator:
    """Generate spatial pathways"""

    def generate_path(self, pattern_type, space_bounds, duration):
        """Generate floor pattern"""

        patterns = {
            'circular': self._circular_path,
            'spiral': self._spiral_path,
            'figure_eight': self._figure_eight,
            'diagonal_cross': self._diagonal_cross,
            'zigzag': self._zigzag_path,
            'random_walk': self._random_walk
        }

        generator = patterns.get(pattern_type, self._random_walk)
        return generator(space_bounds, duration)

    def _spiral_path(self, bounds, duration, turns=3):
        """Generate spiral floor pattern"""
        center = bounds.center
        max_radius = min(bounds.width, bounds.height) / 2

        points = []
        num_points = int(duration * 30)  # 30 points per beat

        for i in range(num_points):
            t = i / num_points
            angle = t * turns * 2 * np.pi
            radius = max_radius * (1 - t)  # Spiral inward

            x = center[0] + radius * np.cos(angle)
            y = center[1] + radius * np.sin(angle)

            points.append((x, y, t * duration))

        return points
```

## Notation Output

### Textual Notation Format

```python
class MovementScore:
    """Text-based movement score"""

    def to_notation(self, phrase):
        """Convert phrase to readable notation"""
        score = []

        for movement in phrase:
            notation = {
                'beat': movement.start_beat,
                'duration': movement.duration_beats,
                'body': self._notate_body(movement),
                'space': self._notate_space(movement),
                'effort': self._notate_effort(movement),
                'description': movement.description
            }
            score.append(notation)

        return score

    def _notate_effort(self, movement):
        """Effort notation symbols"""
        symbols = {
            ('strong', 'quick', 'direct'): '⚡',   # Punch
            ('light', 'sustained', 'indirect'): '☁️',  # Float
            ('strong', 'sustained', 'indirect'): '🌀',  # Wring
            # ... etc
        }
        effort_tuple = (
            movement.effort['weight'],
            movement.effort['time'],
            movement.effort['space']
        )
        return symbols.get(effort_tuple, '○')
```

### Visual Score Representation

```
Time →
|    0    |    1    |    2    |    3    |    4    |
├─────────┼─────────┼─────────┼─────────┼─────────┤
│ ◊ HEAD  │         │    ○    │         │         │
│ ═ ARMS  │  ═══════│════     │   ═════ │═════    │
│ ║ TORSO │    ║    │   ║║    │    ║    │  ║║║    │
│ ‖ LEGS  │   ‖‖    │  ‖  ‖   │   ‖‖    │ ‖    ‖  │
├─────────┼─────────┼─────────┼─────────┼─────────┤
│ Level:  │   High  │   Mid   │   Low   │   Mid   │
│ Effort: │   ⚡    │    ☁️   │    🌀   │   ⚡    │
└─────────┴─────────┴─────────┴─────────┴─────────┘
```

## Best Practices

### Encoding Principles

1. **Preserve intent**: Capture what the choreographer wants, not just positions
2. **Layer information**: Structure > Shape > Dynamics
3. **Allow interpretation**: Don't over-specify unless needed
4. **Support variation**: Enable controlled improvisation

### Analysis Guidelines

- Extract both quantitative (positions) and qualitative (effort) features
- Consider cultural and stylistic context
- Validate with practitioners

## References

- `references/labanotation-symbols.md` - Symbol reference for Labanotation
- `references/lma-glossary.md` - Laban Movement Analysis terminology
- `references/motion-capture-formats.md` - Common mocap data formats
