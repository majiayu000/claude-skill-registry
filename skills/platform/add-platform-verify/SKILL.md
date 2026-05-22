---
name: add_platform.verify
description: "Sets up platform directories and verifies deepwork install works correctly. Use after implementation to confirm integration."
user-invocable: false

---

# add_platform.verify

**Step 4/4** in **integrate** workflow

> Full workflow to integrate a new AI platform into DeepWork

> Adds a new AI platform to DeepWork with adapter, templates, and tests. Use when integrating Cursor, Windsurf, or other AI coding tools.

## Prerequisites (Verify First)

Before proceeding, confirm these steps are complete:
- `/add_platform.implement`

## Instructions

**Goal**: Sets up platform directories and verifies deepwork install works correctly. Use after implementation to confirm integration.

# Verify Installation

## Objective

Ensure the new platform integration works correctly by setting up necessary directories and running the full installation process.

## Task

Perform end-to-end verification that the new platform can be installed and that DeepWork's standard jobs work correctly with it.

### Prerequisites

Ensure the implementation step is complete:
- Adapter class exists in `src/deepwork/adapters.py`
- Templates exist in `src/deepwork/templates/<platform_name>/`
- Tests pass with 100% coverage
- README.md is updated

### Process

1. **Set up platform directories in the DeepWork repo**

   The DeepWork repository itself should have the platform's command directory structure for testing:

   ```bash
   mkdir -p <platform_command_directory>
   ```

   For example:
   - Claude: `.claude/commands/`
   - Cursor: `.cursor/commands/` (or wherever Cursor stores commands)

2. **Run deepwork install for the new platform**

   ```bash
   deepwork install --platform <platform_name>
   ```

   Verify:
   - Command completes without errors
   - No Python exceptions or tracebacks
   - Output indicates successful installation

3. **Check that command files were created**

   List the generated command files:
   ```bash
   ls -la <platform_command_directory>/
   ```

   Verify:
   - `deepwork_jobs.define.md` exists (or equivalent for the platform)
   - `deepwork_jobs.implement.md` exists
   - `deepwork_jobs.refine.md` exists
   - `deepwork_rules.define.md` exists
   - All expected step commands exist

4. **Validate command file content**

   Read each generated command file and verify:
   - Content matches the expected format for the platform
   - Job metadata is correctly included
   - Step instructions are properly rendered
   - Any platform-specific features (hooks, frontmatter) are present

5. **Test alongside existing platforms**

   If other platforms are already installed, verify they still work:
   ```bash
   deepwork install --platform claude
   ls -la .claude/commands/
   ```

   Ensure:
   - New platform doesn't break existing installations
   - Each platform's commands are independent
   - No file conflicts or overwrites

## Quality Criteria

- Platform-specific directories are set up in the DeepWork repo
- `deepwork install --platform <platform_name>` completes without errors
- All expected command files are created:
  - deepwork_jobs.define, implement, refine
  - deepwork_rules.define
  - Any other standard job commands
- Command file content is correct:
  - Matches platform's expected format
  - Job/step information is properly rendered
  - No template errors or missing content
- Existing platforms still work (if applicable)
- No conflicts between platforms
- When all criteria are met, include `<promise>✓ Quality Criteria Met</promise>` in your response

## Context

This is the final validation step before the platform is considered complete. A thorough verification ensures:
- The platform actually works, not just compiles
- Standard DeepWork jobs install correctly
- The platform integrates properly with the existing system
- Users can confidently use the new platform

Take time to verify each aspect - finding issues now is much better than having users discover them later.

## Common Issues to Check

- **Template syntax errors**: May only appear when rendering specific content
- **Path issues**: Platform might expect different directory structure
- **Encoding issues**: Special characters in templates or content
- **Missing hooks**: Platform adapter might not handle all hook types
- **Permission issues**: Directory creation might fail in some cases


### Job Context

A workflow for adding support for a new AI platform (like Cursor, Windsurf, etc.) to DeepWork.

The **integrate** workflow guides you through four phases:
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
- `templates/` (from `implement`)

## Work Branch

Use branch format: `deepwork/add_platform-[instance]-YYYYMMDD`

- If on a matching work branch: continue using it
- If on main/master: create new branch with `git checkout -b deepwork/add_platform-[instance]-$(date +%Y%m%d)`

## Outputs

**Required outputs**:
- `verification_checklist.md`

## Guardrails

- Do NOT skip prerequisite verification if this step has dependencies
- Do NOT produce partial outputs; complete all required outputs before finishing
- Do NOT proceed without required inputs; ask the user if any are missing
- Do NOT modify files outside the scope of this step's defined outputs

## On Completion

1. Verify outputs are created
2. Inform user: "integrate step 4/4 complete, outputs: verification_checklist.md"
3. **integrate workflow complete**: All steps finished. Consider creating a PR to merge the work branch.

---

**Reference files**: `.deepwork/jobs/add_platform/job.yml`, `.deepwork/jobs/add_platform/steps/verify.md`