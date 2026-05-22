---
name: add_platform.add_capabilities
description: "Updates job schema and adapters with any new hook events the platform supports. Use after research to extend DeepWork's hook system."
user-invocable: false
hooks:
  Stop:
    - hooks:
        - type: prompt
          prompt: |
            Verify the capability additions meet ALL criteria:
            1. Any new hooks from the platform (for slash commands only) are added to src/deepwork/schemas/job_schema.py
            2. All existing adapters in src/deepwork/adapters.py are updated with the new hook fields
               (set to None/null if the platform doesn't support that hook)
            3. Only hooks available on slash command definitions are added (not general CLI hooks)
            4. job_schema.py remains valid Python with no syntax errors
            5. adapters.py remains consistent - all adapters have the same hook fields
            6. If no new hooks are needed, document why in a comment

            If ALL criteria are met, include `<promise>✓ Quality Criteria Met</promise>`.

  SubagentStop:
    - hooks:
        - type: prompt
          prompt: |
            Verify the capability additions meet ALL criteria:
            1. Any new hooks from the platform (for slash commands only) are added to src/deepwork/schemas/job_schema.py
            2. All existing adapters in src/deepwork/adapters.py are updated with the new hook fields
               (set to None/null if the platform doesn't support that hook)
            3. Only hooks available on slash command definitions are added (not general CLI hooks)
            4. job_schema.py remains valid Python with no syntax errors
            5. adapters.py remains consistent - all adapters have the same hook fields
            6. If no new hooks are needed, document why in a comment

            If ALL criteria are met, include `<promise>✓ Quality Criteria Met</promise>`.

---

# add_platform.add_capabilities

**Step 2/4** in **add_platform** workflow

> Adds a new AI platform to DeepWork with adapter, templates, and tests. Use when integrating Cursor, Windsurf, or other AI coding tools.

## Prerequisites (Verify First)

Before proceeding, confirm these steps are complete:
- `/add_platform.research`

## Instructions

**Goal**: Updates job schema and adapters with any new hook events the platform supports. Use after research to extend DeepWork's hook system.

# Add Hook Capabilities

## Objective

Update the DeepWork job schema and platform adapters to support any new hook events that the new platform provides for slash command definitions.

## Task

Analyze the hooks documentation from the research step and update the codebase to support any new hook capabilities, ensuring consistency across all existing adapters.

### Prerequisites

Read the hooks documentation created in the previous step:
- `doc/platforms/<platform_name>/hooks_system.md`

Also review the existing schema and adapters:
- `src/deepwork/schemas/job_schema.py`
- `src/deepwork/adapters.py`

### Process

1. **Analyze the new platform's hooks**
   - Read `doc/platforms/<platform_name>/hooks_system.md`
   - List all hooks available for slash command definitions
   - Compare with hooks already in `job_schema.py`
   - Identify any NEW hooks not currently supported

2. **Determine if schema changes are needed**
   - If the platform has hooks that DeepWork doesn't currently support, add them
   - If all hooks are already supported, document this finding
   - Remember: Only add hooks that are available on slash command definitions

3. **Update job_schema.py (if needed)**
   - Add new hook fields to the step schema
   - Follow existing patterns for hook definitions
   - Add appropriate type hints and documentation
   - Example addition:
     ```python
     # New hook from <platform>
     new_hook_name: Optional[List[HookConfig]] = None
     ```

4. **Update all existing adapters**
   - Open `src/deepwork/adapters.py`
   - For EACH existing adapter class:
     - Add the new hook field (set to `None` if not supported)
     - This maintains consistency across all adapters
   - Document why each adapter does or doesn't support the hook

5. **Validate the changes**
   - Run Python syntax check: `python -m py_compile src/deepwork/schemas/job_schema.py`
   - Run Python syntax check: `python -m py_compile src/deepwork/adapters.py`
   - Ensure no import errors

6. **Document the decision**
   - If no new hooks were added, add a comment explaining why
   - If new hooks were added, ensure they're documented in the schema

## Output Format

### job_schema.py

Location: `src/deepwork/schemas/job_schema.py`

If new hooks are added:
```python
@dataclass
class StepDefinition:
    # ... existing fields ...

    # New hook from <platform_name> - [description of what it does]
    new_hook_name: Optional[List[HookConfig]] = None
```

### adapters.py

Location: `src/deepwork/adapters.py`

For each existing adapter, add the new hook field:
```python
class ExistingPlatformAdapter(PlatformAdapter):
    # ... existing code ...

    def get_hook_support(self) -> dict:
        return {
            # ... existing hooks ...
            "new_hook_name": None,  # Not supported by this platform
        }
```

Or if no changes are needed, add a documentation comment:
```python
# NOTE: <platform_name> hooks reviewed on YYYY-MM-DD
# No new hooks to add - all <platform_name> command hooks are already
# supported by the existing schema (stop_hooks covers their validation pattern)
```

## Quality Criteria

- Hooks documentation from research step has been reviewed
- If new hooks exist:
  - Added to `src/deepwork/schemas/job_schema.py` with proper typing
  - ALL existing adapters updated in `src/deepwork/adapters.py`
  - Each adapter indicates support level (implemented, None, or partial)
- If no new hooks needed:
  - Decision documented with a comment explaining the analysis
- Only hooks available on slash command definitions are considered
- `job_schema.py` has no syntax errors (verified with py_compile)
- `adapters.py` has no syntax errors (verified with py_compile)
- All adapters have consistent hook fields (same fields across all adapters)
- When all criteria are met, include `<promise>✓ Quality Criteria Met</promise>` in your response

## Context

DeepWork supports multiple AI platforms, and each platform may have different capabilities for hooks within command definitions. The schema defines what hooks CAN exist, while adapters define what each platform actually SUPPORTS.

This separation allows:
- Job definitions to use any hook (the schema is the superset)
- Platform-specific generation to only use supported hooks (adapters filter)
- Future platforms to add new hooks without breaking existing ones

Maintaining consistency is critical - all adapters must have the same hook fields, even if they don't support them (use `None` for unsupported).

## Common Hook Types

For reference, here are common hook patterns across platforms:

| Hook Type | Purpose | Example Platforms |
|-----------|---------|-------------------|
| `stop_hooks` | Quality validation loops | Claude Code |
| `pre_hooks` | Run before command | Various |
| `post_hooks` | Run after command | Various |
| `validation_hooks` | Validate inputs/outputs | Various |

When you find a new hook type, consider whether it maps to an existing pattern or is genuinely new functionality.


### Job Context

A workflow for adding support for a new AI platform (like Cursor, Windsurf, etc.) to DeepWork.

This job guides you through four phases:
1. **Research**: Capture the platform's CLI configuration and hooks system documentation
2. **Add Capabilities**: Update the job schema and adapters with any new hook events
3. **Implement**: Create the platform adapter, templates, tests (100% coverage), and README updates
4. **Verify**: Ensure installation works correctly and produces expected files

The workflow ensures consistency across all supported platforms and maintains
comprehensive test coverage for new functionality.

**Important Notes**:
- Only hooks available on slash command definitions should be captured
- Each existing adapter must be updated when new hooks are added (typically with null values)
- Tests must achieve 100% coverage for any new functionality
- Installation verification confirms the platform integrates correctly with existing jobs


## Required Inputs


**Files from Previous Steps** - Read these first:
- `hooks_system.md` (from `research`)

## Work Branch

Use branch format: `deepwork/add_platform-[instance]-YYYYMMDD`

- If on a matching work branch: continue using it
- If on main/master: create new branch with `git checkout -b deepwork/add_platform-[instance]-$(date +%Y%m%d)`

## Outputs

**Required outputs**:
- `job_schema.py`
- `adapters.py`

## Guardrails

- Do NOT skip prerequisite verification if this step has dependencies
- Do NOT produce partial outputs; complete all required outputs before finishing
- Do NOT proceed without required inputs; ask the user if any are missing
- Do NOT modify files outside the scope of this step's defined outputs

## Quality Validation

Stop hooks will automatically validate your work. The loop continues until all criteria pass.



**To complete**: Include `<promise>✓ Quality Criteria Met</promise>` in your final response only after verifying ALL criteria are satisfied.

## On Completion

1. Verify outputs are created
2. Inform user: "Step 2/4 complete, outputs: job_schema.py, adapters.py"
3. **Continue workflow**: Use Skill tool to invoke `/add_platform.implement`

---

**Reference files**: `.deepwork/jobs/add_platform/job.yml`, `.deepwork/jobs/add_platform/steps/add_capabilities.md`