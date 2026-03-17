---
name: skill-forge
description: |
  When Claude discovers a non-obvious solution, unusual pattern, or hard-won
  insight during a session, automatically forge it into a new skill. Don't
  just note the learning - create the actual skill file so future sessions
  benefit immediately. This is the flywheel: work → discovery → skill → smarter
  future sessions → repeat.
allowed-tools: |
  bash: ls, cat, mkdir
  file: read, write
---

# Skill Forge

<purpose>
Knowledge that stays in one session is wasted. When Claude discovers something
non-obvious - a debugging technique, a gotcha, a pattern that works - it should
become a skill automatically. Not "maybe document this later" but "forge it now."

This is the flywheel that makes the skill library self-improving.
</purpose>

## When To Activate

Trigger when:

- Claude solves a problem that took multiple attempts
- Claude discovers a non-obvious pattern or gotcha
- A debugging session reveals something others would hit
- User says "we should remember this" or "make this a skill"
- Claude catches itself about to make a mistake it's made before
- A workaround is found for a tool/library limitation
- The solution was counter-intuitive

Do NOT trigger for:

- Obvious solutions anyone would find
- Project-specific knowledge (not generalizable)
- Things already covered by existing skills
- Minor learnings not worth the overhead

## Instructions

### Step 1: Identify the Insight

Capture what was learned:

```
Discovery: [One sentence summary]
Context: [What task/problem led to this]
Why non-obvious: [Why someone else would miss this]
Generalizable: [YES/NO - is this useful beyond this specific case?]
```

If not generalizable, stop - add to breadcrumbs instead, not a skill.

### Step 2: Extract the Pattern

Generalize from the specific case:

```
Specific case: [What happened here]
General pattern: [The reusable insight]
Triggers: [When should future Claude activate this]
```

### Step 3: Draft the Skill

Create the skill structure:

```markdown
---
name: [kebab-case-name]
description: |
  [2-3 sentence description that would trigger activation]
allowed-tools: |
  [appropriate tools]
---

# [Skill Name]

<purpose>
[Why this skill exists - the problem it prevents]
</purpose>

## When To Activate

Trigger when:
- [Condition 1]
- [Condition 2]

## Instructions

### Step 1: [First step]
[Instructions]

### Step 2: [Second step]
[Instructions]

## NEVER
- [Anti-pattern 1]

## ALWAYS
- [Required behaviour 1]

## Examples

### Example 1: [Scenario]
[Concrete example]

<failed-attempts>
What DOESN'T work:
- [Failed approach and why]
</failed-attempts>

## Origin
Forged from: [Brief description of the session/problem that spawned this]
```

### Step 4: Write the Skill File

Create the skill directory and file:

```
skills/[skill-name]/SKILL.md
```

### Step 5: Confirm Creation

```
Skill forged: [skill-name]
Location: skills/[skill-name]/SKILL.md
Trigger: [When it will activate]

This skill will now be available in future sessions.
```

## Quality Checks

Before forging, verify:

<quality-checks>
| Check | Requirement |
|-------|-------------|
| Generalizable | Useful beyond this specific project |
| Non-obvious | Not something Claude would naturally do |
| Actionable | Clear instructions, not just "be careful" |
| Triggered | Clear conditions for when to activate |
| Distinct | Not duplicate of existing skill |
</quality-checks>

## Skill Naming Conventions

<naming>
- Use kebab-case: `cache-invalidation`, not `cacheInvalidation`
- Be specific: `async-cleanup` not `async-stuff`
- Verb or noun that implies action: `trace-imports`, `validate-env`
- Avoid generic names: `helper`, `utils`, `misc`
</naming>

## NEVER

- Forge project-specific knowledge as skills (use breadcrumbs)
- Create skills for obvious things
- Forge without the `<failed-attempts>` section (failures teach)
- Create duplicate skills - check existing ones first
- Forge trivial learnings (overhead not worth it)

## ALWAYS

- Include the origin story (what spawned this skill)
- Add `<failed-attempts>` documenting what doesn't work
- Make triggers specific and unambiguous
- Test that the skill makes sense out of context
- Keep skills focused (one insight per skill)

## Examples

### Example 1: Debugging Discovery

During debugging, Claude discovers that a React hook was causing infinite
re-renders because of object reference comparison.

```
Discovery: useEffect with object dependency causes infinite loops
Context: Debugging React component that kept re-rendering
Why non-obvious: Object looks the same but reference changes each render
Generalizable: YES - common React gotcha

Forging skill: react-dependency-check
```

Resulting skill would include:
- Triggers: React debugging, infinite loops, useEffect issues
- Instructions: Check dependency array for objects/arrays
- Failed attempts: "Tried adding object directly to deps - still loops"

### Example 2: API Gotcha

Claude discovers that an API returns different formats based on count
(single object vs array).

```
Discovery: API returns object for 1 result, array for multiple
Context: Parsing API response failed on single-result queries
Why non-obvious: Only manifests with exactly one result
Generalizable: YES - common API pattern

Forging skill: api-response-normalization
```

### Example 3: Not Worth Forging

Claude fixes a typo in a config file.

```
Discovery: Config had typo in key name
Generalizable: NO - specific to this project

[Not forging - adding to breadcrumbs instead]
```

## The Flywheel

```
Session 1: Struggle with problem X
           ↓
         Solve it after 30 min
           ↓
         Forge skill "handle-X"
           ↓
Session 2: Encounter similar problem
           ↓
         skill-gate activates "handle-X"
           ↓
         Solved in 2 min
           ↓
         Time saved: 28 min
           ↓
         Compound over hundreds of sessions
```

## Integration with Other Skills

- **learn-from-this**: Analyzes failures, skill-forge turns them into skills
- **retrospective**: Reviews session, skill-forge captures key learnings
- **breadcrumbs**: For project-specific notes (not generalizable)
- **skill-gate**: Ensures forged skills get activated

## Why This Skill Exists

Every session, Claude learns things. Most of that knowledge evaporates when
the session ends. Skill-forge captures it.

The goal isn't to document everything - it's to capture the non-obvious wins
that would otherwise need to be rediscovered. Each forged skill is future
time saved.

Build the library. Close the loop. Make the system smarter over time.
