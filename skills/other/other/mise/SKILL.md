---
name: mise
description: >-
  Manage tool versions and tasks with mise (formerly rtx). Use when a user asks to manage Node.js/Python/Go versions per project, replace nvm/pyenv/asdf, or define project-level tool requirements.
license: Apache-2.0
compatibility: 'Linux, macOS, WSL'
metadata:
  author: terminal-skills
  version: 1.0.0
  category: development
  tags:
    - mise
    - version-manager
    - asdf
    - nvm
    - polyglot
---

# mise

## Overview
mise manages tool versions — Node.js, Python, Go, Rust, Ruby, etc. One tool replaces nvm, pyenv, rbenv, and asdf. Also runs project tasks.

## Instructions

### Step 1: Install
```bash
curl https://mise.run | sh
echo 'eval "$(mise activate bash)"' >> ~/.bashrc
```

### Step 2: Configuration
```toml
# mise.toml — Project tool versions and tasks
[tools]
node = "20"
python = "3.12"
go = "1.22"

[env]
DATABASE_URL = "postgresql://localhost/myapp"

[tasks.dev]
run = "npm run dev"

[tasks.test]
run = "npm test"
```

```bash
mise install    # install all tools
mise run dev    # run task
```

## Guidelines
- mise is 10-100x faster than asdf (Rust vs bash).
- Reads .tool-versions, .node-version, .python-version — drop-in replacement.
- Tasks in mise.toml replace Makefiles and package.json scripts.
