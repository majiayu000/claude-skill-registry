---
name: common
description: Shared utilities for Gemini-based skills including API key management, Vertex AI configuration, and client helpers. Use as dependency for skills requiring Gemini API access.
---

# Common Skill Utilities

Thư viện dùng chung cho các skills sử dụng Gemini API.

## Capabilities

- **API Key Management** (quản lý API key) – Tự động tìm `GEMINI_API_KEY` từ nhiều nguồn
- **Vertex AI Support** (hỗ trợ Vertex AI) – Chuyển đổi giữa AI Studio và Vertex AI
- **Client Helpers** (trợ giúp client) – Tự động khởi tạo client phù hợp

## Usage

```python
import sys
from pathlib import Path

# Thêm common directory vào path
common_dir = Path(__file__).parent.parent.parent / 'common'
sys.path.insert(0, str(common_dir))

from api_key_helper import get_api_key_or_exit, get_client, get_vertex_config

# Lấy API key
api_key = get_api_key_or_exit()

# Hoặc lấy client tự động
client_info = get_client()
```

## API Key Lookup Order

1. Process environment variable (`GEMINI_API_KEY`)
2. Project root `.env` file
3. `.claude/.env` file
4. `.claude/skills/.env` file
5. Skill directory `.env` file

## Vertex AI Configuration

```bash
export GEMINI_USE_VERTEX=true
export VERTEX_PROJECT_ID=your-gcp-project-id
export VERTEX_LOCATION=us-central1
```

## Files

- `api_key_helper.py` – Main utility module
- `README.md` – Detailed documentation
