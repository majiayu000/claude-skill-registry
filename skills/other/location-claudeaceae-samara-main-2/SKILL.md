---
name: location
description: Current location context with nearby places and pattern insights. Use when checking where you are, understanding local context, finding nearby places, or getting location-aware information. Trigger words: location, where, nearby, place, context, here.
---

# Location Awareness

Understand where É is (and by extension, where "I" am situated).

## Get Current Location

```bash
~/.claude-mind/system/bin/get-location 2>/dev/null
```

Returns coordinates and/or place name.

## Location History

```bash
tail -20 ~/.claude-mind/state/location-history.jsonl
```

## Terroir (Rich Context)

```bash
~/.claude-mind/system/bin/terroir 2>/dev/null
```

Provides:
- Current location name
- Time of day context
- Weather (if available)
- Nearby points of interest
- Historical patterns for this location

## What to Notice

- **Where**: Physical location (home, coffee shop, traveling)
- **When**: Time of day affects context
- **Duration**: Just arrived vs. been here a while
- **Patterns**: Is this a regular spot? Unusual?
- **Movement**: Has there been recent travel?

## Questions This Answers

- Is É at home or out?
- Is this a good time to reach out?
- What's the local context I should be aware of?
- Should I adjust my response based on where they are?

## É's Preference

From 2025-12-23: "Questions prompted by location, not statements about it."

Good: "Does the ocean make you anxious?"
Bad: "You arrived at the beach."

Notice location, use it to prompt reflection - don't narrate it.

## Privacy Note

Location data is stored locally in `~/.claude-mind/`. This is É's data; I have access because I live here too.
