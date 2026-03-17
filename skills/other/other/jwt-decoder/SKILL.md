---
name: jwt-decoder
description: 解码、验证和生成JWT令牌，支持多种算法。
metadata:
  short-description: JWT令牌工具
source:
  repository: https://github.com/jpadilla/pyjwt
  license: MIT
---

# JWT Decoder Tool

## Description
Decode, verify, and generate JWT (JSON Web Tokens) with support for HS256, RS256, and other algorithms.

## Trigger
- `/jwt` command
- User needs to decode JWT
- User wants to verify tokens

## Usage

```bash
# Decode JWT (no verification)
python scripts/jwt_decoder.py decode "eyJhbGciOiJIUzI1NiIs..."

# Verify JWT with secret
python scripts/jwt_decoder.py verify "eyJ..." --secret "your-secret"

# Generate JWT
python scripts/jwt_decoder.py generate --payload '{"sub": "user123"}' --secret "secret"
```

## Tags
`jwt`, `token`, `auth`, `decode`, `security`

## Compatibility
- Codex: ✅
- Claude Code: ✅
