---
name: compound
description: Capture learnings (problems, decisions, gotchas) from sessions to make future agents more effective
argument-hint: [task-identifier]
---

<skill name="apex:compound" phase="any">

<overview>
Capture and compound knowledge from any session. Extracts problems solved, decisions made, and gotchas discovered - writing them to the task file for future agent retrieval.

This skill can run after any phase or standalone session. It compounds the agent's effectiveness over time.
</overview>

<phase-gate requires="none" sets="none">
  <reads-file>./apex/tasks/[ID].md</reads-file>
  <appends-section>future-agent-notes</appends-section>
  <may-modify>AGENTS.md</may-modify>
</phase-gate>

<initial-response>
<if-no-arguments>
I'll capture learnings from this session to help future agents.

Please provide the task identifier, or I'll try to find the current task from context.

You can find active tasks in `./apex/tasks/` or run with:
`/apex:compound [identifier]`
</if-no-arguments>
<if-arguments>Load task file and begin knowledge capture.</if-arguments>
</initial-response>

<workflow>

<step id="1" title="Load task context">
<instructions>
1. Read `./apex/tasks/[identifier].md`
2. Parse all sections for context:
   - `<research>` - What was investigated
   - `<plan>` - What was decided
   - `<implementation>` - What was built, issues encountered
   - `<ship>` - Review findings, reflection
3. Review conversation history for additional context
4. Extract candidate learnings for each category
</instructions>
</step>

<step id="2" title="Check existing learnings">
<purpose>
Avoid duplication and surface related past learnings.
</purpose>

<search-strategy>
```bash
# Extract keywords from current task
keywords = extract_keywords(task_intent, task_title)

# Search past task files for similar learnings
Grep: "[keywords]" in apex/tasks/*/<future-agent-notes>
Grep: "<problem>.*[keywords]" in apex/tasks/*.md
Grep: "<decision>.*[keywords]" in apex/tasks/*.md
Grep: "<gotcha>.*[keywords]" in apex/tasks/*.md
```
</search-strategy>

<if-similar-found>
Display to user:
```
Found potentially related learnings:

1. [task-id]: "[Brief description of learning]"
2. [task-id]: "[Brief description of learning]"

Continue documenting? (These will be linked as related)
- Yes - Continue (will add to related_tasks)
- Skip - This is duplicate, don't document
```

Wait for user response before proceeding.
</if-similar-found>

<if-no-similar>
Proceed directly to step 3.
</if-no-similar>
</step>

<step id="3" title="Gather learnings from session">
<instructions>
Review the task file and conversation to identify:

**Problems Encountered**:
- What broke or didn't work as expected?
- What symptoms were observed?
- What was the root cause?
- How was it fixed?
- How can it be prevented in future?

**Decisions Made**:
- What architectural or implementation choices were made?
- What alternatives were considered?
- Why was this choice made over others?

**Gotchas Discovered**:
- What surprised you or was counterintuitive?
- What looked like X but actually was Y?
- What documentation was misleading or missing?
</instructions>

<gathering-prompts>
Ask yourself:
1. "What would have saved time if I knew it at the start?"
2. "What mistake did we make that future agents should avoid?"
3. "What decision required significant thought that future agents can reuse?"
4. "What behavior was unexpected or undocumented?"
</gathering-prompts>

<minimum-threshold>
Only document if there's at least ONE meaningful learning.
If the task was trivial with nothing surprising, say:
"No significant learnings to capture from this session."
</minimum-threshold>
</step>

<step id="4" title="Structure learnings">
<format>
```xml
<future-agent-notes>
  <timestamp>[ISO timestamp]</timestamp>

  <problems>
    <problem>
      <what>[Clear description of the problem]</what>
      <symptoms>
        - [Observable sign 1]
        - [Observable sign 2]
      </symptoms>
      <root-cause>[Why it happened]</root-cause>
      <solution>[What fixed it]</solution>
      <prevention>[How to avoid in future]</prevention>
    </problem>
  </problems>

  <decisions>
    <decision>
      <choice>[What we chose]</choice>
      <alternatives>[What we considered]</alternatives>
      <rationale>[Why this choice - be specific]</rationale>
    </decision>
  </decisions>

  <gotchas>
    <gotcha>[Surprising thing - be specific and actionable]</gotcha>
  </gotchas>
</future-agent-notes>
```
</format>

<quality-rules>
- Be specific, not vague ("Missing index on users.organization_id" not "database was slow")
- Include actionable prevention/rationale
- Skip empty sections (don't include `<problems>` if no problems)
- Each item should be self-contained and understandable without full context
</quality-rules>
</step>

<step id="5" title="Write to task file">
<instructions>
1. Read current task file
2. Append `<future-agent-notes>` section after `<ship>` (or last existing section)
3. Update frontmatter with `related_tasks` if similar tasks were found in step 2

**Frontmatter update** (if related tasks found):
```yaml
---
# ... existing frontmatter ...
related_tasks: [task-id-1, task-id-2]
---
```
</instructions>

<confirmation>
Display captured learnings:
```
Learnings captured:

Problems (N):
- [Brief summary of each]

Decisions (N):
- [Brief summary of each]

Gotchas (N):
- [Brief summary of each]

Related tasks linked: [list or "none"]
```
</confirmation>
</step>

<step id="6" title="Offer promotion to AGENTS.md">
<purpose>
Critical learnings should be "always loaded" context in AGENTS.md.
</purpose>

<promotion-prompt>
```
Promote any to AGENTS.md? (These become "always loaded" context)

1. [Problem] [Brief description]
2. [Decision] [Brief description]
3. [Gotcha] [Brief description]
N. None - done

Select (numbers comma-separated, or N for none):
```
</promotion-prompt>

<selection-handling>
- If "N" or "none": Skip to final step
- If numbers selected: Proceed to promotion
</selection-handling>
</step>

<step id="7" title="Promote to AGENTS.md">
<instructions>
1. Read AGENTS.md fully
2. Find `## Learnings` section (create at end if doesn't exist)
3. Check for duplicates (don't add if similar already exists)
4. Append selected items in condensed format
5. Write updated AGENTS.md
</instructions>

<promotion-format>
```markdown
## Learnings

<!-- Auto-generated by /apex:compound. Do not edit directly. -->

### Problems

- **[Short title]** - [1-2 sentence description with actionable prevention]. (from [task-id], [date])

### Decisions

- **[Choice made]** - [1-2 sentence rationale]. (from [task-id], [date])

### Gotchas

- **[Short title]** - [1-2 sentence explanation]. (from [task-id], [date])
```
</promotion-format>

<grouping-rules>
- Group by type (Problems, Decisions, Gotchas)
- Create subsection if doesn't exist
- Append to existing subsection if it exists
- Always include source task and date
</grouping-rules>

<duplicate-check>
Before adding, search for similar content:
```bash
Grep: "[key phrase from learning]" in AGENTS.md
```
If similar exists, skip with message: "Similar learning already in AGENTS.md, skipping."
</duplicate-check>
</step>

<step id="8" title="Final confirmation">
<template>
**Knowledge Captured**

Task: [identifier]

Learnings documented:
- Problems: [N]
- Decisions: [N]
- Gotchas: [N]

Related tasks: [list or "none"]
Promoted to AGENTS.md: [list or "none"]

These learnings will be surfaced by `learnings-researcher` in future `/apex:research` runs.
</template>
</step>

</workflow>

<success-criteria>
- Task file read and context gathered
- Existing learnings checked for duplicates
- Meaningful learnings identified (or explicitly none)
- `<future-agent-notes>` section written to task file
- `related_tasks` updated in frontmatter if applicable
- Promotion to AGENTS.md offered
- Selected items promoted with proper format
- Duplicates avoided in AGENTS.md
</success-criteria>

<when-to-use>
- After `/apex:ship` completes (ship will prompt you)
- After debugging sessions
- After any significant problem-solving
- After making architectural decisions
- When you discover something surprising
- Anytime knowledge would help future agents
</when-to-use>

</skill>
