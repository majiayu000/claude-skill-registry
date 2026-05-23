---
name: plugin-creator
description: "This skill should be used when the user asks to 'create a plugin', 'scaffold a plugin', 'set up plugin structure', 'new plugin', 'add plugin components', or needs to substantially edit an existing plugin."
hooks:
  PostToolUse:
    - matcher: "Edit|Write"
      hooks:
        - type: command
          command: "python3 ${CLAUDE_PLUGIN_ROOT}/hooks/plugin-validate.py"
        - type: command
          command: "python3 ${CLAUDE_PLUGIN_ROOT}/hooks/validate-skill-paths.py"
---

# Plugin Creator (with Superpowers Enforcement)

This skill wraps the built-in `plugin-dev:create-plugin` with enforcement pattern awareness from the superpowers framework. It adds an enforcement audit layer and PostToolUse validation hooks that the built-in version lacks.

## Process

### Step 1: Classify the Plugin

Before drafting, classify what's being created or edited:

| Type | Description | Enforcement Needs |
|------|-------------|-------------------|
| **Full plugin** | New plugin with skills, hooks, commands, agents | High — needs enforcement across all components |
| **Skill addition** | Adding a skill to an existing plugin | Medium — needs skill-level enforcement audit |
| **Hook addition** | Adding hooks to an existing plugin | Medium — needs path validation, matcher coverage |
| **Component edit** | Substantial edit to existing plugin component | Medium — needs re-audit of affected enforcement |

### Anti-Patterns: Read Before Drafting

!`cat ${CLAUDE_SKILL_DIR}/../../references/creator-anti-patterns.md`

### Step 1b: Check for Bang and Hook Opportunities

Before drafting, identify constraints that should be **mechanically enforced** rather than prompt-enforced:

- **Bang-backtick injection** (`!`command``) — inject dynamic context at skill load time
- **Scoped hooks** (PreToolUse/PostToolUse) — fire only while the skill is active, auto-cleaned up

**The principle:** if a constraint is mechanically checkable, enforce it with a hook. If it requires judgment, keep it as prompt text.

### Step 2: Invoke the Built-in Plugin Creator

Use the Skill tool to invoke the built-in plugin creator:

```
Skill(skill="plugin-dev:create-plugin")
```

Follow its full process. The built-in creator handles the workflow — do not reimplement it.

### Step 3: Enforcement Audit (After Each Draft)

After writing or revising plugin components (and before final validation), audit against the superpowers enforcement patterns. Read the enforcement checklist:

!`cat ${CLAUDE_SKILL_DIR}/../../references/enforcement-checklist.md`

Then score the draft using the appropriate template:

#### For Plugin Skills

Score against all 12 patterns from the checklist. Focus especially on:

1. **Iron Laws** — Does each skill have absolute constraints for high-drift actions?
2. **Rationalization Tables** — Does each skill preempt the agent's excuses?
3. **Red Flags + STOP** — Are there pattern interrupts for observable wrong actions?
4. **Trigger-Only Descriptions** — Does each skill description contain ONLY trigger phrases, no process summary?
5. **Gate Functions** — Does every phase transition have a verifiable exit condition?

#### For Plugin Hooks

Verify:

1. **Matcher coverage** — Do hooks fire on the right tool events?
2. **Path validity** — Do hook commands use `${CLAUDE_PLUGIN_ROOT}` (not `${CLAUDE_SKILL_DIR}`)?
3. **Error handling** — Do hooks fail gracefully (non-zero exit blocks the action)?
4. **Scope** — Are hooks scoped to skills (frontmatter) or global (plugin.json)?

#### For Plugin Structure

Verify:

1. **plugin.json** — Valid manifest with correct version, name, description
2. **marketplace.json** — Version matches plugin.json in all locations
3. **Directory layout** — skills/, hooks/, commands/, agents/ as needed
4. **Path portability** — No hardcoded absolute paths in any component

### Step 4: Reconcile Tensions

**Tension resolution:** Enforcement patterns go in skill body (not description), implementation code goes in scripts/, names are descriptive but descriptions are trigger-only.

### Step 5: Continue Iteration

Return to the built-in plugin creator's process for validation and testing. After each iteration's revision, re-run the enforcement audit (Step 3).

During iteration, watch for enforcement iteration signals (see "Enforcement Iteration Signals" in the anti-patterns reference loaded above).

## References

- **Enforcement checklist**: `references/enforcement-checklist.md` (loaded above via bang injection)
- **Anti-patterns**: `references/creator-anti-patterns.md` (loaded above via bang injection)
- **Philosophy**: `references/PHILOSOPHY.md`
- **Built-in plugin creator**: `plugin-dev:create-plugin`
