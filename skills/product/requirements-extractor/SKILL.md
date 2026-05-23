---
name: requirements-extractor
description: Auto-activates when analyzing GitHub issues to extract functional requirements,
  non-functional requirements, acceptance criteria, and user stories.
allowed-tools: Read, Grep, Bash, gh
---

## Purpose

The **requirements-extractor** skill provides structured methods for parsing GitHub issues to extract and organize requirements information. It ensures that all requirements are properly identified, categorized, and documented in a format suitable for downstream design and implementation phases.

## When to Use

This skill auto-activates when you:
- Analyze GitHub issues for requirements
- Parse feature requests or bug reports
- Extract acceptance criteria from issue descriptions
- Identify user stories (As a... I want... So that...)
- Distinguish functional from non-functional requirements
- Clarify ambiguous or missing requirements

## Provided Capabilities

### 1. Requirement Identification
- **Functional Requirements**: What the system must do
- **Non-Functional Requirements**: Quality attributes (performance, security, usability, scalability)
- **Business Requirements**: Business goals and objectives
- **User Requirements**: User-facing capabilities
- **System Requirements**: Technical system capabilities

### 2. Acceptance Criteria Extraction
- Parse acceptance criteria from issue body
- Identify testable conditions
- Convert narratives to checkable criteria
- Flag missing or ambiguous criteria

### 3. User Story Parsing
- Identify user story format: "As a [role], I want [feature], so that [benefit]"
- Extract role, feature, and benefit components
- Parse epic stories vs. individual stories
- Link related stories

### 4. Requirement Categorization
- **Must Have** (P0): Critical for MVP
- **Should Have** (P1): Important but not critical
- **Could Have** (P2): Desirable but optional
- **Won't Have** (P3): Out of scope for this release

### 5. Requirement Validation
- Check for completeness using requirements-checklist.md
- Identify ambiguous language
- Flag conflicting requirements
- Ensure testability

## Usage Guide

### Step 1: Fetch Issue Content

```bash
gh issue view <issue-number> --json title,body,labels,comments --repo matteocervelli/llms
```

### Step 2: Parse Issue Structure

Look for these patterns in issue body:

**Functional Requirements Indicators**:
- "The system must..."
- "The feature should..."
- "Users can..."
- "When X happens, then Y..."

**Non-Functional Requirements Indicators**:
- "Response time..."
- "Must handle N concurrent users..."
- "Should be accessible to..."
- "Must comply with..."
- "Performance target..."

**Acceptance Criteria Indicators**:
- "Acceptance Criteria:"
- "Definition of Done:"
- Checklist items: `- [ ]`
- "Given... When... Then..." (BDD format)

**User Stories Indicators**:
- "As a..."
- "User persona..."
- "Use case..."

### Step 3: Extract Functional Requirements

Parse statements that describe **what** the system does:

```markdown
### Functional Requirements
1. **[FR-001]** User Authentication: System must authenticate users via email/password
2. **[FR-002]** Data Export: Users can export data to CSV, JSON, or PDF formats
3. **[FR-003]** Real-time Updates: System must push updates to clients within 5 seconds
```

**Naming Convention**: FR-XXX for functional requirements

### Step 4: Extract Non-Functional Requirements

Parse quality attributes:

```markdown
### Non-Functional Requirements

#### Performance
- **[NFR-P-001]** API response time must be < 200ms for 95th percentile
- **[NFR-P-002]** System must handle 1000 concurrent users

#### Security
- **[NFR-S-001]** All data transmission must use TLS 1.3+
- **[NFR-S-002]** Passwords must be hashed with bcrypt (cost factor ≥12)

#### Usability
- **[NFR-U-001]** UI must be WCAG 2.1 Level AA compliant
- **[NFR-U-002]** All actions must be reversible within 30 seconds

#### Scalability
- **[NFR-SC-001]** Architecture must support horizontal scaling
- **[NFR-SC-002]** Database must handle 10M+ records without degradation
```

**Naming Convention**: NFR-[Category]-XXX

### Step 5: Extract Acceptance Criteria

Convert issue acceptance criteria to structured format:

```markdown
### Acceptance Criteria

- [ ] **AC-001**: User can log in with valid credentials
  - Given valid email and password
  - When user submits login form
  - Then user is redirected to dashboard
  - And session token is created

- [ ] **AC-002**: Invalid login shows error message
  - Given invalid credentials
  - When user submits login form
  - Then error message displays: "Invalid email or password"
  - And user remains on login page
  - And login attempt is logged

- [ ] **AC-003**: Forgot password link is visible
  - Given user is on login page
  - When user views page
  - Then "Forgot Password?" link is visible
  - And link navigates to password reset flow
```

**Naming Convention**: AC-XXX for acceptance criteria

### Step 6: Parse User Stories

Extract user stories in standard format:

```markdown
### User Stories

**Story 1**: User Login
- **As a** registered user
- **I want to** log in with my email and password
- **So that** I can access my personalized dashboard
- **Priority**: Must Have (P0)
- **Acceptance Criteria**: AC-001, AC-002, AC-003

**Story 2**: Guest Browsing
- **As a** guest visitor
- **I want to** browse public content without logging in
- **So that** I can evaluate the platform before registering
- **Priority**: Should Have (P1)
- **Acceptance Criteria**: AC-004, AC-005
```

### Step 7: Categorize by Priority

Use MoSCoW method:

```markdown
### Requirement Priorities

#### Must Have (P0) - Critical for MVP
- FR-001: User Authentication
- FR-003: Real-time Updates
- NFR-S-001: TLS encryption

#### Should Have (P1) - Important
- FR-002: Data Export
- NFR-U-001: WCAG compliance

#### Could Have (P2) - Desirable
- FR-005: Dark mode support
- NFR-P-003: CDN integration

#### Won't Have (P3) - Out of scope
- FR-010: AI-powered recommendations (future release)
```

### Step 8: Validate Using Checklist

Use `requirements-checklist.md` to validate each requirement:

```bash
# Check against requirements checklist
# Manually verify each criterion from requirements-checklist.md
```

**Validation Criteria**:
- ✅ Clear and unambiguous
- ✅ Testable
- ✅ Complete
- ✅ Consistent (no conflicts)
- ✅ Traceable to business goals
- ✅ Feasible with available resources

### Step 9: Flag Issues

Identify and document:

```markdown
### Requirement Issues

**Ambiguous Requirements**:
- FR-007: "System should be fast" → Needs quantification (What is "fast"?)
- FR-012: "Easy to use" → Needs specific usability criteria

**Missing Requirements**:
- No error handling requirements specified for API failures
- Logging and monitoring requirements not defined
- Backup and recovery procedures not mentioned

**Conflicting Requirements**:
- FR-015 requires real-time sync, but NFR-P-005 sets 5-minute update interval
```

## Best Practices

### 1. Be Thorough
- Read entire issue including comments
- Check linked issues and PRs
- Review labels and milestones
- Look for implicit requirements

### 2. Use Standard Formats
- Consistent naming conventions
- Structured templates
- Clear categorization
- Numbered identifiers

### 3. Validate Completeness
- Every requirement has ID
- Every requirement is testable
- Every requirement has priority
- Every requirement traces to business goal

### 4. Handle Ambiguity
- Flag vague language
- Request clarification
- Document assumptions
- Provide examples

### 5. Consider Non-Obvious Requirements
- Error handling
- Logging and monitoring
- Performance under load
- Data migration needs
- Backward compatibility
- Accessibility
- Internationalization
- Privacy and compliance

## Resources

### requirements-checklist.md
Comprehensive checklist for validating requirements including:
- Completeness criteria
- Clarity criteria
- Consistency checks
- Testability validation
- Feasibility assessment

### extraction-patterns.md
Common patterns for identifying requirements in natural language:
- Keywords and phrases
- Sentence structures
- Issue templates
- Standard formats (BDD, user stories)

## Example Usage

### Input (GitHub Issue)
```
Title: Add user authentication feature

Description:
As a user, I want to log in with my email and password so that I can access my personal data.

The system should support:
- Email/password login
- "Remember me" option
- Forgot password flow
- Account lockout after 5 failed attempts

Acceptance Criteria:
- [ ] User can log in with valid credentials
- [ ] Invalid login shows error message
- [ ] Password reset email sent within 1 minute
- [ ] Locked accounts show appropriate message
```

### Output (Extracted Requirements)
```markdown
## Requirements

### Functional Requirements
1. **[FR-001]** Email/Password Authentication: System must authenticate users via email and password
2. **[FR-002]** Remember Me: System must provide "remember me" checkbox to maintain session
3. **[FR-003]** Password Reset: System must send password reset email when user requests
4. **[FR-004]** Account Lockout: System must lock account after 5 consecutive failed login attempts

### Non-Functional Requirements

#### Security
- **[NFR-S-001]** Password storage must use bcrypt hashing
- **[NFR-S-002]** Session tokens must expire after 24 hours (unless "remember me")
- **[NFR-S-003]** Login attempts must be rate-limited (max 10/hour per IP)

#### Performance
- **[NFR-P-001]** Password reset email must be sent within 1 minute
- **[NFR-P-002]** Login response time must be < 500ms

#### Usability
- **[NFR-U-001]** Error messages must not reveal whether email exists
- **[NFR-U-002]** Locked account message must provide unlock instructions

### Acceptance Criteria
- [ ] **AC-001**: User can log in with valid email/password
- [ ] **AC-002**: Invalid login shows generic error message
- [ ] **AC-003**: Password reset email sent within 1 minute of request
- [ ] **AC-004**: Account locked after 5 failed attempts with clear message
- [ ] **AC-005**: "Remember me" extends session to 30 days

### User Stories
**Story 1**: User Login
- **As a** registered user
- **I want to** log in with email and password
- **So that** I can access my personal data
- **Priority**: Must Have (P0)
```

## Integration

This skill is used by:
- **analysis-specialist** agent during Phase 1: Requirements Analysis
- Activates automatically when agent analyzes GitHub issues
- Provides structured output for analysis document generation

---

**Version**: 2.0.0
**Auto-Activation**: Yes (when extracting requirements)
**Phase**: 1 (Requirements Analysis)
**Created**: 2025-10-29