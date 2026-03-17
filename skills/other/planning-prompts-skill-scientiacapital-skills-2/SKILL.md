---
name: "planning-prompts"
description: "Comprehensive skill for project planning and prompt engineering. Covers hierarchical plans (briefs, roadmaps, phases), Claude-to-Claude meta-prompts, and multi-stage workflows. Use when: planning, prompt creation, agentic pipeline work, project roadmap, meta-prompts, research to implement workflow."
---

<objective>
Enable effective project planning and Claude-to-Claude meta-prompting for solo developers. Creates executable plans (PLAN.md files that ARE prompts), hierarchical planning structures (Brief → Roadmap → Phase), and multi-stage research-plan-implement workflows.
</objective>

<quick_start>
**Start a new project:**
```bash
# Claude creates planning structure
mkdir -p .planning/phases
# Creates: BRIEF.md, ROADMAP.md, phase plans
```

**Invoke via routing:**
- "brief" / "new project" → Create BRIEF.md
- "roadmap" / "phases" → Create ROADMAP.md
- "plan phase" / "next phase" → Create phase PLAN.md
- "meta-prompt" / "research then plan" → Create prompt chain

Plans ARE prompts - PLAN.md is directly executable by Claude.
</quick_start>

<essential_principles>

<principle name="solo_developer_plus_claude">
You are planning for ONE person (the user) and ONE implementer (Claude).
No teams. No stakeholders. No ceremonies. No coordination overhead.
The user is the visionary/product owner. Claude is the builder.
</principle>

<principle name="plans_are_prompts">
PLAN.md is not a document that gets transformed into a prompt.
PLAN.md IS the prompt. It contains:
- Objective (what and why)
- Context (@file references)
- Tasks (type, files, action, verify, done, checkpoints)
- Verification (overall checks)
- Success criteria (measurable)
- Output (SUMMARY.md specification)

When planning a phase, you are writing the prompt that will execute it.
</principle>

<principle name="claude_to_claude_optimization">
Outputs are structured for Claude consumption, not humans:
- Heavy XML structure for parsing
- Metadata blocks (confidence, dependencies, open_questions, assumptions)
- Explicit next steps
- Code examples with context
- Every execution produces SUMMARY.md for quick human scanning
</principle>

<principle name="scope_control">
Plans must complete within ~50% of context usage to maintain consistent quality.

**The quality degradation curve:**
- 0-30% context: Peak quality (comprehensive, thorough, no anxiety)
- 30-50% context: Good quality (engaged, manageable pressure)
- 50-70% context: Degrading quality (efficiency mode, compression)
- 70%+ context: Poor quality (self-lobotomization, rushed work)

**The 2-3 Task Rule:** Each plan should contain 2-3 tasks maximum.

Examples:
- `01-01-PLAN.md` - Phase 1, Plan 1 (2-3 tasks: database schema only)
- `01-02-PLAN.md` - Phase 1, Plan 2 (2-3 tasks: database client setup)
- `01-03-PLAN.md` - Phase 1, Plan 3 (2-3 tasks: API routes)

See: reference/plans.md (scope estimation section)
</principle>

<principle name="human_checkpoints">
Claude automates everything that has a CLI or API. Checkpoints are for verification and decisions, not manual work.

**Checkpoint types:**
- `checkpoint:human-verify` - Human confirms Claude's automated work (visual checks, UI verification)
- `checkpoint:decision` - Human makes implementation choice (auth provider, architecture)

**Rarely needed:** `checkpoint:human-action` - Only for actions with no CLI/API (email verification links, account approvals requiring web login with 2FA)

See: reference/plans.md (checkpoints section)
</principle>

<principle name="deviation_rules">
Plans are guides, not straitjackets. During execution, deviations handled automatically:

1. **Auto-fix bugs** - Broken behavior -> fix immediately, document in Summary
2. **Auto-add missing critical** - Security/correctness gaps -> add immediately, document
3. **Auto-fix blockers** - Can't proceed -> fix immediately, document
4. **Ask about architectural** - Major structural changes -> stop and ask user
5. **Log enhancements** - Nice-to-haves -> auto-log to ISSUES.md, continue
</principle>

<principle name="ship_fast_iterate_fast">
No enterprise process. No approval gates. No multi-week timelines.
Plan -> Execute -> Ship -> Learn -> Repeat.

Milestones mark shipped versions: v1.0 -> v1.1 -> v2.0
</principle>

<principle name="anti_enterprise_patterns">
NEVER include in plans:
- Team structures, roles, RACI matrices
- Stakeholder management, alignment meetings
- Sprint ceremonies, standups, retros
- Multi-week estimates, resource allocation
- Change management, governance processes
- Documentation for documentation's sake

If it sounds like corporate PM theater, delete it.
</principle>

</essential_principles>

<context_scan>
**Run on every invocation** to understand current state:

```bash
# Check for planning structure
ls -la .planning/ 2>/dev/null
ls -la .prompts/ 2>/dev/null

# Find any continue-here files
find . -name ".continue-here*.md" -type f 2>/dev/null

# Check for existing artifacts
[ -f .planning/BRIEF.md ] && echo "BRIEF: exists"
[ -f .planning/ROADMAP.md ] && echo "ROADMAP: exists"
```

**Present findings before intake question.**
</context_scan>

<intake>
Based on scan results, present context-aware options:

**If planning structure exists:**
```
Project: [from BRIEF or directory]
Brief: [exists/missing]
Roadmap: [X phases defined]
Current: [phase status]

What would you like to do?
1. Plan next phase
2. Execute current phase
3. Create handoff (stopping for now)
4. View/update roadmap
5. Create a meta-prompt (for Claude-to-Claude pipeline)
6. Something else
```

**If prompts structure exists:**
```
Found .prompts/ directory with [N] prompt folders.
Latest: {most recent folder}

What would you like to do?
1. Create new prompt (Research/Plan/Do/Refine)
2. Run existing prompt
3. View prompt chain
4. Something else
```

**If no structure found:**
```
No planning or prompt structure found.

What would you like to do?
1. Start new project (create brief + roadmap)
2. Create a meta-prompt chain (research -> plan -> implement)
3. Jump straight to phase planning
4. Get guidance on approach
```

**Wait for response before proceeding.**
</intake>

<routing>
| Intent | Go to |
|--------|-------|
| "brief", "new project", "start project" | reference/plans.md (create-brief section) |
| "roadmap", "phases", "structure" | reference/plans.md (create-roadmap section) |
| "phase", "plan phase", "next phase" | reference/plans.md (plan-phase section) |
| "meta-prompt", "prompt chain", "research then plan" | reference/meta-prompts.md |
| "research prompt", "gather info" | reference/meta-prompts.md (research section) |
| "plan prompt", "create approach" | reference/meta-prompts.md (plan section) |
| "do prompt", "implement", "execute" | reference/meta-prompts.md (do section) |
| "refine", "improve", "iterate" | reference/meta-prompts.md (refine section) |
| "handoff", "pack up", "stopping" | reference/plans.md (handoff section) |
| "resume", "continue" | reference/plans.md (resume section) |
| "guidance", "help" | Show this menu again with explanations |

**After reading the reference, follow it exactly.**
</routing>

<hierarchies>

<project_planning_hierarchy>
The project planning hierarchy (each level builds on previous):

```
BRIEF.md          -> Human vision (you read this)
    |
ROADMAP.md        -> Phase structure (overview)
    |
RESEARCH.md       -> Research prompt (optional, for unknowns)
    |
FINDINGS.md       -> Research output (if research done)
    |
PLAN.md           -> THE PROMPT (Claude executes this)
    |
SUMMARY.md        -> Outcome (existence = phase complete)
```

**Structure:**
```
.planning/
├── BRIEF.md                    # Human vision
├── ROADMAP.md                  # Phase structure + tracking
└── phases/
    ├── 01-foundation/
    │   ├── 01-01-PLAN.md       # Plan 1: Database setup
    │   ├── 01-01-SUMMARY.md    # Outcome (exists = done)
    │   ├── 01-02-PLAN.md       # Plan 2: API routes
    │   └── 01-02-SUMMARY.md
    └── 02-auth/
        ├── 02-01-RESEARCH.md   # Research prompt (if needed)
        ├── 02-01-FINDINGS.md   # Research output
        └── 02-02-PLAN.md       # Implementation prompt
```
</project_planning_hierarchy>

<meta_prompt_hierarchy>
The meta-prompt hierarchy (for Claude-to-Claude pipelines):

```
.prompts/
├── 001-auth-research/
│   ├── completed/
│   │   └── 001-auth-research.md    # Prompt (archived after run)
│   ├── auth-research.md            # Full output (XML for Claude)
│   └── SUMMARY.md                  # Executive summary (markdown for human)
├── 002-auth-plan/
│   ├── completed/
│   │   └── 002-auth-plan.md
│   ├── auth-plan.md
│   └── SUMMARY.md
├── 003-auth-implement/
│   ├── completed/
│   │   └── 003-auth-implement.md
│   └── SUMMARY.md                  # Do prompts create code elsewhere
```

**Purpose types:**
- **Research** - Gather information that planning prompt consumes
- **Plan** - Create approach/roadmap that implementation consumes
- **Do** - Execute a task, produce an artifact
- **Refine** - Improve an existing research or plan output
</meta_prompt_hierarchy>

</hierarchies>

<workflow_patterns>

<research_plan_implement>
The classic three-stage workflow:

1. **Research Prompt** -> Gathers information, produces structured findings
2. **Plan Prompt** -> References research, creates phased approach
3. **Do Prompt** -> References plan, implements each phase

Each stage:
- Produces output for next stage to consume
- Creates SUMMARY.md for human scanning
- Archives prompt after completion
- Captures metadata (confidence, dependencies, open questions)

**Chain detection:** When creating prompts, scan for existing research/plan files to reference.
</research_plan_implement>

<parallel_research>
For topics with multiple independent research areas:

```
Layer 1 (parallel): 001-api-research, 002-db-research, 003-ui-research
Layer 2 (depends on all): 004-architecture-plan
Layer 3 (depends on 004): 005-implement
```

**Execution:** Parallel within layers, sequential between layers.
</parallel_research>

<iterative_refinement>
When initial research/plan needs improvement:

```
001-auth-research        -> Initial research
002-auth-research-refine -> Deeper dive on specific finding
003-auth-plan            -> Plan based on refined research
```

Refine prompts preserve version history and track changes.
</iterative_refinement>

</workflow_patterns>

<output_requirements>

<summary_md>
Every execution produces SUMMARY.md:

```markdown
# {Topic} {Purpose} Summary

**{Substantive one-liner describing outcome}**

## Version
{v1 or "v2 (refined from v1)"}

## Key Findings
- {Most important finding or action}
- {Second key item}
- {Third key item}

## Files Created
{Only for Do prompts}
- `path/to/file.ts` - Description

## Decisions Needed
{Specific actionable decisions, or "None"}

## Blockers
{External impediments, or "None"}

## Next Step
{Concrete forward action}

---
*Confidence: {High|Medium|Low}*
*Full output: {filename.md}*
```

**One-liner must be substantive:**
- Good: "JWT with jose library and httpOnly cookies recommended"
- Bad: "Research completed"
</summary_md>

<metadata_block>
For research and plan outputs, include:

```xml
<metadata>
  <confidence level="{high|medium|low}">
    {Why this confidence level}
  </confidence>
  <dependencies>
    {What's needed to proceed}
  </dependencies>
  <open_questions>
    {What remains uncertain}
  </open_questions>
  <assumptions>
    {What was assumed}
  </assumptions>
</metadata>
```
</metadata_block>

</output_requirements>

<reference_index>
All in `reference/`:

| Reference | Contents |
|-----------|----------|
| plans.md | Project plans: briefs, roadmaps, phases, checkpoints, scope estimation, handoffs |
| meta-prompts.md | Claude-to-Claude pipelines: research/plan/do/refine patterns, execution engine |
</reference_index>

<success_criteria>
Skill succeeds when:
- Context scan runs before intake
- Appropriate workflow selected based on intent
- Plans ARE executable prompts (not separate)
- Hierarchy is maintained (brief -> roadmap -> phase)
- Meta-prompts include metadata and SUMMARY.md
- Chain dependencies detected and honored
- Quality controls prevent research gaps
- Handoffs preserve full context for resumption
- Context limits respected (auto-handoff at 10%)
- All work documented with deviations noted
</success_criteria>
