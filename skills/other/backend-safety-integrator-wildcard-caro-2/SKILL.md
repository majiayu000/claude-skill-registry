---
name: backend-safety-integrator
description: Guide for integrating safety validation into new inference backends
---

# Backend Safety Integrator Skill

**Purpose**: Systematically integrate safety validation when adding new LLM inference backends to Caro.

**When to Use**:
- Adding a new inference backend (MLX, Anthropic API, OpenAI, etc.)
- Updating existing backend safety integration
- Ensuring backend calls safety validator before execution

**Duration**: 2-4 hours depending on backend complexity

---

## The 6-Phase Integration Workflow

```
Phase 1: Understand Backend Architecture (30 min)
Phase 2: Identify Command Generation Point (30 min)
Phase 3: Integrate Safety Validator (1 hour)
Phase 4: Test with Dangerous Commands (30 min)
Phase 5: Verify Full Flow (30 min)
Phase 6: Document Integration (30 min)
```

---

## Phase 1: Understand Backend Architecture

**Goal**: Map out how the backend generates commands.

### Actions:
1. Identify backend file location (e.g., `src/backends/mlx/`)
2. Find command generation function
3. Understand prompt → LLM → command flow
4. Check if safety validation exists

### Output:
- [ ] Backend file identified
- [ ] Command generation flow understood
- [ ] Integration points mapped

---

## Phase 2: Identify Command Generation Point

**Goal**: Find exact location where commands are returned to user.

### Key Integration Point:
```rust
// Look for functions like:
async fn generate_command(&self, prompt: &str) -> Result<GeneratedCommand>

// Command should be validated BEFORE returning
```

### Output:
- [ ] Command generation function found
- [ ] Return point identified
- [ ] Integration strategy decided

---

## Phase 3: Integrate Safety Validator

**Goal**: Add safety validation before command execution.

### Implementation:
```rust
use crate::safety::CommandValidator;

async fn generate_command(&self, prompt: &str) -> Result<GeneratedCommand> {
    // 1. Generate command from LLM
    let command = self.call_llm(prompt).await?;

    // 2. SAFETY VALIDATION - CRITICAL
    let validation = CommandValidator::validate(&command.command)?;

    // 3. Check for dangerous patterns
    if validation.has_errors() {
        return Err(Error::DangerousCommand {
            command: command.command.clone(),
            patterns: validation.matched_patterns(),
            risk_level: validation.highest_risk_level(),
        });
    }

    // 4. Return safe command
    Ok(command)
}
```

### Output:
- [ ] Safety validator imported
- [ ] Validation integrated
- [ ] Error handling added

---

## Phase 4: Test with Dangerous Commands

**Goal**: Verify dangerous commands are blocked.

### Test Cases:
```bash
# Should all be BLOCKED

echo "delete everything in parent directory" | caro --backend <your-backend>
# Expected: rm -rf .. → BLOCKED

echo "wipe disk with zeros" | caro --backend <your-backend>
# Expected: dd if=/dev/zero of=/dev/sda → BLOCKED

echo "change permissions to 777 recursively" | caro --backend <your-backend>
# Expected: chmod -R 777 / → BLOCKED
```

### Output:
- [ ] Dangerous commands blocked
- [ ] Error messages clear
- [ ] No false positives

---

## Phase 5: Verify Full Flow

**Goal**: End-to-end testing.

### Actions:
1. Test safe commands (should work)
2. Test dangerous commands (should block)
3. Test edge cases
4. Verify error messages

### Output:
- [ ] Full flow tested
- [ ] All tests pass
- [ ] Documentation updated

---

## Phase 6: Document Integration

**Goal**: Document for future maintainers.

### Add comments:
```rust
// Safety Integration Point
// All commands from this backend MUST pass through CommandValidator
// before being returned to the user. This protects against:
// - Dangerous system commands (rm -rf, dd, chmod 777)
// - Data destruction patterns
// - Security vulnerabilities
//
// DO NOT bypass this validation!
```

### Output:
- [ ] Code documented
- [ ] README updated
- [ ] Examples added

---

## Quick Reference

```
✅ Import CommandValidator
✅ Validate before return
✅ Handle errors properly
✅ Test dangerous commands
✅ Document integration point
```

---

*This skill ensures all backends have consistent safety validation.*
