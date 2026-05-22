---
name: architecture-introspector
description: |
  USE WHEN: analyzing existing architectures, evaluating architectural decisions, identifying technical debt, planning refactoring, assessing whether patterns are justified, onboarding to complex codebases, reviewing PRs with architectural changes.
  DO NOT USE WHEN: simple code questions, bug fixes, feature implementation, or tasks not requiring architectural analysis.
  For complex architectural analysis, trigger deep thinking with "think harder" or "ultrathink" to enable thorough first-principles reasoning.
license: Complete terms in LICENSE.txt
---

# Architecture Introspector

Systematically analyze software architectures using first principles thinking, applying SpaceX's 5-step engineering methodology combined with software modularity principles to identify unnecessary complexity, validate architectural decisions, and recommend improvements.

## Purpose

This skill provides a rigorous, principle-based framework for evaluating software architectures. It challenges inherited assumptions, identifies unjustified complexity, and applies the "delete first, optimize later" philosophy to architecture. The goal is to achieve simple, justified architectures where every component earns its existence through actual need rather than hypothetical future requirements.

## When to Use This Skill

Use this skill when:

- **Analyzing existing architectures** - Understanding whether current architectural patterns are justified
- **Evaluating architectural decisions** - Questioning whether a proposed abstraction/layer/pattern is necessary
- **Identifying technical debt** - Finding components that add complexity without proportional value
- **Planning refactoring efforts** - Determining what to delete, simplify, or consolidate
- **Onboarding to codebases** - Understanding architectural rationale and identifying areas for improvement
- **Code review of architectural changes** - Ensuring new abstractions meet the 2+ consumer threshold
- **Modernization efforts** - Deciding what to keep, kill, or consolidate during rewrites

## Core Philosophy

### SpaceX's 5-Step Engineering Methodology

1. **Question Every Requirement** - Trace decisions to their origins, challenge assumptions
2. **Delete the Part or Process** - Remove first, optimize never (if it shouldn't exist)
3. **Simplify and Optimize** - Only after deletion is complete
4. **Accelerate Cycle Time** - Speed up validated, simplified processes
5. **Automate** - Last step only, after deletion and simplification

### Software Modularity Principle

**"Modularity without reuse is bureaucracy"**

Extract and modularize based on actual needs (2+ consumers for services/helpers, 3+ for utilities), not hypothetical futures. Premature abstraction creates overhead without benefit.

## How to Use This Skill

### Step 1: Load the Framework

Read the comprehensive framework from `references/first_principles_framework.md`:

```
Read references/first_principles_framework.md
```

This document contains:
- Detailed explanation of all 5 SpaceX principles applied to architecture
- The modularity principle and 2-3 rule
- Anti-patterns to identify
- Decision frameworks
- Output format templates

### Step 2: Define the Introspection Scope

Clarify what is being analyzed:

- **System-wide architecture** - Entire application's structure
- **Subsystem/module** - Specific domain or layer
- **Specific pattern** - Particular architectural decision (e.g., "Should we extract this service?")
- **Feature implementation** - How a feature is architecturally structured

Ask the user:
- What architectural area should be analyzed?
- What specific concerns or questions exist?
- Are there performance issues, maintenance pain points, or complexity complaints?
- Is this exploratory or focused on a specific decision?

### Step 3: Apply the 6-Phase Introspection Process

Follow the process defined in `references/first_principles_framework.md`:

#### Phase 1: Map Current State
- Inventory all components, layers, and abstractions
- Count consumers for each abstraction (critical for deletion phase)
- Trace data/control flow
- Document original decisions and their rationale (if discoverable)

#### Phase 2: Question Requirements
- For each architectural element, ask "Who required this and why?"
- Validate assumptions against current reality
- Identify cargo-culted patterns (e.g., "We use microservices because Netflix does")
- Separate hard constraints (business/technical necessities) from soft constraints (preferences)

#### Phase 3: Delete
**Most important phase - if not occasionally adding things back, not deleting enough**

Identify deletion candidates:
- Abstractions with <2 consumers → Inline them
- Layers adding no value → Remove them
- Duplicated logic → Consolidate
- Unused features → Delete
- Premature generalizations → Simplify to specific need

Apply the modularity principle rigorously:
- Services/helpers with 1 consumer → Move logic into that consumer
- Utilities used <3 times → Inline
- Frameworks for single use case → Replace with simple solution

#### Phase 4: Simplify
**Only for components that survived deletion**

- Reduce cognitive complexity
- Unify similar patterns into a single approach
- Improve naming and contracts
- Lower the learning curve

#### Phase 5: Accelerate
- Identify architectural bottlenecks (deployment dependencies, approval gates)
- Reduce coupling to enable parallel development
- Shorten feedback loops
- Enable incremental deployment

#### Phase 6: Automate
**Only after deletion and simplification**

- Automate validated, simplified patterns
- Create guardrails for architectural principles (e.g., linters enforcing 2+ consumer rule)
- Generate boilerplate for necessary patterns
- Build tooling for remaining complexity

### Step 4: Generate Analysis Report

Produce a comprehensive report using the template from `references/first_principles_framework.md`. The report should include:

- **Executive Summary** - High-level findings and recommendations
- **Current State Map** - Component inventory with consumer counts
- **Challenged Assumptions** - Validation results for questioned requirements
- **Deletion Candidates** - Specific components to remove with justification
- **Simplification Plan** - How to reduce complexity in remaining components
- **Acceleration Opportunities** - Bottlenecks and coupling issues
- **Automation Candidates** - Patterns ready for automation
- **Implementation Plan** - Phased approach with specific actions
- **Metrics** - Before/after comparison (LOC, component count, coupling, deployment time)

### Step 5: Iterate and Refine

After presenting findings:
- Address user questions and concerns
- Dive deeper into specific areas
- Adjust recommendations based on constraints or context
- Help prioritize changes by impact and risk

## Critical Guidelines

### The Deletion Mindset

- **Start by trying to delete everything** - Can always add back if needed
- **Optimize nothing until deletion is complete** - Most common error is optimizing something that shouldn't exist
- **If not occasionally wrong about deletion, not deleting enough** - Being too conservative defeats the purpose

### The 2-3 Rule Enforcement

- **2+ consumers** - Minimum threshold for services, helpers, shared components
- **3+ uses** - Minimum for utilities, hooks, small helpers
- **Below threshold** - Inline the logic, embrace cohesion over decomposition
- **Exception handling** - Only allow exceptions with explicit justification (not "might need later")

### Cargo Cult Detection

Identify patterns adopted without understanding:
- "We use X because Google/Netflix/Amazon does" (different scale, different problems)
- "Everything must be pluggable" (YAGNI - You Aren't Gonna Need It)
- "We need a service mesh for 3 services" (premature distribution)
- "Let's use microservices" (without understanding the operational complexity cost)

### Question Authority (Professionally)

- **Every requirement needs a name** - Who decided this? Why?
- **"Best practice" is not a reason** - Best for whom? In what context?
- **Regulations must be verified** - What's the actual requirement vs. interpretation?
- **"It's always been done this way"** - Weakest possible justification

## Common Use Cases

### Use Case 1: "Should We Extract This Service?"

**User asks**: "Should we create a shared service for this authentication logic?"

**Introspection process**:
1. **Count consumers** - How many components need this logic? (Phase 1)
2. **Question requirement** - Why extract now vs. when 2nd consumer appears? (Phase 2)
3. **If <2 consumers** - Don't extract, keep cohesive (Phase 3: Delete the abstraction idea)
4. **If 2+ consumers** - Extract with simplest possible interface (Phase 4: Simplify)

### Use Case 2: "Our Architecture Is Too Complex"

**User complains**: "It takes 15 files to add a simple feature"

**Introspection process**:
1. **Map the files** - What are they? What's their purpose? (Phase 1)
2. **Count consumers** - How many use each abstraction? (Phase 1)
3. **Challenge each layer** - Who required it? Why? (Phase 2)
4. **Delete single-consumer abstractions** - Inline them (Phase 3)
5. **Simplify what remains** - Reduce ceremony (Phase 4)

### Use Case 3: "Evaluating a Refactoring Plan"

**User proposes**: "We should create a new abstraction layer for data access"

**Introspection process**:
1. **Question the requirement** - What problem does this solve? Who needs it? (Phase 2)
2. **Count potential consumers** - Do 2+ components need this? (Phase 1)
3. **Consider deletion** - Can we solve the problem without adding a layer? (Phase 3)
4. **If justified** - What's the simplest implementation? (Phase 4)

### Use Case 4: "Onboarding to a Codebase"

**User wants to understand**: "Why is this codebase structured this way?"

**Introspection process**:
1. **Map current state** - Inventory components, consumers, patterns (Phase 1)
2. **Research decisions** - Git history, commit messages, comments (Phase 2)
3. **Identify unjustified complexity** - Single-use abstractions, cargo-cult patterns (Phase 3)
4. **Recommend quick wins** - Low-risk deletions and simplifications (Phase 3-4)

## Anti-Patterns to Flag

When analyzing architectures, specifically call out these anti-patterns:

### 1. Enterprise Fizz-Buzz
- 15 files to implement simple logic
- AbstractFactoryFactoryProvider patterns
- Layers upon layers with no clear value

### 2. Premature Abstraction
- "We might need this later" (YAGNI violation)
- Generic frameworks for single use case
- Abstraction with 0-1 consumers

### 3. Not-Invented-Here Syndrome
- Rebuilding proven libraries poorly
- Custom frameworks when standard ones exist
- Reinventing wheels

### 4. Resume-Driven Development
- Latest tech for simple problems
- Over-engineering to learn new framework
- Complexity for complexity's sake

### 5. Cargo Cult Architecture
- Microservices for everything
- "Netflix does it, so should we"
- Enterprise patterns in startups

## Success Metrics

A successful introspection achieves:

- **Fewer components** - Deleted unnecessary abstractions
- **Clear justifications** - Every component has a validated reason to exist
- **High cohesion** - Related functionality stays together
- **Low coupling** - Independent evolution of modules
- **Fast feedback** - Quick from change to production
- **Easy onboarding** - Reduced cognitive load for new developers
- **2+ consumer rule** - Every abstraction serves multiple actual (not hypothetical) needs

## Output Format

Use the Architecture Analysis Report template from `references/first_principles_framework.md`, adapted to the scope:

- For **system-wide analysis** - Full 6-phase report
- For **specific decisions** - Focused analysis on relevant phases
- For **quick evaluations** - Executive summary + key findings
- For **refactoring plans** - Heavy emphasis on Phase 3 (deletion) and Phase 4 (simplification)

## Important Notes

- **Deletion is the hardest step** - Pushback is natural, persist with evidence
- **Question respectfully** - "Who required this?" seeks understanding, not blame
- **Measure before/after** - Quantify improvement (LOC, component count, deployment time)
- **Start small** - Quick wins build momentum for larger changes
- **Add back if wrong** - The point is to err on the side of deletion, course-correct as needed

## Deep Thinking Mode

For complex architectural analysis, activate extended thinking:
- **"think harder"** or **"ultrathink"** triggers maximum reasoning depth (31,999 tokens)
- Use for: system-wide analysis, critical migration planning, multi-system tradeoffs
- Enables thorough first-principles reasoning across all 6 phases
- Recommended when: architecture spans 10+ components, involves legacy systems, or has high stakes

## Integration with Development Workflows

This skill complements:
- **Code review** - Ensure new abstractions meet 2+ consumer threshold
- **Architectural decision records (ADRs)** - Validate decisions against first principles
- **Refactoring planning** - Systematically identify what to delete, simplify, or keep
- **Technical debt assessment** - Quantify unjustified complexity
- **Onboarding documentation** - Explain architectural rationale clearly

## Examples of Good Questions to Ask

During introspection, ask:

- "This service has 1 consumer. Why is it extracted?"
- "What problem would occur if we deleted this layer?"
- "Who decided we need this abstraction? What was their reasoning?"
- "Is this pattern solving a problem we actually have or might have?"
- "Can we inline this and extract later when a 2nd consumer appears?"
- "What's the simplest thing that could possibly work?"
- "Are we optimizing something that shouldn't exist?"

## Remember

The goal is not to delete everything, but to **question everything** and keep only what survives rigorous justification. Good architecture is defined more by what it doesn't have than by what it does have.

**Most common error**: Optimizing something that shouldn't exist.
**Solution**: Delete first, optimize never (if it shouldn't exist) or later (if it should).
