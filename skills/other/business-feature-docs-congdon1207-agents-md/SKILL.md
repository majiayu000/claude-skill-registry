---
name: business-feature-docs
description: Generate enterprise module documentation with 26-section structure and folder hierarchy. Use for module docs, enterprise features, detailed specs in docs/business-features/{Module}/. Includes README, INDEX, API-REFERENCE, detailed-features/. Triggers on "module docs", "enterprise feature docs", "business module", "26-section docs", "detailed feature specs". For single-file quick docs, use feature-docs instead.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Task, TodoWrite
---

<!-- SYNC: Source of truth is docs/templates/skills/business-feature-docs/SKILL.md -->
<!-- Keep in sync with .github/skills/business-feature-docs/SKILL.md -->

# EasyPlatform Business Feature Documentation

Generate comprehensive business feature documentation following the **GOLD STANDARD** template pattern.

**GOLD STANDARD Reference**: `docs/features/README.ExampleFeature1.md` (Example App)
**Template File**: `docs/templates/detailed-feature-docs-template.md`

---

## Output Structure

All documentation MUST be placed in the correct folder structure:

```
docs/
├── BUSINESS-FEATURES.md              # Master index (UPDATE if new module)
└── business-features/
    ├── {Module}/                     # Module folder
    │   ├── README.md                 # Complete module documentation
    │   ├── INDEX.md                  # Navigation hub
    │   ├── API-REFERENCE.md          # Endpoint documentation
    │   ├── TROUBLESHOOTING.md        # Issue resolution guide
    │   └── detailed-features/
    │       ├── README.{FeatureName}.md     # Deep dive (~1000 lines)
    │       └── README.{FeatureName}.ai.md  # AI companion (~300 lines)
    └── ...
```

---

## MANDATORY 26-SECTION STRUCTURE

All feature documentation in `detailed-features/` MUST follow this section order:

| # | Section | Stakeholder Focus |
|---|---------|-------------------|
| 1 | Executive Summary | PO, BA |
| 2 | Business Value | PO, BA |
| 3 | Business Requirements | PO, BA |
| 4 | Business Rules | BA, Dev |
| 5 | Process Flows | BA, Dev, Architect |
| 6 | Design Reference | BA, UX, Dev |
| 7 | System Design | Dev, Architect |
| 8 | Architecture | Dev, Architect |
| 9 | Domain Model | Dev, Architect |
| 10 | API Reference | Dev, Architect |
| 11 | Frontend Components | Dev |
| 12 | Backend Controllers | Dev |
| 13 | Cross-Service Integration | Dev, Architect |
| 14 | Security Architecture | Dev, Architect |
| 15 | Performance Considerations | Dev, Architect, DevOps |
| 16 | Implementation Guide | Dev |
| 17 | Test Specifications | QA |
| 18 | Test Data Requirements | QA |
| 19 | Edge Cases Catalog | QA, Dev |
| 20 | Regression Impact | QA |
| 21 | Troubleshooting | Dev, QA, DevOps |
| 22 | Operational Runbook | DevOps |
| 23 | Roadmap and Dependencies | PO, BA |
| 24 | Related Documentation | All |
| 25 | Glossary | PO, BA |
| 26 | Version History | All |

---

## Phase 1: Module Detection & Context Gathering

### Step 1.1: Identify Target Module

Determine which module the feature belongs to by:
1. User explicitly specifies module name
2. Feature name/domain implies module
3. Search codebase for feature-related entities/commands

### Step 1.2: Read Existing Documentation

Before creating new docs, read existing structure:
```
1. Read docs/BUSINESS-FEATURES.md (master index)
2. Read docs/business-features/{Module}/INDEX.md (if exists)
3. Read docs/business-features/{Module}/README.md (if exists)
4. Identify what already exists vs what needs creation/update
```

### Step 1.3: Codebase Analysis

Gather evidence from source code:
- **Entities**: `src/Services/{Module}/{Module}.Domain/Entities/`
- **Commands**: `src/Services/{Module}/{Module}.Application/UseCaseCommands/`
- **Queries**: `src/Services/{Module}/{Module}.Application/UseCaseQueries/`
- **Controllers**: `src/Services/{Module}/{Module}.Service/Controllers/`
- **Frontend**: `src/BravoWeb/apps/bravo-{module}/` or `src/BravoWeb/libs/apps-domains/`

---

## Phase 2: Key Format Examples

### Quick Navigation by Role

```markdown
| Role | Priority Sections | Key Concerns |
|------|------------------|--------------|
| **Product Owner** | Executive Summary, Business Value, Roadmap | ROI, scope, timeline, dependencies |
| **Business Analyst** | Business Requirements, Business Rules, Process Flows | Requirements traceability, acceptance criteria |
| **Developer** | Architecture, Domain Model, API Reference, Implementation Guide | Code patterns, integration points |
| **Tech Architect** | System Design, Architecture, Cross-Service Integration, Performance | System design, scalability, tech debt |
| **QA Engineer** | Test Specifications, Test Data Requirements, Edge Cases Catalog | Test coverage, automation feasibility |
| **QC Analyst** | All sections | Evidence verification, documentation accuracy |
| **DevOps** | Operational Runbook, Troubleshooting, Performance | Deployment, monitoring, incident response |
```

### Business Requirements (FR-XX)

```markdown
#### FR-{MOD}-01: {Requirement Title}

| Aspect          | Details                                              |
| --------------- | ---------------------------------------------------- |
| **Description** | {What this requirement enables}                      |
| **Scope**       | {Who can use / affected entities}                    |
| **Validation**  | {Business rules and constraints}                     |
| **Priority**    | {P0/P1/P2/P3}                                        |
| **Evidence**    | `{FilePath}:{LineRange}`                             |
```

### User Stories (US-XX)

```markdown
#### US-{MOD}-01: {Story Title}

**As a** {role}
**I want** {goal/desire}
**So that** {benefit/value}

**Acceptance Criteria**:
- [ ] AC-01: {Criterion with evidence reference}
- [ ] AC-02: {Criterion with evidence reference}

**Related Requirements**: FR-{MOD}-01, FR-{MOD}-02
**Evidence**: `{FilePath}:{LineRange}`
```

### Business Value

```markdown
### Value Proposition

| Value Type | Description | Impact | Quantification |
|------------|-------------|--------|----------------|
| Revenue | {Revenue impact} | {H/M/L} | {$ or % if available} |
| Efficiency | {Time/cost savings} | {H/M/L} | {Hours/costs saved} |
| User Experience | {UX improvement} | {H/M/L} | {NPS/satisfaction improvement} |
| Compliance | {Regulatory/audit benefit} | {H/M/L} | {Risk reduction} |
```

### Business Rules

```markdown
### Validation Rules

| Rule ID | Rule | Condition | Action | Evidence |
|---------|------|-----------|--------|----------|
| BR-{MOD}-01 | {Rule name} | {When condition} | {Then action} | `{File}:{Line}` |

### State Transitions

| From State | Event | To State | Conditions | Evidence |
|------------|-------|----------|------------|----------|
| Draft | Activate | Active | {Conditions} | `{File}:{Line}` |
```

### Technical Decisions Log

```markdown
### Technical Decisions Log

| Decision | Date | Options Considered | Chosen | Rationale | Evidence |
|----------|------|-------------------|--------|-----------|----------|
| {Decision title} | {Date} | {Option A, B} | {Chosen} | {Why} | `{File}:{Line}` |

### Technical Debt

| Item | Severity | Impact | Remediation Plan | Evidence |
|------|----------|--------|------------------|----------|
| {Debt item} | H/M/L | {Impact} | {Plan} | `{File}:{Line}` |
```

### Test Specifications (TC-XX)

**Test Summary Table (MANDATORY)**:
```markdown
| Category               | P0 (Critical) | P1 (High) | P2 (Medium) | P3 (Low) | Total |
| ---------------------- | :-----------: | :-------: | :---------: | :------: | :---: |
| {Category1}            | {N}           | {N}       | {N}         | {N}      | {N}   |
| **Total**              | **{N}**       | **{N}**   | **{N}**     | **{N}**  | **{N}**|
```

**Test Case Format**:
```markdown
#### TC-{MOD}-001: {Test Name} [P0]

**Acceptance Criteria**:
- ✅ {Passing criteria 1}
- ✅ {Passing criteria 2}

**GIVEN** {initial context}
**WHEN** {action performed}
**THEN** {expected outcome}

**Edge Cases**:
- ❌ {Invalid scenario} → {Expected error/behavior}

**Evidence**: `{FilePath}:{LineRange}`
```

### Edge Cases Catalog

```markdown
### Input Validation Edge Cases

| ID | Scenario | Input | Expected Behavior | Evidence |
|----|----------|-------|-------------------|----------|
| EC-01 | Empty string | `""` | Validation error | `{File}:{Line}` |
| EC-02 | Max length | `{256 chars}` | Truncate/Error | `{File}:{Line}` |

### Business Logic Edge Cases

| ID | Scenario | Condition | Expected Behavior | Evidence |
|----|----------|-----------|-------------------|----------|
| EC-10 | {Scenario} | {Condition} | {Behavior} | `{File}:{Line}` |
```

### Operational Runbook

```markdown
### Deployment Checklist

- [ ] Database migrations applied
- [ ] Configuration values verified
- [ ] Health checks passing
- [ ] Smoke tests executed
- [ ] Rollback plan ready

### Monitoring

| Metric | Alert Threshold | Dashboard | Escalation |
|--------|-----------------|-----------|------------|
| Error Rate | >1% | {Dashboard URL} | {Team} |
```

### Evidence Verification Protocol

```markdown
## Evidence Verification Protocol

### Verification Summary

| Category | Total Claims | Verified | Stale | Missing | Last Verified |
|----------|-------------|----------|-------|---------|---------------|
| Business Requirements | {N} | {N} | {N} | {N} | {Date} |
| Architecture | {N} | {N} | {N} | {N} | {Date} |
| Test Specifications | {N} | {N} | {N} | {N} | {Date} |
| **Total** | **{N}** | **{N}** | **{N}** | **{N}** | |

### Evidence Verification Table

| Claim ID | Claim | File | Documented Lines | Actual Lines | Status | Verified By |
|----------|-------|------|-----------------|--------------|--------|-------------|
| FR-{MOD}-01 | {Claim} | `{File}` | L{X}-{Y} | L{X}-{Y} | ✅ Verified | {Name/Date} |

### Audit Trail

| Date | Action | Reviewer | Notes |
|------|--------|----------|-------|
| {Date} | Initial verification | {Name} | {Notes} |
```

### Security Architecture

```markdown
### Authorization Matrix

| Role | View | Create | Edit | Delete | Special Permissions |
|------|:----:|:------:|:----:|:------:|---------------------|
| Admin | ✅ | ✅ | ✅ | ✅ | Full access |
| Manager | ✅ | ✅ | ✅ | ❌ | Company scope |
| User | ✅ | ❌ | ❌ | ❌ | Own data only |

### Data Protection

| Data Type | Protection | Evidence |
|-----------|------------|----------|
| PII | Encrypted at rest | `{File}:{Line}` |
```

### Glossary

```markdown
## Glossary

| Term | Definition | Context |
|------|------------|---------|
| {Term} | {Definition for non-technical stakeholders} | {Where used} |
| {Acronym} | {Full form and meaning} | {Where used} |
```

---

## Phase 2.5: AI Companion Generation

Generate AI-agent optimized companion file alongside the comprehensive documentation.

**Output**: `docs/business-features/{Module}/detailed-features/README.{FeatureName}.ai.md`
**Template**: `docs/templates/detailed-feature-docs-template.ai.md`

### AI Companion Structure (10 Sections, ~260 lines)

| Section | Content | Source from Full Doc |
|---------|---------|---------------------|
| Context | Purpose, entities, service | Executive Summary |
| File Locations | Exact paths to all key files | Implementation Guide |
| Domain Model | Properties, expressions | Domain Model |
| API Contracts | Endpoints, request/response shapes | API Reference |
| Business Rules | Validation, state transitions | Business Rules |
| Patterns | Required ✅ / Anti-patterns ❌ | Architecture |
| Integration | Events, dependencies | Cross-Service Integration |
| Security | Authorization matrix | Security Architecture |
| Test Scenarios | Key GIVEN/WHEN/THEN cases | Test Specifications |
| Quick Reference | Decision tree, code snippets | Implementation Guide |

### Compression Rules

1. **Tables over prose** - Convert paragraphs to table rows
2. **Paths over descriptions** - `File:Line` over "located in..."
3. **Signatures over examples** - `{ id: string } → { entity: Dto }` over full code
4. **Decisions over explanations** - What to do, not why

### AI Companion Quality Check

- [ ] File size ≤300 lines
- [ ] All file paths are exact and current
- [ ] API contracts include request/response shapes
- [ ] Business rules have evidence references
- [ ] Patterns section has ✅/❌ markers
- [ ] Evidence chain preserved from full doc

---

## Phase 3: Master Index Update

After creating/updating module docs, update `docs/BUSINESS-FEATURES.md`:

1. Read current content
2. Verify module is listed in the "Detailed Module Documentation" table
3. Add link if missing:
   ```markdown
   | **{Module}** | [Description] | [View Details](./business-features/{Module}/README.md) |
   ```

---

## Anti-Hallucination Protocols

### EVIDENCE_CHAIN_VALIDATION
- Every feature claim MUST have code reference with file path and line numbers
- Read actual source files before documenting
- Never assume behavior without code evidence

### ACCURACY_CHECKPOINT
Before writing any documentation:
- "Have I read the actual code?"
- "Are my line number references accurate?"
- "Can I provide a code snippet as evidence?"

---

## Quality Checklist

- [ ] All 26 mandatory sections present in correct order
- [ ] Quick Navigation by Role included
- [ ] Executive Summary with key capabilities
- [ ] Business Value with ROI analysis
- [ ] User Stories with acceptance criteria (US-XX format)
- [ ] Business Requirements use FR-{MOD}-XX format
- [ ] Business Rules with state transitions
- [ ] Process Flows with diagrams
- [ ] System Design with technical decisions log
- [ ] Security Architecture with authorization matrix
- [ ] Performance Considerations with targets
- [ ] Implementation Guide with code examples
- [ ] Test Summary table with P0-P3 counts
- [ ] Test Data Requirements and fixtures
- [ ] Edge Cases Catalog (validation, business, concurrency)
- [ ] Regression Impact analysis
- [ ] Test cases use TC-{MOD}-XXX format with GIVEN/WHEN/THEN
- [ ] Acceptance criteria use ✅/❌ markers
- [ ] Troubleshooting uses Symptoms/Causes/Resolution format
- [ ] Operational Runbook with deployment checklist
- [ ] Roadmap and Dependencies
- [ ] Evidence Verification Protocol with audit trail
- [ ] Glossary for non-technical stakeholders
- [ ] Version History table at end
- [ ] All code references verified with actual files
- [ ] ASCII diagrams for architecture
- [ ] Master index (BUSINESS-FEATURES.md) updated

### AI Companion Checklist
- [ ] AI companion file created at `README.{FeatureName}.ai.md`
- [ ] AI companion ≤300 lines
- [ ] File locations section complete with exact paths
- [ ] API contracts include request/response shapes
- [ ] All evidence references preserved from full doc
- [ ] Patterns section has required (✅) and anti-patterns (❌)
