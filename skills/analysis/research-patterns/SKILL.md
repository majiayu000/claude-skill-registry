---
name: research-patterns
type: knowledge
description: Research methodology and best practices for finding existing patterns
keywords: research, investigate, pattern, best practice, design, architecture, how should i, what's the best
auto_activate: true
---

# Research Patterns Skill

**Purpose**: Provide methodology and guidelines for researching existing patterns before implementing new features.

**Auto-activates when**: Keywords like "research", "investigate", "design", "architecture", "best practice" appear in conversation.

---

## Research Methodology

### 1. Define Clear Research Question

**Before starting research**:

```markdown
❓ **Research Question Template**:

- What: {What are we trying to build?}
- Why: {Why do we need it?}
- Scope: {What's in scope? What's out of scope?}
- Success: {What would a good solution look like?}
```

**Example**:

```markdown
What: Webhook handling system for receiving external events
Why: Need to integrate with 3rd-party services that push updates
Scope: IN - signature verification, retry logic, async processing
OUT - webhook delivery (we're receiving, not sending)
Success: Secure, reliable, handles 1000+ webhooks/min
```

### 2. Search Existing Codebase First

**Always search internal patterns before external research.**

**Codebase Search Checklist**:

```markdown
□ Grep for relevant keywords (functionality, domain terms)
□ Glob for related files (naming patterns)
□ Read existing implementations (understand current patterns)
□ Check docs/ for existing architecture decisions
□ Review tests/ to understand current test patterns
```

**Common Search Patterns**:

| Goal                | Grep Pattern                           | Glob Pattern                         |
| ------------------- | -------------------------------------- | ------------------------------------ |
| Find authentication | `"auth"`, `"login"`, `"token"`         | `**/*auth*.py`                       |
| Find caching        | `"cache"`, `"memoize"`, `"@lru_cache"` | `**/*cache*.py`                      |
| Find webhooks       | `"webhook"`, `"callback"`, `"event"`   | `**/*webhook*.py`, `**/*event*.py`   |
| Find error handling | `"try:", "except", "raise"`            | `**/*error*.py`, `**/*exception*.py` |

**Decision Tree**:

```
Found existing pattern?
├─ YES → Reuse/extend existing pattern
│         (Don't reinvent the wheel!)
│
└─ NO → Proceed with external research
        (Need to find industry best practices)
```

### 3. External Web Research

**When codebase search yields nothing, research externally.**

**WebSearch Query Strategy**:

#### Query Pattern Templates

**For Best Practices**:

```
"{topic} best practices {current_year}"
"{topic} design patterns {current_year}"
"{topic} common mistakes to avoid"
"{topic} anti-patterns"
```

**For Implementation Guidance**:

```
"{topic} {language} implementation"
"{topic} code examples GitHub"
"{topic} library comparison"
"{topic} step-by-step tutorial"
```

**For Security-Sensitive Topics**:

```
"{topic} security best practices"
"{topic} OWASP guidelines"
"{topic} secure implementation"
"{topic} vulnerability checklist"
```

**For Performance-Critical Topics**:

```
"{topic} performance optimization"
"{topic} scalability patterns"
"{topic} benchmarking"
"{topic} profiling and tuning"
```

**For Architecture Decisions**:

```
"{topic} architecture patterns"
"{topic} system design"
"{topic} microservices vs monolith"
"{topic} when to use"
```

#### Optimal Query Count

- **Minimum**: 3 queries (different angles on same topic)
- **Recommended**: 5 queries (comprehensive coverage)
- **Maximum**: 7 queries (diminishing returns after this)

**Example Research Plan**:

```markdown
Topic: "distributed caching for ML models"

Query 1: "distributed caching best practices 2025"
Query 2: "distributed caching Python Redis examples"
Query 3: "ML model caching strategies"
Query 4: "caching invalidation patterns"
Query 5: "Redis vs Memcached performance comparison"
```

### 4. Source Quality Evaluation

**Not all sources are created equal. Prioritize quality over quantity.**

#### Source Hierarchy (Highest to Lowest)

| Rank | Source Type            | Trust Level | Example                                         |
| ---- | ---------------------- | ----------- | ----------------------------------------------- |
| 1    | Official documentation | ⭐⭐⭐⭐⭐  | Python.org, FastAPI docs, [FRAMEWORK] docs      |
| 2    | Official repositories  | ⭐⭐⭐⭐⭐  | GitHub: pytorch/pytorch, ml-explore/[framework] |
| 3    | Well-known tech blogs  | ⭐⭐⭐⭐    | Martin Fowler, Real Python, Uber Engineering    |
| 4    | GitHub examples        | ⭐⭐⭐⭐    | Popular repos with stars, active maintenance    |
| 5    | Technical whitepapers  | ⭐⭐⭐⭐    | Google, Meta, academic papers                   |
| 6    | Stack Overflow         | ⭐⭐⭐      | Accepted answers, high votes                    |
| 7    | Blog posts             | ⭐⭐⭐      | Individual developers (verify credibility)      |
| 8    | Forum discussions      | ⭐⭐        | Reddit, HN (good for trends, not authority)     |
| 9    | Unverified tutorials   | ⭐          | Medium posts, personal blogs (verify carefully) |

#### Recency Scoring

| Year  | Score      | When to Use                          |
| ----- | ---------- | ------------------------------------ |
| 2025  | ⭐⭐⭐⭐⭐ | Cutting edge, latest practices       |
| 2024  | ⭐⭐⭐⭐⭐ | Recent, highly relevant              |
| 2023  | ⭐⭐⭐⭐   | Still current for most topics        |
| 2022  | ⭐⭐⭐     | Acceptable for stable topics         |
| 2021  | ⭐⭐       | Use only if nothing recent available |
| ≤2020 | ⭐         | Avoid unless foundational concepts   |

**Exceptions** (where older sources are acceptable):

- Fundamental algorithms (sorting, graphs, etc.)
- Established design patterns (Gang of Four patterns)
- Mathematical foundations
- Core Python language features (pre-3.11)

#### Content Quality Scoring

**Award points for**:

- ✅ Multiple code examples (+2)
- ✅ Pros and cons comparison (+2)
- ✅ Performance benchmarks (+1)
- ✅ Security considerations (+1)
- ✅ Edge cases documented (+1)
- ✅ Testing examples (+1)
- ✅ Production experience shared (+1)

**Deduct points for**:

- ❌ Theory only, no code (-2)
- ❌ Incomplete examples (-1)
- ❌ No error handling shown (-1)
- ❌ Conflicting advice (-1)
- ❌ Obvious mistakes in code (-2)

**Overall Quality Formula**:

```
Quality = (Authority × 0.3) + (Recency × 0.25) + (Content × 0.2) + (Depth × 0.15) + (Confirmation × 0.1)
```

### 5. Distill Into Actionable Findings

**Transform research into implementation-ready guidance.**

#### Required Sections in Findings

**1. Executive Summary** (2-3 sentences)

- What's the recommended approach?
- Why is it best for our use case?
- What's the expected effort?

**2. Pattern Analysis**

- **Recommended Approach**: Detailed description + code example
- **Alternatives Considered**: At least 2 alternatives with pros/cons
- **Tradeoffs**: Comparison table

**3. Implementation Guide**

- **Step-by-Step**: Numbered steps with code examples
- **Integration Points**: Where in our codebase this fits
- **Dependencies**: Libraries, tools, infrastructure needed

**4. Pitfalls to Avoid**

- **Common Mistakes**: What developers often get wrong
- **Edge Cases**: Scenarios that need special handling
- **Security Considerations**: Vulnerabilities to prevent
- **Performance Issues**: Bottlenecks to avoid

**5. Source Evaluation**

- Table of all sources with quality ratings
- Notes on why each source was useful/not useful

**6. Next Steps**

- Recommended actions
- Files to create/modify
- Tests to write

---

## Pattern Recognition Framework

### Common Software Patterns

#### 1. Authentication/Authorization

**Research Focus**:

- OAuth 2.0 vs JWT vs API keys
- Session management
- Token refresh strategies
- RBAC vs ABAC

**Key Questions**:

- How are credentials stored securely?
- How is token expiration handled?
- What's the logout flow?
- How to handle concurrent sessions?

**Security Musts**:

- Password hashing (bcrypt, argon2)
- HTTPS only
- CSRF protection
- Rate limiting

#### 2. Caching

**Research Focus**:

- Cache invalidation strategies
- Cache eviction policies (LRU, LFU, TTL)
- Distributed vs local caching
- Cache coherence

**Key Questions**:

- What's the cache hit ratio target?
- How to handle cache misses?
- When to invalidate?
- How to prevent cache stampede?

**Common Patterns**:

- Write-through cache
- Write-behind cache
- Cache-aside
- Read-through cache

#### 3. Webhooks/Event Processing

**Research Focus**:

- Signature verification
- Retry logic and exponential backoff
- Idempotency
- Async vs sync processing

**Key Questions**:

- How to verify webhook authenticity?
- What happens if processing fails?
- How to prevent duplicate processing?
- How to handle order of events?

**Security Musts**:

- HMAC signature verification
- IP whitelisting (if applicable)
- Request validation
- Rate limiting

#### 4. API Design

**Research Focus**:

- REST vs GraphQL vs gRPC
- Versioning strategies
- Error response formats
- Pagination approaches

**Key Questions**:

- How to handle breaking changes?
- What's the rate limiting strategy?
- How to document the API?
- How to test the API?

**Best Practices**:

- Semantic versioning
- OpenAPI/Swagger docs
- Consistent error formats
- HATEOAS (if REST)

#### 5. Data Processing Pipelines

**Research Focus**:

- ETL vs ELT
- Batch vs stream processing
- Error handling and retries
- Monitoring and alerting

**Key Questions**:

- How to handle partial failures?
- How to ensure data quality?
- How to scale processing?
- How to monitor pipeline health?

**Common Tools**:

- Apache Airflow (batch)
- Apache Kafka (streaming)
- dbt (data transformation)
- Prefect (orchestration)

#### 6. Testing Strategies

**Research Focus**:

- Unit vs integration vs E2E tests
- Test data management
- Mocking strategies
- Coverage targets

**Key Questions**:

- What's the right test pyramid?
- How to test external dependencies?
- How to test async code?
- How to ensure tests are fast?

**Best Practices**:

- Arrange-Act-Assert pattern
- Given-When-Then (BDD)
- Test isolation
- Fast feedback loops

---

## Research Output Templates

### Template 1: Pattern Comparison

Use when comparing multiple approaches (e.g., "Redis vs Memcached"):

````markdown
# Comparison: {Option A} vs {Option B} vs {Option C}

## Quick Recommendation

**Use {Option A}** if: {scenario}
**Use {Option B}** if: {scenario}
**Use {Option C}** if: {scenario}

## Detailed Comparison

| Criterion       | Option A         | Option B         | Option C         |
| --------------- | ---------------- | ---------------- | ---------------- |
| **Performance** | {rating + notes} | {rating + notes} | {rating + notes} |
| **Complexity**  | {rating + notes} | {rating + notes} | {rating + notes} |
| **Scalability** | {rating + notes} | {rating + notes} | {rating + notes} |
| **Maintenance** | {rating + notes} | {rating + notes} | {rating + notes} |
| **Community**   | {rating + notes} | {rating + notes} | {rating + notes} |
| **Cost**        | {rating + notes} | {rating + notes} | {rating + notes} |

## Code Examples

### Option A

```python
# Example implementation
```
````

### Option B

```python
# Example implementation
```

### Option C

```python
# Example implementation
```

## Decision Matrix

**For our use case** (insert our specific requirements):

| Requirement | Option A | Option B | Option C |
| ----------- | -------- | -------- | -------- |
| Req 1       | ✅       | ❌       | ✅       |
| Req 2       | ✅       | ✅       | ❌       |
| Req 3       | ❌       | ✅       | ✅       |

**Winner**: {Option} because {reasoning}

````

### Template 2: Implementation Pattern

Use when researching how to implement a feature (e.g., "webhook handling"):

```markdown
# Implementation Pattern: {Feature Name}

## Pattern Overview

**Name**: {Pattern name}
**Category**: {Architectural pattern category}
**Use When**: {Scenarios where this pattern applies}

## Architecture Diagram

````

[Simple ASCII diagram or description]
Component A → Component B → Component C

````

## Step-by-Step Implementation

### Step 1: {First step name}

**What**: {What this step does}
**Why**: {Why it's necessary}

```python
# Code for step 1
````

**Testing**:

```python
# Test for step 1
```

### Step 2: {Second step name}

**What**: {What this step does}
**Why**: {Why it's necessary}

```python
# Code for step 2
```

**Testing**:

```python
# Test for step 2
```

[Continue for all steps...]

## Integration Example

**How it fits into our codebase**:

```python
# Example showing integration with existing code
```

## Configuration

**Environment variables**:

```bash
FEATURE_API_KEY=xxx
FEATURE_TIMEOUT=30
```

**Config file** (`config.yaml`):

```yaml
feature:
  enabled: true
  timeout: 30
  retry_attempts: 3
```

## Error Handling

**Common errors and solutions**:

1. **Error**: {Error description}
   - **Cause**: {Why it happens}
   - **Solution**: {How to fix}
   - **Prevention**: {How to avoid}

2. **Error**: {Error description}
   - **Cause**: {Why it happens}
   - **Solution**: {How to fix}
   - **Prevention**: {How to avoid}

## Monitoring

**Metrics to track**:

- {Metric 1}: {Description + target value}
- {Metric 2}: {Description + target value}
- {Metric 3}: {Description + target value}

**Alerts to set up**:

- {Alert 1}: {Trigger condition}
- {Alert 2}: {Trigger condition}

## Testing Strategy

**Unit tests**:

- Test {functionality A}
- Test {functionality B}

**Integration tests**:

- Test {workflow A}
- Test {workflow B}

**Security tests**:

- Test {attack vector A}
- Test {attack vector B}

````

### Template 3: Security Analysis

Use when researching security-sensitive features:

```markdown
# Security Analysis: {Feature Name}

## Threat Model

### Assets
- {Asset 1}: {Description + value}
- {Asset 2}: {Description + value}

### Threats
1. **{Threat name}** (Severity: High/Medium/Low)
   - Attack vector: {How attack happens}
   - Impact: {What damage occurs}
   - Likelihood: {How likely}

2. **{Threat name}** (Severity: High/Medium/Low)
   - Attack vector: {How attack happens}
   - Impact: {What damage occurs}
   - Likelihood: {How likely}

### Mitigations

| Threat | Mitigation | Implementation | Status |
|--------|------------|----------------|--------|
| {Threat 1} | {How to prevent} | {Code/config} | ✅/❌ |
| {Threat 2} | {How to prevent} | {Code/config} | ✅/❌ |

## OWASP Top 10 Analysis

**Relevant OWASP risks for this feature**:

1. **{OWASP Risk}**: {How it applies}
   - Mitigation: {How we prevent it}

2. **{OWASP Risk}**: {How it applies}
   - Mitigation: {How we prevent it}

## Security Checklist

**Before deployment, verify**:

- [ ] Input validation (all user inputs sanitized)
- [ ] Authentication (only authorized users)
- [ ] Authorization (proper permission checks)
- [ ] Encryption (data at rest + in transit)
- [ ] Logging (security events logged)
- [ ] Rate limiting (prevent abuse)
- [ ] Error handling (no sensitive info leakage)
- [ ] Dependencies (no known vulnerabilities)
- [ ] Secret management (no hardcoded secrets)
- [ ] Security headers (CSP, HSTS, etc.)

## Secure Code Examples

**✅ Secure**:
```python
# Example of secure implementation
````

**❌ Insecure**:

```python
# Example of what NOT to do
```

## Compliance Requirements

**Applicable standards**:

- GDPR: {Relevant requirements}
- OWASP: {Relevant guidelines}
- SOC 2: {Relevant controls}

## Penetration Testing Plan

**Tests to run**:

1. {Test name}: {What to test}
2. {Test name}: {What to test}
3. {Test name}: {What to test}

```

---

## Research Quality Gates

**Before marking research as complete, verify**:

### Completeness Gates

- [ ] **Research question clearly defined**
- [ ] **Codebase searched first** (Grep + Glob + Read)
- [ ] **External research performed** (3-5 WebSearch queries)
- [ ] **Top sources fetched** (5+ WebFetch calls)
- [ ] **Findings documented** (follows template)
- [ ] **Sources evaluated** (quality ratings assigned)
- [ ] **Next steps provided** (actionable recommendations)

### Quality Gates

- [ ] **Code examples included** (not just theory)
- [ ] **Security considered** (if applicable)
- [ ] **Performance analyzed** (if applicable)
- [ ] **Tradeoffs documented** (pros and cons)
- [ ] **Integration points identified** (where it fits in codebase)
- [ ] **Tests recommended** (what to test)
- [ ] **Sources are recent** (2024-2025 preferred)

### Clarity Gates

- [ ] **Executive summary is clear** (2-3 sentences)
- [ ] **Recommendation is specific** (not vague)
- [ ] **Implementation steps are detailed** (can follow without questions)
- [ ] **Pitfalls are concrete** (specific mistakes to avoid)
- [ ] **Next steps are actionable** (can start immediately)

**If any gate fails, research is NOT complete.**

---

## Common Research Anti-Patterns

### ❌ Anti-Pattern 1: Skipping Codebase Search

**Problem**: Researching external patterns without checking if we already have a solution.

**Why Bad**: Reinventing the wheel, inconsistent patterns, wasted time.

**Solution**: ALWAYS search codebase first with Grep + Glob + Read.

### ❌ Anti-Pattern 2: Using Outdated Sources

**Problem**: Relying on tutorials from 2019-2020.

**Why Bad**: Outdated practices, deprecated APIs, security vulnerabilities.

**Solution**: Prioritize 2024-2025 sources. If using older sources, verify they're still current.

### ❌ Anti-Pattern 3: Theory Without Examples

**Problem**: Findings describe patterns but don't show code.

**Why Bad**: Implementer can't translate theory to code without guessing.

**Solution**: Always include multiple code examples with context.

### ❌ Anti-Pattern 4: No Tradeoff Analysis

**Problem**: Recommending one approach without explaining alternatives.

**Why Bad**: Reader doesn't understand WHY this is best for our use case.

**Solution**: Compare at least 2-3 alternatives with pros/cons table.

### ❌ Anti-Pattern 5: Ignoring Security

**Problem**: Researching implementation without security considerations.

**Why Bad**: Vulnerable code gets deployed, security issues discovered later.

**Solution**: Always include security section, even if just "N/A - not security-sensitive".

### ❌ Anti-Pattern 6: Vague Next Steps

**Problem**: "Research complete, proceed with implementation" without specific actions.

**Why Bad**: Implementer doesn't know what files to create or what to do first.

**Solution**: Provide specific, numbered next steps with file names.

---

## Integration with Autonomous Architecture

### How Research Fits Into Workflow

```

User request: "Design a webhook system"
↓
auto_research_trigger.py detects design question
↓
researcher subagent auto-invokes
↓
research-patterns skill provides methodology (THIS SKILL)
↓
researcher performs:

1. Codebase search
2. WebSearch (5 queries)
3. WebFetch (5+ sources)
4. Analysis & distillation
5. Save findings to docs/research/
6. Stage changes
   ↓
   researcher reports: "Research complete, see docs/research/20251018_webhook_system/findings.md"
   ↓
   planner subagent uses findings to create implementation plan
   ↓
   tester subagent writes tests based on findings
   ↓
   implementer subagent implements following findings
   ↓
   Feature complete, aligned with best practices ✅

```

### Research Feeds Other Subagents

**planner** uses research findings to:
- Choose architectural patterns
- Design system components
- Plan implementation phases

**tester** uses research findings to:
- Identify edge cases to test
- Write security tests
- Create performance benchmarks

**implementer** uses research findings to:
- Follow recommended patterns
- Avoid documented pitfalls
- Use proven code examples

**security-auditor** uses research findings to:
- Check for documented vulnerabilities
- Verify security best practices followed
- Validate against OWASP guidelines

**doc-syncer** uses research findings to:
- Document architectural decisions
- Link to research sources
- Explain pattern choices

---

## Example Research Workflows

### Workflow 1: Architecture Decision

**Trigger**: "Should we use microservices or monolith for this feature?"

**Research Process**:
1. Define question: "What architecture pattern for feature X with Y requirements?"
2. Codebase search: Check existing architecture (`docs/architecture/`)
3. WebSearch:
   - "microservices vs monolith decision criteria 2025"
   - "when to use microservices"
   - "monolith to microservices migration patterns"
4. WebFetch: Martin Fowler, microservices.io, AWS architecture blog
5. Distill findings:
   - Comparison table (complexity, ops, scaling, etc.)
   - Decision tree based on our requirements
   - Recommendation with clear reasoning

**Output**: `docs/research/20251018_architecture_decision/findings.md`

### Workflow 2: Library Comparison

**Trigger**: "Which Python caching library should we use?"

**Research Process**:
1. Define question: "Best caching library for ML model inference with TTL support?"
2. Codebase search: Check if we already use a caching library
3. WebSearch:
   - "Python caching libraries comparison 2025"
   - "Redis vs Memcached Python"
   - "cachetools vs dogpile.cache"
4. WebFetch: Official docs for top 3 libraries, performance benchmarks
5. Distill findings:
   - Feature comparison table
   - Performance benchmarks
   - Ease of use comparison
   - Recommendation based on our needs

**Output**: `docs/research/20251018_caching_library/findings.md`

### Workflow 3: Security Pattern

**Trigger**: "How should we handle API key authentication?"

**Research Process**:
1. Define question: "Secure API key authentication for external API?"
2. Codebase search: Check current auth patterns
3. WebSearch:
   - "API key authentication best practices 2025"
   - "API key security OWASP"
   - "API key vs OAuth comparison"
4. WebFetch: OWASP API Security, Auth0 docs, security blogs
5. Distill findings:
   - Security threat model
   - Recommended implementation (key rotation, rate limiting, etc.)
   - OWASP compliance checklist
   - Secure code examples

**Output**: `docs/research/20251018_api_key_auth/findings.md`

---

## Key Takeaways

1. **Research is an investment**: 20 minutes of research saves hours of refactoring.

2. **Codebase first**: Don't reinvent patterns we already have.

3. **Quality over quantity**: 3 great sources > 10 mediocre sources.

4. **Code examples are mandatory**: Theory alone is not actionable.

5. **Security is non-negotiable**: Always consider security implications.

6. **Tradeoffs must be explicit**: Help decision-makers understand choices.

7. **Recent sources preferred**: 2024-2025 for current best practices.

8. **Research feeds the whole workflow**: Findings guide all downstream subagents.

---

**This skill enables confident, informed implementation by ensuring we learn from the industry before we build.**
```
