---
name: consensus-voting
version: 1.0.0
description: Multi-agent consensus voting with domain-weighted expertise for critical decisions requiring structured validation
auto_activates:
  - "security implementation"
  - "authentication change"
  - "authorization logic"
  - "data handling"
  - "encryption"
  - "sensitive data"
  - "critical algorithm"
explicit_triggers:
  - /amplihack:consensus-vote
confirmation_required: false
token_budget: 2500
---

# Consensus Voting Skill

## Purpose

Execute weighted multi-agent voting for critical decisions where domain expertise matters. Unlike debate (collaborative synthesis) or n-version (parallel generation), this skill focuses on **structured voting with expertise weighting** for security, authentication, and data-handling changes.

## Key Insight from Pattern Analysis

From `.claude/context/DISCOVERIES.md` (Pattern Applicability Analysis):

> **Voting vs Expert Judgment Selection Criteria**
>
> **When Voting Works:**
>
> - Adversarial environment (can't trust individual nodes)
> - Binary or simple discrete choices
> - No objective quality metric available
> - Consensus more valuable than correctness
>
> **When Expert Judgment Works:**
>
> - Cooperative environment (honest actors)
> - Complex quality dimensions
> - Objective evaluation criteria exist
> - Correctness more valuable than consensus

**This skill uses BOTH strategically**: Expert judgment to evaluate, weighted voting to decide.

## When to Use This Skill

**AUTO-TRIGGERS (high-risk domains):**

- Security implementations (authentication, authorization)
- Encryption and cryptographic code
- Sensitive data handling (PII, credentials)
- Permission and access control changes
- Critical algorithm implementations

**EXPLICIT TRIGGERS:**

- Major design decisions with competing approaches
- When stakeholder buy-in matters
- Binary or discrete choices needing validation
- Risk-mitigating decisions for production code

**AVOID FOR:**

- Complex trade-off analysis (use `debate-workflow` instead)
- Code generation (use `n-version-workflow` instead)
- Simple implementation choices
- Subjective quality assessments

## Configuration

### Voting Configuration

**Voting Mode:**

- `simple-majority` - 50%+ votes to pass
- `supermajority` - 66%+ votes to pass (DEFAULT for security)
- `unanimous` - 100% agreement required

**Agent Selection:**

- `auto` - Select agents based on detected domain (DEFAULT)
- `manual` - Specify agents explicitly
- `comprehensive` - All relevant agents vote

**Weight Calibration:**

- `static` - Fixed weights per domain (DEFAULT)

### Domain Expertise Weights

| Agent     | Security | Auth | Data | Algorithm | General |
| --------- | -------- | ---- | ---- | --------- | ------- |
| security  | 3.0      | 2.5  | 2.5  | 1.5       | 1.0     |
| reviewer  | 1.5      | 1.5  | 1.5  | 2.0       | 2.0     |
| architect | 1.5      | 2.0  | 2.0  | 2.5       | 2.0     |
| tester    | 1.0      | 1.5  | 1.5  | 2.0       | 1.5     |
| optimizer | 0.5      | 0.5  | 0.5  | 2.5       | 1.0     |
| cleanup   | 0.5      | 0.5  | 0.5  | 1.0       | 1.5     |

**Weight Interpretation:**

- 3.0 = Domain expert (vote counts triple)
- 2.0 = Significant expertise (vote counts double)
- 1.0 = General competence (standard vote)
- 0.5 = Peripheral relevance (half vote)

## Execution Process

### Step 1: Detect Decision Domain

Analyze the change or decision to determine primary domain:

- **Use analyzer agent** to examine code/proposal
- Detect keywords: auth, encrypt, password, token, permission, credential
- Identify file paths: auth/, security/, crypto/
- Classify: SECURITY | AUTH | DATA | ALGORITHM | GENERAL

**Domain Detection Triggers:**

```
SECURITY: encrypt, decrypt, hash, salt, vulnerability, CVE, injection
AUTH: login, logout, session, token, jwt, oauth, password, credential
DATA: pii, gdpr, sensitive, personal, private, secret, key
ALGORITHM: sort, search, calculate, compute, process, transform
```

### Step 2: Select Voting Agents

Based on detected domain, select relevant agents with weights:

**For SECURITY domain:**

- security agent (weight: 3.0) - Primary expert
- architect agent (weight: 1.5) - System design perspective
- reviewer agent (weight: 1.5) - Code quality check
- tester agent (weight: 1.0) - Testability assessment

**For AUTH domain:**

- security agent (weight: 2.5) - Security implications
- architect agent (weight: 2.0) - Integration patterns
- reviewer agent (weight: 1.5) - Implementation quality
- tester agent (weight: 1.5) - Auth flow testing

**For DATA domain:**

- security agent (weight: 2.5) - Data protection
- architect agent (weight: 2.0) - Data architecture
- reviewer agent (weight: 1.5) - Handling patterns
- tester agent (weight: 1.5) - Data validation

**For ALGORITHM domain:**

- optimizer agent (weight: 2.5) - Performance analysis
- architect agent (weight: 2.5) - Design patterns
- tester agent (weight: 2.0) - Correctness testing
- reviewer agent (weight: 2.0) - Code quality

### Step 3: Present Decision to Agents

Each selected agent receives:

- Clear decision statement
- Available options (if applicable)
- Relevant context and constraints
- Evaluation criteria

**Decision Prompt Template:**

```markdown
## Decision Required: [TITLE]

**Domain:** [SECURITY | AUTH | DATA | ALGORITHM]
**Your Weight:** [X.X] (based on domain expertise)

### Context

[Relevant background and constraints]

### Options

1. [Option A]: [Description]
2. [Option B]: [Description]
3. [Reject Both]: Propose alternative

### Evaluation Criteria

- Security implications
- Implementation complexity
- Maintainability
- Risk assessment

### Your Vote

Provide:

1. Your vote (Option 1, 2, or Reject)
2. Confidence level (HIGH, MEDIUM, LOW)
3. Key reasoning (2-3 sentences max)
4. Any conditions or caveats
```

### Step 4: Collect Votes

For each agent, collect structured vote:

```yaml
agent: security
weight: 3.0
vote: Option 1
confidence: HIGH
reasoning: "Option 1 follows OWASP best practices for credential storage. Option 2 uses deprecated hashing algorithm."
conditions: ["Ensure salt length >= 16 bytes", "Use constant-time comparison"]
```

### Step 5: Calculate Weighted Result

**Weighted Vote Calculation:**

```
For each option:
  weighted_score = sum(agent_weight * confidence_multiplier)

Where confidence_multiplier:
  HIGH = 1.0
  MEDIUM = 0.7
  LOW = 0.4
```

**Example Calculation:**

| Agent     | Weight | Vote | Confidence | Score |
| --------- | ------ | ---- | ---------- | ----- |
| security  | 3.0    | A    | HIGH       | 3.0   |
| architect | 1.5    | A    | MEDIUM     | 1.05  |
| reviewer  | 1.5    | B    | HIGH       | 1.5   |
| tester    | 1.0    | A    | LOW        | 0.4   |

```
Option A Score: 3.0 + 1.05 + 0.4 = 4.45
Option B Score: 1.5
Total Weighted Votes: 5.95
Option A Percentage: 74.8% (SUPERMAJORITY)
```

### Step 6: Apply Voting Threshold

Based on configured voting mode:

**simple-majority (50%+):**

- Option with highest weighted score wins if > 50%
- If no option > 50%, proceed to debate or reject

**supermajority (66%+):** (DEFAULT for security)

- Winning option must have > 66% weighted votes
- Provides stronger validation for high-risk decisions

**unanimous (100%):**

- All agents must agree (rare, highest bar)
- Any dissent blocks decision

### Step 7: Report Consensus Result

**If Consensus Reached:**

```markdown
## Consensus Voting Result

**Decision:** [Selected Option]
**Domain:** SECURITY
**Threshold:** Supermajority (66%+)
**Result:** PASSED (74.8%)

### Vote Summary

| Agent     | Weight | Vote | Confidence |
| --------- | ------ | ---- | ---------- |
| security  | 3.0    | A    | HIGH       |
| architect | 1.5    | A    | MEDIUM     |
| reviewer  | 1.5    | B    | HIGH       |
| tester    | 1.0    | A    | LOW        |

### Key Reasoning (from highest-weighted agents)

- **security (3.0):** "Option 1 follows OWASP best practices..."

### Conditions/Caveats

- Ensure salt length >= 16 bytes
- Use constant-time comparison

### Dissenting View

- **reviewer (1.5):** "Option B has simpler implementation..."
```

**If No Consensus:**

```markdown
## Consensus Voting Result

**Decision:** NO CONSENSUS
**Domain:** AUTH
**Threshold:** Supermajority (66%+)
**Result:** FAILED (52.3%)

### Recommendation

- Escalate to `/amplihack:debate` for structured trade-off analysis
- OR: Gather more information and re-vote
- OR: Accept simple majority with documented risk
```

### Step 8: Record Decision

- Log voting result to session decisions
- Document vote reasoning for future reference

## Trade-Offs

**Benefits:**

- Structured decision-making for high-risk domains
- Domain expertise appropriately weighted
- Clear audit trail with reasoning
- Faster than full debate for binary/discrete choices

**Costs:**

- Less nuanced than debate (no synthesis)
- Requires clear options (not generative)
- Weight calibration needs real data
- May miss creative alternatives

**Use When:** Decision is discrete, domain expertise matters, audit trail needed

## Examples

### Example 1: Password Hashing Implementation

**Context:** Choosing between bcrypt, argon2id, and PBKDF2 for new auth system

**Domain Detection:** AUTH (password, hash)

**Agents Selected:**

- security (2.5), architect (2.0), reviewer (1.5), tester (1.5)

**Votes:**

- security: argon2id (HIGH) - "OWASP current recommendation, memory-hard"
- architect: argon2id (MEDIUM) - "Good library support, modern design"
- reviewer: bcrypt (HIGH) - "More battle-tested in production"
- tester: argon2id (MEDIUM) - "Easier to test with configurable params"

**Result:** argon2id wins with 68.2% (supermajority passed)

### Example 2: API Rate Limiting Approach

**Context:** Token bucket vs sliding window vs fixed window

**Domain Detection:** SECURITY (rate limit, protection)

**Agents Selected:**

- security (3.0), optimizer (1.5), architect (1.5), reviewer (1.5)

**Votes:**

- security: token bucket (HIGH) - "Best protection against burst attacks"
- optimizer: sliding window (MEDIUM) - "Better resource utilization"
- architect: token bucket (MEDIUM) - "Industry standard, well-understood"
- reviewer: sliding window (LOW) - "Simpler implementation"

**Result:** token bucket wins with 69.4% (supermajority passed)

### Example 3: No Consensus Scenario

**Context:** Microservices vs monolith for new feature

**Domain Detection:** ALGORITHM (general architecture)

**Agents Selected:**

- architect (2.5), optimizer (2.5), reviewer (2.0), tester (2.0)

**Votes:**

- architect: microservices (MEDIUM) - "Better long-term scalability"
- optimizer: monolith (HIGH) - "Simpler operations, less overhead"
- reviewer: monolith (MEDIUM) - "Easier to maintain initially"
- tester: microservices (LOW) - "Harder to test but more isolated"

**Result:** No consensus (52.1%) - Escalate to `/amplihack:debate`

## Integration with Other Workflows

### Handoff to Debate

When voting fails to reach consensus:

1. Document vote results and reasoning
2. Invoke `Skill(debate-workflow)` with vote context
3. Use voting insights to frame debate perspectives

### After N-Version Implementation

Use consensus voting to select between N-version implementations:

1. N-version generates 3+ implementations
2. Consensus voting selects winner
3. Domain experts have weighted influence on selection

### Philosophy Alignment

This skill enforces:

- **Evidence-Based Decisions:** Votes require reasoning
- **Domain Expertise:** Weights reflect competence
- **Transparent Trade-offs:** Dissent documented
- **Audit Trail:** Full voting record preserved
- **Appropriate Rigor:** Auto-triggers for high-risk domains
