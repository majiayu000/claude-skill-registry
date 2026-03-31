---
name: self-improve
description: "Extract lessons from the current session and route them to the appropriate knowledge layer (project AGENTS.md, auto memory, existing skills, or new skills). Use when the user asks to \"self-improve\", \"distill this session\", \"save learnings\", \"update CLAUDE.md with what we learned\", \"capture session insights\", \"remember this for next time\", \"extract lessons\", \"update skills from session\", or \"what did we learn\"."
---

# Self-Improve

Review the current conversation to extract durable lessons and route each one to the right knowledge layer.

## Step 1: Detect Context

Available destinations:

- **Project CLAUDE.md / AGENTS.md** — `.claude/CLAUDE.md` (may be a symlink to `../AGENTS.md` — resolve it)
- **Auto memory** — The project-specific memory directory at `~/.claude/projects/<project-hash>/memory/`. Read `MEMORY.md` there if it exists.
- **Skills** — Project skills at `skills/` or `.claude/skills/` (resolve symlinks)

Read the project CLAUDE.md/AGENTS.md and MEMORY.md. List all skill directories but do not read them yet — Step 2 needs to run first so you know what to look for.

### Turbo Skill Detection

Read `~/.turbo/config.json` for `repoMode`. If `repoMode` is `"fork"` or `"source"`, turbo skill improvements can be contributed upstream.

If `~/.turbo/repo/` exists, identify which installed skills are turbo skills:

- List directories in `~/.turbo/repo/skills/`
- Any skill in `~/.claude/skills/` that has a matching directory in `~/.turbo/repo/skills/` is a turbo skill
- Skills only in `~/.claude/skills/` (no match in the repo) are user/project skills

**Exception:** If the current project IS the turbo repo (i.e., the working directory contains this skill collection), route turbo skill changes directly to `skills/` in the project directory. Skip the installed-copy indirection and the contribution flow.

## Step 2: Identify Session Skills and Scan for Lessons

### Identify Session Skills

Before scanning for lessons, identify which skills were loaded during this session:

- Scan the conversation for Skill tool invocations and SKILL.md reads from `~/.claude/skills/`
- Build a list of session skills, marking each as turbo or user/project skill (using the detection from Step 1)
- This list informs routing in Step 4: when a lesson clearly arose from a specific skill's workflow, that skill is the natural routing target

### Scan for Lessons

Scan the full conversation with this priority:

1. **Corrections** — Where the user interrupted, said "no", "actually", "stop", "not like that", redirected, or manually fixed something Claude did wrong. Highest-value lessons.
2. **Repeated guidance** — Instructions the user gave more than once.
3. **Skill-shaped knowledge** — Domain expertise that was needed repeatedly, tool/API integration details that had to be looked up, decision frameworks that emerged for evaluating options, content templates or writing conventions that were refined, and multi-step workflows where ordering mattered (as reusable domain knowledge, not the workflow itself — see #4).
4. **New workflows** — Did this session establish a novel multi-step procedure, coordination pattern, or automation that worked? A successful workflow that would need to be repeated is a prime skill candidate — even if it ran fine this time. Distinct from #3: this captures the procedure itself as a repeatable artifact, not knowledge about how to do it. Flag it.
5. **Preferences** — Formatting, naming, style, or tool choices the user expressed.
6. **Failure modes** — Approaches that failed, with what worked instead. For tool or script call failures, trace back to the information source that led to the error and route the fix there (e.g., clarify a reference file, update skill instructions, add missing documentation).
7. **Domain knowledge** — Facts or conventions Claude needed but did not have.
8. **Improvement opportunities** — Out-of-scope improvements noticed during work: code that could be refactored, missing tests, performance issues, readability concerns, or feature ideas that were intentionally skipped to stay focused. **Skipped findings count here**: when code simplification or code review identified a genuine improvement or issue but it was skipped for this session, route it as a project improvement so it isn't lost.
9. **Trusted reviewer feedback** — Human PR review comments that reveal project conventions, patterns, or corrections. Trusted reviewers are repo collaborators with `admin` or `maintain` roles (determine via `gh api repos/{owner}/{repo}/collaborators --jq '.[] | select(.role_name == "admin" or .role_name == "maintain") | .login'`). Their feedback takes precedence over other reviewers and AI bots when there are contradictions.

After scanning, read all skill SKILL.md files (they are small). This gives Step 4 full context for routing.

## Step 3: Filter

Keep only lessons that are:
- **Stable** — likely to remain true across future sessions
- **Non-obvious** — Claude would not already know this
- **Actionable** — can be expressed as a rule or instruction
- **Not already documented** — absent from the files read in Step 1
- **Still a concern** — the issue is not already fixed by changes made in this session. If a bug was found and fixed, or a missing feature was added, future sessions will see the corrected code — they don't need a reminder about the old problem. **Exception: successful workflows and procedures are not "resolved" — they're skill candidates precisely because they worked and will need to be repeated.**

Discard anything session-specific, speculative, one-off, or already resolved by code changes in this session (but not successful workflows — see exception above). If no lessons survive filtering, tell the user and stop.

## Step 4: Route Each Lesson

Assign each surviving lesson to exactly one destination.

**Skill-first rule (mandatory):** Before consulting the table below, check whether the lesson corrects, refines, or adds a guardrail to any existing skill's behavior — turbo or user/project. This includes lessons about skipping steps, wrong defaults, missing edge cases, or any "don't do X when running /skill-name" correction. If yes, route to that skill. Do not route skill corrections to auto memory or CLAUDE.md — they belong in the skill they correct. This rule is not a preference; it is a hard constraint that takes precedence over the table rows below.

| Destination | Criteria |
|---|---|
| **Existing turbo skill** | Lesson would improve a turbo skill's instructions, supporting files, or reference materials, add a missing edge case, correct its workflow, or refine its trigger conditions. Route to any turbo skill whose *domain* covers the lesson — not just the skill worked on in this session. Changes go to the installed copy at `~/.claude/skills/`. If `repoMode` is `"fork"` or `"source"`, also apply to `~/.turbo/repo/` and flag for contribution (see Step 6). |
| **Existing user/project skill** | Same criteria as above, but for non-turbo skills. Changes go to the skill file directly. No contribution flow. |
| **New skill** | A cohesive body of knowledge emerged that deserves its own on-demand context. The test: would this knowledge be too large for a CLAUDE.md section, and should it only be loaded when relevant? See the skill categories table below. |
| **Project CLAUDE.md / AGENTS.md** | Intentional project decisions: conventions, architecture, stack choices, build setup, module boundaries. Also factual corrections to CLAUDE.md content (wrong commands, outdated paths, incorrect conventions) — fix these directly, do not defer to Project improvements. |
| **Auto memory** | Discovered knowledge with no skill home: API quirks, debugging workarounds, compiler gotchas, tool pitfalls, user preferences. Must not overlap with any existing skill's domain — if it does, route to the skill instead (see skill-first rule above). |
| **Project improvements** | Actionable improvement to existing **code**: refactoring, performance, reliability, readability, testing, or DX. Not for documentation fixes — factual errors in CLAUDE.md belong in the row above. Route to `.turbo/improvements.md` via the `/note-improvement` skill. |
| **No destination** | Does not clearly fit any destination. Drop it. Routing a weak lesson is worse than losing it. |

**Skill categories:**

| Category | What it encodes | Example |
|---|---|---|
| Domain expertise | Best practices, patterns, API preferences | SwiftUI expert, Core Data guide |
| Tool/Service integration | API references, operations, ID formats | Paddle, Stripe, Keycloak |
| Decision framework | Judgment criteria, confidence levels, triage | Evaluate findings, performance audit |
| Content template | Writing conventions, tone, structure | Drafting, blog post, changelog |
| Knowledge/Research | Information discovery, schema definitions | Knowledge base, research process |
| Orchestrated workflow | Stateful multi-step procedures | Process ticket, process income |

**Splitting heuristic:** When a session creates scripts or multi-step procedures, split the lesson: a brief pointer goes to CLAUDE.md (script names, purpose), and the full workflow goes to a skill. Don't collapse them into a single CLAUDE.md entry.

**Tiebreakers (in priority order):**
1. **Skill correction → skill (hard rule).** Any lesson that corrects, constrains, or refines a skill's behavior MUST route to that skill. Never to auto memory, never to CLAUDE.md. This is the highest-priority routing rule.
2. **Turbo skill vs. CLAUDE.md → always the turbo skill.** Broader impact (benefits all turbo users), better scoped, loaded only when relevant.
3. **Skill vs. CLAUDE.md → always the skill.** Skills are more discoverable, better scoped, and loaded only when relevant.
4. **Skill vs. auto memory → always the skill.** If a lesson falls within the domain of an existing skill, it goes to the skill. Auto memory is for knowledge that has no skill home.
5. **CLAUDE.md vs. auto memory** — intentional decisions go to CLAUDE.md. Discovered knowledge (gotchas, workarounds, quirks) goes to auto memory.
6. **Lesson vs. improvement** — if the item is *knowledge to remember*, it's a lesson. If it's *work to do later*, it's an improvement. They don't compete — the same session can produce both.

## Step 5: Present Routing Plan

Output a table as text before making any changes:

```
| # | Lesson | Destination | Action |
|---|--------|-------------|--------|
| 1 | Always use X for... | Project AGENTS.md | Append to ## Conventions |
| 2 | The /create-pr skill should... | ~/.claude/skills/create-pr | Update Step 2 |
| 3 | Multi-step deploy workflow | New project skill | Create new skill |
| 4 | User prefers short commit msgs | Auto memory | Append to MEMORY.md |
```

For each lesson, show: concise summary, target file/skill, and whether it's an append, update-in-place, or new creation.

Then use `AskUserQuestion` with these options: **Approve** or **Reject**.

## Step 6: Execute

Apply approved changes in order:

1. **Updates to existing files** — Read the target, find the right section, append or update in place. Match the tone and format already present. For auto memory, follow the memory system conventions from the system prompt. For user/project skill updates, run `/create-skill` to apply the changes.
2. **Updates to turbo skills** — Read `~/.turbo/repo/SKILL-CONVENTIONS.md` for the turbo project's skill conventions. Use these conventions when editing turbo skills. For each lesson routed to a turbo skill:
   1. Run `/create-skill` to update the installed copy at `~/.claude/skills/<name>/SKILL.md` (immediate effect for the user).
   2. If `repoMode` is `"fork"` or `"source"`: use `AskUserQuestion` to ask "These turbo skill improvements could benefit other users. Run `/contribute-turbo` to submit them?" If yes, apply the same changes to `~/.turbo/repo/skills/<name>/SKILL.md`, stage them (`git -C ~/.turbo/repo add skills/<name>/`), and run `/contribute-turbo`.
3. **Improvements** — For items routed to project improvements, run `/note-improvement` with the summary, location, and rationale for each.
4. **New skills** — Run `/create-skill` for each new skill. Provide the trigger conditions and relevant context from the session.

## Writing Guidelines

- Match the tone and format of the target file
- Use imperative mood and short declarative sentences
- Group related insights under a descriptive heading
- Omit rationale unless the rule would seem arbitrary without it
- Never include temporary state, in-progress work, or task-specific details
- Keep lessons generic—avoid overly concrete examples; state the rule, not the instance
- For AGENTS.md: write as agent documentation — project rules any AI agent on this repo should follow
- For auto memory: write as personal Claude notes — concise, operational, organized by topic
- For skills: follow the conventions in the existing skill collection
