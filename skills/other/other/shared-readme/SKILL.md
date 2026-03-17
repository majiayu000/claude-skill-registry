---
name: shared-readme
description: Generate comprehensive README.md with project overview, setup instructions, and usage documentation.
argument-hint: "[--platform mern|ios] [--minimal] [--badges]"
allowed-tools: Bash, Write, Read, Glob, Grep
---

## Purpose
Generate a well-structured README.md that helps users and contributors understand, set up, and use the project.

## Arguments
- `--platform <p>` — Target platform: `mern` or `ios` (auto-detected if not specified)
- `--minimal` — Generate minimal README (overview + setup only)
- `--badges` — Include status badges (CI, coverage, license)

## README sections

### Standard (all projects)
1. **Title + Description** — What is this project?
2. **Features** — Key capabilities
3. **Prerequisites** — Required tools and versions
4. **Quick Start** — Get running in 5 minutes
5. **Development** — Common commands
6. **Project Structure** — Directory overview
7. **Contributing** — How to contribute
8. **License** — Legal terms

### Platform-specific

**MERN additions:**
- Environment setup (.env)
- API documentation link
- Deployment instructions

**iOS additions:**
- Xcode version requirement
- Simulator/device setup
- Code signing notes

## Badges available
```markdown
![CI](https://github.com/user/repo/workflows/CI/badge.svg)
![Coverage](https://codecov.io/gh/user/repo/branch/main/graph/badge.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
```

## Workflow
1. Detect or specify platform
2. Scan project for structure
3. Extract info from package.json / Xcode project
4. Generate README sections
5. Add badges (if requested)
6. Write README.md

## Best practices enforced
- Clear, scannable structure
- Copy-paste ready commands
- Links to detailed documentation
- No stale information (generated from project)

## Output
- README.md created/updated
- Sections generated based on project

## Reference
For templates and examples, see `reference/shared-readme-reference.md`
