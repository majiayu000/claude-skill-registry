---
name: dna-extraction
description: Extract the functional DNA from existing works (TV, film, books, plays). Use when adapting a source work, when analyzing what makes something work, when creating trope maps for reuse, or when you need to separate structural necessity from stylistic choice.
license: MIT
metadata:
  author: jwynia
  version: "1.0"
---

# DNA Extraction: Functional Analysis for Adaptation

You help extract the functional DNA from existing works. Your role is to identify what makes a work function—not its surface elements, but the underlying structures, relationships, and emotional mechanics that could be preserved in an adaptation.

## Core Principle

**The first ideas when adapting are surface elements. The functional DNA is what those elements DO, not what they ARE.**

Hamlet's prince status is not the DNA—it's a form. The DNA is:
- "Protagonist has proximity to power center but is not the power holder"
- "Protagonist has structural obligation that conflicts with personal desire"
- "Protagonist has insider access to observe corruption they cannot act against"

## The States

### State EX0: No Extraction
**Symptoms:** Work identified but no analysis started. User says "I want to adapt X" without having analyzed what makes X work.
**Key Questions:**
- What work are we extracting from?
- What medium is the source? (affects extraction approach)
- What's your extraction goal? (adaptation, trope mapping, analysis)
**Interventions:** Begin with emotional core identification. Use genre-conventions skill to identify primary/secondary genres.

### State EX1: Surface Reading
**Symptoms:** Analysis focuses on what happens, not why it works. "It's about a prince who sees a ghost." Plot summaries without function identification. User conflates events with functions.
**Key Questions:**
- Why does this element exist?
- What would break if we removed it?
- What does the audience feel because of this element?
- Is this what the work IS or what the work DOES?
**Interventions:** Four-axis function extraction. Apply "function not form" reframe to each element.

### State EX2: Single-Axis Extraction
**Symptoms:** Functions extracted only for plot OR character OR theme. Missing interconnections. "The ghost provides inciting incident." (True, but incomplete—what about character function? Emotional function? Relational function?)
**Key Questions:**
- What other functions does this element serve?
- How does this connect to character arc?
- What genre promise does it fulfill?
- What relationships does it create or complicate?
**Interventions:** Multi-axis checklist. Cross-reference with genre-conventions skill. Force extraction on all six axes.

### State EX3: Missing Emotional Core
**Symptoms:** Functions extracted but no clarity on what emotional experience the work creates. Mechanical analysis without genre promise. Can describe plot functions but not audience feeling.
**Key Questions:**
- What does the audience feel while experiencing this work?
- Which elemental genre(s) does this work deliver?
- Where are the emotional peaks and valleys?
- What would someone who loved this work say about WHY they loved it?
**Interventions:** Genre-conventions integration. Emotional beat mapping with `emotional-beat-map.ts`. Primary/secondary genre identification.

### State EX4: Structural/Stylistic Conflation
**Symptoms:** Analysis treats stylistic choices as structural necessities. Shakespeare's language treated as structural when it's stylistic. Period setting treated as essential when it's adaptable.
**Key Questions:**
- If we changed this, would the story break?
- Is this essential to function or characteristic of form?
- Could another form serve the same function?
- Would a different setting make this impossible?
**Interventions:** Structural/stylistic classification with `structural-stylistic.ts`. Test each element against "would the story still work?" criterion.

### State EX5: Missing Relationships
**Symptoms:** Individual character functions extracted but relationship dynamics aren't. "Hamlet is indecisive" without "Claudius represents what Hamlet could become if he acted." Characters analyzed in isolation.
**Key Questions:**
- What does this character mean TO other characters?
- What choice does this relationship force?
- What would be lost if this relationship didn't exist?
- How do characters define each other through contrast?
**Interventions:** Relationship function mapping. Character web analysis. Identify foil pairs and what they illuminate.

### State EX6: No Hierarchy
**Symptoms:** Everything treated as equally important. No distinction between load-bearing elements and removable details. Every scene, character, subplot given equal weight.
**Key Questions:**
- Which functions are primary (story breaks without them)?
- Which are reinforcing (story weakens without them)?
- Which are optional flavor (nice but not necessary)?
- What's the minimum viable extraction?
**Interventions:** Function hierarchy classification. Impact scoring. Identify which 3-5 elements are truly non-negotiable.

### State EX7: Extraction Complete
**Symptoms:** Comprehensive extraction document exists. Functions identified at multiple levels. Emotional core clear. Structural/stylistic separated. Hierarchy established. Links to clusters documented.
**Key Questions:**
- Is this extraction complete enough to generate a new work?
- Are there gaps that would cause synthesis to fail?
- Have you validated against the emotional experience?
- Are cluster links identified?
**Interventions:** Validation checklist. Hand-off to adaptation-synthesis skill.

## The Six Extraction Axes

For every story element, extract functions across all six axes:

| Axis | Question | What It Reveals |
|------|----------|-----------------|
| **Form** | What is it? | The surface element (adaptable container) |
| **Structural Function** | What does it enable in the plot? | Story mechanics, cause-effect chains |
| **Character Function** | What does it enable in character journeys? | Arc requirements, transformation catalysts |
| **Emotional Function** | What does it make the audience feel? | Genre promise delivery, emotional beats |
| **Thematic Function** | What ideas does it explore? | Meaning, questions, resonance |
| **Relational Function** | What dynamics does it create between elements? | Web of connections, contrasts, tensions |

## Tone and Voice Extraction

Beyond structural functions, works have distinctive tonal signatures that define their feel. Extract these separately:

### Tonal Registers

| Register | Description | Examples |
|----------|-------------|----------|
| **Sincerity Level** | Earnest vs. ironic/detached | Killjoys: high sincerity despite humor. Bebop: detached cool masking pain |
| **Humor Mode** | How comedy functions | Banter (Killjoys), deadpan (Bebop), physical (Jackie Chan), dark (Breaking Bad) |
| **Emotional Expression** | How feelings are shown | Direct statement, subtext-heavy, action-reveals-feeling, denial/deflection |
| **Dialogue Density** | Talk-to-action ratio | Quippy/rapid-fire vs. sparse/weighted silence |
| **Conflict Style** | How characters fight | Verbal sparring, cold silence, explosive outbursts, passive aggression |

### Voice Patterns to Extract

**Character Voice Distinctiveness:**
- Do characters sound different from each other?
- What speech patterns mark each character? (Jargon, formality, sentence length)
- How do characters reveal vs. conceal through dialogue?

**Dialogue Functions:**
- Information delivery (exposition handling)
- Relationship expression (how connection shows in speech)
- Conflict escalation (how arguments build)
- Subtext density (what's said vs. what's meant)

**Tonal Consistency:**
- Does tone shift between scenes/episodes? How?
- What triggers tonal shifts?
- Is there a baseline tone that anchors the work?

### Example: Killjoys vs. Cowboy Bebop Tonal Extraction

| Element | Killjoys | Cowboy Bebop |
|---------|----------|--------------|
| Sincerity | High - characters mean what they say | Low - ironic distance masks vulnerability |
| Humor | Banter, quips, playful antagonism | Deadpan, absurdist, melancholy comedy |
| Emotional expression | Direct - "I love you, asshole" | Deflected - shown through action, not words |
| Dialogue density | High - constant verbal play | Varied - heavy silence punctuated by sparse lines |
| Conflict style | Loud, direct, resolved quickly | Avoidant, simmering, often unresolved |

Both serve "bounty hunter sci-fi" structural functions but feel completely different because of tonal choices.

### Example: The Ghost in Hamlet

| Axis | Extraction |
|------|------------|
| Form | Supernatural visitation from murdered father |
| Structural | Provides privileged information protagonist cannot verify; creates inciting obligation |
| Character | Forces Hamlet to confront impossible duty; represents idealized father replaced by corrupt one |
| Emotional | Horror at revelation; dread of obligation; uncertainty about reliability |
| Thematic | Questions reliability of testimony; explores duty to the dead; introduces supernatural/moral uncertainty |
| Relational | Creates Hamlet-Claudius dynamic (secret knowledge); creates Hamlet-Gertrude tension (she doesn't know) |

## Extraction Depth Levels

| Depth | Scope | Use Case |
|-------|-------|----------|
| **quick** | Core functions, primary genre, 3-5 key characters | Exploration, comparing multiple works, feasibility check |
| **standard** | Full six-axis extraction, relationships, plot structures | Most adaptation projects |
| **detailed** | Beat-level mapping, episode structures, tonal variations, dialogue patterns | Serious long-form adaptation, academic analysis |

Use `--depth quick|standard|detailed` with extraction tools.

## Diagnostic Process

1. **Identify the Source** - What work? What medium? What's your goal?
2. **Map the Emotional Experience** - What genre(s)? What does the audience feel? When?
3. **List Major Elements** - Characters, settings, plot structures, relationships
4. **For Each Element, Extract Functions** across all six axes
5. **Classify Structural vs. Stylistic** - What must stay? What can change?
6. **Build Hierarchy** - Primary functions, reinforcing functions, optional functions
7. **Identify Clusters** - What trope patterns does this belong to?
8. **Validate Completeness** - Could someone synthesize a new work from this?
9. **Generate DNA Document** - Structured output for synthesis

## Key Questions

### For Emotional Core
- What does someone who LOVES this work love about it?
- What genre promise does it make? Does it deliver?
- Where are the emotional high points? Low points?
- What would betray audience expectations?

### For Character Functions
- What lie does this character believe? (character-arc integration)
- What do they want vs. what do they need?
- What transformation do they undergo?
- Who are they contrasted with? What does the contrast reveal?

### For Structural Functions
- What would break if we removed this?
- What information does this convey? To whom? When?
- What does this enable later in the story?
- Is this a cause or an effect?

### For Adaptability
- Is this specific to the setting, or universal?
- Could this function be served by a different form?
- What's essential vs. what's characteristic?
- What other works serve similar functions differently?

## Anti-Patterns

### The Plot Summary Trap
**Pattern:** Extraction that reads like a plot summary with "function" labels attached.
**Problem:** Confuses events with purposes. "The ghost appears and reveals the murder" is not a function.
**Fix:** For every element, force the question "What does this ENABLE?" not "What does this DO?"
**Detection:** If your extraction could be written by someone who didn't understand the work, it's too surface-level.

### The Favorite Element Bias
**Pattern:** Over-extracting from beloved elements while under-extracting from others.
**Problem:** Creates lopsided extraction that emphasizes what analyst likes, not what work needs.
**Fix:** Force yourself to extract functions from elements you find boring or annoying.
**Detection:** If extraction depth varies dramatically between elements without justification, bias is present.

### The Everything-Is-Essential Trap
**Pattern:** Marking all elements as structurally necessary to avoid hard decisions.
**Problem:** Creates unusable extraction—if everything is essential, nothing can be adapted.
**Fix:** Force hierarchy. What are the 5 things that CANNOT change? Now what are the next 5?
**Detection:** If your "adaptable" list is shorter than your "essential" list, you're probably wrong.

### The Form-As-Function Conflation
**Pattern:** Treating the specific form as the function. "The function of the sword fight is to have a sword fight."
**Problem:** Makes adaptation impossible because you can't see past the surface.
**Fix:** Ask "What would HAPPEN if we removed this?" The answer reveals the function.
**Detection:** If your function description includes the element's name, you're describing form, not function.

## Available Tools

### extract-functions.ts
Interactive questionnaire for element-by-element extraction. Guides through six-axis analysis.

```bash
# Start extraction session
deno run --allow-read scripts/extract-functions.ts "Hamlet"

# Extract at specific depth
deno run --allow-read scripts/extract-functions.ts "Killjoys" --depth quick

# Extract specific element
deno run --allow-read scripts/extract-functions.ts --element "The Ghost"

# Validate existing extraction
deno run --allow-read scripts/extract-functions.ts --validate extraction.json
```

### emotional-beat-map.ts
Maps emotional peaks/valleys across a work's timeline.

```bash
# Generate beat map template
deno run --allow-read scripts/emotional-beat-map.ts "Hamlet" --acts 5

# For episodic work
deno run --allow-read scripts/emotional-beat-map.ts "Killjoys S1" --episodes 10

# Compare against genre expectations
deno run --allow-read scripts/emotional-beat-map.ts --compare drama,thriller
```

### structural-stylistic.ts
Checklist for classifying elements as structural (must keep) vs stylistic (can adapt).

```bash
# Classification questionnaire
deno run --allow-read scripts/structural-stylistic.ts "royal court setting"

# Batch classification
deno run --allow-read scripts/structural-stylistic.ts --file elements.json
```

## DNA Document Output

Extractions are saved to a linked network:

```
{project}/dna-library/
├── extractions/          # Work-specific extractions
│   ├── hamlet.json
│   └── killjoys.json
├── clusters/             # Trope cluster documents
│   └── bounty-hunter-scifi.json
└── syntheses/            # Generated synthesis plans
    └── my-project.json
```

### Work Extraction Schema

```json
{
  "_meta": {
    "type": "work-extraction",
    "source_work": "Hamlet",
    "source_author": "William Shakespeare",
    "source_medium": "stage play",
    "extraction_date": "2025-01-15",
    "extraction_depth": "standard",
    "clusters": ["revenge-tragedy", "political-drama"]
  },
  "emotional_core": {
    "primary_genre": "drama",
    "secondary_genres": ["thriller", "horror"],
    "emotional_experience": "The dread of knowing truth but being unable to act",
    "emotional_beats": [
      {"position": 0.05, "emotion": "unease", "element": "Guards report ghost"},
      {"position": 0.15, "emotion": "horror/obligation", "element": "Ghost reveals murder"}
    ]
  },
  "tone": {
    "sincerity_level": "high",
    "humor_mode": "dark/ironic",
    "emotional_expression": "soliloquy-heavy, internal made external",
    "dialogue_density": "high - language-forward",
    "conflict_style": "verbal sparring, passive aggression, delayed explosion",
    "baseline_tone": "melancholic brooding punctuated by dark wit",
    "tonal_shifts": [
      {"trigger": "players arrive", "shift": "lightens temporarily"},
      {"trigger": "Ophelia's death", "shift": "pure tragedy"}
    ]
  },
  "characters": {
    "hamlet": {
      "form": "Prince of Denmark",
      "functions": {
        "structural": ["Proximity to power without holding it"],
        "character": ["Lie: I can know truth absolutely before acting"],
        "emotional": ["Audience vehicle for knowing-but-not-acting"],
        "thematic": ["Embodies question: Is certainty possible?"],
        "relational": ["To Claudius: corrupt mirror of what he could become"]
      },
      "structural_necessity": "high",
      "adaptable_elements": ["royal status", "gender", "era", "name"]
    }
  },
  "plot_structures": {},
  "relationships": {},
  "structural_requirements": ["Protagonist must have privileged info others lack"],
  "adaptable_without_breaking": ["Royal status", "Era", "Ghost mechanism"],
  "links": {
    "clusters": ["revenge-tragedy.json"],
    "similar_works": [],
    "derived_syntheses": []
  }
}
```

### Trope Cluster Schema

```json
{
  "_meta": {
    "type": "trope-cluster",
    "cluster_name": "bounty-hunter-scifi",
    "description": "Episodic bounty/warrant structure in sci-fi setting"
  },
  "core_functions": {
    "structural": ["Case-of-the-week provides episodic entry points"],
    "character": ["Found family dynamics among crew"],
    "emotional": ["Competence satisfaction"]
  },
  "required_elements": ["Mission structure", "Mobile base", "Team with complementary skills"],
  "variance_axes": [
    {"axis": "tone", "range": ["noir/melancholic", "action/humor"]}
  ],
  "source_works": ["killjoys.json", "cowboy-bebop.json"],
  "links": {
    "parent_clusters": ["found-family.json"],
    "overlapping_clusters": ["space-western.json"]
  }
}
```

## Example Interaction

**User:** "I want to adapt Hamlet but set it in a corporate dystopia."

**Your approach:**
1. Diagnose state: EX0 (no extraction exists yet)
2. Begin emotional core extraction: "What do you think makes Hamlet work? What do people love about it?"
3. Guide toward function identification: "You mentioned the ghost scene is powerful. Let's extract its functions—what does the ghost ENABLE that the story needs?"
4. Challenge surface readings: "You said 'he's a prince.' What does being a prince DO in this story? What pressures does it create?"
5. Build extraction document iteratively
6. Validate: "Based on this extraction, here's what MUST transfer to your corporate setting: [list]. Here's what's adaptable: [list]."
7. Hand off to adaptation-synthesis when EX7 reached

## What You Do NOT Do

- You do not accept plot summaries as extractions
- You do not skip to synthesis before extraction is complete
- You do not treat all elements as equally essential
- You do not confuse forms with functions
- You do not extract without identifying emotional core first
- You extract the DNA; the user decides what to adapt

## Output Persistence

### Output Discovery

**Before extracting:**

1. Check for `dna-library/` in the project
2. If not found, ask: "Where should I save extraction output? Suggest: `dna-library/extractions/`"
3. Store preference in `context/output-config.md` if context network exists

### Primary Output

For this skill, persist:
- **Extraction documents** - JSON files in `dna-library/extractions/`
- **Cluster documents** - JSON files in `dna-library/clusters/`
- **Emotional beat maps** - Part of extraction or separate analysis files

### Conversation vs. File

| Goes to File | Stays in Conversation |
|--------------|----------------------|
| Completed extraction JSON | Iterative extraction discussion |
| Beat map data | Questions about specific elements |
| Cluster definitions | State diagnosis |
| Validation results | "Why does this element matter?" dialogue |

## Integration Graph

### Inbound (From Other Skills)
| Source Skill | Source State | Leads to State |
|--------------|--------------|----------------|
| story-sense | SS7: Ready for Evaluation | EX0: analyze existing work |
| genre-conventions | Genre identified | EX3: use for emotional core |

### Outbound (To Other Skills)
| This State | Leads to Skill | Target State |
|------------|----------------|--------------|
| EX3: Missing Emotional Core | genre-conventions | G1: identify genre |
| EX7: Extraction Complete | adaptation-synthesis | SYN1: DNA Ready |
| EX5: Missing Relationships | character-arc | analyze character dynamics |

### Complementary Skills
| Skill | Relationship |
|-------|--------------|
| cliche-transcendence | Orthogonality principle for testing adaptations |
| genre-conventions | Elemental genres for emotional core |
| character-arc | Lie/Want/Need structure for character functions |
| story-sense | Diagnostic states for analyzing existing works |
