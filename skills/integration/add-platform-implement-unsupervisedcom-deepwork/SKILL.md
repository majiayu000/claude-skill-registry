---
name: add_platform.implement
description: "Creates platform adapter, templates, tests with 100% coverage, and README documentation. Use after adding hook capabilities."
user-invocable: false
hooks:
  Stop:
    - hooks:
        - type: command
          command: ".deepwork/jobs/add_platform/hooks/run_tests.sh"
        - type: prompt
          prompt: |
            Verify the implementation meets ALL criteria:
            1. Platform adapter class is added to src/deepwork/adapters.py
            2. Templates exist in src/deepwork/templates/<platform>/ with appropriate command structure
            3. Tests exist for all new functionality
            4. Test coverage is 100% for new code (run: uv run pytest --cov)
            5. All tests pass
            6. README.md is updated with:
               - New platform listed in supported platforms
               - Installation instructions for the platform
               - Any platform-specific notes

            If ALL criteria are met, include `<promise>✓ Quality Criteria Met</promise>`.

  SubagentStop:
    - hooks:
        - type: command
          command: ".deepwork/jobs/add_platform/hooks/run_tests.sh"
        - type: prompt
          prompt: |
            Verify the implementation meets ALL criteria:
            1. Platform adapter class is added to src/deepwork/adapters.py
            2. Templates exist in src/deepwork/templates/<platform>/ with appropriate command structure
            3. Tests exist for all new functionality
            4. Test coverage is 100% for new code (run: uv run pytest --cov)
            5. All tests pass
            6. README.md is updated with:
               - New platform listed in supported platforms
               - Installation instructions for the platform
               - Any platform-specific notes

            If ALL criteria are met, include `<promise>✓ Quality Criteria Met</promise>`.

---

# add_platform.implement

**Step 3/4** in **add_platform** workflow

> Adds a new AI platform to DeepWork with adapter, templates, and tests. Use when integrating Cursor, Windsurf, or other AI coding tools.

## Prerequisites (Verify First)

Before proceeding, confirm these steps are complete:
- `/add_platform.research`
- `/add_platform.add_capabilities`

## Instructions

**Goal**: Creates platform adapter, templates, tests with 100% coverage, and README documentation. Use after adding hook capabilities.

# Implement Platform Support

## Objective

Create the complete platform implementation including the adapter class, command templates, comprehensive tests, and documentation updates.

## Task

Build the full platform support by implementing the adapter, creating templates, writing tests with 100% coverage, and updating the README.

### Prerequisites

Read the outputs from previous steps:
- `doc/platforms/<platform_name>/cli_configuration.md` - For template structure
- `src/deepwork/schemas/job_schema.py` - For current schema
- `src/deepwork/adapters.py` - For adapter patterns

Also review existing implementations for reference:
- `src/deepwork/templates/claude/` - Example templates
- `tests/` - Existing test patterns

### Process

1. **Create the platform adapter class**

   Add a new adapter class to `src/deepwork/adapters.py`:

   ```python
   class NewPlatformAdapter(PlatformAdapter):
       """Adapter for <Platform Name>."""

       platform_name = "<platform_name>"
       command_directory = "<path to commands>"  # e.g., ".cursor/commands"
       command_extension = ".md"  # or appropriate extension

       def get_hook_support(self) -> dict:
           """Return which hooks this platform supports."""
           return {
               "stop_hooks": True,  # or False/None
               # ... other hooks
           }

       def generate_command(self, step: StepDefinition, job: JobDefinition) -> str:
           """Generate command file content for this platform."""
           # Use Jinja2 template
           template = self.env.get_template(f"{self.platform_name}/command.md.j2")
           return template.render(step=step, job=job)
   ```

2. **Create command templates**

   Create templates in `src/deepwork/templates/<platform_name>/`:

   - `command.md.j2` - Main command template
   - Any other templates needed for the platform's format

   Use the CLI configuration documentation to ensure the template matches the platform's expected format.

3. **Register the adapter**

   Update the adapter registry in `src/deepwork/adapters.py`:

   ```python
   PLATFORM_ADAPTERS = {
       "claude": ClaudeAdapter,
       "<platform_name>": NewPlatformAdapter,
       # ... other adapters
   }
   ```

4. **Write comprehensive tests**

   Create tests in `tests/` that cover:

   - Adapter instantiation
   - Hook support detection
   - Command generation
   - Template rendering
   - Edge cases (empty inputs, special characters, etc.)
   - Integration with the sync command

   **Critical**: Tests must achieve 100% coverage of new code.

5. **Update README.md**

   Add the new platform to `README.md`:

   - Add to "Supported Platforms" list
   - Add installation instructions:
     ```bash
     deepwork install --platform <platform_name>
     ```
   - Document any platform-specific notes or limitations

6. **Run tests and verify coverage**

   ```bash
   uv run pytest --cov=src/deepwork --cov-report=term-missing
   ```

   - All tests must pass
   - New code must have 100% coverage
   - If coverage is below 100%, add more tests

7. **Iterate until tests pass with full coverage**

   This step has a `stop_hooks` script that runs tests. Keep iterating until:
   - All tests pass
   - Coverage is 100% for new functionality

## Output Format

### templates/

Location: `src/deepwork/templates/<platform_name>/`

Create the following files:

**command.md.j2**:
```jinja2
{# Template for <platform_name> command files #}
{# Follows the platform's expected format from cli_configuration.md #}

[Platform-specific frontmatter or metadata]

# {{ step.name }}

{{ step.description }}

## Instructions

{{ step.instructions_content }}

[... rest of template based on platform format ...]
```

### tests/

Location: `tests/test_<platform_name>_adapter.py`

```python
"""Tests for the <platform_name> adapter."""
import pytest
from deepwork.adapters import NewPlatformAdapter

class TestNewPlatformAdapter:
    """Test suite for NewPlatformAdapter."""

    def test_adapter_initialization(self):
        """Test adapter can be instantiated."""
        adapter = NewPlatformAdapter()
        assert adapter.platform_name == "<platform_name>"

    def test_hook_support(self):
        """Test hook support detection."""
        adapter = NewPlatformAdapter()
        hooks = adapter.get_hook_support()
        assert "stop_hooks" in hooks
        # ... more assertions

    def test_command_generation(self):
        """Test command file generation."""
        # ... test implementation

    # ... more tests for 100% coverage
```

### README.md

Add to the existing README.md:

```markdown
## Supported Platforms

- **Claude Code** - Anthropic's CLI for Claude
- **<Platform Name>** - [Brief description]

## Installation

### <Platform Name>

```bash
deepwork install --platform <platform_name>
```

[Any platform-specific notes]
```

## Quality Criteria

- Platform adapter class added to `src/deepwork/adapters.py`:
  - Inherits from `PlatformAdapter`
  - Implements all required methods
  - Registered in `PLATFORM_ADAPTERS`
- Templates created in `src/deepwork/templates/<platform_name>/`:
  - `command.md.j2` exists and renders correctly
  - Format matches platform's expected command format
- Tests created in `tests/`:
  - Cover all new adapter functionality
  - Cover template rendering
  - All tests pass
- Test coverage is 100% for new code:
  - Run `uv run pytest --cov=src/deepwork --cov-report=term-missing`
  - No uncovered lines in new code
- README.md updated:
  - Platform listed in supported platforms
  - Installation command documented
  - Any platform-specific notes included
- When all criteria are met, include `<promise>✓ Quality Criteria Met</promise>` in your response

## Context

This is the core implementation step. The adapter you create will be responsible for:
- Determining where command files are placed
- Generating command file content from job definitions
- Handling platform-specific features and hooks

The templates use Jinja2 and should produce files that match exactly what the platform expects. Reference the CLI configuration documentation frequently to ensure compatibility.

## Tips

- Study the existing `ClaudeAdapter` as a reference implementation
- Run tests frequently as you implement
- Use `--cov-report=html` for a detailed coverage report
- If a test is hard to write, the code might need refactoring
- Template syntax errors often show up at runtime - test early


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
- `job_schema.py` (from `add_capabilities`)
- `adapters.py` (from `add_capabilities`)
- `cli_configuration.md` (from `research`)

## Work Branch

Use branch format: `deepwork/add_platform-[instance]-YYYYMMDD`

- If on a matching work branch: continue using it
- If on main/master: create new branch with `git checkout -b deepwork/add_platform-[instance]-$(date +%Y%m%d)`

## Outputs

**Required outputs**:
- `templates/` (directory)
- `tests/` (directory)
- `README.md`

## Guardrails

- Do NOT skip prerequisite verification if this step has dependencies
- Do NOT produce partial outputs; complete all required outputs before finishing
- Do NOT proceed without required inputs; ask the user if any are missing
- Do NOT modify files outside the scope of this step's defined outputs

## Quality Validation

Stop hooks will automatically validate your work. The loop continues until all criteria pass.


**Validation script**: `.deepwork/jobs/add_platform/hooks/run_tests.sh` (runs automatically)

**To complete**: Include `<promise>✓ Quality Criteria Met</promise>` in your final response only after verifying ALL criteria are satisfied.

## On Completion

1. Verify outputs are created
2. Inform user: "Step 3/4 complete, outputs: templates/, tests/, README.md"
3. **Continue workflow**: Use Skill tool to invoke `/add_platform.verify`

---

**Reference files**: `.deepwork/jobs/add_platform/job.yml`, `.deepwork/jobs/add_platform/steps/implement.md`