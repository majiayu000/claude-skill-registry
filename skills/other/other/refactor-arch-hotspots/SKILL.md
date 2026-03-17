---
name: refactor-arch-hotspots
description: "[Code Quality] Identifies architectural hotspots: high-churn files, coupling issues, layer violations, and dependency tangles. Use to find systemic issues that cause repeated bugs or slow development."
---

# Refactor: Architecture Hotspots

Find structural issues that create ongoing maintenance burden.

## Hotspot Categories

### 1. High-Churn Files
Files changed frequently indicate poor abstraction boundaries.

### 2. Coupling Analysis
- Afferent Coupling (Ca): Who depends on this?
- Efferent Coupling (Ce): What does this depend on?
- Instability (I): Ce / (Ca + Ce)

### 3. Layer Violations
- UI accessing database directly
- Business logic in controllers
- Circular module dependencies

### 4. Dependency Tangles
- Import cycles
- Bidirectional dependencies
- God modules everything imports

## Prioritization

Focus on hotspots that are:
1. High churn AND high complexity
2. Frequently causing bugs
3. Blocking feature development