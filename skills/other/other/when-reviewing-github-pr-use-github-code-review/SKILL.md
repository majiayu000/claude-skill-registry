---
name: when-reviewing-github-pr-use-github-code-review
description: Comprehensive GitHub pull request code review using multi-agent swarm with specialized reviewers for security, performance, style, tests, and documentation. Coordinates security-auditor, perf-analyzer, code-analyzer, tester, and reviewer agents through mesh topology for parallel analysis. Provides detailed feedback with auto-fix suggestions and merge readiness assessment. Use when reviewing PRs, conducting code audits, or ensuring code quality standards before merge.
agents:
  - security-auditor
  - perf-analyzer
  - code-analyzer
  - tester
  - reviewer
topology: mesh
mcp_tools:
  - mcp__claude-flow__swarm_init
  - mcp__claude-flow__agent_spawn
  - mcp__claude-flow__task_orchestrate
  - mcp__flow-nexus__github_repo_analyze
---

# GitHub Code Review Skill

## Overview

Execute comprehensive, multi-dimensional code reviews for GitHub pull requests using coordinated agent swarms. This skill orchestrates five specialized agents working in parallel to analyze security, performance, code quality, test coverage, and documentation, then synthesizes findings into actionable feedback with merge readiness assessment.

## When to Use This Skill

Activate this skill when reviewing pull requests before merge approval, conducting security audits on code changes, assessing performance implications of new code, validating test coverage and quality standards, or providing structured feedback to contributors.

Use this skill for both internal team PRs and external contributor submissions, complex feature additions requiring thorough review, refactoring changes that impact system architecture, or establishing code review standards and automation.

## Agent Coordination Architecture

### Swarm Topology

Initialize a **mesh topology** for maximum parallel execution and peer-to-peer communication between specialized reviewers. Mesh topology enables each agent to share findings directly with others, creating a comprehensive understanding through collective intelligence.

```bash
# Initialize mesh swarm for PR review
npx claude-flow@alpha swarm init --topology mesh --max-agents 5 --strategy specialized
```

### Specialized Agent Roles

**Security Auditor** (`security-auditor`): Analyze code for security vulnerabilities, injection risks, authentication/authorization flaws, secrets exposure, and dependency vulnerabilities. Check for OWASP Top 10 violations and compliance requirements.

**Performance Analyzer** (`perf-analyzer`): Evaluate performance implications including algorithmic complexity, memory usage patterns, database query efficiency, caching opportunities, and potential bottlenecks. Flag resource-intensive operations.

**Code Analyzer** (`code-analyzer`): Assess code quality, maintainability, and adherence to style guidelines. Check naming conventions, code organization, design patterns, complexity metrics, and architectural consistency.

**Test Engineer** (`tester`): Review test coverage, test quality, and testing best practices. Validate unit tests, integration tests, edge case handling, and test maintainability. Identify gaps in coverage.

**Documentation Reviewer** (`reviewer`): Evaluate documentation quality including code comments, API documentation, README updates, and inline documentation. Ensure clarity and completeness for future maintainers.

## Review Workflow (SOP)

### Phase 1: Initialization and Context Loading

**Step 1.1: Initialize Swarm Coordination**

Set up mesh topology for parallel agent execution:

```bash
# Use MCP tools to initialize coordination
mcp__claude-flow__swarm_init topology=mesh maxAgents=5 strategy=specialized

# Spawn specialized agents
mcp__claude-flow__agent_spawn type=analyst name=security-auditor
mcp__claude-flow__agent_spawn type=optimizer name=perf-analyzer
mcp__claude-flow__agent_spawn type=analyst name=code-analyzer
mcp__claude-flow__agent_spawn type=researcher name=tester
mcp__claude-flow__agent_spawn type=researcher name=reviewer
```

**Step 1.2: Fetch PR Context**

Use the bundled `github-api.sh` script to fetch PR details:

```bash
# Fetch PR metadata, files changed, and existing comments
bash scripts/github-api.sh fetch-pr <owner> <repo> <pr-number>
```

Store PR context in memory for agent access:

```bash
# Save PR context for swarm coordination
npx claude-flow@alpha hooks post-edit \
  --file "pr-context.json" \
  --memory-key "github/pr-review/context"
```

**Step 1.3: Load Review Criteria**

Reference `references/review-criteria.md` for comprehensive standards. This document contains security checklists, performance benchmarks, code style guidelines, test coverage requirements, and documentation standards.

### Phase 2: Parallel Agent Review Execution

Execute all five agents concurrently using Claude Code's Task tool. Each agent runs independently while coordinating through shared memory.

**Launch Concurrent Reviews:**

```plaintext
Task("Security Auditor", "
  Analyze PR for security vulnerabilities:
  1. Check for SQL injection, XSS, CSRF vulnerabilities
  2. Validate authentication and authorization logic
  3. Scan for exposed secrets and credentials
  4. Review dependency security with npm audit / cargo audit
  5. Check OWASP Top 10 compliance

  Use scripts/security-scan.sh for automated scanning.
  Store findings in memory: github/pr-review/security
  Run hooks: npx claude-flow@alpha hooks pre-task --description 'security review'
", "security-auditor")

Task("Performance Analyzer", "
  Evaluate performance implications:
  1. Analyze algorithmic complexity (Big O notation)
  2. Identify memory allocation patterns
  3. Review database queries for N+1 problems
  4. Check caching strategies
  5. Flag synchronous blocking operations

  Use scripts/perf-analysis.sh for profiling data.
  Store findings in memory: github/pr-review/performance
  Run hooks: npx claude-flow@alpha hooks pre-task --description 'performance analysis'
", "perf-analyzer")

Task("Code Quality Analyst", "
  Assess code quality and maintainability:
  1. Check adherence to style guide (references/style-guide.md)
  2. Evaluate naming conventions and clarity
  3. Calculate cyclomatic complexity
  4. Review error handling patterns
  5. Validate architectural consistency

  Use scripts/code-quality.sh for automated linting.
  Store findings in memory: github/pr-review/quality
  Run hooks: npx claude-flow@alpha hooks pre-task --description 'code quality review'
", "code-analyzer")

Task("Test Coverage Engineer", "
  Review testing comprehensiveness:
  1. Measure test coverage percentage
  2. Evaluate test quality and assertions
  3. Check edge case handling
  4. Validate test isolation and independence
  5. Review test documentation

  Use scripts/test-coverage.sh for coverage reports.
  Store findings in memory: github/pr-review/testing
  Run hooks: npx claude-flow@alpha hooks pre-task --description 'test review'
", "tester")

Task("Documentation Reviewer", "
  Evaluate documentation completeness:
  1. Review inline code comments
  2. Check API documentation updates
  3. Validate README changes
  4. Assess documentation clarity
  5. Verify examples and usage guides

  Store findings in memory: github/pr-review/documentation
  Run hooks: npx claude-flow@alpha hooks pre-task --description 'documentation review'
", "reviewer")
```

### Phase 3: Synthesis and Report Generation

After all agents complete their reviews, synthesize findings into a unified report.

**Step 3.1: Aggregate Agent Findings**

Retrieve all agent findings from memory:

```bash
# Collect all review findings
npx claude-flow@alpha memory retrieve --key "github/pr-review/*"
```

**Step 3.2: Generate Comprehensive Report**

Create structured report using the template in `references/review-report-template.md`:

**Report Structure:**
- Executive Summary (merge readiness decision)
- Security Findings (critical/high/medium/low severity)
- Performance Assessment (bottlenecks, optimizations)
- Code Quality Analysis (complexity, maintainability)
- Test Coverage Report (percentage, gaps, improvements)
- Documentation Review (completeness, clarity)
- Auto-Fix Suggestions (automated remediation options)
- Action Items (prioritized recommendations)

**Step 3.3: Calculate Merge Readiness Score**

Apply weighted scoring algorithm:
- Security: 35% weight (blocking if critical issues found)
- Performance: 20% weight
- Code Quality: 20% weight
- Test Coverage: 15% weight
- Documentation: 10% weight

Merge readiness thresholds:
- **Approved**: Score >= 85%, no critical security issues
- **Approved with Comments**: Score 70-84%, minor improvements suggested
- **Changes Requested**: Score < 70% or critical issues present

### Phase 4: Auto-Fix Suggestion Generation

For each identified issue, generate concrete fix suggestions where applicable.

**Step 4.1: Security Auto-Fixes**

Use `scripts/security-fixes.sh` to generate patches for common security issues:
- Remove exposed secrets and add to `.gitignore`
- Add input validation and sanitization
- Fix SQL injection vulnerabilities with parameterized queries
- Add CSRF tokens to form submissions
- Update vulnerable dependencies

**Step 4.2: Performance Auto-Fixes**

Generate optimization suggestions:
- Add database indexes for slow queries
- Implement caching layers
- Replace synchronous operations with async
- Optimize algorithm complexity
- Add pagination for large data sets

**Step 4.3: Code Quality Auto-Fixes**

Apply automated refactoring:
- Break down complex functions (cyclomatic complexity > 10)
- Extract magic numbers to named constants
- Improve naming conventions
- Add error handling
- Format code to style guidelines

### Phase 5: GitHub Integration and Feedback

Post comprehensive review feedback directly to the pull request.

**Step 5.1: Format Review Comments**

Use GitHub API to post structured review:

```bash
# Post comprehensive review to GitHub
bash scripts/github-api.sh post-review \
  --repo <owner/repo> \
  --pr <number> \
  --event <APPROVE|COMMENT|REQUEST_CHANGES> \
  --body-file "review-report.md"
```

**Step 5.2: Add Inline Code Comments**

For specific code issues, add inline comments at relevant line numbers:

```bash
# Add inline comments for each finding
bash scripts/github-api.sh add-comment \
  --repo <owner/repo> \
  --pr <number> \
  --path <file-path> \
  --line <line-number> \
  --body "<comment-text>"
```

**Step 5.3: Apply Labels and Assignees**

Categorize the PR with appropriate labels:

```bash
# Apply review labels
bash scripts/github-api.sh add-labels \
  --repo <owner/repo> \
  --pr <number> \
  --labels "needs-security-review,performance-review,documentation-needed"
```

### Phase 6: Continuous Monitoring

Set up monitoring for PR updates and re-reviews.

**Step 6.1: Track PR Changes**

Monitor for new commits that address feedback:

```bash
# Subscribe to PR updates
mcp__flow-nexus__realtime_subscribe table=pull_requests event=UPDATE
```

**Step 6.2: Trigger Re-Review**

When significant changes are pushed, trigger automated re-review of affected areas only:

```bash
# Orchestrate targeted re-review
mcp__claude-flow__task_orchestrate \
  task="Re-review changed files in PR #<number>" \
  strategy=adaptive \
  maxAgents=3
```

## MCP Tool Integration

### Flow-Nexus GitHub Tools

Use advanced GitHub integration tools when available:

```bash
# Analyze repository for context
mcp__flow-nexus__github_repo_analyze repo=<owner/repo> analysis_type=code_quality

# Get PR details with advanced metrics
mcp__flow-nexus__github_pr_analyze repo=<owner/repo> pr=<number>
```

### Claude Flow Coordination

Leverage coordination tools for swarm management:

```bash
# Monitor review progress
mcp__claude-flow__swarm_status verbose=true

# Get agent performance metrics
mcp__claude-flow__agent_metrics metric=all

# Check task completion
mcp__claude-flow__task_status detailed=true
```

## Best Practices

**Parallel Execution**: Always run all five agents concurrently in a single message using Claude Code's Task tool. This maximizes speed (2.8-4.4x improvement) and enables cross-agent learning.

**Memory Coordination**: Each agent stores findings in memory using standardized keys (`github/pr-review/<category>`). This enables synthesis phase to aggregate findings efficiently.

**Hooks Integration**: All agents run pre-task and post-task hooks for:
- Session restoration (access shared context)
- Progress tracking (coordinate completion)
- Memory updates (store findings)
- Performance metrics (track efficiency)

**Automated Fixes**: Generate concrete fix suggestions, not just problem identification. Provide code snippets, commands, or automated patches where possible.

**Context Awareness**: Review code in context of the full repository architecture. Reference existing patterns, style guides, and conventions from the codebase.

**Progressive Disclosure**: For large PRs (>20 files changed), prioritize critical files and high-risk changes first. Review remaining files in subsequent passes.

## Error Handling

**GitHub API Rate Limits**: Implement exponential backoff and caching. Use GraphQL API for complex queries to reduce request count.

**Large PR Handling**: For PRs with >50 files, batch reviews by logical groupings (features, bug fixes, refactoring). Run multiple review sessions.

**Agent Failures**: If an agent fails, continue with remaining agents and note the gap in the final report. Retry failed agent independently.

**Merge Conflicts**: Flag merge conflicts during review and suggest resolution strategies based on conflict type.

## Output Format

The final review report includes:

1. **Executive Summary** (3-5 sentences)
2. **Merge Readiness Decision** (Approved/Approved with Comments/Changes Requested)
3. **Security Findings** (categorized by severity with CWE references)
4. **Performance Analysis** (bottlenecks, Big O complexity, optimization opportunities)
5. **Code Quality Metrics** (complexity scores, maintainability index, style violations)
6. **Test Coverage Report** (percentage, gaps, recommendations)
7. **Documentation Assessment** (completeness score, missing sections)
8. **Auto-Fix Suggestions** (concrete code changes for each issue)
9. **Action Items** (prioritized list of required/recommended changes)
10. **Comparison to Previous Reviews** (trend analysis if historical data available)

## Advanced Features

**Learning from Feedback**: Track which review comments are addressed vs dismissed. Train neural patterns on successful reviews to improve future accuracy.

**Custom Review Profiles**: Create organization-specific review profiles with weighted priorities (e.g., security-first for fintech, performance-first for real-time systems).

**Integration with CI/CD**: Trigger automated reviews on PR creation via GitHub Actions workflow. Block merges until review approval obtained.

**Reviewer Assignment**: Automatically assign human reviewers based on code ownership (CODEOWNERS file) and agent findings (route security issues to security team).

## References

- `references/review-criteria.md` - Comprehensive review standards
- `references/review-report-template.md` - Report formatting template
- `references/style-guide.md` - Code style guidelines
- `references/security-checklist.md` - OWASP security standards
- `scripts/github-api.sh` - GitHub API interaction utilities
- `scripts/security-scan.sh` - Automated security scanning
- `scripts/perf-analysis.sh` - Performance profiling
- `scripts/code-quality.sh` - Code quality analysis
- `scripts/test-coverage.sh` - Test coverage reporting
- `scripts/security-fixes.sh` - Automated security fix generation
