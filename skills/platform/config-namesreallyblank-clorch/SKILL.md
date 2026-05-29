---
name: config
description: Manage Clorch configuration (Braintrust, API keys, features)
---

# Config - Configuration Management

Manage Clorch optional features and API keys.

## Usage

```bash
/config                    # Show configuration menu
/config braintrust         # Braintrust settings
/config braintrust on      # Enable Braintrust tracing
/config braintrust off     # Disable Braintrust tracing
/config braintrust status  # Check Braintrust status
```

## Braintrust Configuration

### Check Status

```bash
# Check current Braintrust configuration
grep -E "BRAINTRUST|TRACE_TO" ~/.claude/.env 2>/dev/null || echo "Not configured"
```

### Enable Braintrust

If API key exists:
```bash
# Update .env to enable
sed -i '' 's/TRACE_TO_BRAINTRUST=false/TRACE_TO_BRAINTRUST=true/' ~/.claude/.env 2>/dev/null || \
  echo "TRACE_TO_BRAINTRUST=true" >> ~/.claude/.env
echo "Braintrust tracing enabled. Restart Claude Code to apply."
```

If no API key, prompt user:
```yaml
question: "Braintrust API key not found. How would you like to proceed?"
header: "Setup"
options:
  - label: "Enter API key now"
    description: "I have a Braintrust API key ready"
  - label: "Get an API key first"
    description: "Open braintrust.dev to sign up (free tier available)"
  - label: "Skip for now"
    description: "I'll set it up later"
```

### Disable Braintrust

```bash
# Update .env to disable
sed -i '' 's/TRACE_TO_BRAINTRUST=true/TRACE_TO_BRAINTRUST=false/' ~/.claude/.env
echo "Braintrust tracing disabled. Restart Claude Code to apply."
```

## Interactive Menu

When user runs just `/config`:

```yaml
question: "What would you like to configure?"
header: "Config"
options:
  - label: "Braintrust (observability)"
    description: "Token tracking, cost analysis, session debugging"
  - label: "API Keys"
    description: "Perplexity, Nia, and other service keys"
  - label: "Show current config"
    description: "Display all configuration values"
```

### Braintrust Submenu

```yaml
question: "Braintrust configuration:"
header: "Braintrust"
options:
  - label: "Enable tracing"
    description: "Turn on session tracking"
  - label: "Disable tracing"
    description: "Turn off (keeps API key)"
  - label: "Update API key"
    description: "Change or add API key"
  - label: "View status"
    description: "Show current Braintrust config"
```

## Benefits Display

When explaining Braintrust:

```
## What is Braintrust?

Braintrust is an LLM observability platform.

### Benefits:
- Token tracking: See exactly how many tokens each task uses
- Cost analysis: Track API costs across sessions
- Performance debugging: Identify slow agents
- Session replay: Review what happened in past sessions

### Data sent:
- Session metadata (timestamps, agent IDs)
- Token usage per request
- Tool calls and durations
- Conversation context (first 100 chars)

### Privacy:
- Your Braintrust account, your data
- API key stays local in ~/.claude/.env
- Disable anytime: /config braintrust off

Get a free API key: https://braintrust.dev
```

## Implementation

### Parse Command

```python
args = user_input.split()
# /config -> show menu
# /config braintrust -> braintrust menu
# /config braintrust on -> enable
# /config braintrust off -> disable
# /config braintrust status -> show status
```

### Toggle Function

```bash
toggle_braintrust() {
    local action=$1
    local env_file="$HOME/.claude/.env"

    case $action in
        on)
            if grep -q "BRAINTRUST_API_KEY=" "$env_file" 2>/dev/null; then
                sed -i '' 's/TRACE_TO_BRAINTRUST=false/TRACE_TO_BRAINTRUST=true/' "$env_file"
                echo "Enabled. Restart Claude Code to apply."
            else
                echo "No API key found. Run /config braintrust to set up."
            fi
            ;;
        off)
            sed -i '' 's/TRACE_TO_BRAINTRUST=true/TRACE_TO_BRAINTRUST=false/' "$env_file"
            echo "Disabled. Restart Claude Code to apply."
            ;;
        status)
            if grep -q "TRACE_TO_BRAINTRUST=true" "$env_file" 2>/dev/null; then
                echo "Braintrust: ENABLED"
            else
                echo "Braintrust: DISABLED"
            fi
            grep "BRAINTRUST_API_KEY=" "$env_file" 2>/dev/null | sed 's/=.*/=***/' || echo "API Key: Not set"
            ;;
    esac
}
```

## Quick Reference

| Command | Action |
|---------|--------|
| `/config` | Interactive config menu |
| `/config braintrust` | Braintrust setup wizard |
| `/config braintrust on` | Enable tracing |
| `/config braintrust off` | Disable tracing |
| `/config braintrust status` | Show status |
