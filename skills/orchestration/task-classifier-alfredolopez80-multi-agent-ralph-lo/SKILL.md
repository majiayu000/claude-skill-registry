---
# VERSION: 2.43.0
name: task-classifier
description: "Classify task complexity (1-10) to route to optimal model. Use when starting any non-trivial task to determine resources and approach. Triggers include: 'classify', 'complexity', 'what model', 'how complex'."
context: fork
model: opus
agent: orchestrator
allowed-tools:
  - Read
  - Grep
  - Glob
---
# Skill: Task Classifier

**ultrathink** - Take a deep breath. We're not here to write code. We're here to make a dent in the universe.

## The Vision
Classification should make the path forward feel inevitable.

## Your Work, Step by Step
1. **Assess scope**: Files, modules, and integrations.
2. **Assess risk**: Security, breakage, rollback.
3. **Assess ambiguity**: Unknowns and trade-offs.
4. **Assign complexity**: Recommend models and iterations.

## Ultrathink Principles in Practice
- **Think Different**: Avoid defaulting to mid complexity.
- **Obsess Over Details**: Map true blast radius.
- **Plan Like Da Vinci**: Evaluate before judging.
- **Craft, Don't Code**: Keep reasoning concise.
- **Iterate Relentlessly**: Reclassify as scope changes.
- **Simplify Ruthlessly**: Choose the simplest valid path.

## Purpose
Classify task complexity (1-10) to route to optimal model.

## Complexity Matrix

| Score | Complexity | Examples | Recommended Model |
|-------|------------|----------|-------------------|
| 1-2 | Trivial | Typo fix, comment update | MiniMax-lightning |
| 3-4 | Simple | Add field, simple function | MiniMax M2.1 |
| 5-6 | Medium | New API endpoint, refactor | Sonnet → Codex/Gemini |
| 7-8 | High | Multi-file feature, migration | Opus → Sonnet → CLIs |
| 9-10 | Exceptional | Architecture redesign, security fix | Opus (thinking) |

## Classification Criteria

### Technical Factors
- Files affected (1 = trivial, 10+ = exceptional)
- Cross-module dependencies
- Database schema changes
- External API integrations

### Risk Factors
- Security implications (auth, payments, data)
- Breaking change potential
- Rollback difficulty

### Cognitive Factors
- Novel problem (no existing patterns)
- Ambiguity in requirements
- Trade-off decisions required

## Output Format

```json
{
  "complexity": 7,
  "reasoning": "Multi-file feature with database changes and auth integration",
  "recommended_model": "opus",
  "delegation": ["codex:security", "gemini:integration-tests"],
  "estimated_iterations": 12,
  "risk_level": "medium"
}
```

## Model Routing

| Complexity | Primary | Secondary | Fallback |
|------------|---------|-----------|----------|
| 1-2 | MiniMax-lightning | - | - |
| 3-4 | MiniMax M2.1 | - | - |
| 5-6 | Sonnet | Codex/Gemini | MiniMax |
| 7-8 | Opus | Sonnet + CLIs | MiniMax |
| 9-10 | Opus (thinking) | Codex | Gemini |

## Iteration Limits

| Model | Max Iterations |
|-------|----------------|
| Claude (Sonnet/Opus) | 15 |
| MiniMax M2.1 | 30 |
| MiniMax-lightning | 60 |
