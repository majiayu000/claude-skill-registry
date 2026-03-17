---
name: df:debug
description: |
  Systematic debugging with persistent state across context resets.
  Use when the user reports a bug, error, or something not working as expected.
  Triggers on: "debug this", "something's broken", "fix this bug", "not working", "there's an error", "why isn't this working?"
argument-hint: [issue description]
allowed-tools:
  - Read
  - Bash
  - Task
  - AskUserQuestion
---

<objective>
Debug issues using scientific method with subagent isolation.

**Orchestrator role:** Gather symptoms, spawn df-debugger agent, handle checkpoints, spawn continuations.

**Why subagent:** Investigation burns context fast (reading files, forming hypotheses, testing). Fresh 200k context per investigation. Main context stays lean for user interaction.
</objective>

<context>
User's issue: $ARGUMENTS

Check for active sessions:
```bash
ls .planning/debug/*.md 2>/dev/null | grep -v resolved | head -5
```
</context>

<process>

## 0. Initialize Context

```bash
INIT=$(node ~/.claude/devflow/bin/df-tools.cjs state load)
```

Extract `commit_docs` from init JSON. Resolve debugger model:
```bash
DEBUGGER_MODEL=$(node ~/.claude/devflow/bin/df-tools.cjs resolve-model df-debugger --raw)
```

## 1. Check Active Sessions

If active sessions exist AND no $ARGUMENTS:
- List sessions with status, hypothesis, next action
- User picks number to resume OR describes new issue

If $ARGUMENTS provided OR user describes new issue:
- Continue to symptom gathering

## 2. Gather Symptoms (if new issue)

**Step 2a: What happens? (structured)**

Use AskUserQuestion:
- header: "Symptom"
- question: "What happens when the issue occurs?"
- multiSelect: false
- options:
  - "Nothing happens" — Expected action produces no result
  - "Wrong output" — Something happens but it's incorrect
  - "Error displayed" — An error message or crash occurs
  - "Partial success" — Some parts work, others don't

**Step 2b: Impact (structured)**

Use AskUserQuestion:
- header: "Impact"
- question: "How does this affect your workflow?"
- multiSelect: false
- options:
  - "Completely blocked" — Cannot continue without fixing this
  - "Workaround exists" — Can work around it but it's painful
  - "Cosmetic issue" — Functionality works, appearance is wrong
  - "Intermittent" — Sometimes works, sometimes doesn't

**Step 2c: Expected behavior (freeform)**

Ask inline: "What should happen instead? Describe the expected behavior."

**Step 2d: Error details (freeform)**

Ask inline: "Any error messages? Paste them or describe what you see."

**Step 2e: Reproduction (freeform)**

Ask inline: "How do you trigger this? What steps reproduce the issue?"

After all gathered, confirm ready to investigate.

## 3. Spawn df-debugger Agent

Fill prompt and spawn:

```markdown
<objective>
Investigate issue: {slug}

**Summary:** {trigger}
</objective>

<symptoms>
expected: {expected}
actual: {actual}
errors: {errors}
reproduction: {reproduction}
timeline: {timeline}
</symptoms>

<mode>
symptoms_prefilled: true
goal: find_and_fix
</mode>

<debug_file>
Create: .planning/debug/{slug}.md
</debug_file>
```

```
Task(
  prompt=filled_prompt,
  subagent_type="df-debugger",
  model="{debugger_model}",
  description="Debug {slug}"
)
```

## 4. Handle Agent Return

**If `## ROOT CAUSE FOUND`:**
- Display root cause and evidence summary
- Offer options:
  - "Fix now" - spawn fix subagent
  - "Plan fix" - suggest /df:plan-objective --gaps
  - "Manual fix" - done

**If `## CHECKPOINT REACHED`:**
- Present checkpoint details to user
- Get user response
- Spawn continuation agent (see step 5)

**If `## INVESTIGATION INCONCLUSIVE`:**
- Show what was checked and eliminated
- Offer options:
  - "Continue investigating" - spawn new agent with additional context
  - "Manual investigation" - done
  - "Add more context" - gather more symptoms, spawn again

## 5. Spawn Continuation Agent (After Checkpoint)

When user responds to checkpoint, spawn fresh agent:

```markdown
<objective>
Continue debugging {slug}. Evidence is in the debug file.
</objective>

<prior_state>
Debug file: @.planning/debug/{slug}.md
</prior_state>

<checkpoint_response>
**Type:** {checkpoint_type}
**Response:** {user_response}
</checkpoint_response>

<mode>
goal: find_and_fix
</mode>
```

```
Task(
  prompt=continuation_prompt,
  subagent_type="df-debugger",
  model="{debugger_model}",
  description="Continue debug {slug}"
)
```

</process>

<success_criteria>
- [ ] Active sessions checked
- [ ] Symptoms gathered (if new)
- [ ] df-debugger spawned with context
- [ ] Checkpoints handled correctly
- [ ] Root cause confirmed before fixing
</success_criteria>
