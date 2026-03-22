---
name: open
description: Open the frontend in the default browser using the configured port
---

# Open Frontend

Open the frontend URL in the default browser using the port configured in `.env` (VITE_PORT) or the default port 5173.

## Procedure

```bash
# Source .env to get port config
set -a && source .env 2>/dev/null && set +a
VITE_PORT=${VITE_PORT:-5173}

# Open in default browser (macOS)
open "http://localhost:$VITE_PORT"

echo "Opened http://localhost:$VITE_PORT"
```

That's it - just run the command and report the URL that was opened.
