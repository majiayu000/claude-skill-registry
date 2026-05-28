# PRD Validator Skill

## Metadata
- skill_name: prd-validator
- activation_code: PRD_VALIDATOR_V2
- version: 2.0.0
- category: validation
- phase: 3

## Description
Validates PRD documents against the PRD Template v2.0 specification. This includes schema validation, layer dependency checking, interface contract validation, and EARS format verification.

## Activation Criteria
- User mentions "validate PRD", "check PRD", "PRD validation"
- Processing Phase 3 of the pipeline
- User runs `/validate-prd` command

## Validation Steps

### 1. Schema Validation
Verify all 17 required sections exist:
1. Architectural Layer Assignment (L0-L5)
2. Dependency Declaration
3. Interface Contract Summary (YAML EXPORTS/IMPORTS)
4. Executive Summary (with Production-Ready Definition)
5. System Architecture (with diagrams)
6. Feature Requirements (FR-XXX-X.X format, EARS syntax)
7. Non-Functional Requirements (Performance, Security, Reliability, Scalability)
8. Code Structure
9. TDD Implementation (RED/GREEN/REFACTOR/VERIFY)
10. Integration Testing (with Contract Testing)
11. Documentation Requirements
12. Operational Readiness (Monitoring, Alerting, Health Checks)
13. Compliance & Audit
14. Migration & Rollback (with Feature Flags)
15. Risk & Assumptions (FMEA table)
16. Success Metrics
17. Task Decomposition Guidance
Plus: Appendices A-E (Glossary, References, Change History, AI Task Generation, Audit Checklist)

### 2. Layer Validation
Verify component layer assignment and dependencies according to the strict hierarchy:

| Layer | Name | Description | May Depend On |
|-------|------|-------------|---------------|
| L0 | Primitives | Basic types, math utilities, constants | **None** (zero external dependencies) |
| L1 | Infrastructure | Logging, config, I/O, networking | L0 only |
| L2 | Spatial | Coordinate systems, transforms, geometry | L0, L1 |
| L3 | Processing | Algorithms, data processing, ML models | L0, L1, L2 |
| L4 | Fusion | Multi-source integration, state estimation | L0, L1, L2, L3 |
| L5 | Interface | APIs, UIs, external integrations | L0, L1, L2, L3, L4 |

#### Layer Validation Rules

**Rule 1: No Upward Dependencies**
- A component at layer N can ONLY import from layers 0 through N-1
- L3 Processing CANNOT import from L4 Fusion or L5 Interface
- Violation = BLOCKING ERROR

**Rule 2: L0 Zero-Dependency Rule**
- L0 Primitives MUST have zero external dependencies
- L0 components can only use standard library
- Any import from another PRD component = BLOCKING ERROR

**Rule 3: Same-Layer Dependencies (WARNING)**
- Same-layer imports (e.g., L3 imports L3) are discouraged
- Recommend: Extract shared logic to lower layer OR use event-driven communication via L1
- Violation = WARNING (not blocking)

**Rule 4: Dependency Declaration Completeness**
- All imports in Section 1.3 IMPORTS table must specify source layer
- All exports in Section 1.3 EXPORTS table must be implemented
- Missing declarations = ERROR

#### How to Validate

1. **Extract assigned layer** from Section 1.2 "This Component's Layer: LN"
2. **Parse IMPORTS table** in Section 1.3 for all `from: PRD-XXX` entries
3. **For each import**, verify source layer < this component's layer
4. **For L0 components**, verify IMPORTS table is empty or N/A
5. **Flag same-layer imports** as warnings with remediation suggestions

### 3. Interface Contract Validation
Parse Section 1.4 YAML:
```yaml
exports:
  - interface: [Name]
    version: [SemVer]
    stability: [stable|experimental|deprecated]

imports:
  - interface: [Name]
    from: PRD-[XXX]
    version_constraint: ">= X.Y.Z"
```

**Check:** All imports have matching exports in referenced PRDs.

### 4. EARS Format Validation
Requirements must use EARS syntax:
```
WHEN [trigger], the system SHALL [behavior].
```

RFC 2119 keywords: SHALL, MUST, SHOULD, MAY, SHALL NOT, MUST NOT

**Check:** All FR entries use proper EARS format with RFC 2119 keywords.

### 5. FR Identifier Validation
Format: `FR-[PRD]-[Feature].[Requirement]`
Example: `FR-009-1.1`

**Check:** All FR identifiers are unique and properly formatted.

## Output

Generate validation report at `.claude/reports/prd-validation-report.md`:

```markdown
# PRD Validation Report

**PRD:** PRD-XXX
**Validated:** [timestamp]
**Status:** PASSED | FAILED

## Summary
- Schema: ✅ 17/17 sections
- Layers: ✅ No violations
- Interfaces: ✅ All compatible
- EARS Format: ✅ All valid
- FR Identifiers: ✅ All unique

## Issues Found
[List any warnings or errors]

## Recommendations
[Suggested improvements]
```

## Signals

On success: Create `.claude/.signals/prd-validated.json`
On failure: Create `.claude/.signals/prd-validation-failed.json`
