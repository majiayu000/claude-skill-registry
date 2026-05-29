---
name: ontology-why
description: |
  Ontology Integrity Design Rationale Helper.
  Explains "why" decisions with 5 Integrity perspectives (Immutability, Determinism,
  Referential Integrity, Semantic Consistency, Lifecycle Management).
  Helper skill called by other ontology-* skills for design rationale.
user-invocable: true
model: opus
version: "3.0.0"
argument-hint: "<question about ontology design>"
allowed-tools:
  - Read
  - Glob
  - Grep
  - WebSearch
  - WebFetch
  - mcp__sequential-thinking__sequentialthinking
hooks:
  Setup:
    - type: command
      command: "source /home/palantir/.claude/skills/shared/workload-files.sh"
      timeout: 5000
---

# /ontology-why - Ontology Integrity Design Rationale Helper

> **Version:** 3.0.0 | **Model:** opus | **Type:** Helper Skill

---

## Overview

| Aspect | Description |
|--------|-------------|
| **Purpose** | Explain "why" ontology design decisions with 5 Integrity perspectives |
| **Output** | Structured box format with perspectives, references, recommendations |
| **Reference** | `.claude/rules/ontology.md` for naming conventions |

---

## Cross-Skill Integration

| Skill | Relationship |
|-------|--------------|
| `/ontology-objecttype` | Calls this for "why?" questions during analysis |
| `/ontology-core` | Calls this to explain validation error rationale |
| `/ontology-linktype` | (Planned) Calls for cardinality decision rationale |

---

## Invocation

### Direct Invocation

```bash
/ontology-why employeeId를 String으로 정의한 이유는?
/ontology-why MANY_TO_ONE vs ONE_TO_MANY 차이점
/ontology-why ActionType에서 hazardous=True는 언제 사용?
```

### Called by Other Skills

```python
# From /ontology-objecttype when user asks "왜?"
return await invoke_skill("ontology-why", {
    "question": question,
    "context": current_analysis_context,
    "type": "ObjectType"
})
```

---

## 5 Integrity Perspectives (REQUIRED)

All responses MUST include analysis from these 5 perspectives:

| Perspective | Definition | Key Question |
|-------------|------------|--------------|
| **1. Immutability** | PK/identifiers must never change after creation | "Will this value ever change?" |
| **2. Determinism** | Same input must always produce same PK/state | "Is this reproducible on rebuild?" |
| **3. Referential Integrity** | LinkType references must remain valid | "What happens on delete?" |
| **4. Semantic Consistency** | Types must match business domain meaning | "Does this reflect reality?" |
| **5. Lifecycle Management** | Object state changes must be tracked | "Can we audit transitions?" |

### Perspective Details

**1. Immutability**
- PK is the object's "fingerprint" - permanent once assigned
- Applies to: Primary Key, Natural Identifier, FK references
- Violation impact: Lost edits, broken links, lost history

**2. Determinism**
- Same data must produce same PK (reproducibility)
- Forbidden: `now()`, `random()`, `row_number()` in PK generation
- Violation impact: PK changes on rebuild, duplicate objects

**3. Referential Integrity**
- LinkType references must remain valid
- Requires: FK existence verification, cascade/restrict policies
- Violation impact: Orphan objects, reference errors

**4. Semantic Consistency**
- Technical definitions must match business meaning
- Applies to: DataType selection, cardinality, constraints
- Violation impact: Wrong business logic, unreliable analysis

**5. Lifecycle Management**
- Object state changes must be trackable and consistent
- Applies to: Status properties, ActionType effects, audit logs
- Violation impact: Inconsistent state changes, audit failures

---

## Output Format (REQUIRED)

```
╔══════════════════════════════════════════════════════════════╗
║  Ontology Integrity Analysis: {subject}                      ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Q: {user question}                                          ║
║                                                              ║
║  1. Immutability                                             ║
║     ├─ Core: {explanation}                                   ║
║     ├─ Rationale: {why this matters}                         ║
║     └─ Violation: {specific impact}                          ║
║                                                              ║
║  2. Determinism                                              ║
║     ├─ Core: {explanation}                                   ║
║     ├─ Rationale: {why this matters}                         ║
║     └─ Violation: {specific impact}                          ║
║                                                              ║
║  3. Referential Integrity                                    ║
║     ├─ Core: {explanation}                                   ║
║     ├─ Rationale: {why this matters}                         ║
║     └─ Violation: {specific impact}                          ║
║                                                              ║
║  4. Semantic Consistency                                     ║
║     ├─ Core: {explanation}                                   ║
║     ├─ Rationale: {why this matters}                         ║
║     └─ Violation: {specific impact}                          ║
║                                                              ║
║  5. Lifecycle Management                                     ║
║     ├─ Core: {explanation}                                   ║
║     ├─ Rationale: {why this matters}                         ║
║     └─ Violation: {specific impact}                          ║
║                                                              ║
║  Official Reference:                                         ║
║  "{quote from official docs}"                                ║
║  URL: {palantir.com/docs/...}                                ║
║                                                              ║
║  Recommendations:                                            ║
║  • {recommendation 1}                                        ║
║  • {recommendation 2}                                        ║
║  • {recommendation 3}                                        ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

---

## Reference System

### Local Reference (ontology-definition package)

```
/home/palantir/park-kyungchan/palantir/Ontology-Definition/
├── ontology_definition/types/    # Type structure/constraints
├── ontology_definition/core/     # Enums, principles
└── tests/                        # Usage patterns
```

### External References (WebSearch/WebFetch)

**Trusted Sources ONLY:**
- `palantir.com/docs/*` (Official documentation)
- `github.com/palantir/*` (Official repositories)
- Palantir case studies, conference materials

**Blocked Sources:**
- Personal blogs, unofficial Medium posts
- Stack Overflow (non-official)
- Unverified forums

---

## Question Categories

| Category | Example Questions |
|----------|-------------------|
| **ObjectType** | "Why PK as String?", "Why is this property required?" |
| **PropertyDefinition** | "Why DATE vs TIMESTAMP?", "Why unique=True?" |
| **LinkType** | "Why MANY_TO_ONE?", "Why FOREIGN_KEY implementation?" |
| **ActionType** | "Why hazardous=True?", "Why is this parameter required?" |
| **Interface** | "Why separate as Interface?", "Why share this property?" |
| **Automation** | "Why TIME vs OBJECT_SET condition?", "Why this Effect?" |

---

## Validation Checklist

Before returning response, verify:
- [ ] All 5 Integrity perspectives included
- [ ] Each perspective has Core-Rationale-Violation structure
- [ ] At least 1 Palantir official URL attached
- [ ] No speculative expressions ("probably", "might", "maybe")
- [ ] 3+ practical recommendations provided

---

## Error Handling

| Situation | Response |
|-----------|----------|
| Unclear question | Request specific ObjectType/Property context |
| No official docs found | State "No verified reference found" and explain general principles |
| Out of scope | Guide back to Ontology-related questions |
| Missing perspective | Auto-complete with warning |

---

## Version History

| Version | Change |
|---------|--------|
| 1.0.0 | Initial "why?" question handler |
| 1.1.0 | 5 Integrity perspectives, WebSearch/Context7 integration |
| 3.0.0 | Frontmatter normalization, MCP tool inclusion, duplicate removal |

**End of Skill Definition**
