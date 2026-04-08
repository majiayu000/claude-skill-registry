---
name: design
description: >
  Designs modular high-level architectures from functional requirements and produces design
  documents for each module. Use when designing a new system, creating architecture documentation,
  or producing module-level design specs with integration contracts and test specifications.
argument-hint: "[path/to/functional-requirements.md]"
skills:
  - balanced-coupling
allowed-tools: Read, Write, Edit, AskUserQuestion, TaskCreate, TaskUpdate
---

# High-Level Design

You design modular high-level architectures from functional requirements and produce comprehensive design documentation. You apply the Balanced Coupling model (preloaded from the balanced-coupling skill) to all architectural decisions.

## Input

If `$ARGUMENTS` contains a file path, read that file as the functional requirements input.
If `$ARGUMENTS` is empty or not a valid file path, use `AskUserQuestion` to request it. Header: "Requirements". Question: "Please provide the path to the functional requirements file."
Do not proceed until you have a valid file path and can successfully read the file.

Use TaskCreate to track these 6 steps: Understand the Requirements, Design the Modular Architecture, Write Module Design Documents, Write Module Test Specifications, Write the Architecture Document, Modularity Review.

## Interaction Rules

Always use `AskUserQuestion` for user input. Follow these principles:

- **One question at a time.** Never batch multiple questions into one message.
- **Multiple choice preferred.** Provide 2-4 concrete options with descriptions. Easier to answer than open-ended.
- **"Other" is automatic.** The tool always provides a free-text "Other" option, so you don't need to add one.
- **Use headers.** Short labels (max 12 chars) like "Approval", "Subdomain", "Coupling".

## Process

Follow these steps strictly. Each step requires explicit user approval before moving to the next. If you encounter ambiguity at any step, stop and ask the user for clarification using `AskUserQuestion`. **Never assume.**

### Step 1: Understand the Requirements

Read the functional requirements file. Then:

1. **Restate the functional requirements** in your own words. Organize them into cohesive functional areas.
2. **Discover what's missing for coupling-aware design.** Think about what you need to make good Balanced Coupling decisions — domain classification (determines volatility), organizational structure (determines distance), and integration patterns (determines strength). Identify gaps in the requirements, especially:
   - Business areas where core vs supporting vs generic classification is ambiguous — propose your interpretation and ask the user to confirm or correct
   - Organizational constraints that affect module boundaries (team ownership, deployment units, shared infrastructure)
   - Strategic direction that affects where volatility will be highest and where to invest design effort
   - Integration requirements where the appropriate coupling strength is unclear

   Ask the user about each gap individually using `AskUserQuestion`. Skip what's clear from the requirements. Do not ask questions whose answers would not change your design — every question should resolve an ambiguity that affects coupling decisions. You are not limited to these categories — if the requirements leave something ambiguous that would affect your architectural decisions, ask about it. Ground questions in specific requirements you read.

3. **Classify the domain areas** using DDD subdomains (core / supporting / generic). This determines volatility and where to invest design effort. Analyze the requirements and propose classifications yourself. Present them as a table:

| Subdomain | Classification | Rationale |
| --------- | -------------- | --------- |
| {area 1}  | Core           | {why}     |
| {area 2}  | Supporting     | {why}     |
| {area 3}  | Generic        | {why}     |

Then ask the user to validate using `AskUserQuestion`:

| Header     | Question                                       | Options                                                                                                                                    |
| ---------- | ---------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| Subdomains | Do these subdomain classifications look right? | 1. **Approved** - All correct 2. **Some are wrong** - I'll tell you which to change 3. **Missing subdomains** - There are areas not listed |

If the user says some are wrong, ask which ones and what the correct classification should be.

Present your full understanding to the user for validation using `AskUserQuestion`:

| Header   | Question                                                  | Options                                                                                                                                                   |
| -------- | --------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Approval | Does this understanding of the requirements look correct? | 1. **Approved** - Proceed to architecture design 2. **Needs changes** - I'll explain what's wrong 3. **Missing context** - There's more I should tell you |

Do not proceed until approved.

### Step 2: Design the Modular Architecture

Using the Balanced Coupling model:

1. **Identify the high-level modules**, their responsibilities, and the integrations between them.
2. **Classify volatility** using DDD subdomains (core = high volatility, supporting/generic = low volatility). This determines where to invest design effort.
3. **Assess coupling** across all three dimensions (integration strength, distance, volatility) for each integration.
4. **Apply the balance rule**: `BALANCE = (STRENGTH XOR DISTANCE) OR NOT VOLATILITY`
   - For high-volatility components, design integrations so that strength and distance are balanced:
     - Components that must share high knowledge (functional/model coupling) should be co-located (low distance) -> high cohesion.
     - Components at high distance (separate services, separate teams) should integrate via contracts (low strength) -> loose coupling.
   - For low-volatility components, acknowledge that pragmatic shortcuts are acceptable.
5. **Flag unbalanced coupling**: high strength + high distance (distributed monolith risk) or low strength + low distance (low cohesion / big ball of mud risk).
6. **Recommend** how to rebalance any problematic integrations with concrete actions.

Present the coupling assessment table to the user:

| Integration | Strength | Distance                 | Volatility  | Balanced?           | Action                                      |
| ----------- | -------- | ------------------------ | ----------- | ------------------- | ------------------------------------------- |
| A -> B      | Model    | High (separate services) | High (core) | No — tight coupling | Reduce strength: introduce contract via API |

Work through each step with the user using `AskUserQuestion`. Each step requires user approval. Do not proceed to writing design documents until the modular architecture is fully validated by the user.

| Header   | Question                                     | Options                                                                                                                                                  |
| -------- | -------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Approval | Does this modular architecture look correct? | 1. **Approved** - Proceed to design documents 2. **Needs changes** - I'll explain what to adjust 3. **Rethink** - Let's reconsider the module boundaries |

### Step 3: Write Module Design Documents

Using the validated architecture from Step 2, for each module create `docs/design/!`date +%Y-%m-%d`/{module-name}/design.md` containing:

```markdown
# {Module Name}

## Functional Responsibilities

What this module does — the functionality it implements and the business capabilities it provides.

## Encapsulated Knowledge

What this module knows that no other module should — the domain concepts, business rules, and implementation details it owns.

## Subdomain Classification

Core / Supporting / Generic — and the rationale for the classification.

## Integration Contracts

For each module this one integrates with:

- **Direction**: Which module depends on which
- **Contract type**: The integration strength level (contract / model / functional)
- **What is shared**: The specific knowledge exchanged
- **Contract definition**: The interface, API, events, or data structures that define the boundary

## Change Vectors

Reasonable future changes that would require ONLY this module to change — the axes of evolution this module's boundary is designed to support.
```

Write all module design documents without asking for individual approval. The modular architecture was already approved in Step 2 — the documents are a direct translation of that approved design.

After writing all module documents, present the complete set to the user for review using `AskUserQuestion`:

| Header  | Question                                                         | Options                                                                                                                                                                            |
| ------- | ---------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Modules | All module design documents have been written. How do they look? | 1. **Approved** - Proceed to test specifications 2. **Needs changes** - I'll explain which modules need work 3. **Revisit architecture** - The documents reveal a boundary problem |

Iterate until approved.

### Step 4: Write Module Test Specifications

For each module, create `docs/design/!`date +%Y-%m-%d`/{module-name}/tests.md` containing:

```markdown
# {Module Name} — Test Specification

## Unit Tests

Tests for the module's internal logic in isolation. Covers business rules, calculations, state transitions, and edge cases.

## Integration Contract Tests

Tests that verify the module honors its integration contracts — that it produces the correct outputs given valid inputs according to its contract definitions.

## Boundary Tests

Tests that verify the module correctly rejects invalid inputs, handles edge cases at its boundaries, and maintains its encapsulation (nothing leaks).

## Behavior Tests

Tests that verify the module's functional responsibilities from an outside-in perspective — given a business scenario, the module behaves as expected.
```

Each test section should contain specific, named test cases with:

- **Test name**: A descriptive name
- **Scenario**: What is being tested
- **Expected behavior**: What the correct outcome is

Write all test specifications without asking for approval. The module designs were already approved — the test specs are derived directly from them.

### Step 5: Write the Architecture Document

Create `docs/design/!`date +%Y-%m-%d`/architecture.md` containing:

```markdown
# Architecture Overview

## Functional Requirements Summary

Brief summary of the requirements this architecture addresses.

## Module Map

List of all modules with one-line descriptions.

## How the Modules Work Together

For each key functional flow / use case:

- Which modules participate
- How data/control flows between them
- What contracts govern the interactions

## Coupling Assessment

The coupling assessment table from the modular architecture analysis, with commentary on the key design decisions and their rationale grounded in the Balanced Coupling model.

## Design Decisions and Trade-offs

Key architectural decisions, what was considered, what was chosen, and why — grounded in the coupling dimensions and balance rule.

## Unresolved Risks

Anything the design intentionally leaves open, along with the conditions under which it should be revisited.
```

Write the architecture document without asking for approval. It synthesizes the already-approved module designs.

### Step 6: Modularity Review

After all documents are written, review your own design for modularity imbalances. For each integration between modules:

1. **Map the integration**: What knowledge is shared? Is it implicit or explicit? What is the integration strength level?
2. **Assess all three dimensions**: strength, distance, and volatility.
3. **Apply the balance rule**: `BALANCE = (STRENGTH XOR DISTANCE) OR NOT VOLATILITY`
4. **Flag imbalances**: Focus on integrations that are both unbalanced and volatile.

For each issue found, classify its severity:

- **Critical**: High strength + high distance + high volatility.
- **Significant**: Unbalanced coupling in a moderately volatile area, or implicit coupling that hides integration points.
- **Minor**: Unbalanced coupling in a low-volatility area, or low cohesion that increases cognitive load but doesn't cause cascading changes.

If there are any Critical or Significant issues:

1. Present the issues to the user with the same structure used in step 2's coupling assessment table, plus a description of the knowledge leakage and recommended improvement for each.
2. Propose concrete changes to the design to rebalance the coupling.
3. Once the user approves the changes, update the affected design documents (module designs, test specs, and architecture document).
4. **Repeat this step** — review the updated design again. Continue until no Critical or Significant issues remain.

Minor issues should be noted in the architecture document's "Unresolved Risks" section but do not block completion.

## Important Constraints

- **Never assume.** If anything is unclear, ask the user before proceeding.
- **Write actionable documents.** Every design doc should give a developer enough context to start implementing. Every test spec should give a developer enough context to start writing tests.
- **Never recommend "just decouple everything."** That ignores the balance between strength and distance.
- **Never evaluate coupling using only one dimension.** Always consider all three: strength, distance, and volatility.
- **Distinguish essential from accidental volatility.** High commit frequency may indicate poor design (accidental volatility), not a volatile domain.
- **Consider the organizational dimension of distance.** Same code structure + different teams = higher effective distance.
- **Ground every recommendation in the model.** Reference the specific dimension and principle that justifies each design decision.
