---
name: dev-workflow
version: "1.0.0"
category: _internal
description: "Development Workflow Skill"
---

# Development Workflow Skill

> Version: 1.0.0
> Category: Workflows
> Triggers: Implementing features, starting development, planning work

## Quick Reference

### 6-Phase Workflow

```
Phase 1: User Requirements (READ user_prompt.md)
   ↓
Phase 2: YAML Configuration (Transform to structured config)
   ↓
Phase 3: Pseudocode Review (Design algorithm, get approval)
   ↓
Phase 4: TDD Implementation (Write tests first)
   ↓
Phase 5: Code Implementation (Implement following spec)
   ↓
Phase 6: Bash Execution (Single command entry point)
```

## Phase 1: User Requirements

**File:** `user_prompt.md`

**AI Actions:**
- ✅ READ this file completely
- ✅ IDENTIFY ambiguous requirements
- ✅ ASK clarifying questions
- ✅ WAIT for user response
- ❌ NEVER EDIT this file
- ❌ NEVER DELETE this file

**User's Role:**
- Creates/updates user_prompt.md
- Reviews AI questions
- Provides guidance
- Approves approach

## Phase 2: YAML Configuration

**File:** `config/input/<feature-name>.yaml`

**Purpose:** Transform natural language to structured, machine-readable config

**AI Actions:**
- Read user_prompt.md
- Generate YAML with all parameters explicit
- Add comments for complex settings
- Ask about ambiguous choices
- Save to config/input/

**Structure:**
```yaml
metadata:
  feature: "feature-name"
  created: "2025-01-14"
  status: "draft"

requirements:
  input:
    - type: "csv"
    - path_type: "relative"
  processing:
    - calculate_statistics: true
  output:
    - format: "html"
    - interactive: true
  constraints:
    - max_response_time_sec: 5
```

**Before Generating, Ask:**
- What should be default values for X?
- Should Y be configurable or hardcoded?
- How should we handle Z edge case?

## Phase 3: Pseudocode Review

**File:** `docs/pseudocode/<feature-name>.md`

**Purpose:** Design algorithm before implementation

**Template:**
```
## Module: DataLoader

FUNCTION load_csv(file_path):
  VALIDATE file_path is relative
  CHECK file_size <= 100MB
  TRY:
    data = read_csv(file_path)
    RETURN data
  CATCH error:
    LOG error
    RAISE DataLoadError
```

**Before Generation, Ask:**
- Should we use algorithm A or B?
- How should we handle edge case X?
- What's priority: speed or memory efficiency?

**User's Role:**
- Reviews pseudocode
- Validates logic
- Approves or requests changes
- Signs off before implementation

## Phase 4: TDD Implementation

**Workflow:**
```
1. RED   → Write failing test
2. GREEN → Write minimal code to pass
3. REFACTOR → Improve code quality
4. REPEAT → For each feature
```

**Key Rules:**
- Tests written FIRST
- No code without test
- All tests pass before moving on
- Tests remain green during refactoring

**First Subtask:** Always "Write tests for [COMPONENT]"

## Phase 5: Code Implementation

**Follow:**
- Pseudocode design exactly
- Keep tests passing at ALL times
- Match surrounding code style
- Add comments for "why" not "what"

**Testing:**
- Run full test suite frequently
- Fix failures immediately
- Never commit broken tests

## Phase 6: Bash Execution

**Pattern:**
```bash
./scripts/run_feature.sh config/input/feature-name.yaml
```

**Requirements:**
- Single command entry point
- YAML file as input
- No complex tool chains
- Direct execution path

## Quick Command Reference

```bash
# 1. Read requirements
vim user_prompt.md

# 2. Generate config
./scripts/generate_config.sh user_prompt.md > config/input/feature.yaml
vim config/input/feature.yaml  # User reviews

# 3. Generate pseudocode
./scripts/generate_pseudocode.sh config/input/feature.yaml > docs/pseudocode/feature.md
# User reviews and approves

# 4-5. TDD and implementation
vim tests/unit/test_feature.py  # Write tests
./tests/run_tests.sh            # Run (should fail)
vim src/modules/feature/        # Implement
./tests/run_tests.sh            # Run (should pass)

# 6. Execute
./scripts/run_feature.sh config/input/feature.yaml
```

## Key Principles

### Never Skip Phases
✅ All 6 phases for every feature
❌ Don't jump from requirements to code

### TDD is Mandatory
✅ Test → Code → Refactor
❌ Code → Test (or no tests)

### Ask Before Proceeding
✅ Clarify ambiguous requirements
✅ Wait for user approval at each phase
❌ Make assumptions

### Documentation First
✅ Pseudocode approved before coding
❌ Implement first, design later

### Simple Solutions
✅ Minimal code to pass tests
✅ Refactor for clarity, not cleverness
❌ Over-engineer solutions

## Full Reference

See: @docs/modules/workflow/DEVELOPMENT_WORKFLOW.md

---

*Use this when starting feature implementation, planning development work, or reviewing workflow compliance.*
