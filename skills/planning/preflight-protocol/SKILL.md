---
name: preflight-protocol
description: Gray area identification, 4-question decision loops, scope creep detection, and BRIEFING.md generation for phase planning.
---

# Pre-Flight Protocol Skill

// Project Autopilot - Pre-Flight Protocol
// Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

**Purpose:** Structured pre-flight briefing framework that captures decisions, identifies gray areas, and prevents scope creep BEFORE planning begins.

---

## Core Components

### 1. Gray Area Identification

Gray areas are implementation decisions where multiple valid approaches exist. The protocol automatically generates phase-specific gray areas from phase goals.

#### Gray Area Categories

| Category | Examples | Question Style |
|----------|----------|----------------|
| **Layout** | Sidebar vs tabs, card vs list | "How should X be organized?" |
| **Behavior** | Real-time vs polling, infinite scroll vs pagination | "How should X behave when..." |
| **Data** | Format, density, filtering | "How should data be displayed?" |
| **Interaction** | Hover states, click actions, gestures | "What happens when user..." |
| **Mobile** | Responsive vs adaptive, touch behavior | "How should this work on mobile?" |

#### Multi-Select UI Pattern

```
Present gray areas as checkbox list with concrete decision points:

☑️ Layout style — Sidebar navigation vs top tabs?
☑️ Activity feed — Real-time updates or manual refresh?
☐ Settings organization — Single page or categorized sections?
☐ Data density — Compact view or spacious cards?
☑️ Mobile behavior — Responsive or separate mobile view?

[Continue with selected areas] [Skip all - Claude decides]
```

#### Generation Protocol

```
FUNCTION generateGrayAreas(phase):
    goal = phase.objective
    scope = phase.deliverables

    # Extract decision points from goal
    gray_areas = []

    # Analyze nouns for layout decisions
    FOR each noun IN extractNouns(goal):
        IF hasMultipleLayouts(noun):
            gray_areas.add({
                id: generateId(),
                category: "layout",
                question: "How should {noun} be organized?",
                options: getLayoutOptions(noun)
            })

    # Analyze verbs for behavior decisions
    FOR each verb IN extractVerbs(goal):
        IF hasMultipleBehaviors(verb):
            gray_areas.add({
                id: generateId(),
                category: "behavior",
                question: "How should {verb} work?",
                options: getBehaviorOptions(verb)
            })

    # Add standard gray areas if relevant
    IF scope.includes("mobile") OR scope.includes("responsive"):
        gray_areas.add(MOBILE_GRAY_AREA)

    IF scope.includes("data") OR scope.includes("list"):
        gray_areas.add(DATA_DENSITY_GRAY_AREA)

    RETURN gray_areas[0:8]  # Max 8 areas
```

---

### 2. Four-Question Decision Loop

For each selected gray area, ask up to 4 focused questions to capture the user's intent.

#### Loop Protocol

```
FUNCTION questionLoop(gray_area):
    question_count = 0
    decisions = []

    WHILE question_count < 4:
        question_count += 1

        # Generate question with options
        question = generateQuestion(gray_area, question_count, decisions)

        # Present with options
        PRESENT {
            question: question.text,
            options: [
                ...question.specific_options,  # 2-4 specific choices
                {id: "claude", text: "Claude decides", description: "Delegate this to Claude's judgment"}
            ],
            multi_select: question.allows_multi
        }

        # Handle response
        response = AWAIT user_selection

        IF response.selected == "claude":
            markAsAutonomous(gray_area, question.topic)
            LOG "Marked as Claude's discretion: {gray_area.category}"
            BREAK

        # Capture decision
        decisions.add({
            question: question.text,
            answer: response.selected,
            context: response.explanation  # Optional user notes
        })

        # Check if resolved
        IF gray_area.isResolved(decisions):
            BREAK

        # After 4 questions, offer to continue or move on
        IF question_count == 4:
            PRESENT "Would you like to discuss more about {gray_area.label}, or move on?"
            continue_response = AWAIT user_selection
            IF continue_response == "move_on":
                BREAK
            ELSE:
                question_count = 0  # Reset for more questions

    RETURN decisions
```

#### Question Types by Round

| Round | Focus | Example |
|-------|-------|---------|
| 1 | Core approach | "Cards or list view?" |
| 2 | Key variation | "Compact or spacious?" |
| 3 | Edge case | "What about empty state?" |
| 4 | Detail | "Animation on load?" |

---

### 3. Claude's Discretion Section

Areas delegated to Claude's autonomous decision-making.

#### Default Autonomous Areas

These are ALWAYS in Claude's discretion unless user explicitly overrides:

```yaml
claude_discretion_defaults:
  - category: styling
    items:
      - "Exact spacing/padding values"
      - "Animation timing and easing"
      - "Border radius values"
      - "Shadow depths"
      - "Font weight variations"

  - category: code
    items:
      - "Code organization within patterns"
      - "Variable naming within conventions"
      - "Internal function structure"
      - "Comment placement"

  - category: content
    items:
      - "Error message wording"
      - "Placeholder text content"
      - "Loading indicator text"
      - "Empty state messages"
```

#### Marking Protocol

```
FUNCTION markAsAutonomous(area, reason):
    state.claude_discretion.add({
        area: area.label,
        category: area.category,
        reason: reason,  # "User said 'you decide'" or "Not discussed"
        timestamp: now()
    })
```

---

### 4. Scope Creep Detection

Detect when discussion veers outside current phase scope.

#### Detection Protocol

```
FUNCTION detectScopeCreep(user_input, current_phase):
    # Check against phase scope
    phase_scope = loadPhaseScope(current_phase)

    # Extract features/capabilities mentioned
    mentioned = extractFeatures(user_input)

    FOR each feature IN mentioned:
        IF NOT inScope(feature, phase_scope):
            # This is scope creep
            handleScopeCreep(feature, user_input)
            RETURN true

    RETURN false

FUNCTION handleScopeCreep(feature, user_input):
    # Notify user
    LOG "[{feature}] sounds like a new capability — that belongs in its own phase."
    LOG "I'll note it as a deferred idea."

    # Capture for later
    addDeferredIdea({
        feature: feature,
        mentioned_during: current_gray_area,
        original_input: user_input,
        suggested_phase: suggestPhase(feature)
    })

    # Return to current question
    LOG "Back to [{current_gray_area.label}]: {current_question.text}"
```

#### Scope Indicators

```yaml
scope_creep_signals:
  phrases:
    - "We could also"
    - "It would be nice to"
    - "Later we should"
    - "What about adding"
    - "Can we also"

  patterns:
    - New entity type not in phase
    - Integration with external system not planned
    - Feature from future roadmap phase
    - Enhancement to existing (not current) functionality
```

---

## Output: BRIEFING.md

The preflight protocol generates a structured BRIEFING.md file.

### Template

```markdown
# Phase {N}: {Name} - Pre-Flight Briefing

// Project Autopilot - Phase Briefing
// Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

**Generated:** {timestamp}
**Phase Goal:** {goal from flightplan}
**Briefing Duration:** {time_spent}

---

## Phase Boundary

{Explicit scope anchor - what this phase delivers and what it doesn't}

**In Scope:**
- {deliverable 1}
- {deliverable 2}

**Out of Scope:**
- {explicitly excluded}

---

## Implementation Decisions

### {Category 1}
**Gray Area:** {original question}
**Decision:** {selected option}
**Rationale:** {why this choice}

- {Specific detail 1}
- {Specific detail 2}

### {Category 2}
**Gray Area:** {original question}
**Decision:** {selected option}

- {Specific detail}

---

## Claude's Discretion

These areas are delegated to Claude's judgment:

### User Delegated
- {Area 1} - User explicitly said "you decide"
- {Area 2} - User selected "Claude decides"

### Default Autonomous
- Exact spacing/padding values
- Animation timing and easing
- Error message wording
- Code organization within patterns
- Variable naming within conventions
- Internal function structure

---

## Specific Ideas

User-provided references and examples:

- "{Exact quote from user}"
- "I want it like {reference}"
- "{Specific example mentioned}"

---

## Deferred Ideas

Features mentioned but outside current phase scope:

| Feature | Mentioned During | Suggested Phase |
|---------|------------------|-----------------|
| {Feature 1} | Layout discussion | Phase {N+X} |
| {Feature 2} | Behavior discussion | Future consideration |

---

## Technical Context

### Existing Patterns Detected
- {Pattern 1 from codebase analysis}
- {Pattern 2 from codebase analysis}

### Dependencies
**This phase requires:**
- {Prerequisite from earlier phase}

**This phase provides:**
- {What later phases need}

### Integration Points
| From | To | Type |
|------|-----|------|
| {Component} | {Service} | API call |
| {Service} | {Database} | Query |

---

## Briefing Metadata

**Areas Discussed:** {N} of {total}
**Questions Asked:** {N}
**Time per Area:** ~{avg}min

| Area | Status | Questions |
|------|--------|-----------|
| {Area 1} | Decided | 3 |
| {Area 2} | Claude's discretion | 1 |
| {Area 3} | Not discussed | 0 |
```

---

## Integration Points

### With /autopilot:preflight Command
```
preflight.md calls:
- generateGrayAreas(phase)
- questionLoop(area) for each selected
- detectScopeCreep(input) on every user input
- generateBriefingMd(decisions)
```

### With /autopilot:flightplan Command
```
flightplan.md reads:
- BRIEFING.md → Implementation Decisions
- BRIEFING.md → Claude's Discretion
- BRIEFING.md → Technical Context
```

### With /autopilot:takeoff Command
```
takeoff.md reads:
- BRIEFING.md → Claude's Discretion (for autonomous decisions during execution)
- BRIEFING.md → Specific Ideas (for style guidance)
```

---

## Protocol Enforcement

### Rules
1. **Never skip gray area identification** - Always present at least 4 gray areas
2. **Respect the 4-question limit** - Don't interrogate users
3. **Always offer "Claude decides"** - Every question must have this option
4. **Capture scope creep immediately** - Don't let discussion wander
5. **Generate BRIEFING.md always** - Even if all areas are Claude's discretion

### Anti-Patterns
- Asking about codebase patterns (read the code instead)
- Asking technical implementation questions (infer from requirements)
- Generic "what do you want" questions (be specific)
- More than 4 questions per area without user consent
- Forgetting to capture deferred ideas
