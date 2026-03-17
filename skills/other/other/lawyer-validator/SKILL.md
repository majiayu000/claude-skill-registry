---
name: lawyer_validator
description: Validates FINAL_DRAFT.json for legal correctness, Indian court compliance, formatting, and hallucination risk. Produces VALIDATION_REPORT.json with pass/fail and required fixes.
tools: Read, Grep, Glob
disallowedTools: Write, Edit, Bash
---

# Lawyer Validator Skill (Indian Context)

## Purpose
This skill performs court-grade validation of generated legal drafts.
It checks compliance, structure, missing mandatory clauses, jurisdiction correctness, and detects hallucinated facts/citations.



## Inputs
- FINAL_DRAFT.json
- MASTER_FACTS.json
- MERGED_CONTEXT.json
- COMPLIANCE_REPORT.json
- LOCAL_RULES.json
- PRAYER_PACK.json
- CITATION_PACK.json (optional)

## Outputs
Writes:
- VALIDATION_REPORT.json

## Validation Checklist (Mandatory)
1. Jurisdiction correctness (State, City, Court)
2. Correct court heading format
3. Proper party naming format (Petitioner/Respondent)
4. Verification clause present
5. Affidavit requirements included if needed
6. Prayer clause matches proceeding type
7. Annexures referenced correctly
8. Limitation compliance check
9. No missing mandatory sections
10. No hallucinated facts (must exist in MASTER_FACTS or uploaded docs)
11. No unverified citations (must be verified=true and have verification_hash)

## Hard Failure Conditions (Must Fail)
- Missing jurisdiction
- Missing verification clause (where mandatory)
- Any fact not backed by source_doc_id
- Any citation without verified=true + verification_hash
- Relief/prayer not supported by facts
- Wrong court type for proceeding

## Output Schema (VALIDATION_REPORT.json)
Must include:
- status: PASS/FAIL
- issues: [ {severity, section, problem, fix_suggestion} ]
- hallucination_flags: []
- citation_flags: []
- missing_sections: []
- quality_score: 0-100

Model Configuration Test Results
================================
Configuration: [Kimi K2.5]
Total Cost: $X.XX
Execution Time: XX seconds
Accuracy Score: XX%
Notes: [observations]

## Test speed 
U need check te

