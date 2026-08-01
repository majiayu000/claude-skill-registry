---
name: error-troubleshooter
description: 'Automatically troubleshoot unexpected results OR command/script errors
  without user request. Triggers when: (1) unexpected behavior - command succeeded
  but expected effect didn''t happen, missing expec'
---

---
name: error-troubleshooter
description: Automatically troubleshoot unexpected results OR command/script errors without user request. Triggers when: (1) unexpected behavior - command succeeded but expected effect didn't happen, missing expected errors, wrong output, silent failures; (2) explicit failures - stderr, exceptions, non-zero exit, SDK/API errors. Applies systematic diagnosis using error templates, hypothesis testing, and web research for any Stack Overflow-worthy issue.
---

# Error Troubleshooter

## Overview

This skill enables systematic troubleshooting of unexpected behavior and technical failures - whether explicit errors or silent anomalies where commands succeed but don't produce expected results. Proactively investigate any mismatch between expected and actual outcomes using a structured approach that balances quick fixes with thorough analysis.

## When to Use This Skill

Trigger this skill automatically when encountering either:

### (1) Unexpected Behavior (Priority)
- **Command succeeded but expected effect didn't happen** - e.g., configuration set but not taking effect, file created but empty
- **Missing expected errors** - e.g., test was designed to fail but passed, validation that should reject but accepted
- **Wrong or unexpected output** - e.g., different data than expected, incorrect format, unexpected side effects
- **Silent failures** - no error reported but operation clearly didn't work
- **Behavioral anomalies** - program runs but behaves differently than intended

### (2) Explicit Failures
- **Error messages from SDK/API calls** - exceptions, error codes, failure responses
- **Tool execution failures** - Bash errors, script crashes, MCP tool failures
- **Runtime errors** - exceptions in any programming language
- **Build or compilation failures** - compiler errors, linking failures
- **System errors** - permission denied, file not found, connection refused

**Key principle**: If there's any mismatch between expected and actual behavior - whether explicit error or silent anomaly - this skill applies.

## Troubleshooting Decision Tree

### 1. Initial Assessment

When unexpected behavior or an error occurs, immediately assess the situation:

```
Unexpected Behavior or Error Detected
    ↓
What type of issue is this?
    │
    ├─ UNEXPECTED BEHAVIOR (command succeeded but wrong result)
    │   ↓
    │   Document the mismatch:
    │   - What was expected?
    │   - What actually happened?
    │   - Any error messages? (none expected for unexpected behavior)
    │   ↓
    │   Is the cause obvious? (e.g., wrong variable, typo, wrong file)
    │   ├─ YES → Apply quick fix
    │   │         ↓
    │   │      Did expected behavior occur?
    │   │         ├─ YES → Done ✓
    │   │         └─ NO → Revert, proceed to Rigorous Investigation
    │   │
    │   └─ NO → Proceed directly to Rigorous Investigation
    │
    └─ EXPLICIT ERROR (stderr, exception, non-zero exit)
        ↓
        Is the fix obvious from the error message itself?
        ├─ YES → Apply quick fix (Happy Case Path)
        │         ↓
        │      Did it work?
        │         ├─ YES → Done ✓
        │         └─ NO → Revert changes, proceed to Rigorous Investigation
        │
        └─ NO → Is this a common trivial error?
               ├─ YES → Apply known fix based on experience
               │         ↓
               │      Did it work?
               │         ├─ YES → Done ✓
               │         └─ NO → Revert changes, proceed to Rigorous Investigation
               │
               └─ NO → Proceed directly to Rigorous Investigation
```

### 2. Happy Case Path (Quick Resolution)

For issues with obvious causes and fixes:

**Unexpected Behavior Quick Fixes:**
- Obvious typo or wrong variable name
- Wrong file path or target
- Cached data (clear cache and retry)
- Tool not reloaded after changes (restart and retry)

**Explicit Error Quick Fixes:**
- Error message explicitly states the solution (e.g., "Missing required argument --config")
- Common trivial errors (e.g., "command not found" → check installation)
- Direct and unambiguous error descriptions

**Action**: Apply the fix immediately and verify the result.

**Failure criteria for unexpected behavior**: If expected behavior still doesn't occur, revert and switch to rigorous investigation.

**Failure criteria for explicit errors**: If the error message is unchanged OR the problem clearly worsened, revert immediately and switch to rigorous investigation.

### 3. Rigorous Investigation Path (Complex Problems)

When quick fixes fail or the problem is non-trivial, follow this systematic approach:

#### Step 1: Extract Problem Pattern

**For Explicit Errors:**
SDK/API errors often follow fixed templates. Extract the template by:
- Removing variable components (file paths, user inputs, timestamps, IDs)
- Isolating the core error message structure
- Preparing the template for web search

Example:
```
Original: FileNotFoundError: [Errno 2] No such file or directory: '/home/user/data.csv'
Template: FileNotFoundError No such file or directory
```

See `{baseDir}/references/error-template-patterns.md` for detailed guidance.

**For Unexpected Behavior:**
Document the behavior pattern:
- What command/operation was performed?
- What was the expected outcome?
- What actually happened instead?
- Are there any observable symptoms (wrong data, missing files, etc.)?
- Has this operation worked before? When did it stop working?

Formulate a search query focusing on the behavior:
- "command X succeeded but didn't create Y"
- "configuration Z not taking effect"
- "expected validation to fail but passed"

#### Step 2: Gather Environment Information

Collect relevant environment details when:
- The pattern search doesn't yield clear solutions
- Environment-specific factors are likely relevant (versions, configurations, system state)
- Context is needed to understand the problem

**IMPORTANT**: Avoid collecting sensitive information. If sensitive data is necessary, explicitly request user authorization first.

See `{baseDir}/references/environment-info-guide.md` for collection guidelines and privacy protection.

#### Step 3: Research the Problem

Use efficient research strategies:
- **Web Search**: Search the extracted pattern (error template or behavior description)
- **Parallel Investigation**: Use Task tool with subagent_type=Explore for multiple research angles simultaneously
- **Documentation**: Search official docs, GitHub Issues, Stack Overflow for similar problems
- **Counter-evidence**: Look for cases where the expected behavior DID occur to identify what's different

**Token Efficiency**: For complex investigations, delegate research to subagents to avoid context exhaustion.

#### Step 4: Create Debug Notes File

For difficult problems, create a debug notes file to:
- Track theories and test results
- Enable parallel investigation
- Resume from interruptions
- Maintain systematic progress

Use the template in `{baseDir}/assets/debug-notes-template.md` to structure notes.

#### Step 5: Formulate and Test Theories

Based on research:
1. List plausible theories explaining the problem (why error occurred OR why expected behavior didn't happen)
2. Order by likelihood
3. Design tests to verify each theory
4. Execute tests systematically
5. Document results in debug notes
6. Iterate until the correct solution is found

**For unexpected behavior**: Focus theories on "why the expected effect didn't occur" rather than "why an error happened".

#### Step 6: Implement Solution

Once the correct theory is identified:
- Apply the fix
- Verify the problem is resolved:
  - **For errors**: Error no longer occurs
  - **For unexpected behavior**: Expected behavior now occurs as intended
- Document the solution in debug notes (if notes were created)
- Consider if this pattern should be added to common patterns

## Token Efficiency Strategies

For complex investigations:

1. **Use Subagents**: Delegate research tasks using the Task tool with subagent_type=Explore
2. **File-Based Notes**: Write debug notes to files instead of maintaining context in memory
3. **Parallel Research**: Launch multiple subagents simultaneously for different research angles
4. **Selective Context**: Only load reference files when specifically needed

## Key Principles

1. **Proactive Investigation**: Don't wait for the user to request troubleshooting—start investigating immediately when unexpected behavior or errors occur
2. **Prioritize Unexpected Behavior**: Check for silent failures and behavioral anomalies first, as they're more subtle than explicit errors
3. **Bold Hypotheses, Careful Verification**: Generate multiple competing theories, then rigorously verify each with concrete evidence (see `{baseDir}/references/problem-solving-mindset.md`)
4. **Challenge Your Own Reasoning**: Actively search for counter-evidence and successful counter-examples that would disprove your theories
5. **Acknowledge Uncertainty**: Present confidence levels; admit when evidence is incomplete rather than pretending certainty
6. **Revert on Failure**: If a fix doesn't work, always revert before trying another approach
7. **Systematic Documentation**: For difficult problems, maintain structured debug notes
8. **Privacy Protection**: Never collect sensitive information without explicit user authorization
9. **Efficient Resource Usage**: Use subagents and files to manage context for complex investigations

## Resources

This skill includes:

### references/
- `problem-solving-mindset.md` - Scientific approach to problem-solving: bold hypotheses, careful verification, and disciplined reasoning
- `systematic-debugging-methodology.md` - Practical debugging framework: Occam's Razor, diagnostic scripts, evidence hierarchy, and real-world examples
- `troubleshooting-sop.md` - Detailed standard operating procedures for systematic troubleshooting
- `error-template-patterns.md` - Guide to identifying and extracting error message templates
- `environment-info-guide.md` - Environment information collection guidelines with privacy protection
- `common-error-patterns.md` - Database of frequently encountered trivial errors and quick fixes

### assets/
- `debug-notes-template.md` - Template for structured debugging documentation

These resources are loaded as needed during the troubleshooting process.
