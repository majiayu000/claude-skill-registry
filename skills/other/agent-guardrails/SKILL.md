---
name: agent-guardrails
version: "1.1.0"
author: "jzOcb"
license: "MIT"
category: "development-tools"
description: "Stop AI agents from secretly bypassing your rules. Mechanical enforcement with git hooks, secret detection, deployment verification, and import registries. Born from real production incidents: server crashes, token leaks, code rewrites. Works with Claude Code, Clawdbot, Cursor. Install once, enforce forever."
tags:
  - "ai-safety"
  - "code-quality"
  - "enforcement"
  - "git-hooks"
  - "deployment"
  - "security"
  - "automation"
  - "guardrails"
  - "claude-code"
  - "clawdbot"
  - "cursor"
  - "mechanical-enforcement"
  - "agent-reliability"
keywords:
  - "AI agent bypassing"
  - "code enforcement"
  - "git hooks automation"
  - "secret detection"
  - "deployment verification"
  - "import enforcement"
  - "mechanical guardrails"
  - "agent safety"
  - "production incidents"
  - "Claude Code skills"
  - "Clawdbot skills"
  - "AI coding safety"
repository: "https://github.com/jzOcb/agent-guardrails"
homepage: "https://github.com/jzOcb/agent-guardrails#readme"
bugs: "https://github.com/jzOcb/agent-guardrails/issues"
compatibility:
  - "claude-code"
  - "clawdbot"
  - "cursor"
  - "any-ai-agent"
requirements:
  bash: ">=4.0"
  git: ">=2.0"
pricing: "FREE"
---

# Agent Guardrails

Mechanical enforcement for AI agent project standards. Rules in markdown are suggestions. Code hooks are laws.

## Quick Start

```bash
cd your-project/
bash /path/to/agent-guardrails/scripts/install.sh
```

This installs the git pre-commit hook, creates a registry template, and copies check scripts into your project.

## Enforcement Hierarchy

1. **Code hooks** (git pre-commit, pre/post-creation checks) — 100% reliable
2. **Architectural constraints** (registries, import enforcement) — 95% reliable
3. **Self-verification loops** (agent checks own work) — 80% reliable
4. **Prompt rules** (AGENTS.md, system prompts) — 60-70% reliable
5. **Markdown rules** — 40-50% reliable, degrades with context length

## Tools Provided

### Scripts

| Script | When to Run | What It Does |
|--------|------------|--------------|
| `install.sh` | Once per project | Installs hooks and scaffolding |
| `pre-create-check.sh` | Before creating new `.py` files | Lists existing modules/functions to prevent reimplementation |
| `post-create-validate.sh` | After creating/editing `.py` files | Detects duplicates, missing imports, bypass patterns |
| `check-secrets.sh` | Before commits / on demand | Scans for hardcoded tokens, keys, passwords |
| `create-deployment-check.sh` | When setting up deployment verification | Creates .deployment-check.sh, checklist, and git hook template |
| `install-skill-feedback-loop.sh` | When setting up skill update automation | Creates detection, auto-commit, and git hook for skill updates |

### Assets

| Asset | Purpose |
|-------|---------|
| `pre-commit-hook` | Ready-to-install git hook blocking bypass patterns and secrets |
| `registry-template.py` | Template `__init__.py` for project module registries |

### References

| File | Contents |
|------|----------|
| `enforcement-research.md` | Research on why code > prompts for enforcement |
| `agents-md-template.md` | Template AGENTS.md with mechanical enforcement rules |
| `deployment-verification-guide.md` | Full guide on preventing deployment gaps |
| `skill-update-feedback.md` | Meta-enforcement: automatic skill update feedback loop |
| `SKILL_CN.md` | Chinese translation of this document |

## Usage Workflow

### Setting up a new project

```bash
bash scripts/install.sh /path/to/project
```

### Before creating any new .py file

```bash
bash scripts/pre-create-check.sh /path/to/project
```

Review the output. If existing functions cover your needs, import them.

### After creating/editing a .py file

```bash
bash scripts/post-create-validate.sh /path/to/new_file.py
```

Fix any warnings before proceeding.

### Setting up deployment verification

```bash
bash scripts/create-deployment-check.sh /path/to/project
```

This creates:
- `.deployment-check.sh` - Automated verification script
- `DEPLOYMENT-CHECKLIST.md` - Full deployment workflow
- `.git-hooks/pre-commit-deployment` - Git hook template

**Then customize:**
1. Add tests to `.deployment-check.sh` for your integration points
2. Document your flow in `DEPLOYMENT-CHECKLIST.md`
3. Install the git hook

See `references/deployment-verification-guide.md` for full guide.

### Adding to AGENTS.md

Copy the template from `references/agents-md-template.md` and adapt to your project.

## 中文文档 / Chinese Documentation

See `references/SKILL_CN.md` for the full Chinese translation of this skill.

## Common Agent Failure Modes

### 1. Reimplementation (Bypass Pattern)
**Symptom:** Agent creates "quick version" instead of importing validated code.
**Enforcement:** `pre-create-check.sh` + `post-create-validate.sh` + git hook

### 2. Hardcoded Secrets
**Symptom:** Tokens/keys in code instead of env vars.
**Enforcement:** `check-secrets.sh` + git hook

### 3. Deployment Gap
**Symptom:** Built feature but forgot to wire it into production. Users don't receive benefit.
**Example:** Updated `notify.py` but cron still calls old version.
**Enforcement:** `.deployment-check.sh` + git hook

This is the **hardest to catch** because:
- Code runs fine when tested manually
- Agent marks task "done" after writing code
- Problem only surfaces when user complains

**Solution:** Mechanical end-to-end verification before allowing "done."

### 4. **Skill Update Gap** (META - NEW)
**Symptom:** Built enforcement improvement in project but forgot to update the skill itself.
**Example:** Created deployment verification for Project A, but other projects don't benefit because skill wasn't updated.
**Enforcement:** `install-skill-feedback-loop.sh` → automatic detection + semi-automatic commit

This is a **meta-failure mode** because:
- It's about enforcement improvements themselves
- Without fix: improvements stay siloed
- With fix: knowledge compounds automatically

**Solution:** Automatic detection of enforcement improvements with task creation and semi-automatic commits.

## Key Principle

> Don't add more markdown rules. Add mechanical enforcement.
> If an agent keeps bypassing a standard, don't write a stronger rule — write a hook that blocks it.
>
> **Corollary:** If an agent keeps forgetting integration, don't remind it — make it mechanically verify before commit.
