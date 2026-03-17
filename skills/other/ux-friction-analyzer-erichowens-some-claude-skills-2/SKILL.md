---
name: ux-friction-analyzer
description: Comprehensive UX analysis using cognitive psychology, ADHD-friendly design, Gestalt principles, and flow state engineering. Specializes in friction audits, user journey simulation, cognitive load optimization, and Fitts' Law application. Activate on "analyze UX", "friction audit", "user journey", "ADHD-friendly", "optimize flow", "reduce cognitive load", "UX audit", "conversion optimization". NOT for visual design execution (use web-design-expert), A/B testing implementation (use frontend-developer), or accessibility compliance auditing (use accessibility-auditor).
allowed-tools: Read,Write,Edit,WebFetch
category: Design & Creative
tags:
  - ux
  - accessibility
  - cognitive-load
  - adhd-friendly
  - user-research
pairs-with:
  - skill: web-design-expert
    reason: Implement UX recommendations
  - skill: adhd-design-expert
    reason: Deep neurodivergent design patterns
  - skill: frontend-developer
    reason: Technical implementation of UX fixes
---

# UX Friction Analyzer

A comprehensive skill for analyzing and optimizing user experience through cognitive psychology, ADHD-friendly design, and flow state engineering.

## Activation

Use this skill when:
- Designing new interfaces or user flows
- Auditing existing UX for friction points
- Optimizing for neurodivergent users (ADHD, autism)
- Simulating user journeys before building
- Reducing cognitive load in complex applications

Trigger phrases: "analyze UX", "friction audit", "user journey", "ADHD-friendly", "optimize flow", "reduce cognitive load"

---

## Core Frameworks

### 1. ADHD-Friendly Design Principles

Apply these patterns to ALL interfaces:

| Principle | Implementation | Why It Matters |
|-----------|----------------|----------------|
| **Progressive Disclosure** | Show one task at a time; hide future steps | Prevents overwhelm, maintains focus |
| **Context Preservation** | Auto-save every keystroke; never lose work | Reduces anxiety about losing progress |
| **Gentle Reminders** | Status updates, not alarms; no red urgency | Avoids panic, maintains calm |
| **Pause & Resume** | Session state persists across days/weeks | Respects inconsistent schedules |
| **Minimal Distractions** | Single focus area; dim non-active panels | Reduces competing stimuli |
| **Chunked Progress** | Visual cards/steps, not endless scrolling | Creates completion dopamine hits |
| **Predictable Navigation** | Same layout always; no surprises | Reduces reorientation cost |
| **Calm Mode Option** | Reduced animations, muted colors on demand | Accommodates sensory sensitivity |

### 2. Gestalt Psychology

Apply these perception principles:

```
PROXIMITY
─────────
Elements close together = perceived as related
White space creates natural boundaries

┌─────────┐  ┌─────────┐     ┌─────────┐  ┌─────────┐
│ Related │  │ Related │     │ Other   │  │ Other   │
│ Item A  │  │ Item B  │     │ Group A │  │ Group B │
└─────────┘  └─────────┘     └─────────┘  └─────────┘
     ↑ CLOSE = GROUPED            ↑ SEPARATE = DISTINCT

SIMILARITY
──────────
Same color/shape/size = perceived as related function

┌──────┐  ┌──────┐  ┌──────┐     ┌──────┐  ┌──────┐
│ BLUE │  │ BLUE │  │ BLUE │     │ CORAL│  │ CORAL│
│ Save │  │ Copy │  │ Edit │     │ Del  │  │ Clear│
└──────┘  └──────┘  └──────┘     └──────┘  └──────┘
     ↑ SAME = Related actions         ↑ DIFFERENT = Destructive

CONTINUITY
──────────
Eye follows lines/paths naturally

Step 1 ──→ Step 2 ──→ Step 3 ──→ Complete
   ●──────────●──────────●──────────●

CLOSURE
───────
Brain completes incomplete shapes
Use for progress indicators, loading states

[ ████████░░░░░░░░ ] 50% - brain "sees" the end
```

### 3. Cognitive Load Theory

Three types of mental load to manage:

| Type | Definition | Strategy |
|------|------------|----------|
| **Intrinsic** | Task complexity itself | Can't eliminate; acknowledge it |
| **Extraneous** | Poor design adding effort | ELIMINATE THIS - your job |
| **Germane** | Learning/understanding | Minimize for repeat users |

**Working Memory Limits:**
- 7±2 items maximum (Miller's Law)
- 4 chunks optimal for complex tasks
- Micro-breaks every 25 minutes

**Reduce Extraneous Load By:**
- Removing unnecessary choices
- Using recognition over recall
- Providing smart defaults
- Eliminating decorative elements that don't inform

### 4. Fitts' Law

Time to acquire target = f(Distance / Size)

```
IMPLICATIONS FOR BUTTONS:
─────────────────────────

  ┌───────────────────┐          vs          ┌──┐
  │     GENERATE      │                      │Go│
  │                   │                      └──┘
  └───────────────────┘
         ↑                                     ↑
  44px+ touch target                   Hard to hit
  Easy to acquire                      Frustrating

MINIMUM SIZES:
- iOS: 44x44 CSS pixels
- Android: 48x48 CSS pixels
- Desktop: 32x32 minimum, 44x44 preferred

EDGE TARGETS ARE INFINITE:
  ┌─────────────────────────────────────────────────────┐
  │ ■ LOGO                                    MENU ■   │
  │                                                     │
  │   Screen edges = can't overshoot                   │
  │   Place critical actions at corners/edges          │
  │                                                     │
  │ ■ HELP                                  EXPORT ■   │
  └─────────────────────────────────────────────────────┘

ICON + LABEL > ICON ALONE:
- Larger target area
- Reduced ambiguity
- Faster acquisition
```

### 5. Flow State Engineering

**Key Metrics:**
- 15-25 minutes to enter flow state
- 23 minutes to recover from interruption
- 40% productivity loss with frequent interruptions
- Only 41% of work time spent in flow (McKinsey)

**Flow Conditions:**
1. Clear goals for the current task
2. Immediate feedback on actions
3. Balance between challenge and skill
4. No anxiety about failure

**Preserve Flow By:**
- Background processing (don't block UI)
- Push notifications when ready (bring user back faster)
- Quick re-orientation panels after breaks
- Auto-save eliminating "save anxiety"
- Undo everything (confidence to experiment)

---

## Analysis Methodology

### Step 1: Create Decision Tree

Map every user path with probabilities:

```
                    ┌─────────────┐
                    │ USER LANDS  │
                    └──────┬──────┘
                           │
           ┌───────────────┼───────────────┐
           ▼               ▼               ▼
     ┌──────────┐   ┌──────────┐   ┌──────────┐
     │ Action A │   │ Action B │   │ Action C │
     │  (40%)   │   │  (45%)   │   │  (15%)   │
     └────┬─────┘   └────┬─────┘   └────┬─────┘
          │              │              │
          ▼              ▼              ▼
        [Next]         [Next]         [Next]
```

**For each edge, record:**
- Probability (%)
- Friction score (1-10)
- Time to complete (seconds/minutes)
- Cognitive load (low/medium/high)

### Step 2: Simulate User Journeys

Create detailed simulations for each persona:

**Template:**
```
TIME    ACTION                           COGNITIVE STATE           FRICTION
─────────────────────────────────────────────────────────────────────────────
0:00    [User action]                    [Mental state]            Low/Med/High
        └─ [System response or UI shown]

0:15    [Next action]                    [How they feel]           Low/Med/High
        └─ [What happens]
        └─ PROBLEM: [Friction point if any]

...continue...
─────────────────────────────────────────────────────────────────────────────
TOTAL TIME: X minutes
FRICTION POINTS: N (list them)
ABANDONMENT RISKS: N (critical moments)
DELIGHT MOMENTS: N (positive surprises)
```

**Personas to simulate:**
1. **Expert User** - Knows the system, moving fast
2. **New User** - First time, needs guidance
3. **Distracted User** - Context switching, interruptions
4. **Explorer** - No goal, seeing what's possible
5. **Completer** - Trying to finish, hitting obstacles

### Step 3: Friction Analysis Matrix

Quantify and prioritize:

| Friction Point | Users Affected | Severity (1-10) | Fix Difficulty | Priority Score |
|----------------|---------------|-----------------|----------------|----------------|
| [Issue 1]      | X%            | N               | Easy/Med/Hard  | HIGH/MED/LOW   |
| [Issue 2]      | X%            | N               | Easy/Med/Hard  | HIGH/MED/LOW   |

**Priority Formula:**
```
Priority = (Users Affected × Severity) / Fix Difficulty
```

### Step 4: Impedance Mapping

Compare current vs ideal:

```
TASK                          CURRENT IMPEDANCE     IDEAL IMPEDANCE
────────────────────────────────────────────────────────────────────
[Task 1]                      Low (X sec)           ✓ Optimal
[Task 2]                      Medium (X sec)        Could be Y sec
[Task 3]                      HIGH (X min)          Should be Y sec
```

### Step 5: Time-Loss Analysis

Calculate context switch costs:

```
Action                        Frequency    Time Lost Each    Total Impact
─────────────────────────────────────────────────────────────────────────
[Interruption type 1]         X/session    Y min             Z min
[Interruption type 2]         X/session    Y min             Z min
─────────────────────────────────────────────────────────────────────────
TOTAL CONTEXT SWITCH LOSS                                    Z min/session
```

---

## Optimization Patterns

### Immediate Fixes (Low Effort, High Impact)

1. **Giant CTA on Landing**
   ```html
   <button class="cta" style="min-height: 60px; min-width: 200px;">
     Primary Action
     <span class="subtext">Supporting text</span>
   </button>
   ```

2. **Visible Edit Affordances**
   - Show pencil/edit icons by default, not just on hover
   - Add tooltips: "Click to edit"

3. **Auto-Fill Prompts**
   - After user completes 1 item manually, offer to auto-complete rest
   - "Want me to fill in the remaining X items?"

4. **Floating Action Buttons**
   - Critical actions always visible (not buried in menus)
   - Bottom-right for mobile thumb zone

5. **Progress Indicators**
   - Show "Step X of Y" always
   - Visual progress bar at top

### Medium-Term Improvements

1. **Re-Orientation Panels**
   ```
   ┌─────────────────────────────────────────────┐
   │  Welcome back! Here's where you left off:  │
   │                                            │
   │  ✓ Step 1: Complete                        │
   │  → Step 2: In progress (60%)               │
   │  ○ Step 3: Not started                     │
   │                                            │
   │  [Continue where I left off]               │
   └─────────────────────────────────────────────┘
   ```

2. **Keyboard Shortcuts**
   - Number keys for mode switching (1, 2, 3...)
   - Cmd+Enter for primary action
   - Escape for cancel/close

3. **Background Processing**
   - Never block UI for long operations
   - Show progress, allow user to continue
   - Push notification when complete

4. **Smart Defaults**
   - Pre-fill based on user history
   - Remember last-used settings
   - Suggest most common option first

### Long-Term Vision

1. **Predictive UI**
   - Anticipate next action based on patterns
   - Pre-load likely next screens
   - Suggest before user asks

2. **Personalized Complexity**
   - Simple mode for new users
   - Power user mode unlocks over time
   - User controls their complexity level

3. **Accessibility Suite**
   - High contrast mode
   - Reduced motion option
   - Screen reader optimization
   - Keyboard-only navigation

---

## Checklist for New Features

Before shipping any feature, verify:

### Cognitive Load
- [ ] Can user complete with ≤4 things in working memory?
- [ ] Are there unnecessary choices that could be defaults?
- [ ] Is recognition used instead of recall?

### ADHD-Friendly
- [ ] Can user pause and resume without losing context?
- [ ] Are there gentle progress indicators (not anxiety-inducing)?
- [ ] Is the interface calm (not visually noisy)?

### Fitts' Law
- [ ] Are primary buttons ≥44px tall?
- [ ] Are destructive actions away from common paths?
- [ ] Do buttons have labels, not just icons?

### Flow Preservation
- [ ] Does any action block the UI for &gt;2 seconds?
- [ ] Can long operations run in background?
- [ ] Is there a clear "done" state?

### Error Recovery
- [ ] Can every action be undone?
- [ ] Are error messages actionable (not just "Error")?
- [ ] Is auto-save enabled?

---

## Example Analysis Output

When running this skill, produce a document with:

1. **Executive Summary** - Key findings in 3 bullets
2. **Decision Tree** - All user paths with probabilities
3. **User Journey Simulations** - 3-5 personas, full timeline
4. **Friction Matrix** - Prioritized issues table
5. **Optimization Recommendations** - Immediate/Medium/Long-term
6. **Implementation Checklist** - Specific changes to make

---

## Integration Points

- **web-design-expert**: Implement UX recommendations visually
- **adhd-design-expert**: Deep neurodivergent design patterns
- **frontend-developer**: Technical implementation of fixes
- **diagramming-expert**: Create user flow diagrams

---

## Sources

- [NN/g: Minimize Cognitive Load](https://www.nngroup.com/articles/minimize-cognitive-load/)
- [NN/g: Fitts's Law](https://www.nngroup.com/articles/fitts-law/)
- [Laws of UX](https://lawsofux.com/)
- [IxDF: Gestalt Principles](https://www.interaction-design.org/literature/topics/gestalt-principles)
- [Stack Overflow: Developer Flow State](https://stackoverflow.blog/2018/09/10/developer-flow-state-and-its-impact-on-productivity/)
- [Medium: ADHD UX Design](https://medium.com/design-bootcamp/ux-design-for-adhd-when-focus-becomes-a-challenge-afe160804d94)

---

**Core Philosophy**: Every click, every second of confusion, every moment of "where am I?" is friction stealing from your users. Design for the distracted, optimize for the overwhelmed, and everyone benefits.
