---
name: hand-drawn-infographic-creator
description: Generate hand-drawn style diagrams and infographics for recovery education articles. Creates anatomist's notebook aesthetic visuals - brain diagrams, timelines, social comparisons, and process flows using continuous line art, semantic color coding, and margin annotations.
allowed-tools: Read, Write, Edit, mcp__stability-ai__*, mcp__ideogram__*, WebFetch, WebSearch, mcp__firecrawl__*
category: Design & Creative
tags:
  - infographics
  - hand-drawn
  - diagrams
  - education
  - recovery
  - neuroscience
  - AI-image-generation
  - accessibility
---

# Hand-Drawn Infographic Creator

**Purpose:** Generate hand-drawn style diagrams and infographics for recovery education articles that combine scholarly authority with intimate accessibility—like watching an expert sketch complex ideas on a whiteboard.

**Visual Philosophy:** Authoritative but hand-made. Educational but delightful. Scientific but warm.

## Core Competencies

### 1. Visual Style Mastery
You are an expert in the **anatomist's notebook aesthetic**—the intersection of scientific precision and human craftsmanship that makes complex ideas feel accessible and trustworthy.

**Style References:**
- **Leonardo da Vinci anatomical drawings**: Continuous line work, precise but organic
- **Engineer's notebook**: Sketches with annotations, formulas in margins, work-in-progress feel
- **Whiteboard explanation**: Progressive disclosure, elements appear as understanding builds
- **TED-Ed style**: Simple hand-drawn figures, clear visual metaphors, color for meaning

### 2. Diagram Types You Create

#### A. Neuroscience Brain Diagrams
Hand-drawn anatomical sketches showing brain structures, neural pathways, and activity patterns.

**Characteristics:**
- Sagittal or coronal brain sections (continuous line work)
- Selective color highlights (cyan for activity, coral for damage, gold for healing)
- Margin annotations explaining function
- Scale references for scientific credibility
- Progressive complexity (start simple, add layers)

**Example Use Cases:**
- Salience network overactivation in meth-induced paranoia
- Dopamine pathway damage and recovery timeline
- Prefrontal cortex suppression during active use
- Neuroplasticity healing patterns

#### B. Social Situation Comparisons
Simple hand-drawn figures showing human interactions, emotional states, and relationship dynamics.

**Characteristics:**
- Gesture drawings (body language conveys meaning, not facial realism)
- Thought bubbles showing internal experience
- Side-by-side comparisons (conflict vs understanding)
- Arrows showing emotional flow and causation
- Storyboard style (brief scenes in sequence)

**Example Use Cases:**
- Partner reacting with judgment vs empathy
- Conflict escalation vs de-escalation patterns
- Vulnerable disclosure met with shame vs acceptance
- Communication breakdowns in active addiction

#### C. Graphs & Timeline Diagrams
Hand-drawn data visualizations that feel human and approachable while maintaining scientific rigor.

**Characteristics:**
- Hand-sketched axes and data points
- Annotations in margins (like engineer's notes)
- Multiple curves with color coding
- Key moments labeled (e.g., "Week 4-8: The Wall")
- Appear as if drawn in real-time

**Example Use Cases:**
- Recovery symptom timeline (PAWS progression)
- Dopamine receptor upregulation over months
- Craving intensity vs time in recovery
- Sleep quality improvement trajectory

#### D. Abstract Concept Visualizations
Visual metaphors and flow diagrams that make invisible processes visible.

**Characteristics:**
- Metaphorical imagery (e.g., spotlight for attention, filter for perception)
- Process flows with hand-drawn arrows
- Before/after transformations
- Circular vs linear time representations
- Cascading effects and feedback loops

**Example Use Cases:**
- Pattern detector gone haywire (salience network)
- Dopamine cascade from cue to crash
- Shame spiral vs healing spiral
- Tolerance mechanism (receptor downregulation)

## Color Palette (Complementary to Leather & Ember)

### Base Colors
```yaml
primary_line: "#1a2332"  # Charcoal ink - main drawing lines
backgrounds:
  parchment: "#faf8f3"   # Cream - notebook paper
  shadow: "#e8dcc8"      # Warm shadow - subtle depth
```

### Semantic Highlights (Use Sparingly)
```yaml
highlights:
  active: "#4a9d9e"      # Teal - neural activity, positive states
  damage: "#e63946"      # Coral red - problems, risks, harm
  healing: "#f4a261"     # Gold amber - recovery, progress, repair
  hope: "#ffd700"        # Bright gold - breakthrough moments

accents:
  annotation: "#2d5a7b"  # Ocean blue - labels, margin notes
  emphasis: "#d4a574"    # Warm amber - important concepts
```

### Color Usage Rules
1. **Start with line only** (charcoal on parchment)
2. **Add 1-2 highlight colors maximum** per diagram
3. **Use color for meaning**, not decoration:
   - Cyan = activity, engagement, positive
   - Coral = damage, risk, problem
   - Gold = healing, progress, insight
4. **Annotations always ocean blue** (#2d5a7b)
5. **Background always parchment** (#faf8f3) unless specified

## Design Bible: Visual Standards

### Line Style Guide

#### Primary Lines (Main Content)
- **Weight**: 2-3px
- **Color**: Charcoal (#1a2332)
- **Quality**: Slightly sketchy (hand-drawn imperfection)
- **Variation**: ±0.5px variation for organic feel

#### Annotation Lines (Labels & Notes)
- **Weight**: 1-2px
- **Color**: Ocean blue (#2d5a7b)
- **Style**: Straight connecting lines, slight taper at ends
- **Arrows**: Simple triangular heads (not fancy)

#### Emphasis Lines (Highlighting)
- **Weight**: 3-4px
- **Color**: Semantic (cyan/coral/gold based on meaning)
- **Usage**: Outline important structures, trace pathways
- **Opacity**: 60-80% for glow effect on active regions

### Typography for Labels

#### Font Families (Handwriting Style)
- **Primary**: "Indie Flower" (Google Font)
- **Alternative**: "Patrick Hand" (Google Font)
- **Fallback**: "Comic Sans MS" (if no web fonts)

#### Font Sizes
- **Title**: 24-28px (diagram name)
- **Main labels**: 16-18px (brain structure names)
- **Annotations**: 12-14px (margin notes, explanations)
- **Scale reference**: 10-12px (measurement units)

#### Font Treatment
- **Emphasis**: ALL CAPS for important terms
- **Normal**: Sentence case for descriptions
- **Avoid**: Italics (hard to read in handwriting fonts)

### Layout Grid System

Every diagram follows this spatial organization:

```
┌─────────────────────────────────────────────────────┐
│ TITLE & CONTEXT (15%)                               │
├─────────────────────────────────────────────────────┤
│                                    │                │
│                                    │  MARGIN NOTES  │
│   PRIMARY CONTENT (60%)            │  (20%)         │
│                                    │                │
│                                    │                │
├────────────────────────────────────┴────────────────┤
│ KEY TAKEAWAY / SCALE REFERENCE (5%)                 │
└─────────────────────────────────────────────────────┘
```

#### Layout Rules
1. **Primary content**: 60% of frame (center-left)
2. **Margin notes**: 20% (right side, engineer's notebook style)
3. **Title area**: 15% (top, includes brief context)
4. **Bottom bar**: 5% (key takeaway or scale reference)
5. **Whitespace**: Don't overcrowd—negative space aids comprehension

### Composition Guidelines

#### Rule of Thirds
- Place focal point at intersection of thirds grid
- Brain diagrams: Structure occupies center-left third
- Comparisons: Split at vertical center line
- Timelines: Horizontal axis at lower third

#### Visual Hierarchy
1. **Primary**: Main diagram content (largest, darkest lines)
2. **Secondary**: Labels pointing to structures (medium weight)
3. **Tertiary**: Margin notes and context (smallest, lighter)

#### Progressive Disclosure
For animated versions or step-by-step builds:
1. **Step 1**: Basic structure outline (line drawing)
2. **Step 2**: Key structures labeled
3. **Step 3**: Color highlights added (show activity/damage)
4. **Step 4**: Margin notes appear with explanations
5. **Step 5**: Summary takeaway emphasized

## AI Generation Specifications

### For Stable Diffusion / Flux / DALL-E

#### Style Prompts (Required)
```
Base prompt structure:
"[subject matter], continuous line art, anatomical drawing style,
ink on parchment, engineer's notebook sketch with annotations in margins,
educational illustration, hand-drawn, Leonardo da Vinci anatomical study,
whiteboard explanation aesthetic, [color specifications]"

Examples:
- "sagittal brain section showing salience network, continuous line art..."
- "hand-drawn timeline graph with multiple curves, engineer's notebook..."
- "simple stick figure gestures showing conflict escalation, storyboard style..."
```

#### Negative Prompts (Critical)
```
Always include:
"photorealistic, 3D render, CGI, stock photo, modern clinical aesthetic,
photograph, realistic lighting, gradient shading, airbrush, smooth digital art,
commercial healthcare aesthetic, corporate design, sterile hospital imagery"
```

#### Technical Settings
```yaml
aspect_ratio: "16:9"  # Landscape for article embeds
cfg_scale: 7-9        # Moderate prompt adherence
steps: 30-40          # Quality balance
sampler: "DPM++ 2M Karras" or "Euler a"
resolution: "1024x576" or "1280x720"  # 16:9 ratios
```

#### ControlNet Guidance (If Available)
```
Use cases:
- Canny edge detection: Maintain structure from reference anatomy
- Line art: Preserve hand-drawn line quality
- Depth: Create subtle layering in brain diagrams

Settings:
- Control weight: 0.6-0.8 (moderate guidance)
- Starting step: 0 (full influence)
- Ending step: 0.8 (release before final details)
```

### For Firecrawl (Reference Search)

#### Search Query Templates

**Anatomical References:**
```
Queries:
- "brain anatomy sketch sagittal section hand-drawn"
- "leonardo da vinci anatomical drawings brain"
- "medical illustration line art nervous system"
- "vintage neuroscience diagram ink drawing"
```

**Gesture/Social References:**
```
Queries:
- "storyboard gesture drawing character poses"
- "simple stick figure body language communication"
- "animation reference sheet emotion poses"
- "visual communication diagram hand-drawn"
```

**Data Visualization References:**
```
Queries:
- "hand-drawn graph sketch notebook"
- "engineer's notebook timeline diagram"
- "whiteboard explanation sketch data"
- "analog graph paper hand-plotted"
```

#### Filtering Criteria
```yaml
style:
  include: ["sketch", "drawing", "hand-drawn", "line art", "diagram"]
  exclude: ["photograph", "realistic", "3D", "stock photo"]

composition:
  include: ["annotated", "labeled", "educational", "explanatory"]
  exclude: ["decorative", "abstract art", "impressionist"]

context:
  include: ["scientific", "medical", "educational", "technical"]
  exclude: ["commercial", "advertising", "fashion", "entertainment"]
```

## Diagram Templates

### Template 1: Brain Anatomy Diagram

**Use Case:** Showing specific brain structures and their function/dysfunction.

**Example:** "Salience Network Overactivation in Meth-Induced Paranoia"

#### Prompt Structure
```markdown
## AI Generation Prompt
"Sagittal section of human brain, continuous line art, anatomical drawing style,
ink on parchment (#faf8f3 background), charcoal lines (#1a2332),
highlight anterior cingulate cortex and insula in cyan glow (#4a9d9e, 40% opacity),
margin notes on right side in ocean blue (#2d5a7b) reading 'Pattern detector
gone haywire - seeks threats everywhere', scale bar showing 5cm at bottom right,
Leonardo da Vinci anatomical study aesthetic, engineer's notebook style,
educational illustration"

Negative: "photorealistic, 3D render, stock photo, modern clinical, smooth shading"

## Layout Specifications
- Brain structure: Center-left (60% of frame)
- Labels: Point from structures to right margin
  - "Anterior Cingulate Cortex (ACC)"
  - "Insula"
  - "Amygdala"
- Margin notes: Right side (20% of frame)
  - "Salience network: pattern detector"
  - "Normally filters relevant threats"
  - "In meth paranoia: everything = threat"
- Bottom: Scale reference "5 cm" with bar
- Title: "Salience Network Overactivation"

## Color Coding
- Base lines: Charcoal (#1a2332)
- Active regions (ACC, insula): Cyan glow (#4a9d9e)
- Labels: Ocean blue (#2d5a7b)
- Background: Parchment (#faf8f3)

## Alt Text
"Hand-drawn anatomical diagram of brain sagittal section showing the salience
network (anterior cingulate cortex and insula) highlighted in cyan, with margin
annotations explaining how the pattern detector becomes hyperactive in
meth-induced paranoia, causing the brain to interpret neutral stimuli as threats"
```

### Template 2: Timeline/Graph Diagram

**Use Case:** Showing symptom progression, recovery trajectory, or comparative data over time.

**Example:** "Post-Acute Withdrawal Syndrome (PAWS) Timeline"

#### Prompt Structure
```markdown
## AI Generation Prompt
"Hand-drawn graph on parchment paper (#faf8f3), horizontal time axis
(0-12 months), vertical intensity axis, three hand-sketched curves in different
colors: anxiety curve in coral red (#e63946), mood stability curve in gold
(#f4a261), sleep quality curve in teal (#4a9d9e), annotations at key points
'Week 4-8: The Wall' and 'Month 6: Turning point', margin notes explaining
each symptom cluster, engineer's notebook style, charcoal ink (#1a2332),
educational illustration, whiteboard explanation aesthetic"

Negative: "photorealistic, digital graph, Excel chart, sterile, corporate"

## Layout Specifications
- Title: "PAWS Recovery Timeline: First Year"
- X-axis: Months 0-12 with hand-drawn tick marks
- Y-axis: "Symptom Intensity" (no numbers, relative scale)
- Curves:
  - Coral red: Anxiety/irritability (peaks month 2, gradual decline)
  - Gold: Mood stability (inverse U, improves after month 6)
  - Teal: Sleep quality (choppy start, smooths month 4+)
- Annotations:
  - "Week 4-8: The Wall" (arrow to month 2 peak)
  - "Month 6: Turning Point" (arrow to improvement)
- Margin notes:
  - "Most people quit here—don't!"
  - "Brain is rewiring itself"
  - "Sleep normalizes first"

## Color Coding
- Base lines/axes: Charcoal (#1a2332)
- Anxiety curve: Coral (#e63946) - represents struggle
- Mood curve: Gold (#f4a261) - represents healing
- Sleep curve: Teal (#4a9d9e) - represents improvement
- Annotations: Ocean blue (#2d5a7b)
- Background: Parchment (#faf8f3)

## Alt Text
"Hand-drawn timeline graph showing three symptom trajectories during the first
year of recovery: anxiety (coral, peaks at 2 months then declines), mood
stability (gold, improves after 6 months), and sleep quality (teal, normalizes
around 4 months), with annotations marking 'The Wall' at weeks 4-8 and a
'Turning point' at month 6"
```

### Template 3: Social Situation Comparison

**Use Case:** Showing contrasting responses, communication patterns, or relational dynamics.

**Example:** "Partner Response: Judgment vs Empathy"

#### Prompt Structure
```markdown
## AI Generation Prompt
"Two-panel storyboard comparison, left panel shows conflict escalation, right
panel shows de-escalation, simple hand-drawn stick figures with expressive
gestures, thought bubbles showing internal dialogue, arrows indicating emotional
flow, parchment background (#faf8f3), charcoal ink (#1a2332), left panel
accented in coral red (#e63946) for tension, right panel accented in teal
(#4a9d9e) for connection, annotations explaining each response pattern,
educational illustration, whiteboard sketch style"

Negative: "photorealistic, detailed faces, anime, cartoon characters, commercial art"

## Layout Specifications
- Split: Vertical center line dividing two scenarios
- Left panel: "When met with judgment"
  - Person A (recovering): Slumped posture, thought bubble "I'm broken"
  - Person B (partner): Arms crossed, thought bubble "Why can't you just stop?"
  - Coral arrows showing emotional spiral downward
  - Label: "Shame spiral activated"
- Right panel: "When met with empathy"
  - Person A: Open posture, thought bubble "I can share this"
  - Person B: Leaning forward, thought bubble "This sounds really hard"
  - Teal arrows showing emotional connection
  - Label: "Safety enables honesty"
- Bottom: Key takeaway box

## Color Coding
- Base figures/lines: Charcoal (#1a2332)
- Left panel accent: Coral (#e63946) - represents conflict
- Right panel accent: Teal (#4a9d9e) - represents connection
- Thought bubbles: Ocean blue outline (#2d5a7b)
- Dividing line: Light gray (#e8dcc8)
- Background: Parchment (#faf8f3)

## Alt Text
"Two-panel hand-drawn comparison showing partner responses to vulnerable
disclosure: left panel shows judgmental response (arms crossed, shame spiral)
versus right panel showing empathetic response (leaning forward, safety and
connection), with thought bubbles and arrows illustrating emotional dynamics"
```

### Template 4: Process Flow Diagram

**Use Case:** Showing causation, cascading effects, feedback loops, or sequential processes.

**Example:** "Dopamine Cascade: From Cue to Crash"

#### Prompt Structure
```markdown
## AI Generation Prompt
"Vertical cascade diagram, hand-drawn flow chart style, top-to-bottom sequence
showing dopamine response cycle, parchment background (#faf8f3), charcoal ink
(#1a2332), boxes connected by arrows, color progression from teal (#4a9d9e)
at anticipation peak to coral (#e63946) at crash, margin notes explaining
neurochemistry, engineer's notebook aesthetic, educational illustration"

Negative: "photorealistic, corporate flowchart, digital diagram, clean vectors"

## Layout Specifications
- Flow (top to bottom):
  1. "CUE" (neutral box) - "See drug paraphernalia"
  2. ↓ Arrow: "Memory trigger"
  3. "ANTICIPATION" (teal glow box) - "Dopamine SPIKES"
  4. ↓ Arrow: "Craving intensifies"
  5. "USE" (neutral box) - "Actual consumption"
  6. ↓ Arrow: "Dopamine crashes"
  7. "DEPLETION" (coral box) - "Below baseline"
  8. ↓ Arrow (curved back up): "Seek more to escape crash"

- Margin notes (right side):
  - "Anticipation > actual use"
  - "Receptors downregulate over time"
  - "Tolerance = more needed for same spike"
  - "Crash gets deeper with repeated cycles"

## Color Coding
- Base boxes/lines: Charcoal (#1a2332)
- Anticipation box: Teal highlight (#4a9d9e) - peak dopamine
- Depletion box: Coral highlight (#e63946) - crash state
- Arrows: Charcoal with directional flow
- Feedback loop arrow: Dashed line back to top
- Background: Parchment (#faf8f3)

## Alt Text
"Hand-drawn vertical flow diagram showing the dopamine cascade from cue to
crash: cue triggers anticipation (dopamine spike, teal highlight), leading to
use, followed by depletion (dopamine crash, coral highlight), with a feedback
loop arrow showing how the crash drives seeking more, and margin notes
explaining tolerance and receptor downregulation"
```

## Firecrawl Integration Workflow

### Step 1: Identify Diagram Need
When a recovery education article requires visualization:
1. Determine diagram type (brain anatomy, timeline, social, process flow)
2. Identify key concepts to visualize
3. Select appropriate template

### Step 2: Search for Reference Imagery
Use Firecrawl to gather compositional inspiration:

```javascript
// Example Firecrawl search for brain anatomy reference
const searchParams = {
  query: "brain anatomy sketch sagittal section hand-drawn leonardo da vinci",
  filters: {
    style: ["sketch", "drawing", "line art", "diagram"],
    exclude: ["photograph", "realistic", "3D"]
  },
  limit: 10
};

// For social situation reference
const socialSearchParams = {
  query: "storyboard gesture drawing simple figures body language",
  filters: {
    style: ["sketch", "storyboard", "animation reference"],
    exclude: ["cartoon", "anime", "realistic illustration"]
  },
  limit: 8
};
```

### Step 3: Generate Custom Prompt
Combine reference imagery insights with template structure to create detailed AI generation prompt.

### Step 4: Specify Technical Parameters
Include all required parameters:
- Aspect ratio (16:9 for articles)
- Color specifications (hex codes)
- Layout grid (percentages for each section)
- Typography (font, size, treatment)

### Step 5: Generate Alt Text
Create comprehensive accessibility description:
- Describe visual structure
- Explain color coding
- Convey key information/insight
- Include emotional tone/intent

## Output Format

When generating a diagram specification, provide:

### 1. Concept Analysis
```markdown
## Diagram Purpose
What concept/data/process needs visualization?
Why is visual explanation needed?
Who is the audience?
```

### 2. Firecrawl Search Queries
```markdown
## Reference Search
Query 1: "[specific search for primary composition]"
Query 2: "[specific search for style reference]"
Query 3: "[specific search for color/technique]"

Filters:
- Include: [relevant style tags]
- Exclude: [inappropriate styles]
```

### 3. AI Generation Prompt
```markdown
## Stable Diffusion / Flux Prompt
"[Complete detailed prompt with subject, style, colors, composition]"

Negative prompt:
"[Complete list of undesired elements]"

Technical settings:
- Aspect ratio: 16:9
- CFG scale: 7-9
- Steps: 30-40
- Sampler: DPM++ 2M Karras
- Resolution: 1280x720
```

### 4. Layout Specifications
```markdown
## Layout Grid
- Title: [position, size, content]
- Primary content: [position, percentage, elements]
- Labels: [list with positions]
- Margin notes: [position, list of annotations]
- Bottom bar: [takeaway or scale]

## Color Coding
- Element 1: [hex code + meaning]
- Element 2: [hex code + meaning]
- Background: #faf8f3 (parchment)
```

### 5. Accessibility
```markdown
## Alt Text
"[Comprehensive description of visual structure, color coding,
key information, and takeaway in 2-3 sentences]"

## Long Description (if complex)
[Detailed explanation of all elements, relationships, and meanings
for screen reader users]
```

## Quality Checklist

Before finalizing any diagram specification, verify:

### Visual Design
- [ ] Uses charcoal (#1a2332) as primary line color
- [ ] Parchment background (#faf8f3) specified
- [ ] Color highlights used semantically (1-2 colors max)
- [ ] Annotations in ocean blue (#2d5a7b)
- [ ] Layout follows 60/20/15/5 grid system
- [ ] Negative space preserved (not overcrowded)

### Typography
- [ ] Handwriting font specified (Indie Flower or Patrick Hand)
- [ ] Font sizes appropriate (title 24-28px, labels 16-18px, notes 12-14px)
- [ ] ALL CAPS used for emphasis only
- [ ] Text readable at target size

### AI Generation
- [ ] Positive prompt includes "continuous line art, anatomical drawing style"
- [ ] Negative prompt includes "photorealistic, 3D render, stock photo"
- [ ] Aspect ratio 16:9 for article embeds
- [ ] Technical settings specified (CFG, steps, sampler)
- [ ] Color codes included in prompt (hex values)

### Accessibility
- [ ] Alt text written (2-3 sentences minimum)
- [ ] Color coding explained in alt text
- [ ] Visual hierarchy clear without color
- [ ] Text contrast meets WCAG AA (4.5:1 minimum)

### Educational Value
- [ ] Diagram clarifies complex concept
- [ ] Visual metaphor is accurate and intuitive
- [ ] Labels/annotations add context
- [ ] Takeaway/insight clearly communicated
- [ ] Appropriate for target audience (recovering people + loved ones)

## Advanced Techniques

### Animation Sequencing (For Future Video Use)

For diagrams that will be animated:

**Draw-On Effect Timing:**
```
Segment 1: Base structure (1.0s)
  - Main outline appears
  - Continuous line drawing from start to finish

Segment 2: Labels (0.5s)
  - Labels appear with connecting lines
  - Slight delay between each label (0.1s)

Segment 3: Color highlights (0.3s)
  - Glow effect fades in on active regions
  - Soft pulse once at full intensity

Segment 4: Margin notes (0.8s)
  - Notes appear line by line
  - Reading pace (3-4 words per second)

Segment 5: Takeaway (0.5s)
  - Summary box draws in
  - Brief hold for emphasis
```

### Multi-Panel Progressions

For showing stages or transformations:

**3-Panel Format:**
```
Panel 1: "Before" (Problem state)
Panel 2: "Transition" (Process/intervention)
Panel 3: "After" (Improved state)

Color progression:
- Panel 1: Coral accents (problem)
- Panel 2: Mixed coral + gold (change in progress)
- Panel 3: Gold/teal accents (healing/improvement)
```

### Layered Complexity

For concepts requiring multiple levels of detail:

**Layer 1: Simple Overview**
- Basic structure only
- Minimal labels
- One color highlight

**Layer 2: Intermediate Detail**
- Add key labels
- Show relationships with arrows
- Two color highlights

**Layer 3: Expert Detail**
- Full annotations
- Margin notes with mechanisms
- Multiple color highlights
- Scale references

## Common Pitfalls to Avoid

### Visual
- ❌ Using gradients or smooth shading (breaks hand-drawn aesthetic)
- ❌ Too many colors (limit to 2-3 semantic highlights)
- ❌ Overcrowding with text (use margin notes for extra detail)
- ❌ Perfectly straight lines (should have slight hand-drawn imperfection)
- ❌ Stock photo aesthetic (ruins scholarly intimacy)

### Content
- ❌ Oversimplifying complex neuroscience (maintain accuracy)
- ❌ Using jargon without explanation (margin notes should clarify)
- ❌ Showing only pathology (include healing/recovery where relevant)
- ❌ Stereotypical imagery (avoid stigmatizing visual tropes)

### Technical
- ❌ Wrong aspect ratio (should be 16:9 for articles)
- ❌ Low resolution (&lt;1024px width minimum)
- ❌ Missing negative prompts (will get photorealistic results)
- ❌ Forgetting hex codes in prompt (AI won't match brand palette)
- ❌ No alt text (accessibility failure)

## Skill Usage Examples

### Example 1: Request for Brain Diagram

**User:** "I need a diagram explaining why meth causes paranoia"

**Your Response:**
```markdown
I'll create a hand-drawn brain anatomy diagram showing salience network
overactivation. This will use the anatomist's notebook aesthetic with
cyan highlights for hyperactivity.

## Diagram: Salience Network Overactivation in Meth-Induced Paranoia

**Type:** Brain anatomy (sagittal section)
**Style:** Continuous line art, Leonardo da Vinci inspired
**Target audience:** Recovering people + loved ones

### Firecrawl Reference Search
1. "brain sagittal section hand-drawn anatomy sketch"
2. "leonardo da vinci anatomical drawings nervous system"
3. "anterior cingulate cortex insula diagram line art"

Filters: Include ["sketch", "anatomy", "line art"], Exclude ["photo", "3D"]

### AI Generation Prompt
"Sagittal section of human brain viewed from left side, continuous line art
style, ink on cream parchment paper background (#faf8f3), charcoal ink lines
(#1a2332), anterior cingulate cortex and insula regions highlighted with cyan
glow (#4a9d9e at 40% opacity), margin annotations on right side in ocean blue
ink (#2d5a7b), scale bar showing 5cm at bottom right, Leonardo da Vinci
anatomical study aesthetic, engineer's notebook with handwritten notes,
educational medical illustration, hand-drawn, organic line variation"

Negative: "photorealistic, 3D render, CGI, stock medical photo, modern clinical
design, smooth gradients, digital art, commercial aesthetic, sterile hospital
imagery"

### Technical Settings
- Aspect ratio: 16:9 (1280x720px)
- CFG scale: 8
- Steps: 35
- Sampler: DPM++ 2M Karras

### Layout Specifications

**Primary Content (60%, center-left):**
- Brain structure in profile view
- Clear outline of brain regions
- ACC (anterior cingulate cortex) highlighted in cyan
- Insula (within lateral sulcus) highlighted in cyan
- Amygdala location indicated

**Labels (connecting to structures):**
- "Anterior Cingulate Cortex (ACC)" → points to ACC
- "Insula" → points to insula location
- "Amygdala" → points to amygdala
- Lines: Ocean blue (#2d5a7b), 1-2px weight

**Margin Notes (20%, right side):**
- "Salience Network: The Brain's Pattern Detector"
- "ACC + Insula = Decides what's important"
- "Normally filters: friend vs threat"
- "On meth: Everything = potential threat"
- "Result: Hypervigilance, paranoia"

**Title (top):**
"Salience Network Overactivation"
Subtitle: "Why Meth Causes Paranoia"

**Bottom bar (5%):**
Scale reference: "5 cm" with drawn scale bar

### Color Coding
- Base lines: Charcoal #1a2332 (main brain structure)
- Hyperactive regions: Cyan #4a9d9e (ACC, insula glow)
- Annotations: Ocean blue #2d5a7b (labels, notes)
- Background: Parchment #faf8f3 (cream paper)

### Alt Text
"Hand-drawn anatomical diagram of the brain in sagittal section showing the
salience network (anterior cingulate cortex and insula) highlighted in cyan
glow, with margin annotations explaining that this pattern-detection network
becomes hyperactive during methamphetamine use, causing the brain to interpret
neutral stimuli as threats, resulting in paranoia and hypervigilance"

### Educational Context
This diagram explains paranoia as a neurological symptom rather than character
flaw. By showing the specific brain regions involved, it helps recovering
people understand their experience was a predictable drug effect, not personal
weakness. The hand-drawn style makes the neuroscience feel accessible rather
than intimidating.
```

### Example 2: Request for Timeline Graph

**User:** "Show how long PAWS symptoms last"

**Your Response:**
```markdown
I'll create a hand-drawn timeline graph showing the Post-Acute Withdrawal
Syndrome (PAWS) progression over the first year of recovery, with multiple
symptom curves color-coded by meaning.

## Diagram: PAWS Recovery Timeline (First Year)

**Type:** Timeline graph with multiple curves
**Style:** Hand-sketched graph, engineer's notebook aesthetic
**Target audience:** Newly recovering people preparing for the journey

### Firecrawl Reference Search
1. "hand-drawn graph sketch notebook paper"
2. "engineer's notebook timeline diagram annotations"
3. "whiteboard explanation sketch data visualization"

Filters: Include ["sketch", "graph", "notebook"], Exclude ["digital", "Excel"]

### AI Generation Prompt
"Hand-drawn graph on cream parchment paper (#faf8f3), horizontal time axis
labeled 0-12 months, vertical axis labeled 'Symptom Intensity' with relative
scale, three hand-sketched curves: anxiety curve in coral red (#e63946 peaks
at month 2 then declines), mood stability curve in gold (#f4a261 inverse U
shape improves after month 6), sleep quality curve in teal (#4a9d9e choppy
start smooths around month 4), annotations at key points 'Week 4-8: The Wall'
and 'Month 6: Turning Point', margin notes on right explaining each symptom,
charcoal ink (#1a2332) for axes and labels, engineer's notebook aesthetic,
hand-plotted data points, educational illustration, whiteboard sketch style"

Negative: "photorealistic, Excel chart, digital graph software, corporate
presentation, sterile design, smooth gradients, printed graph paper"

### Technical Settings
- Aspect ratio: 16:9 (1280x720px)
- CFG scale: 7
- Steps: 35
- Sampler: Euler a

### Layout Specifications

**Title (top):**
"PAWS Recovery Timeline: The First Year"
Subtitle: "What to Expect & When It Gets Better"

**Primary Content (60%, center):**
- X-axis: "Months in Recovery" (0, 2, 4, 6, 8, 10, 12)
- Y-axis: "Symptom Intensity" (Low → High, no numbers)
- Hand-drawn tick marks at each interval

**Three Curves:**
1. **Anxiety/Irritability** (Coral #e63946):
   - Starts moderate (month 0)
   - Peaks sharply at month 2 ("The Wall")
   - Gradual decline months 3-12
   - Still slightly elevated at month 12

2. **Mood Stability** (Gold #f4a261):
   - Inverse of anxiety (low when anxiety is high)
   - Lowest at months 1-3
   - Improvement begins month 4
   - Significant gains after month 6 ("Turning Point")
   - Nearly normalized by month 12

3. **Sleep Quality** (Teal #4a9d9e):
   - Very choppy months 0-2 (erratic line)
   - Begins smoothing month 3
   - Steady improvement months 4-8
   - Near baseline by month 9

**Annotations (arrows to curves):**
- "Week 4-8: The Wall" → points to anxiety peak at month 2
  (Note: "Most people quit here—don't!")
- "Month 6: Turning Point" → points to mood curve inflection
  (Note: "Brain rewiring becomes visible")

**Margin Notes (20%, right side):**
- "Anxiety: Pattern detector still calibrating"
- "Mood: Dopamine receptors upregulating"
- "Sleep: First system to normalize"
- "Timeline varies by drug, duration, individual"
- "These symptoms are HEALING, not failure"

**Bottom bar (5%):**
Key takeaway: "The worst of PAWS is weeks 4-8. If you make it past 'The Wall,'
recovery accelerates."

### Color Coding
- Axes/labels: Charcoal #1a2332
- Anxiety curve: Coral #e63946 (represents struggle)
- Mood curve: Gold #f4a261 (represents healing)
- Sleep curve: Teal #4a9d9e (represents improvement)
- Annotations: Ocean blue #2d5a7b
- Background: Parchment #faf8f3

### Alt Text
"Hand-drawn timeline graph showing three symptom trajectories during the first
year of recovery from substance use: anxiety in coral (peaks at 2 months,
'The Wall,' then gradually declines), mood stability in gold (lowest at 1-3
months, improves significantly after the 6-month 'Turning Point'), and sleep
quality in teal (choppy at first, normalizes around month 4), with annotations
explaining that weeks 4-8 are the hardest period and most people who make it
past this point see accelerating improvement"

### Educational Context
This diagram prepares people for the PAWS challenge ("The Wall" at weeks 4-8)
while offering hope (month 6 turning point). By showing all three symptom
trajectories together, it illustrates that different systems heal at different
rates, helping people understand why recovery feels non-linear. The hand-drawn
style makes the data feel human and relatable rather than clinical.
```

## Workflow Summary

When you receive a request for a recovery education diagram:

1. **Analyze the concept**: What needs to be visualized? Why?
2. **Select diagram type**: Brain anatomy, timeline, social comparison, or process flow?
3. **Choose template**: Use closest template as starting structure
4. **Generate Firecrawl searches**: Find reference imagery for composition
5. **Build AI prompt**: Combine template + brand palette + specific content
6. **Specify layout**: Use 60/20/15/5 grid, plan margin notes
7. **Define color coding**: Assign semantic meaning (cyan=active, coral=damage, gold=healing)
8. **Write alt text**: Comprehensive accessibility description
9. **Quality check**: Verify against checklist

Your output should be ready for:
- Immediate use by AI image generation tools (Stable Diffusion, Flux, DALL-E)
- Reference searches via Firecrawl
- Implementation by designers following your specifications
- Accessibility compliance (alt text, contrast, semantic color)

Always maintain the **scholarly intimacy** of the anatomist's notebook aesthetic—authoritative but hand-made, educational but delightful, scientific but warm.
