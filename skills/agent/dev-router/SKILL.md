---
name: dev-router
description: Developer agent skill router - routes to 31 dev skills by category and signal keywords, manages 5 sub-agents.
category: routing
---

# Developer Skill Router

> "Right skill, right sub-agent, right time."

# Common Skill Combinations

Typical task types and the skill combinations that work well for them.

## Task Type → Skill Combination Mapping

### 1. New Game Feature (e.g., Player Movement)

**Skills:**

- dev-research-gdd-reading (MANDATORY)
- dev-research-codebase-exploration (MANDATORY)
- dev-r3f-r3f-fundamentals

**Why:** Research ensures patterns are followed.

---

### 2. Multiplayer Feature (e.g., Room Creation)

**Skills:**

- dev-research-gdd-reading (MANDATORY)
- dev-research-codebase-exploration (MANDATORY)
- dev-multiplayer-server-authoritative
- dev-multiplayer-colyseus-server
- dev-multiplayer-colyseus-state
- dev-multiplayer-colyseus-client

**Why:** Full server-authoritative stack from architecture to client. Validation ensures server builds correctly.

---

### 3. Client-Side Prediction (e.g., Movement Prediction)

**Skills:**

- dev-research-gdd-reading (MANDATORY)
- dev-research-codebase-exploration (MANDATORY )
- dev-multiplayer-server-authoritative
- dev-multiplayer-prediction-basics
- dev-multiplayer-prediction-movement
- dev-typescript-advanced

**Why:** Prediction builds on server-authoritative foundation. Advanced TypeScript for generic prediction types.

---

### 4. Asset Loading (e.g., Character Models)

**Skills:**

- dev-research-gdd-reading (MANDATORY)
- dev-research-codebase-exploration (MANDATORY)
- dev-assets-vite-asset-loading
- dev-assets-model-loading
- dev-r3f-r3f-fundamentals

**Why:** Vite patterns + specific model loading. R3F fundamentals for scene integration.

---

### 5. Performance Optimization (e.g., FPS Drop)

**Skills:**

- dev-research-codebase-exploration (MANDATORY)
- dev-performance-performance-basics
- dev-performance-instancing (if many objects)
- dev-performance-lod-systems (if complex models)
- dev-patterns-object-pooling (if transient objects)

**Why:** Start with basics, add specific techniques based on problem. Object pooling for per-frame creation.

---

### 6. UI/HUD Implementation

**Skills:**

- dev-research-gdd-reading (MANDATORY)
- dev-research-codebase-exploration (MANDATORY)
- dev-typescript-basics
- dev-patterns-ui-animations

**Why:** TypeScript for component props. UI animations for polish. E2E testing for UI validation.

---

### 7. Shooting Mechanics

**Skills:**

- dev-research-gdd-reading (MANDATORY)
- dev-research-codebase-exploration (MANDATORY)
- dev-multiplayer-server-authoritative
- dev-multiplayer-prediction-shooting
- dev-r3f-r3f-fundamentals
- dev-patterns-object-pooling

**Why:** Server-authoritative hit detection. Shooting prediction. Object pooling for projectiles.

---

### 8. Territory/Coverage System

**Skills:**

- dev-research-gdd-reading (MANDATORY)
- dev-research-codebase-exploration (MANDATORY)
- dev-patterns-coverage-tracking
- dev-typescript-advanced
- dev-r3f-r3f-fundamentals

**Why:** Coverage tracking pattern. Advanced TypeScript for grid state types. R3F for visualization.

---

### 9. Mobile Touch Controls

**Skills:**

- dev-research-gdd-reading (MANDATORY)
- dev-research-codebase-exploration (MANDATORY)
- dev-performance-mobile-optimization
- dev-patterns-mobile-haptics
- dev-typescript-basics

**Why:** Mobile optimization patterns. Haptics for feedback. E2E testing with touch events.

---

### 10. Bug Fix (any category)

**Skills:**

- dev-research-pattern-finding
- [Category-specific skill based on bug]

**Why:** Find existing patterns first. Load only the relevant domain skill. Validation to ensure fix works.

---

## Skill Load Order

For complex tasks, load skills in this order:

1. **Research first:** dev-research-codebase-exploration (always)
2. **Foundations:** r3f-fundamentals, typescript-basics, server-authoritative
3. **Domain specific:** physics, materials, prediction, etc.
4. **Patterns:** object-pooling, ui-animations
5. **Validation last:** feedback-loops, browser-testing

## Combining with Sub-Agents

```
Task({ subagent_type: "developer-code-research", ... })
  ↓
[Research completes, provides findings]
  ↓
Load domain skills based on findings
  ↓
Task({ subagent_type: "code-implementation", ... })
  ↓
[Implementation completes]
  ↓
Task({ subagent_type: "developer-validation", ... })
  ↓
[Validation passes]
  ↓
Task({ subagent_type: "commit-agent", ... })
```

## Anti-Patterns to Avoid

| Anti-Pattern                                   | Why           | Correct Approach                  |
| ---------------------------------------------- | ------------- | --------------------------------- |
| Loading all R3F skills at once                 | Context bloat | Load only relevant skills         |
| Loading validation before research             | Wasted cycles | Research → Implement → Validate   |
| Skipping research for "simple" tasks           | Miss patterns | Always research first             |
| Loading both basics and advanced TypeScript    | Redundant     | Advanced includes basics concepts |
| Loading multiplayer for single-player features | Unused code   | Only load when needed             |
