---
name: Test Nextflow Example Script
description: Test a Nextflow script by running it, verifying outputs, testing resume functionality, and comparing results with documentation. Use when validating that example scripts work correctly and match their documentation.
---

# Test Nextflow Example Script

Test a Nextflow example script and verify it matches the documentation.

See [../shared/repo-conventions.md](../shared/repo-conventions.md) for directory mapping.

## Working Directory

This skill works in two phases:

1. **Initial phase**: Start from repository root for finding scripts and reading documentation
2. **Execution phase**: Change to the script's directory for running Nextflow (ensures relative paths work)

Return to repository root after testing for final documentation checks.

## Tasks to Perform

1. **Identify the Script**

   - Ask user which script to test (or find recently modified .nf files)
   - Read the script to understand what it does
   - Note any `params.` definitions for testing

2. **Find Related Documentation**

   - Search docs/ for markdown files referencing this script
   - Identify what the documentation claims about outputs and behavior

3. **Run the Script**

   - Change to the script's directory
   - Run: `nextflow run [script.nf]`
   - Capture console output
   - Note the work directory hash

4. **Verify Outputs**

   - Check work directory for outputs
   - If publishDir used, check results/ directory
   - Compare actual output files with what documentation describes
   - Verify file contents match expectations

5. **Test with Resume**

   - Run: `nextflow run [script.nf] -resume`
   - Verify processes show as "cached"
   - Confirm work directory hash is reused

6. **Test with Parameters** (if applicable)

   - Identify parameters from script
   - Run with different parameter values
   - Verify outputs change appropriately

7. **Compare with Documentation**
   - Check console output matches documented examples
   - Verify commands shown in docs are correct
   - Ensure file paths referenced are accurate
   - Confirm expected outputs match reality

## Output Format

Provide a comprehensive test report:

```
# Test Report: [script.nf]

## Script Understanding
- Purpose: [what it does]
- Parameters: [list]
- Expected outputs: [list]

## Test Results

### Basic Run
✓ Script executed successfully
✓ Output files created: [list]
✓ Console output as expected

### Resume Test
✓ All processes cached
✓ Work directory reused

### Parameter Tests
✓ --param1 value: works correctly
[or issues found]

## Documentation Comparison

### Accurate
- Console output examples match
- File paths correct
- Command syntax verified

### Issues Found
- Line 123: Console output shows v25.04 but docs show v24.10
- Example missing --param flag
[or none]

## Recommendations
[Suggested documentation updates or script fixes]
```

## Notes

- Always run from the script's directory
- Save work directory paths for verification
- Test both success and documented failure cases
- If script doesn't work, report why but don't fail - that's useful information
