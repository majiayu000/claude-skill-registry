---
name: cognitive-architectures
description: Patterns from SOAR, ACT-R, and LIDA for advanced agent cognitive cycles
triggers: [cognitive, architecture, soar, act-r, lida, reasoning cycle]
tags: [brain, architecture, theory]
---

# Cognitive Architectures for Agents

## Description
This skill provides implementation patterns derived from classic and modern Cognitive Architectures (SOAR, ACT-R, LIDA) to structure agent reasoning, memory, and decision-making processes beyond simple prompt engineering.

## 1. SOAR (State, Operator, And Result)

**Core Idea:** Intelligence is the ability to solve problems by navigating a "Problem Space" using "Operators."

### Implementation Pattern: Proposal-Evaluation Cycle
Instead of a single "think" step, break agent reasoning into distinct phases:
1.  **Elaboration**: Calculate all immediate inferences from current state.
2.  **Proposal**: Generate candidate operators (actions/thoughts) for the current state.
3.  **Evaluation**: Score candidate operators using preferences (heuristics).
4.  **Selection**: Pick the best operator.
5.  **Application**: Execute it to change the state.

**Code Metaphor:**
```python
def cognitive_cycle(state):
    # 1. Elaboration
    state = enrich_context(state)
    
    # 2. Proposal
    options = generate_candidates(state)
    
    # 3. Evaluation
    scored_options = evaluate_candidates(options, goal=state.goal)
    
    # 4. Selection
    best_op = select_winner(scored_options)
    
    # 5. Application
    new_state = apply_operator(state, best_op)
    return new_state
```

## 2. ACT-R (Adaptive Control of Thought-Rational)

**Core Idea:** Human cognition relies on two distinct memory types: **Declarative** (Facts/Chunks) and **Procedural** (Production Rules).

### Implementation Pattern: Activation-Based Retrieval
Do not retrieve *all* context. Retrieve context based on **Activation** (Recency + Frequency + Relevance).
- **Base Level Activation**: How often/recently was this chunk used?
- **Associative Activation**: How related is this chunk to the current focus?

**Code Metaphor:**
```python
def retrieve_memory(query, memory_store):
    for chunk in memory_store:
        chunk.activation = log(chunk.frequency) - log(time_since_last_use) + similarity(query, chunk)
    
    top_chunk = max(memory_store, key=lambda c: c.activation)
    if top_chunk.activation > THRESHOLD:
        return top_chunk
    return None # Retrieval failure
```

## 3. LIDA (Learning Intelligent Distribution Agent)

**Core Idea:** The **Cognitive Cycle** of Perception -> Understanding -> Consciousness -> Action Selection. Implements **Global Workspace Theory**.

### Implementation Pattern: The "Spotlight" of Consciousness
- **Preconscious Buffers**: Parallel agents process sensory data (e.g., visual, auditory, textual).
- **Coalitions**: Agents form "coalitions" of related information.
- **Global Workspace**: Coalitions compete for entry. The winner is "broadcast" to all other agents, recruiting resources to handle the current situation.

## References
- **Laird, J.** (2012). *The Soar Cognitive Architecture*.
- **Anderson, J. R.** (2007). *How Can the Human Mind Occur in the Physical Universe?* (ACT-R).
- **Franklin, S.** (2006). *The LIDA Architecture*.
