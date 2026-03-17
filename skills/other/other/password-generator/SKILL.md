---
name: password-generator
description: 生成安全密码和密码短语，支持自定义长度、字符集和熵计算。
metadata:
  short-description: 生成安全密码
source:
  repository: https://github.com/python/cpython
  license: PSF
---

# Password Generator Tool

## Description
Generate cryptographically secure passwords with customizable options including length, character sets, and passphrase generation.

## Trigger
- `/password` command
- User needs to generate passwords
- User wants secure random strings

## Usage

```bash
# Generate random password
python scripts/password_generator.py --length 16

# Generate with specific character sets
python scripts/password_generator.py --length 20 --uppercase --lowercase --digits --symbols

# Generate passphrase
python scripts/password_generator.py --passphrase --words 4

# Generate multiple passwords
python scripts/password_generator.py --count 5 --length 12

# Generate PIN
python scripts/password_generator.py --pin --length 6
```

## Tags
`password`, `security`, `random`, `generator`, `crypto`

## Compatibility
- Codex: ✅
- Claude Code: ✅
