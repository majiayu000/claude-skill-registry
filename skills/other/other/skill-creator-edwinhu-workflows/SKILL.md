---
name: skill-creator
description: "This skill should be used when the user asks to 'create a skill', 'improve a skill', 'edit a skill', 'add enforcement patterns', 'audit skill enforcement', or needs to substantially create or edit any SKILL.md file."
hooks:
  PostToolUse:
    - matcher: "Edit|Write"
      hooks:
        - type: command
          command: "python3 ${CLAUDE_PLUGIN_ROOT}/hooks/plugin-validate.py"
        - type: command
          command: "python3 ${CLAUDE_PLUGIN_ROOT}/hooks/validate-skill-paths.py"
---

# Skill Creator (with Superpowers Enforcement)

This skill wraps the built-in `skill-creator:skill-creator` with enforcement pattern awareness from the superpowers framework. It adds an enforcement audit layer to the skill-creator's draft-test-iterate loop.

## When This Skill Applies

All skill creation and improvement work. This skill loads **instead of** the built-in skill-creator because it adds enforcement awareness that the built-in version lacks.

## Process

### Step 1: Classify the Skill

Before drafting, classify the skill being created:

| Type | Description | Enforcement Needs |
|------|-------------|-------------------|
| **Workflow skill** | Multi-phase process (like /dev, /ds, /writing) | High — needs Iron Laws, gates, rationalization tables |
| **Tool skill** | Wraps a tool or API (like readwise, wrds, bluebook) | Medium — needs Red Flags for common misuse |
| **Knowledge skill** | Domain knowledge reference (like ai-anti-patterns) | Low — needs trigger-only descriptions |

This classification determines how much enforcement audit to apply after each draft.

### Anti-Patterns: Read Before Drafting

!`cat ${CLAUDE_SKILL_DIR}/../../references/creator-anti-patterns.md`

### Step 1b: Check for Bang and Hook Opportunities

Before drafting, identify constraints that should be **mechanically enforced** rather than prompt-enforced:

#### Bang-Backtick Injection (`!`command``)

Use bangs to inject dynamic context at skill load time — the command runs before Claude sees the content:

| Use Case | Example |
|----------|---------|
| Environment detection | `!`if [ -f /.dockerenv ]; then echo "CONTAINER"; else echo "HOST"; fi`` |
| Inline reference files | `!`cat ${CLAUDE_SKILL_DIR}/../../references/constraints.md`` |
| Inject current state | `!`git branch --show-current`` |

Bangs only work in **top-level skills** loaded via `Skill()`. Internal skills loaded via `Read()` should use direct `Read()` instructions.

#### Scoped Hooks (PreToolUse / PostToolUse)

Hooks in skill frontmatter fire only while the skill is active — automatically cleaned up when the skill finishes. Use them for constraints that are **mechanically checkable**:

```yaml
hooks:
  PreToolUse:
    - matcher: "Write"
      hooks:
        - type: command
          command: "python3 $HOME/.claude/skills/my-skill/hooks/guard.py"
  PostToolUse:
    - matcher: "Edit|Write"
      hooks:
        - type: command
          command: "python3 ${CLAUDE_PLUGIN_ROOT}/hooks/lint.py"
```

| Enforce with Hook | Keep as Prompt |
|-------------------|----------------|
| File path/extension guards | Rationalization tables |
| Missing prerequisite file checks | Drive-aligned framing |
| Tool parameter validation | Red flags (judgment-based) |
| Post-edit lint/format checks | "Why" explanations |
| Outline-before-prose guards | Deviation rule classification |

**The principle:** if a constraint is mechanically checkable, enforce it with a hook. If it requires judgment or motivation, keep it as prompt text. Hooks cost zero tokens and can't be rationalized away.

### Step 2: Invoke the Built-in Skill Creator

Use the Skill tool to invoke the built-in skill-creator:

```
Skill(skill="skill-creator:skill-creator")
```

Follow its full process: capture intent, interview, draft SKILL.md, write test cases, run evals, iterate. The built-in skill-creator handles the eval loop — do not reimplement it.

### Step 3: Enforcement Audit (After Each Draft)

After writing or revising the skill draft (and before running test cases), audit it against the superpowers enforcement patterns. Read the enforcement checklist:

!`cat ${CLAUDE_SKILL_DIR}/../../references/enforcement-checklist.md`

Then score the draft using the process below.

#### For Workflow Skills (High Enforcement)

Score against all 12 patterns. Use the scoring template from the checklist. Focus on:

1. **Iron Laws** — Does the skill have absolute constraints for high-drift actions? Are they wrapped in `<EXTREMELY-IMPORTANT>` tags with strong framing? If they use soft language ("try to", "should", "consider"), they will be ignored — rewrite with action-masking language.

2. **Rationalization Tables** — Does the skill preempt the agent's excuses? The table must contain *actual excuses the agent generates*, not hypothetical ones. Observe failure modes in test runs, then add entries.

3. **Red Flags + STOP** — Are there pattern interrupts for observable wrong actions? Must target actions ("About to X"), not intentions ("Thinking about X").

4. **Gate Functions** — Does every phase transition have a verifiable exit condition? "Quality is sufficient" is not a gate. "File X contains string Y" is a gate.

5. **Trigger-Only Descriptions** — Does the description contain ONLY trigger phrases? If it contains a process summary, the agent will follow the short description instead of reading the body. This is the single most common skill design mistake.

6. **Drive-Aligned Framing** — Do verification steps use helpfulness-first framing? "Skipping X is NOT HELPFUL — [concrete user harm]" is stronger than "incorrect" or "premature" because it targets the model's strongest drive.

7. **Skill Dependencies** — Does each phase explicitly read and invoke the next phase? Without explicit chaining, the agent will stop and wait.

8. **No Pause Between Tasks** — Does the skill prevent "should I continue?" between tasks?

8b. **Flat Agent Dispatch** — If the skill spawns agents that perform multiple checks or tasks, does the skill spawn them ALL directly in parallel? Or does it spawn a "dispatcher" agent that spawns its own sub-agents? Three-layer delegation (skill → agent → sub-agents) fails because sub-sub-agent results don't reliably return. The orchestrator must spawn all agents directly. See workflow-creator's Iron Law of Flat Dispatch.

9. **Delete & Restart** — For protocol violations, does the skill mandate deletion of contaminated work?

10. **Staged Review Loops** — Do implementation sections have review loops with iteration limits?

11. **Flowcharts as Spec** — For complex processes, is there an ASCII diagram that serves as the authoritative definition?

**Critical gaps** = High-drift action + Absent/Weak enforcement. Fix these before running evals.

#### For Tool Skills (Medium Enforcement)

Score against patterns 2, 3, 5, and 10:

- **Rationalization Tables** — What are common misuse patterns? (e.g., using the wrong API endpoint, skipping authentication)
- **Red Flags + STOP** — What wrong actions can the agent take? (e.g., calling a destructive API without confirmation)
- **Trigger-Only Descriptions** — Keep description to triggers only
- **Staged Review Loops** — For multi-step tool interactions, add review after each step

#### For Knowledge Skills (Low Enforcement)

Score against pattern 5 only:

- **Trigger-Only Descriptions** — This is the most important pattern for knowledge skills. If the description summarizes the knowledge, the agent reads the summary instead of the full body.

### Step 4: Reconcile Tensions

The built-in skill-creator's writing advice and superpowers enforcement patterns have a genuine tension:

| skill-creator says | superpowers says | Resolution |
|---|---|---|
| "Explain the why, avoid heavy-handed MUSTs" | "Iron Laws use strongest framing available" | **Both are right for different contexts.** Use "explain the why" for standalone instructions. Use Iron Laws for high-drift actions where the agent will rationalize shortcuts. |
| "Keep the prompt lean" | "Add Rationalization Tables, Red Flags" | **Enforcement patterns go in the skill body, not the description.** Progressive disclosure keeps it lean — move detailed tables to `references/` if SKILL.md exceeds 500 lines. |
| "Generalize from feedback, don't overfit" | "Observe failure modes, add entries to tables" | **Rationalization Tables ARE generalization.** Each entry captures a class of failures, not a specific test case. |

When the built-in skill-creator suggests removing enforcement patterns because they're "not pulling their weight" or are "oppressively constrictive MUSTs," push back if the pattern addresses a real observed failure mode. The test: did an agent actually take the shortcut this pattern prevents? If yes, keep it.

### Step 5: Continue the Eval Loop

Return to the built-in skill-creator's process for running test cases, grading, and iterating. After each iteration's skill revision, re-run the enforcement audit (Step 3) on the updated draft.

During the eval loop, watch for enforcement iteration signals (see "Enforcement Iteration Signals" in the anti-patterns reference loaded above).

## References

- **Enforcement checklist**: `references/enforcement-checklist.md` (in plugin root) — Full 12-pattern reference with templates. Discover via: `${CLAUDE_SKILL_DIR}/../../references/enforcement-checklist.md`
- **Philosophy**: `PHILOSOPHY.md` (in plugin root) — Three pillars (phased decomposition, deterministic gates, adversarial review). Discover via: `${CLAUDE_SKILL_DIR}/../../PHILOSOPHY.md`
- **Built-in skill-creator**: Handles the eval loop (draft → test → grade → iterate → description optimization)
