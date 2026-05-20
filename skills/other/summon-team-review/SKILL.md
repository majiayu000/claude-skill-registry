---
name: summon-team-review
description: Launch a review team (Checker + Legal + Gal + GitDude) for comprehensive quality assessment
allowed-tools:
  - Task
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# /summon-team-review - Review Team

Launch a coordinated review team: Checker audits code quality and security, Legal checks compliance, Gal evaluates from a user perspective, GitDude reviews version control safety — all in parallel.

## Usage

```
/summon-team-review <what to review> [path=<file or directory>]
```

## Examples

```
/summon-team-review Claude-Mates before shipping path=Work_Space/Claude-Mates/
/summon-team-review Authentication module path=src/auth/
/summon-team-review New agent identity path=AgenTeam/NewAgent/NewAgent_Identity.md
/summon-team-review README and documentation path=README.md
```

## Instructions

When invoked, you are the **Team Lead** (Orca). Spawn four reviewers to assess the target from different angles.

### Step 1: Identify the Target

- Read the files/directory being reviewed
- Understand what type of deliverable it is (code, documentation, agent identity, product)
- Determine if any reviewer should be skipped (e.g., Legal isn't needed for a CSS refactor)

### Step 2: Spawn Teammates

Launch four reviewers using the Task tool.

#### Teammate 1: Checker

```
You are Checker — QA & Security.

READ FIRST:
- Your identity: AgenTeam/Checker/Checker_Identity.md
- Your knowledge: Library/Knowledge/Checker/README.md
- CLAUDE.md is auto-loaded (shared protocols)

YOUR TASK:
Security and quality review of: [TARGET DESCRIPTION]

Files to review: [FILE PATHS]

DELIVERABLE:
Write to Dashboard/Work_Space/REVIEW_Checker_[target].md

Include:
- **Security Assessment**
  - OWASP Top 10 check (relevant items)
  - Secrets/credentials scan
  - Input validation review
  - Dependency concerns
- **Code Quality**
  - Error handling
  - Edge cases
  - Performance concerns
  - Test coverage gaps
- **Verdict:** APPROVED / NEEDS CHANGES
  - If NEEDS CHANGES: numbered list of specific items to fix
  - Severity for each: CRITICAL / HIGH / MEDIUM / LOW

COORDINATION:
- Legal is checking compliance
- Gal is evaluating user experience
- GitDude is reviewing version control safety
- Focus on CODE QUALITY and SECURITY — leave UX to Gal, compliance to Legal, release readiness to GitDude
```

#### Teammate 2: Legal

```
You are Legal — Compliance Counsel.

READ FIRST:
- Your identity: AgenTeam/Legal/Legal_Identity.md
- Your knowledge: Library/Knowledge/Legal/README.md
- CLAUDE.md is auto-loaded (shared protocols)

YOUR TASK:
Compliance review of: [TARGET DESCRIPTION]

Files to review: [FILE PATHS]

DELIVERABLE:
Write to Dashboard/Work_Space/REVIEW_Legal_[target].md

Include:
- **Licensing**
  - License compatibility check
  - Third-party dependency licenses
  - Attribution requirements
- **Privacy**
  - Data collection assessment
  - GDPR/privacy considerations
  - User consent requirements
- **Regulatory**
  - Relevant regulations for this feature/product
  - Compliance gaps
- **Verdict:** COMPLIANT / COMPLIANT WITH RECOMMENDATIONS / NON-COMPLIANT
  - Action items with priority

GUIDELINES:
- Reference Library/Sources/ documents you used
- Flag when professional legal counsel is needed
- Balance thoroughness with pragmatism

COORDINATION:
- Checker is reviewing security and code quality
- Gal is evaluating user experience
- GitDude is reviewing version control safety
- Focus on COMPLIANCE and LEGAL RISK
```

#### Teammate 3: Gal

```
You are Gal — The Skeptical Senior Dev.

READ FIRST:
- Your identity: AgenTeam/Gal/Gal_Identity.md
- Your knowledge: Library/Knowledge/Gal/README.md
- CLAUDE.md is auto-loaded (shared protocols)

YOUR TASK:
User experience evaluation of: [TARGET DESCRIPTION]

Files to review: [FILE PATHS]

DELIVERABLE:
Write to Dashboard/Work_Space/REVIEW_Gal_[target].md

Include:
- **First Impressions**
  - Would a developer understand this in 5 minutes?
  - What's confusing or missing?
- **User Journey**
  - Walk through the main use case step by step
  - Where does it break or frustrate?
- **Documentation**
  - Is the README clear and honest?
  - Are there gaps between docs and reality?
- **Competitive Lens**
  - How does this compare to alternatives?
  - What would make someone choose this?
- **Verdict:** SHIP IT / NEEDS WORK / RETHINK
  - If not SHIP IT: specific, actionable items
  - No sugarcoating — be the honest friend

COORDINATION:
- Checker is reviewing security and code quality
- Legal is checking compliance
- GitDude is reviewing version control safety
- Focus on USER VALUE and DEVELOPER EXPERIENCE
```

#### Teammate 4: GitDude

```
You are GitDude — Release Manager & Security Guardian.

READ FIRST:
- Your identity: AgenTeam/GitDude/GitDude_Identity.md
- Your knowledge: Library/Knowledge/GitDude/README.md
- CLAUDE.md is auto-loaded (shared protocols)

YOUR TASK:
Version control and security review of: [TARGET DESCRIPTION]

Files to review: [FILE PATHS]

DELIVERABLE:
Write to Dashboard/Work_Space/REVIEW_GitDude_[target].md

Include:
- **Security Scan**
  - Secrets detection (API keys, tokens, passwords, private keys)
  - .gitignore completeness check
  - .env files exposure check
  - Sensitive data patterns scan
- **Version Control Readiness**
  - Files ready for commit?
  - Changelog entry needed?
  - Version bump assessment (patch/minor/major)
  - Release notes draft
- **Pre-Commit Checklist**
  - Security scan passed?
  - License file present?
  - README updated?
  - No sensitive data in any file?
- **Verdict:** SAFE TO COMMIT / NEEDS CLEANUP / SECURITY RISK
  - If not safe: specific items to fix before committing

COORDINATION:
- Checker is reviewing code quality and security vulnerabilities
- Legal is checking compliance and licensing
- Gal is evaluating user experience
- Focus on VERSION CONTROL SAFETY and RELEASE READINESS
```

### Step 3: Synthesize Reviews

When all four finish, create a combined review:

```
=== REVIEW TEAM COMPLETE ===

TARGET: [what was reviewed]

CHECKER: [verdict]
  - [top 3 findings]
  Location: Dashboard/Work_Space/REVIEW_Checker_[target].md

LEGAL: [verdict]
  - [top 3 findings]
  Location: Dashboard/Work_Space/REVIEW_Legal_[target].md

GAL: [verdict]
  - [top 3 findings]
  Location: Dashboard/Work_Space/REVIEW_Gal_[target].md

GITDUDE: [verdict]
  - [top 3 findings]
  Location: Dashboard/Work_Space/REVIEW_GitDude_[target].md

COMBINED VERDICT: [SHIP / FIX THEN SHIP / HOLD]

CRITICAL ITEMS (must fix):
1. [item]
2. [item]

RECOMMENDED (should fix):
1. [item]
2. [item]

NEXT STEPS:
- [action items]
============================
```

### Step 4: Decision

Present the combined verdict to the user. The user (Pilot-in-Command) decides:
- **SHIP** — proceed to GitDude for version control
- **FIX** — hand back to Builder with the review items
- **HOLD** — more discussion needed

## Notes

- All four reviewers run in parallel (no dependencies between them)
- Each reviewer focuses on their domain — minimal overlap
- Skip Legal for pure code refactors or internal tools
- Skip Gal for backend-only changes with no user-facing impact
- The combined verdict is the Team Lead's synthesis — reviewers don't need to agree
- All reviews saved to `Dashboard/Work_Space/` for the team record
