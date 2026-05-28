---
name: test-twilio
description: Place Twilio test calls. Use when user invokes /test-twilio.
---

# test-twilio Skill

Place test calls via Twilio to verify call placement works.

## Prerequisites

- Docker compose services running locally

## Known Numbers

| Name | Number |
|------|--------|
| daniel | +5542984348739 |
| wren-dev-daniel | +16505026335 |

**From number:** +19736624281

## Usage

### With shortcut (no prompts)

- `/test-twilio call daniel` - 1 min call to Daniel
- `/test-twilio call wren-dev-daniel` - 1 min call to wren-dev-daniel

### Without shortcut

`/test-twilio` - asks for from and to numbers

## Command

```bash
docker compose exec api python src/scripts/twilio_place_call.py \
  --from "+19736624281" \
  --to "<NUMBER>" \
  --duration-minutes 1 \
  --audio neutral
```

## Options

| Option | Description | Default |
|--------|-------------|---------|
| --duration-minutes | Call duration | 1 |
| --audio | neutral, fight, healthyfight | neutral |

## Troubleshooting

**Call doesn't connect:**
- Check Docker: `docker compose ps`
- Verify Twilio credentials in .env
