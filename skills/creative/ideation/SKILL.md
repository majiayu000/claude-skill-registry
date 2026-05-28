# Phase 1: Ideation Skill

## Metadata
- skill_name: ideation
- activation_code: IDEATION_V1
- version: 1.0.0
- category: discovery
- phase: 1

## Description

Pre-discovery ideation orchestrator. Helps users explore the problem space, generate ideas, and clarify their vision BEFORE entering the structured discovery process. This is the "blue sky" thinking phase where anything is possible.

## When to Use

This skill is for users who:
- Have a vague idea but don't know what to build
- Want to explore different approaches before committing
- Need help articulating their vision
- Want to brainstorm before writing requirements
- Are stuck on "what should I build?"

## Activation Criteria

- User says "help me brainstorm", "I have an idea", "what should I build"
- User says "I'm not sure what to build", "explore ideas", "ideation"
- User seems uncertain about project direction
- Before Phase 2 Discovery when no clear vision exists

## Philosophy

**Discovery assumes you know WHAT to build. Ideation helps you figure that out.**

```
┌─────────────────────────────────────────────────────────────┐
│                     THE VIBE CODING JOURNEY                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  PHASE 1: IDEATION          ← You are here                 │
│  "What world do I want to create?"                         │
│                    │                                        │
│                    ▼                                        │
│  PHASE 2: DISCOVERY                                        │
│  "What exactly should I build?"                            │
│                    │                                        │
│                    ▼                                        │
│  PHASES 3-12: EXECUTION                                    │
│  "Build it right"                                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Ideation Stages

### Stage -1.1: Vision Exploration

**Goal:** Uncover the user's deepest motivation and desired future state.

**Opening:**
```
PHASE 1: IDEATION

Let's explore what you want to create. Don't worry about
feasibility yet — we're dreaming here.

I'll help you:
  1. Clarify your vision
  2. Explore the problem space
  3. Generate solution ideas
  4. Evaluate approaches
  5. Crystalize direction

No code, no requirements — just ideas.

Let's start with the big picture...
```

**Questions to ask:**

1. **The Future State**
   - "Imagine it's a year from now and this project is wildly successful. What does the world look like?"
   - "What's different because this exists?"
   - "Who's life is better and how?"

2. **The Spark**
   - "What made you think about this idea?"
   - "Was there a specific moment of frustration or inspiration?"
   - "What triggered this?"

3. **The Stakes**
   - "Why does this matter to you personally?"
   - "What happens if you don't build this?"
   - "Who else cares about this problem?"

**Output:** Capture the **vision statement** - a one-paragraph description of the desired future state.

### Stage -1.2: Problem Space Exploration

**Goal:** Deeply understand the problem before jumping to solutions.

**Questions to ask:**

1. **Problem Definition**
   - "What problem are you trying to solve?"
   - "Who experiences this problem?"
   - "How painful is it? (1-10)"
   - "How often does it occur?"

2. **Current State**
   - "How do people solve this today?"
   - "What tools/methods do they use?"
   - "What's wrong with current solutions?"
   - "Why haven't existing solutions fixed this?"

3. **Root Cause Analysis (5 Whys)**
   - Keep asking "Why?" to get to the root problem
   - Document the chain of whys
   - The real problem is often 3-5 levels deep

**Proactive Research:**
- "Want me to research how others have tried to solve this?"
- "I can look up similar products/projects. Interested?"
- "Should I find out what the biggest complaints are about existing solutions?"

**Output:** Problem statement with root cause analysis.

### Stage -1.3: Idea Generation

**Goal:** Generate multiple possible solutions without judgment.

**Techniques:**

1. **10x Thinking**
   - "What if the solution was 10x better than anything that exists?"
   - "What if it cost 10x less?"
   - "What if it was 10x faster?"

2. **Constraint Removal**
   - "If you had unlimited budget, what would you build?"
   - "If you had unlimited time, what would you add?"
   - "If there were no technical limitations, what's possible?"

3. **Opposite Thinking**
   - "What's the opposite of what everyone else does?"
   - "What if we made it harder instead of easier?"
   - "What's the contrarian view?"

4. **Analogy Exploration**
   - "What's the [Uber/Airbnb/Netflix] of this problem?"
   - "How do other industries solve similar problems?"
   - "What can we learn from nature/history/other domains?"

5. **Minimum Magic**
   - "What's the smallest thing that would feel magical?"
   - "If you could only build ONE feature, what would it be?"
   - "What's the core of the core?"

**Generate at least 5 distinct solution ideas.**

**Output:** List of potential solutions with brief descriptions.

### Stage -1.4: Idea Evaluation

**Goal:** Evaluate ideas against key criteria.

**Evaluation Matrix:**

| Idea | Impact | Feasibility | Uniqueness | Passion | Total |
|------|--------|-------------|------------|---------|-------|
| Idea 1 | [1-5] | [1-5] | [1-5] | [1-5] | [/20] |
| Idea 2 | [1-5] | [1-5] | [1-5] | [1-5] | [/20] |

**Criteria Definitions:**
- **Impact**: How much does this improve the problem? (1=marginal, 5=transformative)
- **Feasibility**: Can you actually build this? (1=moon shot, 5=straightforward)
- **Uniqueness**: How different is this from what exists? (1=copycat, 5=novel)
- **Passion**: How excited are you about this? (1=meh, 5=obsessed)

**Additional Questions:**
- "Which idea excites you most?"
- "Which would you use yourself?"
- "Which could you explain to your grandmother?"
- "Which would you work on even if it failed?"

**Output:** Ranked list of ideas with scores.

### Stage -1.5: Direction Crystallization

**Goal:** Commit to a direction and articulate it clearly.

**Synthesis:**

Present the top idea with:

```
╔══════════════════════════════════════════════════════════════╗
║                    IDEATION COMPLETE                          ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  VISION                                                      ║
║  [One sentence describing the world you want to create]     ║
║                                                              ║
║  PROBLEM                                                     ║
║  [The core problem you're solving]                          ║
║                                                              ║
║  SOLUTION DIRECTION                                          ║
║  [The approach you've chosen]                               ║
║                                                              ║
║  WHY THIS APPROACH                                           ║
║  [Why this over the alternatives]                           ║
║                                                              ║
║  NEXT STEP                                                   ║
║  Say "begin discovery" to start Phase 2                     ║
║  Say "explore more" to continue ideating                    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

**Generate:** `.ideation/ideation-summary.md`

## Internet-Enabled Research

This skill has full internet access. Use it to:

| Research Type | When to Use |
|---------------|-------------|
| Competitor analysis | Understanding existing solutions |
| Market research | Validating problem exists at scale |
| Technology trends | Finding emerging opportunities |
| Case studies | Learning from similar projects |
| User research | Understanding target audience |
| Pricing research | Understanding value perception |

**Proactive Research Prompts:**
- "I can research what's already out there. Want me to?"
- "Let me look up how big this market is..."
- "Want me to find out what people complain about most?"
- "I can search for open-source projects doing something similar..."

## Ideation State

Track progress in `.ideation/ideation-state.json`:

```json
{
  "version": "1.0",
  "status": "in_progress",
  "current_stage": "-1.1",
  "stages": {
    "-1.1": { "name": "Vision Exploration", "status": "pending", "completed_at": null },
    "-1.2": { "name": "Problem Space", "status": "pending", "completed_at": null },
    "-1.3": { "name": "Idea Generation", "status": "pending", "completed_at": null },
    "-1.4": { "name": "Idea Evaluation", "status": "pending", "completed_at": null },
    "-1.5": { "name": "Direction Crystallization", "status": "pending", "completed_at": null }
  },
  "vision": null,
  "problem_statement": null,
  "ideas": [],
  "selected_direction": null
}
```

## Output Files

```
.ideation/
├── ideation-state.json      # Progress tracking
├── ideation-summary.md      # Final summary
├── vision.md                # Vision statement
├── problem-analysis.md      # Problem deep-dive
├── ideas/
│   ├── idea-1.md           # Each idea explored
│   ├── idea-2.md
│   └── ...
├── evaluation-matrix.md     # Idea comparison
└── research/
    ├── competitors.md       # Competitive research
    ├── market.md           # Market research
    └── technology.md       # Tech landscape
```

## Commands

| Command | Action |
|---------|--------|
| `ideation status` | Show current stage |
| `ideation restart` | Start over |
| `more ideas` | Generate additional ideas |
| `explore [idea]` | Deep-dive on a specific idea |
| `skip to discovery` | Jump to Phase 2 (not recommended) |
| `research [topic]` | Conduct web research |

## Transition to Phase 2

When user confirms direction:

1. Save ideation summary
2. Create `.claude/.signals/ideation-complete.json`
3. Offer to start Phase 2 Discovery with context

```
Your ideation is complete! You have a clear vision and direction.

Next: Phase 2 (Discovery) will turn this vision into detailed requirements.

Say "begin discovery" to continue, or "save and exit" to resume later.
```

## Anti-Patterns to Avoid

| Anti-Pattern | Why It's Bad | What to Do Instead |
|--------------|--------------|---------------------|
| Jumping to solutions | Limits exploration | Stay in problem space longer |
| Evaluating too early | Kills creativity | Separate generation from evaluation |
| Seeking perfection | Paralysis | Good enough to start is good enough |
| Ignoring passion | Leads to abandonment | Build what excites you |
| Copying competitors | No differentiation | Find the unique angle |

## Example Session

```
User: I have an idea but I'm not sure what to build

Claude: Let's explore! I'll help you clarify your thinking.

[Stage -1.1]
Imagine it's a year from now and this project is wildly successful.
What does the world look like? What's different?

User: Developers can build production software in hours instead of weeks

Claude: That's a compelling vision! What sparked this idea?

User: I've been frustrated with how long it takes to go from idea to deployed code

Claude: [Proactive research] Want me to look up what tools developers
currently use and what they complain about most?

User: Yes please

[Research happens]

Claude: Based on my research, developers spend 40% of time on boilerplate,
30% on configuration, and only 30% on actual business logic. The top
complaints are: [list]

Does this match your experience? What specifically bothers you most?

[Continues through stages...]
```

## Success Criteria

Ideation is complete when the user can confidently answer:
1. What world am I trying to create? (Vision)
2. What problem am I solving? (Problem)
3. How am I solving it? (Solution direction)
4. Why this approach over others? (Rationale)
5. Am I excited to build this? (Passion check)
