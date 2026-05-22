---
name: java-enforce-logrecords
description: Enforce CUI logging standards by validating LogRecord usage, testing coverage, and identifier organization
user-invocable: true
allowed-tools: Skill, Read, Write, Edit, Glob, Grep, Bash, Task
---

# Log Record Enforcer Skill

Comprehensive diagnostic and automation command that enforces CUI logging standards across Java modules. Validates that INFO/WARN/ERROR/FATAL use LogRecord, DEBUG/TRACE use direct logger, all LogRecords are tested with LogAssert, and identifiers are properly organized.

## CONTINUOUS IMPROVEMENT RULE

If you discover issues or improvements during execution, record them:

1. **Activate skill**: `Skill: plan-marshall:manage-lessons`
2. **Record lesson** with:
   - Component: `{type: "command", name: "java-enforce-logrecords", bundle: "pm-dev-java"}`
   - Category: bug | improvement | pattern | anti-pattern
   - Summary and detail of the finding

## PARAMETERS

**module** - (Optional) Module name for multi-module projects; if unset, assume single-module and verify

## WORKFLOW

### Step 1: Verify Module Parameter

**Determine project structure:**

1. Activate `plan-marshall:manage-run-config` skill to check for module configuration:
   ```
   Skill: plan-marshall:manage-run-config
   Workflow: Read Configuration
   Field: commands.java-enforce-logrecords.modules
   ```
2. If exists, check for multiple modules
3. If parameter unset:
   - Single-module: Proceed with entire project
   - Multi-module: List available modules and ask user which to analyze

**Module validation:**
- If module parameter provided, verify it exists using Grep in pom.xml files
- If module not found, report error and stop
- Store validated module name for subsequent steps

### Step 2: Verify Build Precondition

Execute build verification (see Build Verification Protocol in CRITICAL RULES).

If build fails, report to caller and stop execution.

### Step 3: Load Configuration and Logging Standards

**Read configuration:**
1. Activate `plan-marshall:manage-run-config` skill:
   ```
   Skill: plan-marshall:manage-run-config
   Workflow: Read Configuration
   Field: commands.java-enforce-logrecords.modules.{module-name}
   ```
2. Extract `logmessages_classes` array
3. Extract `logmessages_documentation` array

**Load logging standards:**
```
Skill: pm-dev-java-cui:cui-logging
```

This loads:
- `standards/logging-standards.md` - LogRecord usage rules
- `standards/logmessages-documentation.md` - Documentation requirements

**Configuration structure (JSON):**
```json
{
  "commands": {
    "java-enforce-logrecords": {
      "modules": {
        "{module-name}": {
          "logmessages_classes": [
            {"package": "com.example.auth", "class": "AuthenticationLogMessages"},
            {"package": "com.example.token", "class": "TokenLogMessages"}
          ],
          "logmessages_documentation": ["doc/LogMessages.adoc"]
        }
      }
    }
  }
}
```

**If configuration missing or incomplete:**
- Attempt to locate LogMessages classes using Glob: `**/*LogMessages.java`
- Attempt to locate LogMessages.adoc using Glob: `**/LogMessages.adoc`
- If still uncertain (confidence < 100%), ask user for help
- Store results using `plan-marshall:manage-run-config` skill:
  ```
  Skill: plan-marshall:manage-run-config
  Workflow: Update Configuration
  Field: commands.java-enforce-logrecords.modules.{module}
  ```

### Step 4: Find and Analyze Logging Violations

**Use `pm-dev-java-cui:cui-logging` skill workflow:**

Execute workflow: Analyze Logging Violations
- target: {module path or project root}

Or run script directly:
```bash
scripts/analyze-logging-violations.py --directory {target}
```

**Script returns structured violations:**
- File locations and line numbers
- Violation types (MISSING_LOG_RECORD, INCORRECT_LOG_RECORD_USAGE)
- Current vs expected usage
- Summary counts

This uses the `pm-dev-java-cui:cui-logging` skill workflow for structured logging standards validation.

### Step 5: Verify LogRecord Usage and Test Coverage

**Analyze LogRecord coverage:**

For each LogMessages class, apply coverage analysis patterns from `pm-dev-java-cui:cui-logging` skill:
- Extract all LogRecord definitions (Pattern 6)
- Find production usage with Grep (Pattern 7)
- Find test coverage with LogAssert (Pattern 8)
- Determine coverage status (Pattern 9)

**Coverage Actions:**
- No references → Remove (unused)
- Production only → Add tests
- Test only → USER REVIEW (critical bug)
- Both → Compliant

See: `standards/logging-enforcement-patterns.md` → Patterns 6-9 (Coverage Analysis)

### Step 6: Generate Execution Plan

**Aggregate findings:**

1. **Group violations by type:**
   - Missing LogRecord (INFO/WARN/ERROR/FATAL using direct string)
   - Prohibited LogRecord (DEBUG/TRACE using LogRecord)

2. **Group LogRecord issues:**
   - Unused LogRecords (no references)
   - Untested LogRecords (production only)
   - Test-only LogRecords (critical bugs)

3. **Create batched work plan:**
   - Batch 1: Fix logging statement violations (/java-implement-code)
   - Batch 2: Remove unused LogRecords (/java-implement-code)
   - Batch 3: Add missing LogAsserts (/java-implement-tests)
   - Batch 4: User review for test-only LogRecords

**Plan format:**
```
ENFORCEMENT PLAN
================

Total Violations: {count}
Total LogRecord Issues: {count}

Batch 1: Fix Logging Statements
- {count} missing LogRecord conversions
- {count} prohibited LogRecord removals
- Command: /java-implement-code

Batch 2: Remove Unused LogRecords
- {count} unused LogRecord definitions
- Command: /java-implement-code

Batch 3: Add Test Coverage
- {count} untested LogRecords
- Command: /java-implement-tests

Batch 4: User Review Required
- {count} test-only LogRecords (critical)
```

### Step 7: Execute Corrections

**Execute batches using agent coordination patterns:**

Follow batch execution templates from `pm-dev-java-cui:cui-logging` skill (Pattern 11).

**Batch 1:** Fix logging violations using /java-implement-code
- Pass violations list with file locations and required corrections
- Verify compilation

**Batch 2:** Remove unused LogRecords using /java-implement-code
- Pass list of unused LogRecords with locations
- Verify compilation

**Batch 3:** Add LogAssert tests using /java-implement-tests
- Pass untested LogRecords with production usage locations
- Use @EnableTestLogger and LogAsserts
- Verify tests pass

**Batch 4:** User review for test-only LogRecords
- Report test-only LogRecords as critical bugs
- Stop execution and await user guidance
- Options: Add production code or remove tests

See: `standards/logging-enforcement-patterns.md` → Pattern 11 (Batch Templates)

### Step 8: Verify Corrections

Execute build verification (see Build Verification Protocol in CRITICAL RULES).

If verification fails, report details and stop execution.

### Step 9: Review and Renumber LogMessages Identifiers

**Apply identifier numbering validation:**

For each LogMessages class:
1. Extract all identifiers with levels
2. Check for gaps, ordering issues, and range compliance
3. Apply renumbering if needed using /java-implement-code
4. Verify no DEBUG/TRACE LogRecords exist

**Standard ranges** (from logging-standards.md):
- INFO: 001-099, WARN: 100-199, ERROR: 200-299, FATAL: 300-399

See: `logging-standards.md` → Message Identifier Ranges
See: `logging-enforcement-patterns.md` → Patterns 13-14 (Identifier Validation)

### Step 10: Update LogMessages Documentation

**Synchronize documentation with code changes:**

For each LogMessages class that was modified:
1. Determine fully qualified class name from file path
2. Locate corresponding LogMessages.adoc file (from configuration in Step 3)
3. Execute documentation workflow

**Execute documentation update using `pm-dev-java-cui:cui-logging` skill workflow:**

Execute workflow: Document LogRecord
- holder_class: {path-to-java-file}
- output_file: {path-to-adoc-file}

Or run script directly:
```bash
scripts/document-logrecord.py --holder {holder_class} --output {output_file}
```

**Verification:**
- Check script completed successfully
- Verify AsciiDoc file was updated
- Ensure all LogRecords are documented

**Error handling:**
- If script fails: Report warning but continue (documentation is secondary to code correctness)
- If AsciiDoc path not found: Skip documentation update and report warning

### Step 11: Final Verification and Report

Execute final build verification (see Build Verification Protocol in CRITICAL RULES).

**Generate summary report:**

```
═══════════════════════════════════════════════════════════════
LOG RECORD ENFORCEMENT COMPLETE
═══════════════════════════════════════════════════════════════

Module: {module-name or "all modules"}

VIOLATIONS FIXED:
- Logging statements corrected: {count}
  • Missing LogRecord (INFO/WARN/ERROR/FATAL): {count}
  • Prohibited LogRecord (DEBUG/TRACE): {count}

LOGRECORD MAINTENANCE:
- Unused LogRecords removed: {count}
- LogAssert tests added: {count}
- Identifiers renumbered: {count}

IDENTIFIER VERIFICATION:
✓ INFO level (001-099): {count} messages, consecutive ordering
✓ WARN level (100-199): {count} messages, consecutive ordering
✓ ERROR level (200-299): {count} messages, consecutive ordering
✓ FATAL level (300-399): {count} messages, consecutive ordering
✓ No DEBUG/TRACE LogRecords found

BUILD STATUS: {SUCCESS/FAILURE}

{If failures: List remaining errors or warnings}

COMPLIANCE STATUS: {COMPLIANT / ISSUES REMAINING}

═══════════════════════════════════════════════════════════════
```

## CRITICAL RULES

**Module Handling:**
- ALWAYS verify module parameter for multi-module projects
- Ask user if module unset and project is multi-module
- Use module parameter in all Maven build commands

**Build Verification Protocol:**
- Execute at Steps 2, 8, and 11
- Use builder-maven-rules skill workflow:
  ```
  Skill: pm-dev-builder:builder-maven-rules
  Workflow: Execute Maven Build
  Parameters:
    goals: clean verify
    module: {module if specified}
    output_mode: errors
  ```
- Success criteria: Exit code 0, zero errors, zero test failures
- On failure: Report details (errors, test failures) and stop execution
- See: `logging-enforcement-patterns.md` → Pattern 15

**Configuration Management:**
- Use `plan-marshall:manage-run-config` skill for all configuration access
- Read path: `commands.java-enforce-logrecords.modules`
- Store LogMessages class and documentation locations in JSON structure
- Ask user for help if locations uncertain (< 100% confidence)
- Update configuration for future executions

**Violation Detection:**
- Use `pm-dev-java-cui:cui-logging` skill workflow: Analyze Logging Violations
- Script handles: finding statements, determining LogRecord usage, applying rules
- Receive structured violations with file locations and types
- Process violation data for batched fixes

**LogRecord Validation Rules:**
- INFO/WARN/ERROR/FATAL: LogRecord REQUIRED → violation if missing
- DEBUG/TRACE: Direct string REQUIRED → violation if LogRecord present
- Every LogRecord MUST have production usage
- Every LogRecord MUST have test coverage (LogAssert)

**Coverage Analysis:**
- No references → Remove LogRecord (unused)
- Production only → Add LogAssert test
- Test only → USER REVIEW REQUIRED (critical bug)
- Both references → Compliant

**Agent Coordination:**
- Use /java-implement-code for production code changes
- Use /java-implement-tests for LogAssert test implementation
- Use Bash + parse-maven-output.py for all build verifications
- Execute commands in batches (grouped by change type)

**Identifier Management:**
- Standard ranges (from logging-standards.md): INFO 001-099, WARN 100-199, ERROR 200-299, FATAL 300-399
- NO identifiers for DEBUG/TRACE (prohibited)
- Renumber to eliminate gaps and ensure consecutive ordering

**Documentation Synchronization:**
- Update LogMessages.adoc when identifiers change
- Verify documentation matches implementation
- Include documentation updates in same batch as code changes

**User Interaction:**
- Ask for module selection if multi-module and parameter unset
- Ask for help if LogMessages locations uncertain
- Stop and request guidance if test-only LogRecords found
- Report all failures immediately (don't continue with broken code)

## USAGE EXAMPLES

**Single-module project:**
```
/java-enforce-logrecords
```

**Multi-module project, specific module:**
```
/java-enforce-logrecords module=oauth-sheriff-core
```

**Multi-module project, all modules:**
```
/java-enforce-logrecords
(will ask which module to analyze)
```

## RELATED

- Skill: `pm-dev-java-cui:cui-logging` - Logging standards, enforcement patterns, and workflows
  - Workflow: Analyze Logging Violations - Detect LOGGER usage violations
  - Workflow: Document LogRecord - Generate AsciiDoc documentation
- Standards: `logging-standards.md`, `logmessages-documentation.md`, `logging-enforcement-patterns.md`
- Command: `/java-implement-code` - Fix production code
- Command: `/java-implement-tests` - Add tests
- Skill: `pm-dev-builder:builder-maven-rules` - Maven standards and build output parsing
