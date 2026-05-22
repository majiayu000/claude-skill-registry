---
name: Debugging Runtime Errors
description: Analyzes stack traces, error logs, and code context to identify root causes and suggest targeted fixes. Specializes in systematic troubleshooting across multiple languages. Use when encountering runtime errors, production issues, exceptions, crashes, or when the user mentions error messages, stack traces, or debugging needs.
---

# Debugging Runtime Errors

Systematically debug and resolve runtime errors through stack trace and error log analysis.

## What you should do

1. **Capture comprehensive error context** – Gather all available debugging information:
   - **Primary error details**: Exception type, error message, and severity level
   - **Complete stack trace**: Full call stack with file paths and line numbers
   - **Error logs**: Application logs, system logs, and runtime output
   - **Environment context**: Operating system, runtime version, deployment environment
   - **Reproduction details**: Steps that triggered the error, frequency, and conditions

2. **Parse and analyze stack trace** – Systematically examine the call stack:
   - **Identify error origin**: Find the exact line and function where the exception occurred
   - **Trace execution path**: Follow the call chain to understand the sequence of events
   - **Categorize stack frames**: Distinguish between application code, library code, and framework code
   - **Highlight critical frames**: Focus on frames in application code that are most relevant
   - **Extract key variables**: Identify variable values and object states mentioned in the trace

3. **Classify error type and severity** – Determine the nature and impact of the error:

   **Exception Categories:**
   - **Logic errors**: NullPointerException, IndexOutOfBounds, IllegalArgument
   - **Resource errors**: OutOfMemory, FileNotFound, NetworkTimeout
   - **Configuration errors**: Missing properties, invalid settings, environment issues
   - **Integration errors**: Database connection failures, API call failures, authentication issues
   - **Concurrency errors**: DeadLocks, race conditions, thread synchronization issues

   **Severity Assessment:**
   - **Critical**: Application crash, data corruption, security breach
   - **High**: Feature unavailable, significant performance degradation
   - **Medium**: Recoverable error, minor functionality impact
   - **Low**: Warning-level issues, logging errors

4. **Investigate relevant source code** – Deep dive into the problematic code:
   - **Read the failing function/method**: Understand the logic at the error location
   - **Analyze input validation**: Check parameter validation and boundary conditions
   - **Review error handling**: Examine existing try/catch blocks and error propagation
   - **Check resource management**: Verify proper cleanup of files, connections, memory
   - **Examine dependencies**: Look at external library usage and integration patterns

5. **Analyze environmental factors** – Consider context that may contribute to the error:
   - **Configuration analysis**: Check application config, environment variables, property files
   - **Runtime environment**: Verify Java/Python/Node.js version compatibility
   - **Resource availability**: Check memory usage, disk space, network connectivity
   - **External dependencies**: Validate database connections, API endpoints, file system access
   - **Timing and concurrency**: Look for race conditions, timing-dependent failures

6. **Identify root cause patterns** – Determine the fundamental cause:

   **Common Root Causes:**
   - **Null/undefined handling**: Missing null checks or initialization
   - **Boundary violations**: Array/list index errors, buffer overflows
   - **Resource exhaustion**: Memory leaks, connection pool exhaustion
   - **Invalid assumptions**: Incorrect assumptions about data format or availability
   - **Configuration mismatches**: Environment-specific settings or missing properties
   - **Race conditions**: Thread safety issues in concurrent code

7. **Develop targeted fix strategy** – Create a specific solution approach:
   - **Immediate mitigation**: Quick fixes to prevent further errors
   - **Root cause resolution**: Address the underlying issue permanently
   - **Defensive programming**: Add error handling and validation to prevent recurrence
   - **Testing strategy**: Define tests to verify the fix and prevent regression
   - **Monitoring enhancements**: Add logging or metrics to catch similar issues early

8. **Implement and validate the fix** – Apply the solution systematically:

   **Fix Implementation:**
   - **Defensive checks**: Add null/undefined checks and input validation
   - **Error handling**: Implement proper try/catch blocks with meaningful error messages
   - **Resource cleanup**: Ensure proper disposal of resources (files, connections, memory)
   - **Configuration fixes**: Update config files, environment variables, or documentation
   - **Logic corrections**: Fix algorithmic errors or incorrect assumptions

   **Validation Steps:**
   - **Reproduce the error**: Confirm you can recreate the original issue
   - **Apply the fix**: Implement the solution without introducing new issues
   - **Test the fix**: Verify the error no longer occurs under the same conditions
   - **Regression testing**: Ensure related functionality still works correctly
   - **Edge case testing**: Test boundary conditions and error scenarios

9. **Create comprehensive debugging report** – Document findings and solution:

   **Error Analysis Summary:**
   - Original error details and stack trace analysis
   - Root cause identification with supporting evidence
   - Environmental factors and contributing conditions
   - Impact assessment and affected functionality

   **Solution Documentation:**
   - Specific fix implemented with code changes
   - Rationale for the chosen approach
   - Alternative solutions considered and why they were rejected
   - Testing performed to validate the fix

   **Prevention Recommendations:**
   - Code review checklist items to prevent similar errors
   - Additional error handling or logging suggestions
   - Configuration or deployment improvements
   - Monitoring and alerting enhancements

**LANGUAGE-SPECIFIC DEBUGGING TECHNIQUES:**

**Python:**
- Analyze traceback with line numbers and module paths
- Check for common errors: NameError, AttributeError, KeyError
- Review imports, virtual environment, and package versions
- Use `pdb` or logging for additional debugging context

**JavaScript/Node.js:**
- Parse V8 stack traces and source map references  
- Handle async/await errors and Promise rejections
- Check for undefined variables, scope issues, and type errors
- Review package.json dependencies and Node.js version compatibility

**Java:**
- Analyze full stack trace with package names and line numbers
- Check for ClassNotFoundException, NullPointerException patterns
- Review classpath, JAR dependencies, and JVM configuration
- Examine thread dumps for concurrency issues

**DEBUGGING BEST PRACTICES:**

- **Methodical approach**: Work systematically from symptoms to root cause
- **Evidence-based**: Base conclusions on observable facts, not assumptions
- **Minimal changes**: Make the smallest possible fix that addresses the root cause
- **Documentation**: Record the debugging process for future reference
- **Testing focus**: Ensure fixes are thoroughly validated before deployment

**DELIVERABLES:**

For each debugging session, provide:
- **Root cause analysis**: Clear explanation of why the error occurred
- **Implemented fix**: Specific code changes with rationale
- **Test validation**: Evidence that the fix resolves the issue
- **Prevention strategy**: Recommendations to avoid similar issues

The goal is to transform cryptic runtime errors into clear, actionable fixes that not only resolve the immediate issue but also improve overall system reliability and maintainability.