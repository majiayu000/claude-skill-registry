---
name: feature-docs
description: Use when the user asks to generate comprehensive feature documentation with verified test cases, create feature README with code evidence, or document a complete feature with test verification. Triggers on keywords like "feature documentation", "document feature", "comprehensive docs", "feature README", "test verification", "verified documentation".
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Task, TodoWrite
---

<!-- SOURCE OF TRUTH: docs/templates/skills/feature-docs/SKILL.md -->
<!-- Synced to: .claude/skills/ and .github/skills/ -->

# Feature Documentation Generation & Verification

Generate comprehensive feature documentation following the **GOLD STANDARD** template pattern.

**GOLD STANDARD Reference**: `docs/features/README.ExampleFeature1.md` (Example App)
**Template File**: `docs/templates/detailed-feature-docs-template.md`

---

## MANDATORY 26-SECTION STRUCTURE

All feature documentation MUST follow this section order:

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

## Phase 1: Feature Analysis

Build knowledge model in `.ai/workspace/analysis/[feature-name].md`.

### Discovery Areas

1. **Domain Entity Discovery**: Entities, value objects, enums
2. **Workflow Discovery**: Commands, Queries, Event Handlers, Background Jobs
3. **API Discovery**: Controllers, endpoints, DTOs
4. **Frontend Discovery**: Components, Services, Stores
5. **Cross-Service Discovery**: Message Bus messages, producers, consumers

---

## Phase 2: Documentation Generation

Generate at `docs/business-features/{Module}/detailed-features/README.{FeatureName}.md`.

### Key Format Examples

**Business Requirements (FR-XX)**:
```markdown
#### FR-{MOD}-01: {Requirement Title}

| Aspect          | Details                                 |
| --------------- | --------------------------------------- |
| **Description** | {What this requirement enables}         |
| **Scope**       | {Who can use / affected entities}       |
| **Evidence**    | `{FilePath}:{LineRange}`                |
```

**User Stories (US-XX)**:
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

**Test Summary Table (MANDATORY)**:
```markdown
| Category               | P0 (Critical) | P1 (High) | P2 (Medium) | P3 (Low) | Total |
| ---------------------- | :-----------: | :-------: | :---------: | :------: | :---: |
| {Category1}            | {N}           | {N}       | {N}         | {N}      | {N}   |
| **Total**              | **{N}**       | **{N}**   | **{N}**     | **{N}**  | **{N}**|
```

**Test Case Format (TC-XX)**:
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

**Troubleshooting Format**:
```markdown
#### {Issue Title}

**Symptoms**: {Observable problem}

**Causes**:
1. {Cause 1}
2. {Cause 2}

**Resolution**:
- {Step 1}
- {Step 2}
```

**Permission Matrix**:
```markdown
| Role | View | Create | Edit | Delete | Special |
|------|:----:|:------:|:----:|:------:|---------|
| Admin | ✅ | ✅ | ✅ | ✅ | Full access |
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

## Phase 3: Verification (2-Pass System)

### First Pass
For EACH code reference:
- Read actual source file at referenced lines
- Compare character-by-character
- Verify line numbers are accurate
- Log mismatches and correct immediately

### Second Pass
- Random sampling (10 code references)
- Cross-reference and TOC verification
- Completeness check

**CRITICAL**: If Second Pass finds MORE THAN 5 issues, HALT and re-run Phase 3.

---

## Anti-Hallucination Protocols

### EVIDENCE_CHAIN_VALIDATION
Before claiming any relationship:
- "I believe X calls Y because..." → show actual code
- "This follows pattern Z because..." → cite specific examples

### DOCUMENTATION_ACCURACY_CHECKPOINT
Before writing any documentation:
- "Have I read the actual code that implements this?"
- "Are my line number references accurate and current?"
- "Can I provide a code snippet as evidence?"

---

## Evidence Verification Protocol (QC)

### Verification Summary Table
```markdown
| Category | Total Claims | Verified | Stale | Missing | Last Verified |
|----------|-------------|----------|-------|---------|---------------|
| Business Requirements | {N} | {N} | {N} | {N} | {Date} |
| Test Specifications | {N} | {N} | {N} | {N} | {Date} |
| **Total** | **{N}** | **{N}** | **{N}** | **{N}** | |
```

### Status Markers
- ✅ Verified - Line numbers match actual source
- ⚠️ Stale - Line numbers shifted, content still exists
- ❌ Missing - Referenced code no longer exists

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

### AI Companion Checklist
- [ ] AI companion file created at `README.{FeatureName}.ai.md`
- [ ] AI companion ≤300 lines
- [ ] File locations section complete with exact paths
- [ ] API contracts include request/response shapes
- [ ] All evidence references preserved from full doc
- [ ] Patterns section has required (✅) and anti-patterns (❌)
