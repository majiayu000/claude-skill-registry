---
name: empathic-templates
description: "Smart templates that understand semantic intent, not just string substitution"
license: MIT
tier: 1
allowed-tools:
  - read_file
  - write_file
related: [moollm, empathic-expressions, postel, yaml-jazz, skill, incarnation, character, coherence-engine]
tags: [moollm, generation, semantic, substitution, understanding]
---

# Empathic Templates

> *"Templates that understand what you mean, not just what you wrote."*

---

## What Is It?

**Empathic Templates** are MOOLLM's approach to template instantiation: templates that leverage LLM comprehension to understand **semantic intent**, not just perform mechanical string substitution.

Traditional templates: `{{name}}` → replace with literal value
Empathic templates: `{{name}}` → understand what name means in context, generate appropriate content

---

## The Difference

### Traditional Templates (Handlebars, Jinja, etc.)

```handlebars
Hello {{name}}!

Your order {{order_id}} has shipped.
Items: {{items}}
Total: ${{total}}
```

**Problem:** If `items` is a list, you need explicit loop syntax. If `total` should be formatted, you need filters. The template is dumb.

### Empathic Templates

```yaml
# The template understands context
greeting: "{{appropriate_greeting}}"
order_summary: "{{summarize_order_naturally}}"
items: "{{list_items_with_quantities}}"
total: "{{format_currency(total)}}"
```

The LLM doesn't just substitute — it **interprets**:
- `{{appropriate_greeting}}` becomes "Good morning, Sarah!" or "Hey there!" based on context
- `{{summarize_order_naturally}}` becomes prose, not data dump
- `{{list_items_with_quantities}}` formats intelligently

---

## How It Works

### 1. Parse Template

```yaml
template: |
  # {{character_name}}
  
  {{describe_appearance}}
  
  ## Personality
  {{personality_as_prose}}
  
  ## Catchphrase
  > "{{generate_catchphrase}}"
```

### 2. Understand Context

```yaml
context:
  character_type: "grumpy wizard"
  setting: "medieval fantasy"
  tone: "humorous"
  age: "ancient"
```

### 3. Semantic Generation

The LLM doesn't just fill slots — it **creates coherent content**:

```markdown
# Grumbald the Insufferable

A stooped figure wrapped in robes that were probably purple
once, before centuries of potion stains and cat hair took
their toll. His beard reaches his knees and contains at
least three quills, a small bird's nest, and what might be
a sandwich from the Third Age.

## Personality

Grumbald has perfected the art of making everyone feel
slightly stupid. He answers questions with questions,
sighs dramatically at simple requests, and has been
known to turn people into newts for using incorrect
grammar. Deep down, he cares — but he'd rather be
turned into a newt himself than admit it.

## Catchphrase

> "I've forgotten more magic than you'll ever know.
> Literally. Where did I put my staff?"
```

---

## Template Syntax

### Basic Slots

```yaml
{{variable}}           # Simple substitution (still works)
{{expression}}         # Empathic expression (interpreted)
{{#if condition}}      # Conditional (condition is interpreted)
{{#each items}}        # Iteration (smart about structure)
{{> partial}}          # Include another template
```

### Empathic Slots (The Magic)

```yaml
{{describe_X}}         # Generate description based on context
{{summarize_Y}}        # Create summary of data
{{generate_Z}}         # Create new content fitting context
{{appropriate_W}}      # Choose fitting value from possibilities
{{format_V}}           # Intelligent formatting
```

### Expressions with Empathic Interpretation

```yaml
{{#if character.is_hungry}}
  {{describe_hunger_behavior}}
{{/if}}

{{#if player.reputation > 50}}
  # The guard recognizes you
  {{guard_friendly_greeting}}
{{else}}
  # The guard is suspicious
  {{guard_suspicious_challenge}}
{{/if}}
```

The conditions use [Empathic Expressions](../empathic-expressions/) for flexible interpretation.

---

## Used For

### Character Creation

```yaml
# CHARACTER.yml.tmpl
id: {{generate_unique_id}}
name: "{{character_name}}"
species: "{{species}}"
description: |
  {{describe_appearance_based_on_species_and_personality}}

personality:
  {{infer_sims_traits_from_description}}

catchphrase: "{{generate_fitting_catchphrase}}"

backstory: |
  {{generate_backstory_consistent_with_setting}}
```

### Room Generation

```yaml
# ROOM.yml.tmpl
room:
  name: "{{room_name}}"
  type: {{room_type}}
  
  description: |
    {{describe_room_atmospherically}}
    
    {{describe_notable_features}}
    
    {{hint_at_secrets_if_any}}

  exits:
    {{generate_exits_based_on_maze_topology}}
    
  objects:
    {{place_appropriate_objects}}
```

### Session Logs

```yaml
# SESSION.md.tmpl
## Session {{session_number}} — {{session_date}}

### Summary
{{summarize_session_events}}

### Key Moments
{{list_memorable_moments}}

### State Changes
{{document_world_changes}}

### Next Steps
{{suggest_continuation_hooks}}
```

---

## The Empathic Expression Connection

Templates use Empathic Expressions for:

### Variables
```yaml
{{user.name}}                    # Simple lookup
{{user.status | capitalize}}     # With filter
{{player.has_item('key')}}       # Method call
```

### Conditions
```yaml
{{#if character.mood == 'happy'}}  # Exact match
{{#if character.is_friendly}}       # Boolean inference
{{#if gold > 100}}                  # Numeric comparison
{{#if player.can_afford(item)}}     # Method evaluation
```

### Iterations
```yaml
{{#each inventory.items}}
  - {{this.name}}: {{this.description}}
{{/each}}
```

### Code-Switching IN Templates
```yaml
# Generate SQL for the report
query: |
  {{empathic_sql: "get all users who ordered in the last month"}}

# Generate the email
email: |
  Dear {{user.name}},
  
  {{summarize_monthly_orders_naturally}}
  
  Total spent: {{format_currency(monthly_total)}}
```

---

## Template Discovery Pattern

**First 50 lines sniff:**

Templates should front-load:
1. Template metadata (name, purpose, required context)
2. Required variables list
3. Optional variables with defaults

```yaml
# CHARACTER.yml.tmpl — Character sheet template
# 
# Required context:
#   - character_name: string
#   - species: string  
#   - setting: string (e.g., "medieval fantasy")
#
# Optional context:
#   - personality_hints: list of traits
#   - backstory_seeds: key events to include
#   - tone: "serious" | "humorous" | "dark" (default: "neutral")

id: {{generate_unique_id}}
name: "{{character_name}}"
# ... rest of template
```

LLM can sniff first 50 lines to understand what the template needs before reading the full file.

---

## Comment Intelligence

The LLM distinguishes between **meta-comments** (instructions for generation) and **concrete comments** (meant for output):

### Meta-Comments (Stripped)

```yaml
# TEMPLATE: This section describes the character's appearance
# INSTRUCTION: Use vivid sensory details
# NOTE: Keep under 100 words
# TODO: Add more variety to hair colors
description: |
  {{describe_appearance}}
```

These are **instructions TO the LLM**. They guide generation but don't appear in output.

### Concrete Comments (Preserved)

```yaml
# This character was created using the incarnation protocol.
# See skills/incarnation/SKILL.md for details.
description: |
  {{describe_appearance}}

# Sims traits determine interaction success rates
sims_traits:
  {{generate_traits}}
```

These are **comments FOR the output file**. They explain the generated content to future readers.

### How the LLM Knows

| Indicator | Type | Action |
|-----------|------|--------|
| `# TEMPLATE:`, `# INSTRUCTION:`, `# NOTE:` | Meta | Strip |
| `# TODO:`, `# FIXME:` in template context | Meta | Strip |
| `# This explains...`, `# See also...` | Concrete | Preserve |
| Comments inside `{{...}}` blocks | Meta | Strip |
| Comments explaining generated values | Concrete | Preserve |
| ALL CAPS directive style | Meta | Strip |
| Lowercase explanatory style | Concrete | Preserve |

### Example: Mixed Comments

**Template:**
```yaml
# TEMPLATE: Character soul file
# INSTRUCTION: Generate YAML Jazz style comments

# This character was incarnated via the full autonomy protocol.
id: {{generate_id}}
name: "{{character_name}}"

# INSTRUCTION: Describe based on species and personality
description: |
  {{describe_appearance}}

# Personality traits affect all interactions
# Higher values = stronger tendency
sims_traits:
  nice: {{nice_value}}  # 0-10, affects social success
  # INSTRUCTION: Infer from description
  playful: {{infer_playful}}
```

**Generated Output:**
```yaml
# This character was incarnated via the full autonomy protocol.
id: palm-001
name: "Palm"

description: |
  A small capuchin monkey with knowing eyes and surprisingly
  dexterous fingers. Palm moves with the confidence of someone
  who has already seen how this story ends.

# Personality traits affect all interactions
# Higher values = stronger tendency
sims_traits:
  nice: 7  # 0-10, affects social success
  playful: 9
```

**What happened:**
- `# TEMPLATE:` and `# INSTRUCTION:` lines → **stripped**
- `# This character was incarnated...` → **preserved**
- `# Personality traits affect...` → **preserved**
- `# 0-10, affects social success` → **preserved**
- `# INSTRUCTION: Infer from description` → **stripped**

### The Principle

> **Meta-comments teach the generator. Concrete comments teach the reader.**

The LLM understands this distinction because it understands **intent**. Directive language instructs; explanatory language documents.

---

## Relationship to Self-Style Inheritance

Templates are **prototypes**. Instantiation creates **instances**:

```yaml
prototype: skills/character/CHARACTER.yml.tmpl
  ↓ instantiate with context
instance: examples/adventure-4/characters/animals/monkey-palm/CHARACTER.yml
```

The template defines **shape and intent**. The instance contains **specific values**.

But empathic templates go further: they generate **appropriate content**, not just fill slots.

---

## Examples

### Instantiating a Buff

```yaml
# BUFF.yml.tmpl
buff:
  id: {{buff_id}}
  name: "{{buff_name}}"
  type: {{buff_type}}
  
  description: |
    {{describe_buff_effect_flavorfully}}
  
  mechanics:
    duration: {{duration}}
    effect: "{{describe_mechanical_effect}}"
    
  trigger: "{{empathic_expression: trigger_condition}}"
  
  flavor_text: |
    {{generate_flavor_text_matching_setting}}
```

**Context:**
```yaml
buff_name: "Sugar Rush"
buff_type: positive
trigger_condition: "eating candy or sweet treats"
setting: "whimsical candy land"
```

**Generated:**
```yaml
buff:
  id: sugar-rush
  name: "Sugar Rush"
  type: positive
  
  description: |
    Your eyes widen, your heart races, and suddenly
    EVERYTHING IS AMAZING. Colors are brighter, sounds
    are sweeter, and you're pretty sure you could
    outrun a unicorn.
  
  mechanics:
    duration: 10 minutes
    effect: "+20% speed, +10% charisma, -10% focus"
    
  trigger: "consuming_sweet_treat"
  
  flavor_text: |
    *The sugar hits your bloodstream like a 
    candy-coated lightning bolt. WHEEEEE!*
```

---

## Templates as Schemas (CRITICAL!)

Templates are not just for instantiation — they ARE THE SCHEMA. The same `.tmpl` file serves as:

1. **Human documentation** — What fields exist, what they mean
2. **Machine schema** — Required vs optional, types, constraints
3. **Prototype definition** — Default values, inherited structure
4. **Code generation source** — Python dataclasses, JS classes, validators

### The Template-Schema Pattern

```yaml
# ADVENTURE.yml.tmpl — Adventure State Schema
# 
# REQUIRED fields (must be provided):
#   - adventure.name: string
#   - player.character: path
#   - navigation.starting_room: path
#
# OPTIONAL fields (can be omitted, inherited, or use defaults):
#   - parameters.*: all have sensible defaults
#   - party.members: defaults to [player.character]
#   - evidence.*: starts empty
#
# COMPUTED fields (LLM generates):
#   - adventure.started: timestamp
#   - selection.targets: starts []
```

### Smart Instantiation: The Drop Pattern

**Traditional:** Fill every slot, even if the value is default.

**Empathic:** DROP optional sections entirely if:
- The value equals the prototype default
- The context doesn't need it
- An abstract description is sufficient

```yaml
# Template has:
parameters:
  time:
    advancement: normal      # Default
  git:
    auto_commit: false       # Default
    auto_push: false         # Default
  debug:
    enabled: false           # Default
    # ...50 more lines of debug config...

# Smart instantiation DROPS the whole section:
# (No parameters block = use all defaults)

# Unless something differs:
parameters:
  debug:
    enabled: true            # Only what changed!
```

### Schema Markers in Templates

Use special comments to mark field requirements:

```yaml
# REQUIRED: Must be provided during instantiation
adventure:
  name: "{{adventure_name}}"           # REQUIRED
  objective: "{{quest_objective}}"     # REQUIRED
  status: active                       # OPTIONAL: has default

# OPTIONAL: Can be omitted entirely
evidence:                              # OPTIONAL: section
  clues: []                            # OPTIONAL: default []
  items: []                            # OPTIONAL: default []

# COMPUTED: Generated by LLM or system
statistics:                            # COMPUTED: section
  rooms_explored: 0                    # COMPUTED: auto-increment
  turns_elapsed: 0                     # COMPUTED: auto-increment

# INHERITED: Comes from prototype
parameters:                            # INHERITED: from simulation skill
  # Only override what differs from skills/simulation/defaults.yml
```

### Field Requirement Markers

| Marker | Meaning | Instantiation Behavior |
|--------|---------|----------------------|
| `# REQUIRED` | Must be filled | Error if missing |
| `# OPTIONAL` | Can be omitted | Drop if default or empty |
| `# OPTIONAL: default X` | Has default value | Drop if equals X |
| `# COMPUTED` | System generates | Never fill from context |
| `# INHERITED` | From prototype | Drop if unchanged |
| `# ABSTRACT` | Natural language OK | Keep as prose placeholder |

### Abstract Fields: Natural Language as Value

Sometimes the "value" is just a description of intent:

```yaml
# Template:
room:
  atmosphere: "{{atmosphere}}"         # ABSTRACT: describe the feeling

# Instantiation with abstract value (valid!):
room:
  atmosphere: |
    A sense of ancient mystery. Dust motes float in shafts of light 
    from high windows. Something important happened here, long ago.
    
# The LLM can work with this! It doesn't need structured data.
```

### Prototype Inheritance

Templates inherit from prototypes. Only override what differs:

```yaml
# skills/room/ROOM.yml.tmpl is the PROTOTYPE
# examples/adventure-4/maze/ROOM.yml is an INSTANCE

# The instance OMITS fields that match the prototype:
room:
  name: "Maze Entrance"     # DIFFERENT: specific name
  # purpose: omitted        # INHERITED: from prototype
  # working_set: omitted    # INHERITED: from prototype
  exits:
    north: corridor-1/      # DIFFERENT: specific exits
    east: dead-end/
  atmosphere: "Confusion and possibility"  # DIFFERENT: specific vibe
```

### Code Generation from Templates

Templates inform Python and JavaScript class generation:

```python
# adventure/schema.py — GENERATED FROM ADVENTURE.yml.tmpl

@dataclass
class Adventure:
    # REQUIRED fields (from template markers)
    name: str
    objective: str
    starting_room: str
    player_character: str
    
    # OPTIONAL fields (have defaults)
    status: str = "active"
    parameters: Optional[Parameters] = None  # Whole section optional
    
    # COMPUTED fields (not in __init__)
    started: str = field(init=False)
    turns_elapsed: int = field(init=False, default=0)
    
    # Unknown fields preserved for round-trip
    _extra: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        self.started = datetime.now().isoformat()
```

```javascript
// engine.js — GENERATED FROM templates

class Adventure {
  // REQUIRED
  name;        // string, must be set
  objective;   // string, must be set
  
  // OPTIONAL with defaults
  status = "active";
  parameters = null;  // null = use global defaults
  
  // COMPUTED (read-only, managed by engine)
  get started() { return this._started; }
  get turns_elapsed() { return this._turns; }
  
  constructor(data) {
    // Validate REQUIRED
    if (!data.name) throw new Error("Adventure requires name");
    if (!data.objective) throw new Error("Adventure requires objective");
    
    // Apply provided values
    Object.assign(this, data);
    
    // Preserve unknown fields
    this._extra = {};
    for (const [k, v] of Object.entries(data)) {
      if (!this.constructor.KNOWN_FIELDS.includes(k)) {
        this._extra[k] = v;
      }
    }
  }
}
```

### LLM Compilation Events

When the template contains expressions, emit events for the LLM to compile:

```yaml
# Template with expressions:
guard:
  allows_entry: "{{empathic_expression: player has the key OR player is known to guard}}"
  greeting: "{{generate: appropriate greeting based on player reputation}}"
  actions:
    - trigger: "{{when: player attempts to pass without permission}}"
      action: "{{do: block and challenge}}"
      score: "{{calculate: based on guard alertness and player stealth}}"
```

The `adventure.py` linter emits events:

```yaml
# Events for LLM compilation:
- event: COMPILE_EXPRESSION
  field: "guard.allows_entry"
  source: "player has the key OR player is known to guard"
  target_language: javascript
  expected_type: boolean
  output_field: "guard.allows_entry_js"  # Where to write the compiled expression
  # Naming convention: {field}_js for JavaScript, {field}_py for Python
  # The corresponding runtime classes know to eval these fields
  
- event: COMPILE_GENERATION
  field: "guard.greeting"
  instruction: "appropriate greeting based on player reputation"
  target_format: string
  context_needed: [player.reputation, guard.personality]
  
- event: COMPILE_SCORE
  field: "guard.actions[0].score"
  instruction: "based on guard alertness and player stealth"
  target_format: "number 0-100"
  inputs: [guard.alertness, player.stealth]
```

The LLM responds with compiled expressions, written to the `_js` or `_py` suffixed fields:

```yaml
# After LLM compilation, the YAML now contains:
guard:
  allows_entry: "player has the key OR player is known to guard"
  allows_entry_js: |
    (ctx) => ctx.player.inventory.includes('key') || 
             ctx.guard.knownPlayers.includes(ctx.player.id)
  allows_entry_py: |
    lambda ctx: 'key' in ctx.player.inventory or 
                ctx.player.id in ctx.guard.known_players
                
  greeting: "appropriate greeting based on player reputation"
  greeting_js: |
    (ctx) => {
      if (ctx.player.reputation > 80) return "Welcome back, friend!";
      if (ctx.player.reputation > 50) return "You may pass.";
      return "Halt! State your business.";
    }
```

### Output Field Naming Convention

| Field | Output Field (JS) | Output Field (Py) |
|-------|-------------------|-------------------|
| `allows_entry` | `allows_entry_js` | `allows_entry_py` |
| `score` | `score_js` | `score_py` |
| `guard.condition` | `guard.condition_js` | `guard.condition_py` |

The runtime classes know to look for these suffixed fields:

```javascript
// engine.js runtime
class Guard {
  checkEntry(ctx) {
    if (this.allows_entry_js) {
      return eval(this.allows_entry_js)(ctx);  // Use compiled
    }
    return this.evaluateEmpathic(this.allows_entry, ctx);  // LLM fallback
  }
}
```

```python
# schema.py runtime
class Guard:
    def check_entry(self, ctx):
        if self.allows_entry_py:
            return eval(self.allows_entry_py)(ctx)  # Use compiled
        return self.evaluate_empathic(self.allows_entry, ctx)  # LLM fallback
```

This creates a **graceful degradation** pattern:
1. If `_js` or `_py` exists → use fast compiled expression
2. If not → fall back to LLM interpretation of natural language

The same YAML file works in both compiled (fast) and interpreted (flexible) modes!

### The Full Template-to-Code Pipeline

```yaml
# Template-to-Code Pipeline
template_pipeline:
  - stage: "ADVENTURE.yml.tmpl"
    role: "Human-readable template/schema"
  - stage: "adventure.py lint"
    role: "Parse, validate, emit events"
    actions:
      - "Validate REQUIRED fields"
      - "Warn on missing OPTIONAL with no default"
      - "Emit COMPILE_EXPRESSION events"
      - "Emit COMPILE_GENERATION events"
      - "Emit COMPILE_SCORE events"
  - stage: "LLM receives events"
    role: "Compiles expressions"
  - stage: "adventure.py compile"
    role: "Generate output"
    outputs:
      - "adventure.json (minimal, machine-readable)"
      - "engine.js (with compiled expressions)"
      - "schema.py (Python classes for validation)"
      - "index.html (playable web app)"
```

### Validation and Linting

Templates enable automated validation:

```yaml
# Linter checks:
validation:
  required_present:
    - adventure.name
    - adventure.objective
    - player.character
    - navigation.starting_room
    
  type_checks:
    - field: simulation.turn
      type: integer
      min: 0
      
    - field: parameters.difficulty
      type: enum
      values: [easy, normal, hard]
      
  expression_checks:
    - field: guard.allows_entry
      must_compile_to: boolean
      
  path_checks:
    - field: player.character
      must_exist: true
      must_be_type: directory
```

### Example: Smart Instantiation

**Template (ROOM.yml.tmpl):**
```yaml
room:
  name: "{{name}}"                    # REQUIRED
  purpose: "{{purpose}}"              # OPTIONAL: default "general"
  created: "{{timestamp}}"            # COMPUTED
  
  context: []                         # OPTIONAL: default []
  cards_in_play: []                   # OPTIONAL: default []
  
  working_set:                        # INHERITED: from prototype
    - "ROOM.yml"
    - "README.md"
    - "state/*.yml"
    
  exits:                              # REQUIRED: at least one
    parent: "../"
    
  atmosphere: "{{atmosphere}}"        # ABSTRACT: natural language OK
```

**Minimal valid instantiation:**
```yaml
# Only what's needed and different:
room:
  name: "Wizard's Study"
  exits:
    parent: "../"
    down: secret-lab/
  atmosphere: "Dusty tomes and arcane instruments"
```

**What the linter infers:**
- ✅ `name` provided (REQUIRED)
- ✅ `exits` has at least one (REQUIRED)
- ⚡ `purpose` missing → use default "general"
- ⚡ `context` missing → use default []
- ⚡ `cards_in_play` missing → use default []
- ⚡ `working_set` missing → inherit from prototype
- ⚡ `created` missing → compute timestamp
- ✅ `atmosphere` is natural language (ABSTRACT valid)

---

## Anti-Pattern: Dumb Templates

**Don't do this:**
```yaml
description: "{{description}}"  # Just passes through
personality: "{{personality}}"  # No generation
```

**Do this:**
```yaml
description: |
  {{describe_character_based_on_traits_and_setting}}
  
personality:
  {{infer_traits_from_context}}
```

Let the LLM add value. That's the whole point.

---

## Anti-Pattern: Repeating Defaults

**Don't do this:**
```yaml
# Every room file repeats the same working_set:
working_set:
  - "ROOM.yml"
  - "README.md"
  - "state/*.yml"
```

**Do this:**
```yaml
# Omit working_set entirely — inherit from ROOM.yml.tmpl prototype
# Only include if this room has DIFFERENT requirements
```

Templates enable inheritance. Use it!

---

## Dovetails With

- [Empathic Expressions](../empathic-expressions/) — The expression engine
- [YAML Jazz](../yaml-jazz/) — Expressive data with comments
- [Skill](../skill/) — Templates as prototypes
- [Prototype](../prototype/) — Self-style inheritance patterns
- [Character](../character/) — Character sheet templates
- [Room](../room/) — Room generation templates
- [Adventure](../adventure/) — Adventure state templates
- [Postel](../postel/) — Generous interpretation in templates
- [Sister-Script](../sister-script/) — Templates drive code generation
- [Format-Design](../format-design/) — Templates ARE the schema

---

## Protocol Symbol

```
EMPATHIC-TEMPLATES
```

Invoke when: Instantiating templates with semantic understanding.

See: [PROTOCOLS.yml](../../PROTOCOLS.yml#EMPATHIC-TEMPLATES)
