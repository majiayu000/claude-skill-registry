---
name: gsd-discuss-phase
description: Gather phase context through adaptive questioning before planning
allowed-tools: Read, Edit, Bash
argument-hint: '[phase]'
---


<objective>
Extract implementation decisions that downstream agents need — researcher and planner will use CONTEXT.md to know what to investigate and what choices are locked.

**How it works:**
1. Analyze the phase to identify gray areas (UI, UX, behavior, etc.)
2. Present gray areas — user selects which to discuss
3. Deep-dive each selected area until satisfied
4. Create CONTEXT.md with decisions that guide research and planning

**Output:** `{phase}-CONTEXT.md` — decisions clear enough that downstream agents can act without asking the user again
</objective>

<execution_context>
@.github/get-shit-done/workflows/discuss-phase.md
@.github/get-shit-done/templates/context.md
</execution_context>

<context>
Phase number: $ARGUMENTS (required)

**Load project state:**
@.planning/STATE.md

**Load roadmap:**
@.planning/ROADMAP.md
</context>

<process>
<step name="validate_phase">
Validate phase number (error if missing or not in roadmap).

1. Check if phase argument provided
2. Parse phase number (handle both integer and decimal: "5", "5.1")
3. Load ROADMAP.md
4. Search for phase in roadmap phases list
5. If not found: display error with available phases, exit
6. Extract phase goal and description
</step>

<step name="check_existing_context">
Check if CONTEXT.md already exists for this phase.

1. Find phase directory: .planning/phases/{phase}-*/
2. Look for {phase}-*-CONTEXT.md files
3. If exists:
   - Display current content
   - Offer: "Update / View only / Skip"
   - If Update: proceed with discussion
   - If View: display full file and exit
   - If Skip: exit
4. If doesn't exist: proceed to analysis
</step>

<step name="analyze_phase">
Analyze phase goal to identify domain-specific gray areas.

**Domain-aware analysis:**
Gray areas depend on what's being built. Based on phase goal, identify:

- Something users SEE → layout, density, interactions, states, visual hierarchy
- Something users CALL → responses, errors, auth, versioning, rate limiting
- Something users RUN → output format, flags, modes, error handling
- Something users READ → structure, tone, depth, flow
- Something being ORGANIZED → criteria, grouping, naming, exceptions

Generate 3-4 **phase-specific** gray areas, not generic categories.

**Examples:**
- Phase: "Build task dashboard" → Gray areas: "Task grouping", "Urgency indicators", "Empty states", "Interaction feedback"
- Phase: "Add authentication" → Gray areas: "Session duration", "Password requirements", "2FA approach", "Error messaging"
- Phase: "Create reports" → Gray areas: "Report formatting", "Date range defaults", "Export formats", "Performance data depth"

**Critical: Scope guardrail**
- Phase boundary from ROADMAP.md is FIXED
- Discussion clarifies HOW to implement, not WHETHER to add more
- If user suggests new capabilities: "That's its own phase. I'll note it for later."
- Capture deferred ideas in separate section — don't lose them, don't act on them
</step>

<step name="present_gray_areas">
Present identified gray areas to user for selection.

1. List all generated gray areas (3-4)
2. For each: brief description of what decisions need to be made
3. Ask: "Which areas do you want to discuss? (select 1 or more)"
4. NO skip/none option — at least one area must be discussed
5. User can select multiple or all
6. Record selected areas for deep-dive
</step>

<step name="deep_dive_areas">
For each selected area, conduct adaptive questioning.

**Probing approach:**
1. Start with 4 context-specific questions for the area
2. Listen to responses, ask follow-up based on answers
3. After 4 questions: "More questions about [area], or move to next?"
4. If more: ask 4 more, check again
5. If next: move to next selected area
6. After all areas: "Ready to create context?"

**Question quality:**
- Ask about SPECIFIC implementation choices, not general preferences
- Focus on user-observable behavior, not technical internals
- Avoid "how should we..." — instead "what do you expect when..."
- Dig into edge cases: "What if X happens? What should user see?"

**Do NOT ask about (Claude handles these):**
- Technical implementation details
- Architecture choices (libraries, patterns)
- Performance optimization strategies
- Testing approaches
- Scope expansion beyond phase boundary
</step>

<step name="synthesize_context">
Synthesize discussion into CONTEXT.md structure.

Use template from templates/context.md as base structure.

**Sections to populate:**

1. **Essential Features**
   - Must-have features user specified
   - Core functionality that defines phase completion
   - User-observable outcomes that MUST exist

2. **Technical Boundaries**
   - Locked decisions: libraries, patterns, architecture
   - Constraints from discussion (e.g., "must use JWT", "no external APIs")
   - Technology choices user specified

3. **Scope Limits**
   - Explicitly out of scope items
   - Features deferred to future phases
   - Boundaries user confirmed

4. **Open Questions**
   - Things to investigate during research
   - Unclear areas that need research findings
   - Technical unknowns that research should answer

**Synthesis rules:**
- Write in clear, actionable language
- Use bullet points, not paragraphs
- Be specific: "Use JWT with 1-hour expiration" not "Handle authentication"
- Capture decisions, not discussion history
- Each item should guide downstream agents without additional user input
</step>

<step name="write_context_file">
Create .planning/phases/{phase}-*/{phase}-*-CONTEXT.md

**Frontmatter:**
```yaml
---
phase: {phase}
discussed: {ISO timestamp}
areas: [{list of discussed areas}]
decisions_count: {number of decisions captured}
---
```

**Body:** Use synthesized sections from previous step

**File naming:**
- Find next available number: {phase}-{NN}-CONTEXT.md
- Typically: {phase}-01-CONTEXT.md (first artifact in phase)
- If multiple discussions: increment number

**Example path:**
`.planning/phases/05-authentication/05-01-CONTEXT.md`
</step>

<step name="commit">
Commit the CONTEXT.md file.

```bash
git add .planning/phases/{phase}-*/{phase}-*-CONTEXT.md
git commit -m "docs(${phase}): capture context from discussion

Areas discussed: {list areas}
Decisions captured: {count}
"
```
</step>

<step name="offer_next">
Present next steps based on phase state.

**If phase has no RESEARCH.md:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 CONTEXT CAPTURED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Discussed: {areas}
Decisions: {count} captured in CONTEXT.md

───────────────────────────────────────────────────────────────

## ▶ Next Up

**Research phase** — investigate open questions and validate approach

/gsd-research-phase {phase}

<sub>/clear first → fresh context window</sub>

───────────────────────────────────────────────────────────────

**Also available:**
- /gsd-plan-phase {phase} — skip research, plan directly (if confident)

───────────────────────────────────────────────────────────────
```

**If phase already has RESEARCH.md:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 CONTEXT UPDATED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Updated decisions based on discussion.
Research may need refresh if decisions changed significantly.

───────────────────────────────────────────────────────────────

## ▶ Next Up

**Plan phase** — create execution plans with updated context

/gsd-plan-phase {phase}

<sub>/clear first → fresh context window</sub>

───────────────────────────────────────────────────────────────

**Also available:**
- /gsd-research-phase {phase} --refresh — re-research with new context
- cat .planning/phases/{phase_dir}/*-CONTEXT.md — review decisions

───────────────────────────────────────────────────────────────
```
</step>
</process>

<anti_patterns>
- Don't ask about technical implementation (Claude decides)
- Don't let scope creep — phase boundary is fixed
- Don't ask generic questions — phase-specific gray areas
- Don't accept "whatever you think" — push for concrete decisions
- Don't write vague context — be specific and actionable
</anti_patterns>

<success_criteria>
- [ ] Phase validated and exists in roadmap
- [ ] Existing CONTEXT.md handling (update/view/skip)
- [ ] Gray areas identified through intelligent analysis
- [ ] User chose which areas to discuss (at least one)
- [ ] Each selected area explored until satisfied
- [ ] Scope creep redirected to deferred ideas
- [ ] CONTEXT.md created with specific, actionable decisions
- [ ] File committed to git
- [ ] User knows next steps (research or plan)
</success_criteria>
