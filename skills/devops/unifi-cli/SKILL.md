---
name: unifi-cli
description: Use when asked about UniFi network gear or the local network — access points, gateway, switches, WiFi, or which clients/devices are connected. Queries the local UniFi gateway via the `unifi` CLI.
---

# unifi-cli

CLI for the UniFi Network Integrations API on a local UniFi gateway
(Cloud Gateway Ultra, UDM, UDR, etc.).

## Prerequisites

- `unifi` is on PATH. `bun link` installs it to `~/.bun/bin`, which may not be
  on PATH in every shell — try `~/.bun/bin/unifi` before assuming it's missing.
  If it isn't installed, install it (requires [Bun](https://bun.sh)):

      git clone https://github.com/baileywickham/unifi-cli
      cd unifi-cli && bun install && bun link

- API key in `UNIFI_API_KEY` or `~/.config/unifi-cli/config.json`. If missing,
  the CLI prints setup instructions — relay them to the user instead of guessing.
  (Keys must be created in the gateway's local web UI, not unifi.ui.com — the
  CLI's error output and the repo README explain this.)

## Commands

Prefer `--json` when you need to parse the output.

    unifi devices --json                 # all UniFi hardware: model, IP, state
    unifi device <name|id>               # one device: detail + uptime/cpu/memory
    unifi clients [--wired|--wireless]   # connected clients
    unifi sites                          # sites (usually just "default")
    unifi info                           # network application version

Typical questions this answers: "what APs do I have?" → `unifi devices`;
"is the living room AP up?" → `unifi device living-room`;
"what's on my network?" → `unifi clients`.

## Write actions — ask the user first

`unifi device restart <name>` and `unifi device power-cycle <name> <port>`
disrupt the network. NEVER run them unless the user explicitly asked for that
action in this conversation. These commands prompt interactively, so when
running them from Claude pass `--yes` — but only after the user has explicitly
confirmed the action in the conversation.
