---
name: mch-wrap
description: Meeting Context Hub session wrap-up. Focus on documentation updates.
---

# MCH Wrap

Meeting Context Hub project-specific session wrap-up. Focus on documentation updates.

## Execution Order

1. Check git status/diff
2. Analyze documentation updates (Task agent)
3. Integrate results and user selection
4. Execute selected actions

## Phase 1: Git Status

```bash
git status --short
git diff --stat HEAD~3
```

## Phase 2: Documentation Update Analysis

Analyze with Task(subagent_type="Explore"):

### AI Context (.claude/ai-context/)

| Change Type | Target |
|-------------|--------|
| Domain terms | .claude/ai-context/domain/glossary.json |
| Entity definitions | .claude/ai-context/domain/entities.json |
| Business rules | .claude/ai-context/domain/rules.json |
| Obsidian config | .claude/ai-context/integrations/obsidian.json |
| Slack integration | .claude/ai-context/integrations/slack.json |
| Notion integration | .claude/ai-context/integrations/notion.json |

### Project Documents

| Change Type | Target |
|-------------|--------|
| Architecture | CLAUDE.md → Architecture section |
| Naming conventions | CLAUDE.md → Naming Convention section |
| Core rules | CLAUDE.md → Core Rules section |
| Module guides | src/*/CLAUDE.md |

### Module CLAUDE.md Files

| Module | Check Items |
|--------|-------------|
| repositories/ | Interface list, rules |
| hooks/ | Hook list, usage |
| lib/ai/ | Prompt list, versions |
| storage/ | Implementation list, swap method |
| application/ | UseCase list |

## Phase 3: User Selection

AskUserQuestion:
- Execute documentation updates
- Create commit
- Both
- Skip

## Phase 4: Execution

Execute selected actions.

## Additional Checklist

- [ ] Zod schema version consistency
- [ ] Prompt version field updates
- [ ] Environment variable .env.local.example sync
