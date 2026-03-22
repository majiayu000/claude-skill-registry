---
name: hudy
description: "Korean public holidays and business day calculations via HuDy MCP. Query holidays, count business days, add/subtract business days, and manage custom holidays."
metadata:
  openclaw:
    requires:
      env:
        - HUDY_API_KEY
    primaryEnv: HUDY_API_KEY
---

# HuDy - Korean Holiday & Business Day Skill

Use the HuDy MCP server to query Korean public holidays, calculate business days, and manage custom holidays directly from your AI agent.

## Setup

### 1. Get an API Key

Sign up at [hudy.co.kr](https://www.hudy.co.kr) and create an API key from the dashboard.

### 2. Connect MCP

**Claude Code:**

```bash
claude mcp add --transport http hudy https://www.hudy.co.kr/api/mcp -H "x-api-key: YOUR_API_KEY"
```

**Claude Desktop / Cursor:**

```json
{
  "mcpServers": {
    "hudy": {
      "url": "https://www.hudy.co.kr/api/mcp",
      "headers": {
        "x-api-key": "YOUR_API_KEY"
      }
    }
  }
}
```

---

## Available Tools

### `get_holidays` (Free)

Query Korean public holidays by year or date range.

```text
"2026년 공휴일 알려줘"
"2026-03-01부터 2026-06-30까지 공휴일 조회해줘"
```

### `count_business_days` (Pro)

Count business days between two dates, excluding weekends and public holidays.

```text
"2026-03-01부터 2026-03-31까지 영업일 며칠이야?"
"이번 달 영업일 수 알려줘"
```

### `add_business_days` (Pro)

Calculate the date N business days after a given date.

```text
"2026-03-01에서 10영업일 후 날짜 알려줘"
"오늘부터 5영업일 뒤는 언제야?"
```

### `subtract_business_days` (Pro)

Calculate the date N business days before a given date.

```text
"2026-03-31에서 5영업일 전 날짜 알려줘"
```

### `check_business_day` (Pro)

Check if a specific date is a business day.

```text
"2026-03-01이 영업일이야?"
"오늘 영업일인지 확인해줘"
```

### Custom Holiday Management (Pro)

Manage user-defined holidays that are included in all business day calculations.

| Tool | Description |
| --- | --- |
| `list_custom_holidays` | List all custom holidays |
| `create_custom_holiday` | Register a new custom holiday |
| `update_custom_holiday` | Update an existing custom holiday |
| `delete_custom_holiday` | Delete a custom holiday |

```text
"회사 창립기념일 2026-05-15로 등록해줘"
"커스텀 공휴일 목록 보여줘"
```

---

## Plans

| Feature | Free | Pro ($3/mo) |
| --- | :---: | :---: |
| Public holiday lookup | ✅ | ✅ |
| Monthly API calls | 100 | 5,000 |
| Business day APIs | ❌ | ✅ |
| Custom holidays | ❌ | ✅ |
| Calendar sync (iCal) | ❌ | ✅ |

---

## Notes

- All dates use `YYYY-MM-DD` format.
- Holiday data is sourced from the Korean government open data portal (data.go.kr).
- Custom holidays are per-user and automatically included in business day calculations.
- Calendar sync provides an iCal URL for Google Calendar, Apple Calendar, and Outlook.
