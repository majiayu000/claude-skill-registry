---
name: dogfood-skills
description: |
  Enforces dogfooding for the skills CLI project. Use when working on
  packages/skills-cli or packages/skills-library. Reminds Claude to run
  `skills scan` and install recommended skills after completing features.
  Triggers on: feature completion, session end, or when reminded.
category: development
user-invocable: true
---

# Dogfood Skills CLI

You are working on the skills CLI project. You MUST use the tools you build.

## Core Principle

This project builds tools for discovering and installing Claude skills. If you don't use these tools yourself, you:
1. Miss bugs and UX issues
2. Don't understand user pain points
3. Fail to validate the value proposition
4. Undermine the project's credibility

## Mandatory Actions

### After Completing Any Feature/Bugfix

1. **Run scan**: `./packages/cli/bin/skills.js scan`
2. **Review recommendations**: Look at HIGH CONFIDENCE matches
3. **Install relevant skills**: `./packages/cli/bin/skills.js scan --all`
4. **If skipping**: Document reason in your response

### Rationalizations (Do Not Skip)

| Rationalization | Why It's Wrong | Required Action |
|-----------------|----------------|-----------------|
| "I'll install later" | You said that last time. And the time before. | Install NOW |
| "I forgot" | Hook exists to remind you. Pay attention. | Run scan immediately |
| "Not relevant to current work" | Scan output shows relevance scores | Justify with evidence from scan output |
| "Too many skills" | Deduplication exists | Use `--show-alternatives` to choose best |
| "Just a small change" | Small changes compound | Scan takes 10 seconds |
| "Tests are passing" | Tests don't verify dogfooding | Run scan anyway |

## Blocking Condition

If you complete a feature without running `skills scan`:

**BLOCKED: DOGFOODING REQUIRED**

You cannot proceed to the next task until you:
1. Run `./packages/cli/bin/skills.js scan`
2. Acknowledge recommendations (list them)
3. Install OR justify skipping each HIGH confidence recommendation

## When to Run Scan

- After implementing a new feature
- After fixing a bug
- After refactoring code
- At the end of a work session
- When the user mentions skills or recommendations
- When this skill is invoked via `/dogfood-skills`

## Quality Check

At end of each session, ask yourself:
- Did I run `skills scan`?
- Did I review the recommendations?
- Did I install recommended skills?
- Did I use installed skills during work?

If any answer is "no", run the scan now before ending.

## Commands Reference

```bash
# Scan for recommended skills
./packages/cli/bin/skills.js scan

# Scan and show all matches (not just top per category)
./packages/cli/bin/skills.js scan --show-alternatives

# Install all high-confidence recommendations
./packages/cli/bin/skills.js scan --all

# List currently installed skills
./packages/cli/bin/skills.js list

# Get help
./packages/cli/bin/skills.js --help
```

## Integration with Other Skills

This skill works alongside:
- **claudeception**: Extract learnings into new skills
- **tdd**: Write tests before fixes (RED → GREEN → REFACTOR)
- **unit-test-workflow**: Generate comprehensive tests

After installing new skills, USE them in your workflow.
