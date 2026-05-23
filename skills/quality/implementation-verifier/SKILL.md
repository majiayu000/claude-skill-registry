# Implementation Verifier Skill

## Metadata
- skill_name: implementation-verifier
- activation_code: IMPLEMENTATION_VERIFIER_V1
- version: 1.0.0
- category: validation
- phase: post-implementation

## Description
Verifies that implementation matches PRD requirements without substitutions or omissions.

## Activation Criteria
- Triggered after Phase 3 (Implementation) completes
- Before marking any task as complete
- When critical components are involved

## Workflow
1. Extract critical requirements from PRD
2. Check for required imports/packages
3. Verify architectural boundaries
4. Validate no unauthorized substitutions
5. Generate compliance report

## Validation Checks

### Package Verification
```python
required_packages = {
    "netmiko": ["from netmiko import", "ConnectHandler"],
    "neo4j": ["from neo4j import", "AsyncGraphDatabase"],
    "ollama": ["ollama", "llama"],
    "fastapi": ["from fastapi import", "FastAPI"]
}
```

### Architecture Verification
- Check separation of concerns
- Verify security boundaries
- Ensure no shortcuts taken

## Output
- Compliance report
- List of missing components
- Substitution warnings
- Recommendations for fixes

## Integration Points
- Reads: PRD, tasks.json, generated code
- Writes: verification-report.json
- Signals: VERIFICATION_FAILED, VERIFICATION_PASSED

## Example Activation
When implementation completes, this skill automatically:
1. Scans all generated files
2. Matches against PRD requirements
3. Alerts on missing critical components
4. Blocks progression until resolved