---
name: anthropic-architect
description: Determine the best Anthropic architecture for your project by analyzing requirements and recommending the optimal combination of Skills, Agents, Prompts, and SDK primitives.
---

# Anthropic Architect

Expert architectural guidance for Anthropic-based projects. Analyze your requirements and receive tailored recommendations on the optimal architecture using Skills, Agents, Subagents, Prompts, and SDK primitives.

## What This Skill Does

Helps you design the right Anthropic architecture for your project by:
- **Analyzing project requirements** - Understanding complexity, scope, and constraints
- **Recommending architectures** - Skills vs Agents vs Prompts vs SDK primitives
- **Applying decision rubrics** - Data-driven architectural choices
- **Following best practices** - 2025 Anthropic patterns and principles
- **Progressive disclosure design** - Efficient context management
- **Security considerations** - Safe, controllable AI systems

## Why Architecture Matters

**Without proper architecture:**
- Inefficient context usage and high costs
- Poor performance and slow responses
- Security vulnerabilities and risks
- Difficult to maintain and scale
- Agents reading entire skill contexts unnecessarily
- Mixed concerns and unclear boundaries

**With engineered architecture:**
- Optimal context utilization
- Fast, focused responses
- Secure, controlled operations
- Easy to maintain and extend
- Progressive disclosure of information
- Clear separation of concerns
- Scalable and reusable components

## Quick Start

### Analyze Your Project

```
Using the anthropic-architect skill, help me determine the best
architecture for: [describe your project]

Requirements:
- [List your key requirements]
- [Complexity level]
- [Reusability needs]
- [Security constraints]
```

### Get Architecture Recommendation

The skill will provide:
1. **Recommended architecture** - Specific primitives to use
2. **Decision reasoning** - Why this architecture fits
3. **Implementation guidance** - How to build it
4. **Best practices** - What to follow
5. **Example patterns** - Similar successful architectures

## The Four Anthropic Primitives

### 1. Skills (Prompt-Based Meta-Tools)

**What:** Organized folders of instructions, scripts, and resources that agents can discover and load dynamically.

**When to use:**
- ✅ Specialized domain knowledge needed
- ✅ Reusable across multiple projects
- ✅ Complex, multi-step workflows
- ✅ Reference materials required
- ✅ Progressive disclosure beneficial

**When NOT to use:**
- ❌ Simple, one-off tasks
- ❌ Project-specific logic only
- ❌ No need for reusability

**Example use cases:**
- Prompt engineering expertise
- Design system generation
- Code review guidelines
- Domain-specific knowledge (finance, medical, legal)

### 2. Agents/Subagents (Autonomous Task Handlers)

**What:** Specialized agents with independent system prompts, dedicated context windows, and specific tool permissions.

**When to use:**
- ✅ Complex, multi-step autonomous tasks
- ✅ Need for isolated context
- ✅ Different tool permissions required
- ✅ Parallel task execution
- ✅ Specialized expertise per task type

**When NOT to use:**
- ❌ Simple queries or lookups
- ❌ Shared context required
- ❌ Sequential dependencies
- ❌ Resource-constrained environments

**Example use cases:**
- Code exploration and analysis
- Test generation and execution
- Documentation generation
- Security audits
- Performance optimization

### 3. Direct Prompts (Simple Instructions)

**What:** Clear, explicit instructions passed directly to Claude without additional structure.

**When to use:**
- ✅ Simple, straightforward tasks
- ✅ One-time operations
- ✅ Quick questions or clarifications
- ✅ No need for specialization
- ✅ Minimal context required

**When NOT to use:**
- ❌ Complex, multi-step processes
- ❌ Need for reusability
- ❌ Requires domain expertise
- ❌ Multiple related operations

**Example use cases:**
- Code explanations
- Quick refactoring
- Simple bug fixes
- Documentation updates
- Direct questions

### 4. SDK Primitives (Custom Workflows)

**What:** Low-level building blocks from the Claude Agent SDK to create custom agent workflows.

**When to use:**
- ✅ Unique workflow requirements
- ✅ Custom tool integration needed
- ✅ Specific feedback loops required
- ✅ Integration with existing systems
- ✅ Fine-grained control needed

**When NOT to use:**
- ❌ Standard use cases covered by Skills/Agents
- ❌ Limited development resources
- ❌ Maintenance burden concern
- ❌ Faster time-to-market priority

**Example use cases:**
- Custom CI/CD integration
- Specialized code analysis pipelines
- Domain-specific automation
- Integration with proprietary systems

## Decision Rubric

Use this rubric to determine the right architecture:

### Task Complexity Analysis

**Low Complexity** → Direct Prompts
- Single operation
- Clear input/output
- No dependencies
- < 5 steps

**Medium Complexity** → Skills
- Multiple related operations
- Reusable patterns
- Reference materials helpful
- 5-20 steps

**High Complexity** → Agents/Subagents
- Multi-step autonomous workflow
- Needs isolated context
- Different tool permissions
- > 20 steps or parallel tasks

**Custom Complexity** → SDK Primitives
- Unique workflows
- System integration required
- Custom tools needed
- Specific feedback loops

### Reusability Assessment

**Single Use** → Direct Prompts
- One-time task
- Project-specific
- No future reuse

**Team Reuse** → Skills
- Multiple team members benefit
- Common workflows
- Shareable knowledge

**Organization Reuse** → Skills + Marketplace
- Cross-team benefit
- Standard patterns
- Company-wide knowledge

**Product Feature** → SDK Primitives
- End-user facing
- Production deployment
- Custom integration

### Context Management Needs

**Minimal Context** → Direct Prompts
- Self-contained task
- No external references
- Simple instructions

**Structured Context** → Skills
- Progressive disclosure needed
- Reference materials required
- Organized information

**Isolated Context** → Agents/Subagents
- Separate concerns
- Avoid context pollution
- Parallel execution

**Custom Context** → SDK Primitives
- Specific context handling
- Integration requirements
- Fine-grained control

### Security & Control Requirements

**Basic Safety** → Direct Prompts + Skills
- Standard guardrails
- No sensitive operations
- Read-only or low-risk

**Controlled Access** → Agents with Tool Restrictions
- Specific tool permissions
- Allowlist approach
- Confirmation required

**High Security** → SDK Primitives + Custom Controls
- Deny-all default
- Explicit confirmations
- Audit logging
- Custom security layers

## Architecture Patterns

### Pattern 1: Skills-First Architecture

**Use when:** Building reusable expertise and workflows

**Structure:**
```
Project
├── skills/
│   ├── domain-expert/
│   │   ├── SKILL.md
│   │   └── references/
│   │       ├── patterns.md
│   │       ├── best_practices.md
│   │       └── examples.md
│   └── workflow-automation/
│       ├── SKILL.md
│       └── scripts/
│           └── automate.sh
└── .claude/
    └── config
```

**Benefits:**
- Reusable across projects
- Progressive disclosure
- Easy to share and maintain
- Clear documentation

### Pattern 2: Agent-Based Architecture

**Use when:** Complex autonomous tasks with isolated concerns

**Structure:**
```
Main Agent (orchestrator)
├── Explore Agent (codebase analysis)
├── Plan Agent (task planning)
├── Code Agent (implementation)
└── Review Agent (validation)
```

**Benefits:**
- Parallel execution
- Isolated contexts
- Specialized expertise
- Clear responsibilities

### Pattern 3: Hybrid Architecture

**Use when:** Complex projects with varied requirements

**Structure:**
```
Main Conversation
├── Direct Prompts (simple tasks)
├── Skills (reusable expertise)
│   ├── code-review-skill
│   └── testing-skill
└── Subagents (complex workflows)
    ├── Explore Agent
    └── Plan Agent
```

**Benefits:**
- Right tool for each task
- Optimal resource usage
- Flexible and scalable
- Best of all approaches

### Pattern 4: SDK Custom Architecture

**Use when:** Unique requirements or product features

**Structure:**
```
Custom Agent SDK Implementation
├── Custom Tools
├── Specialized Feedback Loops
├── System Integrations
└── Domain-Specific Workflows
```

**Benefits:**
- Full control
- Custom integration
- Unique workflows
- Production-ready

## Key Principles (2025)

### 1. Progressive Disclosure
**What:** Show only what's needed, when it's needed.

**Why:** Avoids context limits, reduces costs, improves performance.

**How:** Organize skills with task-based navigation, provide query tools, structure information hierarchically.

### 2. Context as Resource
**What:** Treat context window as precious, limited resource.

**Why:** Every token counts toward limits and costs.

**How:** Use progressive disclosure, prefer retrieval over dumping, compress aggressively, reset periodically.

### 3. Clear Instructions
**What:** Explicit, unambiguous directions.

**Why:** Claude 4.x responds best to clarity.

**How:** Be specific, define output format, provide examples, avoid vagueness.

### 4. Security by Design
**What:** Deny-all default, allowlist approach.

**Why:** Safe, controlled AI systems.

**How:** Limit tool access, require confirmations, audit operations, block dangerous commands.

### 5. Thinking Capabilities
**What:** Leverage Claude's extended thinking mode.

**Why:** Better results for complex reasoning.

**How:** Request step-by-step thinking, allow reflection after tool use, guide initial thinking.

### 6. Two-Message Pattern
**What:** Use meta messages for context without UI clutter.

**Why:** Clean UX while providing necessary context.

**How:** Set isMeta: true for system messages, use for skill loading, keep UI focused.

## Reference Materials

All architectural patterns, decision frameworks, and examples are in the `references/` directory:

- **decision_rubric.md** - Comprehensive decision framework
- **architectural_patterns.md** - Detailed pattern catalog
- **best_practices.md** - 2025 Anthropic best practices
- **use_case_examples.md** - Real-world architecture examples

## Usage Examples

### Example 1: Determining Architecture for Content Generation

**Input:**
```
Using anthropic-architect, I need to build a system that:
- Generates blog posts from product features
- Ensures brand voice consistency
- Includes SEO optimization
- Reusable across marketing team
```

**Analysis:**
- Medium complexity (structured workflow)
- High reusability (team-wide)
- Domain expertise needed (content, SEO, brand)
- Progressive disclosure beneficial

**Recommendation:** **Skills-First Architecture**
- Create `content-generator` skill
- Include brand voice references
- SEO guidelines in references
- Example templates
- Progressive disclosure for different content types

### Example 2: Code Refactoring Tool

**Input:**
```
Using anthropic-architect, I want to:
- Analyze codebase for refactoring opportunities
- Generate refactoring plan
- Execute refactoring with tests
- Review and validate changes
```

**Analysis:**
- High complexity (multi-step, autonomous)
- Different contexts needed (explore, plan, code, review)
- Parallel execution beneficial
- Tool permissions vary by stage

**Recommendation:** **Agent-Based Architecture**
- Main orchestrator agent
- Explore subagent (read-only, codebase analysis)
- Plan subagent (planning, no execution)
- Code subagent (write permissions)
- Review subagent (validation, test execution)

### Example 3: Simple Code Review

**Input:**
```
Using anthropic-architect, I need to:
- Review this PR for bugs
- Check code style
- Suggest improvements
```

**Analysis:**
- Low complexity (single operation)
- One-time task
- No reusability needed
- Minimal context

**Recommendation:** **Direct Prompt**
- Simple, clear instructions
- No skill/agent overhead
- Fast execution
- Sufficient for task

### Example 4: Custom CI/CD Integration

**Input:**
```
Using anthropic-architect, I want to:
- Integrate Claude into CI pipeline
- Custom tool for deployment validation
- Specific workflow for our stack
- Production feature
```

**Analysis:**
- Custom complexity
- System integration required
- Production deployment
- Unique workflows

**Recommendation:** **SDK Primitives**
- Build custom agent with SDK
- Implement custom tools
- Create specialized feedback loops
- Integration with CI system

## Best Practices Checklist

When designing your architecture:

- [ ] Analyzed task complexity accurately
- [ ] Considered reusability requirements
- [ ] Evaluated context management needs
- [ ] Assessed security requirements
- [ ] Applied progressive disclosure where beneficial
- [ ] Chose simplest solution that works
- [ ] Documented architectural decisions
- [ ] Planned for maintenance and updates
- [ ] Considered cost implications
- [ ] Validated with prototype/POC

## Common Anti-Patterns

### Anti-Pattern 1: Over-Engineering
**Problem:** Using Agents/SDK for simple tasks

**Solution:** Start simple, scale complexity as needed

### Anti-Pattern 2: Context Dumping
**Problem:** Loading entire skills into context

**Solution:** Use progressive disclosure, query tools

### Anti-Pattern 3: Mixed Concerns
**Problem:** Single skill/agent doing too much

**Solution:** Separate concerns, use subagents or multiple skills

### Anti-Pattern 4: No Security Boundaries
**Problem:** Full tool access for all agents

**Solution:** Allowlist approach, minimal permissions

### Anti-Pattern 5: Ignoring Reusability
**Problem:** Recreating same prompts repeatedly

**Solution:** Extract to skills, share across projects

## Getting Started

### Step 1: Describe Your Project
Provide clear requirements, complexity level, and constraints.

### Step 2: Receive Recommendation
Get tailored architecture with reasoning.

### Step 3: Review Patterns
Explore similar successful architectures.

### Step 4: Implement
Follow implementation guidance.

### Step 5: Iterate
Refine based on results and feedback.

## Summary

The Anthropic Architect skill helps you:
- Choose the right primitives for your needs
- Design scalable, maintainable architectures
- Follow 2025 best practices
- Avoid common pitfalls
- Optimize for performance and cost

**Key Primitives:**
- **Skills** - Reusable domain expertise
- **Agents** - Autonomous complex workflows
- **Prompts** - Simple direct tasks
- **SDK** - Custom integrations

**Core Principles:**
- Progressive disclosure
- Context as resource
- Security by design
- Clear instructions
- Right tool for the job

---

**"The best architecture is the simplest one that meets your requirements."**
