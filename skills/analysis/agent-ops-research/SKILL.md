````skill
---
name: agent-ops-research
description: "Deep topic research with optional issue creation from findings. Use for researching technologies, patterns, libraries, or any topic requiring investigation."
category: utility
invokes: [agent-ops-state, agent-ops-tasks, agent-ops-interview]
invoked_by: [agent-ops-idea, agent-ops-planning]
state_files:
  read: [constitution.md, focus.md]
  write: [focus.md, issues/backlog.md, docs/*.md]
---

# Research Skill

## Purpose

Conduct structured research on topics, technologies, libraries, patterns, or any subject requiring investigation. Produces documented findings with optional issue creation for actionable items.

## When to Use

- Evaluating a new technology or library
- Investigating best practices for a pattern
- Researching solutions to a problem
- Comparing alternatives (frameworks, tools, approaches)
- Understanding external APIs or services
- Preparing for a design decision

## Research Modes

### Quick Research (default)
Fast investigation using available tools and knowledge.

```
/agent-research "FastAPI vs Flask for REST APIs"
→ Quick comparison based on docs and knowledge
```

### Deep Research
Thorough investigation with documentation lookup, code analysis, and structured output.

```
/agent-research deep "Implementing OAuth2 in Python"
→ Detailed findings with examples and recommendations
```

### Comparative Research
Side-by-side evaluation of alternatives.

```
/agent-research compare "pytest vs unittest vs nose2"
→ Feature matrix, pros/cons, recommendation
```

## Research Procedure

### 1. Scope Definition

Before researching, clarify:
- **Topic**: What exactly are we researching?
- **Context**: Why do we need this information?
- **Constraints**: Time budget, depth required, specific questions?
- **Output**: What format is most useful?

If scope is unclear, invoke `agent-ops-interview` for one question at a time.

### 2. Information Gathering

**Sources (in priority order):**

1. **Workspace Context**
   - Existing code patterns
   - Project documentation
   - Constitution constraints
   - Previous research (`.agent/docs/`)

2. **Built-in Knowledge**
   - Language/framework documentation
   - Common patterns and best practices
   - Known tradeoffs and gotchas

3. **External Tools (if available)**
   - Web search via MCP tools
   - Documentation lookup
   - API exploration

4. **Code Analysis**
   - Read relevant source code
   - Analyze existing implementations
   - Check test patterns

### 3. Synthesis

Organize findings into:
- **Summary**: Key takeaways (1-3 sentences)
- **Details**: Structured findings
- **Recommendations**: What to do based on findings
- **Questions**: What remains unclear
- **References**: Sources used

### 4. Output

**Console Output** (default):
```markdown
## Research: {topic}

### Summary
{1-3 sentence summary}

### Findings
{detailed structured findings}

### Recommendations
{actionable recommendations}

### Open Questions
{what we still don't know}
```

**File Output** (with `--save` or for deep research):
- Location: `.agent/docs/research-{topic-slug}.md`
- Includes full details, references, examples

## Research Output Templates

### Technology Evaluation

```markdown
## Research: {Technology Name}

### Summary
{What it is and whether we should use it}

### Overview
- **What**: {description}
- **Use case**: {when to use}
- **Alternatives**: {competing solutions}

### Evaluation

| Criterion | Rating | Notes |
|-----------|--------|-------|
| Maturity | ⭐⭐⭐⭐ | Active development, 5+ years |
| Documentation | ⭐⭐⭐ | Good but some gaps |
| Community | ⭐⭐⭐⭐⭐ | Large, active |
| Performance | ⭐⭐⭐⭐ | Benchmarks show... |
| Learning curve | ⭐⭐⭐ | Moderate |

### Pros
- {advantage 1}
- {advantage 2}

### Cons
- {disadvantage 1}
- {disadvantage 2}

### Recommendation
{recommendation with rationale}

### References
- {link or source 1}
- {link or source 2}
```

### Comparative Analysis

```markdown
## Research: {Option A} vs {Option B} vs {Option C}

### Summary
{which is best for our use case and why}

### Feature Matrix

| Feature | Option A | Option B | Option C |
|---------|----------|----------|----------|
| {feature 1} | ✅ | ✅ | ❌ |
| {feature 2} | ✅ | ❌ | ✅ |
| {feature 3} | ⚠️ | ✅ | ✅ |

### Detailed Comparison

#### Option A
- **Strengths**: ...
- **Weaknesses**: ...
- **Best for**: ...

#### Option B
...

### Recommendation
{recommendation with rationale}
```

### Problem Investigation

```markdown
## Research: {Problem Description}

### Summary
{root cause and solution}

### Problem Statement
{clear description of the problem}

### Investigation

#### Hypothesis 1: {hypothesis}
- **Evidence for**: ...
- **Evidence against**: ...
- **Verdict**: {confirmed/rejected/uncertain}

#### Hypothesis 2: {hypothesis}
...

### Root Cause
{what we determined the cause to be}

### Solutions

| Solution | Effort | Risk | Recommendation |
|----------|--------|------|----------------|
| {solution 1} | Low | Low | ✅ Recommended |
| {solution 2} | Medium | Low | Consider |
| {solution 3} | High | Medium | Only if needed |

### Recommendation
{what to do}
```

## Issue Creation from Research

After research, if actionable items are found:

```
📋 Research complete. Found {N} actionable items:

- [FEAT] Implement caching layer (from performance findings)
- [CHORE] Update dependency to fix vulnerability
- [DOCS] Document new API integration

Create issues for these? [A]ll / [S]elect / [N]one
```

## Integration with Other Skills

- **agent-ops-idea**: Research can be triggered from idea enrichment
- **agent-ops-planning**: Planning can request research for unknowns
- **agent-ops-tasks**: Research findings become backlog items
- **agent-ops-interview**: Used to clarify research scope

## MCP Tool Integration (Optional)

If MCP tools are available, research can use:

| Tool | Use Case |
|------|----------|
| `web_search` | Search for documentation, tutorials, comparisons |
| `fetch_url` | Retrieve specific documentation pages |
| `brave_search` | Alternative web search |

**Without MCP tools**: Research uses built-in knowledge and workspace analysis only.

## Research Confidence

Rate research confidence based on sources:

| Confidence | Sources |
|------------|---------|
| **High** | Official docs + code analysis + personal experience |
| **Medium** | Official docs OR established best practices |
| **Low** | Community opinions, limited sources, outdated info |

Always state confidence level in recommendations.

## Examples

### Quick Research
```
User: /agent-research "Python dataclasses vs pydantic for config"

Agent:
## Research: dataclasses vs pydantic for Configuration

### Summary
Use **pydantic** for configuration with validation, **dataclasses** for simple data containers.

### Comparison

| Feature | dataclasses | pydantic |
|---------|-------------|----------|
| Validation | ❌ Manual | ✅ Built-in |
| Type coercion | ❌ No | ✅ Yes |
| JSON parsing | ⚠️ Extra code | ✅ Built-in |
| Performance | ✅ Faster | ⚠️ Overhead |
| Dependencies | ✅ stdlib | ❌ External |

### Recommendation
For configuration files: **pydantic** (validation is critical for config)
For internal data: **dataclasses** (simpler, faster)

Confidence: **High** (based on official docs and common practice)
```

### Deep Research with Issue Creation
```
User: /agent-research deep "authentication patterns for REST API"

Agent:
## Research: REST API Authentication Patterns

### Summary
JWT with refresh tokens is recommended for our use case. Requires 3 implementation tasks.

### Findings
[...detailed analysis...]

### Recommendations
1. Implement JWT access tokens (15min expiry)
2. Add refresh token rotation
3. Store refresh tokens in httpOnly cookies

---

📋 Research complete. Found 3 actionable items:

- [FEAT] Implement JWT authentication layer
- [FEAT] Add refresh token rotation
- [SEC] Implement secure cookie storage for tokens

Create issues for these? [A]ll / [S]elect / [N]one
```

## Output

Update `.agent/focus.md`:
```markdown
## Just did
- Research: {topic}
  - Mode: {quick/deep/compare}
  - Confidence: {high/medium/low}
  - Actionable items: {N} (issues created: Y/N)
```

````
