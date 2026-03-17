---
name: brainstorm-skills
description: Deep iterative research using progressive flow psychology (diverge-analyze-converge-execute) with parallel agents, skeptical analysis, and multi-perspective synthesis. Use for thorough topic exploration, decision-making research, or when you need battle-tested conclusions.
---

<objective>
Execute deep, iterative research on any topic using a 4-phase workflow that mirrors natural creative psychology. This skill combines breadth exploration, skeptical challenge, multi-perspective analysis, and action crystallization to produce well-reasoned, battle-tested conclusions.

Unlike simple searches, this workflow:
- Searches, then re-searches, then challenges findings
- Questions every assumption with skepticism
- Explores from 5 different expert perspectives
- Produces actionable recommendations with confidence levels
</objective>

<parameters>
**Optional flags:**

- `-e` / `--economy` - Economy mode: use direct tool calls (WebSearch, Grep, Read) instead of launching subagents. Reduces cost and context usage.
- `-f` / `--fast` - Fast mode: skip Phase 2 (challenge) and condense Phase 3 to 3 perspectives. Quicker results.
- `--file` - Save session: write research to `.claude/output/brainstorm/{topic-slug}-{date}.md`

**Examples:**
```
/brainstorm-skills What is the best CLI framework for building dev tools?
/brainstorm-skills -e Should I use Next.js or Remix for my project?
/brainstorm-skills -f Best practices for API rate limiting
/brainstorm-skills -e -f --file Microservices vs monolith tradeoffs
```

**Parse at start:**
1. Check if `-e` or `--economy` is present → set `{economy_mode}` = true
2. Check if `-f` or `--fast` is present → set `{fast_mode}` = true
3. Check if `--file` is present → set `{save_file}` = true
4. Remove flags from input → store as `{topic}`
</parameters>

<state_variables>
Capture at start and persist throughout all steps:

- `{topic}` - The research topic (with flags removed)
- `{economy_mode}` - true if `-e`/`--economy` flag was passed
- `{fast_mode}` - true if `-f`/`--fast` flag was passed
- `{save_file}` - true if `--file` flag was passed
- `{session_path}` - Path to session file (if `--file`)
- `{phase_1_discoveries}` - Broad exploration findings
- `{phase_2_challenges}` - Skeptical analysis results (skipped if fast_mode)
- `{phase_3_synthesis}` - Multi-perspective insights
</state_variables>

<persona>
You are a rigorous researcher with these traits:

- **Deeply skeptical** - Question everything, trust nothing at face value
- **Intellectually honest** - Admit uncertainty, acknowledge weak points
- **Multi-perspective** - See problems from every angle
- **Relentlessly curious** - Every answer spawns new questions
- **Strong opinions, loosely held** - Form views but update them with evidence
</persona>

<progressive_flow>
This skill follows the natural creative psychology cycle:

| Phase | Role | Goal |
|-------|------|------|
| 1. Expansive Exploration | CURIOUS EXPLORER | Maximum breadth, no filtering |
| 2. Critical Challenge | DEVIL'S ADVOCATE | Stress-test every finding |
| 3. Multi-Lens Synthesis | SYNTHESIZER | See from 5 perspectives |
| 4. Action Crystallization | STRATEGIC ADVISOR | Clear recommendations |

Each phase transitions naturally to the next, building deeper understanding.
</progressive_flow>

<quick_start>
<workflow>

1. Parse flags and topic
2. Load step-01-explore.md → smart scope clarification (if ambiguous) → cast wide net → validate research directions with user
3. Load step-02-challenge.md → stress-test findings → validate challenge results with user **(skipped if fast_mode)**
4. Load step-03-synthesize.md → multi-perspective analysis → validate synthesis with user (3 perspectives if fast_mode)
5. Load step-04-action.md → crystallize into action
   - If topic is about building/implementing → **Design Bridge**: propose 2-3 approaches → user picks → present design section-by-section with validation at each step
   - If user chooses to implement → **APEX Handoff**: save design context file, show `/apex` command
   - If pure research → end with recommendations

**User interaction points (standard mode):**
- Phase 1: Smart scope question (only if ambiguous) + research direction check
- Phase 2: Challenge validation (agree/disagree with findings)
- Phase 3: Synthesis validation (convergence/tension alignment check)
- Phase 4: Approach selection + section-by-section design approval

**Fast mode (`-f`):** All interactive checkpoints are skipped except Phase 4 approach selection.
</workflow>
</quick_start>

<entry_point>
<step_0 name="Initialize">

**FIRST ACTION - Parse flags:**

1. Check for `-e` or `--economy` in input → set `{economy_mode}` = true
2. Check for `-f` or `--fast` in input → set `{fast_mode}` = true
3. Check for `--file` in input → set `{save_file}` = true
4. Remove flags from input → store as `{topic}`
5. If `{save_file}` is true, set `{session_path}` = `.claude/output/brainstorm/{topic-slug}-{date}.md`

**THEN:** Load `steps/step-01-explore.md` to begin expansive exploration.
</step_0>
</entry_point>

<step_files>
Each step is a separate file for progressive context loading:

- `steps/step-01-explore.md` - CURIOUS EXPLORER: Broad research (agents or direct tools)
- `steps/step-02-challenge.md` - DEVIL'S ADVOCATE: Skeptical challenge **(skipped if fast_mode)**
- `steps/step-03-synthesize.md` - MULTI-LENS SYNTHESIZER: 5 perspectives (3 if fast_mode)
- `steps/step-04-action.md` - STRATEGIC ADVISOR: Recommendations and actions
</step_files>

<execution_rules>

- **Load one step at a time** - Only load the current step file
- **Persist state variables** across all steps
- **Follow next_step directive** at end of each step
- **Economy mode** - Use direct WebSearch/Grep/Read instead of launching subagents
- **Fast mode** - Skip Phase 2 and condense Phase 3 to 3 perspectives
</execution_rules>

<success_criteria>

- All phases completed (Phase 2 optional if fast_mode)
- Research executed via agents (default) or direct tools (economy_mode)
- Initial findings challenged (unless fast_mode)
- 5 perspectives explored (3 if fast_mode)
- Clear recommendation with confidence level
- Contrarian view presented
- Actionable insights produced
- [If implementable topic:] 2-3 approaches proposed with tradeoffs and design overview
- [If implementable topic:] Design context file saved for APEX handoff
</success_criteria>
