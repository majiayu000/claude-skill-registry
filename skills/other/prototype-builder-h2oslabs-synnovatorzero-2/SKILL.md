---
name: prototype-builder
description: Quickly scaffold runnable prototype projects. Use when users want to create a new project skeleton, set up a tech stack, or bootstrap an application. Triggers include requests like "create a project", "set up a prototype", "scaffold an app", "build a [type] application", or specifying a tech stack combination.
---

# Prototype Builder

Scaffold runnable prototype projects with `make start` support.

## Workflow

1. **Understand the request** - Identify project type and tech stack
2. **Select or validate stack** - Use default or check user's choice
3. **Create project** - Copy template or generate dynamically
4. **Verify runnable** - Ensure `make start` works

## Project Types & Templates

| Type | Template | Command |
|------|----------|---------|
| Full-stack Web | `assets/nextjs-fastapi/` | Frontend + Backend |
| API Service | `assets/fastapi-simple/` | Backend only |
| CLI Tool | `assets/python-cli/` | Command-line app |

For other combinations, generate dynamically following the same patterns.

## Tech Stack Selection

### When user specifies a stack:
1. Check compatibility (see [references/tech-stack-guide.md](references/tech-stack-guide.md))
2. If reasonable → proceed
3. If problematic → explain concerns and suggest alternatives

### When user doesn't specify:
Select based on project type:
- **Web app** → Next.js + FastAPI
- **API service** → FastAPI
- **CLI tool** → Python

## Project Creation

### Default location
```
~/projects/<project-name>/
```

### Using templates
```bash
cp -r assets/<template>/* <target-path>/
```

Then customize:
1. Update `README.md` with project name/description
2. Adjust configuration as needed
3. Verify `make start` runs successfully

### Dynamic generation
For non-template stacks, create:
1. `Makefile` with `start`, `install` targets
2. Entry point file(s)
3. Dependency file (requirements.txt, package.json)
4. `.gitignore`
5. `README.md`

## Success Criteria

| Project Type | "make start" Result |
|--------------|---------------------|
| Web app | Browser shows page at localhost |
| API service | `/health` returns `{"status": "ok"}` |
| CLI tool | Runs and shows output |

## Boundaries

Do NOT:
- Write business logic code
- Configure production deployment
- Set up database migrations
- Add authentication systems
- Create complex architectures

Focus: Minimal runnable skeleton only.