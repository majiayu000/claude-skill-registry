---
name: review-work
description: Multi-specialist collaborative work review using independent subagents for comprehensive analysis
allowed-tools: Bash, Grep, Read, Glob, LS, Task
argument-hint: "[optional file/area to focus on]"
---

# Multi-Agent Work Review

Execute a multi-specialist work review using independent subagents.

**Usage**: `/review-work-agent [optional file/area to focus on]`

**Arguments**: Optional specific file path or area to focus the review on

## Context
- Recent changes: !git diff HEAD
- Staged changes: !git diff --staged  
- Modified files: !git status --porcelain
- Current branch: !git branch --show-current

## Implementation

Execute this multi-specialist review using the Task tool to create independent subagents:

### Phase 1: Specialist Assignment & Analysis

First, analyze the work type and determine 4-6 specialist roles needed. Then launch parallel subagents using the Task tool, including a parallel Codex "Fresh Eyes" review:

**Example Implementation**:
```
// Launch parallel specialist subagents
Task 1: "Code Quality Specialist"
- Prompt: "As a code quality specialist, review [target] by running git diff/git status, examining code for readability, maintainability, design patterns, and project conventions. Focus on framework-specific patterns, language idioms, and overall code structure based on the detected file types."

Task 2: "Security Engineer"
- Prompt: "As a security engineer, analyze [target] by examining git changes for vulnerabilities, exposed secrets, input validation issues, SQL injection risks, and XSS protection. Check authentication and authorization patterns."

Task 3: "Performance Analyst"  
- Prompt: "As a performance analyst, evaluate [target] changes for efficiency, database query optimization, React re-renders, algorithmic complexity, and scalability concerns using git diff analysis."

Task 4: "Test Coverage Specialist"
- Prompt: "As a test coverage specialist, assess [target] for testing adequacy, edge cases, integration points, and Playwright E2E testing needs. Use Tidewave MCP for Ecto schema analysis if applicable."

Task 5: "Codex Fresh Eyes Review" (PARALLEL)
- MCP: codex
- Prompt: "Review these git changes from scratch without specialist bias. Focus on overall design decisions, architectural consistency, alternative approaches, and anything that feels 'off' from a fresh perspective. What patterns do you recognize from similar codebases that might indicate future issues?"

[Additional specialists as needed based on file types...]
```

Each subagent operates independently with access to git analysis, file reading, and MCP tools.

**Specialist Selection Criteria**:
- **Code files**: Code Quality + Security + Performance + Test Coverage
- **Documentation (*.md)**: Technical Writer + Requirements Analyst + Accuracy Validator  
- **Database/Schema**: Database Specialist (w/ Tidewave + PostgreSQL CLI) + Data Security
- **Mixed changes**: Root Cause Analyst + Quality Engineer + System Architect

### Phase 2: Cross-Pollination Round

After receiving all specialist reports, launch a second round of subagents:

```
Use the Task tool to launch subagents that:
1. Review all other specialists' findings for intersections and conflicts
2. Identify systemic issues spanning multiple domains
3. Cross-validate findings from their specialist perspective
4. Flag integration risks and broader impact
5. Assess collective severity of identified issues
```

### Phase 3: Codex Meta-Analysis

After specialist synthesis, launch final Codex review:

```
Task: "Codex Synthesis Challenge"
- MCP: codex
- Input: All specialist findings + initial synthesis
- Prompt: "Review this multi-specialist analysis. What patterns do you see differently? What risks weren't considered? How would you re-prioritize these findings? Challenge the assumptions and provide alternative perspectives from your different training set."
```

### Phase 4: Final Synthesis & Prioritization

For all rounds:
- Collect all subagent outputs (including Codex perspectives)
- Synthesize findings without losing specialist perspectives
- Integrate Codex challenges and alternative viewpoints
- Prioritize by criticality: Critical → Warnings → Suggestions
- Generate actionable recommendations with file:line references

## Review Checklist

Each specialist should evaluate against these standards:

- **Code Quality**: Simple, readable, self-documenting, well-named, no duplication, follows conventions
- **Security**: No exposed secrets, proper input validation, SQL injection prevention, XSS protection  
- **Error Handling**: Proper boundaries, meaningful messages, graceful degradation
- **Performance**: Efficient algorithms, no unnecessary re-renders, proper memoization, query optimization
- **Testing**: Adequate coverage, edge cases, integration points, E2E with Playwright, smoke tests with Tidewave MCP

## Anti-Repetition Mechanisms

**Moderator Responsibilities**:
- Track thoroughly covered aspects vs. areas needing deeper analysis
- Redirect specialists to focus on unique domain contributions  
- Push for concrete examples and file:line specificity
- Synthesize complementary findings from different perspectives

**Specialist Guidelines**:
- Build on other specialists' findings rather than restating
- Focus on domain-specific insights others likely missed
- Provide concrete examples of how to fix identified issues
- Consider broader system implications of findings

## Output Protocol

```
=== MULTI-AGENT WORK REVIEW: [Target] ===
Files: [X] changed, +[Y] lines, -[Z] lines | Specialists: [Dynamic assignment]

--- ROUND 1 ---
🔍 SPECIALIST ANALYSIS
[Each specialist's git diff analysis and domain findings]

🧠 CODEX FRESH EYES
[Independent Codex perspective on changes and design decisions]

🎯 CROSS-VALIDATION  
[Specialists engage with and validate each other's findings]

⚖️ INTEGRATION ASSESSMENT
[Overall coherence and systemic issue identification]

🔄 CODEX META-ANALYSIS
[Codex challenges to specialist synthesis and alternative perspectives]

--- PRIORITIZED FINDINGS ---

🚨 CRITICAL ISSUES (must fix before commit)
- Security vulnerabilities
- Breaking changes
- Data loss risks  
- Performance regressions

⚠️ WARNINGS (should fix)
- Code quality issues
- Missing error handling
- Incomplete implementations
- Test coverage gaps

💡 SUGGESTIONS (consider improving)  
- Code style improvements
- Better naming conventions
- Refactoring opportunities
- Documentation additions

--- ACTIONABLE RECOMMENDATIONS ---
🎯 IMMEDIATE ACTIONS
[Concrete steps for critical issues with file:line references and fix examples]

📋 IMPROVEMENT PLAN
[Structured approach for addressing warnings and suggestions]

⚠️ REMAINING CONCERNS
[Issues requiring further investigation or discussion]
```

## Success Metrics
- Each specialist provides unique, non-overlapping insights with concrete file:line references
- Codex provides fresh perspective unconstrained by specialist domain focus
- Cross-validation catches issues individual specialists missed
- Codex meta-analysis challenges assumptions and offers alternative viewpoints
- Findings include specific fix examples and broader impact assessment  
- Prioritization reflects actual severity and urgency (including Codex insights)
- Output enables immediate decision-making on commit readiness

Execute the multi-agent work review starting with git analysis and dynamic specialist assignment based on detected changes.

$ARGUMENTS

Begin the multi-agent work review now, examining recent changes and launching appropriate specialists.