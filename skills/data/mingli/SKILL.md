---
name: mingli
description: "Mingli (命理) — Multi-system daily horoscope: Western astrology (natal chart + transits), Ba-Zi / Four Pillars (Bát Tự), numerology, I Ching (Kinh Dịch). Kerykeion + astronomyapi.com. Telegram delivery."
version: 2.0.0
---

# Mingli 命理

Multi-system divination skill: Western astrology (Placidus houses, precise aspects), Ba-Zi / Four Pillars (Ngu Hanh), numerology (LifePath + personal cycles), and I Ching (hexagram + SPARK). Delivered daily via Telegram cron or on-demand.

## Modes

| Mode | Description | Trigger |
|------|-------------|---------|
| **Setup** | Register birth data, compute all charts | "set up my horoscope" |
| **Daily** | Automated 4-system horoscope via cron | Cron schedule |
| **On-demand** | Instant horoscope | "my horoscope", "horoscope now" |
| **I Ching** | Hexagram reading (random or manual) | "cast I Ching", "throw hexagram" |
| **Manage** | Pause/resume/change time | "pause horoscope", "change horoscope time" |

## Scripts

```bash
# Western natal chart (kerykeion — houses, aspects, nodes)
.claude/skills/.venv/bin/python3 .claude/skills/mingli/scripts/calculate-western-natal-chart-using-kerykeion.py \
  --date 2000-03-25 --time 12:00 --tz "Asia/Saigon" --lat 21.0245 --lon 105.84117 --name "User"

# Ba-Zi Four Pillars + Western zodiac
.claude/skills/.venv/bin/python3 .claude/skills/mingli/scripts/calculate-bazi.py \
  --date 1990-05-15 --time 14:30 --tz "Asia/Saigon"

# Planetary positions (astronomyapi.com fallback for transit data)
.claude/skills/.venv/bin/python3 .claude/skills/mingli/scripts/fetch-planetary-positions.py \
  --lat 10.8231 --lon 106.6297

# Numerology — LifePath, Birthday, Attitude, Challenges, Pinnacles, Personal cycles
.claude/skills/.venv/bin/python3 .claude/skills/mingli/scripts/calculate-numerology.py \
  --date 2000-03-25

# I Ching hexagram casting
.claude/skills/.venv/bin/python3 .claude/skills/mingli/scripts/cast-i-ching-hexagram.py --mode random
.claude/skills/.venv/bin/python3 .claude/skills/mingli/scripts/cast-i-ching-hexagram.py \
  --mode manual --upper Kan --lower Kun --moving 2,1
```

## Setup Mode

1. Ask for: **birth date** (YYYY-MM-DD), **birth time** (HH:MM), **birth city** (lat/lon + timezone)
2. Ask for: **Telegram chat ID**, **preferred delivery time** + **timezone**
3. Run all calculation scripts: natal chart, Ba-Zi, numerology
4. Write results to `~/clawd/memory/horoscope-users.md` (include lat/lon, LifePath number)
5. Create daily cron job
6. Confirm: Western sign + ASC + Ba-Zi Day Master + LifePath + delivery schedule

## Daily Mode

Cron triggers 4 scripts → all JSON fed to LLM → compose multi-system horoscope → Telegram.

See `references/horoscope-prompt-template.md` for full agentTurn message.

## On-Demand Mode

Trigger: "my horoscope", "horoscope now", "what's my horoscope today"

Same flow, inline (not isolated session). Includes daily I Ching hexagram.

## I Ching Mode

Trigger: "cast I Ching", "throw hexagram", "que Kinh Dich"

- **Random cast:** 3-coin method, cryptographic randomness
- **Manual input:** User provides upper/lower trigrams + moving lines
- Output: primary hexagram, moving lines, transformed hexagram, SPARK summary

## Management Commands

| Command | Action |
|---------|--------|
| "pause horoscope" | Disable cron job |
| "resume horoscope" | Enable cron job |
| "change horoscope time to 7am" | Update cron schedule |
| "remove horoscope" | Delete cron job + memory entry |

## Cron Delivery

One cron job per user: `horoscope-daily-{username}`

```json
{
  "name": "horoscope-daily-{username}",
  "enabled": true,
  "schedule": { "kind": "cron", "expr": "0 {hour} * * *", "tz": "{timezone}" },
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "[prompt from references/horoscope-prompt-template.md]",
    "model": "claude-sonnet-4-20250514",
    "timeoutSeconds": 180,
    "deliver": true,
    "channel": "telegram",
    "to": "{telegram_chat_id}"
  },
  "isolation": { "postToMainPrefix": "Horoscope delivered", "postToMainMode": "summary" }
}
```

## State Tracking

File: `state/users.json` — maps usernames to cron job IDs.

## Error Handling

- **kerykeion fails:** Fallback to `fetch-planetary-positions.py` (API-based, no houses)
- **API down:** LLM generates horoscope from zodiac knowledge only
- **Memory missing:** Prompt user to run setup first
- **I Ching data missing:** Generate hexagram from embedded trigram math only

## References

- `references/astronomyapi-reference.md` - API auth + endpoints
- `references/zodiac-reference.md` - Western + Chinese zodiac tables, stems, branches
- `references/horoscope-prompt-template.md` - LLM prompt for daily generation
- `references/i-ching-64-hexagrams.json` - 64 hexagrams with Chinese/Vietnamese names

## Dependencies

- **kerykeion** (pip) — natal chart, houses, aspects. Install: `pip install kerykeion`
- **astronomyapi.com** — env: `ASTRONOMY_APP_ID`, `ASTRONOMY_APP_SECRET`
- All other scripts: Python stdlib only
