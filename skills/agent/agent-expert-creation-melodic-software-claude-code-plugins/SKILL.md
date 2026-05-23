---
name: agent-expert-creation
description: Create specialized agent experts with pre-loaded domain knowledge using the Act-Learn-Reuse pattern. Use when building domain-specific agents that maintain mental models via expertise files and self-improve prompts.
allowed-tools: Read, Grep, Glob, Write
---

# Agent Expert Creation Skill

Create specialized agent experts that learn and maintain domain knowledge through the Act-Learn-Reuse pattern.

## Core Problem Solved

> "The massive problem with agents is this. Your agents forget. And that means your agents don't learn."

Generic agents execute and forget. Agent experts execute and learn by maintaining expertise files (mental models) that sync with the codebase.

## When to Use

- Repeated complex tasks in a domain (database, billing, WebSocket)
- High-risk systems where mistakes cascade (security, payments)
- Rapidly evolving code that needs tracked mental models
- Need consistent domain expertise across sessions
- Building plan-build-improve automation cycles

## The Act-Learn-Reuse Pattern

```text
┌─────────────────────────────────────────────────────────────┐
│                    ACT-LEARN-REUSE CYCLE                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   ACT ──────────► LEARN ──────────► REUSE                   │
│    │                │                  │                    │
│    │                │                  │                    │
│    ▼                ▼                  ▼                    │
│  Take useful    Update expertise    Read expertise          │
│  action         file via            file FIRST on           │
│  (build, fix)   self-improve        next execution          │
│                 prompt                                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

| Step | Action | Purpose |
| --- | --- | --- |
| **ACT** | Take a useful action | Generate data to learn from (build, fix, answer) |
| **LEARN** | Store new information in expertise file | Build mental model automatically via self-improve prompt |
| **REUSE** | Read expertise first on next execution | Faster, more confident execution from mental model |

## Expertise Files (Mental Models)

> "The expertise file is the mental model of the problem space for your agent expert... This is not a source of truth. This is a working memory file, a mental model."

### Critical Distinction

| Concept | Is | Is NOT |
| --- | --- | --- |
| Expertise file | Mental model | Source of truth |
| Expertise file | Working memory | Documentation |
| Source of truth | The actual codebase | The expertise file |

### Expertise File Structure (YAML)

```yaml
overview:
  description: "High-level system description"
  tech_stack: "Key technologies"
  patterns: "Architectural patterns"

core_implementation:
  module_name:
    file: "path/to/file.py"
    lines: 400
    purpose: "What this module does"

schema_structure:  # For database experts
  tables:
    table_name:
      purpose: "What this table stores"
      key_columns: ["id", "created_at"]

key_operations:
  operation_category:
    operation_name:
      function: "function_name()"
      logic: "How it works"

best_practices:
  - "Practice 1"
  - "Practice 2"

known_issues:
  - "Issue 1 with workaround"
```

### Line Limits (Critical)

| Size | Lines | Use Case |
| --- | --- | --- |
| Small | ~300-500 | Simple domains, focused scope |
| Medium | ~600-800 | Complex domains, moderate scope |
| Maximum | ~1000 | Very complex domains (enforce limit) |

**Why limits matter:** Context window protection. Expertise files must remain scannable.

## Expert Creation Process

### Step 1: Define the Domain

Identify expertise areas based on risk and complexity:

| Risk Level | Domain Examples | Why Expert? |
| --- | --- | --- |
| **Critical** | Billing, Security | Revenue/security impact |
| **High** | Database, Auth | Foundation for everything |
| **Medium-High** | WebSocket, API | Complex event flows |
| **Medium** | DevOps, CI/CD | Infrastructure dependencies |

### Step 2: Design Expert Directory Structure

```text
.claude/commands/experts/{domain}/
  expertise.yaml        # Mental model (~600-1000 lines max)
  question.md           # REUSE: Query expertise without coding
  self-improve.md       # LEARN: Sync mental model with codebase
  plan.md               # REUSE: Create plan using expertise
  plan-build-improve.md # Full ACT→LEARN→REUSE workflow
```

### Step 3: Create the Self-Improve Prompt

> "Don't directly update this expertise file. Teach your agents how to directly update it so they can maintain it."

The self-improve prompt teaches agents HOW to learn:

```markdown
# {Domain} Expert - Self-Improve

Maintain expertise accuracy by comparing against actual codebase implementation.

## Workflow

1. **Check Git Diff** (if $1 is true)
   - Run `git diff HEAD~1` to see recent changes
   - Skip if no changes relevant to {domain}

2. **Read Current Expertise**
   - Load expertise.yaml mental model

3. **Validate Against Codebase**
   - Line-by-line verification against source files
   - Check file paths, line counts, function names

4. **Identify Discrepancies**
   - List what changed vs what expertise says
   - Prioritize significant changes

5. **Update Expertise File**
   - Sync mental model with actual code
   - Add new patterns discovered
   - Remove outdated information

6. **Enforce Line Limit (MAX_LINES: 1000)**
   - Condense if exceeding limit
   - Prioritize critical information

7. **Validation Check**
   - Ensure valid YAML syntax
   - Verify all file references exist
```

### Step 4: Create Expert Commands

The plan-build-improve triplet:

| Command | Purpose | Model | Tokens (Sub-agent) |
| --- | --- | --- | --- |
| {domain}/plan | Investigate and create specs | opus | ~80K (protected) |
| {domain}/build | Execute from specs | sonnet | Varies |
| {domain}/self-improve | Update mental model | opus | Passes git diff only |

## Expert Definition Template

### Sub-Agent Expert

```markdown
---
name: {domain}-expert
description: Expert in {domain} for {purpose}
tools: [focused tool list]
model: sonnet
color: blue
---

# {Domain} Expert

You are a {domain} expert specializing in {specific area}.

## Expertise

- Deep knowledge of {domain concepts}
- Experience with {common patterns}
- Understanding of {best practices}

## Workflow

1. Analyze the request
2. Apply domain expertise
3. Provide structured output

## Output Format

{Structured format for this expert's outputs}
```

### Plan Command

```markdown
---
description: Plan {domain} implementation with detailed specifications
argument-hint: <{domain}-request>
model: opus
allowed-tools: Read, Glob, Grep, WebFetch
---

# {Domain} Expert - Plan

You are a {domain} expert specializing in planning {domain} implementations.

## Expertise

[Pre-loaded domain knowledge here]

## Workflow

1. **Establish Expertise**
   - Read relevant documentation
   - Review existing implementations

2. **Analyze Request**
   - Understand requirements
   - Identify constraints

3. **Design Solution**
   - Architecture decisions
   - Implementation approach
   - Edge cases

4. **Create Specification**
   - Save to `specs/experts/{domain}/{name}-spec.md`
```

### Build Command

```markdown
---
description: Build {domain} implementation from specification
argument-hint: <spec-file-path>
model: sonnet
allowed-tools: Read, Write, Edit, Bash
---

# {Domain} Expert - Build

You are a {domain} expert specializing in implementing {domain} solutions.

## Workflow

1. Read the specification completely
2. Implement according to spec
3. Validate against requirements
4. Report changes made
```

### Improve Command

```markdown
---
description: Improve {domain} expert knowledge based on completed work
argument-hint: <work-summary>
model: sonnet
allowed-tools: Read, Write, Edit
---

# {Domain} Expert - Improve

Update expert knowledge based on work completed.

## Workflow

1. Analyze completed work
2. Identify new patterns learned
3. Update expert documentation
4. Capture lessons learned
```

## Example: Hook Expert

### Sub-Agent: hook-expert

```markdown
---
name: hook-expert
description: Expert in Claude Code hooks for automation
tools: [Read, Write, Edit, Bash]
model: sonnet
color: cyan
---

# Claude Code Hook Expert

You are an expert in Claude Code hooks.

## Expertise

- Hook event types (PreToolUse, PostToolUse, UserPromptSubmit, etc.)
- Hook configuration in settings.json
- Python hook implementation patterns
- UV script metadata headers
- Hook input/output contracts
```

### Commands

- `/hook_expert_plan` - Plan hook implementation
- `/hook_expert_build` - Build from spec
- `/hook_expert_improve` - Update hook expertise

## Expert File Structure

```text
.claude/
  commands/
    experts/
      {domain}/
        expertise.yaml         # Mental model (600-1000 lines)
        question.md            # Query expertise ($1 = question)
        self-improve.md        # Sync mental model ($1 = check_git_diff)
        plan.md                # Create plan ($1 = task)
        plan-build-improve.md  # Full workflow ($1 = task)

  agents/
    {domain}-expert.md         # Sub-agent definition

specs/
  experts/
    {domain}/
      {feature-name}-spec.md   # Generated specifications
```

## Seeding Strategy

### How to Bootstrap an Expert

1. **Start Blank** - Let agent discover structure

   ```yaml
   # expertise.yaml (initial)
   overview:
     description: "To be populated"
   ```

2. **Run Self-Improve** - Agent builds initial expertise

   ```bash
   /experts/{domain}/self-improve true
   ```

3. **Iterate** - Run self-improve until agent stops finding changes

4. **Validate** - Ensure accuracy against codebase

### When NOT to Build Experts

| Anti-Pattern | Problem |
| --- | --- |
| Stable, unchanging code | Wasted effort - no learning needed |
| Simple/trivial systems | Overhead exceeds benefit |
| Domains you don't understand | Garbage in, garbage out |
| Everything at once | Start with highest-risk domains |

## Anti-Patterns

| Anti-Pattern | Problem | Solution |
| --- | --- | --- |
| Treating expertise as source of truth | Creates duplication, conflicts | Mental model validates against code |
| Manually updating expertise files | Wastes engineer time | Let self-improve prompt maintain |
| Infinite expertise growth | Context window bloat | Enforce line limits (~1000 max) |
| No seeding strategy | Unclear starting point | Start simple, let agent define structure |
| Building experts for stable code | Wasted effort | Only for evolving, complex systems |
| Experts without understanding | Garbage in, garbage out | You must understand the domain first |

## Expert Patterns

### Pattern: Read-Only Expert

For analysis without modification:

```text
Tools: Read, Glob, Grep
Purpose: Audit, review, analyze
Output: Reports and recommendations
```

### Pattern: Build Expert

For implementation work:

```text
Tools: Read, Write, Edit, Bash
Purpose: Create, modify, implement
Output: Code changes and artifacts
```

### Pattern: Research Expert

For information gathering:

```text
Tools: WebFetch, Read, Write
Purpose: Fetch, process, organize
Output: Documentation and summaries
```

## Output Format

When creating an expert, generate:

```json
{
  "expert_name": "{domain}-expert",
  "purpose": "{expertise description}",
  "components": {
    "sub_agent": "{domain}-expert.md",
    "plan_command": "{domain}_expert_plan.md",
    "build_command": "{domain}_expert_build.md",
    "improve_command": "{domain}_expert_improve.md"
  },
  "directories_needed": [
    ".claude/commands/experts/{domain}_expert/",
    "specs/experts/{domain}/",
    "ai_docs/{domain}/"
  ],
  "tools_assigned": ["list", "of", "tools"],
  "model_assignment": {
    "plan": "opus",
    "build": "sonnet",
    "improve": "sonnet"
  }
}
```

## Key Quotes

> "The difference between a generic agent and an agent expert is simple. One executes and forgets, the other executes and learns."
>
> "True experts are always learning. They're updating their mental model."
>
> "Build the system that builds the system. Do not work on the application layer."

## Cross-References

These are conceptual references to TAC course materials and patterns:

- **One Agent, One Purpose** - Specialization principle (TAC Lesson 6)
- **R&D Framework** - Reduce & Delegate strategy (TAC Lesson 8)
- **Context Priming Patterns** - Loading domain context (TAC Lesson 9)
- **12 Leverage Points** - Leverage point #3: System Prompts (TAC Lesson 3)
- **TAC Lesson 13: Agent Experts** - Act-Learn-Reuse pattern source

---

**Last Updated:** 2025-12-15

## Version History

- **v1.0.0** (2025-12-26): Initial release

---
