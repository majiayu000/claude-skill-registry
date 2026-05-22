---
name: create-meta-prompts
description: "Generate meta-prompts for Claude-to-Claude pipelines and multi-stage workflows. Use when creating optimized prompts for complex workflows. Not for simple single-turn prompts or manual messaging."
---

##

Objective
Create prompts optimized for Claude-to-Claude communication in multi-stage workflows. Outputs are structured with XML and metadata for efficient parsing by subsequent prompts.
Every execution produces a `SUMMARY.md` for quick human scanning without reading full outputs.
Each prompt gets its own folder in `.claude/workspace/prompts/` with its output artifacts, enabling clear provenance and chain detection.

##

Quick Start

### Workflow

1. **Intake**: Determine purpose (Do/Plan/Research/Refine), gather requirements
2. **Chain detection**: Check for existing research/plan files to reference
3. **Generate**: Create prompt using purpose-specific patterns
4. **Save**: Create folder in `.claude/workspace/prompts/{number}-{topic}-{purpose}/`
5. **Present**: Show decision tree for running
6. **Execute**: Run prompt(s) with dependency-aware execution engine
7. **Summarize**: Create SUMMARY.md for human scanning

#### Folder Structure

```
.claude/workspace/prompts/
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
├── 004-auth-research-refine/
│   ├── completed/
│   │   └── 004-auth-research-refine.md
│   ├── archive/
│   │   └── auth-research-v1.md     # Previous version
│   └── SUMMARY.md
```

##

Context
Prompts directory: !`[ -d ./.claude/planning/prompts ] && echo "exists" || echo "missing"`
Existing research/plans: !`find ./.claude/planning/prompts -name "*-research.md" -o -name "*-plan.md" 2>/dev/null | head -10`
Next prompt number: !`ls -d ./.claude/workspace/prompts/*/ 2>/dev/null | wc -l | xargs -I {} expr {} + 1`

##

Automated Workflow

### 0. Intake Gate

#### Adaptive Requirements Gathering

##### Critical First Action

**BEFORE analyzing anything**, check if context was provided.
IF no context provided (skill invoked without description):
→ **IMMEDIATELY use AskUserQuestion** with:

- header: "Purpose"
- question: "What is the purpose of this prompt?"
- options:
  - "Do" - Execute a task, produce an artifact
  - "Plan" - Create an approach, roadmap, or strategy
  - "Research" - Gather information or understand something
  - "Refine" - Improve an existing research or plan output
    After selection, ask: "Describe what you want to accomplish" (they select "Other" to provide free text).
    IF context was provided:
    → Check if purpose is inferable from keywords:
- `implement`, `build`, `create`, `fix`, `add`, `refactor` → Do
- `plan`, `roadmap`, `approach`, `strategy`, `decide`, `phases` → Plan
- `research`, `understand`, `learn`, `gather`, `analyze`, `explore` → Research
- `refine`, `improve`, `deepen`, `expand`, `iterate`, `update` → Refine
  → If unclear, ask the Purpose question above as first contextual question
  → If clear, proceed to adaptive_analysis with inferred purpose

##### Adaptive Analysis

Extract and infer:

- **Purpose**: Do, Plan, Research, or Refine
- **Topic identifier**: Kebab-case identifier for file naming (e.g., `auth`, `stripe-payments`)
- **Complexity**: Simple vs complex (affects prompt depth)
- **Prompt structure**: Single vs multiple prompts
- **Target** (Refine only): Which existing output to improve
  If topic identifier not obvious, ask:
- header: "Topic"
- question: "What topic/feature is this for? (used for file naming)"
- Let user provide via "Other" option
- Enforce kebab-case (convert spaces/underscores to hyphens)
  For Refine purpose, also identify target output from `.claude/workspace/prompts/*/` to improve.

##### Chain Detection

Scan `.claude/workspace/prompts/*/` for existing `*-research.md` and `*-plan.md` files.
If found:

1. List them: "Found existing files: auth-research.md (in 001-auth-research/), stripe-plan.md (in 005-stripe-plan/)"
2. Use AskUserQuestion:
   - header: "Reference"
   - question: "Should this prompt reference any existing research or plans?"
   - options: List found files + "None"
   - multiSelect: true
     Match by topic keyword when possible (e.g., "auth plan" → suggest auth-research.md).

##### Contextual Questioning

Generate 2-4 questions using AskUserQuestion based on purpose and gaps.
Load questions from: [references/question-bank.md](references/question-bank.md)
Route by purpose:

- Do → artifact type, scope, approach
- Plan → plan purpose, format, constraints
- Research → depth, sources, output format
- Refine → target selection, feedback, preservation

##### Decision Gate

After receiving answers, present decision gate using AskUserQuestion:

- header: "Ready"
- question: "Ready to create the prompt?"
- options:
  - "Proceed" - Create the prompt with current context
  - "Ask more questions" - I have more details to clarify
  - "Let me add context" - I want to provide additional information
    Loop until "Proceed" selected.

##### Finalization

After "Proceed" selected, state confirmation:
"Creating a {purpose} prompt for: {topic}
Folder: .claude/workspace/prompts/{number}-{topic}-{purpose}/
References: {list any chained files}"
Then proceed to generation.

### 1. Generate

#### Generate Prompt

Load purpose-specific patterns:

- Do: [references/do-patterns.md](references/do-patterns.md)
- Plan: [references/plan-patterns.md](references/plan-patterns.md)
- Research: [references/research-patterns.md](references/research-patterns.md)
- Refine: [references/refine-patterns.md](references/refine-patterns.md)
  Load intelligence rules: [references/intelligence-rules.md](references/intelligence-rules.md)

#### Prompt Structure

All generated prompts include:

1. **Objective**: What to accomplish, why it matters
2. **Context**: Referenced files (@), dynamic context (!)
3. **Requirements**: Specific instructions for the task
4. **Output specification**: Where to save, what structure
5. **Metadata requirements**: For research/plan outputs, specify XML metadata structure
6. **SUMMARY.md requirement**: All prompts must create a SUMMARY.md file
7. **Success criteria**: How to know it worked
   For Research and Plan prompts, output must include:

- `<confidence>` - How confident in findings
- `<dependencies>` - What's needed to proceed
- `<open_questions>` - What remains uncertain
- `<assumptions>` - What was assumed
  All prompts must create `SUMMARY.md` with:
- **One-liner** - Substantive description of outcome
- **Version** - v1 or iteration info
- **Key Findings** - Actionable takeaways
- **Files Created** - (Do prompts only)
- **Decisions Needed** - What requires user input
- **Blockers** - External impediments
- **Next Step** - Concrete forward action

#### File Creation

1. Create folder: `.claude/workspace/prompts/{number}-{topic}-{purpose}/`
2. Create `completed/` subfolder
3. Write prompt to: `.claude/workspace/prompts/{number}-{topic}-{purpose}/{number}-{topic}-{purpose}.md`
4. Prompt instructs output to: `.claude/workspace/prompts/{number}-{topic}-{purpose}/{topic}-{purpose}.md`

### 2. Present

#### Present Decision Tree

After saving prompt(s), present inline (not AskUserQuestion):

#### Single Prompt Presentation

```
Prompt created: .claude/workspace/prompts/{number}-{topic}-{purpose}/{number}-{topic}-{purpose}.md
What's next?
1. Run prompt now
2. Review/edit prompt first
3. Save for later
4. Other
Choose (1-4): _
```

#### Multi-Prompt Presentation

```
Prompts created:
- .claude/workspace/prompts/001-auth-research/001-auth-research.md
- .claude/workspace/prompts/002-auth-plan/002-auth-plan.md
- .claude/workspace/prompts/003-auth-implement/003-auth-implement.md
Detected execution order: Sequential (002 references 001 output, 003 references 002 output)
What's next?
1. Run all prompts (sequential)
2. Review/edit prompts first
3. Save for later
4. Other
Choose (1-4): _
```

### 3. Execute

#### Execution Engine

#### Execution Modes

##### Single Prompt

Straightforward execution of one prompt.

1. Read prompt file contents
2. Spawn Task agent with subagent_type="general-purpose"
3. Include in task prompt:
   - The complete prompt contents
   - Output location: `.claude/workspace/prompts/{number}-{topic}-{purpose}/{topic}-{purpose}.md`
4. Wait for completion
5. Validate output (see validation section)
6. Archive prompt to `completed/` subfolder
7. Report results with next-step options

##### Sequential Execution

For chained prompts where each depends on previous output.

1. Build execution queue from dependency order
2. For each prompt in queue:
   a. Read prompt file
   b. Spawn Task agent
   c. Wait for completion
   d. Validate output
   e. If validation fails → stop, report failure, offer recovery options
   f. If success → archive prompt, continue to next
3. Report consolidated results

###### Progress Reporting

Show progress during execution:

```
Executing 1/3: 001-auth-research... ✓
Executing 2/3: 002-auth-plan... ✓
Executing 3/3: 003-auth-implement... (running)
```

##### Parallel Execution

For independent prompts with no dependencies.

1. Read all prompt files
2. **CRITICAL**: Spawn ALL Task agents in a SINGLE message
   - This is required for true parallel execution
   - Each task includes its output location
3. Wait for all to complete
4. Validate all outputs
5. Archive all prompts
6. Report consolidated results (successes and failures)

###### Failure Handling

Unlike sequential, parallel continues even if some fail:

- Collect all results
- Archive successful prompts
- Report failures with details
- Offer to retry failed prompts

##### Mixed Dependencies

For complex DAGs (e.g., two parallel research → one plan).

1. Analyze dependency graph from @ references
2. Group into execution layers:
   - Layer 1: No dependencies (run parallel)
   - Layer 2: Depends only on layer 1 (run after layer 1 completes)
   - Layer 3: Depends on layer 2, etc.
3. Execute each layer:
   - Parallel within layer
   - Sequential between layers
4. Stop if any dependency fails (downstream prompts can't run)

###### Example

```
Layer 1 (parallel): 001-api-research, 002-db-research
Layer 2 (after layer 1): 003-architecture-plan
Layer 3 (after layer 2): 004-implement
```

##### Dependency Detection

###### Automatic Detection

Scan prompt contents for @ references to determine dependencies:

1. Parse each prompt for `@.claude/workspace/prompts/{number}-{topic}/` patterns
2. Build dependency graph
3. Detect cycles (error if found)
4. Determine execution order

###### Inference Rules

If no explicit @ references found, infer from purpose:

- Research prompts: No dependencies (can parallel)
- Plan prompts: Depend on same-topic research
- Do prompts: Depend on same-topic plan
  Override with explicit references when present.

###### Missing Dependencies

If a prompt references output that doesn't exist:

1. Check if it's another prompt in this session (will be created)
2. Check if it exists in `.claude/workspace/prompts/*/` (already completed)
3. If truly missing:
   - Warn user: "002-auth-plan references auth-research.md which doesn't exist"
   - Offer: Create the missing research prompt first? / Continue anyway? / Cancel?

##### Validation

###### Output Validation

After each prompt completes, verify success:

1. **File exists**: Check output file was created
2. **Not empty**: File has content (> 100 chars)
3. **Metadata present** (for research/plan): Check for required XML tags
   - `<confidence>`
   - `<dependencies>`
   - `<open_questions>`
   - `<assumptions>`
4. **SUMMARY.md exists**: Check SUMMARY.md was created
5. **SUMMARY.md complete**: Has required sections (Key Findings, Decisions Needed, Blockers, Next Step)
6. **One-liner is substantive**: Not generic like "Research completed"

###### Validation Failure

If validation fails:

- Report what's missing
- Offer options:
  - Retry the prompt
  - Continue anyway (for non-critical issues)
  - Stop and investigate

###### Failure Handling

###### Sequential Failure

Stop the chain immediately:

```
✗ Failed at 2/3: 002-auth-plan
Completed:
- 001-auth-research ✓ (archived)
Failed:
- 002-auth-plan: Output file not created
Not started:
- 003-auth-implement
What's next?
1. Retry 002-auth-plan
2. View error details
3. Stop here (keep completed work)
4. Other
```

###### Parallel Failure

Continue others, report all results:

```
Parallel execution completed with errors:
✓ 001-api-research (archived)
✗ 002-db-research: Validation failed - missing <confidence> tag
✓ 003-ui-research (archived)
What's next?
1. Retry failed prompt (002)
2. View error details
3. Continue without 002
4. Other
```

##### Archiving

###### Archive Timing

- **Sequential**: Archive each prompt immediately after successful completion
  - Provides clear state if execution stops mid-chain
- **Parallel**: Archive all at end after collecting results
  - Keeps prompts available for potential retry

###### Archive Operation

Move prompt file to completed subfolder:

```bash
mv .claude/workspace/prompts/{number}-{topic}-{purpose}/{number}-{topic}-{purpose}.md \
   .claude/workspace/prompts/{number}-{topic}-{purpose}/completed/
```

Output file stays in place (not moved).

##### Result Presentation

###### Single Result

```
✓ Executed: 001-auth-research
✓ Created: .claude/workspace/prompts/001-auth-research/SUMMARY.md
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Auth Research Summary
**JWT with jose library and httpOnly cookies recommended**

##
Key Findings
• jose outperforms jsonwebtoken with better TypeScript support
• httpOnly cookies required (localStorage is XSS vulnerable)
• Refresh rotation is OWASP standard

##
Decisions Needed
None - ready for planning

##
Blockers
None

##
Next Step
Create auth-plan.md
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
What's next?
1. Create planning prompt (auth-plan)
2. View full research output
3. Done
4. Other
```

Display the actual SUMMARY.md content inline so user sees findings without opening files.

###### Chain Result

```
✓ Chain completed: auth workflow
Results:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
001-auth-research
**JWT with jose library and httpOnly cookies recommended**
Decisions: None • Blockers: None
002-auth-plan
**4-phase implementation: types → JWT core → refresh → tests**
Decisions: Approve 15-min token expiry • Blockers: None
003-auth-implement
**JWT middleware complete with 6 files created**
Decisions: Review before Phase 2 • Blockers: None
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
All prompts archived. Full summaries in .claude/workspace/prompts/*/SUMMARY.md
What's next?
1. Review implementation
2. Run tests
3. Create new prompt chain
4. Other
```

For chains, show condensed one-liner from each SUMMARY.md with decisions/blockers flagged.

##### Special Cases

###### Re-running Completed

If user wants to re-run an already-completed prompt:

1. Check if prompt is in `completed/` subfolder
2. Move it back to parent folder
3. Optionally backup existing output: `{output}.bak`
4. Execute normally

###### Output Conflicts

If output file already exists:

1. For re-runs: Backup existing → `{filename}.bak`
2. For new runs: Should not happen (unique numbering)
3. If conflict detected: Ask user - Overwrite? / Rename? / Cancel?

###### Commit Handling

After successful execution:

1. Do NOT auto-commit (user controls git workflow)
2. Mention what files were created/modified
3. User can commit when ready
   Exception: If user explicitly requests commit, stage and commit:

- Output files created
- Prompts archived
- Any implementation changes (for Do prompts)

###### Recursive Prompts

If a prompt's output includes instructions to create more prompts:

1. This is advanced usage - don't auto-detect
2. Present the output to user
3. User can invoke skill again to create follow-up prompts
4. Maintains user control over prompt creation

##

Reference Guides
**Prompt patterns by purpose:**

- [references/do-patterns.md](references/do-patterns.md) - Execution prompts + output structure
- [references/plan-patterns.md](references/plan-patterns.md) - Planning prompts + plan.md structure
- [references/research-patterns.md](references/research-patterns.md) - Research prompts + research.md structure
- [references/refine-patterns.md](references/refine-patterns.md) - Iteration prompts + versioning
  **Shared templates:**
- [references/summary-template.md](references/summary-template.md) - SUMMARY.md structure and field requirements
- [references/metadata-guidelines.md](references/metadata-guidelines.md) - Confidence, dependencies, open questions, assumptions
  **Supporting references:**
- [references/question-bank.md](references/question-bank.md) - Intake questions by purpose
- [references/intelligence-rules.md](references/intelligence-rules.md) - Extended thinking, parallel tools, depth decisions

##

Success Criteria
**Prompt Creation:**

- Intake gate completed with purpose and topic identified
- Chain detection performed, relevant files referenced
- Prompt generated with correct structure for purpose
- Folder created in `.claude/workspace/prompts/` with correct naming
- Output file location specified in prompt
- SUMMARY.md requirement included in prompt
- Metadata requirements included for Research/Plan outputs
- Quality controls included for Research outputs (verification checklist, QA, pre-submission)
- Streaming write instructions included for Research outputs
- Decision tree presented
  **Execution (if user chooses to run):**
- Dependencies correctly detected and ordered
- Prompts executed in correct order (sequential/parallel/mixed)
- Output validated after each completion
- SUMMARY.md created with all required sections
- One-liner is substantive (not generic)
- Failed prompts handled gracefully with recovery options
- Successful prompts archived to `completed/` subfolder
- SUMMARY.md displayed inline in results
- Results presented with decisions/blockers flagged
  **Research Quality (for Research prompts):**
- Verification checklist completed
- Quality report distinguishes verified from assumed claims
- Sources consulted listed with URLs
- Confidence levels assigned to findings
- Critical claims verified with official documentation

---

<critical_constraint>
MANDATORY: Create SUMMARY.md for every prompt execution
MANDATORY: Validate output file exists and has required sections before archiving
MANDATORY: Use proper XML metadata tags for research/plan outputs
MANDATORY: Present decision tree before executing prompts
MANDATORY: Handle validation failures gracefully with recovery options
No exceptions. Meta-prompts must maintain provenance and enable human scanning.
</critical_constraint>

---

## Genetic Code

This component carries essential Seed System principles for context: fork isolation:

<critical_constraint>
MANDATORY: All components MUST be self-contained (zero .claude/rules dependency)
MANDATORY: Achieve 80-95% autonomy (0-5 AskUserQuestion rounds per session)
MANDATORY: Description MUST use What-When-Not format in third person
MANDATORY: No component references another component by name in description
MANDATORY: Progressive disclosure - references/ for detailed content
MANDATORY: Use XML for control (mission_control, critical_constraint), Markdown for data
No exceptions. Portability invariant must be maintained.
</critical_constraint>

**Delta Standard**: Good Component = Expert Knowledge − What Claude Already Knows

**Recognition Questions**:

- "Would Claude know this without being told?" → Delete (zero delta)
- "Can this work standalone?" → Fix if no (non-self-sufficient)
- "Did I read the actual file, or just see it in grep?" → Verify before claiming

---
