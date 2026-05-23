---
name: decompose
description: Break a goal into subgoals, constraints, and acceptance criteria. Use when planning complex work, creating work breakdown structures, or defining requirements.
argument-hint: "[goal] [depth] [constraints]"
disable-model-invocation: false
user-invocable: true
allowed-tools: Read, Grep
context: fork
agent: explore
---

## Intent

Break down a complex goal into smaller, manageable subgoals with clear boundaries, dependencies, and acceptance criteria. Enable parallel work and incremental progress.

**Success criteria:**
- Goal fully decomposed (no gaps)
- Subgoals are independently verifiable
- Dependencies are explicit
- Acceptance criteria are testable
- Decomposition depth is appropriate

**Compatible schemas:**
- `schemas/output_schema.yaml`

## Inputs

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| `goal` | Yes | string or object | The goal to decompose |
| `depth` | No | integer | Maximum decomposition depth (default: 3) |
| `constraints` | No | object | Boundaries, limitations, scope |
| `granularity` | No | string | Target size: epic, story, task (default: story) |
| `context` | No | object | Background information |

## Procedure

1) **Understand the goal**: Clarify what needs to be achieved
   - Parse the goal statement
   - Identify success criteria
   - Note implicit requirements
   - Determine scope boundaries

2) **Identify major components**: Find natural divisions
   - Functional areas
   - Phases or stages
   - User journeys
   - Technical layers

3) **Create subgoals**: Define each component
   - Clear, specific objective
   - Bounded scope
   - Measurable outcome
   - Independent when possible

4) **Define dependencies**: Map relationships
   - Which subgoals block others?
   - Which can proceed in parallel?
   - Are there shared resources?
   - Create dependency graph

5) **Add acceptance criteria**: Specify done conditions
   - Testable conditions
   - Measurable outcomes
   - Quality requirements
   - Edge case handling

6) **Validate completeness**: Check coverage
   - Do subgoals cover entire goal?
   - Any gaps or overlaps?
   - Are boundaries clear?
   - Is granularity consistent?

7) **Recurse if needed**: Decompose large subgoals
   - Check against target granularity
   - Decompose subgoals that are too large
   - Maintain consistent depth
   - Stop when atomic enough

## Output Contract

Return a structured object:

```yaml
decomposition:
  goal: string  # Original goal
  depth: integer  # Levels of decomposition
  total_subgoals: integer
  granularity: epic | story | task
subgoals:
  - id: string
    name: string
    description: string
    parent: string | null  # Parent subgoal ID
    level: integer  # Depth in tree
    dependencies: array[string]
    acceptance_criteria:
      - criterion: string
        testable: boolean
        priority: required | optional
    estimated_effort: string | null
    parallelizable: boolean
hierarchy:
  - id: string
    name: string
    children: array  # Nested subgoals
constraints:
  - type: scope | time | resource | technical
    description: string
    affects: array[string]  # Subgoal IDs
gaps:
  - description: string
    suggestion: string
overlaps:
  - subgoals: array[string]
    description: string
    resolution: string
confidence: 0..1
evidence_anchors: ["source:ref"]
assumptions: []
```

### Field Definitions

| Field | Type | Description |
|-------|------|-------------|
| `decomposition` | object | Summary of decomposition |
| `subgoals` | array | Flat list of all subgoals |
| `hierarchy` | array | Tree structure of subgoals |
| `constraints` | array | Boundaries affecting subgoals |
| `gaps` | array | Missing coverage identified |
| `overlaps` | array | Redundant coverage identified |
| `confidence` | number | 0.0-1.0 based on completeness |

## Examples

### Example 1: Feature Decomposition

**Input:**
```yaml
goal: "Implement user authentication system"
granularity: story
constraints:
  scope: "Web application only"
  timeline: "4 weeks"
```

**Output:**
```yaml
decomposition:
  goal: "Implement user authentication system"
  depth: 2
  total_subgoals: 8
  granularity: story
subgoals:
  - id: "SG-1"
    name: "User Registration"
    description: "Allow new users to create accounts"
    parent: null
    level: 1
    dependencies: []
    acceptance_criteria:
      - criterion: "User can register with email and password"
        testable: true
        priority: required
      - criterion: "Email verification sent on registration"
        testable: true
        priority: required
      - criterion: "Duplicate email rejected with clear message"
        testable: true
        priority: required
    estimated_effort: "3d"
    parallelizable: true
  - id: "SG-2"
    name: "User Login"
    description: "Allow existing users to authenticate"
    parent: null
    level: 1
    dependencies: ["SG-1"]
    acceptance_criteria:
      - criterion: "User can login with email and password"
        testable: true
        priority: required
      - criterion: "Failed login shows error without revealing which field wrong"
        testable: true
        priority: required
      - criterion: "Session created on successful login"
        testable: true
        priority: required
    estimated_effort: "2d"
    parallelizable: false
  - id: "SG-3"
    name: "Password Reset"
    description: "Allow users to recover account access"
    parent: null
    level: 1
    dependencies: ["SG-1"]
    acceptance_criteria:
      - criterion: "User can request password reset via email"
        testable: true
        priority: required
      - criterion: "Reset link expires after 24 hours"
        testable: true
        priority: required
      - criterion: "New password must meet complexity requirements"
        testable: true
        priority: required
    estimated_effort: "2d"
    parallelizable: true
  - id: "SG-4"
    name: "Session Management"
    description: "Manage user sessions securely"
    parent: null
    level: 1
    dependencies: ["SG-2"]
    acceptance_criteria:
      - criterion: "Sessions expire after 24 hours of inactivity"
        testable: true
        priority: required
      - criterion: "User can logout, invalidating session"
        testable: true
        priority: required
      - criterion: "Multiple sessions per user supported"
        testable: true
        priority: optional
    estimated_effort: "2d"
    parallelizable: false
  - id: "SG-5"
    name: "OAuth2 Integration"
    description: "Allow login via Google/GitHub"
    parent: null
    level: 1
    dependencies: ["SG-2"]
    acceptance_criteria:
      - criterion: "User can login via Google OAuth"
        testable: true
        priority: required
      - criterion: "User can login via GitHub OAuth"
        testable: true
        priority: required
      - criterion: "OAuth user linked to existing account if email matches"
        testable: true
        priority: required
    estimated_effort: "3d"
    parallelizable: true
  - id: "SG-6"
    name: "Rate Limiting"
    description: "Prevent brute force attacks"
    parent: null
    level: 1
    dependencies: ["SG-2"]
    acceptance_criteria:
      - criterion: "Max 5 failed login attempts per 15 minutes per IP"
        testable: true
        priority: required
      - criterion: "CAPTCHA shown after 3 failed attempts"
        testable: true
        priority: required
    estimated_effort: "1d"
    parallelizable: true
  - id: "SG-7"
    name: "Security Audit Logging"
    description: "Log all auth events for audit"
    parent: null
    level: 1
    dependencies: ["SG-2"]
    acceptance_criteria:
      - criterion: "All login attempts logged with timestamp and IP"
        testable: true
        priority: required
      - criterion: "Password changes logged"
        testable: true
        priority: required
      - criterion: "Logs retained for 90 days"
        testable: true
        priority: required
    estimated_effort: "1d"
    parallelizable: true
  - id: "SG-8"
    name: "Two-Factor Authentication"
    description: "Add optional 2FA for users"
    parent: null
    level: 1
    dependencies: ["SG-2", "SG-4"]
    acceptance_criteria:
      - criterion: "User can enable TOTP-based 2FA"
        testable: true
        priority: required
      - criterion: "Recovery codes provided on 2FA setup"
        testable: true
        priority: required
      - criterion: "2FA prompt on login when enabled"
        testable: true
        priority: required
    estimated_effort: "3d"
    parallelizable: false
hierarchy:
  - id: "SG-1"
    name: "User Registration"
    children: []
  - id: "SG-2"
    name: "User Login"
    children: []
  - id: "SG-3"
    name: "Password Reset"
    children: []
  - id: "SG-4"
    name: "Session Management"
    children: []
  - id: "SG-5"
    name: "OAuth2 Integration"
    children: []
  - id: "SG-6"
    name: "Rate Limiting"
    children: []
  - id: "SG-7"
    name: "Security Audit Logging"
    children: []
  - id: "SG-8"
    name: "Two-Factor Authentication"
    children: []
constraints:
  - type: scope
    description: "Web application only, no mobile"
    affects: ["SG-1", "SG-2", "SG-5"]
  - type: time
    description: "4 week timeline"
    affects: ["SG-8"]
gaps: []
overlaps: []
confidence: 0.9
evidence_anchors:
  - "requirement:auth-system"
assumptions:
  - "Email service available for verification"
  - "OAuth provider apps already created"
  - "No existing user database to migrate"
```

**Evidence pattern:** Each subgoal has testable acceptance criteria, dependencies mapped.

## Verification

- [ ] All aspects of goal covered
- [ ] No gaps in coverage
- [ ] No significant overlaps
- [ ] Acceptance criteria testable
- [ ] Dependencies form valid DAG

**Verification tools:** Read (for requirement analysis)

## Safety Constraints

- `mutation`: false
- `requires_checkpoint`: false
- `requires_approval`: false
- `risk`: low

**Capability-specific rules:**
- Always verify completeness
- Flag gaps explicitly
- Resolve overlaps
- Ensure acceptance criteria are testable
- Note assumptions that affect decomposition

## Composition Patterns

**Commonly follows:**
- `retrieve` - Gather requirements
- `inspect` - Understand existing system
- `explain` - Clarify goal before decomposing

**Commonly precedes:**
- `plan` - Plan decomposed subgoals (REQUIRED by plan)
- `prioritize` - Order subgoals
- `schedule` - Time-order subgoals
- `delegate` - Assign subgoals

**Anti-patterns:**
- Never decompose without understanding goal
- Never leave gaps unidentified
- Never skip acceptance criteria

**Workflow references:**
- See `reference/composition_patterns.md` for plan requiring decompose
