---
name: dapp-sdd:specify
description: Use when expanding a README-based dApp description into a full specification with user stories and acceptance criteria.
---

# Specify Skill

Expands a user's README.md dApp description into a comprehensive specification.

## Input

The user's README.md containing:
- What the dApp should demonstrate
- Basic functionality description
- Any specific requirements or constraints

## Output

A structured specification saved to `.dapp-sdd/spec.md` containing:

### 1. Overview Section
- **Purpose:** What concept this dApp demonstrates
- **Target Audience:** Who will learn from this example
- **Learning Outcomes:** What developers will understand after studying this

### 2. User Stories

Format each as:
```
### US{N}: {Title}

**As a** developer learning Midnight
**I want to** {action}
**So that** {benefit}

**Acceptance Criteria:**
- [ ] AC1: {Specific, testable criterion}
- [ ] AC2: {Specific, testable criterion}
- [ ] AC3: {Specific, testable criterion}
```

### 3. Technical Requirements

- **Compact Contract:** What circuits are needed
- **TypeScript Integration:** CLI commands, deployment scripts
- **State Management:** What state the contract tracks
- **Privacy Model:** What's private vs public

### 4. Out of Scope

Explicitly list what this example does NOT cover to keep it focused.

## Process

1. Read the README.md content provided
2. Identify the core concept being demonstrated
3. Extract functional requirements
4. Generate 2-4 user stories (keep it minimal for examples)
5. Define clear acceptance criteria
6. Document technical requirements
7. Save to `.dapp-sdd/spec.md`

## Skill References

Invoke these skills to validate the specification:
- `compact-core:language-reference` - Verify Compact concepts are correctly referenced
- `midnight-dapp:*` - Ensure dApp patterns are appropriate

## Example Spec Structure

```markdown
# {DApp Name} Specification

## Overview

**Purpose:** Demonstrate {concept} in Midnight
**Target Audience:** Developers learning {topic}
**Learning Outcomes:**
- Understand how to {outcome 1}
- Learn to {outcome 2}

## User Stories

### US1: Basic Contract Interaction

**As a** developer learning Midnight
**I want to** deploy and interact with a simple contract
**So that** I understand the basic development workflow

**Acceptance Criteria:**
- [ ] Contract compiles without errors
- [ ] Contract deploys to local network
- [ ] CLI can call contract circuits

### US2: {Second Story}
...

## Technical Requirements

### Compact Contract
- Circuit: `{name}` - {purpose}
- State: `{field}` - {description}

### TypeScript Integration
- `deploy.ts` - Deployment script
- `cli.ts` - Interactive CLI

### Privacy Model
- Private: {what's private}
- Public: {what's public}

## Out of Scope

- Production deployment
- Error recovery
- Multiple users
```
