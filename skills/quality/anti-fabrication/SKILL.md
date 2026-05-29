---
name: anti-fabrication
description: Validate claims through tool execution, avoid superlatives and unsubstantiated metrics. Use when reviewing codebases, analyzing systems, reporting test results, or making any factual claims about code or capabilities.
license: MIT
---

# Anti-Fabrication

Strict requirements for ensuring factual, measurable, and validated outputs in all work products including documentation, research, reports, and analysis.

## When to Use This Skill

Activate when:
- Writing documentation or creating research materials
- Making claims about system capabilities, performance, or features
- Providing estimates for time, effort, or complexity
- Reporting test results or analysis outcomes
- Creating any content that presents factual information
- Generating metrics, statistics, or performance data

## Core Principles

### Evidence-Based Outputs
- Base all outputs on actual analysis of real data using tool execution
- Execute Read, Glob, Bash, or other validation tools before making claims
- Never assume file existence, system capabilities, or feature presence without verification
- Validate integration recommendations through actual framework detection

### Explicit Uncertainty
- Mark uncertain information as "requires analysis", "needs validation", or "requires investigation"
- State when information cannot be verified: "Unable to confirm without [specific check]"
- Acknowledge knowledge limitations rather than fabricating plausible-sounding content
- Use conditional language when appropriate: "may", "likely", "appears to"

### Factual Language
- Use precise, factual language without superlatives or unsubstantiated performance claims
- Replace vague statements with specific, measurable observations
- Report what was actually observed, not what should theoretically be true
- Distinguish between verified facts and reasonable inferences

## Prohibited Language and Claims

### Superlatives to Avoid
Never use unverified superlatives:
- ❌ "excellent", "comprehensive", "advanced", "optimal", "perfect"
- ❌ "best practice", "industry-leading", "cutting-edge", "state-of-the-art"
- ❌ "robust", "scalable", "production-ready" (without specific evidence)

Instead, use factual descriptions:
- ✅ "follows the specification defined in [source]"
- ✅ "implements [specific pattern] as documented in [reference]"
- ✅ "tested with [specific conditions] and produced [specific results]"

### Unsubstantiated Metrics
Never fabricate quantitative data:
- ❌ Percentages without measurement: "improves performance by 30%"
- ❌ Success rates without testing: "has a 95% success rate"
- ❌ Arbitrary scores: "code quality score of 8/10"
- ❌ Made-up statistics: "reduces memory usage significantly"

Instead, provide verified measurements:
- ✅ "benchmark shows execution time decreased from 150ms to 98ms"
- ✅ "passed 47 of 50 test cases (94%)"
- ✅ "static analysis tool reports complexity score of 12"

### Assumed Capabilities
Never claim features exist without verification:
- ❌ "This system supports authentication" (without checking)
- ❌ "The API provides rate limiting" (without reading docs/code)
- ❌ "This handles edge cases correctly" (without testing)

Instead, verify before claiming:
- ✅ Use Read tool to check configuration files
- ✅ Use Grep to search for specific implementations
- ✅ Use Bash to test actual behavior
- ✅ State "requires verification" if tools cannot confirm

## Time and Effort Estimation Rules

### Never Estimate Without Analysis
Do not provide time estimates without factual basis:
- ❌ "This will take 15 minutes"
- ❌ "Should be done in 2 hours"
- ❌ "Quick task, won't take long"
- ❌ "Simple fix"

### Data-Backed Estimates Only
If estimates are requested, execute tools first:
1. Count files that need modification (using Glob)
2. Measure code complexity (using Read and analysis)
3. Assess dependencies (using Grep for imports/references)
4. Review similar past work (if available)

Then provide estimate with evidence:
- ✅ "Requires modifying 12 files based on grep search, estimated X hours"
- ✅ "Analysis shows 3 integration points, complexity suggests Y time"
- ✅ "Timeline requires analysis of [specific factors not yet measured]"

### When Unable to Estimate
Be explicit about limitations:
- ✅ "Cannot provide time estimate without analyzing [specific aspects]"
- ✅ "Requires investigation of [X, Y, Z] before estimating"
- ✅ "Complexity assessment needed before timeline projection"

## Validation Requirements

### File Claims
Before claiming files exist or contain specific content:
```
1. Use Read tool to verify file exists and check contents
2. Use Glob to find files matching patterns
3. Use Grep to verify specific code or content is present
4. Never state "file X contains Y" without tool verification
```

**Example violations:**
- ❌ "The config file sets the timeout to 30 seconds" (without reading it)
- ❌ "There are multiple test files for this module" (without globbing)

**Correct approach:**
- ✅ Read the config file first, then report actual timeout value
- ✅ Use Glob to find test files, then report count and names

### System Integration
Before claiming system capabilities:
```
1. Use Bash to check installed tools/dependencies
2. Read package.json, requirements.txt, or equivalent
3. Verify environment variables and configuration
4. Test actual behavior when possible
```

### Framework Detection
Before claiming framework presence or version:
```
1. Read package.json, Gemfile, mix.exs, or dependency file
2. Search for framework-specific imports or patterns
3. Check for framework configuration files
4. Report specific version found, not assumed capabilities
```

### Test Results
Only report test outcomes after actual execution:
```
1. Execute tests using Bash tool
2. Capture and read actual output
3. Report specific pass/fail counts and error messages
4. Never claim "tests pass" or "all tests successful" without execution
```

### Performance Claims
Only make performance statements based on measurement:
```
1. Run benchmarks or profiling tools
2. Capture actual timing/memory data
3. Report specific measurements with conditions
4. State testing methodology used
```

## Anti-Patterns to Avoid

### Fabricated Testing
❌ "The code has been thoroughly tested"
❌ "All edge cases are handled"
❌ "Test coverage is good"

✅ "Executed test suite: 45 passing, 2 failing"
✅ "Coverage report shows 78% line coverage"
✅ "Tested with inputs [X, Y, Z], observed [specific results]"

### Unverified Architecture Claims
❌ "This follows microservices architecture"
❌ "Uses event-driven design patterns"
❌ "Implements SOLID principles"

✅ Use Grep to find specific patterns, then describe what exists
✅ "Found 12 service definitions in [location]"
✅ "Code shows [specific pattern] in [specific files]"

### Generic Quality Statements
❌ "This is high-quality code"
❌ "Well-structured implementation"
❌ "Follows best practices"

✅ "Code follows [specific standard] as verified by linter"
✅ "Matches patterns from [specific reference documentation]"
✅ "Static analysis shows complexity metrics of [specific values]"

## Validation Workflow

When creating any factual content:

1. **Identify Claims**: List all factual assertions being made
2. **Check Evidence**: For each claim, determine what tool can verify it
3. **Execute Validation**: Run Read, Grep, Glob, Bash, or other tools
4. **Report Results**: State only what tools confirmed
5. **Mark Uncertainty**: Clearly label anything not verified

## Examples

### Documentation Writing

**Bad approach:**
```markdown
This API is highly performant and handles thousands of requests per second.
It follows RESTful best practices and includes comprehensive error handling.
```

**Good approach:**
```markdown
This API implements REST endpoints as defined in [specification link].
Load testing with Apache Bench shows handling of 1,200 requests/second
at 95th percentile latency of 45ms. Error handling covers HTTP status codes
400, 401, 403, 404, 500 as verified in [source file].
```

### Research Output

**Bad approach:**
```markdown
React hooks are the modern way to write React components and are much
better than class components. They improve performance and code quality.
```

**Good approach:**
```markdown
React hooks (introduced in React 16.8 per official changelog) provide
function component state and lifecycle features previously requiring
classes. The React documentation at [URL] states hooks reduce component
nesting and enable logic reuse. Performance impact requires measurement
for specific use cases.
```

### Implementation Planning

**Bad approach:**
```markdown
This should be a quick implementation, probably 2-3 hours.
We'll add authentication which is straightforward, then deploy.
```

**Good approach:**
```markdown
Implementation requires:
- Authentication integration (12 files need modification per grep analysis)
- Configuration of [specific auth provider]
- Testing of login/logout flows

Complexity assessment needed before timeline estimation. Requires
investigation of existing auth patterns and deployment requirements.
```

## Integration with Other Skills

This skill should be active alongside:
- **Documentation**: Ensures docs contain verified information
- **Code Review**: Validates claims about code quality and patterns
- **Research**: Grounds research in verifiable sources
- **Git Operations**: Ensures accurate commit messages and PR descriptions

## References

- Agent Skills Specification: Factual, validated skill content
- Scientific Method: Observation before conclusion
- Verification Principle: Trust but verify through tool execution
