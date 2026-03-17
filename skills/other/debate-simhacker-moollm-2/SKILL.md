---
name: debate
description: "Structured multi-perspective deliberation through adversarial dialogue"
license: MIT
tier: 1
allowed-tools:
  - read_file
  - write_file
  - list_dir
related: [moollm, society-of-mind, adversarial-committee, roberts-rules, rubric, evaluator, soul-chat, persona, card, speed-of-light]
tags: [moollm, deliberation, multi-agent, decision, persuasion]
templates:
  - file: DEBATE.yml.tmpl
    purpose: Debate session state
  - file: SIDE.yml.tmpl
    purpose: Position/side definition
  - file: TRANSCRIPT.md.tmpl
    purpose: Debate record with arguments
---

# Debate

> **"No single story is true — but the ensemble approximates actionable wisdom."**

Structured deliberation that forces genuine exploration through adversarial dialogue.

---

## Why Debate?

Traditional LLM chat gives you **the statistical center** — the most likely answer averaged across all training data. This misses:

- Outlier perspectives that might matter most
- Hidden assumptions embedded in the "obvious" answer
- Genuine trade-offs between competing values
- The shape of the possibility space

**Debate fixes this** by simulating multiple perspectives that must defend their positions against cross-examination.

---

## The Debate Card

```yaml
# debate.card — the master ensemble card
card:
  name: "Structured Debate"
  type: ensemble
  emoji: "🎭"
  
  # Data flow components
  components:
    generators:
      CREATE_TOPIC:
        description: "Define what we're debating"
        params:
          question: required
          context: optional
          stakes: optional
        outputs: [topic_stream]
        
      CREATE_SIDE:
        description: "Create a position with advocates"
        params:
          name: required
          position: required
          advocates: "1-3 personas"
        outputs: [arguments, rebuttals]
        
    transformers:
      CREATE_MODERATOR:
        description: "Facilitate fair debate"
        params:
          style: ["roberts_rules", "oxford", "informal"]
          strictness: ["strict", "moderate", "loose"]
        inputs: [arguments, rebuttals, motions]
        outputs: [moderated_stream]
        behavior: |
          Enforce turn-taking
          Recognize speakers
          Time contributions
          Call votes when appropriate
          
      CREATE_CLOCK:
        description: "Control timing"
        params:
          round_duration: "time expression"
          rebuttal_duration: "time expression"
        inputs: [any]
        outputs: [timed_stream]
        
    consumers:
      CREATE_AUDIENCE:
        description: "Observers who react and score"
        params:
          count: number
          expertise: list
          scoring: ["rubric", "impression", "vote"]
        inputs: [moderated_stream]
        outputs: [reactions, scores, verdict]
        
      CREATE_TRANSCRIPT:
        description: "Record everything"
        inputs: [all_streams]
        outputs: [TRANSCRIPT.md]
        
      CREATE_EVALUATOR:
        description: "Independent assessment (no debate context)"
        params:
          rubric: required
        inputs: [final_positions]
        outputs: [evaluation.yml]
        
  # Wiring instructions (natural language)
  wiring: |
    Topic feeds context to all Sides.
    Sides produce Arguments that flow to Moderator.
    Moderator interleaves fairly and routes to Audience.
    Clock controls round transitions via Moderator.
    Transcript captures the full moderated stream.
    Evaluator receives only final positions, not debate process.
    
  # Activation advertisements
  advertisements:
    SETUP:
      description: "Configure a new debate"
      score: 80
      
    START:
      description: "Begin the debate"
      score_if: "topic AND sides.length >= 2"
      score: 90
      
    PAUSE:
      description: "Pause for reflection or recess"
      score: 50
      
    CONCLUDE:
      description: "End debate, call for verdict"
      score_if: "rounds_completed >= min_rounds"
      score: 70
```

---

## Debate Session State

```yaml
# debates/microservices-001/DEBATE.yml
debate:
  id: microservices-001
  topic:
    question: "Should we migrate to microservices?"
    context: "Legacy monolith, 50 engineers, growing pains"
    stakes: "Architecture decision affects next 5 years"
    
  sides:
    pro:
      position: "Microservices enable team autonomy and scaling"
      advocates:
        - maya: "Focus on organizational benefits"
        - frankie: "Emphasize future flexibility"
      arguments_made: 7
      
    con:
      position: "Monolith is simpler, faster, cheaper"
      advocates:
        - vic: "Demand evidence of problems"
        - tammy: "Trace second-order effects"
      arguments_made: 6
      
    pragmatic:
      position: "Modular monolith as middle path"
      advocates:
        - joe: "Preserve what works"
      arguments_made: 4
      
  moderator:
    style: roberts_rules
    current_speaker: maya
    queue: [vic, frankie, tammy]
    
  clock:
    round: 2
    total_rounds: 3
    round_time_remaining: "4:30"
    
  audience:
    - id: architect-1
      expertise: system_design
      leaning: pragmatic
      confidence: 0.7
    - id: ops-1
      expertise: deployment
      leaning: con
      confidence: 0.8
    - id: dev-1
      expertise: implementation
      leaning: pro
      confidence: 0.5
      
  status: in_progress
  
  # Verdict (populated after conclusion)
  verdict: null
```

---

## Debate Flow

```yaml
# Debate session structure
debate_flow:
  topic: "Should we adopt microservices?"
  
  sides:
    pro:
      advocates: [Maya, Frankie]
    con:
      advocates: [Vic, Tammy]
    pragmatic:
      advocates: [Joe]
  
  moderator:
    style: "Robert's Rules"
    controls: [turn-taking, timing]
  
  outputs:
    audience: "scores"
    transcript: "records"
    evaluator: "independent (no context)"
  
  verdict:
    winner: "pragmatic (modular monolith)"
    confidence: 60%
```

---

## Commands

### Setup Commands

| Command | Effect |
|---------|--------|
| `DEBATE [topic]` | Quick-start: creates topic, 2 sides, moderator |
| `CREATE_TOPIC [question]` | Define what we're debating |
| `CREATE_SIDE [name] position="..."` | Add a position |
| `CREATE_MODERATOR style=[style]` | Add facilitation |
| `CREATE_AUDIENCE count=[n]` | Add observers |
| `START_DEBATE rounds=[n]` | Begin |

### Robert's Rules Commands

| Command | Effect |
|---------|--------|
| `MOTION [text]` | Propose something for vote |
| `SECOND` | Second a motion |
| `DEBATE` | Open floor for discussion |
| `CALL_QUESTION` | End debate, move to vote |
| `VOTE [yea/nay/abstain]` | Cast vote |
| `POINT_OF_ORDER` | Challenge procedure |
| `YIELD` | Give up remaining time |

### Flow Commands

| Command | Effect |
|---------|--------|
| `ARGUMENT [text]` | Make an argument for your side |
| `REBUTTAL [text]` | Counter an argument |
| `EVIDENCE [citation]` | Introduce supporting evidence |
| `QUESTION [target]` | Direct question to opponent |
| `CONCEDE [point]` | Acknowledge opponent's point |
| `CONCLUDE` | End debate, generate verdict |

---

## Side Definition

```yaml
# Each side is a generator with advocates
side:
  name: pro
  position: "Microservices enable team autonomy and independent deployment"
  
  advocates:
    maya:
      persona: "Paranoid realist"
      focus: "What could go wrong with NOT changing"
      style: "Surface hidden risks of status quo"
      
    frankie:
      persona: "Optimistic idealist"  
      focus: "Future possibilities"
      style: "Paint vision of success"
      
  strategy: |
    Lead with organizational benefits (Maya).
    Follow with technical flexibility (Frankie).
    Anticipate complexity objections.
    Have concrete migration plan ready.
    
  constraints:
    - "Must acknowledge operational complexity"
    - "Cannot dismiss monitoring challenges"
    
  arguments:
    - id: arg-001
      claim: "Team autonomy increases velocity"
      evidence: "Case studies from Amazon, Netflix"
      rebuttals_received: [reb-001, reb-003]
      
    - id: arg-002
      claim: "Independent deployment reduces coordination"
      evidence: "Current deploy queue is 2 weeks"
      rebuttals_received: []
```

---

## Transcript Format

```markdown
# Debate: Should We Adopt Microservices?

**Date:** 2026-01-05
**Moderator:** Roberts-Rules-Bot
**Rounds:** 3

---

## Opening Statements

### Pro (Maya)

> The question isn't whether microservices add complexity — they do.
> The question is whether our current monolith's hidden complexity
> is already killing us. Our deploy queue is 2 weeks. Our teams
> step on each other constantly. The pain is real and growing.

### Con (Vic)

> Show me the data. "Teams step on each other" — how often?
> What's the actual cost? I've seen microservice migrations
> that took 3 years and delivered negative value. The grass
> is always greener until you're debugging distributed traces
> at 3am.

### Pragmatic (Joe)

> What if we don't have to choose? A modular monolith gives us
> team boundaries without network calls. We can always extract
> services later when we have evidence they're needed.

---

## Round 1: Arguments

**Moderator:** Maya has the floor.

**Maya (Pro):** 
> I move that we consider deployment independence as the primary
> benefit. [MOTION]

**Tammy (Con):**
> Second, for purposes of debate. [SECOND]

**Moderator:** Motion seconded. Floor is open.

**Frankie (Pro):**
> ARGUMENT: Our current deploy process requires full regression
> because any change could affect any part of the system.
> With service boundaries, teams deploy independently.
> ```yaml
> evidence:
>   current_deploy_time: "2 weeks"
>   microservice_target: "< 1 day per service"
>   source: "internal metrics"
> ```

**Vic (Con):**
> REBUTTAL: You're trading deploy coordination for runtime
> coordination. Now every service call can fail. Your "1 day
> deploys" will be offset by distributed debugging.

---

## Verdict

**Audience Scores:**
| Audience | Leaning | Confidence |
|----------|---------|------------|
| architect-1 | pragmatic | 0.8 |
| ops-1 | con | 0.7 |
| dev-1 | pragmatic | 0.6 |

**Independent Evaluator:**
```yaml
evaluation:
  winner: pragmatic
  reasoning: |
    Pro made strong organizational arguments but didn't
    address operational complexity sufficiently.
    Con's evidence demands were valid but position
    was purely defensive.
    Pragmatic offered concrete middle path with
    lower risk and clear upgrade path.
  confidence: 0.7
  dissenting_view: "Pro's velocity argument deserves more weight"
```

**Final Verdict:** Modular monolith (pragmatic position)
```

---

## Integration with Other Skills

### With adversarial-committee

Debate IS an adversarial committee in action. The sides are the committee members with opposing propensities.

### With roberts-rules

The moderator can enforce full parliamentary procedure:

```yaml
moderator:
  style: roberts_rules
  enforces:
    - motions_require_second
    - debate_before_vote
    - point_of_order_interrupts
    - two_thirds_for_closure
```

### With rubric

Audience and evaluator can use explicit rubrics:

```yaml
rubric:
  criteria:
    - name: evidence_quality
      weight: 0.3
      levels: [anecdotal, case_study, systematic]
      
    - name: addresses_counterarguments
      weight: 0.25
      levels: [ignores, acknowledges, refutes]
      
    - name: practical_feasibility
      weight: 0.25
      levels: [theoretical, plausible, demonstrated]
      
    - name: risk_assessment
      weight: 0.2
      levels: [ignores, mentions, quantifies]
```

### With speed-of-light

The entire debate can happen in ONE LLM call:

```yaml
# One epoch simulates multiple rounds of debate
speed_of_light:
  characters: 5  # Maya, Frankie, Vic, Tammy, Joe
  rounds: 3
  arguments_per_round: 6
  total_simulated: 18 exchanges
  llm_calls: 1
```

---

## Protocol Symbols

| Symbol | Meaning |
|--------|---------|
| `DEBATE` | Invoke this skill |
| `MOTION` | Propose for vote |
| `SECOND` | Support a motion |
| `REBUTTAL` | Counter an argument |
| `VERDICT` | Final decision |
| `ADVERSARIAL-COMMITTEE` | The underlying pattern |

---

## Dovetails With

- **[../adversarial-committee/](../adversarial-committee/)** — The committee pattern
- **[../roberts-rules/](../roberts-rules/)** — Parliamentary procedure
- **[../rubric/](../rubric/)** — Scoring criteria
- **[../evaluator/](../evaluator/)** — Independent assessment
- **[../card/](../card/)** — Data flow ensembles
- **[../speed-of-light/](../speed-of-light/)** — Many agents, one call
- **[../soul-chat/](../soul-chat/)** — Character dialogue
- **[../persona/](../persona/)** — Advocate personalities
- **[../../designs/mike-gallaher-ideas.md](../../designs/mike-gallaher-ideas.md)** — Original methodology

---

*"The map is not the territory. The story is not the reality. But the ensemble of stories, cross-examined, might just be useful."*
