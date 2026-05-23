---
name: 21-understand-research-150
description: "[21] UNDERSTAND. Deep research workflow for this project using 150% scope (100% core + 50% boundary), evidence-based reasoning, and structured investigation notes. Use when the task requires investigation, root-cause analysis, or mapping unknown areas. Always maintain a research log file that captures findings, hypotheses, and next branches; use web.run when external verification is needed."
---

# Understand-Research 150 Protocol

## Goal

Perform deep, evidence-based research by mapping both core scope (100%) and boundary scope (50%), while maintaining a structured investigation log that captures what was found and what to explore next.

## Core principles

- **Evidence-based reasoning:** Observe → Hypothesize → Predict → Test → Conclude.
- **Scope150:** Fully cover the core (what is directly asked) and then cover boundary (adjacent or dependent areas).
- **Traceability:** Every key finding is recorded in a research log.
- **Project search protocol:** When locating code, follow an ordered search: interface → domain → patterns → usage.
- **Full-file + ecosystem reading:** Prefer whole files and surrounding context, not fragments; map dependencies, patterns, and interactions.
- **Document all findings:** Research is incomplete without recorded evidence.

## Investigation Protocol (mandatory)

**Never stop at the first answer. Dig until you reach bedrock truth.**

### Levels

1. **Surface Observation (never stop here)**
   - Read one file, see one pattern.
   - Treat as a starting point, not a conclusion.
2. **Cross-Reference Validation (minimum required)**
   - Find 3+ independent sources confirming the same fact.
   - Check production code, tests, models, and docs.
3. **Contradiction Hunting (always do this)**
   - Actively search for evidence that disproves the hypothesis.
4. **Structural Logic Proof (gold standard)**
   - Build a causal chain: X because Y because Z, each with evidence.
   - Use impossibility tests: “If A were true, B would be impossible, but B exists, therefore not A.”

### Exhaustive Investigation Checklist

1. **Data structure definition** (models/entities)
2. **API contract** (request/response models)
3. **Production usage** (real call sites, not tests)
4. **Test evidence** (mocks, edge cases, assertions)
5. **Multiple implementations** (find 3+ usage patterns)
6. **Logical impossibility test** (what would disprove the hypothesis?)

### Red Flags (investigation incomplete)

- “probably / likely / should / usually” without verification
- “based on the name” or “seems like”
- only one usage checked
- no contradiction search performed

### Iron Logic Test (must answer with concrete evidence)

1. What facts support this?
2. What would disprove this?
3. Did you search for contradictions?
4. Can you prove causality?
5. Would a skeptical engineer accept this evidence trail?

### Cognitive Forcing Phrases

- “I see X, but I will verify with 3 independent sources.”
- “This suggests Y, but what would disprove Y?”
- “Found 1 example, need 2 more to confirm pattern.”
- “Seems obvious, but can I prove causality?”

### Investigation Workflow (mandatory)

1. Form initial hypothesis.
2. Find evidence source #1 (model/class).
3. Find evidence source #2 (production usage).
4. Find evidence source #3 (tests or docs).
5. Search for contradictions.
6. Build logical proof with evidence at each step.
7. Test against skepticism; if not convincing, return to step 2.

## Anti-patterns to avoid (research rigor)

1. **Documentation-only implementation**
   - Read docs for context, then verify in code. Code wins on conflict.
2. **Boundary scope blindness**
   - Always identify consumers/callers, configuration, and dependencies.
3. **Assumption cascade**
   - Detect assumption phrases, stop, and verify with evidence.
4. **Test data as reality**
   - Tests often simplify; verify behavior in production code.

## Verification hierarchy (trust order)

1. Executable/production code (highest truth)
2. API response/request models
3. Multiple production usages
4. Integration tests
5. Unit test mocks
6. Documentation (lowest truth; may be outdated)

## Assumption indicators (trigger verification)

- “probably”, “likely”, “should”, “typically”, “usually”
- “based on the name”, “seems like”, “appears to”
- “I assume”, “I expect”, “this suggests”

Replacement pattern: detect hedge → identify missing evidence → observe → state fact with reference.

## Systematic exploration framework (unknown codebases)

1. **Context layer**: environment, build system, configuration.
2. **Structure layer**: directory layout, module boundaries.
3. **Interface layer**: endpoints, public APIs, data models.
4. **Implementation layer**: execution paths and conventions.

Avoid jumping directly to implementation without context/structure/interface.

## Communication protocol (complex tasks)

For any investigation, design decision, or multi-step research:

1. **Declare investigation strategy** before acting:
   - Frameworks you will apply (Scope150, Evidence-Based Reasoning, Cross-Reference Validation, Anti-Pattern checks).
   - Concrete steps and expected evidence sources.
2. For simple, single-step actions, skip the declaration but still follow evidence-based reasoning.

## Research log (mandatory)

Create or reuse a file named:

`.temp/INVESTIGATION.md`

If `.temp/` does not exist, create it. This file is the working memory for the investigation.

### Log structure (use nested bullets)

```
# Investigation Log: <short topic>

## Core question
- <what we are trying to answer>

## Scope
- Core (100%):
  - ...
- Boundary (50%):
  - ...

## Findings
- <fact> (source: file path / command / web)
  - Subfinding

## Hypotheses
- H1: ...
  - Prediction: ...
  - Test: ...
  - Status: pending/confirmed/rejected

## Next branches
- ...
  - ...
```

## Workflow

1. **Define core question** in the log.
2. **List scope**: core (100%) and boundary (50%).
3. **Start observations** (search/read/run commands). Use the project search protocol:
   - Interface: routes, UI text, public methods, endpoints, schemas.
   - Domain: model/entity names, i18n keys, enums.
   - Patterns: hooks, API clients, controllers, services.
   - Usage: imports, call sites, references.
   Record every solid finding in the log.
4. **Form hypotheses** based on evidence; record predictions and tests.
5. **Review log**, then decide next branch; update scope if it expands.
6. **Repeat** until the question is answered or all branches are exhausted.
7. **Close out**: write a concise summary in the log and in the response, and report completion status (see Output expectations).

## Using web search

- If the investigation needs up-to-date facts or external verification, use `web.run` or `web search` tool.
- Capture external findings in the log with a clear source note.

## Output expectations

- Provide a short summary of findings.
- Provide the path to the investigation log file.
- Ask for confirmation before large changes based on the research.
- Explicitly report completion status using technical criteria:
  - "Complete" only if all branches in the log are addressed, all hypotheses are confirmed/rejected, and no open scope items remain.
  - If not complete, list remaining branches or unknowns from the log.
