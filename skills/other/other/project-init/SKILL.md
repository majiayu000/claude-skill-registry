---
name: Project Initialization Skill
description: Creates complete project structure with docs, templates, and workflow. Use when user says 'new project', 'init project', 'create project structure', or runs /new-project command.
---

# Project Initialization Skill

## Purpose

Initialize a new project from scratch with complete documentation structure, feature templates, and Claude Code workflow integration.

## Variables

```yaml
DEFAULT_STACK_BACKEND: Python, FastAPI
DEFAULT_STACK_FRONTEND: Gradio
DEFAULT_STACK_DB: PostgreSQL
DEFAULT_STACK_INFRA: Docker, GitHub Actions
```

## Instructions

### When to Use
- User says "new project", "init project", "create project structure"
- User runs `/new-project <ProjectName>`
- User wants to set up a repository from zero

### Workflow

1. **Gather Project Info** (if not provided):
   - Project name
   - One-liner description
   - Stack (or use defaults)
   - MVP scope (brief)

2. **Create Directory Structure**:
   ```
   Execute: .claude/skills/project-init/tools/create_structure.py
   ```

3. **Generate All Templates**:
   - Read each template from `templates/` folder
   - Create files with project name substituted

4. **Initialize Git** (if not already):
   ```bash
   git init
   git add .
   git commit -m "Initial project structure"
   ```

5. **Report Summary**:
   - List created files
   - Show next steps

## File Structure Created

```
{PROJECT}/
├── .claude/
│   ├── commands/
│   │   ├── new-feature.md
│   │   ├── interview.md
│   │   ├── plan.md
│   │   └── implement.md
│   └── settings.json
│
├── docs/
│   ├── project.md
│   ├── feature_cycle.md
│   │
│   ├── architecture/
│   │   └── _index.md
│   │
│   ├── features/
│   │   ├── _index.md
│   │   └── _template/
│   │       ├── spec.md
│   │       ├── design.md
│   │       ├── tasks.md
│   │       ├── tests.md
│   │       └── status.md
│   │
│   ├── sprints/
│   │   └── _index.md
│   │
│   └── decisions/
│       └── _index.md
│
├── src/
│   └── .gitkeep
├── tests/
│   └── .gitkeep
├── CLAUDE.md
└── README.md
```

## Post-Creation Next Steps

Tell user:
1. "Edit `docs/project.md` to define your project"
2. "Run `/new-feature FEAT-001-nombre` to create first feature"
3. "Follow the cycle in `docs/feature_cycle.md`"
