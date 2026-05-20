---
name: workflow-debate
description: Structured adversarial debate between AI councillors using Agent Teams to evaluate ideas, plans, or decisions. ALWAYS use when the user says "council", "debate this", "evaluate this idea", "challenge my plan", "stress-test", "devil's advocate", "multiple perspectives", "évaluer cette idée", "débattre", "challenger mon plan", "tester cette décision", or when the user wants rigorous multi-perspective analysis of a proposal, architecture decision, or strategic choice. Each councillor (visionary, critic, pragmatist, innovator, ethicist, domain expert) represents a distinct perspective and they challenge each other through cross-examination and peer exchange, producing a nuanced verdict (PROCEED / PROCEED WITH CONDITIONS / RECONSIDER / DO NOT PROCEED). Do NOT use for divergent brainstorming or idea generation — use workflow-brainstorm instead.
argument-hint: "[-r N] [-c N] [-s] [-e] [-f focus] <idea or plan to evaluate>"
---

<objective>
Orchestrate a structured adversarial debate (council) between multiple AI councillors, each representing a distinct perspective, to rigorously evaluate an idea, plan, or decision. Unlike brainstorming (divergent exploration), this skill uses structured adversarialism where agents actively challenge each other's positions through cross-examination and direct peer messaging.

Research backing: MIT studies show multi-perspective AI deliberation improves decision accuracy by 7-45%. The AI Council Framework and Debate-Based Consensus patterns demonstrate that structured disagreement surfaces blind spots that single-perspective analysis misses.
</objective>

<prerequisites>
For standard mode (Agent Teams): requires `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` in settings.json env.
Verify: check `~/.claude/settings.json` for this variable before proceeding.

Economy mode (`-e`): no prerequisites, uses sequential subagents instead of Agent Teams.
</prerequisites>

<quick_start>

**Minimal council (3 steps):**

```
1. /council Should we migrate our monolith to microservices?
2. Councillors debate across 2 rounds (default)
3. Receive structured verdict: PROCEED / PROCEED WITH CONDITIONS / RECONSIDER / DO NOT PROCEED
```

**With options:**
```
/council -c 5 -r 3 -s -f security Our plan to store PII in a third-party service
```

</quick_start>

<parameters>

**Flags:**

| Flag | Default | Description |
|------|---------|-------------|
| `-r N` | 2 | Number of debate rounds (1-4) |
| `-c N` | 4 | Number of councillors (3-6) |
| `-s` | false | Save transcript to `.claude/output/council/` |
| `-e` | false | Economy mode: sequential subagents instead of Agent Teams |
| `-f X` | none | Focus domain: technical, business, UX, security, ethics, custom |

**Councillor assignment by `-c N`:**

| Count | Councillors |
|-------|-------------|
| 3 | visionary, critic, pragmatist |
| 4 | + innovator (default) |
| 5 | + ethicist |
| 6 | + domain-expert (requires `-f`) |

**Parse at start:**
1. Check for `-r N` → set `{rounds}` (default 2, clamp 1-4)
2. Check for `-c N` → set `{councillor_count}` (default 4, clamp 3-6)
3. Check for `-s` → set `{save_mode}` = true
4. Check for `-e` → set `{economy_mode}` = true
5. Check for `-f X` → set `{focus}` = X
6. Validate: if `-c 6` without `-f` → warn and reduce to 5
7. Validate: if `-e` and Agent Teams env var set → note economy override
8. Remove all flags from input → store as `{topic}`

</parameters>

<state_variables>
Capture at start and persist throughout all steps:

- `{topic}` - The idea/plan to evaluate (flags removed)
- `{rounds}` - Number of debate rounds (1-4, default 2)
- `{councillor_count}` - Number of councillors (3-6, default 4)
- `{save_mode}` - true if `-s` flag passed
- `{economy_mode}` - true if `-e` flag passed
- `{focus}` - Domain focus if `-f` passed (technical/business/UX/security/ethics/custom)
- `{councillors}` - List of active councillor roles
- `{team_name}` - Team name (if Agent Teams mode)
- `{output_dir}` - Path to output directory (if save_mode)
- `{opening_statements}` - Collected opening positions from step-02
- `{debate_log}` - Accumulated debate exchanges from step-03
- `{position_evolution}` - How each councillor's position changed across rounds
</state_variables>

<roles>
For detailed councillor role descriptions, prompts, and protocols, see [references/roles.md](references/roles.md).

**Summary:**

| Role | Perspective | Agent Type |
|------|-------------|------------|
| **Moderator** | Neutral orchestrator, synthesizer | Team lead (you) |
| **Visionary** | Potential, opportunities, best-case scenarios | `Plan` (read-only) |
| **Critic** | Flaws, risks, failure modes, worst-case | `Plan` (read-only) |
| **Pragmatist** | Feasibility, constraints, execution reality | `Plan` (read-only) |
| **Innovator** | Alternatives, creative reframings | `Plan` (read-only) |
| **Ethicist** | Human impact, moral implications, stakeholders | `Plan` (read-only, 5th) |
| **Domain Expert** | Specialized expertise per `-f` focus | `Plan` (read-only, 6th) |

</roles>

<workflow>

### Phase 1: Setup (step-01)
1. Parse flags and validate configuration
2. Determine councillor roster based on `-c N`
3. Create team (Agent Teams) or prepare sequential execution (economy)
4. Spawn all councillors in parallel

### Phase 2: Opening Statements (step-02)
5. Each councillor independently analyzes the topic from their perspective
6. No cross-contamination — councillors don't see each other's positions yet
7. Moderator collects all opening statements

### Phase 3: Debate Rounds (step-03)
8. Share all positions with every councillor
9. Each councillor must challenge 2+ specific points from others
10. **Peer exchange**: councillors message each other directly via SendMessage
11. Moderator injects anti-groupthink questions between rounds
12. Track position evolution across rounds
13. Repeat for `{rounds}` rounds

### Phase 4: Verdict (step-04)
14. Synthesize consensus and dissensus points
15. Build risk assessment matrix
16. Produce structured verdict with confidence level
17. Present strongest counter-argument (steelmanned)
18. Save transcript (if `-s`) and cleanup team

</workflow>

<step_files>
Each step is a separate file for progressive context loading:

- `steps/step-01-setup.md` - Parse flags, create team, spawn councillors
- `steps/step-02-opening.md` - Independent opening statements (no cross-contamination)
- `steps/step-03-debate.md` - Cross-examination rounds + peer exchange
- `steps/step-04-verdict.md` - Synthesis, verdict, cleanup
</step_files>

<entry_point>
<step_0 name="Initialize">

**FIRST ACTION - Parse flags:**

1. Check for `-r N` → set `{rounds}` (default 2, validate 1-4)
2. Check for `-c N` → set `{councillor_count}` (default 4, validate 3-6)
3. Check for `-s` → set `{save_mode}` = true
4. Check for `-e` → set `{economy_mode}` = true
5. Check for `-f X` → set `{focus}` = X
6. Validate flag combinations (see parameters section)
7. Remove flags from input → store as `{topic}`

**THEN:** Load `steps/step-01-setup.md` to begin council setup.
</step_0>
</entry_point>

<execution_rules>

- **Load one step at a time** - Only load the current step file
- **Persist state variables** across all steps
- **Follow next_step directive** at end of each step
- **You are the Moderator** - Orchestrate, don't argue. Stay neutral.
- **Economy mode** - Use sequential Task calls with subagent_type `Plan` instead of Agent Teams
- **Peer exchange is the differentiator** - In standard mode, councillors MUST message each other directly
- **Anti-groupthink** - If positions converge too quickly, inject challenging questions
- **Steelman, don't strawman** - Present the strongest version of opposing arguments
- **Read-only councillors** - Councillors analyze and argue, they NEVER modify files
- **Always cleanup** - Shutdown all councillors + TeamDelete when done

</execution_rules>

<success_criteria>

- All councillors produced opening statements independently
- At least `{rounds}` rounds of cross-examination completed
- Peer exchange occurred (councillors challenged each other directly)
- Position evolution tracked across rounds
- Structured verdict produced with confidence level
- Consensus AND dissensus points identified
- Risk assessment matrix included
- Strongest counter-argument steelmanned
- Team cleaned up properly (shutdown + delete)
- Transcript saved (if `-s` flag)

</success_criteria>
