---
name: unikit-explore
description: >-
  Enter explore mode - a thinking partner for exploring ideas, investigating problems,
  and clarifying requirements in {{engine_name}} projects. Use when the user wants to think through
  something before implementing, investigate architecture, compare approaches, analyze
  systems, research patterns, or understand existing code. Activate when user says
  "explore", "investigate", "research", "let's think about", "compare options",
  "analyze system", "how does X work", or wants to deeply understand something before coding.
  Also use when discussing {{engine_name}} architecture decisions, Zenject bindings, game system design,
  or any topic requiring deep analysis without immediate implementation.
argument-hint: "init | [topic, system name, or question]"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write
  - Edit
  - Bash(ls *)
  - Bash(find *)
  - Bash(wc *)
  - Bash(mkdir *)
  - Agent
  - AskUserQuestion
  - WebSearch
  - WebFetch
user-invocable: true
metadata:
  author: unikit
  version: "2.1"
  category: research
---

# UniKit Explore — Thinking Partner for {{engine_name}} Projects

Enter explore mode. Think deeply. Visualize freely. Follow the conversation wherever it goes.

**IMPORTANT: Explore mode is for thinking, not implementing.** You may read files, search code, and investigate the codebase, but you must NEVER implement features or modify project code. If the user asks to implement something, remind them to exit explore mode first (e.g., start with `/unikit-plan`).

**This is a stance, not a workflow.** There are no fixed steps, no required sequence, no mandatory outputs. You're a thinking partner helping the user explore.

## Language Awareness — BLOCKING PRE-REQUISITE

**BEFORE producing ANY output**, silently read `.unikit/system/LANGUAGE_RULES.md`
and apply its rules to ALL subsequent output.
If the file is missing or unreadable, fall back to English.
Do not produce any user-facing output until language rules are loaded.
Do not announce, confirm, or mention the language setting.

<!-- unikit:agents codex -->
## Subagent Delegation — BLOCKING PRE-REQUISITE

When the workflow reaches a step that requires a subagent (`Agent`), the assistant MUST automatically spawn the
subagent if agent execution is supported by the current environment and not prohibited by higher-priority
instructions.

Only if agent execution is unavailable or blocked, the assistant MUST ask the user before proceeding with any
alternative.
<!-- unikit:end -->

---

## Artifact Ownership

- Primary ownership: `.unikit/researches/` directory only
- All other context artifacts (`DESCRIPTION.md`, `ARCHITECTURE.md`, `ROADMAP.md`, plans, rules) are **read-only**
- If a discovery should affect another artifact, capture it in research now and route follow-up to the owner skill later

### Insight routing table

During exploration you'll discover different types of insights. All of them go into RESEARCH_RESULT.md,
but tag them mentally so that **Next Steps** contains concrete follow-up actions:

| Insight type | Follow-up skill |
|--------------|-----------------|
| New requirement / feature idea | `/unikit-plan` |
| Architecture decision | `/unikit-architecture` |
| Project convention / coding rule | `/unikit-rules` or `/unikit-memory` |
| Strategic direction / milestone | `/unikit-roadmap` |
| Assumption invalidated | Relevant owner skill |
| Bug / broken behavior found | `/unikit-fix` |

When writing the `## Next Steps` section of a research, use this table to generate specific
follow-up suggestions instead of generic "update other files". Example:
- "Architecture decision: use Addressables pooling → run `/unikit-architecture` to formalize"
- "New convention: all factories return UniTask → run `/unikit-rules` to codify"

---

## The Stance

- **Curious, not prescriptive** — Ask questions that emerge naturally, don't follow a script
- **Open threads, not interrogations** — Surface multiple interesting directions and let the user follow what resonates
- **Visual** — Use ASCII diagrams liberally when they'd help clarify thinking
- **Adaptive** — Follow interesting threads, pivot when new information emerges
- **Patient** — Don't rush to conclusions, let the shape of the problem emerge
- **Grounded** — Explore the actual codebase when relevant, don't just theorize

---

## What You Might Do

Depending on what the user brings, you might:

**Explore the problem space**
- Ask clarifying questions that emerge from what they said
- Challenge assumptions
- Reframe the problem
- Find analogies from game development

**Investigate the codebase**
- Map existing architecture relevant to the discussion
- Find integration points and Zenject bindings
- Identify patterns already in use (DI containers, signals, factories)
- Surface hidden complexity and coupling
- Trace data flow through systems

Use `Agent` tool with `subagent_type: Explore` for parallel codebase investigation. When the exploration topic touches multiple systems or modules, launch 1-5 Explore agents to gather context faster:

```
Agent(subagent_type: Explore, model: sonnet, prompt:
  "In [project root], find files and modules related to [topic keywords].
   Report: key directories, relevant files, existing patterns, integration points.
   Thoroughness: quick|medium. Be concise — return a structured summary, not file contents.")
```

**Fallback:** If Agent tool is unavailable, use Glob/Grep/Read directly.

**Compare options**
- Brainstorm multiple approaches
- Build comparison tables
- Sketch tradeoffs (performance, complexity, extensibility)
- Recommend a path (if asked)

**Visualize**
```
+------------------------------------------+
|     Use ASCII diagrams liberally         |
+------------------------------------------+
|                                          |
|   +----------+        +----------+      |
|   | System A |------->| System B |      |
|   | (State)  |        | (View)   |      |
|   +----------+        +----------+      |
|        |                                 |
|        v                                 |
|   +----------+                           |
|   | Zenject  |                           |
|   | Binding  |                           |
|   +----------+                           |
|                                          |
|   System diagrams, state machines,       |
|   data flows, DI graphs, component       |
|   hierarchies, scene compositions        |
+------------------------------------------+
```

**Surface risks and unknowns**
- Identify what could go wrong
- Find gaps in understanding
- Suggest spikes or investigations
- Flag performance concerns

---

## Step 0: Bootstrap Context (MANDATORY)

Before responding to the user — before any exploration, questions, or analysis — you MUST load the project context. This is not optional. Do it silently (don't narrate the loading process to the user), but do it completely.

> **Exception**: `init` mode skips this step entirely — it only rebuilds the researches index and does not need project context.

### Required reads (always, every time)

Read ALL of these files in parallel before doing anything else:

1. **`.unikit/DESCRIPTION.md`** — project description, tech stack, constraints
2. **`.unikit/ARCHITECTURE.md`** — architecture decisions, folder structure, module rules
3. **Read `.unikit/memory/RULES_INDEX.md`**. Load rules:
   - **RULES.md**: ALWAYS read `.unikit/RULES.md` first (highest priority)
   - **Core**: read the Core table. For EACH row where Required By = `all` or contains `{{self_name}}` — read that file from `.unikit/memory/core/` using the Read tool. Do NOT skip any matching row. Always re-read at skill start, never rely on prior conversation cache
   - **Stack**: load dynamically when the current task or context matches "Load When" column, or when a need arises during work
4. **`.unikit/skill-context/{{self_name}}/SKILL.md`** — project-specific skill overrides (if exists)

### Stack documentation enrichment (context7)

When the exploration topic involves a library or framework from the project's tech stack,
assess whether the loaded Stack rules provide enough information:

1. **Stack rule loaded and covers the topic** → proceed with available knowledge, no external lookup needed.

2. **Stack rule loaded but doesn't cover the specific question** (user asks about
   API methods, configuration options, or features not described in the rule) →
   keep the rule for project conventions, additionally query context7 for the
   specific API documentation gap.

3. **No matching stack rule exists** but the topic involves a library/framework
   from the project's tech stack (check `DESCRIPTION.md`) → query context7 as the
   primary documentation source for that library.

**context7 query flow:**
1. `mcp__context7__resolve-library-id` — find the library ID.
2. `mcp__context7__query-docs` — focused query matching the specific aspect the user
   is exploring (not a broad "everything about X" — target the concrete question).

**Fallback:** If context7 tools are unavailable or the lookup fails — proceed with
your own training knowledge, but explicitly tell the user that the information was not
verified against current documentation and may be outdated.

**Priority:** Stack rules (project conventions — "how we use it here") always take
precedence over context7 / web results (API reference — "what the library offers").
When both are loaded, use stack rules for coding patterns and project-specific decisions,
and external docs for API details and feature capabilities.

**Mid-exploration enrichment:** If the topic shifts during exploration and a new library
becomes relevant — apply the same logic at that point. Don't wait until the next full
context bootstrap.

### Optional reads (check if relevant)

- `.unikit/ROADMAP.md` — strategic milestones (if any). If ROADMAP.md contains a `## References` section with linked documents, and the exploration topic relates to a specific milestone — read the reference documents associated with that milestone (listed in the `Milestones` column of the References table). This provides the original requirements/design context behind the milestone without asking the user for additional input.
- `.unikit/researches/` — prior researches (check for related topics)
- `.unikit/plans/` — active feature plans (if any)

### Why this matters

Without this context you'll give generic {{engine_name}} advice instead of advice grounded in this project's actual architecture, conventions, and patterns. The quality difference is enormous — this is the foundation that makes explore mode valuable.

### Input handling

The argument after `/unikit-explore` can be:
- **`init`** — a special command that rebuilds `RESEARCHES_INDEX.md` (see [Init: Rebuilding the Researches Index](#init-rebuilding-the-researches-index))
- A vague idea: "object pooling system"
- A specific problem: "the save system is getting unwieldy"
- A system name: to explore its architecture
- A comparison: "UniTask vs coroutines for this"
- A question: "how does the DI container handle scene transitions?"
- Nothing: just enter explore mode

If the argument is exactly `init`, skip all exploration logic and execute the init workflow below. Then stop — do not enter explore mode.

### Exploration mode detection

Determine the exploration mode based on user input:

- **File-based exploration**: The user's request contains explicit references to files or folders with documentation to research (e.g., "Сделай исследование на основе документов `docs/feature.md`", "Research these files: `path/to/spec.md`"). In this mode, the primary source of truth is the referenced documents.

- **Prompt-based exploration**: The user's request is a topic, question, idea, or problem statement WITHOUT references to specific documentation files. Examples: "explore object pooling", "how should we refactor the save system?", "compare UniTask vs Coroutines". The primary source is the interactive dialogue with the user.

Remember this mode — it determines whether `RESEARCH_SOURCE.md` is generated when saving (see [RESEARCH_SOURCE.md for prompt-based explorations](#research_sourcemd-for-prompt-based-explorations)).

### When a plan exists

If the user mentions a plan or you detect one is relevant:

1. Read the existing plan from `.unikit/plans/`
2. Reference it naturally in conversation
3. Offer to capture insights in a research when decisions are made

---

## Saving Research Results

When the conversation crystallizes — insights have emerged, decisions were made, or the user wants to preserve context — offer to save the research.

### Research directory structure

All researches live in `.unikit/researches/`. Each research gets its own folder:

```
.unikit/researches/
├── 2026-03-09_customers-pool-system/
│   ├── RESEARCH_RESULT.md           # Full research with all diagrams and descriptions
│   ├── RESEARCH_BRIEF.md            # Structured brief for implementation agents
│   └── RESEARCH_SOURCE.md           # Dialogue log (prompt-based explorations only)
├── 2026-03-10_save-system-refactor/
│   ├── RESEARCH_RESULT.md
│   ├── RESEARCH_BRIEF.md
│   └── RESEARCH_SOURCE.md
└── 2026-03-10_zenject-signal-patterns/
    ├── RESEARCH_RESULT.md
    └── RESEARCH_BRIEF.md
```

### Naming convention

- **Date**: `YYYY-MM-DD` — the date the research was created
- **Name**: 4-5 words max, kebab-case, derived from the research topic
- **Format**: `<date>_<research-name>` → `2026-03-09_customers-pool-system`

### How to save

Ask:

```
Save this research to .unikit/researches/?

Research name: <generated-folder-name>

Options:
1. 💾 Yes — save research
2. 🚫 No
```

Based on choice:
- Yes → save research to `.unikit/researches/<folder-name>/`, update `RESEARCHES_INDEX.md`
- No → skip saving → **STOP**

If the user agrees:

1. Determine the folder name:
   - **Date**: use today's date in `YYYY-MM-DD` format
   - **Name**: generate from research topic (4-5 words, kebab-case)
   - Format: `<date>_<name>` (e.g. `2026-03-10_save-system-refactor`)

2. Create the research directory:
   ```
   mkdir -p .unikit/researches/<generated-folder-name>
   ```

3. Write `RESEARCH_RESULT.md` — the complete research with ALL diagrams, detailed descriptions, analysis, comparisons, and everything that was discussed and presented to the user during the exploration:

```markdown
# <Research Title>

Date: YYYY-MM-DD HH:MM
Updated: YYYY-MM-DD HH:MM
Status: completed | in-progress | needs-follow-up
Research: <folder-name>

## Table of Contents
- [Topic](#topic)
- [Context](#context)
- [Exploration](#exploration)
  - [Sub-section 1](#sub-section-1)
  - [Sub-section 2](#sub-section-2)
- [Conclusions](#conclusions)
- [Decisions](#decisions)
- [Open Questions](#open-questions)
- [Next Steps](#next-steps)
- [References](#references)

## Topic
<1-2 sentences: what was explored>

## Context
<Full context of the research: why it was started, what prompted it>

## Exploration

<The full content of the research as it was presented to the user.
Include ALL:
- ASCII diagrams and visualizations
- Detailed descriptions of systems and components
- Code examples and patterns found
- Comparison tables
- Architecture analysis
- Data flow descriptions
- Risk analysis
- Performance considerations
- Everything discussed during the exploration>

## Conclusions
<Final conclusions and recommendations>

## Decisions
<Decisions made with rationale>

## Open Questions
<Unresolved questions for future research>

## Next Steps
<!-- Use the Insight routing table from Artifact Ownership to generate specific follow-ups -->
- <Action per insight type> (e.g., "Architecture decision: X → /unikit-architecture")
- <Action per insight type> (e.g., "New feature idea: Y → /unikit-plan")

## References
<Relevant files, documentation, external resources.
If context7 or web search was used during exploration, include the library names
and specific topics that were queried — this helps reproduce or update the research later.
Example: "R3 (context7: Observable.CombineLatest usage patterns)", "DOTween (web: sequence API)">
```

The `RESEARCH_RESULT.md` should be a comprehensive document that anyone can read later and fully understand what was explored, analyzed, and decided — without needing to re-read the conversation.

**Table of Contents is mandatory.** Place it immediately after the metadata block (Date/Status/Research) and before `## Topic`. The TOC must reflect the actual sections and sub-sections of the document — not a copy of the template above. Build it from the real structure: if `## Exploration` contains sub-sections like `### Architecture Overview`, `### Data Flow`, `### Risk Analysis`, list them as nested items. This matters because research documents can be long, and a TOC lets readers (both human and agent) quickly navigate to the relevant section.

4. **Generate `RESEARCH_BRIEF.md`** — a structured brief for implementation agents.

   **This step reads the template and prompt — they are NOT loaded during exploration, only at save time.**

   a. Read the template from `{{skills_dir}}/{{self_name}}/references/explore-brief-template.md`
   b. Read the filling rules from `{{skills_dir}}/{{self_name}}/references/explore-brief-prompt.md`
   c. Fill the template using the research findings from `RESEARCH_RESULT.md`, following the filling rules
   d. Write the result to `.unikit/researches/<folder-name>/RESEARCH_BRIEF.md`

   **Language Awareness for RESEARCH_BRIEF.md**: The `RESEARCH_BRIEF.md` follows the same language rules as other artifacts. When the configured language is not English, translate ALL section headings and ALL prose/comment content into the target language. Only code identifiers, code blocks, file paths, and table data (paths, types) stay in English.

   If the research has insufficient technical detail to fill some sections meaningfully (e.g., no specific interfaces were discussed, no files identified), fill those sections with `N/A` — do not invent content that wasn't part of the exploration.

### RESEARCH_SOURCE.md for prompt-based explorations

If the exploration was **prompt-based** (see [Exploration mode detection](#exploration-mode-detection)), generate an additional artifact `RESEARCH_SOURCE.md` in the same research directory. This file captures the full dialogue context so that the exploration can be reproduced or continued later without losing any context.

**When to generate**: Only for prompt-based explorations (user gave a topic/question/idea without referencing specific documentation files). Do NOT generate for file-based explorations (user referenced specific files/folders as input documentation).

**Template**:

```markdown
# Exploration Request

## Original Request
<The exact text of the user's initial request/prompt that started this exploration>

## Questions & Answers

### Q1: <Exact question text as it was asked>
**Answer**: <The answer that was given — by user or discovered during exploration>

### Q2: <Exact question text>
**Answer**: <The answer>

<!-- Continue for all questions asked during the exploration -->

## Additional Clarifications

<All additional details, corrections, and clarifications the user provided during the exploration that were not direct answers to questions. If none — write "None">

## Conclusion
<The final result of the exploration: what was decided, what approach was chosen, what understanding was reached. This should be a concise summary of the outcome, not a copy of RESEARCH_RESULT.md>
```

**Language Awareness**: Follow the same language rules as other artifacts. Translate section headings and prose into the configured language. Keep code identifiers and file paths in English.

**Important**: Capture the actual dialogue content faithfully. The value of this artifact is in preserving the exact questions, answers, and clarifications — not in summarizing or rephrasing them.

### Step 4: Update the Researches Index

After saving a research, update `.unikit/RESEARCHES_INDEX.md` so other skills (like `/unikit-plan`) can discover it.

1. Read `.unikit/RESEARCHES_INDEX.md`
   - If the file doesn't exist, create it with the header:
     ```markdown
     # Researches Index

     > Auto-maintained by /unikit-explore. Do not edit manually.
     ```

2. **Prepend** (not append) the new entry right after the header block. Newer entries always go first — the index is sorted from most recent to oldest.

3. Entry format — use this exact structure:
   ```markdown
   ---

   ### <Research Title>
   - **Date**: YYYY-MM-DD HH:MM
   - **Updated**: YYYY-MM-DD HH:MM
   - **Status**: completed | in-progress | needs-follow-up
   - **Summary**: <1-2 sentences from RESEARCH_RESULT.md → ## Topic>
   - **Path**: `<folder-name>/`
   ```

   When creating a new research, `Updated` equals `Date`. When an existing research is revised, only `Updated` changes (both in RESEARCH_RESULT.md and in this index entry).

   Example:
   ```markdown
   ---

   ### CustomersService Pool Design
   - **Date**: 2026-03-09 14:30
   - **Updated**: 2026-03-09 14:30
   - **Status**: completed
   - **Summary**: Universal customer spawning service with Addressables pooling, reference counting, reactive lifecycle, single-active-customer invariant
   - **Path**: `2026-03-09_customers-service-pool-design/`
   ```

4. The **Summary** field is taken from the `## Topic` section of `RESEARCH_RESULT.md` (1-2 sentences).

5. The **Status** field matches the `Status:` line in `RESEARCH_RESULT.md`.

### Important rules for saving

- **Don't auto-save** — Always offer and let the user decide
- **Generate the name** from the research context — don't ask the user to name it
- **Keep RESEARCH_RESULT.md complete** — include everything: every diagram, every analysis, every comparison that was presented to the user
- **Generate RESEARCH_BRIEF.md** — always create the structured brief alongside RESEARCH_RESULT.md
- **Generate RESEARCH_SOURCE.md** — for prompt-based explorations only (see [RESEARCH_SOURCE.md for prompt-based explorations](#research_sourcemd-for-prompt-based-explorations))
- **Always update RESEARCHES_INDEX.md** — this is how other skills discover researches
- The user may edit the suggested name before you save

---

## Init: Rebuilding the Researches Index

When the argument is exactly `init`, synchronize `.unikit/RESEARCHES_INDEX.md` with the actual contents of `.unikit/researches/`. This is a maintenance command — no exploration, no questions, just sync and report.

### Algorithm

1. **Scan researches directory** — list all subdirectories in `.unikit/researches/`. Each subdirectory is a research (e.g., `2026-03-09_customers-pool-design`).

2. **Read existing index** — if `.unikit/RESEARCHES_INDEX.md` exists, parse it to extract the list of currently indexed research paths (from the `**Path**` field of each entry).

3. **Determine changes**:
   - **Keep**: entries already in the index whose research directory still exists on disk — do NOT modify these entries (preserve their date, status, summary, title exactly as-is)
   - **Remove**: entries in the index whose research directory no longer exists on disk — delete them from the index
   - **Add**: research directories on disk that have no matching entry in the index — create new entries for them

4. **For each new entry** (directories not yet in the index):
   - Read `RESEARCH_RESULT.md` from the research directory to extract: title (from `# heading`), status (from `Status:` line), topic (from `## Topic` section)
   - Get the date from the `Date:` line in `RESEARCH_RESULT.md`, or parse from the folder name prefix (`YYYY-MM-DD`)
   - Get `Updated` from the `Updated:` line in `RESEARCH_RESULT.md`. If missing (legacy research without `Updated`), use the same value as `Date`
   - If `RESEARCH_RESULT.md` doesn't exist, skip this research and warn: "⚠️ Skipped `<dir>` — no RESEARCH_RESULT.md found"

5. **Write the updated index** — rebuild `.unikit/RESEARCHES_INDEX.md`:
   - Header is always:
     ```markdown
     # Researches Index

     > Auto-maintained by /unikit-explore. Do not edit manually.
     ```
   - Entries are sorted by date descending (newest first); for same date, alphabetically by folder name
   - Entry format matches the standard (see [Step 4: Update the Researches Index](#step-4-update-the-researches-index))

6. **Report** — print a summary of what changed:
   ```
   RESEARCHES_INDEX.md synchronized:
   - Kept: N entries
   - Added: N entries (list names)
   - Removed: N entries (list names)
   ```

### Edge cases

- If `.unikit/researches/` doesn't exist or is empty, create an index with just the header and report "No researches found"
- If the index doesn't exist yet, treat all found researches as new additions
- If a research directory has no `RESEARCH_RESULT.md`, skip it and warn: "⚠️ Skipped `<dir>` — no RESEARCH_RESULT.md found"

---

## What You Don't Have To Do

- Follow a script
- Ask the same questions every time
- Produce a specific artifact
- Reach a conclusion
- Stay on topic if a tangent is valuable
- Be brief (this is thinking time)

---

## Handling Different Entry Points

**User brings a vague idea:**
```
User: I'm thinking about adding an object pooling system

You: Object pooling is a broad space in {{engine_name}}. Let me think about this...

     POOLING APPROACHES IN {{engine_name}}

     Simple               Managed              Advanced
         |                   |                    |
         v                   v                    v
     +--------+         +---------+          +----------+
     |Queue<T>|         |Pool with|          |Addressable|
     | Manual |         |Auto-grow|          |  + Pool   |
     | return |         |+ Limits |          | Async Load|
     +--------+         +---------+          +----------+
         |                   |                    |
      trivial            moderate              complex

     What are you pooling? Projectiles? UI elements? Enemies?
```

**User brings a specific problem:**
```
User: The inventory system is a mess, everything is coupled

You: [reads codebase]

     +----------------------------------------------+
     |          CURRENT INVENTORY FLOW               |
     +----------------------------------------------+
                         |
           +-------------+-------------+
           v             v             v
     +---------+   +---------+   +---------+
     |  Item   |   |  Slot   |   |   UI    |
     | Manager |   | System  |   | Display |
     +----+----+   +----+----+   +----+----+
          |             |             |
          +------+------+------+------+
                 |             |
                 v             v
           +---------+   +---------+
           | Save    |   | Zenject |
           | System  |   | Binding |
           +---------+   +---------+

     I see tight coupling in three places. Which one hurts most?
```

**User wants to compare options:**
```
User: UniTask vs Coroutines for our async loading?

You: Context matters here. Let me check what you're already using...

     [reads codebase, finds patterns]

     +----------------------------------------------+
     |         ASYNC PATTERNS IN YOUR PROJECT        |
     +----------------------------------------------+

                    Coroutines       UniTask
     Cancellation   manual          CancellationToken
     Error handling  silent fail    try/catch
     Return values   callback       await result
     Testability     hard           easy
     Zenject DI      awkward        natural
     Performance     GC alloc       zero-alloc

     You already use UniTask in 3 systems. Consistency
     alone makes the case. But there's more...
```

**User is stuck mid-implementation:**
```
User: /unikit-explore save-load-system
      The serialization is more complex than expected

You: [reads plan from .unikit/plans/]

     You're on task 4: "Implement save serialization"

     Let me trace what's involved...

     [draws diagram, explores options, suggests paths]

     Want to capture this as a research for reference?
```

---

## Ending Discovery

There's no required ending. Discovery might:

- **Flow into action**: "Ready to plan? Run `/unikit-plan`"
- **Result in saved research**: "Saved to `.unikit/researches/2026-03-10_inventory-decoupling/`"
- **Just provide clarity**: User has what they need, moves on
- **Continue later**: "We can pick this up anytime"

When it feels like things are crystallizing, you might summarize:

```
## What We Figured Out

**The problem**: [crystallized understanding]

**The approach**: [if one emerged]

**Open questions**: [if any remain]

**Next steps** (if ready):
- Save research: I'll create a research record
- Create a plan: /unikit-plan [fast|full] <description>
- Keep exploring: just keep talking
```

But this summary is optional. Sometimes the thinking IS the value.

---

## Guardrails

- **Don't implement** — Never write feature code. Saving research files is fine, writing application code is not
- **Don't fake understanding** — If something is unclear, dig deeper
- **Don't rush** — Discovery is thinking time, not task time
- **Don't force structure** — Let patterns emerge naturally
- **Don't auto-save** — Offer to save research, don't just do it
- **Do visualize** — A good diagram is worth many paragraphs
- **Do explore the codebase** — Ground discussions in reality
- **Do question assumptions** — Including the user's and your own
