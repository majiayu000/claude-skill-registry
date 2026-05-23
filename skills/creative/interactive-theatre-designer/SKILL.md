---
name: interactive-theatre-designer
description: Designs interactive theatrical experiences with branching narratives, audience participation systems, and immersive environmental storytelling.
license: MIT
---

# Interactive Theatre Designer

This skill provides guidance for creating theatrical experiences where audiences participate in, influence, or co-create the performance through interactive systems and branching narratives.

## Core Competencies

- **Branching Narrative**: Multi-path story structures
- **Audience Agency**: Meaningful choice and participation
- **Immersive Design**: Environmental storytelling, site-specific work
- **Live Systems**: Real-time adaptation and emergence
- **Hybrid Formats**: Physical/digital integration

## Interactive Theatre Fundamentals

### Spectrum of Interactivity

```
Passive                                                     Active
│                                                              │
├──Traditional──┬──Promenade──┬──Immersive──┬──Participatory──┤
│   Theatre     │   Theatre   │   Theatre   │    Theatre      │
│               │             │             │                 │
│ Fixed seats   │ Audience    │ Audience    │ Audience        │
│ Fourth wall   │ moves       │ is inside   │ affects         │
│ No agency     │ Partial     │ story world │ narrative       │
│               │ agency      │ Some agency │ Full agency     │
└───────────────┴─────────────┴─────────────┴─────────────────┘
```

### Participation Modes

| Mode | Description | Design Challenge |
|------|-------------|------------------|
| Witness | Observe from within | Manage sight lines, intimacy |
| Explorer | Choose where to go | Balance FOMO, reward curiosity |
| Player | Make story choices | Create meaningful stakes |
| Co-creator | Generate content | Scaffold creativity |
| Performer | Become a character | Lower inhibition barriers |

## Branching Narrative Design

### Structure Types

```
Linear with Variations
A ──→ B ──→ C ──→ D
      ↓
      B' (variation based on earlier choice)

Branching Tree
      ┌── B1 ──→ C1
A ────┤
      └── B2 ──→ C2 ──┬── D1
                      └── D2

Folding Paths (reconvergent)
      ┌── B1 ──┐
A ────┤        ├──→ D
      └── B2 ──┘

Hub and Spoke
         ┌── B ──┐
    ┌────┤       │
A ──┤    └───────┘
    │    ┌── C ──┐
    └────┤       │
         └───────┘

Parallel Threads
A1 ───────→ B1 ───────→ C1
            ↕ sync
A2 ───────→ B2 ───────→ C2
```

### Choice Architecture

```python
class NarrativeChoice:
    """A decision point in the story"""

    def __init__(self, prompt, options):
        self.prompt = prompt
        self.options = options
        self.context_requirements = []
        self.consequences = {}

    def evaluate_options(self, audience_state):
        """Determine available choices based on state"""
        available = []
        for option in self.options:
            if option.is_available(audience_state):
                available.append(option)

        # Always ensure at least two meaningful options
        if len(available) < 2:
            available.append(self._create_fallback_option())

        return available


class StoryBeat:
    """A unit of narrative action"""

    def __init__(self, content, duration_range, choice=None):
        self.content = content
        self.min_duration = duration_range[0]
        self.max_duration = duration_range[1]
        self.choice = choice  # Optional NarrativeChoice
        self.state_changes = {}  # What this beat modifies
        self.prerequisites = []  # What must be true to reach this
```

### Consequence Systems

```python
class ConsequenceTracker:
    """Track choices and their ripple effects"""

    def __init__(self):
        self.choices_made = []
        self.world_state = {}
        self.character_relationships = {}
        self.available_endings = set()

    def record_choice(self, choice_id, option_selected, timestamp):
        self.choices_made.append({
            'choice': choice_id,
            'selected': option_selected,
            'time': timestamp
        })
        self._apply_consequences(choice_id, option_selected)
        self._update_available_endings()

    def _apply_consequences(self, choice_id, option):
        """Apply immediate and delayed consequences"""
        # Immediate effects
        for effect in option.immediate_effects:
            self._apply_effect(effect)

        # Queue delayed effects
        for effect in option.delayed_effects:
            self._queue_effect(effect)

    def get_story_fingerprint(self):
        """Unique identifier for this audience's journey"""
        return hash(tuple(
            (c['choice'], c['selected'])
            for c in self.choices_made
        ))
```

## Audience Agency Design

### Choice Design Principles

**Make Choices Meaningful**:
- Clear stakes: What's at risk?
- Visible consequences: Changes they can observe
- Emotional investment: Characters they care about
- No "right" answer: Multiple valid paths

**Avoid Choice Paralysis**:
- Limit to 2-4 options at decision points
- Provide adequate context (but not too much)
- Use time pressure sparingly and purposefully
- Signal importance level of choices

### Voting and Collective Choice

```python
class CollectiveDecision:
    """Aggregate audience input into story decisions"""

    def __init__(self, voting_method='plurality'):
        self.voting_method = voting_method
        self.votes = {}

    def collect_votes(self, options, timeout_seconds=30):
        """Gather votes from audience"""
        # Methods: raise hands, mobile app, physical movement, sound
        pass

    def resolve(self):
        """Determine outcome based on voting method"""
        methods = {
            'plurality': self._plurality,      # Most votes wins
            'supermajority': self._supermajority,  # Needs 2/3
            'consensus': self._consensus,      # Unanimous
            'weighted': self._weighted,        # Some votes count more
            'random_delegate': self._delegate  # One person decides
        }
        return methods[self.voting_method]()

    def _plurality(self):
        return max(self.votes.keys(), key=lambda x: self.votes[x])
```

### Individual vs Collective Agency

| Approach | Pros | Cons |
|----------|------|------|
| Individual choices | Personal investment | Logistical complexity |
| Collective voting | Easy to manage | Minority feels unheard |
| Representative | Balance of both | Choosing representative |
| Parallel paths | Everyone gets agency | Requires more content |

## Immersive Environment Design

### Space as Narrative

```
TRADITIONAL STAGE          IMMERSIVE SPACE

┌─────────────────┐       ┌─────────────────────────────┐
│                 │       │  GARDEN    │    LIBRARY    │
│      STAGE      │       │  (Past)    │    (Memory)   │
│                 │       │     ◇      ↔      ◇        │
├─────────────────┤       ├────────────┼───────────────┤
│    AUDIENCE     │       │  KITCHEN   │    BEDROOM    │
│                 │       │  (Present) │    (Future)   │
└─────────────────┘       │     ◇      ↔      ◇        │
                          └─────────────────────────────┘
                               ◇ = Performance hotspot
                               ↔ = Audience flow path
```

### Environmental Storytelling Elements

```python
class ImmersiveSpace:
    """Design an immersive theatrical environment"""

    def __init__(self, venue):
        self.venue = venue
        self.zones = {}
        self.artifacts = []
        self.ambient_states = {}

    def add_zone(self, zone):
        """Define a narrative zone"""
        self.zones[zone.name] = zone

    def design_discovery_path(self, story_beats):
        """Create environmental narrative arc"""
        path = []
        for beat in story_beats:
            zone = self._select_zone_for_beat(beat)
            artifacts = self._place_artifacts(beat, zone)
            ambient = self._set_ambient_state(beat, zone)
            path.append({
                'beat': beat,
                'zone': zone,
                'artifacts': artifacts,
                'ambient': ambient
            })
        return path


class NarrativeArtifact:
    """Object that tells story when discovered"""

    def __init__(self, name, backstory, discovery_trigger):
        self.name = name
        self.backstory = backstory  # What it reveals
        self.discovery_trigger = discovery_trigger  # How found
        self.required_for_story = False
        self.hidden_level = 0  # 0=obvious, 5=very hidden
```

### Sensory Design

| Sense | Storytelling Uses | Technical Considerations |
|-------|-------------------|--------------------------|
| Visual | Character, mood, focus | Lighting plots, scenic |
| Audio | Atmosphere, transition | Speakers, acoustic design |
| Smell | Memory, place, emotion | Scent machines, natural |
| Touch | Texture, temperature | Material selection |
| Taste | Ritual, communion | Food safety, allergies |

## Live System Design

### Real-Time Adaptation

```python
class ShowController:
    """Manage live show based on audience behavior"""

    def __init__(self, script, performers, systems):
        self.script = script
        self.performers = performers
        self.systems = systems  # Lights, sound, effects
        self.current_beat = None
        self.audience_state = AudienceState()

    def update(self):
        """Called continuously during show"""
        # Observe audience
        self.audience_state.update(self._observe_audience())

        # Check for triggers
        triggers = self._check_triggers()

        # Adapt if needed
        for trigger in triggers:
            self._handle_trigger(trigger)

        # Cue performers
        self._send_performer_cues()

    def _check_triggers(self):
        """Detect conditions that require adaptation"""
        triggers = []

        # Audience engagement low
        if self.audience_state.engagement < 0.3:
            triggers.append(('low_engagement', 'intensify'))

        # Audience moving to unexpected zone
        if self._unexpected_movement():
            triggers.append(('migration', 'redirect_or_adapt'))

        # Time running over/under
        pace = self._calculate_pace()
        if pace < 0.8:
            triggers.append(('slow_pace', 'compress'))
        elif pace > 1.2:
            triggers.append(('fast_pace', 'expand'))

        return triggers
```

### Performer Communication

```python
class PerformerCueSystem:
    """Real-time communication with performers"""

    def __init__(self):
        self.performers = {}
        self.cue_queue = []

    def add_performer(self, name, device_type):
        """Register performer with their cue device"""
        self.performers[name] = {
            'device': device_type,  # 'earpiece', 'wearable', 'visual'
            'current_track': None,
            'status': 'ready'
        }

    def send_cue(self, performer, cue_type, content, urgency='normal'):
        """Send cue to specific performer"""
        cue = {
            'performer': performer,
            'type': cue_type,  # 'go', 'hold', 'redirect', 'improv'
            'content': content,
            'urgency': urgency
        }
        self._transmit(cue)

    def broadcast_state_change(self, new_state):
        """Inform all performers of story state change"""
        for performer in self.performers:
            self.send_cue(
                performer,
                'state_change',
                new_state,
                urgency='low'
            )
```

## Documentation and Planning

### Show Bible Structure

```markdown
## [Show Title] Production Bible

### Concept
- Logline (one sentence)
- Themes
- Audience experience goals

### Narrative
- Story summary (non-branching core)
- Branch points and options
- Endings (and how reached)
- Character breakdowns

### Space
- Venue requirements
- Zone map
- Artifacts inventory
- Technical requirements

### Interactivity
- Choice points catalog
- Participation mechanics
- Edge cases and recovery

### Operations
- Audience journey map
- Performer tracks
- Stage management protocol
- Emergency procedures
```

### Run Sheet Format

```
TIME    | BEAT           | ACTION                | TRIGGERS
--------|----------------|----------------------|------------------
0:00    | GATHERING      | Audience enters      | N/A
0:15    | INTRO          | Host welcome         | All present
0:20    | CHOICE 1       | Vote on path         | 2 min timer
0:22    | BRANCH A or B  | Split audience       | Vote result
...     | ...            | ...                  | ...
1:45    | CONVERGENCE    | All paths meet       | All groups arrive
2:00    | FINALE         | Final choice         | Timer
2:10    | END            | House lights         | Applause
```

## Best Practices

### Designing for Failure

- Plan for empty rooms (no one chooses that path)
- Plan for crowded rooms (everyone chooses same path)
- Plan for confused audiences (unclear instructions)
- Plan for disruptive participants (graceful management)
- Plan for technical failures (degraded mode operation)

### Rehearsal Process

1. **Paper prototype**: Walk through on paper first
2. **Block rehearsal**: Test spacing and movement
3. **Branch rehearsals**: Practice each path separately
4. **Integration**: Run full show with choices
5. **Audience tests**: Invited audience for feedback
6. **Tech**: Add all technical elements
7. **Previews**: Public performances for refinement

## References

- `references/choice-architecture.md` - Designing meaningful decisions
- `references/immersive-case-studies.md` - Notable productions analysis
- `references/live-systems-tech.md` - Technical implementation patterns
