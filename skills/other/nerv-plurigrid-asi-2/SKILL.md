---
name: nerv
description: 'NERV - Rapid LocalSend Test with Voice'
version: 1.0.0
---

# NERV - Rapid LocalSend Test with Voice

Rapid peer discovery and LocalSend connectivity testing with Italian voice announcements.

## State Machine

```
VOID → SEEKING → FOUND → READY
```

## Commands

```bash
# Full test with voice announcements
bb nerv.bb test

# Silent peer discovery
bb nerv.bb seek

# Just announce status
bb nerv.bb announce
```

## Features

- **Tailscale Integration**: Discovers online peers via Tailscale status
- **LocalSend Check**: Tests port 53317 connectivity
- **Voice Announcements**: Emma (Premium) at rate 180 for energetic Italian phrases
- **State Machine**: Tracks discovery progress

## Voice Phrases

- "NERV inizializzazione!" - startup
- "Cercando peers nella rete!" - seeking
- "Trovati N peers!" - found count
- "Peer X online!" - each peer
- "X pronto per trasporto!" - LocalSend ready
- "NERV online! Trasporto topologico pronto!" - final ready

## Dependencies

- Babashka
- Tailscale.app
- macOS `say` command
