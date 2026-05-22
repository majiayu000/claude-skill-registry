---
name: java-maintain-logger
description: Execute systematic logging standards maintenance with plan tracking and comprehensive test coverage
user-invocable: true
allowed-tools: Skill, Read, Write, Edit, Glob, Grep, Bash, Task, SlashCommand
---

# Logger Maintain Skill

Systematically implements and maintains logging standards across modules while preserving functionality and tracking progress via plan.md.

## CONTINUOUS IMPROVEMENT RULE

If you discover issues or improvements during execution, record them:

1. **Activate skill**: `Skill: plan-marshall:manage-lessons`
2. **Record lesson** with:
   - Component: `{type: "command", name: "java-maintain-logger", bundle: "pm-dev-java"}`
   - Category: bug | improvement | pattern | anti-pattern
   - Summary and detail of the finding

## PARAMETERS

- **module** - Module name for single module (optional, processes all if not specified)
- **create-plan** - Generate/regenerate plan.md from current state (optional, default: false)

## CRITICAL CONSTRAINTS

### Production Code Protection

**MUST:**
- Modify ONLY logging-related code
- Preserve all existing functionality
- Focus exclusively on logging implementation and testing

**MUST NOT:**
- Make non-logging production code changes
- Alter business logic behavior
- Change method signatures or APIs

### Bug Handling Protocol

When non-logging production bugs discovered:
1. **STOP** maintenance immediately
2. **DOCUMENT** bug (location, description, impact)
3. **ASK USER** for approval to fix
4. **WAIT** for explicit confirmation
5. **SEPARATE COMMIT** for bug fix if approved
6. **RESUME** logging maintenance after commit

**Never fix non-logging bugs without user approval.**

### Testing Philosophy - CRITICAL

**LogAsserts MUST be in business logic tests - NEVER standalone coverage tests.**

See `pm-dev-java-cui:cui-logging` skill (logging-maintenance-reference.md#test-implementation) for detailed examples.

## WORKFLOW

### Step 0: Parameter Validation

- If `module` specified: verify module exists
- If `create-plan` specified: will regenerate plan.md
- Determine processing scope (single module vs all)

### Step 1: Load Logging Standards

```
Skill: pm-dev-java-cui:cui-logging
```

This loads comprehensive logging standards including:
- logging-standards.md - Implementation standards for new code
- logging-maintenance-reference.md - Maintenance reference for existing code
- dsl-constants.md - DSL pattern for LogMessages structure

**On load failure:** Report error and abort command.

### Step 2: Pre-Maintenance Verification

**2.1 Build Verification:**

```
Skill: pm-dev-builder:builder-maven-rules
Workflow: Execute Maven Build
Parameters:
  goals: -Ppre-commit clean verify -DskipTests
  module: {module if specified}
  output_mode: errors
```

**On build failure:** Prompt user "[F]ix build first / [A]bort", track in `pre_verification_failures`.

**2.2 Module Identification:**

If `module` parameter not specified:
- Use Glob to identify all Maven modules
- Determine processing order (dependencies first)

**2.3 Standards Review Confirmation:**

Display loaded standards summary and confirm readiness with user.

### Step 3: Create/Update Planning Document

**3.1 Generate plan.md:**

If `create-plan=true` OR plan.md doesn't exist, run LogRecord Discovery Script from `pm-dev-java-cui:cui-logging` skill (logging-maintenance-reference.md#logrecord-discovery-and-coverage-verification).

**3.2 Display Status:**

```
Total LogRecords: {total}
Tested: {tested}
Missing: {missing}
Completion: {percentage}%
```

**3.3 Store Inventory:** Parse plan.md table for progress tracking.

### Step 4: Module-by-Module Analysis

For each module, run systematic violation detection using Explore agent:

**4.1 Logger Audit:**

```
Task:
  subagent_type: Explore
  model: sonnet
  description: Audit logger configuration
  prompt: |
    Identify logging configuration violations in module {module}.
    Apply detection criteria from `pm-dev-java-cui:cui-logging` skill:
    logging-maintenance-reference.md#standards-violation-detection

    Return structured list of violations with locations.
```

**4.2 LogRecord Audit:**

```
Task:
  subagent_type: Explore
  model: sonnet
  description: Audit LogRecord usage
  prompt: |
    Check LogRecord usage compliance in module {module}.
    Apply rules from `pm-dev-java-cui:cui-logging` skill:
    logging-maintenance-reference.md#logrecord-implementation-issues

    Return structured findings.
```

**4.3 LogMessages Review:**

```
Task:
  subagent_type: Explore
  model: sonnet
  description: Review LogMessages structure
  prompt: |
    Review LogMessages class structure in module {module}.
    Apply patterns from `pm-dev-java-cui:cui-logging` skill:
    logging-maintenance-reference.md#logmessages-structure-issues

    Return findings with specific violations.
```

**4.4 Documentation Check:**

Verify doc/LogMessages.adoc exists and matches implementation.

**4.5 Duplicate Detection:**

```
Task:
  subagent_type: Explore
  model: sonnet
  description: Detect duplicate log messages
  prompt: |
    Identify duplicate logging patterns in module {module}.
    Apply detection patterns from `pm-dev-java-cui:cui-logging` skill:
    logging-maintenance-reference.md#duplicate-detection-patterns

    Suggest consolidation opportunities.
```

**4.6 Display Module Analysis Summary** and prompt user: "[P]roceed / [S]kip / [A]bort"

### Step 5: Implementation Phase

Apply fixes using /java-implement-code command with patterns from `pm-dev-java-cui:cui-logging` skill:

**5.1 Logger Migration:**

```
SlashCommand: /pm-dev-java:java-implement-code task="Migrate logger to CuiLogger in {file}.
Replace logger with CuiLogger.
Apply migration pattern from `pm-dev-java-cui:cui-logging` skill: logging-maintenance-reference.md#logger-migration

CRITICAL: Only modify logging code, no other changes."
```

**5.2 LogRecord Implementation:**

```
SlashCommand: /pm-dev-java:java-implement-code task="Add LogRecord usage in {file}.
Convert direct logging to LogRecord.
Apply implementation pattern from `pm-dev-java-cui:cui-logging` skill: logging-maintenance-reference.md#logrecord-implementation

CRITICAL: Only modify logging code."
```

**If non-logging bug discovered:** Apply bug handling protocol (stop, document, ask user, wait).

**5.3 LogMessages Creation/Update:**

```
SlashCommand: /pm-dev-java:java-implement-code task="Create/update LogMessages class for module {module}.
Use template from `pm-dev-java-cui:cui-logging` skill: logging-maintenance-reference.md#logmessages-structure

CRITICAL: Only create/modify LogMessages, no other changes."
```

**5.4 Documentation Update:**

Create or update doc/LogMessages.adoc following standard format.

**5.5 Test Implementation - CRITICAL STEP:**

```
Task:
  subagent_type: Explore
  model: sonnet
  description: Find business logic test for LogRecord
  prompt: |
    Find the appropriate business logic test for LogRecord {logrecord_name}.
    Follow troubleshooting guide from `pm-dev-java-cui:cui-logging` skill:
    logging-maintenance-reference.md#finding-the-right-business-logic-test

    Return: test file, test method, line number for LogAsserts.
    CRITICAL: Must be EXISTING business logic test, not new coverage test.
```

Then add LogAsserts to existing test (see `pm-dev-java-cui:cui-logging` skill for LogAsserts patterns).

**If no business logic test exists:** Prompt user "[C]reate business test first / [S]kip / [A]bort"

### Step 6: Verification Phase

**6.1 Module Build Verification:**

```
Skill: pm-dev-builder:builder-maven-rules
Workflow: Execute Maven Build
Parameters:
  goals: clean test
  module: {module}
  output_mode: structured
```

**On failure:** Analyze cause, apply bug handling protocol if non-logging.

**6.2 LogRecord Coverage Verification:**

For each LogRecord in module:
1. Verify production reference (Grep for `.format()` calls)
2. Verify test reference (Grep for LogAsserts usage)
3. Update plan.md status

**6.3 Full Build Verification:**

```
Skill: pm-dev-builder:builder-maven-rules
Workflow: Execute Maven Build
Parameters:
  goals: -Ppre-commit clean install
  module: {module}
  output_mode: errors
```

**6.4 Module Commit:**

```
Bash: git add {module files} plan.md
Bash: git commit -m "$(cat <<'EOF'
refactor(logging): implement logging standards in {module}

Logging improvements:
- Logger migrations: {count} completed
- LogRecord implementations: {count} completed
- Tests updated: {count} business logic tests
- Documentation: doc/LogMessages.adoc updated

plan.md status: {tested}/{total} LogRecords tested

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

Proceed to next module.

### Step 7: Final Verification

**7.1 Complete Build:**

```
Skill: pm-dev-builder:builder-maven-rules
Workflow: Execute Maven Build
Parameters:
  goals: -Ppre-commit clean install
  output_mode: errors
```

**7.2 Final plan.md Update:** Update with completion timestamp.

**7.3 Generate Final Report:** Review all plan.md files and generate summary.

### Step 8: Display Summary

```
╔════════════════════════════════════════════════════════════╗
║       Logger Maintenance Summary                           ║
╚════════════════════════════════════════════════════════════╝

Scope: {module or 'all modules'}

Modules Processed: {modules_completed} / {total_modules}

Logger Migrations: {logger_migrations}
LogRecord Implementations: {logrecord_implementations}
Tests Updated: {tests_updated}
LogRecord Coverage: {tested_logrecords}/{total_logrecords} ({coverage_percentage}%)
Documentation: {doc_count} files created/updated
Bugs Found: {bugs_found} ({bugs_fixed} fixed, {bugs_skipped} skipped)

Build Status: {SUCCESS/FAILURE}
Time Taken: {elapsed_time}

See plan.md for detailed LogRecord inventory.
```

## STATISTICS TRACKING

Track throughout workflow:
- `pre_verification_failures` - Pre-maintenance build failures
- `modules_completed` / `modules_skipped` - Module processing
- `logger_migrations` - Total logger migrations
- `logrecord_implementations` - Total LogRecord implementations
- `tests_updated` - Business logic tests updated with LogAsserts
- `tests_missing` - LogRecords without business logic tests
- `bugs_found` / `bugs_fixed` / `bugs_skipped` - Bug handling
- `module_verification_failures` - Module verification failures
- `total_logrecords` / `tested_logrecords` - Coverage metrics
- `elapsed_time` - Total execution time

Display all statistics in final summary.

## ERROR HANDLING

**Build Failures:** Display detailed errors, distinguish logging vs non-logging, apply bug handling protocol.

**Test Failures:** Analyze cause, fix if logging-related, apply bug handling protocol if non-logging.

**Missing Business Logic Tests:** Document LogRecords without tests, prompt user for guidance.

**Non-Logging Bugs:** STOP immediately, document thoroughly, ask user approval, separate commit if approved.

## USAGE EXAMPLES

```
# Process all modules
/java-maintain-logger

# Process single module
/java-maintain-logger module=auth-service

# Generate/regenerate plan
/java-maintain-logger create-plan

# Process module and regenerate plan
/java-maintain-logger module=user-api create-plan
```

## ARCHITECTURE

Orchestrates skill workflows and commands:
- **`pm-dev-java-cui:cui-logging` skill** - Logging standards and maintenance reference
- **Explore agent** - Violation detection and business test location
- **/java-implement-code command** - Logging code modifications
- **Bash** - Maven builds for verification
- **pm-dev-builder:builder-maven-rules skill** - Build output parsing
- **Bash** - LogRecord discovery script and plan.md updates (scripts from skill)

## RELATED

- `pm-dev-java-cui:cui-logging` skill - Logging standards and maintenance reference
- `/java-implement-code` command - Code modifications
- `pm-dev-builder:builder-maven-rules` skill - Maven standards and output parsing
- `/java-refactor-code` command - Broader code refactoring
- `/java-enforce-logrecords` command - Automated logging enforcement
