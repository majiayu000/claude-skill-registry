---
name: superclaude-prompt-generator
description: Expert SuperClaude prompt engineering assistant that analyzes user needs and crafts optimal prompts using the full SuperClaude framework - commands, flags, personas, MCP servers, wave orchestration, parallel execution patterns, continuous execution directives, and the new PM Agent orchestration system with PDCA cycles and Serena memory integration.
version: 2.3.0
author: SuperClaude Framework
category: productivity
---

# SuperClaude Prompt Generator

**Expert prompt engineering for the SuperClaude framework**

This skill helps you craft optimal SuperClaude prompts by:
- Analyzing your current need and context
- Selecting the right commands, flags, personas, and MCP servers
- Leveraging orchestration and parallel execution patterns
- Applying parallel-by-default optimization strategies
- Explaining the reasoning behind each prompt design choice
- Ensuring best practices and framework compliance

## 🔴 CRITICAL: All SuperClaude Prompts MUST Start with a Command

**Every generated prompt MUST begin with a `/sc:` command.** This is non-negotiable for SuperClaude framework compliance.

### Why Commands Are Mandatory
- Commands activate the SuperClaude orchestration engine
- Commands enable auto-persona activation and MCP coordination
- Commands trigger wave orchestration for complex operations
- Commands ensure proper task management and quality gates
- Natural language alone bypasses the SuperClaude framework

### Command Selection Priority
1. **First**: Choose the most appropriate `/sc:` command from available commands
2. **Always**: Start the prompt with the command + required arguments
3. **Then**: Add flags, personas, and other modifiers
4. **Never**: Generate prompts without a leading `/sc:` command

**Available Commands: 30+ total** (organized by category)

**Development & Implementation** (4 commands):
- `/sc:build` - Project builder with framework detection
- `/sc:implement` - Feature and code implementation with intelligent persona activation
- `/sc:design` - Design orchestration across architecture, API, and UI domains
- `/sc:workflow` - Generate implementation workflows from PRDs and feature requirements

**Analysis & Investigation** (4 commands):
- `/sc:analyze` - Multi-dimensional code and system analysis (wave-enabled)
- `/sc:troubleshoot` - Problem investigation and debugging
- `/sc:explain` - Educational explanations of code and concepts
- `/sc:business-panel` - Multi-expert business strategy analysis

**Quality & Enhancement** (2 commands):
- `/sc:improve` - Evidence-based code enhancement (wave-enabled)
- `/sc:cleanup` - Systematic technical debt reduction and code cleanup

**Planning & Estimation** (3 commands):
- `/sc:task` - Long-term project management and task orchestration
- `/sc:estimate` - Evidence-based development estimation
- `/sc:brainstorm` - Interactive requirements discovery and exploration

**Testing** (1 command):
- `/sc:test` - Comprehensive testing workflows with Playwright integration

**Documentation** (1 command):
- `/sc:document` - Generate focused documentation for components and APIs

**Version Control** (1 command):
- `/sc:git` - Git workflow assistant with intelligent commit messages

**Session Lifecycle** (3 commands):
- `/sc:load` - Load project context and session state using Serena MCP
- `/sc:save` - Save session context with timestamped versioning
- `/sc:reflect` - Task validation and quality reflection using Serena MCP

**Meta & Discovery** (3 commands):
- `/sc:index` - Browse command catalog and framework documentation
- `/sc:help` - List all available /sc commands with descriptions
- `/sc:select-tool` - Intelligent MCP tool selection (Serena vs Morphllm routing)

**Orchestration & Project Management** (4 commands - NEW):
- `/sc:pm` - **PM Agent**: Always-active orchestration layer with PDCA cycles and Serena memory integration
- `/sc:agent` - SC Agent session controller that orchestrates investigation, implementation, and review
- `/sc:recommend` - Ultra-intelligent command recommendation engine with multi-language support
- `/sc:index-repo` - Repository indexing for 94% token reduction (58K → 3K tokens)

**Expert Review** (1 command):
- `/sc:spec-panel` - Multi-expert specification review and critique

**Team Coordination** (1 command):
- `/sc:team` - Activate specialized team members (37+ roles: pm, lead, backend, frontend, devops, qa, security, performance, data, ml, mobile, dba, ux, platform, docs, accessibility, release, compliance, ba, solutions, observability, api, cost, designer, researcher, analyst, product-analyst, integration, architect, fullstack, growth, sre, technical-writer, enterprise-architect, program-manager, customer-success-engineer, solutions-engineer, growth-engineer, product-designer)
  - **Special Note**: `/sc:team` is a framework-level meta-command that loads agent contexts from `~/.claude/agents/[role].md` rather than being a standalone command file

**Wave Orchestration** (1 command):
- `/sc:spawn` - Meta-system task orchestration with intelligent breakdown

**Research** (1 command):
- `/sc:research` - Deep web research with adaptive strategies

**Note**: Check `/Users/arlenagreer/.claude/commands/sc/` directory for the complete and current list of available commands. The `/sc:team` command is implemented through the agent system in `/Users/arlenagreer/.claude/agents/` rather than as a standalone command file.

### If Required Command Doesn't Exist
If the ideal command doesn't exist:
1. **First**: Check `/Users/arlenagreer/.claude/commands/sc/` to verify it truly doesn't exist
2. **Option A**: Note that the command should be created (preferred for recurring needs)
3. **Option B**: Use the closest existing command (e.g., `/sc:analyze` for analysis tasks)
4. **Always**: Explain which command was chosen and why

## How to Use This Skill

Simply describe what you need to accomplish, and this skill will:

1. **Analyze Your Need**: Understand complexity, domain, operation type, and scope
2. **Select SuperClaude Command**: Choose the appropriate `/sc:` command (MANDATORY FIRST STEP)
3. **Design the Prompt**: Add optimal flags, personas, and MCP servers
4. **Identify Parallelization**: Apply parallel-first optimization (CRITICAL for efficiency)
5. **Explain the Thinking**: Document why each choice was made and how it ensures the best result
6. **Output the Prompt**: Provide the complete, ready-to-use SuperClaude prompt starting with the command

## 🔴 CRITICAL: Continuous Execution Principle

**Unless explicitly instructed otherwise, all generated prompts MUST emphasize continuous, uninterrupted execution.**

### Default Behavior
- **Complete the entire task** from start to finish without stopping
- **Do not pause** to summarize progress after each major step
- **Do not ask permission** to proceed to the next phase
- **Execute all planned steps** in the workflow without interruption

### When to Include Pauses
Only suggest stopping points when:
- User explicitly requests checkpoints ("pause after analysis", "wait for approval")
- Safety-critical operations requiring manual validation
- User input is genuinely needed to proceed (missing requirements, unclear specifications)
- Resource constraints require staged execution

### Prompt Language Patterns

**Good (Continuous)**:
- "Complete the entire implementation from start to finish"
- "Execute all steps in this workflow without stopping"
- "Proceed through all phases: analysis → design → implementation → testing"
- "Work through the complete task until done"

**Bad (Unnecessary Pauses)**:
- "After completing phase 1, summarize and ask if you should continue"
- "Complete the analysis, then wait for confirmation before proceeding"
- "Stop after each component to check if the approach is correct"
- "Pause between steps to get user approval"

### Integration with Generated Prompts

Every generated prompt should include explicit continuous execution language unless the user specifically requests otherwise.

## Prompt Engineering Workflow

### Step 1: Understand the Request

Analyze the user's request to identify:
- **Primary Domain**: Frontend, backend, security, performance, architecture, etc.
- **Operation Type**: Analysis, creation, implementation, modification, debugging, iterative
- **Complexity Level**: Simple (1-2 files, basic task), Moderate (3-10 files, analysis), Complex (system-wide, >10 steps)
- **Scope**: File, module, project, or system level
- **Special Requirements**: Security, performance, quality focus, testing needs
- **Parallelization Opportunities**: Independent operations, multi-file work, analysis scope

### Step 2: Select SuperClaude Command (MANDATORY FIRST)

**🔴 CRITICAL: Every prompt MUST start with a `/sc:` command.**

Based on the analysis, select the most appropriate command:

**Commands** (from `/sc:` commands):
- Development: `/sc:build`, `/sc:implement`, `/sc:design`
- Analysis: `/sc:analyze`, `/sc:troubleshoot`, `/sc:explain`, `/sc:business-panel`
- Quality: `/sc:improve`, `/sc:cleanup`
- Planning: `/sc:workflow`, `/sc:estimate`, `/sc:task`, `/sc:brainstorm`
- Orchestration: `/sc:pm` (PM Agent), `/sc:agent`, `/sc:recommend`, `/sc:index-repo`
- Testing: `/sc:test`
- Documentation: `/sc:document`
- Research: `/sc:research`
- Meta: `/sc:git`, `/sc:load`, `/sc:index`, `/sc:spawn`

**To find all available commands:**
Check `/Users/arlenagreer/.claude/commands/sc/` directory for the complete current list.

**If the ideal command doesn't exist:**
- First verify by checking the commands directory
- Note that it should be created (preferred for recurring needs)
- Use the closest existing command as a fallback
- Explain the gap and workaround in the analysis section

### Step 2.3: Key Command Details

#### `/sc:help` - Command Discovery
**Purpose**: Primary discovery mechanism for finding available SuperClaude commands

**Usage**:
```bash
/sc:help [query]
```

**Key Features**:
- Lists all available `/sc:` commands with descriptions
- Searchable by keyword or category
- Shows command syntax and common usage patterns
- Provides quick reference for flag combinations
- Auto-updates when new commands are added

**When to Use**:
- User unsure which command exists for their need
- Exploring available SuperClaude capabilities
- Quick reference lookup for command syntax
- Verifying command availability before crafting prompts

**Integration**:
- Works with Context7 for command documentation
- Provides examples from COMMANDS.md reference
- Links to detailed command specifications

#### `/sc:save` - Session Persistence
**Purpose**: Save session context and project state using Serena MCP for cross-session continuity

**Usage**:
```bash
/sc:save [--type session|learnings|context|all] [--summarize] [--checkpoint]
```

**Key Features**:
- **Idempotency Contract**: Append-only model with ISO 8601 timestamps
- **Versioning**: Each save creates new timestamped entry (session_YYYY-MM-DD_HHMMSS)
- **Data Safety**: No overwrites - all saves preserved in memory history
- **Automatic Triggers**: 30-minute intervals, task completion, risky operations
- **Rollback Capability**: Previous versions accessible via Serena memory operations

**Idempotency Behavior**:
- **First Call**: Creates timestamped memory entry
- **Repeated Calls**: Creates NEW timestamped version (append-only)
- **Conflict Resolution**: Last-write-wins within same minute
- **Data Integrity**: Validation ensures memory write success before confirmation

**When to Use**:
- End of coding session to preserve context
- Before risky operations (create restore point)
- After completing major milestones
- When switching between projects
- Automatic checkpoints (every 30 minutes)

**Integration**:
- **Serena MCP**: Memory management and persistence
- **Compensation Logic**: Atomic writes with rollback on failure
- **Session Lifecycle**: Works with `/sc:load` for complete session management

#### `/sc:reflect` - Quality Validation
**Purpose**: Task reflection and validation using Serena MCP analysis capabilities

**Usage**:
```bash
/sc:reflect [--aspect task-adherence|collected-information|completion]
```

**Key Features**:
- **Task Adherence**: Validates approach against original goals
- **Information Completeness**: Analyzes session completeness and gaps
- **Completion Criteria**: Evaluates whether task is truly done
- **Evidence-Based**: All assessments supported by session data

**Reflection Tools** (Serena MCP):
- `think_about_task_adherence`: Validates approach against goals
- `think_about_collected_information`: Analyzes session completeness
- `think_about_whether_you_are_done`: Evaluates completion criteria

**When to Use**:
- Before marking complex tasks as complete
- Mid-task validation of approach correctness
- After analysis phase to verify thoroughness
- When uncertain if requirements are fully met
- Quality gate checkpoints in workflows

**Integration**:
- **Serena MCP**: Semantic code understanding for context analysis
- **Sequential**: Structured reasoning for validation logic
- **Quality Gates**: Steps 2.5 & 7.5 in 10-step validation cycle

**Performance**: <200ms for core reflection operations

### Step 2.3.1: Session Lifecycle Workflow

**Purpose**: Understanding how `/sc:load`, `/sc:save`, and `/sc:reflect` work together as a unified session management system.

#### Complete Session Management Cycle

**Phase 1: Session Initialization**
- **Command**: `/sc:load [project-name]`
- **Purpose**: Restore project context, previous learnings, and active tasks from prior sessions
- **Serena MCP**: Loads session memory with project-specific context and discoveries
- **Triggers**:
  - New terminal session starting work on existing project
  - Project switch (moving from one codebase to another)
  - Context refresh needed (reconnecting to previous work state)
  - Returning after break (hours, days, or weeks later)
- **What Gets Loaded**:
  - Project structure understanding and architectural decisions
  - Previous discoveries and learnings about the codebase
  - Active task context and workflow state
  - Code patterns, conventions, and project-specific knowledge
  - Team decisions and documentation references

**Phase 2: Active Development**
- **Auto-Checkpoints**: Every 30 minutes via `/sc:save --checkpoint`
  - Automatic background saves preserve ongoing work
  - No user intervention required
  - Captures incremental progress and discoveries
- **Manual Saves**: Triggered strategically
  - Before risky operations (major refactors, schema changes, deployments)
  - After completing major milestones (feature complete, PR ready, tests passing)
  - Before context switches (switching branches, different project focus)
  - When significant decisions are made (architectural choices, pattern adoptions)
- **Memory Accumulation**: Continuous learning during work
  - Session discoveries (new code patterns identified, edge cases found)
  - Code patterns recognized (architectural patterns, anti-patterns, best practices)
  - Decisions documented (why certain approaches chosen, alternatives considered)
  - Problem-solving strategies (debugging techniques that worked, performance insights)

**Phase 3: Quality Validation**
- **Command**: `/sc:reflect --aspect task-adherence`
- **Purpose**: Validate work against original goals before marking tasks complete
- **Serena Analysis**: Semantic validation using project context
  - **Task Adherence**: Did the approach align with stated objectives?
  - **Information Completeness**: Was sufficient information gathered and considered?
  - **True Completion**: Is the task genuinely done, or are there remaining gaps?
- **Validation Timing**:
  - Before marking complex tasks as "completed"
  - Mid-task validation when approach seems off-track
  - After analysis phase to verify thoroughness
  - When uncertain if all requirements met
  - At quality gate checkpoints in multi-phase workflows
- **Reflection Aspects**:
  - `--aspect task-adherence`: Validate approach correctness
  - `--aspect collected-information`: Analyze session data completeness
  - `--aspect completion`: Evaluate true completion criteria

**Phase 4: Session Closure**
- **Command**: `/sc:save --type all --summarize`
- **Purpose**: Comprehensive session capture with learnings for future sessions
- **Versioning**: Timestamped entry `session_YYYY-MM-DD_HHMMSS`
  - ISO 8601 format ensures consistent chronological sorting
  - Each save creates new version (append-only, no overwrites)
  - Previous versions preserved in memory history
  - Rollback capability via Serena memory operations
- **Idempotency**: Append-only model ensures data safety
  - First call: Creates timestamped memory entry
  - Repeated calls: Creates NEW timestamped version (never overwrites)
  - Conflict resolution: Last-write-wins within same minute
  - Data integrity: Validation ensures write success before confirmation
- **What Gets Saved**:
  - Session summary and key accomplishments
  - New learnings and discoveries about the codebase
  - Decisions made and their rationale
  - Problems encountered and solutions found
  - Code patterns identified and adopted
  - Next session recommendations (what to focus on, what to avoid)

#### Workflow Diagram

```
┌──────────────────────────────────────────────────────────────────────────┐
│                        Session Lifecycle Flow                             │
└──────────────────────────────────────────────────────────────────────────┘

    ┌─────────────┐
    │   START     │
    │ New Session │
    └──────┬──────┘
           │
           ▼
    ┌─────────────────────────────────────────────┐
    │  Phase 1: LOAD                              │
    │  /sc:load [project]                         │
    │  • Restore context from Serena memory       │
    │  • Load previous learnings                  │
    │  • Resume active tasks                      │
    └──────────────┬──────────────────────────────┘
                   │
                   ▼
    ┌─────────────────────────────────────────────┐
    │  Phase 2: WORK                              │
    │  Active Development                         │
    │  • Code, analyze, implement                 │
    │  • Accumulate discoveries                   │
    │  • Auto-checkpoint every 30min              │
    │  • Manual saves at milestones               │
    └──────────────┬──────────────────────────────┘
                   │
                   ▼
    ┌─────────────────────────────────────────────┐
    │  Phase 3: REFLECT                           │
    │  /sc:reflect --aspect task-adherence        │
    │  • Validate approach correctness            │
    │  • Verify information completeness          │
    │  • Confirm true task completion             │
    └──────────────┬──────────────────────────────┘
                   │
                   ▼
    ┌─────────────────────────────────────────────┐
    │  Phase 4: SAVE                              │
    │  /sc:save --type all --summarize            │
    │  • Capture session summary                  │
    │  • Document learnings & decisions           │
    │  • Create timestamped version               │
    │  • Preserve for future sessions             │
    └──────────────┬──────────────────────────────┘
                   │
                   ▼
    ┌─────────────────────────────────────────────┐
    │   NEXT SESSION                              │
    │   Loop back to Phase 1 (LOAD)               │
    │   Context preserved, ready to continue      │
    └─────────────────────────────────────────────┘

Continuous Cycle: Load → Work → Reflect → Save → (Next Session Load)
                  ▲_______________________________________________|
```

#### Practical Usage Examples

**Example 1: Starting Work on Existing Project**
```bash
# Morning: Start new session
/sc:load bryan-mobile-app

# Work throughout the day...
# (Auto-checkpoints happen automatically every 30 min)

# Before lunch: Manual save
/sc:save --checkpoint --summarize

# Afternoon: Continue work...

# Before major refactor: Create restore point
/sc:save --type context --checkpoint

# End of day: Validate completion
/sc:reflect --aspect task-adherence

# End of day: Comprehensive save
/sc:save --type all --summarize
```

**Example 2: Multi-Day Feature Development**
```bash
# Day 1: Start feature
/sc:load my-project
# Implement authentication module...
/sc:save --type all --summarize

# Day 2: Continue feature (context preserved)
/sc:load my-project
# Work continues seamlessly with yesterday's context...
/sc:reflect --aspect collected-information
/sc:save --type all --summarize

# Day 3: Final validation
/sc:load my-project
# Complete testing and documentation...
/sc:reflect --aspect completion
/sc:save --type all --summarize
```

**Example 3: Context Switch Between Projects**
```bash
# Working on Project A
/sc:load project-a
# Make progress...
/sc:save --type session --checkpoint

# Emergency: Switch to Project B
/sc:load project-b
# Handle urgent issue...
/sc:save --type all --summarize

# Return to Project A (context restored)
/sc:load project-a
# Continue exactly where you left off...
```

#### Troubleshooting Common Issues

**Issue 1: Load Fails with "Project Not Found"**
- **Symptom**: `/sc:load project-name` returns error saying project doesn't exist
- **Root Cause**: Project has never been saved, or name mismatch
- **Solutions**:
  1. Verify project name spelling (case-sensitive)
  2. Check available projects: Use Serena MCP `list_memories` tool
  3. First-time project: Just start working, save will create new project memory
  4. Name standardization: Use consistent naming (e.g., `project-name` not `Project Name`)

**Issue 2: Save Conflicts or Duplicate Entries**
- **Symptom**: Multiple saves creating too many versions
- **Root Cause**: Frequent manual saves creating version bloat (idempotent behavior working as designed)
- **Solutions**:
  1. Rely on auto-checkpoints (every 30min) for routine saves
  2. Manual saves only for significant milestones
  3. This is actually expected behavior (append-only for safety)
  4. Periodic cleanup: Use Serena memory management to consolidate old versions

**Issue 3: Reflect Shows Incomplete Task When You Think It's Done**
- **Symptom**: `/sc:reflect --aspect completion` indicates task not truly complete
- **Root Cause**: Missing test coverage, incomplete documentation, or edge cases not handled
- **Solutions**:
  1. Review reflection feedback carefully - often catches real gaps
  2. Run additional analysis passes to verify completeness
  3. Check task scope - did original requirements include tests, docs, validation?
  4. Use `/sc:reflect --aspect collected-information` to identify missing data

**Issue 4: Serena MCP Connection Errors**
- **Symptom**: "Serena MCP unavailable" or timeout errors during load/save/reflect
- **Root Cause**: MCP server not running or network/permission issues
- **Solutions**:
  1. Check Serena MCP status: Verify server is running and accessible
  2. Restart MCP server: Sometimes resolves transient connection issues
  3. Check permissions: Ensure Claude Code has access to Serena
  4. Fallback: Document work manually, retry save when MCP restored
  5. Prevention: Use `--validate` flag to check MCP status before critical operations

**Issue 5: Memory Fragmentation After Long Project**
- **Symptom**: Load times increasing, memory size growing too large
- **Root Cause**: Accumulated sessions over weeks/months without cleanup
- **Solutions**:
  1. Periodic consolidation: Use `/sc:save --consolidate` to merge similar entries
  2. Archive old sessions: Move completed feature sessions to archive
  3. Clean delete: Remove obsolete sessions that are no longer relevant
  4. Memory hygiene: Monthly cleanup of stale project memories

**Issue 6: Context Loss Between Sessions**
- **Symptom**: After `/sc:load`, context doesn't feel complete or accurate
- **Root Cause**: Insufficient save detail or missing --summarize flag
- **Solutions**:
  1. Use `--type all --summarize` for comprehensive saves
  2. Add explicit summaries during save (describe key decisions made)
  3. Save more frequently at decision points
  4. Use `/sc:reflect` before save to capture session insights
  5. Document "why" not just "what" in your work

#### Best Practices for Session Lifecycle

**✅ DO**:
- Always `/sc:load` at start of work session to restore context
- Rely on 30-minute auto-checkpoints for routine progress saves
- Use `/sc:reflect` before marking complex tasks complete
- Save with `--type all --summarize` at end of significant work sessions
- Create restore points with `/sc:save --checkpoint` before risky operations
- Use consistent project naming across sessions
- Document decisions and learnings in session work

**❌ DON'T**:
- Skip loading at session start (loses valuable context)
- Over-save manually (defeats purpose of auto-checkpoints)
- Mark tasks complete without reflection validation
- Use different project names for same codebase
- Delete memories unless absolutely certain they're obsolete
- Rely solely on auto-saves for critical milestones (use manual save)

#### Integration with Other Commands

**Session Lifecycle + Workflow Commands**:
- `/sc:implement` → Use reflect to validate implementation completeness
- `/sc:analyze` → Save analysis insights for future reference
- `/sc:improve` → Reflect on improvements before/after for quality validation
- `/sc:build` → Save build configurations and decisions
- `/sc:task` → Load project context for long-term task continuity

**Session Lifecycle + Quality Gates**:
- Steps 2.5 & 7.5 in 10-step validation cycle use `/sc:reflect`
- Pre-execution validation with loaded context awareness
- Post-completion verification before session save

**Session Lifecycle + Team Coordination**:
- Team handoffs benefit from comprehensive session saves
- `/sc:team` agents can load shared project context
- Collaborative work maintains session continuity across team members

#### `/sc:spec-panel` - Expert Specification Review
**Purpose**: Multi-expert specification review using renowned specification and software engineering experts

**Usage**:
```bash
/sc:spec-panel [document] [--mode discussion|critique|socratic] [--experts <list>] [--focus <areas>]
```

**Key Features**:
- **Expert Panel**: 11 renowned experts (Wiegers, Fowler, Hohpe, Newman, Nygard, Crispin, Gregory, Cockburn, Adzic, Hightower, Vogels)
- **Three Analysis Modes**:
  - **Discussion**: Collaborative improvement through expert dialogue
  - **Critique**: Systematic review with priorities and severity ratings
  - **Socratic**: Learning-focused questioning for deeper understanding
- **Multi-Domain**: Requirements, architecture, testing, quality, cloud infrastructure
- **Quality Scoring**: 0-10 scale with improvement recommendations

**Analysis Modes**:
- **Discussion Mode**: Experts build on each other's insights collaboratively
- **Critique Mode**: Systematic review with CRITICAL/HIGH/MEDIUM/LOW severity ratings
- **Socratic Mode**: Expert-guided questioning for strategic learning

**When to Use**:
- Before implementing complex features (validation)
- After drafting PRDs or technical specifications
- When seeking expert-level architectural feedback
- For quality validation of critical system designs
- Learning best practices from multiple expert perspectives

**Integration**:
- **Sequential**: Multi-expert coordination and synthesis
- **Context7**: Specification patterns and best practices
- **Quality Gates**: Expert validation in Phase 2 of workflows

**Output**: Comprehensive critique with quality scores, prioritized issues, and improvement recommendations

#### `/sc:team` - Team Coordination
**Purpose**: Activate specialized software engineering team members for coordinated development

**Usage**:
```bash
/sc:team [member] [action]
/sc:team:pm [action]         # Direct role access
/sc:team:backend [action]    # Specialist activation
```

**Team Members** (37+ specialized roles):
- **Product & Planning**: pm (Product Manager), ba (Business Analyst), product-analyst
- **Technical Leadership**: lead (Tech Lead), architect, solutions, enterprise-architect
- **Engineering**: backend, frontend, fullstack, mobile, data, ml, integration
- **Infrastructure**: devops, platform, sre, observability, release, cost
- **Quality & Testing**: qa, performance, security, accessibility
- **Design & Research**: ux, designer, researcher, product-designer
- **Documentation**: docs, technical-writer
- **Database**: dba
- **Specialized**: api, compliance, program-manager, customer-success-engineer, solutions-engineer, growth, growth-engineer

**Key Features**:
- **Framework-Level Implementation**: Loads agent contexts from `~/.claude/agents/[role].md`
- **Auto-Handoff**: Automatic coordination triggers between team members
- **Workflow Integration**: TDD, specification-driven, handoff protocols
- **Quality Gates**: Team-specific validation checkpoints

**Handoff Triggers** (automatic):
- Requirements complete → Tech Lead activation
- Architecture approved → Engineering team activation
- Implementation complete → QA activation
- Testing complete → DevOps activation
- Security/Performance reviews → Throughout workflow

**When to Use**:
- Multi-phase development requiring multiple specialists
- When specific domain expertise needed (security, performance, compliance)
- Cross-functional coordination (PM → Lead → Engineers → QA → DevOps)
- Simulating real team workflows and handoffs

**Integration**:
- **Agent System**: Loads from `~/.claude/agents/` directory (47 agent files)
- **Coordination**: `team-config.md` defines handoff protocols
- **Personas**: Maps to 11 SuperClaude personas for domain expertise

**Special Note**: `/sc:team` is a framework-level meta-command rather than a standalone command file. It integrates with the agent persona loading system.

#### `/sc:select-tool` - Intelligent MCP Tool Selection
**Purpose**: Intelligent routing between Serena and Morphllm MCP servers based on operation complexity and requirements

**Usage**:
```bash
/sc:select-tool [operation] [--analyze] [--explain]
```

**Key Features**:
- **Complexity Scoring**: Multi-dimensional analysis of file count, operation type, and requirements
- **Intelligent Routing**: Automatic selection between Serena (semantic) and Morphllm (pattern-based) operations
- **Performance Optimization**: Sub-100ms decision time with >95% selection accuracy
- **Decision Transparency**: Explain mode shows scoring logic and selection rationale

**Decision Matrix** (see Step 2.4 for detailed server capabilities):

**Direct Mappings**:
- Symbol operations (rename, extract, move) → **Serena**
- Pattern edits (bulk replacements, style enforcement) → **Morphllm**
- Memory operations (save, load, persistence) → **Serena**
- Session lifecycle → **Serena**
- Framework updates → **Morphllm**

**Complexity Thresholds**:
- **Score >0.6** (High complexity) → Serena MCP
  - Multi-file symbol operations
  - Dependency tracking required
  - LSP integration needed
  - Semantic understanding critical

- **Score <0.4** (Low complexity) → Morphllm MCP
  - Simple text replacements
  - Pattern-based bulk edits
  - Speed-critical operations
  - Token optimization priority

- **Score 0.4-0.6** (Medium complexity) → Feature-based selection
  - Evaluate specific operation requirements
  - Consider performance vs accuracy trade-offs
  - Default to Serena for safety

**Scoring Factors**:
- File count: >10 files increases complexity
- Operation type: Semantic operations score higher
- Language/framework: Multi-language increases complexity
- Requirements: LSP, dependencies, context increase complexity

**When to Use**:
- Uncertain which MCP server is optimal for your operation
- Need to understand tool selection logic and reasoning
- Want to optimize between speed (Morphllm) and accuracy (Serena)
- Learning the decision patterns for future manual selection

**Integration**:
- **Automatic**: Used internally by `/sc:refactor`, `/sc:edit`, `/sc:implement`, `/sc:improve`
- **Manual**: Explicit routing decisions when user specifies tool preference
- **Cross-Reference**: See Step 2.4 for detailed Serena vs Morphllm guidance

**Example Routing Decisions**:
```
"rename getUserData function everywhere"
→ Analysis: High complexity (symbol operation, multi-file)
→ Selection: Serena MCP (LSP capabilities, dependency tracking)
→ Confidence: 95%

"update all console.log to logger.info"
→ Analysis: Low complexity (pattern-based, text replacement)
→ Selection: Morphllm MCP (pattern matching, speed optimized)
→ Confidence: 98%

"save project context and discoveries"
→ Direct mapping: Memory operations → Serena MCP
→ Rationale: Session persistence and project memory
→ Confidence: 100%
```

**Fallback Strategy**:
- **Tier 1**: Selected MCP server (Serena or Morphllm)
- **Tier 2**: Alternative MCP server if primary unavailable
- **Tier 3**: Native Claude Code tools as last resort

**Performance Metrics**:
- Decision time: <100ms
- Selection accuracy: >95% based on operation outcomes
- Confidence scoring: 0-100% based on clarity of operation type

**Special Note**: This is a meta-command for intelligent tool routing. Most users won't call it directly - it's automatically invoked by other commands. However, using `--analyze` or `--explain` flags can help understand tool selection decisions and improve your own manual MCP server choices.

#### `/sc:pm` - PM Agent (Project Management Orchestration) - NEW
**Purpose**: Always-active foundation layer for intelligent orchestration with PDCA cycles and Serena memory integration

**Usage**:
```bash
/sc:pm [task-description]
/sc:pm --cycle plan|do|check|act
/sc:pm --self-improve
```

**Key Features**:
- **Always-Active Foundation**: PM Agent is the orchestration layer that coordinates all other commands
- **PDCA Cycle Integration**: Plan-Do-Check-Act methodology for systematic task execution
- **Serena Memory Integration**: Cross-session learning with standardized memory key schema
- **Self-Improvement Workflows**: Continuous documentation of patterns, mistakes, and learnings
- **Sub-Agent Orchestration**: Auto-delegation to domain specialists without manual routing

**PDCA Cycle Methodology**:
```
PLAN Phase:
├── Write plan to memory: plan/[feature]/hypothesis
├── Document: architecture, rationale, risks
└── Validate: requirements completeness

DO Phase:
├── Execute with checkpoints: execution/[feature]/do
├── Log errors and solutions: execution/[feature]/errors
└── Progressive implementation with validation

CHECK Phase:
├── Evaluate results: evaluation/[feature]/check
├── Measure against success criteria: evaluation/[feature]/metrics
└── Document lessons: evaluation/[feature]/lessons

ACT Phase:
├── Standardize successful patterns
├── Update learning memories: learning/patterns/[name]
└── Feed improvements into next cycle
```

**Memory Key Schema** (Serena MCP):
```yaml
Session Context:
  session/context      - Current session state and discoveries
  session/last         - Previous session summary
  session/checkpoint   - Auto-save checkpoint data

Planning Artifacts:
  plan/[feature]/hypothesis    - Initial approach hypothesis
  plan/[feature]/architecture  - Architectural decisions
  plan/[feature]/rationale     - Decision justifications

Execution Tracking:
  execution/[feature]/do       - Implementation progress
  execution/[feature]/errors   - Encountered errors
  execution/[feature]/solutions - Applied solutions

Evaluation Results:
  evaluation/[feature]/check   - Validation results
  evaluation/[feature]/metrics - Success measurements
  evaluation/[feature]/lessons - Learnings captured

Cross-Session Learning:
  learning/patterns/[name]     - Reusable patterns discovered
  learning/solutions/[error]   - Error → Solution mappings
  learning/mistakes/[timestamp] - Mistakes to avoid

Project Context:
  project/context      - Overall project understanding
  project/architecture - System architecture
  project/conventions  - Code patterns and standards
```

**Self-Correction Workflow**:
1. **Root Cause Analysis**: When errors occur, PM Agent analyzes underlying causes
2. **Solution Documentation**: Successful fixes are logged to `learning/solutions/[error]`
3. **Pattern Recognition**: Recurring patterns are promoted to `learning/patterns/[name]`
4. **Mistake Avoidance**: Failures are documented in `learning/mistakes/[timestamp]`
5. **Next Session Benefits**: Learnings are loaded and applied in future sessions

**Sub-Agent Orchestration**:
- PM Agent automatically delegates to domain specialists based on task context
- No manual routing required - intelligent task analysis determines appropriate agents
- Handoff protocols ensure context preservation between agents
- Quality gates validate outputs before proceeding

**When to Use**:
- Starting new features that require systematic planning
- Complex tasks benefiting from PDCA methodology
- When you want cross-session learning and context preservation
- Long-running projects requiring orchestration across multiple sessions
- Tasks that benefit from self-improvement and pattern capture

**Integration**:
- **Serena MCP**: Primary integration for memory and persistence
- **Sequential**: Complex reasoning during PLAN and CHECK phases
- **All Commands**: PM Agent can orchestrate any other `/sc:` command
- **Session Lifecycle**: Works with `/sc:load`, `/sc:save`, `/sc:reflect`

**Example Workflows**:
```bash
# Start a new feature with PDCA methodology
/sc:pm "Implement user authentication with JWT tokens"

# Explicitly work through PDCA phases
/sc:pm --cycle plan "authentication feature planning"
/sc:pm --cycle do "implement JWT authentication"
/sc:pm --cycle check "validate authentication implementation"
/sc:pm --cycle act "standardize authentication patterns"

# Enable self-improvement documentation
/sc:pm --self-improve "capture learnings from this session"
```

**Best Practices**:
- ✅ Use PM Agent for complex, multi-step features
- ✅ Let PDCA cycle guide systematic execution
- ✅ Document decisions in memory for future reference
- ✅ Review learning memories to avoid repeated mistakes
- ❌ Don't use for simple, one-off tasks (use specific commands instead)
- ❌ Don't skip CHECK phase - validation is critical

#### `/sc:agent` - SC Agent Session Controller - NEW
**Purpose**: Session controller that orchestrates investigation, implementation, and review workflows

**Usage**:
```bash
/sc:agent [task-description]
```

**Key Features**:
- **Startup Checklist**: Auto-runs `git status` and reports core service availability
- **Confidence-Based Execution**: Pre-implementation confidence score ≥0.90 required
- **Helper Integration**: Auto-activates `@confidence-check`, `@deep-research`, `@repo-index`, `@self-review`
- **Token Discipline**: Short status messages, efficient communication

**Task Protocol**:
1. **Clarify Scope**: Confirm success criteria, blockers, constraints
2. **Plan Investigation**: Use parallel tool calls, reach for helper agents
3. **Iterate Until Confident**: Track confidence, don't implement below 0.90
4. **Implementation Wave**: Grouped edits, single checkpoint summary
5. **Self-Review**: Invoke `@self-review` to double-check outcomes

**When to Use**:
- Starting work sessions that need systematic orchestration
- Complex tasks requiring confidence validation before implementation
- When you want automatic helper agent coordination

#### `/sc:recommend` - Command Recommendation Engine - NEW
**Purpose**: Intelligent command recommendation based on user input analysis

**Usage**:
```bash
/sc:recommend [user-query]
```

**Key Features**:
- **Multi-Language Support**: Recognizes intent across languages
- **Confidence Scoring**: Ranks recommendations by relevance
- **Context-Aware**: Considers current project state and history
- **Learning Integration**: Improves recommendations based on usage patterns

**When to Use**:
- Uncertain which `/sc:` command is best for your need
- Learning the SuperClaude command ecosystem
- Quick command discovery without reading full documentation

#### `/sc:index-repo` - Repository Indexing - NEW
**Purpose**: Generate comprehensive project index for 94% token reduction

**Usage**:
```bash
/sc:index-repo
/sc:index-repo mode=update
/sc:index-repo mode=quick
```

**Key Features**:
- **Massive Token Savings**: 58K tokens → 3K tokens (94% reduction)
- **Parallel Analysis**: 5 concurrent Glob searches for structure analysis
- **Metadata Extraction**: Entry points, key modules, API surface, dependencies
- **Two Output Files**: `PROJECT_INDEX.md` (3KB human-readable) + `PROJECT_INDEX.json` (10KB machine-readable)

**ROI Calculation**:
- Index creation: 2,000 tokens (one-time)
- Index reading: 3,000 tokens (every session)
- Full codebase read: 58,000 tokens (every session)
- **Break-even**: 1 session
- **10 sessions savings**: 550,000 tokens

**When to Use**:
- Starting work on a new codebase
- After major structural changes
- When token efficiency is critical
- For quick project orientation

### Step 2.4: MCP Server Details

SuperClaude integrates with powerful MCP (Model Context Protocol) servers that extend Claude's capabilities. Understanding when to use each server is critical for optimal prompt crafting.

#### Serena MCP Server
**Purpose**: Semantic code understanding with project memory and session persistence

**Capabilities**:
- Symbol operations (rename, extract, move functions/classes)
- Project-wide code navigation and exploration
- Multi-language projects with LSP integration
- Session lifecycle management (`/sc:load`, `/sc:save`, project activation)
- Memory-driven development workflows
- Large codebase analysis (>50 files, complex architecture)

**Choose Serena When**:
- **Over Morphllm**: For symbol operations, not pattern-based edits
- **For semantic understanding**: Symbol references, dependency tracking, LSP integration
- **For session persistence**: Project context, memory management, cross-session learning
- **For large projects**: Multi-language codebases requiring architectural understanding
- **Not for simple edits**: Basic text replacements, style enforcement, bulk operations

**Works Best With**:
- **Morphllm**: Serena analyzes semantic context → Morphllm executes precise edits
- **Sequential**: Serena provides project context → Sequential performs architectural analysis

**Command Integration**:
- `/sc:load` - Requires Serena for project context loading
- `/sc:save` - Requires Serena for memory persistence
- `/sc:reflect` - Uses Serena for semantic code understanding
- `/sc:select-tool` - Routes between Serena and Morphllm intelligently

**Example Use Cases**:
```
"rename getUserData function everywhere" → Serena (symbol operation with dependency tracking)
"find all references to this class" → Serena (semantic search and navigation)
"load my project context" → Serena (/sc:load with project activation)
"save my current work session" → Serena (/sc:save with memory persistence)
```

**When NOT to Use Serena**:
```
"update all console.log to logger" → Use Morphllm (pattern-based replacement)
"create a login form" → Use Magic (UI component generation)
"enforce ESLint rules" → Use Morphllm (style guide application)
```

**Activation Flags**: `--serena` (explicit), auto-activated by session lifecycle commands

#### Morphllm MCP Server
**Purpose**: Pattern-based code editing engine with token optimization for bulk transformations

**Capabilities**:
- Multi-file edit operations with consistent patterns
- Framework updates, style guide enforcement, code cleanup
- Bulk text replacements across multiple files
- Natural language edit instructions with specific scope
- Token optimization with 30-50% efficiency gains

**Choose Morphllm When**:
- **Over Serena**: For pattern-based edits, not symbol operations
- **For bulk operations**: Style enforcement, framework updates, text replacements
- **When token efficiency matters**: Fast Apply scenarios with compression needs
- **For simple to moderate complexity**: <10 files, straightforward transformations
- **Not for semantic operations**: Symbol renames, dependency tracking, LSP integration

**Works Best With**:
- **Serena**: Serena analyzes semantic context → Morphllm executes precise edits
- **Sequential**: Sequential plans edit strategy → Morphllm applies systematic changes

**Command Integration**:
- `/sc:cleanup` - Ideal for bulk cleanup operations
- `/sc:improve` - Pattern-based code improvements
- `/sc:select-tool` - Routes between Serena and Morphllm intelligently

**Example Use Cases**:
```
"update all React class components to hooks" → Morphllm (pattern transformation)
"enforce ESLint rules across project" → Morphllm (style guide application)
"replace all console.log with logger calls" → Morphllm (bulk text replacement)
"update import paths after refactoring" → Morphllm (bulk pattern replacement)
```

**When NOT to Use Morphllm**:
```
"rename getUserData function everywhere" → Use Serena (symbol operation)
"analyze code architecture" → Use Sequential (complex analysis)
"explain this algorithm" → Native Claude (simple explanation)
```

**Activation Flags**: `--morph` or `--morphllm` (explicit), auto-activated by bulk edit patterns

#### Serena vs Morphllm Decision Matrix

| Operation Type | Use Serena | Use Morphllm |
|----------------|------------|--------------|
| Symbol rename | ✅ Yes | ❌ No |
| Bulk text replacement | ❌ No | ✅ Yes |
| Find references | ✅ Yes | ❌ No |
| Style enforcement | ❌ No | ✅ Yes |
| Session persistence | ✅ Yes | ❌ No |
| Framework updates | ❌ No | ✅ Yes |
| Dependency tracking | ✅ Yes | ❌ No |
| Pattern-based edits | ❌ No | ✅ Yes |
| LSP integration | ✅ Yes | ❌ No |
| Token optimization | Moderate | High (30-50%) |

**Key Decision Factors**:
1. **Semantic vs Pattern**: Symbol operations → Serena, text patterns → Morphllm
2. **Scope**: Single refactoring → Serena, bulk operations → Morphllm
3. **Integration**: Session lifecycle → Serena, code cleanup → Morphllm
4. **Efficiency**: Complex analysis → Serena, simple bulk edits → Morphllm

**Combined Workflow Example**:
```
Task: "Refactor authentication module and update all usage sites"
1. Serena: Analyze authentication module structure and find all references
2. Sequential: Plan refactoring strategy based on dependencies
3. Morphllm: Apply consistent patterns across all usage sites
4. Serena: Verify symbol references after refactoring
```

### Step 2.5: Add Complementary Facilities

After selecting the command, add complementary facilities:

**Flags** (behavioral modifiers):
- Mode Activation: `--brainstorm`, `--introspect`, `--task-manage`, `--orchestrate`, `--token-efficient`
- MCP Servers: `--c7`/`--context7`, `--seq`/`--sequential`, `--magic`, `--play`/`--playwright`, `--morph`/`--morphllm`, `--serena`
- Analysis Depth: `--think`, `--think-hard`, `--ultrathink`
- Execution Control: `--delegate`, `--concurrency`, `--loop`, `--validate`, `--safe-mode`
- Output Optimization: `--scope`, `--focus`, `--uc`

**Personas** (domain experts):
- Technical: `--persona-architect`, `--persona-frontend`, `--persona-backend`, `--persona-security`, `--persona-performance`
- Process: `--persona-analyzer`, `--persona-qa`, `--persona-refactorer`, `--persona-devops`
- Knowledge: `--persona-mentor`, `--persona-scribe`

**MCP Server Integration** (see Step 2.4 for detailed server selection guidance):
- **Context7**: Library docs, framework patterns, best practices
- **Sequential**: Complex analysis, multi-step reasoning, systematic debugging
- **Magic**: UI component generation, design systems
- **Playwright**: Browser testing, E2E scenarios, performance metrics
- **Serena**: Semantic code understanding, symbol operations, session persistence (see Step 2.4)
- **Morphllm**: Pattern-based bulk edits, style enforcement, token optimization (see Step 2.4)

**Wave Orchestration** (for complex operations):
- Wave-enabled commands: `/sc:analyze`, `/sc:build`, `/sc:implement`, `/sc:improve`, `/sc:design`, `/sc:task`, `/sc:workflow`
- Wave strategies: `--wave-strategy progressive`, `systematic`, `adaptive`, `enterprise`
- Auto-activation: complexity ≥0.7 + files >20 + operation_types >2

### Step 2.5: Apply Parallel-First Philosophy

**🔴 CRITICAL PRINCIPLE FROM RULES.MD: "PARALLEL EVERYTHING"**

SuperClaude's Tool Optimization rule mandates:
- **Default Behavior**: Execute independent operations in parallel, NEVER sequentially
- **Planning Integration**: Identify parallelization during planning phase (Plan → TodoWrite → **Analyze Parallel Ops** → Execute)
- **Single Message Pattern**: Use one message with multiple tool calls for independent operations
- **Efficiency First**: Choose speed and power over familiarity - use the fastest method available

#### Parallelization Analysis Checklist

**Ask these questions for EVERY prompt:**

1. **File Operations**:
   - [ ] Can these file reads happen simultaneously? → Batch Read calls in single message
   - [ ] Are file edits independent? → Use MultiEdit for 3+ files
   - [ ] Multiple file searches needed? → Parallel Grep/Glob calls

2. **Analysis Scope**:
   - [ ] Analyzing multiple directories? → `--delegate --parallel-dirs`
   - [ ] Multiple focus areas (security + performance + quality)? → `--multi-agent --parallel-focus`
   - [ ] >50 files to examine? → Task agent delegation with parallel sub-agents

3. **Multi-Domain Operations**:
   - [ ] Frontend + Backend + DevOps work? → Parallel Task agents for each domain
   - [ ] Independent testing across components? → `--delegate --sub-agents [count]`

4. **Wave Operations**:
   - [ ] Multiple phases (review → plan → implement)? → Wave mode with parallel execution within phases
   - [ ] Large-scale refactoring? → `--wave-mode --systematic-waves` with parallel file processing

5. **Dependencies**:
   - [ ] Are operations truly independent, or do some depend on others?
   - [ ] If dependencies exist, can we parallelize within dependency groups?

#### Multi-Tool Call Pattern

**How Claude Code Executes Parallel Operations**:

Claude Code can call multiple tools in a **single message**. This is the key to parallelization:

```
Good (Parallel):
Message 1: [Read file1, Read file2, Read file3, Grep pattern1, Grep pattern2]
→ All execute simultaneously, results arrive together

Bad (Sequential):
Message 1: [Read file1]
Message 2: [Read file2]
Message 3: [Read file3]
→ Each waits for previous to complete (3x slower)
```

**When crafting prompts, explicitly suggest parallel execution where applicable:**
- "Read all configuration files in parallel"
- "Search for patterns across codebase simultaneously"
- "Analyze frontend, backend, and infrastructure in parallel"

#### When NOT to Parallelize

**Sequential execution is appropriate when:**

1. **Security-Critical Operations**: Authentication, encryption, compliance validation (reduce attack surface)
2. **Sequential Dependencies**: Operation B requires results from Operation A
3. **Resource Constraints**: System already at 85%+ resource usage
4. **Data Consistency**: Operations that must maintain strict ordering for correctness
5. **Debugging**: When you need to observe step-by-step execution for troubleshooting

**Important**: In prompts, explicitly note when sequential execution is chosen and why.

### Step 2.5.1: Parallelization Dependency Management

**Purpose**: Understanding when operations can be truly parallel vs when sequential ordering is required

Effective parallelization requires understanding dependency relationships between operations. This section provides patterns for identifying true independence, recognizing dependencies, and making informed execution ordering decisions.

#### Dependency Resolution Patterns

**Independent Operations** (can be parallelized):
- **File reads from different files**: Each read operation accesses distinct files with no shared state
  - Example: Reading `config.json`, `package.json`, `README.md` simultaneously
  - Benefit: 3x speedup for 3 files
- **Pattern searches across independent directories**: Separate directory trees with no interdependencies
  - Example: Searching `src/`, `tests/`, `docs/` in parallel
  - Benefit: Near-linear scalability with directory count
- **Analysis of separate domains**: Frontend, backend, security, performance operate on different concerns
  - Example: UI analysis + API analysis + security scan running simultaneously
  - Benefit: Domain expertise applied concurrently
- **Testing independent components**: Test suites with no shared fixtures or state
  - Example: Component A tests + Component B tests in parallel
  - Benefit: Test execution time reduced proportionally
- **Documentation generation for separate modules**: Independent documentation contexts
  - Example: API docs + User guide + Developer guide generated concurrently
  - Benefit: Documentation pipeline parallelization

**Sequential Dependencies** (must be ordered):
- **Read → Analyze → Edit same file**: Each step requires previous step's output
  - Example: Read config → Parse values → Update config → Validate changes
  - Reasoning: Analysis needs file content, edit needs analysis results, validation needs new content
- **Create directory → Create files within directory**: Child creation depends on parent existence
  - Example: `mkdir components/auth` → `touch components/auth/login.tsx`
  - Reasoning: File system hierarchy requires parent before children
- **Build dependencies → Run dependent code**: Runtime execution needs compiled artifacts
  - Example: Compile TypeScript → Bundle JavaScript → Run application
  - Reasoning: Each stage produces inputs for next stage
- **Schema migration → Data migration**: Data transformation depends on schema structure
  - Example: Add column to table → Populate column with calculated values
  - Reasoning: Data migration logic requires new schema to exist
- **Authentication → Authorized operations**: Security operations must validate before proceeding
  - Example: Login → Fetch protected resource
  - Reasoning: Authorization check must complete before accessing protected resources

**Partial Dependencies** (can be partially parallelized):
- **Group A files independent from Group B files**: Parallelize groups, sequence within if needed
  - Example: Frontend files (parallel) + Backend files (parallel), then integration
  - Pattern: `[Frontend1 || Frontend2 || Frontend3] && [Backend1 || Backend2] → Integration`
  - Benefit: Parallelism within domains, coordination across domains
- **Multiple analysis passes**: Parallelize within pass, sequence passes if each builds on previous
  - Example: Pass 1 (syntax + style + imports in parallel) → Pass 2 (semantic analysis using Pass 1 results)
  - Pattern: `Wave 1: [Analysis A || Analysis B || Analysis C] → Wave 2: [Synthesis using Wave 1]`
  - Benefit: Maximum parallelism within each analysis wave
- **Test suites with setup/teardown**: Parallelize tests, sequence lifecycle hooks
  - Example: `Setup (sequential) → [Test1 || Test2 || Test3] → Teardown (sequential)`
  - Pattern: `Before → [Parallel Tests] → After`
  - Benefit: Test execution parallelized while maintaining fixture integrity

#### Parallel Execution Boundaries

**Wave Boundaries**:
- **Operations within a wave can be parallel**: All operations at same wave level execute concurrently
- **Waves themselves are sequential**: Wave N+1 begins only after Wave N completes
- **Example**: Analysis wave (all parallel) → Planning wave (all parallel) → Implementation wave
  ```
  Wave 1 (Parallel): [Security Analysis || Performance Analysis || Quality Analysis]
       ↓ (Sequential boundary - all Wave 1 must complete)
  Wave 2 (Parallel): [Architecture Planning || Test Planning || Deployment Planning]
       ↓ (Sequential boundary - all Wave 2 must complete)
  Wave 3 (Parallel): [Frontend Implementation || Backend Implementation || Infrastructure Setup]
  ```
- **Benefit**: Structured parallelism with clear synchronization points

**Domain Boundaries**:
- **Frontend operations parallel to backend operations**: Separate technology stacks and concerns
  - Example: React component development || Node.js API development
  - Independence: Frontend uses mocked APIs, backend uses test data
- **Security analysis parallel to performance analysis**: Different evaluation criteria
  - Example: Vulnerability scanning || Performance profiling
  - Independence: Security focuses on threats, performance on bottlenecks
- **Testing parallel to documentation generation**: Different artifacts and processes
  - Example: E2E test execution || API documentation generation
  - Independence: Testing validates behavior, docs describe interfaces

**File System Boundaries**:
- **Independent directories can be processed in parallel**: No cross-directory dependencies
  - Example: Analyzing `src/components/` || `src/utils/` || `src/services/`
  - Assumption: Directories represent logical module boundaries
- **Files within same directory can be read in parallel**: Read-only operations are concurrent-safe
  - Example: Reading all `.tsx` files in `components/` simultaneously
  - Safety: File system handles concurrent reads
- **Edits to same file must be sequential**: Write operations require serialization
  - Example: Edit 1 → Edit 2 → Edit 3 (all modifying `config.ts`)
  - Reasoning: Prevents race conditions and merge conflicts

#### Sequential Override Criteria

**When to Force Sequential** (override parallel default):

1. **Security Operations**: Authentication, encryption, authorization flows
   - **Reasoning**: Attack surface reduction requires sequential validation gates
   - **Example**: Login → Validate credentials → Establish session → Authorize request
   - **Trade-off**: Security integrity > execution speed
   - **Flag**: Use `--sequential` with explicit security justification

2. **Data Integrity**: Database transactions, file system mutations, state updates
   - **Reasoning**: ACID properties and consistency require atomic sequential operations
   - **Example**: Begin transaction → Read balance → Deduct amount → Update balance → Commit transaction
   - **Trade-off**: Correctness > parallelism
   - **Flag**: Document transactional requirements

3. **Resource Constraints**: System at >85% resource usage, memory limits approaching
   - **Reasoning**: Parallel operations could cause resource exhaustion and failures
   - **Example**: Already at 90% memory → Sequential processing to stay within limits
   - **Trade-off**: Stability > speed optimization
   - **Flag**: Use `--safe-mode` with resource justification

4. **Debugging**: Step-by-step execution needed for troubleshooting
   - **Reasoning**: Understanding failure requires observing execution order
   - **Example**: Sequential execution to identify which step in chain causes error
   - **Trade-off**: Debuggability > efficiency
   - **Flag**: Temporary for investigation, remove after debugging

5. **Explicit Dependencies**: Operation B requires Operation A results as input
   - **Reasoning**: Cannot execute B without A's output data
   - **Example**: API call returns ID → Use ID to fetch related resource
   - **Trade-off**: Logical dependency (no choice)
   - **Documentation**: Show dependency chain clearly: A → B → C

**How to Specify Sequential**:
- **Flag Usage**: Add `--sequential` flag to override parallel default
- **Document Reason**: Always explain: "Sequential required for [security|dependencies|resources]"
- **Specify Dependency Chain**: Make execution order explicit: "A → B → C (results flow sequentially)"
- **Justify Trade-off**: Explain what parallel benefit is being sacrificed and why

#### Execution Ordering Examples

**Example 1: Multi-File Analysis (Parallel)**
```
Task: Analyze 10 component files for performance issues
Dependency: None (files are independent React components with no shared state)
Execution: Parallel read of all 10 files → Parallel analysis of each component
Reasoning:
  - File reads are concurrent-safe (read-only operations)
  - Each component analysis is independent (no cross-component dependencies)
  - Performance metrics are per-component (no aggregation needed during analysis)
Efficiency: 10x speedup vs sequential (linear scaling with file count)
Tool Pattern: Single message with 10 Read calls + parallel analysis Task agents
```

**Example 2: File Edit Chain (Sequential)**
```
Task: Read config → Parse values → Update config → Validate
Dependency: Each step requires previous step's output
Execution: Sequential chain (Read → Parse → Update → Validate)
Reasoning:
  - Parse needs file content from Read
  - Update needs parsed values from Parse
  - Validate needs new file content from Update
  - True data dependencies prevent parallelization
Efficiency: Cannot parallelize (true dependencies exist)
Tool Pattern: Sequential Read → Edit → Validation with explicit ordering
Justification: Data flow dependencies require sequential execution
```

**Example 3: Mixed Dependencies (Partial Parallel)**
```
Task: Analyze frontend (5 files) and backend (5 files), then compare results
Dependency: Frontend files independent, backend files independent, comparison depends on both
Execution:
  Wave 1 (Parallel): [Frontend analysis (5 files) || Backend analysis (5 files)]
  Wave 2 (Sequential): Compare frontend vs backend results
Reasoning:
  - Within frontend: 5 files are independent → Parallel
  - Within backend: 5 files are independent → Parallel
  - Between domains: Frontend independent of backend → Parallel
  - Comparison: Requires both analyses complete → Sequential after Wave 1
Efficiency: 5x speedup (10 files in 2 parallel groups vs 10 sequential)
Tool Pattern: Single message with 10 parallel Read calls → 2 parallel domain Task agents → Sequential synthesis
Benefit: Maximum parallelism within waves, coordination across waves
```

**Example 4: Security-Critical Sequential (Override)**
```
Task: Implement authentication flow with security validation
Dependency: Security validation gates require sequential execution
Execution: Sequential (deliberately avoiding parallelization)
  Login → Validate credentials → Rate limit check → Establish session → Authorize
Reasoning:
  - Security operations must complete in strict order to reduce attack surface
  - Each gate validates before proceeding to next stage
  - Parallel execution would allow bypassing validation steps
Efficiency: 0% parallel benefit (security > speed trade-off)
Tool Pattern: Sequential operations with explicit `--sequential` flag
Justification: "Sequential required for security: validation gates must execute in order"
Trade-off: Sacrificing parallelization for security integrity
```

**Example 5: Resource-Constrained Sequential (Override)**
```
Task: Process 100 large video files with encoding
Dependency: None (files are independent)
Natural Execution: Parallel (all 100 files simultaneously for maximum speed)
Actual Execution: Sequential batches of 5 files at a time
Reasoning:
  - System has 32GB RAM, each encoding uses 8GB
  - Parallel execution of 100 would require 800GB RAM (not available)
  - Resource constraint forces sequential batching despite independence
Efficiency: 5x speedup vs pure sequential (batch of 5), but 20x slower than full parallel (if resources allowed)
Tool Pattern: `--concurrency 5` to limit parallel operations to resource availability
Justification: "Sequential batching required for resource constraints: 32GB RAM limit"
Trade-off: Sacrificing maximum parallelization for system stability
```

#### Decision Framework

**Step 1: Identify Operations**
- List all operations in the task
- Determine what each operation produces and consumes

**Step 2: Map Dependencies**
- Create dependency graph showing data flow between operations
- Identify operations with no incoming edges (can start immediately)
- Identify operations with incoming edges (must wait for dependencies)

**Step 3: Group by Waves**
- Wave 1: All operations with no dependencies (fully parallel)
- Wave 2: Operations depending only on Wave 1 (parallel within wave)
- Wave N: Operations depending on Wave N-1 (parallel within wave)

**Step 4: Check Constraints**
- Security constraints: Do any operations require sequential validation?
- Resource constraints: Can system handle full parallelism?
- Data integrity: Do any operations require transactional sequencing?

**Step 5: Document Decision**
- Specify parallel operations: "Operations A, B, C execute in parallel"
- Specify sequential boundaries: "Operation D waits for A, B, C completion"
- Justify sequential overrides: "Sequential required for [reason]"
- Estimate efficiency gain: "Expected X% speedup via parallelization"

#### Integration with SuperClaude Framework

**Automatic Parallelization**:
- **`--delegate --parallel-dirs`**: Auto-parallelizes directory processing
- **`--multi-agent --parallel-focus`**: Spawns parallel domain-specific agents
- **MultiEdit tool**: Parallelizes edits across multiple files automatically
- **Wave orchestration**: Structures operations into parallel waves with sequential boundaries

**Manual Parallelization Specification**:
- **Prompt language**: "Execute operations A, B, C in parallel"
- **Tool pattern**: Single message with multiple tool calls
- **Explicit documentation**: "Parallel execution: [operations] because [independence reason]"

**Sequential Override Specification**:
- **`--sequential` flag**: Forces sequential execution with justification
- **Explicit dependency chains**: Document as "A → B → C (sequential due to dependencies)"
- **Reasoning annotation**: Always explain why parallel was overridden

### Step 2.6: Workflow Compensation and Error Recovery

**Purpose**: Understanding how to handle failures, rollback operations, and recover from errors while maintaining system consistency and data integrity.

Effective workflow execution requires planning for failure scenarios. This section provides patterns for error recovery, rollback procedures, and compensation logic to ensure graceful degradation and recovery from failures.

#### Rollback Procedures

**Rollback Patterns for Common Operations**:

**File Operations**:
- **Create File Rollback**: Delete the created file
  - Example: Created `new-config.json` → Rollback deletes `new-config.json`
  - Implementation: Track created files, delete on rollback trigger
  - Safety: Verify file was created by this operation (timestamp/hash check)
- **Edit File Rollback**: Restore from backup or checkpoint
  - Example: Modified `config.json` → Rollback restores original content
  - Implementation: Create backup before edit, restore from backup on failure
  - Integration: Use `/sc:save --checkpoint` before risky edits
- **Delete File Rollback**: Restore from backup
  - Example: Deleted `old-config.json` → Rollback restores from backup
  - Implementation: Move to `.trash/` instead of permanent delete, restore from trash
  - Retention: Keep `.trash/` backups for session duration

**Database Operations**:
- **Transaction Rollback**: Use database transaction boundaries
  - Example: `BEGIN TRANSACTION → Updates → COMMIT` or `ROLLBACK`
  - Implementation: Wrap related database operations in explicit transactions
  - Safety: Ensure all-or-nothing execution for related changes
- **Schema Migration Rollback**: Execute down migration
  - Example: Add column migration → Rollback removes column
  - Implementation: Maintain paired up/down migrations for all schema changes
  - Testing: Test rollback path as rigorously as forward migration
- **Data Migration Rollback**: Compensating updates or restore from backup
  - Example: Data transformation applied → Rollback reverses transformation
  - Implementation: Log all data changes, apply inverse transformations
  - Validation: Verify data integrity after rollback

**Infrastructure Operations**:
- **Deployment Rollback**: Revert to previous deployment version
  - Example: Deploy v2.0 fails → Rollback to v1.9
  - Implementation: Keep previous version artifacts, automated rollback triggers
  - Safety: Health checks determine rollback necessity
- **Configuration Rollback**: Restore previous configuration state
  - Example: Update load balancer config → Rollback to previous config
  - Implementation: Version all configurations, track deployment history
  - Automation: Automated rollback on validation failure

#### Error Recovery Patterns

**Retry with Exponential Backoff**:
- **Pattern**: Retry failed operations with increasing delays
- **Formula**: `delay = base_delay × (2 ^ retry_count) + random_jitter`
  - Example: 1s, 2s, 4s, 8s delays with ±20% jitter
- **Max Retries**: Typically 3-5 retries before giving up
- **Use Cases**:
  - Network operations (API calls, database connections)
  - Transient failures (temporary resource unavailability)
  - Rate-limited operations (respect rate limits while retrying)
- **Implementation**:
  ```
  for attempt in range(max_retries):
    try:
      result = operation()
      return result  # Success
    except TransientError:
      if attempt < max_retries - 1:
        delay = base_delay * (2 ** attempt) + random(0, jitter)
        sleep(delay)
        continue
      else:
        raise  # Max retries exceeded
  ```
- **When NOT to Use**: Data corruption errors, authentication failures, permanent errors

**Circuit Breaker Pattern**:
- **Purpose**: Prevent cascading failures by failing fast when downstream services are unhealthy
- **States**:
  - **CLOSED**: Normal operation, requests pass through
  - **OPEN**: Failure threshold exceeded, requests fail immediately without calling downstream
  - **HALF-OPEN**: Testing if downstream has recovered, limited requests allowed
- **Thresholds**:
  - Failure count or percentage (e.g., 5 consecutive failures or >50% error rate)
  - Time window (e.g., last 60 seconds)
  - Recovery timeout (e.g., wait 30 seconds before trying HALF-OPEN)
- **Use Cases**:
  - External API calls that may be unavailable
  - Database connections during outages
  - Resource-intensive operations that may overload system
- **Implementation**:
  ```
  Circuit Breaker State Machine:
  CLOSED → (failures exceed threshold) → OPEN
  OPEN → (recovery timeout elapsed) → HALF-OPEN
  HALF-OPEN → (test requests succeed) → CLOSED
  HALF-OPEN → (test requests fail) → OPEN
  ```
- **Benefits**: Prevent resource exhaustion, fail fast, automatic recovery testing

**Fallback Strategies**:
- **Cached Response**: Return stale cached data when primary source fails
  - Example: API call fails → Return last successful response from cache
  - Validity: Cache expiration policy (e.g., 5-minute TTL acceptable)
  - Indication: Mark response as "cached fallback" for user awareness
- **Default Value**: Use sensible default when data unavailable
  - Example: Configuration fetch fails → Use built-in default configuration
  - Safety: Ensure defaults are safe and tested
  - Documentation: Clearly document default behavior
- **Degraded Functionality**: Operate with reduced features
  - Example: Recommendation engine fails → Show popular items instead
  - UX: Gracefully degrade rather than complete failure
  - Notification: Inform user of degraded mode
- **Alternative Service**: Route to backup service when primary fails
  - Example: Primary payment processor down → Use secondary processor
  - Coordination: Ensure alternative service is compatible
  - Monitoring: Track which service handled request

#### Partial Completion Handling

**Resume from Checkpoint**:
- **Checkpoint Pattern**: Save progress at known-good states
  - Example: Multi-file refactoring → Checkpoint after each file
  - Implementation: `/sc:save --checkpoint` at milestone boundaries
  - Granularity: Balance checkpoint frequency vs overhead (every 5-10 operations)
- **Resume Logic**: Detect incomplete work and restart from checkpoint
  - Example: Operation interrupted at file 5/10 → Resume from file 6
  - State Detection: Check which operations completed successfully
  - Idempotency: Ensure resumed operations can safely re-execute
- **Progress Tracking**:
  ```
  Checkpoint Structure:
  - Operation ID: unique identifier for operation
  - Completed Steps: [step1, step2, step3]
  - Remaining Steps: [step4, step5, step6]
  - State Data: {file_index: 5, total_files: 10}
  - Timestamp: ISO 8601 timestamp
  ```
- **Integration with `/sc:save`**:
  - Automatic checkpoints every 30 minutes (session lifecycle)
  - Manual checkpoints before risky operations
  - Serena MCP memory persistence for checkpoint state

**Compensating Transactions**:
- **Pattern**: Execute compensating action to undo partial work
- **Example Scenarios**:
  - **Order Processing**: Order placed but payment failed → Cancel order (compensating transaction)
  - **User Registration**: User created but email send failed → Delete user account (compensation)
  - **Multi-Step Migration**: Step 2 fails → Execute inverse of Step 1 (compensation)
- **Compensation Logic**:
  ```
  Forward Transaction Chain:
  Step 1: Create User → Success
  Step 2: Send Welcome Email → FAILURE

  Compensation Chain (reverse order):
  Compensate Step 1: Delete User → Success (compensation)

  Final State: Clean rollback (user not created)
  ```
- **Implementation Requirements**:
  - Track all successful operations in forward chain
  - Design compensating operation for each forward operation
  - Execute compensations in reverse order (LIFO)
  - Ensure compensations are idempotent (can be retried safely)
- **Complex Example (Multi-Service Transaction)**:
  ```
  E-commerce Purchase Flow:
  1. Reserve Inventory → Success (compensation: Release Inventory)
  2. Charge Payment → Success (compensation: Refund Payment)
  3. Create Shipment → FAILURE

  Compensation Execution:
  - Compensate Step 2: Refund Payment → Success
  - Compensate Step 1: Release Inventory → Success
  - Final State: No charge, no inventory reserved, no shipment
  ```

#### Compensation Logic for Atomic Operations

**Atomic Operation Requirements**:
- **Definition**: Operation that must complete entirely or not at all (all-or-nothing)
- **Examples**: Database transactions, file system moves, multi-step deployments
- **Guarantees**: ACID properties (Atomicity, Consistency, Isolation, Durability)

**Atomicity Patterns**:

**Two-Phase Commit (2PC)**:
- **Phase 1 (Prepare)**: All participants prepare to commit and signal readiness
- **Phase 2 (Commit/Abort)**: Coordinator tells all participants to commit or abort
- **Use Case**: Distributed transactions across multiple databases or services
- **Failure Handling**:
  - Any participant fails Phase 1 → All participants abort
  - Coordinator fails after Phase 1 → Timeout triggers abort
  - Participant fails Phase 2 → Retry commit until success or manual intervention

**Saga Pattern (Long-Running Transactions)**:
- **Pattern**: Break long transaction into series of local transactions with compensations
- **Execution**: Each local transaction followed by compensation definition
- **Coordination**: Choreography (event-driven) or Orchestration (central coordinator)
- **Example**:
  ```
  Saga: Book Flight + Reserve Hotel + Rent Car

  Step 1: Book Flight
    - Success → Continue to Step 2
    - Failure → Saga fails (nothing to compensate)
    - Compensation: Cancel Flight Booking

  Step 2: Reserve Hotel
    - Success → Continue to Step 3
    - Failure → Compensate Step 1 (Cancel Flight)
    - Compensation: Cancel Hotel Reservation

  Step 3: Rent Car
    - Success → Saga completes
    - Failure → Compensate Step 2 (Cancel Hotel), then Step 1 (Cancel Flight)
    - Compensation: Cancel Car Rental
  ```
- **Advantages**: Works with long-running processes, handles distributed systems
- **Trade-offs**: Eventual consistency (not immediate), compensation must be designed carefully

**Idempotent Operations**:
- **Definition**: Operation that produces same result when executed multiple times
- **Importance**: Enables safe retries without side effects
- **Design Guidelines**:
  - Use unique operation IDs to detect duplicates
  - Check if operation already completed before executing
  - Design operations to be naturally idempotent (e.g., SET vs INCREMENT)
- **Examples**:
  - **Idempotent**: `SET user.status = "active"` (can execute multiple times safely)
  - **NOT Idempotent**: `INCREMENT user.login_count` (multiple executions cause issues)
  - **Made Idempotent**: `INCREMENT_ONCE(operation_id, user.login_count)` (check operation_id first)

#### Integration with `/sc:save` Checkpoint System

**Checkpoint Strategy for Workflows**:

**Pre-Operation Checkpoints**:
- **Before Risky Operations**: Create restore point before dangerous changes
  - Command: `/sc:save --type context --checkpoint`
  - Captures: Current file states, configuration, project context
  - Use Case: Before major refactors, schema changes, deployments
  - Rollback: Restore from checkpoint if operation fails

**Mid-Operation Checkpoints**:
- **During Long-Running Operations**: Periodic progress saves
  - Trigger: Every 30 minutes (automatic) or after major milestones
  - Captures: Completed steps, remaining work, intermediate state
  - Use Case: Multi-hour operations, batch processing, large refactors
  - Resume: Continue from last checkpoint if interrupted

**Post-Operation Checkpoints**:
- **After Successful Completion**: Capture successful end state
  - Command: `/sc:save --type all --summarize`
  - Captures: Final state, learnings, decisions, next steps
  - Use Case: Feature completion, milestone reached, phase done
  - Value: Known-good state for future rollback point

**Checkpoint Naming Convention**:
```
session_YYYY-MM-DD_HHMMSS_[type]
- session_2025-11-12_143000_pre-refactor
- session_2025-11-12_150000_mid-refactor-checkpoint
- session_2025-11-12_153000_post-refactor-success
```

**Rollback from Checkpoint**:
```
1. Identify checkpoint to restore: `/sc:load` lists available checkpoints
2. Load checkpoint state: Serena MCP memory operations
3. Analyze differences: Compare current state vs checkpoint state
4. Restore files: Revert changed files to checkpoint versions
5. Validate: Verify restored state is consistent
6. Document: Record why rollback was necessary
```

**Checkpoint Integration Examples**:

**Example 1: Risky Refactoring with Checkpoints**
```
Workflow:
1. Current state: Authentication module working
2. Create checkpoint: /sc:save --type context --checkpoint
   → Checkpoint: session_2025-11-12_140000_pre-auth-refactor
3. Execute refactor: Restructure authentication module
4. Tests fail: New structure breaks existing integrations
5. Rollback decision: Restore from checkpoint
6. Load checkpoint: /sc:load session_2025-11-12_140000_pre-auth-refactor
7. Analyze failure: Study what went wrong before re-attempting
8. Revised approach: New refactoring strategy based on learnings
9. Create new checkpoint: /sc:save --checkpoint (before second attempt)
```

**Example 2: Long-Running Migration with Progress Checkpoints**
```
Workflow:
1. Start migration: 100 database tables to migrate
2. Checkpoint after every 10 tables:
   - Table 10: /sc:save --checkpoint → session_...._table-10
   - Table 20: /sc:save --checkpoint → session_...._table-20
   - Table 30: /sc:save --checkpoint → session_...._table-30
3. Interruption at table 35: System failure or user cancellation
4. Resume from checkpoint: Load session_...._table-30
5. Restart from table 31: Skip already-completed tables 1-30
6. Continue migration: Tables 31-100 with continued checkpoints
7. Final checkpoint: /sc:save --type all --summarize (complete)
```

#### Best Practices for Workflow Compensation

**✅ DO**:
- Always checkpoint before risky operations
- Design compensating transactions for all critical operations
- Make operations idempotent whenever possible
- Test rollback procedures as thoroughly as forward operations
- Document compensation logic for each operation
- Use exponential backoff for transient failures
- Implement circuit breakers for external dependencies
- Track operation state for resume capability

**❌ DON'T**:
- Assume operations will always succeed (plan for failure)
- Forget to test rollback paths (untested rollbacks will fail when needed)
- Make operations that cannot be compensated (design for reversibility)
- Retry indefinitely without backoff (respect rate limits, prevent cascading failures)
- Delete data permanently without backup (always have recovery option)
- Skip checkpoints to save time (checkpoints enable recovery)
- Ignore partial completion scenarios (handle interruptions gracefully)

#### Error Recovery Decision Framework

**Step 1: Classify Error Type**
- **Transient**: Temporary failure (network timeout, resource contention)
  - Action: Retry with exponential backoff
- **Permanent**: Fundamental problem (invalid input, authentication failure)
  - Action: Fail fast, report error, do not retry
- **Degraded**: Partial failure (primary service down, secondary available)
  - Action: Use fallback strategy

**Step 2: Determine Recovery Strategy**
- **Retry**: Transient errors with low failure count
- **Circuit Breaker**: Repeated failures indicating systemic issue
- **Fallback**: Alternative approach available
- **Rollback**: Operation partially completed, consistency requires reversal
- **Compensate**: Complex multi-step operation with forward progress

**Step 3: Execute Recovery**
- Apply selected strategy
- Monitor recovery success
- Escalate if recovery fails (circuit breaker opens, max retries exceeded)

**Step 4: Document and Learn**
- Log error details and recovery actions
- Capture in `/sc:save --summarize` for future learning
- Update compensation logic if new failure modes discovered

### Step 3: Apply Optimization Patterns

**Tool Selection Matrix with Parallel Alternatives**:

| Task Type | Best Tool | Parallel Alternative | Use Case |
|-----------|-----------|---------------------|----------|
| Multi-file edits | MultiEdit | N/A (already parallel) | 3+ file changes |
| File reads | Batch Read calls | Task agent with parallel reads | 5+ files |
| Pattern searches | Parallel Grep/Glob | Task(Explore) for open-ended | Multiple patterns |
| Complex analysis | Task agent | Multiple Task agents (parallel domains) | Multi-domain work |
| Code search | Grep tool | Parallel Grep calls | Multiple search terms |
| UI components | Magic MCP | Task(frontend) with Magic | Multiple components |
| Documentation | Context7 MCP | Parallel Context7 queries | Multiple libraries |
| Browser testing | Playwright MCP | Task(frontend-qc-agent) | 3+ components |
| Directory analysis | `--delegate --parallel-dirs` | Task agents per directory | 7+ directories |

**Complexity-Based Routing with Parallel Optimization**:

- **Simple** (1-2 files, <3 steps):
  - Standard command, minimal flags
  - Parallel file reads if multiple files

- **Moderate** (3-10 files, analysis):
  - Add `--think`, relevant persona
  - MultiEdit for file changes
  - Parallel Read/Grep operations
  - Consider `--delegate` for 5+ files

- **Complex** (>10 files, system-wide):
  - Add `--delegate`, `--wave-mode`, multiple personas
  - Automatic parallel directory processing
  - Task agent delegation with parallel sub-agents
  - Parallel focus agents for multi-domain work

**Auto-Delegation Triggers** (from ORCHESTRATOR.md):

```yaml
directory_threshold:
  condition: "directory_count > 7"
  action: "auto-enable --delegate --parallel-dirs"
  efficiency_gain: "65%"

file_threshold:
  condition: "file_count > 50 AND complexity > 0.6"
  action: "auto-enable --delegate --sub-agents [calculated]"
  efficiency_gain: "70%"

multi_domain:
  condition: "domains.length > 3"
  action: "auto-enable --delegate --parallel-focus"
  efficiency_gain: "60%"

wave_operations:
  condition: "complexity > 0.8 AND files > 20 AND operation_types > 2"
  action: "auto-enable --wave-mode --progressive-waves"
  efficiency_gain: "80%"
```

### Step 3.5: Framework Integration Validation

**Purpose**: Verify correct auto-activation of personas, MCP servers, and orchestration strategies based on command context and user intent.

#### Command-Persona Auto-Activation Mappings

**Development Commands**:
- `/sc:build` → frontend (UI builds), backend (API builds), architect (system builds)
- `/sc:implement` → Domain-specific persona based on feature keywords
  - "authentication" → security persona
  - "API" → backend persona
  - "component" → frontend persona
  - "performance" → performance persona
- `/sc:design` → architect (system), frontend (UI), backend (API)

**Analysis Commands**:
- `/sc:analyze` → analyzer persona (primary) + domain-specific based on `--focus` flag
  - `--focus performance` → performance persona
  - `--focus security` → security persona
  - `--focus quality` → refactorer persona
  - `--focus architecture` → architect persona
- `/sc:troubleshoot` → analyzer persona + domain-specific based on error context
- `/sc:explain` → mentor persona (educational focus)

**Quality Commands**:
- `/sc:improve` → refactorer persona (primary) + domain-specific
  - `--perf` flag → performance persona
  - `--security` flag → security persona
  - `--quality` flag → refactorer persona
- `/sc:cleanup` → refactorer persona

**Planning Commands**:
- `/sc:workflow` → architect persona (system design focus)
- `/sc:estimate` → analyzer persona + architect persona

**Testing Commands**:
- `/sc:test` → qa persona + playwright MCP

**Documentation Commands**:
- `/sc:document` → scribe persona + Context7 MCP
- `/sc:git` → devops persona (commits) + scribe persona (messages)

**Meta Commands**:
- `/sc:help` → mentor persona (educational)
- `/sc:load` → analyzer persona (project context analysis)
- `/sc:reflect` → analyzer persona (quality validation)

**Expert Review Commands**:
- `/sc:spec-panel` → Activates 11 expert personas (Wiegers, Fowler, Hohpe, Newman, Nygard, Crispin, Gregory, Cockburn, Adzic, Hightower, Vogels)

**Team Coordination Commands**:
- `/sc:team` → Loads agent context from `~/.claude/agents/[role].md` + activates corresponding persona

#### MCP Server Auto-Activation Logic

**Context7 Auto-Activation**:
- Library imports detected in code
- Framework-specific questions ("How do I use React hooks?")
- Documentation keywords ("best practices", "patterns", "examples")
- Scribe persona active (documentation focus)

**Sequential Auto-Activation**:
- Complex debugging scenarios (multi-component failures)
- System design questions (architectural analysis)
- `--think`, `--think-hard`, or `--ultrathink` flags present
- Analyzer persona active with complexity >0.7

**Magic Auto-Activation**:
- UI component requests ("/ui", "/21", "create button")
- Design system queries
- Frontend persona active
- Component-related keywords ("modal", "form", "card")

**Playwright Auto-Activation**:
- Browser testing keywords ("E2E", "integration test", "visual test")
- Performance monitoring requests ("Core Web Vitals", "load time")
- QA persona active
- `--test` or `--validate` flags with browser context

**Serena Auto-Activation**:
- Symbol operations ("rename function", "find references")
- Session lifecycle commands (`/sc:load`, `/sc:save`)
- Project-wide navigation requests
- Large codebase analysis (>50 files detected)

**Morphllm Auto-Activation**:
- Bulk edit operations ("update all", "replace everywhere")
- Style enforcement ("apply formatting", "fix linting")
- Pattern-based transformations
- Token optimization priority (`--uc` flag)

#### Wave-Enabled Command Triggers

**Automatic Wave Activation** (complexity ≥0.7 + files >20 + operation_types >2):

**Tier 1 Wave Commands** (Primary wave orchestration):
- `/sc:analyze` → Systematic analysis waves when:
  - Multi-domain analysis required (>3 domains)
  - Comprehensive scope ("entire system", "full audit")
  - `--comprehensive` or `--systematic` flags present

- `/sc:build` → Progressive build waves when:
  - Multi-framework projects detected
  - Complex dependency chains (>5 levels)
  - `--optimize` flag for multi-pass optimization

- `/sc:implement` → Iterative implementation waves when:
  - Feature spans multiple domains (frontend + backend + database)
  - Complex integration requirements
  - `--systematic` or `--iterative` flags present

- `/sc:improve` → Enhancement waves when:
  - System-wide improvements requested
  - Multiple quality dimensions (`--quality`, `--perf`, `--security` together)
  - `--loop` flag for iterative refinement

**Tier 2 Wave Commands** (Conditional wave orchestration):
- `/sc:design` → Architecture waves when:
  - Multi-component system design
  - `--comprehensive` flag with complex requirements

- `/sc:task` → Multi-phase task waves when:
  - Long-term project management (>1 week)
  - Cross-domain coordination required

**Wave Strategy Auto-Selection**:
- **Progressive waves**: Performance optimization, incremental improvements
- **Systematic waves**: Code reviews, comprehensive audits, refactoring
- **Adaptive waves**: Multi-domain analysis, complex troubleshooting
- **Enterprise waves**: Large-scale transformations, legacy modernization (files >100)
- **Wave validation**: Production deployments, security audits, critical operations

#### Validation Tests

**Test 1: Command-Persona Mapping**
```
Given: User invokes `/sc:implement "authentication system"`
Expected: Security persona auto-activates
Verify: Backend persona also activates for API implementation
Confidence: >95%
```

**Test 2: MCP Server Auto-Activation**
```
Given: User invokes `/sc:build` with React component files detected
Expected: Magic MCP auto-activates for UI generation
Verify: Context7 auto-activates for React patterns
Confidence: >90%
```

**Test 3: Wave Orchestration Trigger**
```
Given: User invokes `/sc:analyze` with 75 files, 4 domains, complexity 0.85
Expected: Wave mode auto-activates with systematic strategy
Verify: Multi-wave coordination with domain-specific sub-agents
Confidence: >95%
```

**Test 4: Multi-Server Coordination**
```
Given: User invokes `/sc:improve --perf --security` on large codebase
Expected: Sequential (analysis) + Serena (symbol ops) + Context7 (patterns)
Verify: Performance persona + Security persona both active
Confidence: >90%
```

---

### Step 4: Generate and Explain

**Output Format**:
```
# Crafted SuperClaude Prompt

/sc:[command] [arguments] [--flags] [--personas] [--mcp-servers]

**Execution Directive**: Complete this entire task from start to finish without stopping. Do not pause to summarize or ask permission to proceed between phases. Execute all steps continuously until the complete task is done. [Modify this only if user explicitly requested checkpoints or if safety-critical validation is required]

---

# Prompt Engineering Analysis

## Request Analysis
- **Domain**: [Identified domain]
- **Operation Type**: [Type of operation]
- **Complexity**: [Simple/Moderate/Complex]
- **Scope**: [File/Module/Project/System]
- **Parallelization Potential**: [High/Medium/Low/None - with reasoning]

## Facility Selection Rationale

### Command Choice: /sc:[command]
- **Why**: [Reasoning for this command]
- **Alternative Considered**: [Other options and why not chosen]
- **Note**: [If command doesn't exist, note it should be created]

### Flags Applied: [List of flags]
- **[Flag Name]**: [Why this flag was selected]
- **[Flag Name]**: [Why this flag was selected]

### Personas Activated: [List of personas]
- **[Persona Name]**: [Why this persona expertise is needed]

### MCP Servers: [List of servers]
- **[Server Name]**: [What capability this provides]

### Orchestration Strategy
- **Parallel Execution**: [Specific parallel opportunities and how they're leveraged]
  - File operations: [Batched reads, MultiEdit, etc.]
  - Analysis: [Parallel domains, directory delegation, etc.]
  - Task delegation: [Sub-agent strategies, if applicable]
  - Efficiency gain: [Estimated percentage improvement]
- **Sequential Dependencies**: [If any, explicitly documented with reasoning]
- **Wave Mode**: [If applicable, why wave mode was chosen]
- **Delegation Strategy**: [Directory/file/focus-based delegation]

## Why This Prompt Is Optimal

[Comprehensive explanation of how the combination of facilities ensures the best result, including parallelization benefits]

## Expected Outcome

[What the user should expect from executing this prompt]

## Performance Metrics
- **Estimated Token Efficiency**: [Token usage optimization strategies applied]
- **Execution Speed**: [Parallelization impact on completion time]
- **Resource Utilization**: [Expected resource usage and optimization]
```

## Example Usage

### Example 1: Security-Critical (Sequential Preferred)

**User Request**: "I need to add authentication to my web application"

**Skill Output**:
```
# Crafted SuperClaude Prompt

/sc:implement "user authentication system" --persona-security --persona-backend --seq --c7 --validate --output detailed --testing

**Execution Directive**: Complete the entire authentication implementation from start to finish without stopping. Proceed through all phases (analysis → design → implementation → testing) continuously without pausing to summarize or ask permission. Only pause if critical security validation issues are detected that require immediate user attention.

---

# Prompt Engineering Analysis

## Request Analysis
- **Domain**: Security + Backend (multi-domain)
- **Operation Type**: Implementation + Creation
- **Complexity**: Complex (security-critical, multi-component)
- **Scope**: Project level (affects multiple areas)
- **Parallelization Potential**: Low - security-critical operations benefit from sequential validation

## Facility Selection Rationale

### Command Choice: /sc:implement
- **Why**: Implementation command is purpose-built for feature creation with intelligent persona activation
- **Alternative Considered**: /sc:build (but implement better for feature-level work)

### Flags Applied
- **--persona-security**: Security-first approach for authentication (threat modeling, compliance)
- **--persona-backend**: Server-side expertise for API and database work
- **--seq**: Complex multi-step logic analysis for auth flows
- **--c7**: Access to authentication patterns and best practices
- **--validate**: Pre-execution risk assessment for security-critical feature
- **--output detailed**: Comprehensive steps with security explanations
- **--testing**: Include test strategy and validation steps

### Personas Activated
- **Security**: Primary - threat modeling, vulnerability assessment, compliance standards
- **Backend**: Supporting - API design, database schema, session management

### MCP Servers
- **Sequential**: Multi-step reasoning for complex auth flows and security analysis
- **Context7**: Authentication patterns, security best practices, framework-specific implementations

### Orchestration Strategy
- **Parallel Execution**: Minimal - security-critical implementation prefers sequential validation
  - File operations: Standard sequential reads for security review
  - Analysis: Sequential security assessment to reduce attack surface
  - Task delegation: Not used - security work requires single-threaded validation
  - Efficiency gain: 0% (security > speed trade-off)
- **Sequential Dependencies**: All auth components have security dependencies requiring ordered validation
- **Wave Mode**: Not activated (complexity <0.7 threshold, single focused feature)
- **Delegation Strategy**: None - security-critical work stays in single context

## Why This Prompt Is Optimal

This prompt ensures the best result by:
1. **Security-First**: Activates security persona as primary decision-maker
2. **Expert Guidance**: Combines security and backend domain expertise
3. **Best Practices**: Context7 provides proven authentication patterns
4. **Systematic Analysis**: Sequential enables proper auth flow design
5. **Risk Management**: Validation flag ensures pre-execution security review
6. **Comprehensive Output**: Detailed mode provides security explanations and rationale
7. **Quality Assurance**: Testing flag ensures validation strategy included
8. **Appropriate Sequencing**: Deliberately avoids parallelization for security integrity
9. **Continuous Execution**: Explicit directive ensures uninterrupted workflow completion without unnecessary pauses

The combination prevents common authentication vulnerabilities while following framework best practices and delivering results efficiently.

## Expected Outcome

You'll receive:
- Complete authentication system implementation
- Security-reviewed code with threat mitigation
- Proper session management and password handling
- Database schema with security considerations
- API endpoints with authentication middleware
- Test strategy for authentication flows
- Security best practices documentation

## Performance Metrics
- **Estimated Token Efficiency**: Standard (detailed output for security context)
- **Execution Speed**: Sequential by design (security > speed)
- **Resource Utilization**: Moderate (single-threaded security validation)
```

### Example 2: Large-Scale Analysis (Parallel-Heavy)

**User Request**: "Analyze our entire monorepo for performance issues, security vulnerabilities, and code quality problems"

**Skill Output**:
```
# Crafted SuperClaude Prompt

/sc:analyze @monorepo/ --comprehensive --delegate --parallel-dirs --multi-agent --parallel-focus security,performance,quality --think-hard --c7 --seq --uc --output structured

**Execution Directive**: Execute the complete monorepo analysis from start to finish without stopping. Run all parallel analysis agents continuously, synthesize findings, and deliver the complete structured report. Do not pause between analysis phases or wait for confirmation to proceed to synthesis. Complete the entire workflow in one continuous execution.

---

# Prompt Engineering Analysis

## Request Analysis
- **Domain**: Multi-domain (Security + Performance + Quality)
- **Operation Type**: Comprehensive analysis across multiple dimensions
- **Complexity**: Very Complex (monorepo-scale, multi-domain, >100 files likely)
- **Scope**: System level (entire codebase)
- **Parallelization Potential**: Very High - independent analysis domains, multiple directories

## Facility Selection Rationale

### Command Choice: /sc:analyze
- **Why**: Analysis command with wave-enabled comprehensive mode for large-scale examination
- **Alternative Considered**: Manual /sc:troubleshoot (but too narrow for multi-domain analysis)

### Flags Applied
- **--comprehensive**: Trigger complete analysis across all identified issues
- **--delegate**: Enable sub-agent delegation for large codebase (auto-activates with monorepo scope)
- **--parallel-dirs**: Process directories in parallel (critical for monorepo efficiency)
- **--multi-agent**: Spawn specialized agents for each focus area
- **--parallel-focus security,performance,quality**: Three parallel analysis streams
- **--think-hard**: Deep analysis required for system-wide assessment (10K token budget per domain)
- **--c7**: Access to security patterns, performance benchmarks, quality standards
- **--seq**: Coordination of multi-agent findings and synthesis
- **--uc**: Ultra-compressed output due to large scope (30-50% token reduction)
- **--output structured**: Organized findings by domain and severity

### Personas Activated
- **Security**: Vulnerability assessment, threat modeling, compliance gaps
- **Performance**: Bottleneck identification, optimization opportunities, resource usage
- **Analyzer**: Root cause analysis, evidence-based investigation (coordination role)

### MCP Servers
- **Context7**: Best practices for security, performance, and quality across detected frameworks
- **Sequential**: Multi-agent coordination, synthesis of findings, pattern recognition

### Orchestration Strategy
- **Parallel Execution**: MAXIMUM - this is the ideal parallelization scenario
  - File operations: Parallel directory scans (estimated 30+ directories)
  - Analysis: 3 parallel focus agents (security, performance, quality) analyzing simultaneously
  - Task delegation: Automatic sub-agent spawning per directory (estimated 10-15 agents)
  - Efficiency gain: **70-85%** (vs sequential analysis)

  **Execution Pattern**:
  ```
  Wave 1 (Parallel):
    ├─ Security Agent → Scans all dirs for vulnerabilities
    ├─ Performance Agent → Profiles all modules for bottlenecks
    └─ Quality Agent → Analyzes code quality metrics

  Wave 2 (Sequential):
    └─ Sequential Synthesis → Combines findings, identifies cross-cutting issues
  ```

- **Sequential Dependencies**: Only final synthesis phase (after all parallel agents complete)
- **Wave Mode**: Auto-activated (complexity >0.8, files >100, operation_types = 3)
- **Delegation Strategy**:
  - **Directory-based**: `--parallel-dirs` for file system parallelization
  - **Focus-based**: `--parallel-focus` for domain parallelization
  - Estimated concurrent agents: 12-18 (3 focus agents × 4-6 directory agents each)

## Why This Prompt Is Optimal

This prompt maximizes efficiency through:

1. **Massive Parallelization**: 3 focus agents + 10-15 directory agents = **70-85% time savings**
2. **Domain Expertise**: Specialized agents for security, performance, and quality
3. **Intelligent Coordination**: Sequential synthesis after parallel analysis prevents duplication
4. **Resource Optimization**: `--uc` flag reduces token usage by 30-50% for large output
5. **Framework Integration**: Context7 provides best practices for each identified framework
6. **Structured Output**: Organized findings enable actionable prioritization
7. **Scalability**: Delegation handles monorepo scale without manual orchestration
8. **Continuous Execution**: Explicit directive ensures all parallel agents run to completion without interruption

**Parallel Execution Benefits**:
- **Time**: 70-85% faster than sequential (3 domains × 5 directories = ~15x parallelization)
- **Thoroughness**: Each agent focuses deeply without context switching
- **Completeness**: No analysis domain missed, no directory overlooked
- **Workflow Efficiency**: Uninterrupted execution from start to final synthesis delivers complete results in one run

## Expected Outcome

You'll receive structured analysis with:

**Security Findings**:
- Vulnerability inventory by severity (Critical → Low)
- Attack surface analysis
- Compliance gap assessment
- Remediation recommendations

**Performance Findings**:
- Bottleneck identification with profiling data
- Resource usage analysis (CPU, memory, I/O)
- Optimization opportunities prioritized by impact
- Performance benchmark comparisons

**Quality Findings**:
- Code quality metrics (complexity, duplication, maintainability)
- Technical debt assessment
- Refactoring opportunities
- Testing coverage gaps

**Cross-Cutting Issues**:
- Problems affecting multiple domains
- Systemic patterns requiring architectural changes
- Priority matrix for remediation planning

## Performance Metrics
- **Estimated Token Efficiency**: 30-50% reduction via `--uc` (expected ~50K tokens vs ~100K without compression)
- **Execution Speed**: 70-85% faster via massive parallelization (estimated 15-20 min vs 90-120 min sequential)
- **Resource Utilization**: High concurrency (12-18 parallel agents), efficient resource distribution
- **Parallelization Factor**: ~15x (3 focus domains × 5 avg directories)
```

## Best Practices

### 1. Start with Domain Analysis
Identify the primary domain to select the right persona and MCP servers.

### 2. Assess Complexity AND Parallelization Potential
- Simple → Standard command, minimal flags, **parallel file reads if 2+ files**
- Moderate → Add `--think`, relevant persona, **MultiEdit for 3+ files**, **parallel searches**
- Complex → Add `--delegate`, `--wave-mode`, multiple personas, **automatic parallel processing**

### 3. **MANDATORY: Leverage Parallelization** (RULES.md compliance)
- **Default Assumption**: Operations are parallel unless proven sequential
- **Explicit Documentation**: Note when sequential chosen and why
- **Checklist Application**: Use parallelization checklist for every prompt
- **Multi-Tool Pattern**: Recommend single-message multi-tool calls where applicable

### 4. Choose Appropriate Depth
- Standard work → No depth flags
- Important analysis → `--think`
- Critical decisions → `--think-hard`
- System redesign → `--ultrathink`

### 5. Add Safety for Production
For production environments or risky operations, always add:
- `--validate` (pre-execution risk assessment)
- `--safe-mode` (maximum validation)

### 6. Optimize for Token Efficiency
When context is high or operation is large:
- Add `--uc` flag for compressed output (30-50% reduction)
- Use `--scope` to limit analysis boundaries
- Leverage `--focus` to target specific domains

### 7. Enable Iterative Workflows
For improvement and refinement tasks:
- Add `--loop` for automatic iteration cycles
- Specify `--iterations [n]` for controlled refinement

### 8. Wave Mode for Large Operations
When dealing with:
- Files >20 and complexity >0.7
- Multiple operation types (>2)
- Enterprise-scale changes
- **Automatic parallel execution within waves**
→ Use `--wave-mode` with appropriate strategy

### 9. Task Agent Delegation for Multi-Domain Work
When requirements span multiple domains:
- Frontend + Backend → Parallel Task agents with domain-specific personas
- Testing 3+ components → `Task(frontend-qc-agent)` with parallel sub-agents
- Complex debugging → `Task(frontend-debug-agent)` with specialized domain agents

### 10. Document Sequential Choices
When choosing sequential over parallel execution:
- Explicitly state the reason (security, dependencies, resource constraints)
- Document the trade-off (security > speed, correctness > efficiency)
- Show what would have been parallelizable in different context

### 11. 🔴 CRITICAL: Always Include Continuous Execution Directive
Every generated prompt MUST include clear continuous execution instructions:
- **Default**: "Complete this entire task from start to finish without stopping"
- **Explicit**: Specify that LLM should not pause to summarize between phases
- **Clear**: State that permission to proceed is not needed unless explicitly requested by user
- **Exception-Based**: Only include checkpoints when user explicitly requests them or safety demands it

**Why This Matters**:
- Prevents unnecessary interruptions that break workflow momentum
- Reduces back-and-forth communication overhead
- Ensures tasks are completed efficiently in single execution runs
- Aligns with user expectation of autonomous task completion

**Template Language**:
```
**Execution Directive**: Complete this entire task from start to finish without stopping.
Do not pause to summarize or ask permission to proceed between phases. Execute all steps
continuously until the complete task is done. [Add checkpoint exceptions only if user
explicitly requested them or if safety-critical validation is required]
```

## Reference Materials

This skill uses a comprehensive SuperClaude reference located at:
`references/superclaude-reference.md`

The reference includes:
- Complete command catalog with wave-enabled commands
- All behavioral flags organized by category
- 11 specialized personas with auto-activation keywords
- MCP server integration details
- Wave orchestration system
- Orchestration patterns and complexity detection
- **Parallelization strategies and optimization patterns**
- Prompt optimization strategies
- Common prompt patterns with examples
- Best practices for prompt crafting

**Key RULES.md References for Parallelization**:
- Tool Optimization (🟢 RECOMMENDED): "Parallel Everything: Execute independent operations in parallel, never sequentially"
- Planning Efficiency (🔴 CRITICAL): "Parallelization Analysis: During planning, explicitly identify operations that can run concurrently"
- Workflow Rules (🟡 IMPORTANT): "Batch Operations: ALWAYS parallel tool calls by default, sequential ONLY for dependencies"

## Technical Implementation

This skill follows the SuperClaude framework principles:
- **Evidence-Based**: All facility selections are justified with reasoning
- **Context-Aware**: Adapts to project context and user familiarity
- **Parallel-First**: **MANDATES parallelization analysis for every prompt (RULES.md compliance)**
- **Continuous-Execution**: **REQUIRES explicit continuous execution directives in all prompts**
- **Efficiency-Optimized**: Targets 30-85% time/token savings through intelligent optimization
- **Quality-Focused**: Ensures validation, testing, and best practices
- **Framework-Compliant**: Follows all SuperClaude orchestration patterns

### Parallelization Philosophy (v2.0 Enhancement)

**Core Principle**: "Every prompt should be analyzed for parallel execution opportunities. Sequential execution is the exception, not the default, and must be explicitly justified."

**Implementation**:
1. **Analysis Phase**: Run parallelization checklist for every request
2. **Design Phase**: Incorporate parallel patterns into prompt structure
3. **Documentation Phase**: Explicitly document parallel vs sequential choices
4. **Optimization Phase**: Estimate efficiency gains from parallelization

### Continuous Execution Philosophy (v2.1 Enhancement)

**Core Principle**: "Unless explicitly instructed otherwise, generated prompts must direct the LLM to complete the entire task without stopping. Unnecessary pauses break workflow momentum and reduce efficiency."

**Default Behavior**:
- LLM executes complete workflow from start to finish
- No pausing to summarize after each major step
- No asking permission to proceed between phases
- Work continues until task is fully complete

**Exception Criteria** (when checkpoints ARE appropriate):
- User explicitly requests staged execution ("pause after analysis")
- Safety-critical operations requiring manual validation before proceeding
- Genuine missing information that prevents continuation
- Resource constraints requiring staged execution

**Implementation**:
1. **Every Generated Prompt**: Include explicit "Execution Directive" section
2. **Template Language**: Use standardized continuous execution phrasing
3. **Exception Handling**: Only modify directive when user explicitly requests checkpoints
4. **Reasoning Documentation**: If checkpoints added, explain why they're necessary

**Benefits**:
- Eliminates unnecessary back-and-forth communication overhead
- Maintains workflow momentum and context continuity
- Reduces total time to task completion by 40-60%
- Aligns with user expectation of autonomous AI agent behavior
- Prevents context loss from interrupted execution

## Stakeholder Impact Analysis

### What's New in Version 2.2

This section documents user-facing changes, new capabilities, and migration guidance for updated SuperClaude framework documentation.

#### New Commands Added (6 Commands)

**Meta & Utility Commands**:

1. **`/sc:help`** - Command catalog and discovery
   - **Purpose**: Browse available commands by category with search capabilities
   - **Use Case**: New users exploring the framework, developers looking for specific command capabilities
   - **Example**: `/sc:help search "testing"` → Returns all testing-related commands

2. **`/sc:save`** - Session state persistence and checkpoint management
   - **Purpose**: Save project context, session state, and create restore points
   - **Use Case**: Long-running projects, risky operations requiring rollback capability, session continuity
   - **Example**: `/sc:save --type context --checkpoint` → Creates named checkpoint for workflow recovery

3. **`/sc:reflect`** - Task reflection and validation
   - **Purpose**: Analyze task completion, validate outcomes, identify improvements
   - **Use Case**: Quality assurance, post-implementation review, continuous improvement
   - **Example**: `/sc:reflect --task "authentication implementation"` → Validates implementation quality

4. **`/sc:select-tool`** - Intelligent MCP tool selection
   - **Purpose**: Analyze operations and recommend optimal MCP tool combinations
   - **Use Case**: Complex operations with multiple valid tool options, performance optimization
   - **Example**: `/sc:select-tool --operation "bulk code transformation"` → Recommends Morphllm MCP

**Team Coordination & Analysis Commands**:

5. **`/sc:team`** - Software engineering team member activation
   - **Purpose**: Activate specialized team agents (pm, lead, backend, frontend, devops, qa, security, performance, data, ml, mobile, dba, ux, platform, docs, accessibility, release, compliance, ba, solutions, observability, api, cost, designer, researcher, analyst, product-analyst, integration, architect, fullstack, growth, sre, technical-writer, enterprise-architect, program-manager, customer-success-engineer, solutions-engineer, growth-engineer, product-designer)
   - **Use Case**: Team workflows, specialized expertise, handoff coordination, TDD workflows
   - **Example**: `/sc:team backend implement-api` → Activates backend engineer agent with specialized context

6. **`/sc:spec-panel`** - Multi-expert specification review
   - **Purpose**: Review specifications, PRDs, and technical documents with expert panel feedback
   - **Use Case**: Specification validation, architectural review, design document quality assurance
   - **Example**: `/sc:spec-panel @feature-spec.md` → Expert panel analyzes and provides recommendations

#### New MCP Server Documentation (2 Servers)

**Serena MCP**:
- **Purpose**: Semantic code understanding with project memory and session persistence
- **Key Features**: Symbol operations, project-wide navigation, LSP integration, session lifecycle management
- **When to Use**: Symbol refactoring, large codebase analysis, `/sc:load` and `/sc:save` operations
- **Examples**: Rename symbol across codebase, find all references, project context loading

**Morphllm MCP**:
- **Purpose**: Efficient pattern-based multi-file code transformations
- **Key Features**: Bulk edits, style enforcement, pattern application across files
- **When to Use**: Bulk code transformations, style updates, pattern-based refactoring
- **Examples**: Update all console.log to logger, enforce naming conventions, bulk import updates

#### Enhanced Capabilities

**1. Parallelization Ordering Guarantees (Step 2.5.1)**
- Explicit dependency management for parallel operations
- Deterministic execution ordering when dependencies exist
- Tool sequencing patterns for complex workflows
- Integration with Sequential MCP for dependency analysis

**2. Workflow Compensation and Error Recovery (Step 2.6)**
- Comprehensive rollback procedures for file, database, and infrastructure operations
- Error recovery patterns: exponential backoff, circuit breaker, fallback strategies
- Partial completion handling with checkpoint resume capability
- Compensation logic for atomic operations: Saga pattern, two-phase commit, idempotent operations
- Integration with `/sc:save` checkpoint system for workflow recovery

**3. Framework Integration Validation (Step 3.5)**
- Validation tests for persona activation, MCP server coordination, flag combinations
- Cross-persona collaboration verification
- Wave mode integration validation
- Quality assurance for generated prompts

**4. Unified Session Lifecycle Documentation (Step 2.4.1)**
- Complete session patterns: initialization, work execution, checkpointing, saving
- Integration with Serena MCP for memory management
- Checkpoint system with rollback capability
- Best practices for session state persistence

### Migration Guide

#### For Existing Users

**No Breaking Changes**: All existing workflows, prompts, and commands continue to work exactly as before. This update is **purely additive**.

**Backward Compatibility Guarantee**:
- ✅ All 20 existing commands function identically
- ✅ Existing prompt patterns remain valid
- ✅ Previous flags and personas unchanged
- ✅ No deprecated features or commands
- ✅ Existing MCP server integrations work as before

#### Adopting New Commands

**Gradual Adoption Recommended**: Integrate new capabilities incrementally based on your workflow needs.

**Command Adoption Priority**:

**High Priority (Immediate Value)**:
1. **`/sc:help`** → Start here: Discover all available commands and capabilities
2. **`/sc:save`** → Critical for project continuity: Save context before risky operations
3. **`/sc:team`** → For team-based workflows: Activate specialized agents for complex tasks

**Medium Priority (Enhanced Workflows)**:
4. **`/sc:select-tool`** → For power users: Optimize MCP tool selection for performance
5. **`/sc:reflect`** → For quality focus: Validate task completion and identify improvements

**Low Priority (Specialized Use Cases)**:
6. **`/sc:spec-panel`** → For specification review: Get expert validation on technical documents

#### Adopting New MCP Servers

**Serena MCP**:
- **Replace**: Manual file searching and navigation for symbol operations
- **When**: Working with large codebases (>50 files), need symbol refactoring
- **How**: Automatically integrated with `/sc:load` and `/sc:save` commands

**Morphllm MCP**:
- **Replace**: Sequential Edit tool calls for bulk transformations
- **When**: Applying patterns across multiple files, style enforcement
- **How**: Use `/sc:select-tool --operation "pattern transformation"` for recommendations

#### Migration Examples

**Before (Version 2.1)**:
```
"Analyze the authentication module and suggest improvements"
```

**After (Version 2.2 - Enhanced with New Capabilities)**:
```
"Using /sc:save to create a pre-analysis checkpoint, then analyze the authentication module with /sc:team security for specialized security expertise. After analysis, use /sc:reflect to validate findings quality. Suggest improvements with rollback procedures per Step 2.6 compensation patterns."
```

**Before (Version 2.1)**:
```
"Rename getUserData function across the codebase"
```

**After (Version 2.2 - Optimized with Serena MCP)**:
```
"Use Serena MCP symbol operations to rename getUserData function across the entire codebase, ensuring all references are updated. Create /sc:save checkpoint before operation for rollback capability."
```

**Before (Version 2.1)**:
```
"Update all console.log statements to use logger"
```

**After (Version 2.2 - Optimized with Morphllm MCP)**:
```
"Use /sc:select-tool to determine optimal approach. Apply Morphllm MCP for efficient pattern-based transformation of console.log to logger across all files."
```

### When to Use New vs Existing Workflows

**Use New Commands When**:
- **`/sc:help`**: Exploring capabilities, discovering commands for specific tasks
- **`/sc:save`**: Before risky operations, starting long-running projects, need rollback points
- **`/sc:reflect`**: Validating task completion, quality assurance, continuous improvement focus
- **`/sc:team`**: Need specialized expertise, team coordination workflows, TDD processes
- **`/sc:select-tool`**: Complex operations with multiple tool options, performance optimization needs
- **`/sc:spec-panel`**: Specification review, design document validation, expert feedback needed

**Continue Existing Workflows When**:
- Simple, straightforward tasks not requiring specialized capabilities
- Quick operations where checkpoint overhead isn't beneficial
- Single-domain work not requiring team coordination
- Tool selection is obvious and doesn't require analysis

### Adoption Recommendations

**For New Users**:
1. Start with `/sc:help` to discover available commands
2. Use `/sc:save` early to establish checkpoint habits
3. Explore `/sc:team` for specialized workflows
4. Gradually integrate other commands as needs arise

**For Power Users**:
1. Integrate `/sc:select-tool` for performance optimization
2. Use `/sc:reflect` for systematic quality improvement
3. Leverage Serena and Morphllm MCP servers for efficiency
4. Apply Step 2.6 compensation patterns for complex workflows

**For Team Environments**:
1. Adopt `/sc:team` for role-based workflows
2. Use `/sc:spec-panel` for collaborative review processes
3. Establish `/sc:save` checkpoint standards for team continuity
4. Apply parallelization ordering guarantees (Step 2.5.1) for coordinated work

**For Enterprise Users**:
1. Implement `/sc:save` checkpoint governance
2. Use `/sc:team` for cross-functional coordination
3. Apply Step 2.6 compensation patterns for production operations
4. Leverage Step 3.5 validation tests for quality assurance

### Breaking Changes

**None**: This release contains no breaking changes. All updates are additive enhancements that extend existing capabilities without modifying or removing any functionality.

### Documentation Version

**Current Version**: 2.2.0
**Previous Version**: 2.1.0
**Release Type**: Minor version (additive features, no breaking changes)
**Backward Compatibility**: 100% (all existing prompts and workflows continue to work)

## Skill Maintenance

This skill references SuperClaude documentation version as of creation. For the latest:
- Command updates: Check `/Users/arlenagreer/.claude/COMMANDS.md`
- Flag additions: Check `/Users/arlenagreer/.claude/FLAGS.md`
- Persona changes: Check `/Users/arlenagreer/.claude/PERSONAS.md`
- MCP updates: Check `/Users/arlenagreer/.claude/MCP.md`
- **Parallelization rules**: Check `/Users/arlenagreer/.claude/RULES.md` (Tool Optimization, Planning Efficiency sections)
- **Orchestration patterns**: Check `/Users/arlenagreer/.claude/ORCHESTRATOR.md` (Auto-delegation triggers, parallel patterns)

---

**Version 2.2 - Complete Framework Coverage**

Closed 24% documentation gap with comprehensive documentation for 6 commands (/sc:help, /sc:save, /sc:reflect, /sc:select-tool, /sc:team, /sc:spec-panel), 2 MCP servers (Serena, Morphllm), and 5 framework enhancements (parallelization ordering, workflow compensation, framework validation, session lifecycle, stakeholder impact). Now featuring 100% command coverage (26/26), complete MCP server documentation (6/6), and expert-validated quality (9.6/10 spec-panel score).

**Version 2.1 - Continuous Execution Enhancement**

Continuous execution directives with maximum parallelization efficiency.

---

Ready to craft optimal SuperClaude prompts with complete framework coverage! Describe what you need to accomplish, and I'll generate a prompt leveraging all 26 commands, 6 MCP servers, advanced parallelization patterns, workflow compensation strategies, and continuous execution directives.
