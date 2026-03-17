---
name: brain-mode
description: Meta-Cognitive Orchestrator. Supersedes Loki by adding Active Inference, dynamic cost-routing, and episodic memory to the SDLC loop. Uses "System 2" thinking to plan, route, and optimize work.
triggers: [brain activate, supermode, solve everything, brain mode, meta orchestrate]
context_cost: high
---

# Brain Mode — Meta-Cognitive Orchestrator

> **Supersedes**: `loki-mode`
> **Concept**: Applies Active Inference (Free Energy Principle) to Software Engineering.
> **Goal**: Minimize "Surprise" (Bugs, Delays, Costs) by continuously updating internal models and routing work intelligently.

---

## 1. The Cognitive Loop (System 2)

Brain Mode runs a continuous "OODA Loop" on top of the standard SDLC:

1.  **Observe (Sensation)**: Read `PROJECT_STATE`, `AUDIT_LOG`, and recent `terminal` outputs.
2.  **Orient (Perception)**: Update `internal_model` (Belief State). "Are we on track? Is this task hard?"
3.  **Decide (Policy Selection)**: Choose the best "Skill" or "Mode" to minimize expected free energy (cost/risk).
    - *Routine Task?* -> Delegate to `Local LLM` (via `cost-benefit-router`).
    - *Complex Task?* -> Delegate to `Remote SOTA` (via `cost-benefit-router`).
    - *Massive Project?* -> Invoke `loki-mode` (System 1 execution).
4.  **Act (Active Inference)**: Execute the chosen policy.

---

## 2. Dynamic Routing (The "Budget" Layer)

**Crucial Upgrade**: Brain Mode does not blindly fire expensive calls. It consults `cost-benefit-router` first.

```mermaid
graph TD
    A[Task Request] --> B{Brain Mode Analysis}
    B -->|High Complexity / Novel| C[Remote SOTA (Claude 3.5/GPT-4o)]
    B -->|Low Complexity / Routine| D[Local LLM (Llama 3/Mistral)]
    B -->|Massive Scope| E[Loki Swarm Orchestration]
```

---

## 3. Execution Protocol

### Phase B01: Context Loading (Working Memory)
1.  **Load Episodic Memory**: Query `episodic-consolidation` -> "Have we solved a similar problem?"
2.  **Load Semantic Memory**: Read `knowledge-map` -> "What concepts represent this domain?"
3.  **Synthesize**: Create a `CURRENT_CONTEXT.md` (Short-term working memory).

### Phase B02: Strategy Selection
1.  Call `brain/cost-benefit-router.skill.md` with inputs:
    - Task Description
    - User Constraints (Time vs Budget)
2.  **Decision**:
    - **Strategy A (Quick Fix)**: Direct tool use (coding/edit).
    - **Strategy B (Deep Think)**: `sequential-thinking` -> `plan` -> `execute`.
    - **Strategy C (Full Swarm)**: Initialize `loki-mode` (S01-S10).

### Phase B03: Execution & Monitoring (The "Watcher")
If delegating to `loki-mode` or `sub-agents`, Brain Mode remains active as a **Supervisor**:
- **Monitor**: Watch `PREDICTION_ERROR` logs.
- **Intervene**: If `loki` gets stuck (looping), Brain Mode pauses execution and:
  - Rewrites the prompt (Neuro-plasticity).
  - Injects new knowledge (RAG).
  - Switches models (Dynamic Routing).

### Phase B04: Consolidation (Learning)
After task completion:
1.  **Calculate Prediction Error**: "Did it take longer than expected?"
2.  **Update Priors**: "Local LLM was too weak for React Hooks" -> Update Router weights.
3.  **Save Episode**: Write to `brain/memory/episodic_log`.

---

## Command Interface

```bash
# Full Autonomy (Best for new projects)
/brain-mode "Build a CRM system"

# Specific Optimization (Best for existing projects)
/brain-mode "Refactor the auth layer using local models only"

# Debugging (When Loki fails)
/brain-mode --fix-last-error
```

## Integration with Loki

Brain Mode treats `loki-mode` as a **Sub-Routine**.
- `loki` is the "Body" (Arms/Legs) doing the heavy lifting.
- `brain` is the "Mind" deciding *where* to move the body.

If `loki` is running:
- `brain-mode` watches `agents/memory/PROJECT_STATE.md`.
- It performs "Meta-Checks" at every checkpoint (S01, S02...).
