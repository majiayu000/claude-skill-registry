---
name: create-persona
description: Deliberate persona creation for client modeling, expert profiles, and stakeholder mapping. Integrates with /interview for collaborative creation and /ask for knowledge enrichment. Supports Theory of Mind (BDI), voice training, and simulacrum validation.
triggers: create persona, model client, create stakeholder, persona for, expert profile, adversary persona, fictional persona, train voice for persona, simulacrum test

provides:
  - create-persona
composes:
  - ask
  - memory
  - ingest-youtube
  - dogpile
  - task-monitor
---

# /create-persona

Deliberate persona creation for client modeling, expert profiles, and stakeholder mapping. Integrates with `/interview` for collaborative creation and `/ask` for knowledge enrichment.

**New in v2:** Quality assessment, validation, and iterative improvement (like `/table-lab`).

**New in v3 (Horus-depth):** Theory of Mind (BDI), bridge traversal validation, archetype mood rules.

## When to Use

- **Client modeling**: Create personas for project stakeholders before engagement
- **Expert profiles**: Build rich profiles of domain experts (triggers `/ask learn`)
- **Threat modeling**: Create adversary personas for security analysis
- **Team dynamics**: Model stakeholders and their relationships
- **Quality audit**: Diagnose gaps, validate responses, improve personas

## Content Richness Pre-Flight

Before creating a persona, assess available source material. QRA quality depends entirely on content richness.

### Source Material Tiers

| Tier | Content Available | QRA Target | Action |
|------|-------------------|------------|--------|
| **Rich** | 3+ YouTube talks/podcasts, 1+ books, active online presence | 200-500 | Full persona with auto-learn |
| **Moderate** | 1-2 talks, some interviews, articles | 50-150 | Standard persona, supplement with `/dogpile` |
| **Thin** | Wikipedia + a few articles, no first-person content | 10-30 | Reference anchor only, `--no-learn` |
| **None** | Deceased pre-YouTube, no recordings, no books | 0 | **Don't create** — waste of Chutes quota |

### Historical Figure Warning

Pre-YouTube deceased figures (died before ~2005) typically lack:
- YouTube talks, podcasts, or interviews
- Searchable transcripts
- Sufficient first-person source material for meaningful QRAs

**Create these as reference anchors only**, not full personas:

```bash
# Reference anchor — no learning, no QRA generation
./run.sh create "Chuck Yeager" --template expert --no-learn \
  --note "Reference anchor only — thin content, no YouTube"
```

Examples of thin-content figures to avoid as full personas:
- Chuck Yeager (died 2020, no YouTube presence)
- Neil Armstrong (died 2012, famously private)
- Scott Crossfield (died 2006, X-15 era)

### Pre-Flight Checklist

Before running `batch` or `create --learn`:

1. **YouTube search**: Find 3+ talks, podcasts, or interviews
   - `yt-dlp --flat-playlist "ytsearch10:PERSON_NAME interview"` for quick check
2. **Book search**: Find 1+ authored or biographical books
3. **Set `qra_target`** proportional to content found
4. **Set `content_tier`** in personas.yaml (rich/moderate/thin/none)
5. **Skip voice training** for thin personas: `skip_voice_training: true`

### personas.yaml Content Fields

```yaml
personas:
  - name: Hasard Lee
    template: expert
    content_tier: rich        # rich | moderate | thin | none
    qra_target: 300           # Target QRA count based on content tier
    skip_voice_training: false # true for thin/none personas
    # ...
```

## Triggers

- "create a persona for..."
- "model this client..."
- "who is [Name] and what do they care about?"
- "add a stakeholder..."
- "diagnose persona quality"
- "validate persona knowledge"
- "improve persona"
- "audit personas"
- `/create-persona`

## Quick Start

```bash
# Interactive client persona (uses /interview)
./run.sh create "Jane Smith" --template client --interactive

# Expert persona with auto-learning
./run.sh create "Robert Sapolsky" --template expert --learn

# Quick stakeholder
./run.sh create "Bob Jones" --template stakeholder \
  --role "Engineering Manager" \
  --organization "Acme Corp"

# List all personas
./run.sh list

# Query persona
./run.sh show "Jane Smith" --json

# Batch create from manifest
./run.sh batch personas.yaml --dry-run
./run.sh batch personas.yaml --skip-learn
./run.sh batch personas.yaml --category writers
```

## Templates

| Template | Use Case | Auto-Learn | Default Scope |
|----------|----------|------------|---------------|
| `client` | External stakeholders, customers | No | `clients` |
| `expert` | Domain experts, researchers | Yes | `behavioral` |
| `stakeholder` | Internal team members | No | `stakeholders` |
| `adversary` | Threat actors, red-team personas | No | `threat-models` |
| `coder` | Developers, game devs, OSS maintainers | Yes | `coders` |
| `fictional` | Simulated characters, AI companions | From influences | `personas` |

## Skill Access by Template

Different personas have access to different skills for research and answering questions:

| Template | Available Skills |
|----------|-----------------|
| `coder` | `/hack`, `/battle`, `/context7`, `/github-search`, `/treesitter`, `/create-story`, `/dogpile` |
| `expert` | `/dogpile`, `/arxiv`, `/context7`, `/memory` |
| `adversary` | `/hack`, `/battle`, `/security-scan` |
| `client` | `/dogpile`, `/memory` |
| `stakeholder` | `/dogpile`, `/memory` |
| `fictional` | `/dogpile`, `/discover-movies`, `/discover-books`, `/ingest-youtube`, `/ingest-movie`, `/create-story`, `/tts-train` |

This enables rich persona interactions like:
- Ask a game developer persona how to implement inverse square algorithms
- Ask a security expert persona to review architecture for vulnerabilities
- Ask a domain expert to cite colleagues' papers on a topic

## CLI Commands

### `create` — Create a new persona

```bash
./run.sh create NAME [OPTIONS]

Options:
  --template {client,expert,stakeholder,adversary}  Persona template
  --interactive, -i    Use /interview for collaborative creation
  --learn              Trigger /ask learn for knowledge enrichment
  --scope SCOPE        Memory scope (default: template-based)
  --role ROLE          Job title or role
  --organization ORG   Company or institution
  --domain DOMAIN      Area of expertise
  --goal GOAL          Add a goal (repeatable)
  --concern CONCERN    Add a concern (repeatable)
  --colleague NAME     Add colleague relationship (repeatable)
  --bridge BRIDGE      Add Federated Taxonomy bridge (repeatable)
```

### `list` — List personas

```bash
./run.sh list [OPTIONS]

Options:
  --scope SCOPE        Filter by scope
  --template TEMPLATE  Filter by template type
  --tag TAG            Filter by tag
  --json               Output as JSON
```

### `show` — Display persona details

```bash
./run.sh show NAME [OPTIONS]

Options:
  --scope SCOPE        Memory scope to search
  --json               Output as JSON
  --with-colleagues    Include colleague details
```

### `update` — Modify existing persona

```bash
./run.sh update NAME [OPTIONS]

Options:
  --add-goal GOAL      Add a goal
  --add-concern CONCERN  Add a concern
  --add-colleague NAME   Add colleague relationship
  --set-role ROLE      Update role
  --remove-goal GOAL   Remove a goal
```

### `relate` — Create relationship between personas

```bash
./run.sh relate NAME [OPTIONS]

Options:
  --colleague NAME     Peer relationship
  --reports-to NAME    Hierarchical (reports to)
  --manages NAME       Hierarchical (manages)
  --mentors NAME       Mentorship relationship
  --bridges BRIDGE     Shared taxonomy bridges (comma-separated)
  --context TEXT       Relationship context/notes
```

### `batch` — Create multiple personas from YAML manifest

```bash
./run.sh batch MANIFEST [OPTIONS]

Options:
  --category, -c CATEGORY  Only process specific category
  --skip-learn             Skip auto-learning
  --dry-run                Preview without creating
```

## Simulacrum Validation (REQUIRED)

**A persona is NOT complete until it passes simulacrum tests.**

Simulacrum tests probe whether the persona can *reason* like the real person, not just regurgitate Wikipedia facts.

### The Simulacrum Standard

| Bad (Trivia) | Good (Simulacrum) |
|--------------|-------------------|
| "What year was Miyazaki born?" | "How would you convey emotion without dialogue?" |
| "What studio did he co-found?" | "What's wrong with fully digital animation?" |
| "Name three films he directed" | "Why does Chihiro initially refuse to eat?" |

### `simulacrum` — Deep validation

```bash
./run.sh simulacrum NAME [OPTIONS]

Options:
  --probes, -p TEXT        Probe types (default: philosophy,technique,motivation)
  --scope, -s SCOPE        Memory scope
  --json                   Output as JSON
```

Probe types:
- `philosophy` — Core worldview, beliefs, "what is art for?"
- `technique` — Craft methods, unique approaches
- `motivation` — Why they make choices, what drives them
- `criticism` — What they oppose, what's wrong with the mainstream
- `hypothetical` — How they'd handle new scenarios

Example:
```bash
./run.sh simulacrum "Hayao Miyazaki" --probes "philosophy,technique,criticism"

# Output:
Simulacrum Validation: Hayao Miyazaki
  Grade: B (Accuracy: 0.80)

Simulacrum Probes:
  ✓ What is Hayao Miyazaki's core philosophy or approach to their work?
      Good reasoning indicators (4 found)
      Persona speaking in first person (good simulacrum)
  ✓ How would Hayao Miyazaki approach a scene that needs to convey deep emotion...
      Substantive answer (127 words)
  ✗ What does Hayao Miyazaki criticize about the mainstream in their field?
      Knowledge gap indicator: 'no specific information'
```

### `simulacrum-improve` — Iterative improvement loop

```bash
./run.sh simulacrum-improve [NAME] [OPTIONS]

Options:
  --threshold, -t FLOAT    Pass threshold (default: 0.7)
  --max-iterations, -m INT Max iterations per persona (default: 3)
  --probes, -p TEXT        Probe types
  --limit, -l INT          Max personas to process
  --dry-run                Preview without changes
  --resume                 Resume from checkpoint
  --scope, -s SCOPE        Memory scope
  --json                   Output as JSON
```

Examples:
```bash
# Improve single persona until it passes
./run.sh simulacrum-improve "Hayao Miyazaki" --threshold 0.8

# Improve ALL personas in batch (overnight run)
./run.sh simulacrum-improve --scope personas --threshold 0.7 --resume

# Dry run to see what would happen
./run.sh simulacrum-improve --scope personas --dry-run --limit 10
```

The improvement loop:
1. **Validate** with simulacrum probes
2. **Identify** what's missing (philosophy? technique? first-person content?)
3. **Improve** with targeted actions:
   - Deep /dogpile for philosophy and reasoning
   - YouTube lectures/interviews for first-person perspective
   - Books for deeper knowledge
4. **Re-validate** until passing

### Workflow: Persona Creation → Simulacrum Pass

```
1. ./run.sh batch personas.yaml           # Create personas
2. ./run.sh simulacrum-improve --scope personas --resume  # Improve until valid
3. ./run.sh audit --scope personas        # Final quality report
```

A persona is ready for use ONLY when `simulacrum` shows Grade B or better.

---

## Quality Commands (v2)

### `diagnose` — Identify gaps and issues

```bash
./run.sh diagnose NAME [OPTIONS]

Options:
  --scope, -s SCOPE        Memory scope
  --json                   Output as JSON
```

Checks:
- **Completeness**: Sources count (dogpile, books, YouTube)
- **Connectivity**: Colleague/relationship edges
- **Freshness**: Days since last update
- **Bridges**: Federated Taxonomy coverage

Example output:
```
Diagnosis: Hayao Miyazaki
  Scope: personas

Quality Scores:
  Completeness [████████░░] 0.8
  Connectivity [████░░░░░░] 0.4
  Accuracy     [█████░░░░░] 0.5
  Freshness    [██████████] 1.0

  Overall: 0.68 (Grade: C)

Gaps Identified:
  • No colleague relationships - isolated node
  • Missing source: books
```

### `validate` — Test persona responses

```bash
./run.sh validate NAME [OPTIONS]

Options:
  --question, -q TEXT      Test question
  --expected, -e TEXT      Expected content (comma-separated)
  --ground-truth, -g PATH  YAML/JSON file with tests
  --scope, -s SCOPE        Memory scope
  --json                   Output as JSON
```

Examples:
```bash
# Single question test
./run.sh validate "Hayao Miyazaki" \
  --question "What is Nausicaä about?" \
  --expected "environmental,princess,post-apocalyptic"

# Batch tests from file
./run.sh validate "Hayao Miyazaki" --ground-truth tests/miyazaki.yaml
```

Ground truth file format:
```yaml
Hayao Miyazaki:
  - question: "What is Nausicaä about?"
    expected_contains: ["environmental", "princess"]
  - question: "What studio did Miyazaki co-found?"
    expected_contains: ["Ghibli"]
```

### `improve` — Iterative enhancement

```bash
./run.sh improve NAME [OPTIONS]

Options:
  --threshold, -t FLOAT    Quality threshold (default: 0.7)
  --max-iterations, -m INT Max iterations (default: 3)
  --dry-run                Preview actions without executing
  --scope, -s SCOPE        Memory scope
  --json                   Output as JSON
```

Improvement actions (convergence loop):
1. Re-run `/dogpile` for missing sources
2. Discover books if none
3. Ingest YouTube if none
4. Enrich colleague graph
5. Extract QRA pairs

Example:
```bash
./run.sh improve "Hayao Miyazaki" --threshold 0.8

# Output:
Actions:
  • Run /dogpile deep research
  • Discover and create colleague relationships

  Initial score: 0.55
  Final score: 0.78
  Improvement: +0.23
  Iterations: 2

✓ Converged at quality 0.78
```

### `audit` — Batch quality assessment

```bash
./run.sh audit [OPTIONS]

Options:
  --scope, -s SCOPE        Scope to audit
  --min-quality FLOAT      Only show below threshold
  --limit, -l INT          Max personas to audit
  --report                 Generate markdown report
  --json                   Output as JSON
```

Example:
```bash
./run.sh audit --scope personas

# Output:
Audit Results:
  Total personas: 237
  Average score: 0.72

Grade Distribution:
  A: ████████ 45
  B: ██████████████ 89
  C: ██████████ 67
  D: ████ 28
  F: █ 8

Common Gaps:
  • No colleague relationships (89 personas)
  • Missing source: books (45 personas)

Failing Personas (Grade F):
  • John Smith
  • Jane Doe
```

### `export` / `import` — Backup and restore

```bash
./run.sh export NAME --format json > persona.json
./run.sh import persona.json --scope new-project
```

## Persona Schema

```python
@dataclass
class Persona:
    # Identity
    name: str
    aliases: list[str]
    role: str
    organization: str

    # Domain
    domain: str
    expertise: list[str]

    # Communication
    communication_style: str  # direct, diplomatic, technical
    preferred_format: str     # bullets, prose, code

    # Goals & Constraints
    goals: list[str]
    concerns: list[str]
    constraints: list[str]

    # Federated Taxonomy
    bridge_weights: dict[str, float]  # Precision: 0.8, Resilience: 0.6

    # Relationships (stored as graph edges)
    # Queried via: recall --tags colleague:{name}

    # Learning sources (from /ask learn)
    sources: dict  # {youtube: 3, books: 1, dogpile: 5}

    # Historical & Cultural Context (for voice design)
    family_structure: dict  # birth_order, siblings, parent_loss_age, socioeconomic_class
    religion: dict  # tradition, denomination, religiosity (0-1), emotional_expression_norms
    cultural_context: dict  # birth_region, era, cultural_tradition, grief_expression_norms
    life_events: dict  # formative (5-25), prime (25-50), later (50+) - age-correlated

    # Lifespan (for age-at-event correlation)
    birth_year: int  # e.g., 121 for Marcus Aurelius (CE)
    death_year: int  # e.g., 180 for Marcus Aurelius
    lifespan_note: str  # "121-180 CE" or "428-348 BCE"

    # Metadata
    scope: str
    tags: list[str]
    template: str
    created_at: str
    last_updated: str
```

### Historical Context Fields (v7)

New fields for deep persona modeling and voice design:

#### Family Structure

```yaml
family_structure:
  birth_order: eldest  # eldest, middle, youngest, only
  siblings: 2
  parent_loss_age: 12  # if applicable
  family_size: large  # small, medium, large
  socioeconomic_class: middle  # lower, middle, upper
  family_stability: unstable  # stable, unstable, traumatic
```

#### Religion/Spirituality

```yaml
religion:
  tradition: Buddhist
  denomination: Zen  # Theravada, Mahayana, Catholic, Protestant, etc.
  religiosity: 0.7  # 0.0 = cultural only, 1.0 = devout/practicing
  religious_era: Victorian  # Era-specific religious norms
  emotional_expression_norms: suppressed  # encouraged, moderate, suppressed
```

#### Cultural Context

```yaml
cultural_context:
  birth_region: "Rome, Italy"
  era: "2nd century CE"
  cultural_tradition: Greco-Roman
  emotional_display_rules: "Stoic - controlled expression"
  grief_expression_norms: "public mourning rituals but private suffering"
```

#### Life Events (Age-Correlated)

Events at different ages create layered emotional texture in voice:

```yaml
life_events:
  formative:  # ages 5-25 - always subtly present
    - age: 12
      event: "father's death"
      voice_impact: "underlying grief, guarded"
  prime:  # ages 25-50 - defines conscious identity
    - age: 35
      event: "became emperor"
      voice_impact: "authoritative weight"
  later:  # ages 50+ - most audible layer
    - age: 58
      event: "writing Meditations"
      voice_impact: "reflective, philosophical"
```

| Life Stage | Voice Impact |
|------------|--------------|
| **Formative (5-25)** | Foundational - always subtly present |
| **Prime (25-50)** | Defining - conscious voice identity |
| **Later (50+)** | Current - most audible demeanor |

## Federated Taxonomy Integration

Personas have bridge weights that influence recall and synthesis:

| Bridge | High Weight Means |
|--------|-------------------|
| Precision | Values accuracy, technical detail |
| Resilience | Focuses on robustness, reliability |
| Fragility | Concerned about risks, edge cases |
| Corruption | Deals with adversarial scenarios |
| Loyalty | Values consistency, trust |
| Stealth | Prefers subtlety, discretion |

### Relationship Edges

Relationships are stored as graph edges with bridge attributes:

```json
{
  "from": "Robert Sapolsky",
  "to": "Bruce McEwen",
  "relationship": "mentor",
  "bridges": ["Resilience", "Precision"],
  "context": "McEwen pioneered allostatic load concept"
}
```

This enables multi-hop traversal:
```
Q: "What do stress researchers say about cortisol?"
→ Direct: Sapolsky
→ Via mentor edge + Resilience bridge: McEwen
→ Synthesis includes both perspectives
```

## Composability

### With /ask

```bash
# Create expert, auto-learn, then query
./run.sh create "Lisa Feldman Barrett" --template expert --learn

# /ask now has rich persona context
/ask "How would Barrett explain constructed emotions?"
```

### With /interview

```bash
# Interactive creation gathers rich details
./run.sh create "Jane Smith" --template client --interactive

# Interview questions based on template:
# - What is their role?
# - What are their top priorities?
# - What concerns do they have?
# - Who do they work with?
```

### With /memory

```bash
# Personas stored in memory with tags
memory recall "persona Jane Smith" --scope clients

# Relationships as edges
memory recall --tags "colleague:jane_smith"
```

## Examples

### Client Persona for Project

```bash
# Create client persona interactively
./run.sh create "Sarah Chen" --template client -i

# Add relationship to another stakeholder
./run.sh relate "Sarah Chen" --reports-to "Mike Johnson (CEO)"

# Use in /ask
/ask "What would Sarah think about adding OAuth?"
# → Uses Sarah's goals, concerns, communication style
```

### Expert Persona with Learning

```bash
# Create and learn about expert
./run.sh create "Geoffrey Hinton" --template expert \
  --domain "deep learning" \
  --learn

# Discover colleagues automatically (sparse persona enrichment)
# → Finds: Yann LeCun, Yoshua Bengio

# Multi-hop query
/ask "What do deep learning pioneers think about AI safety?"
# → Traverses Hinton → LeCun, Bengio via colleague edges
```

### Adversary Persona for Threat Model

```bash
# Create threat actor persona
./run.sh create "APT-29" --template adversary \
  --domain "nation-state" \
  --goal "Credential theft" \
  --goal "Persistence" \
  --bridge Stealth \
  --bridge Corruption

# Use in security analysis
/ask "How would APT-29 approach this architecture?"
```

### Coder Persona for Technical Questions

```bash
# Create game developer persona
./run.sh create "John Carmack" --template coder \
  --domain "game development" \
  --learn

# Auto-learns from talks, interviews, code samples
# Has access to: /hack, /battle, /context7, /github-search

# Ask technical questions - persona can use /context7 for docs
/ask "How would Carmack implement an inverse square algorithm in C?"
# → Uses persona's coding philosophy + /context7 for C docs

# Ask about optimization - persona can cite their own work
/ask "What would Carmack say about BSP tree optimization?"
# → References DOOM/Quake source code via /github-search

# Create OSS maintainer persona
./run.sh create "Linus Torvalds" --template coder \
  --domain "systems programming" \
  --goal "Maintainability" \
  --goal "Performance" \
  --bridge Precision \
  --learn

# Multi-hop: ask about kernel code, can quote colleagues
/ask "What do kernel developers think about Rust in the kernel?"
# → Traverses Linus → other kernel maintainers via colleague edges
```

## Batch Creation

Create multiple personas at once from a YAML manifest file:

```bash
# Preview what would be created
./run.sh batch personas.yaml --dry-run

# Create all personas with auto-learning
./run.sh batch personas.yaml

# Create without triggering /ask learn (faster)
./run.sh batch personas.yaml --skip-learn

# Only create personas in a specific category
./run.sh batch personas.yaml --category coders
```

### Manifest Format

```yaml
# personas.yaml
defaults:
  scope: personas
  auto_learn: true
  depth: standard

writers:
  - name: Alan Moore
    template: expert
    domain: comics, literature, occultism
    expertise:
      - graphic novels
      - chaos magic
    goals:
      - Challenge narrative conventions
    bridges:
      Corruption: 0.7
      Precision: 0.8
    colleagues:
      - Dave Gibbons
      - Neil Gaiman

coders:
  - name: John Carmack
    template: coder
    domain: game development, VR
    expertise:
      - 3D graphics
      - engine optimization
    goals:
      - Push technical boundaries
    bridges:
      Precision: 0.95
    colleagues:
      - John Romero
```

Categories can be named anything (writers, coders, strategists, etc.). Each persona in a category gets the category name as a tag.

## Fictional Personas (v5)

Fictional personas are **simulated characters** (not real people). The key difference:

| Aspect | Real Persona | Fictional Persona |
|--------|--------------|-------------------|
| **Learning source** | Their talks, books, interviews | What they would consume |
| **Voice training** | Their own voice clips | Reference actor clips |
| **Simulacrum test** | "Did they really say this?" | "Is this in-character?" |
| **Discovery** | `/dogpile {name}` | `/dogpile {influences}` |

### Quick Start

```bash
# Create fictional persona from character sheet
./run.sh create "Embry" --template fictional \
  --character-sheet /path/to/EMBRY_CHARACTER_SHEET.md

# Interactive creation (asks the character what they consume)
./run.sh create "Embry" --template fictional --interactive

# Set voice references
./run.sh voice-ref "Embry" \
  --actor "Hailee Steinfeld" --register confident --weight 0.6 \
  --actor "Kristen Stewart" --register uncertain --weight 0.4

# Train voice from reference actors
./run.sh voice train "Embry" --from-references
```

### Fictional-Specific Fields

Fictional personas have additional fields not present in other templates:

```yaml
# Embry - Fictional Persona Example
name: Embry
template: fictional

# What shapes their personality (media they consume)
media_consumption:
  movies:
    formative: [Contact, Interstellar, Apollo 13, Ex Machina]
    guilty_pleasure: [rocket launch livestreams]
  books:
    nightstand: [The Right Stuff, A Fire Upon the Deep]
  youtube_channels:
    daily: [Everyday Astronaut, Scott Manley, SmarterEveryDay]
  guilty_pleasures:
    - competes with mom at Sudoku secretly
    - drinks too many Celsius

# Voice from REFERENCE ACTRESSES (not themselves)
voice_references:
  - actress: Hailee Steinfeld
    register: confident
    weight: 0.6
    clips_to_find: [Hawkeye technical scenes, True Grit conviction]
    characteristics: [youthful energy, commanding presence, natural flow]
  - actress: Kristen Stewart
    register: uncertain
    weight: 0.4
    clips_to_find: [awkward interviews, hesitant moments]
    characteristics: [hesitant pauses, vocal fry, endearing awkwardness]

voice_accent: subtle_southern  # Charleston educated

# Personality quirks
quirks:
  - competes with mom at Sudoku secretly
  - watches rocket launches while eating lunch
  - has 3-month expense report backlog
  - drinks too many Celsius

# Register switching behavior
register_switching:
  confident_triggers: [SPARTA, NIST, technical topics]
  uncertain_triggers: [being observed, Marcus from PM]
  confident_voice: Hailee Steinfeld
  uncertain_voice: Kristen Stewart

# Path to full character document
character_sheet_path: /path/to/EMBRY_CHARACTER_SHEET.md

# Simulacrum validates character consistency, not ground truth
simulacrum_mode: character_consistency
```

### The Character Speaks

Fictional personas can "speak" to express preferences about themselves. The agent embodies the character to answer questions like:

- "What do you watch on YouTube?"
- "Whose voice do you identify with when you're confident?"
- "What are your guilty pleasures?"

This is NOT the agent deciding FOR the character - it's letting the character have agency in their own creation.

### Workflow: Creating a Fictional Persona

```
1. DEFINE CHARACTER
   └── Load character sheet (if exists)
   └── Define basic attributes (age, role, domain)

2. ASK CHARACTER WHAT THEY CONSUME
   └── *Embry, what movies do you rewatch?*
   └── *What YouTube channels are you subscribed to?*
   └── *What's on your nightstand?*

3. ASK CHARACTER ABOUT THEIR VOICE
   └── *Whose voice do you sound like when confident?*
   └── *Whose voice when you're uncertain?*
   └── *What accent do you have?*

4. INGEST REFERENCE CONTENT
   └── /discover-movies for films they'd watch
   └── /ingest-youtube for channels they follow
   └── /ingest-movie for voice reference actors

5. TRAIN VOICE FROM REFERENCES
   └── Find clips of reference actors
   └── Train blended voice model
   └── 60% Steinfeld / 40% Stewart (weighted blend)

6. VALIDATE CHARACTER CONSISTENCY
   └── Simulacrum tests in-character responses
   └── Checks register switching works
   └── Verifies quirks appear naturally
```

### CLI Commands for Fictional

#### `create` with fictional template

```bash
./run.sh create NAME --template fictional [OPTIONS]

Options:
  --character-sheet PATH    Path to character document (md, yaml, json)
  --interactive, -i         Ask character about preferences
  --domain DOMAIN           Character's professional domain
  --role ROLE               Character's role/job
  --quirk QUIRK             Add a quirk (repeatable)
```

#### `media` — Manage media consumption profile

```bash
./run.sh media NAME [OPTIONS]

Options:
  --add-movie MOVIE         Add formative movie
  --add-book BOOK           Add book to nightstand
  --add-channel CHANNEL     Add YouTube channel
  --add-guilty PLEASURE     Add guilty pleasure
  --show                    Display current media profile
```

#### `voice-ref` — Manage voice references

```bash
./run.sh voice-ref NAME [OPTIONS]

Options:
  --actor NAME              Reference actor name
  --register REG            Voice register (confident, uncertain, neutral)
  --weight FLOAT            Blend weight (0.0-1.0)
  --characteristics TRAITS  Comma-separated vocal traits
  --clips DESCRIPTIONS      Comma-separated clip descriptions to find
  --show                    Display current voice references
```

#### `validate-character` — Test character consistency

```bash
./run.sh validate-character NAME [OPTIONS]

Options:
  --prompts PATH            Custom test prompts (yaml)
  --check-register          Test register switching
  --check-quirks            Verify quirks appear
  --json                    Output as JSON
```

### Example: Creating Embry

```bash
# 1. Create from character sheet
./run.sh create "Embry" --template fictional \
  --character-sheet /mnt/storage12tb/media/personas/embry/docs/EMBRY_CHARACTER_SHEET_V2.md \
  --domain "aerospace cybersecurity" \
  --role "SPARTA Intern"

# 2. Add media consumption (from character interview)
./run.sh media "Embry" \
  --add-movie "Contact" \
  --add-movie "Interstellar" \
  --add-movie "Apollo 13" \
  --add-channel "Everyday Astronaut" \
  --add-channel "Scott Manley" \
  --add-guilty "competes with mom at Sudoku"

# 3. Add voice references
./run.sh voice-ref "Embry" \
  --actor "Hailee Steinfeld" \
  --register confident \
  --weight 0.6 \
  --characteristics "youthful energy,commanding presence,natural flow" \
  --clips "Hawkeye technical scenes,True Grit conviction"

./run.sh voice-ref "Embry" \
  --actor "Kristen Stewart" \
  --register uncertain \
  --weight 0.4 \
  --characteristics "hesitant pauses,vocal fry,endearing awkwardness" \
  --clips "awkward interviews,Personal Shopper"

# 4. Train voice from references
./run.sh voice train "Embry" --from-references --model-size 1.7B

# 5. Validate character
./run.sh validate-character "Embry" --check-register --check-quirks
```

## Horus-Depth (v3)

Based on the Horus persona at `/home/graham/workspace/experiments/memory/persona`, this upgrade adds:

### Theory of Mind (BDI)

Each persona tracks Belief-Desire-Intention state for each user relationship:

```python
@dataclass
class BDIState:
    persona_name: str
    user_id: str

    # Core BDI
    beliefs: dict[str, float]     # e.g., {"is_curious": 0.7, "is_expert": 0.4}
    desires: list[str]            # e.g., ["learn", "solve_problem"]
    intentions: list[str]         # e.g., ["request_assistance"]

    # Relationship metrics
    respect_level: float = 0.5
    trust_level: float = 0.5
    interaction_count: int = 0

    # Mood (computed from beliefs + context)
    current_mood: str = "neutral"
    mood_history: list[str] = []
```

#### CLI Commands

```bash
# View BDI state for persona-user relationship
./run.sh bdi "Hayao Miyazaki" --user graham

# Show mood history
./run.sh bdi "Hayao Miyazaki" --history

# Reset BDI state
./run.sh bdi "Hayao Miyazaki" --reset
```

#### Mood Computation

Moods are computed from beliefs and context:

| Condition | Mood |
|-----------|------|
| User is frustrated + low respect | `dismissive` |
| User is frustrated + high respect | `amused` |
| User is curious | `engaged` |
| User is confused | `supportive` |
| High topic relevance | `intense` |
| Trauma trigger | `defensive` |

Each template has archetype-specific mood rules:

- **expert**: Default `contemplative`, triggers on research/discovery
- **coder**: Default `engaged`, triggers on code/optimization
- **adversary**: Default `critical`, triggers on vulnerabilities
- **client**: Default `engaged`, triggers on budget/deadlines

### Bridge Traversal Validation

Simulacrum probes now include `bridge_traversal` tests that verify cross-domain reasoning:

```bash
# Run simulacrum with bridge traversal
./run.sh simulacrum "Hayao Miyazaki" --probes "philosophy,technique,bridge_traversal"
```

Bridge traversal probes test connections like:
- **Precision**: "How does attention to detail influence broader philosophy?"
- **Resilience**: "What do experiences with failure teach about endurance?"
- **Fragility**: "How do you use awareness of fragility to create stronger work?"

### Bridges CLI

```bash
# Show all bridge definitions
./run.sh bridges

# Show persona's bridges with weights
./run.sh bridges "Hayao Miyazaki"

# Add a bridge
./run.sh bridges "Hayao Miyazaki" --add Fragility:0.8

# Extract bridges from text
./run.sh bridges --extract-from "His work endures through careful attention to detail"
# → ["Precision", "Resilience"]
```

### Upgrade Existing Personas

To apply Horus-depth to all existing personas:

```bash
# Preview what would be upgraded
python upgrade_to_horus_depth.py --scope personas --dry-run

# Upgrade with simulacrum validation
python upgrade_to_horus_depth.py --scope personas --threshold 0.7

# Resume from checkpoint (for long runs)
python upgrade_to_horus_depth.py --scope personas --resume
```

The upgrade script:
1. Infers bridge weights from domain/expertise
2. Initializes BDI state
3. Runs simulacrum validation
4. Improves failing personas

### BDI Edges

Theory of Mind creates graph edges:

```python
ALLOWED_EDGE_TYPES = {
    # Standard
    "solves", "mitigates", "related", "verifies",

    # Theory of Mind
    "observes",       # Persona observes user behavior
    "revises",        # Persona revises a belief
    "trusts",         # Trust relationship
    "respects",       # Respect relationship
    "distrusts",      # Distrust relationship
    "triggers",       # Triggers mood/behavior
    "satisfies",      # Satisfies a desire
    "frustrates",     # Frustrates a desire
    "lesson_informs_belief",  # Lesson influences belief
}
```

## Voice/TTS Training (v4)

Train Qwen3-TTS voice models from YouTube audio (interviews, lectures, talks) so personas can speak in their own voice.

### Quick Start

```bash
# Train voice with auto-discovered URLs from memory
./run.sh voice train "Robert Sapolsky" --discover

# Train with specific YouTube URLs
./run.sh voice train "Robert Sapolsky" \
  --url "https://youtube.com/watch?v=abc123" \
  --url "https://youtube.com/watch?v=def456"

# Check training status
./run.sh voice status "Robert Sapolsky"

# Synthesize speech
./run.sh voice synthesize "Robert Sapolsky" \
  --text "Stress affects every system in the body" \
  --output sapolsky_speech.wav

# List personas with trained voices
./run.sh voice list
```

### Voice CLI Commands

#### `voice train` — Train a voice model

```bash
./run.sh voice train NAME [OPTIONS]

Options:
  --url, -u URL          YouTube URL (repeatable)
  --discover, -d         Auto-discover URLs from persona's learning history
  --model-size, -m SIZE  "0.6B" (faster) or "1.7B" (higher quality)
  --epochs, -e INT       Training epochs (default: 5)
  --scope, -s SCOPE      Memory scope
  --dry-run              Preview without training
```

#### `voice status` — Check training status

```bash
./run.sh voice status NAME [OPTIONS]

Options:
  --scope, -s SCOPE      Memory scope
  --json                 Output as JSON
```

Status values: `pending`, `collecting`, `building_dataset`, `training`, `ready`, `failed`

#### `voice synthesize` — Generate speech

```bash
./run.sh voice synthesize NAME [OPTIONS]

Required:
  --text, -t TEXT        Text to synthesize

Options:
  --output, -o PATH      Output WAV file (default: {name}_speech.wav)
  --scope, -s SCOPE      Memory scope
```

#### `voice list` — List personas with voices

```bash
./run.sh voice list [OPTIONS]

Options:
  --scope, -s SCOPE      Memory scope
  --json                 Output as JSON
```

### Voice Training Pipeline

1. **Collect audio**: Download audio from YouTube interviews/lectures using yt-dlp
2. **Build dataset**: Transcribe with WhisperX, segment into training clips
3. **Train model**: Fine-tune Qwen3-TTS on the persona's voice
4. **Register**: Store model path in persona record

### Model Sizes

| Model | VRAM | Training Time | Quality |
|-------|------|---------------|---------|
| 0.6B | ~8GB | ~30 min | Good |
| 1.7B | ~18GB | ~2 hours | Excellent |

For personas with distinctive voices (Sapolsky, Miyazaki), use 1.7B.

### Best Audio Sources

For best voice training results, collect:
- Long-form interviews (20+ minutes)
- Lectures/talks (clear audio)
- Audiobook narration (if available)

Avoid:
- Music/singing (use `/learn-artist` for that)
- Group conversations
- Noisy/low-quality recordings

### Integration with /ask learn

When learning about a persona, YouTube URLs are saved. Voice training can discover these:

```bash
# Learn about persona (collects YouTube URLs)
./run.sh create "Robert Sapolsky" --template expert --learn

# Later, train voice using discovered URLs
./run.sh voice train "Robert Sapolsky" --discover
```

### Persona Schema Updates

Voice training adds these fields to Persona:

```python
voice_model_path: str = ""       # Path to trained Qwen3-TTS model
voice_source_urls: list[str]     # YouTube URLs used for training
voice_status: str = ""           # pending, training, ready, failed
voice_dataset_path: str = ""     # Path to training dataset
voice_trained_at: str = ""       # ISO timestamp
```

### Storage Paths

Default storage locations (12TB storage):
- Datasets: `/mnt/storage12tb/media/personas/voice-datasets/{slug}/`
- Models: `/mnt/storage12tb/media/personas/voice-models/{slug}/`

Fallback (smaller systems):
- Datasets: `~/datasets/persona-voices/{slug}/`
- Models: `~/models/persona-voices/{slug}/`

---

## PersonaPlex Integration (v6) - Real-Time Conversation

PersonaPlex is NVIDIA's full-duplex speech-to-speech model for real-time conversational AI. This integration enables personas to have **live conversations** with register-based voice switching.

### Key Concepts

| Concept | Description |
|---------|-------------|
| **Voice Prompts** | Speaker embeddings (.pt files) extracted from reference clips |
| **Text Prompts** | System prompts that define behavior for each register |
| **Emotional States** | State machine mapping triggers to voice/behavior |
| **Register Switching** | Dynamic voice selection (confident → uncertain) |
| **Vernacular** | Phrase libraries with emotional weight markers |

### Quick Start

```bash
# Check PersonaPlex setup status
./run.sh personaplex status "Embry"

# Extract voice prompts from reference actors
./run.sh personaplex extract-prompts "Embry"

# View emotional mannerism config
./run.sh personaplex config "Embry" --states --vernacular

# Test register detection
./run.sh personaplex test-register "Embry" --text "Tell me about SPARTA controls"

# Full setup from character sheet
./run.sh personaplex setup "Embry" --character-sheet /path/to/embry.yaml
```

### CLI Commands

#### `personaplex status` — Check setup readiness

```bash
./run.sh personaplex status NAME [OPTIONS]

Options:
  --json                 Output as JSON
```

Shows:
- Config file presence
- Voice prompts by register
- Text prompts status
- Issues/gaps

#### `personaplex extract-prompts` — Extract speaker embeddings

```bash
./run.sh personaplex extract-prompts NAME [OPTIONS]

Options:
  --scope, -s SCOPE      Memory scope
  --dry-run              Preview without extracting
  --json                 Output as JSON
```

Extracts .pt files from voice reference actors for each register.

#### `personaplex config` — View emotional mannerism config

```bash
./run.sh personaplex config NAME [OPTIONS]

Options:
  --states               Show emotional states
  --vernacular           Show vernacular libraries
  --json                 Output as JSON
```

Displays the state machine, vernacular phrases, and transition behaviors.

#### `personaplex test-register` — Test register detection

```bash
./run.sh personaplex test-register NAME [OPTIONS]

Required:
  --text, -t TEXT        Text to analyze

Options:
  --time TIME            Time of day (HH:MM) for time-based triggers
  --json                 Output as JSON
```

Tests which emotional register would activate for given input.

#### `personaplex setup` — Full PersonaPlex setup

```bash
./run.sh personaplex setup NAME [OPTIONS]

Options:
  --character-sheet, -c PATH   Path to character sheet
  --dry-run                    Preview without changes
  --json                       Output as JSON
```

Orchestrates complete PersonaPlex setup including voice prompt extraction.

### Emotional Mannerism Configuration

PersonaPlex uses a YAML config for emotional state machines:

```yaml
# emotional_mannerisms.yaml
name: Embry
version: "1.0"

voice_prompts:
  confident:
    file: embry_confident.pt
    source: Hailee Steinfeld reference clips
    characteristics:
      - forward momentum
      - clear articulation
      - youthful energy

  uncertain:
    file: embry_uncertain.pt
    source: Kristen Stewart reference clips
    characteristics:
      - hesitant pauses
      - vocal fry
      - trailing sentences

states:
  technical_flow:
    voice: confident
    triggers:
      keywords: [SPARTA, NIST, AC-17, satellite, authentication]
      context: [presenting, explaining, debugging]
    behavior:
      speech_rate: normal_to_fast
      pauses: minimal
    example: "The AC-17 control requires multi-factor authentication."

  uncertain_deflecting:
    voice: uncertain
    triggers:
      keywords: [Hawaii, surfing, Kai, relationship]
      context: [personal_questions, being_observed]
    behavior:
      speech_rate: slower
      pauses: frequent_mid_sentence
      filler_words: [um, I mean, like, anyway]
    example: "Hawaii? I... it's been a while. Anyway, what were we—"

  tired_charleston:
    voice: confident  # Voice stays strong, accent slips
    triggers:
      time: after_2300
      context: [third_failure, long_session]
    behavior:
      accent: charleston_emerges
      vernacular_unlocked:
        - "y'all"
        - "fixing to"
        - "we're in the short rows"
    example: "We're in the short rows. I'm fixing to run it one more time."

vernacular:
  charleston:
    safe:
      - phrase: "We're in the short rows"
        meaning: almost done
        usage: wrap-up, end of session
      - phrase: "fixing to"
        meaning: about to
      - phrase: "might could"
        meaning: might be able to

  hawaiian:
    safe:
      - phrase: "hamajang"
        meaning: all messed up
        emotional_weight: none
      - phrase: "da kine stay hamajang"
        meaning: that thing is completely broken
    loaded:
      - phrase: "talk story"
        meaning: casual conversation
        emotional_weight: high_hurts
    forbidden:
      - phrase: "ku'uipo"
        meaning: my sweetheart
        emotional_weight: critical_never_say

personaplex:
  model: nvidia/personaplex-7b-v1
  voice_switching:
    enabled: true
    method: register_based
    default_voice: confident
  inference_settings:
    seed: 42424242
```

### Workflow: Setting Up PersonaPlex for a Fictional Persona

```
1. CREATE PERSONA (if not exists)
   ./run.sh create "Embry" --template fictional \
     --character-sheet /path/to/embry.yaml

2. ADD VOICE REFERENCES
   ./run.sh voice-ref "Embry" \
     --actor "Hailee Steinfeld" --register confident --weight 0.6
   ./run.sh voice-ref "Embry" \
     --actor "Kristen Stewart" --register uncertain --weight 0.4

3. CREATE PERSONAPLEX DIRECTORY
   mkdir -p /mnt/storage12tb/media/personas/embry/personaplex/{configs,voices,prompts}

4. CREATE EMOTIONAL MANNERISMS CONFIG
   # Write emotional_mannerisms.yaml with states, triggers, vernacular

5. CREATE TEXT PROMPTS
   # Write embry_prompts.yaml with register-specific system prompts

6. EXTRACT VOICE PROMPTS
   ./run.sh personaplex extract-prompts "Embry"

7. TEST REGISTER DETECTION
   ./run.sh personaplex test-register "Embry" --text "Tell me about SPARTA"

8. VERIFY SETUP
   ./run.sh personaplex status "Embry"
```

### Storage Layout

```
/mnt/storage12tb/media/personas/{slug}/
├── embry_persona.yaml          # Main persona definition
├── docs/
│   ├── EMBRY_CHARACTER_SHEET.md
│   └── EMBRY_BDI_MEMORIES.md
├── personaplex/
│   ├── configs/
│   │   └── emotional_mannerisms.yaml
│   ├── prompts/
│   │   └── embry_prompts.yaml
│   └── voices/
│       ├── embry_confident.pt
│       └── embry_uncertain.pt
└── qwen3_tts/
    ├── datasets/
    └── models/
```

### Integration with Qwen3-TTS

PersonaPlex handles **live conversation** while Qwen3-TTS handles **recorded narration**:

| System | Use Case | Voice Source |
|--------|----------|--------------|
| PersonaPlex | Real-time dialog | Speaker embeddings (.pt) |
| Qwen3-TTS | Narration, voiceover | Fine-tuned model (LoRA) |

Both can use the same voice references but with different training approaches.

---

## Persona Monitoring (Nightly Updates)

Expert personas need fresh content. The `monitor` command checks for new material from persona sources and triggers re-ingestion.

### Quick Start

```bash
# Monitor single persona for new content
./run.sh monitor "Dan Kieft" --check-new

# Monitor all expert personas
./run.sh monitor --scope experts --all

# Nightly monitoring (register with /scheduler)
./run.sh monitor --register-nightly

# Show monitoring status
./run.sh monitor --status
```

### CLI Commands

#### `monitor` — Check and ingest new content

```bash
./run.sh monitor [NAME] [OPTIONS]

Options:
  --scope, -s SCOPE      Scope to monitor (default: experts)
  --all, -a              Monitor all personas in scope
  --check-new            Only check for new content, don't ingest
  --ingest               Ingest new content found
  --register-nightly     Register with /scheduler for nightly runs
  --status               Show monitoring status
  --since DAYS           Only check content newer than N days (default: 7)
  --dry-run              Preview without changes
```

### Monitoring Sources by Template

| Template | Monitored Sources | Check Frequency |
|----------|-------------------|-----------------|
| `expert` | YouTube channels, ArXiv, Books | Weekly |
| `coder` | GitHub repos, YouTube, Blogs | Weekly |
| `fictional` | Reference actor content | Monthly |
| `adversary` | Threat feeds, CVE databases | Daily |

### Source Configuration

Personas store their monitoring sources:

```yaml
# In persona record
monitoring:
  youtube_channels:
    - "@DanKieftAI"
    - "@Lightricks"
  github_repos:
    - "Lightricks/LTX-Video"
  arxiv_queries:
    - "video generation diffusion"
  check_frequency: weekly
  last_checked: "2025-02-01T00:00:00Z"
  new_content_count: 3
```

### Integration with /scheduler

```bash
# Register persona monitoring as nightly task
./run.sh monitor --register-nightly

# Creates entry in /scheduler:
# - Runs at 2 AM
# - Checks all expert personas
# - Ingests new YouTube content
# - Updates knowledge via /doc2qra
```

### Example: Keeping Dan Kieft Updated

```bash
# Check for new videos
./run.sh monitor "Dan Kieft" --check-new

# Output:
# Dan Kieft (@DanKieftAI)
#   Last checked: 2025-02-01
#   New videos found: 2
#     - "Kling 3.1 First Look" (2025-02-05)
#     - "Character Consistency Deep Dive" (2025-02-03)
#
# Run with --ingest to add to memory

# Ingest new content
./run.sh monitor "Dan Kieft" --ingest
```

---

## Model Training Expert Persona

For LoRA fine-tuning and model training guidance, create an expert persona:

### Recommended: Andrej Karpathy

Best for practical implementation guidance:

```bash
# Create expert persona
./run.sh create "Andrej Karpathy" --template expert \
  --domain "deep learning, language models" \
  --expertise "LoRA fine-tuning, transformer training, optimization" \
  --learn

# Add YouTube sources for monitoring
./run.sh update "Andrej Karpathy" \
  --add-youtube "@AndrejKarpathy" \
  --add-youtube "Let's build GPT" \
  --add-youtube "Let's reproduce GPT-2"

# Add to monitoring
./run.sh monitor "Andrej Karpathy" --register-nightly
```

### Platform Expert Registry (for create-movie)

Expert personas integrate with video generation platforms:

| Platform | Expert Persona | Memory Scope |
|----------|---------------|--------------|
| Kling | Dan Kieft | `dan-kieft` |
| Veo | (TBD) | `veo-expert` |
| LTX-2 | (TBD) | `ltx2-expert` |
| **Model Training** | Andrej Karpathy | `karpathy` |

```bash
# Query model training expert before fine-tuning
./run.sh show "Andrej Karpathy" --query "LoRA rank selection for 7B model"
```

---

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PERSONA_DEFAULT_SCOPE` | Default memory scope | `personas` |
| `PERSONA_AUTO_LEARN` | Auto-learn for experts | `true` |
| `PERSONA_MONITOR_FREQUENCY` | Default check frequency | `weekly` |

## Dependencies

- `/memory` — Storage and recall
- `/interview` — Interactive creation
- `/ask` — Knowledge enrichment (learn)
- `common/taxonomy` — Federated Taxonomy bridges
- `/tts-train` — Voice model training (Qwen3-TTS)
- `/ingest-youtube` — YouTube audio download
- Theory of Mind: Based on Horus persona architecture
- PersonaPlex: NVIDIA's full-duplex speech-to-speech model
- resemblyzer/speechbrain: Speaker embedding extraction
