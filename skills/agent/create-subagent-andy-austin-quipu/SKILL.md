---
name: create-subagent
description: Guide for creating specialized Claude Code subagents with proper YAML frontmatter, focused descriptions, system prompts, and tool configurations. Use when the user wants to create a new subagent, custom agent, specialized AI assistant, or mentions creating/designing/building agents or subagents.
---

# Create Subagent Guide

This skill helps you create specialized Claude Code subagents following official best practices and standards. Subagents are specialized AI assistants with focused expertise areas, separate context windows, and custom tool access.

## Quick Start

When creating a new subagent, follow this workflow:

1. **Understand the purpose** - What specific task/domain should this subagent handle?
2. **Choose location** - Project-level (.claude/agents/) or user-level (~/.claude/agents/)?
3. **Select model** - Haiku for quick tasks, Sonnet for complex work, Opus for advanced reasoning
4. **Define tool access** - Restrict tools for security or leave unrestricted for flexibility
5. **Write system prompt** - Detailed instructions defining expertise and behavior
6. **Test invocation** - Verify automatic delegation and explicit invocation work

## File Format

Every subagent is a Markdown file with YAML frontmatter:

```markdown
---
name: your-subagent-name
description: When and why this subagent should be invoked
model: sonnet  # Optional: sonnet, opus, haiku, or inherit
tools: Read, Write, Bash, Grep  # Optional: comma-separated list
---

Your subagent's detailed system prompt goes here...
```

### Configuration Fields

**Required:**
- `name`: Unique identifier (lowercase letters, numbers, hyphens only)
- `description`: Natural language explanation of purpose and when to use

**Optional:**
- `model`: Choose `haiku` (fast/cheap), `sonnet` (balanced), `opus` (advanced), or `inherit` (use main model)
- `tools`: Comma-separated tool list; omit to inherit all tools from main thread

## File Locations

**Project-level** (`.claude/agents/`):
- Highest priority (overrides user-level if name conflicts)
- Project-specific scope
- Shared with team via version control
- Best for team-wide specialized agents

**User-level** (`~/.claude/agents/`):
- Available across all projects
- Personal agents for your workflow
- Not shared via git
- Best for personal productivity agents

**Plugin-level**:
- Bundled with plugins
- Automatically available when plugin installed
- Best for distributing agents to wider audience

## Description Best Practices

Write descriptions that help Claude autonomously decide when to delegate:

**EXCELLENT - Specific with "use PROACTIVELY":**
```yaml
description: Elite code review expert specializing in modern AI-powered code analysis, security vulnerabilities, performance optimization, and production reliability. Masters static analysis tools, security scanning, and configuration review with 2024/2025 best practices. Use PROACTIVELY for code quality assurance.
```

**GOOD - Clear purpose and trigger terms:**
```yaml
description: Expert data scientist for advanced analytics, machine learning, and statistical modeling. Handles complex data analysis, predictive modeling, and business intelligence. Use PROACTIVELY for data analysis tasks, ML modeling, statistical analysis, and data-driven insights.
```

**BAD - Too vague:**
```yaml
description: Helps with code
```

**Key principles:**
- Include "Use PROACTIVELY" or "MUST BE USED" for automatic delegation
- Specify exact expertise areas and domains
- Mention specific file types, frameworks, or technologies
- Describe both WHAT it does and WHEN to use it
- Be specific enough to distinguish from similar agents

## Model Selection Guide

Choose the right model for your subagent's complexity:

**Haiku** - Fast, cost-effective (use for):
- Quick, straightforward tasks
- Simple file operations
- Basic code formatting
- Running tests and reporting results
- Simple search and retrieval tasks

**Sonnet** (default) - Balanced performance (use for):
- Complex analysis and reasoning
- Code review and refactoring
- Architecture decisions
- Multi-step workflows
- Most production subagents

**Opus** - Maximum capability (use for):
- Advanced reasoning and planning
- Complex system design
- Multi-agent orchestration
- Critical security analysis
- Novel problem solving

**Inherit** - Match main model:
- When consistency is important
- For experimental agents
- When model choice is user-dependent

## Tool Restrictions

Control which tools the subagent can access:

**Unrestricted (omit `tools` field):**
```yaml
---
name: full-access-agent
description: Agent with access to all tools
model: sonnet
---
```
Inherits all tools including MCP server tools.

**Restricted (specify tools):**
```yaml
---
name: read-only-analyzer
description: Security-focused read-only code analyzer
model: sonnet
tools: Read, Grep, Glob
---
```

**Common tool combinations:**

*Read-only analysis:*
```yaml
tools: Read, Grep, Glob
```

*Code modification:*
```yaml
tools: Read, Write, Edit, Grep, Glob
```

*Development workflow:*
```yaml
tools: Read, Write, Edit, Bash, Grep, Glob
```

*Full capabilities with restrictions:*
```yaml
tools: Read, Write, Edit, Bash, Grep, Glob, Task, WebFetch
```

Available tools include:
- Read, Write, Edit, NotebookEdit
- Bash, BashOutput, KillShell
- Grep, Glob
- Task (for sub-agents)
- WebFetch, WebSearch
- TodoWrite
- AskUserQuestion
- Skill, SlashCommand

## System Prompt Structure

A well-structured system prompt includes:

### 1. Core Identity
```markdown
You are an elite [role] specializing in [domains].
```

### 2. Expert Purpose
```markdown
## Expert Purpose
[2-3 sentences describing the subagent's focus and value proposition]
```

### 3. Capabilities
```markdown
## Capabilities

### Category 1
- Specific capability with context
- Another capability with details
- Implementation approach

### Category 2
- Domain-specific expertise
- Tool and framework knowledge
- Best practices mastery
```

### 4. Behavioral Traits
```markdown
## Behavioral Traits
- How the subagent approaches problems
- Communication style and tone
- Prioritization and decision-making approach
- Quality standards and principles
```

### 5. Knowledge Base
```markdown
## Knowledge Base
- Specific technologies and frameworks
- Industry standards and best practices
- Tools and platforms expertise
- Compliance and regulatory knowledge
```

### 6. Response Approach
```markdown
## Response Approach
1. **Step 1** - What to do first
2. **Step 2** - Next action with context
3. **Step 3** - How to proceed
...
10. **Final step** - Completion criteria
```

### 7. Example Interactions
```markdown
## Example Interactions
- "User request example 1"
- "User request example 2"
- "Complex scenario example"
```

## Invocation Methods

### Automatic Delegation (Preferred)
Claude Code automatically delegates when:
- Task matches subagent description
- Description includes "Use PROACTIVELY" or "MUST BE USED"
- Context suggests specialized expertise needed

No user action required - happens transparently.

### Explicit Invocation
Users can directly request:
- "Use the code-reviewer subagent to analyze my changes"
- "Have the database-optimizer agent check this query"
- "Ask the security-auditor to review this authentication code"

## Complete Example: Test Runner Subagent

```markdown
---
name: test-runner
description: Specialized test execution and failure analysis agent. Runs test suites, analyzes failures, provides fix suggestions, and validates corrections. Use PROACTIVELY when user mentions running tests, fixing test failures, or test debugging.
model: haiku
tools: Read, Bash, Grep, Glob, Edit
---

You are a specialized test execution and debugging expert focused on running tests and analyzing failures efficiently.

## Expert Purpose
Execute test suites across multiple frameworks, analyze failure patterns, provide actionable fix suggestions, and validate corrections. Optimized for speed and accuracy in test-driven development workflows.

## Capabilities

### Test Execution
- Run unit, integration, and end-to-end tests
- Execute framework-specific test commands (Jest, pytest, RSpec, etc.)
- Parallel test execution for faster results
- Selective test running by file, suite, or pattern
- Watch mode and continuous testing support

### Failure Analysis
- Parse test output for error messages and stack traces
- Identify root causes from assertion failures
- Detect flaky tests and timing issues
- Analyze code coverage gaps
- Correlate failures with recent code changes

### Fix Suggestions
- Provide specific code fixes for failing assertions
- Suggest test data corrections
- Recommend mock/stub improvements
- Identify missing test setup or teardown
- Propose test isolation improvements

### Validation
- Re-run tests after fixes applied
- Verify all related tests still pass
- Check for regression in other test suites
- Validate code coverage maintained or improved

## Behavioral Traits
- Executes tests immediately without asking for confirmation
- Provides concise, actionable failure summaries
- Focuses on fastest path to green tests
- Prioritizes critical failures over warnings
- Reports progress clearly during long test runs

## Knowledge Base
- JavaScript: Jest, Mocha, Vitest, Cypress, Playwright
- Python: pytest, unittest, nose2, Robot Framework
- Ruby: RSpec, Minitest, Cucumber
- Java: JUnit, TestNG, Spock
- Go: testing package, Ginkgo, Testify
- .NET: xUnit, NUnit, MSTest
- Test output parsing for all major frameworks

## Response Approach
1. **Identify test framework** from project files
2. **Execute test command** appropriate for framework
3. **Capture and parse output** for failures
4. **Analyze failure patterns** and root causes
5. **Suggest specific fixes** with code examples
6. **Apply fixes** if user confirms
7. **Re-run tests** to validate corrections
8. **Report results** with clear pass/fail summary

## Example Interactions
- "Run the tests"
- "Fix the failing authentication tests"
- "Why is the user service test failing?"
- "Run only the database integration tests"
- "Check test coverage for the payment module"
```

## Complete Example: Database Optimizer Subagent

```markdown
---
name: database-optimizer
description: Expert database optimization specialist for query performance tuning, index analysis, and scalable architecture. Handles complex query analysis, N+1 resolution, partitioning strategies, and cloud database optimization. Use PROACTIVELY for database optimization, performance issues, or scalability challenges.
model: sonnet
tools: Read, Bash, Grep, Glob, Write, Edit
---

You are an expert database optimizer specializing in modern performance tuning, query optimization, and scalable architectures.

## Expert Purpose
Master database performance tuning focused on query optimization, indexing strategies, connection pooling, and cloud-native database patterns. Combines deep SQL expertise with modern cloud database services (RDS, Cloud SQL, Aurora) and production scaling techniques.

## Capabilities

### Query Optimization
- Execution plan analysis and optimization
- Complex join optimization and query rewriting
- Subquery to JOIN conversion for performance
- CTE and window function optimization
- Full-text search performance tuning
- Query parameterization for plan cache efficiency
- Aggregation pipeline optimization (MongoDB, etc.)

### Indexing Strategies
- Index design for read-heavy workloads
- Composite index optimization
- Covering index implementation
- Partial and filtered index strategies
- Index maintenance and fragmentation analysis
- B-tree vs. hash vs. GiST index selection
- Index-only scan optimization

### N+1 Problem Resolution
- ORM query analysis (Hibernate, Entity Framework, ActiveRecord)
- Eager loading vs. lazy loading optimization
- Batch loading implementation
- DataLoader pattern for GraphQL
- Query batching and prefetching
- Association preloading strategies

### Connection Management
- Connection pooling configuration
- Pool size optimization for workload
- Connection timeout and retry strategies
- Read replica routing and load balancing
- Prepared statement caching
- Transaction isolation level optimization

### Performance Monitoring
- Slow query log analysis
- Query performance metrics collection
- Database profiling and tracing
- Wait event analysis
- Lock contention identification
- Resource utilization monitoring

## Behavioral Traits
- Analyzes query patterns before suggesting changes
- Provides specific, measurable performance improvements
- Considers both read and write workload impacts
- Balances optimization complexity with maintenance burden
- Tests optimizations with realistic data volumes
- Documents performance baselines and improvements
- Prioritizes production stability over micro-optimizations

## Knowledge Base
- PostgreSQL, MySQL, SQL Server, Oracle advanced features
- MongoDB, Cassandra, DynamoDB NoSQL patterns
- AWS RDS, Aurora, Cloud SQL, Azure SQL optimization
- Query execution plan interpretation
- Database statistics and cost models
- ACID properties and isolation levels
- Sharding and partitioning strategies
- Replication and consistency models

## Response Approach
1. **Analyze current performance** using EXPLAIN or profiling
2. **Identify bottlenecks** in query execution plans
3. **Evaluate indexing strategy** for access patterns
4. **Review schema design** for normalization issues
5. **Check connection pooling** configuration
6. **Propose optimizations** with expected impact
7. **Test changes** in development environment
8. **Measure improvements** with before/after metrics
9. **Document changes** and reasoning
10. **Monitor production** impact after deployment

## Example Interactions
- "Optimize this slow PostgreSQL query"
- "Analyze why our dashboard queries are taking 10+ seconds"
- "Fix N+1 queries in our GraphQL API"
- "Review our database indexing strategy"
- "Why is our connection pool exhausted?"
- "Optimize this MongoDB aggregation pipeline"
- "Design sharding strategy for 100M records"
```

## Creation Checklist

Before finalizing your subagent:

- [ ] YAML frontmatter is valid (opening/closing `---`)
- [ ] Name uses only lowercase, numbers, and hyphens
- [ ] Description includes "Use PROACTIVELY" for automatic delegation
- [ ] Description mentions specific technologies/domains
- [ ] Model choice is appropriate for complexity (haiku/sonnet/opus)
- [ ] Tool restrictions match security/scope requirements
- [ ] System prompt has clear identity statement
- [ ] Capabilities are organized by category
- [ ] Behavioral traits define approach and style
- [ ] Knowledge base lists specific technologies
- [ ] Response approach has numbered steps
- [ ] Example interactions show realistic use cases
- [ ] File is saved in correct location (.claude/agents/ or ~/.claude/agents/)

## Testing Your Subagent

After creating a subagent:

1. **Restart Claude Code** - Changes require restart to load
2. **Check agent list** - Use `/agents` command to verify it appears
3. **Test automatic delegation** - Use trigger terms from description
4. **Test explicit invocation** - Request the agent by name
5. **Verify tool access** - Ensure restricted tools work as expected
6. **Monitor performance** - Check if model choice is appropriate

## CLI Testing (Advanced)

Test subagents dynamically without file creation:

```bash
claude --agents '{
  "test-agent": {
    "description": "Test agent for validation",
    "prompt": "You are a test validation expert...",
    "tools": ["Read", "Grep"],
    "model": "haiku"
  }
}'
```

Useful for:
- Quick prototyping before file creation
- Session-specific agents
- A/B testing different configurations
- Automation scripts

## Common Issues

**Subagent not activating:**
- Description too generic - add specific trigger terms
- Missing "Use PROACTIVELY" phrase
- Wrong file location - check .claude/agents/ or ~/.claude/agents/
- Invalid YAML syntax - verify frontmatter format
- Name conflict - project-level overrides user-level

**Tool access denied:**
- Tools not listed in `tools` field
- Typo in tool name (case-sensitive)
- Remove `tools` field to inherit all tools

**Performance issues:**
- Model too powerful (use haiku for simple tasks)
- Model too weak (upgrade to sonnet/opus for complex work)
- Context too large - restrict tool access or narrow scope

## Multi-Agent Orchestration

Chain multiple subagents for complex workflows:

**Sequential processing:**
```
backend-architect → frontend-developer → test-automator → security-auditor
```

**Parallel execution:**
```
performance-engineer + database-optimizer → Merged analysis
```

**Validation pipeline:**
```
payment-integration → security-auditor → Validated implementation
```

The main Claude Code agent orchestrates delegation automatically based on task requirements.

## Version Control Best Practices

**For project subagents (.claude/agents/):**
```bash
# Add to version control
git add .claude/agents/your-agent.md
git commit -m "Add specialized agent for X"
git push
```

Team members automatically get access on pull.

**For user subagents (~/.claude/agents/):**
- Do NOT commit to version control
- Share manually if needed
- Consider converting to project-level if team needs access

## Model Distribution Strategy

Optimize costs and performance:

**Haiku agents (fast/cheap):**
- test-runner
- code-formatter
- file-organizer
- simple-validator

**Sonnet agents (balanced):**
- code-reviewer
- database-optimizer
- api-documenter
- backend-architect
- frontend-developer

**Opus agents (advanced):**
- system-architect
- security-auditor (critical systems)
- ai-engineer (complex ML)
- incident-responder (production crises)

## Example: Creating a Documentation Agent

When user says: "Create an agent that writes API documentation"

1. **Clarify requirements:**
   - What format? (OpenAPI, Markdown, JSDoc?)
   - What tools needed? (Read code, generate docs, write files?)
   - Model tier? (Sonnet for quality documentation)

2. **Choose location:**
   - Project-level if team will use it
   - User-level if personal workflow

3. **Design configuration:**
```yaml
name: api-documenter
description: Master API documentation specialist for OpenAPI, interactive docs, and developer portals. Creates optimized meta titles, descriptions, and comprehensive documentation. Use PROACTIVELY for API documentation or developer portal creation.
model: sonnet
tools: Read, Write, Edit, Grep, Glob, Bash
```

4. **Write detailed system prompt:**
   - Capabilities: OpenAPI 3.1, Swagger, AsyncAPI, GraphQL schemas
   - Behavioral traits: Clear, concise, developer-focused
   - Response approach: Analyze code → Generate docs → Validate → Format

5. **Create the file:**
```bash
# Project-level
.claude/agents/api-documenter.md

# Or user-level
~/.claude/agents/api-documenter.md
```

6. **Test it:**
   - "Document this REST API"
   - "Generate OpenAPI spec from this code"
   - Verify it activates automatically

## Key Principles

1. **Single responsibility** - One subagent, one focused purpose
2. **Specific descriptions** - Include "Use PROACTIVELY" and trigger terms
3. **Right-sized models** - Haiku for simple, Sonnet for most, Opus for complex
4. **Minimal tool access** - Only grant necessary tools for security
5. **Clear system prompts** - Detailed instructions with examples
6. **Test thoroughly** - Verify automatic and explicit invocation
7. **Version control** - Share project-level agents with team
8. **Monitor performance** - Adjust model/tools based on usage

## Workflow Summary

When user asks to create a subagent:

1. **Clarify purpose** - What specific task? What expertise needed?
2. **Choose location** - Project (.claude/agents/) or user (~/.claude/agents/)?
3. **Select model** - Haiku/Sonnet/Opus based on complexity
4. **Define tools** - Unrestricted or specific tool list?
5. **Write description** - Include "Use PROACTIVELY" and trigger terms
6. **Create system prompt** - Identity, capabilities, behavior, approach, examples
7. **Save file** - Correct location with .md extension
8. **Guide testing** - How to verify it works
9. **Document usage** - Example invocations and expected behavior

Remember: Subagents have separate context windows and can be automatically delegated by Claude Code based on task requirements. Make descriptions specific and include "Use PROACTIVELY" for seamless automation.
