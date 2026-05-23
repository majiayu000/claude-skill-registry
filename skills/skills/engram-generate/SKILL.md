---
name: engram-generate
description: |
  Generate project-specific skills from Claude Code session history.
  Use when: (1) starting work on a new-to-you codebase, (2) onboarding to a project,
  (3) capturing learned patterns for future sessions.
category: workflow
disable-model-invocation: false
user-invocable: true
allowed-tools: Read, Bash, Write, Edit, Glob
---

# Engram Generate

Generate project-specific skills by analyzing Claude Code session history.

## When to Use

- Starting work on a codebase you've worked on before
- Onboarding to a project (after initial exploration sessions)
- Periodically to capture evolving conventions
- Before handing off a project to another agent

## Workflow

### Step 1: Generate a skill from history

```bash
npx engram generate-skill --workspace . --days 30
```

This analyzes your Claude Code sessions and generates a SKILL.md encoding:
- Files that are frequently edited together
- Test and build commands used
- Common tool sequences
- Error patterns and their fixes

### Step 2: Review the generated skill

The skill is created in `generated-skills/<project>-conventions/SKILL.md`.

Review it for accuracy:
- Remove any sensitive information
- Correct any misidentified patterns
- Add missing conventions you know about

### Step 3: Install the skill

```bash
# Copy to your skills directory
cp -r generated-skills/<project>-conventions ~/.claude/skills/

# Or use the skills CLI
skills add ./generated-skills/<project>-conventions
```

### Step 4: Keep it updated

Re-run periodically (e.g., monthly) to capture new patterns:

```bash
npx engram generate-skill --workspace . --days 30 --update
```

## Integration with Skills CLI

Use with `skills sync` to keep generated skills up to date:

```bash
# Add engram as a skill source
skills source add https://github.com/bobamatcha/engram

# Sync skills from engram
skills sync engram-recall engram-generate
```

## Output

The generated skill includes:

| Section | What It Contains |
|---------|------------------|
| **Files Often Changed Together** | File co-edit patterns |
| **Testing** | Test commands used in this project |
| **Building** | Build/compile commands |
| **Common Workflows** | Frequent tool sequences |
| **Common Issues** | Error patterns and fixes |

## Integration with Other Skills

| Skill | When to Combine |
|-------|-----------------|
| **engram-recall** | Use recall before generate to review history |
| **describe-codebase** | Generate after describing to capture conventions |
| **project-init** | Generate skill after initial project setup |

## Example Output

```markdown
# myproject Conventions

## Files Often Changed Together
- `src/index.ts` → also check: `src/types.ts`, `tests/index.test.ts`

## Testing
```bash
npm test
npm run test:watch
```

## Common Workflows
- Read → Edit → Bash (used 15x)
- Write → Bash → Read (used 8x)
```

## Important

- Generated skills are starting points — refine them
- Don't include sensitive paths or credentials
- Update skills when project structure changes significantly
