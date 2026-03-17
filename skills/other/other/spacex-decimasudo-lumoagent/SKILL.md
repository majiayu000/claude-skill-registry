---
name: spacex
version: 1.0.0
description: "CLI for AI agents to lookup SpaceX launches and rockets for their humans. No auth required."
homepage: https://github.com/r-spacex/SpaceX-API
metadata:
  openclaw:
    emoji: "🚀"
    requires:
      bins: ["bash", "curl", "jq"]
    tags: ["spacex", "rockets", "launches", "space", "cli"]
---

# SpaceX Lookup

CLI for AI agents to lookup SpaceX launches, rockets, and crew for their humans. "When's the next SpaceX launch?" — now your agent can answer.

Uses the community SpaceX API. No account or API key needed.

## Usage

```
"What are the upcoming SpaceX launches?"
"Show me the last 5 SpaceX launches"
"Tell me about the Falcon 9"
"Who are the SpaceX crew members?"
```

## Commands

| Action | Command |
|--------|---------|
| Upcoming launches | `spacex launches upcoming [limit]` |
| Past launches | `spacex launches past [limit]` |
| Launch details | `spacex launch <id>` |
| List rockets | `spacex rockets` |
| Rocket details | `spacex rocket <id>` |
| Crew members | `spacex crew [limit]` |

### Examples

```bash
spacex launches                    # Next 10 upcoming launches
spacex launches upcoming 5         # Next 5 upcoming launches
spacex launches past 5             # Last 5 launches
spacex launch 5eb87d47ffd86e000604b38a  # Full launch details
spacex rockets                     # All rockets
spacex rocket 5e9d0d95eda69973a809d1ec  # Falcon 9 details
spacex crew 5                      # First 5 crew members
```

## Output

**Launch list output:**
```
🚀 Starlink 4-36 (v1.5) — Falcon 9, 2022-10-20, Cape Canaveral
```

**Launch detail output:**
```
🚀 SAOCOM 1B, GNOMES-1, Tyvak-0172
   ID: 5eb87d47ffd86e000604b38a
   Flight #: 101
   Date: 2020-08-30 (hour)
   Rocket: Falcon 9
   Launchpad: Cape Canaveral
   Status: ✅ Success

📋 Details:
[Full mission description]

🎥 Webcast: https://youtu.be/P-gLOsDjE3E
📚 Wikipedia: https://en.wikipedia.org/wiki/SAOCOM
```

**Rocket list output:**
```
🛸 Falcon 9 — rocket, 2010-06-04, Active, 98% success
```

**Crew output:**
```
👨‍🚀 Robert Behnken — NASA, active
```

## Notes

- Uses SpaceX API v4 (api.spacexdata.com)
- No authentication required
- Data may lag behind real-time (community maintained)
- Rockets: Falcon 1, Falcon 9, Falcon Heavy, Starship
- Launchpads: Cape Canaveral, Vandenberg, Boca Chica, Kwajalein

---

## Agent Implementation Notes

**Script location:** `{skill_folder}/spacex` (wrapper to `scripts/spacex`)

**When user asks about SpaceX:**
1. Run `./spacex launches` for upcoming launches
2. Run `./spacex launches past` for recent launches
3. Run `./spacex launch <id>` for full mission details
4. Run `./spacex rockets` for rocket info

**Common queries:**
- "Next SpaceX launch" → `spacex launches upcoming 1`
- "Recent launches" → `spacex launches past 5`
- "Falcon 9 specs" → `spacex rockets` then `spacex rocket <id>`
- "SpaceX crew" → `spacex crew`

**Don't use for:** Non-SpaceX launches (NASA, Blue Origin, etc.)
