---
name: project-commands
description: Manages project-specific commands for development, testing, and deployment. Use when needing to run project commands or when setting up commands for a new project.
---

# Project Commands Skill

This skill helps agents find and use the correct commands for the current project.

## Finding Commands

All project-specific commands are defined in `.claude/commands.md`. Always read this file before running commands.

```bash
# Read the commands file
cat .claude/commands.md
```

## Command Categories

### Development
- **Install**: Set up project dependencies
- **Dev**: Start development server
- **Build**: Create production build

### Testing
- **Test**: Run all tests
- **Test:unit**: Unit tests only
- **Test:e2e**: End-to-end tests (Playwright)
- **Test:coverage**: Tests with coverage report

### Code Quality
- **Lint**: Check code style
- **Format**: Auto-format code
- **Typecheck**: Verify types

## Setting Up Commands for a New Project

1. Copy the template:
```bash
cp .claude/commands.template.md [target-project]/.claude/commands.md
```

2. Replace placeholders with actual commands:
```
{{install}} → npm install (or yarn, pnpm, etc.)
{{dev}} → npm run dev
{{dev_url}} → http://localhost:3000
{{test}} → npm test
```

3. Remove unused sections (database, docker, etc.)

## Common Patterns by Stack

### Node.js / npm
```
{{install}}: npm install
{{dev}}: npm run dev
{{test}}: npm test
{{build}}: npm run build
```

### Python / pip
```
{{install}}: pip install -r requirements.txt
{{dev}}: python manage.py runserver
{{test}}: pytest
{{build}}: python setup.py build
```

### Go
```
{{install}}: go mod download
{{dev}}: go run .
{{test}}: go test ./...
{{build}}: go build
```

### Rust
```
{{install}}: cargo build
{{dev}}: cargo run
{{test}}: cargo test
{{build}}: cargo build --release
```

## Agent Usage

When an agent needs to run a command:

1. Check `.claude/commands.md` for the correct command
2. Use the command exactly as specified
3. If a command is missing, ask the user or check `package.json`/equivalent

## Updating Commands

If you discover the correct command for an action:
1. Update `.claude/commands.md` with the correct command
2. Ensure other agents can find it in the future