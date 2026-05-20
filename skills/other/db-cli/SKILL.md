---
name: db-cli
description: Search Deutsche Bahn train connections. Use for finding train routes, schedules, and travel times in Germany.
---

# Usage

```bash
# Basic search (uses current time)
db-cli "Berlin Hbf" "München Hbf"

# Search with specific departure time
db-cli -d "2025-01-15T14:30" "Frankfurt" "Hamburg"

# Search with arrival time
db-cli -a "2025-01-15T18:00" "Köln" "Stuttgart"
```

# Output Format

Results show connections with:

- Departure/arrival times
- Duration
- Number of transfers
- Train types (ICE, IC, RE, etc.)
- Platform information

See [README.md](../../db-cli/README.md) for full documentation.
