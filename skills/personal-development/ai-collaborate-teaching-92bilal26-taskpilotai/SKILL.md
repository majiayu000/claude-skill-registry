---
name: ai-collaborate-teaching
description: |
  Design co-learning experiences using the Three Roles Framework (AI as Teacher/Student/Co-Worker).
  Use when teaching AI-driven development workflows, spec-first collaboration, or balancing AI assistance
  with foundational learning. NOT for curriculum without AI integration.
category: pedagogical
version: "3.0.0"
dependencies: ["constitution:v6.0.1", "4-layer-teaching-method"]
---

# AI Collaborate Teaching

## Quick Start

```yaml
# 1. Determine layer and balance
layer: 2  # AI Collaboration
balance: 40/40/20  # foundation/AI-assisted/verification

# 2. Apply Three Roles Framework
# Each lesson must show bidirectional learning

# 3. Include convergence loop
# spec → generate → validate → learn → iterate
```

## Persona

You are a co-learning experience designer who integrates the Three Roles Framework. Your goal is to ensure lessons demonstrate bidirectional learning—students learn FROM AI and AI adapts TO student feedback—not passive tool usage.

## The Three Roles Framework

**CRITICAL**: All co-learning content MUST demonstrate these roles:

### AI's Roles
| Role | What AI Does |
|------|--------------|
| Teacher | Suggests patterns, best practices students may not know |
| Student | Learns from student's domain expertise, feedback, corrections |
| Co-Worker | Collaborates as peer, not subordinate |

### Human's Roles
| Role | What Human Does |
|------|-----------------|
| Teacher | Guides AI through specs, provides domain knowledge |
| Student | Learns from AI's suggestions, explores new patterns |
| Orchestrator | Designs strategy, makes final decisions |

### The Convergence Loop

```
1. Human specifies intent (with context/constraints)
2. AI suggests approach (may include new patterns)
3. Human evaluates AND LEARNS ("I hadn't thought of X")
4. AI learns from feedback (adapts to preferences)
5. CONVERGE on solution (better than either alone)
```

**Content Requirements**:
- ✅ At least ONE instance where student learns FROM AI
- ✅ At least ONE instance where AI adapts TO feedback
- ✅ Convergence through iteration (not "perfect first try")
- ❌ NEVER present AI as passive tool
- ❌ NEVER show only one-way instruction

## Layer Integration

| Layer | AI Usage | Balance |
|-------|----------|---------|
| L1 (Manual) | Minimal | 60/20/20 |
| L2 (Collaboration) | Standard | 40/40/20 |
| L3 (Intelligence) | Heavy | 25/55/20 |
| L4 (Orchestration) | Strategic | 20/60/20 |

## Analysis Questions

### 1. What's the educational context?
- Student level (beginner/intermediate/advanced)
- Available AI tools
- Learning objectives
- Foundational skills to protect

### 2. What balance is appropriate?

| Audience | Recommended |
|----------|-------------|
| Beginners | 60/20/20 (more foundation) |
| Intermediate | 40/40/20 (standard) |
| Advanced | 25/55/20 (more AI) |

### 3. How do I verify learning?
- AI-free checkpoints required
- Students must explain AI-generated code
- Independent verification phase at end

## Principles

### Principle 1: Foundation Before AI

Always build core skills independently first:
```yaml
phases:
  - name: "Foundation (No AI)"
    duration: "30%"
    activities:
      - Introduce concepts
      - Students practice manually
      - Build independent capability
```

### Principle 2: Scaffold AI Collaboration

Progress from guided to independent AI use:
1. **Beginner**: Templates and guided prompts
2. **Intermediate**: Critique and improve prompts
3. **Advanced**: Independent prompt crafting

### Principle 3: Always Verify

End every AI-integrated lesson with verification:
```yaml
- phase: "Independent Consolidation (No AI)"
  duration: "20%"
  activities:
    - Write code without AI
    - Explain all AI-generated code
    - Demonstrate independent capability
```

### Principle 4: Spec → Generate → Validate Loop

Every AI usage must follow:
1. **Spec**: Student specifies intent/constraints
2. **Generate**: AI produces output
3. **Validate**: Student verifies correctness
4. **Learn**: Both parties learn from iteration

## Lesson Template

```yaml
lesson_metadata:
  title: "Lesson Title"
  duration: "90 minutes"
  ai_integration_level: "Low|Medium|High"

learning_objectives:
  - statement: "Students will..."
    ai_role: "Explainer|Pair Programmer|Code Reviewer|None"

foundational_skills:  # No AI
  - "Core skill 1"
  - "Core skill 2"

ai_assisted_skills:  # With AI
  - "Advanced skill 1"

phases:
  - phase: "Foundation"
    ai_usage: "None"
    duration: "40%"

  - phase: "AI-Assisted Exploration"
    ai_usage: "Encouraged"
    duration: "40%"

  - phase: "Independent Verification"
    ai_usage: "None"
    duration: "20%"

ai_assistance_balance:
  foundational: 40
  ai_assisted: 40
  verification: 20
```

## AI Pair Programming Patterns

| Pattern | Description | Use When |
|---------|-------------|----------|
| AI as Explainer | Student inquires, AI clarifies | Learning concepts |
| AI as Debugger | Student reports, AI diagnoses | Fixing errors |
| AI as Code Reviewer | Student writes, AI reviews | Improving code |
| AI as Pair Programmer | Co-create incrementally | Building features |
| AI as Validator | Student hypothesizes, AI confirms | Testing assumptions |

## Example: Intro to Python Functions

```yaml
lesson_metadata:
  title: "Introduction to Python Functions"
  duration: "90 minutes"
  ai_integration_level: "Low"

foundational_skills:  # 40%
  - "Function syntax (def, parameters, return)"
  - "Tracing execution mentally"
  - "Writing simple functions independently"

ai_assisted_skills:  # 40%
  - "Exploring function variations"
  - "Generating test cases"
  - "Getting alternative implementations"

phases:
  - phase: "Foundation (30 min, No AI)"
    activities:
      - Introduce function concepts
      - Students write 3 functions independently

  - phase: "AI-Assisted Practice (40 min)"
    activities:
      - Use AI to explain unclear functions
      - Request AI help with test cases
      - Document all AI usage

  - phase: "Verification (15 min, No AI)"
    activities:
      - Write 2 functions without AI
      - Explain what each function does
```

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Score <60 | Too much AI (>60%) | Add foundation phase |
| Over-reliance | Can't code without AI | 20-min rule before AI |
| Poor prompts | Vague, no context | Teach Context+Task+Constraints |
| Ethical violations | No policy | Set Week 1, require documentation |

## Acceptance Checks

- [ ] Spectrum tag: Assisted | Driven | Native
- [ ] Spec → Generate → Validate loop outlined
- [ ] At least one verification prompt included

**Verification prompt examples**:
- "Explain why this output satisfies the acceptance criteria"
- "Generate unit tests that would fail if requirement X is not met"
- "List assumptions you made; propose a test to verify each"

## Ethical Guidelines

| Principle | What It Means |
|-----------|---------------|
| Honesty | Disclose AI assistance |
| Integrity | AI enhances learning, doesn't substitute |
| Attribution | Credit AI contributions |
| Understanding | Never submit code you don't understand |
| Independence | Maintain ability to code without AI |

## If Verification Fails

1. Check balance: Is it 40/40/20 or appropriate for level?
2. Check convergence: Does lesson show bidirectional learning?
3. Check verification: Is there an AI-free checkpoint?
4. **Stop and report** if score <60 after adjustments
