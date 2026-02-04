---
name: qwen_cli_refactor
description: Strategic CLI refactoring using Qwen 1.5B for extracting command modules from monolithic main() functions
version: 1.0.0
author: 0102_infrastructure_team
agents: [qwen, gemma]
dependencies: [pattern_memory, wre_core]
domain: code_refactoring
intent_type: REFACTORING
promotion_state: prototype
pattern_fidelity_threshold: 0.90
---

# Qwen CLI Refactoring Skill

**Agent**: Qwen 1.5B (strategic analysis + code extraction)
**Validation**: Gemma 270M (pattern fidelity check)
**Token Budget**: 1,300 tokens (800 extraction + 400 refactoring + 100 validation)

---

## Skill Purpose

Refactor monolithic CLI files (>1,000 lines) by extracting logical command modules while preserving all functionality. Uses Qwen for strategic analysis and module extraction, with Gemma validation for pattern fidelity.

**Trigger Source**: Manual invocation by 0102 when CLI files exceed WSP 49 limits

**Success Criteria**:
- Reduce main() function size by >70%
- Extract 5+ independent command modules
- Zero regressions (all flags work identically)
- Pattern fidelity >90% (Gemma validation)

---

## Input Context

```json
{
  "file_path": "path/to/cli.py",
  "current_lines": 1470,
  "main_function_lines": 1144,
  "target_reduction_percent": 70,
  "preserve_flags": ["--search", "--index", "--all-67-flags"],
  "output_directory": "path/to/cli/commands/"
}
```

---

## Micro Chain-of-Thought Steps

### Step 1: Analyze CLI Structure (200 tokens)

**Qwen Analysis Task**:
Read cli.py and identify:
1. Command-line argument groups (search, index, holodae, etc.)
2. Logical sections in main() function
3. Shared dependencies between sections
4. Natural module boundaries

**Output**:
```json
{
  "total_lines": 1470,
  "main_function_lines": 1144,
  "argument_groups": [
    {"name": "search", "flags": ["--search", "--limit"], "lines": [601, 750]},
    {"name": "index", "flags": ["--index-all", "--index-code"], "lines": [751, 900]},
    {"name": "holodae", "flags": ["--start-holodae", "--stop-holodae"], "lines": [901, 1050]},
    {"name": "module", "flags": ["--link-modules", "--query-modules"], "lines": [1051, 1200]},
    {"name": "codeindex", "flags": ["--code-index-report"], "lines": [1201, 1350]}
  ],
  "shared_dependencies": ["throttler", "reward_events", "args"],
  "extraction_priority": ["search", "index", "holodae", "module", "codeindex"]
}
```

---

### Step 2: Extract Command Modules (400 tokens)

**Qwen Extraction Task**:
For each command group:
1. Extract code from main() function
2. Create `commands/{name}.py` file
3. Convert to class-based command pattern
4. Preserve all flag handling logic

**Template Pattern**:
```python
# commands/search.py
from typing import Any, Dict
from ..core import HoloIndex

class SearchCommand:
    def __init__(self, holo_index: HoloIndex):
        self.holo_index = holo_index

    def execute(self, args, throttler, add_reward_event) -> Dict[str, Any]:
        \"\"\"Execute search command with preserved flag logic\"\"\"
        # [EXTRACTED CODE FROM MAIN() LINES 601-750]
        results = self.holo_index.search(args.search, limit=args.limit)
        return {"results": results, "success": True}
```

**Output**: 5 new command module files created

---

### Step 3: Refactor main() Function (200 tokens)

**Qwen Refactoring Task**:
1. Remove extracted code from main()
2. Add command routing logic
3. Instantiate command classes
4. Delegate execution to appropriate command

**New main() Structure**:
```python
def main() -> None:
    args = parser.parse_args()
    throttler = AgenticOutputThrottler()

    # Initialize HoloIndex
    holo_index = HoloIndex(...)

    # Command routing
    if args.search:
        from .commands.search import SearchCommand
        cmd = SearchCommand(holo_index)
        result = cmd.execute(args, throttler, add_reward_event)
    elif args.index or args.index_all:
        from .commands.index import IndexCommand
        cmd = IndexCommand(holo_index)
        result = cmd.execute(args, throttler, add_reward_event)
    # ... etc for other commands

    # Render output (preserved logic)
    render_response(throttler, result, args)
```

**Output**: Refactored main.py (reduced from 1,144 → ~300 lines)

---

### Step 4: Gemma Pattern Fidelity Validation (100 tokens)

**Gemma Validation Task**:
Compare original vs refactored:
1. All 67 flags still recognized
2. Execution flow unchanged
3. Output format identical
4. No missing imports

**Validation Checks**:
```python
original_flags = extract_flags("cli.py")
refactored_flags = extract_flags("cli/main.py") + extract_flags("cli/commands/*.py")

assert set(original_flags) == set(refactored_flags), "Missing flags detected"
assert pattern_fidelity >= 0.90, "Pattern fidelity below threshold"
```

**Output**:
```json
{
  "pattern_fidelity": 0.95,
  "flags_preserved": 67,
  "missing_flags": [],
  "regressions_detected": 0,
  "validation_passed": true
}
```

---

### Step 5: Generate Migration Report (100 tokens)

**Report Contents**:
1. Files created (5 command modules)
2. main() reduction (1,144 → 300 lines, 74% reduction)
3. Validation results (fidelity: 95%)
4. Token cost (actual vs estimated)
5. Next steps (testing, documentation)

**Output**:
```markdown
# CLI Refactoring Report

**Date**: 2025-10-25
**File**: holo_index/cli.py
**Status**: COMPLETE ✅

## Changes Summary
- main() reduced: 1,144 → 300 lines (74% reduction)
- Command modules created: 5
- Total lines: 1,470 → 1,350 (distributed across 6 files)
- Pattern fidelity: 95% (Gemma validated)

## Files Created
1. cli/commands/search.py (200 lines)
2. cli/commands/index.py (180 lines)
3. cli/commands/holodae.py (190 lines)
4. cli/commands/module.py (210 lines)
5. cli/commands/codeindex.py (170 lines)

## Validation
- ✅ All 67 flags preserved
- ✅ Zero regressions detected
- ✅ Pattern fidelity: 95%
- ✅ Imports resolved

## Token Cost
- Estimated: 1,300 tokens
- Actual: 1,150 tokens (12% under budget)

## Next Steps
1. Run integration tests
2. Update documentation
3. Commit with 0102 approval
```

---

## Execution Constraints

### Authorized Actions (Autonomous)
- ✅ Create new files in `cli/commands/` directory
- ✅ Extract code from main() function
- ✅ Update imports in main.py
- ✅ Run Gemma validation checks

### Requires 0102 Approval
- ❌ Modifying flag names
- ❌ Removing any flags
- ❌ Changing command behavior
- ❌ Committing changes to git

### Safety Guardrails
1. **Backup**: Create `cli.py.backup` before modification
2. **Validation**: Gemma fidelity must be ≥90%
3. **Rollback**: Restore backup if validation fails
4. **Reporting**: Report progress after each extraction

---

## Pattern Memory Storage

After successful execution, store refactoring pattern:

```json
{
  "pattern_name": "cli_refactoring",
  "original_size": 1470,
  "refactored_size": 1350,
  "main_reduction": 0.74,
  "modules_extracted": 5,
  "token_cost": 1150,
  "fidelity": 0.95,
  "success": true,
  "learned": "Extract commands by flag groups, preserve shared state via dependency injection"
}
```

---

## Example Invocation

**Via WRE Master Orchestrator**:
```python
from modules.infrastructure.wre_core.wre_master_orchestrator import WREMasterOrchestrator

orchestrator = WREMasterOrchestrator()

result = orchestrator.execute_skill(
    skill_name="qwen_cli_refactor",
    agent="qwen",
    input_context={
        "file_path": "holo_index/cli.py",
        "current_lines": 1470,
        "main_function_lines": 1144,
        "target_reduction_percent": 70,
        "output_directory": "holo_index/cli/commands/"
    }
)

print(f"Refactoring {'succeeded' if result['success'] else 'failed'}")
print(f"Pattern fidelity: {result['pattern_fidelity']}")
print(f"Token cost: {result['token_cost']}")
```

---

## WSP Compliance

**References**:
- WSP 49: Module Structure (file size limits)
- WSP 72: Block Independence (command isolation)
- WSP 50: Pre-Action Verification (backup before modification)
- WSP 96: WRE Skills Protocol (this skill definition)

---

## Success Metrics

| Metric | Target | Actual (Expected) |
|--------|--------|-------------------|
| main() reduction | >70% | 74% |
| Modules extracted | 5 | 5 |
| Pattern fidelity | >90% | 95% |
| Token cost | <1,500 | 1,150 |
| Regressions | 0 | 0 |

**Next Evolution**: After 10+ successful executions, promote from prototype → production
