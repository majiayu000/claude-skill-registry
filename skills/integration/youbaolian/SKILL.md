---
name: youbaolian
description: Manage youbaolian, orders, users, organ REST API.
homepage: https://cxv3-new.youbaolian.top
metadata: {"clawdbot":{"emoji":"📊","requires":{"bins":["jq","curl"],"env":["YBL_URL","YBL_CRYPTION"]}}}
---

# Youbaolian Skill

## Setup

1.Configure your ybl sever in `credentials.json`:
```json
{
    "name": "Server Ybl",
    "url": "https://cxv3-new.youbaolian.top",
    "account": {
        "encryption": "1W2VGiJLPZUQkBiPsbkwiT+fW9hD3IMKlrA9dhYKakG0shYmRHVYNpO3SKzbqwf6Iw8x067uaqXa2o+VTUrc9RpFeX5YJ5Y5jphtNWm00WhYjP3K5c3gkV+j/kqY2AP3WXF5IvKNFoNEiQkl71P9o8RLDoRzym+GFJMjE70psXEfM="
    }
}
```

2. Set environment variables:
   ```bash
   export YBL_URL="https://cxv3-new.youbaolian.top"
   export YBL_ENCRYPTION="1W2VGiJLPZUQkBiPsbkwiT+fW9hD3IMKlrA9dhYKakG0shYmRHVYNpO3SKzbqwf6Iw8x067uaqXa2o+VTUrc9RpFeX5YJ5Y5jphtNWm00WhYjP3K5c3gkV+j/kqY2AP3WXF5IvKNFoNEiQkl71P9o8RLDoRzym+GFJMjE70psXEfM="
   ```

3. Get authentication token:
   ```bash
   export TB_TOKEN=$(curl -s -X POST "$YBL_URL/insapi/v3/union/unionLoginEncryptionPortal" \
    -H "Content-Type: application/json" \
    -d "{\"encryption\":\"$YBL_ENCRYPTION\"}" | jq -r '.data.token')
   ```

## Usage

All commands use curl to interact with the Youbaolian REST API.


### Authentication

**Login and get token:**
```bash
curl -s -X POST "$YBL_URL/insapi/v3/union/unionLoginEncryptionPortal" \
  -H "Content-Type: application/json" \
  -d "{\"encryption\":\"$YBL_ENCRYPTION\"}" | jq -r '.data.token'
```