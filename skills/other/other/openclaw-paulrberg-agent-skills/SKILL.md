---
disable-model-invocation: false
name: openclaw
user-invocable: false
description: This skill should be used when the user mentions "openclaw", "OpenClaw CLI", asks to "send a message via openclaw", "manage openclaw agents", "configure openclaw gateway", "check openclaw status", "run openclaw agent", or asks about OpenClaw setup, channels, devices, or messaging automation.
---

# OpenClaw CLI

## Overview

OpenClaw is a multi-channel messaging and agent platform. The CLI provides commands for gateway management, agent orchestration, channel operations (WhatsApp, Telegram), device pairing, and automated messaging workflows.

## Quick Reference

```bash
# Check CLI version and help
openclaw --version
openclaw --help

# Setup and configuration
openclaw setup          # Initialize config and workspace
openclaw onboard        # Interactive setup wizard
openclaw configure      # Set credentials and defaults
openclaw doctor         # Health checks and diagnostics

# Gateway operations
openclaw gateway        # Start the WebSocket gateway
openclaw gateway --port 18789  # Custom port
openclaw --dev gateway  # Dev mode (isolated state, port 19001)
openclaw health         # Check gateway health
openclaw status         # Channel health and sessions

# Agent operations
openclaw agent --to +15555550123 --message "Hello"
openclaw agents         # Manage agent workspaces

# Messaging
openclaw message send --target +15555550123 --message "Hi"
openclaw message send --channel telegram --target @mychat --message "Hi"

# Channel management
openclaw channels login --verbose  # Link WhatsApp/Telegram
openclaw channels       # Manage channels

# Device and session management
openclaw devices        # Device pairing and tokens
openclaw sessions       # List conversation sessions
```

## Common Workflows

### Initial Setup

```bash
openclaw setup
openclaw onboard
openclaw channels login --verbose
```

### Start Gateway and Send Message

```bash
openclaw gateway &
openclaw message send --target +15555550123 --message "Test"
```

### Run Agent Turn

```bash
openclaw agent --to +15555550123 --message "Run summary" --deliver
```

## Profile Isolation

Use `--dev` or `--profile <name>` to isolate state:

```bash
openclaw --dev gateway           # Uses ~/.openclaw-dev
openclaw --profile test gateway  # Uses ~/.openclaw-test
```

## Documentation

Run `openclaw --help` for the latest available commands and options.

Full documentation: https://docs.openclaw.ai/cli
