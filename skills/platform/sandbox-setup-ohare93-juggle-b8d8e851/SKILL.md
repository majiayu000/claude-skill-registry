---
name: sandbox-setup
description: Configure Claude Code sandbox settings for this repository
---

# Sandbox Setup Skill

Configure Claude Code for optimal autonomous agent execution in this repository.

## What This Skill Does

1. **Analyzes your codebase** to detect:
   - Programming languages (Go, Python, Node.js, Rust, etc.)
   - Package managers (go mod, npm, pip, cargo, etc.)
   - Build tools and test runners
   - Dev servers and their ports

2. **Generates tailored permissions** for `.claude/settings.json`:
   - Allow commands for detected tools
   - Network access for package registries
   - File system permissions for build outputs

3. **Preserves existing settings**:
   - Merges with hooks configuration
   - Keeps deny rules for secrets
   - Maintains ask rules for git push

## How to Use

When invoked, I will:
1. Scan the repository for configuration files (package.json, go.mod, Cargo.toml, requirements.txt, etc.)
2. Ask clarifying questions about your workflow
3. Present proposed settings for your approval
4. Update .claude/settings.json

## Detection Patterns

I look for these files to detect your stack:
- `go.mod` → Go (go build, go test, go mod)
- `package.json` → Node.js (npm, yarn, pnpm, node)
- `Cargo.toml` → Rust (cargo build, cargo test)
- `requirements.txt` / `pyproject.toml` → Python (pip, python, pytest)
- `Gemfile` → Ruby (bundle, ruby, rake)
- `pom.xml` / `build.gradle` → Java (mvn, gradle)
- `devbox.json` → Devbox (devbox run)

## Settings Structure

The generated settings follow this structure:
```json
{
  "sandbox": {
    "enabled": true,
    "autoAllowBashIfSandboxed": true
  },
  "permissions": {
    "allow": ["Bash(detected-tools:*)"],
    "deny": ["Read(./.env)", "Read(./secrets/**)"],
    "ask": ["Bash(juggle agent:*)", "Bash(git push:*)"]
  },
  "hooks": { ... }
}
```

## Reference

For detailed sandbox configuration options, see:
https://www.nathanonn.com/claude-code-sandbox-explained/
