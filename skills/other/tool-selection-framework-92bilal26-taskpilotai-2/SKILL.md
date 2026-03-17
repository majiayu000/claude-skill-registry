---
name: tool-selection-framework
category: "intelligence-design"
applies_to: ["context-management", "tool-optimization"]
required_for: ["content-implementer", "tool-strategy"]
description: |
  Design systematic decision frameworks for selecting appropriate AI tools (Claude Code vs Gemini CLI)
  based on context requirements, codebase size, reasoning depth needs, and task complexity. Use this
  skill when starting projects with unclear tool requirements, optimizing context-constrained workflows,
  or designing multi-phase strategies that leverage multiple tools' strengths. This skill helps match
  tool capabilities to task characteristics, preventing wasted context and ensuring optimal resource
  allocation.
version: "1.0.0"
dependencies: ["constitution:v6.0.1"]
---

# Tool Selection Framework

## Purpose

Enable developers to select the right AI tool for each development task through systematic evaluation of context requirements, codebase characteristics, and task complexity. This skill helps:
- Match tool capabilities (context window, reasoning depth, cost) to task requirements
- Design multi-phase workflows that leverage tool-specific strengths
- Optimize context utilization by choosing appropriate tool for codebase size
- Balance cost, performance, and reasoning depth based on project constraints
- Avoid wasting context with mismatched tool selection
- Create extensible decision frameworks that adapt to new tools

## When to Activate

Use this skill when:
- Starting new project with uncertain tool requirements
- Codebase size approaches/exceeds Claude Code context limits (200K tokens)
- Task requires broad exploration (large codebase analysis, pattern discovery)
- Task requires deep reasoning (architectural decisions, security analysis)
- Multi-phase workflow needed (exploration → implementation)
- Optimizing cost/performance balance for long-term project
- Team asks "Should we use Claude Code or Gemini CLI for this?"
- Students learning context-aware development tool selection

## Persona

"Think like a resource optimization engineer allocating specialized tools to tasks where each tool excels. Your goal is to maximize development productivity by matching tool capabilities—context window size, reasoning depth, cost efficiency—to specific task characteristics such as codebase size, complexity, and phase (exploration vs implementation)."

## Questions (Analysis Framework)

Before selecting a tool or designing a multi-tool workflow, analyze through these questions:

### Question 1: Codebase Size Assessment
**"How many lines of code does this project have?"**

**Size Categories**:
- **< 50K lines** → Claude Code sufficient
  - **Rationale**: 200K context window handles full codebase + conversation
  - **Action**: Use Claude Code exclusively
  - **Example**: Small web app, CLI tool, microservice

- **50K-500K lines** → Evaluate task type
  - **Rationale**: Codebase fits in Gemini (2M context) but may fit Claude Code with selective loading
  - **Decision depends on**: Task type (exploration vs focused), reasoning depth needed
  - **Action**: Apply Task Type Analysis (Question 2)
  - **Example**: Medium web application, API backend, data processing system

- **> 500K lines** → Gemini for exploration, Claude Code for implementation
  - **Rationale**: Full codebase exceeds Claude Code context; Gemini handles broad analysis
  - **Action**: Multi-phase workflow (Gemini → Claude Code)
  - **Example**: Large monolith, multi-service platform, legacy system

**How to measure**:
```bash
# Count lines of code (excluding comments, blank lines)
cloc . --exclude-dir=node_modules,venv
```

### Question 2: Task Type Evaluation
**"Is this an exploration task or focused implementation?"**

**Exploration Tasks** (Broad understanding, pattern discovery):
- Understanding unknown codebase architecture
- Finding all instances of pattern X across system
- Analyzing how feature Y is implemented everywhere
- Discovering dependencies and relationships
- Mapping data flow through large system
- **Tool recommendation**: Gemini CLI (2M context for broad scan)

**Focused Implementation** (Specific feature, bounded scope):
- Implementing one feature in known module
- Fixing specific bug in identified component
- Refactoring isolated function/class
- Adding unit tests for existing code
- Writing documentation for single module
- **Tool recommendation**: Claude Code (200K context sufficient, deep reasoning)

**Hybrid Tasks** (Both exploration and implementation):
- Feature spanning multiple unfamiliar modules
- Refactoring across unknown codebase
- Performance optimization requiring system understanding
- **Tool recommendation**: Multi-phase (Gemini explore → Claude Code implement)

### Question 3: Reasoning Depth Requirements
**"Does this task need deep architectural reasoning or surface-level pattern matching?"**

**Deep Reasoning Tasks** (Architectural decisions, tradeoffs, security):
- System design decisions (choosing architecture)
- Security analysis (finding vulnerabilities)
- Performance optimization (algorithmic improvements)
- Complex refactoring (maintaining correctness)
- Architectural decision records (weighing tradeoffs)
- **Tool recommendation**: Claude Code (superior reasoning, latest models)

**Pattern Matching Tasks** (Applying known solutions, generating boilerplate):
- Generating CRUD operations
- Creating standard API endpoints
- Writing boilerplate configuration
- Finding code duplication
- Applying consistent formatting
- **Tool recommendation**: Either tool (pattern matching doesn't require deepest reasoning)

**Exploration Tasks** (Understanding existing patterns):
- Reading unfamiliar codebase
- Understanding how system works
- Finding where functionality lives
- Mapping component relationships
- **Tool recommendation**: Gemini CLI (2M context for comprehensive scan)

### Question 4: Context Budget Constraints
**"What's the token budget for this task?"**

**Tight Budget** (Cost-sensitive, optimize per-token value):
- Personal projects (low budget)
- Repetitive tasks (frequent tool use)
- Learning/experimentation (many sessions)
- **Tool recommendation**: Claude Code (lower cost per token)
- **Strategy**: Use progressive loading, compress context aggressively

**Liberal Budget** (Exploration prioritized, cost secondary):
- Professional projects (budget allocated)
- One-time migrations (rare event, worth investment)
- Critical understanding needed (business value justifies cost)
- **Tool recommendation**: Gemini CLI acceptable for exploration
- **Strategy**: Load full codebase, comprehensive analysis

**Balanced Budget** (Cost matters, but productivity critical):
- Most development work
- **Tool recommendation**: Match tool to task (don't waste context)
- **Strategy**: Use Claude Code for focused work, Gemini sparingly for exploration

### Question 5: Time Sensitivity
**"Is this task time-critical?"**

**Time-Critical** (Fast iteration needed):
- Production bug fix (downtime costly)
- Urgent feature request (deadline pressure)
- Blocking issue (team waiting)
- **Tool recommendation**: Claude Code (faster response, optimized for development)
- **Strategy**: Focus scope, load only essential context

**Non-Time-Critical** (Thorough understanding prioritized):
- Learning new codebase (onboarding)
- Architectural planning (design phase)
- Technical debt analysis (long-term planning)
- **Tool recommendation**: Gemini CLI acceptable (thorough exploration worth time)
- **Strategy**: Comprehensive analysis, multi-phase if needed

### Question 6: Expertise Level
**"Do you already understand this codebase?"**

**Expert** (Familiar with codebase, know where things are):
- **Tool recommendation**: Claude Code (focused work in known areas)
- **Strategy**: Load relevant files, skip exploration

**Intermediate** (General familiarity, need occasional reference):
- **Tool recommendation**: Claude Code with on-demand loading
- **Strategy**: Foundation context + fetch references as needed

**Novice** (New to codebase, need broad understanding):
- **Tool recommendation**: Gemini CLI for initial exploration
- **Strategy**: Multi-phase (Gemini learn → Claude Code implement)

## Principles

### Principle 1: Right Tool for the Job
**"Don't use Gemini when Claude Code suffices; don't constrain Claude Code when Gemini excels."**

Match tool to task characteristics:
- **Small codebase** (<50K lines) → Claude Code (no need for 2M context)
- **Large codebase** (>500K lines) → Gemini for exploration (2M context handles full codebase)
- **Deep reasoning** (architecture, security) → Claude Code (superior reasoning)
- **Broad exploration** (unknown system) → Gemini (2M context for comprehensive scan)

**Anti-pattern**: Using Gemini for 10K-line project (wasting context, slower, higher cost)
**Anti-pattern**: Using Claude Code to explore 1M-line monolith (insufficient context, frustration)

### Principle 2: Specialization Value
**"Each tool has an optimal context window for its task type."**

Claude Code (200K context):
- Optimal for: Focused implementation in known modules
- Sufficient for: Small to medium codebases (<100K lines)
- Handles: Deep reasoning with adequate context
- Sweet spot: One feature, 10-20 files, architectural decisions

Gemini CLI (2M context):
- Optimal for: Broad exploration across large codebases
- Sufficient for: Understanding unfamiliar systems (>100K lines)
- Handles: Pattern discovery, relationship mapping, comprehensive analysis
- Sweet spot: Learning phase, multi-module understanding, system-wide patterns

### Principle 3: Multi-Phase Approach
**"Exploration + Implementation as sequential workflow, not single tool."**

When task requires both broad understanding AND focused implementation:
1. **Phase 1: Gemini (Exploration)**
   - Load large codebase (500K-2M lines)
   - Explore: "How does authentication work across all services?"
   - Generate summary document (5K-10K tokens)
   - Create knowledge checkpoint

2. **Phase 2: Claude Code (Implementation)**
   - Load Gemini summary (5K tokens)
   - Load Foundation/Current context (20K tokens)
   - Implement: "Add OAuth to authentication" (focused work)
   - Deep reasoning with adequate context (175K available)

**Result**: Best of both tools (comprehensive understanding + deep reasoning)

### Principle 4: Cost Awareness
**"Token budget influences tool selection for large codebases."**

Cost considerations:
- **Gemini CLI**: Higher cost per session (large context loaded)
  - **When justified**: Rare exploration tasks, one-time understanding, critical system analysis
  - **When wasteful**: Frequent use for small tasks, repeated loading of same context

- **Claude Code**: Lower cost per session (smaller context)
  - **When optimal**: Frequent focused work, iterative development, most implementation tasks
  - **When insufficient**: Large codebase exploration, comprehensive system analysis

**Strategy**: Use expensive tool (Gemini) strategically (exploration phase), then switch to efficient tool (Claude Code) for iteration.

### Principle 5: Future Extensibility
**"Framework applies to current tools; adapts to new tools."**

Tool landscape evolves:
- **Today**: Claude Code (200K), Gemini CLI (2M)
- **Tomorrow**: GPT-4 (128K), Claude Opus (1M), Gemini Ultra (10M)

Framework adapts:
- **Decision factors stay constant**: Codebase size, task type, reasoning depth, cost
- **Tool capabilities update**: New context window sizes, reasoning improvements, pricing changes
- **Apply same analysis**: Match evolving tool capabilities to task characteristics

**Example future decision**:
```
IF codebase < 100K lines:
  Use Claude Opus (1M context, superior reasoning)
ELSE IF codebase 100K-5M lines:
  Use Gemini Ultra (10M context, comprehensive exploration)
```

## Decision Algorithm

### Algorithm 1: Tool Selection Decision Tree

```
START: Assess Codebase Size

IF codebase < 50K lines:
  → Claude Code is sufficient
  → Use Claude Code for all work
  → END

ELSE IF codebase 50K-500K lines:
  → Evaluate task type

  IF task = "exploration" (understand unknown system):
    → Gemini first (broad understanding)
    → THEN Claude Code (focused implementation)
    → Go to Multi-Phase Workflow (Algorithm 2)

  ELSE IF task = "focused" (implement one feature):
    → Claude Code directly
    → Load relevant files (Foundation + Current)
    → END

  ELSE IF task = "deep reasoning" (architecture, security):
    → Claude Code (superior reasoning)
    → Load essential context only
    → END

ELSE IF codebase > 500K lines:
  → Claude Code insufficient
  → Multi-Phase Workflow required
  → Go to Algorithm 2

Multi-Phase Workflow (Algorithm 2):
  Phase 1: Gemini Session
    - Load full/large codebase
    - Explore: Answer architectural questions
    - Generate summary document (5K-10K tokens)
    - Create checkpoint

  Phase 2: Claude Code Session
    - Load Gemini summary (5K tokens)
    - Load Foundation/Current (20K tokens)
    - Implement feature with deep reasoning (175K available)

END: Execute with selected tool(s)
```

### Algorithm 2: Multi-Phase Workflow

```
Phase 1: Gemini Exploration

INPUT: Large codebase (>500K lines), exploration question

PROCESS:
1. Load codebase into Gemini (use 2M context)
2. Ask exploration questions:
   - "What's the overall architecture?"
   - "How does feature X work across services?"
   - "Where is Y implemented?"
3. Generate summary document:
   - Architecture overview (components, dependencies)
   - Key patterns discovered
   - Files relevant to current task
   - Constraints and design decisions
4. Save summary (target: <10K tokens)

OUTPUT: Summary document for Phase 2

---

Phase 2: Claude Code Implementation

INPUT: Summary from Phase 1, implementation task

PROCESS:
1. Load summary into Claude Code (5K-10K tokens)
2. Load Foundation context (CLAUDE.md, architecture.md, decisions.md)
3. Load Current context (files relevant to task)
4. Total context loaded: ~50K tokens
5. Available for work: 150K tokens
6. Implement feature with deep reasoning
7. Validate against specification

OUTPUT: Implemented feature

---

Checkpoint Between Phases:

Create checkpoint document:
- What was learned in Phase 1 (Gemini exploration)
- What will be implemented in Phase 2 (Claude Code work)
- Key constraints from exploration
- Files identified as relevant
```

## Tool Capability Matrix

| Factor | Claude Code | Gemini CLI |
|--------|-------------|------------|
| **Context Window** | 200K standard, 1M extended | 2M standard |
| **Best Use Case** | Focused implementation, deep reasoning | Broad exploration, large codebase analysis |
| **Reasoning Depth** | Excellent (latest models) | Good (sufficient for most) |
| **Cost per Session** | Lower (smaller context) | Higher (larger context) |
| **Response Latency** | Faster (optimized for dev) | Potentially slower (larger context) |
| **Ideal Codebase Size** | <100K lines | >100K lines |
| **Task Complexity** | Deep architectural reasoning | Pattern discovery, relationship mapping |
| **Specialization** | AI-native development | General-purpose exploration |

## Examples

### Example 1: Small Project (30K lines)

**Scenario**: Building a Flask API (30K lines of code)

**Analysis**:
- **Codebase size**: 30K lines → Claude Code sufficient
- **Task type**: Adding new API endpoint (focused implementation)
- **Reasoning depth**: Moderate (standard CRUD operation)
- **Context budget**: Personal project (optimize cost)
- **Time sensitivity**: Not critical (learning project)

**Decision**: Claude Code exclusively

**Rationale**:
- 30K-line codebase fits comfortably in 200K context
- Focused task doesn't need 2M context
- Claude Code provides deep reasoning for architectural decisions
- Lower cost per session (personal budget)
- Faster iteration for development workflow

**Workflow**:
```
1. Load Foundation: CLAUDE.md, architecture.md (10K tokens)
2. Load Current: API routes, models relevant to endpoint (20K tokens)
3. Total context: 30K tokens (15% utilization)
4. Available: 170K tokens for implementation work
5. Implement endpoint with Claude Code
```

---

### Example 2: Medium Project Exploration (200K lines)

**Scenario**: Understanding unfamiliar Django project (200K lines)

**Analysis**:
- **Codebase size**: 200K lines → Borderline for Claude Code
- **Task type**: Exploration (learning unknown system)
- **Reasoning depth**: Surface understanding (not deep implementation yet)
- **Context budget**: Professional work (budget available)
- **Expertise level**: Novice (new to codebase)

**Decision**: Multi-phase (Gemini explore → Claude Code implement)

**Rationale**:
- 200K-line codebase challenging for Claude Code full scan
- Gemini's 2M context handles comprehensive exploration
- After understanding, Claude Code provides deep reasoning for implementation
- One-time exploration cost justified (professional work)
- Multi-phase optimizes for both understanding and implementation

**Workflow**:
```
Phase 1: Gemini Exploration (2 hours)
1. Load full Django project (200K lines)
2. Ask: "What's the overall architecture?"
3. Ask: "How does authentication work?"
4. Ask: "Where is the payment processing logic?"
5. Generate summary: Key components, patterns, relevant files (8K tokens)
6. Save summary as exploration-checkpoint.md

Phase 2: Claude Code Implementation (ongoing)
1. Load exploration-checkpoint.md (8K tokens)
2. Load Foundation: CLAUDE.md, architecture.md (10K tokens)
3. Load Current: Files for specific feature (30K tokens)
4. Total context: 48K tokens (24% utilization)
5. Implement features with deep reasoning (152K available)
```

---

### Example 3: Large Legacy System (800K lines)

**Scenario**: Migrating authentication in legacy system (800K lines)

**Analysis**:
- **Codebase size**: 800K lines → Exceeds Claude Code context
- **Task type**: Hybrid (exploration + implementation)
- **Reasoning depth**: Deep (security-critical, complex migration)
- **Context budget**: Enterprise project (cost acceptable)
- **Time sensitivity**: Moderate (planned migration, not urgent)

**Decision**: Multi-phase workflow (Gemini explore → Claude Code implement)

**Rationale**:
- 800K lines exceeds Claude Code's 200K context
- Gemini handles full system exploration
- Authentication migration requires deep reasoning (Claude Code strength)
- Multi-phase workflow leverages both tools' strengths

**Workflow**:
```
Phase 1: Gemini Exploration (1 day)
1. Load full legacy system (800K lines into 2M context)
2. Exploration questions:
   - "How is authentication currently implemented across all modules?"
   - "Which files contain authentication logic?"
   - "What are the dependencies for current auth system?"
   - "What would break if we change authentication?"
3. Generate comprehensive summary (15K tokens):
   - Current authentication architecture
   - All files touching authentication (list with explanations)
   - Dependencies and integration points
   - Migration risks and considerations
4. Save as auth-migration-analysis.md

Phase 2: Claude Code Implementation (2 weeks)
1. Load auth-migration-analysis.md (15K tokens)
2. Load Foundation: CLAUDE.md, architecture.md, decisions.md (15K tokens)
3. For each module being migrated:
   - Load Current: Module files (30K tokens)
   - Total context: 60K tokens (30% utilization)
   - Implement migration with deep reasoning (140K available)
   - Validate against security requirements
   - Create checkpoint for next module
4. Repeat for all modules

Result:
- Gemini provided comprehensive system understanding
- Claude Code provided deep security reasoning for implementation
- Best of both tools leveraged systematically
```

---

### Example 4: Time-Critical Bug Fix (100K lines)

**Scenario**: Production bug in 100K-line codebase, downtime expensive

**Analysis**:
- **Codebase size**: 100K lines → Claude Code manageable with selective loading
- **Task type**: Focused (fix specific bug)
- **Reasoning depth**: Moderate to deep (diagnose + fix)
- **Context budget**: Not primary concern (downtime costly)
- **Time sensitivity**: CRITICAL (production down)

**Decision**: Claude Code (fast iteration prioritized)

**Rationale**:
- Time-critical: Claude Code faster than Gemini
- Bug fix is focused: Don't need full 100K-line scan
- Selective loading: Load only relevant modules (30K tokens)
- Deep reasoning: Claude Code diagnoses root cause effectively
- Cost secondary to speed: Production downtime expensive

**Workflow**:
```
1. Identify bug location (from error logs, monitoring)
2. Load Foundation: CLAUDE.md (project patterns)
3. Load Current: Files related to bug (error-prone module + dependencies)
4. Total context: 40K tokens (20% utilization)
5. Available: 160K tokens for diagnosis + fix
6. Claude Code: Deep reasoning to diagnose root cause
7. Implement fix with validation
8. Deploy quickly

Time saved: Using Claude Code directly (no Gemini exploration phase)
Result: Bug fixed in 2 hours vs potential 4+ hours with multi-phase
```

---

### Example 5: Learning New Framework (Documentation)

**Scenario**: Learning React (not codebase, but large documentation corpus)

**Analysis**:
- **Corpus size**: React docs + tutorials + examples (large corpus)
- **Task type**: Learning (broad understanding)
- **Reasoning depth**: Surface to moderate (learning fundamentals)
- **Context budget**: Personal learning (optimize cost)
- **Time sensitivity**: Not critical (self-paced learning)

**Decision**: Either tool, prefer Claude Code for learning conversations

**Rationale**:
- Documentation is structured (not sprawling codebase)
- Claude Code handles React docs + conversation effectively
- Learning benefits from iterative questioning (Claude Code optimized)
- Cost-efficient for extended learning sessions
- Gemini overkill for documentation learning

**Workflow**:
```
1. Load React documentation selectively (as needed)
2. Ask Claude Code: "Explain React hooks with examples"
3. Iterate: "How does useEffect work?"
4. Iterate: "When should I use useContext?"
5. Practice: "Generate a component using these hooks"
6. Total context grows organically (conversation-driven)
7. Claude Code 200K context sufficient for learning dialogue
```

---

## Decision Matrix (Quick Reference)

| Codebase Size | Task Type | Recommended Tool | Workflow |
|--------------|-----------|------------------|----------|
| < 50K | Any | Claude Code | Single-phase (Claude) |
| 50K-100K | Focused | Claude Code | Single-phase (Claude) |
| 50K-100K | Exploration | Claude Code or Gemini | Single or multi-phase |
| 100K-500K | Focused | Claude Code | Single-phase (selective loading) |
| 100K-500K | Exploration | Gemini → Claude | Multi-phase |
| > 500K | Any | Gemini → Claude | Multi-phase (required) |

**Override conditions**:
- **Deep reasoning needed** → Claude Code (regardless of size, with selective loading)
- **Time-critical** → Claude Code (faster iteration)
- **Cost-sensitive + large codebase** → Multi-phase with minimal Gemini use

---

## Output Format

When recommending tool selection, provide:

### Tool Recommendation Template
```markdown
## Tool Selection for [Task Description]

**Analysis**:
- **Codebase size**: [X lines]
- **Task type**: [Exploration / Focused / Hybrid]
- **Reasoning depth**: [Surface / Moderate / Deep]
- **Context budget**: [Tight / Balanced / Liberal]
- **Time sensitivity**: [Critical / Moderate / Not critical]
- **Expertise level**: [Novice / Intermediate / Expert]

**Recommendation**: [Claude Code / Gemini CLI / Multi-phase]

**Rationale**:
- [Reason 1 based on analysis]
- [Reason 2 based on analysis]
- [Reason 3 based on tool capabilities]

**Workflow**:
[Single-phase workflow OR Multi-phase workflow with Phase 1 and Phase 2]

**Expected outcome**: [What this approach achieves]
```

---

## Tips for Success

1. **Measure codebase size**: Use `cloc` to count lines accurately
2. **Start with question framework**: Answer all 6 questions before deciding
3. **Default to Claude Code**: For most tasks (<100K lines), Claude Code sufficient
4. **Use Gemini strategically**: Exploration phase for large codebases, not routine work
5. **Multi-phase for large projects**: Gemini (learn) → Claude Code (implement) pattern
6. **Consider cost**: Gemini sessions more expensive (larger context), use judiciously
7. **Time-critical favors Claude Code**: Faster iteration, optimized for development
8. **Document tool choices**: Record in decisions.md (why this tool for this task)
9. **Iterate framework**: As tools evolve, update capability matrix
10. **Validate assumptions**: If tool choice feels wrong, re-analyze with framework

---

**Ready to select the right tool?** Provide:
- Codebase size (lines of code)
- Task description (what needs to be done)
- Current challenges (context limits, time pressure, cost concerns)
- Expertise level (familiar with codebase or new)

Or describe a scenario and I'll apply the framework to recommend tool selection with detailed workflow!
