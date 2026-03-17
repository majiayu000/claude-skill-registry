---
name: request-expert-second-opinion
description: Consult another expert coding agent via codex CLI for extra tricky bugs or complex feature design reviews. Codex investigates thoroughly and writes a markdown summary to ./tmp/ — it never modifies source code.
---

# Request Expert Second Opinion

Use this skill when you're stuck on a particularly tricky bug or need another expert's perspective on a complex feature design.

## When to Use

**Tricky Bugs:**

- Bug persists after multiple investigation attempts
- Root cause unclear despite thorough debugging
- Intermittent or hard-to-reproduce issues
- Complex race conditions or timing issues
- Subtle architectural or logical flaws

**Complex Feature Planning:**

- Multiple valid architectural approaches
- High-stakes design decisions
- Cross-cutting concerns (security, performance, scalability)
- Need validation of technical approach
- Uncertainty about trade-offs

## Core Requirement: Write Findings to File

**Codex must NEVER modify source code.** Its sole output must be a markdown file in `./tmp/` summarizing findings and recommendations.

Always include this instruction in every codex prompt:

```
CRITICAL CONSTRAINTS:
- Do NOT modify any source files
- Do NOT write any code
- Your ONLY output must be a markdown file written to ./tmp/second-opinion-[topic].md
- The markdown file must contain: findings, analysis, recommendations, and suggested implementation approach
- Investigate thoroughly first, then write the summary file
```

## Structured Prompt Patterns

### Bug Investigation Template

```bash
mkdir -p ./tmp && codex exec --full-auto "
CRITICAL CONSTRAINTS:
- Do NOT modify any source files
- Do NOT write any code
- Your ONLY output must be a markdown file written to ./tmp/second-opinion-[bug-name].md
- Investigate thoroughly, then write the summary

PROBLEM:
[Clear description of the bug]

SYMPTOMS:
- [Observable behavior]
- [Error messages or logs]
- [Affected environments/scenarios]

INVESTIGATION SO FAR:
1. [What you checked]
2. [Debugging performed]
3. [Hypotheses ruled out]

RELEVANT CODE:
[Code snippets or file paths]

After thorough investigation, write ./tmp/second-opinion-[bug-name].md with:
1. Root cause analysis
2. Why it's happening
3. Recommended fix approach
4. Alternative approaches considered
5. Risks and trade-offs
"
```

### Feature Design Review Template

```bash
mkdir -p ./tmp && codex exec --full-auto "
CRITICAL CONSTRAINTS:
- Do NOT modify any source files
- Do NOT write any code
- Your ONLY output must be a markdown file written to ./tmp/second-opinion-[feature-name].md
- Investigate the codebase thoroughly, then write the summary

FEATURE REQUEST:
[What needs to be implemented]

CURRENT ARCHITECTURE:
[Relevant system components and patterns]

PROPOSED APPROACH:
[Your initial design]

CONSTRAINTS:
- [Technical constraints]
- [Performance requirements]

CONCERNS:
- [What you're uncertain about]
- [Potential risks or trade-offs]

After thorough investigation, write ./tmp/second-opinion-[feature-name].md with:
1. Assessment of proposed approach
2. Recommended approach (may differ)
3. Key trade-offs
4. Implementation guidance
5. Risks to watch out for
"
```

## Advanced Options

### Attach Context Files

```bash
# Include specific files for review
mkdir -p ./tmp && codex exec --full-auto -i /path/to/file1.go -i /path/to/file2.go "
CRITICAL CONSTRAINTS:
- Do NOT modify any source files
- Write findings to ./tmp/second-opinion-[topic].md only

Review these files and write your analysis of [issue] to ./tmp/second-opinion-[topic].md
"
```

### Change Working Directory

```bash
# Execute in specific directory context
mkdir -p ./tmp && codex exec --full-auto -C /path/to/project "
CRITICAL CONSTRAINTS:
- Do NOT modify any source files
- Write findings to ./tmp/second-opinion-[topic].md only

Investigate [topic] and write your analysis to ./tmp/second-opinion-[topic].md
"
```

### Use Different Model

```bash
# Use specific model for deep analysis
mkdir -p ./tmp && codex exec --full-auto -m o3 "
CRITICAL CONSTRAINTS:
- Do NOT modify any source files
- Write findings to ./tmp/second-opinion-[topic].md only

[Your investigation request]
"
```

## Best Practices

### Provide Sufficient Context

- Include relevant code snippets (not entire files)
- Share error messages and stack traces verbatim
- Specify environment details (AWS, Python version, dependencies)
- Mention what's already been tried

### Ask Specific Questions

❌ "Help me fix this bug"
✅ "I suspect a race condition between X and Y. How would you verify this hypothesis?"

❌ "How should I build this feature?"
✅ "I'm choosing between approach A (pros: X, cons: Y) and approach B (pros: Z, cons: W). Which aligns better with our async Lambda pattern?"

### Scope the Request

- Focus on one bug or one design decision
- Break complex features into smaller consultation requests
- Don't ask for full implementation, ask for guidance

### Interpret the Response

After receiving expert opinion:

1. **Validate suggestions** against project patterns (CLAUDE.md, PROJECT_KNOWLEDGE.md)
2. **Test recommendations** in isolation before applying broadly
3. **Document insights** in memory if they reveal project-wide patterns
4. **Ask follow-ups** if the response raises new questions

## Integration with Agents

**When to use this skill vs. agents:**

| Situation                     | Tool                                | Reason                                                           |
|-------------------------------|-------------------------------------|------------------------------------------------------------------|
| Need fresh perspective on bug | This skill                          | External expert not bound by current investigation tunnel vision |
| Need to implement bug fix     | `product-software-engineer` agent   | Implementation work                                              |
| Need architectural validation | This skill                          | Second opinion on design trade-offs                              |
| Need to implement feature     | `product-software-engineer` agent   | Implementation work                                              |
| Stuck after agent failed      | This skill                          | Break through blockage with new approach                         |
| Need deeper research          | `Explore` or `web-researcher` agent | Systematic codebase/web exploration                              |

## Examples

### Example 1: Tricky Lambda Timeout

```bash
mkdir -p ./tmp && codex exec --full-auto "
CRITICAL CONSTRAINTS:
- Do NOT modify any source files
- Write findings to ./tmp/second-opinion-lambda-timeout.md only

PROBLEM:
Lambda function times out at 30s, but local tests complete in 2s. The function:
- Queries DynamoDB (5 items, takes ~100ms locally)
- Calls OpenAI API (takes ~3s locally)
- Writes to S3 (takes ~200ms locally)

CloudWatch logs show the function starts, logs 'Fetching from DynamoDB', then times out 30s later with no further logs.

Lambda is in a private subnet with VPC endpoints for DynamoDB and S3. Security groups allow all outbound. NAT Gateway is healthy.

Investigate the codebase, review the Lambda and VPC configuration, then write ./tmp/second-opinion-lambda-timeout.md with:
1. Root cause hypothesis
2. Evidence supporting it
3. Recommended fix approach
4. How to verify the fix
"
```

### Example 2: DynamoDB Table Migration Strategy

```bash
mkdir -p ./tmp && codex exec --full-auto "
CRITICAL CONSTRAINTS:
- Do NOT modify any source files
- Write findings to ./tmp/second-opinion-dynamo-migration.md only

CONTEXT:
We need to migrate from single DynamoDB table to separate tables for:
1. Job results (hot data, frequent reads)
2. Analysis metadata (cold data, infrequent reads)

Current table: 50GB, composite PK/SK pattern

Our philosophy (from PROJECT_KNOWLEDGE.md): delete aggressively, never preserve backwards compatibility.

Investigate the current table usage and access patterns in the codebase, then write ./tmp/second-opinion-dynamo-migration.md with:
1. Assessment of migration complexity
2. Recommended migration approach (aligned with no-backwards-compatibility philosophy)
3. Key risks
4. Suggested implementation order
"
```

### Example 3: Async Retry Pattern Review

```bash
mkdir -p ./tmp && codex exec --full-auto -C /Users/noy/Code/deway-main/backend-aws "
CRITICAL CONSTRAINTS:
- Do NOT modify any source files
- Write findings to ./tmp/second-opinion-retry-logic.md only

Review the async patterns in apps/ and modules/ and assess a proposed approach for adding retry logic:

PROPOSAL:
Add retry with exponential backoff for:
- External API calls (OpenAI, data sources)
- S3 uploads
- DynamoDB writes

Context: Lambdas are event-driven (EventBridge), no SQS queue, 5min timeout.

After investigation, write ./tmp/second-opinion-retry-logic.md with:
1. Assessment of whether retries belong at handler vs service level
2. Idempotency considerations for DynamoDB writes
3. Whether exponential backoff fits all cases
4. Recommended approach with rationale
"
```

## Limitations

- **Not a replacement for systematic debugging**: Use agents and tools first
- **External context**: Codex expert doesn't have your conversation history
- **Read-only**: Codex must not modify source code — only write to `./tmp/`
- **Cost**: Each invocation uses API credits

## Follow-up Actions

After codex writes its findings to `./tmp/second-opinion-*.md`:

1. Read the file and review the recommendations
2. Delegate implementation to `product-software-engineer` or `infra-software-engineer`
3. Run `tests-runner` to verify solutions
4. If the insight reveals a project-wide pattern, add it to PROJECT_KNOWLEDGE.md
