---
name: changelog
description: Set up git-cliff for automated changelog generation. Use `/changelog init` to initialize in a new project.
argument-hint: init
allowed-tools: Bash, Read, Write, Edit
user-invocable: true
---

# Changelog Skill

Manage automated changelog generation using git-cliff for ZeroAE projects.

## Commands

| Command | Description |
|---------|-------------|
| `/changelog init` | Set up git-cliff in a new project |

## init

Set up git-cliff configuration and GitHub Actions workflow.

### Process

1. **Check Current State**
```bash
ls cliff.toml 2>/dev/null
ls .github/workflows/release.yml 2>/dev/null
```

2. **Create cliff.toml**

If missing, create `cliff.toml` in project root using [cliff-config.toml](cliff-config.toml).

3. **Update Release Workflow**

If `.github/workflows/release.yml` exists, add the changelog generation step from [workflow-snippet.yml](workflow-snippet.yml).

If no release workflow exists, inform the user they need to create one first.

4. **Verify Setup**
```bash
git cliff --unreleased
```

### Output

Report what was created/updated and any manual steps needed.

## Reference Files

- [cliff-config.toml](cliff-config.toml) - Standard git-cliff configuration
- [workflow-snippet.yml](workflow-snippet.yml) - GitHub Actions release job snippet
