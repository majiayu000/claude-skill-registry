---
name: superspec:brainstorm
description: |
  Use before any feature work. Progressive design flow with four phases:
  Explore → Propose → Design → Spec
  Outputs: proposal.md, design.md, specs/*.md
---

# Brainstorming: From Ideas to Specifications

## Overview

A progressive flow that guides from free exploration to structured specifications.
One command, four phases, complete design documentation.

```
┌─────────────────────────────────────────────────────────────────────┐
│                     /superspec:brainstorm                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   Phase 1: EXPLORE                                                   │
│   ─────────────────                                                  │
│   Free exploration, understand the problem                           │
│   • Ask clarifying questions                                         │
│   • Investigate the codebase                                         │
│   • Visualize ideas                                                  │
│                                                                      │
│                    ↓ Problem sufficiently clear                      │
│                                                                      │
│   Phase 2: PROPOSE → proposal.md                                     │
│   ─────────────────                                                  │
│   Define change scope                                                │
│   • Why (problem/opportunity)                                        │
│   • What Changes (change list)                                       │
│   • Capabilities (feature scope)                                     │
│   • Impact (affected areas)                                          │
│                                                                      │
│                    ↓ Scope confirmed                                 │
│                                                                      │
│   Phase 3: DESIGN → design.md                                        │
│   ─────────────────                                                  │
│   Technical solution design                                          │
│   • 2-3 approach comparison                                          │
│   • Chosen approach with rationale                                   │
│   • Trade-offs                                                       │
│   • Technical details                                                │
│                                                                      │
│                    ↓ Approach confirmed                              │
│                                                                      │
│   Phase 4: SPEC → specs/*.md                                         │
│   ─────────────────                                                  │
│   Define specifications (testable behavior)                          │
│   • Requirements (system SHALL...)                                   │
│   • Scenarios (WHEN/THEN → each becomes a test)                      │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

**Announce at start:** "I'm using the brainstorm skill to explore this idea and develop specifications."

## When to Use

**Always use before:**
- New features or functionality
- Breaking changes
- Architecture changes
- Behavior modifications

**Skip for:**
- Bug fixes (restore intended behavior)
- Typos, formatting
- Configuration changes

---

## Phase 1: EXPLORE

### The Stance

This phase is **a stance, not a workflow**. Be curious, not prescriptive.

### What You Do

**Understand Context First:**
```bash
superspec list --specs    # Existing specs
superspec list            # In-progress changes
```

**Then Explore Freely:**
- Ask clarifying questions (one at a time)
- Challenge assumptions
- Reframe the problem
- Investigate the codebase
- Visualize with ASCII diagrams

### Visualization

Use ASCII diagrams liberally:

```
┌─────────────────────────────────────────┐
│     Current State vs Desired State       │
├─────────────────────────────────────────┤
│   NOW                    GOAL            │
│   ┌────────┐            ┌────────┐      │
│   │ Single │  ────────▶ │  2FA   │      │
│   │ Factor │            │ Enabled│      │
│   └────────┘            └────────┘      │
└─────────────────────────────────────────┘
```

### Transition Signal

> "I have sufficient understanding of the problem. Let's define the change scope."

---

## Phase 2: PROPOSE → proposal.md

### Purpose

Define **Why** and **What**, without addressing How.

### Output

Create: `superspec/changes/[change-id]/proposal.md`

```markdown
# Change: [Brief Description]

## Why
[1-2 sentences - problem/opportunity]

What problem does this solve?
Why is this the right time to address it?

## What Changes
- [Change 1]
- [Change 2]
- [**BREAKING** if applicable]

## Capabilities

### New Capabilities
- [capability-name]: [brief description]

### Modified Capabilities
- [existing-capability]: [what changes]

## Impact
- Affected specs: [list]
- Affected code: [key files]
- Affected APIs: [endpoints]
- Dependencies: [new/changed]
```

### Key Points

- Keep it brief (within 1 page)
- Focus on Why and What
- Don't include technical details (that's for design.md)

### Transition Signal

> "Change scope confirmed. Let's design the technical solution."

---

## Phase 3: DESIGN → design.md

### Purpose

Define **How** - technical solution and decisions.

### Output

Create: `superspec/changes/[change-id]/design.md`

```markdown
# Design: [Feature Name]

## Context
[Background, current state, constraints]

## Goals / Non-Goals

### Goals
- [What this design achieves]

### Non-Goals
- [What this design explicitly excludes]

## Approaches Considered

### Approach A: [Name]
[Description]

**Pros:**
- [Advantage 1]
- [Advantage 2]

**Cons:**
- [Disadvantage 1]
- [Disadvantage 2]

### Approach B: [Name]
[Description]

**Pros:**
- [Advantages]

**Cons:**
- [Disadvantages]

### Approach C: [Name] (if applicable)
[Description]

## Decision

**Chosen Approach:** [A/B/C]

**Rationale:**
[Why this approach was selected]

## Trade-offs
[What we're giving up and why it's acceptable]

## Technical Details

### Architecture
[High-level architecture description]

### Key Components
- [Component 1]: [Purpose]
- [Component 2]: [Purpose]

### Data Flow
```
[ASCII diagram of data flow]
```

## Risks and Mitigations
| Risk | Mitigation |
|------|------------|
| [Risk 1] | [How to mitigate] |
| [Risk 2] | [How to mitigate] |

## Open Questions
- [Question 1]
- [Question 2]
```

### Key Points

- **Must** compare 2-3 approaches
- Clearly state the rationale for selection
- Document trade-offs
- Technical details should be specific but not excessive

### Transition Signal

> "Technical solution confirmed. Let's define the specifications - each Scenario will become a test case."

---

## Phase 4: SPEC → specs/*.md

### Purpose

Define **testable behavior** - Requirements and Scenarios.

### Critical Mindset

```
Each Scenario will become a TDD test
Write Scenarios like test descriptions
```

### Output

Create: `superspec/changes/[change-id]/specs/[capability]/spec.md`

**For New Capabilities:**

```markdown
# [Capability Name] Specification

## Purpose
[1-2 sentences explaining what this capability provides]

## Requirements

### Requirement: [Requirement Name]
The system SHALL [behavior description].

#### Scenario: [Scenario Name]
- **WHEN** [trigger condition]
- **THEN** [expected result]
- **AND** [additional result] (optional)

#### Scenario: [Another Scenario]
- **WHEN** [different condition]
- **THEN** [different result]

### Requirement: [Another Requirement]
The system SHALL [another behavior].

#### Scenario: [Scenario Name]
- **WHEN** [condition]
- **THEN** [result]
```

**For Modified Capabilities (Delta Spec):**

```markdown
## ADDED Requirements

### Requirement: [New Feature]
The system SHALL [new behavior].

#### Scenario: [New Scenario]
- **WHEN** [condition]
- **THEN** [result]

## MODIFIED Requirements

### Requirement: [Existing Feature - EXACT NAME MATCH]
The system SHALL [updated behavior - FULL CONTENT].

#### Scenario: [Updated Scenario]
- **WHEN** [updated condition]
- **THEN** [updated result]

## REMOVED Requirements

### Requirement: [Deprecated Feature]
**Reason**: [Why removing]
**Migration**: [How to handle existing usage]

## RENAMED Requirements
- FROM: `### Requirement: Old Name`
- TO: `### Requirement: New Name`
```

### Scenario Writing Tips

**Think Like Tests:**

| Pattern | Example |
|---------|---------|
| Happy path | `Scenario: Successful login` |
| Error case | `Scenario: Invalid password rejected` |
| Edge case | `Scenario: Empty input handled` |
| State change | `Scenario: Account locked after 5 failures` |

**Be Specific:**

```markdown
# Bad - Too vague
#### Scenario: User logs in
- WHEN user logs in
- THEN it works

# Good - Specific and testable
#### Scenario: Valid credentials accepted
- **WHEN** user provides valid email and password
- **THEN** system returns authentication token
- **AND** session is created with 24-hour expiry
```

### Validation

After writing specs:

```bash
superspec validate [change-id] --strict
```

---

## Complete Example

### Phase 1: EXPLORE

```
User: I want to add two-factor authentication

Claude: Let me first understand...

┌─────────────────────────────────────────────┐
│              2FA Option Space                │
├─────────────────────────────────────────────┤
│   TOTP          SMS           WebAuthn      │
│   ┌────┐       ┌────┐        ┌────┐        │
│   │ App│       │ Phone│      │ Key │        │
│   └────┘       └────┘        └────┘        │
│   Works offline Needs network Needs hardware│
└─────────────────────────────────────────────┘

A few questions:
1. Who are the primary users?
2. Do you need offline verification?
3. Any budget constraints?

User: Consumer-focused, need offline, low budget

Claude: Understood, this points to TOTP solution. Let's define the change scope...
```

### Phase 2: PROPOSE → proposal.md

```markdown
# Change: Add Two-Factor Authentication

## Why
Users have requested additional account security. Single-factor auth
identified as vulnerability in security audit.

## What Changes
- Add TOTP-based 2FA option
- Add backup codes for recovery
- **BREAKING**: Login flow requires 2FA when enabled

## Capabilities

### New Capabilities
- two-factor-auth: TOTP setup, verification, management
- backup-codes: Generation and redemption

### Modified Capabilities
- user-auth: Login flow includes 2FA step

## Impact
- Affected specs: user-auth
- Affected code: src/auth/*
- Affected APIs: POST /auth/login, /auth/2fa/*
- Dependencies: otplib (new)
```

### Phase 3: DESIGN → design.md

```markdown
# Design: Two-Factor Authentication

## Context
Current system uses single-factor (password) authentication.
Need to add optional 2FA for enhanced security.

## Goals / Non-Goals

### Goals
- TOTP-based 2FA
- Backup codes for recovery
- Seamless user experience

### Non-Goals
- SMS OTP (cost, security concerns)
- WebAuthn (complexity, hardware requirement)

## Approaches Considered

### Approach A: TOTP Only
Standard TOTP with authenticator apps.

**Pros:** Simple, offline, free, standard
**Cons:** Requires app installation

### Approach B: TOTP + Email Fallback
TOTP primary, email OTP as fallback.

**Pros:** More accessible
**Cons:** Email less secure, adds complexity

### Approach C: TOTP + WebAuthn
TOTP primary, WebAuthn for advanced users.

**Pros:** Most secure option available
**Cons:** Complex, hardware dependency

## Decision

**Chosen Approach:** A (TOTP Only)

**Rationale:**
- Meets offline requirement
- No additional cost
- Industry standard
- Can add WebAuthn later as enhancement

## Trade-offs
- Users must install authenticator app
- No fallback if phone lost (mitigated by backup codes)

## Technical Details

### Architecture
```
┌──────────┐     ┌──────────┐     ┌──────────┐
│  Client  │────▶│   API    │────▶│ TOTP Svc │
└──────────┘     └──────────┘     └──────────┘
                       │
                       ▼
                ┌──────────┐
                │    DB    │
                │ (secret) │
                └──────────┘
```

### Key Components
- TOTPService: Generate/verify codes
- BackupCodeService: Generate/redeem codes
- AuthMiddleware: 2FA verification step

## Risks and Mitigations
| Risk | Mitigation |
|------|------------|
| User loses phone | Backup codes |
| Time sync issues | 30-second window tolerance |
```

### Phase 4: SPEC → specs/*.md

```markdown
# Two-Factor Authentication Specification

## Purpose
Provides TOTP-based two-factor authentication for enhanced security.

## Requirements

### Requirement: 2FA Setup
The system SHALL allow users to enable TOTP-based 2FA.

#### Scenario: Generate setup QR code
- **WHEN** user requests 2FA setup
- **THEN** system generates TOTP secret
- **AND** displays QR code for authenticator app
- **AND** displays manual entry code

#### Scenario: Verify setup with valid code
- **WHEN** user enters valid TOTP code during setup
- **THEN** 2FA is enabled on account
- **AND** backup codes are generated

#### Scenario: Reject invalid setup code
- **WHEN** user enters invalid TOTP code during setup
- **THEN** setup fails
- **AND** user can retry

### Requirement: 2FA Verification
The system SHALL require TOTP verification during login when enabled.

#### Scenario: Valid TOTP accepted
- **WHEN** user enters valid TOTP code
- **THEN** login succeeds
- **AND** session is created

#### Scenario: Invalid TOTP rejected
- **WHEN** user enters invalid TOTP code
- **THEN** login fails
- **AND** attempt is logged

#### Scenario: Rate limiting on failures
- **WHEN** user fails 5 TOTP attempts
- **THEN** account is temporarily locked
- **AND** user is notified
```

---

## Outputs Summary

After completing all four phases:

```
superspec/changes/[change-id]/
├── proposal.md      # Phase 2: Why + What
├── design.md        # Phase 3: How (technical solution)
└── specs/
    └── [capability]/
        └── spec.md  # Phase 4: What (specification details)
```

## Validation

Before proceeding to planning:

```bash
superspec validate [change-id] --strict
```

## Next Step

After brainstorm completes:

> "Design complete! Documents saved:
> - `superspec/changes/[id]/proposal.md`
> - `superspec/changes/[id]/design.md`
> - `superspec/changes/[id]/specs/[cap]/spec.md`
>
> Validation: `superspec validate [id] --strict`
>
> Next step: `/superspec:plan` to create TDD implementation plan"

---

## Key Principles

| Principle | Description |
|-----------|-------------|
| **Progressive Convergence** | From free exploration gradually converge to structured specifications |
| **Document Separation** | proposal / design / specs each have their own responsibility, avoiding overly long context |
| **Must Compare Approaches** | Design phase requires at least 2-3 approaches |
| **Scenario = Test** | Writing Scenarios is writing test descriptions |

## Document Responsibilities

| Document | Content | When AI Reads |
|----------|---------|---------------|
| `proposal.md` | Why + What | Understanding change purpose |
| `design.md` | How (technical solution) | Understanding implementation approach |
| `specs/*.md` | What (specification details) | Implementation and verification |

## Red Flags

| Warning Sign | Problem |
|--------------|---------|
| Skipping Explore and going straight to Spec | May not fully understand the problem |
| Only one approach | Haven't fully explored alternatives |
| proposal.md too long | Should move technical details to design.md |
| Scenario too vague | Cannot convert to test |
| No WHEN/THEN | Format error, validation will fail |
