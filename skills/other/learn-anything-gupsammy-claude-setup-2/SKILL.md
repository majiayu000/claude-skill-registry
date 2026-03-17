---
name: learn-anything
description: Metalearning skill that helps master any topic efficiently by identifying critical 20% material, building expert vocabulary, and creating research-backed learning roadmaps. Auto-trigger when user says "learn [topic]", "help me learn [topic]", "I want to learn [topic]", or asks for guidance on understanding a new subject. Supports comprehensive plans, interactive guidance, or minimalist just-in-time delivery.
---

# Learn Anything

Transform "I want to learn X" into actionable learning roadmaps using metalearning principles: identify the critical 20%, build expert vocabulary, sequence logically (why before how), prioritize current best practices.

## When to Use

Activate when user:
- Says "learn [topic]" or "help me learn [topic]"
- Asks "how do I get started with [subject]?"
- Requests structured approach to mastering something new

Do NOT use when:
- User has content and wants action plans (use ship-learn-next)
- Request is for implementation help, not learning

## Core Principles

1. **Pareto Focus**: Identify 20% of material delivering 80% of practical value
2. **Logical Sequencing**: Foundations before details, why before how
3. **Vocabulary First**: Build expert lexicon for better understanding and prompting
4. **Practical Bias**: Optimize for applicable knowledge over comprehensive coverage

## State Management - Global ~/.learn Directory

All learning artifacts are saved globally in `~/.learn/[topic-slug]/`:

```
~/.learn/
├── react/
│   ├── plan.md              # Learning plan (all modes)
│   ├── progress.json        # State tracking (interactive/minimalist)
│   ├── vocabulary.md        # Dependency-sequenced vocab
│   ├── notes.md            # User's learning notes (optional)
│   └── apps/               # Interactive app prompts (interactive/minimalist)
│       ├── components.md
│       ├── hooks.md
│       └── state-management.md
├── rust/
│   ├── plan.md
│   ├── progress.json
│   ├── vocabulary.md
│   └── apps/
│       └── ownership.md
```

**Benefits**: Learning state persists across all projects. Can continue learning from any directory.

**Setup**: Create `~/.learn/` directory on first use if it doesn't exist. Use topic slug (lowercase, hyphens) for subdirectory names.

## Three Output Modes

**Mode Selection**: Ask preference BEFORE research (affects how material is structured). Default to comprehensive if unclear.

### Comprehensive Plan (Default)
- **Delivery**: Save complete `plan.md` with detailed 20% starter pack and full roadmap
- **State**: No progress tracking needed
- **Best for**: Self-directed learners who want complete picture upfront
- **Artifacts**: `~/.learn/[topic]/plan.md` only

### Interactive Guide
- **Delivery**: Present one concept at a time, validate understanding before progressing
- **State**: Track progress in `progress.json`, update as user completes concepts
- **Best for**: Learners wanting accountability and validation
- **Artifacts**: `plan.md` + `progress.json` + `vocabulary.md`
- **Flexibility**: Allow rollback, concept reordering, adding concepts mid-journey

### Minimalist Just-In-Time
- **Delivery**: Only immediate next resource and key terms
- **State**: Track progress in `progress.json`, user returns for next step
- **Best for**: Action-oriented learners avoiding analysis paralysis
- **Artifacts**: `plan.md` (minimal) + `progress.json` + `vocabulary.md`
- **Flexibility**: Allow rollback, concept reordering, adding concepts mid-journey

## Resuming Existing Learning

Before starting new learning plan, check if `~/.learn/[topic-slug]/` exists:

**If exists**:
1. Read `progress.json` to check mode and current state
2. Ask: "I found an existing learning plan for [topic]. Would you like to: A) Continue where you left off, B) Start fresh, C) Review your progress?"

**If continuing**:
- Load current concept from progress.json
- Present next step based on mode (Interactive/Minimalist) or remind them of plan (Comprehensive)
- Reference what they've already learned when presenting new material

**If starting fresh**:
- Archive old directory to `~/.learn/[topic]-archive-[timestamp]/`
- Proceed with new learning plan

**If reviewing progress**:
- Display concepts completed, current concept, vocabulary learned
- Allow modifications: "Want to go back to any concept? Add new concepts? Continue forward?"

## Workflow

### Step 1: Understand Intent

Extract topic from user request, then ask 2-3 questions to understand context:

**Focus on intent and application:**
- "What's driving you to learn [topic]?" (Work project / Career shift / Building something specific / Pure curiosity)
- "Where will you apply this knowledge?" (Specific project / General skill / Professional requirement / Personal exploration)
- "What's your current experience with [topic] or related areas?" (Complete beginner / Some exposure / Familiar with adjacent topics)

Use AskUserQuestion with conversational multiple choice options. Keep brief - gather just enough to tailor the plan.

### Step 2: Intelligent Research

Conduct adaptive web searches based on topic maturity and ecosystem:

**Search Strategy (adapt per topic):**

For established technologies/fields:
- "[topic] official documentation"
- "[topic] reddit" (find community discussions, real practitioner opinions)
- "[topic] learning path" or "[topic] roadmap"
- "getting started [topic]" (beginner resources)
- "[topic] vs [alternative]" (understand positioning and use cases)

For emerging/niche topics:
- "[topic] github" (find projects, examples, real usage)
- "[topic] tutorial"
- "what is [topic]" (understand current state)
- "[topic] use cases" (practical applications)

For academic/theoretical topics:
- "[topic] course"
- "[topic] textbook recommendation"
- "[topic] explained" (accessible introductions)

**Research Goals:**
1. Current state and recent developments (what's modern vs outdated)
2. Highest-impact resources (official docs, respected courses, definitive guides)
3. Expert vocabulary (terms, jargon, acronyms used casually)
4. Learning dependencies (prerequisites, logical sequencing)
5. Common pitfalls and confusing concepts

**Resource Quality Signals:**
- Official/maintained documentation
- Community consensus (upvotes, recommendations)
- Recent publication (relevance to current practices)
- Beginner-friendly vs advanced (match user level)
- Free and accessible

Run 4-6 searches adapting to what you discover. Don't follow template blindly.

### Step 3: Identify Critical 20%

Analyze research to extract 3-7 core topics providing maximum foundation.

**Selection Criteria:**
- Unlocks understanding of other concepts
- Used frequently in practice
- Foundational vs nice-to-know
- Current best practices (skip legacy/deprecated)

For each core topic:
- Why it matters (conceptual foundation)
- 1-2 highest-impact resources
- 5-10 key vocabulary terms
- Time estimate
- Concrete capability gained

**Example (React):**
- 20%: Components, JSX, Props/State, Hooks, Event Handling
- NOT 20%: Class components (outdated), advanced patterns, SSR (later), testing (later)

### Step 4: Build Full Roadmap

Sequence remaining topics into Foundation → Intermediate → Advanced.

For each topic beyond 20%:
- Brief description
- Why it matters
- One highest-impact resource
- Mark optional vs essential

Keep lean. This is a map, not detailed instructions.

### Step 5: Compile Vocabulary

Build **dependency-based vocabulary sequence** - order terms by conceptual dependencies, not arbitrary tiers.

**Sequencing Principle**: Learn foundational terms before terms that depend on them.

Example (React):
1. **Component** (foundation - needed for everything)
2. **JSX** (syntax - needed to write components)
3. **Props** (component inputs - builds on component understanding)
4. **State** (component data - parallel to props)
5. **Hook** (function for state/effects - builds on state concept)
6. **useState** (specific hook - builds on hook concept)
7. **useEffect** (specific hook - builds on hook + component lifecycle)

**Coverage**: Identify 10-30 terms covering the 20% material. If dependencies require more terms, include them. Always start from first principles.

**Format for each term**:
```
**Term**: Definition (1 sentence) + why it matters/when you'll use it
Dependencies: [terms you need to know first, if any]
```

**For Interactive/Minimalist modes**: Pre-sequence vocabulary to match concept order. As each concept is introduced, present only its terms and dependencies (building on previously learned terms).

**For Comprehensive mode**: Present full sequenced vocabulary list in plan.md.

**Save to**: `~/.learn/[topic]/vocabulary.md` with dependency indicators.

### Step 6: Generate Interactive App Prompts (When Beneficial)

For Interactive and Minimalist modes, generate creative app prompts for concepts where hands-on practice significantly enhances learning.

**When to generate app prompts:**
- Visual/spatial concepts (UI components, layouts, animations, data structures)
- Algorithmic concepts (sorting, searching, recursion, state machines)
- Interactive patterns (event handling, state management, user flows)
- Abstract concepts that benefit from visualization (closures, async, memory management)
- **Skip for**: Pure theory, historical context, simple definitions, tool installation

**App Design Principles:**

Generate fully custom app ideas that maximize learning through interaction. Consider:

1. **Active Learning**: User manipulates, builds, or experiments (not just reads/watches)
2. **Immediate Feedback**: Visual/interactive responses show concept in action
3. **Progressive Complexity**: Start simple, allow exploration of edge cases
4. **Concept Isolation**: Focus on one core concept, avoid overwhelming with related topics
5. **Playful Discovery**: Make it fun - games, challenges, creative tools over dry drills

**Creative App Types** (examples, not templates):
- **Builders**: "Build your own X" - construct the concept from components
- **Simulators**: Interactive simulation showing concept behavior
- **Visualizers**: Animate or visualize abstract concepts in real-time
- **Playgrounds**: Sandbox for experimentation with instant visual feedback
- **Games**: Gamified learning (e.g., "sort the array faster", "catch the bug")
- **Explorers**: Interactive documentation where user explores concept space
- **Challenges**: Puzzle/problem-solving that requires applying the concept

**Prompt Generation Process:**

For each concept needing an app:

1. **Identify core learning goal**: What should user viscerally understand after using this app?
2. **Design interaction**: How will user interact? What will they build/manipulate/explore?
3. **Determine requirements**: Need image generation? LLM for dynamic content? Neither?
4. **Write concise prompt** (50-150 words):
   - App name and core idea
   - What user does (interaction model)
   - What they learn through interaction
   - Tech requirements: "Requires: Image generation" or "Requires: LLM for dynamic examples" or "Static interactive UI only"

**Prompt Format:**

```markdown
### Interactive Learning App: [Concept Name]

**App Idea**: [Creative name - 2-4 words]

[2-3 sentence description of the app and what user does]

**Learning Goal**: [What concept becomes clear through interaction]

**Requirements**: [Image generation / LLM / Neither - just interactive UI]

**Google AI Studio Prompt**:
---
[Concise 50-150 word prompt describing the app to build]
---
```

**Examples:**

For "React Components":
```
**App Idea**: Component Constructor

Build React components by dragging visual elements and see the JSX code generate in real-time. Click components to see props, modify values to see re-renders. Break things intentionally to understand component boundaries.

**Learning Goal**: Understand component composition, props flow, and re-rendering through visual manipulation.

**Requirements**: Static interactive UI only

**Google AI Studio Prompt**:
---
Create an interactive web app where users build React components visually. Left side: drag-and-drop elements (button, input, div, text). Right side: live JSX code generation. Users can click any component to edit props, see how changes propagate. Include a "break it" button that introduces common mistakes (missing keys, wrong prop types) to learn debugging. Real-time visual updates as they build. Make it playful and colorful.
---
```

For "Sorting Algorithms":
```
**App Idea**: Sort Race Visualizer

Watch different sorting algorithms compete in real-time with animated array bars. Adjust speed, array size, and initial order. See comparison counts and swaps. Predict which algorithm wins for different data patterns.

**Learning Goal**: Intuitively understand algorithm performance through visual competition.

**Requirements**: Static interactive UI only

**Google AI Studio Prompt**:
---
Build a sorting algorithm race visualizer. Show 3-4 algorithms (bubble, quick, merge, insertion) running simultaneously on the same array, represented as colored bars. Animate every comparison and swap with smooth transitions. Controls: speed slider, array size, initial order (random, sorted, reversed). Display live stats: comparisons, swaps, time. Add "race mode" where algorithms compete. Make it feel like a game with exciting animations and sound effects (optional). Users discover performance patterns through play.
---
```

For "JavaScript Closures":
```
**App Idea**: Closure Factory Explorer

Create functions that "remember" values. Build closures by locking in variables, then invoke them with different inputs to see which data persists vs changes. Visual memory boxes show captured scope.

**Learning Goal**: Understand lexical scope and variable capture through interactive function building.

**Requirements**: LLM for dynamic code generation and explanations

**Google AI Studio Prompt**:
---
Create an interactive closure explorer. Users write simple functions that capture variables from outer scope. App shows visual "memory boxes" representing scopes - outer and inner. When function is invoked, highlight which variables come from where. Generate diverse examples on-demand using an LLM (simple counter, event handlers, private data patterns). Let users modify code and see scope visualization update. Explain closure behavior in plain language as they experiment. Make the invisible visible.
---
```

**Storage and Delivery:**

1. Save app prompt to `~/.learn/[topic]/apps/[concept-slug].md`
2. Display inline in conversation when presenting the concept
3. Treat as optional supplementary material (don't gate progress)

**In Interactive Mode**: Show app prompt after presenting resource, before understanding check
**In Minimalist Mode**: Show app prompt with the resource link and vocabulary

### Step 7: Generate Output

#### Mode 1: Comprehensive Plan

Save to `~/.learn/[topic]/plan.md` with structure:

```markdown
# Learning Plan: [Topic]

**Context**: [Current level] | [Goal/Application] | Generated: [date]

## First 20% - Starter Pack

### 1. [Core Topic]
**Why**: [Conceptual explanation]
**Vocabulary**: [Terms with dependencies]
**Resource**: [URL] - [Why valuable] - Time: [Estimate]
**After this**: [Capability gained]

[Repeat for 3-7 core topics]

## Full Roadmap
### Intermediate: [Topics with brief descriptions + resources]
### Advanced: [Topics with brief descriptions + resources]
### Optional: [When needed]

## Vocabulary Reference
[Dependency-sequenced terms with definitions - from vocabulary.md]

## Learning Tips
[3-5 tips: pitfalls, best practices, communities]

## Next Steps
Start with topic 1, learn vocabulary as you go, complete resource, assess next direction.
```

After saving: Confirm location, summarize 20%, encourage action.

#### Mode 2: Interactive Guide

**Initial Setup**:
1. Create `~/.learn/[topic]/` directory
2. Save `plan.md` with full learning plan (for reference)
3. Save `vocabulary.md` with dependency-sequenced terms
4. Initialize `progress.json`:

```json
{
  "mode": "interactive",
  "topic": "React",
  "current_concept": 1,
  "concepts": [
    {"id": 1, "name": "Components", "status": "in_progress", "started_at": "2025-01-15"},
    {"id": 2, "name": "JSX", "status": "pending"},
    {"id": 3, "name": "Props & State", "status": "pending"}
  ],
  "vocabulary_progress": {
    "learned": [],
    "current": ["component", "render"],
    "upcoming": ["jsx", "props", "state"]
  },
  "history": []
}
```

**Delivery Flow**:

**First interaction** - Present current concept:
```
📚 Learning React - Concept 1/5: Components

**Why this matters**: [Conceptual explanation]

**Vocabulary for this concept**:
- **Component**: [Definition + usage]
  Dependencies: None (foundational)
- **Render**: [Definition + usage]
  Dependencies: Component

**Resource**: [Name + URL]
Why this resource: [What makes it valuable]
Time: [Estimate]

[If concept benefits from interactive app, display app prompt here:]

**🎮 Interactive Learning App**: [App Name]
[Description and learning goal]
[Google AI Studio prompt in code block]
Saved to: ~/.learn/react/apps/components.md

**After completing**: Return and I'll check your understanding before moving to JSX.

Progress saved to: ~/.learn/react/progress.json
```

**When user returns** - Check understanding:
```
Welcome back! Let's validate your understanding of Components.

Quick check:
- What is a component in your own words?
- How does rendering work?

[Based on response:]
✓ Great understanding → Update progress.json, move to concept 2
⚠ Some gaps → Clarify misconceptions, offer supplementary resource
✗ Struggling → Suggest re-doing resource or different approach, keep on concept 1
```

**State Updates**:
- Mark concept completed, update `vocabulary_progress.learned`
- Set next concept to "in_progress"
- Add to `history` array
- Save progress.json

**Flexibility Commands** (user can say these anytime):
- "Go back to [concept]" → Rollback, set that concept to "in_progress", add to history
- "I want to review [concept]" → Allow re-learning, build on what was taught before
- "Add a concept about [topic]" → Insert into concepts array, update sequence
- "Skip to [concept]" → Mark current as completed, jump ahead (allow but discourage)
- "Show my progress" → Display current state from progress.json

**Conversation Style**: One concept at a time, validate before progressing, adaptive pacing, encouraging tone. Build on previously learned vocabulary when introducing new terms.

#### Mode 3: Minimalist Just-In-Time

**Initial Setup**:
1. Create `~/.learn/[topic]/` directory
2. Save minimal `plan.md` (just concept list + brief descriptions)
3. Save `vocabulary.md` with dependency-sequenced terms
4. Initialize `progress.json` (same structure as Interactive mode)

**Delivery Flow**:

**First interaction** - Minimal, actionable:
```
🎯 Learning React - Step 1/5: Components

Start here: [Resource name + URL]
Time: ~2 hours

Key terms to understand:
- **Component**: [Definition]
  Dependencies: None
- **Render**: [Definition]
  Dependencies: Component

[If concept benefits from interactive app:]

🎮 Optional Interactive App: [App Name]
[Google AI Studio prompt - concise version]
Full prompt saved: ~/.learn/react/apps/components.md

Return when done for the next step.

Progress: ~/.learn/react/progress.json
```

**When user returns** - Brief check + next step:
```
Welcome back!

Quick: What's one key thing you learned about components?

[Based on response - acknowledge briefly]

Next step: JSX (Step 2/5)
Resource: [URL]
Time: ~1 hour

New vocabulary (builds on what you know):
- **JSX**: [Definition]
  Dependencies: Component, Render
- **Element**: [Definition]
  Dependencies: JSX

Return when done.
```

**State Updates**: Same as Interactive mode - mark completed, update vocabulary progress, save to progress.json.

**Flexibility Commands**: Same as Interactive mode - allow rollback, review, add concepts, show progress.

**Key Difference from Interactive**: No understanding validation checks. Trust user to self-assess. Focus on momentum and just-in-time information delivery.

## Quality Standards

Regardless of mode:

✅ Research is current (prioritize recent resources when topic evolves rapidly)
✅ Resources are accessible (prefer free, high-quality, maintained)
✅ Vocabulary is practical (actual usage, not exhaustive lists)
✅ Sequencing is logical (foundation → advanced, why → how)
✅ 20% is truly impactful (each topic unlocks significant understanding)
✅ Resources are vetted (recommend best, not first search results)
✅ Explanations are clear (intelligent but unfamiliar audience)

## Edge Cases & Guidelines

**Broad topic**: Narrow via AskUserQuestion before research. "AI covers ML, NLP, computer vision - which interests you?"

**Niche topic**: Deeper research needed. If resources limited, start with fundamentals before specialization.

**User has resource**: Research quality. Build around if good, suggest alternatives if outdated. Provide vocabulary/sequencing regardless.

**Mode switch**: Adapt from current state using progress.json. No re-interview needed.

**What NOT to do**: Passive study plans, exhaustive vocabulary (50+ terms), skip research, broad 20% (10+ topics), mechanical interview questions.

**Success criteria**: Clear 20%, current research-backed resources, dependency-sequenced vocabulary, logical sequencing, realistic estimates, applicable knowledge focus. After 20%, can user engage independently?
