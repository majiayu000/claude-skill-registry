---
name: env-manager
description: 管理环境变量和.env文件，支持验证、加密和模板生成。
metadata:
  short-description: 管理.env文件
source:
  repository: https://github.com/theskumar/python-dotenv
  license: BSD-3-Clause
---

# Environment Manager Tool

## Description
Manage environment variables and .env files with validation, encryption support, and template generation.

## Trigger
- `/env` command
- User needs to manage env vars
- User wants to work with .env files

## Usage

```bash
# List environment variables
python scripts/env_manager.py list

# Get specific variable
python scripts/env_manager.py get DATABASE_URL

# Set variable in .env
python scripts/env_manager.py set API_KEY "secret123" --file .env

# Generate .env.example
python scripts/env_manager.py template .env --output .env.example

# Validate .env file
python scripts/env_manager.py validate .env --required API_KEY,DB_URL
```

## Tags
`env`, `environment`, `dotenv`, `config`, `secrets`

## Compatibility
- Codex: ✅
- Claude Code: ✅
