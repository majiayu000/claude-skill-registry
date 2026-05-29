---
name: ops-streamdeck
description: >
  Stream Deck control skill for agents. Provides ability to restart streamdeck
  daemons, execute button tasks, query status, and manage Stream Deck
  hardware through a persistent daemon interface. Works with the streamdeck
  Python package for CLI operations and agent-driven automation.
allowed-tools: Bash, Read
triggers:
  - restart streamdeck
  - streamdeck button
  - execute streamdeck task
  - streamdeck status
  - streamdeck daemon
  - start streamdeck
  - stop streamdeck
metadata:
  short-description: Stream Deck daemon control and automation
---

# Stream Deck Skill

Agent-accessible interface for Stream Deck control. Provides persistent daemon
management, button task execution, and status querying capabilities.

## Architecture

The streamdeck project has two components:

1. **CLI Tool** (`streamdeck` command) - Manual operations by users
2. **Daemon** (this skill) - Persistent service for agent automation

```
┌─────────────────────────────────────────────────────────────────────┐
│                    AGENT / AUTOMATION                          │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐     │
│  │  Stream Deck Skill (this skill)               │     │
│  │  • Restart daemon                              │     │
│  │  • Execute button tasks                        │◄──►│
│  │  • Query status                                 │     │
│  └────────────────────────────────────────────────────────┘     │
│                          │                                   │
│                          ▼                                   │
│  ┌────────────────────────────────────────────────────────┐     │
│  │  Stream Deck Daemon (persistent service)        │     │
│  │  • Manages Stream Deck hardware               │     │
│  │  • Executes button press events                 │     │
│  │  • Provides status API                         │     │
│  └────────────────────────────────────────────────────────┘     │
│                          │                                   │
│                          ▼                                   │
│  ┌────────────────────────────────────────────────────────┐     │
│  │  Stream Deck CLI (manual operations)        │     │
│  │  • User-invoked commands                     │     │
│  │  • Video chat, lights, monitoring, etc.      │     │
│  └────────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────────┘
```

## Quick Start

### 1. Start the Daemon

```bash
# Start the streamdeck daemon in the background
./run.sh daemon start

# Or start in foreground for debugging
./run.sh daemon start --foreground
```

### 2. Use Agent Commands

```bash
# Restart the daemon
./run.sh restart

# Execute a button task
./run.sh button <button_id> [args...]

# Query daemon status
./run.sh status

# List available buttons
./run.sh list-buttons

# Get daemon logs
./run.sh logs
```

## Commands

### Daemon Management

| Command | Description |
|----------|-------------|
| `daemon start` | Start the streamdeck daemon (background) |
| `daemon start --foreground` | Start daemon in foreground (for debugging) |
| `daemon stop` | Stop the streamdeck daemon |
| `daemon restart` | Restart the streamdeck daemon |
| `daemon status` | Check if daemon is running |
| `daemon logs` | View daemon logs |

### Button Operations

| Command | Description |
|----------|-------------|
| `button <id>` | Execute button press event |
| `button <id> --hold` | Execute button long-press event |
| `list-buttons` | List all available button IDs |
| `button-info <id>` | Get information about a button |

### Status Queries

| Command | Description |
|----------|-------------|
| `status` | Get overall daemon status |
| `status --json` | Get status in JSON format |
| `status --buttons` | Get button states |

### Configuration

| Command | Description |
|----------|-------------|
| `config` | Show current configuration |
| `config --set <key> <value>` | Set configuration value |
| `config --get <key>` | Get configuration value |

## Configuration

The daemon reads configuration from:

1. **Environment Variables:**
   - `STREAMDECK_DAEMON_PORT` - Port for daemon API (default: 48970)
   - `STREAMDECK_DAEMON_HOST` - Host for daemon API (default: 127.0.0.1)
   - `STREAMDECK_LOG_LEVEL` - Log level (DEBUG, INFO, WARNING, ERROR)

2. **Config File:** `~/.streamdeck/daemon.json`

### Example Config

```json
{
  "daemon": {
    "port": 48970,
    "host": "127.0.0.1",
    "log_level": "INFO"
  },
  "buttons": {
    "0": {
      "name": "Video Chat Start",
      "command": "streamdeck videochat start"
    },
    "1": {
      "name": "Video Chat Stop",
      "command": "streamdeck videochat stop"
    },
    "2": {
      "name": "Lights Toggle",
      "command": "streamdeck lights toggle"
    },
    "3": {
      "name": "Time Tracker Toggle",
      "command": "streamdeck time-tracker toggle"
    }
  }
}
```

## Integration with Stream Deck CLI

The daemon works alongside the existing streamdeck CLI:

- **CLI** - Used for manual operations by humans
- **Daemon** - Used for automated operations by agents
- Both** share the same configuration and codebase

This dual approach ensures:
- ✅ Human users can continue using familiar CLI commands
- ✅ Agents have reliable daemon for automation
- ✅ No breaking changes to existing functionality
- ✅ Consistent behavior across both interfaces

## API Endpoints

The daemon exposes a simple HTTP API:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `GET /status` | GET | Get daemon status |
| `GET /buttons` | GET | List all buttons |
| `GET /buttons/{id}` | GET | Get button info |
| `POST /buttons/{id}` | POST | Execute button press |
| `POST /buttons/{id}/hold` | POST | Execute button long-press |
| `POST /restart` | POST | Restart daemon |
| `POST /stop` | POST | Stop daemon |

### Example API Usage

```bash
# Get status
curl http://127.0.0.1:48970/status

# Execute button
curl -X POST http://127.0.0.1:48970/buttons/0

# Get button info
curl http://127.0.0.1:48970/buttons/0
```

## Troubleshooting

### Daemon Won't Start

```bash
# Check if port is already in use
lsof -i :48970

# Check logs for errors
./run.sh logs

# Try starting in foreground to see errors
./run.sh daemon start --foreground
```

### Button Not Executing

```bash
# Check button configuration
./run.sh button-info <id>

# Verify daemon is running
./run.sh status

# Check logs for errors
./run.sh logs
```

### Permission Issues

The daemon requires access to:
- Stream Deck hardware (USB device access)
- Configuration directory (`~/.streamdeck/`)
- Network port (48970) for API

On Linux, ensure user has proper permissions:
```bash
# Add user to dialout group (for serial port access)
sudo usermod -a -G dialout $USER

# Ensure ~/.streamdeck is writable
chmod 755 ~/.streamdeck
```

## Development

### Running Tests

```bash
# Run daemon tests
./sanity.sh

# Run with verbose output
./sanity.sh --verbose
```

### Adding New Features

To add new button commands:

1. Add button configuration to `~/.streamdeck/daemon.json`
2. Implement command handler in daemon code
3. Test with: `./run.sh button <id>`

## Data Storage

- **Config:** `~/.streamdeck/daemon.json` - Button configurations and daemon settings
- **Logs:** `~/.streamdeck/daemon.log` - Daemon activity logs
- **State:** `~/.streamdeck/daemon.state` - Current button states (runtime only)

## Dependencies

- Python 3.8+
- Stream Deck Python SDK (`streamdeck`)
- FastAPI (for daemon API)
- Uvicorn (for daemon server)
- Pydantic (for API models)

Install dependencies:
```bash
# Via uvx (recommended)
uvx --from "git+https://github.com/grahama1970/streamdeck.git" streamdeck-daemon

# Or manually
pip install streamdeck fastapi uvicorn pydantic
```

## License

MIT License - See LICENSE file for details.
