---
name: create-plans
description: Create hierarchical project plans optimized for solo agentic development. Use when planning projects, phases, or tasks that Claude will execute. Produces Claude-executable plans with verification criteria, not enterprise documentation. Handles briefs, roadmaps, phase plans, and context handoffs.
---

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

<principle name="scope_control">
Plans must complete within ~50% of context usage to maintain consistent quality.

**The quality degradation curve:**
- 0-30% context: Peak quality (comprehensive, thorough, no anxiety)
- 30-50% context: Good quality (engaged, manageable pressure)
- 50-70% context: Degrading quality (efficiency mode, compression)
- 70%+ context: Poor quality (self-lobotomization, rushed work)

**Critical insight:** Claude doesn't degrade at 80% - it degrades at ~40-50% when it sees context mounting and enters "completion mode." By 80%, quality has already crashed.

**Solution:** Aggressive atomicity - split phases into many small, focused plans.

Examples:
- `01-01-PLAN.md` - Phase 1, Plan 1 (2-3 tasks: database schema only)
- `01-02-PLAN.md` - Phase 1, Plan 2 (2-3 tasks: database client setup)
- `01-03-PLAN.md` - Phase 1, Plan 3 (2-3 tasks: API routes)
- `01-04-PLAN.md` - Phase 1, Plan 4 (2-3 tasks: UI components)

Each plan is independently executable, verifiable, and scoped to **2-3 tasks maximum**.

**Atomic task principle:** Better to have 10 small, high-quality plans than 3 large, degraded plans. Each commit should be surgical, focused, and maintainable.

**Autonomous execution:** Plans without checkpoints execute via subagent with fresh context - impossible to degrade.

See: references/scope-estimation.md
</principle>

<principle name="human_checkpoints">
**Claude automates everything that has a CLI or API.** Checkpoints are for verification and decisions, not manual work.

**Checkpoint types:**
- `checkpoint:human-verify` - Human confirms Claude's automated work (visual checks, UI verification)
- `checkpoint:decision` - Human makes implementation choice (auth provider, architecture)

**Rarely needed:** `checkpoint:human-action` - Only for actions with no CLI/API (email verification links, account approvals requiring web login with 2FA)

**Critical rule:** If Claude CAN do it via CLI/API/tool, Claude MUST do it. Never ask human to:
- Deploy to Vercel/Railway/Fly (use CLI)
- Create Stripe webhooks (use CLI/API)
- Run builds/tests (use Bash)
- Write .env files (use Write tool)
- Create database resources (use provider CLI)

**Protocol:** Claude automates work → reaches checkpoint:human-verify → presents what was done → waits for confirmation → resumes

See: references/checkpoints.md, references/cli-automation.md
</principle>

<principle name="deviation_rules">
Plans are guides, not straitjackets. Real development always involves discoveries.

**During execution, deviations are handled automatically via 5 embedded rules:**

1. **Auto-fix bugs** - Broken behavior → fix immediately, document in Summary
2. **Auto-add missing critical** - Security/correctness gaps → add immediately, document
3. **Auto-fix blockers** - Can't proceed → fix immediately, document
4. **Ask about architectural** - Major structural changes → stop and ask user
5. **Log enhancements** - Nice-to-haves → auto-log to ISSUES.md, continue

**No user intervention needed for Rules 1-3, 5.** Only Rule 4 (architectural) requires user decision.

**All deviations documented in Summary** with: what was found, what rule applied, what was done, commit hash.

**Result:** Flow never breaks. Bugs get fixed. Scope stays controlled. Complete transparency.

See: workflows/execute-phase.md (deviation_rules section)
</principle>

<principle name="ship_fast_iterate_fast">
No enterprise process. No approval gates. No multi-week timelines.
Plan → Execute → Ship → Learn → Repeat.

**Milestone-driven:** Ship v1.0 → mark milestone → plan v1.1 → ship → repeat.
Milestones mark shipped versions and enable continuous iteration.
</principle>

<principle name="milestone_boundaries">
Milestones mark shipped versions (v1.0, v1.1, v2.0).

**Purpose:**
- Historical record in MILESTONES.md (what shipped when)
- Greenfield → Brownfield transition marker
- Git tags for releases
- Clear completion rituals

**Default approach:** Extend existing roadmap with new phases.
- v1.0 ships (phases 1-4) → add phases 5-6 for v1.1
- Continuous phase numbering (01-99)
- Milestone groupings keep roadmap organized

**Archive ONLY for:** Separate codebases or complete rewrites (rare).

See: references/milestone-management.md
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

<principle name="context_awareness">
Monitor token usage via system warnings.

**At 25% remaining**: Mention context getting full
**At 15% remaining**: Pause, offer handoff
**At 10% remaining**: Auto-create handoff, stop

Never start large operations below 15% without user confirmation.
</principle>

<principle name="user_gates">
Never charge ahead at critical decision points. Use gates:
- **AskUserQuestion**: Structured choices (2-4 options)
- **Inline questions**: Simple confirmations
- **Decision gate loop**: "Ready, or ask more questions?"

Mandatory gates:
- Before writing PLAN.md (confirm breakdown)
- After low-confidence research
- On verification failures
- After phase completion with issues
- Before starting next phase with previous issues

See: references/user-gates.md
</principle>

<principle name="git_versioning">
All planning artifacts are version controlled. Commit outcomes, not process.

- Check for repo on invocation, offer to initialize
- Commit only at: initialization, phase completion, handoff
- Intermediate artifacts (PLAN.md, RESEARCH.md, FINDINGS.md) NOT committed separately
- Git log becomes project history

See: references/git-integration.md
</principle>

</essential_principles>

<context_scan>
**Run on every invocation** to understand current state:

```bash
# Check git status
git rev-parse --git-dir 2>/dev/null || echo "NO_GIT_REPO"

# Check for planning structure
ls -la .planning/ 2>/dev/null
ls -la .planning/phases/ 2>/dev/null

# Find any continue-here files
find . -name ".continue-here.md" -type f 2>/dev/null

# Check for existing artifacts
[ -f .planning/BRIEF.md ] && echo "BRIEF: exists"
[ -f .planning/ROADMAP.md ] && echo "ROADMAP: exists"
```

**If NO_GIT_REPO detected:**
Inline question: "No git repo found. Initialize one? (Recommended for version control)"
If yes: `git init`

**Present findings before intake question.**
</context_scan>

<domain_expertise>
**Domain expertise lives in `~/.claude/skills/expertise/`**

Before creating roadmap or phase plans, determine if domain expertise should be loaded.

<scan_domains>
```bash
ls ~/.claude/skills/expertise/ 2>/dev/null
```

This reveals available domain expertise (e.g., macos-apps, iphone-apps, unity-games, nextjs-ecommerce).

**If no domain skills found:** Proceed without domain expertise (graceful degradation). The skill works fine without domain-specific context.
</scan_domains>

<inference_rules>
If user's request contains domain keywords, INFER the domain:

| Keywords | Domain Skill |
|----------|--------------|
| "macOS", "Mac app", "menu bar", "AppKit", "SwiftUI desktop" | expertise/macos-apps |
| "iPhone", "iOS", "iPad", "mobile app", "SwiftUI mobile" | expertise/iphone-apps |
| "Unity", "game", "C#", "3D game", "2D game" | expertise/unity-games |
| "MIDI", "MIDI tool", "sequencer", "MIDI controller", "music app", "MIDI 2.0", "MPE", "SysEx" | expertise/midi |
| "Agent SDK", "Claude SDK", "agentic app" | expertise/with-agent-sdk |
| "Python automation", "workflow", "API integration", "webhooks", "Celery", "Airflow", "Prefect" | expertise/python-workflow-automation |
| "UI", "design", "frontend", "interface", "responsive", "visual design", "landing page", "website design", "Tailwind", "CSS", "web design" | expertise/ui-design |

If domain inferred, confirm:
```
Detected: [domain] project → expertise/[skill-name]
Load this expertise for planning? (Y / see other options / none)
```
</inference_rules>

<no_inference>
If no domain obvious from request, present options:

```
What type of project is this?

Available domain expertise:
1. macos-apps - Native macOS with Swift/SwiftUI
2. iphone-apps - Native iOS with Swift/SwiftUI
3. unity-games - Unity game development
4. swift-midi-apps - MIDI/audio apps
5. with-agent-sdk - Claude Agent SDK apps
6. ui-design - Stunning UI/UX design & frontend development
[... any others found in expertise/]

N. None - proceed without domain expertise
C. Create domain skill first

Select:
```
</no_inference>

<load_domain>
When domain selected, use intelligent loading:

**Step 1: Read domain SKILL.md**
```bash
cat ~/.claude/skills/expertise/[domain]/SKILL.md 2>/dev/null
```

This loads core principles and routing guidance (~5k tokens).

**Step 2: Determine what references are needed**

Domain SKILL.md should contain a `<references_index>` section that maps planning contexts to specific references.

Example:
```markdown
<references_index>
**For database/persistence phases:** references/core-data.md, references/swift-concurrency.md
**For UI/layout phases:** references/swiftui-layout.md, references/appleHIG.md
**For system integration:** references/appkit-integration.md
**Always useful:** references/swift-conventions.md
</references_index>
```

**Step 3: Load only relevant references**

Based on the phase being planned (from ROADMAP), load ONLY the references mentioned for that type of work.

```bash
# Example: Planning a database phase
cat ~/.claude/skills/expertise/macos-apps/references/core-data.md
cat ~/.claude/skills/expertise/macos-apps/references/swift-conventions.md
```

**Context efficiency:**
- SKILL.md only: ~5k tokens
- SKILL.md + selective references: ~8-12k tokens
- All references (old approach): ~20-27k tokens

Announce: "Loaded [domain] expertise ([X] references for [phase-type])."

**If domain skill not found:** Inform user and offer to proceed without domain expertise.

**If SKILL.md doesn't have references_index:** Fall back to loading all references with warning about context usage.
</load_domain>

<when_to_load>
Domain expertise should be loaded BEFORE:
- Creating roadmap (phases should be domain-appropriate)
- Planning phases (tasks must be domain-specific)

Domain expertise is NOT needed for:
- Creating brief (vision is domain-agnostic)
- Resuming from handoff (context already established)
- Transition between phases (just updating status)
</when_to_load>
</domain_expertise>

<intake>
Based on scan results, present context-aware options:

**If handoff found:**
```
Found handoff: .planning/phases/XX/.continue-here.md
[Summary of state from handoff]

1. Resume from handoff
2. Discard handoff, start fresh
3. Different action
```

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
5. Something else
```

**If no planning structure:**
```
No planning structure found.

What would you like to do?
1. Start new project (create brief)
2. Create roadmap from existing brief
3. Jump straight to phase planning
4. Get guidance on approach
```

**Wait for response before proceeding.**
</intake>

<routing>
| Response | Workflow |
|----------|----------|
| "brief", "new project", "start", 1 (no structure) | `workflows/create-brief.md` |
| "roadmap", "phases", 2 (no structure) | `workflows/create-roadmap.md` |
| "phase", "plan phase", "next phase", 1 (has structure) | `workflows/plan-phase.md` |
| "chunk", "next tasks", "what's next" | `workflows/plan-chunk.md` |
| "execute", "run", "do it", "build it", 2 (has structure) | **EXIT SKILL** → Use `/run-plan <path>` slash command |
| "research", "investigate", "unknowns" | `workflows/research-phase.md` |
| "handoff", "pack up", "stopping", 3 (has structure) | `workflows/handoff.md` |
| "resume", "continue", 1 (has handoff) | `workflows/resume.md` |
| "transition", "complete", "done", "next" | `workflows/transition.md` |
| "milestone", "ship", "v1.0", "release" | `workflows/complete-milestone.md` |
| "guidance", "help", 4 | `workflows/get-guidance.md` |

**Critical:** Plan execution should NOT invoke this skill. Use `/run-plan` for context efficiency (skill loads ~20k tokens, /run-plan loads ~5-7k).

**After reading the workflow, follow it exactly.**
</routing>

<hierarchy>
The planning hierarchy (each level builds on previous):

```
BRIEF.md          → Human vision (you read this)
    ↓
ROADMAP.md        → Phase structure (overview)
    ↓
RESEARCH.md       → Research prompt (optional, for unknowns)
    ↓
FINDINGS.md       → Research output (if research done)
    ↓
PLAN.md           → THE PROMPT (Claude executes this)
    ↓
SUMMARY.md        → Outcome (existence = phase complete)
```

**Rules:**
- Roadmap requires Brief (or prompts to create one)
- Phase plan requires Roadmap (knows phase scope)
- PLAN.md IS the execution prompt
- SUMMARY.md existence marks phase complete
- Each level can look UP for context
</hierarchy>

<output_structure>
All planning artifacts go in `.planning/`:

```
.planning/
├── BRIEF.md                    # Human vision
├── ROADMAP.md                  # Phase structure + tracking
└── phases/
    ├── 01-foundation/
    │   ├── 01-01-PLAN.md       # Plan 1: Database setup
    │   ├── 01-01-SUMMARY.md    # Outcome (exists = done)
    │   ├── 01-02-PLAN.md       # Plan 2: API routes
    │   ├── 01-02-SUMMARY.md
    │   ├── 01-03-PLAN.md       # Plan 3: UI components
    │   └── .continue-here-01-03.md  # Handoff (temporary, if needed)
    └── 02-auth/
        ├── 02-01-RESEARCH.md   # Research prompt (if needed)
        ├── 02-01-FINDINGS.md   # Research output
        ├── 02-02-PLAN.md       # Implementation prompt
        └── 02-02-SUMMARY.md
```

**Naming convention:**
- Plans: `{phase}-{plan}-PLAN.md` (e.g., 01-03-PLAN.md)
- Summaries: `{phase}-{plan}-SUMMARY.md` (e.g., 01-03-SUMMARY.md)
- Phase folders: `{phase}-{name}/` (e.g., 01-foundation/)

Files sort chronologically. Related artifacts (plan + summary) are adjacent.
</output_structure>

<reference_index>
All in `references/`:

**Structure:** directory-structure.md, hierarchy-rules.md
**Formats:** handoff-format.md, plan-format.md
**Patterns:** context-scanning.md, context-management.md
**Planning:** scope-estimation.md, checkpoints.md, milestone-management.md
**Process:** user-gates.md, git-integration.md, research-pitfalls.md
**Domain:** domain-expertise.md (guide for creating context-efficient domain skills)
</reference_index>

<templates_index>
All in `templates/`:

| Template | Purpose |
|----------|---------|
| brief.md | Project vision document with current state |
| roadmap.md | Phase structure with milestone groupings |
| phase-prompt.md | Executable phase prompt (PLAN.md) |
| research-prompt.md | Research prompt (RESEARCH.md) |
| summary.md | Phase outcome (SUMMARY.md) with deviations |
| milestone.md | Milestone entry for MILESTONES.md |
| issues.md | Deferred enhancements log (ISSUES.md) |
| continue-here.md | Context handoff format |
</templates_index>

<workflows_index>
All in `workflows/`:

| Workflow | Purpose |
|----------|---------|
| create-brief.md | Create project vision document |
| create-roadmap.md | Define phases from brief |
| plan-phase.md | Create executable phase prompt |
| execute-phase.md | Run phase prompt, create summary |
| research-phase.md | Create and run research prompt |
| plan-chunk.md | Plan immediate next tasks |
| transition.md | Mark phase complete, advance |
| complete-milestone.md | Mark shipped version, create milestone entry |
| handoff.md | Create context handoff for pausing |
| resume.md | Load handoff, restore context |
| get-guidance.md | Help decide planning approach |
</workflows_index>

<success_criteria>
Planning skill succeeds when:
- Context scan runs before intake
- Appropriate workflow selected based on state
- PLAN.md IS the executable prompt (not separate)
- Hierarchy is maintained (brief → roadmap → phase)
- Handoffs preserve full context for resumption
- Context limits are respected (auto-handoff at 10%)
- Deviations handled automatically per embedded rules
- All work (planned and discovered) fully documented
- Domain expertise loaded intelligently (SKILL.md + selective references, not all files)
- Plan execution uses /run-plan command (not skill invocation)
</success_criteria>
