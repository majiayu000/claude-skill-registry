---
name: gitignore
description: Generates .gitignore file for Git version control exclusions. Defines files and directories to exclude from version control like node_modules, build artifacts, and local environment files.
---

# Git Ignore Skill

## Purpose
Generate the `.gitignore` file for version control exclusions.

## Output
Create the file: `.gitignore`

## Notes
- Excludes macOS system files (.DS_Store)
- Excludes node_modules and build artifacts (dist, dist-ssr)
- Excludes local environment files (.env.local, .env.*.local, .env)
- Excludes all editor directories (.vscode, .idea)
- Excludes log files from npm, yarn, and pnpm
- Excludes test coverage reports
- Excludes *.local files for local-only configurations
