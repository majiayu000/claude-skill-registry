# PRD Compliance Validator Skill

## Metadata
- skill_name: prd-compliance-validator
- activation_code: PRD_COMPLIANCE_VALIDATOR_V1
- version: 1.0.0
- category: validation
- phase: post-implementation

## Description
Generic validation skill that ensures implementation matches PRD requirements without hardcoding specific tools.

## Activation Criteria
- Triggered after implementation phase
- When tasks marked complete
- Before deployment phase

## Workflow

### 1. Requirement Extraction
```bash
# Extract MUST USE statements from PRD
grep -i "must use\|must implement\|required:" docs/PRD.md

# Extract CANNOT USE statements
grep -i "do not use\|cannot use\|forbidden:" docs/PRD.md

# Extract architectural requirements
grep -i "architecture\|separation\|boundary" docs/PRD.md
```

### 2. Dynamic Validation
- Parse PRD for explicit requirements
- Build validation rules based on PRD content
- Check implementation against extracted rules
- No hardcoded tool names

### 3. Validation Process
```python
class PRDComplianceValidator:
    def extract_requirements(self, prd_path):
        """Extract requirements dynamically from PRD"""
        requirements = {
            "must_use": [],
            "cannot_use": [],
            "architecture": []
        }
        # Parse PRD for requirement patterns
        return requirements
    
    def validate_implementation(self, requirements, src_path):
        """Validate against extracted requirements"""
        violations = []
        for req in requirements["must_use"]:
            if not self.find_in_code(req, src_path):
                violations.append(f"Missing: {req}")
        return violations
```

## Generic Patterns

### Requirement Detection Patterns
- `MUST use [component]`
- `REQUIRES [component]`
- `DO NOT substitute [x] with [y]`
- `CANNOT use [component]`
- `[Component] is MANDATORY`

### Implementation Verification
- Search for required components in code
- Check configuration files
- Verify service definitions
- Validate architectural boundaries

## Output Format
```json
{
    "compliance": {
        "status": "pass|fail",
        "requirements_met": [],
        "violations": [],
        "warnings": []
    },
    "extracted_from": "docs/PRD.md",
    "validation_time": "2024-01-01T00:00:00Z"
}
```

## Integration Points
- Reads: PRD, implementation files
- Writes: .prd-compliance-report.json
- Signals: COMPLIANCE_CHECK_COMPLETE

## No Hardcoding
This skill MUST NOT contain:
- Specific tool names (netmiko, neo4j, etc.)
- Fixed validation patterns
- Hardcoded file paths
- Tool-specific checks

Instead, it dynamically adapts to ANY PRD by:
- Extracting requirements at runtime
- Building validation rules from PRD content
- Using generic search patterns
- Adapting to project structure