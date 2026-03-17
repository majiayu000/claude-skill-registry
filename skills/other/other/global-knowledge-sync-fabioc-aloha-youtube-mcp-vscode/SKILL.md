---
name: "Global Knowledge Sync"
description: "Synchronize insights between local projects and the Alex Global Knowledge repository"
---

# Global Knowledge Sync Skill

Manages bidirectional synchronization between local project knowledge and the centralized Alex Global Knowledge repository.

## First-Time Setup (New Users)

If you don't have a Global Knowledge repository yet, create one:

### Option 1: GitHub CLI (Recommended)
```powershell
cd C:\Development  # or your projects folder
gh repo create My-Global-Knowledge --private --description "Alex Global Knowledge Base" --clone
cd My-Global-Knowledge
```

### Option 2: Manual
1. Create a new private GitHub repo named `My-Global-Knowledge`
2. Clone it as a sibling to your projects

### Scaffold the Repository
After creating the repo, initialize the structure:

```powershell
# Create folders
mkdir patterns, insights, skills

# Create index.json
@'
{
  "version": "1.0.0",
  "lastUpdated": "$(Get-Date -Format 'yyyy-MM-ddTHH:mm:ssZ')",
  "entries": []
}
'@ | Out-File -FilePath index.json -Encoding utf8

# Create README
@'
# My Global Knowledge Base

Cross-project learnings for Alex Cognitive Architecture.

## Structure
- `patterns/` - Reusable solutions (GK-*.md)
- `insights/` - Timestamped learnings (GI-*.md)
- `skills/` - Skill registry for pull-sync
- `index.json` - Master search index

## Usage
- `/knowledge <query>` - Search knowledge
- `/saveinsight` - Save a learning
- `/promote` - Make local knowledge global
'@ | Out-File -FilePath README.md -Encoding utf8

# Commit
git add -A
git commit -m "feat: initialize global knowledge structure"
git push
```

## Repository Location

**Default**: The GK repo should be a sibling folder to your project workspace:
- Your Project: `C:\Development\YourProject\`
- Global Knowledge: `C:\Development\My-Global-Knowledge\`

**Configuration**: Set via `globalKnowledgeRepo` in `.github/config/alex-settings.json`

**Note**: All heirs inherit this skill — GK sync works in any Alex-enabled project.

## Capabilities

### 1. Save Insight to GK
Save a learning from the current project to global knowledge.

**Trigger**: `/saveinsight`, `save this insight`, `promote to global`

**Process**:
1. Capture insight title and content
2. Determine type: `pattern` (reusable) or `insight` (timestamped)
3. Assign category and tags
4. Generate file: `GK-{slug}.md` or `GI-{slug}-{date}.md`
5. Update `index.json` with metadata
6. Commit to GK repo (optional auto-push)

### 2. Search Global Knowledge
Find relevant knowledge from past projects.

**Trigger**: `/knowledge <query>`, `have I solved this before?`

**Process**:
1. Search `index.json` for matching entries (title, tags, summary)
2. Return top matches with links
3. Optionally read full content

### 3. Sync During Dream
Automated sync during dream/meditation cycles.

**Trigger**: Dream protocol, meditation consolidation

**Process**:
1. Check for uncommitted changes in GK repo
2. Pull latest from remote
3. Regenerate `KNOWLEDGE-INDEX.md` if entries changed
4. Report sync status in dream output

### 4. Promote Local Skill to Global
Promote a project's skill file to global pattern.

**Trigger**: `/promote`, `make this global`

**Process**:
1. Select local file from `.github/skills/` or skill
2. Convert to GK format with proper frontmatter
3. Add source project attribution
4. Save to `patterns/` folder

### 5. Skill Pull-Sync (For Heirs)
Discover and pull new skills from the GK repository.

**Trigger**: `/checkskills`, session start (if auto-check enabled)

**Process**:
1. Read `skills/skill-registry.json` from GK
2. Compare against local skills
3. Report new/updated skills available
4. Pull on demand via `/pullskill <id>`

**Registry Structure** (`skills/skill-registry.json`):
```json
{
  "version": "1.0.0",
  "skills": [
    {
      "id": "skill-development",
      "version": "1.0.0",
      "inheritance": "inheritable",
      "priority": "core",
      "source": "master-alex"
    }
  ],
  "wishlist": [...],
  "projectTypeMatching": {...}
}
```

**Project-Skill Matching**:
Heirs detect project type and recommend relevant wishlist skills. See [skill-development](.github/skills/skill-development/SKILL.md) for full protocol.

## Integration Points

### Dream Protocol
Add to dream checklist:
```markdown
- [ ] GK sync: Pull latest, check uncommitted, regenerate index
```

### Meditation Protocol
During consolidation, prompt:
- "Any insights worth saving globally?"
- Auto-detect cross-project patterns

### Upgrade Process
When upgrading a project:
1. Check if project has relevant GK entries
2. Suggest applicable patterns
3. Note project in `relatedProjects` of used entries

## File Formats

### Pattern (GK-*)
```markdown
# Pattern Title

**ID**: GK-pattern-slug
**Category**: category-name
**Tags**: tag1, tag2, tag3
**Source**: Original project name
**Created**: 2026-02-06T12:00:00Z

---

## Description
What this pattern solves.

## Implementation
How to apply it.

## Examples
Code samples.
```

### Insight (GI-*)
```markdown
# Insight Title

**ID**: GI-insight-slug-2026-02-06
**Category**: category-name
**Tags**: tag1, tag2
**Source Project**: project-name
**Date**: 2026-02-06T12:00:00Z

---

## Context
What problem you were solving.

## Insight
What you learned.

## Applicability
When to use this again.
```

## Categories

| Category | Use For |
|----------|---------|
| `architecture` | System design, patterns, structure |
| `api-design` | REST, GraphQL, API patterns |
| `debugging` | Troubleshooting, diagnostics |
| `deployment` | CI/CD, infrastructure, publishing |
| `documentation` | Docs, diagrams, formatting |
| `error-handling` | Exception handling, recovery |
| `patterns` | Design patterns, reusable solutions |
| `performance` | Optimization, profiling |
| `refactoring` | Code improvement, cleanup |
| `security` | Auth, encryption, vulnerabilities |
| `testing` | Unit, integration, E2E |
| `tooling` | Dev tools, configuration |
| `general` | Everything else |

## Related Skills

- [meditation-facilitation](.github/skills/meditation-facilitation/SKILL.md) - Creates insights during meditation
- [bootstrap-learning](.github/skills/bootstrap-learning/SKILL.md) - Uses GK to accelerate learning
- [global-knowledge](.github/skills/global-knowledge/SKILL.md) - Core GK search capability
