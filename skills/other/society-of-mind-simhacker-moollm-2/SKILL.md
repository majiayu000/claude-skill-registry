---
name: society-of-mind
description: "Intelligence emerges from many simple agents (Minsky)"
license: MIT
tier: 0
allowed-tools: [read_file, list_dir]
protocol: SOCIETY-OF-MIND
related: [moollm, k-lines, adversarial-committee, multi-presence, speed-of-light, simulator-effect, character, persona, mind-mirror, constructionism, debate, soul-chat]
tags: [moollm, meta, philosophy, minsky, emergence, agents, k-lines]
---

# Society of Mind Skill

> *Simulate the mind as a society of agents.*

## Overview

This skill implements Minsky's Society of Mind theory within MOOLLM. Intelligence emerges from the interaction of many simple agents -- not from a single unified controller.

## Core Mechanics

### 1. Agent Definition

An agent is a minimal process with:

```yaml
agent:
  id: agent_identifier
  function: what it does
  activates_when: [conditions...]
  suppresses: [other agents...]
  amplifies: [other agents...]
  connects_to: [related agents...]
  knows: scope of awareness (usually minimal)
```

Agents are deliberately simple. They do one thing. They know nothing about the whole.

### 2. Agency Formation

Agents cluster into agencies -- groups that produce emergent behavior:

```yaml
agency:
  id: agency_identifier
  purpose: what emerges
  agents: [list of agent ids]
  coordination: how they interact
  emergence: what behavior appears
```

### 3. K-Line Activation

K-lines connect to agents. Activating a K-line activates its connected agents:

```yaml
k_line:
  symbol: "grandmother"
  activates:
    - face_recognition.elderly_female
    - olfactory.cookies
    - emotion.love
    - narrative.family_stories
    - kinship.maternal_line
```

### 4. Competition and Suppression

Agents compete for control. Active agents suppress competing agents:

```yaml
competition:
  scenario: "Should I eat or socialize?"
  
  hunger_agency:
    strength: 7
    votes_for: [go_to_kitchen, find_food]
    suppresses: [conversation, stay_here]
    
  social_agency:
    strength: 8
    votes_for: [continue_talking, stay_here]
    suppresses: [leave, interrupt]
    
  winner: social_agency (strength 8 > 7)
  behavior: continue conversation
  consequence: hunger grows stronger
```

### 5. B-Brain Observation

Higher-level agents watch lower-level agents:

```yaml
b_brain:
  observes: [a_brain_agents...]
  reports: current state
  enables: self_reflection
  
  example:
    a_brain: "I am getting angry"
    b_brain: "I notice that I am getting angry"
    c_brain: "I notice that I am noticing that I am getting angry"
```

## MOOLLM Implementation

### Skills as Agents

```yaml
# Each skill directory is an agent
skills/bartender/:
  function: serve drinks, hear secrets
  activates_when: in pub, customer speaks
  connects_to: [economy, soul-chat, persona]
  
skills/evaluator/:
  function: judge outputs against rubrics
  activates_when: rubric invoked
  suppresses: uncritical acceptance
```

### Characters as Societies

```yaml
character:
  name: Palm
  id: palm
  
  inner_society:
    agents:
      - {id: creative, strength: 9}
      - {id: social, strength: 8}
      - {id: philosophical, strength: 8}
      - {id: playful, strength: 9}
      - {id: melancholy, strength: 6}
      
    default_active: [creative, playful]
    default_suppressed: [melancholy]
    
  external_presentation: emergent from agent competition
```

### Committees as Deliberating Societies

```yaml
# adversarial-committee IS a society deliberating
committee_session:
  agents:
    maya:
      propensity: paranoid_realism
      function: surface hidden agendas
      
    frankie:
      propensity: idealism  
      function: surface missed opportunities
      
    vic:
      propensity: evidence_focus
      function: demand proof
      
  protocol: roberts_rules
  emergence: robust decision surviving cross-examination
```

### Rooms as Agent Configurations

```yaml
# Entering a room activates agents
pub_stage:
  activates:
    - performance_framing
    - bartender_service
    - audience_awareness
    - tribute_ethics
    
  suppresses:
    - private_mode
    - unfiltered_output
```

## Protocols

### Agent Instantiation Protocol

When creating an agent:

1. **Minimal function** -- one clear purpose
2. **Activation conditions** -- when it fires
3. **Connections** -- what it amplifies/suppresses
4. **Scope awareness** -- what it knows (usually little)

### Agency Assembly Protocol

When assembling an agency:

1. **Identify component agents**
2. **Define coordination mechanism**
3. **Specify emergent behavior**
4. **Test for unintended suppression**

### Competition Resolution Protocol

When agents conflict:

1. **Measure strengths** (from context, history, urgency)
2. **Winner activates**, loser suppresses
3. **Suppressed agent remains**, grows stronger over time
4. **Eventually suppressed agent may win** (need shift)

### B-Brain Integration Protocol

For self-reflective characters:

1. **A-brain:** Direct agents (hunger, anger, creativity)
2. **B-brain:** Observation agents (I notice I am...)
3. **C-brain:** Meta-observation (I notice I notice...)
4. **Integration:** B-brain can influence A-brain

## Examples

### Example 1: Character Inner Conflict

```yaml
session:
  character: Palm
  situation: Should he publish his essay?
  
  agent_debate:
    creative:
      position: "The work is good. Share it."
      strength: 9
      
    fear:
      position: "They might judge harshly."
      strength: 7
      
    social:
      position: "Don gives good feedback."
      strength: 8
      
    perfectionist:
      position: "One more revision."
      strength: 6
      
  resolution:
    creative + social (17) > fear + perfectionist (13)
    action: Palm shares the essay with Don
```

### Example 2: Multi-Agent LLM Call

```yaml
prompt: |
  You are simulating Palm's inner society.
  
  SITUATION: Palm finds a philosophical error in his essay.
  
  CREATIVE AGENT: [speaks]
  PERFECTIONIST AGENT: [speaks]
  PHILOSOPHICAL AGENT: [speaks]
  PLAYFUL AGENT: [speaks]
  
  Show their debate. Palm makes a decision.
  
output_format:
  - Each agent speaks in character
  - Conflicts are explicit
  - Resolution emerges from debate
  - Final action stated
```

### Example 3: Sims-Style Autonomy

```yaml
sim:
  name: Bob
  
  current_motives:
    hunger: 7/10
    social: 4/10
    fun: 6/10
    energy: 5/10
    
  available_actions:
    - eat_food: {hunger: +3, time: -1}
    - call_friend: {social: +2, fun: +1, time: -1}
    - watch_tv: {fun: +2, energy: -1, time: -2}
    - sleep: {energy: +5, time: -8}
    
  autonomy_algorithm:
    for each action:
      score = sum(motive_weight * action_effect)
    select: highest scoring action
    
  result:
    eat_food: 7 * 3 = 21
    call_friend: 4 * 2 + 6 * 1 = 14
    watch_tv: 6 * 2 = 12
    sleep: 5 * 5 = 25
    
    winner: sleep (highest urgency * effect)
```

## Anti-Patterns

### Anti-Pattern 1: Unified Controller

```yaml
# WRONG: Single agent controls all
character:
  name: Palm
  controller: central_palm_agent
  behavior: whatever controller decides
  
# RIGHT: Behavior emerges from competition
character:
  name: Palm
  agents: [creative, social, philosophical, playful, melancholy]
  behavior: emergent from agent competition
```

### Anti-Pattern 2: Omniscient Agents

```yaml
# WRONG: Agent knows everything
hunger_agent:
  knows: all character state, world state, goals, ethics
  
# RIGHT: Agent knows only its domain
hunger_agent:
  knows: stomach emptiness, food location
  does_not_know: social implications of eating now
```

### Anti-Pattern 3: Static Hierarchy

```yaml
# WRONG: Fixed dominance
agents:
  primary: rational_agent
  secondary: emotional_agent
  # rational always wins
  
# RIGHT: Dynamic competition
agents:
  - rational: {strength: varies_by_context}
  - emotional: {strength: varies_by_situation}
  # winner depends on circumstances
```

## Integration Points

| Skill | Integration |
|-------|-------------|
| [k-lines/](../k-lines/) | Activation mechanism for agents |
| [adversarial-committee/](../adversarial-committee/) | Deliberating society |
| [multi-presence/](../multi-presence/) | Multiple agents in scene |
| [speed-of-light/](../speed-of-light/) | Many agents per call |
| [needs/](../needs/) | Motive agents competing |
| [advertisement/](../advertisement/) | Action scoring for agents |
| [mind-mirror/](../mind-mirror/) | B-brain observation |
| [character/](../character/) | Characters as societies |
| [persona/](../persona/) | Persona as agent overlay |
| [simulator-effect/](../simulator-effect/) | Emergence from sparse agents |

## References

### Primary Sources

- Minsky, M. (1985). *The Society of Mind*. Simon & Schuster. ISBN 0-671-60740-5.
- Minsky, M. (1980). "K-lines: A Theory of Memory." *Cognitive Science* 4(2), 117-133. [PDF](https://courses.media.mit.edu/2004spring/mas966/Minsky%201980%20K-lines.pdf)
- Minsky, M. (2006). *The Emotion Machine*. Simon & Schuster. ISBN 0-7432-7663-9.

### Related Theory

- Minsky, M. & Papert, S. (1969/1988). *Perceptrons*. MIT Press.
- Papert, S. (1980). *Mindstorms: Children, Computers, and Powerful Ideas*. Basic Books.
- Drescher, G. (1991). *Made-Up Minds: A Constructivist Approach to AI*. MIT Press.

### Game Design

- Wright, W. (1996). "Stupid Fun: Thoughts on Game Design." Stanford HCI Seminar.
- Wright, W. (2003). "Dynamics of Game Design." GDC Keynote.

### LLM Applications

- Park, J.S. et al. (2023). "Generative Agents: Interactive Simulacra of Human Behavior." *UIST*. [arXiv:2304.03442](https://arxiv.org/abs/2304.03442)

### MOOLLM Documentation

- [k-lines/README.md](../k-lines/README.md) -- Full K-lines theory and MOOLLM implementation
- [adversarial-committee/README.md](../adversarial-committee/README.md) -- Committee as deliberating society
- [needs/README.md](../needs/README.md) -- Sims motive system
- [simulator-effect/README.md](../simulator-effect/README.md) -- Implication over simulation
- [EVAL-INCARNATE-FRAMEWORK.md](../../designs/eval/EVAL-INCARNATE-FRAMEWORK.md#appendix-a-intellectual-lineage) -- K-lines section
- [sims-astrology.md](../../designs/sims/sims-astrology.md) -- Astrillogical Effect case study
