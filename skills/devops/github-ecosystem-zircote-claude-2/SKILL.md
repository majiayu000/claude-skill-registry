---
name: github-ecosystem
description: Generate comprehensive GitHub ecosystem configuration including CI/CD workflows, issue templates, PR templates, CODEOWNERS, dependabot, and Copilot instructions. Language-agnostic with Python, Go, and TypeScript support. Auto-detects project language from pyproject.toml, go.mod, or package.json. Use when setting up GitHub repos, adding CI/CD pipelines, creating issue/PR templates, configuring dependabot, adding CODEOWNERS, setting up Copilot instructions, or enhancing existing projects with GitHub tooling. Works on new or existing repositories with smart merging.
---

# GitHub Ecosystem Configuration Generator

Generates production-ready GitHub configuration for any project.

## Quick Start

Run in a project directory to auto-detect language and generate configuration:
```bash
python scripts/generate_github_config.py --project-path .
```

## Supported Languages

| Language   | Detection Files               | CI Tools                           |
|------------|-------------------------------|------------------------------------|
| Python     | pyproject.toml, setup.py      | ruff, mypy, bandit, pytest         |
| Go         | go.mod                        | golangci-lint, go test             |
| TypeScript | package.json + tsconfig.json  | eslint, prettier, tsc, vitest/jest |

## Components

### GitHub Actions Workflows

**ci.yml** - Continuous Integration
- Multi-version test matrix
- Code quality checks (lint, format, typecheck)
- Security scanning
- Coverage reporting
- Build verification

**release.yml** (optional) - Release Automation
- Version bumping
- GitHub Release creation
- Package publishing
- Changelog generation

**docker.yml** (optional) - Container Builds
- Multi-platform builds (amd64, arm64)
- GHCR publishing
- Caching optimization

### Issue Templates

- **bug_report.md** - Structured bug reporting
- **feature_request.md** - Feature proposals with API examples
- **config.yml** - Template chooser configuration

### Other Templates

- **PULL_REQUEST_TEMPLATE.md** - PR checklist with change types
- **CODEOWNERS** - Code ownership definitions
- **dependabot.yml** - Automated dependency updates
- **copilot-instructions.md** - GitHub Copilot context

## Configuration Options

| Option | Default | Description |
|--------|---------|-------------|
| --project-path | . | Project directory |
| --language | (auto) | Force language: python, go, typescript |
| --components | all | Comma-separated: workflows,templates,dependabot,codeowners,copilot |
| --include-release | false | Include release workflow |
| --include-docker | false | Include docker workflow |
| --codeowners | (optional) | CODEOWNERS entries (e.g., "* @team") |
| --overwrite | false | Overwrite existing files |

## Enhancement Mode

When `.github/` already exists, the skill enters enhancement mode:
- Detects existing configuration
- Shows what will be added/modified
- Merges without overwriting (unless --overwrite)
- Preserves custom modifications

## Generated Structure

```
.github/
├── workflows/
│   ├── ci.yml              # Always generated
│   ├── release.yml         # With --include-release
│   └── docker.yml          # With --include-docker
├── ISSUE_TEMPLATE/
│   ├── bug_report.md
│   ├── feature_request.md
│   └── config.yml
├── PULL_REQUEST_TEMPLATE.md
├── CODEOWNERS              # With --codeowners
├── dependabot.yml
└── copilot-instructions.md
```

## Language-Specific Details

See reference files for detailed workflow patterns:
- `references/python-workflow.md` - Python CI/CD patterns
- `references/go-workflow.md` - Go CI/CD patterns
- `references/typescript-workflow.md` - TypeScript CI/CD patterns

## Post-Generation

After generation:
1. Review generated workflows for your needs
2. Add any required secrets (e.g., PYPI_API_TOKEN for publishing)
3. Customize version matrices if needed
4. Update CODEOWNERS with actual team handles
