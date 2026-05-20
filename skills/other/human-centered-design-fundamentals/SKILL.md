---
name: human-centered-design-fundamentals
description: Apply cognitive psychology principles to design discoverable, understandable products through affordances, signifiers, feedback, and conceptual models. For physical and digital interfaces requiring
  human interaction. NOT for pure aesthetics, marketing, or AI-only systems.
allowed-tools: Read
metadata:
  category: Design & Creative
  tags:
  - human
  - centered
  - design
  pairs-with:
  - skill: ux-friction-analyzer
    reason: UX friction analysis applies human-centered design principles to identify usability barriers
  - skill: adhd-design-expert
    reason: ADHD-aware design is a specialized application of human-centered design for neurodivergent users
  - skill: design-justice
    reason: Design justice extends human-centered design to explicitly center marginalized communities
---

# Human-Centered Design Fundamentals
Design products that accommodate actual human cognition and behavior rather than expecting humans to adapt to arbitrary system requirements.

## When to Use
✅ Use for: 
- Physical product design (doors, appliances, controls, tools)
- Digital interface design (software, touchscreens, dashboards)
- System design where human error is critical (medical devices, industrial controls, aircraft)
- Redesigning systems after repeated user errors
- Creating instructions and documentation
- Error prevention and safety-critical systems

❌ NOT for: 
- Pure visual design without functional components
- Marketing and brand identity
- Autonomous systems with no human interaction
- Systems where users have unlimited training time and perfect memory

## Core Process

### Seven Stages of Action Decision Tree

```
START: User encounters system
│
├─→ Is this GOAL-DRIVEN (user has objective)?
│   ├─→ YES: Begin at Stage 1 (Form Goal)
│   │   ├─→ Can user identify what they want? 
│   │   │   ├─→ NO: MISTAKE likely → Provide clear conceptual model
│   │   │   └─→ YES: Proceed to Stage 2
│   │   │
│   │   ├─→ Stage 2: Plan action sequence
│   │   │   ├─→ Are alternatives clear?
│   │   │   │   ├─→ NO: MISTAKE likely → Improve discoverability
│   │   │   │   └─→ YES: Proceed to Stage 3
│   │   │
│   │   ├─→ Stage 3: Specify action
│   │   │   ├─→ Is correct action obvious?
│   │   │   │   ├─→ NO: Gulf of Execution too wide → Add signifiers
│   │   │   │   └─→ YES: Proceed to Stage 4
│   │   │
│   │   └─→ Stage 4: Perform action
│   │       ├─→ Is user expert (subconscious execution)?
│   │       │   ├─→ YES: High SLIP risk → Add forcing functions
│   │       │   └─→ NO: Conscious execution → Provide clear affordances
│   │
└─→ Is this EVENT-DRIVEN (environmental trigger)?
    └─→ YES: Begin at Stage 5 (Perceive state)
        ├─→ Stage 5: Perceive world state
        │   ├─→ Is feedback immediate (&lt;0.1s)?
        │   │   ├─→ NO: Add immediate feedback
        │   │   └─→ YES: Proceed to Stage 6
        │
        ├─→ Stage 6: Interpret perception
        │   ├─→ Does system state make sense?
        │   │   ├─→ NO: Gulf of Evaluation too wide → Improve conceptual model
        │   │   └─→ YES: Proceed to Stage 7
        │
        └─→ Stage 7: Compare with goal
            ├─→ Is outcome clear?
            │   ├─→ NO: Add better feedback + conceptual model
            │   └─→ YES: Action cycle complete
            │
            └─→ Goal achieved?
                ├─→ NO: Return to Stage 2 (new plan)
                └─→ YES: END
```

### Design Evaluation Decision Tree

```
EVALUATE DESIGN: Start here
│
├─→ Discoverability Check
│   ├─→ Can user determine possible actions without instructions?
│   │   ├─→ NO: Missing signifiers → Add visible indicators
│   │   └─→ YES: Check constraints
│   │
│   ├─→ Are constraints visible and effective?
│   │   ├─→ NO: Add physical/semantic/cultural/logical constraints
│   │   └─→ YES: Check mapping
│   │
│   └─→ Is control-to-effect mapping natural?
│       ├─→ NO: Redesign spatial relationships or use cultural conventions
│       └─→ YES: Proceed to Understanding Check
│
├─→ Understanding Check
│   ├─→ Does system image communicate conceptual model?
│   │   ├─→ NO: Improve structure, labels, documentation
│   │   └─→ YES: Check feedback
│   │
│   ├─→ Is feedback immediate and informative?
│   │   ├─→ NO: Add/improve feedback mechanisms
│   │   └─→ YES: Check processing levels
│   │
│   └─→ Are all three levels addressed?
│       ├─→ Visceral: Is it aesthetically appealing?
│       ├─→ Behavioral: Does it support learned patterns?
│       └─→ Reflective: Will memory of use be positive?
│
└─→ Error Prevention Check
    ├─→ What error types are possible?
    │   ├─→ SLIPS (execution errors)?
    │   │   └─→ Add forcing functions, reduce steps, prevent capture
    │   ├─→ MISTAKES (planning errors)?
    │   │   └─→ Improve conceptual model, add feedforward
    │   └─→ MEMORY LAPSES?
    │       └─→ Put knowledge in world, add reminders, minimize steps
    │
    ├─→ Are modes present?
    │   ├─→ YES: MODE ERROR risk
    │   │   ├─→ Can you eliminate modes?
    │   │   │   ├─→ YES: Eliminate them
    │   │   │   └─→ NO: Make current mode extremely salient
    │   │
    └─→ Does security exceed human capability?
        └─→ YES: Users will create workarounds → Redesign for actual capabilities
```

### Root Cause Analysis Process

```
INCIDENT OCCURS
│
├─→ Ask: "What happened?" (Identify symptom)
│   └─→ Document observable failure
│
├─→ Ask: "Why did this happen?" (First cause)
│   ├─→ Answer: "Human error"
│   │   └─→ NEVER STOP HERE - This is anti-pattern
│   └─→ Continue investigation
│
├─→ Ask: "Why did the human make that error?" (Second why)
│   ├─→ Was signifier missing/unclear?
│   ├─→ Was feedback absent/poor?
│   ├─→ Was mapping unnatural?
│   ├─→ Was conceptual model wrong?
│   └─→ Continue for each factor
│
├─→ Ask: "Why was design inadequate?" (Third why)
│   └─→ Investigate design process failures
│
├─→ Ask: "Why did process fail?" (Fourth why)
│   └─→ Investigate organizational factors
│
├─→ Ask: "Why did organization allow this?" (Fifth why)
│   └─→ Reach fundamental systemic cause
│
└─→ DECISION: Fix person or fix system?
    ├─→ Multiple people made same error?
    │   └─→ YES: System design failure → REDESIGN SYSTEM
    └─→ Isolated incident with unique circumstances?
        └─→ Investigate further - may still be system issue
```

## Anti-Patterns

### 🚫 Blaming Human Error

**Novice approach:**
- Incident occurs
- Investigation identifies operator action as proximate cause  
- Conclusion: "Human error - operator needs retraining"
- Action: Discipline/replace operator, add more warnings
- Timeline: Immediate blame assignment within hours/days

**Expert approach:**
- Incident occurs
- Acknowledge human action as symptom, not cause
- Apply Five Whys: "Why did operator make that choice?"
- Discover: Ambiguous signifier, mode confusion, inadequate feedback, excessive memory load
- Conclusion: "System failed to support human capabilities"
- Action: Redesign interface to prevent error conditions
- Timeline: Weeks of investigation to understand systemic factors

**Shibboleth:** "If an error is common, it's a design failure. Human error usually is a result of poor design: it should be called system error."

---

### 🚫 Norman Doors (Signifier Failure)

**Novice approach:**
- Design beautiful door with minimal visual interruption
- Use identical hardware on both sides
- Add small "PUSH" sign when people struggle
- Blame users for not reading sign
- Timeline: Sign added after first complaints (days)

**Expert approach:**
- Design inherently communicates operation
- Push side: Flat plate (anti-affordance for pulling)
- Pull side: Vertical handle (affordance for gripping)
- Hinge side visible where applicable
- No signs needed - hardware IS the signifier
- Timeline: Correct from initial design specification

**Shibboleth:** "The design of the door should indicate how to work it without any need for signs, certainly without any need for trial and error."

---

### 🚫 Mode Errors

**Novice approach:**
- Single button performs different functions in different modes
- Mode indicated by small icon or buried in menu
- User manual explains mode system
- "Users should remember current mode"
- Timeline: Mode confusion appears immediately but attributed to user error

**Expert approach:**
- Minimize modes entirely - use different controls for different functions
- If modes unavoidable: Make current mode EXTREMELY salient
- Use forcing functions to prevent dangerous mode transitions
- Physical mode indicators that cannot be overlooked
- Test with interruptions to verify mode clarity
- Timeline: Mode clarity validated during prototype testing before release

**Shibboleth:** "Mode errors are design errors. When equipment has multiple modes, the equipment must make the mode clearly visible."

---

### 🚫 Knowledge-In-Head Assumption

**Novice approach:**
- Expect users to memorize 8+ character passwords with mixed case, numbers, symbols
- Require remembering multi-step procedures
- Provide training once, assume retention
- "Users need to pay more attention"
- Timeline: Password policies created in single meeting

**Expert approach:**
- Recognize working memory holds 3-7 items, fragile under interruption
- Design puts knowledge in world: Structure, constraints, visible reminders
- Multi-factor authentication: "Something you have" + "something you know"
- Procedures self-evident from interface structure
- Checklists and external aids for critical sequences
- Timeline: Iterative testing reveals memory failures; design evolves

**Shibboleth:** "The most effective way of helping people remember is to make it unnecessary. Put required knowledge in the world."

---

### 🚫 Missing Feedback

**Novice approach:**
- Button press triggers background process
- No indication action was received
- User unsure if click registered
- User clicks multiple times ("button mashing")
- System processes multiple requests
- Timeline: Complaint emerges after users discover duplicates (days/weeks)

**Expert approach:**
- Immediate feedback within 0.1 seconds of action
- Button shows depressed state
- Progress indicator for operations &gt;1 second
- Clear completion confirmation
- Prevent duplicate actions through lock-in forcing function
- Timeline: Feedback designed into initial prototype

**Shibboleth:** "Feedback must be immediate, informative, and appropriately prioritized. Poor feedback can be worse than no feedback."

---

### 🚫 Aesthetics Over Usability

**Novice approach:**
- Hide all controls for visual minimalism
- Invisible door hardware (smooth glass)
- Touch-sensitive surfaces with no tactile feedback
- "Clean design" means featureless
- Timeline: Awards received; usability complaints ignored for years

**Expert approach:**
- Beauty and usability need not conflict
- Controls visible but elegantly integrated
- Signifiers enhance rather than detract from aesthetics
- Address visceral (beauty) AND behavioral (usability) AND reflective (pride of ownership)
- Timeline: Iterative prototypes balance all three processing levels

**Shibboleth:** "Attractive things work better - but only when they ALSO work well. Good design is invisible because it fits needs perfectly."

---

### 🚫 Excessive Security Theater

**Novice approach:**
- 12+ character passwords changed monthly
- Complex rules: uppercase, lowercase, numbers, symbols, no dictionary words
- Multiple authentication steps for routine tasks
- Lock users out after 3 failed attempts
- Timeline: Security policy implemented top-down in single quarter

**Expert approach:**
- Recognize humans cannot remember 50+ complex passwords
- Accept reality: Excessive security → insecurity via workarounds
- Users write passwords on monitors, use "Password123!", disable locks
- Design FOR human limitations: Password managers, biometrics, tokens
- Balance security with usability to prevent counterproductive behavior
- Timeline: Security usability testing reveals actual user behavior; policy adjusted

**Shibboleth:** "Making systems too secure makes them less secure. We must accept human behavior the way it is, not the way we wish it to be."

## Mental Models & Shibboleths

**Gulf Metaphor:**
- Novice: "Users need training to cross the gulf"
- Expert: "Designer builds bridges across gulfs through signifiers (execution) and feedback + conceptual models (evaluation)"

**Knowledge Distribution:**
- Novice: "Users should memorize procedures"
- Expert: "Combination of person + artifact creates intelligence; design puts knowledge in world"

**Error Attribution:**
- Novice: "Operator error caused failure"
- Expert: "Never stop at human error - apply Five Whys to reach systemic cause"

**Swiss Cheese Model:**
- Novice: "Find the single root cause"
- Expert: "Accidents occur when holes in multiple defensive layers align simultaneously"

**Action Cycles:**
- Novice: "Users always start with clear goals"
- Expert: "Behavior can be goal-driven (top-down) or event-driven (opportunistic) - design supports both"

**Processing Levels:**
- Novice: "Focus on functionality"
- Expert: "Address visceral (immediate aesthetics), behavioral (learned patterns), and reflective (long-term memory and meaning)"

## Temporal Knowledge

**1988 (Original Edition):** Focus on affordances; academic cognitive psychology perspective; "Psychology of Everyday Things" title emphasized scientific foundation

**2013 (Revised Edition):** Shifted emphasis from affordances to signifiers after recognizing confusion in digital design community; added chapters on emotion, experience design, and design thinking; incorporated business and industry perspectives from author's Apple/HP experience

**Pre-automation era (&lt;1900s):** Direct physical manipulation; immediate mechanical feedback; human operators controlled complex systems with transparent cause-effect relationships

**Modern automation (1900s-2000s):** Separation of users from direct system control; new error modes from automation; "ironies of automation" where increased automation demands higher operator skill

**Touchscreen era (2000s+):** Loss of physical affordances; gesture-based interaction; metaphor shift from "moving window" to "moving text" scrolling; elimination of tactile feedback requiring stronger visual signifiers

**Current challenge (2010s+):** Balancing security requirements with human cognitive limitations; designing for interruption-heavy multitasking environments; accommodating aging populations with declining capabilities

## References
- Source: "The Design of Everyday Things" (Revised and Expanded Edition, 2013) by Don Norman
- Original Edition: "The Psychology of Everyday Things" (1988)
- Foundation: Cognitive psychology research on human perception, memory, action, and error