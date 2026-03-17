# Mock Detector Skill

## Metadata
- skill_name: mock-detector
- activation_code: MOCK_DETECTOR_V1
- version: 1.0.0
- category: validation
- phase: 3, 4, 5

## Description
Detects and prevents mock/simulated implementations in operational code. Ensures all code is real, functional implementation or explicit failure.

## Activation Criteria
- After code generation in Phase 3
- Before integration testing in Phase 4
- During deployment validation in Phase 5
- When mock patterns detected in code

## Core Principle
**"Fail honestly rather than succeed falsely"**

## Detection Patterns

### Forbidden in Operational Code
```python
# Mock implementations
mock_service, MockClass, FakeConnection
simulated_deployment, fake_response
dummy_data, stub_connection

# Placeholder returns
return "success"  # Without actual logic
return {"status": "ok"}  # Hardcoded response

# Simulation functions
def simulate_*(), mock_*(), fake_*()

# Incomplete implementations
# TODO: implement real connection
# FIXME: placeholder
# Not actually connecting
```

### Allowed ONLY in Tests
- Files: *_test.py, *.test.js, *.spec.js
- Directories: /tests, /test, /__tests__, /spec
- Test fixtures and mocks for unit testing

## Validation Process

### 1. Scan Source Code
```bash
# Check for mock patterns in operational code
find src/ services/ -type f -name "*.py" | \
  xargs grep -l "mock\|fake\|simulated\|dummy"

# Exclude test files
find . -name "*test*" -prune -o -type f -exec grep -l "mock" {} \;
```

### 2. Pattern Analysis
```python
class MockDetector:
    FORBIDDEN_PATTERNS = [
        r"class\s+Mock",
        r"class\s+Fake", 
        r"def\s+simulate_",
        r"return\s+['\"]success['\"]",
        r"#.*fake|mock|placeholder",
        r"TODO.*implement.*real"
    ]
    
    def scan_file(self, filepath):
        if self.is_test_file(filepath):
            return []  # Mocks allowed in tests
        
        violations = []
        for pattern in self.FORBIDDEN_PATTERNS:
            if re.search(pattern, content, re.IGNORECASE):
                violations.append({
                    "file": filepath,
                    "pattern": pattern,
                    "severity": "CRITICAL"
                })
        return violations
```

### 3. Enforcement Actions

#### If Mock Detected:
1. **STOP pipeline immediately**
2. **Generate violation report**
3. **Require human intervention**
4. **Block deployment**

#### Violation Report:
```json
{
    "violation": "MOCK_CODE_DETECTED",
    "files": [
        {
            "path": "src/services/deployment.py",
            "line": 45,
            "code": "return 'success'  # TODO: implement",
            "issue": "Hardcoded response without implementation"
        }
    ],
    "action_required": "Replace with real implementation or explicit failure",
    "pipeline_status": "BLOCKED"
}
```

## Required Replacements

### Instead of Mock → Real or Fail

```python
# ❌ FORBIDDEN: Mock implementation
def connect_to_device():
    print("Simulating connection...")
    return True

# ✅ REQUIRED: Real implementation
def connect_to_device():
    ssh = paramiko.SSHClient()
    ssh.connect(host, username, password)
    return ssh

# ✅ ALSO ACCEPTABLE: Explicit failure
def connect_to_device():
    raise NotImplementedError(
        "SSH connection requires netmiko library"
    )
```

### Instead of Placeholder → Complete or Error

```python
# ❌ FORBIDDEN: Placeholder
def deploy_config(config):
    # TODO: Implement deployment
    return {"status": "success"}

# ✅ REQUIRED: Complete implementation
def deploy_config(config):
    connection = establish_connection()
    result = connection.send_config(config)
    return parse_response(result)

# ✅ ALSO ACCEPTABLE: Clear error
def deploy_config(config):
    raise RuntimeError(
        "Cannot deploy: Missing device credentials"
    )
```

## Integration Points
- Reads: All source code files
- Validates: Non-test code only
- Writes: .mock-violations.json
- Signals: MOCK_VIOLATION_DETECTED
- Blocks: Pipeline progression if violations found

## Exceptions

### Test Files (Mocks Allowed)
- Unit tests requiring mocks
- Integration test fixtures
- Test data generators
- Performance test stubs

### Documentation (Allowed)
- Example code in docs
- README examples
- Tutorial code

## Severity Levels

### CRITICAL (Pipeline Stops)
- Mock service in production code
- Simulated deployment in operations
- Fake data in business logic

### WARNING (Logged but Continues)
- TODO comments about implementation
- Deprecated code marked for removal

## Success Criteria
- Zero mock implementations in /src
- Zero simulated services in /services
- All connections are real or fail explicitly
- No hardcoded success responses

## Failure Message
```
════════════════════════════════════════════
  MOCK CODE VIOLATION DETECTED
════════════════════════════════════════════

Mock/simulated code found in operational components.
This violates the "fail honestly" principle.

Required Actions:
1. Replace ALL mock code with real implementations
2. If real implementation impossible, use explicit error
3. Move any test mocks to test directories only

The pipeline will not continue until resolved.
```